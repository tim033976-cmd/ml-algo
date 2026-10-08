# ml-algo

A small, honest starting point for machine-learning stock trading research:
daily prices → features → walk-forward model → backtest with trading costs.

## Quick start

```bash
pip install -r requirements.txt
python run.py --ticker SPY                 # download from Yahoo Finance and run
python run.py --ticker AAPL --model logreg --threshold 0.53 --cost-bps 10
python run.py --csv my_prices.csv          # your own data (date, open, high, low, close, volume)
python run.py --synthetic                  # offline sanity check on a random walk
pytest                                     # leakage / correctness tests
```

## How it works

| File | What it does |
|---|---|
| `mlalgo/data.py` | Loads OHLCV from Yahoo, a CSV, or synthetic random-walk data |
| `mlalgo/features.py` | Momentum, volatility, moving-average distance, RSI, volume, etc. Target = is tomorrow's return positive? |
| `mlalgo/model.py` | **Walk-forward** training: refit every quarter on past data only, predict the next block |
| `mlalgo/backtest.py` | Converts probabilities to positions, charges costs on every trade, and reports CAGR, Sharpe and max drawdown against buy & hold |
| `run.py` | Command-line tool that ties it all together |

## Things that will fool you (and how this repo guards against them)

1. **Lookahead bias.** Features on day *t* use only data up to the close of *t*. `tests/test_features_have_no_lookahead` changes future prices and checks that past features stay the same.
2. **Random train/test splits.** Never shuffle time series. All predictions here are out-of-sample walk-forward, with an embargo gap between the training labels and the test data.
3. **Ignoring costs.** A strategy that trades daily can look great before costs and lose money after them. Use `--cost-bps` to test this.
4. **Overfitting by tuning.** Every threshold or feature you try on the same history makes the backtest more optimistic. Keep a final holdout period you don't look at until the end.
5. **Accuracy isn't profit.** 52% accuracy can lose money. Compare Sharpe and drawdown against buy & hold.
6. **Sanity check.** `--synthetic` runs on pure noise, where no real edge exists. If you ever see a strong result there, you have a bug.

Realistic expectations: daily direction prediction on liquid large caps typically gives an AUC of about 0.50–0.53. A real edge usually comes from better data (cross-sectional ranking across many stocks, fundamentals, alternative data) rather than fancier models.

## Ideas for next steps

- Cross-sectional model: rank many tickers each day and go long the top decile.
- Predict volatility-adjusted or multi-day returns (`--horizon 5`).
- Add market regime features (VIX, rates, sector ETFs).
- Paper trade before using real money.

*Research code, not financial advice.*
