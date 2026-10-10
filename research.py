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
from mlalgo.research import fundamentals as F
from mlalgo.research import shorts as SH
from mlalgo.research.entries import ENTRIES
from mlalgo.research.insights import append_history, findings
from mlalgo.research.run import EXIT_NAMES, MENU, run


def md(df: pd.DataFrame, floatfmt=".2f", index=False) -> str:
    return df.to_markdown(index=index, floatfmt=floatfmt)


def _menu_section(menu, menu_ports, menu_choice, regime, regime_pit, gates, md, regime_all=None):
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
        "## 13. Bracket menu and market regime for the +20/-10 model's picks (runs 17-18)",
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
        *(["Same, S&P 500 stocks only after they joined the index (point-in-time survivorship check):", "",
           md(regime_pit.reset_index(), floatfmt=".3f"), ""] if regime_pit is not None and len(regime_pit) else []),
        *(["All stocks (no model), +20/-10, by the same splits: does a leading sector help on its own?", "",
           md(regime_all.reset_index(), floatfmt=".3f"), ""] if regime_all is not None and len(regime_all) else []),
        "Regime gates, one family at a time: skip the buckets of that family that were below break-even in-sample "
        "(hit < 33% or negative return), then trade the model's top 10% with +20/-10. RULE rows keep only the picks that "
        "pass a rule fixed in advance: leading groups (run 19: top 3 of 11 sectors / top 30% of sub-industries by "
        "median RS) and the user's run-21 rules (SPY/QQQ vs 21 & 50 SMA, breadth, A/D line, sector & sub-industry "
        "green / up 5 days / above 21 EMA; groups = equal-weight median of member stocks). "
        "Portfolio 2018+:",
        "",
        md(pd.DataFrame([{"gate": f, "skipped (chosen IS)": ", ".join(map(str, sk)) or "nothing",
                          "CAGR": a["CAGR"] if a else np.nan, "max_DD": a["max_DD"] if a else np.nan,
                          "trades": a["trades"] if a else np.nan,
                          "PIT CAGR": p["CAGR"] if p else np.nan, "PIT max_DD": p["max_DD"] if p else np.nan}
                         for f, sk, a, p in gates]), floatfmt=".3f") if gates else "",
        "",
    ]


WF_ROCKET = ["wf_rocket_breakout", "wf_rocket_gap"]
WF_SCAN = ["wf_scan_pullback", "wf_scan_base", "wf_rocket_gap"]


