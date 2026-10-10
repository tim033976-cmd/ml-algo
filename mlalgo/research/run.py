"""Run every entry setup on every stock and simulate every exit plan on every signal."""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from mlalgo.market import index_regime, rates_regime
from mlalgo.research import engine
from mlalgo.research.entries import all_signals, bars
from mlalgo.structure import ML_FEATURES, setup_score, structure_features

EXIT_NAMES = list(engine.EXITS)
EXIT_CODES = np.array([engine.EXITS[k][0] for k in EXIT_NAMES], dtype=np.int64)
GROUP_COLS = ["industry_rs", "industry_rank", "sector_rs", "qull_rank"]
# run 19: sector percentile among sectors (leading sectors), kept out of the model features so the
# goal model stays comparable with runs 16-18
GROUP_EXTRA = ["sector_rank", "r6_rank"]   # r6_rank (run 20): 6-month return percentile
SIGNAL_EXTRAS = ["risk_pct", "risk_adr", "vol_ratio", "gap", "close_strength",
                 "prior_move", "flag_depth", "flag_days", "base_depth", "contraction",
                 "pattern_len", "pattern_width", "pattern_touches", "coil_range", "uptrend_tpl"]
MARKET_COLS = ["mkt_ok", "mkt_ema_stack", "mkt_ret_21", "mkt_above200", "qqq_ok", "qqq_ret_21",
               "qqq_trend", "rates_rising", "breadth_50"]
VIX_COLS = ["vix", "vix_chg_1", "vix_chg_5", "vix_pct_1y", "vix_term", "spy_ret_1", "spy_ret_5"]
# run 20 (workflow PDF): Nasdaq-100 regime, 2 = green (QQQ > 200d and 50d > 200d), 1 = yellow
# (> 200d, 50d < 200d), 0 = red (< 200d). Not a model feature.
REGIME_COLS = ["ndx_regime"]
# run 21 (user): shorter market trend (21/50 SMA instead of 200), breadth and the advance/decline
# line. Codes for *_2150: 3 = above both, 2 = above the 21 only, 1 = above the 50 only, 0 = below both.
REGIME_COLS += ["spy_2150", "qqq_2150", "breadth_20", "breadth_50_chg10", "ad_2150", "ad_chg10"]
# sector / sub-industry short-term momentum ("tech and software ETFs both green")
GROUP_MOM = ["sec_ret1", "sec_ret5", "sec_up21", "ind_ret1", "ind_ret5", "ind_up21"]
GROUP_EXTRA += GROUP_MOM


def _rs_composite(df: pd.DataFrame) -> pd.Series:
    c = df["close"]
    return 0.4 * (c / c.shift(63) - 1) + 0.3 * (c / c.shift(126) - 1) + 0.3 * (c / c.shift(252) - 1)


