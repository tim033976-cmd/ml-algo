"""Basic indicators shared across modules (all causal: row t uses data up to t)."""
from __future__ import annotations

import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def atr(df: pd.DataFrame, n: int) -> pd.Series:
    prev = df["close"].shift()
    tr = pd.concat([df["high"] - df["low"], (df["high"] - prev).abs(), (df["low"] - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def adr_pct(df: pd.DataFrame, n: int = 20) -> pd.Series:
    """Average daily range, as a fraction (0.04 = 4%)."""
    return (df["high"] / df["low"] - 1).rolling(n).mean()
