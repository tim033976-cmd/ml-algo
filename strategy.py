"""Backtest the setups + trade management plan, and test each trading "rule" against the data.

Examples:
    python strategy.py --universe universes/sample.txt
    python strategy.py --universe universes/sample.txt --require-market --ml
    python strategy.py --tickers NVDA,AMD,MU,PANW --setups breakout,retest --target-r 3
"""
import argparse

import numpy as np
import pandas as pd

from mlalgo import pipeline, setup_model
from mlalgo.setups import SETUPS, SetupConfig
from mlalgo.trade_sim import ExitConfig, trade_stats
from mlalgo.universe import PRESETS

# (name, column, bins, labels): each tests a claim from the playbook / paper
CLAIMS = [
    ("Market above 8/21/50 EMA (SPY)", "mkt_ok", [-0.5, 0.5, 1.5], ["no", "yes"]),
    ("Staircase number (1st/2nd best?)", "base_count", [-0.5, 0.5, 2.5, np.inf], ["0", "1-2", "3+"]),
    ("Pullback volume vs 50d avg (quiet = good?)", "down_vol_ratio_10", [-np.inf, 0.8, 1.2, np.inf], ["<0.8", "0.8-1.2", ">1.2"]),
    ("Volatility contracting (ATR10/ATR50)", "atr_ratio", [-np.inf, 0.8, 1.0, np.inf], ["<0.8", "0.8-1.0", ">1.0"]),
    ("Relative strength rank", "rs_rank", [0, 0.85, 0.95, 1.0], ["70-85%", "85-95%", "95%+"]),
    ("Extension from 8 EMA (ADRs)", "ext_ema8_adr", [-np.inf, 1, 2, np.inf], ["<1", "1-2", ">2"]),
    ("Position in 12m range (paper: low = better)", "range_pos_12m", [-0.01, 0.5, 0.85, 1.01], ["<50%", "50-85%", ">85%"]),
    ("Rates rising (paper: headwind)", "rates_rising", [-0.5, 0.5, 1.5], ["no", "yes"]),
]


def claims_table(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, col, bins, labels in CLAIMS:
        if col not in trades or trades[col].isna().all():
            continue
        groups = pd.cut(trades[col], bins=bins, labels=labels)
        for label, g in trades.groupby(groups, observed=True):
            s = trade_stats(g)
            rows.append({"claim": name, "bucket": label, "trades": int(s["trades"]), "win_rate": s.get("win_rate"),
                         "avg_R": s.get("avg_R"), "profit_factor": s.get("profit_factor")})
    return pd.DataFrame(rows).set_index(["claim", "bucket"])


def main() -> None:
    p = argparse.ArgumentParser()
    pipeline.add_source_args(p)
    p.add_argument("--filter", choices=list(PRESETS), default="momentum")
    p.add_argument("--setups", default=",".join(SETUPS))
    p.add_argument("--target-r", type=float, default=2.0, help="first trim target in R multiples")
    p.add_argument("--max-risk", type=float, default=0.10)
    p.add_argument("--require-market", action="store_true", help="only take signals when SPY > 8/21/50 EMA")
    p.add_argument("--ml", action="store_true", help="walk-forward ML filter on the signals")
    p.add_argument("--out", help="save all trades to CSV")
    a = p.parse_args()

    prices, market = pipeline.load(a)
    cfg = PRESETS[a.filter]
    panel = pipeline.build(prices, market, cfg)
    which = tuple(s.strip() for s in a.setups.split(","))
    signals = pipeline.signals_for(prices, panel, SetupConfig(max_risk=a.max_risk), which, a.require_market)
    trades = pipeline.trades_for(prices, panel, signals, ExitConfig(target_r=a.target_r))
    if trades.empty:
        print("No trades. Loosen filters or add more tickers.")
        return

    pd.set_option("display.float_format", "{:.3f}".format)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)
    print(f"\n{len(prices)} tickers, {trades['entry_date'].min().date()} -> {trades['exit_date'].max().date()}, "
          f"filter={a.filter}, first target={a.target_r}R, market filter={'on' if a.require_market else 'off'}")

    by_setup = {s: trade_stats(g) for s, g in trades.groupby("setup")}
    by_setup["ALL"] = trade_stats(trades)
    print("\nSetup performance (R = multiples of initial risk; trims at target / 8 EMA / 21 EMA / 50 EMA):")
    print(pd.DataFrame(by_setup))
    print("\nExit reasons:")
    print(trades["exit_reason"].value_counts(normalize=True).rename("share").to_frame().T)

    print("\nDo the rules hold up? (all setups pooled)")
    print(claims_table(trades))

    if a.ml:
        prob = setup_model.walk_forward(trades)
        print("\nML filter, out-of-sample (trained only on trades closed before each quarter):")
        print(setup_model.evaluate(trades, prob))

    if a.out:
        trades.to_csv(a.out, index=False)
        print(f"\nsaved {len(trades)} trades to {a.out}")


if __name__ == "__main__":
    main()
