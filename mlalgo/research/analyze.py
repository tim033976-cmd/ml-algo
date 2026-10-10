"""Evaluate every (entry x filter x exit) strategy in-sample vs out-of-sample, compare to a
random-entry baseline, train an ML meta-labeling model walk-forward, extract readable rules,
and simulate a capital-constrained portfolio for the best candidates."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from mlalgo.research.entries import ENTRIES
from mlalgo.research.run import EXIT_NAMES, GROUP_COLS, MARKET_COLS, SIGNAL_EXTRAS, VIX_COLS
from mlalgo.research.shortterm import SHORT_FEATURES
from mlalgo.structure import ML_FEATURES

IS_END = pd.Timestamp("2018-01-01")
BASELINE = "random_uptrend"
FILTERS = {
    "all": lambda s: np.ones(len(s), bool),
    "mkt_ok": lambda s: (s["mkt_ok"] == 1).to_numpy(),
    "rs80": lambda s: (s["rs_rank"] >= 0.8).to_numpy(),
    "early_stage": lambda s: s["base_count"].between(1, 2).to_numpy(),
    "rs80_mkt": lambda s: ((s["rs_rank"] >= 0.8) & (s["mkt_ok"] == 1)).to_numpy(),
    "rs80_early": lambda s: ((s["rs_rank"] >= 0.8) & s["base_count"].between(1, 2)).to_numpy(),
    # Qullamaggie's scan: top 3% performer over 1/3/6 months and ADR >= 4%; and with his regime rule
    "qull_scan": lambda s: ((s["qull_rank"] >= 0.97) & (s["adr_pct"] >= 0.04)).to_numpy(),
    "qull_scan_regime": lambda s: ((s["qull_rank"] >= 0.97) & (s["adr_pct"] >= 0.04) & (s["qqq_trend"] == 1)).to_numpy(),
    # "hot theme": the stock's sub-industry is in the top 30% of sub-industries by median RS
    "theme": lambda s: (s["industry_rank"] >= 0.7).to_numpy(),
    "rs80_theme": lambda s: ((s["rs_rank"] >= 0.8) & (s["industry_rank"] >= 0.7)).to_numpy(),
    "rs80_early_theme": lambda s: ((s["rs_rank"] >= 0.8) & s["base_count"].between(1, 2) & (s["industry_rank"] >= 0.7)).to_numpy(),
    # run 20, the user's workflow PDF. Rockets: price >= $10, >= $20M a day, top 20% 6-month return.
    "wf_rocket": lambda s: ((s["entry"] >= 10) & (s["dollar_vol_50"] >= 20e6) & (s["r6_rank"] >= 0.8)).to_numpy(),
    "wf_rocket_green": lambda s: ((s["entry"] >= 10) & (s["dollar_vol_50"] >= 20e6) & (s["r6_rank"] >= 0.8)
                                  & (s["ndx_regime"] == 2)).to_numpy(),
    # scanner: above a rising 200d, 50d > 200d, within 15% of the 52w high; logical stop <= 10% away
    "wf_scan": lambda s: ((s["uptrend_tpl"] == 1) & (s["risk_pct"] <= 0.10)).to_numpy(),
    "wf_scan_green": lambda s: ((s["uptrend_tpl"] == 1) & (s["risk_pct"] <= 0.10) & (s["ndx_regime"] == 2)).to_numpy(),
}
FEATURES = list(dict.fromkeys(ML_FEATURES + SIGNAL_EXTRAS + MARKET_COLS + GROUP_COLS + ["rs_rank"]))


def _stats(R: np.ndarray, ret: np.ndarray, years: float) -> dict:
    n = len(R)
    if n == 0:
        return {"n": 0}
    sd = R.std(ddof=1) if n > 1 else np.nan
    gains, losses = R[R > 0].sum(), -R[R <= 0].sum()
    return {"n": n, "per_yr": n / years, "win": (R > 0).mean(), "avgR": R.mean(), "medR": np.median(R),
            "pf": gains / losses if losses > 0 else np.inf, "t": R.mean() / sd * np.sqrt(n) if sd and sd > 0 else np.nan,
            "R_per_yr": R.sum() / years, "avg_ret": ret.mean()}


def split(sig: pd.DataFrame, exit_name: str):
    is_mask = (sig[f"exit_{exit_name}"] < IS_END).to_numpy()
    oos_mask = (sig["date"] >= IS_END).to_numpy()
    return is_mask, oos_mask


def leaderboard(sig: pd.DataFrame) -> pd.DataFrame:
    first, last = sig["date"].min(), sig["date"].max()
    is_years = (IS_END - first).days / 365.25
    oos_years = (last - IS_END).days / 365.25
    rows = []
    for entry, s in sig.groupby("entry_name"):
        fmasks = {f: fn(s) for f, fn in FILTERS.items()}
        for ex in EXIT_NAMES:
            R, ret = s[f"R_{ex}"].to_numpy(float), s[f"ret_{ex}"].to_numpy(float)
            is_m, oos_m = split(s, ex)
            for f, fm in fmasks.items():
                a = _stats(R[fm & is_m], ret[fm & is_m], is_years)
                b = _stats(R[fm & oos_m], ret[fm & oos_m], oos_years)
                rows.append({"entry": entry, "filter": f, "exit": ex,
                             **{f"IS_{k}": v for k, v in a.items()}, **{f"OOS_{k}": v for k, v in b.items()}})
    lb = pd.DataFrame(rows)
    return lb.sort_values("IS_t", ascending=False).reset_index(drop=True)


def selection_check(lb: pd.DataFrame, min_is: int = 100, min_oos: int = 50) -> dict:
    v = lb[(lb["IS_n"] >= min_is) & (lb["OOS_n"] >= min_oos) & (lb["entry"] != BASELINE)]
    top = v.nlargest(20, "IS_t")
    top_avg = v[v["IS_n"] >= 200].nlargest(20, "IS_avgR")
    base = lb[lb["entry"] == BASELINE]
    return {
        "strategies_tested": int(len(lb)),
        "strategies_with_enough_trades": int(len(v)),
        "rank_corr_IS_vs_OOS_avgR": float(v["IS_avgR"].corr(v["OOS_avgR"], method="spearman")),
        "rank_corr_IS_vs_OOS_t": float(v["IS_t"].corr(v["OOS_t"], method="spearman")),
        "OOS_avgR_all_strategies": float(v["OOS_avgR"].mean()),
        "OOS_avgR_top20_by_IS": float(top["OOS_avgR"].mean()),
        "OOS_avgR_top20_by_IS_avgR": float(top_avg["OOS_avgR"].mean()),
        "OOS_avgR_random_baseline": float(base["OOS_avgR"].mean()),
        "share_top20_positive_OOS": float((top["OOS_avgR"] > 0).mean()),
    }


def vs_baseline(lb: pd.DataFrame, filt: str = "all", period: str = "OOS") -> pd.DataFrame:
    """avgR of each entry minus the random baseline with the same exit and filter."""
    t = lb[lb["filter"] == filt].pivot(index="entry", columns="exit", values=f"{period}_avgR")
    return (t - t.loc[BASELINE]).drop(index=BASELINE)


def entry_summary(lb: pd.DataFrame) -> pd.DataFrame:
    """For each entry, pick the exit and filter with the best IS t-stat, then show OOS."""
    v = lb[lb["IS_n"] >= 50]
    best = v.loc[v.groupby("entry")["IS_t"].idxmax()]
    cols = ["entry", "filter", "exit", "IS_n", "IS_per_yr", "IS_win", "IS_avgR", "IS_t",
            "OOS_n", "OOS_per_yr", "OOS_win", "OOS_avgR", "OOS_pf", "OOS_t", "OOS_R_per_yr"]
    return best[cols].sort_values("OOS_avgR", ascending=False).reset_index(drop=True)


def exit_summary(lb: pd.DataFrame) -> pd.DataFrame:
    v = lb[(lb["filter"] == "all") & (lb["entry"] != BASELINE)]
    out = v.groupby("exit")[["IS_avgR", "OOS_avgR", "OOS_win", "OOS_pf"]].mean()
    out["OOS_beats_baseline_share"] = vs_baseline(lb).gt(0).mean()
    return out.sort_values("OOS_avgR", ascending=False)


# ------------------------------------------------------------------ ML meta-labeling
# Run 1 lesson: a classifier on "R > 0" learned that wider stops win more often (higher win rate,
# same avg R). The model now predicts R itself (clipped so one 30R outlier can't dominate).
R_CLIP = (-2.0, 8.0)


def _model():
    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
                                         min_samples_leaf=300, l2_regularization=1.0, random_state=0)


def _target(d, exit_name):
    return d[f"R_{exit_name}"].clip(*R_CLIP).to_numpy()


def _rank_corr(estimator, X, y):
    return spearmanr(estimator.predict(X), y).statistic


def ml_dataset(sig: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    d = sig[sig["entry_name"] != BASELINE].copy()
    # setup-specific features are NaN for other setups by design; an all-NaN column breaks HGB
    specific = ["prior_move", "flag_depth", "flag_days", "base_depth", "contraction",
                "pattern_len", "pattern_width", "pattern_touches", "coil_range"]
    d[specific] = d[specific].fillna(-1)
    for c in FEATURES:
        if d[c].isna().all():
            d[c] = 0.0
    onehot = pd.get_dummies(d["entry_name"], prefix="is").astype("float32")
    d = pd.concat([d, onehot], axis=1)
    return d, FEATURES + list(onehot.columns)


def ml_walk_forward(sig: pd.DataFrame, exit_name: str, max_train: int = 250_000, min_train: int = 5000):
    d, cols = ml_dataset(sig)
    y = _target(d, exit_name)
    years = sorted(d["date"].dt.year.unique())
    prob = pd.Series(np.nan, index=d.index)
    take = pd.Series(False, index=d.index)
    rng = np.random.default_rng(0)
    for yr in years:
        start = pd.Timestamp(f"{yr}-01-01")
        tr = np.flatnonzero((d[f"exit_{exit_name}"] < start).to_numpy())
        te = np.flatnonzero((d["date"].dt.year == yr).to_numpy())
        if len(tr) < min_train or len(te) == 0:
            continue
        if len(tr) > max_train:
            tr = rng.choice(tr, max_train, replace=False)
        m = _model().fit(d.iloc[tr][cols], y[tr])
        thr = np.quantile(m.predict(d.iloc[tr][cols]), 2 / 3)  # causal top-third cut
        p = m.predict(d.iloc[te][cols])
        prob.iloc[te], take.iloc[te] = p, p >= thr
    d["prob"], d["take"] = prob, take
    return d, cols


def ml_report(d: pd.DataFrame, exit_name: str) -> dict:
    o = d[(d["date"] >= IS_END) & d["prob"].notna()]
    R = o[f"R_{exit_name}"]
    deciles = o.groupby(pd.qcut(o["prob"], 10, labels=False, duplicates="drop"))[f"R_{exit_name}"].agg(
        n="count", avgR="mean", win=lambda r: (r > 0).mean())
    per_entry = o.groupby("entry_name").apply(lambda g: pd.Series({
        "n_all": len(g), "avgR_all": g[f"R_{exit_name}"].mean(),
        "n_taken": int(g["take"].sum()), "avgR_taken": g.loc[g["take"], f"R_{exit_name}"].mean(),
        "avgR_skipped": g.loc[~g["take"], f"R_{exit_name}"].mean()}), include_groups=False)
    return {"auc_oos": roc_auc_score(R > 0, o["prob"]), "rank_corr_oos": spearmanr(o["prob"], R).statistic,
            "deciles": deciles,
            "per_entry": per_entry.sort_values("avgR_taken", ascending=False),
            "taken": {"n": int(o["take"].sum()), "avgR": R[o["take"]].mean(), "win": (R[o["take"]] > 0).mean()},
            "skipped": {"n": int((~o["take"]).sum()), "avgR": R[~o["take"]].mean(), "win": (R[~o["take"]] > 0).mean()}}


def ml_importance(d: pd.DataFrame, cols: list[str], exit_name: str, n_eval: int = 60_000) -> pd.DataFrame:
    is_m = d[f"exit_{exit_name}"] < IS_END
    tr = d[is_m].sample(min(250_000, int(is_m.sum())), random_state=0)
    te = d[d["date"] >= IS_END]
    te = te.sample(min(n_eval, len(te)), random_state=0)
    m = _model().fit(tr[cols], _target(tr, exit_name))
    pi = permutation_importance(m, te[cols], _target(te, exit_name), scoring=_rank_corr, n_repeats=3, random_state=0)
    return pd.DataFrame({"feature": cols, "rank_corr_drop": pi.importances_mean}).sort_values("rank_corr_drop", ascending=False)


def rule_tree(d: pd.DataFrame, cols: list[str], exit_name: str, depth: int = 3) -> pd.DataFrame:
    """Shallow tree on in-sample data -> human-readable rules, each scored out-of-sample."""
    feat = [c for c in cols if not c.startswith("is_")] + [c for c in cols if c.startswith("is_")]
    is_d = d[d[f"exit_{exit_name}"] < IS_END]
    oos_d = d[d["date"] >= IS_END]
    X = is_d[feat].fillna(-999)
    tree = DecisionTreeRegressor(max_depth=depth, min_samples_leaf=max(2000, len(is_d) // 100), random_state=0)
    tree.fit(X, is_d[f"R_{exit_name}"].clip(-3, 10))
    t = tree.tree_

    paths = {}

    def walk(node, conds):
        if t.children_left[node] == -1:
            paths[node] = " AND ".join(conds) or "(all)"
            return
        f, thr = feat[t.feature[node]], t.threshold[node]
        walk(t.children_left[node], conds + [f"{f} <= {thr:.3g}"])
        walk(t.children_right[node], conds + [f"{f} > {thr:.3g}"])

    walk(0, [])
    is_leaf = tree.apply(X)
    oos_leaf = tree.apply(oos_d[feat].fillna(-999))
    rows = []
    for leaf, rule in paths.items():
        a = is_d[f"R_{exit_name}"].to_numpy()[is_leaf == leaf]
        b = oos_d[f"R_{exit_name}"].to_numpy()[oos_leaf == leaf]
        rows.append({"rule": rule, "IS_n": len(a), "IS_avgR": a.mean() if len(a) else np.nan,
                     "OOS_n": len(b), "OOS_avgR": b.mean() if len(b) else np.nan,
                     "OOS_win": (b > 0).mean() if len(b) else np.nan})
    return pd.DataFrame(rows).sort_values("IS_avgR", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------ portfolio simulation
def portfolio(trades: pd.DataFrame, exit_name: str, priority: str, start=IS_END, capital=100_000.0,
              risk=0.01, max_pos=10, pos_cap=0.20, closes: pd.DataFrame | None = None,
              idle: pd.Series | None = None, adaptive: bool = False) -> dict:
    """Fixed-fractional sizing (1% equity at risk per trade), max 10 positions, no leverage.
    With `closes` (dates x tickers), open positions are marked to market every day, so the
    drawdown is honest; without it equity only moves when trades close (run 1-3 reports).
    `idle`: close prices of an asset (e.g. SPY) that uninvested cash is held in (run 5: EP
    portfolios averaged ~6 of 10 slots filled, with the rest of the cash earning nothing).
    `size_mult` column (optional): per-trade multiplier of the risk; 0 skips the trade.
    `adaptive`: size like a discretionary pro, by how the strategy is working right now: risk
    x0.5 when the last 20 closed trades averaged < 0R, x1.5 when > +0.5R (only closed trades)."""
    t = trades[trades["date"] >= start].copy()
    if exit_name == "per_row":  # each row carries its own exit plan in `exit_choice`
        t["exit_date"], t["ret"] = pd.NaT, np.nan
        for ex in t["exit_choice"].unique():
            m = t["exit_choice"] == ex
            t.loc[m, "exit_date"] = t.loc[m, f"exit_{ex}"]
            t.loc[m, "ret"] = t.loc[m, f"ret_{ex}"].astype(float)
        t["exit_date"] = pd.to_datetime(t["exit_date"])
    else:
        t["exit_date"] = t[f"exit_{exit_name}"]
        t["ret"] = t[f"ret_{exit_name}"].astype(float)
    t = t.sort_values(["date", priority], ascending=[True, False])
    by_day = {d: g for d, g in t.groupby("date", sort=True)}
    if closes is not None:
        days = list(closes.index[closes.index >= start])
        px = closes
    else:
        days = sorted(set(t["date"]) | set(t["exit_date"]))
        px = None
    cash, realized = capital, capital
    open_pos: list[tuple] = []          # (exit_date, alloc, ret, ticker, entry_price, risk_pct)
    closed_R: list[float] = []
    curve, taken = [], []
    idle_ret = idle.pct_change().fillna(0) if idle is not None else None
    for day in days:
        if idle_ret is not None and day in idle_ret.index:
            gain = cash * float(idle_ret.at[day])
            cash += gain
            realized += gain
        still = []
        for pos in open_pos:
            if pos[0] <= day:
                cash += pos[1] * (1 + pos[2])
                realized += pos[1] * pos[2]
                taken.append(pos[2])
                closed_R.append(pos[2] / max(pos[5], 1e-4))
            else:
                still.append(pos)
        open_pos = still
        g = by_day.get(day)
        if g is not None:
            held = {p[3] for p in open_pos}
            mult = 1.0
            if adaptive and len(closed_R) >= 20:
                recent = float(np.mean(closed_R[-20:]))
                mult = 0.5 if recent < 0 else (1.5 if recent > 0.5 else 1.0)
            for r in g.itertuples(index=False):
                if len(open_pos) >= max_pos:
                    break
                if r.ticker in held or r.exit_date <= day:
                    continue
                size = mult * getattr(r, "size_mult", 1.0)   # run 20: per-trade size (regime half size)
                if size <= 0:
                    continue
                alloc = min(realized * risk * size / max(r.risk_pct, 1e-4), realized * pos_cap, cash)
                if alloc < realized * 0.02:
                    continue
                cash -= alloc
                open_pos.append((r.exit_date, alloc, r.ret, r.ticker, r.entry, r.risk_pct))
                held.add(r.ticker)
        if px is not None:
            mtm = cash
            for pos in open_pos:
                c = px.at[day, pos[3]] if pos[3] in px.columns else np.nan
                mtm += pos[1] * (c / pos[4]) if c == c else pos[1]
        else:
            mtm = realized
        curve.append((day, realized, mtm, len(open_pos)))
    eq = pd.DataFrame(curve, columns=["date", "realized", "equity", "positions"]).set_index("date")
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    dd = lambda x: (x / x.cummax() - 1).min()
    taken = np.array(taken)
    return {"CAGR": (eq["equity"].iloc[-1] / capital) ** (1 / years) - 1,
            "max_DD": dd(eq["equity"]), "max_DD_realized": dd(eq["realized"]),
            "trades": len(taken), "win": (taken > 0).mean() if len(taken) else np.nan,
            "avg_positions": eq["positions"].mean(), "final_equity": eq["equity"].iloc[-1], "curve": eq["equity"]}


def spy_stats(spy: pd.DataFrame, start=IS_END) -> dict:
    c = spy["close"][spy.index >= start]
    years = (c.index[-1] - c.index[0]).days / 365.25
    return {"CAGR": (c.iloc[-1] / c.iloc[0]) ** (1 / years) - 1, "max_DD": (c / c.cummax() - 1).min()}


def strategy_pool(sig: pd.DataFrame, picks: pd.DataFrame) -> pd.DataFrame:
    """Signals of several (entry, filter, exit) strategies combined; when two strategies fire on
    the same stock and day, keep the one ranked higher in `picks` (row order)."""
    parts = []
    for rank, r in enumerate(picks.itertuples()):
        s = sig[sig["entry_name"] == r.entry]
        s = s[FILTERS[r.filter](s)]
        parts.append(s.assign(exit_choice=r.exit, strategy_rank=rank))
    pool = pd.concat(parts).sort_values("strategy_rank")
    return pool.drop_duplicates(["date", "ticker"], keep="first")


def yearly(curve: pd.Series) -> pd.Series:
    y = curve.groupby(curve.index.year).last()
    first = curve.iloc[0]
    return pd.concat([pd.Series([y.iloc[0] / first - 1], index=[y.index[0]]), y.pct_change().iloc[1:]])


def concentration(curve: pd.Series) -> float:
    """Share of the total log-return that came from the two best calendar years."""
    y = np.log1p(yearly(curve))
    total = y.sum()
    return float(y.nlargest(2).sum() / total) if total > 0 else np.nan


# ------------------------------------------------------------------ superperformer model
# "How do top traders do it?" They spend their time finding the stocks that are about to make
# huge moves (O'Neil / Minervini studied hundreds of big winners by hand). This model learns that
# directly: from every stock every 10 days, which chart / RS / market states preceded a >= 40%
# gain within 3 months. Walk-forward by year; a row is only trained on once its 3-month label
# window has ended before the test year starts.
# user goal (run 13): daily chart, +10% / +20% before -10%. Break-even hit rates ignore the
# trades that time out at 63 days, which the expected-return column includes.
GOALS = {"b10": ("+10% before -10%", 0.50), "b20": ("+20% before -10%", 1 / 3)}
SHORT_LABELS = {"green1": "next day green (close > open)", "up1": "up next day (close to close)",
                "up3": "up over the next 3 days", "up5": "up over the next week (5 days)"}
SUPER_FEATURES = list(dict.fromkeys(ML_FEATURES + MARKET_COLS + GROUP_COLS + ["rs_rank"]))


def _super_model():
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
                                          min_samples_leaf=500, l2_regularization=1.0, random_state=0)


def _label(d, label):
    if label == "clean" and "clean_super" in d:
        return (d["clean_super"] == 1).to_numpy()
    if label in GOALS:
        return (d[f"{label}_hit"] == 1).to_numpy() if f"{label}_hit" in d else None
    if label in SHORT_LABELS:
        return (d[f"y_{label}"] == 1).to_numpy() if f"y_{label}" in d else None
    return (d["fwd_max_gain"] >= 0.40).to_numpy() if "fwd_max_gain" in d else None


def _xy(d, label="gain40", features=None):
    features = features or SUPER_FEATURES
    X = d.reindex(columns=features).copy()
    for c in features:
        if X[c].isna().all():
            X[c] = 0.0
    return X, _label(d, label)


def super_walk_forward(sample: pd.DataFrame, score: list[pd.DataFrame], max_train: int = 200_000,
                       label: str = "gain40", col: str = "super_prob", features=None, step: int = 1):
    """Adds `col` (predicted probability) to `sample` and to every frame in `score`.
    label: 'gain40' = high >= +40% within 3 months; 'clean' = +40% before -20%."""
    sample = sample.copy()
    sample[col] = np.nan
    score = [f.copy() for f in score]
    for f in score:
        f[col] = np.nan
    rng = np.random.default_rng(0)
    lab_col = f"y_{label}" if label in SHORT_LABELS else "fwd_max_gain"
    known = sample[lab_col].notna()
    years = sorted(sample["date"].dt.year.unique())
    for yr in years[::step]:
        start = pd.Timestamp(f"{yr}-01-01")
        test_years = [y for y in years if yr <= y < yr + step]
        tr = np.flatnonzero((known & (sample["label_end"] < start)).to_numpy())
        if len(tr) < 20_000:
            continue
        if len(tr) > max_train:
            tr = rng.choice(tr, max_train, replace=False)
        X, y = _xy(sample.iloc[tr], label, features)
        if y.sum() < 200:
            continue
        m = _super_model().fit(X, y)
        te = sample["date"].dt.year.isin(test_years).to_numpy()
        sample.loc[te, col] = m.predict_proba(_xy(sample[te], features=features)[0])[:, 1]
        for f in score:
            fm = f["date"].dt.year.isin(test_years).to_numpy()
            if fm.any():
                f.loc[fm, col] = m.predict_proba(_xy(f[fm], features=features)[0])[:, 1]
    return sample, score


def super_report(sample: pd.DataFrame, label: str = "gain40", col: str = "super_prob") -> dict:
    o = sample[(sample["date"] >= IS_END) & sample[col].notna() & sample["fwd_max_gain"].notna()]
    y = pd.Series(_label(o, label), index=o.index)
    o = o.assign(_y=y)
    dec = o.groupby(pd.qcut(o[col], 10, labels=False, duplicates="drop")).agg(
        n=("fwd_max_gain", "size"), hit_rate=("_y", "mean"),
        avg_3m_return=("fwd_ret_63", "mean"), median_3m_return=("fwd_ret_63", "median"),
        share_down_20pct=("fwd_ret_63", lambda r: (r <= -0.20).mean()))
    return {"n": len(o), "base_rate": float(y.mean()), "auc": float(roc_auc_score(y, o[col])),
            "top_decile_rate": float(dec["hit_rate"].iloc[-1]), "deciles": dec}


def super_explain(sample: pd.DataFrame, n_eval: int = 80_000):
    """Permutation importance (model trained before 2018, scored after), readable rules, and a
    profile of what future superperformers looked like vs. everything else."""
    known = sample[sample["fwd_max_gain"].notna()]
    tr = known[known["label_end"] < IS_END]
    tr = tr.sample(min(200_000, len(tr)), random_state=0)
    te = known[known["date"] >= IS_END]
    te = te.sample(min(n_eval, len(te)), random_state=0)
    Xtr, ytr = _xy(tr)
    Xte, yte = _xy(te)
    m = _super_model().fit(Xtr, ytr)
    pi = permutation_importance(m, Xte, yte, scoring="roc_auc", n_repeats=3, random_state=0)
    imp = pd.DataFrame({"feature": SUPER_FEATURES, "auc_drop": pi.importances_mean}).sort_values("auc_drop", ascending=False)

    tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=max(2000, len(tr) // 100), random_state=0)
    tree.fit(Xtr.fillna(-999), ytr)
    t = tree.tree_
    paths = {}

    def walk(node, conds):
        if t.children_left[node] == -1:
            paths[node] = " AND ".join(conds) or "(all)"
            return
        f, thr = SUPER_FEATURES[t.feature[node]], t.threshold[node]
        walk(t.children_left[node], conds + [f"{f} <= {thr:.3g}"])
        walk(t.children_right[node], conds + [f"{f} > {thr:.3g}"])

    walk(0, [])
    li, lo = tree.apply(Xtr.fillna(-999)), tree.apply(Xte.fillna(-999))
    rules = pd.DataFrame([{"rule": r, "IS_n": int((li == k).sum()), "IS_rate": ytr[li == k].mean(),
                           "OOS_n": int((lo == k).sum()), "OOS_rate": yte[lo == k].mean() if (lo == k).any() else np.nan}
                          for k, r in paths.items()]).sort_values("IS_rate", ascending=False)
    top = list(imp["feature"].head(12))
    prof = pd.DataFrame({"future superperformers (median)": te.loc[yte, top].median(),
                         "everything else (median)": te.loc[~yte, top].median()})
    return imp, rules.reset_index(drop=True), prof


def signals_by_super(sig: pd.DataFrame, exit_name: str) -> pd.DataFrame:
    """Do setups in stocks the model flags as likely superperformers pay more? (OOS)"""
    o = sig[(sig["date"] >= IS_END) & sig["super_prob"].notna() & (sig["entry_name"] != BASELINE)]
    g = pd.qcut(o["super_prob"], 3, labels=["low", "mid", "high"])
    return o.groupby(g, observed=True).agg(n=(f"R_{exit_name}", "size"), avgR=(f"R_{exit_name}", "mean"),
                                           win=(f"R_{exit_name}", lambda r: (r > 0).mean()),
                                           avgR_sma50=("R_sma50_close", "mean"))


def goal_report(sample: pd.DataFrame, goal: str, col: str, keep: pd.Series | None = None) -> pd.DataFrame:
    """Out-of-sample: by decile of the model's probability, how often did the stock hit the target
    before the stop, how often the stop, and what was the net return per trade (incl. timeouts)?
    `keep` restricts rows (e.g. point-in-time S&P 500 members); deciles use the full OOS cut-offs."""
    o = sample[(sample["date"] >= IS_END) & sample[col].notna() & sample[f"{goal}_hit"].notna()]
    edges = np.unique(np.quantile(o[col], np.linspace(0, 1, 11)))
    if keep is not None:
        o = o[keep.reindex(o.index).fillna(False).to_numpy()]
    dec = pd.cut(o[col], edges, labels=False, include_lowest=True)
    stop = o[f"{goal}_ret"] <= -(0.10 - 1e-6) - 0.002 + 1e-9
    return o.assign(_stop=stop).groupby(dec).agg(
        n=(col, "size"), predicted=(col, "mean"), hit_target=(f"{goal}_hit", "mean"),
        hit_stop=("_stop", "mean"), avg_net_return=(f"{goal}_ret", "mean"), median_return=(f"{goal}_ret", "median"))


def top_decile_trades(sample: pd.DataFrame, goal: str, col: str, q: float = 0.9) -> pd.DataFrame:
    """Model-only entries: buy at the close of sample days where the score is in the top 10% of that
    year's scores, exit with the bracket. Formatted for portfolio(..., exit_name='bracket')."""
    o = sample[sample[col].notna() & sample[f"{goal}_ret"].notna()]
    o = o[o[col] >= o.groupby(o["date"].dt.year)[col].transform(lambda p: p.quantile(q))]
    return pd.DataFrame({"date": o["date"], "ticker": o["ticker"], "entry": o["close"], "risk_pct": 0.10,
                         "exit_bracket": o[f"{goal}_exit"], "ret_bracket": o[f"{goal}_ret"].astype(float),
                         "priority": o[col], "rs_rank": o["rs_rank"]})


