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
    # next-day stop orders (qull_breakout) legitimately use day idx+1 for the fill: stop one day early
    key = lambda s: s[s["idx"] < cut - 1][cols].sort_values(cols[:2]).reset_index(drop=True)
    pd.testing.assert_frame_equal(key(base), key(after))


def _pattern_df(top, bottom, breakout_close, n_pre=200):
    """Zig-zag between two trendlines (one swing every 6 bars), then a breakout bar."""
    rng = np.random.default_rng(0)
    pre = np.linspace(50, top[0] * 0.95, n_pre)
    body = []
    for i in range(len(top)):
        body.append(bottom[i] + (top[i] - bottom[i]) * (0.5 + 0.5 * np.cos(i * np.pi / 6)))
    close = np.r_[pre, body, [breakout_close]]
    high = close * 1.002
    low = close * 0.998
    vol = np.r_[np.full(len(close) - 1, 1e6), 3e6]
    return pd.DataFrame({"open": close, "high": high, "low": low, "close": close, "volume": vol},
                        index=pd.bdate_range("2015-01-01", periods=len(close)))


def _detect(df):
    b = bars(df)
    t, kind, *_ = engine.pattern_signals(b["h"], b["l"], b["c"], b["v"], b["vol50prev"], 60, 3, 0.0005, 0.02, 0.75, 1.2)
    return {int(i): int(k) for i, k in zip(t, kind)}


def test_ascending_triangle_and_falling_wedge_detected():
    n = 60
    asc = _pattern_df(np.full(n, 100.0), np.linspace(88, 98, n), 102.0)
    assert _detect(asc).get(len(asc) - 1) == engine.PATTERNS["asc_triangle"]
    wedge = _pattern_df(np.linspace(100, 92, n), np.linspace(88, 87, n) - np.linspace(0, 3, n) * 0 - np.linspace(0, 2, n), 93.5)
    assert _detect(wedge).get(len(wedge) - 1) == engine.PATTERNS["falling_wedge"]


def test_pattern_detector_does_not_use_future_data():
    df = synthetic(4000, seed=301)
    df["volume"] *= 5
    cut = 3000
    tampered = df.copy()
    tampered.iloc[cut:] *= np.linspace(1, 0.4, len(df) - cut)[:, None]

    def run(d):
        b = bars(d)
        t, kind, stop, *_ = engine.pattern_signals(b["h"], b["l"], b["c"], b["v"], b["vol50prev"],
                                                   60, 3, 0.0005, 0.02, 0.75, 1.2)
        keep = t < cut
        return t[keep], kind[keep], stop[keep]

    a, b_ = run(df), run(tampered)
    assert len(a[0]) >= 5  # the check must actually cover some patterns
    for x, y in zip(a, b_):
        np.testing.assert_array_equal(x, y)


def test_superperformer_label_and_features_are_point_in_time():
    from mlalgo.research.run import superperformer_sample
    from mlalgo.structure import structure_features
    df = synthetic(1200, seed=21)
    df["volume"] *= 5
    rs = pd.Series(0.5, index=df.index)
    s = superperformer_sample("T", df, structure_features(df), rs, None)
    row = s[s["fwd_max_gain"].notna()].iloc[3]
    t = df.index.get_loc(row["date"])
    expected = df["high"].iloc[t + 1:t + 64].max() / df["close"].iloc[t] - 1
    assert np.isclose(row["fwd_max_gain"], expected, rtol=1e-5)
    # features must not change when the future changes
    tampered = df.copy()
    tampered.iloc[t + 1:] *= 2
    s2 = superperformer_sample("T", tampered, structure_features(tampered), rs, None)
    labels = (["fwd_max_gain", "fwd_ret_63", "clean_super"] + [c for c in s.columns if c[:3] in ("b10", "b20")]
              + [c for c in s.columns if c.startswith(("y_", "r_"))])
    a = s[s["date"] == row["date"]].drop(columns=labels).reset_index(drop=True)
    b = s2[s2["date"] == row["date"]].drop(columns=labels).reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)
    # clean label: +40% (high) reached before a -20% low within 63 days
    c0 = df["close"].iloc[t]
    hs, ls = df["high"].iloc[t + 1:t + 64].to_numpy(), df["low"].iloc[t + 1:t + 64].to_numpy()
    up = np.flatnonzero(hs >= 1.4 * c0)
    dn = np.flatnonzero(ls <= 0.8 * c0)
    expect_clean = len(up) > 0 and (len(dn) == 0 or up[0] < dn[0])
    assert row["clean_super"] == float(expect_clean)


