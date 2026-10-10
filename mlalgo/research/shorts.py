"""Qullamaggie's third setup, parabolic shorts, on daily bars (run 23).

Setup (known at the close of day t): up >= 50% in 10 days, >= 3 up closes in the last 4 days,
close >= 20% above the 10-day average. Entry: within the next 3 days, the first close below the
prior day's low (the first sign of weakness); short at that close. Stop: the high of the run
(the last 10 days up to the entry). Cover when price falls back to the 10- or 20-day average
(yesterday's value, filled at the open if it gaps through), or after 20 days. Stop checked first
on every bar (conservative). Costs 0.1% per side; borrow fees are not modelled.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

COVERS = {"sma10": 10, "sma20": 20}
VARIANTS = ("trigger", "no_trigger")   # no_trigger: short the parabolic day's close, no weakness needed


def signals(df: pd.DataFrame, min_gain: float = 0.5, max_risk: float = 0.35, cooldown: int = 20) -> pd.DataFrame:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    cs = pd.Series(c)
    sma10 = cs.rolling(10).mean().to_numpy()
    gain10 = c / cs.shift(10).to_numpy() - 1
    up = np.r_[False, c[1:] > c[:-1]]
    ups4 = pd.Series(up.astype(float)).rolling(4).sum().to_numpy()
    para = (gain10 >= min_gain) & (ups4 >= 3) & (c >= 1.2 * sma10)
    rows, last = [], -10**9
    for t in np.flatnonzero(para):
        if t - last <= cooldown or t < 30:
            continue
        for variant in VARIANTS:
            d = t
            if variant == "trigger":
                d = next((k for k in range(t + 1, min(t + 4, n)) if c[k] < l[k - 1]), -1)
                if d < 0:
                    continue
            if d >= n - 1:
                continue
            stop = h[max(0, d - 9):d + 1].max()
            risk = stop / c[d] - 1
            if risk <= 0 or risk > max_risk:
                continue
            rows.append({"idx": d, "setup_idx": t, "variant": variant, "entry": c[d], "stop": stop,
                         "risk_pct": risk, "gain10": gain10[t]})
        last = t
    return pd.DataFrame(rows)


def simulate(df: pd.DataFrame, sig: pd.DataFrame, max_days: int = 20, cost: float = 0.001) -> pd.DataFrame:
    """R multiple of each short for each cover rule."""
    if sig.empty:
        return sig
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    out = sig.copy()
    for name, w in COVERS.items():
        ma = pd.Series(c).rolling(w).mean().to_numpy()
        R, ret = [], []
        for r in sig.itertuples():
            t, e, s = r.idx, r.entry, r.stop
            px = None
            for d in range(t + 1, min(t + max_days, n - 1) + 1):
                if h[d] >= s:                         # stopped out (gap above the stop fills at the open)
                    px = max(o[d], s)
                    break
                level = ma[d - 1]
                if l[d] <= level:                     # back to the moving average: cover
                    px = min(o[d], level)
                    break
            if px is None:
                px = c[min(t + max_days, n - 1)]
            g = (e - px) / e - 2 * cost
            ret.append(g)
            R.append(g / ((s - e) / e))
        out[f"R_{name}"] = R
        out[f"ret_{name}"] = ret
    return out


def run_all(prices: dict[str, pd.DataFrame], min_price: float = 5.0, min_dollar_vol: float = 10e6) -> pd.DataFrame:
    frames = []
    for t, df in prices.items():
        if len(df) < 60:
            continue
        s = signals(df)
        if s.empty:
            continue
        c = df["close"].to_numpy(float)
        dv = (df["close"] * df["volume"]).rolling(50).mean().to_numpy()
        adr = (df["high"] / df["low"] - 1).rolling(20).mean().to_numpy()
        s = s[(c[s["idx"]] >= min_price) & (dv[s["idx"]] >= min_dollar_vol)]
        if s.empty:
            continue
        s = simulate(df, s)
        s["ticker"], s["date"], s["adr_pct"] = t, df.index[s["idx"]], adr[s["idx"]]
        frames.append(s)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def report(sh: pd.DataFrame, is_end: pd.Timestamp) -> pd.DataFrame:
    if sh.empty:
        return pd.DataFrame()
    rows = []
    for (variant, period), g in sh.groupby(["variant", np.where(sh["date"] < is_end, "IS", "OOS")]):
        for cov in COVERS:
            R = g[f"R_{cov}"]
            pos, neg = R[R > 0].sum(), -R[R < 0].sum()
            rows.append({"variant": variant, "cover": cov, "period": period, "n": len(R), "win": (R > 0).mean(),
                         "avgR": R.mean(), "PF": pos / neg if neg > 0 else np.nan, "avg_ret": g[f"ret_{cov}"].mean()})
    return pd.DataFrame(rows).sort_values(["variant", "cover", "period"])
