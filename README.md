# ml-algo

A small, honest starting point for machine-learning stock trading research:
daily prices → features → walk-forward model → backtest with trading costs.

## Scanner: universe → filter → chart structure → "primed?"

```bash
python scan.py --universe universes/sample.txt               # today's ranked watchlist
python scan.py --universe universes/sample.txt --evaluate    # does it actually work? (walk-forward)
python scan.py --tickers NVDA,AAPL,META --target 0.15 --stop 0.07 --horizon 30
python scan.py --csv-dir prices/                             # folder of TICKER.csv files
python scan.py --synthetic --evaluate                        # offline pipeline check
```

**Stage 1: filter the universe** (`mlalgo/universe.py`, all thresholds are CLI flags)

| Filter | Default |
|---|---|
| Price | ≥ $10 |
| Liquidity | 50-day average $ volume ≥ $20M |
| Trend template | close > SMA50 > SMA150 > SMA200, with SMA200 rising |
| Near highs | within 25% of the 52-week high |
| Off lows | ≥ 30% above the 52-week low |
| Relative strength | top 30% of the universe (weighted 3/6/12-month return) |

The scan prints how many stocks survive each filter.

**Stage 2: chart structure** (`mlalgo/structure.py`). For each candidate it measures the "tight base near highs" setup:

- **Volatility contraction (VCP):** the last 60 days are split into three 20-day legs. It checks whether each pullback is smaller than the one before (`contraction_ratio`, `contracting`).
- **Tightness:** the 10-day price range, plus 10-day ATR divided by 50-day ATR (`tight_10`, `atr_ratio`). ATR is average true range, a standard daily volatility measure.
- **Volume dry-up:** 10-day volume divided by 50-day volume (`vol_dryup`). It also compares volume on up days with volume on down days (`updown_vol_50`).
- **Higher lows**, base depth, and distance to the pivot (the top of the base).
- `setup_score`: a transparent 0–1 rule-based score showing what fraction of these "primed" conditions are met.

**Stage 3: ML** (`mlalgo/labels.py`, `mlalgo/primed_model.py`). "It went" is defined with a triple barrier: from the close on the signal day, did the stock hit `+target` before `-stop` within `horizon` days? A gradient-boosting model is trained on all filtered candidates from all stocks to predict that outcome from the structure features. It outputs `prob_primed` for today's candidates.

`--evaluate` runs this walk-forward with an embargo period, so training labels never overlap test dates. It compares three groups: all candidates, the top 5 per day by rule score, and the top 5 per day by ML probability. If the top picks don't beat "all candidates" on hit rate and average trade return, the structure signal isn't adding anything.

Caveats: a ticker list of *today's* index members has survivorship bias (it leaves out stocks that later failed or were dropped). Stop fills assume no gaps through the stop. Daily bars can't tell whether the stop or the target was hit first on the same day; this code counts that as a stop.

## Single-ticker model

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
