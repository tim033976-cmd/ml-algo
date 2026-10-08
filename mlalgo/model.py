"""Walk-forward training: the only honest way to evaluate a trading model.

The model is refit every `retrain_every` days on all data before the test block
(expanding window), skipping an `embargo` gap so training labels never overlap
with the test period. Predictions are therefore always out-of-sample.
"""
from __future__ import annotations

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_model(kind: str = "gbm"):
    if kind == "gbm":
        return HistGradientBoostingClassifier(
            max_depth=3, learning_rate=0.05, max_iter=200, l2_regularization=1.0,
            min_samples_leaf=50, random_state=0,
        )
    if kind == "logreg":
        return make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000))
    raise ValueError(f"unknown model kind {kind!r}")


def walk_forward_predict(
    X: pd.DataFrame,
    y: pd.Series,
    kind: str = "gbm",
    min_train: int = 756,     # ~3 years
    retrain_every: int = 63,  # ~quarterly
    embargo: int = 1,         # >= horizon, so train labels don't peek into the test block
) -> pd.Series:
    """Out-of-sample probability that the next return is positive, indexed like X."""
    preds = []
    for start in range(min_train, len(X), retrain_every):
        train_end = start - embargo
        model = build_model(kind).fit(X.iloc[:train_end], y.iloc[:train_end])
        block = X.iloc[start : start + retrain_every]
        preds.append(pd.Series(model.predict_proba(block)[:, 1], index=block.index))
    if not preds:
        raise ValueError(f"need more than min_train={min_train} rows, got {len(X)}")
    return pd.concat(preds).rename("prob_up")
