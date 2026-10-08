"""Daily scan: market regime -> filter the universe -> setups firing now -> primed watchlist.

Examples:
    python scan.py --universe universes/sample.txt
    python scan.py --universe universes/sample.txt --fundamentals          # + paper factors & theme
    python scan.py --universe universes/sample.txt --filter trend_template --evaluate
"""
import argparse

import pandas as pd

from mlalgo import pipeline, primed_model, setup_model
from mlalgo.labels import label_panel
from mlalgo.setups import SetupConfig
from mlalgo.structure import ML_FEATURES
from mlalgo.universe import FILTER_COLUMNS, PRESETS

WATCH = ["close", "prob_primed", "setup_score", "base_count", "dist_to_pivot", "tight_10", "atr_ratio",
         "vol_dryup", "down_vol_ratio_10", "adr_pct", "rs_rank", "ext_ema8_adr"]


def main() -> None:
    p = argparse.ArgumentParser()
    pipeline.add_source_args(p)
    p.add_argument("--filter", choices=list(PRESETS), default="momentum")
    p.add_argument("--min-rs", type=float, default=0.70)
    p.add_argument("--target", type=float, default=0.10, help="primed model: profit target (0.10 = +10%%)")
    p.add_argument("--stop", type=float, default=0.05, help="primed model: stop loss")
    p.add_argument("--horizon", type=int, default=20, help="primed model: max days")
    p.add_argument("--recent", type=int, default=3, help="show setups that fired in the last N days")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--fundamentals", action="store_true", help="fetch FCF yield, B/M, ROA, size, industry (slow)")
    p.add_argument("--evaluate", action="store_true", help="walk-forward test of the primed model")
    p.add_argument("--out", help="save the watchlist to CSV")
    a = p.parse_args()

    prices, market = pipeline.load(a)
    cfg = PRESETS[a.filter]
    cfg = type(cfg)(**{**cfg.__dict__, "min_rs_rank": a.min_rs})
    panel = pipeline.build(prices, market, cfg)
    panel = panel.join(label_panel(prices, target=a.target, stop=a.stop, horizon=a.horizon))
    pd.set_option("display.float_format", "{:.3f}".format)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)

    dates = panel.index.get_level_values("date")
    last = dates.max()
    today = panel.xs(last, level="date")

    # ---- market regime
    m = today.iloc[0]
    print(f"\n{last.date()}  universe: {len(prices)} tickers")
    print(f"Market: SPY above 8/21/50 EMA = {'YES' if m.get('mkt_ok') == 1 else 'NO (reduce size)'}"
          + (f", QQQ = {'YES' if m.get('qqq_ok') == 1 else 'NO'}" if "qqq_ok" in today else "")
          + (f", rates rising vs 1y ago = {'YES (headwind)' if m.get('rates_rising') == 1 else 'no'}" if "rates_rising" in today else ""))

    # ---- stage 1 funnel
    print(f"\nFilter funnel ({a.filter}):")
    remaining = pd.Series(True, index=today.index)
    for col in FILTER_COLUMNS:
        remaining &= today[col]
        print(f"  after {col[2:]:<10} {remaining.sum():>5}")

    # ---- setups firing now, scored by a model trained on all past (closed) trades
    signals = pipeline.signals_for(prices, panel, SetupConfig())
    recent_cut = dates.unique().sort_values()[-a.recent]
    live = pd.concat([s for s in signals.values()], ignore_index=True) if signals else pd.DataFrame()
    live = live[live["date"] >= recent_cut] if len(live) else live
    if len(live):
        feats = panel.reindex(pd.MultiIndex.from_arrays([live["date"], live["ticker"]])).reset_index(drop=True)
        live = pd.concat([live.reset_index(drop=True), feats.drop(columns=[c for c in feats.columns if c in live.columns])], axis=1)
        trades = pipeline.trades_for(prices, panel, signals)
        if len(trades) >= 100:
            model = setup_model.fit_final(trades)
            live = setup_model.add_setup_dummies(live)
            live["prob_win"] = model.predict_proba(live[setup_model.feature_columns(live)])[:, 1]
        cols = ["date", "ticker", "setup", "entry", "stop", "risk_pct", "level"] + (["prob_win"] if "prob_win" in live else []) + ["base_count", "rs_rank", "mkt_ok"]
        print(f"\nSetups that fired in the last {a.recent} days (entry = close, stop per setup; prob_win = P(trade makes >= 1R)):")
        print(live[cols].sort_values(cols[7] if "prob_win" in live else "date", ascending=False).to_string(index=False))
    else:
        print(f"\nNo setups fired in the last {a.recent} days.")

    # ---- primed watchlist: passing the filter, not yet broken out
    model = primed_model.fit_final(panel)
    cands = today[today["passes"]].dropna(subset=ML_FEATURES).copy()
    if len(cands):
        cands["prob_primed"] = model.predict_proba(cands[ML_FEATURES])[:, 1]
        if a.fundamentals:
            from mlalgo.fundamentals import fetch_fundamentals, paper_score, theme_strength
            fund = fetch_fundamentals(list(today.index))
            today_f = today.join(fund)
            cands = cands.join(fund)
            cands["theme_rs"] = theme_strength(today_f["rs_rank"], today_f["industry"]).reindex(cands.index)
            cands = cands[cands["market_cap"].isna() | (cands["market_cap"] >= 300e6)]
            cands["paper_score"] = paper_score(cands)
        cands = cands.sort_values("prob_primed", ascending=False)
        show = WATCH + (["industry", "theme_rs", "market_cap", "fcf_yield", "book_to_market", "roa", "overinvesting", "paper_score"] if a.fundamentals else [])
        print(f"\nPrimed watchlist (P = hits +{a.target:.0%} before -{a.stop:.0%} within {a.horizon} days):")
        print(cands[show].head(a.top))
        if a.out:
            cands[show].to_csv(a.out)
            print(f"saved {a.out}")
    else:
        print("\nNo stocks pass the filters today.")

    if a.evaluate:
        prob = primed_model.walk_forward(panel, horizon=a.horizon)
        print("\nPrimed model walk-forward evaluation:")
        print(primed_model.evaluate(panel, prob))


if __name__ == "__main__":
    main()
