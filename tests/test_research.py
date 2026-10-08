import numpy as np
import pandas as pd

from mlalgo.data import synthetic
from mlalgo.research import engine
from mlalgo.research.entries import all_signals, bars
from mlalgo.trade_sim import ExitConfig, simulate

CODES = {k: v[0] for k, v in engine.EXITS.items()}


def _sim(df, t, entry, stop, code, cost=0.0):
    b = bars(df)
    ret, R, xidx, reason = engine.simulate_all(
        b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["sma50"], b["ema8"], b["ema21"], b["ema50"],
        b["atr20"], b["low10prev"], np.array([t]), np.array([entry]), np.array([stop]), np.array([code]), 250, cost)
    return ret[0, 0], R[0, 0], xidx[0, 0], reason[0, 0]


def test_trim_ema_matches_original_simulator():
    df = synthetic(1500, seed=7)
    c, l = df["close"].to_numpy(), df["low"].to_numpy()
    for t in range(300, 1400, 37):
        sig = pd.DataFrame({"idx": [t], "setup": ["x"], "entry": [c[t]], "stop": [min(l[t], c[t] * 0.97)]})
        ref = simulate(df, sig, ExitConfig(target_r=2.0, cost_pct=0.001)).iloc[0]
        ret, R, xidx, _ = _sim(df, t, c[t], sig["stop"][0], CODES["trim_ema"], 0.001)
        assert np.isclose(ret, ref["ret"]) and np.isclose(R, ref["R"]) and xidx - t == ref["days"]


def _df(close, high=None, low=None, open_=None):
    close = np.asarray(close, float)
    idx = pd.bdate_range("2020-01-01", periods=len(close))
    return pd.DataFrame({"open": close if open_ is None else open_, "high": close * 1.005 if high is None else high,
                         "low": close * 0.995 if low is None else low, "close": close, "volume": 1e6}, index=idx)


def test_oneil_takes_20pct_and_caps_stop_at_8pct():
    close = np.r_[np.linspace(50, 100, 100), [104, 110, 116, 121, 130]]
    df = _df(close, open_=close * 0.99)     # day 103 opens at 119.8, trades through 120
    ret, R, xidx, reason = _sim(df, 99, 100.0, 80.0, CODES["oneil_20_8"])   # 20% stop gets capped to 8%
    assert reason == 3 and np.isclose(ret, 0.20) and np.isclose(R, 0.20 / 0.08) and xidx == 103


def test_qull_partial_on_day5_then_trail_10sma():
    up = np.linspace(50, 100, 100)
    close = np.r_[up, [102, 104, 106, 108, 110, 112, 90]]
    df = _df(close)
    ret, R, xidx, reason = _sim(df, 99, 100.0, 97.0, CODES["qull_sma10"])
    # day 5 (close 110): sell 1/3; stop -> 100. Next day 112 holds; then 90 opens below the
    # breakeven stop -> remaining 2/3 filled at the open (90).
    expected = (1 / 3) * 0.10 + (2 / 3) * (90 / 100 - 1)
    assert np.isclose(ret, expected) and reason == 1


def test_flag_detector_finds_textbook_flag():
    run = np.linspace(20, 40, 40)                        # +100% run-up
    flag_ = 40 - 2 * np.abs(np.sin(np.linspace(0, 3, 15))) * np.linspace(1, 0.3, 15)  # shallow, higher lows
    close = np.r_[np.full(120, 20.0), run, flag_, [41.5]]
    high = close * 1.01
    high[159] = 40.5                                    # pivot = top of the run
    low = close * 0.99
    vol = np.r_[np.full(len(close) - 1, 1e6), 3e6]
    df = pd.DataFrame({"open": close, "high": high, "low": low, "close": close, "volume": vol},
                      index=pd.bdate_range("2020-01-01", periods=len(close)))
    b = bars(df)
    t, move, depth, days = engine.flag_signals(b["h"], b["l"], b["c"], b["v"], b["vol50"], b["sma20"], b["adr"],
                                               0.3, 60, 5, 40, 0.25, 0.0, 1.2, False)
    assert list(t) == [len(close) - 1] and move[0] > 0.9 and depth[0] < 0.25


def test_research_signals_do_not_use_future_data():
    df = synthetic(1200, seed=11)
    df["volume"] *= 5
    cut = 900
    base = all_signals(df, bars(df))
    tampered = df.copy()
    tampered.iloc[cut:] *= np.linspace(1, 3, len(df) - cut)[:, None]
    after = all_signals(tampered, bars(tampered))
    cols = ["idx", "entry_name", "entry", "stop"]
    key = lambda s: s[s["idx"] < cut][cols].sort_values(cols[:2]).reset_index(drop=True)
    pd.testing.assert_frame_equal(key(base), key(after))
