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
from mlalgo.research.run import EXIT_NAMES, MENU, run


def md(df: pd.DataFrame, floatfmt=".2f", index=False) -> str:
    return df.to_markdown(index=index, floatfmt=floatfmt)


def _menu_section(menu, menu_ports, menu_choice, regime, skipped, md):
    """Section 13 (run 17): which bracket, and which market regimes, for the goal model's top picks."""
    piv = lambda d, v: d.pivot_table(index="bracket", columns="period", values=v, sort=False)
    top = menu[menu["tier"] == "top 10%"]
    t = piv(top, "hit_target").add_prefix("hit_").join(piv(top, "avg_net_return").add_prefix("ret_")) \
        .join(piv(top, "return_per_month").add_prefix("per_month_")).join(piv(top, "avg_days").add_prefix("days_"))
    t.insert(0, "breakeven_hit", top.drop_duplicates("bracket").set_index("bracket")["breakeven_hit"])
    oos = menu[menu["period"] == "OOS"].pivot_table(index="bracket", columns="tier", values="hit_target", sort=False)
    oos_r = menu[menu["period"] == "OOS"].pivot_table(index="bracket", columns="tier", values="avg_net_return", sort=False)
    port = menu_ports.set_index("bracket").drop(columns="key") if menu_ports is not None and len(menu_ports) else None
    return [
        "## 13. Bracket menu and market regime for the +20/-10 model's picks (run 17)",
        "",
        "Every stock every 10 days, entry at the close, 63-day limit, 0.1% costs per side. Stocks ranked by the "
        "+20/-10 goal model (walk-forward, so pre-2018 scores are also out-of-sample for their year). Top 10% = top "
        "10% of scores within each year. Brackets are chosen on IS (walk-forward years before 2018) and judged on 2018+. "
        f"IS choice: best return per month = {menu_choice['return per month']}, best return per trade = "
        f"{menu_choice['return per trade']}.",
        "",
        "Model top 10%: hit rate, net return per trade, return per month held, days held (IS vs OOS):",
        "",
        md(t, index=True, floatfmt=".3f"),
        "",
        "OOS hit rate by tier (all stocks = no model):",
        "",
        md(oos, index=True, floatfmt=".3f"),
        "",
        "OOS net return per trade by tier:",
        "",
        md(oos_r, index=True, floatfmt=".4f"),
        "",
        *(["Portfolio 2018+ (top 10% model, 1% risk per trade = position size 1%/stop, max 10 positions, 20% cap):", "",
           md(port, index=True, floatfmt=".3f"), ""] if port is not None else []),
        "Model top 10%, +20/-10, by market regime at entry (breadth terciles and the 3-day market model cut use IS data):",
        "",
        md(regime.reset_index(), floatfmt=".3f"),
        "",
        f"Regime gate (section 9, REGIME row) skips buckets that were below break-even in-sample (hit < 33% or "
        f"negative return): {skipped or 'none'}.",
        "",
    ]


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
        market = {k: prices.pop(k) for k in ("SPY", "QQQ", "^IRX", "^VIX", "^VIX3M") if k in prices}
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

    sample_path = Path(a.cache) / "superperformer_sample.parquet"
    if a.signals and Path(a.signals).exists():
        sig = pd.read_parquet(a.signals)
        sample = pd.read_parquet(sample_path) if sample_path.exists() else pd.DataFrame()
    else:
        sig, sample = run(prices, market, workers=a.workers or None, universe=universe)
        sig.to_parquet(Path(a.cache) / "signals.parquet", index=False)
        if len(sample):
            sample.to_parquet(sample_path, index=False)
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

    # ---------------- superperformer model: learn what future big winners look like beforehand
    sup = sup_clean = None
    short, goal_ext, short_imp = {}, {}, None
    menu = regime = menu_choice = menu_ports = regime_skipped = None
    if len(sample):
        sample, (sig,) = A.super_walk_forward(sample, [sig])
        sup = A.super_report(sample)
        # run-11 lesson: +40% highs reward plain volatility; also model "+40% before -20%"
        if "clean_super" in sample:
            sample, (sig,) = A.super_walk_forward(sample, [sig], label="clean", col="clean_prob")
            sup_clean = A.super_report(sample, label="clean", col="clean_prob")
            sup_clean["deciles"].to_csv(out / "super_clean_deciles.csv")
        else:
            sup_clean = None
        sup_imp, sup_rules, sup_prof = A.super_explain(sample)
        sup_sig = A.signals_by_super(sig, ref_exit)
        sup["deciles"].to_csv(out / "super_deciles.csv")
        sup_imp.to_csv(out / "super_importance.csv", index=False)
        sup_rules.to_csv(out / "super_rules.csv", index=False)
        sup_prof.to_csv(out / "super_profile.csv")
        print(f"[research] superperformer model done ({time.time() - t0:.0f}s)")

        # ---------------- the user's goal: +10% / +20% before -10% on the daily chart
        pit = None
        if "date_added" in universe.columns:
            added = pd.to_datetime(universe.set_index("ticker")["date_added"], errors="coerce")
            sp500 = set(universe.loc[universe["index"] == "sp500", "ticker"])
            pit = lambda d: d["ticker"].isin(sp500) & (d["date"] >= d["ticker"].map(added))
        goal_tables = {}
        for g, (gname, breakeven) in A.GOALS.items():
            if f"{g}_hit" not in sample:
                continue
            sample, (sig,) = A.super_walk_forward(sample, [sig], label=g, col=f"p_{g}")
            goal_tables[g] = {"all": A.goal_report(sample, g, f"p_{g}"),
                              "tiers": A.goal_tiers(sample, g, f"p_{g}"),
                              "tiers_pit": A.goal_tiers(sample, g, f"p_{g}", keep=pit(sample)) if pit else None,
                              "pit": A.goal_report(sample, g, f"p_{g}", keep=pit(sample)) if pit else None,
                              "name": gname, "breakeven": breakeven}
            goal_tables[g]["all"].to_csv(out / f"goal_{g}_deciles.csv")
        print(f"[research] goal models done ({time.time() - t0:.0f}s)")

        # ---------------- run 16: short horizons (concrete daily/weekly data + VIX only)
        short = {}
        if "y_up1" in sample:
            for lab in A.SHORT_LABELS:
                sample, _ = A.super_walk_forward(sample, [], label=lab, col=f"s_{lab}", features=A.SHORT_ALL,
                                                 step=2, max_train=150_000)
                sample, _ = A.super_walk_forward(sample, [], label=lab, col=f"m_{lab}", features=A.SHORT_MARKET_ONLY,
                                                 step=2, max_train=150_000)
                short[lab] = {"all": A.short_report(sample, lab, f"s_{lab}"),
                              "market": A.short_report(sample, lab, f"m_{lab}")}
            short_imp = A.short_importance(sample, "up5", A.SHORT_ALL)
            short_imp.to_csv(out / "short_importance_up5.csv", index=False)
            # do the new features improve the +20/-10 goal model?
            sample, _ = A.super_walk_forward(sample, [], label="b20", col="p_b20_ext", features=A.SHORT_ALL)
            goal_ext = {"original": A.goal_tiers(sample, "b20", "p_b20"), "with new features": A.goal_tiers(sample, "b20", "p_b20_ext")}
        print(f"[research] short-horizon models done ({time.time() - t0:.0f}s)")

        # ---------------- run 17: bracket menu and market regime for the goal model's top picks
        score_col = "p_b20_ext" if "p_b20_ext" in sample else "p_b20"
        if f"{next(iter(MENU))}_ret" in sample and score_col in sample:
            menu = A.bracket_menu(sample, score_col, MENU)
            menu.to_csv(out / "bracket_menu.csv", index=False)
            is_top = menu[(menu["period"] == "IS") & (menu["tier"] == "top 10%")]
            menu_choice = ({"return per month": is_top.loc[is_top["return_per_month"].idxmax(), "key"],
                            "return per trade": is_top.loc[is_top["avg_net_return"].idxmax(), "key"]}
                           if len(is_top) else {"return per month": "n/a (no IS scores)", "return per trade": "n/a"})
            regime = A.regime_report(sample, score_col)
            regime.to_csv(out / "regime_top10.csv")
        print(f"[research] bracket menu + regime done ({time.time() - t0:.0f}s)")

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
    pool20 = A.strategy_pool(sig, ranked.head(20))
    # how pros size: more when the strategy is working, less when it isn't
    port_rows.append(("Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)",
                      A.portfolio(pool20, "per_row", "rs_rank", closes=closes, adaptive=True)))
    if "super_prob" in sig:
        port_rows.append(("Top 20 by IS expectancy, ranked by superperformer model",
                          A.portfolio(pool20, "per_row", "super_prob", closes=closes)))
        allsig = sig[(sig["entry_name"] != A.BASELINE) & sig["super_prob"].notna()]
        port_rows.append((f"All setups, ranked by superperformer model / {ref_exit}",
                          A.portfolio(allsig, ref_exit, "super_prob", closes=closes)))
        def top10(df, col="super_prob"):
            # causal-enough cut: 90th percentile of the score within each calendar year of signals
            return df[df[col] >= df.groupby(df["date"].dt.year)[col].transform(lambda p: p.quantile(0.9))]

        top_sup = top10(allsig)
        port_rows.append((f"Only setups in the model's top 10% likely superperformers / sma50_close",
                          A.portfolio(top_sup, "sma50_close", "super_prob", closes=closes)))
        # run-11 checks: is it the setups, survivorship, beaten-down rebounds, or volatility?
        base_sig = sig[(sig["entry_name"] == A.BASELINE) & sig["super_prob"].notna()]
        port_rows.append(("CHECK random entries in the model's top 10% / sma50_close",
                          A.portfolio(top10(base_sig), "sma50_close", "super_prob", closes=closes)))
        port_rows.append(("CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close",
                          A.portfolio(top_sup[top_sup["dist_52w_high"] >= -0.40], "sma50_close", "super_prob", closes=closes)))
        port_rows.append(("Top 10% model + adaptive sizing / sma50_close",
                          A.portfolio(top_sup, "sma50_close", "super_prob", closes=closes, adaptive=True)))
        if "clean_prob" in sig:
            clean_sig = sig[(sig["entry_name"] != A.BASELINE) & sig["clean_prob"].notna()]
            port_rows.append(("Top 10% CLEAN model (+40% before -20%) / sma50_close",
                              A.portfolio(top10(clean_sig, "clean_prob"), "sma50_close", "clean_prob", closes=closes)))
        # ---- user goal portfolios: +20% / +10% before -10%, daily chart
        for g in [x for x in ("b20", "b10") if f"p_{x}" in sig]:
            exit_g = "bracket_20_10" if g == "b20" else "bracket_10_10"
            only_model = A.top_decile_trades(sample, g, f"p_{g}")
            port_rows.append((f"GOAL {g}: model's top 10% stocks, no setup needed / {exit_g}",
                              A.portfolio(only_model, "bracket", "priority", closes=closes)))
            port_rows.append((f"GOAL {g}: model top 10% + adaptive sizing / {exit_g}",
                              A.portfolio(only_model, "bracket", "priority", closes=closes, adaptive=True)))
            gs = sig[(sig["entry_name"] != A.BASELINE) & sig[f"p_{g}"].notna()]
            port_rows.append((f"GOAL {g}: setups in the model's top 10% / {exit_g}",
                              A.portfolio(top10(gs, f"p_{g}"), exit_g, f"p_{g}", closes=closes)))
            if pit is not None:
                port_rows.append((f"GOAL {g}: model top 10%, S&P 500 point-in-time only / {exit_g}",
                                  A.portfolio(only_model[pit(only_model).to_numpy()], "bracket", "priority", closes=closes)))
        # ---- run 17: every bracket on the goal model's top 10%, and a regime gate chosen in-sample
        if menu is not None:
            menu_ports = []
            cal = closes.index
            for key, (up, dn) in MENU.items():
                res = A.portfolio(A.menu_trades(sample, key, dn, score_col, cal), "bracket", "priority", closes=closes)
                menu_ports.append({"bracket": f"+{up:.0%} / -{dn:.0%}", "key": key, **{m: res[m] for m in ("CAGR", "max_DD", "trades", "win")}})
                if key in menu_choice.values() or key in ("m20_10", "m10_10"):
                    tag = ", ".join(k for k, v in menu_choice.items() if v == key)
                    port_rows.append((f"MENU top 10% model / +{up:.0%} -{dn:.0%}" + (f" (IS best {tag})" if tag else ""), res))
            menu_ports = pd.DataFrame(menu_ports)
            menu_ports.to_csv(out / "bracket_menu_portfolio.csv", index=False)
            gated, regime_skipped = A.regime_gate(sample, score_col, regime)
            if (gated["date"] >= A.IS_END).sum() >= 50:
                port_rows.append((f"REGIME top 10% model, skipping {len(regime_skipped)} IS-below-break-even regimes / +20% -10%",
                                  A.portfolio(A.menu_trades(gated, "m20_10", 0.10, score_col, cal, q=0), "bracket", "priority", closes=closes)))
        # ---- Qullamaggie replication: his scan, his setups (flag breakouts via buy-stop, EPs),
        #      his exits, and his Nasdaq-trend exposure rule
        qull_entries = ["qull_breakout", "qull_breakout_60", "ep_gap10", "ep_gap8_hold"]
        qpool = sig[sig["entry_name"].isin(qull_entries)]
        qpool = qpool[A.FILTERS["qull_scan"](qpool)]
        for ex in ("qull_sma10", "qull_sma20", "sma50_close", "bracket_20_10"):
            port_rows.append((f"QULL scan+setups / {ex}", A.portfolio(qpool, ex, "qull_rank", closes=closes)))
        qreg = qpool[qpool["qqq_trend"] == 1]
        for ex in ("qull_sma10", "qull_sma20", "sma50_close"):
            port_rows.append((f"QULL scan+setups, only when QQQ > 10 & 20 SMA / {ex}",
                              A.portfolio(qreg, ex, "qull_rank", closes=closes)))
            port_rows.append((f"QULL ... + regime + adaptive sizing / {ex}",
                              A.portfolio(qreg, ex, "qull_rank", closes=closes, adaptive=True)))
        if pit is not None:
            port_rows.append(("QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20",
                              A.portfolio(qreg[pit(qreg).to_numpy()], "qull_sma20", "qull_rank", closes=closes)))
        if "date_added" in universe.columns:
            added = universe.set_index("ticker")["date_added"]
            added = pd.to_datetime(added, errors="coerce")
            sp5 = top_sup[top_sup["ticker"].isin(universe.loc[universe["index"] == "sp500", "ticker"])].copy()
            sp5["date_added"] = sp5["ticker"].map(added)
            after = sp5[sp5["date"] >= sp5["date_added"]]
            n_oos = lambda d: int((d["date"] >= A.IS_END).sum())
            port_rows.append((f"SURVIVORSHIP S&P 500 names, all dates, top 10% model ({n_oos(sp5)} signals) / sma50_close",
                              A.portfolio(sp5, "sma50_close", "super_prob", closes=closes)))
            port_rows.append((f"SURVIVORSHIP S&P 500 names, only after joining the index ({n_oos(after)} signals) / sma50_close",
                              A.portfolio(after, "sma50_close", "super_prob", closes=closes)))
    # run-5 lesson: the EP portfolio left ~40% of capital idle and earning nothing
    pool10 = A.strategy_pool(sig, ranked.head(10))
    spy_close = market["SPY"]["close"] if "SPY" in market else None
    for risk, slots in ((0.01, 10), (0.02, 10), (0.02, 15)):
        port_rows.append((f"Top 10 by IS expectancy, {risk:.0%} risk, {slots} slots, idle cash in SPY",
                          A.portfolio(pool10, "per_row", "rs_rank", closes=closes, idle=spy_close,
                                      risk=risk, max_pos=slots)))
    spy = A.spy_stats(market["SPY"]) if "SPY" in market else {"CAGR": np.nan, "max_DD": np.nan}
    port = pd.DataFrame([{"strategy": k, **{m: v for m, v in res.items() if m != "curve"},
                          "top2_years_share": A.concentration(res["curve"])} for k, res in port_rows])
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
    found, nxt, key = findings(lb, sel, vsb, vsb_is, exs, filt, mlr, imp, rules, port, sup,
                               sup_imp if sup else None, goal_tables if sup else None)
    if menu is not None:  # run 17: bracket menu
        oos = menu[(menu["period"] == "OOS") & (menu["tier"] == "top 10%")].set_index("key")
        ch = menu_choice["return per month"]
        if ch in oos.index:
            r, b = oos.loc[ch], oos.loc["m20_10"]
            found.append(f"Bracket menu: in-sample best (return per month) is {r['bracket']}. OOS top 10%: hit "
                         f"{r['hit_target']:.1%} (break-even {r['breakeven_hit']:.0%}), {r['avg_net_return']:+.2%} per trade, "
                         f"{r['return_per_month']:+.2%} per month held, vs +20/-10: hit {b['hit_target']:.1%}, "
                         f"{b['avg_net_return']:+.2%}, {b['return_per_month']:+.2%}/month.")
            key["menu_choice"], key["menu_choice_oos_ret"] = r["bracket"], float(r["avg_net_return"])
        found.append(f"Regime gate skipped (chosen in-sample): {regime_skipped or 'none'}.")
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
        *([
            "## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?",
            "",
            f"Every stock every 10 trading days (n={sup['n']:,} out-of-sample rows). Base rate of a >= 40% gain within 3 months: "
            f"{sup['base_rate']:.1%}. The model's top 10% hit it {sup['top_decile_rate']:.1%} of the time "
            f"({sup['top_decile_rate'] / sup['base_rate']:.1f}x the base rate). AUC {sup['auc']:.3f}.",
            "",
            md(sup["deciles"], index=True, floatfmt=".3f"),
            "",
            "What matters most (permutation importance, drop in OOS AUC):",
            "",
            md(sup_imp.head(15), floatfmt=".4f"),
            "",
            "Profile: future superperformers vs everything else, at the moment of the sample:",
            "",
            md(sup_prof, index=True, floatfmt=".3f"),
            "",
            "Readable rules (depth-3 tree fit before 2018, scored after):",
            "",
            md(sup_rules, floatfmt=".3f"),
            "",
            *([f"Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate "
               f"{sup_clean['base_rate']:.1%}, model top 10% {sup_clean['top_decile_rate']:.1%} "
               f"({sup_clean['top_decile_rate'] / sup_clean['base_rate']:.1f}x), AUC {sup_clean['auc']:.3f}.", "",
               md(sup_clean["deciles"], index=True, floatfmt=".3f"), ""] if sup_clean else []),
            *sum(([f"### Your goal: {v['name']} (daily chart, entry at the close, 63-day time limit)", "",
                   f"Break-even hit rate is about {v['breakeven']:.0%} (before costs and timeouts). By decile of the model's "
                   "probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the "
                   "average net return per trade (0.1% costs per side, timeouts included).", "",
                   md(v["all"], index=True, floatfmt=".3f"), "",
                   "Higher confidence tiers (all stocks / point-in-time S&P 500):", "",
                   md(v["tiers"], index=True, floatfmt=".3f"), "",
                   *([md(v["tiers_pit"], index=True, floatfmt=".3f"), ""] if v.get("tiers_pit") is not None else []),
                   *(["S&P 500 stocks only, and only after they joined the index (survivorship check):", "",
                      md(v["pit"], index=True, floatfmt=".3f"), ""] if v["pit"] is not None else [])]
                  for g, v in goal_tables.items()), []),
            "Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that "
            "survived. See the SURVIVORSHIP and CHECK rows in section 9.",
            "",
            f"Setup signals split by the model's score (OOS, exit {ref_exit}; last column sma50_close):",
            "",
            md(sup_sig, index=True, floatfmt=".3f"),
            "",
        ] if sup else []),
        *([
            "## 12. Short horizons: green day / next day / 3 days / week (out-of-sample 2018+)",
            "",
            "Features: candle anatomy, gaps and fair value gaps, relative volume, round numbers / moving averages / "
            "swing support & resistance / 20-day trend line, completed-week structure, VIX (level, change, percentile, "
            "VIX/VIX3M), plus everything the earlier models use. Market-only = market + VIX + calendar features only. "
            "Retrained every 2 years. 'top/bottom' = actual up-rate in the model's highest/lowest 10%; spread = their "
            "difference in average return over the horizon.",
            "",
            md(pd.DataFrame([{"target": A.SHORT_LABELS[k], "model": m, "base rate": v[m]["base"], "AUC": v[m]["auc"],
                              "accuracy": v[m]["accuracy"], "top 10% up": v[m]["top"], "bottom 10% up": v[m]["bottom"],
                              "return spread": v[m]["spread"]} for k, v in short.items() for m in ("all", "market")]),
               floatfmt=".3f"),
            "",
            "Up over the next week, by decile of the full model:",
            "",
            md(short["up5"]["all"]["deciles"], index=True, floatfmt=".4f"),
            "",
            "What drives the 1-week prediction (permutation importance, drop in OOS AUC):",
            "",
            md(short_imp.head(15), floatfmt=".4f"),
            "",
            "Do the new features improve the +20%/-10% goal model? (OOS tiers)",
            "",
            *sum(([f"**{k}**", "", md(v, index=True, floatfmt=".3f"), ""] for k, v in goal_ext.items()), []),
        ] if short else []),
        *(_menu_section(menu, menu_ports, menu_choice, regime, regime_skipped, md) if menu is not None else []),
        "## 11. Qullamaggie replication (per trade, out-of-sample 2018+; IS in brackets)",
        "",
        "Scan = top 3% performer over 1, 3 or 6 months with ADR >= 4%. Regime = QQQ above its 10- and 20-day SMAs. "
        "qull_breakout = buy-stop above the flag high the next day (fill at the trigger or the gap open), stop at the "
        "tighter of the 3-day low and 1 ADR; a same-day touch of the stop counts as stopped out. Portfolio rows start "
        "with QULL in section 9.",
        "",
        md(lb[lb["entry"].isin(["qull_breakout", "qull_breakout_60", "ep_gap10", "ep_gap8_hold", A.BASELINE])
              & lb["filter"].isin(["all", "qull_scan", "qull_scan_regime"])
              & lb["exit"].isin(["qull_sma10", "qull_sma20", "sma50_close", "bracket_20_10"])]
           [["entry", "filter", "exit", "IS_n", "IS_win", "IS_avgR", "OOS_n", "OOS_per_yr", "OOS_win", "OOS_avgR", "OOS_pf", "OOS_t"]]
           .sort_values(["entry", "filter", "exit"])),
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
