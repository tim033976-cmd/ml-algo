"""Real-data strategy research: S&P 1500 (+ former S&P 500 members), ~20 published breakout
entries x 9 exit plans x 6 filters, selected on 2006-2017 and judged on 2018-today.

    python research.py                      # full run (downloads ~1,600 tickers from Yahoo)
    python research.py --limit 200          # quicker run on the first 200 tickers
    python research.py --signals data/signals.parquet   # re-analyze without recomputing
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo.research import analyze as A
from mlalgo.research import data as D
from mlalgo.research import engine
from mlalgo.research.entries import ENTRIES
from mlalgo.research.insights import append_history, findings
from mlalgo.research.run import EXIT_NAMES, run


def md(df: pd.DataFrame, floatfmt=".2f", index=False) -> str:
    return df.to_markdown(index=index, floatfmt=floatfmt)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cache", default="data")
    p.add_argument("--out", default="results")
    p.add_argument("--start", default="2005-01-01")
    p.add_argument("--indexes", default="sp500,sp400,sp600")
    p.add_argument("--limit", type=int, default=0, help="only use the first N tickers (quick runs)")
    p.add_argument("--workers", type=int, default=0)
    p.add_argument("--signals", help="reuse a saved signals.parquet")
    p.add_argument("--prices-parquet", help="use this long-format price file instead of downloading")
    p.add_argument("--universe-csv", help="with --prices-parquet: universe file with sector / sub_industry")
    p.add_argument("--download-only", action="store_true", help="fetch and cache prices, then stop")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    Path(a.cache).mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if a.prices_parquet:
        prices = D.from_long(pd.read_parquet(a.prices_parquet))
        market = {k: prices.pop(k) for k in ("SPY", "QQQ", "^IRX") if k in prices}
        universe = (pd.read_csv(a.universe_csv) if a.universe_csv else
                    pd.DataFrame({"ticker": list(prices), "index": "file", "status": "current"}))
    else:
        universe, prices, market = D.load_all(a.cache, a.start, tuple(a.indexes.split(",")))
    if a.download_only:
        print(f"[research] cached {len(prices)} tickers + {list(market)}")
        return
    if a.limit:
        prices = dict(list(prices.items())[: a.limit])
    print(f"[research] {len(prices)} tickers, market: {list(market)}  ({time.time() - t0:.0f}s)")

    if a.signals and Path(a.signals).exists():
        sig = pd.read_parquet(a.signals)
    else:
        sig = run(prices, market, workers=a.workers or None, universe=universe)
        sig.to_parquet(Path(a.cache) / "signals.parquet", index=False)
    print(f"[research] {len(sig):,} signals ({time.time() - t0:.0f}s)")

    # ---------------- strategy grid
    lb = A.leaderboard(sig)
    lb.to_csv(out / "leaderboard.csv", index=False)
    sel = A.selection_check(lb)
    ent = A.entry_summary(lb)
    exs = A.exit_summary(lb)
    vsb = A.vs_baseline(lb)
    vsb_is = A.vs_baseline(lb, period="IS")
    ent.to_csv(out / "entry_summary.csv", index=False)
    exs.to_csv(out / "exit_summary.csv")
    vsb.to_csv(out / "vs_baseline_oos.csv")
    filt = (lb[(lb["entry"] != A.BASELINE) & (lb["IS_n"] >= 50) & (lb["OOS_n"] >= 30)]
            .groupby("filter")[["IS_avgR", "OOS_avgR", "OOS_win"]].mean().sort_values("OOS_avgR", ascending=False))
    robust = lb[(lb["IS_t"] >= 3) & (lb["OOS_t"] >= 2) & (lb["entry"] != A.BASELINE)]
    print(f"[research] grid done ({time.time() - t0:.0f}s)")

    # ---------------- ML (reference exit chosen on in-sample data only)
    ref_exit = exs["IS_avgR"].idxmax()
    d, cols = A.ml_walk_forward(sig, ref_exit)
    mlr = A.ml_report(d, ref_exit)
    ml_alt = {}
    ep = sig[sig["entry_name"].str.startswith("ep_") | (sig["entry_name"] == A.BASELINE)]
    try:
        d_ep, _ = A.ml_walk_forward(ep, "sma50_close", min_train=1000)
        ml_alt["episodic pivots only / sma50_close"] = A.ml_report(d_ep, "sma50_close")
    except Exception as e:
        print(f"[research] EP-only ML skipped: {e}")
    if ref_exit != "trim_ema":  # also score the user's own exit plan
        d2, _ = A.ml_walk_forward(sig, "trim_ema")
        ml_alt["your trim plan (trim_ema)"] = A.ml_report(d2, "trim_ema")
    imp = A.ml_importance(d, cols, ref_exit)
    rules = A.rule_tree(d, cols, ref_exit)
    mlr["deciles"].to_csv(out / "ml_deciles.csv")
    mlr["per_entry"].to_csv(out / "ml_per_entry.csv")
    imp.to_csv(out / "ml_importance.csv", index=False)
    rules.to_csv(out / "ml_rules.csv", index=False)
    print(f"[research] ML done ({time.time() - t0:.0f}s)")

    # ---------------- portfolio simulation, 2018 -> today (marked to market daily)
    closes = pd.DataFrame({t: df["close"] for t, df in prices.items()}).astype("float32").ffill()
    port_rows, curves = [], {}
    cands = lb[(lb["IS_n"] >= 100) & (lb["entry"] != A.BASELINE)].drop_duplicates("entry").head(5)
    for r in cands.itertuples():
        s = sig[(sig["entry_name"] == r.entry)]
        s = s[A.FILTERS[r.filter](s)]
        port_rows.append((f"{r.entry} / {r.filter} / {r.exit}", A.portfolio(s, r.exit, "rs_rank", closes=closes)))
    pooled = d[d["prob"].notna()].copy()
    pooled["random_priority"] = np.random.default_rng(0).random(len(pooled))
    early = pooled[A.FILTERS["rs80_early"](pooled)]
    base = sig[sig["entry_name"] == A.BASELINE].copy()
    base["random_priority"] = np.random.default_rng(1).random(len(base))
    # which way of choosing among many same-day signals works? (run-1 lesson: ranking mattered)
    P = lambda df, ex, pr: A.portfolio(df, ex, pr, closes=closes)
    port_rows += [
        (f"All setups, ML-filtered (top third), ranked by ML / {ref_exit}", P(pooled[pooled["take"]], ref_exit, "prob")),
        (f"All setups, ranked by RS / {ref_exit}", P(pooled, ref_exit, "rs_rank")),
        (f"All setups, random order / {ref_exit}", P(pooled, ref_exit, "random_priority")),
        (f"All setups + rs80_early filter, ranked by RS / {ref_exit}", P(early, ref_exit, "rs_rank")),
        (f"BASELINE random entries, ranked by RS / {ref_exit}", P(base, ref_exit, "rs_rank")),
        (f"BASELINE random entries, random order / {ref_exit}", P(base, ref_exit, "random_priority")),
    ]
    # setups chosen on IN-SAMPLE data only: beat random entries by >= 0.05R before 2018
    is_n = lb[lb["filter"] == "all"].groupby("entry")["IS_n"].max()
    for ex in dict.fromkeys([ref_exit, "sma50_close"]):
        chosen = [e for e in vsb_is.index[vsb_is[ex] >= 0.05] if is_n.get(e, 0) >= 100]
        pool = pooled[pooled["entry_name"].isin(chosen)]
        if len(pool):
            port_rows.append((f"IS-selected setups ({len(chosen)}), ranked by RS / {ex}", P(pool, ex, "rs_rank")))
            port_rows.append((f"IS-selected setups, only when SPY > 200d / {ex}",
                              P(pool[pool["mkt_above200"] == 1], ex, "rs_rank")))
    port_rows.append(("All setups, ranked by RS / sma50_close", P(pooled, "sma50_close", "rs_rank")))
    # run-4 lesson: ranking by in-sample EXPECTANCY (min 200 trades) selected strategies that held up
    # out-of-sample (+0.34R avg) but they were never traded as a portfolio. Each keeps its own exit.
    ranked = lb[(lb["IS_n"] >= 200) & (lb["entry"] != A.BASELINE)].sort_values("IS_avgR", ascending=False)
    for k in (5, 10, 20):
        picks = ranked.head(k)
        pool = A.strategy_pool(sig, picks)
        port_rows.append((f"Top {k} strategies by IS expectancy (own exits), ranked by RS",
                          P(pool, "per_row", "rs_rank")))
    top10_picks = ranked.head(10)[["entry", "filter", "exit", "IS_n", "IS_avgR", "OOS_n", "OOS_avgR", "OOS_t"]]
    spy = A.spy_stats(market["SPY"]) if "SPY" in market else {"CAGR": np.nan, "max_DD": np.nan}
    port = pd.DataFrame([{"strategy": k, **{m: v for m, v in res.items() if m != "curve"}} for k, res in port_rows])
    port.loc[len(port)] = {"strategy": "SPY buy & hold", "CAGR": spy["CAGR"], "max_DD": spy["max_DD"]}
    port.to_csv(out / "portfolio.csv", index=False)
    # year-by-year for the best few portfolios vs SPY
    best_names = port[~port["strategy"].str.startswith(("SPY", "BASELINE"))].nlargest(3, "CAGR")["strategy"].tolist()
    curves_d = dict(port_rows)
    yr = pd.DataFrame({k: A.yearly(curves_d[k]["curve"]) for k in best_names})
    if "SPY" in market:
        spy_c = market["SPY"]["close"]
        yr["SPY"] = A.yearly(spy_c[spy_c.index >= A.IS_END])
    yr.to_csv(out / "portfolio_yearly.csv")
    pd.DataFrame({k: res["curve"] for k, res in port_rows}).ffill().to_csv(out / "equity_curves.csv")

    # ---------------- what this run tells us
    found, nxt, key = findings(lb, sel, vsb, vsb_is, exs, filt, mlr, imp, rules, port)
    hist = append_history(out / "history.csv", key, len(prices), len(sig))
    (out / "insights.json").write_text(json.dumps({"findings": found, "next_steps": nxt, "key": key}, indent=2, default=str))

    # ---------------- report
    first, last = sig["date"].min().date(), sig["date"].max().date()
    counts = sig.groupby("entry_name").size().rename("signals")
    lines = [
        "# Strategy research report",
        "",
        f"Generated {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC in {(time.time() - t0) / 60:.0f} min.",
        f"Universe: {len(prices)} stocks with data ({', '.join(f'{k}: {v}' for k, v in universe['index'].value_counts().items())}; "
        f"{int((universe['status'] == 'removed').sum())} former S&P 500 members). Signals {first} -> {last}: {len(sig):,}.",
        f"**In-sample (selection): trades closed before IS_END_STR. Out-of-sample (judgement): entries from IS_END_STR.**",
        "R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.",
        "",
        "## What this run tells us",
        "",
        *[f"- {x}" for x in found],
        "",
        "**Next steps for the strategy:**",
        "",
        *[f"{i + 1}. {x}" for i, x in enumerate(nxt)],
        "",
        "**Run history** (each run should move these numbers):",
        "",
        md(hist.tail(10)),
        "",
        "## 1. Did picking the best in-sample strategies work out-of-sample?",
        "",
        md(pd.Series(sel).rename("value").to_frame(), floatfmt=".3f", index=True),
        "",
        "If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the "
        "average and the random baseline out-of-sample, the selection carries real information.",
        "",
        "## 2. Robust strategies (IS t >= 3 and OOS t >= 2)",
        "",
        md(robust[["entry", "filter", "exit", "IS_n", "IS_avgR", "IS_t", "OOS_n", "OOS_per_yr", "OOS_win", "OOS_avgR", "OOS_pf", "OOS_t", "OOS_R_per_yr"]].head(30))
        if len(robust) else "_None._",
        "",
        "## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results",
        "",
        md(lb[lb["IS_n"] >= 50][["entry", "filter", "exit", "IS_n", "IS_avgR", "IS_t", "OOS_n", "OOS_win", "OOS_avgR", "OOS_pf", "OOS_t"]].head(30)),
        "",
        "## 4. Each entry with its best in-sample exit/filter",
        "",
        md(ent),
        "",
        "## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)",
        "",
        md(vsb.round(3), index=True),
        "",
        "Same, in-sample:",
        "",
        md(vsb_is.round(3), index=True),
        "",
        "## 6. Exit plans (averaged over all entries, no filter)",
        "",
        md(exs, index=True),
        "",
        "## 7. Filters (averaged over all entry x exit combinations)",
        "",
        md(filt, index=True),
        "",
        f"## 8. ML meta-labeling (exit: {ref_exit}, chosen in-sample; walk-forward, yearly retrain)",
        "",
        f"The model predicts R (clipped {A.R_CLIP}). Out-of-sample rank correlation with realized R: {mlr['rank_corr_oos']:.3f}; "
        f"AUC for R > 0: {mlr['auc_oos']:.3f} (0.5 = no skill). "
        f"Taken (model's top third, causal threshold): n={mlr['taken']['n']:,}, avgR={mlr['taken']['avgR']:.3f}, win={mlr['taken']['win']:.3f}. "
        f"Skipped: n={mlr['skipped']['n']:,}, avgR={mlr['skipped']['avgR']:.3f}, win={mlr['skipped']['win']:.3f}.",
        "",
        "Out-of-sample avgR by predicted-probability decile (0 = lowest):",
        "",
        md(mlr["deciles"], index=True),
        "",
        "Per entry (OOS):",
        "",
        md(mlr["per_entry"], index=True),
        "",
        *([f"- Same model on {k}: rank corr {v['rank_corr_oos']:.3f}, taken avgR {v['taken']['avgR']:.3f} "
           f"(n={v['taken']['n']:,}) vs skipped {v['skipped']['avgR']:.3f} (n={v['skipped']['n']:,})." for k, v in ml_alt.items()]),
        "",
        "What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):",
        "",
        md(imp.head(20), floatfmt=".4f"),
        "",
        "Readable rules (depth-3 tree fit in-sample, scored out-of-sample):",
        "",
        md(rules),
        "",
        "## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)",
        "",
        md(port.drop(columns=["final_equity"], errors="ignore")),
        "",
        "max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only "
        "counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.",
        "",
        "Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):",
        "",
        md(top10_picks),
        "",
        "Year-by-year returns (best 3 portfolios by CAGR vs SPY):",
        "",
        md((yr * 100).round(1), floatfmt=".1f", index=True),
        "",
        "## Appendix: entries and exits",
        "",
        md(pd.DataFrame([(k, v[3], counts.get(k, 0)) for k, v in ENTRIES.items()], columns=["entry", "source / rule", "signals"])),
        "",
        md(pd.DataFrame([(k, v[1]) for k, v in engine.EXITS.items()], columns=["exit", "rule"])),
        "",
        "Caveats: index membership lists are current (plus former S&P 500 members Yahoo still serves), so "
        "survivorship bias remains; daily bars cannot reproduce intraday entries; one decision per signal, no slippage model beyond costs.",
    ]
    (out / "report.md").write_text("\n".join(lines).replace("IS_END_STR", str(A.IS_END.date())))
    (out / "summary.json").write_text(json.dumps({k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                                                  for k, v in sel.items()}, indent=2))
    print(f"[research] wrote {out / 'report.md'} ({time.time() - t0:.0f}s)")


IS_END_STR = "IS_END_STR"

if __name__ == "__main__":
    main()
