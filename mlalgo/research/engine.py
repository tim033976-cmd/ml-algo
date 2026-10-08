"""Fast (numba) kernels: pattern detection loops and the exit-plan simulator."""
from __future__ import annotations

import numpy as np
from numba import njit

# ---------------------------------------------------------------- exits
EXITS = {
    # name: (code, description)
    "trim_ema": (0, "1/4 at +2R then BE stop; 1/4 on close<8EMA, 1/4 <21EMA, rest <50EMA"),
    "qull_sma10": (1, "Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<10SMA"),
    "qull_sma20": (2, "Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<20SMA"),
    "oneil_20_8": (3, "O'Neil: stop max 8% below entry, take all at +20%, time stop 60 days"),
    "fixed_3r_20d": (4, "stop, target 3R, time stop 20 days"),
    "chandelier_3atr": (5, "trailing stop = highest close - 3 x ATR(20)"),
    "donchian_10low": (6, "Turtle-style: exit on close below the prior 10-day low"),
    "ema21_close": (7, "exit on first close below the 21 EMA"),
    "sma50_close": (8, "position trade: exit on first close below the 50 SMA"),
}

REASON = {0: "end", 1: "stop", 2: "rule", 3: "target"}


@njit(cache=True)
def _sim_one(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev,
             t, entry, stop0, code, max_days, cost):
    n = len(c)
    stop = stop0
    if code == 3:
        stop = max(stop, entry * 0.92)
    risk = entry - stop
    remaining = 1.0
    pnl = 0.0
    stage = 0
    hi_close = entry
    reason = 0
    end = min(n - 1, t + max_days)
    d = t
    for d in range(t + 1, end + 1):
        if l[d] <= stop:
            px = min(o[d], stop)
            pnl += remaining * (px / entry - 1.0)
            remaining = 0.0
            reason = 1
            break
        held = d - t
        if code == 0:
            tgt = entry + 2.0 * risk
            if stage == 0 and h[d] >= tgt:
                px = max(o[d], tgt)
                pnl += 0.25 * (px / entry - 1.0)
                remaining -= 0.25
                stage = 1
                stop = max(stop, entry)
            if stage == 1 and c[d] < ema8[d]:
                pnl += 0.25 * (c[d] / entry - 1.0)
                remaining -= 0.25
                stage = 2
            if stage == 2 and c[d] < ema21[d]:
                pnl += 0.25 * (c[d] / entry - 1.0)
                remaining -= 0.25
                stage = 3
            if c[d] < ema50[d]:
                reason = 2
                break
        elif code == 1 or code == 2:
            if stage == 0 and held >= 5:
                if c[d] > entry:
                    pnl += (1.0 / 3.0) * (c[d] / entry - 1.0)
                    remaining -= 1.0 / 3.0
                    stop = max(stop, entry)
                stage = 1
            if held >= 5:
                ma = sma10[d] if code == 1 else sma20[d]
                if c[d] < ma:
                    reason = 2
                    break
        elif code == 3:
            tgt = entry * 1.20
            if h[d] >= tgt:
                px = max(o[d], tgt)
                pnl += remaining * (px / entry - 1.0)
                remaining = 0.0
                reason = 3
                break
            if held >= 60:
                reason = 2
                break
        elif code == 4:
            tgt = entry + 3.0 * risk
            if h[d] >= tgt:
                px = max(o[d], tgt)
                pnl += remaining * (px / entry - 1.0)
                remaining = 0.0
                reason = 3
                break
            if held >= 20:
                reason = 2
                break
        elif code == 5:
            if c[d] > hi_close:
                hi_close = c[d]
            trail = hi_close - 3.0 * atr20[d]
            if trail > stop:
                stop = trail
        elif code == 6:
            if c[d] < low10prev[d]:
                reason = 2
                break
        elif code == 7:
            if c[d] < ema21[d]:
                reason = 2
                break
        elif code == 8:
            if c[d] < sma50[d]:
                reason = 2
                break
    if remaining > 1e-9:
        pnl += remaining * (c[d] / entry - 1.0)
    pnl -= 2.0 * cost
    return pnl, pnl / (risk / entry), d, reason


