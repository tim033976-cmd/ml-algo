# Research log (newest first)

## Run 10 — 2026-10-08 (commit 54a58fb): idle cash in SPY, bigger risk
- **Top 10 by IS expectancy, 1% risk, idle cash in SPY:** 15.2% CAGR, −34% max DD. SPY: 14.6% / −34%. That is essentially SPY plus a little: it beat SPY in 2019, 2020, 2022 (−8% vs −18%) and 2026, and lagged in 2024 (+16 vs +25) and 2025 (−12 vs +18).
- **2% risk is worse:** 13%, −39%. With 2% risk most positions hit the 20% size cap and cash runs out at ~5 positions, so 10 vs 15 slots made no difference (identical results). More risk per trade doesn't add return here, only drawdown.
- **Without idle cash:** the top 20 by IS expectancy is still the best risk-adjusted (13.8%, −26%).
- **Conclusion:** the mechanical setups give SPY-like returns with different timing. Beating SPY decisively needs something the setups alone don't provide (stock selection / sizing), which is what run 11 tests.

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