def goal_tiers(sample: pd.DataFrame, goal: str, col: str, keep: pd.Series | None = None) -> pd.DataFrame:
    """Does more confidence mean better odds? Hit rate for the model's top 10/5/2/1% (OOS cut-offs)."""
    o = sample[(sample["date"] >= IS_END) & sample[col].notna() & sample[f"{goal}_hit"].notna()]
    cuts = {f"top {int(round((1 - q) * 100))}%": np.quantile(o[col], q) for q in (0.90, 0.95, 0.98, 0.99)}
    if keep is not None:
        o = o[keep.reindex(o.index).fillna(False).to_numpy()]
    rows = []
    for name, cut in {"all stocks": -np.inf, **cuts}.items():
        g = o[o[col] >= cut]
        rows.append({"tier": name, "n": len(g), "hit_target": g[f"{goal}_hit"].mean(),
                     "hit_stop": (g[f"{goal}_ret"] <= -0.1019).mean(), "avg_net_return": g[f"{goal}_ret"].mean()})
    return pd.DataFrame(rows).set_index("tier")


# feature sets for the short-horizon study (run 16)
SHORT_ALL = list(dict.fromkeys(SUPER_FEATURES + SHORT_FEATURES + VIX_COLS))
SHORT_MARKET_ONLY = list(dict.fromkeys(MARKET_COLS + VIX_COLS + ["dow", "month"]))


