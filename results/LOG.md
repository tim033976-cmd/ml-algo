# Research log (newest first)

## Run 16 — 2026-10-09 (commit 00c2b0a): short horizons, concrete data only
- **Short-horizon direction is close to a coin flip.** OOS AUC 0.51-0.52, accuracy 51-52% vs base rates 49-51%: green day 0.514, up 1 day 0.514, **up 3 days 0.520** (best: top 10% up 53.2% vs bottom 10% 45.1%, ~0.6% return spread over 3 days), up 5 days 0.508 (not monotonic, unusable).
- **Chart features add nothing beyond the market.** The market-only model (market + VIX + calendar) matches or beats the full model on every horizon. Top drivers of the 1-week model: SPY 1-day return, breadth, VIX 1-day change, month, VIX 5-day change, VIX/VIX3M. Candle anatomy, gaps/FVGs, round numbers and support/resistance rank at the bottom.
- **They do slightly improve the +20/−10 goal model:** top 1% 42.8% → 44.2% hit (avg +3.7% → +4.2% net), top 2% 40.6 → 41.6%, top 10% 37.4 → 38.3%. Small but consistent: keep them in the goal model.
- **Conclusion:** don't trade next-day / next-week direction from daily charts. Use the new features inside the +20/−10 model, and at most use the 3-day market model to avoid entering on the worst days (entry timing), to be tested.

## Run 16 — planned 2026-10-09: short horizons with concrete data only
User decision: test the probability of a green day / up next day / up over 3 days / up over a week, using **concrete data only**: no VWAP, volume profile or CVD proxies (those need intraday / order-flow data).
- New features (`mlalgo/research/shortterm.py`, all point-in-time, tested): candle anatomy (body, wicks, close location, inside/outside day, NR7, streaks, previous candle), gaps (overnight gap, gap filled, bullish/bearish fair value gaps), relative volume, round-number distance, 20/200 SMA distance, nearest confirmed swing support/resistance, 20-day trend-line slope and residual, completed-week structure (weekly return, close location, higher high / higher low, above the 10-week MA, week-to-date), VIX (level, 1/5-day change, 1-year percentile, VIX/VIX3M), SPY 1/5-day return, calendar.
- Labels: next-day green (close > open), up 1 / 3 / 5 days (close to close).
- Models: all features vs **market-only** (market + VIX + calendar), walk-forward retrained every 2 years. Report AUC, accuracy, top/bottom-decile up-rate, return spread, importance. Expectation: ~52-54% at best; the bar is the natural base rate (~50-53%).
- Also: do these features improve the +20/-10 goal model? (original vs extended, OOS tiers)
- Price cache bumped to v4 to download ^VIX and ^VIX3M.

## Run 15 — 2026-10-08 (commit f522ebc): Qullamaggie replication on daily data
- **His breakout with his exits fails mechanically on daily bars.** qull_breakout + qull_sma10/20: OOS −0.15 to −0.25R per trade (PF 0.64-0.77, win 33-37%), IS similar. Portfolios: **−11% to −14% CAGR, −71% to −76% DD**. With his regime rule: −2% to −7% CAGR. The 60%-run variant is no better.
- **The same breakouts with longer exits are fine:** + bracket +20/−10 → +0.15R OOS (t 6.8; regime +0.19R), + sma50 & regime +0.28R. So his entries/stocks are OK; the fast 10/20-SMA trailing with tight stops is what loses on daily bars.
- **His scan helps EPs a lot, after 2018 only:** ep_gap10 / ep_gap8_hold + qull_scan + sma50: OOS +0.83 to +1.0R (PF 2.3-2.5), but IS only +0.01 to +0.15R. That is period-dependent (2018+ momentum era), so treat it with caution.
- **Regime rule (QQQ > 10/20 SMA)** improves breakouts slightly (+0.04 to +0.10R) and cuts portfolio drawdowns. Best Qull portfolio: scan + setups + regime + sma50 → 18% CAGR, −45% DD; + adaptive sizing 14% / −34%. Not better than the +20/−10 model portfolio (18% / −29% point-in-time).
- **Likely reasons the replication fails:** (1) on daily bars the stop is touched on the entry day in many trades, and we count that as a loss even when the low may have come *before* the entry (conservative); his intraday entry + LOD stop avoids that ambiguity; (2) a tight stop (<= 1 ADR) on volatile names gets hit by normal noise; (3) his discretionary selection (he skips most setups).
- **Next:** measure how many trades are decided by the ambiguous entry-day bar, bound the result (optimistic vs conservative fill), test wider stops (flag low, 2 ADR), and check with 2 years of hourly data which assumption is right.

