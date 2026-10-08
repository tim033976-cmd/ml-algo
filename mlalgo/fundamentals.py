"""Fundamental snapshot for today's scan, based on "The Alchemy of Multibagger Stocks"
(Yartseva, 2025). Over a one-year horizon, the 10-baggers studied there were best explained by:
  * high free-cash-flow yield (the strongest factor)
  * value (high book-to-market)
  * profitability (ROA)
  * small size
  * investment that is covered by profit growth: asset growth > EBITDA growth was a negative
  * rising interest rates were a headwind (see market.rates_regime)
EPS / sales growth were NOT significant in that study.

These are the *latest* numbers from Yahoo, not point-in-time history, so they're used to rank
today's candidates only. They are never used in the backtest, since that would leak future data.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd


def _latest_two(stmt: pd.DataFrame | None, names: list[str]) -> tuple[float, float]:
    if stmt is None or stmt.empty:
        return np.nan, np.nan
    for name in names:
        if name in stmt.index:
            vals = pd.to_numeric(stmt.loc[name], errors="coerce").dropna()  # columns: newest first
            if len(vals) >= 2:
                return float(vals.iloc[0]), float(vals.iloc[1])
    return np.nan, np.nan


def parse_fundamentals(info: dict, balance_sheet: pd.DataFrame | None, income_stmt: pd.DataFrame | None) -> dict:
    mcap = info.get("marketCap") or np.nan
    fcf = info.get("freeCashflow")
    ptb = info.get("priceToBook")
    a0, a1 = _latest_two(balance_sheet, ["Total Assets"])
    e0, e1 = _latest_two(income_stmt, ["EBITDA", "Normalized EBITDA"])
    asset_growth = a0 / a1 - 1 if a1 and a1 > 0 else np.nan
    ebitda_growth = e0 / e1 - 1 if e1 and e1 > 0 else np.nan
    return {
        "market_cap": mcap,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "fcf_yield": fcf / mcap if fcf is not None and mcap and mcap > 0 else np.nan,
        "book_to_market": 1 / ptb if ptb and ptb > 0 else np.nan,
        "roa": info.get("returnOnAssets", np.nan),
        "asset_growth": asset_growth,
        "ebitda_growth": ebitda_growth,
        "overinvesting": float(asset_growth > ebitda_growth) if not (np.isnan(asset_growth) or np.isnan(ebitda_growth)) else np.nan,
    }


def _fetch_one(ticker: str) -> dict:
    import yfinance as yf

    try:
        tk = yf.Ticker(ticker)
        return {"ticker": ticker, **parse_fundamentals(tk.info or {}, tk.balance_sheet, tk.income_stmt)}
    except Exception:
        return {"ticker": ticker}


def fetch_fundamentals(tickers: list[str], workers: int = 8) -> pd.DataFrame:
    with ThreadPoolExecutor(workers) as ex:
        return pd.DataFrame(list(ex.map(_fetch_one, tickers))).set_index("ticker")


def paper_score(f: pd.DataFrame) -> pd.Series:
    """0..1 rank-based score: FCF yield, value, ROA, smaller size; penalty for overinvesting."""
    ranks = pd.concat([
        f["fcf_yield"].rank(pct=True),
        f["book_to_market"].rank(pct=True),
        f["roa"].rank(pct=True),
        (-f["market_cap"]).rank(pct=True),
    ], axis=1)
    return ranks.mean(axis=1) - 0.25 * f["overinvesting"].fillna(0)


def theme_strength(rs_rank: pd.Series, industry: pd.Series) -> pd.Series:
    """Median relative-strength rank of each stock's industry: is the whole group leading?"""
    df = pd.DataFrame({"rs": rs_rank, "ind": industry}).dropna()
    return df.groupby("ind")["rs"].transform("median").reindex(rs_rank.index)