def workflow_test(sig, lb, closes, market, pit):
    """Run 20: backtest the price-based rules of the user's workflow PDF (rockets 15%, Nasdaq-100
    scanner 25%, core index 40%; the Singapore part and all fundamental tests can't be tested here).
    Rules are taken as written, nothing is tuned. The Nasdaq-100 isn't in the universe, so the
    scanner runs on point-in-time S&P 500 members (large caps) and on the full universe."""
    out = {"ports": [], "trades": None, "regime": None, "blend": None}
    if not set(WF_ROCKET + WF_SCAN) <= set(sig["entry_name"]) or "ndx_regime" not in sig:
        return out
    size = lambda d: d["ndx_regime"].map({2.0: 1.0, 1.0: 0.5, 0.0: 0.0}).fillna(1.0)   # green / yellow / red
    roc = sig[sig["entry_name"].isin(WF_ROCKET)]
    roc = roc[A.FILTERS["wf_rocket"](roc)].copy()
    roc["size_mult"] = size(roc)
    scn = sig[sig["entry_name"].isin(WF_SCAN)]
    scn = scn[A.FILTERS["wf_scan"](scn)].copy()
    rr = ((0.10 - scn["risk_pct"]) / 0.05).clip(0, 1)
    scn["wf_score"] = (40 * scn["rs_rank"] + 30 * rr) / 70        # the business-momentum 30% isn't testable
    scn["size_mult"] = size(scn)
    base = sig[sig["entry_name"] == A.BASELINE]
    b_roc = base[A.FILTERS["wf_rocket"](base)].copy()
    b_roc["size_mult"] = size(b_roc)
    b_scn = base[A.FILTERS["wf_scan"](base)].copy()
    b_scn["wf_score"] = b_scn["rs_rank"]
    b_scn["size_mult"] = size(b_scn)
    nr = lambda d: d.drop(columns="size_mult")            # ignore the regime rule
    # run 21 (user): the PDF's regime with QQQ's 21/50 SMA instead of the 200: above both full size,
    # above one half size, below both no new entries
    s2150 = lambda d: d.assign(size_mult=d["qqq_2150"].map({3.0: 1.0, 2.0: 0.5, 1.0: 0.5, 0.0: 0.0}).fillna(1.0)) \
        if "qqq_2150" in d else d
    P = lambda d, ex, pr, risk, slots: A.portfolio(d, ex, pr, closes=closes, risk=risk, max_pos=slots, pos_cap=0.10)
    pt = (lambda d: d[pit(d).to_numpy()]) if pit is not None else None
    R = lambda d, ex: P(d, ex, "r6_rank", 0.005, 3)        # rockets: 0.5% risk, 3 positions
    S = lambda d, ex: P(d, ex, "wf_score", 0.006, 4)       # scanner: 0.6% risk, 4 positions
    ports = [
        ("rockets as written (regime sizing) / wf_rocket", R(roc, "wf_rocket")),
        ("rockets, no regime rule / wf_rocket", R(nr(roc), "wf_rocket")),
        ("rockets, QQQ 21/50 regime / wf_rocket", R(s2150(roc), "wf_rocket")),
        ("rockets / sma50_close", R(roc, "sma50_close")),
        ("rockets / bracket_20_10", R(roc, "bracket_20_10")),
        ("BASELINE random entries, rocket filter + regime / wf_rocket", R(b_roc, "wf_rocket")),
    ]
    if pt:
        ports += [("rockets as written, S&P 500 point-in-time only / wf_rocket", R(pt(roc), "wf_rocket"))]
        ports += [
            ("scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10", S(pt(scn), "wf_weekly10")),
            ("scanner PIT, no regime rule / wf_weekly10", S(nr(pt(scn)), "wf_weekly10")),
            ("scanner PIT, QQQ 21/50 regime / wf_weekly10", S(s2150(pt(scn)), "wf_weekly10")),
            ("scanner PIT / sma50_close", S(pt(scn), "sma50_close")),
            ("BASELINE random entries, scanner filter + regime, PIT / wf_weekly10", S(pt(b_scn), "wf_weekly10")),
        ]
    ports += [("scanner as written, full universe / wf_weekly10", S(scn, "wf_weekly10"))]
    out["ports"] = ports
    # per trade: each setup vs the random baseline, same filter and exit (IS and OOS)
    ex_ok = lb["exit"].isin(["wf_rocket", "wf_weekly10", "sma50_close", "bracket_20_10"])
    rk = lb["entry"].isin(WF_ROCKET + [A.BASELINE]) & lb["filter"].isin(["wf_rocket", "wf_rocket_green"])
    sk = lb["entry"].isin(WF_SCAN + [A.BASELINE]) & lb["filter"].isin(["wf_scan", "wf_scan_green"])
    keep = lb[ex_ok & (rk | sk)]
    out["trades"] = keep[["entry", "filter", "exit", "IS_n", "IS_avgR", "IS_win", "OOS_n", "OOS_avgR", "OOS_win", "OOS_t"]
                         ].sort_values(["filter", "exit", "OOS_avgR"], ascending=[True, True, False])
    # per trade by Nasdaq regime (green / yellow / red), with the PDF's own exits
    rows = []
    for name, d, ex in (("rockets", roc, "wf_rocket"), ("scanner", scn, "wf_weekly10"),
                        ("random (rocket filter)", b_roc, "wf_rocket"), ("random (scanner filter)", b_scn, "wf_weekly10")):
        for period, m in (("IS", d["date"] < A.IS_END), ("OOS", d["date"] >= A.IS_END)):
            for col, labels in (("ndx_regime", {2.0: "PDF green (200d)", 1.0: "PDF yellow", 0.0: "PDF red"}),
                                ("qqq_2150", {3.0: "QQQ > 21 & 50", 2.0: "QQQ > 21 only", 1.0: "QQQ > 50 only", 0.0: "QQQ < both"})):
                if col not in d:
                    continue
                for reg, g in d[m].groupby(col):
                    rows.append({"part": name, "regime": labels.get(reg, reg),
                                 "period": period, "n": len(g), "avgR": g[f"R_{ex}"].mean(), "win": (g[f"R_{ex}"] > 0).mean()})
    if rows:
        t = pd.DataFrame(rows).pivot_table(index=["part", "regime"], columns="period", values=["n", "avgR", "win"], sort=False)
        t.columns = [f"{p}_{v}" for v, p in t.columns]
        out["regime"] = t[[c for c in ("IS_n", "IS_avgR", "IS_win", "OOS_n", "OOS_avgR", "OOS_win") if c in t]].reset_index()
    # the PDF's portfolio: 40% core index + 25% scanner + 15% rockets + 20% Singapore (untested -> cash)
    curves = dict(ports)
    spy = market["SPY"]["close"] if "SPY" in market else None
    sc_key = "scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10"
    ro_key = "rockets as written, S&P 500 point-in-time only / wf_rocket"
    if spy is not None and sc_key in curves and ro_key in curves:
        r = pd.DataFrame({"core": spy[spy.index >= A.IS_END].pct_change(),
                          "scanner": curves[sc_key]["curve"].pct_change(),
                          "rockets": curves[ro_key]["curve"].pct_change()}).dropna(how="all").fillna(0.0)
        blends = {"PDF split: 40% SPY / 25% scanner / 15% rockets / 20% cash": {"core": 0.40, "scanner": 0.25, "rockets": 0.15},
                  "trading parts only, 25:15": {"scanner": 0.625, "rockets": 0.375},
                  "SPY 100%": {"core": 1.0}}
        res = []
        for name, w in blends.items():
            eq = (1 + sum(r[k] * v for k, v in w.items())).cumprod()
            yrs = (eq.index[-1] - eq.index[0]).days / 365.25
            res.append({"portfolio (2018+, daily rebalanced)": name, "CAGR": eq.iloc[-1] ** (1 / yrs) - 1,
                        "max_DD": (eq / eq.cummax() - 1).min(), "worst_year": A.yearly(eq).min()})
        out["blend"] = pd.DataFrame(res)
    return out


