"""ML on top of the filtered candidates: P(stock hits target before stop | chart structure).

Trained cross-sectionally (all candidates from all tickers pooled) and evaluated
walk-forward by date, with an embargo of `horizon` days so training labels never
overlap the test period.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from mlalgo.structure import ML_FEATURES


def build_model():
    return HistGradientBoostingClassifier(
        max_depth=3, learning_rate=0.05, max_iter=300, l2_regularization=1.0,
        min_samples_leaf=100, random_state=0,
    )


def training_rows(panel: pd.DataFrame) -> pd.DataFrame:
    """Filtered candidates with a known outcome."""
    return panel[panel["passes"] & panel["outcome"].notna()].dropna(subset=ML_FEATURES)


def walk_forward(panel: pd.DataFrame, horizon: int, min_train_days: int = 756,
                 retrain_every: int = 63) -> pd.Series:
    rows = training_rows(panel)
    dates = panel.index.get_level_values("date").unique().sort_values()
    preds = []
    for i in range(min_train_days, len(dates), retrain_every):
        train_cut = dates[i - horizon - 1]  # embargo: labels need `horizon` future days
        test_dates = dates[i : i + retrain_every]
        rdates = rows.index.get_level_values("date")
        train = rows[rdates <= train_cut]
        test = rows[(rdates >= test_dates[0]) & (rdates <= test_dates[-1])]
        if len(test) == 0 or train["outcome"].eq(1).sum() < 20:
            continue
        model = build_model().fit(train[ML_FEATURES], train["outcome"].eq(1))
        preds.append(pd.Series(model.predict_proba(test[ML_FEATURES])[:, 1], index=test.index))
    if not preds:
        raise ValueError("Not enough filtered history to train; loosen filters or add data.")
    return pd.concat(preds).rename("prob_primed")


def evaluate(panel: pd.DataFrame, prob: pd.Series, top_k: int = 5) -> pd.DataFrame:
    """Each day, compare all candidates vs. the top-k by rule score vs. the top-k by ML probability."""
    df = panel.loc[prob.index, ["outcome", "trade_ret", "setup_score"]].assign(prob=prob)
    by_date = df.groupby(level="date")
    picks = {
        "all candidates": df,
        f"top {top_k} by rule score": df[by_date["setup_score"].rank(ascending=False, method="first") <= top_k],
        f"top {top_k} by ML prob": df[by_date["prob"].rank(ascending=False, method="first") <= top_k],
    }
    rows = {}
    for name, d in picks.items():
        rows[name] = {
            "signals": len(d),
            "hit_target_rate": (d["outcome"] == 1).mean(),
            "stopped_rate": (d["outcome"] == -1).mean(),
            "avg_trade_ret": d["trade_ret"].mean(),
        }
    return pd.DataFrame(rows).T


def fit_final(panel: pd.DataFrame):
    rows = training_rows(panel)
    return build_model().fit(rows[ML_FEATURES], rows["outcome"].eq(1))