def short_report(sample: pd.DataFrame, label: str, col: str) -> dict:
    """OOS: base rate, AUC, accuracy at 50%, and the up-rate / avg return by decile."""
    o = sample[(sample["date"] >= IS_END) & sample[col].notna() & sample[f"y_{label}"].notna()]
    y = o[f"y_{label}"] == 1
    ret_col = {"green1": "r_up1"}.get(label, f"r_{label}")
    dec = o.groupby(pd.qcut(o[col], 10, labels=False, duplicates="drop")).agg(
        n=(col, "size"), predicted=(col, "mean"), actual_up=(f"y_{label}", "mean"), avg_return=(ret_col, "mean"))
    return {"base": float(y.mean()), "auc": float(roc_auc_score(y, o[col])),
            "accuracy": float(((o[col] >= 0.5) == y).mean()),
            "top": float(dec["actual_up"].iloc[-1]), "bottom": float(dec["actual_up"].iloc[0]),
            "spread": float(dec["avg_return"].iloc[-1] - dec["avg_return"].iloc[0]), "deciles": dec}


def short_importance(sample: pd.DataFrame, label: str, features: list[str], n_eval: int = 60_000) -> pd.DataFrame:
    known = sample[sample[f"y_{label}"].notna()]
    tr = known[known["date"] < IS_END].sample(min(200_000, int((known["date"] < IS_END).sum())), random_state=0)
    te = known[known["date"] >= IS_END]
    te = te.sample(min(n_eval, len(te)), random_state=0)
    Xtr, ytr = _xy(tr, label, features)
    Xte, yte = _xy(te, label, features)
    m = _super_model().fit(Xtr, ytr)
    pi = permutation_importance(m, Xte, yte, scoring="roc_auc", n_repeats=3, random_state=0)
    return pd.DataFrame({"feature": features, "auc_drop": pi.importances_mean}).sort_values("auc_drop", ascending=False)


