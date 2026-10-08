"""Feature engineering.

Rule: every feature on row t may only use data available at the close of day t.
The target on row t is the *next* day's return (close t -> close t+1), which is
what you'd earn by deciding at today's close and holding one day.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / window, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / window, adjust=False).mean()
    return 100 - 100 / (1 + gain / loss)


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    c, h, l, v = df["close"], df["high"], df["low"], df["volume"]
    logret = np.log(c).diff()
    f = pd.DataFrame(index=df.index)

    for n in (1, 2, 5, 10, 21, 63):
        f[f"ret_{n}"] = np.log(c / c.shift(n))
    for n in (5, 21, 63):
        f[f"vol_{n}"] = logret.rolling(n).std()
    for n in (10, 50, 200):
        f[f"dist_sma_{n}"] = c / c.rolling(n).mean() - 1
    f["vol_ratio"] = f["vol_5"] / f["vol_63"]
    f["rsi_14"] = _rsi(c)
    f["range"] = (h - l) / c
    f["close_in_range"] = (c - l) / (h - l).replace(0, np.nan)
    f["volume_z"] = (v - v.rolling(21).mean()) / v.rolling(21).std()
    f["dist_high_252"] = c / c.rolling(252).max() - 1
    f["dow"] = df.index.dayofweek
    return f


def make_dataset(df: pd.DataFrame, horizon: int = 1) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Returns (X, y, fwd_ret). y = 1 if the forward `horizon`-day return is positive."""
    X = make_features(df)
    fwd_ret = df["close"].shift(-horizon) / df["close"] - 1
    data = X.assign(_fwd=fwd_ret).replace([np.inf, -np.inf], np.nan).dropna()
    fwd = data.pop("_fwd")
    y = (fwd > 0).astype(int)
    return data, y, fwd
