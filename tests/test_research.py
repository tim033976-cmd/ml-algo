import re

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
        b["atr20"], b["low10prev"], b["wkx"], np.array([t]), np.array([entry]), np.array([stop]), np.array([code]), 250, cost)
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
              + [c for c in s.columns if c.startswith(("y_", "r_"))]
              + [c for c in s.columns if re.fullmatch(r"m\d+_\d+_(ret|days)", c)])
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


def test_bracket_menu_columns_match_bracket_outcome_and_portfolio_exit_dates():
    from mlalgo.research import analyze as A
    from mlalgo.research.run import MENU, bracket_outcome, superperformer_sample
    from mlalgo.structure import structure_features
    df = synthetic(1200, seed=21)
    df["volume"] *= 5
    s = superperformer_sample("T", df, structure_features(df), pd.Series(0.5, index=df.index), None)
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    known = s[s["fwd_max_gain"].notna()]
    idx = np.array([df.index.get_loc(d) for d in known["date"]])
    for key, (up, dn) in MENU.items():
        _, ret, xi = bracket_outcome(o, h, l, c, idx, up, dn, 63)
        assert np.allclose(known[f"{key}_ret"], ret, rtol=1e-5)
        assert (known[f"{key}_days"].to_numpy() == xi - idx).all()
    # +20/-10 in the menu is the goal label
    assert np.allclose(known["m20_10_ret"], known["b20_ret"])
    # exit dates rebuilt from days held land on the real exit bar
    s2 = known.assign(score=np.arange(len(known), dtype=float))
    tr = A.menu_trades(s2, "m15_8", 0.08, "score", df.index, q=0)
    j = np.array([df.index.get_loc(d) for d in tr["date"]]) + s2["m15_8_days"].to_numpy()
    assert (tr["exit_bracket"].to_numpy() == df.index[j].to_numpy()).all()
    assert (tr["risk_pct"] == 0.08).all()


def test_group_frames_sector_rank_is_percentile_among_sectors():
    from mlalgo.research.run import group_frames
    idx = pd.date_range("2020-01-01", periods=3)
    tick = [f"T{i}" for i in range(9)]
    # three sectors of three stocks; sector C strongest, A weakest
    rank = pd.DataFrame([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]] * 3, index=idx, columns=tick)
    u = pd.DataFrame({"ticker": tick, "sector": ["A"] * 3 + ["B"] * 3 + ["C"] * 3, "sub_industry": ["x"] * 9})
    g = group_frames(rank, u, tick)
    assert np.allclose(g["T0"]["sector_rank"], 1 / 3) and np.allclose(g["T8"]["sector_rank"], 1.0)
    assert np.allclose(g["T4"]["sector_rs"], 0.5)


def test_workflow_rocket_exit_sells_third_at_25pct_then_breakeven_stop():
    # flat at 100 (50 SMA = 100), entry at 100; next day +26% high closes 120; then a dip to 99
    close = [100.0] * 300 + [120.0, 105.0]
    high = [100.5] * 300 + [126.0, 110.0]
    low = [99.5] * 300 + [101.0, 99.0]
    open_ = [100.0] * 300 + [101.0, 110.0]
    df = _df(close, high, low, open_)
    ret, _, xidx, reason = _sim(df, 299, 100.0, 92.0, CODES["wf_rocket"])
    # 1/3 sold at 125 (+25%), stop moved to 100 and hit on the next bar: (1/3) * 25% overall
    assert np.isclose(ret, 0.25 / 3) and xidx == 301 and reason == 1