def test_bracket_outcome_target_stop_gap_and_timeout():
    from mlalgo.research.run import bracket_outcome
    #            day: 0    1    2    3    4
    o = np.array([100, 101, 104, 108, 100.0])
    h = np.array([100, 103, 111, 109, 101.0])
    l = np.array([100,  99, 103, 107,  99.0])
    c = np.array([100, 102, 108, 108, 100.0])
    # entry day 0 at 100: day 2 high 111 >= 110 -> +10% target (open 104 < 110, so fills at 110)
    hit, ret, xi = bracket_outcome(o, h, l, c, np.array([0]), 0.10, 0.10, 3, cost=0)
    assert hit[0] == 1 and np.isclose(ret[0], 0.10) and xi[0] == 2
    # +20% never reached within 3 days and no -10% -> closes at day 3 close (108)
    hit, ret, xi = bracket_outcome(o, h, l, c, np.array([0]), 0.20, 0.10, 3, cost=0)
    assert hit[0] == 0 and np.isclose(ret[0], 0.08) and xi[0] == 3
    # gap down through the stop fills at the open; same-bar target+stop counts as the stop
    o2, h2, l2, c2 = (np.array([100, 85.0]), np.array([100, 125.0]), np.array([100, 80.0]), np.array([100, 90.0]))
    hit, ret, _ = bracket_outcome(o2, h2, l2, c2, np.array([0]), 0.20, 0.10, 3, cost=0)
    assert hit[0] == -1 and np.isclose(ret[0], -0.15)


def test_engine_bracket_exit_matches_label_logic():
    from mlalgo.research.run import bracket_outcome
    df = synthetic(900, seed=12)
    b = bars(df)
    for t in range(300, 800, 50):
        e = b["c"][t]
        for code, up in ((CODES["bracket_10_10"], 0.10), (CODES["bracket_20_10"], 0.20)):
            ret, _, xidx, _ = _sim(df, t, e, e * 0.5, code, cost=0.001)
            _, r2, x2 = bracket_outcome(b["o"], b["h"], b["l"], b["c"], np.array([t]), up, 0.10, 63)
            assert np.isclose(ret, r2[0]) and xidx == x2[0]


def test_picks_drops_todays_partial_bar_only_before_the_close(monkeypatch):
    import picks
    from datetime import datetime, timezone
    idx = pd.to_datetime(["2026-10-06", "2026-10-07", "2026-10-08"])
    dfs = {"X": pd.DataFrame({"close": [1.0, 2.0, 3.0]}, index=idx)}

    class Morning(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 10, 8, 14, 30, tzinfo=timezone.utc)

    class Evening(Morning):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 10, 8, 22, 30, tzinfo=timezone.utc)

    monkeypatch.setattr(picks, "datetime", Morning)
    assert len(picks.trim_incomplete(dfs)["X"]) == 2
    monkeypatch.setattr(picks, "datetime", Evening)
    assert len(picks.trim_incomplete(dfs)["X"]) == 3


def test_qull_breakout_fills_at_pivot_or_gap_open():
    run = np.linspace(20, 40, 40)
    flag_ = 39 - 1.5 * np.abs(np.sin(np.linspace(0, 3, 15))) * np.linspace(1, 0.3, 15)
    close = np.r_[np.full(120, 20.0), run, flag_, [41.0]]
    high = close * 1.01
    high[159] = 40.5          # pivot
    low = close * 0.99
    open_ = close.copy()
    open_[-1] = 40.0          # opens below the pivot, trades through it
    df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": 1e6},
                      index=pd.bdate_range("2020-01-01", periods=len(close)))
    b = bars(df)
    t, fill, stop, *_ = engine.qull_setups(b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["adr"],
                                           0.3, 60, 5, 40, 0.25, 0.0)
    assert list(t) == [len(close) - 2]                     # setup known at the prior close
    assert np.isclose(fill[0], 40.5 * 1.001)               # filled at the trigger, not the close
    assert stop[0] < fill[0]


def test_forward_tracker_scores_logged_picks(tmp_path):
    import picks
    idx = pd.bdate_range("2026-01-01", periods=80)
    close = np.r_[np.full(10, 100.0), np.linspace(100, 125, 70)]
    df = pd.DataFrame({"open": close, "high": close * 1.01, "low": close * 0.99, "close": close}, index=idx)
    day = idx[9]
    p = pd.DataFrame({"date": [day], "ticker": ["X"], "close": [100.0], "p_b20": [0.4], "p_b10": [0.6]})
    picks.track_forward(tmp_path, {"X": df}, p, p.iloc[:0], day, str(tmp_path))
    out = pd.read_csv(tmp_path / "forward_test.csv")
    assert out.loc[0, "b20_result"] == "target" and np.isclose(out.loc[0, "b20_ret"], 0.198)
    assert (tmp_path / "picks_history.csv").exists() and (tmp_path / "forward_test.md").exists()


def test_short_features_point_in_time_and_labels():
    from mlalgo.research.shortterm import short_features, short_labels
    df = synthetic(900, seed=31)
    cut = 600
    t2 = df.copy()
    t2.iloc[cut:] *= 1.7
    a, b = short_features(df).iloc[:cut], short_features(t2).iloc[:cut]
    pd.testing.assert_frame_equal(a, b)
    lab = short_labels(df)
    t = 100
    c, o = df["close"].to_numpy(), df["open"].to_numpy()
    assert lab["y_up1"].iloc[t] == float(c[t + 1] > c[t])
    assert lab["y_green1"].iloc[t] == float(c[t + 1] > o[t + 1])
    assert np.isclose(lab["r_up5"].iloc[t], c[t + 5] / c[t] - 1, rtol=1e-5)
