"""Glue: load data -> panel of features -> filters -> setup signals -> simulated trades."""
from __future__ import annotations

import pandas as pd

from mlalgo import market as mkt
from mlalgo import universe
from mlalgo.setups import SETUPS, SetupConfig, find_signals
from mlalgo.structure import build_panel
from mlalgo.trade_sim import ExitConfig, simulate
from mlalgo.universe import FilterConfig, apply_filters

# Filters a stock must pass on the signal day to be traded. Trend/location filters are left
# to the setups themselves (an undercut briefly dips below the EMAs by design).
GATE = ["f_price", "f_liquidity", "f_adr", "f_rs"]


def add_source_args(p) -> None:
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--universe", help="file with one ticker per line")
    src.add_argument("--tickers", help="comma-separated tickers")
    src.add_argument("--csv-dir", help="folder of <TICKER>.csv files")
    p.add_argument("--start", default="2010-01-01")


def load(a) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    if a.csv_dir:
        prices = universe.load_csv_dir(a.csv_dir)
    else:
        tickers = universe.read_tickers(a.universe) if a.universe else [t.strip().upper() for t in a.tickers.split(",")]
        prices = universe.load_yahoo_many(tickers, start=a.start)
    try:
        market = mkt.load_market_yahoo(a.start)
    except Exception:
        market = mkt.synthetic_market(prices)
    return prices, market


def build(prices, market, cfg: FilterConfig) -> pd.DataFrame:
    panel = build_panel(prices)
    dates = panel.index.get_level_values("date")
    m = market.reindex(market.index.union(dates.unique())).ffill().reindex(dates)
    for col in m.columns:
        panel[col] = m[col].to_numpy()
    return apply_filters(panel, cfg)


def signals_for(prices, panel, setup_cfg=SetupConfig(), which=SETUPS, require_market=False) -> dict[str, pd.DataFrame]:
    out = {}
    for ticker, df in prices.items():
        sig = find_signals(df, setup_cfg, which)
        if sig.empty:
            continue
        keys = pd.MultiIndex.from_arrays([sig["date"], [ticker] * len(sig)])
        rows = panel.reindex(keys)
        ok = rows[GATE].fillna(False).astype(bool).all(axis=1).to_numpy()
        if require_market and "mkt_ok" in rows:
            ok &= rows["mkt_ok"].fillna(0).to_numpy() == 1
        sig = sig[ok]
        if len(sig):
            out[ticker] = sig.assign(ticker=ticker)
    return out


def trades_for(prices, panel, signals: dict[str, pd.DataFrame], exit_cfg=ExitConfig()) -> pd.DataFrame:
    trades = []
    for ticker, sig in signals.items():
        tr = simulate(prices[ticker], sig, exit_cfg)
        if len(tr):
            trades.append(tr.assign(ticker=ticker))
    if not trades:
        return pd.DataFrame()
    trades = pd.concat(trades, ignore_index=True).sort_values("entry_date", ignore_index=True)
    feats = panel.reindex(pd.MultiIndex.from_arrays([trades["entry_date"], trades["ticker"]])).reset_index(drop=True)
    return pd.concat([trades, feats.drop(columns=[c for c in feats.columns if c in trades.columns])], axis=1)