def test_workflow_weekly_exit_only_on_completed_weeks():
    df = synthetic(600, seed=5)
    b = bars(df)
    wkx = pd.Series(b["wkx"], index=df.index)
    fired = wkx[wkx > 0].index
    assert len(fired) > 0
    nxt = df.index.to_series().shift(-1)
    # every exit signal is on the last trading day of its week, never on the last (unfinished) bar
    assert all(nxt[d] is pd.NaT or nxt[d].to_period("W-FRI") != d.to_period("W-FRI") for d in fired)
    assert wkx.iloc[-1] == 0
    # changing future prices doesn't change earlier triggers
    t = 400
    tampered = df.copy()
    tampered.iloc[t:] *= 0.5
    w2 = bars(tampered)["wkx"]
    assert (b["wkx"][:t] == w2[:t]).all()
    # it fires when the weekly close is below the 10-week MA
    wc = df["close"].groupby(df.index.to_period("W-FRI")).last()
    below = (wc < wc.rolling(10).mean())
    d = fired[5]
    assert below[d.to_period("W-FRI")]


def test_workflow_gap_hold_waits_two_days_and_stops_under_gap_low():
    from mlalgo.research.entries import wf_gap_hold
    n = 80
    close = np.full(n, 50.0)
    open_, high, low = close.copy(), close * 1.005, close * 0.995
    g = 70
    open_[g], close[g], high[g], low[g] = 54.0, 55.0, 56.0, 53.0      # +8% gap
    for k in (71, 72):
        open_[k], close[k], high[k], low[k] = 55.0, 55.5, 56.0, 54.0   # holds above 53
    close[73:], open_[73:], high[73:], low[73:] = 55.0, 55.0, 55.5, 54.5
    df = _df(close, high, low, open_)
    df.loc[df.index[g], "volume"] = 5e6
    s = wf_gap_hold(bars(df))
    assert list(s["idx"]) == [72] and np.isclose(s["stop"].iloc[0], 53.0 * 0.995)
    # a day that undercuts the gap-day low cancels it
    low2 = low.copy()
    low2[71] = 52.0
    assert wf_gap_hold(bars(_df(close, high, low2, open_).assign(volume=df["volume"]))).empty


def test_market_internals_ad_line_and_2150_codes():
    from mlalgo.research.run import _above_2150, market_internals
    idx = pd.bdate_range("2020-01-01", periods=120)
    up = pd.DataFrame({"close": np.linspace(10, 20, 120)}, index=idx)
    down = pd.DataFrame({"close": np.linspace(20, 10, 120)}, index=idx)
    m = market_internals({"A": up, "B": up.copy(), "C": down})
    # 2 advancers, 1 decliner every day -> the A/D line rises by 1 a day and sits above its averages
    assert m["ad_2150"].iloc[-1] == 3 and np.isclose(m["ad_chg10"].iloc[-1], 10 / 3)
    assert np.isclose(m["breadth_20"].iloc[-1], 2 / 3)
    # codes: rising series above both, falling below both, NaN before 50 bars
    assert _above_2150(up["close"]).iloc[-1] == 3 and _above_2150(down["close"]).iloc[-1] == 0
    assert np.isnan(_above_2150(up["close"]).iloc[30])


def test_group_momentum_uses_member_median_and_is_point_in_time():
    from mlalgo.research.run import group_momentum
    idx = pd.bdate_range("2020-01-01", periods=60)
    px = {t: pd.DataFrame({"close": 100 * (1 + r) ** np.arange(60)}, index=idx)
          for t, r in (("a", 0.01), ("b", 0.02), ("c", 0.03), ("d", -0.01), ("e", -0.01))}
    g = pd.Series({"a": "tech", "b": "tech", "c": "tech", "d": "small", "e": "small"})
    m = group_momentum(px, g)
    assert np.isclose(m["ret1"]["tech"].iloc[-1], 0.02)          # median of 1%, 2%, 3%
    assert m["ret1"]["small"].isna().all()                       # fewer than 3 members
    assert np.isclose(m["ret5"]["tech"].iloc[-1], 1.02 ** 5 - 1) and m["up21"]["tech"].iloc[-1] == 1
    # tampering with the future doesn't change the past
    px2 = {t: d.assign(close=d["close"].where(d.index < idx[40], d["close"] * 0.5)) for t, d in px.items()}
    m2 = group_momentum(px2, g)
    pd.testing.assert_frame_equal(m["ret5"].iloc[:40], m2["ret5"].iloc[:40])


