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


def _playbook(fn):
    def run(b, df, **_):
        s = fn(df, playbook.SetupConfig(max_risk=1.0))
        return _frame(s["idx"], s["stop"])
    return run


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
    c, adr = b["c"][t], b["adr"][t]
    s["entry"] = c
    s["stop"] = np.minimum(s["stop"].to_numpy(), c * (1 - min_stop_adr * np.nan_to_num(adr)))
    s["risk_pct"] = (c - s["stop"]) / c
    s["risk_adr"] = s["risk_pct"] / adr
    s["vol_ratio"] = b["v"][t] / b["vol50prev"][t]
    s["gap"] = b["o"][t] / b["c"][t - 1] - 1
    s["close_strength"] = _strength(b)[t]
    s = s.replace([np.inf, -np.inf], np.nan)
    ok = ((s["risk_pct"] > 0) & (s["risk_pct"] <= max_risk) & (c >= min_price)
          & (c * b["vol50"][t] >= min_dollar_vol))
    return s[ok.to_numpy()].reset_index(drop=True)
