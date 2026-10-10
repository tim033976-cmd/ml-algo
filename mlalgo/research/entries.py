"""Entry setups from published / professional breakout methods, on daily bars.

Every signal is fully known at the close of its day and is entered at that close.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from mlalgo import setups as playbook
from mlalgo.indicators import ema
from mlalgo.research import engine


np.seterr(divide="ignore", invalid="ignore")  # zero-volume days produce inf/nan ratios; cleaned below


def bars(df: pd.DataFrame) -> dict[str, np.ndarray]:
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))
    prev = c.shift()
    tr = pd.concat([h - l, (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1)
    b = {
        "o": o, "h": h, "l": l, "c": c, "v": v,
        "sma10": c.rolling(10).mean(), "sma20": c.rolling(20).mean(), "sma50": c.rolling(50).mean(),
        "sma150": c.rolling(150).mean(), "sma200": c.rolling(200).mean(),
        "ema8": ema(c, 8), "ema21": ema(c, 21), "ema50": ema(c, 50),
        "atr20": tr.rolling(20).mean(), "adr": (h / l - 1).rolling(20).mean(),
        "vol50": v.rolling(50).mean(), "low10prev": l.rolling(10).min().shift(1),
    }
    b["vol50prev"] = b["vol50"].shift(1)
    # run 20: weekly close below the 10-week MA (known at the week's last close; 1.0 = exit signal)
    week_end = pd.Series(c.index.to_period("W-FRI"), index=c.index)
    is_end = week_end != week_end.shift(-1)
    if len(c):
        is_end.iloc[-1] = False  # the last bar's week may not be finished
    wc = c[is_end]
    wma = wc.rolling(10).mean()
    b["wkx"] = ((wc < wma).astype(float)).reindex(c.index).fillna(0.0)
    return {k: s.to_numpy(np.float64) for k, s in b.items()}


def _frame(idx, stop, **extra) -> pd.DataFrame:
    return pd.DataFrame({"idx": np.asarray(idx, dtype=np.int64), "stop": np.asarray(stop, float), **extra})


def _rmax(x, n, shift=1):
    return pd.Series(x).rolling(n).max().shift(shift).to_numpy()


def _rmin(x, n, shift=1):
    return pd.Series(x).rolling(n).min().shift(shift).to_numpy()


def _shift(x, k):
    return pd.Series(x).shift(k).to_numpy()


def _strength(b):
    rng = b["h"] - b["l"]
    return np.where(rng > 0, (b["c"] - b["l"]) / np.where(rng > 0, rng, 1), 0.5)


# ------------------------------------------------------------------ entries
def donchian(b, n):
    """Turtle / trading-range break: close above the prior n-day high. Stop = 2 ATR."""
    hh = _rmax(b["h"], n)
    sig = (b["c"] > hh) & (_shift(b["c"], 1) <= _shift(hh, 1))
    t = np.flatnonzero(sig)
    return _frame(t, b["c"][t] - 2 * b["atr20"][t])


def high52(b, fresh):
    """52-week-high breakout (George & Hwang 2004). fresh=True: after >= 20 days below the high."""
    hh = _rmax(b["h"], 252)
    sig = (b["c"] > hh) & (_shift(b["c"], 1) <= _shift(hh, 1))
    if fresh:
        sig &= _rmax(b["h"], 20) < _rmax(b["h"], 232, shift=21)
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t])


def base_breakout(b, L):
    """O'Neil / Darvas base: >= 30% prior advance, then an L-day base 8-35% deep whose high is
    at least 10 days old; breakout on >= 1.4x volume closing in the upper half of the bar."""
    level = _rmax(b["h"], L - 10, shift=11)
    recent = _rmax(b["h"], 10)
    depth = (level - _rmin(b["l"], L)) / level
    prior = _shift(b["c"], L) / _rmin(b["l"], 126, shift=L + 1)
    sig = ((recent <= level) & (b["c"] > level) & (depth >= 0.08) & (depth <= 0.35) & (prior >= 1.3)
           & (b["v"] >= 1.4 * b["vol50prev"]) & (_strength(b) >= 0.5))
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t], base_depth=depth[t])


def vcp(b):
    """Minervini VCP: trend template, three shrinking 20-day contractions (last <= 12%),
    volume dry-up, then a breakout above the final contraction's high on >= 1.4x volume.
    Stop = low of the last 10 days."""
    c, s50, s150, s200 = b["c"], b["sma50"], b["sma150"], b["sma200"]
    tt = (c > s50) & (s50 > s150) & (s150 > s200) & (s200 > _shift(s200, 21))
    tt = _shift(tt.astype(float), 1) == 1

    def leg(off):
        hi, lo = _rmax(b["h"], 20, shift=off), _rmin(b["l"], 20, shift=off)
        return (hi - lo) / hi

    r1, r2, r3 = leg(41), leg(21), leg(1)
    dry = _shift(pd.Series(b["v"]).rolling(10).mean().to_numpy(), 1) / b["vol50prev"]
    pivot = _rmax(b["h"], 20)
    sig = tt & (r3 < r2) & (r2 < r1) & (r3 <= 0.12) & (dry <= 0.9) & (c > pivot) & (b["v"] >= 1.4 * b["vol50prev"])
    t = np.flatnonzero(sig)
    return _frame(t, _rmin(b["l"], 10)[t], contraction=(r3 / r1)[t])


def flag(b, min_move, run_window=60, max_flag=40, early=False):
    """Qullamaggie flag / high-tight flag (see engine.flag_signals). Stop = low of day."""
    t, move, depth, days = engine.flag_signals(
        b["h"], b["l"], b["c"], b["v"], b["vol50"], b["sma20"], b["adr"],
        min_move, run_window, 5, max_flag, 0.25, 0.03, 1.2, early)
    return _frame(t, b["l"][t], prior_move=move, flag_depth=depth, flag_days=days)


def episodic_pivot(b, gap, neglected=False, vol_mult=3.0, hold=False):
    """Episodic pivot / gap-and-go: gap up >= gap on >= 3x volume, closing in the upper half.
    neglected=True: stock hadn't already run (<= +20% over the prior 6 months)."""
    c_prev = _shift(b["c"], 1)
    g = b["o"] / c_prev - 1
    sig = (g >= gap) & (b["v"] >= vol_mult * b["vol50prev"]) & (_strength(b) >= 0.5)
    if hold:  # closed above the open: buyers held the gap all day
        sig &= b["c"] > b["o"]
    if neglected:
        sig &= (c_prev / _shift(b["c"], 127) - 1) <= 0.2
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t])


