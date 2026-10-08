"""Evaluate every (entry x filter x exit) strategy in-sample vs out-of-sample, compare to a
random-entry baseline, train an ML meta-labeling model walk-forward, extract readable rules,
and simulate a capital-constrained portfolio for the best candidates."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeRegressor

from mlalgo.research.entries import ENTRIES
from mlalgo.research.run import EXIT_NAMES, GROUP_COLS, MARKET_COLS, SIGNAL_EXTRAS
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
    # "hot theme": the stock's sub-industry is in the top 30% of sub-industries by median RS
    "theme": lambda s: (s["industry_rank"] >= 0.7).to_numpy(),
    "rs80_theme": lambda s: ((s["rs_rank"] >= 0.8) & (s["industry_rank"] >= 0.7)).to_numpy(),
    "rs80_early_theme": lambda s: ((s["rs_rank"] >= 0.8) & s["base_count"].between(1, 2) & (s["industry_rank"] >= 0.7)).to_numpy(),
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
              risk=0.01, max_pos=10, pos_cap=0.20, closes: pd.DataFrame | None = None) -> dict:
    """Fixed-fractional sizing (1% equity at risk per trade), max 10 positions, no leverage.
    With `closes` (dates x tickers), open positions are marked to market every day, so the
    drawdown is honest; without it equity only moves when trades close (run 1-3 reports)."""
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
    open_pos: list[tuple] = []          # (exit_date, alloc, ret, ticker, entry_price)
    curve, taken = [], []
    for day in days:
        still = []
        for pos in open_pos:
            if pos[0] <= day:
                cash += pos[1] * (1 + pos[2])
                realized += pos[1] * pos[2]
                taken.append(pos[2])
            else:
                still.append(pos)
        open_pos = still
        g = by_day.get(day)
        if g is not None:
            held = {p[3] for p in open_pos}
            for r in g.itertuples(index=False):
                if len(open_pos) >= max_pos:
                    break
                if r.ticker in held or r.exit_date <= day:
                    continue
                alloc = min(realized * risk / max(r.risk_pct, 1e-4), realized * pos_cap, cash)
                if alloc < realized * 0.02:
                    continue
                cash -= alloc
                open_pos.append((r.exit_date, alloc, r.ret, r.ticker, r.entry))
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
