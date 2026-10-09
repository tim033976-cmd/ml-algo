"""Short-horizon features from concrete daily / weekly data only (no VWAP, volume profile or
order-flow proxies). Every value on day t uses data up to the close of day t."""
from __future__ import annotations

import numpy as np
import pandas as pd

SHORT_FEATURES = [
    # candle anatomy (today and yesterday)
    "body_pct", "range_pct", "upper_wick", "lower_wick", "close_loc", "body_pct_prev", "close_loc_prev",
    "inside_day", "outside_day", "nr7", "green_streak", "ret_1", "ret_3", "ret_5",
    # gaps
    "gap_pct", "gap_filled", "fvg_bull", "fvg_bear", "fvg_bull_10", "fvg_bear_10",
    # volume
    "rel_vol", "rel_vol_prev", "vol_trend_5_50",
    # levels
    "dist_round", "dist_sma20", "dist_sma200", "above_sma200", "dist_resistance", "dist_support",
    "trend_slope_20", "trend_resid_20",
    # weekly structure (completed weeks only) and week-to-date
    "wk_ret_1", "wk_close_loc", "wk_hh", "wk_hl", "wk_above_10wma", "wtd_ret",
    # calendar
    "dow", "month",
]


def _swings(h: np.ndarray, l: np.ndarray, k: int = 3):
    """Confirmed swing highs/lows: a swing at i is only known at i+k."""
    n = len(h)
    hi = np.full(n, np.nan)
    lo = np.full(n, np.nan)
    for i in range(k, n - k):
        if h[i] == h[i - k:i + k + 1].max():
            hi[i + k] = h[i]          # becomes known k bars later
        if l[i] == l[i - k:i + k + 1].min():
            lo[i + k] = l[i]
    return hi, lo


def _nearest_levels(c: np.ndarray, hi_known: np.ndarray, lo_known: np.ndarray, lookback: int = 120):
    """Distance to the nearest confirmed swing high above / swing low below the close."""
    n = len(c)
    res = np.full(n, np.nan)
    sup = np.full(n, np.nan)
    hi_idx = np.flatnonzero(~np.isnan(hi_known))
    lo_idx = np.flatnonzero(~np.isnan(lo_known))
    for t in range(n):
        hs = hi_known[hi_idx[(hi_idx <= t) & (hi_idx > t - lookback)]]
        ls = lo_known[lo_idx[(lo_idx <= t) & (lo_idx > t - lookback)]]
        above = hs[hs > c[t]]
        below = ls[ls < c[t]]
        if len(above):
            res[t] = above.min() / c[t] - 1
        if len(below):
            sup[t] = 1 - below.max() / c[t]
    return res, sup