def pocket_pivot(b):
    """Morales & Kacher pocket pivot: up day with volume above every down-day volume of the
    prior 10 days, near the 10-day line, in an uptrend (above a rising 50-day)."""
    c, v = b["c"], b["v"]
    down_vol = np.where(c < _shift(c, 1), v, 0.0)
    maxdown = _rmax(down_vol, 10)
    sig = ((c > _shift(c, 1)) & (maxdown > 0) & (v > maxdown) & (c >= 0.99 * b["sma10"]) & (c <= 1.04 * b["sma10"])
           & (c > b["sma50"]) & (b["sma50"] > _shift(b["sma50"], 10)))
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t])


def stage2(b):
    """Weinstein stage 1 -> 2: breakout above a 100-day base (<= 40% deep) while the 30-week
    (150-day) average was flat during the base and is now flat-to-rising; >= 2x volume."""
    s150 = b["sma150"]
    hh, ll = _rmax(b["h"], 100), _rmin(b["l"], 100)
    depth = (hh - ll) / hh
    slope_now = s150 / _shift(s150, 20) - 1
    slope_then = _shift(s150, 50) / _shift(s150, 70) - 1
    sig = ((b["c"] > hh) & (depth <= 0.40) & (slope_now >= -0.005) & (np.abs(slope_then) <= 0.03)
           & (b["c"] > s150) & (b["v"] >= 2 * b["vol50prev"]))
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t], base_depth=depth[t])


def chart_pattern(b, kind, window=60):
    """Wedges / triangles from trendlines through confirmed swing points (engine.pattern_signals).
    Computed once per stock (stored on that stock's bar dict), then split by pattern type."""
    key = f"_patterns_{window}"
    if key not in b:
        b[key] = engine.pattern_signals(
            b["h"], b["l"], b["c"], b["v"], b["vol50prev"], window, 3, 0.0005, 0.02, 0.75, 1.2)
    t, kinds, stop, length, width, touches = b[key]
    sel = kinds == engine.PATTERNS[kind]
    return _frame(t[sel], np.minimum(stop[sel], b["l"][t[sel]]), pattern_len=length[sel],
                  pattern_width=width[sel], pattern_touches=touches[sel])


