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
    # the user's goal (run 13): a fixed bracket on the daily chart
    "bracket_10_10": (9, "stop -10%, target +10%, close after 63 days if neither"),
    "bracket_20_10": (10, "stop -10%, target +20%, close after 63 days if neither"),
    # run 20: the user's workflow PDF
    "wf_rocket": (11, "workflow rockets: sell 1/3 at +25% and move the stop to entry, trail the rest on close<50SMA"),
    "wf_weekly10": (12, "workflow scanner: exit on a weekly close below the 10-week MA (setup stop stays)"),
}

REASON = {0: "end", 1: "stop", 2: "rule", 3: "target"}


@njit(cache=True)
def _sim_one(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev, wkx,
             t, entry, stop0, code, max_days, cost):
    n = len(c)
    stop = stop0
    if code == 3:
        stop = max(stop, entry * 0.92)
    elif code == 9 or code == 10:
        stop = entry * 0.90  # fixed -10% stop replaces the setup's stop
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
        elif code == 9 or code == 10:
            tgt = entry * (1.10 if code == 9 else 1.20)
            if h[d] >= tgt:
                px = max(o[d], tgt)
                pnl += remaining * (px / entry - 1.0)
                remaining = 0.0
                reason = 3
                break
            if held >= 63:
                reason = 2
                break
        elif code == 11:
            tgt = entry * 1.25
            if stage == 0 and h[d] >= tgt:
                px = max(o[d], tgt)
                pnl += (1.0 / 3.0) * (px / entry - 1.0)
                remaining -= 1.0 / 3.0
                stage = 1
                stop = max(stop, entry)
            if c[d] < sma50[d]:
                reason = 2
                break
        elif code == 12:
            if wkx[d] > 0.5:
                reason = 2
                break
    if remaining > 1e-9:
        pnl += remaining * (c[d] / entry - 1.0)
    pnl -= 2.0 * cost
    return pnl, pnl / (risk / entry), d, reason


