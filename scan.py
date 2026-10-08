"""Universe -> filter -> chart-structure scoring -> ML "primed" probability.

Examples:
    python scan.py --universe universes/sample.txt                # today's ranked watchlist
    python scan.py --universe universes/sample.txt --evaluate     # walk-forward test of the approach
    python scan.py --tickers NVDA,AAPL,MSFT,META --target 0.15 --stop 0.07 --horizon 30
    python scan.py --synthetic --evaluate                         # offline pipeline check
"""
import argparse

import pandas as pd

from mlalgo import universe
from mlalgo.labels import label_panel
from mlalgo.primed_model import evaluate, fit_final, walk_forward
from mlalgo.structure import ML_FEATURES, build_panel
from mlalgo.universe import FILTER_COLUMNS, FilterConfig, apply_filters

SHOW = ["close", "setup_score", "prob_primed", "dist_to_pivot", "contraction_ratio", "tight_10",
        "atr_ratio", "vol_dryup", "rs_rank", "dist_52w_high"]


def main() -> None:
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--universe", help="file with one ticker per line")
    src.add_argument("--tickers", help="comma-separated tickers")
    src.add_argument("--csv-dir", help="folder of <TICKER>.csv files")
    src.add_argument("--synthetic", action="store_true")
    p.add_argument("--start", default="2010-01-01")
    p.add_argument("--target", type=float, default=0.10, help="profit target (0.10 = +10%%)")
    p.add_argument("--stop", type=float, default=0.05, help="stop loss (0.05 = -5%%)")
    p.add_argument("--horizon", type=int, default=20, help="max trading days to hold")
    p.add_argument("--min-price", type=float, default=10.0)
    p.add_argument("--min-dollar-volume", type=float, default=20e6)
    p.add_argument("--min-rs", type=float, default=0.70)
    p.add_argument("--no-trend", action="store_true", help="skip the trend-template filter")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--evaluate", action="store_true", help="run the walk-forward evaluation")
    p.add_argument("--out", help="save today's scan to CSV")
    a = p.parse_args()

    if a.synthetic:
        prices = universe.synthetic_universe()
        cfg = FilterConfig(min_price=0, min_dollar_volume=0, min_rs_rank=a.min_rs, require_trend=not a.no_trend)
    else:
        if a.csv_dir:
            prices = universe.load_csv_dir(a.csv_dir)
        else:
            tickers = universe.read_tickers(a.universe) if a.universe else [t.strip().upper() for t in a.tickers.split(",")]
            prices = universe.load_yahoo_many(tickers, start=a.start)
        cfg = FilterConfig(a.min_price, a.min_dollar_volume, min_rs_rank=a.min_rs, require_trend=not a.no_trend)

    panel = build_panel(prices)
    panel = apply_filters(panel, cfg)
    panel = panel.join(label_panel(prices, target=a.target, stop=a.stop, horizon=a.horizon))
    pd.set_option("display.float_format", "{:.3f}".format)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)

    # ---- Stage 1: today's funnel
    last = panel.index.get_level_values("date").max()
    today = panel.xs(last, level="date")
    print(f"\nUniverse: {len(prices)} tickers, latest date {last.date()}")
    remaining = pd.Series(True, index=today.index)
    for col in FILTER_COLUMNS:
        remaining &= today[col]
        print(f"  after {col[2:]:<10} {remaining.sum():>5}")

    # ---- Stage 2: score today's candidates
    model = fit_final(panel)
    cands = today[today["passes"]].dropna(subset=ML_FEATURES).copy()
    if len(cands):
        cands["prob_primed"] = model.predict_proba(cands[ML_FEATURES])[:, 1]
        cands = cands.sort_values("prob_primed", ascending=False)
        print(f"\nPrimed candidates (P = hits +{a.target:.0%} before -{a.stop:.0%} within {a.horizon} days):")
        print(cands[SHOW].head(a.top))
        if a.out:
            cands[SHOW].to_csv(a.out)
            print(f"saved {a.out}")
    else:
        print("\nNo stocks pass the filters today.")

    # ---- Does it actually work? (out-of-sample)
    if a.evaluate:
        prob = walk_forward(panel, horizon=a.horizon)
        print(f"\nWalk-forward evaluation {prob.index.get_level_values('date').min().date()} -> "
              f"{prob.index.get_level_values('date').max().date()}:")
        print(evaluate(panel, prob))


if __name__ == "__main__":
    main()
