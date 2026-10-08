import numpy as np
import pandas as pd

from mlalgo.data import synthetic
from mlalgo.labels import triple_barrier
from mlalgo.structure import build_panel, structure_features
from mlalgo.universe import FilterConfig, apply_filters, synthetic_universe


def test_structure_features_have_no_lookahead():
    df = synthetic(700)
    base = structure_features(df)
    tampered = df.copy()
    tampered.iloc[500:] *= 1.7
    pd.testing.assert_frame_equal(base.iloc[:500], structure_features(tampered).iloc[:500])


def _bars(highs, lows, closes):
    idx = pd.bdate_range("2021-01-01", periods=len(closes))
    return pd.DataFrame({"open": closes, "high": highs, "low": lows, "close": closes, "volume": 1e6}, index=idx)


def test_triple_barrier_target_stop_and_timeout():
    # day0 entry at 100; day2 high hits 110 -> target
    df = _bars([100, 105, 111, 100, 100, 100], [100, 99, 101, 99, 99, 99], [100, 104, 108, 100, 100, 100])
    out = triple_barrier(df, target=0.10, stop=0.05, horizon=3)
    assert out.loc[df.index[0], "outcome"] == 1 and out.loc[df.index[0], "days_held"] == 2
    # day1 entry at 104; stop 98.8; nothing hits within 3 days -> timeout at close of day4
    assert out.loc[df.index[1], "outcome"] == 0
    assert np.isclose(out.loc[df.index[1], "trade_ret"], 100 / 104 - 1)
    # last 3 rows lack future data
    assert out.iloc[-3:].isna().all().all()


def test_same_day_target_and_stop_counts_as_stop():
    df = _bars([100, 120, 100], [100, 80, 100], [100, 100, 100])
    out = triple_barrier(df, target=0.10, stop=0.05, horizon=1)
    assert out.iloc[0]["outcome"] == -1


def test_filters_are_point_in_time_and_rank_cross_sectionally():
    panel = apply_filters(build_panel(synthetic_universe(n=10, n_days=600)), FilterConfig(min_price=0, min_dollar_volume=0))
    ranks = panel["rs_rank"].dropna().groupby(level="date")
    assert (ranks.max() == 1.0).all()
    assert panel["passes"].dtype == bool
