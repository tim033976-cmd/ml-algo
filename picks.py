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
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from mlalgo.research import analyze as A
from mlalgo.research import data as D
from mlalgo.research.entries import all_signals, bars
from mlalgo.research.run import cross_section, group_frames, market_frame, superperformer_sample
from mlalgo.structure import ML_FEATURES, setup_score, structure_features

CAL_START = pd.Timestamp("2023-01-01")   # calibration years: model trained before, checked on these


def trim_incomplete(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Yahoo returns a partial bar for today while the US market is open. Drop it until the
    close (~20:00 UTC) so features and signals only use finished daily bars."""
    now = datetime.now(timezone.utc)
    today = pd.Timestamp(now.date())
    if now.hour < 21:
        return {t: (df.iloc[:-1] if len(df) and df.index[-1] >= today else df) for t, df in dfs.items()}
    return dfs


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
    prices, market = trim_incomplete(prices), trim_incomplete(market)
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
        # 1) honest probabilities: train on data before CAL_START, map scores to the hit rates
        #    actually seen on CAL_START+ (isotonic), so the % shown is out-of-sample, not in-sample
        early = known[known["label_end"] < CAL_START]
        early = early.sample(min(300_000, len(early)), random_state=0)
        holdout = known[known["date"] >= CAL_START]
        m_early = A._super_model().fit(*A._xy(early, g))
        h_score = m_early.predict_proba(A._xy(holdout)[0])[:, 1]
        h_y = A._label(holdout, g)
        # binned calibration: 20 equal-count bins of held-out scores -> their actual hit rate
        edges = np.unique(np.quantile(h_score, np.linspace(0, 1, 21)))
        bin_rate = pd.Series(h_y).groupby(np.clip(np.searchsorted(edges, h_score, side="right") - 1, 0, len(edges) - 2)).mean()
        calibrate = lambda sc: bin_rate.reindex(np.clip(np.searchsorted(edges, sc, side="right") - 1, 0, len(edges) - 2)).to_numpy()
        top = h_score >= np.quantile(h_score, 0.9)
        latest.attrs[f"{g}_base"] = float(h_y.mean())
        latest.attrs[f"{g}_top10_hit"] = float(h_y[top].mean())
        latest.attrs[f"{g}_top10_ret"] = float(holdout[f"{g}_ret"].to_numpy()[top].mean())
        # 2) final model on all history scores today; the isotonic map turns scores into honest %
        train = known.sample(min(300_000, len(known)), random_state=0)
        model = A._super_model().fit(*A._xy(train, g))
        raw = model.predict_proba(A._xy(latest)[0])[:, 1]
        latest[f"p_{g}"] = calibrate(m_early.predict_proba(A._xy(latest)[0])[:, 1])  # honest % (same model as the bins)
        latest[f"score_{g}"] = raw                                                   # final model, for ranking ties

    liquid = (latest["close"] >= 5) & (latest["dollar_vol_50"] >= 5e6)
    latest = latest[liquid].copy()
    latest["stop_-10%"] = latest["close"] * 0.90
    latest["target_+10%"] = latest["close"] * 1.10
    latest["target_+20%"] = latest["close"] * 1.20
    if "sector" in universe:
        latest["sector"] = latest["ticker"].map(universe.drop_duplicates("ticker").set_index("ticker")["sector"])
    latest["setups_last_3_days"] = latest["setups_last_3_days"].fillna("")
    # momentum-style leaders: strong RS, near highs, above the 50-day (the user's trading style)
    leader = (latest["rs_rank"] >= 0.70) & (latest["dist_52w_high"] >= -0.25) & (latest["dist_sma50"] > 0)
    rank_cols = ["p_b20", "score_b20"]
    picks = latest.sort_values(rank_cols, ascending=False).head(a.top)
    leaders = latest[leader].sort_values(rank_cols, ascending=False).head(a.top)
    cols = ["ticker", "close", "p_b20", "p_b10", "stop_-10%", "target_+10%", "target_+20%", "adr_pct", "rs_rank",
            "dist_52w_high", "base_count", "setups_last_3_days"] + (["sector"] if "sector" in latest else [])
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pd.concat([picks[cols].assign(list="all"), leaders[cols].assign(list="leaders")]).to_csv(out / "today_picks.csv", index=False)

    def table(df):
        show = df[cols].copy()
        for c in ("p_b20", "p_b10", "rs_rank", "dist_52w_high", "adr_pct"):
            show[c] = (show[c] * 100).round(1)
        return show.to_markdown(index=False, floatfmt=".2f")

    lines = [
        f"# Daily picks — {asof.date()}",
        "",
        f"Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.",
        f"Model trained on {len(sample):,} past snapshots of {len(prices)} stocks. Probabilities are in %.",
        "",
        f"**Probabilities are calibrated out-of-sample** (model trained before {CAL_START.year}, checked on "
        f"{CAL_START.year}-today). On those held-out years: all stocks hit +20% before -10% "
        f"{latest.attrs['b20_base']:.0%} of the time; the model's top 10% {latest.attrs['b20_top10_hit']:.0%} "
        f"(avg {latest.attrs['b20_top10_ret']:+.1%} net per trade; break-even ~33%). +10% before -10%: "
        f"{latest.attrs['b10_base']:.0%} vs {latest.attrs['b10_top10_hit']:.0%} (break-even ~50%).",
        "",
        "Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired "
        "recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.",
        "",
        "## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day",
        "",
        table(leaders) if len(leaders) else "_No leaders today._",
        "",
        "## All stocks (the model's overall favourites; often beaten-down, volatile names)",
        "",
        table(picks),
    ]
    (out / "today_picks.md").write_text("\n".join(lines))
    print(f"[picks] wrote {out / 'today_picks.md'} ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
