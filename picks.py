"""Daily picks for the user's goal: which stocks have the best odds of +20% (or +10%) before -10%?

Trains the goal models on all history (every stock every 10 days, labels only where the 63-day
window has closed), then scores every stock on the latest close. Writes results/today_picks.md.

    python picks.py                 # downloads fresh prices (needs internet: run on GitHub Actions)
    python picks.py --top 40
"""
import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo.research import analyze as A
from mlalgo.research import data as D
from mlalgo.research.entries import all_signals, bars
from mlalgo.research.run import cross_section, group_frames, market_frame, superperformer_sample
from mlalgo.structure import ML_FEATURES, setup_score, structure_features


def _worker(args):
    ticker, df, rs, grp = args
    feats = structure_features(df)
    feats["setup_score"] = setup_score(feats)
    sample = superperformer_sample(ticker, df, feats, rs, grp)
    last = feats.iloc[[-1]][[c for c in ML_FEATURES + ["dollar_vol_50", "avg_vol_50"] if c in feats]].copy()
    last.insert(0, "date", df.index[-1])
    last.insert(0, "ticker", ticker)
    last["close"] = df["close"].iloc[-1]
    last["rs_rank"] = rs.reindex(df.index).iloc[-1]
    for col in ("industry_rs", "industry_rank", "sector_rs"):
        last[col] = grp[col].reindex(df.index).iloc[-1] if grp is not None else np.nan
    try:
        sig = all_signals(df, bars(df), warmup=0)
        today = sig[sig["idx"] >= len(df) - 3]["entry_name"].unique()
        last["setups_last_3_days"] = ", ".join(s for s in today if s != "random_uptrend")
    except Exception:
        last["setups_last_3_days"] = ""
    return sample, last


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cache", default="data_picks")
    p.add_argument("--out", default="results")
    p.add_argument("--start", default="2005-01-01")
    p.add_argument("--top", type=int, default=30)
    p.add_argument("--max-age-days", type=float, default=0.5, help="re-download prices if older than this")
    a = p.parse_args()
    t0 = time.time()

    universe, prices, market = D.load_all(a.cache, a.start, max_age_days=a.max_age_days)
    rank, breadth = cross_section(prices)
    mkt = market_frame(market, breadth)
    grp = group_frames(rank, universe, prices)
    tasks = [(t, df, rank[t], grp.get(t)) for t, df in prices.items()]
    with ProcessPoolExecutor(os.cpu_count() or 1) as ex:
        results = list(ex.map(_worker, tasks, chunksize=10))
    sample = pd.concat([r[0] for r in results if len(r[0])], ignore_index=True)
    latest = pd.concat([r[1] for r in results], ignore_index=True)
    asof = latest["date"].max()
    latest = latest[latest["date"] == asof]  # stocks that traded on the latest day
    m = mkt.reindex(mkt.index.union(pd.DatetimeIndex(sample["date"].unique()).union([asof]))).ffill()
    sample = sample.join(m, on="date")
    latest = latest.join(m, on="date")
    print(f"[picks] {len(prices)} stocks, {len(sample):,} training rows, as of {asof.date()} ({time.time() - t0:.0f}s)")

    for g in ("b20", "b10"):
        known = sample[sample[f"{g}_hit"].notna()]
        train = known.sample(min(300_000, len(known)), random_state=0)
        X, y = A._xy(train, g)
        model = A._super_model().fit(X, y)
        latest[f"p_{g}"] = model.predict_proba(A._xy(latest)[0])[:, 1]
        # historical calibration for context: hit rate of the top 10% of scores in the training data
        tp = model.predict_proba(X)[:, 1]
        latest.attrs[f"{g}_top10_hit"] = float(y[tp >= np.quantile(tp, 0.9)].mean())
        latest.attrs[f"{g}_base"] = float(y.mean())

    liquid = (latest["close"] >= 5) & (latest["dollar_vol_50"] >= 5e6)
    picks = latest[liquid].sort_values("p_b20", ascending=False).head(a.top).copy()
    picks["stop_-10%"] = picks["close"] * 0.90
    picks["target_+10%"] = picks["close"] * 1.10
    picks["target_+20%"] = picks["close"] * 1.20
    if "sector" in universe:
        picks["sector"] = picks["ticker"].map(universe.drop_duplicates("ticker").set_index("ticker")["sector"])
    cols = ["ticker", "close", "p_b20", "p_b10", "stop_-10%", "target_+10%", "target_+20%", "adr_pct", "rs_rank",
            "dist_52w_high", "base_count", "setups_last_3_days"] + (["sector"] if "sector" in picks else [])
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    picks[cols].to_csv(out / "today_picks.csv", index=False)
    show = picks[cols].copy()
    for c in ("p_b20", "p_b10", "rs_rank", "dist_52w_high", "adr_pct"):
        show[c] = (show[c] * 100).round(1)
    lines = [
        f"# Daily picks — {asof.date()}",
        "",
        f"Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.",
        f"Model trained on {len(sample):,} past snapshots of {len(prices)} stocks. Probabilities are in %.",
        "",
        f"Historically (training data): all stocks hit +20% before -10% {latest.attrs['b20_base']:.0%} of the time; "
        f"the model's top 10% {latest.attrs['b20_top10_hit']:.0%}. "
        f"+10% before -10%: {latest.attrs['b10_base']:.0%} vs {latest.attrs['b10_top10_hit']:.0%}. "
        "Out-of-sample (2018+) the top 10% hit +20% first about 38-39% of the time vs a ~33% break-even "
        "(see results/report.md). Training-data rates are optimistic; trust the out-of-sample ones.",
        "",
        "Sorted by p_b20 = model probability of +20% before -10%. `setups_last_3_days` lists setups that fired "
        "(e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.",
        "",
        show.to_markdown(index=False, floatfmt=".2f"),
    ]
    (out / "today_picks.md").write_text("\n".join(lines))
    print(f"[picks] wrote {out / 'today_picks.md'} ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