# ------------------------------------------------------------------ run 17: bracket menu + regime
# Hit rate is mostly a property of the bracket (a far target and a near stop must hit less
# often), so compare brackets on what they earn: net return per trade and per month held.
# The bracket is chosen on the walk-forward years before 2018 and judged on 2018+.
def _top(o: pd.DataFrame, col: str, q: float) -> pd.DataFrame:
    """Rows whose score is in the top (1-q) of their calendar year (same cut as top_decile_trades)."""
    if q <= 0:
        return o
    return o[o[col] >= o.groupby(o["date"].dt.year)[col].transform(lambda p: p.quantile(q))]


def bracket_menu(sample: pd.DataFrame, col: str, menu: dict, tiers=(("all stocks", 0.0), ("top 10%", 0.9), ("top 2%", 0.98))) -> pd.DataFrame:
    rows = []
    base = sample[sample[col].notna()]
    for period, m in (("IS", base["date"] < IS_END), ("OOS", base["date"] >= IS_END)):
        o = base[m]
        for tier, q in tiers:
            g = _top(o, col, q)
            for key, (up, dn) in menu.items():
                r = g[f"{key}_ret"].dropna().astype(float)
                if r.empty:
                    continue
                days = g.loc[r.index, f"{key}_days"].astype(float)
                rows.append({"period": period, "tier": tier, "bracket": f"+{up:.0%} / -{dn:.0%}", "key": key,
                             "n": len(r), "hit_target": (r >= up - 0.0021).mean(), "hit_stop": (r <= -dn - 0.0019).mean(),
                             "avg_net_return": r.mean(), "avg_days": days.mean(),
                             "return_per_month": r.mean() / max(days.mean(), 1) * 21,
                             "breakeven_hit": dn / (up + dn)})
    return pd.DataFrame(rows)