def test_parabolic_short_trigger_stop_and_cover():
    from mlalgo.research import shorts
    # 40 flat days at 10, then a parabolic run to ~16.5 in 6 days, then weakness and a fade
    close = [10.0] * 40 + [11, 12, 13.2, 14.5, 15.5, 16.5] + [15.0, 13.0, 12.0, 11.0, 10.5, 10.2, 10.0, 10.0]
    high = [c * 1.01 for c in close]
    low = [c * 0.99 for c in close]
    low[46] = 14.8                       # day 46 closes 15.0 < prior low (16.5 * 0.99): the trigger
    df = _df(close, high, low, close)
    s = shorts.signals(df)
    trig = s[s["variant"] == "trigger"]
    assert len(trig) == 1 and trig["idx"].iloc[0] == 46
    assert np.isclose(trig["stop"].iloc[0], 16.5 * 1.01)
    r = shorts.simulate(df, trig, cost=0.0)
    # covers when the low reaches yesterday's 10-day average (a profit), never stopped out
    assert r["R_sma10"].iloc[0] > 0 and r["R_sma20"].iloc[0] >= r["R_sma10"].iloc[0] - 1e-9
    # a squeeze through the stop is a loss of about -1R or worse (gap fills at the open)
    close2 = close[:47] + [18.0] * 7
    df2 = _df(close2, [c * 1.01 for c in close2], [c * 0.99 for c in close2], close2)
    r2 = shorts.simulate(df2, trig, cost=0.0)
    assert r2["R_sma10"].iloc[0] <= -1.0


def test_parabolic_short_signals_do_not_use_future_data():
    from mlalgo.research import shorts
    df = synthetic(1500, seed=3)
    df["close"] = df["close"] * np.exp(np.r_[np.zeros(700), np.linspace(0, 1.2, 10), np.full(790, 1.2)])
    df["high"], df["low"], df["open"] = df["close"] * 1.02, df["close"] * 0.98, df["close"]
    base = shorts.signals(df)
    cut = 760
    tampered = df.copy()
    tampered.iloc[cut:] *= 0.3
    after = shorts.signals(tampered)
    key = lambda s: s[s["idx"] < cut][["idx", "variant", "entry", "stop"]].reset_index(drop=True)
    pd.testing.assert_frame_equal(key(base), key(after))


def test_momentum_portfolio_picks_vol_adjusted_leaders_and_breadth_timing():
    from mlalgo.research import analyze as A
    idx = pd.bdate_range("2015-01-01", periods=400)
    rng = np.random.default_rng(0)
    # 'smooth' rises steadily, 'wild' rises the same on average but with big noise, 'flat' doesn't rise
    smooth = 100 * np.exp(np.cumsum(np.full(400, 0.002)))
    wild = 100 * np.exp(np.cumsum(0.002 + rng.normal(0, 0.04, 400)))
    flat = 100 * np.exp(np.cumsum(rng.normal(0, 0.005, 400)))
    closes = pd.DataFrame({"smooth": smooth, "wild": wild, "flat": flat}, index=idx)
    r = A.momentum_portfolio(closes, closes * 1e6, top=1, cost=0.0)
    # after the warm-up, holding 'smooth' only: daily return = its 0.2% drift
    late = r[r.index >= idx[300]]
    assert np.allclose(late, np.exp(0.002) - 1, atol=1e-9)
    # breadth timing: in the market only between a < 20% reading and a > 60% reading, from the next day
    spy = pd.Series(np.linspace(100, 110, 10), index=idx[:10])
    br = pd.Series([0.5, 0.1, 0.3, 0.7, 0.5, 0.15, 0.5, 0.5, 0.65, 0.5], index=idx[:10])
    t = A.breadth_timing(spy, br)
    held = (t != 0).astype(int).tolist()
    assert held == [0, 0, 1, 1, 0, 0, 1, 1, 1, 0]


