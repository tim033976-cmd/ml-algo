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


def _atr(df: pd.DataFrame, n: int) -> pd.Series:
    prev = df["close"].shift()
    tr = pd.concat([df["high"] - df["low"], (df["high"] - prev).abs(), (df["low"] - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


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
    f["days_since_pivot"] = h.rolling(40).apply(lambda x: len(x) - 1 - np.argmax(x), raw=True)
    f["close_in_range_20"] = (c - l.rolling(20).min()) / (pivot - l.rolling(20).min())
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
]
