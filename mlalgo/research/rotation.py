"""A concentrated leader portfolio run the way top swing traders run theirs (run 25).

Hold at most N (3-5) stocks, equal weight (1/N of equity each at entry), decided at each close:
- Leaders only (Minervini / O'Neil / Qullamaggie): price >= $10, >= $20M a day, close above a rising
  50-day which is above the 200-day, within 25% of the 52-week high; ranked by momentum.
- Entry: the best-ranked leader not held fills an empty slot; optionally only on the day of a setup
  (episodic pivot / breakout signal), and only while the market regime is on (QQQ above its 200-day).
- Exit (whichever comes first, at the close): a close below the trailing average (10 / 20 / 50-day:
  Qullamaggie's fast trails or the O'Neil/Minervini 50-day), a close 8% below the entry (their max
  stop), or, with the 'rank' rule, falling out of the top 3N. Delisted stocks are sold at the last price.
Costs 0.1% per side. Everything is computed from data known at that close.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SCORES = ("mom_6m1m", "mom_12_1", "qull_best")
EXITS = ("sma10", "sma20", "sma50", "sma50_rank")


def prepare(closes: pd.DataFrame, dollar_vol: pd.DataFrame, members: pd.DataFrame | None = None) -> dict:
    """Arrays (dates x tickers) shared by every configuration. `closes` must NOT be forward-filled
    (a missing price = not trading; a stock that stops trading is sold at its last price)."""
    c = closes.astype("float64")
    s = {w: c.rolling(w, min_periods=w).mean() for w in (10, 20, 50, 200)}
    hi = c.rolling(252, min_periods=200).max()
    r = {n: c / c.shift(n) - 1 for n in (21, 63, 126, 252)}
    scores = {
        "mom_6m1m": 0.7 * r[126] + 0.3 * r[21],                       # the course's momentum score
        "mom_12_1": c.shift(21) / c.shift(252) - 1,                    # academic 12-1 momentum
        "qull_best": pd.concat([r[n].rank(axis=1, pct=True) for n in (21, 63, 126)]).groupby(level=0).max(),
    }
    leader = ((c >= 10) & (dollar_vol.reindex_like(c) >= 20e6) & (c > s[50]) & (s[50] > s[200])
              & (s[50] > s[50].shift(10)) & (c >= 0.75 * hi))
    if members is not None:
        leader &= members.reindex(index=c.index, columns=c.columns).fillna(False).astype(bool)
    return {"dates": c.index, "tickers": c.columns, "c": c.to_numpy(), "sma": {w: v.to_numpy() for w, v in s.items()},
            "leader": leader.to_numpy(), "scores": {k: v.reindex(index=c.index, columns=c.columns).to_numpy() for k, v in scores.items()}}


def run(P: dict, n: int = 4, score: str = "mom_6m1m", exit_rule: str = "sma50", regime: np.ndarray | None = None,
        setup: np.ndarray | None = None, stop: float = 0.08, cost: float = 0.001, start: str = "2007-01-01",
        filt: np.ndarray | None = None) -> dict:
    """Simulate one configuration. `regime`: bool per date (True = new entries allowed). `setup`: bool
    dates x tickers (True = a setup fired that day); None = any leader may be bought."""
    dates, c, sc, lead = P["dates"], P["c"], P["scores"][score], P["leader"]
    if filt is not None:                       # run 26: e.g. fundamentals must confirm (sales / EPS growth)
        lead = lead & filt
    trail = P["sma"][{"sma10": 10, "sma20": 20, "sma50": 50, "sma50_rank": 50}[exit_rule]]
    t0 = int(np.searchsorted(dates.values, np.datetime64(pd.Timestamp(start))))
    cash, hold = 1.0, {}                       # ticker index -> [shares, entry price, entry t, last price, last t]
    eq, trades = np.full(len(dates), np.nan), []
    for t in range(t0, len(dates)):
        px = c[t]
        ok = lead[t] & ~np.isnan(sc[t])
        ranked = np.flatnonzero(ok)
        ranked = ranked[np.argsort(-sc[t, ranked])]
        top_set = set(ranked[:3 * n].tolist()) if exit_rule == "sma50_rank" else None
        # exits
        for j in list(hold):
            h = hold[j]
            p = px[j]
            if np.isnan(p):
                if t - h[4] > 5:               # stopped trading (delisted / acquired): sell at the last price
                    cash += h[0] * h[3] * (1 - cost)
                    trades.append((h[2], t, j, h[3] / h[1] - 1))
                    del hold[j]
                continue
            h[3], h[4] = p, t
            out = p < trail[t, j] or p <= h[1] * (1 - stop) or (top_set is not None and j not in top_set)
            if out:
                cash += h[0] * p * (1 - cost)
                trades.append((h[2], t, j, p / h[1] - 1))
                del hold[j]
        equity = cash + sum(h[0] * h[3] for h in hold.values())
        # entries
        if len(hold) < n and (regime is None or regime[t]):
            cand = ranked[setup[t, ranked]] if setup is not None else ranked
            cand = [j for j in cand[: n + len(hold)] if j not in hold]
            for j in cand:
                if len(hold) >= n:
                    break
                alloc = min(equity / n, cash)
                if alloc < equity * 0.05:
                    break
                hold[j] = [alloc * (1 - cost) / px[j], px[j], t, px[j], t]
                cash -= alloc
        eq[t] = cash + sum(h[0] * h[3] for h in hold.values())
    curve = pd.Series(eq, index=dates).dropna()
    tr = pd.DataFrame(trades, columns=["t_in", "t_out", "j", "ret"])
    tr["days"] = tr["t_out"] - tr["t_in"]
    tr["date_in"] = dates[tr["t_in"].to_numpy()] if len(tr) else pd.Series(dtype="datetime64[ns]")
    tr["date_out"] = dates[tr["t_out"].to_numpy()] if len(tr) else pd.Series(dtype="datetime64[ns]")
    tr["ticker"] = P["tickers"][tr["j"].to_numpy()] if len(tr) else pd.Series(dtype=object)
    open_pos = [{"ticker": P["tickers"][j], "entry_date": dates[h[2]], "entry": h[1], "last": h[3],
                 "gain": h[3] / h[1] - 1, "stop_8%": h[1] * (1 - stop), "trail_level": trail[len(dates) - 1, j]}
                for j, h in hold.items()]
    return {"curve": curve, "trades": tr, "open": pd.DataFrame(open_pos)}


def stats(res: dict, is_end: pd.Timestamp) -> dict:
    out = {}
    curve, tr = res["curve"], res["trades"]
    for name, m in (("IS", curve.index < is_end), ("OOS", curve.index >= is_end)):
        e = curve[m]
        if len(e) < 60:
            continue
        e = e / e.iloc[0]
        yrs = (e.index[-1] - e.index[0]).days / 365.25
        cagr, dd = e.iloc[-1] ** (1 / yrs) - 1, (e / e.cummax() - 1).min()
        t = tr[(tr["date_in"] < is_end) == (name == "IS")] if len(tr) else tr
        out.update({f"{name}_CAGR": cagr, f"{name}_maxDD": dd, f"{name}_CAGR_per_DD": cagr / abs(dd) if dd else np.nan,
                    f"{name}_trades": len(t), f"{name}_win": (t["ret"] > 0).mean() if len(t) else np.nan,
                    f"{name}_avg_days": t["days"].mean() if len(t) else np.nan})
    return out


def fund_daily(fund: pd.DataFrame, index: pd.DatetimeIndex, columns, metric: str, max_days: int = 140) -> pd.DataFrame:
    """dates x tickers value of a fundamental metric as known on each day (from the day after the filing),
    dropped once it is more than `max_days` trading days old."""
    f = fund.dropna(subset=["avail"]).sort_values(["avail", "end"]).drop_duplicates(["ticker", "avail"], keep="last")
    f = f.assign(avail=f["avail"].astype("datetime64[ns]"))
    w = f.pivot(index="avail", columns="ticker", values=metric)
    w = w.reindex(w.index.union(index)).ffill(limit=max_days * 2).reindex(index)
    age = f.assign(one=1.0).pivot(index="avail", columns="ticker", values="one")
    age = age.reindex(age.index.union(index)).reindex(index).notna()
    fresh = pd.DataFrame(np.where(age, 1.0, np.nan), index=index, columns=age.columns).ffill(limit=max_days).notna()
    return w.where(fresh).reindex(columns=columns)


def earnings_gap_mask(opens: pd.DataFrame, closes: pd.DataFrame, earn: pd.DataFrame, gap: float = 0.05,
                      lookback: int = 63) -> pd.DataFrame:
    """True where the stock gapped up >= `gap` on an earnings reaction day (the filing day or the next
    trading day) within the last `lookback` trading days: the market confirming the numbers."""
    idx = closes.index
    e = np.zeros(closes.shape, dtype=bool)
    if earn is not None and len(earn):
        pos = np.searchsorted(idx.values, earn["date"].astype("datetime64[ns]").values)
        ok = pos < len(idx)
        for k in (0, 1):
            p = np.minimum(pos[ok] + k, len(idx) - 1)
            cols = earn["ticker"].to_numpy()[ok]
            keep = np.isin(cols, closes.columns)
            e[p[keep], closes.columns.get_indexer(cols[keep])] = True
    g = (opens / closes.shift(1) - 1) >= gap
    return (g & e).astype(float).rolling(lookback, min_periods=1).max() > 0
