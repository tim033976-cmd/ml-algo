"""Universe construction (S&P 1500 incl. former S&P 500 members) and bulk price download."""
from __future__ import annotations

import io
import time
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo.data import _normalize

WIKI = {
    "sp500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "sp400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "sp600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
SP500_FALLBACK = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
UA = {"User-Agent": "Mozilla/5.0 (research script; contact via GitHub)"}


def _yahoo_symbol(s: str) -> str:
    return str(s).strip().upper().replace(".", "-")


def _tables(url: str) -> list[pd.DataFrame]:
    import requests

    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return pd.read_html(io.StringIO(r.text))


def _flatten(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [" ".join(str(x) for x in c if "Unnamed" not in str(x)).strip() for c in df.columns]
    return df


def index_members(name: str) -> tuple[list[str], list[str]]:
    """(current members, removed members). Removed members only for the S&P 500 changes table."""
    current, removed = [], []
    try:
        tables = [_flatten(t) for t in _tables(WIKI[name])]
        for t in tables:
            col = next((c for c in t.columns if c in ("Symbol", "Ticker symbol", "Ticker")), None)
            if col is not None and len(t) > 100:
                current = [_yahoo_symbol(s) for s in t[col].dropna()]
                break
        if name == "sp500":
            for t in tables:
                rcol = next((c for c in t.columns if c.startswith("Removed") and ("Ticker" in c or "Symbol" in c)), None)
                if rcol is not None:
                    removed = [_yahoo_symbol(s) for s in t[rcol].dropna() if str(s).strip() and str(s) != "nan"]
                    break
    except Exception as e:  # network / layout change
        print(f"[universe] {name}: wikipedia failed ({e})")
    if not current and name == "sp500":
        current = [_yahoo_symbol(s) for s in pd.read_csv(SP500_FALLBACK)["Symbol"]]
    return current, removed


def build_universe(indexes=("sp500", "sp400", "sp600")) -> pd.DataFrame:
    rows = []
    for name in indexes:
        cur, rem = index_members(name)
        rows += [(t, name, "current") for t in cur] + [(t, name, "removed") for t in rem]
        print(f"[universe] {name}: {len(cur)} current, {len(rem)} removed")
    df = pd.DataFrame(rows, columns=["ticker", "index", "status"])
    return df.drop_duplicates("ticker", keep="first").reset_index(drop=True)


def download(tickers: list[str], start: str, chunk: int = 80, retries: int = 3) -> dict[str, pd.DataFrame]:
    import yfinance as yf

    out: dict[str, pd.DataFrame] = {}
    for i in range(0, len(tickers), chunk):
        batch = tickers[i : i + chunk]
        for attempt in range(retries):
            try:
                raw = yf.download(batch, start=start, auto_adjust=False, progress=False,
                                  group_by="ticker", threads=True)
                break
            except Exception as e:
                print(f"[download] batch {i}: {e}; retry {attempt + 1}")
                time.sleep(5 * (attempt + 1))
        else:
            continue
        for t in batch:
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                df = _normalize(sub.copy())
            except (KeyError, ValueError):
                continue
            df = df[(df["close"] > 0) & (df["volume"] >= 0)]
            if len(df) >= 300:
                out[t] = df.astype(np.float64)
        print(f"[download] {min(i + chunk, len(tickers))}/{len(tickers)} requested, {len(out)} usable")
        time.sleep(1)
    return out


def to_long(prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frames = [df.assign(ticker=t) for t, df in prices.items()]
    long = pd.concat(frames).rename_axis("date").reset_index()
    return long.astype({c: "float32" for c in ("open", "high", "low", "close", "volume")})


def from_long(long: pd.DataFrame) -> dict[str, pd.DataFrame]:
    out = {}
    for t, g in long.groupby("ticker", sort=False):
        out[t] = g.set_index("date")[["open", "high", "low", "close", "volume"]].astype(np.float64).sort_index()
    return out


def load_all(cache_dir: str, start: str, indexes=("sp500", "sp400", "sp600"), max_age_days: int = 6):
    """Returns (universe df, prices dict, market dict) using a parquet cache."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    pfile, ufile = cache / "prices.parquet", cache / "universe.csv"
    fresh = pfile.exists() and (time.time() - pfile.stat().st_mtime) < max_age_days * 86400
    if fresh:
        universe = pd.read_csv(ufile)
        long = pd.read_parquet(pfile)
        print(f"[data] loaded cache: {long['ticker'].nunique()} tickers")
    else:
        universe = build_universe(indexes)
        tickers = list(universe["ticker"]) + ["SPY", "QQQ", "^IRX"]
        prices = download(list(dict.fromkeys(tickers)), start)
        long = to_long(prices)
        long.to_parquet(pfile, index=False)
        universe.to_csv(ufile, index=False)
    prices = from_long(long)
    market = {k: prices.pop(k) for k in ("SPY", "QQQ", "^IRX") if k in prices}
    universe = universe[universe["ticker"].isin(prices)]
    return universe, prices, market