def group_strength(rank: pd.DataFrame, groups: pd.Series, min_members: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Median RS rank of each group (sector / sub-industry) per day, and the group's percentile
    among groups. Groups with fewer than `min_members` stocks trading that day are left NaN."""
    g = groups.reindex(rank.columns)
    med = rank.T.groupby(g).median().T
    cnt = rank.T.groupby(g).count().T
    med = med.where(cnt >= min_members)
    return med.astype("float32"), med.rank(axis=1, pct=True).astype("float32")


def cross_section(prices: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.Series]:
    """Relative-strength percentile rank of every stock on every day, and market breadth
    (share of stocks above their 50-day average)."""
    rs = pd.DataFrame({t: _rs_composite(df) for t, df in prices.items()}).astype("float32")
    rank = rs.rank(axis=1, pct=True).astype("float32")
    above = pd.DataFrame({t: (df["close"] > df["close"].rolling(50).mean()).astype("float32")
                          .where(df["close"].rolling(50).count() == 50) for t, df in prices.items()})
    breadth = above.mean(axis=1).rename("breadth_50")
    return rank, breadth


def _above_2150(x: pd.Series) -> pd.Series:
    a21, a50 = x > x.rolling(21).mean(), x > x.rolling(50).mean()
    code = pd.Series(np.select([a21 & a50, a21, a50], [3.0, 2.0, 1.0], 0.0), index=x.index)
    return code.where(x.rolling(50).count() == 50)


def market_internals(prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Run 21: % of stocks above their 20-day average, the 10-day change of the % above the 50-day,
    and the advance/decline line (cumulative advancers - decliners) vs its 21/50-day averages."""
    close = pd.DataFrame({t: df["close"] for t, df in prices.items()})
    chg = close.diff()
    adv, dec = (chg > 0).sum(axis=1), (chg < 0).sum(axis=1)
    ad = (adv - dec).cumsum()
    above20 = (close > close.rolling(20).mean()).where(close.rolling(20).count() == 20)
    above50 = (close > close.rolling(50).mean()).where(close.rolling(50).count() == 50)
    b50 = above50.mean(axis=1)
    return pd.DataFrame({"breadth_20": above20.mean(axis=1), "breadth_50_chg10": b50 - b50.shift(10),
                         "ad_2150": _above_2150(ad), "ad_chg10": (ad - ad.shift(10)) / close.notna().sum(axis=1)})


def market_frame(market: dict[str, pd.DataFrame], breadth: pd.Series, internals: pd.DataFrame | None = None) -> pd.DataFrame:
    parts = [breadth] + ([internals] if internals is not None else [])
    if "SPY" in market:
        spy = market["SPY"]
        parts.append(index_regime(spy, "mkt"))
        parts.append((spy["close"] > spy["close"].rolling(200).mean()).astype(int).rename("mkt_above200"))
    if "QQQ" in market:
        q = market["QQQ"]["close"]
        parts.append(index_regime(market["QQQ"], "qqq")[["qqq_ok", "qqq_ret_21"]])
        # Qullamaggie: be aggressive only when the Nasdaq is above its 10- and 20-day averages
        parts.append(((q > q.rolling(10).mean()) & (q > q.rolling(20).mean())).astype(int).rename("qqq_trend"))
    if "^IRX" in market:
        parts.append(rates_regime(market["^IRX"]["close"]))
    if "^VIX" in market:
        vx = market["^VIX"]["close"]
        parts.append(pd.DataFrame({"vix": vx, "vix_chg_1": vx.pct_change(), "vix_chg_5": vx.pct_change(5),
                                   "vix_pct_1y": vx.rolling(252).rank(pct=True)}))
        if "^VIX3M" in market:
            parts.append((vx / market["^VIX3M"]["close"]).rename("vix_term"))
    if "SPY" in market:
        sc = market["SPY"]["close"]
        parts.append(pd.DataFrame({"spy_ret_1": sc.pct_change(), "spy_ret_5": sc.pct_change(5)}))
    m = pd.concat(parts, axis=1).sort_index().ffill()
    if "QQQ" in market:
        q = market["QQQ"]["close"]
        s50, s200 = q.rolling(50).mean(), q.rolling(200).mean()
        reg = pd.Series(np.where(q < s200, 0.0, np.where(s50 > s200, 2.0, 1.0)), index=q.index).where(s200.notna())
        m["ndx_regime"] = reg.reindex(m.index).ffill()
        m["qqq_2150"] = _above_2150(q).reindex(m.index).ffill()
    if "SPY" in market:
        m["spy_2150"] = _above_2150(market["SPY"]["close"]).reindex(m.index).ffill()
    return m.reindex(columns=MARKET_COLS + VIX_COLS + REGIME_COLS)


SUPER_HORIZON, SUPER_GAIN, SAMPLE_EVERY = 63, 0.40, 10
BRACKETS = {"b10": 0.10, "b20": 0.20}   # user goal: +10% / +20% before -10% (run 13)
BRACKET_STOP = 0.10
# run 17: the bracket menu. Hit rate is mostly set by where the target and stop sit; which
# bracket gives the best return per month of capital, and the best portfolio?
MENU_TARGETS = (0.05, 0.10, 0.15, 0.20, 0.30)
MENU_STOPS = (0.05, 0.08, 0.10, 0.15)
MENU = {f"m{int(round(u * 100))}_{int(round(d * 100))}": (u, d) for u in MENU_TARGETS for d in MENU_STOPS}


def bracket_outcome(o, h, l, c, idx, up, dn, horizon, cost=0.001):
    """Enter at the close of each idx. Daily bars: +up (high) vs -dn (low), whichever comes first;
    if both happen on the same day the stop is assumed first (conservative). Gaps fill at the open.
    Returns hit (1 target, -1 stop, 0 neither), net return, exit index."""
    n = len(c)
    hit = np.zeros(len(idx))
    ret = np.full(len(idx), np.nan)
    xi = np.minimum(idx + horizon, n - 1)
    done = np.zeros(len(idx), dtype=bool)
    entry = c[idx]
    for k in range(1, horizon + 1):
        j = idx + k
        live = ~done & (j < n)
        if not live.any():
            break
        jj = np.minimum(j, n - 1)
        stop_hit = live & (l[jj] <= entry * (1 - dn))
        tgt_hit = live & ~stop_hit & (h[jj] >= entry * (1 + up))
        hit[stop_hit], hit[tgt_hit] = -1, 1
        ret[stop_hit] = np.minimum(o[jj], entry * (1 - dn))[stop_hit] / entry[stop_hit] - 1
        ret[tgt_hit] = np.maximum(o[jj], entry * (1 + up))[tgt_hit] / entry[tgt_hit] - 1
        xi[stop_hit | tgt_hit] = jj[stop_hit | tgt_hit]
        done |= stop_hit | tgt_hit
    rest = ~done
    ret[rest] = c[xi[rest]] / entry[rest] - 1
    return hit, ret - 2 * cost, xi


def superperformer_sample(ticker, df, feats_all, rs_rank, grp, warmup=252) -> pd.DataFrame:
    """Every 10th trading day of every stock, with its chart state and whether it went on to
    gain >= 40% (intraday high) within the next 63 trading days: the 'superperformance' that
    O'Neil and Minervini studied by hand. The label uses future data by design; the features
    don't, and the walk-forward training only uses rows whose 63-day window has fully ended."""
    n = len(df)
    idx = np.arange(warmup, n, SAMPLE_EVERY)
    if len(idx) == 0:
        return pd.DataFrame()
    c, h = df["close"].to_numpy(float), df["high"].to_numpy(float)
    fwd_max = pd.Series(h).rolling(SUPER_HORIZON).max().shift(-SUPER_HORIZON).to_numpy()
    fwd_ret = pd.Series(c).shift(-SUPER_HORIZON).to_numpy() / c - 1
    out = feats_all.iloc[idx][[x for x in ML_FEATURES + ["dollar_vol_50"] if x in feats_all]].reset_index(drop=True)
    out.insert(0, "date", df.index[idx])
    out.insert(0, "ticker", ticker)
    out["rs_rank"] = rs_rank.reindex(df.index).to_numpy()[idx]
    for col in GROUP_COLS + GROUP_EXTRA:
        out[col] = grp[col].reindex(df.index).to_numpy()[idx] if grp is not None and col in grp else np.nan
    out["fwd_max_gain"] = fwd_max[idx] / c[idx] - 1
    # "clean" superperformer: reaches +40% before it ever trades 20% below the starting close
    l = df["low"].to_numpy(float)
    first_up = np.full(len(idx), np.inf)
    first_dn = np.full(len(idx), np.inf)
    for k in range(SUPER_HORIZON, 0, -1):   # iterate backwards so the earliest hit wins
        j = np.minimum(idx + k, n - 1)
        first_up = np.where(h[j] >= 1.4 * c[idx], k, first_up)
        first_dn = np.where(l[j] <= 0.8 * c[idx], k, first_dn)
    out["clean_super"] = ((first_up < first_dn) & np.isfinite(first_up)).astype("float32")
    o = df["open"].to_numpy(float)
    for name, up in BRACKETS.items():
        hit, bret, bxi = bracket_outcome(o, h, l, c, idx, up, BRACKET_STOP, SUPER_HORIZON)
        out[f"{name}_hit"] = (hit == 1).astype("float32")
        out[f"{name}_ret"] = bret
        out[f"{name}_exit"] = df.index[bxi]
    menu = {}
    for name, (up, dn) in MENU.items():
        _, mret, mxi = bracket_outcome(o, h, l, c, idx, up, dn, SUPER_HORIZON)
        menu[f"{name}_ret"] = mret
        menu[f"{name}_days"] = (mxi - idx).astype("int16")
    out = pd.concat([out, pd.DataFrame(menu)], axis=1)
    out["fwd_ret_63"] = fwd_ret[idx]
    out["label_end"] = df.index[np.minimum(idx + SUPER_HORIZON, n - 1)]
    unknown = idx + SUPER_HORIZON > n - 1
    out.loc[unknown, ["fwd_max_gain", "fwd_ret_63", "clean_super"] + [f"{b}_{x}" for b in BRACKETS for x in ("hit", "ret")]
            + [f"{m}_ret" for m in MENU]] = np.nan
    out["close"] = c[idx]
    # run 22 (user): how far price is stretched above its 200-day average
    out["ext_200"] = c[idx] / pd.Series(c).rolling(200).mean().to_numpy()[idx] - 1
    # short-horizon features (concrete daily/weekly data only) and next 1/3/5-day labels
    from mlalgo.research.shortterm import short_features, short_labels
    sf = short_features(df).iloc[idx].reset_index(drop=True)
    sl = short_labels(df).iloc[idx].reset_index(drop=True)
    out = pd.concat([out.reset_index(drop=True), sf, sl], axis=1)
    ok = (c[idx] >= 5) & (c[idx] * feats_all["avg_vol_50"].to_numpy()[idx] >= 5e6)
    return out[ok].astype({k: "float32" for k in out.select_dtypes("float64").columns})


def process_ticker(args):
    ticker, df, rs_rank, grp, max_days, cost, seed = args
    b = bars(df)
    feats_all = structure_features(df)
    feats_all["setup_score"] = setup_score(feats_all)
    sample = superperformer_sample(ticker, df, feats_all, rs_rank, grp)
    sig = all_signals(df, b, seed=seed)
    if sig.empty:
        return None, sample
    idx = sig["idx"].to_numpy()
    ret, rmult, xidx, reason = engine.simulate_all(
        b["o"], b["h"], b["l"], b["c"], b["sma10"], b["sma20"], b["sma50"], b["ema8"], b["ema21"], b["ema50"],
        b["atr20"], b["low10prev"], b["wkx"], idx, sig["entry"].to_numpy(), sig["stop"].to_numpy(), EXIT_CODES, max_days, cost)
    feats = feats_all.iloc[idx].reset_index(drop=True)
    out = pd.DataFrame({"ticker": ticker, "date": df.index[idx], "entry_name": sig["entry_name"].to_numpy(),
                        "entry": sig["entry"].to_numpy(), "stop": sig["stop"].to_numpy()})
    for col in SIGNAL_EXTRAS:
        out[col] = sig[col].to_numpy() if col in sig else np.nan
    out["rs_rank"] = rs_rank.reindex(df.index).to_numpy()[idx]
    for col in GROUP_COLS + GROUP_EXTRA:
        out[col] = grp[col].reindex(df.index).to_numpy()[idx] if grp is not None and col in grp else np.nan
    out = pd.concat([out, feats[[c for c in ML_FEATURES + ["trend_template", "dollar_vol_50"] if c in feats]]], axis=1)
    dates = df.index.to_numpy()
    for j, name in enumerate(EXIT_NAMES):
        out[f"R_{name}"] = rmult[:, j].astype("float32")
        out[f"ret_{name}"] = ret[:, j].astype("float32")
        out[f"days_{name}"] = (xidx[:, j] - idx).astype("int16")
        out[f"exit_{name}"] = dates[xidx[:, j]]
        out[f"reason_{name}"] = reason[:, j].astype("int8")
        out.loc[xidx[:, j] == len(dates) - 1, f"reason_{name}"] = 0  # still open at data end
    return out, sample


def perf_rank(prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Qullamaggie's scan: the best performers over 1, 3 or 6 months. Per day, each stock's best
    percentile rank across the three look-backs (0.98 = top 2% on at least one of them)."""
    ranks = []
    for n in (21, 63, 126):
        r = pd.DataFrame({t: df["close"] / df["close"].shift(n) - 1 for t, df in prices.items()})
        ranks.append(r.rank(axis=1, pct=True))
    return pd.concat(ranks).groupby(level=0).max().astype("float32")


def ret_rank(prices: dict[str, pd.DataFrame], n: int = 126) -> pd.DataFrame:
    """Per-day percentile of each stock's n-day return (workflow PDF: top 20% over 6 months)."""
    r = pd.DataFrame({t: df["close"] / df["close"].shift(n) - 1 for t, df in prices.items()})
    return r.rank(axis=1, pct=True).astype("float32")


def group_momentum(prices: dict[str, pd.DataFrame], groups: pd.Series, min_members: int = 3) -> dict[str, pd.DataFrame]:
    """Equal-weight group index from members' median daily return: today's return, 5-day return,
    and whether the index is above its 21-day EMA. Groups with < min_members stocks are NaN."""
    rets = pd.DataFrame({t: df["close"].pct_change() for t, df in prices.items()})
    g = groups.reindex(rets.columns)
    med = rets.T.groupby(g).median().T
    cnt = rets.T.groupby(g).count().T
    med = med.where(cnt >= min_members)
    idx = (1 + med.fillna(0)).cumprod().where(med.notna())
    return {"ret1": med.astype("float32"), "ret5": (idx / idx.shift(5) - 1).astype("float32"),
            "up21": (idx > idx.ewm(span=21, adjust=False).mean()).astype("float32").where(med.notna())}


def group_frames(rank: pd.DataFrame, universe: pd.DataFrame | None, tickers,
                 qrank: pd.DataFrame | None = None, r6: pd.DataFrame | None = None,
                 prices: dict[str, pd.DataFrame] | None = None) -> dict[str, pd.DataFrame]:
    """Per-ticker sub-industry / sector RS series (empty if the universe has no sector info)."""
    grp = {}
    if qrank is not None:
        for t in tickers:
            grp[t] = pd.DataFrame({"qull_rank": qrank[t] if t in qrank else np.nan}, index=rank.index)
    if r6 is not None:
        for t in tickers:
            g = pd.DataFrame({"r6_rank": r6[t] if t in r6 else np.nan}, index=rank.index)
            grp[t] = g if t not in grp else pd.concat([grp[t], g], axis=1)
    if universe is None or "sub_industry" not in universe:
        return grp
    u = universe.drop_duplicates("ticker").set_index("ticker")
    ind_rs, ind_rank = group_strength(rank, u["sub_industry"].replace("nan", np.nan))
    sec_rs, sec_rank = group_strength(rank, u["sector"].replace("nan", np.nan))
    mom = {}
    if prices is not None:
        mom["sec"] = group_momentum(prices, u["sector"].replace("nan", np.nan))
        mom["ind"] = group_momentum(prices, u["sub_industry"].replace("nan", np.nan))
    for t in tickers:
        if t in u.index:
            sub, sec = u.at[t, "sub_industry"], u.at[t, "sector"]
            g = pd.DataFrame({
                "industry_rs": ind_rs[sub] if sub in ind_rs else np.nan,
                "industry_rank": ind_rank[sub] if sub in ind_rank else np.nan,
                "sector_rs": sec_rs[sec] if sec in sec_rs else np.nan,
                "sector_rank": sec_rank[sec] if sec in sec_rank else np.nan,
                **{f"{k}_{f}": (mom[k][f][grp_] if grp_ in mom[k][f] else np.nan)
                   for k, grp_ in (("sec", sec), ("ind", sub)) if k in mom for f in ("ret1", "ret5", "up21")}},
                index=rank.index).astype("float32")
            grp[t] = g if t not in grp else pd.concat([grp[t], g], axis=1)
    return grp


def run(prices: dict[str, pd.DataFrame], market: dict[str, pd.DataFrame], max_days: int = 250,
        cost: float = 0.001, workers: int | None = None, universe: pd.DataFrame | None = None) -> pd.DataFrame:
    rank, breadth = cross_section(prices)
    mkt = market_frame(market, breadth, market_internals(prices))
    grp = group_frames(rank, universe, prices, qrank=perf_rank(prices), r6=ret_rank(prices), prices=prices)
    tasks = [(t, df, rank[t], grp.get(t), max_days, cost, i) for i, (t, df) in enumerate(prices.items())]
    workers = workers or os.cpu_count() or 1
    frames, samples = [], []

    def collect(results):
        for k, (res, smp) in enumerate(results):
            if res is not None:
                frames.append(res)
            if smp is not None and len(smp):
                samples.append(smp)
            if (k + 1) % 200 == 0:
                print(f"[run] {k + 1}/{len(tasks)} tickers")

    if workers > 1:
        with ProcessPoolExecutor(workers) as ex:
            collect(ex.map(process_ticker, tasks, chunksize=10))
    else:
        collect(map(process_ticker, tasks))

    def with_market(d):
        m = mkt.reindex(mkt.index.union(pd.DatetimeIndex(d["date"].unique()))).ffill()
        d = d.join(m, on="date")
        fc = d.select_dtypes("float64").columns
        d[fc] = d[fc].astype("float32")
        return d.sort_values(["date", "ticker"]).reset_index(drop=True)

    sig = with_market(pd.concat(frames, ignore_index=True))
    sample = with_market(pd.concat(samples, ignore_index=True)) if samples else pd.DataFrame()
    return sig, sample