## Run 15 — planned 2026-10-08: Qullamaggie replication on daily data
User decision: match Qullamaggie's strategy and validate it rather than trust it.
- **Scan:** top 3% performer over 1, 3 or 6 months (per-day percentile, best of the three) with ADR >= 4% (`qull_scan`), plus his regime rule, QQQ above its 10- and 20-day SMAs (`qull_scan_regime`, `qqq_trend`).
- **Entry `qull_breakout` / `qull_breakout_60`:** setup known at the close (30%/60%+ run, 5-40 day consolidation <= 25% deep, higher lows, holding the 10/20 SMA, not yet broken out). A buy-stop above the pivot the next day fills at max(open, trigger). Stop = the tighter of the 3-day low and 1 ADR below the fill. Features use data up to the setup day only. A same-day stop touch counts as stopped (conservative). EPs are kept as his second setup.
- **Exits:** his (sell 1/3 on day 5, breakeven stop, trail the 10/20 SMA), plus sma50 and the user's +20/-10 bracket.
- **Portfolios:** scan + setups with each exit, with/without the regime rule, + adaptive sizing, point-in-time S&P 500.
- **Forward test:** picks.py now logs the top 10 of each list daily and scores them (+20/+10 vs -10, 63 days) as prices arrive: results/forward_test.md.
- Intraday (hourly, 2 years) cross-check of daily fills is planned after this run.

## Run 13 — 2026-10-08 (commit 749e984): the user's goal
Out-of-sample 2018+, every stock every 10 days (~280k rows), entry at the close, 63-day limit, 0.2% round-trip costs:
- **+20% before −10% (break-even ~33%):** all stocks 23%. The model's top 10% hit it **38%**, avg **+2.6% net per trade**. **Point-in-time S&P 500 top 10%: 39%, +3.9% per trade** (n=4,264), so this survives the survivorship check. Monotonic across deciles; the top decile is a little overconfident (predicted 45%, actual 38%).
- **But the stop rate also rises with the score** (top decile 53% stopped vs 33% in the bottom decile): the model mostly picks volatile stocks, which hit both levels more often. The edge is that the target wins more of those races, not that the stop is avoided.
- **+10% before −10% (break-even ~50%):** weak. All stocks 49%, top 10% 56%, +1.5% per trade. PIT S&P 500 58%, +2.3%.
- **Bottom deciles are also slightly positive** (bull-market drift 2018-2026): the edge over an average stock is ~+1.3% per trade for b20.
- **Portfolios:** b20 model top 10% (no setup needed): **22% CAGR, −41% DD**; point-in-time S&P 500 only: **18%, −29%** (SPY 14.6%, −34%). b10: 15% / −34%; PIT 10% / −26%. Requiring a setup on top of the model *hurt* b20 (10% CAGR) but helped b10 (17%).
- **Conclusion:** the goal is reachable at modest odds. The best honest version is ~39% chance of +20% before −10% (vs 33% break-even) on point-in-time S&P 500 stocks, worth ~+3-4% per trade and ~18% a year with a lower drawdown than SPY.