def tight_coil(b, days, adr_mult):
    """Tightness breakout: the last `days` closes sit within adr_mult x ADR of each other (a
    coiled spring), price above a rising 50-day; trigger is a close above the coil's high on
    >= 1.2x volume. Stop = bottom of the coil."""
    c = b["c"]
    rng = (_rmax(c, days) - _rmin(c, days)) / _shift(c, 1)
    coil_hi, coil_lo = _rmax(b["h"], days), _rmin(b["l"], days)
    sig = ((rng <= adr_mult * _shift(b["adr"], 1)) & (c > coil_hi) & (c > b["sma50"])
           & (b["sma50"] > _shift(b["sma50"], 20)) & (b["v"] >= 1.2 * b["vol50prev"]))
    t = np.flatnonzero(sig)
    return _frame(t, coil_lo[t], coil_range=rng[t])


def qull_breakout(b, min_move=0.30, max_flag=40):
    """Qullamaggie breakout with a realistic daily-chart order: setup known at the close, buy-stop
    above the pivot the next day (engine.qull_setups). Entry price is the fill, not the close."""
    t, fill, stop, move, depth, days = engine.qull_setups(
        b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["adr"], min_move, 60, 5, max_flag, 0.25, 0.035)
    return _frame(t, stop, fill=fill, prior_move=move, flag_depth=depth, flag_days=days)


def _playbook(fn):
    def run(b, df, **_):
        s = fn(df, playbook.SetupConfig(max_risk=1.0))
        return _frame(s["idx"], s["stop"])
    return run


# ------------------------------------------------------------------ run 20: the user's workflow PDF
def wf_rocket_breakout(b):
    """Workflow 'US rockets': breakout from a base of >= 6 weeks to a new 52-week high on >= 1.5x
    volume; not more than 5% above the breakout point. Stop 8% below entry."""
    old = _rmax(b["h"], 222, shift=31)          # the 52-week high as it stood 30+ days ago
    base = _rmax(b["h"], 30)                    # the last 30 days stayed at or below it
    sig = ((base <= old) & (b["c"] > old) & (b["c"] <= old * 1.05)
           & (b["v"] >= 1.5 * b["vol50prev"]))
    t = np.flatnonzero(sig)
    return _frame(t, b["c"][t] * 0.92)


def wf_gap_hold(b, gap=0.05, days=2):
    """Workflow 'earnings gap up >= 5% that holds above the gap-day low for 2-3 days': entry at the
    close `days` days after the gap if no low since undercut the gap-day low; stop just under it.
    No earnings dates in the data: a gap on >= 2x volume is the proxy."""
    g = b["o"] / _shift(b["c"], 1) - 1
    gday = (g >= gap) & (b["v"] >= 2.0 * b["vol50prev"])
    ok = _shift(gday.astype(float), days) == 1
    lows_after = pd.Series(b["l"]).rolling(days).min().to_numpy()   # lows of the `days` days after the gap
    gap_low = _shift(b["l"], days)
    sig = ok & (lows_after > gap_low)
    t = np.flatnonzero(sig)
    return _frame(t, gap_low[t] * 0.995)


def _uptrend_template(b):
    s50, s200 = b["sma50"], b["sma200"]
    return (b["c"] > s200) & (s200 > _shift(s200, 21)) & (s50 > s200) & (b["c"] >= 0.85 * _rmax(b["h"], 252, shift=0))


def wf_scan_pullback(b):
    """Workflow 'Nasdaq-100 scanner' entry: in an uptrend, a pullback to the 21 EMA or 50 SMA that
    holds (a low within 1% of the MA in the last 5 days, no close below it), then a close above the
    prior day's high. Stop just under the pullback low."""
    near21 = (b["l"] <= b["ema21"] * 1.01) & (b["c"] >= b["ema21"])
    near50 = (b["l"] <= b["sma50"] * 1.01) & (b["c"] >= b["sma50"])
    touched = pd.Series((near21 | near50).astype(float)).rolling(5).max().to_numpy() == 1
    sig = _uptrend_template(b) & touched & (b["c"] > _shift(b["h"], 1)) & (_shift(b["c"], 1) <= _shift(b["h"], 2))
    t = np.flatnonzero(sig)
    return _frame(t, _rmin(b["l"], 5, shift=0)[t] * 0.995)


