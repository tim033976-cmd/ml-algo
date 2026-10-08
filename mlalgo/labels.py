"""What "it went" means: a triple-barrier label.

Buy at the close of day t. Within the next `horizon` days, did price hit
+target before it hit -stop? If both happen on the same day we assume the stop
hit first (conservative). If neither, the trade closes at day t+horizon.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def triple_barrier(df: pd.DataFrame, target: float = 0.10, stop: float = 0.05, horizon: int = 20) -> pd.DataFrame:
    c, h, l = (df[k].to_numpy(float) for k in ("close", "high", "low"))
    n = len(c)
    idx = np.arange(n)[:, None] + np.arange(1, horizon + 1)[None, :]   # [t, k] -> day t+k
    valid = idx[:, -1] < n
    idx = np.minimum(idx, n - 1)
    hit_up = h[idx] >= (c * (1 + target))[:, None]
    hit_dn = l[idx] <= (c * (1 - stop))[:, None]
    big = horizon + 1
    first_up = np.where(hit_up.any(1), hit_up.argmax(1) + 1, big)
    first_dn = np.where(hit_dn.any(1), hit_dn.argmax(1) + 1, big)

    stopped = (first_dn <= first_up) & (first_dn < big)          # ties -> stop (conservative)
    targeted = (first_up < first_dn)
    outcome = np.select([stopped, targeted], [-1.0, 1.0], 0.0)
    ret = np.select([stopped, targeted], [-stop, target], c[np.minimum(np.arange(n) + horizon, n - 1)] / c - 1)
    days = np.select([stopped, targeted], [first_dn, first_up], horizon).astype(float)
    out = pd.DataFrame({"outcome": outcome, "trade_ret": ret, "days_held": days}, index=df.index)
    out[~valid] = np.nan  # not enough future data to know the outcome yet
    return out


def label_panel(prices: dict[str, pd.DataFrame], **kw) -> pd.DataFrame:
    frames = {t: triple_barrier(df, **kw) for t, df in prices.items()}
    return pd.concat(frames, names=["ticker", "date"]).swaplevel().sort_index()