## Run 14 — 2026-10-08 (commit e7af2f7): confidence tiers + first daily picks
- **More confidence = better odds** (OOS 2018+). +20% before −10%: top 10% 38%, top 5% 39%, top 2% 41%, top 1% 42%; point-in-time S&P 500: 39 / 41 / **44 / 44%**, avg net +3.9% → +4.7% per trade. +10% before −10%: top 10% 56% → top 1% 63% (PIT 58 → 65%).
- **First picks run** exposed three problems: (1) it ran at ~10:20 ET, so today's bar was partial; (2) final-model probabilities were in-sample-overconfident (~55-60% vs ~40-44% real); (3) all 30 picks were beaten-down names (35-60% below highs, low RS), the model's strongest statistical mode but not the user's momentum style.
- **Fixes:** drop today's bar before 21:00 UTC (tested); probabilities calibrated on held-out 2023+ years with 20 equal-count bins (isotonic gave 0/100% extremes); a second list of **leaders** (RS >= 70th pct, within 25% of the 52w high, above the 50-day) shown first.

## Run 14 — planned 2026-10-08
- Confidence tiers: do the top 5/2/1% have better odds than the top 10%?
- `picks.py` + `picks.yml`: daily list of stocks ranked by P(+20% before −10%), with stop/targets and any setups that fired in the last 3 days. Scheduled runs fire only from the default branch.

## Run 13 — planned 2026-10-08: the user's goal, +10% / +20% before −10% on the daily chart
User decision: daily chart only (no intraday). Goal: a model that gives a high probability of +10% to +20% before a −10% loss.
- New exits `bracket_10_10` and `bracket_20_10`: fixed −10% stop, +10% / +20% target, 63-day time limit. Gaps fill at the open; target and stop in the same bar count as the stop. The engine matches the label logic exactly (unit test).
- New labels on every stock every 10 days: did it hit +10% (b10) / +20% (b20) before −10%? Plus the net bracket return including timeouts and 0.2% round-trip costs.
- Walk-forward classifiers for each goal. Report by probability decile: predicted vs actual hit rate (calibration), stop rate, avg net return per trade. Break-even ≈ 50% (b10) and 33% (b20) before costs and timeouts.
- The survivorship check is built in: the same tables for S&P 500 names only after they joined the index.
- Portfolios: model top-10% stocks with no setup needed, + adaptive sizing, setups in the top 10%, and point-in-time S&P 500 only.

## Run 10 — 2026-10-08 (commit 54a58fb): idle cash in SPY, bigger risk
- **Top 10 by IS expectancy, 1% risk, idle cash in SPY:** 15.2% CAGR, −34% max DD. SPY: 14.6% / −34%. That is essentially SPY plus a little: it beat SPY in 2019, 2020, 2022 (−8% vs −18%) and 2026, and lagged in 2024 (+16 vs +25) and 2025 (−12 vs +18).
- **2% risk is worse:** 13%, −39%. With 2% risk most positions hit the 20% size cap and cash runs out at ~5 positions, so 10 vs 15 slots made no difference (identical results). More risk per trade doesn't add return here, only drawdown.
- **Without idle cash:** the top 20 by IS expectancy is still the best risk-adjusted (13.8%, −26%).
- **Conclusion:** the mechanical setups give SPY-like returns with different timing. Beating SPY decisively needs something the setups alone don't provide (stock selection / sizing), which is what run 11 tests.

## Run 11 — 2026-10-08 (commit 0c6ddba): superperformer model + adaptive sizing
- **Superperformer model (every stock every 10 days, ~280k OOS rows):** the model's top 10% hit +40% within 3 months **30.4%** of the time vs a 7.1% base rate (4.3x), AUC 0.83, monotonic across deciles. Avg 3-month return: top decile +11.6% vs about +2% overall.
- **What drives it:** ADR% (volatility) by far, then distance above the 52w low and below the 52w high. Profile of future superperformers: ADR 4.5% vs 2.6%, 27% below the 52w high (vs 13%), base_count 0. RS rank barely matters. Top rule: stocks > 54% below their 52w high hit +40% 45% of the time (IS and OOS), i.e. beaten-down rebounds.
- **Your setups in high-score stocks:** +0.19R (sma50 exit) vs −0.10R in low-score stocks.
- **Portfolios:** setups only in the model's top 10% with the sma50 exit: **28% CAGR**, −42% DD, beat SPY in 6/9 years, top-2-years share 51% (least concentrated so far). Adaptive sizing on the top-20 pool: **17% / −24%** vs 14% / −26%, better on both.
- **Warnings:** (1) survivorship: the universe is today's members, so beaten-down stocks in it are ones that recovered; (2) "+40% high within 3 months" rewards volatility (a stock can hit +40% and still crash).