def menu_trades(sample: pd.DataFrame, key: str, stop: float, col: str, calendar: pd.DatetimeIndex, q: float = 0.9) -> pd.DataFrame:
    """Top-decile model entries exited with bracket `key`; exit date from days held on `calendar`."""
    o = _top(sample[sample[col].notna() & sample[f"{key}_ret"].notna()], col, q)
    pos = np.searchsorted(calendar.values, o["date"].values) + o[f"{key}_days"].to_numpy(int)
    exit_date = calendar[np.minimum(pos, len(calendar) - 1)]
    return pd.DataFrame({"date": o["date"].values, "ticker": o["ticker"].values, "entry": o["close"].values,
                         "risk_pct": stop, "exit_bracket": exit_date, "ret_bracket": o[f"{key}_ret"].astype(float).values,
                         "priority": o[col].values, "rs_rank": o["rs_rank"].values,
                         "adr_pct": o["adr_pct"].values if "adr_pct" in o else np.nan})


ADR_BINS = [-np.inf, 0.03, 0.05, 0.08, 0.12, 0.15, np.inf]
ADR_LABELS = ["< 3%", "3-5%", "5-8%", "8-12%", "12-15%", "> 15%"]


def regime_splits(d: pd.DataFrame, ref: pd.DataFrame) -> dict[str, pd.Series]:
    """Market-state buckets known at the close of the entry day. Breadth terciles use in-sample
    cut-offs from `ref` so nothing is fitted on 2018+."""
    b1, b2 = ref["breadth_50"].quantile([1 / 3, 2 / 3]) if "breadth_50" in ref else (np.nan, np.nan)
    out = {}
    if "breadth_50" in d:
        out["breadth (stocks above 50d)"] = pd.cut(d["breadth_50"], [-np.inf, b1, b2, np.inf],
                                                    labels=[f"low (< {b1:.0%})", "mid", f"high (> {b2:.0%})"])
    if "vix" in d:
        out["VIX level"] = pd.cut(d["vix"], [0, 15, 20, 30, np.inf], labels=["< 15", "15-20", "20-30", "> 30"])
    if "vix_term" in d:
        out["VIX / VIX3M"] = pd.cut(d["vix_term"], [0, 0.9, 1.0, np.inf], labels=["< 0.9 (calm)", "0.9-1.0", "> 1.0 (stress)"])
    if "mkt_above200" in d:
        out["SPY above 200d"] = d["mkt_above200"].map({1.0: "yes", 0.0: "no"})
    if "qqq_trend" in d:
        out["QQQ above 10 & 20 SMA"] = d["qqq_trend"].map({1.0: "yes", 0.0: "no"})
    if "mkt_ret_21" in d:
        out["SPY 1-month return"] = pd.cut(d["mkt_ret_21"], [-np.inf, -0.03, 0.0, 0.03, np.inf],
                                           labels=["< -3%", "-3..0%", "0..3%", "> 3%"])
    # run 21 (user): short market trend, breadth, A/D line, and sector / sub-industry momentum
    code = {3.0: "above 21 & 50", 2.0: "above 21 only", 1.0: "above 50 only", 0.0: "below both"}
    for col, name in (("spy_2150", "SPY vs 21/50 SMA"), ("qqq_2150", "QQQ vs 21/50 SMA"), ("ad_2150", "A/D line vs its 21/50 MA")):
        if col in d:
            out[name] = d[col].map(code)
    if "breadth_20" in d:
        out["% of stocks above 20d"] = pd.cut(d["breadth_20"], [-np.inf, 0.4, 0.6, np.inf], labels=["< 40%", "40-60%", "> 60%"])
    if "breadth_50_chg10" in d:
        out["% above 50d, 10-day change"] = pd.cut(d["breadth_50_chg10"], [-np.inf, -0.05, 0.05, np.inf],
                                                   labels=["falling (< -5 pts)", "flat", "rising (> +5 pts)"])
    if "ad_chg10" in d:
        out["A/D line, 10-day change"] = pd.cut(d["ad_chg10"], [-np.inf, -0.5, 0.5, np.inf],
                                                labels=["falling", "flat", "rising"])
    for f, name in (("ret1", "today green"), ("ret5", "up over 5 days"), ("up21", "above 21 EMA")):
        a, b = f"sec_{f}", f"ind_{f}"
        if a in d and b in d:
            x, y = (d[a] > 0.5) if f == "up21" else (d[a] > 0), (d[b] > 0.5) if f == "up21" else (d[b] > 0)
            lab = np.select([x & y, x | y], ["both", "one of the two"], "neither")
            out[f"sector & sub-industry {name}"] = pd.Series(lab, index=d.index).where(d[a].notna() & d[b].notna())
    # run 24 (course): don't chase more than ~10% above the 21 EMA
    if "dist_ema21" in d:
        out["distance above the 21 EMA"] = pd.cut(d["dist_ema21"], [-np.inf, 0, 0.05, 0.10, 0.15, np.inf],
                                                  labels=["below", "0-5%", "5-10%", "10-15%", "> 15%"])
    # run 23 (user's ADR% infographic): minimum 5%, sweet spot 5-12%, > 15% often fails, needs $10M+/day
    if "adr_pct" in d:
        out["ADR%"] = pd.cut(d["adr_pct"], ADR_BINS, labels=ADR_LABELS)
        if "dollar_vol_50" in d:
            out["ADR% (only stocks trading >= $10M/day)"] = out["ADR%"].where(d["dollar_vol_50"] >= 10e6)
    # run 22 (user): early fundamental inflection (SEC filings, point-in-time) and the price rules
    if "inflection" in d:
        out["fundamental inflection (all 4)"] = d["inflection"].map({1.0: "yes", 0.0: "no"})
    if "rev_accel_q" in d:
        out["revenue growth accelerating"] = pd.cut(d["rev_accel_q"], [-np.inf, 0.5, 1.5, np.inf],
                                                    labels=["no (decelerating)", "1 quarter", "2+ quarters"])
    if "op_lev" in d:
        lev = (d["op_lev"] > 0) | (d.get("op_turn_pos", pd.Series(0, index=d.index)) == 1)
        out["operating income outgrowing revenue"] = pd.Series(np.where(lev, "yes", "no"), index=d.index).where(
            d["op_lev"].notna() | d.get("op_turn_pos", pd.Series(np.nan, index=d.index)).notna())
    if "op_margin_chg" in d:
        out["operating margin vs a year ago"] = pd.Series(np.where(d["op_margin_chg"] > 0, "expanding", "shrinking"),
                                                          index=d.index).where(d["op_margin_chg"].notna())
    if "fcf_margin_chg" in d:
        out["FCF margin vs a year ago"] = pd.Series(np.where(d["fcf_margin_chg"] > 0, "improving", "worse"),
                                                    index=d.index).where(d["fcf_margin_chg"].notna())
    if "updown_vol_50" in d:
        out["up/down volume, 50 days"] = pd.cut(d["updown_vol_50"], [-np.inf, 0.8, 1.0, 1.3, np.inf],
                                                labels=["< 0.8 (distribution)", "0.8-1.0", "1.0-1.3", "> 1.3 (accumulation)"])
    if "ext_200" in d:
        out["price vs 200-day"] = pd.cut(d["ext_200"], [-np.inf, 0, 0.1, 0.3, 0.5, np.inf],
                                         labels=["below", "0-10% above", "10-30% above", "30-50% above", "> 50% above"])
    if "ret_126" in d:
        out["6-month gain"] = pd.cut(d["ret_126"], [-np.inf, 0, 0.2, 0.5, 1.0, np.inf],
                                     labels=["< 0", "0-20%", "20-50%", "50-100%", "> 100%"])
    # run 19: stock-level group strength (median RS rank of the group, percentile among groups)
    if "sector_rank" in d:
        out["sector (11 GICS, by median RS)"] = pd.cut(d["sector_rank"], [-np.inf, 0.30, 0.75, np.inf],
                                                        labels=["bottom 3", "middle 5", "top 3 (leading)"])
    if "industry_rank" in d:
        out["sub-industry (by median RS)"] = pd.cut(d["industry_rank"], [-np.inf, 0.3, 0.7, np.inf],
                                                     labels=["bottom 30%", "middle", "top 30% (leading)"])
    if "m_up3" in d:
        cut = ref["m_up3"].quantile(0.1) if "m_up3" in ref and ref["m_up3"].notna().any() else np.nan
        if cut == cut:
            out["3-day market model"] = np.where(d["m_up3"].isna(), None,
                                                 np.where(d["m_up3"] <= cut, "bottom 10% (skip?)", "rest"))
            out["3-day market model"] = pd.Series(out["3-day market model"], index=d.index)
    return out


