"""Stage 1: load a stock universe and filter it down to candidates.

Every filter is evaluated point-in-time (using only data up to that day), so the
same code works for today's scan and for historical training/backtests.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo import data


def read_tickers(path: str) -> list[str]:
    """One ticker per line (or comma separated); '#' starts a comment."""
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.split("#")[0]
        out += [t.strip().upper() for t in line.split(",") if t.strip()]
    return list(dict.fromkeys(out))


def load_yahoo_many(tickers: list[str], start: str = "2010-01-01") -> dict[str, pd.DataFrame]:
    import yfinance as yf

    raw = yf.download(tickers, start=start, auto_adjust=False, progress=False, group_by="ticker", threads=True)
    prices = {}
    for t in tickers:
        try:
            df = data._normalize(raw[t].copy()) if len(tickers) > 1 else data._normalize(raw.copy())
        except KeyError:
            continue
        if len(df) > 300:
            prices[t] = df
    if not prices:
        raise RuntimeError("No data downloaded (check tickers / network).")
    return prices


def load_csv_dir(folder: str) -> dict[str, pd.DataFrame]:
    """A folder of <TICKER>.csv files."""
    return {p.stem.upper(): data.load_csv(str(p)) for p in sorted(Path(folder).glob("*.csv"))}


def synthetic_universe(n: int = 60, n_days: int = 2500, seed: int = 0) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    out = {}
    for i in range(n):
        df = data.synthetic(n_days, seed=seed * 1000 + i)
        drift = rng.normal(0.0004, 0.0006)  # some names trend, some don't
        df[["open", "high", "low", "close"]] *= np.exp(drift * np.arange(n_days))[:, None]
        out[f"SYN{i:03d}"] = df
    return out


@dataclass
class FilterConfig:
    min_price: float = 10.0
    min_dollar_volume: float = 20e6      # 50-day average $ volume
    max_below_52w_high: float = 0.25     # within 25% of 52-week high
    min_above_52w_low: float = 0.30      # at least 30% above 52-week low
    min_rs_rank: float = 0.70            # top 30% relative strength in the universe
    require_trend: bool = True           # close > SMA50 > SMA150 > SMA200, SMA200 rising


FILTER_COLUMNS = ["f_price", "f_liquidity", "f_trend", "f_near_high", "f_off_low", "f_rs"]


def apply_filters(panel: pd.DataFrame, cfg: FilterConfig = FilterConfig()) -> pd.DataFrame:
    """Adds one boolean column per filter plus `passes` (all filters true).
    `panel` is the (date, ticker) frame from structure.build_panel."""
    p = panel
    p["f_price"] = p["close"] >= cfg.min_price
    p["f_liquidity"] = p["dollar_vol_50"] >= cfg.min_dollar_volume
    p["f_trend"] = p["trend_template"].astype(bool) if cfg.require_trend else True
    p["f_near_high"] = p["dist_52w_high"] >= -cfg.max_below_52w_high
    p["f_off_low"] = p["above_52w_low"] >= cfg.min_above_52w_low
    p["f_rs"] = p["rs_rank"] >= cfg.min_rs_rank
    p["passes"] = p[FILTER_COLUMNS].all(axis=1)
    return p
