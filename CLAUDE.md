# ml-algo: working notes for Claude

## Goal
Find stock-trading strategies (screen -> chart setup -> entry -> exit) that work on **real data**,
using ML to test many variations honestly. The user trades breakout / momentum setups.

## Rules
- **Never backtest on synthetic data.** Random-walk data is allowed only inside unit tests that
  check mechanics (lookahead, fills). Don't report numbers from synthetic data.
- Real data comes from Yahoo via GitHub Actions (`.github/workflows/research.yml`); this sandbox
  can't reach Yahoo. Pushing changes under `mlalgo/`, `research.py`, `requirements.txt` triggers a
  run (and **cancels any run in progress**, so don't push mid-run unless you mean to).
- Selection on 2006-2017 only (`IS_END` in `mlalgo/research/analyze.py`), judgement on 2018+.
  Never tune anything on out-of-sample results and then report those same results as validation.
- Always compare against the `random_uptrend` baseline with the same exit and filter.

## Research loop (every run must teach us something)
1. Run (push or Actions -> research -> Run workflow). Results land in `results/`.
2. Read `results/report.md` -> "What this run tells us" and "Next steps", plus `results/history.csv`.
3. Pick the top next step, change the code, add or adjust tests, push, repeat.
4. Record what was learned and decided in `results/LOG.md` (newest first): hypothesis, change,
   result, decision. Don't repeat experiments that are already logged.

## Layout
- `mlalgo/research/entries.py` entry setups (add new ones to `ENTRIES`)
- `mlalgo/research/engine.py` numba exit simulator (`EXITS`) and pattern kernels
- `mlalgo/research/analyze.py` leaderboard, baseline, ML, rules, portfolio
- `mlalgo/research/insights.py` findings / next steps / history
- `scan.py`, `strategy.py` user-facing daily scan and playbook backtest
- Tests: `python -m pytest -q`

## Known findings (update as runs come in; details in results/LOG.md)
- Episodic pivots (gap >= 8-10% on 3x volume) are the most consistent edge vs random entries,
  robust across all tested variants (gap 5-15%, volume 2-5x).
- Ranking same-day signals by RS is worth ~16 CAGR points vs random order (run 3).
- Superperformer model (predict +40% in 3 months, clean: before -20%) ranks stocks well (top decile
  4x base rate, AUC 0.83). Volatility (ADR) is its main driver. Stock selection is most of the edge.
- SURVIVORSHIP IS LARGE: S&P 500 names traded on all dates 47% CAGR vs only after joining the index
  20% (run 12). Always report point-in-time results; treat all-dates numbers as inflated.
- Adaptive sizing (x0.5 / x1.5 by last 20 closed trades) improved risk-adjusted returns every time.
- Next-day / 3-day / 1-week direction from daily data is a coin flip (AUC 0.51-0.52, run 16);
  what little edge exists is market-wide (SPY, VIX, breadth), not chart features.
- Qullamaggie's breakout with his fast 10/20-SMA exits loses on daily bars (run 15); his scan and
  setups work with longer exits (sma50, +20/-10).
- Select strategies by in-sample expectancy (avgR, n >= 200), not t-stat (run 4).
- Industry-group ("theme") RS did not help as a filter (run 4). Honest MTM drawdowns of pooled
  portfolios are ~-50%: a portfolio must be judged on drawdown, not just CAGR.
- Wikipedia no longer lists removed S&P 500 members; survivorship bias is a standing caveat.
- Stock selection matters as much as the entry: rs80_early (RS top 20% + 1st/2nd staircase) lifts even random entries.
- SPY-above-EMAs market filter adds nothing. Exit on a close below the 50 SMA is the most robust.
- ML must predict R (not win/loss); a win/loss classifier just learns stop width.
- Hit rate is set by the bracket geometry (run 17): +5/-10 hits 72% but break-even is 67%. Return per
  month held is ~flat across brackets; wider stops (+20/-15, +30/-15) cut portfolio drawdown.
- The goal model's picks hit +20/-10 far more often when VIX is 20-30 (43% IS and OOS) than when VIX < 20
  (~30%): buy the fear, not the calm. Holds point-in-time (run 18), but a VIX>=20 filter only halves the
  trades at the same CAGR; use VIX for sizing, not as a filter.
- Goal model with run-16 features, top 10%, +20/-10, point-in-time S&P 500: 21% CAGR / -30% DD vs SPY
  14.5% / -34% (run 18). The original-feature model only made 12% point-in-time.