def regime_report(sample: pd.DataFrame, col: str, key: str = "b20", q: float = 0.9, keep=None) -> pd.DataFrame:
    """For the model's top 10% (+20/-10 by default): hit rate and net return by market regime,
    in-sample and out-of-sample side by side. `keep(df)` restricts rows after the top-10% cut
    (e.g. point-in-time S&P 500 members)."""
    o = _top(sample[sample[col].notna() & sample[f"{key}_ret"].notna()], col, q)
    if keep is not None:
        o = o[keep(o).to_numpy()]
    ref = sample[sample["date"] < IS_END]
    hit = f"{key}_hit" if f"{key}_hit" in o else None
    rows = []
    for name, grp in regime_splits(o, ref).items():
        for period, pm in (("IS", o["date"] < IS_END), ("OOS", o["date"] >= IS_END)):
            g = o[pm]
            for lvl, x in g.groupby(grp[pm.to_numpy()].to_numpy(), observed=True):
                rows.append({"regime": name, "bucket": lvl, "period": period, "n": len(x),
                             "hit_target": x[hit].mean() if hit else np.nan, "avg_net_return": x[f"{key}_ret"].mean()})
    if not rows:
        return pd.DataFrame()
    t = pd.DataFrame(rows).pivot_table(index=["regime", "bucket"], columns="period",
                                       values=["n", "hit_target", "avg_net_return"], sort=False)
    t.columns = [f"{p}_{m}" for m, p in t.columns]
    return t[[c for c in ("IS_n", "IS_hit_target", "IS_avg_net_return", "OOS_n", "OOS_hit_target", "OOS_avg_net_return") if c in t]]