def wf_scan_base(b):
    """Workflow scanner entry: in an uptrend, close above a base of >= 4 weeks (20 days, <= 25% deep).
    Stop just under the base low."""
    level = _rmax(b["h"], 20)
    lo = _rmin(b["l"], 20)
    depth = (level - lo) / level
    sig = _uptrend_template(b) & (b["c"] > level) & (_shift(b["c"], 1) <= _shift(level, 1)) & (depth <= 0.25)
    t = np.flatnonzero(sig)
    return _frame(t, lo[t] * 0.995, base_depth=depth[t])


# ------------------------------------------------------------------ run 24: Techno Charts course setups
def tc_ema_cross_base(b, window=60):
    """21/50 EMA bullish crossover, then the FIRST breakout from a tight 10-day base (<= 12% deep) on
    >= 1.5x volume within 60 days, while the 21 EMA is still above the 50. Stop: the base low."""
    e21, e50 = b["ema21"], b["ema50"]
    cross = (e21 > e50) & (_shift(e21, 1) <= _shift(e50, 1))
    hi, lo = _rmax(b["h"], 10), _rmin(b["l"], 10)
    brk = ((b["c"] > hi) & ((hi - lo) / hi <= 0.12) & (b["v"] >= 1.5 * b["vol50prev"]) & (e21 > e50))
    out, stops, last = [], [], -1
    for x in np.flatnonzero(cross):
        if x <= last:
            continue
        cand = np.flatnonzero(brk[x + 5:x + window + 1])
        if len(cand):
            t = x + 5 + cand[0]
            out.append(t)
            stops.append(lo[t])
            last = t
    return _frame(out, stops)


def _supertrend_dir(h, l, c, period=7, mult=2.0):
    """Supertrend direction (+1 up / -1 down) on HLC/3, as in the course's settings (7, 2)."""
    n = len(c)
    prev_c = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))
    atr = pd.Series(tr).ewm(alpha=1 / period, adjust=False).mean().to_numpy()
    mid = (h + l + c) / 3
    up, dn = mid - mult * atr, mid + mult * atr
    d = np.ones(n)
    fu, fd = up.copy(), dn.copy()
    for i in range(1, n):
        fu[i] = max(up[i], fu[i - 1]) if c[i - 1] > fu[i - 1] else up[i]
        fd[i] = min(dn[i], fd[i - 1]) if c[i - 1] < fd[i - 1] else dn[i]
        d[i] = 1 if c[i] > fd[i - 1] else (-1 if c[i] < fu[i - 1] else d[i - 1])
    return d, fu


def tc_supertrend_ema(b):
    """Supertrend (7, 2, HLC/3) flips to buy on the SAME candle that closes back above the 21 EMA.
    The course claims a 60-70% win rate. Stop: the Supertrend line."""
    d, fu = _supertrend_dir(b["h"], b["l"], b["c"])
    flip = (d == 1) & (_shift(d, 1) == -1)
    cross = (b["c"] > b["ema21"]) & (_shift(b["c"], 1) <= _shift(b["ema21"], 1))
    t = np.flatnonzero(flip & cross)
    return _frame(t, fu[t])


def tc_reversal_base(b):
    """Reversal: >= 35% below the 52-week high, but back above the 50 EMA with the 21 EMA above the
    50 and rising; buy the close above a 20-day base (<= 20% deep). Stop: the base low."""
    hh52 = _rmax(b["h"], 252, shift=0)
    hi, lo = _rmax(b["h"], 20), _rmin(b["l"], 20)
    sig = ((b["c"] <= 0.65 * hh52) & (b["c"] > b["ema50"]) & (b["ema21"] > b["ema50"])
           & (b["ema21"] > _shift(b["ema21"], 5)) & (b["c"] > hi) & (_shift(b["c"], 1) <= _shift(hi, 1))
           & ((hi - lo) / hi <= 0.20))
    t = np.flatnonzero(sig)
    return _frame(t, lo[t])


def tc_ema200_second_pullback(b, min_below=60):
    """After a stock closes back above its 200 EMA (having been below it for >= 60 days), skip the
    first pullback to the 200 EMA and buy the second: a low within 1% of the 200 EMA, then a close
    above the prior day's high while still above the 200 EMA. Stop 6% below the 200 EMA."""
    c, l, h = b["c"], b["l"], b["h"]
    e200 = pd.Series(c).ewm(span=200, adjust=False).mean().to_numpy()
    below = (c < e200).astype(int)
    run = pd.Series(below).groupby((below == 0).cumsum()).cumsum().to_numpy()   # days below so far
    out, stops = [], []
    n = len(c)
    t = 200
    while t < n:
        if c[t] > e200[t] and c[t - 1] <= e200[t - 1] and run[t - 1] >= min_below:
            touches, k, in_touch = 0, t + 1, False
            while k < min(n, t + 150) and c[k] > e200[k] * 0.97:
                touch = l[k] <= e200[k] * 1.01
                if touch and not in_touch:
                    touches += 1
                in_touch = touch or (in_touch and c[k] <= h[k - 1])
                if touches >= 2 and c[k] > h[k - 1] and c[k] > e200[k]:
                    out.append(k)
                    stops.append(e200[k] * 0.94)
                    break
                k += 1
            t = k
        t += 1
    return _frame(out, stops)