def run24(sig, sample, lb, closes, prices, market, pit, pit_current, hist, score_col, out):
    """Run 24 (consolidated): earnings placebo, hold-through-earnings, survivorship, momentum and
    breadth-timing portfolios, edge vs risk part 2, cost stress, picks replay, course setups."""
    from mlalgo.research.run import market_internals
    r = {"ports": []}
    period = lambda d: np.where(d["date"] < A.IS_END, "IS", "OOS")
    # 1) earnings placebo: do gaps drift because of earnings news (post-earnings drift), or regardless?
    if "earnings_gap" in sig and sig["earnings_gap"].notna().any():
        g = sig[(sig["entry_name"].str.startswith("ep_") | sig["entry_name"].isin(["wf_rocket_gap", A.BASELINE]))
                & sig["earnings_gap"].notna()].copy()
        g["group"] = np.where(g["entry_name"] == A.BASELINE, "random entries",
                              np.where(g["entry_name"] == "wf_rocket_gap", "gap >= 5% holding 2 days", "episodic pivots (ep_*)"))
        g["earnings"] = np.where(g["earnings_gap"] == 1, "earnings release", "no earnings")
        g["period"] = period(g)
        t = g.groupby(["group", "earnings", "period"]).agg(n=("R_sma50_close", "size"), avgR_sma50=("R_sma50_close", "mean"),
                                                           win_sma50=("R_sma50_close", lambda x: (x > 0).mean()),
                                                           avgR_b20=("R_bracket_20_10", "mean")).unstack("period")
        t.columns = [f"{p}_{m}" for m, p in t.columns]
        r["placebo"] = t.reset_index()
    # 2) hold through earnings: model picks by days to the next earnings release
    if score_col and "days_to_earnings" in sample and sample["days_to_earnings"].notna().any():
        o = A._top(sample[sample[score_col].notna() & sample["b20_ret"].notna()], score_col, 0.9)
        o = o[o["days_to_earnings"].notna()]
        b = pd.cut(o["days_to_earnings"], [-1, 7, 30, 63, np.inf], labels=["<= 7 days", "8-30 days", "31-63 days", "> 63 days"])
        t = o.groupby([b, period(o)], observed=True).agg(n=("b20_ret", "size"), hit=("b20_hit", "mean"),
                                                         avg_ret=("b20_ret", "mean")).unstack()
        t.columns = [f"{p}_{m}" for m, p in t.columns]
        r["earnings_hold"] = t.reset_index().rename(columns={"days_to_earnings": "next earnings in"})
    cal = closes.index
    spy = market["SPY"]["close"] if "SPY" in market else None
    # 3) survivorship: point-in-time with current members only vs incl. former members
    if score_col and pit is not None and pit_current is not None:
        tr = A.menu_trades(sample, "m20_10", 0.10, score_col, cal)
        rows = []
        for name, fn in (("current members only (as before)", pit_current), ("incl. former members (membership history)", pit)):
            sub = tr[fn(tr).to_numpy()]
            res = A.portfolio(sub, "bracket", "priority", closes=closes)
            o = sub[sub["date"] >= A.IS_END]
            rows.append({"point-in-time S&P 500": name, "trades_OOS": len(o), "hit_OOS": (o["ret_bracket"] >= 0.197).mean(),
                         "avg_ret_OOS": o["ret_bracket"].mean(), "CAGR": res["CAGR"], "max_DD": res["max_DD"]})
            r["ports"].append((f"SURVIVORSHIP goal model top 10%, PIT {name} / +20% -10%", res))
        r["survivorship"] = pd.DataFrame(rows)
    # 4) course: volatility-adjusted momentum portfolio and breadth timing of the index
    dv = pd.DataFrame({t: (df["close"] * df["volume"]).rolling(50).mean() for t, df in prices.items()}).reindex(cal)
    mom = {}
    members = D.sp500_mask(hist, cal, closes.columns) if hist is not None and len(hist) else None
    for name, kw in (("top 10, vol-adjusted (course 9.8)", {}), ("top 20, vol-adjusted", {"top": 20}),
                     ("top 10, raw momentum (not vol-adjusted)", {"vol_adj": False})):
        mom[f"{name}, all stocks"] = A.momentum_portfolio(closes, dv, **kw)
        if members is not None:
            mom[f"{name}, S&P 500 point-in-time"] = A.momentum_portfolio(closes, dv, members=members, **kw)
    internals = market_internals(prices)
    irx = market["^IRX"]["close"] if "^IRX" in market else None
    if spy is not None:
        mom["SPY buy & hold"] = spy.pct_change().fillna(0)
        mom["SPY timed by breadth: buy < 20% above 20d, sell > 60% (course 2.2)"] = A.breadth_timing(spy, internals["breadth_20"], irx=irx)
        b50 = (pd.DataFrame({t: (df["close"] > df["close"].rolling(50).mean()).where(df["close"].rolling(50).count() == 50)
                             for t, df in prices.items()}).mean(axis=1))
        mom["SPY timed by % above 50d (same thresholds)"] = A.breadth_timing(spy, b50, irx=irx)
    r["course_ports"] = pd.DataFrame([{"strategy": k, **A.split_stats(v)} for k, v in mom.items()])
    # 5) edge vs risk part 2: year by year, and market-adjusted (alpha / beta vs SPY)
    if score_col:
        yrs = {"full universe": A.vol_matched_years(sample, score_col)}
        if pit is not None:
            yrs["S&P 500 point-in-time"] = A.vol_matched_years(sample, score_col, keep=pit)
        r["years"] = pd.concat([v.assign(sample=k) for k, v in yrs.items()]).reset_index().rename(columns={"date": "year"})
        ab = []
        tr = A.menu_trades(sample, "m20_10", 0.10, score_col, cal)
        if spy is not None:
            curves = {"goal model top 10%, full universe": A.portfolio(tr, "bracket", "priority", closes=closes)["curve"]}
            if pit is not None:
                curves["goal model top 10%, S&P 500 PIT"] = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes)["curve"]
            for k, v in mom.items():
                if "point-in-time" in k or "breadth" in k or "50d" in k:
                    eq = (1 + v[v.index >= A.IS_END]).cumprod()
                    curves[k] = eq
            curves["SPY"] = spy[spy.index >= A.IS_END]
            ab = [{"strategy (2018+)": k, **A.alpha_beta(v, spy)} for k, v in curves.items()]
        r["alpha"] = pd.DataFrame(ab)
        # 6) cost stress: +0.4% per round trip (0.3% per side instead of 0.1%)
        rows = []
        for name, keep in (("goal model top 10%, full universe", None), ("goal model top 10%, S&P 500 PIT", pit)):
            if name.endswith("PIT") and keep is None:
                continue
            t2 = tr if keep is None else tr[keep(tr).to_numpy()]
            for c_name, extra in (("0.1% per side", 0.0), ("0.3% per side", 0.004)):
                res = A.portfolio(t2.assign(ret_bracket=t2["ret_bracket"] - extra), "bracket", "priority", closes=closes)
                rows.append({"strategy": name, "costs": c_name, "CAGR": res["CAGR"], "max_DD": res["max_DD"]})
        ep = sig[sig["entry_name"].isin(["ep_gap10", "ep_gap8_hold"])]
        ep = ep[A.FILTERS["rs80"](ep)]
        for c_name, extra in (("0.1% per side", 0.0), ("0.3% per side", 0.004)):
            res = A.portfolio(ep.assign(ret_sma50_close=ep["ret_sma50_close"] - extra), "sma50_close", "rs_rank", closes=closes)
            rows.append({"strategy": "episodic pivots (gap 10% / 8% hold), RS top 20% / sma50", "costs": c_name,
                         "CAGR": res["CAGR"], "max_DD": res["max_DD"]})
        r["costs"] = pd.DataFrame(rows)
        # 7) replay of the picks tool's rule (current features vs the upgraded set)
        reps = {"picks tool as today (original features)": A.replay_picks(sample),
                "upgraded features (run-16 set)": A.replay_picks(sample, features=A.SHORT_ALL)}
        reps = {k: v for k, v in reps.items() if len(v)}
        if reps:
            r["replay"] = pd.concat([A.replay_summary(v).assign(model=k) for k, v in reps.items()]).reset_index()
            pd.concat([v.assign(model=k) for k, v in reps.items()]).to_csv(out / "picks_replay.csv", index=False)
    # 8) course setups vs random entries (same filter and exit)
    tc = [e for e in ENTRIES if e.startswith("tc_")]
    r["course_setups"] = lb[lb["entry"].isin(tc + [A.BASELINE]) & lb["filter"].isin(["all", "rs80"])
                            & lb["exit"].isin(["sma50_close", "ema21_close", "bracket_20_10"])][
        ["entry", "filter", "exit", "IS_n", "IS_avgR", "IS_win", "OOS_n", "OOS_avgR", "OOS_win"]].sort_values(["filter", "exit", "entry"])
    for k in ("placebo", "earnings_hold", "survivorship", "course_ports", "years", "alpha", "costs", "replay", "course_setups"):
        if k in r and isinstance(r[k], pd.DataFrame):
            r[k].to_csv(out / f"run24_{k}.csv", index=False)
    return r