def regime_gate(sample: pd.DataFrame, col: str, table: pd.DataFrame, key: str = "b20", q: float = 0.9,
                min_n: int = 200, breakeven: float = 1 / 3):
    """Model top 10% minus the regime buckets that were below break-even IN-SAMPLE (hit rate under
    `breakeven` or a negative average return, n >= min_n). Returns the kept rows and the skipped
    buckets; nothing about the rule is fitted on 2018+."""
    o = _top(sample[sample[col].notna() & sample[f"{key}_ret"].notna()], col, q)
    bad = ([(r, b) for (r, b), x in table.iterrows()
           if x.get("IS_n", 0) >= min_n and (x.get("IS_avg_net_return", 0) < 0 or x.get("IS_hit_target", 1) < breakeven)]
           if len(table) else [])
    splits = regime_splits(o, sample[sample["date"] < IS_END])
    skip = np.zeros(len(o), dtype=bool)
    for r, b in bad:
        skip |= (pd.Series(splits[r], index=o.index).astype(object) == b).to_numpy()
    return o[~skip], bad


# ------------------------------------------------------------------ run 23: is the model just volatility?
def vol_matched(sample: pd.DataFrame, col: str, key: str = "b20", q: float = 0.9, keep=None) -> pd.DataFrame:
    """The model's top 10% vs what stocks with the SAME volatility and momentum did: every row is put
    in a cell (calendar year x ADR decile x 6-month-return quintile, cut-offs per year); a pick's
    'expected' result is the average of all rows in its cell. If the model's edge is only that it
    picks volatile, strong stocks, actual minus expected is ~0."""
    d = sample[sample[col].notna() & sample[f"{key}_ret"].notna() & sample["adr_pct"].notna() & sample["ret_126"].notna()].copy()
    yr = d["date"].dt.year
    d["_adr_q"] = d.groupby(yr)["adr_pct"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    d["_mom_q"] = d.groupby(yr)["ret_126"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    cell = [yr, d["_adr_q"], d["_mom_q"]]
    d["_exp_hit"] = d.groupby(cell)[f"{key}_hit"].transform("mean")
    d["_exp_ret"] = d.groupby(cell)[f"{key}_ret"].transform("mean")
    top = _top(d, col, q)
    if keep is not None:
        top = top[keep(top).to_numpy()]
    rows = []
    for period, m in (("IS", top["date"] < IS_END), ("OOS", top["date"] >= IS_END)):
        g = top[m]
        rows.append({"period": period, "n": len(g), "hit": g[f"{key}_hit"].mean(), "matched_hit": g["_exp_hit"].mean(),
                     "ret": g[f"{key}_ret"].mean(), "matched_ret": g["_exp_ret"].mean()})
    t = pd.DataFrame(rows)
    t["edge_hit"], t["edge_ret"] = t["hit"] - t["matched_hit"], t["ret"] - t["matched_ret"]
    return t


def setups_by_adr(sig: pd.DataFrame, exit_name: str = "sma50_close", min_dollar_vol: float = 10e6) -> pd.DataFrame:
    """Per-trade R of setup groups by ADR% bucket (stocks trading >= $10M/day), IS and OOS."""
    groups = {"episodic pivots (ep_*)": sig["entry_name"].str.startswith("ep_"),
              "breakouts (qull / rocket / base / flag)": sig["entry_name"].str.contains("qull_breakout|wf_rocket|base_|flag_|htf"),
              "all setups": sig["entry_name"] != BASELINE, "random entries": sig["entry_name"] == BASELINE}
    s = sig[(sig["dollar_vol_50"] >= min_dollar_vol) & sig["adr_pct"].notna()]
    b = pd.cut(s["adr_pct"], ADR_BINS, labels=ADR_LABELS)
    rows = []
    for name, m in groups.items():
        m = m.reindex(s.index).fillna(False).to_numpy()
        for period, pm in (("IS", s["date"] < IS_END), ("OOS", s["date"] >= IS_END)):
            g = s[m & pm.to_numpy()]
            for lvl, x in g.groupby(b[m & pm.to_numpy()].to_numpy(), observed=True):
                rows.append({"setups": name, "ADR%": lvl, "period": period, "n": len(x),
                             "avgR": x[f"R_{exit_name}"].mean(), "win": (x[f"R_{exit_name}"] > 0).mean()})
    if not rows:
        return pd.DataFrame()
    t = pd.DataFrame(rows).pivot_table(index=["setups", "ADR%"], columns="period", values=["n", "avgR", "win"], sort=False)
    t.columns = [f"{p}_{v}" for v, p in t.columns]
    order = {k: i for i, k in enumerate(ADR_LABELS)}
    t = t.reset_index()
    t["_o"] = t["ADR%"].map(order)
    return t.sort_values(["setups", "_o"]).drop(columns="_o")[
        ["setups", "ADR%"] + [c for c in ("IS_n", "IS_avgR", "IS_win", "OOS_n", "OOS_avgR", "OOS_win") if c in t]]


# ------------------------------------------------------------------ run 24: course portfolio ideas
def _curve_stats(eq: pd.Series) -> dict:
    eq = eq.dropna()
    if len(eq) < 30:
        return {"CAGR": np.nan, "max_DD": np.nan}
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    return {"CAGR": (eq.iloc[-1] / eq.iloc[0]) ** (1 / yrs) - 1, "max_DD": (eq / eq.cummax() - 1).min()}


def split_stats(daily_ret: pd.Series, start="2007-01-01") -> dict:
    """CAGR / max drawdown before 2018 (IS) and from 2018 (OOS) for a daily return series."""
    r = daily_ret[daily_ret.index >= start].fillna(0.0)
    out = {}
    for name, m in (("IS", r.index < IS_END), ("OOS", r.index >= IS_END)):
        st = _curve_stats((1 + r[m]).cumprod())
        out[f"{name}_CAGR"], out[f"{name}_maxDD"] = st["CAGR"], st["max_DD"]
    return out


def momentum_portfolio(closes: pd.DataFrame, dollar_vol: pd.DataFrame, top: int = 10, vol_adj: bool = True,
                       members: pd.DataFrame | None = None, cost: float = 0.001, min_dv: float = 5e6) -> pd.Series:
    """Course lesson 9.8: score = 0.7 x 6-month return + 0.3 x 1-month return, each divided by the
    stock's volatility (126-day std of daily returns); hold the top N equally weighted, rebalanced at
    the close of each month's last trading day. Costs on traded weight. Returns daily portfolio returns."""
    rets = closes.pct_change(fill_method=None)
    vol = rets.rolling(126, min_periods=100).std() * np.sqrt(252)
    r126, r21 = closes / closes.shift(126) - 1, closes / closes.shift(21) - 1
    score = (0.7 * r126 + 0.3 * r21) / (vol if vol_adj else 1.0)
    ok = (closes >= 5) & (dollar_vol >= min_dv) & score.notna()
    if members is not None:
        ok &= members.reindex(index=closes.index, columns=closes.columns).fillna(False).astype(bool)
    month_end = closes.index.to_series().groupby(closes.index.to_period("M")).max()
    w = pd.DataFrame(0.0, index=closes.index, columns=closes.columns)
    prev = pd.Series(0.0, index=closes.columns)
    costs = pd.Series(0.0, index=closes.index)
    days = list(closes.index)
    pos = {d: i for i, d in enumerate(days)}
    ends = [d for d in month_end if pos[d] + 1 < len(days)]
    for k, d in enumerate(ends):
        sc = score.loc[d].where(ok.loc[d])
        pick = sc.nlargest(top).index
        new = pd.Series(0.0, index=closes.columns)
        if len(pick):
            new[pick] = 1.0 / len(pick)
        nxt = ends[k + 1] if k + 1 < len(ends) else days[-1]
        a, b = pos[d] + 1, pos[nxt] + 1
        w.iloc[a:b] = new.to_numpy()
        costs.iloc[a] = cost * (new - prev).abs().sum()
        prev = new
    return (w * rets.fillna(0.0)).sum(axis=1) - costs


def breadth_timing(spy_close: pd.Series, breadth: pd.Series, buy_below: float = 0.2, sell_above: float = 0.6,
                   irx: pd.Series | None = None) -> pd.Series:
    """Course lesson 2.2: buy the index when < 20% of stocks are above their 20-day average (washed out),
    sell when > 60% are (stretched); in T-bills (or cash) otherwise. Decided at the close, held from the next day."""
    b = breadth.reindex(spy_close.index).ffill()
    state, s = np.zeros(len(b)), 0
    for i, x in enumerate(b.to_numpy()):
        if x == x:
            s = 1 if x < buy_below else (0 if x > sell_above else s)
        state[i] = s
    held = pd.Series(state, index=spy_close.index).shift(1).fillna(0)
    cash = (irx.reindex(spy_close.index).ffill() / 100 / 252).fillna(0) if irx is not None else 0.0
    return held * spy_close.pct_change().fillna(0) + (1 - held) * cash


def vol_matched_years(sample: pd.DataFrame, col: str, key: str = "b20", q: float = 0.9, keep=None) -> pd.DataFrame:
    """Run 24: the volatility-matched edge year by year (is it consistent or one or two lucky years?)."""
    d = sample[sample[col].notna() & sample[f"{key}_ret"].notna() & sample["adr_pct"].notna() & sample["ret_126"].notna()].copy()
    yr = d["date"].dt.year
    d["_a"] = d.groupby(yr)["adr_pct"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    d["_m"] = d.groupby(yr)["ret_126"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    d["_eh"] = d.groupby([yr, d["_a"], d["_m"]])[f"{key}_hit"].transform("mean")
    d["_er"] = d.groupby([yr, d["_a"], d["_m"]])[f"{key}_ret"].transform("mean")
    top = _top(d, col, q)
    if keep is not None:
        top = top[keep(top).to_numpy()]
    g = top.groupby(top["date"].dt.year)
    return pd.DataFrame({"n": g.size(), "hit": g[f"{key}_hit"].mean(), "matched_hit": g["_eh"].mean(),
                         "edge_hit": g[f"{key}_hit"].mean() - g["_eh"].mean(),
                         "edge_ret": g[f"{key}_ret"].mean() - g["_er"].mean()})


def alpha_beta(curve: pd.Series, spy_close: pd.Series) -> dict:
    """Run 24: market-adjusted performance of a daily equity curve vs SPY: beta, annual alpha (and its
    t-stat), Sharpe of both, return / max drawdown, worst month."""
    r = curve.pct_change().dropna()
    m = spy_close.pct_change().reindex(r.index).fillna(0)
    if len(r) < 60:
        return {}
    X = np.c_[np.ones(len(m)), m.to_numpy()]
    coef, *_ = np.linalg.lstsq(X, r.to_numpy(), rcond=None)
    resid = r.to_numpy() - X @ coef
    se = np.sqrt(resid.var(ddof=2) * np.linalg.inv(X.T @ X)[0, 0])
    st = _curve_stats(curve)
    monthly = (1 + r).groupby(r.index.to_period("M")).prod() - 1
    sh = lambda x: x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else np.nan
    return {"beta": coef[1], "alpha_annual": coef[0] * 252, "alpha_t": coef[0] / se if se > 0 else np.nan,
            "sharpe": sh(r), "spy_sharpe": sh(m), "CAGR": st["CAGR"], "max_DD": st["max_DD"],
            "CAGR_per_DD": st["CAGR"] / abs(st["max_DD"]) if st["max_DD"] else np.nan, "worst_month": monthly.min()}


# ------------------------------------------------------------------ run 24: replay of the daily picks tool
def replay_picks(sample: pd.DataFrame, start="2023-01-01", features=None, retrain_days: int = 91,
                 top: int = 10, key: str = "b20") -> pd.DataFrame:
    """Replays picks.py's rule on past dates: train the goal model only on rows whose label window had
    closed (retrained every `retrain_days`), score every liquid stock on the replay date, take the top 10
    overall and the top 10 'leaders' (RS >= 0.7, within 25% of the 52w high, above the 50-day), and score
    their real +20/-10 outcomes. One row per pick."""
    d = sample[sample[f"{key}_ret"].notna()]
    dates = sorted(d.loc[d["date"] >= start, "date"].unique())
    rows, model, trained_at = [], None, None
    for day in dates:
        day = pd.Timestamp(day)
        if model is None or (day - trained_at).days >= retrain_days:
            tr = sample[(sample["label_end"] < day) & sample["fwd_max_gain"].notna()]
            tr = tr.sample(min(300_000, len(tr)), random_state=0)
            model = _super_model().fit(*_xy(tr, key, features))
            trained_at = day
        x = d[(d["date"] == day) & (d["close"] >= 5) & (d["dollar_vol_50"] >= 5e6)]
        if len(x) < 100:
            continue
        x = x.assign(_score=model.predict_proba(_xy(x, features=features)[0])[:, 1])
        leader = (x["rs_rank"] >= 0.70) & (x["dist_52w_high"] >= -0.25) & (x["dist_sma50"] > 0)
        for name, g in (("all", x), ("leaders", x[leader])):
            p = g.nlargest(top, "_score")
            rows.append(p[["date", "ticker", f"{key}_hit", f"{key}_ret", "_score"]].assign(list=name))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def replay_summary(rep: pd.DataFrame, key: str = "b20") -> pd.DataFrame:
    if rep.empty:
        return pd.DataFrame()
    g = rep.groupby("list")
    return pd.DataFrame({"dates": g["date"].nunique(), "picks": g.size(), "hit": g[f"{key}_hit"].mean(),
                         "avg_ret": g[f"{key}_ret"].mean(), "median_ret": g[f"{key}_ret"].median(),
                         "share_dates_hit_ge_33%": g.apply(lambda x: (x.groupby("date")[f"{key}_hit"].mean() >= 1 / 3).mean())})
