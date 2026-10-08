import numpy as np
import pandas as pd

from mlalgo.data import synthetic
from mlalgo.fundamentals import paper_score, parse_fundamentals
from mlalgo.setups import SetupConfig, find_signals
from mlalgo.trade_sim import ExitConfig, simulate


def _df(close, high=None, low=None, volume=None, open_=None):
    close = np.asarray(close, float)
    idx = pd.bdate_range("2020-01-01", periods=len(close))
    return pd.DataFrame({
        "open": close if open_ is None else open_,
        "high": close * 1.01 if high is None else high,
        "low": close * 0.99 if low is None else low,
        "close": close,
        "volume": np.full(len(close), 1e6) if volume is None else volume,
    }, index=idx)


def test_signals_do_not_use_future_data():
    df = synthetic(900, seed=3)
    cut = 700
    base = find_signals(df)
    tampered = df.copy()
    tampered.iloc[cut:] *= np.linspace(1, 2, len(df) - cut)[:, None]
    after = find_signals(tampered)
    cols = ["idx", "setup", "entry", "stop"]
    b = base[base["idx"] < cut][cols].reset_index(drop=True)
    a = after[after["idx"] < cut][cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(b, a)


def test_breakout_detected_on_volume_through_twice_tested_level():
    # uptrend, then a 40-day flat base under 110 that tags the level twice, then a volume breakout
    up = np.linspace(60, 105, 200)
    base = np.full(40, 105.0)
    high_base = base * 1.01
    high_base[[5, 25]] = 110.0                       # two separate rejections at 110
    close = np.r_[up, base, 112.0]
    high = np.r_[up * 1.01, high_base, 113.0]
    low = np.r_[up * 0.99, base * 0.99, 109.0]
    vol = np.r_[np.full(240, 1e6), 3e6]
    sig = find_signals(_df(close, high, low, vol), SetupConfig(), which=("breakout",))
    assert len(sig) == 1 and sig.iloc[0]["idx"] == 240
    assert np.isclose(sig.iloc[0]["level"], 110.0)
    no_vol = find_signals(_df(close, high, low, np.full(241, 1e6)), SetupConfig(), which=("breakout",))
    assert no_vol.empty  # no volume confirmation -> no signal


def test_trim_plan():
    # entry 100, stop 95 (R = 5): runs to 110 (2R target -> trim 1/4, stop to breakeven), then falls
    close = np.r_[np.linspace(50, 100, 120), [104, 108, 112, 99]]
    df = _df(close)
    sig = pd.DataFrame({"idx": [119], "setup": ["breakout"], "entry": [100.0], "stop": [95.0]})
    tr = simulate(df, sig, ExitConfig(target_r=2.0, cost_pct=0)).iloc[0]
    assert tr["hit_target"]
    # bar 3 opens at 112, above the 110 target -> 1/4 fills at the open (112); stop -> breakeven.
    # Next bar opens at 99, gapping below the breakeven stop -> the rest fills at 99.
    expected = 0.25 * 0.12 + 0.75 * (99 / 100 - 1)
    assert np.isclose(tr["ret"], expected) and tr["exit_reason"] == "breakeven"
    assert np.isclose(tr["R"], expected / 0.05)


def test_stop_and_target_same_bar_counts_as_stop():
    close = np.r_[np.linspace(50, 100, 120), [100]]
    high = close * 1.01
    low = close * 0.99
    high[-1], low[-1] = 120, 90
    df = _df(close, high, low)
    sig = pd.DataFrame({"idx": [119], "setup": ["breakout"], "entry": [100.0], "stop": [95.0]})
    tr = simulate(df, sig, ExitConfig(cost_pct=0)).iloc[0]
    assert tr["exit_reason"] == "stop" and np.isclose(tr["R"], -1)


def test_parse_fundamentals_and_overinvesting_flag():
    bs = pd.DataFrame({"2024": [120.0], "2023": [100.0]}, index=["Total Assets"])
    inc = pd.DataFrame({"2024": [11.0], "2023": [10.0]}, index=["EBITDA"])
    f = parse_fundamentals({"marketCap": 1e9, "freeCashflow": 5e7, "priceToBook": 2.0, "returnOnAssets": 0.1}, bs, inc)
    assert np.isclose(f["fcf_yield"], 0.05) and np.isclose(f["book_to_market"], 0.5)
    assert f["overinvesting"] == 1.0  # assets +20% vs EBITDA +10%
    scores = paper_score(pd.DataFrame([f, {**f, "fcf_yield": 0.10, "overinvesting": 0.0}]))
    assert scores.iloc[1] > scores.iloc[0]