def _run24_section(r, md):
    T = lambda k, f=".3f": md(r[k], floatfmt=f) if isinstance(r.get(k), pd.DataFrame) and len(r[k]) else "(not available)"
    return [
        "## 16. Run 24: consolidated tests",
        "",
        "### Earnings placebo: do gaps drift because of earnings news?",
        "Gap setups split by whether an earnings release (SEC 8-K Item 2.02) was filed that day or up to 3 days "
        "before. If 'no earnings' gaps do as well, post-earnings drift is not the reason the setup works.",
        "",
        T("placebo"),
        "",
        "### Holding through earnings (course: don't, without a cushion)",
        "Goal model top 10%, +20/-10, by days from entry to the next earnings release:",
        "",
        T("earnings_hold"),
        "",
        "### Survivorship: current members only vs incl. former S&P 500 members",
        "",
        T("survivorship"),
        "",
        "### Is the edge real? Year by year vs same-volatility, same-momentum stocks",
        "",
        T("years"),
        "",
        "### Market-adjusted (2018+): beta, alpha vs SPY, Sharpe, return / drawdown",
        "",
        T("alpha"),
        "",
        "### Cost stress (0.3% per side)",
        "",
        T("costs"),
        "",
        "### Replay of the daily picks tool's rule (top 10 per date, model retrained quarterly, 2023+)",
        "",
        T("replay"),
        "",
        "### Course portfolios: volatility-adjusted momentum and breadth timing (IS 2007-2017, OOS 2018+)",
        "",
        T("course_ports"),
        "",
        "### Course setups vs random entries (R multiples)",
        "",
        T("course_setups"),
        "",
    ]