@njit(cache=True)
def simulate_all(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev, wkx,
                 sig_idx, sig_entry, sig_stop, codes, max_days, cost):
    ns, ne = len(sig_idx), len(codes)
    ret = np.empty((ns, ne))
    rmult = np.empty((ns, ne))
    exit_idx = np.empty((ns, ne), dtype=np.int64)
    reason = np.empty((ns, ne), dtype=np.int64)
    for i in range(ns):
        for j in range(ne):
            a, b, d, r = _sim_one(o, h, l, c, sma10, sma20, sma50, ema8, ema21, ema50, atr20, low10prev, wkx,
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


# ---------------------------------------------------------------- wedges / triangles
PATTERNS = {"asc_triangle": 1, "desc_triangle": 2, "sym_triangle": 3, "falling_wedge": 4, "rising_wedge": 5}


@njit(cache=True)
def _fit(xs, ys, m):
    """Least-squares line through m points; returns slope, intercept."""
    sx = 0.0
    sy = 0.0
    for i in range(m):
        sx += xs[i]
        sy += ys[i]
    mx, my = sx / m, sy / m
    num = 0.0
    den = 0.0
    for i in range(m):
        num += (xs[i] - mx) * (ys[i] - my)
        den += (xs[i] - mx) ** 2
    b = num / den if den > 0 else 0.0
    return b, my - b * mx


@njit(cache=True)
def pattern_signals(h, l, c, v, vol50prev, window, k, flat_tol, touch_tol, min_converge, vol_mult):
    """Trendline patterns from CONFIRMED swing points (a swing at i needs i+k <= t-1, so nothing
    after the signal day is used). Upper line through swing highs, lower line through swing lows
    (the last 2-3 touches per side), each within touch_tol of its line, closes contained between the lines,
    and the lines converging. Classified by the slopes (fraction of price per day):
      asc_triangle   flat top, rising bottom      desc_triangle  falling top, flat bottom
      sym_triangle   falling top, rising bottom    falling_wedge  both falling, converging
      rising_wedge   both rising, converging
    Signal: first close above the upper line on >= vol_mult x average volume.
    Stop: the lowest swing low of the last part of the pattern (lower line at the signal day)."""
    n = len(c)
    out_t = np.empty(n, dtype=np.int64)
    out_kind = np.empty(n, dtype=np.int64)
    out_stop = np.empty(n)
    out_len = np.empty(n)
    out_width = np.empty(n)
    out_touch = np.empty(n)
    m = 0
    hx = np.empty(window)
    hy = np.empty(window)
    lx = np.empty(window)
    ly = np.empty(window)
    for t in range(window + k + 2, n):
        start = t - window
        last_pivot = t - 1 - k
        nh = 0
        nl = 0
        for i in range(max(start, k), last_pivot + 1):
            is_hi = True
            is_lo = True
            for j in range(i - k, i + k + 1):
                if h[j] > h[i]:
                    is_hi = False
                if l[j] < l[i]:
                    is_lo = False
            if is_hi:
                hx[nh] = i
                hy[nh] = h[i]
                nh += 1
            if is_lo:
                lx[nl] = i
                ly[nl] = l[i]
                nl += 1
        if nh < 2 or nl < 2:
            continue
        # trendlines are drawn through the most recent touches (up to 3 per side), as a chartist would
        if nh > 3:
            for i in range(3):
                hx[i], hy[i] = hx[nh - 3 + i], hy[nh - 3 + i]
            nh = 3
        if nl > 3:
            for i in range(3):
                lx[i], ly[i] = lx[nl - 3 + i], ly[nl - 3 + i]
            nl = 3
        bu, au = _fit(hx, hy, nh)
        bl, al = _fit(lx, ly, nl)
        ok = True
        for i in range(nh):
            if abs(hy[i] - (au + bu * hx[i])) > touch_tol * hy[i]:
                ok = False
        for i in range(nl):
            if abs(ly[i] - (al + bl * lx[i])) > touch_tol * ly[i]:
                ok = False
        if not ok:
            continue
        x0 = min(hx[0], lx[0])
        for i in range(int(x0), t):   # contained: no close outside the pattern before today
            up = au + bu * i
            lo = al + bl * i
            if c[i] > up * (1 + touch_tol) or c[i] < lo * (1 - touch_tol):
                ok = False
                break
        if not ok:
            continue
        up_t = au + bu * t
        lo_t = al + bl * t
        up_prev = au + bu * (t - 1)
        w0 = (au + bu * x0) - (al + bl * x0)
        w1 = up_t - lo_t
        if w0 <= 0 or w1 <= 0 or w1 > min_converge * w0:
            continue
        if not (c[t] > up_t and c[t - 1] <= up_prev and v[t] >= vol_mult * vol50prev[t]):
            continue
        su = bu / c[t - 1]
        sl = bl / c[t - 1]
        kind = 0
        if abs(su) <= flat_tol and sl > flat_tol:
            kind = 1
        elif su < -flat_tol and abs(sl) <= flat_tol:
            kind = 2
        elif su < -flat_tol and sl > flat_tol:
            kind = 3
        elif su < -flat_tol and sl < -flat_tol:
            kind = 4
        elif su > flat_tol and sl > flat_tol:
            kind = 5
        if kind == 0:
            continue
        out_t[m], out_kind[m], out_stop[m] = t, kind, lo_t
        out_len[m], out_width[m], out_touch[m] = t - x0, w1 / c[t], nh + nl
        m += 1
    return out_t[:m], out_kind[:m], out_stop[:m], out_len[:m], out_width[:m], out_touch[:m]


# ---------------------------------------------------------------- Qullamaggie-style breakout (buy-stop)
@njit(cache=True)
def qull_setups(o, h, l, c, sma10, sma20, adr, min_move, run_window, min_flag, max_flag, max_depth, min_adr):
    """Setup known at the close of day t: a >= min_move run into a high (pivot), then an orderly
    consolidation of min_flag..max_flag days, no deeper than max_depth, higher lows, price holding
    the 10/20-day averages, not yet broken out, ADR >= min_adr.
    Order for day t+1: buy-stop just above the pivot. Filled only if day t+1 trades through it, at
    max(open, pivot). Stop = the tighter of the last 3 days' low and 1 ADR below the fill.
    Returns setup day t (features use data up to t only), fill price, stop."""
    n = len(c)
    out_t = np.empty(n, dtype=np.int64)
    out_fill = np.empty(n)
    out_stop = np.empty(n)
    out_move = np.empty(n)
    out_depth = np.empty(n)
    out_days = np.empty(n)
    m = 0
    for t in range(run_window + max_flag + 2, n - 1):
        if adr[t] < min_adr or np.isnan(sma20[t]):
            continue
        pi = t - max_flag + 1
        for k in range(t - max_flag + 1, t + 1):
            if h[k] >= h[pi]:
                pi = k
        days = t - pi
        if days < min_flag:
            continue
        pivot = h[pi]
        if c[t] >= pivot:
            continue
        lo_after = l[pi]
        for k in range(pi, t + 1):
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
        mid = pi + (t - pi) // 2
        lo1 = l[pi]
        for k in range(pi, mid + 1):
            if l[k] < lo1:
                lo1 = l[k]
        lo2 = l[mid + 1] if mid + 1 <= t else lo1
        for k in range(mid + 1, t + 1):
            if l[k] < lo2:
                lo2 = l[k]
        if lo2 < lo1:
            continue
        if c[t] < 0.98 * sma20[t] or c[t] < 0.97 * sma10[t]:
            continue
        trigger = pivot * 1.001
        if h[t + 1] < trigger:
            continue
        fill = max(o[t + 1], trigger)
        low3 = min(l[t], min(l[t - 1], l[t - 2]))
        stop = max(low3, fill * (1.0 - adr[t]))
        if stop >= fill:
            continue
        out_t[m], out_fill[m], out_stop[m] = t, fill, stop
        out_move[m], out_depth[m], out_days[m] = move, depth, days
        m += 1
    return out_t[:m], out_fill[:m], out_stop[:m], out_move[:m], out_depth[:m], out_days[:m]
