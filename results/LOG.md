# Research log (newest first)

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
