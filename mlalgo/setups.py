"""Entry setups, detected on daily bars. Every signal is known at the close of its day,
and entry is assumed at that close (we can't replay 5-minute "sniper" entries with daily data).

breakout  - tight base under a key level that has rejected price >= 2 times, then a close
            above that level on >= 1.5x average volume, with price above a stacked 8/21/50 EMA.
            Stop = low of the breakout day.
retest    - the "8/21 cross" playbook: 8 EMA crosses above 21 EMA -> price closes above the key
            level -> pulls back to retest the level / 8 EMA and holds -> entry when price closes
            above the prior day's high (confirmation). Stop = low of the retest.
undercut  - undercut & rally: price dips below the low of a tight base, then closes back above
            it (the reclaim). Stop = lowest low of the undercut.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from mlalgo.indicators import adr_pct, ema

SETUPS = ("breakout", "retest", "undercut")


@dataclass
class SetupConfig:
    level_lookback: int = 40       # days used to find the key level / base
    touch_tol: float = 0.015       # within 1.5% of the level counts as a touch
    min_touches: int = 2           # level must have rejected price at least twice
    max_base_depth: float = 0.25   # base high-to-low depth
    max_tight_10: float = 0.15     # range of the last 10 days before the breakout
    vol_mult: float = 1.5          # breakout volume vs 50-day average
    max_risk: float = 0.10         # skip signals whose stop is > 10% away
    min_stop_adr: float = 0.5      # stop at least half an ADR below entry (avoids 0.1%-wide stops)
    # retest playbook
    break_window: int = 30         # days after the 8/21 cross for the level to break
    retest_window: int = 15        # days after the break for the retest
    confirm_window: int = 5        # days after the retest for confirmation
    max_level_dist: float = 0.20   # key level must be within 20% of price at the cross
    # undercut
    undercut_days: int = 3


def _signals_frame(df, idx, setup, entry, stop, level) -> pd.DataFrame:
    out = pd.DataFrame({"idx": idx, "setup": setup, "entry": entry, "stop": stop, "level": level})
    out["date"] = df.index[out["idx"].to_numpy()] if len(out) else pd.DatetimeIndex([])
    out["risk_pct"] = (out["entry"] - out["stop"]) / out["entry"]
    return out


def breakouts(df: pd.DataFrame, cfg: SetupConfig) -> pd.DataFrame:
    o, h, l, c, v = (df[k].to_numpy(float) for k in ("open", "high", "low", "close", "volume"))
    n, L = len(c), cfg.level_lookback
    if n <= L + 50:
        return _signals_frame(df, [], [], [], [], [])
    hw = sliding_window_view(h, L)[: n - L]           # window for day t = L..n-1 is h[t-L:t]
    lw = sliding_window_view(l, L)[: n - L]
    level = hw.max(1)
    near = hw >= level[:, None] * (1 - cfg.touch_tol)
    touches = (near & ~np.pad(near[:, :-1], ((0, 0), (1, 0)))).sum(1)   # count separate visits
    depth = (level - lw.min(1)) / level
    tight = (hw[:, -10:].max(1) - lw[:, -10:].min(1)) / level

    t = np.arange(L, n)
    cs = df["close"]
    e8, e21, e50 = (ema(cs, k).to_numpy() for k in (8, 21, 50))
    vol50_prev = pd.Series(v).rolling(50).mean().shift(1).to_numpy()
    ok = ((c[t] > level) & (touches >= cfg.min_touches) & (depth <= cfg.max_base_depth)
          & (tight <= cfg.max_tight_10) & (v[t] >= cfg.vol_mult * vol50_prev[t])
          & (c[t] > e8[t]) & (e8[t] > e21[t]) & (e21[t] > e50[t]))
    risk = (c[t] - l[t]) / c[t]
    ok &= (risk > 0) & (risk <= cfg.max_risk)
    sel = t[ok]
    return _signals_frame(df, sel, "breakout", c[sel], l[sel], level[ok])


def retests(df: pd.DataFrame, cfg: SetupConfig) -> pd.DataFrame:
    h, l, c = (df[k].to_numpy(float) for k in ("high", "low", "close"))
    cs = df["close"]
    e8, e21 = ema(cs, 8).to_numpy(), ema(cs, 21).to_numpy()
    prior_high = df["high"].rolling(cfg.level_lookback).max().shift(1).to_numpy()
    rows = []
    state = 0  # 0 idle, 1 crossed, 2 broke level, 3 retested
    level = t_cross = t_break = t_retest = 0
    retest_low = np.inf
    for t in range(1, len(c)):
        crossed_up = e8[t] > e21[t] and e8[t - 1] <= e21[t - 1]
        if crossed_up:
            lvl = prior_high[t]
            if not np.isnan(lvl) and lvl <= c[t] * (1 + cfg.max_level_dist):
                state, level, t_cross = 1, lvl, t
            else:
                state = 0
            continue
        if e8[t] <= e21[t]:
            state = 0
            continue
        if state == 1:
            if t - t_cross > cfg.break_window:
                state = 0
            elif c[t] > level:
                state, t_break = 2, t
        elif state == 2:
            if t - t_break > cfg.retest_window or c[t] < level * (1 - cfg.touch_tol):
                state = 0
            elif l[t] <= max(level, e8[t]) * (1 + cfg.touch_tol):
                state, t_retest, retest_low = 3, t, l[t]
        elif state == 3:
            if t - t_retest > cfg.confirm_window or c[t] < level * (1 - cfg.touch_tol):
                state = 0
            elif c[t] > h[t - 1] and c[t] > e8[t]:
                stop = min(retest_low, l[t])
                if 0 < (c[t] - stop) / c[t] <= cfg.max_risk:
                    rows.append((t, c[t], stop, level))
                state = 0
            else:
                retest_low = min(retest_low, l[t])
    idx, entry, stop, lvl = (list(x) for x in zip(*rows)) if rows else ([], [], [], [])
    return _signals_frame(df, idx, "retest", entry, stop, lvl)


def undercuts(df: pd.DataFrame, cfg: SetupConfig) -> pd.DataFrame:
    l, c = df["low"], df["close"]
    k, L = cfg.undercut_days, cfg.level_lookback // 2
    base_low = l.rolling(L).min().shift(k + 1)           # base defined before the undercut window
    base_high = df["high"].rolling(L).max().shift(k + 1)
    e21, e50 = ema(c, 21), ema(c, 50)
    recent_low = l.rolling(k + 1).min()
    sig = ((recent_low < base_low) & (c > base_low) & ((c.shift() < base_low) | (l < base_low))
           & ((base_high - base_low) / base_high <= cfg.max_base_depth) & (e21 > e50))
    sig &= ~sig.shift(1, fill_value=False).astype(float).rolling(5, min_periods=1).max().astype(bool)
    risk = (c - recent_low) / c
    sig &= (risk > 0) & (risk <= cfg.max_risk)
    t = np.flatnonzero(sig.to_numpy())
    return _signals_frame(df, t, "undercut", c.to_numpy()[t], recent_low.to_numpy()[t], base_low.to_numpy()[t])


def find_signals(df: pd.DataFrame, cfg: SetupConfig = SetupConfig(), which=SETUPS) -> pd.DataFrame:
    funcs = {"breakout": breakouts, "retest": retests, "undercut": undercuts}
    sig = pd.concat([funcs[s](df, cfg) for s in which], ignore_index=True).sort_values("idx", kind="stable")
    if len(sig):
        adr = adr_pct(df).to_numpy()[sig["idx"].to_numpy()]
        sig["stop"] = np.minimum(sig["stop"], sig["entry"] * (1 - cfg.min_stop_adr * np.nan_to_num(adr)))
        sig["risk_pct"] = (sig["entry"] - sig["stop"]) / sig["entry"]
        sig = sig[sig["risk_pct"] <= cfg.max_risk]
    return sig