def test_in_sp500_uses_membership_spells():
    from mlalgo.research.data import in_sp500
    hist = pd.DataFrame({"ticker": ["A", "A", "B"], "start": pd.to_datetime(["2010-01-01", "2015-01-01", "2012-01-01"]),
                         "end": pd.to_datetime(["2012-01-01", None, "2013-01-01"])})
    d = pd.DataFrame({"ticker": ["A", "A", "A", "B", "B", "C"],
                      "date": pd.to_datetime(["2011-06-01", "2013-06-01", "2020-01-01", "2012-06-01", "2014-01-01", "2012-06-01"])})
    assert in_sp500(d, hist).tolist() == [True, False, True, True, False, False]


def test_replay_picks_trains_only_on_closed_labels(monkeypatch):
    from mlalgo.research import analyze as A
    rng = np.random.default_rng(0)
    dates = pd.bdate_range("2020-01-01", periods=60, freq="10B")
    rows = []
    for i, d in enumerate(dates):
        for t in range(150):
            rows.append({"date": d, "ticker": f"T{t}", "close": 20.0, "dollar_vol_50": 1e7, "rs_rank": rng.random(),
                         "dist_52w_high": -0.1, "dist_sma50": 0.05, "fwd_max_gain": 0.1, "b20_hit": float(rng.random() < 0.3),
                         "b20_ret": rng.normal(0, 0.1), "label_end": d + pd.Timedelta(days=91), "f1": rng.random()})
    s = pd.DataFrame(rows)
    seen = []
    real = A._super_model

    class Spy:
        def fit(self, X, y):
            seen.append(len(X))
            self.m = real().fit(X, y)
            return self

        def predict_proba(self, X):
            return self.m.predict_proba(X)

    monkeypatch.setattr(A, "_super_model", Spy)
    rep = A.replay_picks(s, start=str(dates[40].date()), features=["f1"], retrain_days=91)
    # first training date: only rows whose label window ended before it
    first = dates[40]
    assert seen[0] == int((s["label_end"] < first).sum())
    assert set(rep["list"]) == {"all", "leaders"} and rep.groupby(["date", "list"]).size().max() == 10


def test_leader_rotation_mechanics():
    from mlalgo.research import rotation as R
    idx = pd.bdate_range("2010-01-01", periods=600)
    g = np.arange(600)
    up = lambda r: 50 * np.exp(r * g)
    closes = pd.DataFrame({"fast": up(0.003), "mid": up(0.002), "slow": up(0.001), "flat": np.full(600, 50.0)}, index=idx)
    # 'mid' crashes 20% on day 450 (stop), 'slow' stops trading on day 500 (delisted)
    closes.loc[idx[450]:, "mid"] *= 0.8
    closes.loc[idx[500]:, "slow"] = np.nan
    dv = closes * 1e6
    P = R.prepare(closes, dv)
    res = R.run(P, n=2, start=str(idx[300].date()), cost=0.0)
    tr = res["trades"]
    # the two strongest leaders are bought first; 'flat' is never a leader
    assert "flat" not in set(P["tickers"][j] for j in tr["j"])
    assert any(P["tickers"][j] == "mid" and t_out == 450 for j, t_out in zip(tr["j"], tr["t_out"]))   # 8% stop
    assert any(P["tickers"][j] == "slow" for j in tr["j"])                                            # sold after delisting
    assert set(res["open"]["ticker"]) <= {"fast", "mid", "slow"} and "fast" in set(res["open"]["ticker"])
    # equity: holding 'fast' (+0.3%/day) and one other, never worse than flat
    assert res["curve"].iloc[-1] > 1.0
    s = R.stats(res, pd.Timestamp("2011-06-01"))
    assert {"IS_CAGR", "OOS_CAGR", "OOS_maxDD"} <= set(s)
