"""Run 28: sector momentum first, then the strongest S&P 500 stocks inside the leading sectors.

Broad sector ETFs are used only as indicators (we hold stocks, not ETFs); communication services and
real estate are folded into tech and financials (data.SECTOR_MERGE). 'members' momentum (equal-weight
index of a sector's point-in-time S&P 500 members) is kept as a fallback for missing ETF data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from mlalgo.research.data import SECTOR_ETF, SECTOR_MERGE


def assign_sectors(closes: pd.DataFrame, known: pd.Series, etfs: dict[str, pd.Series]) -> pd.Series:
    """ticker -> GICS sector. Former members have no sector on Wikipedia: give them the sector whose
    ETF their daily returns track most closely (shortcut: uses the whole history, not point-in-time)."""
    sec = known.replace(SECTOR_MERGE).reindex(closes.columns).where(lambda s: s.isin(list(SECTOR_ETF)))
    todo = sec.index[sec.isna()]
    if len(todo) and etfs:
        r = closes[todo].pct_change(fill_method=None)
        corr = pd.DataFrame({name: r.corrwith(etfs[SECTOR_ETF[name]].reindex(r.index).pct_change(fill_method=None))
                             for name in SECTOR_ETF if SECTOR_ETF[name] in etfs})
        sec.loc[todo] = corr.idxmax(axis=1).where(corr.notna().any(axis=1))
    return sec


def sector_returns(closes: pd.DataFrame, sector: pd.Series, members: pd.DataFrame | None,
                   etfs: dict[str, pd.Series], lookback: int, source: str = "etf") -> pd.DataFrame:
    """dates x sectors: `lookback`-day return of each sector, from its ETF ('etf', member index where
    the ETF is missing) or from the equal-weight index of its point-in-time members ('members')."""
    r = closes.pct_change(fill_method=None)
    if members is not None:
        r = r.where(members.reindex(index=r.index, columns=r.columns).fillna(False).astype(bool))
    idx = (1 + r.T.groupby(sector.reindex(r.columns)).mean().T.fillna(0)).cumprod()
    out = idx / idx.shift(lookback) - 1
    if source == "etf":
        for name, etf in SECTOR_ETF.items():
            if etf in etfs and name in out:
                e = etfs[etf].reindex(out.index)
                out[name] = (e / e.shift(lookback) - 1).fillna(out[name])
    return out.reindex(columns=[s for s in SECTOR_ETF if s in out])


def choose(sret: pd.DataFrame, k: int, absolute: bool, decide: np.ndarray | None = None,
           confirm: pd.DataFrame | None = None, ranks: tuple | None = None) -> pd.DataFrame:
    """dates x sectors bool: the top-k sectors by return, decided on `decide` days and held until the
    next one. `absolute`: a chosen sector must also be up over the lookback (else its slot is cash).
    `confirm`: dates x sectors bool a sector must pass to be ranked (e.g. earnings growing).
    `ranks` (run 29): keep exactly these sector ranks, e.g. (2,) = only the second strongest."""
    s = sret if confirm is None else sret.where(confirm.reindex_like(sret).fillna(False).astype(bool))
    rk = s.rank(axis=1, ascending=False, method="first")
    top = rk.isin(ranks) if ranks else rk <= k
    if absolute:
        top &= s > 0
    top = top & s.notna()
    if decide is not None:
        top = top.where(pd.Series(decide, index=top.index), np.nan).ffill().fillna(False).astype(bool)
    return top


def stock_mask(chosen: pd.DataFrame, sector: pd.Series, columns) -> np.ndarray:
    """dates x tickers bool: the stock's sector is chosen that day."""
    onehot = pd.get_dummies(sector.reindex(columns)).reindex(columns=chosen.columns, fill_value=False).astype(float)
    return (chosen.astype(float).to_numpy() @ onehot.to_numpy().T) > 0


def today_table(closes, sector, etfs, leader, score, eps_yoy, members=None) -> pd.DataFrame:
    """One row per sector at the last close: ETF returns over 1w / 1m / 3m / 6m, % of members above their
    50-day, median reported EPS growth (latest vs a quarter earlier), and the top 3 leaders by momentum."""
    last = closes.index[-1]
    sma50 = closes.rolling(50).mean().iloc[-1]
    mem = members.iloc[-1].reindex(closes.columns).fillna(False).astype(bool) if members is not None else \
        pd.Series(True, index=closes.columns)
    rows = []
    for name, etf in SECTOR_ETF.items():
        cols = sector.index[(sector == name) & mem.reindex(sector.index).fillna(False)]
        row = {"sector": name, "ETF": etf}
        if etf in etfs:
            e = etfs[etf].dropna()
            for lab, n in (("1w", 5), ("1m", 21), ("3m", 63), ("6m", 126)):
                row[lab] = e.iloc[-1] / e.iloc[-1 - n] - 1 if len(e) > n else np.nan
        c = closes[cols].iloc[-1]
        row["pct_above_50d"] = (c > sma50[cols]).mean() if len(cols) else np.nan
        if eps_yoy is not None:
            row["EPS_growth_now"] = eps_yoy[cols].iloc[-1].median() if len(cols) else np.nan
            row["EPS_growth_qtr_ago"] = eps_yoy[cols].iloc[-64].median() if len(cols) and len(eps_yoy) > 64 else np.nan
        sc = score.loc[last, cols][leader.loc[last, cols]].dropna().sort_values(ascending=False)
        row["top_leaders"] = ", ".join(sc.index[:3])
        rows.append(row)
    return pd.DataFrame(rows).sort_values("1m", ascending=False)


def top_in_sector(score: pd.DataFrame, pool: pd.DataFrame, sector: pd.Series, chosen: pd.DataFrame, n: int) -> np.ndarray:
    """dates x tickers bool (run 29): the n highest-scoring pool stocks inside each chosen sector."""
    ok = pool & pd.DataFrame(stock_mask(chosen, sector, score.columns), index=score.index, columns=score.columns)
    rk = score.where(ok).T.groupby(sector.reindex(score.columns)).rank(ascending=False, method="first").T
    return (rk <= n).reindex(columns=score.columns, fill_value=False).to_numpy()
