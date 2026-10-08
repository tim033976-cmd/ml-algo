# Research log (newest first)

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