@njit(cache=True)
def simulate_all(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev,
                 sig_idx, sig_entry, sig_stop, codes, max_days, cost):
    ns, ne = len(sig_idx), len(codes)
    ret = np.empty((ns, ne))
    rmult = np.empty((ns, ne))
    exit_idx = np.empty((ns, ne), dtype=np.int64)
    reason = np.empty((ns, ne), dtype=np.int64)
    for i in range(ns):
        for j in range(ne):
            a, b, d, r = _sim_one(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev,
                                  sig_idx[i], sig_entry[i], sig_stop[i], codes[j], max_days, cost)
            ret[i, j], rmult[i, j], exit_idx[i, j], reason[i, j] = a, b, d, r
    return ret, rmult, exit_idx, reason


# ---------------------------------------------------------------- flag / high-tight-flag detector
@njit(cache=True)
def flag_signals(h, l, c, v, vol50, sma20, adr, min_move, run_window, min_flag, max_flag,
                 max_depth, min_adr, vol_mult, early):
    """Qullamaggie-style flag: a big move (>= min_move within run_window days) into a high,
    then an orderly consolidation of min_flag..max_flag days, no deeper than max_depth, with
    higher lows and price holding near the 20SMA. Trigger: close above the flag high
    (early=False) or above the last 5-day high while still inside the flag (early=True)."""
    n = len(c)
    out_t = np.empty(n, dtype=np.int64)
    out_move = np.empty(n)
    out_depth = np.empty(n)
    out_days = np.empty(n)
    m = 0
    start = run_window + max_flag + 2
    for t in range(start, n):
        if adr[t - 1] < min_adr or v[t] < vol_mult * vol50[t - 1]:
            continue
        pi = t - max_flag
        for k in range(t - max_flag, t):
            if h[k] > h[pi]:
                pi = k
        days = t - pi
        if days < min_flag:
            continue
        pivot = h[pi]
        lo_after = l[pi + 1]
        for k in range(pi + 1, t):
            if l[k] < lo_after:
                lo_after = l[k]
        depth = (pivot - lo_after) / pivot
        if depth > max_depth:
            continue
        lo_before = l[pi - run_window]
        for k in range(pi - run_window, pi + 1):
            if l[k] < lo_before:
                lo_before = l[k]
        move = pivot / lo_before - 1.0
        if move < min_move:
            continue
        mid = pi + 1 + (t - pi - 1) // 2
        lo1 = l[pi + 1]
        for k in range(pi + 1, mid):
            if l[k] < lo1:
                lo1 = l[k]
        lo2 = l[mid]
        for k in range(mid, t):
            if l[k] < lo2:
                lo2 = l[k]
        if lo2 < lo1:
            continue
        if c[t - 1] < 0.97 * sma20[t - 1]:
            continue
        if early:
            hi5 = h[t - 5]
            for k in range(t - 5, t):
                if h[k] > hi5:
                    hi5 = h[k]
            if not (c[t] > hi5 and c[t - 1] <= hi5 and c[t] <= pivot):
                continue
        else:
            if not (c[t] > pivot and c[t - 1] <= pivot):
                continue
        out_t[m], out_move[m], out_depth[m], out_days[m] = t, move, depth, days
        m += 1
    return out_t[:m], out_move[:m], out_depth[:m], out_days[:m]


@njit(cache=True)
def staircase_count(c, h20prev, sma200, min_base):
    n = len(c)
    out = np.zeros(n)
    count = 0
    since = 0
    for t in range(n):
        if np.isnan(sma200[t]) or c[t] < sma200[t]:
            count = 0
        if not np.isnan(h20prev[t]) and c[t] > h20prev[t]:
            if since >= min_base:
                count += 1
            since = 0
        else:
            since += 1
        out[t] = count
    return out
