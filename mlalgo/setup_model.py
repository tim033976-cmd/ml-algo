"""ML on top of the setup signals: which of these trades are worth taking?

Each simulated trade is one row: the chart-structure features on the signal day (plus market
regime and setup type). Label = the trade made at least 1R. Walk-forward by calendar quarter,
training only on trades that had already *closed* before the quarter started (no leakage).
"""
from __future__ import annotations

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from mlalgo.market import MARKET_FEATURES
from mlalgo.setups import SETUPS
from mlalgo.structure import ML_FEATURES
from mlalgo.trade_sim import trade_stats


def feature_columns(df: pd.DataFrame) -> list[str]:
    extra = [c for c in MARKET_FEATURES if c in df.columns]
    return ML_FEATURES + extra + ["risk_pct"] + [f"is_{s}" for s in SETUPS]


def add_setup_dummies(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(**{f"is_{s}": (df["setup"] == s).astype(int) for s in SETUPS})


def build_model():
    return HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200,
                                          l2_regularization=1.0, min_samples_leaf=40, random_state=0)


def walk_forward(trades: pd.DataFrame, min_train: int = 150) -> pd.Series:
    trades = add_setup_dummies(trades)
    cols = feature_columns(trades)
    y = trades["R"] >= 1
    quarters = trades["entry_date"].dt.to_period("Q")
    preds = []
    for q in sorted(quarters.unique()):
        start = q.start_time
        train = trades["exit_date"] < start
        test = quarters == q
        if train.sum() < min_train or y[train].sum() < 20:
            continue
        model = build_model().fit(trades.loc[train, cols], y[train])
        preds.append(pd.Series(model.predict_proba(trades.loc[test, cols])[:, 1], index=trades.index[test]))
    if not preds:
        raise ValueError("Not enough trades to train the setup model.")
    return pd.concat(preds).rename("prob_win")


def evaluate(trades: pd.DataFrame, prob: pd.Series) -> pd.DataFrame:
    t = trades.loc[prob.index].assign(prob=prob)
    cut = t["prob"].quantile(2 / 3)
    return pd.DataFrame({
        "all OOS signals": trade_stats(t),
        "top third by ML": trade_stats(t[t["prob"] >= cut]),
        "bottom third by ML": trade_stats(t[t["prob"] <= t["prob"].quantile(1 / 3)]),
    })


def fit_final(trades: pd.DataFrame):
    trades = add_setup_dummies(trades)
    closed = trades[trades["exit_reason"] != "open"]
    return build_model().fit(closed[feature_columns(closed)], closed["R"] >= 1)
