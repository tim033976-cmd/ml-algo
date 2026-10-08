"""Loading daily OHLCV price data."""
from __future__ import annotations

import numpy as np
import pandas as pd

COLUMNS = ["open", "high", "low", "close", "volume"]


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):  # yfinance returns (field, ticker)
        df = df.droplevel(1, axis=1)
    df = df.rename(columns=lambda c: str(c).lower().replace(" ", "_"))
    if "adj_close" in df.columns:  # prefer split/dividend-adjusted prices
        ratio = df["adj_close"] / df["close"]
        for col in ["open", "high", "low", "close"]:
            df[col] = df[col] * ratio
    df = df[COLUMNS].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.index.name = "date"
    return df.sort_index()


def load_yahoo(ticker: str, start: str = "2005-01-01", end: str | None = None) -> pd.DataFrame:
    import yfinance as yf

    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if df.empty:
        raise RuntimeError(f"No data downloaded for {ticker!r} (check ticker / network).")
    return _normalize(df)


def load_csv(path: str) -> pd.DataFrame:
    """CSV with a date column plus open/high/low/close/volume (any case)."""
    df = pd.read_csv(path)
    date_col = next(c for c in df.columns if c.lower() in ("date", "datetime", "timestamp"))
    return _normalize(df.set_index(date_col))


def synthetic(n_days: int = 3000, seed: int = 0) -> pd.DataFrame:
    """Random-walk prices for testing the pipeline offline. There is no real edge here,
    so a model that 'works' on this data is a sign of a bug (e.g. lookahead)."""
    rng = np.random.default_rng(seed)
    rets = rng.normal(0.0003, 0.012, n_days)
    close = 100 * np.exp(np.cumsum(rets))
    open_ = close * np.exp(rng.normal(0, 0.003, n_days))
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0, 0.005, n_days)))
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0, 0.005, n_days)))
    volume = rng.lognormal(15, 0.3, n_days)
    idx = pd.bdate_range("2010-01-01", periods=n_days, name="date")
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=idx
    )