## Run 12 — 2026-10-08 (commit d8399f4): stress tests of the superperformer edge
- **Survivorship / future-membership bias is large.** S&P 500 names, top-10% model setups, sma50 exit: **47% CAGR on all dates, but 20% CAGR when a stock is only traded after it actually joined the S&P 500** (point-in-time; 2,705 vs 5,163 OOS signals; DD −32% both). Most of the apparent excess comes from knowing which stocks *will become* index members. The honest number for that subset is ~20% vs SPY 14.6%, with a similar drawdown.
- **The stock selection is most of the edge:** random entries in the model's top-10% stocks made 20% CAGR (−43% DD); adding real setups raised it to 28% (−42%).
- **It doesn't depend on beaten-down rebounds:** leaders only (within 40% of the 52w high) did better, 32% / −39%.
- **Clean label (+40% before −20%):** same lift (top decile 27.5% vs 6.7%, 4.1x, AUC 0.83), portfolio 28% / **−33%**, a lower drawdown than the plain label.
- **Adaptive sizing helps again:** top 10% + adaptive 33% / −31% (vs 28% / −42%). It has improved risk-adjusted returns in every test.
- **Conclusion:** the model-ranked approach beats SPY even point-in-time (~20% vs 15% in the S&P 500 subset), but the headline 28-47% numbers are inflated by survivorship in this free-data universe. A definitive answer needs survivorship-free data with delisted stocks (e.g. Norgate Data or Sharadar). Every all-dates number should get a large haircut.

## Run 12 — planned 2026-10-08: is the superperformer edge real?
- Survivorship test: S&P 500 names traded on all dates vs only after their Wikipedia "Date added".
- Random entries in the model's top 10% (is it the setups or the stock list?).
- Leaders only (within 40% of the 52w high): does it work without beaten-down rebounds?
- Clean label: +40% before −20%.
- Top 10% + adaptive sizing.

## Run 11 — planned 2026-10-08: "how do top traders consistently beat the S&P?"
Six runs show our setups have a real per-trade edge, but as portfolios they roughly match SPY with lumpy years (2023-24). What pros do that we haven't modelled:
1. **They hunt for future superperformers, not setups.** O'Neil and Minervini studied hundreds of big winners to see what they looked like *before* the move. New: a model trained on every stock every 10 days (~600k rows) to predict a >= 40% gain within 3 months. Walk-forward by year; rows only train once their 3-month label window has closed. Reports lift over the base rate, permutation importance, a profile of future winners vs everything else, readable rules, and whether setups in high-score stocks pay more. Portfolios are ranked by this score.
2. **They size by how their strategy is working** (bigger in hot streaks, smaller in cold). New: adaptive sizing at 0.5x risk when the last 20 closed trades averaged < 0R and 1.5x when > +0.5R (closed trades only).
3. Not testable with this data (logged as caveats): intraday entries with tight stops, small caps / IPOs outside the S&P 1500, leverage and concentration, and survivorship among traders (we hear from the winners).
- Fix: history.csv read commit hashes like `5e93689` as numbers (inf). It now reads them as text; the file is repaired.