def _workflow_section(wf, md):
    port = pd.DataFrame([{"strategy": k, **{m: v.get(m) for m in ("CAGR", "max_DD", "trades", "win", "avg_positions")}}
                         for k, v in wf["ports"]])
    return [
        "## 14. Your Stock Selection Workflow PDF, price-testable rules (run 20)",
        "",
        "Rules as written, nothing tuned. Rockets: 6-week base -> new 52w high on 1.5x volume (<= 5% above the "
        "pivot, stop -8%) or a >= 5% gap on 2x volume holding its low for 2 days (no earnings dates: volume is the "
        "proxy); price >= $10, >= $20M/day, top 20% 6-month return; exit = sell 1/3 at +25%, stop to entry, trail "
        "the 50 SMA. Scanner: above a rising 200d, 50d > 200d, within 15% of the 52w high; entry = pullback to the "
        "21 EMA / 50 SMA then a close above the prior high, a 4-week base breakout, or a holding gap; stop under the "
        "pullback/base low, skipped if > 10%; ranked by RS (40) + stop distance (30); exit = weekly close below the "
        "10-week MA. Regime (QQQ): green full size, yellow half, red no new entries. Sizing: rockets 0.5% risk x 3 "
        "positions, scanner 0.6% x 4, max 10% per stock. Not testable here: fundamentals (guidance, revenue, FCF, "
        "estimates), the Singapore part, the Nasdaq-100 membership itself.",
        "",
        "Per trade vs random entries with the same filter and exit (R multiples):",
        "",
        md(wf["trades"], floatfmt=".3f"),
        "",
        "Per trade by Nasdaq-100 regime at entry (the PDF's own exits):",
        "",
        md(wf["regime"], floatfmt=".3f") if wf.get("regime") is not None else "",
        "",
        "Portfolios 2018+ (marked to market daily):",
        "",
        md(port, floatfmt=".3f"),
        "",
        *(["The PDF's full split (Singapore part as cash; scanner and rockets point-in-time):", "",
           md(wf["blend"], floatfmt=".3f"), ""] if wf.get("blend") is not None else []),
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
    # run 22: point-in-time fundamentals from SEC filings (cached next to the prices)
    fund = F.load_fundamentals(a.cache, list(prices)) if not a.prices_parquet or \
        (Path(a.cache) / "fundamentals.parquet").exists() else pd.DataFrame()
    earn = F.load_earnings(a.cache, list(prices)) if not a.prices_parquet or \
        (Path(a.cache) / "earnings.parquet").exists() else pd.DataFrame()
    if a.download_only:
        print(f"[research] cached {len(prices)} tickers + {list(market)}, fundamentals for "
              f"{fund['ticker'].nunique() if len(fund) else 0} tickers")
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
    if len(sample):
        sample = F.attach(sample, fund)
        print(f"[research] fundamentals known on {sample['rev_yoy'].notna().mean():.0%} of sample rows")
        sample = F.tag_earnings(sample, earn)
    sig = F.tag_earnings(sig, earn)

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
    regime_all = None
    vm_tab = None
    pit = pit_current = None
    hist_file = Path(a.cache) / "sp500_history.csv"          # local smoke tests can supply one
    sp_hist = D.sp500_history() if not a.prices_parquet else (
        pd.read_csv(hist_file, parse_dates=["start", "end"]) if hist_file.exists() else None)
    menu = regime = regime_pit = menu_choice = menu_ports = regime_skipped = None
    regime_gates = []
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
            sp500 = set(universe.loc[(universe["index"] == "sp500") & (universe["status"] == "current"), "ticker"])
            pit_current = lambda d: d["ticker"].isin(sp500) & (d["date"] >= d["ticker"].map(added))
            pit = pit_current
        # run 24: membership spells incl. former members (removed since 2006) -> a fuller point-in-time set
        if sp_hist is not None and len(sp_hist):
            pit = lambda d: D.in_sp500(d, sp_hist)
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
            # run 22: do point-in-time fundamentals (and the 200-day extension) improve the goal model?
            if "rev_yoy" in sample and sample["rev_yoy"].notna().mean() > 0.2:
                fund_feats = list(dict.fromkeys(A.SHORT_ALL + F.FUND_FEATURES + ["ext_200"]))
                sample, _ = A.super_walk_forward(sample, [], label="b20", col="p_b20_fund", features=fund_feats)
                goal_ext["with fundamentals"] = A.goal_tiers(sample, "b20", "p_b20_fund")
                if pit:
                    goal_ext["with new features, point-in-time S&P 500"] = A.goal_tiers(sample, "b20", "p_b20_ext", keep=pit(sample))
                    goal_ext["with fundamentals, point-in-time S&P 500"] = A.goal_tiers(sample, "b20", "p_b20_fund", keep=pit(sample))
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
            regime_pit = A.regime_report(sample, score_col, keep=pit) if pit else None
            # run 19: the same splits for ALL stocks (no model): do leading sectors help on their own?
            regime_all = A.regime_report(sample, score_col, q=0.0)
            regime_all.to_csv(out / "regime_all_stocks.csv")
            # run 23: is the model's edge just volatility + momentum? (same-ADR, same-momentum comparison)
            vm = {"goal model (full universe)": A.vol_matched(sample, score_col)}
            if pit:
                vm["goal model, S&P 500 point-in-time"] = A.vol_matched(sample, score_col, keep=pit)
            vm_tab = pd.concat([v.assign(sample=k) for k, v in vm.items()], ignore_index=True)
            vm_tab.to_csv(out / "vol_matched.csv", index=False)
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
            # run 18: one regime family at a time (run 17's combined gate skipped nearly everything);
            # within a family, skip the buckets that were below break-even in-sample
            fams = list(dict.fromkeys(regime.index.get_level_values(0)))
            for fam in fams:
                gated, skipped = A.regime_gate(sample, score_col, regime[regime.index.get_level_values(0) == fam])
                if not skipped or (gated["date"] >= A.IS_END).sum() < 50:
                    regime_gates.append((fam, [b for _, b in skipped], None, None))
                    continue
                tr = A.menu_trades(gated, "m20_10", 0.10, score_col, cal, q=0)
                full = A.portfolio(tr, "bracket", "priority", closes=closes)
                pt = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes) if pit else None
                regime_gates.append((fam, [b for _, b in skipped], full, pt))
                port_rows.append((f"REGIME {fam}: skip {[b for _, b in skipped]} / +20% -10%", full))
                if pt is not None:
                    port_rows.append((f"REGIME {fam}, S&P 500 point-in-time only / +20% -10%", pt))
            # run 19 (user's question): only trade the model's picks from leading sectors / sub-industries
            # (pre-registered cut-offs: top 3 of 11 sectors, top 30% of sub-industries by median RS)
            top_rows = A._top(sample[sample[score_col].notna() & sample["m20_10_ret"].notna()], score_col, 0.9)
            T = top_rows
            leading = {"top 3 sectors only": T["sector_rank"] >= 0.75,
                       "top 30% sub-industries only": T["industry_rank"] >= 0.7,
                       "top 3 sectors AND top 30% sub-industries": (T["sector_rank"] >= 0.75) & (T["industry_rank"] >= 0.7)}
            # run 21 (user's rules, fixed in advance): short market trend, breadth, A/D line, group momentum
            if "spy_2150" in T:
                both = lambda f: (T[f"sec_{f}"] > (0.5 if f == "up21" else 0)) & (T[f"ind_{f}"] > (0.5 if f == "up21" else 0))
                leading.update({
                    "SPY above its 21 & 50 SMA": T["spy_2150"] == 3,
                    "QQQ above its 21 & 50 SMA": T["qqq_2150"] == 3,
                    "SPY above its 50 SMA (21 either way)": T["spy_2150"].isin([1, 3]),
                    "A/D line above its 21 & 50 MA": T["ad_2150"] == 3,
                    "> 50% of stocks above their 50d": T["breadth_50"] > 0.5,
                    "% above 50d rising over 10 days": T["breadth_50_chg10"] > 0,
                    "sector AND sub-industry green today": both("ret1"),
                    "sector AND sub-industry up over 5 days": both("ret5"),
                    "sector AND sub-industry above 21 EMA": both("up21"),
                    "SPY > 21 & 50 + sector & sub-industry up 5 days": (T["spy_2150"] == 3) & both("ret5"),
                })
            # run 24 (course): don't buy more than ~10% above the 21 EMA
            leading.update({"<= 10% above the 21 EMA (course rule)": T["dist_ema21"] <= 0.10})
            # run 23 (user's ADR% infographic)
            leading.update({
                "ADR% >= 5% (the infographic's minimum)": T["adr_pct"] >= 0.05,
                "ADR% 5-12% (the infographic's sweet spot)": T["adr_pct"].between(0.05, 0.12),
                "ADR% <= 15% (skip the wildest)": T["adr_pct"] <= 0.15,
                "ADR% 5-12% and >= $10M/day": T["adr_pct"].between(0.05, 0.12) & (T["dollar_vol_50"] >= 10e6),
            })
            # run 22 (user): early fundamental inflection + volume accumulation + not extended
            if "inflection" in T:
                price_ok = (T["updown_vol_50"] > 1.0) & (T["ext_200"] < 0.30) & (T["ret_126"] < 0.50)
                leading.update({
                    "fundamental inflection (rev accel 2q + op leverage + margin + FCF up)": T["inflection"] == 1,
                    "revenue growth accelerating 2+ quarters": T["rev_accel_q"] >= 2,
                    "accumulation (up/down volume 50d > 1)": T["updown_vol_50"] > 1.0,
                    "not extended (< 30% above the 200-day)": T["ext_200"] < 0.30,
                    "not already up 50%+ in 6 months": T["ret_126"] < 0.50,
                    "price rules only (accumulation + not extended + not up 50%)": price_ok,
                    "user's full method (inflection + price rules)": price_ok & (T["inflection"] == 1),
                })
            for name, m in leading.items():
                g = top_rows[m.fillna(False).to_numpy()]
                if (g["date"] >= A.IS_END).sum() < 50:
                    continue
                tr = A.menu_trades(g, "m20_10", 0.10, score_col, cal, q=0)
                full = A.portfolio(tr, "bracket", "priority", closes=closes)
                pt = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes) if pit else None
                regime_gates.append((f"RULE: {name}", [], full, pt))
                port_rows.append((f"RULE {name}, model top 10% / +20% -10%", full))
                if pt is not None:
                    port_rows.append((f"RULE {name}, S&P 500 point-in-time only / +20% -10%", pt))
            if "inflection" in sample and sample["inflection"].notna().any():
                S_ = sample[sample["m20_10_ret"].notna() & sample["rev_yoy_d1"].notna()]
                p_ok = (S_["updown_vol_50"] > 1.0) & (S_["ext_200"] < 0.30) & (S_["ret_126"] < 0.50)
                for name, m in {"user's method alone, no model (inflection + price rules)": p_ok & (S_["inflection"] == 1),
                                "fundamental inflection alone, no model": S_["inflection"] == 1}.items():
                    g = S_[m.fillna(False).to_numpy()]
                    if (g["date"] >= A.IS_END).sum() < 50:
                        continue
                    tr = A.menu_trades(g, "m20_10", 0.10, "rev_yoy_d1", cal, q=0)   # fastest acceleration first
                    full = A.portfolio(tr, "bracket", "priority", closes=closes)
                    pt_ = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes) if pit else None
                    regime_gates.append((f"METHOD: {name}", [], full, pt_))
                    port_rows.append((f"METHOD {name} / +20% -10%", full))
            if "p_b20_fund" in sample:
                tr = A.menu_trades(sample, "m20_10", 0.10, "p_b20_fund", cal)
                full = A.portfolio(tr, "bracket", "priority", closes=closes)
                pt_ = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes) if pit else None
                regime_gates.append(("MODEL + fundamentals as features, top 10%", [], full, pt_))
                port_rows.append(("MODEL with fundamentals, top 10% / +20% -10%", full))
            # run 23: "higher ADR% = smaller position": scale risk by 6% / ADR (x0.4 .. x1.5)
            tr = A.menu_trades(sample, "m20_10", 0.10, score_col, cal)
            tr["size_mult"] = (0.06 / tr["adr_pct"]).clip(0.4, 1.5).fillna(1.0)
            full = A.portfolio(tr, "bracket", "priority", closes=closes)
            pt_ = A.portfolio(tr[pit(tr).to_numpy()], "bracket", "priority", closes=closes) if pit else None
            regime_gates.append(("SIZE: position scaled by 6% / ADR (x0.4-1.5)", [], full, pt_))
            port_rows.append(("SIZE model top 10%, position scaled by 6% / ADR / +20% -10%", full))
            if pit:
                base_tr = A.menu_trades(sample, "m20_10", 0.10, score_col, cal)
                regime_gates.append(("(no gate)", [], A.portfolio(base_tr, "bracket", "priority", closes=closes),
                                     A.portfolio(base_tr[pit(base_tr).to_numpy()], "bracket", "priority", closes=closes)))
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
    # ---------------- run 23: ADR% by setup, and Qullamaggie's parabolic shorts
    adr_tab = A.setups_by_adr(sig)
    adr_tab.to_csv(out / "setups_by_adr.csv", index=False)
    shorts_all = SH.run_all(prices)
    shorts_tab = SH.report(shorts_all, A.IS_END)
    shorts_tab.to_csv(out / "parabolic_shorts.csv", index=False)
    if len(shorts_all):
        sa = shorts_all[shorts_all["variant"] == "trigger"]
        shorts_adr = sa.groupby([pd.cut(sa["adr_pct"], A.ADR_BINS, labels=A.ADR_LABELS),
                                 np.where(sa["date"] < A.IS_END, "IS", "OOS")], observed=True)["R_sma10"].agg(["size", "mean"]).unstack()
    else:
        shorts_adr = pd.DataFrame()
    # ---------------- run 20: the user's "Stock Selection Workflow" PDF, price-testable parts
    wf = workflow_test(sig, lb, closes, market, pit)
    for k, res in wf["ports"]:
        port_rows.append((f"WORKFLOW {k}", res))
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

    # ---------------- run 24: consolidated tests
    r24 = run24(sig, sample, lb, closes, prices, market, pit, pit_current, sp_hist,
                score_col if menu is not None else None, out)

    # ---------------- what this run tells us
    found, nxt, key = findings(lb, sel, vsb, vsb_is, exs, filt, mlr, imp, rules, port, sup,
                               sup_imp if sup else None, goal_tables if sup else None)
    for k, v in wf["ports"]:
        if "as written" in k or "21/50" in k:
            found.append(f"Workflow PDF {k}: {v['CAGR']:.1%} CAGR, {v['max_DD']:.0%} DD, {v['trades']} trades.")
    if wf.get("blend") is not None:
        b0 = wf["blend"].iloc[0]
        found.append(f"Workflow PDF split (40/25/15/20 cash): {b0['CAGR']:.1%} CAGR, {b0['max_DD']:.0%} DD vs SPY "
                     f"{wf['blend'].iloc[-1]['CAGR']:.1%}, {wf['blend'].iloc[-1]['max_DD']:.0%}.")
    if vm_tab is not None:   # run 23
        for r in vm_tab[vm_tab["period"] == "OOS"].itertuples():
            found.append(f"Volatility-matched check ({r.sample}, OOS): model top 10% hit {r.hit:.1%} vs {r.matched_hit:.1%} "
                         f"for same-ADR, same-momentum stocks; return {r.ret:+.2%} vs {r.matched_ret:+.2%} per trade.")
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
        for f, sk, a, p in regime_gates:
            if a:
                found.append(f"{'Filter ' + f if f.startswith(('RULE', 'METHOD', 'MODEL', 'SIZE')) else f'Regime gate {f} (skip ' + (', '.join(map(str, sk)) or 'nothing') + ')'}: {a['CAGR']:.1%} CAGR, "
                             f"{a['max_DD']:.0%} DD" + (f"; point-in-time S&P 500 {p['CAGR']:.1%}, {p['max_DD']:.0%}" if p else "") + ".")
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
        *_run24_section(r24, md),
        "## 15. ADR%, volatility-matched check, parabolic shorts (run 23)",
        "",
        "Is the goal model only picking volatile, strong stocks? Its top 10% vs the average of all stocks in the "
        "same year, ADR decile and 6-month-return quintile (+20/-10). edge = actual - matched:",
        "",
        md(vm_tab, floatfmt=".3f") if vm_tab is not None else "",
        "",
        "Setups by ADR% (stocks >= $10M/day, exit sma50_close, R multiples). The infographic says: < 5% too slow, "
        "5-12% the sweet spot, > 15% often fails:",
        "",
        md(adr_tab, floatfmt=".3f") if len(adr_tab) else "",
        "",
        "Qullamaggie's parabolic shorts (up >= 50% in 10 days, >= 3 up closes of 4, >= 20% above the 10-day; entry = "
        "first close below the prior day's low within 3 days, or no_trigger = short the parabolic day itself; stop = "
        "high of the run; cover at the 10- or 20-day average or after 20 days; price >= $5, >= $10M/day; borrow "
        "fees not included):",
        "",
        md(shorts_tab, floatfmt=".3f") if len(shorts_tab) else "(no signals)",
        "",
        *(["Parabolic shorts (trigger, cover at the 10-day) by ADR%: count and average R", "",
           md(shorts_adr, index=True, floatfmt=".3f"), ""] if len(shorts_adr) else []),
        *(_workflow_section(wf, md) if wf.get("trades") is not None else []),
        *(_menu_section(menu, menu_ports, menu_choice, regime, regime_pit, regime_gates, md, regime_all) if menu is not None else []),
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
