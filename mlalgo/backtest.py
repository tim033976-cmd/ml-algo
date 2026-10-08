"""Turn predictions into positions and measure performance after costs."""
from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def positions_from_probs(prob: pd.Series, threshold: float = 0.52, allow_short: bool = False) -> pd.Series:
    long = (prob > threshold).astype(float)
    if allow_short:
        return long - (prob < 1 - threshold).astype(float)
    return long


def backtest(position: pd.Series, fwd_ret: pd.Series, cost_bps: float = 5.0) -> pd.DataFrame:
    """position[t] is decided at close t and earns fwd_ret[t] (close t -> t+1).
    Costs are charged on every change in position."""
    fwd = fwd_ret.reindex(position.index)
    turnover = position.diff().abs().fillna(position.abs())
    strat = position * fwd - turnover * cost_bps / 1e4
    return pd.DataFrame({"position": position, "strategy": strat, "buy_hold": fwd})


def metrics(returns: pd.Series) -> dict:
    r = returns.dropna()
    equity = (1 + r).cumprod()
    years = len(r) / TRADING_DAYS
    dd = equity / equity.cummax() - 1
    std = r.std()
    return {
        "total_return": equity.iloc[-1] - 1,
        "cagr": equity.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan,
        "sharpe": r.mean() / std * np.sqrt(TRADING_DAYS) if std > 0 else np.nan,
        "max_drawdown": dd.min(),
        "hit_rate": (r[r != 0] > 0).mean(),
    }


def report(bt: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"strategy": metrics(bt["strategy"]), "buy_hold": metrics(bt["buy_hold"])})
    out.loc["exposure", "strategy"] = bt["position"].abs().mean()
    out.loc["trades_per_year", "strategy"] = bt["position"].diff().abs().sum() / (len(bt) / TRADING_DAYS)
    return out
