# ml-algo

A small, honest starting point for machine-learning stock trading research:
daily prices → features → walk-forward model → backtest with trading costs.

## Daily picks (your goal: +20% / +10% before -10%)

**Actions → picks → Run workflow** builds `results/today_picks.md`: every stock ranked by the model's
probability of hitting +20% (and +10%) before a -10% loss within 63 trading days, with stop / target
prices and any setups that fired in the last 3 days. Out-of-sample (2018+) the model's top 10% hit
+20% first ~38-39% of the time vs a ~33% break-even (all stocks: 23%). Paper trade before using it.

## Strategy research on real data (runs on GitHub Actions)

`research.py` tests ~20 published breakout entries (Turtle/Donchian, 52-week high, O'Neil/Darvas bases,
Minervini VCP, Qullamaggie flags and episodic pivots, high tight flag, pocket pivot, Weinstein stage 2,
plus your 8/21 retest, multi-touch breakout and undercut) against **a random-entry baseline**, each with
9 exit plans and 6 filters, on the S&P 500/400/600 plus former S&P 500 members since 2005.

* Strategies are **selected on 2006-2017** and **judged on 2018-today**, which they never saw.
* An ML meta-labeling model is trained walk-forward (yearly) to decide which signals to take; permutation
  importance and a shallow decision tree turn it into readable rules, each checked out-of-sample.
* The best candidates run through a portfolio simulation ($100k, 1% risk per trade, max 10 positions) vs SPY.

It runs automatically on GitHub Actions whenever the research code changes (or from the **Actions** tab →
**research** → **Run workflow**). Results are committed to `results/`; start with `results/report.md`.
Locally: `python research.py` (needs internet access to Yahoo; takes ~30-60 min).

## Getting started (no install, in your browser)

1. On the GitHub repo page, switch the branch dropdown to this branch.
2. Click the green **Code** button → **Codespaces** tab → **Create codespace on …**
3. Wait for setup to finish (it installs the Python packages automatically). A terminal opens at the bottom.
4. Try the commands below.

On your own computer, install Python 3.10+ instead, download the code, then run `pip install -r requirements.txt` in its folder.

## The playbook: market → leaders → setup → entry → trim plan

```bash
python strategy.py --universe universes/sample.txt                  # backtest setups + exits, test each rule
python strategy.py --universe universes/sample.txt --require-market --ml
python scan.py --universe universes/sample.txt --fundamentals       # today's signals + watchlist
```

| Step | Rule | Code |
|---|---|---|
| Market | Long when SPY/QQQ are above their 8/21/50 EMAs; reduce size in chop | `mlalgo/market.py`, `--require-market` |
| Leaders | Price > $3, volume > 500k, ADR > 2%, above 8/21/50 EMA, top 30% relative strength (`--filter momentum`) | `mlalgo/universe.py` |
| Setup | Tight base, volume drying up, above the MAs, 1st/2nd staircase step, quiet pullback (not big red candles on rising volume) | `mlalgo/structure.py` |
| Entry: **breakout** | Close through a level rejected ≥ 2 times, ≥ 1.5× volume. Stop = low of day | `mlalgo/setups.py` |
| Entry: **retest** | 8/21 EMA cross → break key level → retest level/8 EMA → close above the prior high. Stop = retest low | `mlalgo/setups.py` |
| Entry: **undercut & rally** | Dip below the base low, then reclaim it. Stop = undercut low | `mlalgo/setups.py` |
| Management | Sell 1/4 at +2R and move the stop to breakeven. Then sell 1/4 on a close below the 8 EMA, 1/4 below the 21 EMA, and the rest below the 50 EMA | `mlalgo/trade_sim.py` |

`strategy.py` reports win rate, average R (profit in multiples of initial risk), profit factor and share of 5R+ winners for each setup. It then prints a **"do the rules hold up?"** table that splits trades by market regime, staircase number, pullback volume, volatility contraction, RS rank, extension from the 8 EMA, 12-month range position and the rates regime. Every rule gets tested instead of trusted. `--ml` trains a model on the setup signals walk-forward, using only trades that had already closed, and checks whether its top third beats taking every signal.

Limits of daily data: entries are at the signal day's close (not 5-minute "sniper" entries), a gap through a stop fills at the open, and if the stop and target fall inside the same bar the stop is assumed to hit first. The default cost is 0.1% per side.

**Multibagger paper factors** (Yartseva 2025, `mlalgo/fundamentals.py`, `--fundamentals`): FCF yield, book-to-market, ROA, small size, and a flag for asset growth outpacing EBITDA growth. These are combined into `paper_score`, with an industry-level relative strength as the theme gauge. Yahoo only provides *current* fundamentals, so these columns rank today's candidates and are never used in backtests. Note that the paper studies a 1-year horizon and found that buying near 12-month *lows* after a decline worked best for 10-baggers. That's the opposite of the momentum playbook, so the claims table checks `range_pos_12m` on your own trades.

## Scanner: universe → filter → chart structure → "primed?"

```bash
python scan.py --universe universes/sample.txt               # today's ranked watchlist
python scan.py --universe universes/sample.txt --evaluate    # does it actually work? (walk-forward)
python scan.py --csv-dir prices/                             # folder of TICKER.csv files
```

**Stage 1: filter the universe** (`mlalgo/universe.py`). There are two presets: `--filter momentum` (the default, described above) and `--filter trend_template`:

| Filter | trend_template |
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
pytest                                     # leakage / correctness tests
```

## How it works

| File | What it does |
|---|---|
| `mlalgo/data.py` | Loads OHLCV from Yahoo or a CSV (random-walk data is used only inside unit tests) |
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
6. **Sanity check.** The unit tests check for lookahead by changing future prices and confirming that past signals don't change.

Realistic expectations: daily direction prediction on liquid large caps typically gives an AUC of about 0.50–0.53. A real edge usually comes from better data (cross-sectional ranking across many stocks, fundamentals, alternative data) rather than fancier models.

## Ideas for next steps

- Cross-sectional model: rank many tickers each day and go long the top decile.
- Predict volatility-adjusted or multi-day returns (`--horizon 5`).
- Add market regime features (VIX, rates, sector ETFs).
- Paper trade before using real money.

*Research code, not financial advice.*
