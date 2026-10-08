import numpy as np
import pandas as pd

from mlalgo.backtest import backtest, report
from mlalgo.data import synthetic
from mlalgo.features import make_dataset, make_features
from mlalgo.model import walk_forward_predict


def test_features_have_no_lookahead():
    """Changing future prices must not change past feature values."""
    df = synthetic(600)
    base = make_features(df)
    cut = 400
    tampered = df.copy()
    tampered.iloc[cut:] *= 1.5
    after = make_features(tampered)
    pd.testing.assert_frame_equal(base.iloc[:cut], after.iloc[:cut])


def test_target_is_next_day_return():
    df = synthetic(400)
    X, y, fwd = make_dataset(df)
    t = X.index[10]
    nxt = df.index[df.index.get_loc(t) + 1]
    assert np.isclose(fwd[t], df.loc[nxt, "close"] / df.loc[t, "close"] - 1)


def test_no_edge_on_random_walk():
    """On pure noise, out-of-sample AUC should be near 0.5. A high score means leakage."""
    df = synthetic(2000, seed=1)
    X, y, _ = make_dataset(df)
    prob = walk_forward_predict(X, y, kind="logreg", min_train=500, retrain_every=126)
    from sklearn.metrics import roc_auc_score
    assert abs(roc_auc_score(y.reindex(prob.index), prob) - 0.5) < 0.05


def test_backtest_costs():
    idx = pd.bdate_range("2020-01-01", periods=4)
    pos = pd.Series([1.0, 1.0, 0.0, 1.0], index=idx)
    fwd = pd.Series([0.01, 0.01, 0.01, 0.01], index=idx)
    bt = backtest(pos, fwd, cost_bps=10)
    # enter (cost), hold, exit (cost, no return), re-enter (cost)
    assert np.allclose(bt["strategy"], [0.01 - 0.001, 0.01, -0.001, 0.01 - 0.001])
    assert "sharpe" in report(bt).index
