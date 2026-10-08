"""Stage 2: chart-structure features that describe whether a stock is "primed".

"Primed" here means the classic base-breakout setup:
  * strong prior uptrend, trading near its highs
  * a base whose pullbacks get progressively smaller (volatility contraction / VCP)
  * price tightening up with volume drying up
  * sitting just under the pivot (top of the base), with higher lows

All features at row t use only data up to the close of day t.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from mlalgo.indicators import adr_pct, atr as _atr, ema


def _days_since_max(x: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) >= n:
        w = np.lib.stride_tricks.sliding_window_view(x, n)
        out[n - 1:] = n - 1 - np.argmax(w, axis=1)
    return out


def _staircase_count(c: pd.Series, h: pd.Series, sma200: pd.Series, min_base: int = 10, lookback: int = 20) -> np.ndarray:
    """How many 'steps' the current uptrend has made: breakouts to a new 20-day high after
    a rest of >= `min_base` days, counted since price was last below its 200-day SMA.
    1st/2nd steps are the sweet spot; late steps fail more often."""
    prior_high = h.rolling(lookback).max().shift(1).to_numpy()
    cc, s = c.to_numpy(), sma200.to_numpy()
    out = np.zeros(len(cc))
    count, since_high = 0, 0
    for t in range(len(cc)):
        if np.isnan(s[t]) or cc[t] < s[t]:
            count = 0
        if not np.isnan(prior_high[t]) and cc[t] > prior_high[t]:
            if since_high >= min_base:
                count += 1
            since_high = 0
        else:
            since_high += 1
        out[t] = count
    return out


def _window_range(df: pd.DataFrame, length: int, offset: int) -> pd.Series:
    """(high - low) / high over the `length` days ending `offset` days ago."""
    hi = df["high"].rolling(length).max().shift(offset)
    lo = df["low"].rolling(length).min().shift(offset)
    return (hi - lo) / hi


def structure_features(df: pd.DataFrame) -> pd.DataFrame:
    c, h, l, v = df["close"], df["high"], df["low"], df["volume"]
    f = pd.DataFrame(index=df.index)
    f["close"] = c
    f["dollar_vol_50"] = (c * v).rolling(50).mean()

    # --- trend / location
    sma50, sma150, sma200 = (c.rolling(n).mean() for n in (50, 150, 200))
    f["trend_template"] = ((c > sma50) & (sma50 > sma150) & (sma150 > sma200)
                           & (sma200 > sma200.shift(21))).astype(int)
    f["dist_sma50"] = c / sma50 - 1
    f["sma200_slope"] = sma200 / sma200.shift(21) - 1
    f["dist_52w_high"] = c / h.rolling(252).max() - 1
    f["above_52w_low"] = c / l.rolling(252).min() - 1
    f["ret_63"] = c / c.shift(63) - 1
    f["ret_126"] = c / c.shift(126) - 1
    f["ret_252"] = c / c.shift(252) - 1

    # --- base: last 60 days split into three 20-day legs (oldest -> newest)
    r1, r2, r3 = _window_range(df, 20, 40), _window_range(df, 20, 20), _window_range(df, 20, 0)
    f["base_depth_60"] = _window_range(df, 60, 0)
    f["leg1_range"], f["leg2_range"], f["leg3_range"] = r1, r2, r3
    f["contraction_ratio"] = r3 / r1                       # < 1 means pullbacks are shrinking
    f["contracting"] = ((r3 < r2) & (r2 < r1)).astype(int)
    lows = [l.rolling(20).min().shift(s) for s in (40, 20, 0)]
    f["higher_lows"] = ((lows[2] > lows[1]) & (lows[1] > lows[0])).astype(int)

    # --- tightness and volume dry-up
    f["atr_ratio"] = _atr(df, 10) / _atr(df, 50)          # < 1 means volatility is compressing
    f["atr_pct"] = _atr(df, 14) / c
    f["tight_10"] = (h.rolling(10).max() - l.rolling(10).min()) / c
    f["close_std_10"] = c.pct_change().rolling(10).std()
    f["vol_dryup"] = v.rolling(10).mean() / v.rolling(50).mean()
    up = (c > c.shift()).astype(float)
    f["updown_vol_50"] = (v * up).rolling(50).sum() / (v * (1 - up)).rolling(50).sum()

    # --- pivot: top of the recent base
    pivot = h.rolling(40).max()
    f["dist_to_pivot"] = c / pivot - 1                     # 0 = at pivot, -0.03 = 3% below
    f["days_since_pivot"] = _days_since_max(h.to_numpy(float), 40)
    f["close_in_range_20"] = (c - l.rolling(20).min()) / (pivot - l.rolling(20).min())

    # --- EMA momentum gauge (8/21/50) and daily range
    e8, e21, e50 = ema(c, 8), ema(c, 21), ema(c, 50)
    f["avg_vol_50"] = v.rolling(50).mean()
    f["adr_pct"] = adr_pct(df)
    f["above_emas"] = ((c > e8) & (c > e21) & (c > e50)).astype(int)
    f["ema_stack"] = ((e8 > e21) & (e21 > e50)).astype(int)
    f["ext_ema8_adr"] = (c / e8 - 1) / f["adr_pct"]        # extension from 8 EMA in ADRs
    f["dist_ema21"] = c / e21 - 1

    # --- healthy pullback vs reversal: quiet drift on low volume vs big red candles on rising volume
    down = c < c.shift()
    f["down_vol_ratio_10"] = (v.where(down).rolling(10, min_periods=1).mean() / v.rolling(50).mean()).fillna(0)
    f["down_candle_exp_5"] = ((h - l).where(down).rolling(5, min_periods=1).mean() / _atr(df, 20)).fillna(0)
    f["distribution_days_25"] = (down & (c.pct_change() < -0.002) & (v > v.rolling(50).mean())).rolling(25).sum()
    f["closes_below_e21_10"] = (c < e21).rolling(10).sum()

    # --- stage analysis (Weinstein, 30-week ~ 150-day SMA) and staircase count
    sma150 = c.rolling(150).mean()
    f["sma150_slope"] = sma150 / sma150.shift(20) - 1
    f["stage"] = np.select([(c > sma150) & (f["sma150_slope"] > 0.005),
                            (c < sma150) & (f["sma150_slope"] < -0.005)], [2, 4], 1)  # 1 = basing/flat
    f["base_count"] = _staircase_count(c, h, sma200)

    # --- the multibagger paper's entry-point factor: where in the 12-month range is price?
    hi252, lo252 = h.rolling(252).max(), l.rolling(252).min()
    f["range_pos_12m"] = (c - lo252) / (hi252 - lo252)
    return f.replace([np.inf, -np.inf], np.nan)


def setup_score(p: pd.DataFrame) -> pd.Series:
    """Transparent rule-based 0..1 score: fraction of 'primed' conditions met."""
    checks = pd.DataFrame({
        "near_pivot": p["dist_to_pivot"].between(-0.06, 0.0),
        "contracting": p["contraction_ratio"] < 0.7,
        "tight": p["tight_10"] < 0.08,
        "vol_compress": p["atr_ratio"] < 0.85,
        "vol_dryup": p["vol_dryup"] < 0.85,
        "higher_lows": p["higher_lows"] == 1,
        "shallow_base": p["base_depth_60"] < 0.30,
        "accumulation": p["updown_vol_50"] > 1.0,
        "above_emas": p["above_emas"] == 1,
        "quiet_pullback": p["down_vol_ratio_10"] < 1.0,
        "early_stage": p["base_count"].between(1, 2),
    })
    return checks.mean(axis=1)


def build_panel(prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Stack per-ticker features into one (date, ticker) frame and add cross-sectional ranks."""
    frames = {t: structure_features(df) for t, df in prices.items()}
    panel = pd.concat(frames, names=["ticker", "date"]).swaplevel().sort_index()
    # Relative strength: weighted momentum ranked against the universe on each day
    rs = 0.4 * panel["ret_63"] + 0.3 * panel["ret_126"] + 0.3 * panel["ret_252"]
    panel["rs_rank"] = rs.groupby(level="date").rank(pct=True)
    panel["setup_score"] = setup_score(panel)
    return panel


ML_FEATURES = [
    "dist_sma50", "sma200_slope", "dist_52w_high", "above_52w_low", "ret_63", "ret_126", "rs_rank",
    "base_depth_60", "leg1_range", "leg2_range", "leg3_range", "contraction_ratio", "contracting",
    "higher_lows", "atr_ratio", "atr_pct", "tight_10", "close_std_10", "vol_dryup", "updown_vol_50",
    "dist_to_pivot", "days_since_pivot", "close_in_range_20", "setup_score",
    "adr_pct", "above_emas", "ema_stack", "ext_ema8_adr", "dist_ema21", "down_vol_ratio_10",
    "down_candle_exp_5", "distribution_days_25", "closes_below_e21_10", "sma150_slope", "stage",
    "base_count", "range_pos_12m",
]
