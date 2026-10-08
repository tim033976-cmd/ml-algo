"""Simulate the trade-management plan on each signal.

  * Initial stop: from the setup (low of day / low of retest / undercut low).
  * Trim 1/4 at the first target (default +2R), then move the stop to breakeven.
  * Trim 1/4 on the first close below the 8 EMA, 1/4 on the first close below the 21 EMA.
  * Exit everything on a close below the 50 EMA (or the stop).

Costs: `cost_pct` per side. Conservative fills: a gap below the stop fills at the open; if the stop and target are both
inside one daily bar we assume the stop hit first. One open trade per ticker at a time.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from mlalgo.indicators import ema


@dataclass
class ExitConfig:
    target_r: float = 2.0
    trim: float = 0.25
    max_days: int = 250
    cost_pct: float = 0.001        # slippage + commission per side (0.1%)


def simulate(df: pd.DataFrame, signals: pd.DataFrame, cfg: ExitConfig = ExitConfig()) -> pd.DataFrame:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    e8, e21, e50 = (ema(df["close"], k).to_numpy() for k in (8, 21, 50))
    n = len(c)
    trades, busy_until = [], -1
    for sig in signals.itertuples(index=False):
        t = int(sig.idx)
        if t <= busy_until or t >= n - 1:
            continue
        entry, stop = sig.entry, sig.stop
        risk = entry - stop
        target = entry + cfg.target_r * risk
        remaining, pnl, stage, reason = 1.0, 0.0, 0, "open"

        def sell(frac, px):
            nonlocal remaining, pnl
            frac = min(frac, remaining)
            pnl += frac * (px / entry - 1)
            remaining -= frac

        d = t
        for d in range(t + 1, min(n, t + 1 + cfg.max_days)):
            if o[d] <= stop or l[d] <= stop:
                sell(remaining, min(o[d], stop))
                reason = "breakeven" if stage else "stop"
                break
            if stage == 0 and h[d] >= target:
                sell(cfg.trim, max(o[d], target))
                stage, stop = 1, max(stop, entry)
            if stage == 1 and c[d] < e8[d]:
                sell(cfg.trim, c[d])
                stage = 2
            if stage == 2 and c[d] < e21[d]:
                sell(cfg.trim, c[d])
                stage = 3
            if c[d] < e50[d]:
                sell(remaining, c[d])
                reason = "ema50"
                break
        else:
            reason = "open" if d == n - 1 else "max_days"
        if remaining > 1e-12:
            sell(remaining, c[d])
        pnl -= 2 * cfg.cost_pct
        busy_until = d
        trades.append({
            "setup": sig.setup, "entry_date": df.index[t], "exit_date": df.index[d], "entry": entry,
            "stop": sig.stop, "risk_pct": risk / entry, "ret": pnl, "R": pnl / (risk / entry),
            "days": d - t, "hit_target": stage >= 1, "exit_reason": reason,
        })
    return pd.DataFrame(trades)


def trade_stats(trades: pd.DataFrame) -> pd.Series:
    if trades.empty:
        return pd.Series({"trades": 0})
    r = trades["R"]
    wins, losses = r[r > 0], r[r <= 0]
    return pd.Series({
        "trades": len(r),
        "win_rate": (r > 0).mean(),
        "avg_R": r.mean(),
        "median_R": r.median(),
        "avg_win_R": wins.mean() if len(wins) else np.nan,
        "avg_loss_R": losses.mean() if len(losses) else np.nan,
        "profit_factor": wins.sum() / -losses.sum() if losses.sum() < 0 else np.inf,
        "avg_ret": trades["ret"].mean(),
        "hit_target": trades["hit_target"].mean(),
        "big_winners_5R": (r >= 5).mean(),
        "avg_days": trades["days"].mean(),
    })
