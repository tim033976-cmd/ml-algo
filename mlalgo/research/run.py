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
                 "prior_move", "flag_depth", "flag_days", "base_depth", "contraction",
                 "pattern_len", "pattern_width", "pattern_touches", "coil_range"]
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


SUPER_HORIZON, SUPER_GAIN, SAMPLE_EVERY = 63, 0.40, 10


def superperformer_sample(ticker, df, feats_all, rs_rank, grp, warmup=252) -> pd.DataFrame:
    """Every 10th trading day of every stock, with its chart state and whether it went on to
    gain >= 40% (intraday high) within the next 63 trading days: the 'superperformance' that
    O'Neil and Minervini studied by hand. The label uses future data by design; the features
    don't, and the walk-forward training only uses rows whose 63-day window has fully ended."""
    n = len(df)
    idx = np.arange(warmup, n, SAMPLE_EVERY)
    if len(idx) == 0:
        return pd.DataFrame()
    c, h = df["close"].to_numpy(float), df["high"].to_numpy(float)
    fwd_max = pd.Series(h).rolling(SUPER_HORIZON).max().shift(-SUPER_HORIZON).to_numpy()
    fwd_ret = pd.Series(c).shift(-SUPER_HORIZON).to_numpy() / c - 1
    out = feats_all.iloc[idx][[x for x in ML_FEATURES + ["dollar_vol_50"] if x in feats_all]].reset_index(drop=True)
    out.insert(0, "date", df.index[idx])
    out.insert(0, "ticker", ticker)
    out["rs_rank"] = rs_rank.reindex(df.index).to_numpy()[idx]
    for col in GROUP_COLS:
        out[col] = grp[col].reindex(df.index).to_numpy()[idx] if grp is not None and col in grp else np.nan
    out["fwd_max_gain"] = fwd_max[idx] / c[idx] - 1
    # "clean" superperformer: reaches +40% before it ever trades 20% below the starting close
    l = df["low"].to_numpy(float)
    first_up = np.full(len(idx), np.inf)
    first_dn = np.full(len(idx), np.inf)
    for k in range(SUPER_HORIZON, 0, -1):   # iterate backwards so the earliest hit wins
        j = np.minimum(idx + k, n - 1)
        first_up = np.where(h[j] >= 1.4 * c[idx], k, first_up)
        first_dn = np.where(l[j] <= 0.8 * c[idx], k, first_dn)
    out["clean_super"] = ((first_up < first_dn) & np.isfinite(first_up)).astype("float32")
    out["fwd_ret_63"] = fwd_ret[idx]
    out["label_end"] = df.index[np.minimum(idx + SUPER_HORIZON, n - 1)]
    out.loc[idx + SUPER_HORIZON > n - 1, ["fwd_max_gain", "fwd_ret_63", "clean_super"]] = np.nan
    ok = (c[idx] >= 5) & (c[idx] * feats_all["avg_vol_50"].to_numpy()[idx] >= 5e6)
    return out[ok].astype({k: "float32" for k in out.select_dtypes("float64").columns})


def process_ticker(args):
    ticker, df, rs_rank, grp, max_days, cost, seed = args
    b = bars(df)
    feats_all = structure_features(df)
    feats_all["setup_score"] = setup_score(feats_all)
    sample = superperformer_sample(ticker, df, feats_all, rs_rank, grp)
    sig = all_signals(df, b, seed=seed)
    if sig.empty:
        return None, sample
    idx = sig["idx"].to_numpy()
    ret, rmult, xidx, reason = engine.simulate_all(
        b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["sma50"], b["ema8"], b["ema21"], b["ema50"],
        b["atr20"], b["low10prev"], idx, sig["entry"].to_numpy(), sig["stop"].to_numpy(), EXIT_CODES, max_days, cost)
    feats = feats_all.iloc[idx].reset_index(drop=True)
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
    return out, sample


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
    frames, samples = [], []

    def collect(results):
        for k, (res, smp) in enumerate(results):
            if res is not None:
                frames.append(res)
            if smp is not None and len(smp):
                samples.append(smp)
            if (k + 1) % 200 == 0:
                print(f"[run] {k + 1}/{len(tasks)} tickers")

    if workers > 1:
        with ProcessPoolExecutor(workers) as ex:
            collect(ex.map(process_ticker, tasks, chunksize=10))
    else:
        collect(map(process_ticker, tasks))

    def with_market(d):
        m = mkt.reindex(mkt.index.union(pd.DatetimeIndex(d["date"].unique()))).ffill()
        d = d.join(m, on="date")
        fc = d.select_dtypes("float64").columns
        d[fc] = d[fc].astype("float32")
        return d.sort_values(["date", "ticker"]).reset_index(drop=True)

    sig = with_market(pd.concat(frames, ignore_index=True))
    sample = with_market(pd.concat(samples, ignore_index=True)) if samples else pd.DataFrame()
    return sig, sample