def random_uptrend(b, seed):
    """Baseline: random days while price is above a rising 50-day average. Same stop rule."""
    rng = np.random.default_rng(seed)
    sig = (b["c"] > b["sma50"]) & (b["sma50"] > _shift(b["sma50"], 10)) & (rng.random(len(b["c"])) < 1 / 30)
    t = np.flatnonzero(sig)
    return _frame(t, b["l"][t])


# name -> (function, kwargs, needs_df, source)
ENTRIES = {
    "donchian_20": (donchian, {"n": 20}, False, "Turtle 20-day breakout / trading-range break (Brock et al. 1992)"),
    "donchian_55": (donchian, {"n": 55}, False, "Turtle 55-day breakout"),
    "high52": (high52, {"fresh": False}, False, "52-week-high breakout (George & Hwang 2004)"),
    "high52_fresh": (high52, {"fresh": True}, False, "52-week high after >= 20 days of consolidation"),
    "base_25": (base_breakout, {"L": 25}, False, "O'Neil/Darvas 5-week base breakout"),
    "base_50": (base_breakout, {"L": 50}, False, "O'Neil 10-week base breakout"),
    "vcp": (vcp, {}, False, "Minervini volatility contraction pattern"),
    "flag_30": (flag, {"min_move": 0.3}, False, "Qullamaggie flag after a 30%+ move"),
    "flag_60": (flag, {"min_move": 0.6}, False, "Qullamaggie flag after a 60%+ move"),
    "flag_30_early": (flag, {"min_move": 0.3, "early": True}, False, "Qullamaggie flag, early entry inside the flag"),
    "htf": (flag, {"min_move": 0.9, "run_window": 40, "max_flag": 25}, False, "High tight flag (O'Neil / Bulkowski)"),
    "ep_gap5": (episodic_pivot, {"gap": 0.05}, False, "Gap up >= 5% on 3x volume"),
    "ep_gap10": (episodic_pivot, {"gap": 0.10}, False, "Episodic pivot: gap >= 10% on 3x volume"),
    "ep_gap8_neglected": (episodic_pivot, {"gap": 0.08, "neglected": True}, False, "Episodic pivot from neglect (Qullamaggie)"),
    "ep_gap15": (episodic_pivot, {"gap": 0.15}, False, "Episodic pivot: gap >= 15% on 3x volume"),
    "ep_gap10_vol2": (episodic_pivot, {"gap": 0.10, "vol_mult": 2.0}, False, "EP variant: gap >= 10% on only 2x volume"),
    "ep_gap10_vol5": (episodic_pivot, {"gap": 0.10, "vol_mult": 5.0}, False, "EP variant: gap >= 10% on 5x volume"),
    "ep_gap8_hold": (episodic_pivot, {"gap": 0.08, "hold": True}, False, "EP variant: gap >= 8%, closes above the open"),
    "pocket_pivot": (pocket_pivot, {}, False, "Morales & Kacher pocket pivot"),
    "asc_triangle": (chart_pattern, {"kind": "asc_triangle"}, False, "Ascending triangle breakout (flat top, rising lows)"),
    "desc_triangle": (chart_pattern, {"kind": "desc_triangle"}, False, "Descending triangle, upside breakout"),
    "sym_triangle": (chart_pattern, {"kind": "sym_triangle"}, False, "Symmetrical triangle breakout (pennant)"),
    "falling_wedge": (chart_pattern, {"kind": "falling_wedge"}, False, "Falling wedge breakout"),
    "rising_wedge": (chart_pattern, {"kind": "rising_wedge"}, False, "Rising wedge, upside breakout"),
    "tight_coil_7": (tight_coil, {"days": 7, "adr_mult": 1.0}, False, "7-day coil: closes within 1 ADR, breakout on volume"),
    "tight_coil_15": (tight_coil, {"days": 15, "adr_mult": 1.5}, False, "15-day coil: closes within 1.5 ADR, breakout on volume"),
    "stage2": (stage2, {}, False, "Weinstein stage 2 breakout"),
    "ema_retest": (_playbook(playbook.retests), {}, True, "8/21 EMA cross -> break -> retest (your playbook)"),
    "multi_touch": (_playbook(playbook.breakouts), {}, True, "Multi-touch level breakout on volume (your playbook)"),
    "undercut": (_playbook(playbook.undercuts), {}, True, "Undercut & rally (your playbook)"),
    "qull_breakout": (qull_breakout, {}, False, "Qullamaggie breakout: buy-stop above the flag high next day"),
    "qull_breakout_60": (qull_breakout, {"min_move": 0.60}, False, "Qullamaggie breakout after a 60%+ move"),
    "wf_rocket_breakout": (wf_rocket_breakout, {}, False, "Workflow PDF rockets: 6-week base -> 52w high on 1.5x vol, stop -8%"),
    "wf_rocket_gap": (wf_gap_hold, {}, False, "Workflow PDF rockets: gap >= 5% (2x vol) holding its low 2 days"),
    "wf_scan_pullback": (wf_scan_pullback, {}, False, "Workflow PDF scanner: uptrend pullback to 21EMA/50SMA, close > prior high"),
    "wf_scan_base": (wf_scan_base, {}, False, "Workflow PDF scanner: uptrend, breakout from a 4-week base"),
    "tc_ema_cross_base": (tc_ema_cross_base, {}, False, "Course: 21/50 EMA crossover, then the first base breakout"),
    "tc_supertrend_ema": (tc_supertrend_ema, {}, False, "Course: Supertrend flip + close above 21 EMA, same candle"),
    "tc_reversal_base": (tc_reversal_base, {}, False, "Course: reversal, 35%+ off the high, EMAs turned up, base breakout"),
    "tc_ema200_2nd": (tc_ema200_second_pullback, {}, False, "Course: second pullback to the 200 EMA after reclaiming it"),
    "random_uptrend": (random_uptrend, {"seed": 0}, False, "BASELINE: random entries in an uptrend"),
}


