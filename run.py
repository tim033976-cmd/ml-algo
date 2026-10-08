"""End-to-end: data -> features -> walk-forward model -> backtest.

Examples:
    python run.py --ticker SPY
    python run.py --ticker AAPL --model logreg --threshold 0.53 --cost-bps 10
    python run.py --csv my_prices.csv
"""
import argparse

import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score

from mlalgo import data
from mlalgo.backtest import backtest, positions_from_probs, report
from mlalgo.features import make_dataset
from mlalgo.model import walk_forward_predict


def main() -> None:
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group()
    src.add_argument("--ticker", default="SPY")
    src.add_argument("--csv")
    p.add_argument("--start", default="2005-01-01")
    p.add_argument("--model", choices=["gbm", "logreg"], default="gbm")
    p.add_argument("--horizon", type=int, default=1)
    p.add_argument("--threshold", type=float, default=0.52)
    p.add_argument("--allow-short", action="store_true")
    p.add_argument("--cost-bps", type=float, default=5.0)
    p.add_argument("--out", help="optional path to save daily results CSV")
    a = p.parse_args()

    if a.csv:
        df, name = data.load_csv(a.csv), a.csv
    else:
        df, name = data.load_yahoo(a.ticker, start=a.start), a.ticker

    X, y, fwd = make_dataset(df, horizon=a.horizon)
    prob = walk_forward_predict(X, y, kind=a.model, embargo=a.horizon)
    y_oos = y.reindex(prob.index)

    # For multi-day horizons, trade the 1-day return each day so P&L isn't double-counted.
    daily_fwd = (df["close"].shift(-1) / df["close"] - 1).reindex(prob.index)
    pos = positions_from_probs(prob, a.threshold, a.allow_short)
    bt = backtest(pos, daily_fwd, a.cost_bps)

    pd.set_option("display.float_format", "{:.4f}".format)
    print(f"\n{name}: {len(df)} days, out-of-sample {prob.index[0].date()} -> {prob.index[-1].date()}")
    print(f"OOS accuracy {accuracy_score(y_oos, prob > 0.5):.4f}  "
          f"(base rate up-days {y_oos.mean():.4f}),  AUC {roc_auc_score(y_oos, prob):.4f}\n")
    print(report(bt))
    if a.out:
        bt.assign(prob_up=prob).to_csv(a.out)
        print(f"\nsaved {a.out}")


if __name__ == "__main__":
    main()
