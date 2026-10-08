"""Market regime: be aggressive only when the index is above its 8/21/50 EMAs.
Optional rates regime (from the multibagger paper: rising rates hurt growth stocks)."""
from __future__ import annotations

import pandas as pd

from mlalgo.indicators import ema


def index_regime(df: pd.DataFrame, prefix: str = "mkt") -> pd.DataFrame:
    c = df["close"]
    e8, e21, e50 = ema(c, 8), ema(c, 21), ema(c, 50)
    return pd.DataFrame({
        f"{prefix}_ok": ((c > e8) & (c > e21) & (c > e50)).astype(int),
        f"{prefix}_ema_stack": ((e8 > e21) & (e21 > e50)).astype(int),
        f"{prefix}_ret_21": c / c.shift(21) - 1,
    }, index=df.index)


def rates_regime(irx_close: pd.Series) -> pd.DataFrame:
    """^IRX = 13-week T-bill yield, a proxy for the Fed rate. 1 = higher than a year ago."""
    return pd.DataFrame({"rates_rising": (irx_close > irx_close.shift(252)).astype(int)}, index=irx_close.index)


def load_market_yahoo(start: str) -> pd.DataFrame:
    import yfinance as yf

    from mlalgo.data import _normalize

    parts = []
    for sym, prefix in (("SPY", "mkt"), ("QQQ", "qqq")):
        parts.append(index_regime(_normalize(yf.download(sym, start=start, auto_adjust=False, progress=False)), prefix))
    try:
        irx = yf.download("^IRX", start=start, auto_adjust=False, progress=False)["Close"].squeeze()
        parts.append(rates_regime(irx.dropna()))
    except Exception:  # rates are optional
        pass
    out = pd.concat(parts, axis=1).ffill()
    out.index = pd.to_datetime(out.index).tz_localize(None)
    return out


def synthetic_market(prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Equal-weight index of the universe (for offline runs)."""
    rets = pd.DataFrame({t: df["close"].pct_change() for t, df in prices.items()}).mean(axis=1).fillna(0)
    return index_regime(pd.DataFrame({"close": 100 * (1 + rets).cumprod()}), "mkt")


MARKET_FEATURES = ["mkt_ok", "mkt_ema_stack", "mkt_ret_21", "qqq_ok", "rates_rising"]