## Run 6 — 2026-10-08 (commit 32c75da), 659,965 signals: wedges, triangles, tightness
Excess avg R over random entries, averaged over all exits (OOS 2018+; IS in brackets):
- **descending triangle (upside breakout):** +0.21 (IS +0.21). Consistent, but only ~80 signals/yr and n=706 OOS.
- **falling wedge:** +0.13 (IS +0.27). With the O'Neil exit: IS +0.48R, OOS +0.19R, t 3.6, ~170/yr. The best new setup.
- **symmetrical triangle:** +0.13 (IS +0.08).
- **ascending triangle:** +0.05; **rising wedge:** +0.00. No edge, despite asc triangles' reputation.
- **tight coils:** 7-day +0.04, 15-day +0.00. Tightness alone is not an edge, which matches the user's own trades (the tightest ATR bucket did worse) and the low ML importance of tightness features in every run.
- With the sma50 exit and no filter, every pattern is near zero OOS. Their edge depends on the exit (O'Neil +20% target suits patterns better than long trends).
- Bullish patterns that beat random are the ones that break a *falling* upper line (falling wedge, descending and symmetrical triangle). Flat-top (ascending) triangles did not.
- Run 9 (idle cash in SPY) was cancelled at the moment run 8 finished, for an unknown reason. Re-triggered.

## Run 5 — 2026-10-08 (commit fd50739)
- **Top-10-by-IS-expectancy portfolio (all EP strategies):** 12.0% CAGR, −32% MTM max DD, 506 trades, avg 6.3 of 10 slots used. Top 5: 10%/−33%. Top 20: 8%/−33%. SPY: 14.6%/−34%. The per-trade edge is real (OOS +0.3 to +0.6R), but there are too few signals (~57/yr) to keep capital working.
- **Lumpy returns:** the best portfolios made 68-87% in 2023-2024 but mostly trailed SPY in 2018-2022.
- **EP-only ML is useless:** taken +0.354R vs skipped +0.353R. Stop investing in ML meta-labeling for EP. The pooled ML still only separates losers.
- **Next (added to run 6 via [skip ci], since run 6 checks out the newest code):** hold idle cash in SPY; test 2% risk and 15 slots; report how much growth comes from the two best years.

## Run 6 — planned 2026-10-08 (queued behind run 5)
**User question:** do ascending/descending triangles, wedges and tightness work?
- New entries: `asc_triangle`, `desc_triangle`, `sym_triangle`, `falling_wedge`, `rising_wedge` (60-day window). Trendlines are fit through the last 2-3 *confirmed* swing highs/lows (a swing at i needs i+3 <= t-1, so nothing after the signal day is used). Each touch must be within 2% of its line, closes must stay inside the pattern, and the lines must narrow by >= 25%. The pattern is classified by the slopes (flat = |slope| <= 0.05% of price per day). Signal: first close above the upper line on >= 1.2x volume. Stop: the lower line or the day's low, whichever is lower.
- New entries: `tight_coil_7` (7 closes within 1 ADR) and `tight_coil_15` (15 closes within 1.5 ADR), then a breakout above the coil high on >= 1.2x volume, above a rising 50-day. Stop: coil low.
- First detector version required *every* swing in the window to touch the lines and fired 0 times on test data; changed to the last 2-3 touches. A dedicated lookahead test covers the pattern kernel.
- Prior evidence on tightness: in the user's own 1,363 trades, the tightest ATR bucket (ATR10/ATR50 < 0.8) did *worse* (−0.11R). Tightness features (tight_10, atr_ratio, close_std_10) have ranked low in ML importance in every run.

## Run 5 — planned 2026-10-08
**Changes, each driven by a run-4 finding:**
1. Trade the expectancy-selected strategies as portfolios: the top 5/10/20 by IS avgR (min 200 IS trades), each keeping its own exit. Duplicates on the same stock and day keep the higher-ranked strategy. Signals are ranked by RS.
2. Year-by-year returns of the best portfolios vs SPY, to check consistency rather than a single CAGR.
3. ML trained on episodic pivots only (run 3: ML helped within EP but not in the pooled set).

## Run 4 — 2026-10-08 (commit 48a9d03), 633,749 signals
- **Selecting by expectancy works:** the top 20 strategies by IS avgR (n >= 200) averaged **+0.34R OOS**, vs +0.06R for all strategies. Top 20 by IS t-stat only made +0.05R, because t-stat favours frequent, thin-edge setups. All 20 are episodic pivots with RS/early filters, mostly with the sma50_close exit. Examples (OOS): ep_gap8_hold/rs80/sma50 +0.58R (PF 1.90, t 3.19, 624 trades), ep_gap10/early_stage/sma50 +0.58R (t 3.25), ep_gap5/rs80_early/sma50 +0.40R.
- **Edge vs random in both periods (>= 0.05R):** all 7 EP variants, donchian_20/55, undercut, ema_retest, flag_60, flag_30_early, high52_fresh. **No edge:** high52, multi_touch, stage2.
- **Theme (sub-industry RS) doesn't help:** theme alone +0.021R vs none +0.023R. rs80_early_theme was best IS (+0.12) but fell to +0.06 OOS, below rs80_early (+0.16). Negative result; keep the features in ML but not as a filter.
- **Honest drawdowns are large:** mark-to-market max DD is −50% for all setups ranked by RS (20.9% CAGR), and −47% to −52% for IS-selected setup pools. SPY: 14.6% CAGR, −34%. The SPY > 200d overlay barely helped (−50 → −43% with the O'Neil exit, none with sma50). Portfolios are flooded with frequent thin-edge signals, while the high-expectancy EP strategies (~40-70 trades a year) were never traded on their own. Addressed in run 5.
- **ML** still adds little in the pooled set: rank corr 0.25, flat deciles, risk_adr dominant.

## Run 4 — planned 2026-10-08
**Changes, each driven by a run-3 finding:**
1. *Survivorship:* the run-3 diagnostics showed Wikipedia's S&P 500 page no longer has a changes table, so former members can't be recovered there (and Yahoo serves few delisted tickers). Accepted as a caveat. The main metric (excess over random entries from the same universe) cancels much of this bias.
2. *Hot theme:* the same page carries GICS sector / sub-industry. Added sub-industry and sector RS (median RS rank of each group per day, groups with >= 3 stocks) as ML features, plus filters `theme`, `rs80_theme` and `rs80_early_theme`. The theme idea comes from the user's playbook, chosen before seeing any results.
3. *Honest drawdowns:* the portfolio is now marked to market daily. Runs 1-3 only counted closed trades (run 3's best was −47% realized).
4. *Portfolio from in-sample choices only:* pool the setups that beat random entries by >= 0.05R before 2018 (min 100 trades), with the IS-best exit and with sma50_close. Also test an SPY > 200-day overlay to cut drawdowns.
5. *Insights logic:* run 3 said "selection is mostly noise" despite a rank correlation of 0.57. The real issue is that t-stat ranking favours frequent thin-edge strategies, so the top 20 by IS avgR is now reported too. "Edge" now requires >= +0.05R over random in both periods (run 3 listed 16 entries).

## Run 3 — 2026-10-08 (commit 5e93689), 633,749 signals
- **Episodic pivots are robust across variations:** every EP variant beat random entries in both periods. OOS excess: gap15 +0.32R, gap10_vol2 +0.27, gap10 +0.26, gap10_vol5 +0.25, gap8_hold +0.21, gap8_neglected +0.18, gap5 +0.14. An edge that survives parameter changes is less likely to be overfit.
- **Exit:** sma50_close is the best OOS exit (+0.16R avg over entries) and second-best IS (+0.10 vs O'Neil +0.12). Quick-profit exits (Qullamaggie day-5 partials, fixed 3R/20d) are worst on daily bars.
- **Filters:** rs80_early +0.16R OOS (best); it lifts even random entries in both periods (IS +0.05R, OOS +0.09R). mkt_ok does nothing again.
- **ML (R regression):** OOS rank correlation 0.25, but mean R by decile is flat beyond the bottom decile. It identifies losers (decile 0 = −0.10R), not big winners. Per entry, ML "taken" beat "skipped" for every EP variant (e.g. ep_gap10 +0.21 vs +0.01), but not for donchian or ema_retest. The current features can't predict big winners, so new information is needed (theme strength added in run 4).
- **Portfolio (realized):** all setups ranked by RS 20.9% CAGR vs random order 5.0%. The same signals in a different order cost about 16 points a year, so **RS ranking among same-day signals is a major part of the edge**. Random entries ranked by RS: 3.6%.
- **Infrastructure:** results saved correctly with the new commit step.

## Run 2 — 2026-10-08: computed, results lost (infrastructure lessons)
- Run 2 finished (633,789 signals, ML 13 min) but its results commit hit a merge conflict with a manual re-run's results and the push loop failed silently. **Fix:** the commit step now always commits on top of the latest branch, keeps LOG.md, merges history.csv, and fails loudly if it can't push. Tested locally against a simulated conflicting push.
- A manual re-run of an old run re-uses that run's old commit, and new runs were cancelling in-progress ones. **Fix:** runs queue instead of cancelling, and they check out the newest branch code.
- The removed S&P 500 members parser still found 0 (Wikipedia's table layout is unknown from the sandbox). **Fix:** broader detection plus diagnostics printed to the run log. Bumped the price cache (v3).
- Reproducibility check: the manual re-run of the run-1 code reproduced run 1's numbers exactly.
- Run 3 = run 2's experiments (R-regression ML, EP variants, ranking portfolios), re-done.

## Run 2 — planned 2026-10-08
**Changes, each driven by a run-1 finding:**
1. Survivorship: the removed-members parser found 0 tickers. Rewrote it to work with any Wikipedia header layout; bumped the price cache so the universe is rebuilt.
2. ML target: the run-1 classifier (R > 0) mostly learned stop width (`risk_adr` dominated). Win rate rose by decile but avg R didn't (top decile ≈ 0R). The model now predicts R itself (regression, clipped to [-2, 8]) and is also scored on the trim_ema exit plan.
3. Episodic pivots were the most consistent edge, so added variants: gap ≥ 15%, gap 10% on 2× and on 5× volume, gap 8% closing above the open.
4. Portfolio: compare ways of choosing among same-day signals (RS rank, ML prediction, random order) and the rs80_early-filtered pool.
5. Data hygiene: zero-volume days produced inf ratios; these are now cleaned.

**Watch for:** does EP hold up with former members included? Does R-regression ML give monotonic avg R by decile? Is RS ranking the source of the portfolio edge?

**Caveat:** 2018+ has now been looked at, so anything chosen *because* it looked good after 2018 isn't validated by it. The real holdout from here on is forward (paper) trading.

## Run 1 — 2026-10-08 (commit b1d5ff1)
1,488 stocks (S&P 500/400/600 current members only), 628,659 signals, 20 entries × 9 exits × 6 filters.
- **Selection works partly:** IS-vs-OOS rank correlation 0.47. The top 20 by IS averaged +0.05R OOS vs −0.07R for random entries.
- **Consistent edge vs random entries (both periods, most exits):** episodic pivots (ep_gap5/10/8_neglected), donchian_20/55, ema_retest. High52_fresh and vcp were small.
- **No edge:** high52 (plain), pocket_pivot, multi_touch, stage2 (positive IS, negative OOS), htf (too few signals).
- **Flags and bases:** strong OOS but negative IS, so the result depends on the period.
- **Filters:** rs80_early (top-20% RS and 1st/2nd staircase) is the best filter. It even lifts *random* entries to +0.21R OOS with the 50-SMA exit, so stock selection is a large part of the edge. mkt_ok (SPY above 8/21/50 EMA) adds nothing, matching the user's own trades.
- **Exits:** sma50_close best OOS (+0.08R average). O'Neil 20/8 was best IS but decayed. Qullamaggie day-5 partials were worst on daily bars.
- **ML (R > 0 classifier):** AUC 0.615, but the gain was in win rate, not avg R. It learned stop width. Fixed in run 2.
- **Portfolio 2018+ ($100k, 1% risk, 10 slots):** all setups ranked by RS 21% CAGR (realized max DD −42%) vs SPY 15%. Random entries ranked by RS 4%. ML-filtered 2%.
