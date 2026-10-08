"""Turn a research run into findings + concrete next steps, and keep a run-to-run history,
so every run feeds the next iteration of the strategy."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo.research.analyze import BASELINE


def findings(lb, sel, vsb, vsb_is, exs, filt, mlr, imp, rules, port) -> tuple[list[str], list[str], dict]:
    f, nxt, key = [], [], {}

    # 1. does in-sample selection carry information?
    rc = sel["rank_corr_IS_vs_OOS_avgR"]
    top, base, avg = sel["OOS_avgR_top20_by_IS"], sel["OOS_avgR_random_baseline"], sel["OOS_avgR_all_strategies"]
    works = rc > 0.2 and top > max(base, avg)
    f.append(f"Selection {'carries real information' if works else 'is mostly noise'}: IS-vs-OOS rank correlation "
             f"{rc:.2f}; the 20 best in-sample strategies averaged {top:+.3f}R out-of-sample vs {avg:+.3f}R for all "
             f"strategies and {base:+.3f}R for random entries.")
    if not works:
        nxt.append("In-sample rankings don't persist: test fewer, more different ideas instead of fine-tuning parameters.")
    key.update(rank_corr=rc, top20_oos=top, baseline_oos=base)

    # 2. which entries beat random entries in BOTH periods (with the same exits)?
    n_oos = lb[(lb["filter"] == "all")].groupby("entry")["OOS_n"].max()
    n_is = lb[(lb["filter"] == "all")].groupby("entry")["IS_n"].max()
    thin = [e for e in vsb.index if n_oos.get(e, 0) < 100 or n_is.get(e, 0) < 100]
    if thin:
        f.append("Too few signals to judge (need 100+ per period): " + ", ".join(f"{e} (IS {int(n_is.get(e, 0))}, OOS {int(n_oos.get(e, 0))})" for e in thin) + ".")
        nxt.append(f"Loosen the definitions of {', '.join(thin)} or widen the universe so they can be evaluated.")
    vsb, vsb_is = vsb.drop(index=thin), vsb_is.drop(index=thin)
    both = ((vsb > 0) & (vsb_is > 0)).mean(axis=1).sort_values(ascending=False)
    excess = vsb.mean(axis=1)
    edge = [e for e in both.index if both[e] >= 0.6 and excess[e] > 0]
    noedge = [e for e in both.index if both[e] <= 0.2]
    f.append("Entries that beat random entries in both periods for most exits: "
             + (", ".join(f"{e} ({excess[e]:+.2f}R OOS)" for e in edge) if edge else "none") + ".")
    if noedge:
        f.append("Entries with no edge over random entries: " + ", ".join(noedge) + ".")
        nxt.append(f"Drop or rework: {', '.join(noedge)}.")
    if edge:
        nxt.append(f"Focus development on: {', '.join(edge)} (tune them on IS data only, re-check OOS).")
    key.update(edge_entries=edge, no_edge_entries=noedge)

    # 3. exits
    best_exit = exs.index[0]
    f.append(f"Best exit out-of-sample (avg over entries): {best_exit} ({exs['OOS_avgR'].iloc[0]:+.3f}R); "
             f"worst: {exs.index[-1]} ({exs['OOS_avgR'].iloc[-1]:+.3f}R).")
    key["best_exit"] = best_exit

    # 4. filters vs no filter
    if "all" in filt.index:
        delta = (filt["OOS_avgR"] - filt.loc["all", "OOS_avgR"]).drop("all")
        good = delta[delta > 0.03]
        bad = delta[delta < -0.03]
        f.append("Filters that help OOS: " + (", ".join(f"{k} ({v:+.3f}R)" for k, v in good.items()) or "none")
                 + "; that hurt: " + (", ".join(f"{k} ({v:+.3f}R)" for k, v in bad.items()) or "none") + ".")
        if len(good):
            nxt.append(f"Make {good.index[0]} a default filter.")
        key["helpful_filters"] = list(good.index)

    # 5. ML
    auc = mlr["auc_oos"]
    dec = mlr["deciles"]["avgR"]
    mono = pd.Series(dec.values).corr(pd.Series(range(len(dec))), method="spearman")
    gap = mlr["taken"]["avgR"] - mlr["skipped"]["avgR"]
    useful = auc >= 0.53 and mono >= 0.6 and gap > 0.05
    f.append(f"ML filter {'adds value' if useful else 'adds little'}: OOS AUC {auc:.3f}, decile monotonicity {mono:.2f}, "
             f"taken {mlr['taken']['avgR']:+.3f}R vs skipped {mlr['skipped']['avgR']:+.3f}R.")
    top_feats = list(imp["feature"].head(5))
    f.append("Features the model relies on most: " + ", ".join(top_feats) + ".")
    nxt.append(f"Inspect {top_feats[0]} and {top_feats[1]}: plot avgR by bucket and consider a hard rule.")
    if not useful:
        nxt.append("ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).")
    key.update(ml_auc=auc, ml_monotonic=mono, ml_gap=gap, top_features=top_feats)

    # 6. rules that held up
    overall = rules["OOS_avgR"].mean()
    held = rules[(rules["IS_avgR"] > 0) & (rules["OOS_avgR"] > 0) & (rules["OOS_n"] >= 200)]
    if len(held):
        r = held.iloc[0]
        f.append(f"Best readable rule that held OOS: `{r['rule']}` (IS {r['IS_avgR']:+.2f}R, OOS {r['OOS_avgR']:+.2f}R, n={int(r['OOS_n'])}).")
        nxt.append("Turn that rule into a scan filter and test it as its own strategy.")
    key["rules_held"] = int(len(held))

    # 7. portfolio vs SPY
    strat = port[~port["strategy"].str.startswith(("SPY", "BASELINE"))]
    spy = port.loc[port["strategy"] == "SPY buy & hold", "CAGR"]
    if len(strat) and len(spy):
        b = strat.loc[strat["CAGR"].idxmax()]
        f.append(f"Best portfolio 2018->today: {b['strategy']} at {b['CAGR']:.1%} CAGR (max realized DD {b['max_DD_realized']:.1%}) "
                 f"vs SPY {spy.iloc[0]:.1%}.")
        key.update(best_portfolio=b["strategy"], best_cagr=b["CAGR"], spy_cagr=spy.iloc[0])
        if b["CAGR"] < spy.iloc[0]:
            nxt.append("No strategy beat buy-and-hold after constraints: improve trade selection before adding complexity.")
    return f, nxt, key


def append_history(path: Path, key: dict, n_tickers: int, n_signals: int) -> pd.DataFrame:
    row = {"run_utc": pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M"),
           "commit": os.environ.get("GITHUB_SHA", "local")[:7], "tickers": n_tickers, "signals": n_signals}
    row.update({k: (", ".join(v) if isinstance(v, list) else v) for k, v in key.items()})
    hist = pd.read_csv(path) if path.exists() else pd.DataFrame()
    hist = pd.concat([hist, pd.DataFrame([row])], ignore_index=True)
    hist.to_csv(path, index=False)
    return hist
