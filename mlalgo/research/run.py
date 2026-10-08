"""Run every entry setup on every stock and simulate every exit plan on every signal."""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from mlalgo.market import index_regime, rates_regime
from mlalgo.research import engine
from mlalgo.research.entries import all_signals, bars
from mlalgo.structure import ML_FEATURES, setup_score, structure_features

EXIT_NAMES = list(engine.EXITS)
EXIT_CODES = np.array([engine.EXITS[k][0] for k in EXIT_NAMES], dtype=np.int64)
GROUP_COLS = ["industry_rs", "industry_rank", "sector_rs"]
SIGNAL_EXTRAS = ["risk_pct", "risk_adr", "vol_ratio", "gap", "close_strength",
                 "prior_move", "flag_depth", "flag_days", "base_depth", "contraction"]
MARKET_COLS = ["mkt_ok", "mkt_ema_stack", "mkt_ret_21", "mkt_above200", "qqq_ok", "qqq_ret_21",
               "rates_rising", "breadth_50"]


def _rs_composite(df: pd.DataFrame) -> pd.Series:
    c = df["close"]
    return 0.4 * (c / c.shift(63) - 1) + 0.3 * (c / c.shift(126) - 1) + 0.3 * (c / c.shift(252) - 1)


def group_strength(rank: pd.DataFrame, groups: pd.Series, min_members: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Median RS rank of each group (sector / sub-industry) per day, and the group's percentile
    among groups. Groups with fewer than `min_members` stocks trading that day are left NaN."""
    g = groups.reindex(rank.columns)
    med = rank.T.groupby(g).median().T
    cnt = rank.T.groupby(g).count().T
    med = med.where(cnt >= min_members)
    return med.astype("float32"), med.rank(axis=1, pct=True).astype("float32")


def cross_section(prices: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.Series]:
    """Relative-strength percentile rank of every stock on every day, and market breadth
    (share of stocks above their 50-day average)."""
    rs = pd.DataFrame({t: _rs_composite(df) for t, df in prices.items()}).astype("float32")
    rank = rs.rank(axis=1, pct=True).astype("float32")
    above = pd.DataFrame({t: (df["close"] > df["close"].rolling(50).mean()).astype("float32")
                          .where(df["close"].rolling(50).count() == 50) for t, df in prices.items()})
    breadth = above.mean(axis=1).rename("breadth_50")
    return rank, breadth


def market_frame(market: dict[str, pd.DataFrame], breadth: pd.Series) -> pd.DataFrame:
    parts = [breadth]
    if "SPY" in market:
        spy = market["SPY"]
        parts.append(index_regime(spy, "mkt"))
        parts.append((spy["close"] > spy["close"].rolling(200).mean()).astype(int).rename("mkt_above200"))
    if "QQQ" in market:
        parts.append(index_regime(market["QQQ"], "qqq")[["qqq_ok", "qqq_ret_21"]])
    if "^IRX" in market:
        parts.append(rates_regime(market["^IRX"]["close"]))
    m = pd.concat(parts, axis=1).sort_index().ffill()
    return m.reindex(columns=MARKET_COLS)


def process_ticker(args) -> pd.DataFrame | None:
    ticker, df, rs_rank, grp, max_days, cost, seed = args
    b = bars(df)
    sig = all_signals(df, b, seed=seed)
    if sig.empty:
        return None
    idx = sig["idx"].to_numpy()
    ret, rmult, xidx, reason = engine.simulate_all(
        b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["sma50"], b["ema8"], b["ema21"], b["ema50"],
        b["atr20"], b["low10prev"], idx, sig["entry"].to_numpy(), sig["stop"].to_numpy(), EXIT_CODES, max_days, cost)
    feats = structure_features(df).iloc[idx].reset_index(drop=True)
    feats["setup_score"] = setup_score(feats)
    out = pd.DataFrame({"ticker": ticker, "date": df.index[idx], "entry_name": sig["entry_name"].to_numpy(),
                        "entry": sig["entry"].to_numpy(), "stop": sig["stop"].to_numpy()})
    for col in SIGNAL_EXTRAS:
        out[col] = sig[col].to_numpy() if col in sig else np.nan
    out["rs_rank"] = rs_rank.reindex(df.index).to_numpy()[idx]
    for col in GROUP_COLS:
        out[col] = grp[col].reindex(df.index).to_numpy()[idx] if grp is not None and col in grp else np.nan
    out = pd.concat([out, feats[[c for c in ML_FEATURES + ["trend_template", "dollar_vol_50"] if c in feats]]], axis=1)
    dates = df.index.to_numpy()
    for j, name in enumerate(EXIT_NAMES):
        out[f"R_{name}"] = rmult[:, j].astype("float32")
        out[f"ret_{name}"] = ret[:, j].astype("float32")
        out[f"days_{name}"] = (xidx[:, j] - idx).astype("int16")
        out[f"exit_{name}"] = dates[xidx[:, j]]
        out[f"reason_{name}"] = reason[:, j].astype("int8")
        out.loc[xidx[:, j] == len(dates) - 1, f"reason_{name}"] = 0  # still open at data end
    return out


def run(prices: dict[str, pd.DataFrame], market: dict[str, pd.DataFrame], max_days: int = 250,
        cost: float = 0.001, workers: int | None = None, universe: pd.DataFrame | None = None) -> pd.DataFrame:
    rank, breadth = cross_section(prices)
    mkt = market_frame(market, breadth)
    grp = {}
    if universe is not None and "sub_industry" in universe:
        u = universe.set_index("ticker")
        ind_rs, ind_rank = group_strength(rank, u["sub_industry"].replace("nan", np.nan))
        sec_rs, _ = group_strength(rank, u["sector"].replace("nan", np.nan))
        for t in prices:
            if t in u.index:
                sub, sec = u.at[t, "sub_industry"], u.at[t, "sector"]
                grp[t] = pd.DataFrame({
                    "industry_rs": ind_rs[sub] if sub in ind_rs else np.nan,
                    "industry_rank": ind_rank[sub] if sub in ind_rank else np.nan,
                    "sector_rs": sec_rs[sec] if sec in sec_rs else np.nan}, index=rank.index)
    tasks = [(t, df, rank[t], grp.get(t), max_days, cost, i) for i, (t, df) in enumerate(prices.items())]
    workers = workers or os.cpu_count() or 1
    frames = []
    if workers > 1:
        with ProcessPoolExecutor(workers) as ex:
            for k, res in enumerate(ex.map(process_ticker, tasks, chunksize=10)):
                if res is not None:
                    frames.append(res)
                if (k + 1) % 200 == 0:
                    print(f"[run] {k + 1}/{len(tasks)} tickers")
    else:
        frames = [r for r in map(process_ticker, tasks) if r is not None]
    sig = pd.concat(frames, ignore_index=True)
    m = mkt.reindex(mkt.index.union(pd.DatetimeIndex(sig["date"].unique()))).ffill()
    sig = sig.join(m, on="date")
    float_cols = sig.select_dtypes("float64").columns
    sig[float_cols] = sig[float_cols].astype("float32")
    return sig.sort_values(["date", "ticker"]).reset_index(drop=True)