def all_signals(df: pd.DataFrame, b: dict, cooldown: int = 10, max_risk: float = 0.12,
                min_stop_adr: float = 0.5, min_price: float = 5.0, min_dollar_vol: float = 5e6,
                warmup: int = 252, seed: int = 0) -> pd.DataFrame:
    n = len(b["c"])
    frames = []
    for name, (fn, kw, needs_df, _) in ENTRIES.items():
        if name == "random_uptrend":
            kw = {**kw, "seed": seed}
        s = fn(b, df, **kw) if needs_df else fn(b, **kw)
        if s.empty:
            continue
        s = s[(s["idx"] >= warmup) & (s["idx"] <= n - 2)]
        keep, last = [], -10**9
        for i in s["idx"].to_numpy():
            keep.append(i - last > cooldown)
            if keep[-1]:
                last = i
        s = s[np.array(keep, dtype=bool)] if len(s) else s
        frames.append(s.assign(entry_name=name))
    if not frames:
        return pd.DataFrame()
    s = pd.concat(frames, ignore_index=True)
    t = s["idx"].to_numpy()
    adr = b["adr"][t]
    # entry at the signal-day close, except setups that model a next-day stop order (column `fill`)
    c = s["fill"].fillna(pd.Series(b["c"][t], index=s.index)).to_numpy() if "fill" in s else b["c"][t]
    s["entry"] = c
    s["stop"] = np.minimum(s["stop"].to_numpy(), c * (1 - min_stop_adr * np.nan_to_num(adr)))
    s["risk_pct"] = (c - s["stop"]) / c
    s["risk_adr"] = s["risk_pct"] / adr
    s["vol_ratio"] = b["v"][t] / b["vol50prev"][t]
    s["gap"] = b["o"][t] / b["c"][t - 1] - 1
    s["close_strength"] = _strength(b)[t]
    s["uptrend_tpl"] = _uptrend_template(b)[t].astype(float)   # run 20: the workflow scanner's trend rules
    s = s.replace([np.inf, -np.inf], np.nan)
    ok = ((s["risk_pct"] > 0) & (s["risk_pct"] <= max_risk) & (c >= min_price)
          & (c * b["vol50"][t] >= min_dollar_vol))
    return s[ok.to_numpy()].reset_index(drop=True)