def short_features(df: pd.DataFrame) -> pd.DataFrame:
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))
    f = pd.DataFrame(index=df.index)
    rng = (h - l).replace(0, np.nan)
    f["body_pct"] = c / o - 1
    f["range_pct"] = (h - l) / c
    f["upper_wick"] = (h - np.maximum(o, c)) / rng
    f["lower_wick"] = (np.minimum(o, c) - l) / rng
    f["close_loc"] = (c - l) / rng
    f["body_pct_prev"] = f["body_pct"].shift(1)
    f["close_loc_prev"] = f["close_loc"].shift(1)
    f["inside_day"] = ((h < h.shift(1)) & (l > l.shift(1))).astype(float)
    f["outside_day"] = ((h > h.shift(1)) & (l < l.shift(1))).astype(float)
    f["nr7"] = ((h - l) <= (h - l).rolling(7).min()).astype(float)
    up = (c > c.shift(1)).astype(int)
    f["green_streak"] = up.groupby((up != up.shift()).cumsum()).cumsum() * up - (1 - up).groupby((up != up.shift()).cumsum()).cumsum() * (1 - up)
    for n in (1, 3, 5):
        f[f"ret_{n}"] = c / c.shift(n) - 1

    prev_c = c.shift(1)
    f["gap_pct"] = o / prev_c - 1
    f["gap_filled"] = (((o > prev_c) & (l <= prev_c)) | ((o < prev_c) & (h >= prev_c))).astype(float)
    bull = l > h.shift(2)                      # fair value gap: today's low above the high two bars ago
    bear = h < l.shift(2)
    f["fvg_bull"] = np.where(bull, (l - h.shift(2)) / c, 0.0)
    f["fvg_bear"] = np.where(bear, (l.shift(2) - h) / c, 0.0)
    f["fvg_bull_10"] = bull.astype(float).rolling(10).sum()
    f["fvg_bear_10"] = bear.astype(float).rolling(10).sum()

    vol50 = v.rolling(50).mean()
    f["rel_vol"] = v / vol50
    f["rel_vol_prev"] = f["rel_vol"].shift(1)
    f["vol_trend_5_50"] = v.rolling(5).mean() / vol50

    step = 5 * 10 ** (np.floor(np.log10(c.clip(lower=0.01))) - 1)     # 47 -> 5, 230 -> 50, 1800 -> 500
    f["dist_round"] = (c - (c / step).round() * step) / c
    for n in (20, 200):
        f[f"dist_sma{n}"] = c / c.rolling(n).mean() - 1
    f["above_sma200"] = (f["dist_sma200"] > 0).astype(float)
    hi_known, lo_known = _swings(h.to_numpy(float), l.to_numpy(float))
    res, sup = _nearest_levels(c.to_numpy(float), hi_known, lo_known)
    f["dist_resistance"], f["dist_support"] = res, sup
    x = np.arange(20, dtype=float)
    lc = np.log(c.to_numpy(float))
    w = np.lib.stride_tricks.sliding_window_view(lc, 20) if len(lc) >= 20 else np.empty((0, 20))
    slope = np.full(len(lc), np.nan)
    resid = np.full(len(lc), np.nan)
    if len(w):
        xm = x - x.mean()
        b = (w - w.mean(1, keepdims=True)) @ xm / (xm @ xm)
        fit_last = w.mean(1) + b * xm[-1]
        sd = (w - (w.mean(1, keepdims=True) + b[:, None] * xm)).std(1)
        slope[19:] = b
        resid[19:] = (w[:, -1] - fit_last) / np.where(sd > 0, sd, np.nan)
    f["trend_slope_20"], f["trend_resid_20"] = slope, resid

    # weekly bars from completed weeks only: compute on weekly data, shift one week, map to days
    wk = df.resample("W-FRI").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    wf = pd.DataFrame(index=wk.index)
    wf["wk_ret_1"] = wk["close"].pct_change()
    wf["wk_close_loc"] = (wk["close"] - wk["low"]) / (wk["high"] - wk["low"]).replace(0, np.nan)
    wf["wk_hh"] = (wk["high"] > wk["high"].shift(1)).astype(float)
    wf["wk_hl"] = (wk["low"] > wk["low"].shift(1)).astype(float)
    wf["wk_above_10wma"] = (wk["close"] > wk["close"].rolling(10).mean()).astype(float)
    week_end = df.index.to_period("W-FRI").to_timestamp("D", how="end").normalize()
    prev_week = (week_end - pd.Timedelta(days=7))
    wf.index = wf.index.normalize()
    mapped = wf.reindex(prev_week)
    mapped.index = df.index
    f = pd.concat([f, mapped], axis=1)
    last_week_close = wk["close"]
    last_week_close.index = last_week_close.index.normalize()
    lwc = last_week_close.reindex(prev_week).to_numpy()
    f["wtd_ret"] = c.to_numpy() / lwc - 1

    f["dow"] = df.index.dayofweek.astype(float)
    f["month"] = df.index.month.astype(float)
    return f.replace([np.inf, -np.inf], np.nan).astype("float32")


def short_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Targets (future data by design): next-day green candle (close > open), next-day up
    (close > today's close), up over 3 and 5 days, and the matching returns."""
    o, c = df["open"], df["close"]
    out = pd.DataFrame(index=df.index)
    out["y_green1"] = (c.shift(-1) > o.shift(-1)).astype(float)
    for n, name in ((1, "up1"), (3, "up3"), (5, "up5")):
        r = c.shift(-n) / c - 1
        out[f"y_{name}"] = (r > 0).astype(float)
        out[f"r_{name}"] = r
    out.loc[c.shift(-5).isna(), :] = np.nan
    return out.astype("float32")
