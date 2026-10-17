# Strategy research report

Generated 2026-10-17 05:28 UTC in 87 min.
Universe: 1543 stocks with data (sp500: 658, sp600: 537, sp400: 346; 159 former S&P 500 members). Signals 2006-01-03 -> 2026-10-15: 954,390.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.49). Top 20 by IS t-stat: +0.065R OOS; top 20 by IS avgR (n>=200): +0.391R; all strategies +0.050R; random entries -0.022R.
- Too few signals to judge (need 100+ per period): htf (IS 53, OOS 103).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.30R, OOS +0.31R), ep_gap10_vol5 (IS +0.18R, OOS +0.21R), ep_gap8_hold (IS +0.18R, OOS +0.17R), ep_gap8_neglected (IS +0.20R, OOS +0.15R), desc_triangle (IS +0.18R, OOS +0.15R), tc_supertrend_ema (IS +0.15R, OOS +0.11R), ep_gap5 (IS +0.14R, OOS +0.11R), wf_rocket_gap (IS +0.10R, OOS +0.20R), ep_gap10 (IS +0.10R, OOS +0.22R), falling_wedge (IS +0.22R, OOS +0.09R), ep_gap10_vol2 (IS +0.07R, OOS +0.24R), wf_rocket_breakout (IS +0.14R, OOS +0.06R), undercut (IS +0.11R, OOS +0.06R), tc_ema_cross_base (IS +0.12R, OOS +0.06R), donchian_20 (IS +0.10R, OOS +0.06R), wf_scan_pullback (IS +0.11R, OOS +0.05R), sym_triangle (IS +0.05R, OOS +0.07R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
- Best exit out-of-sample (avg over entries): wf_weekly10 (+0.097R); worst: qull_sma10 (-0.042R).
- Filters that help OOS: qull_scan_regime (+0.113R), rs80_early (+0.107R), qull_scan (+0.080R), rs80_early_theme (+0.065R), early_stage (+0.051R), wf_scan_green (+0.042R), wf_rocket_green (+0.035R); that hurt: none.
- ML filter adds little: OOS rank corr 0.002, AUC 0.505, decile monotonicity -0.55, taken +0.082R vs skipped +0.074R.
- Features the model relies on most: rates_rising, above_52w_low, adr_pct, sector_rs, rs_rank.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.07R, OOS +0.05R), qull_scan (IS +0.08R, OOS +0.17R), rs80_early_theme (IS +0.09R, OOS +0.07R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.554` (IS +0.33R, OOS +0.13R, n=48920).
- Superperformer model: 30.4% of its top-10% picks gained >= 40% within 3 months vs 7.2% for all stocks (4.2x), AUC 0.834. Driven by: adr_pct, above_52w_low, dist_52w_high, atr_pct, leg1_range.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 53% (break-even ~50%), avg net return per trade +0.8%. Point-in-time S&P 500 top 10%: 54%, +1.4% per trade (n=7694).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 36% (break-even ~33%), avg net return per trade +2.0%. Point-in-time S&P 500 top 10%: 37%, +2.6% per trade (n=5097).
- Best portfolio 2018->today: RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10% at 35.7% CAGR (max drawdown -51.5%) vs SPY 14.3%.
- Best return per unit of drawdown: RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10% (32.2% CAGR, -31.5% max DD).
- Workflow PDF rockets as written (regime sizing) / wf_rocket: 2.1% CAGR, -12% DD, 192 trades.
- Workflow PDF rockets, QQQ 21/50 regime / wf_rocket: 1.4% CAGR, -9% DD, 193 trades.
- Workflow PDF rockets as written, S&P 500 point-in-time only / wf_rocket: 1.3% CAGR, -7% DD, 142 trades.
- Workflow PDF scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10: 0.8% CAGR, -17% DD, 357 trades.
- Workflow PDF scanner PIT, QQQ 21/50 regime / wf_weekly10: -2.5% CAGR, -25% DD, 381 trades.
- Workflow PDF scanner as written, full universe / wf_weekly10: 0.7% CAGR, -23% DD, 373 trades.
- Workflow PDF split (40/25/15/20 cash): 6.4% CAGR, -17% DD vs SPY 14.3%, -34%.
- Volatility-matched check (goal model (full universe), OOS): model top 10% hit 38.6% vs 34.0% for same-ADR, same-momentum stocks; return +2.69% vs +1.95% per trade.
- Volatility-matched check (goal model, S&P 500 point-in-time, OOS): model top 10% hit 38.1% vs 32.4% for same-ADR, same-momentum stocks; return +3.03% vs +1.93% per trade.
- Bracket menu: in-sample best (return per month) is +20% / -8%. OOS top 10%: hit 34.1% (break-even 29%), +2.10% per trade, +2.25% per month held, vs +20/-10: hit 38.6%, +2.68%, +2.42%/month.
- Regime gate breadth (stocks above 50d) (skip high (> 71%), mid): 14.1% CAGR, -40% DD; point-in-time S&P 500 10.2%, -32%.
- Regime gate VIX level (skip 15-20, < 15): 27.4% CAGR, -29% DD; point-in-time S&P 500 20.5%, -28%.
- Regime gate VIX / VIX3M (skip < 0.9 (calm), > 1.0 (stress)): 19.9% CAGR, -39% DD; point-in-time S&P 500 7.2%, -30%.
- Regime gate SPY above 200d (skip yes): 7.4% CAGR, -26% DD; point-in-time S&P 500 7.1%, -24%.
- Regime gate QQQ above 10 & 20 SMA (skip yes): 22.1% CAGR, -46% DD; point-in-time S&P 500 8.2%, -27%.
- Regime gate SPY 1-month return (skip -3..0%, > 3%): 15.9% CAGR, -41% DD; point-in-time S&P 500 3.5%, -31%.
- Regime gate SPY vs 21/50 SMA (skip above 21 & 50, above 50 only): 11.6% CAGR, -40% DD; point-in-time S&P 500 10.7%, -27%.
- Regime gate QQQ vs 21/50 SMA (skip above 21 & 50): 19.9% CAGR, -31% DD; point-in-time S&P 500 3.8%, -34%.
- Regime gate A/D line vs its 21/50 MA (skip above 21 & 50, above 50 only): 7.3% CAGR, -41% DD; point-in-time S&P 500 7.7%, -30%.
- Regime gate % of stocks above 20d (skip 40-60%, > 60%): 14.1% CAGR, -37% DD; point-in-time S&P 500 7.1%, -25%.
- Regime gate % above 50d, 10-day change (skip flat): 31.2% CAGR, -31% DD; point-in-time S&P 500 12.1%, -30%.
- Regime gate A/D line, 10-day change (skip flat, rising): 11.8% CAGR, -43% DD; point-in-time S&P 500 5.9%, -26%.
- Regime gate sector & sub-industry today green (skip both, one of the two): 17.0% CAGR, -51% DD; point-in-time S&P 500 6.8%, -32%.
- Regime gate sector & sub-industry up over 5 days (skip both): 22.3% CAGR, -47% DD; point-in-time S&P 500 12.2%, -30%.
- Regime gate sector & sub-industry above 21 EMA (skip both, one of the two): 24.3% CAGR, -46% DD; point-in-time S&P 500 10.6%, -29%.
- Regime gate distance above the 21 EMA (skip 0-5%, 5-10%): 16.2% CAGR, -45% DD; point-in-time S&P 500 14.0%, -32%.
- Regime gate ADR% (skip < 3%): 27.0% CAGR, -39% DD; point-in-time S&P 500 17.6%, -41%.
- Regime gate ADR% (only stocks trading >= $10M/day) (skip < 3%): 30.2% CAGR, -35% DD; point-in-time S&P 500 17.6%, -41%.
- Regime gate fundamental inflection (all 4) (skip no, yes): 12.5% CAGR, -32% DD; point-in-time S&P 500 6.6%, -13%.
- Regime gate revenue growth accelerating (skip 1 quarter, no (decelerating)): 23.1% CAGR, -44% DD; point-in-time S&P 500 9.8%, -27%.
- Regime gate operating income outgrowing revenue (skip yes): 26.2% CAGR, -43% DD; point-in-time S&P 500 15.0%, -25%.
- Regime gate operating margin vs a year ago (skip expanding, shrinking): 14.4% CAGR, -36% DD; point-in-time S&P 500 16.3%, -19%.
- Regime gate FCF margin vs a year ago (skip improving): 12.9% CAGR, -55% DD; point-in-time S&P 500 9.9%, -32%.
- Regime gate up/down volume, 50 days (skip 1.0-1.3, > 1.3 (accumulation)): 15.1% CAGR, -39% DD; point-in-time S&P 500 14.8%, -31%.
- Regime gate price vs 200-day (skip 0-10% above, 10-30% above, 30-50% above, > 50% above): 13.4% CAGR, -37% DD; point-in-time S&P 500 16.1%, -28%.
- Regime gate 6-month gain (skip 0-20%, 20-50%, 50-100%, > 100%): 17.1% CAGR, -38% DD; point-in-time S&P 500 17.2%, -30%.
- Regime gate sector (11 GICS, by median RS) (skip bottom 3, top 3 (leading)): 20.5% CAGR, -52% DD; point-in-time S&P 500 11.0%, -30%.
- Regime gate sub-industry (by median RS) (skip top 30% (leading)): 16.3% CAGR, -49% DD; point-in-time S&P 500 14.6%, -33%.
- Regime gate 3-day market model (skip rest): 6.4% CAGR, -15% DD; point-in-time S&P 500 2.3%, -9%.
- Filter RULE: top 3 sectors only: 21.5% CAGR, -29% DD; point-in-time S&P 500 7.0%, -21%.
- Filter RULE: top 30% sub-industries only: 26.0% CAGR, -29% DD; point-in-time S&P 500 7.8%, -25%.
- Filter RULE: top 3 sectors AND top 30% sub-industries: 21.8% CAGR, -29% DD; point-in-time S&P 500 3.5%, -19%.
- Filter RULE: SPY above its 21 & 50 SMA: 32.2% CAGR, -32% DD; point-in-time S&P 500 9.6%, -19%.
- Filter RULE: QQQ above its 21 & 50 SMA: 27.1% CAGR, -34% DD; point-in-time S&P 500 13.1%, -21%.
- Filter RULE: SPY above its 50 SMA (21 either way): 26.1% CAGR, -33% DD; point-in-time S&P 500 13.9%, -23%.
- Filter RULE: A/D line above its 21 & 50 MA: 18.6% CAGR, -37% DD; point-in-time S&P 500 13.1%, -25%.
- Filter RULE: > 50% of stocks above their 50d: 21.1% CAGR, -41% DD; point-in-time S&P 500 10.4%, -27%.
- Filter RULE: % above 50d rising over 10 days: 26.0% CAGR, -30% DD; point-in-time S&P 500 5.3%, -32%.
- Filter RULE: sector AND sub-industry green today: 20.9% CAGR, -33% DD; point-in-time S&P 500 10.6%, -30%.
- Filter RULE: sector AND sub-industry up over 5 days: 22.2% CAGR, -35% DD; point-in-time S&P 500 12.7%, -26%.
- Filter RULE: sector AND sub-industry above 21 EMA: 19.7% CAGR, -41% DD; point-in-time S&P 500 10.3%, -25%.
- Filter RULE: SPY > 21 & 50 + sector & sub-industry up 5 days: 24.4% CAGR, -32% DD; point-in-time S&P 500 9.5%, -16%.
- Filter RULE: <= 10% above the 21 EMA (course rule): 25.6% CAGR, -36% DD; point-in-time S&P 500 16.1%, -33%.
- Filter RULE: ADR% >= 5% (the infographic's minimum): 33.2% CAGR, -48% DD; point-in-time S&P 500 8.3%, -33%.
- Filter RULE: ADR% 5-12% (the infographic's sweet spot): 34.7% CAGR, -49% DD; point-in-time S&P 500 8.1%, -33%.
- Filter RULE: ADR% <= 15% (skip the wildest): 28.5% CAGR, -34% DD; point-in-time S&P 500 13.8%, -33%.
- Filter RULE: ADR% 5-12% and >= $10M/day: 35.7% CAGR, -51% DD; point-in-time S&P 500 8.1%, -33%.
- Filter RULE: fundamental inflection (rev accel 2q + op leverage + margin + FCF up): 15.7% CAGR, -25% DD; point-in-time S&P 500 4.0%, -17%.
- Filter RULE: revenue growth accelerating 2+ quarters: 29.4% CAGR, -33% DD; point-in-time S&P 500 8.5%, -24%.
- Filter RULE: accumulation (up/down volume 50d > 1): 24.8% CAGR, -45% DD; point-in-time S&P 500 7.8%, -29%.
- Filter RULE: not extended (< 30% above the 200-day): 18.6% CAGR, -38% DD; point-in-time S&P 500 16.7%, -32%.
- Filter RULE: not already up 50%+ in 6 months: 19.7% CAGR, -37% DD; point-in-time S&P 500 16.0%, -31%.
- Filter RULE: price rules only (accumulation + not extended + not up 50%): 19.3% CAGR, -48% DD; point-in-time S&P 500 8.2%, -27%.
- Filter RULE: user's full method (inflection + price rules): 1.2% CAGR, -25% DD; point-in-time S&P 500 -0.2%, -14%.
- Filter METHOD: user's method alone, no model (inflection + price rules): 9.1% CAGR, -26% DD; point-in-time S&P 500 3.3%, -20%.
- Filter METHOD: fundamental inflection alone, no model: 15.2% CAGR, -37% DD; point-in-time S&P 500 9.8%, -24%.
- Filter MODEL + fundamentals as features, top 10%: 24.1% CAGR, -34% DD; point-in-time S&P 500 21.8%, -28%.
- Filter SIZE: position scaled by 6% / ADR (x0.4-1.5): 24.2% CAGR, -39% DD; point-in-time S&P 500 16.8%, -31%.
- Regime gate (no gate) (skip nothing): 27.6% CAGR, -34% DD; point-in-time S&P 500 13.7%, -33%.

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
3. Focus development on: ep_gap15, ep_gap10_vol5, ep_gap8_hold, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, undercut, tc_ema_cross_base, donchian_20, wf_scan_pullback, sym_triangle (tune them on IS data only, re-check OOS).
4. Make qull_scan_regime a default filter.
5. Inspect rates_rising and above_52w_low: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around qull_scan first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                                                                                | no_edge_entries                                                            | best_exit   | helpful_filters                                                                                              |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                       | filters_lifting_baseline                 |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                                  |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret | menu_choice   |   menu_choice_oos_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:------------|:-------------------------------------------------------------------------------------------------------------|---------:|---------------:|---------------:|---------:|:-------------------------------------------------------------------|:-----------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:----------------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|:--------------|----------------------:|
| 2026-10-09 14:16 | e1db28d  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                                                          | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok              | early_stage, rs80_early_theme            |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 15:34 | 246a119  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme            |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 16:26 | c39a032  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme            |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-10 02:25 | 404aae3  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme            |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-10 13:16 | 7a7fe02  |      1540 |    952523 |        0.48 |        0.06 |          -0.01 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green, rs80 |     0.51 |           0.01 |          -0.26 |     0.01 | rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope | rs80_early_theme                         |            2 | RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%           |        0.34 |       0.15 | REGIME 3-day market model: skip ['rest'] / +20% -10%                              |        0.83 |         4.22 | adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range      |               0.52 |               0.01 |               0.37 |               0.02 | +30% / -5%    |                  0.02 |
| 2026-10-10 15:18 | 3de3b4a  |      1540 |    952523 |        0.48 |        0.06 |          -0.01 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green, rs80 |     0.51 |           0.01 |          -0.26 |     0.01 | rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope | rs80_early_theme                         |            2 | RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%           |        0.34 |       0.15 | REGIME 3-day market model: skip ['rest'] / +20% -10%                              |        0.83 |         4.22 | adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range      |               0.52 |               0.01 |               0.37 |               0.02 | +30% / -5%    |                  0.02 |
| 2026-10-10 16:44 | 51ff2b3  |      1540 |    952523 |        0.48 |        0.06 |          -0.01 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green, rs80 |     0.51 |           0.01 |          -0.26 |     0.01 | rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope | rs80_early_theme                         |            2 | RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%           |        0.32 |       0.15 | REGIME 3-day market model: skip ['rest'] / +20% -10%                              |        0.83 |         4.22 | adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range      |               0.52 |               0.01 |               0.37 |               0.02 | +30% / -5%    |                  0.02 |
| 2026-10-11 05:33 | f92aaf7  |      1540 |    952523 |        0.48 |        0.06 |          -0.01 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green, rs80 |     0.51 |           0.01 |          -0.26 |     0.01 | rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope | rs80_early_theme                         |            2 | RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%           |        0.32 |       0.15 | REGIME 3-day market model: skip ['rest'] / +20% -10%                              |        0.83 |         4.22 | adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range      |               0.52 |               0.01 |               0.37 |               0.02 | +30% / -5%    |                  0.02 |
| 2026-10-17 03:59 | ccaba0b  |      1543 |    954390 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, ep_gap8_hold, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, undercut, tc_ema_cross_base, donchian_20, wf_scan_pullback, sym_triangle                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.00 |          -0.55 |     0.01 | rates_rising, above_52w_low, adr_pct, sector_rs, rs_rank           | early_stage, qull_scan, rs80_early_theme |            2 | RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10%                        |        0.36 |       0.14 | RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10%                         |        0.83 |         4.22 | adr_pct, above_52w_low, dist_52w_high, atr_pct, leg1_range      |               0.53 |               0.01 |               0.36 |               0.02 | +20% / -8%    |                  0.02 |
| 2026-10-17 05:28 | 86eb5f4  |      1543 |    954390 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, ep_gap8_hold, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, undercut, tc_ema_cross_base, donchian_20, wf_scan_pullback, sym_triangle                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.00 |          -0.55 |     0.01 | rates_rising, above_52w_low, adr_pct, sector_rs, rs_rank           | early_stage, qull_scan, rs80_early_theme |            2 | RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10%                        |        0.36 |       0.14 | RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10%                         |        0.83 |         4.22 | adr_pct, above_52w_low, dist_52w_high, atr_pct, leg1_range      |               0.53 |               0.01 |               0.36 |               0.02 | +20% / -8%    |                  0.02 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 7995.000 |
| strategies_with_enough_trades | 6318.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.486 |
| rank_corr_IS_vs_OOS_t         |    0.532 |
| OOS_avgR_all_strategies       |    0.050 |
| OOS_avgR_top20_by_IS          |    0.065 |
| OOS_avgR_top20_by_IS_avgR     |    0.391 |
| OOS_avgR_random_baseline      |   -0.022 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  70486 |      0.18 |  44.53 |   67927 |      7731.49 |      0.47 |       0.09 |     1.19 |   19.65 |         694.26 |
| wf_scan_pullback | all           | bracket_20_10 |  71779 |      0.18 |  44.36 |   70011 |      7968.69 |      0.47 |       0.09 |     1.19 |   20.08 |         724.57 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70878 |      0.15 |  43.45 |   67927 |      7731.49 |      0.54 |       0.06 |     1.15 |   17.16 |         484.65 |
| wf_scan_pullback | all           | bracket_10_10 |  72176 |      0.14 |  43.30 |   70011 |      7968.69 |      0.54 |       0.06 |     1.15 |   17.29 |         496.86 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  61579 |      0.17 |  38.63 |   59013 |      6716.89 |      0.48 |       0.12 |     1.25 |   23.84 |         789.82 |
| donchian_20      | all           | bracket_20_10 |  69894 |      0.16 |  38.17 |   79590 |      9058.97 |      0.45 |       0.07 |     1.14 |   16.43 |         655.24 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61971 |      0.13 |  37.64 |   59013 |      6716.89 |      0.55 |       0.08 |     1.21 |   21.58 |         567.40 |
| pocket_pivot     | all           | bracket_20_10 |  48753 |      0.19 |  37.42 |   48748 |      5548.52 |      0.46 |       0.06 |     1.13 |   11.70 |         353.01 |
| pocket_pivot     | all           | bracket_10_10 |  49161 |      0.15 |  37.23 |   48748 |      5548.52 |      0.53 |       0.05 |     1.11 |   11.20 |         271.32 |
| donchian_20      | all           | bracket_10_10 |  70339 |      0.13 |  36.53 |   79590 |      9058.97 |      0.53 |       0.05 |     1.11 |   13.69 |         430.91 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57913 |      0.17 |  35.98 |   62682 |      7134.50 |      0.45 |       0.07 |     1.14 |   14.45 |         513.21 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  50461 |      0.17 |  35.62 |   47878 |      5449.50 |      0.46 |       0.08 |     1.16 |   14.03 |         417.46 |
| donchian_20      | mkt_ok        | bracket_10_10 |  58311 |      0.13 |  34.14 |   62682 |      7134.50 |      0.53 |       0.05 |     1.11 |   12.07 |         338.40 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50799 |      0.13 |  33.99 |   47878 |      5449.50 |      0.54 |       0.05 |     1.12 |   11.92 |         283.64 |
| wf_scan_base     | all           | bracket_20_10 |  31867 |      0.19 |  33.59 |   25089 |      2855.64 |      0.48 |       0.04 |     1.10 |    6.34 |         125.87 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  36204 |      0.15 |  33.51 |   32529 |      3702.47 |      0.54 |       0.05 |     1.12 |    9.43 |         184.13 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35886 |      0.19 |  33.08 |   32529 |      3702.47 |      0.46 |       0.06 |     1.13 |    9.72 |         234.42 |
| donchian_20      | wf_scan       | bracket_20_10 |  43267 |      0.17 |  32.62 |   41670 |      4742.90 |      0.46 |       0.06 |     1.11 |    9.44 |         262.26 |
| wf_scan_base     | all           | bracket_10_10 |  32085 |      0.16 |  32.48 |   25089 |      2855.64 |      0.53 |       0.04 |     1.09 |    6.53 |         108.56 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35472 |      0.18 |  32.12 |   34199 |      3892.55 |      0.46 |       0.06 |     1.12 |    9.01 |         226.76 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  25142 |      0.20 |  31.81 |   17699 |      2014.51 |      0.48 |       0.04 |     1.09 |    5.04 |          80.95 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35824 |      0.15 |  31.79 |   34199 |      3892.55 |      0.53 |       0.05 |     1.11 |    9.05 |         183.53 |
| donchian_20      | wf_scan       | bracket_10_10 |  43569 |      0.14 |  31.69 |   41670 |      4742.90 |      0.53 |       0.03 |     1.07 |    6.88 |         153.23 |
| donchian_55      | all           | bracket_20_10 |  47683 |      0.16 |  31.67 |   51592 |      5872.23 |      0.45 |       0.06 |     1.11 |   10.59 |         335.37 |
| donchian_55      | all           | bracket_10_10 |  48044 |      0.13 |  31.40 |   51592 |      5872.23 |      0.53 |       0.03 |     1.07 |    7.16 |         179.67 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25317 |      0.16 |  30.78 |   17699 |      2014.51 |      0.54 |       0.04 |     1.11 |    6.48 |          88.74 |
| donchian_20      | early_stage   | bracket_20_10 |  36880 |      0.19 |  30.65 |   48102 |      5474.99 |      0.46 |       0.09 |     1.18 |   16.36 |         514.77 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23410 |      0.21 |  29.42 |   26042 |      2964.11 |      0.47 |       0.10 |     1.22 |   13.90 |         306.52 |
| undercut         | all           | bracket_20_10 |  23161 |      0.23 |  29.38 |   26720 |      3041.28 |      0.47 |       0.13 |     1.26 |   16.90 |         393.92 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  27142 |      0.18 |  29.38 |   19981 |      2274.25 |      0.47 |       0.04 |     1.08 |    4.53 |          80.76 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  70486 |      0.18 |  44.53 |   67927 |      0.47 |       0.09 |     1.19 |   19.65 |
| wf_scan_pullback | all           | bracket_20_10 |  71779 |      0.18 |  44.36 |   70011 |      0.47 |       0.09 |     1.19 |   20.08 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70878 |      0.15 |  43.45 |   67927 |      0.54 |       0.06 |     1.15 |   17.16 |
| wf_scan_pullback | all           | bracket_10_10 |  72176 |      0.14 |  43.30 |   70011 |      0.54 |       0.06 |     1.15 |   17.29 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  61579 |      0.17 |  38.63 |   59013 |      0.48 |       0.12 |     1.25 |   23.84 |
| donchian_20      | all           | bracket_20_10 |  69894 |      0.16 |  38.17 |   79590 |      0.45 |       0.07 |     1.14 |   16.43 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61971 |      0.13 |  37.64 |   59013 |      0.55 |       0.08 |     1.21 |   21.58 |
| pocket_pivot     | all           | bracket_20_10 |  48753 |      0.19 |  37.42 |   48748 |      0.46 |       0.06 |     1.13 |   11.70 |
| pocket_pivot     | all           | bracket_10_10 |  49161 |      0.15 |  37.23 |   48748 |      0.53 |       0.05 |     1.11 |   11.20 |
| donchian_20      | all           | bracket_10_10 |  70339 |      0.13 |  36.53 |   79590 |      0.53 |       0.05 |     1.11 |   13.69 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57913 |      0.17 |  35.98 |   62682 |      0.45 |       0.07 |     1.14 |   14.45 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  50461 |      0.17 |  35.62 |   47878 |      0.46 |       0.08 |     1.16 |   14.03 |
| donchian_20      | mkt_ok        | bracket_10_10 |  58311 |      0.13 |  34.14 |   62682 |      0.53 |       0.05 |     1.11 |   12.07 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50799 |      0.13 |  33.99 |   47878 |      0.54 |       0.05 |     1.12 |   11.92 |
| wf_scan_base     | all           | bracket_20_10 |  31867 |      0.19 |  33.59 |   25089 |      0.48 |       0.04 |     1.10 |    6.34 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  36204 |      0.15 |  33.51 |   32529 |      0.54 |       0.05 |     1.12 |    9.43 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35886 |      0.19 |  33.08 |   32529 |      0.46 |       0.06 |     1.13 |    9.72 |
| donchian_20      | wf_scan       | bracket_20_10 |  43267 |      0.17 |  32.62 |   41670 |      0.46 |       0.06 |     1.11 |    9.44 |
| wf_scan_base     | all           | bracket_10_10 |  32085 |      0.16 |  32.48 |   25089 |      0.53 |       0.04 |     1.09 |    6.53 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35472 |      0.18 |  32.12 |   34199 |      0.46 |       0.06 |     1.12 |    9.01 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  25142 |      0.20 |  31.81 |   17699 |      0.48 |       0.04 |     1.09 |    5.04 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35824 |      0.15 |  31.79 |   34199 |      0.53 |       0.05 |     1.11 |    9.05 |
| donchian_20      | wf_scan       | bracket_10_10 |  43569 |      0.14 |  31.69 |   41670 |      0.53 |       0.03 |     1.07 |    6.88 |
| donchian_55      | all           | bracket_20_10 |  47683 |      0.16 |  31.67 |   51592 |      0.45 |       0.06 |     1.11 |   10.59 |
| donchian_55      | all           | bracket_10_10 |  48044 |      0.13 |  31.40 |   51592 |      0.53 |       0.03 |     1.07 |    7.16 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25317 |      0.16 |  30.78 |   17699 |      0.54 |       0.04 |     1.11 |    6.48 |
| donchian_20      | early_stage   | bracket_20_10 |  36880 |      0.19 |  30.65 |   48102 |      0.46 |       0.09 |     1.18 |   16.36 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23410 |      0.21 |  29.42 |   26042 |      0.47 |       0.10 |     1.22 |   13.90 |
| undercut         | all           | bracket_20_10 |  23161 |      0.23 |  29.38 |   26720 |      0.47 |       0.13 |     1.26 |   16.90 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  27142 |      0.18 |  29.38 |   19981 |      0.47 |       0.04 |     1.08 |    4.53 |

## 4. Each entry with its best in-sample exit/filter

| entry              | filter           | exit          |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-------------------|:-----------------|:--------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| ep_gap15           | rs80_mkt         | bracket_20_10 |     68 |        5.67 |     0.54 |      0.54 |   3.17 |     152 |        17.30 |      0.44 |       0.24 |     1.43 |    2.05 |           4.15 |
| flag_30            | rs80_early_theme | bracket_20_10 |    135 |       11.26 |     0.50 |      0.35 |   2.89 |     215 |        24.47 |      0.42 |       0.21 |     1.36 |    2.07 |           5.14 |
| flag_30_early      | wf_scan_green    | bracket_20_10 |    582 |       48.52 |     0.42 |      0.16 |   2.79 |    1039 |       118.26 |      0.43 |       0.18 |     1.32 |    4.14 |          21.68 |
| ep_gap8_neglected  | wf_scan_green    | bracket_10_10 |    165 |       13.76 |     0.69 |      0.35 |   5.10 |     213 |        24.24 |      0.58 |       0.16 |     1.40 |    2.39 |           3.86 |
| ep_gap10_vol5      | wf_scan_green    | bracket_10_10 |    145 |       12.09 |     0.66 |      0.30 |   3.87 |     181 |        20.60 |      0.58 |       0.16 |     1.39 |    2.16 |           3.23 |
| falling_wedge      | all              | bracket_20_10 |   1283 |      106.97 |     0.57 |      0.30 |   9.13 |    1567 |       178.36 |      0.48 |       0.16 |     1.34 |    5.05 |          27.81 |
| ep_gap10_vol2      | wf_scan_green    | bracket_10_10 |    219 |       18.26 |     0.63 |      0.25 |   3.83 |     399 |        45.41 |      0.58 |       0.15 |     1.36 |    3.01 |           6.77 |
| ep_gap10           | wf_scan_green    | bracket_10_10 |    202 |       16.84 |     0.62 |      0.23 |   3.43 |     332 |        37.79 |      0.57 |       0.14 |     1.33 |    2.57 |           5.25 |
| tc_supertrend_ema  | all              | bracket_20_10 |  18970 |     1581.56 |     0.53 |      0.21 |  24.58 |   23343 |      2656.91 |      0.47 |       0.14 |     1.28 |   16.59 |         368.36 |
| undercut           | all              | bracket_20_10 |  23161 |     1930.96 |     0.54 |      0.23 |  29.38 |   26720 |      3041.28 |      0.47 |       0.13 |     1.26 |   16.90 |         393.92 |
| desc_triangle      | all              | bracket_20_10 |    769 |       64.11 |     0.57 |      0.24 |   6.06 |     722 |        82.18 |      0.48 |       0.11 |     1.25 |    2.58 |           9.28 |
| random_uptrend     | all              | bracket_20_10 |  30882 |     2574.67 |     0.53 |      0.19 |  29.27 |   34624 |      3940.92 |      0.46 |       0.09 |     1.19 |   14.09 |         372.95 |
| wf_scan_pullback   | wf_scan          | bracket_20_10 |  70486 |     5876.51 |     0.54 |      0.18 |  44.53 |   67927 |      7731.49 |      0.47 |       0.09 |     1.19 |   19.65 |         694.26 |
| base_25            | mkt_ok           | bracket_20_10 |   1503 |      125.31 |     0.46 |      0.14 |   4.20 |    1917 |       218.19 |      0.42 |       0.08 |     1.14 |    2.71 |          18.52 |
| ep_gap5            | wf_scan_green    | bracket_10_10 |    859 |       71.62 |     0.63 |      0.23 |   7.13 |     923 |       105.06 |      0.55 |       0.08 |     1.19 |    2.61 |           8.87 |
| ep_gap8_hold       | wf_scan_green    | bracket_10_10 |    303 |       25.26 |     0.64 |      0.26 |   4.74 |     437 |        49.74 |      0.55 |       0.08 |     1.18 |    1.69 |           3.99 |
| ema_retest         | all              | bracket_20_10 |  14525 |     1210.97 |     0.55 |      0.19 |  20.96 |   15924 |      1812.48 |      0.46 |       0.08 |     1.15 |    7.92 |         138.21 |
| donchian_20        | all              | bracket_20_10 |  69894 |     5827.16 |     0.52 |      0.16 |  38.17 |   79590 |      9058.97 |      0.45 |       0.07 |     1.14 |   16.43 |         655.24 |
| asc_triangle       | all              | bracket_20_10 |   1093 |       91.12 |     0.57 |      0.19 |   6.03 |     876 |        99.71 |      0.47 |       0.07 |     1.15 |    1.79 |           7.02 |
| flag_60            | rs80_theme       | bracket_20_10 |    144 |       12.01 |     0.48 |      0.34 |   2.75 |     260 |        29.59 |      0.38 |       0.07 |     1.10 |    0.73 |           2.03 |
| sym_triangle       | all              | bracket_10_10 |    890 |       74.20 |     0.58 |      0.12 |   3.67 |     931 |       105.97 |      0.55 |       0.07 |     1.16 |    2.10 |           7.07 |
| pocket_pivot       | all              | bracket_20_10 |  48753 |     4064.60 |     0.54 |      0.19 |  37.42 |   48748 |      5548.52 |      0.46 |       0.06 |     1.13 |   11.70 |         353.01 |
| donchian_55        | all              | bracket_20_10 |  47683 |     3975.40 |     0.53 |      0.16 |  31.67 |   51592 |      5872.23 |      0.45 |       0.06 |     1.11 |   10.59 |         335.37 |
| qull_breakout      | wf_scan_green    | bracket_10_10 |    905 |       75.45 |     0.57 |      0.14 |   3.92 |    2011 |       228.89 |      0.53 |       0.05 |     1.10 |    2.15 |          11.54 |
| wf_rocket_gap      | wf_scan_green    | bracket_10_10 |   1253 |      104.46 |     0.60 |      0.19 |   6.99 |    1483 |       168.80 |      0.54 |       0.05 |     1.11 |    1.93 |           8.28 |
| qull_breakout_60   | wf_scan_green    | bracket_10_10 |    356 |       29.68 |     0.56 |      0.14 |   2.31 |     999 |       113.71 |      0.53 |       0.05 |     1.10 |    1.46 |           5.57 |
| wf_scan_base       | all              | bracket_20_10 |  31867 |     2656.80 |     0.57 |      0.19 |  33.59 |   25089 |      2855.64 |      0.48 |       0.04 |     1.10 |    6.34 |         125.87 |
| wf_rocket_breakout | all              | bracket_10_10 |   2433 |      202.84 |     0.61 |      0.16 |   8.91 |    2527 |       287.62 |      0.54 |       0.04 |     1.09 |    2.12 |          11.75 |
| tc_ema_cross_base  | all              | bracket_20_10 |   7364 |      613.95 |     0.54 |      0.17 |  13.68 |    6977 |       794.13 |      0.45 |       0.03 |     1.07 |    2.42 |          26.73 |
| high52_fresh       | all              | bracket_10_10 |   8217 |      685.06 |     0.61 |      0.17 |  16.97 |    8556 |       973.85 |      0.53 |       0.03 |     1.08 |    3.22 |          32.59 |
| high52             | all              | bracket_10_10 |  30218 |     2519.32 |     0.59 |      0.14 |  26.50 |   29613 |      3370.57 |      0.52 |       0.02 |     1.05 |    3.92 |          73.62 |
| tight_coil_7       | wf_scan          | bracket_10_10 |   4742 |      395.35 |     0.60 |      0.17 |  13.45 |    3661 |       416.70 |      0.52 |       0.02 |     1.05 |    1.33 |           8.73 |
| rising_wedge       | all              | bracket_10_10 |   2105 |      175.50 |     0.58 |      0.12 |   6.46 |    1756 |       199.87 |      0.52 |       0.02 |     1.05 |    0.87 |           3.94 |
| base_50            | all              | bracket_10_10 |   2336 |      194.76 |     0.56 |      0.10 |   5.05 |    2716 |       309.14 |      0.52 |       0.02 |     1.04 |    1.01 |           6.05 |
| vcp                | wf_scan          | bracket_20_10 |   1169 |       97.46 |     0.55 |      0.18 |   5.74 |     725 |        82.52 |      0.45 |       0.01 |     1.02 |    0.26 |           0.89 |
| multi_touch        | all              | bracket_10_10 |  12633 |     1053.23 |     0.59 |      0.14 |  16.83 |   10780 |      1226.99 |      0.51 |       0.00 |     1.00 |    0.05 |           0.57 |
| tc_ema200_2nd      | mkt_ok           | bracket_10_10 |    766 |       63.86 |     0.57 |      0.12 |   3.50 |    1073 |       122.13 |      0.50 |      -0.01 |     0.99 |   -0.17 |          -0.61 |
| stage2             | all              | bracket_10_10 |   6004 |      500.56 |     0.61 |      0.18 |  15.70 |    4908 |       558.63 |      0.51 |      -0.01 |     0.99 |   -0.41 |          -3.06 |
| tc_reversal_base   | mkt_ok           | bracket_10_10 |    154 |       12.84 |     0.72 |      0.45 |   5.67 |     134 |        15.25 |      0.50 |      -0.02 |     0.96 |   -0.25 |          -0.35 |
| tight_coil_15      | wf_scan          | bracket_10_10 |    891 |       74.28 |     0.62 |      0.19 |   6.39 |     690 |        78.54 |      0.49 |      -0.04 |     0.92 |   -1.05 |          -3.00 |
| htf                | all              | sma50_close   |     53 |        4.42 |     0.17 |      0.39 |   0.63 |     103 |        11.72 |      0.11 |      -0.37 |     0.62 |   -1.31 |          -4.30 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |           -0.03 |           -0.02 |              0.06 |             0.06 |          0.02 |           0.09 |         0.06 |         0.02 |         0.00 |          0.01 |       0.09 |        0.03 |         -0.03 |
| base_25            |           -0.03 |            0.01 |              0.08 |             0.07 |          0.08 |           0.07 |         0.07 |         0.02 |         0.05 |          0.21 |       0.11 |        0.18 |          0.19 |
| base_50            |           -0.04 |           -0.01 |              0.13 |             0.09 |          0.11 |           0.10 |         0.09 |         0.05 |         0.08 |          0.20 |       0.13 |        0.18 |          0.20 |
| desc_triangle      |            0.02 |            0.02 |              0.25 |             0.23 |          0.20 |           0.19 |         0.26 |         0.12 |         0.18 |          0.06 |       0.17 |        0.06 |          0.13 |
| donchian_20        |           -0.01 |           -0.02 |              0.08 |             0.07 |          0.08 |           0.10 |         0.07 |         0.06 |         0.07 |          0.06 |       0.10 |        0.06 |          0.05 |
| donchian_55        |           -0.03 |           -0.04 |              0.05 |             0.04 |          0.05 |           0.07 |         0.04 |         0.04 |         0.04 |          0.06 |       0.09 |        0.05 |          0.03 |
| ema_retest         |           -0.02 |           -0.02 |              0.05 |             0.04 |          0.06 |           0.08 |         0.07 |         0.05 |         0.04 |          0.06 |       0.08 |        0.07 |          0.04 |
| ep_gap10           |           -0.04 |            0.01 |              0.21 |             0.31 |          0.24 |           0.18 |         0.12 |         0.08 |         0.14 |          0.48 |       0.28 |        0.41 |          0.49 |
| ep_gap10_vol2      |           -0.03 |            0.05 |              0.27 |             0.32 |          0.24 |           0.17 |         0.18 |         0.10 |         0.15 |          0.47 |       0.28 |        0.41 |          0.51 |
| ep_gap10_vol5      |           -0.07 |            0.02 |              0.22 |             0.29 |          0.19 |           0.18 |         0.10 |         0.05 |         0.09 |          0.49 |       0.30 |        0.40 |          0.47 |
| ep_gap15           |            0.01 |            0.12 |              0.26 |             0.29 |          0.23 |           0.24 |         0.25 |         0.09 |         0.12 |          0.69 |       0.35 |        0.58 |          0.75 |
| ep_gap5            |           -0.04 |           -0.01 |              0.13 |             0.15 |          0.14 |           0.11 |         0.08 |         0.06 |         0.09 |          0.20 |       0.14 |        0.17 |          0.17 |
| ep_gap8_hold       |           -0.03 |            0.01 |              0.15 |             0.23 |          0.19 |           0.14 |         0.11 |         0.06 |         0.11 |          0.37 |       0.23 |        0.32 |          0.36 |
| ep_gap8_neglected  |           -0.04 |           -0.02 |              0.11 |             0.14 |          0.20 |           0.17 |         0.15 |         0.07 |         0.10 |          0.27 |       0.21 |        0.27 |          0.28 |
| falling_wedge      |            0.04 |            0.06 |              0.18 |             0.14 |          0.09 |           0.19 |         0.19 |         0.05 |         0.07 |          0.02 |       0.07 |        0.03 |         -0.00 |
| flag_30            |           -0.05 |            0.01 |              0.02 |             0.08 |          0.10 |           0.04 |        -0.01 |         0.04 |         0.05 |          0.23 |       0.11 |        0.16 |          0.18 |
| flag_30_early      |            0.01 |            0.11 |              0.19 |             0.18 |          0.19 |           0.16 |         0.22 |         0.14 |         0.14 |          0.28 |       0.19 |        0.26 |          0.41 |
| flag_60            |           -0.06 |            0.05 |              0.14 |             0.12 |          0.13 |           0.07 |         0.07 |         0.09 |         0.07 |          0.48 |       0.26 |        0.34 |          0.33 |
| high52             |           -0.04 |           -0.05 |             -0.06 |            -0.06 |         -0.04 |          -0.03 |        -0.06 |        -0.05 |        -0.06 |         -0.05 |      -0.04 |       -0.04 |         -0.07 |
| high52_fresh       |           -0.03 |           -0.04 |              0.05 |             0.03 |          0.07 |           0.05 |         0.04 |         0.02 |         0.03 |          0.07 |       0.06 |        0.06 |          0.04 |
| htf                |           -0.26 |           -0.20 |             -0.24 |            -0.34 |         -0.17 |          -0.19 |        -0.23 |        -0.05 |        -0.12 |         -0.34 |      -0.12 |       -0.30 |         -0.34 |
| multi_touch        |           -0.06 |           -0.09 |             -0.05 |            -0.01 |         -0.03 |          -0.00 |        -0.06 |        -0.01 |        -0.02 |         -0.06 |      -0.02 |       -0.05 |         -0.09 |
| pocket_pivot       |           -0.01 |           -0.03 |             -0.04 |            -0.04 |         -0.02 |          -0.00 |        -0.04 |        -0.02 |        -0.02 |         -0.05 |      -0.02 |       -0.05 |         -0.06 |
| qull_breakout      |           -0.02 |            0.05 |             -0.10 |            -0.11 |         -0.09 |          -0.14 |        -0.12 |        -0.17 |        -0.14 |          0.03 |      -0.11 |       -0.02 |         -0.01 |
| qull_breakout_60   |           -0.01 |            0.09 |             -0.11 |            -0.12 |         -0.08 |          -0.12 |        -0.08 |        -0.16 |        -0.14 |          0.13 |      -0.10 |        0.05 |          0.03 |
| rising_wedge       |           -0.04 |           -0.05 |             -0.04 |            -0.07 |         -0.03 |           0.03 |         0.02 |         0.05 |         0.02 |         -0.07 |      -0.01 |       -0.05 |         -0.10 |
| stage2             |           -0.07 |           -0.09 |             -0.08 |            -0.08 |         -0.07 |          -0.03 |        -0.10 |        -0.05 |        -0.06 |         -0.11 |      -0.07 |       -0.10 |         -0.13 |
| sym_triangle       |            0.00 |           -0.01 |              0.14 |             0.09 |          0.11 |           0.15 |         0.11 |         0.10 |         0.12 |          0.02 |       0.07 |        0.04 |          0.03 |
| tc_ema200_2nd      |           -0.04 |           -0.06 |              0.07 |             0.07 |          0.04 |           0.08 |         0.06 |         0.07 |         0.06 |         -0.00 |       0.05 |       -0.00 |         -0.05 |
| tc_ema_cross_base  |           -0.03 |           -0.06 |              0.07 |             0.08 |          0.09 |           0.11 |         0.08 |         0.07 |         0.08 |          0.06 |       0.12 |        0.07 |          0.03 |
| tc_reversal_base   |           -0.02 |           -0.04 |              0.06 |             0.04 |         -0.04 |           0.12 |         0.05 |        -0.03 |        -0.01 |         -0.05 |       0.06 |       -0.04 |         -0.08 |
| tc_supertrend_ema  |            0.04 |            0.04 |              0.19 |             0.17 |          0.14 |           0.20 |         0.18 |         0.11 |         0.14 |          0.05 |       0.11 |        0.06 |          0.06 |
| tight_coil_15      |           -0.08 |           -0.10 |             -0.01 |            -0.04 |         -0.00 |           0.05 |        -0.02 |         0.04 |         0.02 |         -0.10 |       0.01 |       -0.07 |         -0.12 |
| tight_coil_7       |           -0.05 |           -0.06 |              0.00 |             0.00 |          0.03 |           0.06 |         0.02 |         0.04 |         0.04 |         -0.01 |       0.05 |       -0.01 |         -0.03 |
| undercut           |            0.03 |            0.04 |              0.17 |             0.15 |          0.01 |           0.08 |         0.12 |         0.07 |         0.07 |         -0.01 |       0.01 |       -0.01 |          0.04 |
| vcp                |           -0.01 |           -0.04 |              0.05 |             0.03 |          0.03 |           0.09 |         0.03 |         0.05 |         0.05 |         -0.06 |       0.03 |       -0.04 |         -0.11 |
| wf_rocket_breakout |           -0.02 |           -0.04 |              0.07 |             0.07 |          0.09 |           0.10 |         0.05 |         0.08 |         0.08 |          0.08 |       0.12 |        0.07 |          0.06 |
| wf_rocket_gap      |            0.01 |            0.07 |              0.23 |             0.24 |          0.22 |           0.17 |         0.23 |         0.12 |         0.17 |          0.29 |       0.24 |        0.26 |          0.30 |
| wf_scan_base       |           -0.02 |           -0.05 |              0.08 |             0.06 |          0.08 |           0.10 |         0.07 |         0.07 |         0.07 |          0.02 |       0.09 |        0.03 |         -0.01 |
| wf_scan_pullback   |            0.00 |           -0.00 |              0.09 |             0.07 |          0.06 |           0.10 |         0.09 |         0.06 |         0.07 |          0.03 |       0.08 |        0.04 |          0.02 |

Same, in-sample:

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |            0.01 |           -0.00 |              0.04 |             0.02 |          0.03 |           0.07 |         0.06 |         0.05 |         0.03 |         -0.03 |       0.08 |       -0.02 |         -0.01 |
| base_25            |           -0.07 |           -0.07 |             -0.02 |            -0.02 |          0.01 |           0.09 |        -0.04 |         0.08 |         0.05 |          0.05 |       0.10 |        0.03 |          0.06 |
| base_50            |           -0.04 |           -0.06 |             -0.00 |             0.01 |          0.03 |           0.14 |        -0.03 |         0.09 |         0.06 |         -0.03 |       0.09 |       -0.01 |         -0.04 |
| desc_triangle      |            0.04 |            0.05 |              0.17 |             0.30 |          0.14 |           0.21 |         0.21 |         0.17 |         0.16 |          0.20 |       0.25 |        0.19 |          0.29 |
| donchian_20        |           -0.02 |           -0.03 |              0.10 |             0.11 |          0.14 |           0.16 |         0.10 |         0.11 |         0.12 |          0.12 |       0.18 |        0.11 |          0.14 |
| donchian_55        |           -0.02 |           -0.03 |              0.08 |             0.09 |          0.11 |           0.14 |         0.08 |         0.09 |         0.10 |          0.10 |       0.17 |        0.10 |          0.12 |
| ema_retest         |            0.00 |            0.00 |              0.08 |             0.09 |          0.12 |           0.13 |         0.16 |         0.07 |         0.07 |          0.15 |       0.13 |        0.15 |          0.16 |
| ep_gap10           |           -0.03 |           -0.01 |              0.14 |             0.10 |          0.14 |           0.12 |        -0.05 |         0.14 |         0.10 |          0.16 |       0.22 |        0.12 |          0.11 |
| ep_gap10_vol2      |           -0.05 |           -0.05 |              0.12 |             0.06 |          0.11 |           0.11 |        -0.05 |         0.11 |         0.08 |          0.11 |       0.18 |        0.09 |          0.07 |
| ep_gap10_vol5      |            0.03 |            0.05 |              0.22 |             0.18 |          0.17 |           0.21 |         0.02 |         0.23 |         0.18 |          0.28 |       0.33 |        0.24 |          0.17 |
| ep_gap15           |            0.07 |            0.12 |              0.41 |             0.31 |          0.33 |           0.32 |         0.10 |         0.32 |         0.30 |          0.41 |       0.48 |        0.36 |          0.31 |
| ep_gap5            |           -0.02 |           -0.04 |              0.16 |             0.12 |          0.16 |           0.16 |         0.08 |         0.14 |         0.13 |          0.23 |       0.22 |        0.20 |          0.22 |
| ep_gap8_hold       |           -0.01 |            0.01 |              0.22 |             0.21 |          0.23 |           0.19 |         0.11 |         0.18 |         0.16 |          0.27 |       0.31 |        0.25 |          0.27 |
| ep_gap8_neglected  |            0.01 |            0.04 |              0.24 |             0.24 |          0.23 |           0.19 |         0.17 |         0.16 |         0.19 |          0.29 |       0.28 |        0.28 |          0.30 |
| falling_wedge      |            0.06 |            0.11 |              0.31 |             0.35 |          0.22 |           0.30 |         0.38 |         0.22 |         0.23 |          0.13 |       0.20 |        0.13 |          0.25 |
| flag_30            |           -0.15 |           -0.16 |             -0.10 |            -0.10 |         -0.07 |           0.06 |        -0.12 |         0.03 |        -0.03 |         -0.10 |       0.01 |       -0.09 |         -0.15 |
| flag_30_early      |           -0.09 |           -0.11 |              0.12 |             0.09 |          0.11 |           0.06 |        -0.03 |         0.07 |         0.10 |         -0.00 |       0.04 |        0.01 |          0.03 |
| flag_60            |           -0.14 |           -0.14 |              0.07 |             0.05 |          0.07 |           0.13 |        -0.02 |         0.16 |         0.10 |          0.09 |       0.13 |        0.10 |          0.01 |
| high52             |           -0.01 |           -0.03 |             -0.03 |            -0.04 |          0.01 |           0.03 |        -0.02 |        -0.01 |        -0.01 |         -0.03 |       0.01 |       -0.03 |         -0.03 |
| high52_fresh       |            0.02 |            0.01 |              0.05 |             0.06 |          0.08 |           0.09 |         0.08 |         0.05 |         0.06 |          0.07 |       0.08 |        0.07 |          0.05 |
| htf                |           -0.23 |           -0.17 |             -0.09 |             0.24 |          0.12 |           0.07 |        -0.10 |         0.13 |         0.19 |          0.42 |       0.27 |        0.23 |          0.41 |
| multi_touch        |           -0.01 |           -0.03 |              0.07 |             0.09 |          0.11 |           0.11 |         0.11 |         0.08 |         0.07 |          0.12 |       0.11 |        0.12 |          0.12 |
| pocket_pivot       |            0.00 |           -0.00 |              0.04 |             0.06 |          0.07 |           0.04 |         0.05 |         0.04 |         0.04 |          0.07 |       0.05 |        0.06 |          0.08 |
| qull_breakout      |           -0.15 |           -0.18 |             -0.33 |            -0.32 |         -0.27 |          -0.20 |        -0.36 |        -0.17 |        -0.20 |         -0.35 |      -0.23 |       -0.33 |         -0.35 |
| qull_breakout_60   |           -0.15 |           -0.18 |             -0.24 |            -0.27 |         -0.24 |          -0.22 |        -0.34 |        -0.15 |        -0.18 |         -0.28 |      -0.19 |       -0.26 |         -0.30 |
| rising_wedge       |           -0.02 |           -0.04 |              0.00 |             0.02 |          0.05 |           0.08 |        -0.01 |         0.04 |         0.03 |          0.02 |       0.11 |        0.03 |          0.04 |
| stage2             |            0.03 |            0.02 |              0.11 |             0.14 |          0.16 |           0.12 |         0.17 |         0.08 |         0.10 |          0.15 |       0.15 |        0.15 |          0.15 |
| sym_triangle       |           -0.03 |           -0.06 |              0.07 |             0.08 |          0.11 |           0.10 |        -0.01 |         0.11 |         0.09 |          0.04 |       0.11 |        0.03 |          0.03 |
| tc_ema200_2nd      |           -0.05 |           -0.08 |              0.08 |             0.12 |          0.14 |           0.17 |         0.07 |         0.15 |         0.13 |          0.06 |       0.15 |        0.06 |          0.08 |
| tc_ema_cross_base  |           -0.01 |           -0.02 |              0.11 |             0.14 |          0.14 |           0.15 |         0.14 |         0.12 |         0.12 |          0.14 |       0.23 |        0.14 |          0.17 |
| tc_reversal_base   |            0.25 |            0.28 |              0.24 |             0.28 |          0.27 |           0.41 |         0.45 |         0.31 |         0.23 |          0.31 |       0.40 |        0.30 |          0.32 |
| tc_supertrend_ema  |            0.00 |            0.02 |              0.21 |             0.22 |          0.18 |           0.25 |         0.20 |         0.17 |         0.18 |          0.09 |       0.19 |        0.09 |          0.15 |
| tight_coil_15      |            0.00 |           -0.01 |              0.14 |             0.18 |          0.12 |           0.17 |         0.15 |         0.14 |         0.12 |          0.12 |       0.23 |        0.12 |          0.18 |
| tight_coil_7       |            0.01 |           -0.01 |              0.12 |             0.17 |          0.14 |           0.17 |         0.12 |         0.12 |         0.11 |          0.16 |       0.23 |        0.15 |          0.19 |
| undercut           |            0.02 |            0.04 |              0.21 |             0.23 |          0.05 |           0.14 |         0.20 |         0.19 |         0.18 |          0.01 |       0.08 |        0.01 |          0.09 |
| vcp                |           -0.02 |           -0.03 |              0.07 |             0.08 |          0.11 |           0.14 |         0.10 |         0.11 |         0.09 |          0.08 |       0.17 |        0.08 |          0.11 |
| wf_rocket_breakout |            0.02 |            0.01 |              0.12 |             0.13 |          0.17 |           0.21 |         0.14 |         0.14 |         0.16 |          0.14 |       0.24 |        0.14 |          0.15 |
| wf_rocket_gap      |           -0.04 |           -0.05 |              0.12 |             0.10 |          0.12 |           0.15 |         0.08 |         0.14 |         0.12 |          0.14 |       0.19 |        0.13 |          0.11 |
| wf_scan_base       |            0.01 |            0.00 |              0.10 |             0.12 |          0.15 |           0.18 |         0.14 |         0.14 |         0.14 |          0.10 |       0.21 |        0.10 |          0.12 |
| wf_scan_pullback   |           -0.00 |           -0.01 |              0.14 |             0.15 |          0.13 |           0.18 |         0.13 |         0.13 |         0.13 |          0.09 |       0.18 |        0.08 |          0.12 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| wf_weekly10     |      0.08 |       0.10 |      0.26 |     1.14 |                       0.62 |
| sma50_close     |      0.07 |       0.09 |      0.27 |     1.13 |                       0.70 |
| bracket_20_10   |      0.17 |       0.09 |      0.44 |     1.16 |                       0.40 |
| wf_rocket       |      0.06 |       0.06 |      0.27 |     1.10 |                       0.68 |
| oneil_20_8      |      0.13 |       0.04 |      0.28 |     1.06 |                       0.78 |
| bracket_10_10   |      0.13 |       0.03 |      0.53 |     1.08 |                       0.23 |
| trim_ema        |      0.01 |       0.01 |      0.34 |     1.03 |                       0.80 |
| donchian_10low  |      0.03 |       0.01 |      0.30 |     1.03 |                       0.78 |
| chandelier_3atr |      0.04 |       0.00 |      0.30 |     1.01 |                       0.78 |
| fixed_3r_20d    |      0.01 |      -0.01 |      0.38 |     1.01 |                       0.82 |
| ema21_close     |     -0.03 |      -0.02 |      0.30 |     0.96 |                       0.75 |
| qull_sma20      |     -0.04 |      -0.03 |      0.43 |     0.94 |                       0.80 |
| qull_sma10      |     -0.04 |      -0.04 |      0.43 |     0.92 |                       0.80 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| qull_scan_regime |     -0.01 |       0.14 |      0.34 |
| rs80_early       |      0.11 |       0.13 |      0.37 |
| qull_scan        |     -0.02 |       0.10 |      0.34 |
| rs80_early_theme |      0.08 |       0.09 |      0.36 |
| early_stage      |      0.08 |       0.08 |      0.36 |
| wf_scan_green    |      0.06 |       0.07 |      0.36 |
| wf_rocket_green  |      0.04 |       0.06 |      0.35 |
| rs80             |      0.05 |       0.05 |      0.35 |
| wf_rocket        |      0.01 |       0.04 |      0.35 |
| rs80_mkt         |      0.07 |       0.04 |      0.34 |
| wf_scan          |      0.06 |       0.04 |      0.35 |
| rs80_theme       |      0.05 |       0.03 |      0.35 |
| all              |      0.05 |       0.02 |      0.35 |
| theme            |      0.05 |       0.02 |      0.35 |
| mkt_ok           |      0.06 |       0.02 |      0.34 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.002; AUC for R > 0: 0.505 (0.5 = no skill). Taken (model's top third, causal threshold): n=122,276, avgR=0.082, win=0.463. Skipped: n=325,072, avgR=0.074, win=0.452.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 44740.00 |   0.10 |  0.45 |
|      1 | 44730.00 |   0.10 |  0.46 |
|      2 | 44735.00 |   0.07 |  0.45 |
|      3 | 44734.00 |   0.06 |  0.45 |
|      4 | 44735.00 |   0.07 |  0.45 |
|      5 | 44735.00 |   0.07 |  0.46 |
|      6 | 44735.00 |   0.07 |  0.46 |
|      7 | 44734.00 |   0.06 |  0.45 |
|      8 | 44735.00 |   0.05 |  0.45 |
|      9 | 44735.00 |   0.10 |  0.47 |

Per entry (OOS):

| entry_name         |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:-------------------|---------:|-----------:|----------:|-------------:|---------------:|
| flag_60            |   639.00 |       0.14 |    163.00 |         0.28 |           0.09 |
| wf_rocket_gap      |  4040.00 |       0.17 |   1200.00 |         0.28 |           0.12 |
| qull_breakout_60   |  1947.00 |       0.19 |    454.00 |         0.26 |           0.17 |
| ep_gap15           |   391.00 |       0.22 |    200.00 |         0.21 |           0.23 |
| base_25            |  2490.00 |       0.10 |    643.00 |         0.20 |           0.07 |
| flag_30_early      |  2012.00 |       0.20 |    458.00 |         0.19 |           0.20 |
| ep_gap8_neglected  |   955.00 |       0.08 |    366.00 |         0.18 |           0.01 |
| flag_30            |  1849.00 |       0.11 |    432.00 |         0.18 |           0.08 |
| ep_gap10_vol2      |  1217.00 |       0.15 |    492.00 |         0.17 |           0.13 |
| falling_wedge      |  1567.00 |       0.16 |    563.00 |         0.17 |           0.15 |
| undercut           | 26720.00 |       0.13 |   9362.00 |         0.16 |           0.11 |
| ep_gap8_hold       |  1214.00 |       0.11 |    487.00 |         0.15 |           0.07 |
| ep_gap10           |   962.00 |       0.11 |    404.00 |         0.15 |           0.08 |
| base_50            |  2716.00 |       0.09 |    756.00 |         0.14 |           0.07 |
| ep_gap5            |  2384.00 |       0.08 |    872.00 |         0.14 |           0.05 |
| qull_breakout      |  4553.00 |       0.15 |   1093.00 |         0.12 |           0.15 |
| tc_reversal_base   |   160.00 |       0.05 |     47.00 |         0.12 |           0.02 |
| rising_wedge       |  1756.00 |       0.05 |    485.00 |         0.11 |           0.02 |
| tc_supertrend_ema  | 23343.00 |       0.14 |   8352.00 |         0.10 |           0.16 |
| desc_triangle      |   722.00 |       0.11 |    220.00 |         0.09 |           0.12 |
| tight_coil_7       |  5433.00 |       0.03 |   1391.00 |         0.08 |           0.02 |
| wf_scan_pullback   | 70011.00 |       0.09 |  18804.00 |         0.08 |           0.10 |
| vcp                |   887.00 |       0.05 |    206.00 |         0.07 |           0.05 |
| sym_triangle       |   931.00 |       0.09 |    237.00 |         0.07 |           0.09 |
| ema_retest         | 15924.00 |       0.08 |   4251.00 |         0.07 |           0.08 |
| donchian_20        | 79590.00 |       0.07 |  20916.00 |         0.06 |           0.08 |
| donchian_55        | 51592.00 |       0.06 |  12642.00 |         0.06 |           0.05 |
| tight_coil_15      |  1049.00 |      -0.00 |    271.00 |         0.06 |          -0.03 |
| high52             | 29613.00 |       0.04 |   6887.00 |         0.06 |           0.04 |
| multi_touch        | 10780.00 |       0.01 |   2946.00 |         0.06 |          -0.01 |
| pocket_pivot       | 48748.00 |       0.06 |  13096.00 |         0.06 |           0.07 |
| wf_scan_base       | 25089.00 |       0.04 |   6057.00 |         0.06 |           0.04 |
| ep_gap10_vol5      |   471.00 |       0.12 |    207.00 |         0.05 |           0.18 |
| stage2             |  4908.00 |       0.01 |   1482.00 |         0.04 |          -0.00 |
| htf                |   103.00 |      -0.10 |     28.00 |         0.04 |          -0.15 |
| high52_fresh       |  8556.00 |       0.05 |   2268.00 |         0.03 |           0.06 |
| wf_rocket_breakout |  2527.00 |       0.05 |    756.00 |         0.03 |           0.06 |
| tc_ema200_2nd      |  1646.00 |       0.04 |    479.00 |         0.02 |           0.04 |
| tc_ema_cross_base  |  6977.00 |       0.03 |   2039.00 |         0.02 |           0.04 |
| asc_triangle       |   876.00 |       0.07 |    264.00 |        -0.00 |           0.10 |

- Same model on episodic pivots only / sma50_close: rank corr -0.006, taken avgR 0.386 (n=3,436) vs skipped 0.288 (n=4,158).
- Same model on your trim plan (trim_ema): rank corr 0.105, taken avgR 0.009 (n=130,253) vs skipped -0.038 (n=317,095).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature       |   rank_corr_drop |
|:--------------|-----------------:|
| rates_rising  |           0.0140 |
| above_52w_low |           0.0071 |
| adr_pct       |           0.0062 |
| sector_rs     |           0.0056 |
| rs_rank       |           0.0042 |
| sma200_slope  |           0.0041 |
| industry_rs   |           0.0027 |
| mkt_above200  |           0.0020 |
| sma150_slope  |           0.0018 |
| industry_rank |           0.0015 |
| base_count    |           0.0015 |
| mkt_ok        |           0.0013 |
| dist_52w_high |           0.0011 |
| mkt_ret_21    |           0.0010 |
| gap           |           0.0008 |
| close_std_10  |           0.0005 |
| dist_sma50    |           0.0004 |
| atr_ratio     |           0.0004 |
| dist_ema21    |           0.0003 |
| base_depth_60 |           0.0002 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.554    |  12214 |      0.61 |   16827 |       0.08 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.554   |  30770 |      0.33 |   48920 |       0.13 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.429 |  85988 |      0.30 |   67332 |       0.01 |      0.47 |
| rates_rising <= 0.5 AND qqq_ret_21 <= 0.0297 AND breadth_50 > 0.647   |  38836 |      0.26 |   59906 |       0.09 |      0.46 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.429  |  88996 |      0.18 |   64023 |      -0.00 |      0.42 |
| rates_rising <= 0.5 AND qqq_ret_21 <= 0.0297 AND breadth_50 <= 0.647  |  73047 |      0.08 |   68280 |       0.14 |      0.47 |
| rates_rising <= 0.5 AND qqq_ret_21 > 0.0297 AND mkt_ret_21 > 0.0141   |  91663 |      0.04 |  117643 |       0.08 |      0.45 |
| rates_rising <= 0.5 AND qqq_ret_21 > 0.0297 AND mkt_ret_21 <= 0.0141  |   6351 |     -0.47 |    4417 |       0.14 |      0.45 |

## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?

Every stock every 10 trading days (n=285,457 out-of-sample rows). Base rate of a >= 40% gain within 3 months: 7.2%. The model's top 10% hit it 30.4% of the time (4.2x the base rate). AUC 0.834.

|   super_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28546.000 |      0.001 |          -0.005 |              0.011 |              0.069 |
|            1 | 28546.000 |      0.004 |           0.009 |              0.014 |              0.049 |
|            2 | 28545.000 |      0.011 |           0.017 |              0.018 |              0.049 |
|            3 | 28546.000 |      0.014 |           0.021 |              0.021 |              0.053 |
|            4 | 28546.000 |      0.027 |           0.028 |              0.027 |              0.062 |
|            5 | 28545.000 |      0.044 |           0.034 |              0.030 |              0.071 |
|            6 | 28546.000 |      0.063 |           0.041 |              0.035 |              0.083 |
|            7 | 28545.000 |      0.097 |           0.047 |              0.035 |              0.102 |
|            8 | 28546.000 |      0.156 |           0.062 |              0.042 |              0.123 |
|            9 | 28546.000 |      0.304 |           0.108 |              0.066 |              0.160 |

What matters most (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| adr_pct       |     0.0875 |
| above_52w_low |     0.0266 |
| dist_52w_high |     0.0259 |
| atr_pct       |     0.0072 |
| leg1_range    |     0.0054 |
| leg2_range    |     0.0046 |
| mkt_above200  |     0.0035 |
| qull_rank     |     0.0028 |
| tight_10      |     0.0022 |
| sma200_slope  |     0.0019 |
| breadth_50    |     0.0015 |
| base_count    |     0.0008 |
| industry_rs   |     0.0008 |
| sma150_slope  |     0.0007 |
| leg3_range    |     0.0005 |

Profile: future superperformers vs everything else, at the moment of the sample:

|               |   future superperformers (median) |   everything else (median) |
|:--------------|----------------------------------:|---------------------------:|
| adr_pct       |                             0.045 |                      0.026 |
| above_52w_low |                             0.586 |                      0.341 |
| dist_52w_high |                            -0.275 |                     -0.128 |
| atr_pct       |                             0.047 |                      0.027 |
| leg1_range    |                             0.186 |                      0.120 |
| leg2_range    |                             0.194 |                      0.120 |
| mkt_above200  |                             1.000 |                      1.000 |
| qull_rank     |                             0.778 |                      0.708 |
| tight_10      |                             0.154 |                      0.087 |
| sma200_slope  |                             0.000 |                      0.009 |
| breadth_50    |                             0.560 |                      0.604 |
| base_count    |                             0.000 |                      1.000 |

Readable rules (depth-3 tree fit before 2018, scored after):

| rule                                                                  |   IS_n |   IS_rate |   OOS_n |   OOS_rate |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|
| dist_52w_high <= -0.521 AND dist_52w_high <= -0.627                   |   2316 |     0.457 |    1005 |      0.452 |
| dist_52w_high <= -0.521 AND dist_52w_high > -0.627                    |   3529 |     0.259 |    1722 |      0.289 |
| dist_52w_high > -0.521 AND adr_pct > 0.0321 AND above_52w_low > 1.03  |   8618 |     0.142 |    6242 |      0.236 |
| dist_52w_high > -0.521 AND adr_pct > 0.0321 AND above_52w_low <= 1.03 |  36717 |     0.066 |   18335 |      0.128 |
| dist_52w_high > -0.521 AND adr_pct <= 0.0321 AND adr_pct > 0.0251     |  35220 |     0.027 |   18518 |      0.040 |
| dist_52w_high > -0.521 AND adr_pct <= 0.0321 AND adr_pct <= 0.0251    | 113600 |     0.005 |   34178 |      0.009 |

Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate 6.8%, model top 10% 27.5% (4.0x), AUC 0.827.

|   clean_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28546.000 |      0.001 |          -0.004 |              0.011 |              0.065 |
|            1 | 28546.000 |      0.004 |           0.009 |              0.014 |              0.050 |
|            2 | 28545.000 |      0.010 |           0.016 |              0.018 |              0.052 |
|            3 | 28546.000 |      0.016 |           0.021 |              0.021 |              0.055 |
|            4 | 28546.000 |      0.026 |           0.029 |              0.027 |              0.061 |
|            5 | 28545.000 |      0.040 |           0.034 |              0.030 |              0.070 |
|            6 | 28546.000 |      0.061 |           0.040 |              0.033 |              0.083 |
|            7 | 28545.000 |      0.096 |           0.049 |              0.038 |              0.099 |
|            8 | 28546.000 |      0.151 |           0.062 |              0.043 |              0.126 |
|            9 | 28546.000 |      0.275 |           0.105 |              0.062 |              0.160 |

### Your goal: +10% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 50% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28546.000 |       0.270 |        0.397 |      0.334 |            0.006 |           0.019 |
|       1 | 28546.000 |       0.354 |        0.444 |      0.350 |            0.009 |           0.034 |
|       2 | 28545.000 |       0.399 |        0.467 |      0.370 |            0.008 |           0.044 |
|       3 | 28546.000 |       0.435 |        0.474 |      0.393 |            0.007 |           0.046 |
|       4 | 28546.000 |       0.465 |        0.498 |      0.394 |            0.009 |           0.081 |
|       5 | 28545.000 |       0.493 |        0.505 |      0.404 |            0.009 |           0.098 |
|       6 | 28546.000 |       0.521 |        0.512 |      0.411 |            0.009 |           0.098 |
|       7 | 28545.000 |       0.552 |        0.518 |      0.411 |            0.010 |           0.098 |
|       8 | 28546.000 |       0.593 |        0.520 |      0.416 |            0.009 |           0.098 |
|       9 | 28546.000 |       0.678 |        0.526 |      0.426 |            0.008 |           0.098 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 285457.000 |        0.486 |      0.391 |            0.008 |
| top 10%    |  28546.000 |        0.526 |      0.426 |            0.008 |
| top 5%     |  14273.000 |        0.535 |      0.426 |            0.009 |
| top 2%     |   5710.000 |        0.553 |      0.411 |            0.013 |
| top 1%     |   2855.000 |        0.567 |      0.402 |            0.016 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97516.000 |        0.463 |      0.360 |            0.009 |
| top 10%    |  7694.000 |        0.541 |      0.390 |            0.014 |
| top 5%     |  3985.000 |        0.549 |      0.388 |            0.015 |
| top 2%     |  1674.000 |        0.555 |      0.384 |            0.016 |
| top 1%     |   882.000 |        0.567 |      0.390 |            0.018 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 14805.000 |       0.268 |        0.391 |      0.305 |            0.008 |           0.022 |
|       1 | 12929.000 |       0.353 |        0.431 |      0.327 |            0.010 |           0.034 |
|       2 | 11168.000 |       0.399 |        0.446 |      0.347 |            0.009 |           0.036 |
|       3 | 10070.000 |       0.434 |        0.451 |      0.372 |            0.007 |           0.037 |
|       4 |  9132.000 |       0.465 |        0.476 |      0.375 |            0.009 |           0.052 |
|       5 |  8340.000 |       0.492 |        0.483 |      0.384 |            0.009 |           0.057 |
|       6 |  7812.000 |       0.521 |        0.492 |      0.397 |            0.008 |           0.064 |
|       7 |  7853.000 |       0.552 |        0.502 |      0.390 |            0.010 |           0.098 |
|       8 |  7713.000 |       0.593 |        0.516 |      0.387 |            0.011 |           0.098 |
|       9 |  7694.000 |       0.681 |        0.541 |      0.390 |            0.014 |           0.098 |

### Your goal: +20% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 33% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28546.000 |       0.044 |        0.061 |      0.338 |            0.001 |          -0.004 |
|       1 | 28546.000 |       0.078 |        0.110 |      0.363 |            0.007 |          -0.003 |
|       2 | 28545.000 |       0.108 |        0.145 |      0.402 |            0.008 |          -0.010 |
|       3 | 28546.000 |       0.138 |        0.179 |      0.435 |            0.009 |          -0.020 |
|       4 | 28546.000 |       0.171 |        0.223 |      0.449 |            0.013 |          -0.026 |
|       5 | 28545.000 |       0.206 |        0.262 |      0.472 |            0.016 |          -0.037 |
|       6 | 28546.000 |       0.243 |        0.291 |      0.494 |            0.017 |          -0.068 |
|       7 | 28545.000 |       0.285 |        0.324 |      0.512 |            0.020 |          -0.102 |
|       8 | 28546.000 |       0.335 |        0.344 |      0.535 |            0.019 |          -0.102 |
|       9 | 28546.000 |       0.441 |        0.364 |      0.553 |            0.020 |          -0.102 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 285457.000 |        0.230 |      0.455 |            0.013 |
| top 10%    |  28546.000 |        0.364 |      0.553 |            0.020 |
| top 5%     |  14273.000 |        0.365 |      0.564 |            0.018 |
| top 2%     |   5710.000 |        0.367 |      0.578 |            0.016 |
| top 1%     |   2855.000 |        0.379 |      0.578 |            0.018 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97516.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5097.000 |        0.366 |      0.512 |            0.026 |
| top 5%     |  2608.000 |        0.380 |      0.515 |            0.028 |
| top 2%     |  1106.000 |        0.380 |      0.548 |            0.023 |
| top 1%     |   587.000 |        0.409 |      0.538 |            0.029 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 17085.000 |       0.044 |        0.060 |      0.316 |            0.004 |           0.002 |
|       1 | 14652.000 |       0.078 |        0.107 |      0.345 |            0.011 |           0.003 |
|       2 | 12825.000 |       0.108 |        0.140 |      0.381 |            0.011 |          -0.004 |
|       3 | 11377.000 |       0.138 |        0.165 |      0.425 |            0.009 |          -0.015 |
|       4 |  9527.000 |       0.171 |        0.210 |      0.425 |            0.015 |          -0.015 |
|       5 |  8238.000 |       0.205 |        0.237 |      0.447 |            0.017 |          -0.015 |
|       6 |  7207.000 |       0.243 |        0.266 |      0.458 |            0.019 |          -0.023 |
|       7 |  6118.000 |       0.285 |        0.301 |      0.479 |            0.021 |          -0.040 |
|       8 |  5390.000 |       0.334 |        0.325 |      0.501 |            0.022 |          -0.102 |
|       9 |  5097.000 |       0.445 |        0.366 |      0.512 |            0.026 |          -0.102 |

Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that survived. See the SURVIVORSHIP and CHECK rows in section 9.

Setup signals split by the model's score (OOS, exit bracket_20_10; last column sma50_close):

| super_prob   |          n |   avgR |   win |   avgR_sma50 |
|:-------------|-----------:|-------:|------:|-------------:|
| low          | 149116.000 |  0.013 | 0.485 |       -0.071 |
| mid          | 149116.000 |  0.076 | 0.458 |       -0.048 |
| high         | 149116.000 |  0.138 | 0.422 |        0.143 |

## 12. Short horizons: green day / next day / 3 days / week (out-of-sample 2018+)

Features: candle anatomy, gaps and fair value gaps, relative volume, round numbers / moving averages / swing support & resistance / 20-day trend line, completed-week structure, VIX (level, change, percentile, VIX/VIX3M), plus everything the earlier models use. Market-only = market + VIX + calendar features only. Retrained every 2 years. 'top/bottom' = actual up-rate in the model's highest/lowest 10%; spread = their difference in average return over the horizon.

| target                         | model   |   base rate |   AUC |   accuracy |   top 10% up |   bottom 10% up |   return spread |
|:-------------------------------|:--------|------------:|------:|-----------:|-------------:|----------------:|----------------:|
| next day green (close > open)  | all     |       0.493 | 0.519 |      0.513 |        0.523 |           0.476 |           0.006 |
| next day green (close > open)  | market  |       0.493 | 0.517 |      0.511 |        0.531 |           0.538 |          -0.000 |
| up next day (close to close)   | all     |       0.500 | 0.510 |      0.509 |        0.524 |           0.506 |           0.003 |
| up next day (close to close)   | market  |       0.500 | 0.493 |      0.484 |        0.476 |           0.499 |          -0.003 |
| up over the next 3 days        | all     |       0.509 | 0.524 |      0.520 |        0.529 |           0.467 |           0.005 |
| up over the next 3 days        | market  |       0.509 | 0.521 |      0.525 |        0.533 |           0.504 |           0.001 |
| up over the next week (5 days) | all     |       0.514 | 0.505 |      0.508 |        0.521 |           0.504 |          -0.001 |
| up over the next week (5 days) | market  |       0.514 | 0.512 |      0.515 |        0.532 |           0.496 |           0.003 |

Up over the next week, by decile of the full model:

|   s_up5 |          n |   predicted |   actual_up |   avg_return |
|--------:|-----------:|------------:|------------:|-------------:|
|       0 | 29437.0000 |      0.3471 |      0.5044 |      -0.0004 |
|       1 | 29437.0000 |      0.4270 |      0.5186 |       0.0020 |
|       2 | 29437.0000 |      0.4640 |      0.5075 |       0.0021 |
|       3 | 29436.0000 |      0.4918 |      0.4980 |       0.0016 |
|       4 | 29437.0000 |      0.5164 |      0.5074 |       0.0015 |
|       5 | 29437.0000 |      0.5395 |      0.5176 |       0.0017 |
|       6 | 29436.0000 |      0.5633 |      0.5311 |       0.0024 |
|       7 | 29437.0000 |      0.5902 |      0.5268 |       0.0011 |
|       8 | 29437.0000 |      0.6264 |      0.5035 |      -0.0019 |
|       9 | 29437.0000 |      0.7041 |      0.5214 |      -0.0012 |

What drives the 1-week prediction (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| spy_ret_1     |     0.0089 |
| breadth_50    |     0.0074 |
| vix_chg_1     |     0.0054 |
| month         |     0.0042 |
| spy_ret_5     |     0.0023 |
| qqq_ret_21    |     0.0019 |
| vix_term      |     0.0018 |
| vix           |     0.0017 |
| sector_rs     |     0.0014 |
| qqq_ok        |     0.0011 |
| dow           |     0.0009 |
| vix_chg_5     |     0.0009 |
| mkt_above200  |     0.0009 |
| industry_rank |     0.0007 |
| wk_ret_1      |     0.0007 |

Do the new features improve the +20%/-10% goal model? (OOS tiers)

**original**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 285457.000 |        0.230 |      0.455 |            0.013 |
| top 10%    |  28546.000 |        0.364 |      0.553 |            0.020 |
| top 5%     |  14273.000 |        0.365 |      0.564 |            0.018 |
| top 2%     |   5710.000 |        0.367 |      0.578 |            0.016 |
| top 1%     |   2855.000 |        0.379 |      0.578 |            0.018 |

**with new features**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 285457.000 |        0.230 |      0.455 |            0.013 |
| top 10%    |  28546.000 |        0.385 |      0.532 |            0.026 |
| top 5%     |  14273.000 |        0.401 |      0.525 |            0.030 |
| top 2%     |   5710.000 |        0.434 |      0.494 |            0.040 |
| top 1%     |   2855.000 |        0.461 |      0.471 |            0.049 |

**with fundamentals**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 285457.000 |        0.230 |      0.455 |            0.013 |
| top 10%    |  28546.000 |        0.389 |      0.523 |            0.028 |
| top 5%     |  14273.000 |        0.408 |      0.513 |            0.032 |
| top 2%     |   5710.000 |        0.440 |      0.484 |            0.042 |
| top 1%     |   2855.000 |        0.464 |      0.467 |            0.048 |

**with new features, point-in-time S&P 500**

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97516.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5447.000 |        0.372 |      0.500 |            0.030 |
| top 5%     |  2804.000 |        0.406 |      0.480 |            0.038 |
| top 2%     |  1226.000 |        0.426 |      0.456 |            0.045 |
| top 1%     |   634.000 |        0.457 |      0.420 |            0.057 |

**with fundamentals, point-in-time S&P 500**

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97516.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5488.000 |        0.370 |      0.490 |            0.030 |
| top 5%     |  2909.000 |        0.393 |      0.481 |            0.035 |
| top 2%     |  1268.000 |        0.433 |      0.438 |            0.049 |
| top 1%     |   650.000 |        0.466 |      0.428 |            0.056 |

## 20. Run 29: sector rotation from the S&P 500's own stocks -> the top 1-3 stocks of the leading sector

Sector momentum = return of an equal-weight index of each sector's S&P 500 members at the time (9 sectors: communication services counted as tech, real estate as financials; former members included). At each weekly (Friday) or monthly check: rank sectors by 1-week / 1-month / 3-month / 6-month return, take the strongest, the second strongest, or both, and hold the top 1/2/3 S&P 500 stocks of each chosen sector (ranked by the same lookback or by 6m/1m momentum). Everything else is sold at the check. Equal weight, 0.1% per side, no stop. 144 configurations, chosen on 2007-2017, judged on 2018+.

Median by setting:

| value          |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD | setting           |
|:---------------|----------:|-----------:|-----------------:|-----------:|------------:|------------------:|:------------------|
| 1 month        |    -0.004 |     -0.496 |           -0.006 |      0.035 |      -0.496 |             0.081 | sector momentum   |
| 1 week         |    -0.002 |     -0.398 |           -0.004 |     -0.003 |      -0.475 |            -0.006 | sector momentum   |
| 3 months       |     0.009 |     -0.511 |            0.018 |      0.031 |      -0.531 |             0.051 | sector momentum   |
| 6 months       |     0.010 |     -0.566 |            0.014 |     -0.002 |      -0.557 |            -0.002 | sector momentum   |
| monthly        |     0.025 |     -0.440 |            0.065 |      0.066 |      -0.422 |             0.153 | check             |
| weekly         |    -0.012 |     -0.548 |           -0.024 |     -0.025 |      -0.587 |            -0.049 | check             |
| #1 and #2      |     0.007 |     -0.434 |            0.017 |      0.015 |      -0.448 |             0.046 | sectors           |
| #1 only        |    -0.002 |     -0.531 |           -0.003 |      0.006 |      -0.606 |             0.009 | sectors           |
| #2 only        |     0.001 |     -0.488 |            0.003 |     -0.002 |      -0.556 |            -0.004 | sectors           |
| 6m/1m momentum |     0.007 |     -0.521 |            0.012 |      0.017 |      -0.538 |             0.029 | stocks ranked by  |
| same lookback  |    -0.005 |     -0.444 |           -0.012 |      0.002 |      -0.491 |             0.005 | stocks ranked by  |
| 1              |    -0.012 |     -0.575 |           -0.019 |      0.021 |      -0.607 |             0.029 | stocks per sector |
| 2              |     0.002 |     -0.465 |            0.005 |      0.004 |      -0.509 |             0.007 | stocks per sector |
| 3              |     0.011 |     -0.392 |            0.023 |     -0.003 |      -0.480 |            -0.007 | stocks per sector |

Top 10 (by 2007-2017 return / drawdown). Winner: sector momentum: 3 months, check: monthly, sectors: #2 only, stocks ranked by: same lookback, stocks per sector: 3

| sector momentum   | check   | sectors   | stocks ranked by   |   stocks per sector |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |
|:------------------|:--------|:----------|:-------------------|--------------------:|----------:|-----------:|-----------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|
| 3 months          | monthly | #2 only   | same lookback      |                   3 |     0.109 |     -0.277 |            0.395 |      0.111 |      -0.389 |             0.284 |          218 |     0.546 |         23.867 |
| 1 week            | monthly | #1 only   | same lookback      |                   3 |     0.053 |     -0.191 |            0.276 |      0.035 |      -0.288 |             0.122 |          126 |     0.540 |         21.262 |
| 6 months          | monthly | #1 and #2 | 6m/1m momentum     |                   3 |     0.069 |     -0.266 |            0.260 |      0.056 |      -0.361 |             0.155 |          365 |     0.482 |         29.482 |
| 6 months          | monthly | #1 and #2 | same lookback      |                   3 |     0.061 |     -0.273 |            0.223 |      0.049 |      -0.407 |             0.119 |          351 |     0.479 |         29.940 |
| 1 week            | monthly | #1 and #2 | 6m/1m momentum     |                   3 |     0.051 |     -0.242 |            0.212 |      0.084 |      -0.252 |             0.331 |          422 |     0.576 |         23.332 |
| 3 months          | monthly | #2 only   | 6m/1m momentum     |                   3 |     0.061 |     -0.319 |            0.190 |      0.077 |      -0.413 |             0.187 |          236 |     0.517 |         23.716 |
| 6 months          | monthly | #2 only   | 6m/1m momentum     |                   3 |     0.071 |     -0.372 |            0.190 |     -0.013 |      -0.688 |            -0.019 |          235 |     0.532 |         23.345 |
| 3 months          | monthly | #1 and #2 | 6m/1m momentum     |                   3 |     0.061 |     -0.352 |            0.174 |      0.054 |      -0.396 |             0.137 |          409 |     0.494 |         27.015 |
| 6 months          | monthly | #1 and #2 | 6m/1m momentum     |                   2 |     0.052 |     -0.323 |            0.162 |      0.076 |      -0.418 |             0.183 |          242 |     0.517 |         29.537 |
| 1 month           | monthly | #1 and #2 | 6m/1m momentum     |                   3 |     0.047 |     -0.314 |            0.151 |      0.089 |      -0.348 |             0.255 |          461 |     0.538 |         23.249 |

Benchmarks:

| strategy                                     |   IS_CAGR |   IS_maxDD |   OOS_CAGR |   OOS_maxDD |
|:---------------------------------------------|----------:|-----------:|-----------:|------------:|
| SPY                                          |     0.082 |     -0.552 |      0.143 |      -0.337 |
| QQQ                                          |     0.134 |     -0.534 |      0.194 |      -0.351 |
| hold the #1 sector's ETF (3 months, monthly) |     0.040 |     -0.507 |      0.074 |      -0.378 |

| strategy (2018+)   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| run 29 winner      |  0.620 |          0.048 |     0.576 |    0.524 |        0.803 |  0.111 |   -0.389 |         0.284 |        -0.140 |

Year by year:

|     year |   winner |    SPY |    QQQ |
|---------:|---------:|-------:|-------:|
| 2007.000 |    0.492 |  0.053 |  0.188 |
| 2008.000 |   -0.106 | -0.368 | -0.417 |
| 2009.000 |    0.016 |  0.264 |  0.547 |
| 2010.000 |    0.408 |  0.151 |  0.201 |
| 2011.000 |   -0.135 |  0.019 |  0.035 |
| 2012.000 |    0.129 |  0.160 |  0.181 |
| 2013.000 |    0.286 |  0.323 |  0.366 |
| 2014.000 |   -0.067 |  0.135 |  0.192 |
| 2015.000 |    0.021 |  0.012 |  0.094 |
| 2016.000 |    0.062 |  0.120 |  0.071 |
| 2017.000 |    0.290 |  0.217 |  0.327 |
| 2018.000 |   -0.283 | -0.046 | -0.001 |
| 2019.000 |    0.107 |  0.312 |  0.390 |
| 2020.000 |    0.226 |  0.183 |  0.484 |
| 2021.000 |    0.427 |  0.287 |  0.274 |
| 2022.000 |   -0.116 | -0.182 | -0.326 |
| 2023.000 |    0.025 |  0.262 |  0.549 |
| 2024.000 |    0.315 |  0.249 |  0.256 |
| 2025.000 |    0.197 |  0.177 |  0.208 |
| 2026.000 |    0.310 |  0.128 |  0.159 |

Where the winner's money was (share of holding days by sector):

| sector                 |   share of holding days |
|:-----------------------|------------------------:|
| Consumer Staples       |                   0.150 |
| Information Technology |                   0.141 |
| Consumer Discretionary |                   0.139 |
| Materials              |                   0.117 |
| Industrials            |                   0.114 |
| Utilities              |                   0.108 |
| Health Care            |                   0.084 |
| Financials             |                   0.077 |
| Energy                 |                   0.068 |

Sector momentum today (S&P 500 member index):

| sector                 |   1 week |   1 month |   3 months |   6 months |
|:-----------------------|---------:|----------:|-----------:|-----------:|
| Health Care            |    0.035 |     0.051 |      0.152 |      0.229 |
| Energy                 |    0.039 |     0.050 |      0.145 |      0.215 |
| Consumer Staples       |    0.055 |     0.042 |      0.017 |      0.070 |
| Utilities              |    0.023 |     0.024 |     -0.053 |     -0.062 |
| Consumer Discretionary |    0.025 |     0.018 |     -0.025 |     -0.074 |
| Industrials            |    0.005 |     0.006 |     -0.041 |     -0.017 |
| Financials             |    0.015 |    -0.010 |     -0.032 |      0.035 |
| Materials              |    0.031 |    -0.010 |      0.019 |     -0.010 |
| Information Technology |   -0.058 |    -0.025 |      0.060 |      0.162 |

Today's holdings of the top 3 configurations:

| configuration                                   | sectors             | holdings now                   |
|:------------------------------------------------|:--------------------|:-------------------------------|
| 3 months, monthly, #2 only, same lookback, 3    | Energy              | MPC, VLO, APA                  |
| 1 week, monthly, #1 only, same lookback, 3      | Consumer Staples    | KDP                            |
| 6 months, monthly, #1 and #2, 6m/1m momentum, 3 | Health Care, Energy | MRNA, MPC, HUM, VLO, PSX, VEEV |

Winner's trades since 2018:

| ticker   | sector                 | date_in             | date_out            |   days |    ret |
|:---------|:-----------------------|:--------------------|:--------------------|-------:|-------:|
| KR       | Consumer Staples       | 2018-01-31 00:00:00 | 2018-02-28 00:00:00 |     19 | -0.103 |
| KDP      | Consumer Staples       | 2018-01-31 00:00:00 | 2018-02-28 00:00:00 |     19 | -0.026 |
| TGT      | Consumer Staples       | 2018-01-31 00:00:00 | 2018-02-28 00:00:00 |     19 |  0.011 |
| NFLX     | Information Technology | 2018-02-28 00:00:00 | 2018-03-29 00:00:00 |     21 |  0.014 |
| HPE      | Information Technology | 2018-02-28 00:00:00 | 2018-03-29 00:00:00 |     21 | -0.053 |
| STX      | Information Technology | 2018-02-28 00:00:00 | 2018-03-29 00:00:00 |     21 |  0.107 |
| NKTR     | Consumer Discretionary | 2018-03-29 00:00:00 | 2018-04-30 00:00:00 |     21 | -0.213 |
| KSS      | Consumer Discretionary | 2018-03-29 00:00:00 | 2018-04-30 00:00:00 |     21 | -0.052 |
| VLO      | Energy                 | 2018-04-30 00:00:00 | 2018-05-31 00:00:00 |     22 |  0.100 |
| COP      | Energy                 | 2018-04-30 00:00:00 | 2018-05-31 00:00:00 |     22 |  0.033 |
| PSX      | Energy                 | 2018-04-30 00:00:00 | 2018-05-31 00:00:00 |     22 |  0.053 |
| NRG      | Utilities              | 2018-05-31 00:00:00 | 2018-06-29 00:00:00 |     21 | -0.103 |
| EXC      | Utilities              | 2018-05-31 00:00:00 | 2018-06-29 00:00:00 |     21 |  0.029 |
| UA       | Consumer Discretionary | 2018-06-29 00:00:00 | 2018-07-31 00:00:00 |     21 | -0.111 |
| TRIP     | Consumer Discretionary | 2018-06-29 00:00:00 | 2018-07-31 00:00:00 |     21 |  0.041 |
| UAA      | Consumer Discretionary | 2018-06-29 00:00:00 | 2018-07-31 00:00:00 |     21 | -0.112 |
| NOV      | Energy                 | 2018-07-31 00:00:00 | 2018-08-31 00:00:00 |     23 | -0.032 |
| DVN      | Energy                 | 2018-07-31 00:00:00 | 2018-08-31 00:00:00 |     23 | -0.046 |
| OKE      | Energy                 | 2018-07-31 00:00:00 | 2018-08-31 00:00:00 |     23 | -0.053 |
| KR       | Consumer Staples       | 2018-08-31 00:00:00 | 2018-09-28 00:00:00 |     19 | -0.076 |
| MKC      | Consumer Staples       | 2018-08-31 00:00:00 | 2018-09-28 00:00:00 |     19 |  0.055 |
| CHD      | Consumer Staples       | 2018-08-31 00:00:00 | 2018-09-28 00:00:00 |     19 |  0.049 |
| FLS      | Industrials            | 2018-09-28 00:00:00 | 2018-10-31 00:00:00 |     23 | -0.161 |
| UAL      | Industrials            | 2018-09-28 00:00:00 | 2018-10-31 00:00:00 |     23 | -0.040 |
| LUV      | Industrials            | 2018-09-28 00:00:00 | 2018-10-31 00:00:00 |     23 | -0.214 |
| DG       | Consumer Staples       | 2018-10-31 00:00:00 | 2018-11-30 00:00:00 |     21 | -0.004 |
| MKC      | Consumer Staples       | 2018-10-31 00:00:00 | 2018-12-31 00:00:00 |     40 | -0.029 |
| HRL      | Consumer Staples       | 2018-10-31 00:00:00 | 2018-12-31 00:00:00 |     40 | -0.022 |
| CHD      | Consumer Staples       | 2018-11-30 00:00:00 | 2019-01-31 00:00:00 |     40 | -0.024 |
| PG       | Consumer Staples       | 2018-12-31 00:00:00 | 2019-01-31 00:00:00 |     21 |  0.058 |
| CMG      | Consumer Discretionary | 2019-02-28 00:00:00 | 2019-04-30 00:00:00 |     42 |  0.133 |
| ULTA     | Consumer Discretionary | 2019-03-29 00:00:00 | 2019-04-30 00:00:00 |     21 |  0.001 |
| EL       | Consumer Staples       | 2019-04-30 00:00:00 | 2019-05-31 00:00:00 |     22 | -0.060 |
| MKC      | Consumer Staples       | 2019-04-30 00:00:00 | 2019-05-31 00:00:00 |     22 |  0.013 |
| AWK      | Utilities              | 2019-05-31 00:00:00 | 2019-06-28 00:00:00 |     20 |  0.026 |
| SRE      | Utilities              | 2019-05-31 00:00:00 | 2019-06-28 00:00:00 |     20 |  0.046 |
| SO       | Utilities              | 2019-05-31 00:00:00 | 2019-06-28 00:00:00 |     20 |  0.033 |
| APD      | Materials              | 2019-06-28 00:00:00 | 2019-07-31 00:00:00 |     22 |  0.008 |
| VMC      | Materials              | 2019-06-28 00:00:00 | 2019-07-31 00:00:00 |     22 |  0.008 |
| CF       | Materials              | 2019-07-31 00:00:00 | 2019-08-30 00:00:00 |     22 | -0.022 |
| SHW      | Materials              | 2019-07-31 00:00:00 | 2019-08-30 00:00:00 |     22 |  0.029 |
| COST     | Consumer Staples       | 2019-08-30 00:00:00 | 2019-09-30 00:00:00 |     20 | -0.023 |
| TGT      | Consumer Staples       | 2019-08-30 00:00:00 | 2019-10-31 00:00:00 |     43 | -0.001 |
| CPB      | Consumer Staples       | 2019-08-30 00:00:00 | 2019-10-31 00:00:00 |     43 |  0.037 |
| LKQ      | Industrials            | 2019-10-31 00:00:00 | 2019-11-29 00:00:00 |     20 |  0.038 |
| PWR      | Industrials            | 2019-10-31 00:00:00 | 2019-11-29 00:00:00 |     20 | -0.010 |
| NWL      | Industrials            | 2019-10-31 00:00:00 | 2019-11-29 00:00:00 |     20 |  0.025 |
| GE       | Industrials            | 2019-11-29 00:00:00 | 2019-12-31 00:00:00 |     21 | -0.009 |
| URI      | Industrials            | 2019-11-29 00:00:00 | 2019-12-31 00:00:00 |     21 |  0.090 |
| XRX      | Industrials            | 2019-11-29 00:00:00 | 2019-12-31 00:00:00 |     21 | -0.047 |
| SWKS     | Information Technology | 2019-12-31 00:00:00 | 2020-01-31 00:00:00 |     21 | -0.064 |
| AMD      | Information Technology | 2019-12-31 00:00:00 | 2020-02-28 00:00:00 |     40 | -0.008 |
| FTNT     | Information Technology | 2019-12-31 00:00:00 | 2020-02-28 00:00:00 |     40 | -0.044 |
| NOW      | Information Technology | 2020-01-31 00:00:00 | 2020-03-31 00:00:00 |     41 | -0.153 |
| NFLX     | Information Technology | 2020-02-28 00:00:00 | 2020-03-31 00:00:00 |     22 |  0.018 |
| REGN     | Health Care            | 2020-03-31 00:00:00 | 2020-04-30 00:00:00 |     21 |  0.077 |
| GILD     | Health Care            | 2020-03-31 00:00:00 | 2020-04-30 00:00:00 |     21 |  0.124 |
| KR       | Consumer Staples       | 2020-04-30 00:00:00 | 2020-05-29 00:00:00 |     20 |  0.037 |
| CLX      | Consumer Staples       | 2020-04-30 00:00:00 | 2020-06-30 00:00:00 |     42 |  0.177 |
| GIS      | Consumer Staples       | 2020-04-30 00:00:00 | 2020-06-30 00:00:00 |     42 |  0.029 |
| CAG      | Consumer Staples       | 2020-05-29 00:00:00 | 2020-06-30 00:00:00 |     22 |  0.011 |
| EBAY     | Consumer Discretionary | 2020-06-30 00:00:00 | 2020-07-31 00:00:00 |     22 |  0.054 |
| DHI      | Consumer Discretionary | 2020-06-30 00:00:00 | 2020-07-31 00:00:00 |     22 |  0.193 |
| UPS      | Industrials            | 2020-07-31 00:00:00 | 2020-08-31 00:00:00 |     21 |  0.153 |
| WHR      | Industrials            | 2020-07-31 00:00:00 | 2020-08-31 00:00:00 |     21 |  0.097 |
| AMZN     | Consumer Discretionary | 2020-08-31 00:00:00 | 2020-09-30 00:00:00 |     21 | -0.088 |
| BBY      | Consumer Discretionary | 2020-08-31 00:00:00 | 2020-09-30 00:00:00 |     21 |  0.009 |
| DHI      | Consumer Discretionary | 2020-08-31 00:00:00 | 2020-10-30 00:00:00 |     43 | -0.064 |
| PHM      | Consumer Discretionary | 2020-09-30 00:00:00 | 2020-10-30 00:00:00 |     22 | -0.119 |
| LEN      | Consumer Discretionary | 2020-09-30 00:00:00 | 2020-10-30 00:00:00 |     22 | -0.138 |
| TPR      | Consumer Discretionary | 2020-10-30 00:00:00 | 2020-12-31 00:00:00 |     42 |  0.398 |
| UAA      | Consumer Discretionary | 2020-11-30 00:00:00 | 2020-12-31 00:00:00 |     22 |  0.036 |
| LNC      | Financials             | 2020-12-31 00:00:00 | 2021-01-29 00:00:00 |     19 | -0.089 |
| IVZ      | Financials             | 2020-12-31 00:00:00 | 2021-01-29 00:00:00 |     19 |  0.181 |
| ZION     | Financials             | 2020-12-31 00:00:00 | 2021-01-29 00:00:00 |     19 |  0.016 |
| NTAP     | Information Technology | 2021-01-29 00:00:00 | 2021-02-26 00:00:00 |     19 | -0.058 |
| AMAT     | Information Technology | 2021-01-29 00:00:00 | 2021-03-31 00:00:00 |     42 |  0.385 |
| MU       | Information Technology | 2021-01-29 00:00:00 | 2021-03-31 00:00:00 |     42 |  0.127 |
| WDC      | Information Technology | 2021-02-26 00:00:00 | 2021-03-31 00:00:00 |     23 | -0.026 |
| AAL      | Financials             | 2021-03-31 00:00:00 | 2021-04-30 00:00:00 |     21 | -0.091 |
| IVZ      | Financials             | 2021-03-31 00:00:00 | 2021-04-30 00:00:00 |     21 |  0.071 |
| HIG      | Financials             | 2021-03-31 00:00:00 | 2021-04-30 00:00:00 |     21 | -0.012 |
| WFC      | Financials             | 2021-04-30 00:00:00 | 2021-05-28 00:00:00 |     20 |  0.039 |
| COF      | Financials             | 2021-04-30 00:00:00 | 2021-05-28 00:00:00 |     20 |  0.081 |
| LNC      | Financials             | 2021-04-30 00:00:00 | 2021-05-28 00:00:00 |     20 |  0.088 |
| DXC      | Industrials            | 2021-05-28 00:00:00 | 2021-06-30 00:00:00 |     22 |  0.027 |
| EFX      | Industrials            | 2021-05-28 00:00:00 | 2021-06-30 00:00:00 |     22 |  0.019 |
| EXPD     | Industrials            | 2021-05-28 00:00:00 | 2021-06-30 00:00:00 |     22 |  0.007 |
| IDXX     | Health Care            | 2021-06-30 00:00:00 | 2021-07-30 00:00:00 |     21 |  0.074 |
| CRL      | Health Care            | 2021-06-30 00:00:00 | 2021-07-30 00:00:00 |     21 |  0.100 |
| WST      | Health Care            | 2021-06-30 00:00:00 | 2021-07-30 00:00:00 |     21 |  0.147 |
| IT       | Information Technology | 2021-07-30 00:00:00 | 2021-08-31 00:00:00 |     22 |  0.166 |
| AMD      | Information Technology | 2021-07-30 00:00:00 | 2021-08-31 00:00:00 |     22 |  0.043 |
| FTNT     | Information Technology | 2021-07-30 00:00:00 | 2021-09-30 00:00:00 |     43 |  0.073 |
| MPWR     | Information Technology | 2021-08-31 00:00:00 | 2021-09-30 00:00:00 |     21 | -0.020 |
| NOW      | Information Technology | 2021-08-31 00:00:00 | 2021-09-30 00:00:00 |     21 | -0.033 |
| DXCM     | Health Care            | 2021-09-30 00:00:00 | 2021-10-29 00:00:00 |     21 |  0.140 |
| BAC      | Financials             | 2021-10-29 00:00:00 | 2021-11-30 00:00:00 |     21 | -0.069 |
| AIG      | Financials             | 2021-10-29 00:00:00 | 2021-11-30 00:00:00 |     21 | -0.110 |
| RF       | Financials             | 2021-10-29 00:00:00 | 2021-11-30 00:00:00 |     21 | -0.039 |
| NVDA     | Information Technology | 2021-11-30 00:00:00 | 2021-12-31 00:00:00 |     22 | -0.100 |
| AMD      | Information Technology | 2021-11-30 00:00:00 | 2021-12-31 00:00:00 |     22 | -0.091 |
| ANET     | Information Technology | 2021-11-30 00:00:00 | 2021-12-31 00:00:00 |     22 |  0.159 |
| EIX      | Utilities              | 2021-12-31 00:00:00 | 2022-01-31 00:00:00 |     20 | -0.080 |
| EXC      | Utilities              | 2021-12-31 00:00:00 | 2022-01-31 00:00:00 |     20 |  0.003 |
| ED       | Utilities              | 2021-12-31 00:00:00 | 2022-01-31 00:00:00 |     20 |  0.013 |
| MKC      | Consumer Staples       | 2022-01-31 00:00:00 | 2022-02-28 00:00:00 |     19 | -0.051 |
| CHD      | Consumer Staples       | 2022-01-31 00:00:00 | 2022-02-28 00:00:00 |     19 | -0.044 |
| ADM      | Consumer Staples       | 2022-02-28 00:00:00 | 2022-03-31 00:00:00 |     23 |  0.151 |
| SYY      | Consumer Staples       | 2022-02-28 00:00:00 | 2022-03-31 00:00:00 |     23 | -0.057 |
| MO       | Consumer Staples       | 2022-02-28 00:00:00 | 2022-03-31 00:00:00 |     23 |  0.036 |
| SRE      | Utilities              | 2022-03-31 00:00:00 | 2022-04-29 00:00:00 |     20 | -0.040 |
| EXC      | Utilities              | 2022-03-31 00:00:00 | 2022-04-29 00:00:00 |     20 | -0.018 |
| NI       | Utilities              | 2022-03-31 00:00:00 | 2022-04-29 00:00:00 |     20 | -0.077 |
| NUE      | Materials              | 2022-04-29 00:00:00 | 2022-05-31 00:00:00 |     21 | -0.144 |
| CF       | Materials              | 2022-04-29 00:00:00 | 2022-05-31 00:00:00 |     21 |  0.024 |
| NRG      | Utilities              | 2022-05-31 00:00:00 | 2022-06-30 00:00:00 |     21 | -0.171 |
| CNP      | Utilities              | 2022-05-31 00:00:00 | 2022-06-30 00:00:00 |     21 | -0.077 |
| LW       | Industrials            | 2022-07-29 00:00:00 | 2022-08-31 00:00:00 |     23 |  0.001 |
| PWR      | Industrials            | 2022-07-29 00:00:00 | 2022-08-31 00:00:00 |     23 |  0.019 |
| AES      | Utilities              | 2022-08-31 00:00:00 | 2022-09-30 00:00:00 |     21 | -0.112 |
| NEE      | Utilities              | 2022-08-31 00:00:00 | 2022-09-30 00:00:00 |     21 | -0.078 |
| MPC      | Energy                 | 2022-09-30 00:00:00 | 2022-10-31 00:00:00 |     21 |  0.144 |
| COP      | Energy                 | 2022-09-30 00:00:00 | 2022-10-31 00:00:00 |     21 |  0.232 |
| BIIB     | Health Care            | 2022-10-31 00:00:00 | 2022-12-30 00:00:00 |     42 | -0.023 |
| GILD     | Health Care            | 2022-10-31 00:00:00 | 2022-12-30 00:00:00 |     42 |  0.103 |
| DXCM     | Health Care            | 2022-11-30 00:00:00 | 2022-12-30 00:00:00 |     21 | -0.026 |
| UHS      | Health Care            | 2022-12-30 00:00:00 | 2023-01-31 00:00:00 |     20 |  0.052 |
| FCX      | Materials              | 2023-01-31 00:00:00 | 2023-02-28 00:00:00 |     19 | -0.082 |
| STLD     | Materials              | 2023-01-31 00:00:00 | 2023-02-28 00:00:00 |     19 |  0.045 |
| LVS      | Consumer Discretionary | 2023-02-28 00:00:00 | 2023-03-31 00:00:00 |     23 | -0.000 |
| BKNG     | Consumer Discretionary | 2023-02-28 00:00:00 | 2023-03-31 00:00:00 |     23 |  0.051 |
| WYNN     | Consumer Discretionary | 2023-02-28 00:00:00 | 2023-04-28 00:00:00 |     42 |  0.055 |
| MGM      | Consumer Discretionary | 2023-03-31 00:00:00 | 2023-04-28 00:00:00 |     19 |  0.011 |
| PNW      | Utilities              | 2023-04-28 00:00:00 | 2023-05-31 00:00:00 |     22 | -0.015 |
| EIX      | Utilities              | 2023-04-28 00:00:00 | 2023-05-31 00:00:00 |     22 | -0.083 |
| PCG      | Utilities              | 2023-05-31 00:00:00 | 2023-06-30 00:00:00 |     21 |  0.020 |
| CCL      | Consumer Discretionary | 2023-06-30 00:00:00 | 2023-07-31 00:00:00 |     20 |  0.001 |
| NCLH     | Consumer Discretionary | 2023-06-30 00:00:00 | 2023-07-31 00:00:00 |     20 |  0.014 |
| RCL      | Consumer Discretionary | 2023-06-30 00:00:00 | 2023-07-31 00:00:00 |     20 |  0.052 |
| DAL      | Industrials            | 2023-07-31 00:00:00 | 2023-08-31 00:00:00 |     23 | -0.073 |
| CARR     | Industrials            | 2023-07-31 00:00:00 | 2023-09-29 00:00:00 |     43 | -0.073 |
| URI      | Industrials            | 2023-08-31 00:00:00 | 2023-09-29 00:00:00 |     20 | -0.067 |
| CAT      | Industrials            | 2023-08-31 00:00:00 | 2023-09-29 00:00:00 |     20 | -0.029 |
| ANET     | Information Technology | 2023-10-31 00:00:00 | 2023-11-30 00:00:00 |     21 |  0.097 |
| INTC     | Information Technology | 2023-11-30 00:00:00 | 2023-12-29 00:00:00 |     20 |  0.124 |
| IT       | Information Technology | 2023-11-30 00:00:00 | 2023-12-29 00:00:00 |     20 |  0.037 |
| PANW     | Information Technology | 2023-11-30 00:00:00 | 2023-12-29 00:00:00 |     20 | -0.001 |
| DHI      | Consumer Discretionary | 2023-12-29 00:00:00 | 2024-01-31 00:00:00 |     21 | -0.060 |
| EXPE     | Consumer Discretionary | 2023-12-29 00:00:00 | 2024-02-29 00:00:00 |     41 | -0.099 |
| RCL      | Consumer Discretionary | 2023-12-29 00:00:00 | 2024-02-29 00:00:00 |     41 | -0.047 |
| BBWI     | Consumer Discretionary | 2024-01-31 00:00:00 | 2024-02-29 00:00:00 |     20 |  0.076 |
| URI      | Industrials            | 2024-02-29 00:00:00 | 2024-03-28 00:00:00 |     20 |  0.040 |
| BLDR     | Industrials            | 2024-02-29 00:00:00 | 2024-03-28 00:00:00 |     20 |  0.069 |
| UBER     | Industrials            | 2024-02-29 00:00:00 | 2024-03-28 00:00:00 |     20 | -0.032 |
| GE       | Industrials            | 2024-03-28 00:00:00 | 2024-04-30 00:00:00 |     22 |  0.157 |
| ETN      | Industrials            | 2024-03-28 00:00:00 | 2024-04-30 00:00:00 |     22 |  0.018 |
| PCAR     | Industrials            | 2024-03-28 00:00:00 | 2024-04-30 00:00:00 |     22 | -0.144 |
| CEG      | Utilities              | 2024-04-30 00:00:00 | 2024-05-31 00:00:00 |     22 |  0.170 |
| NRG      | Utilities              | 2024-04-30 00:00:00 | 2024-05-31 00:00:00 |     22 |  0.115 |
| PEG      | Utilities              | 2024-04-30 00:00:00 | 2024-05-31 00:00:00 |     22 |  0.097 |
| TRGP     | Energy                 | 2024-05-31 00:00:00 | 2024-06-28 00:00:00 |     19 |  0.089 |
| WMB      | Energy                 | 2024-05-31 00:00:00 | 2024-06-28 00:00:00 |     19 |  0.036 |
| KMI      | Energy                 | 2024-05-31 00:00:00 | 2024-06-28 00:00:00 |     19 |  0.019 |
| FICO     | Information Technology | 2024-07-31 00:00:00 | 2024-08-30 00:00:00 |     22 |  0.081 |
| UHS      | Health Care            | 2024-08-30 00:00:00 | 2024-09-30 00:00:00 |     20 | -0.037 |
| GILD     | Health Care            | 2024-08-30 00:00:00 | 2024-09-30 00:00:00 |     20 |  0.071 |
| MHK      | Industrials            | 2024-09-30 00:00:00 | 2024-10-31 00:00:00 |     23 | -0.164 |
| UAL      | Industrials            | 2024-10-31 00:00:00 | 2024-11-29 00:00:00 |     20 |  0.237 |
| AXON     | Industrials            | 2024-10-31 00:00:00 | 2024-11-29 00:00:00 |     20 |  0.528 |
| RJF      | Financials             | 2024-11-29 00:00:00 | 2024-12-31 00:00:00 |     21 | -0.082 |
| SYF      | Financials             | 2024-11-29 00:00:00 | 2024-12-31 00:00:00 |     21 | -0.037 |
| BX       | Financials             | 2024-11-29 00:00:00 | 2024-12-31 00:00:00 |     21 | -0.098 |
| AVGO     | Information Technology | 2024-12-31 00:00:00 | 2025-01-31 00:00:00 |     20 | -0.046 |
| PLTR     | Information Technology | 2024-12-31 00:00:00 | 2025-02-28 00:00:00 |     39 |  0.123 |
| GDDY     | Information Technology | 2024-12-31 00:00:00 | 2025-02-28 00:00:00 |     39 | -0.091 |
| JBL      | Information Technology | 2025-01-31 00:00:00 | 2025-02-28 00:00:00 |     19 | -0.046 |
| PM       | Consumer Staples       | 2025-02-28 00:00:00 | 2025-03-31 00:00:00 |     21 |  0.031 |
| WMT      | Consumer Staples       | 2025-02-28 00:00:00 | 2025-03-31 00:00:00 |     21 | -0.107 |
| ED       | Utilities              | 2025-03-31 00:00:00 | 2025-04-30 00:00:00 |     21 |  0.020 |
| EXC      | Utilities              | 2025-03-31 00:00:00 | 2025-04-30 00:00:00 |     21 |  0.018 |
| AEP      | Utilities              | 2025-03-31 00:00:00 | 2025-04-30 00:00:00 |     21 | -0.009 |
| PM       | Consumer Staples       | 2025-04-30 00:00:00 | 2025-05-30 00:00:00 |     21 |  0.054 |
| MNST     | Consumer Staples       | 2025-04-30 00:00:00 | 2025-05-30 00:00:00 |     21 |  0.064 |
| AXON     | Industrials            | 2025-05-30 00:00:00 | 2025-07-31 00:00:00 |     42 |  0.007 |
| PWR      | Industrials            | 2025-06-30 00:00:00 | 2025-07-31 00:00:00 |     22 |  0.074 |
| GEV      | Industrials            | 2025-05-30 00:00:00 | 2025-08-29 00:00:00 |     63 |  0.297 |
| ROK      | Industrials            | 2025-07-31 00:00:00 | 2025-08-29 00:00:00 |     21 | -0.020 |
| BKR      | Energy                 | 2025-08-29 00:00:00 | 2025-09-30 00:00:00 |     21 |  0.073 |
| APP      | Information Technology | 2025-09-30 00:00:00 | 2025-10-31 00:00:00 |     23 | -0.113 |
| WDC      | Information Technology | 2025-09-30 00:00:00 | 2025-10-31 00:00:00 |     23 |  0.251 |
| STX      | Information Technology | 2025-09-30 00:00:00 | 2025-10-31 00:00:00 |     23 |  0.084 |
| UHS      | Health Care            | 2025-10-31 00:00:00 | 2025-11-28 00:00:00 |     19 |  0.123 |
| NEE      | Utilities              | 2025-11-28 00:00:00 | 2025-12-31 00:00:00 |     22 | -0.070 |
| CEG      | Utilities              | 2025-11-28 00:00:00 | 2025-12-31 00:00:00 |     22 | -0.030 |
| NRG      | Utilities              | 2025-11-28 00:00:00 | 2025-12-31 00:00:00 |     22 | -0.060 |
| NUE      | Materials              | 2025-12-31 00:00:00 | 2026-01-30 00:00:00 |     20 |  0.090 |
| ALB      | Materials              | 2025-12-31 00:00:00 | 2026-03-31 00:00:00 |     61 |  0.272 |
| FCX      | Materials              | 2025-12-31 00:00:00 | 2026-03-31 00:00:00 |     61 |  0.160 |
| NEM      | Materials              | 2026-01-30 00:00:00 | 2026-03-31 00:00:00 |     41 | -0.035 |
| LYB      | Materials              | 2026-03-31 00:00:00 | 2026-04-30 00:00:00 |     21 | -0.074 |
| DOW      | Materials              | 2026-03-31 00:00:00 | 2026-04-30 00:00:00 |     21 | -0.028 |
| CF       | Materials              | 2026-03-31 00:00:00 | 2026-04-30 00:00:00 |     21 | -0.043 |
| LITE     | Information Technology | 2026-04-30 00:00:00 | 2026-05-29 00:00:00 |     20 | -0.052 |
| CIEN     | Information Technology | 2026-04-30 00:00:00 | 2026-05-29 00:00:00 |     20 |  0.100 |
| SNDK     | Information Technology | 2026-04-30 00:00:00 | 2026-05-29 00:00:00 |     20 |  0.546 |
| MPC      | Energy                 | 2026-05-29 00:00:00 | 2026-06-30 00:00:00 |     21 |  0.028 |
| VLO      | Energy                 | 2026-05-29 00:00:00 | 2026-06-30 00:00:00 |     21 |  0.064 |
| CAT      | Industrials            | 2026-06-30 00:00:00 | 2026-07-31 00:00:00 |     22 | -0.233 |
| UAL      | Industrials            | 2026-06-30 00:00:00 | 2026-07-31 00:00:00 |     22 | -0.108 |
| URI      | Industrials            | 2026-06-30 00:00:00 | 2026-07-31 00:00:00 |     22 | -0.047 |
| DOC      | Financials             | 2026-07-31 00:00:00 | 2026-08-31 00:00:00 |     21 | -0.042 |
| MPC      | Energy                 | 2026-08-31 00:00:00 | 2026-09-30 00:00:00 |     21 |  0.059 |
| VLO      | Energy                 | 2026-08-31 00:00:00 | 2026-09-30 00:00:00 |     21 |  0.080 |
| PSX      | Energy                 | 2026-08-31 00:00:00 | 2026-09-30 00:00:00 |     21 |  0.035 |
| MRNA     | Health Care            | 2026-09-30 00:00:00 | 2026-10-16 00:00:00 |     12 |  0.132 |
| VEEV     | Health Care            | 2026-09-30 00:00:00 | 2026-10-16 00:00:00 |     12 |  0.087 |
| RVTY     | Health Care            | 2026-09-30 00:00:00 | 2026-10-16 00:00:00 |     12 | -0.002 |

## 19. Run 28: sector momentum first, then the strongest stocks in the leading sectors; and the best stock of the year

9 broad sector ETFs (XLK, XLV, XLF, XLY, XLI, XLP, XLE, XLU, XLB; communication services counted as tech, real estate as financials) are only the momentum signal; the book holds the strongest S&P 500 stocks (point-in-time incl. former members; leaders: rising 50-day > 200-day, near highs, 6m/1m momentum) from the top 1-3 sectors, 15 positions, no stop, sold when the sector drops out or the stock leaves the top 30 at a rebalance. Sector momentum over 1 week / 1 month / 3 / 6 months; weekly or monthly; optionally cash for a chosen sector that is down (dual momentum) or only sectors whose median reported EPS growth is positive. Chosen on 2010-2017, judged on 2018+. 0.1% per side. Former members get the sector whose ETF they track most closely.

Median by setting (beats_base = share of configurations better than the same book with no sector rule):

| value              |   IS_CAGR |   IS_maxDD |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   beats_base_IS10_CAGR_per_DD |   beats_base_OOS_CAGR_per_DD | setting          |
|:-------------------|----------:|-----------:|------------:|-------------:|-------------------:|-----------:|------------:|------------------:|------------------------------:|-----------------------------:|:-----------------|
| etf                |     0.044 |     -0.360 |       0.072 |       -0.221 |              0.307 |      0.029 |      -0.388 |             0.074 |                         0.000 |                        0.000 | indicator        |
| 5                  |     0.077 |     -0.256 |       0.091 |       -0.196 |              0.464 |      0.026 |      -0.356 |             0.073 |                         0.000 |                        0.000 | lookback_days    |
| 21                 |     0.035 |     -0.397 |       0.063 |       -0.239 |              0.269 |      0.020 |      -0.388 |             0.044 |                         0.000 |                        0.000 | lookback_days    |
| 63                 |     0.043 |     -0.433 |       0.080 |       -0.210 |              0.340 |      0.041 |      -0.380 |             0.106 |                         0.000 |                        0.000 | lookback_days    |
| 126                |     0.044 |     -0.338 |       0.062 |       -0.273 |              0.250 |      0.028 |      -0.408 |             0.070 |                         0.000 |                        0.000 | lookback_days    |
| monthly            |     0.065 |     -0.273 |       0.085 |       -0.217 |              0.355 |      0.043 |      -0.367 |             0.127 |                         0.000 |                        0.000 | rebalance        |
| weekly             |     0.017 |     -0.440 |       0.030 |       -0.241 |              0.129 |      0.007 |      -0.419 |             0.016 |                         0.000 |                        0.000 | rebalance        |
| 1                  |     0.036 |     -0.312 |       0.062 |       -0.231 |              0.270 |      0.010 |      -0.388 |             0.024 |                         0.000 |                        0.000 | top_sectors      |
| 2                  |     0.039 |     -0.383 |       0.074 |       -0.239 |              0.340 |      0.023 |      -0.389 |             0.057 |                         0.000 |                        0.000 | top_sectors      |
| 3                  |     0.052 |     -0.403 |       0.077 |       -0.214 |              0.340 |      0.043 |      -0.385 |             0.113 |                         0.000 |                        0.000 | top_sectors      |
| no                 |     0.047 |     -0.388 |       0.077 |       -0.220 |              0.338 |      0.039 |      -0.385 |             0.097 |                         0.000 |                        0.000 | cash_if_negative |
| yes                |     0.040 |     -0.325 |       0.066 |       -0.231 |              0.276 |      0.027 |      -0.394 |             0.065 |                         0.000 |                        0.000 | cash_if_negative |
| none               |     0.028 |     -0.425 |       0.054 |       -0.222 |              0.240 |      0.038 |      -0.381 |             0.095 |                         0.000 |                        0.000 | earnings_confirm |
| sector EPS growing |     0.085 |     -0.198 |       0.110 |       -0.198 |              0.556 |      0.013 |      -0.388 |             0.035 |                         0.500 |                        0.000 | earnings_confirm |

Top 10 (by 2010-2017 return / drawdown). Winner: indicator=etf, lookback_days=5, rebalance=monthly, top_sectors=3, cash_if_negative=no, earnings_confirm=sector EPS growing

| indicator   |   lookback_days | rebalance   |   top_sectors | cash_if_negative   | earnings_confirm   |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days | beats_base_IS10_CAGR_per_DD   | beats_base_OOS_CAGR_per_DD   | beats_base_OOS_CAGR   |
|:------------|----------------:|:------------|--------------:|:-------------------|:-------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|:------------------------------|:-----------------------------|:----------------------|
| etf         |               5 | monthly     |             3 | no                 | sector EPS growing |     0.141 |     -0.196 |            0.720 |        1018 |    0.598 |        31.986 |      0.007 |      -0.406 |             0.017 |         1053 |     0.505 |         29.463 |       0.186 |       -0.196 |              0.948 |          1018 |      0.598 |          31.986 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             2 | yes                | sector EPS growing |     0.093 |     -0.131 |            0.714 |         997 |    0.617 |        24.393 |      0.000 |      -0.289 |             0.001 |          901 |     0.496 |         26.474 |       0.120 |       -0.131 |              0.919 |           997 |      0.617 |          24.393 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             2 | no                 | sector EPS growing |     0.132 |     -0.196 |            0.677 |        1230 |    0.614 |        25.979 |      0.019 |      -0.356 |             0.053 |         1113 |     0.509 |         27.235 |       0.168 |       -0.196 |              0.860 |          1230 |      0.614 |          25.979 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             1 | yes                | sector EPS growing |     0.083 |     -0.135 |            0.616 |        1124 |    0.622 |        20.732 |      0.026 |      -0.274 |             0.096 |         1019 |     0.523 |         21.730 |       0.110 |       -0.135 |              0.816 |          1124 |      0.622 |          20.732 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             3 | yes                | sector EPS growing |     0.094 |     -0.159 |            0.590 |         822 |    0.609 |        28.202 |      0.002 |      -0.357 |             0.007 |          813 |     0.490 |         28.123 |       0.129 |       -0.159 |              0.814 |           822 |      0.609 |          28.202 | True                          | False                        | False                 |
| etf         |              21 | monthly     |             3 | no                 | sector EPS growing |     0.116 |     -0.194 |            0.601 |        1002 |    0.568 |        32.192 |      0.092 |      -0.387 |             0.237 |         1039 |     0.500 |         29.930 |       0.154 |       -0.194 |              0.793 |          1002 |      0.568 |          32.192 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             3 | no                 | none               |     0.092 |     -0.456 |            0.201 |        1485 |    0.574 |        26.380 |      0.071 |      -0.367 |             0.193 |         1213 |     0.535 |         26.481 |       0.151 |       -0.197 |              0.765 |          1485 |      0.574 |          26.380 | True                          | False                        | False                 |
| etf         |              63 | monthly     |             3 | no                 | sector EPS growing |     0.110 |     -0.194 |            0.565 |         818 |    0.561 |        39.667 |      0.064 |      -0.384 |             0.168 |          867 |     0.466 |         35.164 |       0.144 |       -0.194 |              0.742 |           818 |      0.561 |          39.667 | True                          | False                        | False                 |
| etf         |               5 | monthly     |             1 | no                 | sector EPS growing |     0.091 |     -0.159 |            0.572 |        1312 |    0.603 |        21.076 |      0.039 |      -0.282 |             0.139 |         1184 |     0.532 |         22.222 |       0.115 |       -0.159 |              0.721 |          1312 |      0.603 |          21.076 | True                          | False                        | False                 |
| etf         |              63 | monthly     |             3 | yes                | sector EPS growing |     0.093 |     -0.191 |            0.487 |         727 |    0.556 |        39.409 |      0.055 |      -0.403 |             0.136 |          700 |     0.477 |         34.709 |       0.123 |       -0.191 |              0.646 |           727 |      0.556 |          39.409 | True                          | False                        | False                 |

Benchmarks:

| strategy                                                               |   IS_CAGR |   IS_maxDD |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |
|:-----------------------------------------------------------------------|----------:|-----------:|------------:|-------------:|-------------------:|-----------:|------------:|------------------:|
| no sector rule (run 27 style: 15 leaders, 6m/1m, monthly top-30 check) |     0.075 |     -0.466 |       0.120 |       -0.209 |              0.573 |      0.177 |      -0.411 |             0.431 |
| SPY                                                                    |     0.082 |     -0.552 |       0.136 |       -0.186 |            nan     |      0.143 |      -0.337 |           nan     |
| QQQ                                                                    |     0.134 |     -0.534 |       0.177 |       -0.161 |            nan     |      0.194 |      -0.351 |           nan     |

| strategy (2018+)   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| sector winner      |  0.809 |         -0.087 |    -1.384 |    0.150 |        0.803 |  0.007 |   -0.406 |         0.017 |        -0.254 |
| no sector rule     |  0.955 |          0.063 |     0.785 |    0.698 |        0.803 |  0.177 |   -0.411 |         0.431 |        -0.320 |

Year by year:

|     year |   sector winner |   no sector rule |    SPY |
|---------:|----------------:|-----------------:|-------:|
| 2010.000 |           0.108 |            0.050 |  0.131 |
| 2011.000 |           0.070 |           -0.075 |  0.019 |
| 2012.000 |           0.235 |            0.191 |  0.160 |
| 2013.000 |           0.528 |            0.368 |  0.323 |
| 2014.000 |           0.071 |            0.222 |  0.135 |
| 2015.000 |           0.064 |           -0.054 |  0.012 |
| 2016.000 |           0.144 |            0.093 |  0.120 |
| 2017.000 |           0.340 |            0.236 |  0.217 |
| 2018.000 |          -0.067 |           -0.018 | -0.046 |
| 2019.000 |           0.024 |            0.031 |  0.312 |
| 2020.000 |          -0.072 |            0.279 |  0.183 |
| 2021.000 |           0.178 |            0.291 |  0.287 |
| 2022.000 |          -0.155 |           -0.067 | -0.182 |
| 2023.000 |           0.081 |            0.216 |  0.262 |
| 2024.000 |           0.220 |            0.094 |  0.249 |
| 2025.000 |           0.077 |            0.147 |  0.177 |
| 2026.000 |          -0.146 |            0.784 |  0.128 |

### Today's sector table (like the user's BofA table, but reported, not estimated, EPS growth)

| sector                 | ETF   |     1w |     1m |     3m |     6m |   pct_above_50d |   EPS_growth_now |   EPS_growth_qtr_ago | top_leaders      |
|:-----------------------|:------|-------:|-------:|-------:|-------:|----------------:|-----------------:|---------------------:|:-----------------|
| Energy                 | XLE   |  0.049 |  0.065 |  0.185 |  0.257 |           0.762 |            1.071 |                0.183 | MPC, VLO, PSX    |
| Consumer Staples       | XLP   |  0.050 |  0.056 |  0.039 |  0.077 |           0.706 |            0.056 |                0.025 | EL, SJM, KDP     |
| Health Care            | XLV   |  0.035 |  0.051 |  0.114 |  0.197 |           0.729 |            0.150 |                0.146 | MRNA, HUM, VEEV  |
| Utilities              | XLU   |  0.019 |  0.020 | -0.054 | -0.073 |           0.710 |            0.067 |                0.089 | AES              |
| Consumer Discretionary | XLY   | -0.003 |  0.012 | -0.017 | -0.062 |           0.396 |            0.053 |                0.005 | BBY, WSM, ABNB   |
| Materials              | XLB   |  0.030 |  0.009 |  0.022 | -0.010 |           0.480 |            0.100 |                0.112 | IFF, CTVA, ECL   |
| Financials             | XLF   |  0.014 | -0.003 | -0.006 |  0.066 |           0.349 |            0.250 |                0.227 | FDS, MET, V      |
| Industrials            | XLI   | -0.009 | -0.005 | -0.056 | -0.028 |           0.296 |            0.132 |                0.106 | ADP, EXPD, IEX   |
| Information Technology | XLK   | -0.077 | -0.023 |  0.045 |  0.191 |           0.333 |            0.366 |                0.240 | NTAP, DDOG, ZBRA |

Winner's sectors today: Health Care, Consumer Staples, Energy. Its holdings at the last close:

| ticker   | entry_date          |   entry |    last |   gain |   stop |   trail_level |
|:---------|:--------------------|--------:|--------:|-------:|-------:|--------------:|
| MRNA     | 2026-09-30 00:00:00 | 192.570 | 218.010 |  0.132 |    nan |           nan |
| MPC      | 2026-10-16 00:00:00 | 478.070 | 478.070 |  0.000 |    nan |           nan |
| HUM      | 2026-10-16 00:00:00 | 413.160 | 413.160 |  0.000 |    nan |           nan |
| VLO      | 2026-10-16 00:00:00 | 444.710 | 444.710 |  0.000 |    nan |           nan |
| PSX      | 2026-10-16 00:00:00 | 293.170 | 293.170 |  0.000 |    nan |           nan |
| VEEV     | 2026-10-16 00:00:00 | 310.360 | 310.360 |  0.000 |    nan |           nan |
| CNC      | 2026-10-16 00:00:00 |  69.160 |  69.160 |  0.000 |    nan |           nan |
| CRL      | 2026-10-16 00:00:00 | 300.150 | 300.150 |  0.000 |    nan |           nan |
| RVTY     | 2026-10-16 00:00:00 | 152.640 | 152.640 |  0.000 |    nan |           nan |
| IQV      | 2026-10-16 00:00:00 | 266.900 | 266.900 |  0.000 |    nan |           nan |
| A        | 2026-10-16 00:00:00 | 172.970 | 172.970 |  0.000 |    nan |           nan |
| EL       | 2026-10-16 00:00:00 | 104.540 | 104.540 |  0.000 |    nan |           nan |
| APA      | 2026-10-16 00:00:00 |  49.150 |  49.150 |  0.000 |    nan |           nan |
| ABBV     | 2026-10-16 00:00:00 | 285.420 | 285.420 |  0.000 |    nan |           nan |
| WST      | 2026-10-16 00:00:00 | 384.020 | 384.020 |  0.000 |    nan |           nan |

### The user's rule: buy the best S&P 500 stock(s) of the past 12 months

Members on that date only (no price or liquidity filter), ranked by 12-month return, equal weight.

|   stocks | exit                                 | buy            |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|---------:|:-------------------------------------|:---------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
|        1 | hold 12 months (re-rank each year)   | once a year    |    -0.176 |     -0.967 |           -0.182 |          12 |    0.583 |       251.667 |      0.805 |      -0.555 |             1.451 |            6 |     0.833 |        293.333 |      -0.144 |       -0.966 |             -0.149 |            12 |      0.583 |         251.667 |
|        1 | monthly: sell if out of the top 20   | once a year    |    -0.101 |     -0.930 |           -0.108 |          11 |    0.273 |       162.909 |      0.466 |      -0.555 |             0.840 |            4 |     1.000 |        255.250 |      -0.097 |       -0.930 |             -0.104 |            11 |      0.273 |         162.909 |
|        1 | monthly: sell if out of the top 20   | refill monthly |    -0.239 |     -0.994 |           -0.240 |          22 |    0.500 |       132.500 |      0.330 |      -0.674 |             0.489 |           10 |     0.700 |        190.400 |      -0.107 |       -0.952 |             -0.112 |            22 |      0.500 |         132.500 |
|        1 | close below 50-day                   | once a year    |    -0.068 |     -0.616 |           -0.111 |          12 |    0.250 |        15.750 |      0.113 |      -0.314 |             0.359 |            8 |     0.750 |         36.625 |      -0.073 |       -0.453 |             -0.161 |            12 |      0.250 |          15.750 |
|        1 | close below 50-day                   | refill monthly |    -0.065 |     -0.867 |           -0.076 |          76 |    0.421 |        22.921 |      0.029 |      -0.696 |             0.042 |           71 |     0.451 |         16.930 |      -0.008 |       -0.657 |             -0.012 |            76 |      0.421 |          22.921 |
|        1 | monthly: sell if 12-month return < 0 | once a year    |    -0.103 |     -0.887 |           -0.116 |          12 |    0.417 |       210.917 |      0.705 |      -0.555 |             1.270 |            7 |     0.857 |        221.286 |      -0.042 |       -0.887 |             -0.047 |            12 |      0.417 |         210.917 |
|        1 | monthly: sell if 12-month return < 0 | refill monthly |    -0.155 |     -0.974 |           -0.159 |          17 |    0.412 |       177.647 |      0.695 |      -0.555 |             1.252 |            9 |     0.778 |        195.556 |       0.071 |       -0.878 |              0.081 |            17 |      0.412 |         177.647 |
|        3 | hold 12 months (re-rank each year)   | once a year    |     0.040 |     -0.840 |            0.047 |          34 |    0.588 |       259.088 |      0.553 |      -0.412 |             1.341 |           19 |     0.789 |        277.895 |       0.172 |       -0.701 |              0.245 |            34 |      0.588 |         259.088 |
|        3 | monthly: sell if out of the top 20   | once a year    |     0.045 |     -0.656 |            0.069 |          30 |    0.400 |       136.633 |      0.198 |      -0.404 |             0.490 |           15 |     0.600 |        139.733 |       0.095 |       -0.656 |              0.145 |            30 |      0.400 |         136.633 |
|        3 | monthly: sell if out of the top 20   | refill monthly |    -0.047 |     -0.794 |           -0.059 |          65 |    0.385 |       126.492 |      0.215 |      -0.497 |             0.432 |           38 |     0.526 |        144.921 |       0.078 |       -0.547 |              0.143 |            65 |      0.385 |         126.492 |
|        3 | close below 50-day                   | once a year    |    -0.036 |     -0.385 |           -0.094 |          36 |    0.333 |        19.639 |      0.065 |      -0.157 |             0.412 |           24 |     0.583 |         24.708 |      -0.023 |       -0.262 |             -0.090 |            36 |      0.333 |          19.639 |
|        3 | close below 50-day                   | refill monthly |    -0.061 |     -0.807 |           -0.076 |         244 |    0.389 |        20.385 |      0.095 |      -0.404 |             0.236 |          195 |     0.426 |         19.236 |      -0.001 |       -0.582 |             -0.001 |           244 |      0.389 |          20.385 |
|        3 | monthly: sell if 12-month return < 0 | once a year    |     0.062 |     -0.771 |            0.080 |          34 |    0.500 |       219.235 |      0.482 |      -0.412 |             1.170 |           20 |     0.750 |        228.200 |       0.146 |       -0.717 |              0.204 |            34 |      0.500 |         219.235 |
|        3 | monthly: sell if 12-month return < 0 | refill monthly |    -0.008 |     -0.898 |           -0.009 |          49 |    0.429 |       178.959 |      0.451 |      -0.412 |             1.095 |           25 |     0.600 |        212.800 |       0.129 |       -0.761 |              0.170 |            49 |      0.429 |         178.959 |
|        5 | hold 12 months (re-rank each year)   | once a year    |     0.040 |     -0.773 |            0.051 |          57 |    0.596 |       260.509 |      0.346 |      -0.385 |             0.899 |           31 |     0.645 |        267.645 |       0.180 |       -0.550 |              0.327 |            57 |      0.596 |         260.509 |
|        5 | monthly: sell if out of the top 20   | once a year    |     0.049 |     -0.482 |            0.101 |          52 |    0.462 |       126.269 |      0.176 |      -0.366 |             0.481 |           29 |     0.448 |        112.690 |       0.100 |       -0.482 |              0.207 |            52 |      0.462 |         126.269 |
|        5 | monthly: sell if out of the top 20   | refill monthly |    -0.010 |     -0.805 |           -0.013 |         111 |    0.459 |       121.351 |      0.175 |      -0.443 |             0.394 |           70 |     0.471 |        136.286 |       0.112 |       -0.566 |              0.197 |           111 |      0.459 |         121.351 |
|        5 | close below 50-day                   | once a year    |    -0.011 |     -0.264 |           -0.041 |          60 |    0.350 |        24.833 |      0.049 |      -0.159 |             0.309 |           40 |     0.575 |         23.375 |       0.009 |       -0.129 |              0.073 |            60 |      0.350 |          24.833 |
|        5 | close below 50-day                   | refill monthly |    -0.027 |     -0.749 |           -0.036 |         402 |    0.393 |        20.761 |      0.070 |      -0.373 |             0.187 |          331 |     0.393 |         18.326 |       0.025 |       -0.555 |              0.046 |           402 |      0.393 |          20.761 |
|        5 | monthly: sell if 12-month return < 0 | once a year    |     0.065 |     -0.635 |            0.102 |          57 |    0.491 |       215.667 |      0.294 |      -0.370 |             0.793 |           34 |     0.559 |        205.500 |       0.156 |       -0.529 |              0.295 |            57 |      0.491 |         215.667 |
|        5 | monthly: sell if 12-month return < 0 | refill monthly |     0.000 |     -0.828 |            0.000 |          83 |    0.434 |       176.904 |      0.302 |      -0.383 |             0.788 |           44 |     0.523 |        199.455 |       0.140 |       -0.603 |              0.232 |            83 |      0.434 |         176.904 |
|       10 | hold 12 months (re-rank each year)   | once a year    |     0.008 |     -0.713 |            0.012 |         113 |    0.558 |       262.814 |      0.253 |      -0.390 |             0.648 |           61 |     0.721 |        267.934 |       0.117 |       -0.409 |              0.287 |           113 |      0.558 |         262.814 |
|       10 | monthly: sell if out of the top 20   | once a year    |     0.029 |     -0.398 |            0.074 |         107 |    0.467 |       102.692 |      0.115 |      -0.304 |             0.378 |           66 |     0.485 |         95.879 |       0.073 |       -0.309 |              0.237 |           107 |      0.467 |         102.692 |
|       10 | monthly: sell if out of the top 20   | refill monthly |     0.035 |     -0.700 |            0.050 |         250 |    0.476 |       107.544 |      0.204 |      -0.385 |             0.529 |          164 |     0.500 |        110.848 |       0.146 |       -0.362 |              0.402 |           250 |      0.476 |         107.544 |
|       10 | close below 50-day                   | once a year    |     0.001 |     -0.216 |            0.006 |         120 |    0.392 |        26.158 |      0.025 |      -0.158 |             0.161 |           80 |     0.438 |         19.762 |       0.017 |       -0.122 |              0.140 |           120 |      0.392 |          26.158 |
|       10 | close below 50-day                   | refill monthly |    -0.006 |     -0.613 |           -0.010 |         792 |    0.395 |        20.547 |      0.079 |      -0.301 |             0.264 |          644 |     0.401 |         18.831 |       0.050 |       -0.360 |              0.139 |           792 |      0.395 |          20.547 |
|       10 | monthly: sell if 12-month return < 0 | once a year    |     0.035 |     -0.572 |            0.061 |         113 |    0.442 |       208.743 |      0.176 |      -0.382 |             0.460 |           65 |     0.569 |        209.785 |       0.117 |       -0.347 |              0.337 |           113 |      0.442 |         208.743 |
|       10 | monthly: sell if 12-month return < 0 | refill monthly |    -0.019 |     -0.781 |           -0.025 |         169 |    0.402 |       171.254 |      0.204 |      -0.384 |             0.530 |           83 |     0.566 |        210.422 |       0.088 |       -0.511 |              0.172 |           169 |      0.402 |         171.254 |

Does it depend on the month you start? Hold 12 months, bought at each of the 12 month-ends (median / worst / best):

|   stocks |   IS_CAGR_median |   IS_CAGR_min |   IS_CAGR_max |   IS_maxDD_median |   IS_maxDD_min |   IS_maxDD_max |   OOS_CAGR_median |   OOS_CAGR_min |   OOS_CAGR_max |   OOS_maxDD_median |   OOS_maxDD_min |   OOS_maxDD_max |
|---------:|-----------------:|--------------:|--------------:|------------------:|---------------:|---------------:|------------------:|---------------:|---------------:|-------------------:|----------------:|----------------:|
|    1.000 |           -0.076 |        -0.221 |         0.226 |            -0.948 |         -0.994 |         -0.686 |             0.021 |         -0.192 |          0.805 |             -0.769 |          -0.964 |          -0.555 |
|    3.000 |            0.028 |        -0.056 |         0.090 |            -0.789 |         -0.896 |         -0.692 |             0.172 |          0.083 |          0.553 |             -0.532 |          -0.662 |          -0.412 |
|    5.000 |            0.040 |         0.002 |         0.091 |            -0.725 |         -0.811 |         -0.672 |             0.177 |          0.090 |          0.346 |             -0.502 |          -0.606 |          -0.385 |
|   10.000 |            0.051 |         0.008 |         0.074 |            -0.701 |         -0.775 |         -0.645 |             0.189 |          0.104 |          0.311 |             -0.410 |          -0.496 |          -0.367 |

One stock, bought every 31 Dec: the picks

| ticker   | date_in             | date_out            |    ret |
|:---------|:--------------------|:--------------------|-------:|
| ATI      | 2006-12-29 00:00:00 | 2007-12-31 00:00:00 | -0.042 |
| AAPL     | 2007-12-31 00:00:00 | 2008-12-31 00:00:00 | -0.569 |
| HRB      | 2008-12-31 00:00:00 | 2009-12-31 00:00:00 |  0.030 |
| EP       | 2009-12-31 00:00:00 | 2010-12-31 00:00:00 | -0.681 |
| NFLX     | 2010-12-31 00:00:00 | 2011-12-30 00:00:00 | -0.606 |
| ISRG     | 2011-12-30 00:00:00 | 2012-12-31 00:00:00 |  0.059 |
| PHM      | 2012-12-31 00:00:00 | 2013-12-31 00:00:00 |  0.131 |
| NFLX     | 2013-12-31 00:00:00 | 2014-12-31 00:00:00 | -0.072 |
| LUV      | 2014-12-31 00:00:00 | 2015-12-31 00:00:00 |  0.024 |
| NFLX     | 2015-12-31 00:00:00 | 2016-12-30 00:00:00 |  0.082 |
| NVDA     | 2016-12-30 00:00:00 | 2017-12-29 00:00:00 |  0.820 |
| NRG      | 2017-12-29 00:00:00 | 2018-12-31 00:00:00 |  0.396 |
| AMD      | 2018-12-31 00:00:00 | 2020-12-31 00:00:00 |  3.968 |
| TSLA     | 2020-12-31 00:00:00 | 2021-12-31 00:00:00 |  0.498 |
| DVN      | 2021-12-31 00:00:00 | 2022-12-30 00:00:00 |  0.509 |
| OXY      | 2022-12-30 00:00:00 | 2023-12-29 00:00:00 | -0.041 |
| NVDA     | 2023-12-29 00:00:00 | 2024-12-31 00:00:00 |  1.712 |
| PLTR     | 2024-12-31 00:00:00 | 2025-12-31 00:00:00 |  1.350 |

|     year |   best stock of the year |    SPY |
|---------:|-------------------------:|-------:|
| 2007.000 |                   -0.044 |  0.053 |
| 2008.000 |                   -0.570 | -0.368 |
| 2009.000 |                    0.028 |  0.264 |
| 2010.000 |                   -0.681 |  0.151 |
| 2011.000 |                   -0.606 |  0.019 |
| 2012.000 |                    0.057 |  0.160 |
| 2013.000 |                    0.129 |  0.323 |
| 2014.000 |                   -0.074 |  0.135 |
| 2015.000 |                    0.022 |  0.012 |
| 2016.000 |                    0.080 |  0.120 |
| 2017.000 |                    0.816 |  0.217 |
| 2018.000 |                    0.393 | -0.046 |
| 2019.000 |                    1.484 |  0.312 |
| 2020.000 |                    0.996 |  0.183 |
| 2021.000 |                    0.495 |  0.287 |
| 2022.000 |                    0.506 | -0.182 |
| 2023.000 |                   -0.043 |  0.262 |
| 2024.000 |                    1.707 |  0.249 |
| 2025.000 |                    1.346 |  0.177 |
| 2026.000 |                    0.929 |  0.128 |

Stocks per sector (incl. former members assigned by correlation):

| sector                 |   stocks |
|:-----------------------|---------:|
| Financials             |      368 |
| Industrials            |      285 |
| Information Technology |      232 |
| Consumer Discretionary |      201 |
| Health Care            |      162 |
| Materials              |       79 |
| Energy                 |       77 |
| Consumer Staples       |       76 |
| Utilities              |       63 |

## 18. Run 27: a diversified 10-20 stock momentum book, and should a long-term holder use a stop?

Leaders only (rising 50-day above the 200-day, near 52-week highs, >= $10, >= $20M/day), S&P 500 point-in-time incl. former members, equal weight. Every version rebalances monthly (sells what fell out of the top 2N at month-end); the exit rules are added on top. 432 configurations: 10/15/20 stocks x 2 momentum ranks x fundamentals (none / sales >= 20% and EPS >= 25%) x buying daily or at month-ends x QQQ > 200d rule x 9 exits. Chosen on 2010-2017 (IS10, when SEC fundamentals exist); judged on 2018+ (OOS). 0.1% per side.

The stop question: median over all configurations for each exit rule:

| exit                             |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_win |   OOS_avg_days |
|:---------------------------------|------------:|-------------:|-------------------:|-----------:|------------:|------------------:|----------:|---------------:|
| no stop (monthly rebalance only) |       0.067 |       -0.226 |              0.259 |      0.135 |      -0.364 |             0.394 |     0.464 |         46.734 |
| fixed 8% stop                    |       0.045 |       -0.250 |              0.176 |      0.123 |      -0.350 |             0.368 |     0.424 |         38.993 |
| wide stop 2.5 x ADR              |       0.043 |       -0.265 |              0.179 |      0.118 |      -0.350 |             0.353 |     0.412 |         37.970 |
| wide stop 3 x ADR                |       0.048 |       -0.261 |              0.167 |      0.121 |      -0.357 |             0.347 |     0.431 |         40.152 |
| close below 50-day               |       0.025 |       -0.264 |              0.091 |      0.093 |      -0.279 |             0.310 |     0.370 |         25.605 |
| 50-day + 3 x ADR stop            |       0.026 |       -0.265 |              0.099 |      0.095 |      -0.285 |             0.304 |     0.362 |         24.944 |
| 50-day + fundamentals break      |       0.016 |       -0.262 |              0.070 |      0.053 |      -0.266 |             0.201 |     0.448 |         12.874 |
| close below 200-day              |       0.066 |       -0.227 |              0.263 |      0.120 |      -0.350 |             0.362 |     0.453 |         44.488 |
| fundamentals break only          |       0.043 |       -0.229 |              0.193 |      0.094 |      -0.349 |             0.283 |     0.499 |         20.162 |

Best configuration for each exit rule (chosen on 2010-2017):

|   N | rank by   | fundamentals   | buy       | regime     | exit                             |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|----:|:----------|:---------------|:----------|:-----------|:---------------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
|  20 | qull_best | none           | daily     | none       | no stop (monthly rebalance only) |     0.087 |     -0.430 |            0.202 |        1074 |    0.496 |        48.403 |      0.151 |      -0.351 |             0.431 |          909 |     0.488 |         44.301 |       0.136 |       -0.218 |              0.623 |          1074 |      0.496 |          48.403 |
|  20 | mom_6m1m  | none           | daily     | none       | close below 200-day              |     0.068 |     -0.426 |            0.161 |        1051 |    0.454 |        48.842 |      0.110 |      -0.384 |             0.286 |          896 |     0.459 |         45.281 |       0.115 |       -0.195 |              0.591 |          1051 |      0.454 |          48.842 |
|  15 | mom_6m1m  | none           | month-end | none       | fundamentals break only          |     0.055 |     -0.436 |            0.125 |        1018 |    0.524 |        30.112 |      0.094 |      -0.361 |             0.260 |          948 |     0.497 |         22.945 |       0.091 |       -0.168 |              0.541 |          1018 |      0.524 |          30.112 |
|  20 | qull_best | none           | daily     | none       | fixed 8% stop                    |     0.071 |     -0.418 |            0.171 |        1226 |    0.457 |        42.009 |      0.124 |      -0.378 |             0.328 |         1117 |     0.432 |         36.446 |       0.120 |       -0.245 |              0.488 |          1226 |      0.457 |          42.009 |
|  20 | qull_best | none           | daily     | none       | wide stop 2.5 x ADR              |     0.062 |     -0.457 |            0.135 |        1302 |    0.444 |        39.703 |      0.138 |      -0.397 |             0.347 |         1124 |     0.442 |         36.211 |       0.110 |       -0.243 |              0.450 |          1302 |      0.444 |          39.703 |
|  20 | qull_best | none           | daily     | none       | wide stop 3 x ADR                |     0.061 |     -0.452 |            0.135 |        1223 |    0.465 |        42.296 |      0.125 |      -0.412 |             0.304 |         1085 |     0.447 |         37.765 |       0.106 |       -0.246 |              0.433 |          1223 |      0.465 |          42.296 |
|  20 | qull_best | none           | daily     | none       | close below 50-day               |     0.040 |     -0.440 |            0.090 |        1972 |    0.395 |        26.080 |      0.084 |      -0.371 |             0.225 |         1632 |     0.374 |         25.363 |       0.079 |       -0.262 |              0.302 |          1972 |      0.395 |          26.080 |
|  20 | qull_best | none           | daily     | none       | 50-day + 3 x ADR stop            |     0.041 |     -0.434 |            0.095 |        2023 |    0.394 |        25.420 |      0.085 |      -0.362 |             0.236 |         1685 |     0.370 |         24.399 |       0.079 |       -0.267 |              0.298 |          2023 |      0.394 |          25.420 |
|  20 | qull_best | none           | month-end | QQQ > 200d | 50-day + fundamentals break      |     0.030 |     -0.249 |            0.121 |        1397 |    0.475 |        19.566 |      0.044 |      -0.203 |             0.219 |         1193 |     0.468 |         14.902 |       0.037 |       -0.210 |              0.178 |          1397 |      0.475 |          19.566 |

Number of stocks (median):

|      N |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |
|-------:|------------:|-------------:|-------------------:|-----------:|------------:|------------------:|
| 10.000 |       0.037 |       -0.311 |              0.125 |      0.122 |      -0.370 |             0.367 |
| 15.000 |       0.042 |       -0.247 |              0.179 |      0.104 |      -0.332 |             0.353 |
| 20.000 |       0.037 |       -0.217 |              0.189 |      0.077 |      -0.283 |             0.287 |

Other settings (median):

| value              |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD | setting      |
|:-------------------|------------:|-------------:|-------------------:|-----------:|------------:|------------------:|:-------------|
| none               |       0.072 |       -0.261 |              0.250 |      0.130 |      -0.381 |             0.359 | fundamentals |
| sales + EPS growth |       0.027 |       -0.240 |              0.112 |      0.084 |      -0.284 |             0.296 | fundamentals |
| daily              |       0.043 |       -0.267 |              0.166 |      0.110 |      -0.349 |             0.353 | buy          |
| month-end          |       0.036 |       -0.242 |              0.151 |      0.090 |      -0.310 |             0.298 | buy          |
| QQQ > 200d         |       0.036 |       -0.252 |              0.147 |      0.107 |      -0.291 |             0.367 | regime       |
| none               |       0.043 |       -0.255 |              0.181 |      0.096 |      -0.354 |             0.285 | regime       |
| mom_6m1m           |       0.038 |       -0.248 |              0.156 |      0.097 |      -0.336 |             0.307 | rank by      |
| qull_best          |       0.041 |       -0.260 |              0.167 |      0.108 |      -0.334 |             0.356 | rank by      |

Top 10 overall (by 2010-2017 return / drawdown). Winner: 20, qull_best, none, daily, none, no stop (monthly rebalance only)

|   N | rank by   | fundamentals   | buy       | regime   | exit                             |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|----:|:----------|:---------------|:----------|:---------|:---------------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
|  20 | qull_best | none           | daily     | none     | no stop (monthly rebalance only) |     0.087 |     -0.430 |            0.202 |        1074 |    0.496 |        48.403 |      0.151 |      -0.351 |             0.431 |          909 |     0.488 |         44.301 |       0.136 |       -0.218 |              0.623 |          1074 |      0.496 |          48.403 |
|  20 | mom_6m1m  | none           | daily     | none     | no stop (monthly rebalance only) |     0.074 |     -0.416 |            0.178 |        1013 |    0.466 |        51.094 |      0.139 |      -0.387 |             0.358 |          857 |     0.473 |         47.131 |       0.117 |       -0.195 |              0.603 |          1013 |      0.466 |          51.094 |
|  20 | qull_best | none           | month-end | none     | no stop (monthly rebalance only) |     0.080 |     -0.429 |            0.186 |        1037 |    0.501 |        48.860 |      0.138 |      -0.351 |             0.393 |          903 |     0.484 |         43.891 |       0.130 |       -0.218 |              0.596 |          1037 |      0.501 |          48.860 |
|  20 | mom_6m1m  | none           | month-end | none     | no stop (monthly rebalance only) |     0.073 |     -0.409 |            0.179 |         979 |    0.470 |        51.788 |      0.128 |      -0.387 |             0.330 |          845 |     0.464 |         46.985 |       0.116 |       -0.195 |              0.596 |           979 |      0.470 |          51.788 |
|  20 | mom_6m1m  | none           | daily     | none     | close below 200-day              |     0.068 |     -0.426 |            0.161 |        1051 |    0.454 |        48.842 |      0.110 |      -0.384 |             0.286 |          896 |     0.459 |         45.281 |       0.115 |       -0.195 |              0.591 |          1051 |      0.454 |          48.842 |
|  20 | qull_best | none           | daily     | none     | close below 200-day              |     0.078 |     -0.433 |            0.181 |        1115 |    0.482 |        46.233 |      0.119 |      -0.378 |             0.316 |          950 |     0.471 |         42.447 |       0.128 |       -0.219 |              0.582 |          1115 |      0.482 |          46.233 |
|  15 | mom_6m1m  | none           | daily     | none     | no stop (monthly rebalance only) |     0.075 |     -0.466 |            0.161 |         787 |    0.471 |        49.667 |      0.177 |      -0.411 |             0.431 |          670 |     0.479 |         45.642 |       0.120 |       -0.209 |              0.573 |           787 |      0.471 |          49.667 |
|  15 | mom_6m1m  | none           | daily     | none     | close below 200-day              |     0.074 |     -0.465 |            0.159 |         812 |    0.457 |        47.563 |      0.147 |      -0.408 |             0.361 |          695 |     0.459 |         43.929 |       0.116 |       -0.210 |              0.556 |           812 |      0.457 |          47.563 |
|  20 | mom_6m1m  | none           | month-end | none     | close below 200-day              |     0.066 |     -0.401 |            0.165 |         986 |    0.459 |        50.196 |      0.112 |      -0.384 |             0.293 |          846 |     0.453 |         46.220 |       0.109 |       -0.197 |              0.552 |           986 |      0.459 |          50.196 |
|  15 | qull_best | none           | daily     | none     | no stop (monthly rebalance only) |     0.076 |     -0.443 |            0.172 |         844 |    0.480 |        46.226 |      0.172 |      -0.375 |             0.458 |          708 |     0.503 |         42.747 |       0.125 |       -0.230 |              0.545 |           844 |      0.480 |          46.226 |

Benchmarks:

| benchmark                                         |   IS10_CAGR |   IS10_maxDD |   OOS_CAGR |   OOS_maxDD |
|:--------------------------------------------------|------------:|-------------:|-----------:|------------:|
| SPY                                               |       0.136 |       -0.186 |      0.143 |      -0.337 |
| QQQ                                               |       0.177 |       -0.161 |      0.194 |      -0.351 |
| simple top-10 momentum, monthly, no stop (run 24) |       0.115 |       -0.199 |      0.128 |      -0.412 |

| strategy (2018+)   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| run 27 winner, PIT |  0.903 |          0.040 |     0.567 |    0.659 |        0.803 |  0.151 |   -0.351 |         0.431 |        -0.271 |

Year by year (winner vs SPY):

|     year |   winner |    SPY |
|---------:|---------:|-------:|
| 2010.000 |    0.175 |  0.131 |
| 2011.000 |   -0.052 |  0.019 |
| 2012.000 |    0.174 |  0.160 |
| 2013.000 |    0.381 |  0.323 |
| 2014.000 |    0.213 |  0.135 |
| 2015.000 |   -0.049 |  0.012 |
| 2016.000 |    0.089 |  0.120 |
| 2017.000 |    0.220 |  0.217 |
| 2018.000 |   -0.021 | -0.046 |
| 2019.000 |    0.085 |  0.312 |
| 2020.000 |    0.288 |  0.183 |
| 2021.000 |    0.228 |  0.287 |
| 2022.000 |   -0.053 | -0.182 |
| 2023.000 |    0.050 |  0.262 |
| 2024.000 |    0.077 |  0.249 |
| 2025.000 |    0.212 |  0.177 |
| 2026.000 |    0.594 |  0.128 |

Winner's trades in NVDA / SNDK-type leaders:

| ticker   | date_in             | date_out            |   days |    ret |
|:---------|:--------------------|:--------------------|-------:|-------:|
| ANET     | 2019-04-30 00:00:00 | 2019-05-31 00:00:00 |     22 | -0.217 |
| ANET     | 2020-07-31 00:00:00 | 2020-08-31 00:00:00 |     21 | -0.140 |
| ANET     | 2021-11-30 00:00:00 | 2022-01-31 00:00:00 |     42 |  0.002 |
| ANET     | 2022-11-30 00:00:00 | 2022-12-30 00:00:00 |     21 | -0.129 |
| ANET     | 2023-03-31 00:00:00 | 2023-05-31 00:00:00 |     41 | -0.009 |
| ANET     | 2023-08-31 00:00:00 | 2023-11-30 00:00:00 |     63 |  0.125 |
| ANET     | 2023-12-29 00:00:00 | 2024-04-30 00:00:00 |     83 |  0.089 |
| ANET     | 2024-06-28 00:00:00 | 2024-08-30 00:00:00 |     44 |  0.008 |
| ANET     | 2024-12-31 00:00:00 | 2025-01-31 00:00:00 |     20 |  0.043 |
| ANET     | 2025-07-31 00:00:00 | 2025-11-28 00:00:00 |     84 |  0.061 |
| APP      | 2025-09-30 00:00:00 | 2025-11-28 00:00:00 |     42 | -0.166 |
| APP      | 2025-12-31 00:00:00 | 2026-01-30 00:00:00 |     20 | -0.298 |
| AVGO     | 2015-05-29 00:00:00 | 2015-07-31 00:00:00 |     44 | -0.152 |
| AVGO     | 2015-12-31 00:00:00 | 2016-01-29 00:00:00 |     19 | -0.079 |
| AVGO     | 2018-12-31 00:00:00 | 2019-05-31 00:00:00 |    104 | -0.002 |
| AVGO     | 2021-12-31 00:00:00 | 2022-01-31 00:00:00 |     20 | -0.120 |
| AVGO     | 2023-05-31 00:00:00 | 2023-09-29 00:00:00 |     84 |  0.039 |
| AVGO     | 2024-06-28 00:00:00 | 2024-08-30 00:00:00 |     44 |  0.014 |
| AVGO     | 2024-12-31 00:00:00 | 2025-01-31 00:00:00 |     20 | -0.046 |
| AVGO     | 2025-05-30 00:00:00 | 2025-12-31 00:00:00 |    148 |  0.438 |
| CRWD     | 2024-06-28 00:00:00 | 2024-07-31 00:00:00 |     22 | -0.395 |
| CRWD     | 2025-01-31 00:00:00 | 2025-03-31 00:00:00 |     40 | -0.114 |
| CRWD     | 2026-05-29 00:00:00 | 2026-10-16 00:00:00 |     97 |  0.244 |
| META     | 2023-03-31 00:00:00 | 2023-08-31 00:00:00 |    105 |  0.396 |
| META     | 2024-02-29 00:00:00 | 2024-04-30 00:00:00 |     42 | -0.122 |
| NVDA     | 2020-07-31 00:00:00 | 2020-10-30 00:00:00 |     64 |  0.181 |
| NVDA     | 2021-06-30 00:00:00 | 2021-09-30 00:00:00 |     64 |  0.036 |
| NVDA     | 2021-10-29 00:00:00 | 2022-01-31 00:00:00 |     63 | -0.042 |
| NVDA     | 2023-02-28 00:00:00 | 2023-09-29 00:00:00 |    148 |  0.874 |
| NVDA     | 2024-01-31 00:00:00 | 2024-07-31 00:00:00 |    125 |  0.902 |
| NVDA     | 2024-10-31 00:00:00 | 2024-11-29 00:00:00 |     20 |  0.041 |
| PLTR     | 2024-09-30 00:00:00 | 2025-02-28 00:00:00 |    103 |  1.283 |
| PLTR     | 2025-05-30 00:00:00 | 2025-11-28 00:00:00 |    126 |  0.278 |
| SMCI     | 2024-03-28 00:00:00 | 2024-04-30 00:00:00 |     22 | -0.150 |
| SMCI     | 2025-07-31 00:00:00 | 2025-08-29 00:00:00 |     21 | -0.296 |
| SNDK     | 2025-11-28 00:00:00 | 2026-07-31 00:00:00 |    167 |  4.441 |
| VRT      | 2026-03-31 00:00:00 | 2026-07-31 00:00:00 |     84 | -0.036 |

Winner's holdings at the last close:

| ticker   | entry_date          |   entry |    last |   gain |   stop |   trail_level |
|:---------|:--------------------|--------:|--------:|-------:|-------:|--------------:|
| NTAP     | 2026-07-31 00:00:00 | 178.098 | 203.800 |  0.144 |    nan |           nan |
| MPC      | 2026-07-31 00:00:00 | 315.606 | 478.070 |  0.515 |    nan |           nan |
| VLO      | 2026-07-31 00:00:00 | 312.900 | 444.710 |  0.421 |    nan |           nan |
| PSX      | 2026-07-31 00:00:00 | 210.562 | 293.170 |  0.392 |    nan |           nan |
| CRL      | 2026-07-31 00:00:00 | 232.510 | 300.150 |  0.291 |    nan |           nan |
| MRNA     | 2026-08-31 00:00:00 | 140.340 | 218.010 |  0.553 |    nan |           nan |
| VEEV     | 2026-08-31 00:00:00 | 285.690 | 310.360 |  0.086 |    nan |           nan |
| ZBRA     | 2026-08-31 00:00:00 | 353.550 | 369.010 |  0.044 |    nan |           nan |
| PTC      | 2026-10-16 00:00:00 | 192.980 | 192.980 |  0.000 |    nan |           nan |
| HUM      | 2026-10-16 00:00:00 | 413.160 | 413.160 |  0.000 |    nan |           nan |
| CTSH     | 2026-10-16 00:00:00 |  66.030 |  66.030 |  0.000 |    nan |           nan |
| IT       | 2026-10-16 00:00:00 | 205.350 | 205.350 |  0.000 |    nan |           nan |
| RVTY     | 2026-10-16 00:00:00 | 152.640 | 152.640 |  0.000 |    nan |           nan |
| DDOG     | 2026-10-16 00:00:00 | 247.110 | 247.110 |  0.000 |    nan |           nan |
| APA      | 2026-10-16 00:00:00 |  49.150 |  49.150 |  0.000 |    nan |           nan |
| CRM      | 2026-10-16 00:00:00 | 240.700 | 240.700 |  0.000 |    nan |           nan |
| CNC      | 2026-10-16 00:00:00 |  69.160 |  69.160 |  0.000 |    nan |           nan |
| PLTR     | 2026-10-16 00:00:00 | 186.030 | 186.030 |  0.000 |    nan |           nan |

## 17. Runs 25-26: concentrated leader portfolio (3-5 stocks) on top traders' rules, with fundamentals

Hold N stocks (equal weight), decided at every close. Leaders only: price >= $10, >= $20M/day, above a rising 50-day that is above the 200-day, within 25% of the 52-week high; S&P 500 members at the time (incl. later-removed ones). Entry: best-ranked leader into an empty slot (optionally only within 3 days of a top-trader setup: episodic pivot / breakout / base / flag / VCP; optionally only while QQQ > 200-day). Exit at the close: below the 10/20/50-day average, 8% below entry, or (rank) out of the top 3N. 0.1% per side. 144 configurations x 7 fundamentals filters; the winner is chosen on 2007-2017 return / drawdown only.

Top 10 configurations by IS (2007-2017) CAGR / max drawdown, with their OOS (2018+) results:

|   N | rank by   | exit   | regime     | entry          | fundamentals                 |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|----:|:----------|:-------|:-----------|:---------------|:-----------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
|   4 | mom_12_1  | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.061 |     -0.216 |            0.283 |         177 |    0.452 |        40.497 |      0.101 |      -0.275 |             0.367 |          205 |     0.390 |         35.341 |       0.068 |       -0.216 |              0.316 |           177 |      0.452 |          40.497 |
|   3 | mom_12_1  | sma20  | none       | setup required | EPS growth >= 25% (O'Neil C) |     0.049 |     -0.184 |            0.265 |         296 |    0.446 |        16.899 |      0.109 |      -0.355 |             0.306 |          388 |     0.433 |         14.698 |       0.056 |       -0.184 |              0.305 |           296 |      0.446 |          16.899 |
|   5 | qull_best | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.057 |     -0.221 |            0.258 |         209 |    0.474 |        42.354 |      0.081 |      -0.298 |             0.272 |          251 |     0.410 |         35.363 |       0.065 |       -0.221 |              0.296 |           209 |      0.474 |          42.354 |
|   5 | mom_6m1m  | sma50  | QQQ > 200d | any leader     | EPS growth >= 25% (O'Neil C) |     0.074 |     -0.293 |            0.251 |         305 |    0.436 |        32.370 |      0.144 |      -0.344 |             0.419 |          324 |     0.380 |         28.725 |       0.079 |       -0.293 |              0.268 |           305 |      0.436 |          32.370 |
|   4 | mom_6m1m  | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.057 |     -0.233 |            0.244 |         172 |    0.483 |        41.866 |      0.069 |      -0.267 |             0.258 |          208 |     0.404 |         34.433 |       0.062 |       -0.233 |              0.268 |           172 |      0.483 |          41.866 |
|   5 | qull_best | sma50  | none       | setup required | EPS growth >= 25% (O'Neil C) |     0.049 |     -0.217 |            0.224 |         224 |    0.446 |        40.478 |      0.068 |      -0.325 |             0.209 |          286 |     0.406 |         34.168 |       0.054 |       -0.217 |              0.248 |           224 |      0.446 |          40.478 |
|   5 | mom_6m1m  | sma50  | none       | any leader     | EPS growth >= 25% (O'Neil C) |     0.076 |     -0.343 |            0.221 |         336 |    0.432 |        31.167 |      0.123 |      -0.448 |             0.274 |          396 |     0.348 |         26.843 |       0.082 |       -0.343 |              0.238 |           336 |      0.432 |          31.167 |
|   5 | mom_6m1m  | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.046 |     -0.216 |            0.214 |         218 |    0.468 |        40.798 |      0.069 |      -0.263 |             0.263 |          253 |     0.419 |         35.209 |       0.051 |       -0.216 |              0.234 |           218 |      0.468 |          40.798 |
|   3 | qull_best | sma50  | none       | setup required | EPS growth >= 25% (O'Neil C) |     0.062 |     -0.292 |            0.214 |         133 |    0.474 |        42.556 |      0.112 |      -0.371 |             0.303 |          174 |     0.408 |         34.534 |       0.069 |       -0.292 |              0.236 |           133 |      0.474 |          42.556 |
|   3 | mom_6m1m  | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.061 |     -0.284 |            0.214 |         130 |    0.485 |        42.023 |      0.101 |      -0.270 |             0.373 |          158 |     0.405 |         34.456 |       0.063 |       -0.284 |              0.220 |           130 |      0.485 |          42.023 |

Run 26: do fundamentals confirming the move help? Median over the same 144 configurations for each filter (sales growth = revenue YoY from SEC filings; EPS = diluted EPS YoY or turning positive; earnings gap = >= 5% gap up on an earnings day in the last 3 months), and the share of configurations where the filter beat no filter on return / drawdown:

| fundamentals                      |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   share_beating_none_IS |   share_beating_none_OOS |
|:----------------------------------|----------:|-----------:|-----------------:|-----------:|------------:|------------------:|------------------------:|-------------------------:|
| none                              |    -0.040 |     -0.651 |           -0.064 |      0.056 |      -0.462 |             0.127 |                   0.000 |                    0.000 |
| sales growth >= 20%               |     0.007 |     -0.404 |            0.019 |      0.077 |      -0.385 |             0.203 |                   0.854 |                    0.681 |
| EPS growth >= 25% (O'Neil C)      |     0.020 |     -0.361 |            0.065 |      0.082 |      -0.425 |             0.213 |                   1.000 |                    0.743 |
| sales >= 20% and EPS >= 25%       |     0.006 |     -0.387 |            0.019 |      0.114 |      -0.350 |             0.364 |                   0.854 |                    0.833 |
| sales + EPS, revenue accelerating |     0.013 |     -0.339 |            0.043 |      0.056 |      -0.336 |             0.183 |                   0.840 |                    0.681 |
| earnings gap up in last 3 months  |    -0.018 |     -0.480 |           -0.043 |      0.071 |      -0.380 |             0.190 |                   0.389 |                    0.771 |
| sales + EPS + earnings gap        |    -0.003 |     -0.303 |           -0.012 |      0.054 |      -0.335 |             0.189 |                   0.708 |                    0.681 |

Best configuration that requires fundamentals (chosen on IS):

|   N | rank by   | exit   | regime     | entry          | fundamentals                 |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|----:|:----------|:-------|:-----------|:---------------|:-----------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
|   4 | mom_12_1  | sma50  | QQQ > 200d | setup required | EPS growth >= 25% (O'Neil C) |     0.061 |     -0.216 |            0.283 |         177 |    0.452 |        40.497 |      0.101 |      -0.275 |             0.367 |          205 |     0.390 |         35.341 |       0.068 |       -0.216 |              0.316 |           177 |      0.452 |          40.497 |

Case study: trades in NVDA / SNDK-type leaders (NVDA, SNDK, PLTR, SMCI, META, AVGO, VRT, ANET, CRWD, APP):

| version                         | ticker   | date_in             | date_out            |   days |    ret |
|:--------------------------------|:---------|:--------------------|:--------------------|-------:|-------:|
| CAN SLIM style (pre-registered) | ANET     | 2019-03-22 00:00:00 | 2019-05-03 00:00:00 |     29 | -0.072 |
| CAN SLIM style (pre-registered) | ANET     | 2021-12-15 00:00:00 | 2022-01-07 00:00:00 |     16 | -0.066 |
| IS winner                       | ANET     | 2023-03-09 00:00:00 | 2023-05-02 00:00:00 |     37 | -0.092 |
| best with fundamentals (IS)     | ANET     | 2023-03-09 00:00:00 | 2023-05-02 00:00:00 |     37 | -0.092 |
| CAN SLIM style (pre-registered) | ANET     | 2023-08-04 00:00:00 | 2023-09-21 00:00:00 |     33 | -0.010 |
| CAN SLIM style (pre-registered) | ANET     | 2023-10-31 00:00:00 | 2024-04-12 00:00:00 |    112 |  0.354 |
| IS winner                       | ANET     | 2023-11-02 00:00:00 | 2024-04-12 00:00:00 |    110 |  0.281 |
| best with fundamentals (IS)     | ANET     | 2023-11-02 00:00:00 | 2024-04-12 00:00:00 |    110 |  0.281 |
| CAN SLIM style (pre-registered) | ANET     | 2026-07-07 00:00:00 | 2026-07-29 00:00:00 |     16 | -0.051 |
| IS winner                       | AVGO     | 2025-09-11 00:00:00 | 2025-09-29 00:00:00 |     12 | -0.087 |
| best with fundamentals (IS)     | AVGO     | 2025-09-11 00:00:00 | 2025-09-29 00:00:00 |     12 | -0.087 |
| IS winner                       | CRWD     | 2026-08-27 00:00:00 | 2026-09-02 00:00:00 |      4 | -0.108 |
| best with fundamentals (IS)     | CRWD     | 2026-08-27 00:00:00 | 2026-09-02 00:00:00 |      4 | -0.108 |
| CAN SLIM style (pre-registered) | CRWD     | 2026-08-27 00:00:00 | 2026-09-02 00:00:00 |      4 | -0.108 |
| CAN SLIM style (pre-registered) | CRWD     | 2026-09-02 00:00:00 | 2026-10-16 00:00:00 |     31 |  0.118 |
| IS winner                       | CRWD     | 2026-09-11 00:00:00 | 2026-10-16 00:00:00 |     25 |  0.100 |
| best with fundamentals (IS)     | CRWD     | 2026-09-11 00:00:00 | 2026-10-16 00:00:00 |     25 |  0.100 |
| CAN SLIM style (pre-registered) | META     | 2024-02-02 00:00:00 | 2024-04-19 00:00:00 |     53 |  0.014 |
| CAN SLIM style (pre-registered) | META     | 2024-07-05 00:00:00 | 2024-07-15 00:00:00 |      6 | -0.081 |
| CAN SLIM style (pre-registered) | NVDA     | 2021-05-21 00:00:00 | 2021-08-18 00:00:00 |     61 |  0.270 |
| IS winner                       | NVDA     | 2024-05-23 00:00:00 | 2024-07-24 00:00:00 |     41 |  0.101 |
| best with fundamentals (IS)     | NVDA     | 2024-05-23 00:00:00 | 2024-07-24 00:00:00 |     41 |  0.101 |
| CAN SLIM style (pre-registered) | NVDA     | 2024-05-23 00:00:00 | 2024-07-24 00:00:00 |     41 |  0.101 |
| CAN SLIM style (pre-registered) | NVDA     | 2025-10-29 00:00:00 | 2025-11-06 00:00:00 |      6 | -0.092 |
| CAN SLIM style (pre-registered) | NVDA     | 2026-04-29 00:00:00 | 2026-06-10 00:00:00 |     29 | -0.041 |
| IS winner                       | PLTR     | 2024-12-20 00:00:00 | 2025-01-07 00:00:00 |     10 | -0.131 |
| best with fundamentals (IS)     | PLTR     | 2024-12-20 00:00:00 | 2025-01-07 00:00:00 |     10 | -0.131 |
| CAN SLIM style (pre-registered) | PLTR     | 2024-12-20 00:00:00 | 2025-01-07 00:00:00 |     10 | -0.131 |
| CAN SLIM style (pre-registered) | PLTR     | 2025-02-04 00:00:00 | 2025-02-24 00:00:00 |     13 | -0.127 |
| IS winner                       | PLTR     | 2025-05-12 00:00:00 | 2025-09-03 00:00:00 |     78 |  0.308 |
| best with fundamentals (IS)     | PLTR     | 2025-05-12 00:00:00 | 2025-09-03 00:00:00 |     78 |  0.308 |
| CAN SLIM style (pre-registered) | PLTR     | 2025-05-12 00:00:00 | 2025-09-03 00:00:00 |     78 |  0.308 |
| IS winner                       | VRT      | 2026-04-08 00:00:00 | 2026-06-05 00:00:00 |     41 |  0.069 |
| best with fundamentals (IS)     | VRT      | 2026-04-08 00:00:00 | 2026-06-05 00:00:00 |     41 |  0.069 |

Pre-registered trader-style versions (not selected on any results):

|   N | rank by   | exit       | regime     | entry          | fundamentals                |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days | style                                                                                          |
|----:|:----------|:-----------|:-----------|:---------------|:----------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|:-----------------------------------------------------------------------------------------------|
|   4 | qull_best | sma20      | QQQ > 200d | setup required | none                        |    -0.008 |     -0.444 |           -0.019 |         560 |    0.427 |        16.159 |      0.063 |      -0.280 |             0.226 |          471 |     0.399 |         15.456 |       0.020 |       -0.284 |              0.071 |           560 |      0.427 |          16.159 | Qullamaggie style (best-of 1/3/6m RS, setup, 20-day trail, QQQ > 200d, 4 stocks)               |
|   4 | mom_6m1m  | sma50      | QQQ > 200d | setup required | none                        |     0.037 |     -0.283 |            0.129 |         243 |    0.444 |        38.580 |      0.112 |      -0.264 |             0.424 |          217 |     0.359 |         34.074 |       0.030 |       -0.283 |              0.107 |           243 |      0.444 |          38.580 | Minervini / O'Neil style (6m/1m momentum, setup, 50-day trail, QQQ > 200d, 4 stocks)           |
|   5 | mom_6m1m  | sma50_rank | none       | any leader     | none                        |     0.001 |     -0.725 |            0.002 |         688 |    0.378 |        19.653 |      0.106 |      -0.510 |             0.208 |          593 |     0.379 |         18.250 |       0.054 |       -0.473 |              0.114 |           688 |      0.378 |          19.653 | Pure leader rotation (6m/1m momentum, any leader, 50-day + rank, no regime, 5 stocks)          |
|   4 | mom_6m1m  | sma50      | QQQ > 200d | setup required | sales >= 20% and EPS >= 25% |     0.012 |     -0.291 |            0.040 |         126 |    0.381 |        36.659 |      0.107 |      -0.269 |             0.396 |          167 |     0.389 |         34.695 |       0.009 |       -0.291 |              0.031 |           126 |      0.381 |          36.659 | CAN SLIM style (6m/1m momentum, setup, 50-day trail, QQQ > 200d, sales + EPS growth, 4 stocks) |

IS winner: 4, mom_12_1, sma50, QQQ > 200d, setup required, EPS growth >= 25% (O'Neil C). Robustness:

| version                                       |   IS_CAGR |   IS_maxDD |   IS_CAGR_per_DD |   IS_trades |   IS_win |   IS_avg_days |   OOS_CAGR |   OOS_maxDD |   OOS_CAGR_per_DD |   OOS_trades |   OOS_win |   OOS_avg_days |   IS10_CAGR |   IS10_maxDD |   IS10_CAGR_per_DD |   IS10_trades |   IS10_win |   IS10_avg_days |
|:----------------------------------------------|----------:|-----------:|-----------------:|------------:|---------:|--------------:|-----------:|------------:|------------------:|-------------:|----------:|---------------:|------------:|-------------:|-------------------:|--------------:|-----------:|----------------:|
| IS winner, S&P 500 point-in-time (0.1%/side)  |     0.061 |     -0.216 |            0.283 |         177 |    0.452 |        40.497 |      0.101 |      -0.275 |             0.367 |          205 |     0.390 |         35.341 |       0.068 |       -0.216 |              0.316 |           177 |      0.452 |          40.497 |
| IS winner, S&P 500 point-in-time, 0.3%/side   |     0.045 |     -0.239 |            0.188 |         177 |    0.452 |        40.497 |      0.076 |      -0.318 |             0.240 |          205 |     0.390 |         35.341 |       0.046 |       -0.239 |              0.195 |           177 |      0.452 |          40.497 |
| IS winner, all stocks (survivorship-inflated) |     0.052 |     -0.363 |            0.144 |         193 |    0.456 |        38.943 |      0.230 |      -0.328 |             0.699 |          235 |     0.370 |         31.140 |       0.050 |       -0.363 |              0.137 |           193 |      0.456 |          38.943 |

Benchmarks (same periods):

| benchmark   |   IS_CAGR |   IS_maxDD |   OOS_CAGR |   OOS_maxDD |
|:------------|----------:|-----------:|-----------:|------------:|
| SPY         |     0.082 |     -0.552 |      0.143 |      -0.337 |
| QQQ         |     0.134 |     -0.534 |      0.194 |      -0.351 |

| strategy (2018+)   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| IS winner, PIT     |  0.472 |          0.046 |     0.733 |    0.574 |        0.803 |  0.101 |   -0.275 |         0.367 |        -0.146 |

Year by year (IS winner vs SPY):

|     year |   IS winner |    SPY |
|---------:|------------:|-------:|
| 2007.000 |       0.000 |  0.053 |
| 2008.000 |       0.000 | -0.368 |
| 2009.000 |       0.121 |  0.264 |
| 2010.000 |       0.126 |  0.151 |
| 2011.000 |      -0.055 |  0.019 |
| 2012.000 |       0.120 |  0.160 |
| 2013.000 |       0.295 |  0.323 |
| 2014.000 |       0.096 |  0.135 |
| 2015.000 |      -0.021 |  0.012 |
| 2016.000 |      -0.068 |  0.120 |
| 2017.000 |       0.109 |  0.217 |
| 2018.000 |      -0.088 | -0.046 |
| 2019.000 |       0.093 |  0.312 |
| 2020.000 |       0.034 |  0.183 |
| 2021.000 |       0.122 |  0.287 |
| 2022.000 |      -0.066 | -0.182 |
| 2023.000 |      -0.045 |  0.262 |
| 2024.000 |       0.427 |  0.249 |
| 2025.000 |       0.195 |  0.177 |
| 2026.000 |       0.331 |  0.128 |

Today's portfolio (IS winner, as of the last close):

| ticker   | entry_date          |   entry |    last |   gain |    stop |   trail_level |
|:---------|:--------------------|--------:|--------:|-------:|--------:|--------------:|
| VLO      | 2026-09-02 00:00:00 | 366.090 | 444.710 |  0.215 | 336.803 |       381.631 |
| PLTR     | 2026-09-22 00:00:00 | 184.990 | 186.030 |  0.006 | 170.191 |       182.569 |
| NTAP     | 2026-09-30 00:00:00 | 209.607 | 203.800 | -0.028 | 192.839 |       201.652 |
| COP      | 2026-10-16 00:00:00 | 146.510 | 146.510 |  0.000 | 134.789 |       131.673 |

## 16. Run 24: consolidated tests

### Earnings placebo: do gaps drift because of earnings news?
Gap setups split by whether an earnings release (SEC 8-K Item 2.02) was filed that day or up to 3 days before. If 'no earnings' gaps do as well, post-earnings drift is not the reason the setup works.

| group                    | earnings         |   IS_n |   OOS_n |   IS_avgR_sma50 |   OOS_avgR_sma50 |   IS_win_sma50 |   OOS_win_sma50 |   IS_avgR_b20 |   OOS_avgR_b20 |
|:-------------------------|:-----------------|-------:|--------:|----------------:|-----------------:|---------------:|----------------:|--------------:|---------------:|
| episodic pivots (ep_*)   | earnings release |   3512 |    5435 |           0.276 |            0.434 |          0.339 |           0.330 |         0.226 |          0.150 |
| episodic pivots (ep_*)   | no earnings      |   1561 |    2111 |           0.230 |            0.093 |          0.282 |           0.243 |         0.135 |          0.012 |
| gap >= 5% holding 2 days | earnings release |   1058 |    1262 |           0.107 |            0.136 |          0.323 |           0.316 |         0.130 |          0.091 |
| gap >= 5% holding 2 days | no earnings      |   1906 |    2747 |           0.161 |            0.335 |          0.315 |           0.320 |         0.166 |          0.205 |
| random entries           | earnings release |   1470 |    1539 |           0.054 |           -0.016 |          0.171 |           0.191 |         0.154 |          0.055 |
| random entries           | no earnings      |  30237 |   32814 |           0.068 |           -0.024 |          0.152 |           0.138 |         0.198 |          0.096 |

### Holding through earnings (course: don't, without a cushion)
Goal model top 10%, +20/-10, by days from entry to the next earnings release:

| next earnings in   |   IS_n |   OOS_n |   IS_hit |   OOS_hit |   IS_avg_ret |   OOS_avg_ret |
|:-------------------|-------:|--------:|---------:|----------:|-------------:|--------------:|
| <= 7 days          |   1663 |    2103 |    0.352 |     0.419 |        0.020 |         0.033 |
| 8-30 days          |   5709 |    8060 |    0.348 |     0.417 |        0.022 |         0.036 |
| 31-63 days         |   6865 |    9973 |    0.328 |     0.372 |        0.016 |         0.022 |
| > 63 days          |   6891 |    8098 |    0.309 |     0.365 |        0.013 |         0.022 |

### Survivorship: current members only vs incl. former S&P 500 members

| point-in-time S&P 500                     |   trades_OOS |   hit_OOS |   avg_ret_OOS |   CAGR |   max_DD |
|:------------------------------------------|-------------:|----------:|--------------:|-------:|---------:|
| current members only (as before)          |         3861 |     0.392 |         0.035 |  0.171 |   -0.277 |
| incl. former members (membership history) |         4672 |     0.382 |         0.030 |  0.137 |   -0.331 |

### Is the edge real? Year by year vs same-volatility, same-momentum stocks

|   year |    n |   hit |   matched_hit |   edge_hit |   edge_ret | sample                |
|-------:|-----:|------:|--------------:|-----------:|-----------:|:----------------------|
|   2008 | 1786 | 0.219 |         0.210 |      0.009 |     -0.001 | full universe         |
|   2009 | 1626 | 0.403 |         0.384 |      0.019 |      0.008 | full universe         |
|   2010 | 1753 | 0.442 |         0.342 |      0.100 |      0.022 | full universe         |
|   2011 | 1954 | 0.404 |         0.297 |      0.107 |      0.014 | full universe         |
|   2012 | 1918 | 0.404 |         0.337 |      0.067 |      0.016 | full universe         |
|   2013 | 2112 | 0.360 |         0.337 |      0.023 |     -0.000 | full universe         |
|   2014 | 2312 | 0.254 |         0.229 |      0.026 |     -0.006 | full universe         |
|   2015 | 2447 | 0.131 |         0.173 |     -0.042 |     -0.031 | full universe         |
|   2016 | 2561 | 0.385 |         0.333 |      0.053 |     -0.003 | full universe         |
|   2017 | 2741 | 0.344 |         0.315 |      0.029 |      0.001 | full universe         |
|   2018 | 3002 | 0.258 |         0.271 |     -0.013 |     -0.014 | full universe         |
|   2019 | 3004 | 0.370 |         0.351 |      0.019 |     -0.003 | full universe         |
|   2020 | 3064 | 0.526 |         0.435 |      0.091 |      0.021 | full universe         |
|   2021 | 3280 | 0.401 |         0.299 |      0.102 |      0.026 | full universe         |
|   2022 | 3389 | 0.396 |         0.303 |      0.093 |      0.029 | full universe         |
|   2023 | 3453 | 0.345 |         0.328 |      0.017 |     -0.006 | full universe         |
|   2024 | 3691 | 0.367 |         0.336 |      0.031 |      0.003 | full universe         |
|   2025 | 3685 | 0.402 |         0.371 |      0.031 |      0.001 | full universe         |
|   2026 | 1982 | 0.420 |         0.386 |      0.035 |      0.011 | full universe         |
|   2008 |  478 | 0.215 |         0.208 |      0.008 |     -0.004 | S&P 500 point-in-time |
|   2009 |  631 | 0.395 |         0.387 |      0.007 |      0.006 | S&P 500 point-in-time |
|   2010 |  495 | 0.444 |         0.352 |      0.092 |      0.017 | S&P 500 point-in-time |
|   2011 |  483 | 0.418 |         0.301 |      0.117 |      0.017 | S&P 500 point-in-time |
|   2012 |  526 | 0.409 |         0.330 |      0.079 |      0.020 | S&P 500 point-in-time |
|   2013 |  414 | 0.357 |         0.316 |      0.041 |     -0.001 | S&P 500 point-in-time |
|   2014 |  306 | 0.186 |         0.201 |     -0.015 |     -0.014 | S&P 500 point-in-time |
|   2015 |  588 | 0.085 |         0.163 |     -0.078 |     -0.039 | S&P 500 point-in-time |
|   2016 |  509 | 0.361 |         0.322 |      0.039 |     -0.005 | S&P 500 point-in-time |
|   2017 |  342 | 0.225 |         0.288 |     -0.063 |     -0.023 | S&P 500 point-in-time |
|   2018 |  531 | 0.249 |         0.248 |      0.001 |     -0.008 | S&P 500 point-in-time |
|   2019 |  346 | 0.347 |         0.307 |      0.039 |      0.001 | S&P 500 point-in-time |
|   2020 |  698 | 0.490 |         0.419 |      0.071 |      0.017 | S&P 500 point-in-time |
|   2021 |  429 | 0.403 |         0.273 |      0.130 |      0.031 | S&P 500 point-in-time |
|   2022 |  790 | 0.422 |         0.298 |      0.123 |      0.039 | S&P 500 point-in-time |
|   2023 |  548 | 0.361 |         0.301 |      0.060 |      0.002 | S&P 500 point-in-time |
|   2024 |  429 | 0.324 |         0.320 |      0.004 |     -0.007 | S&P 500 point-in-time |
|   2025 |  544 | 0.381 |         0.350 |      0.030 |      0.003 | S&P 500 point-in-time |
|   2026 |  357 | 0.387 |         0.380 |      0.006 |     -0.001 | S&P 500 point-in-time |

### Market-adjusted (2018+): beta, alpha vs SPY, Sharpe, return / drawdown

| strategy (2018+)                                                   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------------------------------------------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| goal model top 10%, full universe                                  |  1.011 |          0.137 |     1.713 |    0.956 |        0.803 |  0.276 |   -0.342 |         0.807 |        -0.145 |
| goal model top 10%, S&P 500 PIT                                    |  0.829 |          0.036 |     0.511 |    0.625 |        0.803 |  0.137 |   -0.331 |         0.414 |        -0.137 |
| top 10, vol-adjusted (course 9.8), S&P 500 point-in-time           |  0.906 |          0.020 |     0.282 |    0.580 |        0.803 |  0.128 |   -0.412 |         0.311 |        -0.301 |
| top 20, vol-adjusted, S&P 500 point-in-time                        |  0.864 |          0.023 |     0.414 |    0.664 |        0.803 |  0.136 |   -0.326 |         0.416 |        -0.227 |
| top 10, raw momentum (not vol-adjusted), S&P 500 point-in-time     |  1.153 |          0.062 |     0.730 |    0.714 |        0.803 |  0.199 |   -0.410 |         0.485 |        -0.280 |
| SPY timed by breadth: buy < 20% above 20d, sell > 60% (course 2.2) |  0.540 |         -0.024 |    -0.743 |    0.419 |        0.803 |  0.050 |   -0.283 |         0.176 |        -0.125 |
| SPY timed by % above 50d (same thresholds)                         |  0.491 |         -0.010 |    -0.309 |    0.488 |        0.803 |  0.057 |   -0.283 |         0.203 |        -0.125 |
| SPY                                                                |  1.000 |         -0.000 |    -6.070 |    0.803 |        0.803 |  0.143 |   -0.337 |         0.425 |        -0.125 |

### Cost stress (0.3% per side)

| strategy                                                | costs         |   CAGR |   max_DD |
|:--------------------------------------------------------|:--------------|-------:|---------:|
| goal model top 10%, full universe                       | 0.1% per side |  0.276 |   -0.342 |
| goal model top 10%, full universe                       | 0.3% per side |  0.211 |   -0.382 |
| goal model top 10%, S&P 500 PIT                         | 0.1% per side |  0.137 |   -0.331 |
| goal model top 10%, S&P 500 PIT                         | 0.3% per side |  0.098 |   -0.369 |
| episodic pivots (gap 10% / 8% hold), RS top 20% / sma50 | 0.1% per side |  0.125 |   -0.249 |
| episodic pivots (gap 10% / 8% hold), RS top 20% / sma50 | 0.3% per side |  0.099 |   -0.263 |

### Replay of the daily picks tool's rule (top 10 per date, model retrained quarterly, 2023+)

| list    |   dates |   picks |   hit |   avg_ret |   median_ret |   share_dates_hit_ge_33% | model                                   |
|:--------|--------:|--------:|------:|----------:|-------------:|-------------------------:|:----------------------------------------|
| all     |      89 |     890 | 0.415 |     0.028 |       -0.102 |                    0.573 | picks tool as today (original features) |
| leaders |      89 |     890 | 0.397 |     0.026 |       -0.102 |                    0.584 | picks tool as today (original features) |
| all     |      89 |     890 | 0.394 |     0.023 |       -0.102 |                    0.573 | upgraded features (run-16 set)          |
| leaders |      89 |     890 | 0.392 |     0.024 |       -0.102 |                    0.562 | upgraded features (run-16 set)          |

### Course portfolios: volatility-adjusted momentum and breadth timing (IS 2007-2017, OOS 2018+)

| strategy                                                           |   IS_CAGR |   IS_maxDD |   OOS_CAGR |   OOS_maxDD |
|:-------------------------------------------------------------------|----------:|-----------:|-----------:|------------:|
| top 10, vol-adjusted (course 9.8), all stocks                      |     0.092 |     -0.573 |      0.300 |      -0.453 |
| top 10, vol-adjusted (course 9.8), S&P 500 point-in-time           |     0.061 |     -0.567 |      0.128 |      -0.412 |
| top 20, vol-adjusted, all stocks                                   |     0.090 |     -0.524 |      0.248 |      -0.427 |
| top 20, vol-adjusted, S&P 500 point-in-time                        |     0.061 |     -0.519 |      0.136 |      -0.326 |
| top 10, raw momentum (not vol-adjusted), all stocks                |     0.174 |     -0.660 |      0.492 |      -0.482 |
| top 10, raw momentum (not vol-adjusted), S&P 500 point-in-time     |     0.091 |     -0.610 |      0.199 |      -0.410 |
| SPY buy & hold                                                     |     0.082 |     -0.552 |      0.143 |      -0.337 |
| SPY timed by breadth: buy < 20% above 20d, sell > 60% (course 2.2) |     0.048 |     -0.289 |      0.050 |      -0.283 |
| SPY timed by % above 50d (same thresholds)                         |     0.014 |     -0.381 |      0.057 |      -0.283 |

### Course setups vs random entries (R multiples)

| entry             | filter   | exit          |   IS_n |   IS_avgR |   IS_win |   OOS_n |   OOS_avgR |   OOS_win |
|:------------------|:---------|:--------------|-------:|----------:|---------:|--------:|-----------:|----------:|
| random_uptrend    | all      | bracket_20_10 |  30882 |     0.190 |    0.532 |   34624 |      0.095 |     0.455 |
| tc_ema200_2nd     | all      | bracket_20_10 |   1140 |     0.113 |    0.492 |    1646 |      0.037 |     0.429 |
| tc_ema_cross_base | all      | bracket_20_10 |   7364 |     0.174 |    0.544 |    6977 |      0.034 |     0.451 |
| tc_reversal_base  | all      | bracket_20_10 |    173 |     0.465 |    0.572 |     160 |      0.050 |     0.406 |
| tc_supertrend_ema | all      | bracket_20_10 |  18970 |     0.212 |    0.529 |   23343 |      0.139 |     0.471 |
| random_uptrend    | all      | ema21_close   |  31645 |    -0.137 |    0.206 |   34624 |     -0.096 |     0.205 |
| tc_ema200_2nd     | all      | ema21_close   |   1158 |     0.001 |    0.344 |    1646 |     -0.055 |     0.303 |
| tc_ema_cross_base | all      | ema21_close   |   7537 |     0.007 |    0.368 |    6977 |     -0.005 |     0.358 |
| tc_reversal_base  | all      | ema21_close   |    172 |     0.133 |    0.459 |     160 |     -0.132 |     0.256 |
| tc_supertrend_ema | all      | ema21_close   |  19242 |     0.045 |    0.300 |   23343 |      0.045 |     0.293 |
| random_uptrend    | all      | sma50_close   |  31488 |    -0.033 |    0.146 |   34624 |     -0.025 |     0.140 |
| tc_ema200_2nd     | all      | sma50_close   |   1147 |     0.023 |    0.354 |    1646 |     -0.028 |     0.317 |
| tc_ema_cross_base | all      | sma50_close   |   7410 |     0.106 |    0.371 |    6977 |      0.039 |     0.346 |
| tc_reversal_base  | all      | sma50_close   |    170 |     0.279 |    0.418 |     160 |     -0.071 |     0.269 |
| tc_supertrend_ema | all      | sma50_close   |  19185 |     0.057 |    0.330 |   23343 |      0.027 |     0.334 |
| random_uptrend    | rs80     | bracket_20_10 |   9932 |     0.151 |    0.484 |   11674 |      0.100 |     0.434 |
| tc_ema200_2nd     | rs80     | bracket_20_10 |     38 |     0.105 |    0.447 |      49 |      0.315 |     0.490 |
| tc_ema_cross_base | rs80     | bracket_20_10 |   1443 |     0.145 |    0.502 |    1413 |      0.137 |     0.467 |
| tc_reversal_base  | rs80     | bracket_20_10 |      1 |     0.376 |    1.000 |       2 |      1.980 |     1.000 |
| tc_supertrend_ema | rs80     | bracket_20_10 |   2620 |     0.202 |    0.508 |    3028 |      0.066 |     0.429 |
| random_uptrend    | rs80     | ema21_close   |  10096 |    -0.149 |    0.201 |   11674 |     -0.091 |     0.202 |
| tc_ema200_2nd     | rs80     | ema21_close   |     38 |     0.031 |    0.421 |      49 |     -0.022 |     0.367 |
| tc_ema_cross_base | rs80     | ema21_close   |   1449 |     0.020 |    0.381 |    1413 |      0.052 |     0.374 |
| tc_reversal_base  | rs80     | ema21_close   |      1 |     0.064 |    1.000 |       2 |     -0.068 |     0.500 |
| tc_supertrend_ema | rs80     | ema21_close   |   2640 |     0.075 |    0.333 |    3028 |      0.027 |     0.301 |
| random_uptrend    | rs80     | sma50_close   |  10056 |    -0.089 |    0.144 |   11674 |     -0.026 |     0.139 |
| tc_ema200_2nd     | rs80     | sma50_close   |     38 |     0.038 |    0.474 |      49 |      0.056 |     0.408 |
| tc_ema_cross_base | rs80     | sma50_close   |   1434 |     0.102 |    0.377 |    1413 |      0.213 |     0.371 |
| tc_reversal_base  | rs80     | sma50_close   |      1 |     0.023 |    1.000 |       2 |     -0.984 |     0.000 |
| tc_supertrend_ema | rs80     | sma50_close   |   2623 |     0.129 |    0.336 |    3028 |      0.065 |     0.309 |

## 15. ADR%, volatility-matched check, parabolic shorts (run 23)

Is the goal model only picking volatile, strong stocks? Its top 10% vs the average of all stocks in the same year, ADR decile and 6-month-return quintile (+20/-10). edge = actual - matched:

| period   |     n |   hit |   matched_hit |   ret |   matched_ret |   edge_hit |   edge_ret | sample                            |
|:---------|------:|------:|--------------:|------:|--------------:|-----------:|-----------:|:----------------------------------|
| IS       | 21210 | 0.329 |         0.293 | 0.017 |         0.016 |      0.037 |      0.001 | goal model (full universe)        |
| OOS      | 28550 | 0.386 |         0.340 | 0.027 |         0.019 |      0.046 |      0.007 | goal model (full universe)        |
| IS       |  4772 | 0.315 |         0.291 | 0.016 |         0.018 |      0.025 |     -0.002 | goal model, S&P 500 point-in-time |
| OOS      |  4672 | 0.381 |         0.324 | 0.030 |         0.019 |      0.058 |      0.011 | goal model, S&P 500 point-in-time |

Setups by ADR% (stocks >= $10M/day, exit sma50_close, R multiples). The infographic says: < 5% too slow, 5-12% the sweet spot, > 15% often fails:

| setups                                  | ADR%   |       IS_n |   IS_avgR |   IS_win |      OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------|:-------|-----------:|----------:|---------:|-----------:|-----------:|----------:|
| all setups                              | < 3%   | 300781.000 |     0.149 |    0.291 | 281723.000 |     -0.048 |     0.257 |
| all setups                              | 3-5%   |  55945.000 |     0.003 |    0.273 | 106601.000 |      0.118 |     0.273 |
| all setups                              | 5-8%   |   8367.000 |    -0.125 |    0.237 |  18424.000 |      0.203 |     0.267 |
| all setups                              | 8-12%  |    476.000 |    -0.340 |    0.132 |    894.000 |      0.012 |     0.188 |
| all setups                              | 12-15% |     38.000 |    -0.792 |    0.105 |     61.000 |     -0.078 |     0.344 |
| all setups                              | > 15%  |     13.000 |    -0.595 |    0.462 |     13.000 |     -0.269 |     0.615 |
| breakouts (qull / rocket / base / flag) | < 3%   |   4472.000 |     0.127 |    0.332 |   4606.000 |      0.118 |     0.303 |
| breakouts (qull / rocket / base / flag) | 3-5%   |   5935.000 |    -0.064 |    0.236 |  11360.000 |      0.180 |     0.225 |
| breakouts (qull / rocket / base / flag) | 5-8%   |   1902.000 |    -0.241 |    0.179 |   4035.000 |      0.077 |     0.204 |
| breakouts (qull / rocket / base / flag) | 8-12%  |    265.000 |    -0.332 |    0.140 |    376.000 |     -0.196 |     0.138 |
| breakouts (qull / rocket / base / flag) | 12-15% |     11.000 |    -0.675 |    0.182 |     14.000 |     -0.572 |     0.143 |
| breakouts (qull / rocket / base / flag) | > 15%  |      3.000 |    -0.677 |    0.333 |      3.000 |     -0.346 |     0.333 |
| episodic pivots (ep_*)                  | < 3%   |   1728.000 |     0.166 |    0.328 |   1865.000 |      0.036 |     0.287 |
| episodic pivots (ep_*)                  | 3-5%   |   1872.000 |     0.415 |    0.332 |   3452.000 |      0.551 |     0.314 |
| episodic pivots (ep_*)                  | 5-8%   |    534.000 |     0.202 |    0.303 |   1449.000 |      0.309 |     0.310 |
| episodic pivots (ep_*)                  | 8-12%  |     83.000 |    -0.194 |    0.145 |    166.000 |     -0.448 |     0.187 |
| episodic pivots (ep_*)                  | 12-15% |     22.000 |    -0.923 |    0.045 |     33.000 |      0.498 |     0.545 |
| episodic pivots (ep_*)                  | > 15%  |      9.000 |    -0.328 |    0.556 |      8.000 |      0.150 |     0.875 |
| random entries                          | < 3%   |  20971.000 |     0.131 |    0.158 |  20931.000 |     -0.117 |     0.135 |
| random entries                          | 3-5%   |   4277.000 |    -0.193 |    0.134 |   8503.000 |      0.154 |     0.150 |
| random entries                          | 5-8%   |    819.000 |     0.177 |    0.173 |   1819.000 |      0.225 |     0.151 |
| random entries                          | 8-12%  |    136.000 |    -0.600 |    0.110 |    226.000 |      0.520 |     0.177 |
| random entries                          | 12-15% |     13.000 |    -0.733 |    0.077 |     21.000 |     -0.482 |     0.143 |
| random entries                          | > 15%  |      9.000 |    -0.988 |    0.000 |     11.000 |     -1.256 |     0.000 |

Qullamaggie's parabolic shorts (up >= 50% in 10 days, >= 3 up closes of 4, >= 20% above the 10-day; entry = first close below the prior day's low within 3 days, or no_trigger = short the parabolic day itself; stop = high of the run; cover at the 10- or 20-day average or after 20 days; price >= $5, >= $10M/day; borrow fees not included):

| variant    | cover   | period   |   n |   win |   avgR |    PF |   avg_ret |
|:-----------|:--------|:---------|----:|------:|-------:|------:|----------:|
| no_trigger | sma10   | IS       | 162 | 0.247 |  3.316 | 3.369 |     0.003 |
| no_trigger | sma10   | OOS      | 372 | 0.288 |  4.388 | 2.956 |     0.016 |
| no_trigger | sma20   | IS       | 162 | 0.198 |  3.768 | 3.573 |     0.006 |
| no_trigger | sma20   | OOS      | 372 | 0.231 |  4.791 | 3.070 |     0.014 |
| trigger    | sma10   | IS       |  94 | 0.596 | -0.065 | 0.771 |    -0.003 |
| trigger    | sma10   | OOS      | 204 | 0.613 |  0.132 | 1.421 |     0.011 |
| trigger    | sma20   | IS       |  94 | 0.479 | -0.178 | 0.636 |    -0.017 |
| trigger    | sma20   | OOS      | 204 | 0.510 |  0.064 | 1.135 |     0.006 |

Parabolic shorts (trigger, cover at the 10-day) by ADR%: count and average R

| adr_pct   |   ('size', 'IS') |   ('size', 'OOS') |   ('mean', 'IS') |   ('mean', 'OOS') |
|:----------|-----------------:|------------------:|-----------------:|------------------:|
| < 3%      |            1.000 |           nan     |           -1.048 |           nan     |
| 3-5%      |            3.000 |            14.000 |            0.063 |            -0.302 |
| 5-8%      |           20.000 |            82.000 |           -0.408 |             0.260 |
| 8-12%     |           32.000 |            88.000 |           -0.084 |             0.116 |
| 12-15%    |           24.000 |            12.000 |            0.187 |             0.023 |
| > 15%     |           14.000 |             8.000 |            0.079 |            -0.080 |

## 14. Your Stock Selection Workflow PDF, price-testable rules (run 20)

Rules as written, nothing tuned. Rockets: 6-week base -> new 52w high on 1.5x volume (<= 5% above the pivot, stop -8%) or a >= 5% gap on 2x volume holding its low for 2 days (no earnings dates: volume is the proxy); price >= $10, >= $20M/day, top 20% 6-month return; exit = sell 1/3 at +25%, stop to entry, trail the 50 SMA. Scanner: above a rising 200d, 50d > 200d, within 15% of the 52w high; entry = pullback to the 21 EMA / 50 SMA then a close above the prior high, a 4-week base breakout, or a holding gap; stop under the pullback/base low, skipped if > 10%; ranked by RS (40) + stop distance (30); exit = weekly close below the 10-week MA. Regime (QQQ): green full size, yellow half, red no new entries. Sizing: rockets 0.5% risk x 3 positions, scanner 0.6% x 4, max 10% per stock. Not testable here: fundamentals (guidance, revenue, FCF, estimates), the Singapore part, the Nasdaq-100 membership itself.

Per trade vs random entries with the same filter and exit (R multiples):

| entry              | filter          | exit          |   IS_n |   IS_avgR |   IS_win |   OOS_n |   OOS_avgR |   OOS_win |   OOS_t |
|:-------------------|:----------------|:--------------|-------:|----------:|---------:|--------:|-----------:|----------:|--------:|
| wf_rocket_gap      | wf_rocket       | bracket_20_10 |    688 |     0.092 |    0.453 |    1259 |      0.123 |     0.427 |   3.171 |
| random_uptrend     | wf_rocket       | bracket_20_10 |   5604 |     0.146 |    0.494 |    8637 |      0.092 |     0.439 |   6.532 |
| wf_rocket_breakout | wf_rocket       | bracket_20_10 |    464 |     0.078 |    0.461 |     800 |      0.075 |     0.444 |   1.622 |
| wf_rocket_gap      | wf_rocket       | sma50_close   |    694 |     0.070 |    0.310 |    1259 |      0.239 |     0.305 |   2.300 |
| wf_rocket_breakout | wf_rocket       | sma50_close   |    465 |     0.040 |    0.378 |     800 |      0.145 |     0.335 |   2.028 |
| random_uptrend     | wf_rocket       | sma50_close   |   5704 |    -0.131 |    0.146 |    8637 |     -0.041 |     0.138 |  -0.828 |
| wf_rocket_gap      | wf_rocket       | wf_rocket     |    694 |     0.066 |    0.313 |    1259 |      0.201 |     0.313 |   2.467 |
| wf_rocket_breakout | wf_rocket       | wf_rocket     |    465 |     0.052 |    0.385 |     800 |      0.117 |     0.344 |   1.859 |
| random_uptrend     | wf_rocket       | wf_rocket     |   5704 |    -0.120 |    0.147 |    8637 |     -0.038 |     0.143 |  -0.861 |
| wf_rocket_gap      | wf_rocket       | wf_weekly10   |    692 |     0.022 |    0.288 |    1259 |      0.186 |     0.285 |   2.226 |
| wf_rocket_breakout | wf_rocket       | wf_weekly10   |    464 |     0.041 |    0.373 |     800 |      0.116 |     0.333 |   1.677 |
| random_uptrend     | wf_rocket       | wf_weekly10   |   5703 |    -0.145 |    0.135 |    8637 |     -0.008 |     0.130 |  -0.150 |
| wf_rocket_gap      | wf_rocket_green | bracket_20_10 |    531 |     0.131 |    0.469 |    1050 |      0.184 |     0.447 |   4.262 |
| random_uptrend     | wf_rocket_green | bracket_20_10 |   4446 |     0.144 |    0.489 |    7039 |      0.117 |     0.444 |   7.361 |
| wf_rocket_breakout | wf_rocket_green | bracket_20_10 |    358 |     0.164 |    0.486 |     637 |      0.114 |     0.458 |   2.155 |
| wf_rocket_gap      | wf_rocket_green | sma50_close   |    537 |     0.136 |    0.328 |    1050 |      0.293 |     0.310 |   2.412 |
| wf_rocket_breakout | wf_rocket_green | sma50_close   |    359 |     0.115 |    0.404 |     637 |      0.190 |     0.341 |   2.308 |
| random_uptrend     | wf_rocket_green | sma50_close   |   4546 |    -0.187 |    0.143 |    7039 |     -0.033 |     0.136 |  -0.588 |
| wf_rocket_gap      | wf_rocket_green | wf_rocket     |    537 |     0.135 |    0.331 |    1050 |      0.245 |     0.319 |   2.601 |
| wf_rocket_breakout | wf_rocket_green | wf_rocket     |    359 |     0.136 |    0.412 |     637 |      0.160 |     0.349 |   2.195 |
| random_uptrend     | wf_rocket_green | wf_rocket     |   4546 |    -0.172 |    0.144 |    7039 |     -0.034 |     0.140 |  -0.684 |
| wf_rocket_gap      | wf_rocket_green | wf_weekly10   |    535 |     0.077 |    0.307 |    1050 |      0.235 |     0.293 |   2.450 |
| wf_rocket_breakout | wf_rocket_green | wf_weekly10   |    358 |     0.088 |    0.391 |     637 |      0.156 |     0.336 |   1.942 |
| random_uptrend     | wf_rocket_green | wf_weekly10   |   4545 |    -0.211 |    0.130 |    7039 |     -0.003 |     0.128 |  -0.048 |
| wf_rocket_gap      | wf_scan         | bracket_20_10 |   1419 |     0.212 |    0.505 |    1629 |      0.103 |     0.443 |   3.193 |
| wf_scan_pullback   | wf_scan         | bracket_20_10 |  70486 |     0.183 |    0.545 |   67927 |      0.090 |     0.470 |  19.647 |
| random_uptrend     | wf_scan         | bracket_20_10 |  21945 |     0.193 |    0.544 |   22280 |      0.084 |     0.460 |  10.316 |
| wf_scan_base       | wf_scan         | bracket_20_10 |  25142 |     0.198 |    0.582 |   17699 |      0.040 |     0.485 |   5.035 |
| wf_rocket_gap      | wf_scan         | sma50_close   |   1430 |     0.234 |    0.315 |    1629 |      0.095 |     0.292 |   1.177 |
| wf_scan_pullback   | wf_scan         | sma50_close   |  71281 |     0.056 |    0.283 |   67927 |      0.000 |     0.270 |   0.014 |
| wf_scan_base       | wf_scan         | sma50_close   |  25315 |     0.074 |    0.340 |   17699 |     -0.007 |     0.307 |  -0.765 |
| random_uptrend     | wf_scan         | sma50_close   |  22418 |    -0.014 |    0.148 |   22280 |     -0.093 |     0.139 |  -3.222 |
| wf_rocket_gap      | wf_scan         | wf_rocket     |   1430 |     0.221 |    0.318 |    1629 |      0.087 |     0.298 |   1.321 |
| wf_scan_pullback   | wf_scan         | wf_rocket     |  71281 |     0.056 |    0.284 |   67927 |      0.001 |     0.271 |   0.077 |
| wf_scan_base       | wf_scan         | wf_rocket     |  25315 |     0.074 |    0.340 |   17699 |     -0.005 |     0.307 |  -0.647 |
| random_uptrend     | wf_scan         | wf_rocket     |  22418 |    -0.011 |    0.148 |   22280 |     -0.083 |     0.141 |  -3.056 |
| wf_rocket_gap      | wf_scan         | wf_weekly10   |   1429 |     0.204 |    0.304 |    1629 |      0.044 |     0.277 |   0.679 |
| wf_scan_pullback   | wf_scan         | wf_weekly10   |  71120 |     0.087 |    0.294 |   67927 |      0.010 |     0.277 |   1.141 |
| wf_scan_base       | wf_scan         | wf_weekly10   |  25201 |     0.096 |    0.367 |   17699 |     -0.007 |     0.326 |  -0.747 |
| random_uptrend     | wf_scan         | wf_weekly10   |  22411 |    -0.015 |    0.138 |   22280 |     -0.069 |     0.131 |  -2.229 |
| wf_rocket_gap      | wf_scan_green   | bracket_20_10 |   1242 |     0.231 |    0.512 |    1483 |      0.132 |     0.453 |   3.871 |
| wf_scan_pullback   | wf_scan_green   | bracket_20_10 |  61579 |     0.169 |    0.538 |   59013 |      0.118 |     0.480 |  23.840 |
| random_uptrend     | wf_scan_green   | bracket_20_10 |  19387 |     0.180 |    0.538 |   19743 |      0.107 |     0.469 |  12.313 |
| wf_scan_base       | wf_scan_green   | bracket_20_10 |  22566 |     0.172 |    0.568 |   16052 |      0.048 |     0.485 |   5.655 |
| wf_rocket_gap      | wf_scan_green   | sma50_close   |   1253 |     0.258 |    0.322 |    1483 |      0.117 |     0.295 |   1.329 |
| wf_scan_pullback   | wf_scan_green   | sma50_close   |  62374 |     0.019 |    0.278 |   59013 |      0.022 |     0.273 |   2.382 |
| wf_scan_base       | wf_scan_green   | sma50_close   |  22739 |     0.037 |    0.327 |   16052 |      0.006 |     0.310 |   0.625 |
| random_uptrend     | wf_scan_green   | sma50_close   |  19860 |    -0.079 |    0.144 |   19743 |     -0.073 |     0.141 |  -2.343 |
| wf_rocket_gap      | wf_scan_green   | wf_rocket     |   1253 |     0.244 |    0.326 |    1483 |      0.105 |     0.301 |   1.477 |
| wf_scan_pullback   | wf_scan_green   | wf_rocket     |  62374 |     0.019 |    0.278 |   59013 |      0.023 |     0.274 |   2.739 |
| wf_scan_base       | wf_scan_green   | wf_rocket     |  22739 |     0.038 |    0.327 |   16052 |      0.007 |     0.310 |   0.794 |
| random_uptrend     | wf_scan_green   | wf_rocket     |  19860 |    -0.075 |    0.145 |   19743 |     -0.063 |     0.142 |  -2.159 |
| wf_rocket_gap      | wf_scan_green   | wf_weekly10   |   1252 |     0.224 |    0.315 |    1483 |      0.058 |     0.283 |   0.849 |
| wf_scan_pullback   | wf_scan_green   | wf_weekly10   |  62213 |     0.035 |    0.287 |   59013 |      0.031 |     0.281 |   3.234 |
| wf_scan_base       | wf_scan_green   | wf_weekly10   |  22625 |     0.051 |    0.353 |   16052 |      0.000 |     0.328 |   0.014 |
| random_uptrend     | wf_scan_green   | wf_weekly10   |  19853 |    -0.091 |    0.134 |   19743 |     -0.055 |     0.133 |  -1.655 |

Per trade by Nasdaq-100 regime at entry (the PDF's own exits):

| part                    | regime           |      IS_n |   IS_avgR |   IS_win |     OOS_n |   OOS_avgR |   OOS_win |
|:------------------------|:-----------------|----------:|----------:|---------:|----------:|-----------:|----------:|
| rockets                 | PDF red          |   158.000 |    -0.179 |    0.291 |   259.000 |     -0.019 |     0.328 |
| rockets                 | PDF yellow       |   105.000 |    -0.222 |    0.229 |   113.000 |     -0.064 |     0.239 |
| rockets                 | PDF green (200d) |   924.000 |     0.178 |    0.377 |  1687.000 |      0.213 |     0.330 |
| rockets                 | QQQ < both       |   194.000 |     0.197 |    0.392 |   301.000 |      0.026 |     0.296 |
| rockets                 | QQQ > 50 only    |   107.000 |     0.095 |    0.299 |   176.000 |      0.234 |     0.318 |
| rockets                 | QQQ > 21 only    |    72.000 |    -0.054 |    0.389 |    97.000 |      0.224 |     0.330 |
| rockets                 | QQQ > 21 & 50    |   814.000 |     0.084 |    0.346 |  1485.000 |      0.186 |     0.331 |
| scanner                 | PDF red          |  6979.000 |     0.453 |    0.381 |  7696.000 |     -0.198 |     0.250 |
| scanner                 | PDF yellow       |  4681.000 |     0.458 |    0.362 |  3011.000 |      0.078 |     0.283 |
| scanner                 | PDF green (200d) | 88326.000 |     0.119 |    0.316 | 76548.000 |      0.025 |     0.291 |
| scanner                 | QQQ < both       | 14492.000 |     0.273 |    0.362 | 14943.000 |      0.051 |     0.306 |
| scanner                 | QQQ > 50 only    | 11416.000 |     0.170 |    0.306 |  8900.000 |     -0.059 |     0.276 |
| scanner                 | QQQ > 21 only    |  5008.000 |     0.379 |    0.406 |  3990.000 |      0.091 |     0.334 |
| scanner                 | QQQ > 21 & 50    | 69070.000 |     0.116 |    0.311 | 59422.000 |      0.000 |     0.281 |
| random (rocket filter)  | PDF red          |   718.000 |     0.308 |    0.189 |  1176.000 |     -0.204 |     0.147 |
| random (rocket filter)  | PDF yellow       |   440.000 |    -0.280 |    0.114 |   422.000 |      0.357 |     0.171 |
| random (rocket filter)  | PDF green (200d) |  4616.000 |    -0.022 |    0.153 |  7039.000 |     -0.034 |     0.140 |
| random (rocket filter)  | QQQ < both       |   972.000 |     0.355 |    0.186 |  1616.000 |     -0.281 |     0.136 |
| random (rocket filter)  | QQQ > 50 only    |   688.000 |    -0.022 |    0.161 |   850.000 |     -0.040 |     0.159 |
| random (rocket filter)  | QQQ > 21 only    |   297.000 |     0.560 |    0.259 |   355.000 |      0.501 |     0.197 |
| random (rocket filter)  | QQQ > 21 & 50    |  3817.000 |    -0.131 |    0.137 |  5816.000 |     -0.004 |     0.139 |
| random (scanner filter) | PDF red          |  1435.000 |     0.634 |    0.181 |  1777.000 |     -0.453 |     0.113 |
| random (scanner filter) | PDF yellow       |  1123.000 |     0.498 |    0.150 |   760.000 |      0.464 |     0.139 |
| random (scanner filter) | PDF green (200d) | 20129.000 |     0.053 |    0.141 | 19743.000 |     -0.055 |     0.133 |
| random (scanner filter) | QQQ < both       |  3088.000 |     0.490 |    0.186 |  3825.000 |     -0.219 |     0.130 |
| random (scanner filter) | QQQ > 50 only    |  2681.000 |     0.140 |    0.138 |  2267.000 |     -0.141 |     0.130 |
| random (scanner filter) | QQQ > 21 only    |   923.000 |     0.475 |    0.193 |   826.000 |      0.153 |     0.166 |
| random (scanner filter) | QQQ > 21 & 50    | 15995.000 |     0.013 |    0.134 | 15362.000 |     -0.033 |     0.130 |

Portfolios 2018+ (marked to market daily):

| strategy                                                            |   CAGR |   max_DD |   trades |   win |   avg_positions |
|:--------------------------------------------------------------------|-------:|---------:|---------:|------:|----------------:|
| rockets as written (regime sizing) / wf_rocket                      |  0.021 |   -0.117 |      192 | 0.297 |           2.347 |
| rockets, no regime rule / wf_rocket                                 |  0.011 |   -0.117 |      236 | 0.305 |           2.719 |
| rockets, QQQ 21/50 regime / wf_rocket                               |  0.014 |   -0.088 |      193 | 0.311 |           2.435 |
| rockets / sma50_close                                               |  0.024 |   -0.106 |      191 | 0.293 |           2.348 |
| rockets / bracket_20_10                                             |  0.027 |   -0.088 |      175 | 0.446 |           2.422 |
| BASELINE random entries, rocket filter + regime / wf_rocket         |  0.011 |   -0.213 |      473 | 0.152 |           2.464 |
| rockets as written, S&P 500 point-in-time only / wf_rocket          |  0.013 |   -0.070 |      142 | 0.338 |           2.029 |
| scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10 |  0.008 |   -0.174 |      357 | 0.283 |           3.414 |
| scanner PIT, no regime rule / wf_weekly10                           |  0.003 |   -0.171 |      419 | 0.313 |           3.931 |
| scanner PIT, QQQ 21/50 regime / wf_weekly10                         | -0.025 |   -0.252 |      381 | 0.262 |           3.471 |
| scanner PIT / sma50_close                                           |  0.010 |   -0.192 |      394 | 0.266 |           3.353 |
| BASELINE random entries, scanner filter + regime, PIT / wf_weekly10 |  0.034 |   -0.166 |      518 | 0.156 |           3.303 |
| scanner as written, full universe / wf_weekly10                     |  0.007 |   -0.226 |      373 | 0.263 |           3.395 |

The PDF's full split (Singapore part as cash; scanner and rockets point-in-time):

| portfolio (2018+, daily rebalanced)                       |   CAGR |   max_DD |   worst_year |
|:----------------------------------------------------------|-------:|---------:|-------------:|
| PDF split: 40% SPY / 25% scanner / 15% rockets / 20% cash |  0.064 |   -0.168 |       -0.089 |
| trading parts only, 25:15                                 |  0.011 |   -0.134 |       -0.057 |
| SPY 100%                                                  |  0.143 |   -0.337 |       -0.182 |

## 13. Bracket menu and market regime for the +20/-10 model's picks (runs 17-18)

Every stock every 10 days, entry at the close, 63-day limit, 0.1% costs per side. Stocks ranked by the +20/-10 goal model (walk-forward, so pre-2018 scores are also out-of-sample for their year). Top 10% = top 10% of scores within each year. Brackets are chosen on IS (walk-forward years before 2018) and judged on 2018+. IS choice: best return per month = m20_8, best return per trade = m30_15.

Model top 10%: hit rate, net return per trade, return per month held, days held (IS vs OOS):

| bracket     |   breakeven_hit |   hit_IS |   hit_OOS |   ret_IS |   ret_OOS |   per_month_IS |   per_month_OOS |   days_IS |   days_OOS |
|:------------|----------------:|---------:|----------:|---------:|----------:|---------------:|----------------:|----------:|-----------:|
| +5% / -5%   |           0.500 |    0.525 |     0.554 |    0.001 |     0.004 |          0.004 |           0.019 |     5.237 |      4.263 |
| +5% / -8%   |           0.615 |    0.640 |     0.671 |    0.002 |     0.006 |          0.006 |           0.021 |     7.501 |      6.073 |
| +5% / -10%  |           0.667 |    0.688 |     0.728 |    0.002 |     0.008 |          0.005 |           0.025 |     8.832 |      7.239 |
| +5% / -15%  |           0.750 |    0.763 |     0.811 |    0.004 |     0.013 |          0.006 |           0.028 |    11.886 |      9.696 |
| +10% / -5%  |           0.333 |    0.376 |     0.397 |    0.005 |     0.008 |          0.010 |           0.020 |     9.430 |      7.719 |
| +10% / -8%  |           0.444 |    0.486 |     0.516 |    0.007 |     0.012 |          0.011 |           0.022 |    13.610 |     11.155 |
| +10% / -10% |           0.500 |    0.536 |     0.578 |    0.008 |     0.016 |          0.011 |           0.025 |    15.992 |     13.398 |
| +10% / -15% |           0.600 |    0.613 |     0.675 |    0.011 |     0.023 |          0.011 |           0.027 |    21.180 |     17.963 |
| +15% / -5%  |           0.250 |    0.292 |     0.309 |    0.008 |     0.010 |          0.013 |           0.020 |    13.180 |     10.918 |
| +15% / -8%  |           0.348 |    0.382 |     0.416 |    0.012 |     0.017 |          0.013 |           0.022 |    18.890 |     15.766 |
| +15% / -10% |           0.400 |    0.422 |     0.471 |    0.013 |     0.022 |          0.013 |           0.024 |    22.044 |     18.869 |
| +15% / -15% |           0.500 |    0.486 |     0.560 |    0.017 |     0.032 |          0.013 |           0.027 |    28.547 |     24.984 |
| +20% / -5%  |           0.200 |    0.229 |     0.251 |    0.011 |     0.013 |          0.014 |           0.020 |    16.190 |     13.632 |
| +20% / -8%  |           0.286 |    0.299 |     0.341 |    0.015 |     0.021 |          0.014 |           0.022 |    22.905 |     19.597 |
| +20% / -10% |           0.333 |    0.329 |     0.386 |    0.017 |     0.027 |          0.013 |           0.024 |    26.550 |     23.294 |
| +20% / -15% |           0.429 |    0.379 |     0.461 |    0.022 |     0.039 |          0.014 |           0.027 |    33.868 |     30.479 |
| +30% / -5%  |           0.143 |    0.131 |     0.164 |    0.013 |     0.017 |          0.014 |           0.020 |    20.331 |     17.624 |
| +30% / -8%  |           0.211 |    0.167 |     0.220 |    0.019 |     0.026 |          0.014 |           0.022 |    28.280 |     25.005 |
| +30% / -10% |           0.250 |    0.182 |     0.249 |    0.021 |     0.033 |          0.013 |           0.024 |    32.461 |     29.419 |
| +30% / -15% |           0.333 |    0.209 |     0.295 |    0.026 |     0.048 |          0.014 |           0.027 |    40.598 |     37.777 |

OOS hit rate by tier (all stocks = no model):

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |        0.526 |     0.554 |    0.572 |
| +5% / -8%   |        0.639 |     0.671 |    0.685 |
| +5% / -10%  |        0.686 |     0.728 |    0.742 |
| +5% / -15%  |        0.744 |     0.811 |    0.831 |
| +10% / -5%  |        0.351 |     0.397 |    0.416 |
| +10% / -8%  |        0.446 |     0.516 |    0.533 |
| +10% / -10% |        0.486 |     0.578 |    0.597 |
| +10% / -15% |        0.538 |     0.675 |    0.701 |
| +15% / -5%  |        0.240 |     0.309 |    0.330 |
| +15% / -8%  |        0.309 |     0.416 |    0.436 |
| +15% / -10% |        0.337 |     0.471 |    0.492 |
| +15% / -15% |        0.376 |     0.560 |    0.592 |
| +20% / -5%  |        0.163 |     0.251 |    0.278 |
| +20% / -8%  |        0.210 |     0.341 |    0.371 |
| +20% / -10% |        0.230 |     0.386 |    0.418 |
| +20% / -15% |        0.259 |     0.461 |    0.505 |
| +30% / -5%  |        0.076 |     0.164 |    0.196 |
| +30% / -8%  |        0.099 |     0.220 |    0.261 |
| +30% / -10% |        0.109 |     0.249 |    0.294 |
| +30% / -15% |        0.124 |     0.295 |    0.352 |

OOS net return per trade by tier:

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |       0.0008 |    0.0039 |   0.0056 |
| +5% / -8%   |       0.0029 |    0.0062 |   0.0080 |
| +5% / -10%  |       0.0043 |    0.0085 |   0.0105 |
| +5% / -15%  |       0.0067 |    0.0128 |   0.0165 |
| +10% / -5%  |       0.0029 |    0.0075 |   0.0106 |
| +10% / -8%  |       0.0062 |    0.0119 |   0.0147 |
| +10% / -10% |       0.0083 |    0.0156 |   0.0188 |
| +10% / -15% |       0.0121 |    0.0233 |   0.0281 |
| +15% / -5%  |       0.0045 |    0.0103 |   0.0146 |
| +15% / -8%  |       0.0087 |    0.0166 |   0.0208 |
| +15% / -10% |       0.0111 |    0.0216 |   0.0257 |
| +15% / -15% |       0.0158 |    0.0320 |   0.0386 |
| +20% / -5%  |       0.0056 |    0.0131 |   0.0187 |
| +20% / -8%  |       0.0102 |    0.0210 |   0.0265 |
| +20% / -10% |       0.0130 |    0.0268 |   0.0325 |
| +20% / -15% |       0.0181 |    0.0393 |   0.0486 |
| +30% / -5%  |       0.0067 |    0.0169 |   0.0258 |
| +30% / -8%  |       0.0118 |    0.0263 |   0.0362 |
| +30% / -10% |       0.0149 |    0.0332 |   0.0438 |
| +30% / -15% |       0.0205 |    0.0477 |   0.0623 |

Portfolio 2018+ (top 10% model, 1% risk per trade = position size 1%/stop, max 10 positions, 20% cap):

| bracket     |   CAGR |   max_DD |   trades |   win |
|:------------|-------:|---------:|---------:|------:|
| +5% / -5%   | -0.082 |   -0.742 | 3000.000 | 0.512 |
| +5% / -8%   |  0.011 |   -0.698 | 3329.000 | 0.628 |
| +5% / -10%  |  0.049 |   -0.717 | 3330.000 | 0.685 |
| +5% / -15%  |  0.113 |   -0.360 | 2485.000 | 0.778 |
| +10% / -5%  |  0.143 |   -0.477 | 2040.000 | 0.372 |
| +10% / -8%  |  0.145 |   -0.490 | 2237.000 | 0.488 |
| +10% / -10% |  0.151 |   -0.518 | 2081.000 | 0.543 |
| +10% / -15% |  0.130 |   -0.379 | 1507.000 | 0.648 |
| +15% / -5%  |  0.146 |   -0.443 | 1600.000 | 0.289 |
| +15% / -8%  |  0.202 |   -0.482 | 1649.000 | 0.410 |
| +15% / -10% |  0.237 |   -0.512 | 1535.000 | 0.468 |
| +15% / -15% |  0.168 |   -0.415 | 1099.000 | 0.572 |
| +20% / -5%  |  0.325 |   -0.432 | 1367.000 | 0.266 |
| +20% / -8%  |  0.280 |   -0.443 | 1401.000 | 0.362 |
| +20% / -10% |  0.276 |   -0.342 | 1209.000 | 0.423 |
| +20% / -15% |  0.187 |   -0.359 |  932.000 | 0.517 |
| +30% / -5%  |  0.260 |   -0.415 | 1057.000 | 0.212 |
| +30% / -8%  |  0.271 |   -0.400 | 1090.000 | 0.315 |
| +30% / -10% |  0.260 |   -0.412 |  962.000 | 0.359 |
| +30% / -15% |  0.182 |   -0.323 |  723.000 | 0.451 |

Model top 10%, +20/-10, by market regime at entry (breadth terciles and the 3-day market model cut use IS data):

| regime                                 | bucket               |      IS_n |   IS_hit_target |   IS_avg_net_return |     OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|----------:|----------------:|--------------------:|----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         |  6964.000 |           0.330 |               0.025 |  5324.000 |            0.395 |                0.030 |
| breadth (stocks above 50d)             | low (< 53%)          |  7076.000 |           0.358 |               0.022 | 14565.000 |            0.375 |                0.024 |
| breadth (stocks above 50d)             | mid                  |  7170.000 |           0.300 |               0.005 |  8661.000 |            0.399 |                0.029 |
| VIX level                              | 15-20                |  6592.000 |           0.285 |               0.002 |  9705.000 |            0.342 |                0.011 |
| VIX level                              | 20-30                |  4465.000 |           0.434 |               0.044 | 12500.000 |            0.429 |                0.043 |
| VIX level                              | < 15                 |  7661.000 |           0.300 |               0.015 |  5218.000 |            0.330 |                0.005 |
| VIX level                              | > 30                 |  2492.000 |           0.347 |               0.015 |  1127.000 |            0.555 |                0.083 |
| VIX / VIX3M                            | 0.9-1.0              |  6986.000 |           0.378 |               0.033 | 11941.000 |            0.395 |                0.030 |
| VIX / VIX3M                            | < 0.9 (calm)         | 11481.000 |           0.305 |               0.011 | 13478.000 |            0.384 |                0.024 |
| VIX / VIX3M                            | > 1.0 (stress)       |  2743.000 |           0.307 |               0.001 |  3131.000 |            0.362 |                0.026 |
| SPY above 200d                         | no                   |  6022.000 |           0.354 |               0.018 |  6523.000 |            0.407 |                0.035 |
| SPY above 200d                         | yes                  | 15188.000 |           0.319 |               0.017 | 22027.000 |            0.380 |                0.024 |
| QQQ above 10 & 20 SMA                  | no                   |  9538.000 |           0.348 |               0.022 | 15681.000 |            0.386 |                0.028 |
| QQQ above 10 & 20 SMA                  | yes                  | 11672.000 |           0.314 |               0.013 | 12869.000 |            0.386 |                0.025 |
| SPY 1-month return                     | -3..0%               |  3781.000 |           0.287 |               0.002 |  5842.000 |            0.386 |                0.029 |
| SPY 1-month return                     | 0..3%                |  6629.000 |           0.342 |               0.024 |  7952.000 |            0.400 |                0.029 |
| SPY 1-month return                     | < -3%                |  3990.000 |           0.398 |               0.031 |  7194.000 |            0.366 |                0.023 |
| SPY 1-month return                     | > 3%                 |  6810.000 |           0.301 |               0.010 |  7562.000 |            0.390 |                0.026 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 12636.000 |           0.321 |               0.015 | 13606.000 |            0.379 |                0.022 |
| SPY vs 21/50 SMA                       | above 21 only        |   528.000 |           0.337 |               0.017 |  1829.000 |            0.419 |                0.039 |
| SPY vs 21/50 SMA                       | above 50 only        |  2439.000 |           0.227 |              -0.006 |  2663.000 |            0.393 |                0.029 |
| SPY vs 21/50 SMA                       | below both           |  5607.000 |           0.393 |               0.032 | 10452.000 |            0.388 |                0.030 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 12504.000 |           0.291 |               0.007 | 12874.000 |            0.373 |                0.021 |
| QQQ vs 21/50 SMA                       | above 21 only        |   761.000 |           0.386 |               0.032 |  1740.000 |            0.432 |                0.038 |
| QQQ vs 21/50 SMA                       | above 50 only        |  2092.000 |           0.337 |               0.023 |  3892.000 |            0.401 |                0.032 |
| QQQ vs 21/50 SMA                       | below both           |  5853.000 |           0.400 |               0.034 | 10044.000 |            0.389 |                0.030 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 12896.000 |           0.297 |               0.008 | 13304.000 |            0.397 |                0.030 |
| A/D line vs its 21/50 MA               | above 21 only        |   907.000 |           0.434 |               0.037 |  1337.000 |            0.272 |               -0.012 |
| A/D line vs its 21/50 MA               | above 50 only        |  2663.000 |           0.303 |               0.016 |  3776.000 |            0.341 |                0.016 |
| A/D line vs its 21/50 MA               | below both           |  4744.000 |           0.412 |               0.038 | 10133.000 |            0.404 |                0.032 |
| % of stocks above 20d                  | 40-60%               |  5200.000 |           0.322 |               0.014 |  7031.000 |            0.330 |                0.007 |
| % of stocks above 20d                  | < 40%                |  5360.000 |           0.348 |               0.020 | 11054.000 |            0.394 |                0.031 |
| % of stocks above 20d                  | > 60%                | 10650.000 |           0.323 |               0.017 | 10465.000 |            0.416 |                0.036 |
| % above 50d, 10-day change             | falling (< -5 pts)   |  8596.000 |           0.351 |               0.026 | 12883.000 |            0.389 |                0.029 |
| % above 50d, 10-day change             | flat                 |  4921.000 |           0.263 |              -0.006 |  7601.000 |            0.377 |                0.023 |
| % above 50d, 10-day change             | rising (> +5 pts)    |  7693.000 |           0.347 |               0.022 |  8066.000 |            0.390 |                0.027 |
| A/D line, 10-day change                | flat                 |  5877.000 |           0.276 |              -0.003 |  8010.000 |            0.385 |                0.026 |
| A/D line, 10-day change                | falling              |  5847.000 |           0.392 |               0.037 | 10529.000 |            0.401 |                0.033 |
| A/D line, 10-day change                | rising               |  9486.000 |           0.324 |               0.017 | 10011.000 |            0.372 |                0.021 |
| sector & sub-industry today green      | both                 |  6301.000 |           0.309 |               0.012 |  8987.000 |            0.381 |                0.026 |
| sector & sub-industry today green      | neither              |  7010.000 |           0.358 |               0.026 | 10922.000 |            0.400 |                0.032 |
| sector & sub-industry today green      | one of the two       |  2472.000 |           0.320 |               0.014 |  3902.000 |            0.367 |                0.020 |
| sector & sub-industry up over 5 days   | both                 |  7085.000 |           0.303 |               0.010 |  9396.000 |            0.400 |                0.031 |
| sector & sub-industry up over 5 days   | neither              |  6088.000 |           0.364 |               0.029 | 10658.000 |            0.385 |                0.027 |
| sector & sub-industry up over 5 days   | one of the two       |  2608.000 |           0.339 |               0.019 |  3757.000 |            0.367 |                0.021 |
| sector & sub-industry above 21 EMA     | both                 |  7451.000 |           0.314 |               0.013 |  9021.000 |            0.390 |                0.028 |
| sector & sub-industry above 21 EMA     | neither              |  5618.000 |           0.358 |               0.026 | 10738.000 |            0.396 |                0.031 |
| sector & sub-industry above 21 EMA     | one of the two       |  2714.000 |           0.332 |               0.019 |  4052.000 |            0.359 |                0.018 |
| distance above the 21 EMA              | 0-5%                 |  6233.000 |           0.314 |               0.017 |  6807.000 |            0.379 |                0.026 |
| distance above the 21 EMA              | 10-15%               |   887.000 |           0.342 |               0.016 |   975.000 |            0.414 |                0.034 |
| distance above the 21 EMA              | 5-10%                |  2862.000 |           0.286 |               0.004 |  2745.000 |            0.383 |                0.025 |
| distance above the 21 EMA              | > 15%                |   433.000 |           0.337 |               0.010 |   629.000 |            0.375 |                0.021 |
| distance above the 21 EMA              | below                | 10795.000 |           0.348 |               0.021 | 17394.000 |            0.388 |                0.027 |
| ADR%                                   | > 15%                |    71.000 |           0.423 |               0.028 |    46.000 |            0.457 |                0.033 |
| ADR%                                   | 12-15%               |    95.000 |           0.421 |               0.026 |    90.000 |            0.422 |                0.041 |
| ADR%                                   | 3-5%                 | 11457.000 |           0.344 |               0.019 | 16959.000 |            0.382 |                0.026 |
| ADR%                                   | 5-8%                 |  3735.000 |           0.349 |               0.007 |  6885.000 |            0.425 |                0.030 |
| ADR%                                   | 8-12%                |   675.000 |           0.385 |               0.014 |   883.000 |            0.433 |                0.030 |
| ADR%                                   | < 3%                 |  5177.000 |           0.273 |               0.019 |  3687.000 |            0.317 |                0.022 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |    57.000 |           0.509 |               0.055 |    43.000 |            0.465 |                0.036 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |    80.000 |           0.425 |               0.028 |    85.000 |            0.412 |                0.039 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 |  9240.000 |           0.345 |               0.019 | 15213.000 |            0.381 |                0.026 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  3028.000 |           0.351 |               0.008 |  6339.000 |            0.424 |                0.029 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |   526.000 |           0.392 |               0.017 |   829.000 |            0.431 |                0.030 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 |  4184.000 |           0.278 |               0.021 |  3291.000 |            0.315 |                0.021 |
| fundamental inflection (all 4)         | no                   | 12261.000 |           0.332 |               0.021 | 24630.000 |            0.385 |                0.026 |
| fundamental inflection (all 4)         | yes                  |   566.000 |           0.329 |               0.024 |  1297.000 |            0.390 |                0.030 |
| revenue growth accelerating            | 1 quarter            |  3254.000 |           0.317 |               0.017 |  6069.000 |            0.394 |                0.030 |
| revenue growth accelerating            | 2+ quarters          |  2747.000 |           0.373 |               0.034 |  5722.000 |            0.384 |                0.026 |
| revenue growth accelerating            | no (decelerating)    |  6826.000 |           0.322 |               0.018 | 14136.000 |            0.383 |                0.025 |
| operating income outgrowing revenue    | no                   |  6117.000 |           0.339 |               0.020 | 13107.000 |            0.393 |                0.026 |
| operating income outgrowing revenue    | yes                  |  4564.000 |           0.317 |               0.019 |  9106.000 |            0.373 |                0.024 |
| operating margin vs a year ago         | expanding            |  5472.000 |           0.331 |               0.020 | 11695.000 |            0.372 |                0.021 |
| operating margin vs a year ago         | shrinking            |  5192.000 |           0.328 |               0.019 | 10469.000 |            0.399 |                0.029 |
| FCF margin vs a year ago               | improving            |  6110.000 |           0.320 |               0.018 | 13444.000 |            0.383 |                0.026 |
| FCF margin vs a year ago               | worse                |  5533.000 |           0.334 |               0.022 | 11934.000 |            0.391 |                0.028 |
| up/down volume, 50 days                | 0.8-1.0              |  4716.000 |           0.339 |               0.019 |  7210.000 |            0.384 |                0.026 |
| up/down volume, 50 days                | 1.0-1.3              |  5642.000 |           0.323 |               0.016 |  7210.000 |            0.382 |                0.026 |
| up/down volume, 50 days                | < 0.8 (distribution) |  5520.000 |           0.349 |               0.021 |  8568.000 |            0.394 |                0.029 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  5332.000 |           0.307 |               0.011 |  5562.000 |            0.381 |                0.027 |
| price vs 200-day                       | below                | 10404.000 |           0.350 |               0.020 | 16121.000 |            0.389 |                0.027 |
| price vs 200-day                       | 0-10% above          |  2638.000 |           0.308 |               0.016 |  3125.000 |            0.362 |                0.022 |
| price vs 200-day                       | 10-30% above         |  4607.000 |           0.304 |               0.017 |  4760.000 |            0.376 |                0.025 |
| price vs 200-day                       | 30-50% above         |  2375.000 |           0.318 |               0.013 |  2618.000 |            0.396 |                0.029 |
| price vs 200-day                       | > 50% above          |  1186.000 |           0.314 |               0.000 |  1926.000 |            0.417 |                0.032 |
| 6-month gain                           | 0-20%                |  3709.000 |           0.305 |               0.015 |  4389.000 |            0.378 |                0.027 |
| 6-month gain                           | 20-50%               |  4071.000 |           0.302 |               0.016 |  4471.000 |            0.378 |                0.025 |
| 6-month gain                           | 50-100%              |  2328.000 |           0.331 |               0.013 |  3211.000 |            0.417 |                0.035 |
| 6-month gain                           | < 0                  | 10313.000 |           0.350 |               0.020 | 14983.000 |            0.382 |                0.026 |
| 6-month gain                           | > 100%               |   789.000 |           0.307 |              -0.002 |  1496.000 |            0.411 |                0.027 |
| sector (11 GICS, by median RS)         | bottom 3             |  4407.000 |           0.328 |               0.014 |  6007.000 |            0.390 |                0.029 |
| sector (11 GICS, by median RS)         | middle 5             |  8150.000 |           0.335 |               0.022 | 13040.000 |            0.392 |                0.030 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  4526.000 |           0.323 |               0.014 |  5718.000 |            0.375 |                0.021 |
| sub-industry (by median RS)            | bottom 30%           |  4950.000 |           0.353 |               0.024 |  8507.000 |            0.388 |                0.027 |
| sub-industry (by median RS)            | middle               |  5301.000 |           0.334 |               0.019 |  8506.000 |            0.388 |                0.029 |
| sub-industry (by median RS)            | top 30% (leading)    |  5490.000 |           0.313 |               0.013 |  6777.000 |            0.387 |                0.027 |
| 3-day market model                     | bottom 10% (skip?)   |  1547.000 |           0.434 |               0.045 |   586.000 |            0.608 |                0.092 |
| 3-day market model                     | rest                 | 19663.000 |           0.321 |               0.015 | 27964.000 |            0.381 |                0.025 |

Same, S&P 500 stocks only after they joined the index (point-in-time survivorship check):

| regime                                 | bucket               |     IS_n |   IS_hit_target |   IS_avg_net_return |    OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|---------:|----------------:|--------------------:|---------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         | 1563.000 |           0.319 |               0.025 |  823.000 |            0.389 |                0.036 |
| breadth (stocks above 50d)             | low (< 53%)          | 1613.000 |           0.340 |               0.021 | 2538.000 |            0.366 |                0.026 |
| breadth (stocks above 50d)             | mid                  | 1596.000 |           0.288 |               0.002 | 1311.000 |            0.406 |                0.035 |
| VIX level                              | 15-20                | 1573.000 |           0.265 |              -0.001 | 1335.000 |            0.322 |                0.007 |
| VIX level                              | 20-30                | 1192.000 |           0.426 |               0.048 | 2588.000 |            0.418 |                0.046 |
| VIX level                              | < 15                 | 1153.000 |           0.234 |               0.002 |  525.000 |            0.280 |               -0.011 |
| VIX level                              | > 30                 |  854.000 |           0.363 |               0.021 |  224.000 |            0.549 |                0.085 |
| VIX / VIX3M                            | 0.9-1.0              | 1670.000 |           0.395 |               0.041 | 2185.000 |            0.396 |                0.036 |
| VIX / VIX3M                            | < 0.9 (calm)         | 2321.000 |           0.276 |               0.006 | 1883.000 |            0.379 |                0.026 |
| VIX / VIX3M                            | > 1.0 (stress)       |  781.000 |           0.262 |              -0.009 |  604.000 |            0.334 |                0.022 |
| SPY above 200d                         | no                   | 1766.000 |           0.357 |               0.021 | 1451.000 |            0.405 |                0.042 |
| SPY above 200d                         | yes                  | 3006.000 |           0.291 |               0.013 | 3221.000 |            0.371 |                0.025 |
| QQQ above 10 & 20 SMA                  | no                   | 2145.000 |           0.337 |               0.022 | 2773.000 |            0.386 |                0.033 |
| QQQ above 10 & 20 SMA                  | yes                  | 2627.000 |           0.298 |               0.011 | 1899.000 |            0.375 |                0.027 |
| SPY 1-month return                     | -3..0%               |  734.000 |           0.240 |              -0.009 |  882.000 |            0.392 |                0.033 |
| SPY 1-month return                     | 0..3%                | 1310.000 |           0.343 |               0.029 | 1190.000 |            0.405 |                0.034 |
| SPY 1-month return                     | < -3%                | 1116.000 |           0.370 |               0.026 | 1402.000 |            0.347 |                0.024 |
| SPY 1-month return                     | > 3%                 | 1612.000 |           0.290 |               0.009 | 1198.000 |            0.390 |                0.032 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 2829.000 |           0.304 |               0.013 | 1939.000 |            0.369 |                0.024 |
| SPY vs 21/50 SMA                       | above 21 only        |  125.000 |           0.344 |               0.028 |  341.000 |            0.449 |                0.058 |
| SPY vs 21/50 SMA                       | above 50 only        |  489.000 |           0.176 |              -0.021 |  366.000 |            0.355 |                0.017 |
| SPY vs 21/50 SMA                       | below both           | 1329.000 |           0.388 |               0.035 | 2026.000 |            0.386 |                0.034 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 2751.000 |           0.265 |               0.002 | 1843.000 |            0.362 |                0.023 |
| QQQ vs 21/50 SMA                       | above 21 only        |  186.000 |           0.419 |               0.046 |  304.000 |            0.441 |                0.042 |
| QQQ vs 21/50 SMA                       | above 50 only        |  409.000 |           0.337 |               0.028 |  646.000 |            0.390 |                0.031 |
| QQQ vs 21/50 SMA                       | below both           | 1426.000 |           0.392 |               0.036 | 1879.000 |            0.387 |                0.035 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 2839.000 |           0.269 |               0.003 | 2018.000 |            0.399 |                0.037 |
| A/D line vs its 21/50 MA               | above 21 only        |  264.000 |           0.428 |               0.039 |  217.000 |            0.175 |               -0.039 |
| A/D line vs its 21/50 MA               | above 50 only        |  516.000 |           0.316 |               0.022 |  566.000 |            0.318 |                0.013 |
| A/D line vs its 21/50 MA               | below both           | 1153.000 |           0.403 |               0.040 | 1871.000 |            0.406 |                0.037 |
| % of stocks above 20d                  | 40-60%               | 1035.000 |           0.288 |               0.006 | 1000.000 |            0.282 |               -0.006 |
| % of stocks above 20d                  | < 40%                | 1215.000 |           0.343 |               0.024 | 2016.000 |            0.395 |                0.035 |
| % of stocks above 20d                  | > 60%                | 2522.000 |           0.313 |               0.016 | 1656.000 |            0.425 |                0.047 |
| % above 50d, 10-day change             | falling (< -5 pts)   | 1849.000 |           0.340 |               0.027 | 2104.000 |            0.379 |                0.030 |
| % above 50d, 10-day change             | flat                 | 1065.000 |           0.202 |              -0.021 | 1272.000 |            0.372 |                0.027 |
| % above 50d, 10-day change             | rising (> +5 pts)    | 1858.000 |           0.356 |               0.025 | 1296.000 |            0.394 |                0.034 |
| A/D line, 10-day change                | flat                 | 1254.000 |           0.234 |              -0.014 | 1233.000 |            0.380 |                0.029 |
| A/D line, 10-day change                | falling              | 1339.000 |           0.394 |               0.042 | 1915.000 |            0.396 |                0.036 |
| A/D line, 10-day change                | rising               | 2179.000 |           0.314 |               0.017 | 1524.000 |            0.365 |                0.024 |
| sector & sub-industry today green      | both                 |  998.000 |           0.295 |               0.013 | 1263.000 |            0.405 |                0.040 |
| sector & sub-industry today green      | neither              | 1328.000 |           0.369 |               0.036 | 1775.000 |            0.397 |                0.036 |
| sector & sub-industry today green      | one of the two       |  423.000 |           0.345 |               0.021 |  596.000 |            0.361 |                0.023 |
| sector & sub-industry up over 5 days   | both                 | 1196.000 |           0.296 |               0.013 | 1294.000 |            0.400 |                0.038 |
| sector & sub-industry up over 5 days   | neither              | 1089.000 |           0.388 |               0.042 | 1830.000 |            0.397 |                0.036 |
| sector & sub-industry up over 5 days   | one of the two       |  463.000 |           0.328 |               0.018 |  510.000 |            0.367 |                0.026 |
| sector & sub-industry above 21 EMA     | both                 | 1243.000 |           0.333 |               0.022 | 1180.000 |            0.408 |                0.038 |
| sector & sub-industry above 21 EMA     | neither              | 1034.000 |           0.353 |               0.033 | 1876.000 |            0.399 |                0.037 |
| sector & sub-industry above 21 EMA     | one of the two       |  472.000 |           0.320 |               0.019 |  578.000 |            0.348 |                0.023 |
| distance above the 21 EMA              | 0-5%                 | 1329.000 |           0.296 |               0.015 | 1025.000 |            0.353 |                0.023 |
| distance above the 21 EMA              | 10-15%               |  192.000 |           0.396 |               0.031 |  127.000 |            0.394 |                0.040 |
| distance above the 21 EMA              | 5-10%                |  648.000 |           0.259 |              -0.002 |  351.000 |            0.379 |                0.026 |
| distance above the 21 EMA              | > 15%                |   80.000 |           0.387 |               0.022 |   96.000 |            0.406 |                0.028 |
| distance above the 21 EMA              | below                | 2523.000 |           0.331 |               0.019 | 3073.000 |            0.390 |                0.033 |
| ADR%                                   | > 15%                |   36.000 |           0.500 |               0.044 |    1.000 |            0.000 |               -0.102 |
| ADR%                                   | 12-15%               |   44.000 |           0.477 |               0.044 |    3.000 |            0.667 |                0.098 |
| ADR%                                   | 3-5%                 | 2392.000 |           0.332 |               0.016 | 2892.000 |            0.395 |                0.034 |
| ADR%                                   | 5-8%                 |  696.000 |           0.339 |               0.006 |  687.000 |            0.408 |                0.025 |
| ADR%                                   | 8-12%                |  171.000 |           0.380 |               0.014 |   74.000 |            0.473 |                0.042 |
| ADR%                                   | < 3%                 | 1433.000 |           0.258 |               0.019 | 1015.000 |            0.317 |                0.023 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |   36.000 |           0.500 |               0.044 |    1.000 |            0.000 |               -0.102 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |   44.000 |           0.477 |               0.044 |    3.000 |            0.667 |                0.098 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 | 2391.000 |           0.332 |               0.016 | 2892.000 |            0.395 |                0.034 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  695.000 |           0.338 |               0.005 |  687.000 |            0.408 |                0.025 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |  170.000 |           0.376 |               0.013 |   74.000 |            0.473 |                0.042 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 | 1431.000 |           0.259 |               0.019 | 1012.000 |            0.318 |                0.023 |
| fundamental inflection (all 4)         | no                   | 2775.000 |           0.308 |               0.018 | 4213.000 |            0.382 |                0.031 |
| fundamental inflection (all 4)         | yes                  |   86.000 |           0.244 |               0.013 |  273.000 |            0.344 |                0.017 |
| revenue growth accelerating            | 1 quarter            |  740.000 |           0.291 |               0.015 | 1000.000 |            0.370 |                0.026 |
| revenue growth accelerating            | 2+ quarters          |  537.000 |           0.345 |               0.036 |  975.000 |            0.352 |                0.020 |
| revenue growth accelerating            | no (decelerating)    | 1584.000 |           0.301 |               0.013 | 2511.000 |            0.394 |                0.035 |
| operating income outgrowing revenue    | no                   | 1181.000 |           0.315 |               0.015 | 2023.000 |            0.402 |                0.033 |
| operating income outgrowing revenue    | yes                  |  913.000 |           0.292 |               0.018 | 1703.000 |            0.343 |                0.016 |
| operating margin vs a year ago         | expanding            |  983.000 |           0.291 |               0.016 | 1832.000 |            0.343 |                0.016 |
| operating margin vs a year ago         | shrinking            | 1109.000 |           0.317 |               0.017 | 1893.000 |            0.406 |                0.035 |
| FCF margin vs a year ago               | improving            | 1136.000 |           0.302 |               0.019 | 2099.000 |            0.369 |                0.026 |
| FCF margin vs a year ago               | worse                | 1409.000 |           0.294 |               0.013 | 2338.000 |            0.391 |                0.033 |
| up/down volume, 50 days                | 0.8-1.0              | 1142.000 |           0.344 |               0.024 | 1326.000 |            0.372 |                0.026 |
| up/down volume, 50 days                | 1.0-1.3              | 1256.000 |           0.316 |               0.016 | 1131.000 |            0.376 |                0.029 |
| up/down volume, 50 days                | < 0.8 (distribution) | 1376.000 |           0.306 |               0.014 | 1513.000 |            0.402 |                0.039 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  998.000 |           0.295 |               0.008 |  702.000 |            0.365 |                0.023 |
| price vs 200-day                       | below                | 2863.000 |           0.336 |               0.019 | 3045.000 |            0.389 |                0.033 |
| price vs 200-day                       | 0-10% above          |  470.000 |           0.291 |               0.010 |  449.000 |            0.370 |                0.027 |
| price vs 200-day                       | 10-30% above         |  873.000 |           0.281 |               0.014 |  646.000 |            0.373 |                0.029 |
| price vs 200-day                       | 30-50% above         |  436.000 |           0.278 |               0.007 |  303.000 |            0.333 |                0.016 |
| price vs 200-day                       | > 50% above          |  130.000 |           0.308 |               0.012 |  229.000 |            0.397 |                0.024 |
| 6-month gain                           | 0-20%                |  709.000 |           0.283 |               0.009 |  677.000 |            0.399 |                0.035 |
| 6-month gain                           | 20-50%               |  751.000 |           0.265 |               0.011 |  667.000 |            0.379 |                0.029 |
| 6-month gain                           | 50-100%              |  411.000 |           0.326 |               0.021 |  383.000 |            0.371 |                0.026 |
| 6-month gain                           | < 0                  | 2813.000 |           0.338 |               0.019 | 2771.000 |            0.381 |                0.031 |
| 6-month gain                           | > 100%               |   88.000 |           0.239 |              -0.015 |  174.000 |            0.356 |                0.006 |
| sector (11 GICS, by median RS)         | bottom 3             | 1019.000 |           0.317 |               0.013 | 1119.000 |            0.382 |                0.036 |
| sector (11 GICS, by median RS)         | middle 5             | 1370.000 |           0.354 |               0.034 | 1920.000 |            0.402 |                0.037 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  653.000 |           0.312 |               0.016 |  752.000 |            0.383 |                0.028 |
| sub-industry (by median RS)            | bottom 30%           | 1084.000 |           0.374 |               0.035 | 1510.000 |            0.405 |                0.038 |
| sub-industry (by median RS)            | middle               |  848.000 |           0.337 |               0.023 | 1255.000 |            0.408 |                0.038 |
| sub-industry (by median RS)            | top 30% (leading)    |  801.000 |           0.292 |               0.015 |  854.000 |            0.358 |                0.027 |
| 3-day market model                     | bottom 10% (skip?)   |  428.000 |           0.442 |               0.051 |  123.000 |            0.585 |                0.089 |
| 3-day market model                     | rest                 | 4344.000 |           0.303 |               0.012 | 4549.000 |            0.376 |                0.029 |

All stocks (no model), +20/-10, by the same splits: does a leading sector help on its own?

| regime                                 | bucket               |       IS_n |   IS_hit_target |   IS_avg_net_return |      OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|-----------:|----------------:|--------------------:|-----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         |  72870.000 |           0.164 |               0.025 |  74104.000 |            0.210 |                0.009 |
| breadth (stocks above 50d)             | low (< 53%)          |  68461.000 |           0.219 |               0.020 | 108673.000 |            0.261 |                0.021 |
| breadth (stocks above 50d)             | mid                  |  70728.000 |           0.160 |               0.015 | 102680.000 |            0.212 |                0.008 |
| VIX level                              | 15-20                |  59974.000 |           0.164 |               0.018 | 109326.000 |            0.207 |                0.009 |
| VIX level                              | 20-30                |  44044.000 |           0.264 |               0.034 |  86702.000 |            0.274 |                0.021 |
| VIX level                              | < 15                 |  87607.000 |           0.135 |               0.019 |  72006.000 |            0.174 |                0.002 |
| VIX level                              | > 30                 |  20434.000 |           0.241 |               0.003 |  17423.000 |            0.395 |                0.046 |
| VIX / VIX3M                            | 0.9-1.0              |  69439.000 |           0.204 |               0.024 | 104872.000 |            0.244 |                0.017 |
| VIX / VIX3M                            | < 0.9 (calm)         | 120904.000 |           0.156 |               0.020 | 160361.000 |            0.211 |                0.009 |
| VIX / VIX3M                            | > 1.0 (stress)       |  21716.000 |           0.244 |               0.010 |  20224.000 |            0.310 |                0.024 |
| SPY above 200d                         | no                   |  46601.000 |           0.247 |               0.014 |  52689.000 |            0.279 |                0.015 |
| SPY above 200d                         | yes                  | 165458.000 |           0.162 |               0.022 | 232768.000 |            0.219 |                0.012 |
| QQQ above 10 & 20 SMA                  | no                   |  87336.000 |           0.203 |               0.020 | 123101.000 |            0.235 |                0.011 |
| QQQ above 10 & 20 SMA                  | yes                  | 124723.000 |           0.165 |               0.020 | 162356.000 |            0.227 |                0.015 |
| SPY 1-month return                     | -3..0%               |  41851.000 |           0.180 |               0.019 |  45548.000 |            0.225 |                0.015 |
| SPY 1-month return                     | 0..3%                |  76763.000 |           0.163 |               0.020 |  90999.000 |            0.217 |                0.010 |
| SPY 1-month return                     | < -3%                |  29008.000 |           0.261 |               0.021 |  45372.000 |            0.261 |                0.014 |
| SPY 1-month return                     | > 3%                 |  64437.000 |           0.166 |               0.021 | 103538.000 |            0.231 |                0.015 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 130105.000 |           0.162 |               0.021 | 180033.000 |            0.214 |                0.010 |
| SPY vs 21/50 SMA                       | above 21 only        |   9045.000 |           0.204 |               0.015 |  17244.000 |            0.269 |                0.026 |
| SPY vs 21/50 SMA                       | above 50 only        |  22174.000 |           0.131 |               0.000 |  21876.000 |            0.226 |                0.010 |
| SPY vs 21/50 SMA                       | below both           |  50735.000 |           0.246 |               0.027 |  66304.000 |            0.268 |                0.020 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 128886.000 |           0.159 |               0.017 | 168618.000 |            0.218 |                0.012 |
| QQQ vs 21/50 SMA                       | above 21 only        |  11961.000 |           0.199 |               0.022 |  17160.000 |            0.254 |                0.020 |
| QQQ vs 21/50 SMA                       | above 50 only        |  20701.000 |           0.177 |               0.024 |  30238.000 |            0.223 |                0.009 |
| QQQ vs 21/50 SMA                       | below both           |  50511.000 |           0.233 |               0.025 |  69441.000 |            0.258 |                0.016 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 133013.000 |           0.159 |               0.019 | 172692.000 |            0.209 |                0.009 |
| A/D line vs its 21/50 MA               | above 21 only        |   7870.000 |           0.188 |              -0.011 |   8241.000 |            0.302 |                0.018 |
| A/D line vs its 21/50 MA               | above 50 only        |  26446.000 |           0.164 |               0.021 |  39755.000 |            0.240 |                0.020 |
| A/D line vs its 21/50 MA               | below both           |  44730.000 |           0.255 |               0.028 |  64769.000 |            0.271 |                0.019 |
| % of stocks above 20d                  | 40-60%               |  50689.000 |           0.163 |               0.012 |  75739.000 |            0.206 |                0.003 |
| % of stocks above 20d                  | < 40%                |  50835.000 |           0.226 |               0.024 |  72988.000 |            0.274 |                0.024 |
| % of stocks above 20d                  | > 60%                | 110535.000 |           0.168 |               0.022 | 136730.000 |            0.221 |                0.013 |
| % above 50d, 10-day change             | falling (< -5 pts)   |  83214.000 |           0.194 |               0.025 | 104840.000 |            0.243 |                0.016 |
| % above 50d, 10-day change             | flat                 |  49181.000 |           0.146 |               0.008 |  77272.000 |            0.215 |                0.007 |
| % above 50d, 10-day change             | rising (> +5 pts)    |  79664.000 |           0.188 |               0.023 | 103345.000 |            0.229 |                0.014 |
| A/D line, 10-day change                | flat                 |  58826.000 |           0.166 |               0.014 |  77406.000 |            0.227 |                0.011 |
| A/D line, 10-day change                | falling              |  57114.000 |           0.214 |               0.024 |  78585.000 |            0.268 |                0.022 |
| A/D line, 10-day change                | rising               |  96119.000 |           0.170 |               0.022 | 129466.000 |            0.209 |                0.009 |
| sector & sub-industry today green      | both                 |  78846.000 |           0.163 |               0.019 | 111769.000 |            0.220 |                0.012 |
| sector & sub-industry today green      | neither              |  69645.000 |           0.188 |               0.023 |  95752.000 |            0.241 |                0.017 |
| sector & sub-industry today green      | one of the two       |  27235.000 |           0.177 |               0.023 |  41365.000 |            0.221 |                0.012 |
| sector & sub-industry up over 5 days   | both                 |  87758.000 |           0.161 |               0.020 | 122471.000 |            0.224 |                0.014 |
| sector & sub-industry up over 5 days   | neither              |  60071.000 |           0.195 |               0.022 |  84750.000 |            0.243 |                0.016 |
| sector & sub-industry up over 5 days   | one of the two       |  27881.000 |           0.177 |               0.022 |  41660.000 |            0.211 |                0.008 |
| sector & sub-industry above 21 EMA     | both                 |  96253.000 |           0.158 |               0.022 | 130237.000 |            0.208 |                0.010 |
| sector & sub-industry above 21 EMA     | neither              |  51404.000 |           0.210 |               0.022 |  76350.000 |            0.266 |                0.023 |
| sector & sub-industry above 21 EMA     | one of the two       |  28069.000 |           0.173 |               0.018 |  42299.000 |            0.220 |                0.010 |
| distance above the 21 EMA              | 0-5%                 | 103677.000 |           0.146 |               0.021 | 119764.000 |            0.189 |                0.009 |
| distance above the 21 EMA              | 10-15%               |   2884.000 |           0.289 |               0.012 |   6318.000 |            0.331 |                0.019 |
| distance above the 21 EMA              | 5-10%                |  18140.000 |           0.225 |               0.017 |  30568.000 |            0.264 |                0.013 |
| distance above the 21 EMA              | > 15%                |   1144.000 |           0.298 |              -0.001 |   3038.000 |            0.352 |                0.011 |
| distance above the 21 EMA              | below                |  86214.000 |           0.208 |               0.020 | 125769.000 |            0.253 |                0.016 |
| ADR%                                   | > 15%                |    341.000 |           0.282 |              -0.018 |    345.000 |            0.380 |                0.013 |
| ADR%                                   | 12-15%               |    614.000 |           0.280 |              -0.018 |    553.000 |            0.410 |                0.024 |
| ADR%                                   | 3-5%                 |  45439.000 |           0.299 |               0.018 |  88616.000 |            0.321 |                0.017 |
| ADR%                                   | 5-8%                 |  12466.000 |           0.319 |              -0.000 |  20659.000 |            0.404 |                0.025 |
| ADR%                                   | 8-12%                |   3362.000 |           0.282 |              -0.018 |   3587.000 |            0.450 |                0.038 |
| ADR%                                   | < 3%                 | 149837.000 |           0.130 |               0.024 | 171697.000 |            0.157 |                0.009 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |    297.000 |           0.313 |              -0.008 |    322.000 |            0.382 |                0.014 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |    537.000 |           0.279 |              -0.018 |    515.000 |            0.410 |                0.024 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 |  36214.000 |           0.298 |               0.017 |  79509.000 |            0.319 |                0.016 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  10052.000 |           0.315 |              -0.001 |  18885.000 |            0.402 |                0.024 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |   2758.000 |           0.280 |              -0.018 |   3305.000 |            0.451 |                0.038 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 | 128404.000 |           0.125 |               0.024 | 157491.000 |            0.155 |                0.009 |
| fundamental inflection (all 4)         | no                   | 125850.000 |           0.165 |               0.024 | 242629.000 |            0.234 |                0.013 |
| fundamental inflection (all 4)         | yes                  |   6560.000 |           0.169 |               0.034 |  14065.000 |            0.243 |                0.019 |
| revenue growth accelerating            | 1 quarter            |  35101.000 |           0.164 |               0.025 |  65085.000 |            0.240 |                0.018 |
| revenue growth accelerating            | 2+ quarters          |  30857.000 |           0.172 |               0.030 |  60539.000 |            0.229 |                0.013 |
| revenue growth accelerating            | no (decelerating)    |  66452.000 |           0.163 |               0.022 | 131070.000 |            0.233 |                0.012 |
| operating income outgrowing revenue    | no                   |  48072.000 |           0.187 |               0.027 | 101367.000 |            0.257 |                0.015 |
| operating income outgrowing revenue    | yes                  |  53465.000 |           0.153 |               0.024 | 102211.000 |            0.226 |                0.011 |
| operating margin vs a year ago         | expanding            |  55638.000 |           0.162 |               0.024 | 110532.000 |            0.236 |                0.011 |
| operating margin vs a year ago         | shrinking            |  45617.000 |           0.178 |               0.027 |  92880.000 |            0.249 |                0.016 |
| FCF margin vs a year ago               | improving            |  62758.000 |           0.161 |               0.027 | 133525.000 |            0.238 |                0.015 |
| FCF margin vs a year ago               | worse                |  57163.000 |           0.167 |               0.025 | 118835.000 |            0.230 |                0.012 |
| up/down volume, 50 days                | 0.8-1.0              |  49130.000 |           0.185 |               0.020 |  68683.000 |            0.238 |                0.015 |
| up/down volume, 50 days                | 1.0-1.3              |  65226.000 |           0.169 |               0.020 |  87875.000 |            0.215 |                0.011 |
| up/down volume, 50 days                | < 0.8 (distribution) |  40576.000 |           0.225 |               0.021 |  56235.000 |            0.275 |                0.018 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  57127.000 |           0.158 |               0.019 |  72664.000 |            0.208 |                0.009 |
| price vs 200-day                       | below                |  70274.000 |           0.237 |               0.019 | 112619.000 |            0.266 |                0.015 |
| price vs 200-day                       | 0-10% above          |  64593.000 |           0.132 |               0.024 |  74494.000 |            0.174 |                0.010 |
| price vs 200-day                       | 10-30% above         |  65476.000 |           0.152 |               0.020 |  76212.000 |            0.203 |                0.011 |
| price vs 200-day                       | 30-50% above         |   9194.000 |           0.261 |               0.014 |  15811.000 |            0.308 |                0.017 |
| price vs 200-day                       | > 50% above          |   2522.000 |           0.305 |               0.002 |   6321.000 |            0.385 |                0.023 |
| 6-month gain                           | 0-20%                |  85427.000 |           0.133 |               0.024 |  97874.000 |            0.175 |                0.010 |
| 6-month gain                           | 20-50%               |  44403.000 |           0.169 |               0.018 |  55517.000 |            0.228 |                0.013 |
| 6-month gain                           | 50-100%              |   8455.000 |           0.268 |               0.011 |  15234.000 |            0.337 |                0.023 |
| 6-month gain                           | < 0                  |  71941.000 |           0.230 |               0.019 | 112702.000 |            0.260 |                0.014 |
| 6-month gain                           | > 100%               |   1833.000 |           0.315 |               0.005 |   4130.000 |            0.385 |                0.020 |
| sector (11 GICS, by median RS)         | bottom 3             |  44212.000 |           0.175 |               0.021 |  56400.000 |            0.228 |                0.015 |
| sector (11 GICS, by median RS)         | middle 5             |  92662.000 |           0.179 |               0.023 | 127602.000 |            0.232 |                0.015 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  51325.000 |           0.169 |               0.017 |  75418.000 |            0.220 |                0.011 |
| sub-industry (by median RS)            | bottom 30%           |  46311.000 |           0.191 |               0.023 |  68959.000 |            0.236 |                0.012 |
| sub-industry (by median RS)            | middle               |  75630.000 |           0.166 |               0.022 | 104822.000 |            0.219 |                0.015 |
| sub-industry (by median RS)            | top 30% (leading)    |  53135.000 |           0.174 |               0.018 |  74868.000 |            0.233 |                0.013 |
| 3-day market model                     | bottom 10% (skip?)   |  21758.000 |           0.232 |               0.022 |   4975.000 |            0.401 |                0.060 |
| 3-day market model                     | rest                 | 190301.000 |           0.175 |               0.020 | 280482.000 |            0.227 |                0.012 |

Regime gates, one family at a time: skip the buckets of that family that were below break-even in-sample (hit < 33% or negative return), then trade the model's top 10% with +20/-10. RULE rows keep only the picks that pass a rule fixed in advance: leading groups (run 19: top 3 of 11 sectors / top 30% of sub-industries by median RS) and the user's run-21 rules (SPY/QQQ vs 21 & 50 SMA, breadth, A/D line, sector & sub-industry green / up 5 days / above 21 EMA; groups = equal-weight median of member stocks). Portfolio 2018+:

| gate                                                                        | skipped (chosen IS)                                  |   CAGR |   max_DD |   trades |   PIT CAGR |   PIT max_DD |
|:----------------------------------------------------------------------------|:-----------------------------------------------------|-------:|---------:|---------:|-----------:|-------------:|
| breadth (stocks above 50d)                                                  | high (> 71%), mid                                    |  0.141 |   -0.396 |      734 |      0.102 |       -0.317 |
| VIX level                                                                   | 15-20, < 15                                          |  0.274 |   -0.286 |      696 |      0.205 |       -0.276 |
| VIX / VIX3M                                                                 | < 0.9 (calm), > 1.0 (stress)                         |  0.199 |   -0.387 |      842 |      0.072 |       -0.299 |
| SPY above 200d                                                              | yes                                                  |  0.074 |   -0.256 |      343 |      0.071 |       -0.240 |
| QQQ above 10 & 20 SMA                                                       | yes                                                  |  0.221 |   -0.459 |      930 |      0.082 |       -0.268 |
| SPY 1-month return                                                          | -3..0%, > 3%                                         |  0.159 |   -0.415 |      960 |      0.035 |       -0.313 |
| SPY vs 21/50 SMA                                                            | above 21 & 50, above 50 only                         |  0.116 |   -0.399 |      594 |      0.107 |       -0.273 |
| QQQ vs 21/50 SMA                                                            | above 21 & 50                                        |  0.199 |   -0.311 |      838 |      0.038 |       -0.343 |
| A/D line vs its 21/50 MA                                                    | above 21 & 50, above 50 only                         |  0.073 |   -0.410 |      632 |      0.077 |       -0.295 |
| % of stocks above 20d                                                       | 40-60%, > 60%                                        |  0.141 |   -0.367 |      690 |      0.071 |       -0.250 |
| % above 50d, 10-day change                                                  | flat                                                 |  0.312 |   -0.311 |     1141 |      0.121 |       -0.303 |
| A/D line, 10-day change                                                     | flat, rising                                         |  0.118 |   -0.427 |      717 |      0.059 |       -0.259 |
| sector & sub-industry today green                                           | both, one of the two                                 |  0.170 |   -0.511 |     1138 |      0.068 |       -0.323 |
| sector & sub-industry up over 5 days                                        | both                                                 |  0.223 |   -0.466 |     1182 |      0.122 |       -0.301 |
| sector & sub-industry above 21 EMA                                          | both, one of the two                                 |  0.243 |   -0.462 |     1135 |      0.106 |       -0.290 |
| distance above the 21 EMA                                                   | 0-5%, 5-10%                                          |  0.162 |   -0.452 |     1195 |      0.140 |       -0.319 |
| ADR%                                                                        | < 3%                                                 |  0.270 |   -0.389 |     1214 |      0.176 |       -0.407 |
| ADR% (only stocks trading >= $10M/day)                                      | < 3%                                                 |  0.302 |   -0.353 |     1220 |      0.176 |       -0.407 |
| fundamental inflection (all 4)                                              | no, yes                                              |  0.125 |   -0.318 |      811 |      0.066 |       -0.128 |
| revenue growth accelerating                                                 | 1 quarter, no (decelerating)                         |  0.231 |   -0.444 |     1080 |      0.098 |       -0.267 |
| operating income outgrowing revenue                                         | yes                                                  |  0.262 |   -0.433 |     1189 |      0.150 |       -0.246 |
| operating margin vs a year ago                                              | expanding, shrinking                                 |  0.144 |   -0.362 |      952 |      0.163 |       -0.193 |
| FCF margin vs a year ago                                                    | improving                                            |  0.129 |   -0.549 |     1172 |      0.099 |       -0.324 |
| up/down volume, 50 days                                                     | 1.0-1.3, > 1.3 (accumulation)                        |  0.151 |   -0.388 |     1163 |      0.148 |       -0.307 |
| price vs 200-day                                                            | 0-10% above, 10-30% above, 30-50% above, > 50% above |  0.134 |   -0.371 |     1169 |      0.161 |       -0.280 |
| 6-month gain                                                                | 0-20%, 20-50%, 50-100%, > 100%                       |  0.171 |   -0.376 |     1145 |      0.172 |       -0.296 |
| sector (11 GICS, by median RS)                                              | bottom 3, top 3 (leading)                            |  0.205 |   -0.517 |     1167 |      0.110 |       -0.300 |
| sub-industry (by median RS)                                                 | top 30% (leading)                                    |  0.163 |   -0.493 |     1209 |      0.146 |       -0.330 |
| 3-day market model                                                          | rest                                                 |  0.064 |   -0.149 |      124 |      0.023 |       -0.086 |
| RULE: top 3 sectors only                                                    | nothing                                              |  0.215 |   -0.286 |      899 |      0.070 |       -0.212 |
| RULE: top 30% sub-industries only                                           | nothing                                              |  0.260 |   -0.290 |      917 |      0.078 |       -0.251 |
| RULE: top 3 sectors AND top 30% sub-industries                              | nothing                                              |  0.218 |   -0.291 |      793 |      0.035 |       -0.188 |
| RULE: SPY above its 21 & 50 SMA                                             | nothing                                              |  0.322 |   -0.315 |      901 |      0.096 |       -0.193 |
| RULE: QQQ above its 21 & 50 SMA                                             | nothing                                              |  0.271 |   -0.336 |      900 |      0.131 |       -0.206 |
| RULE: SPY above its 50 SMA (21 either way)                                  | nothing                                              |  0.261 |   -0.330 |      983 |      0.139 |       -0.231 |
| RULE: A/D line above its 21 & 50 MA                                         | nothing                                              |  0.186 |   -0.372 |      897 |      0.131 |       -0.249 |
| RULE: > 50% of stocks above their 50d                                       | nothing                                              |  0.211 |   -0.406 |      917 |      0.104 |       -0.272 |
| RULE: % above 50d rising over 10 days                                       | nothing                                              |  0.260 |   -0.299 |      971 |      0.053 |       -0.317 |
| RULE: sector AND sub-industry green today                                   | nothing                                              |  0.209 |   -0.334 |     1017 |      0.106 |       -0.303 |
| RULE: sector AND sub-industry up over 5 days                                | nothing                                              |  0.222 |   -0.354 |     1015 |      0.127 |       -0.261 |
| RULE: sector AND sub-industry above 21 EMA                                  | nothing                                              |  0.197 |   -0.407 |      988 |      0.103 |       -0.251 |
| RULE: SPY > 21 & 50 + sector & sub-industry up 5 days                       | nothing                                              |  0.244 |   -0.316 |      798 |      0.095 |       -0.155 |
| RULE: <= 10% above the 21 EMA (course rule)                                 | nothing                                              |  0.256 |   -0.362 |     1217 |      0.161 |       -0.332 |
| RULE: ADR% >= 5% (the infographic's minimum)                                | nothing                                              |  0.332 |   -0.477 |     1467 |      0.083 |       -0.334 |
| RULE: ADR% 5-12% (the infographic's sweet spot)                             | nothing                                              |  0.347 |   -0.488 |     1439 |      0.081 |       -0.334 |
| RULE: ADR% <= 15% (skip the wildest)                                        | nothing                                              |  0.285 |   -0.342 |     1204 |      0.138 |       -0.331 |
| RULE: ADR% 5-12% and >= $10M/day                                            | nothing                                              |  0.357 |   -0.515 |     1443 |      0.081 |       -0.334 |
| RULE: fundamental inflection (rev accel 2q + op leverage + margin + FCF up) | nothing                                              |  0.157 |   -0.250 |      571 |      0.040 |       -0.168 |
| RULE: revenue growth accelerating 2+ quarters                               | nothing                                              |  0.294 |   -0.332 |     1033 |      0.085 |       -0.244 |
| RULE: accumulation (up/down volume 50d > 1)                                 | nothing                                              |  0.248 |   -0.450 |     1079 |      0.078 |       -0.286 |
| RULE: not extended (< 30% above the 200-day)                                | nothing                                              |  0.186 |   -0.376 |     1158 |      0.167 |       -0.324 |
| RULE: not already up 50%+ in 6 months                                       | nothing                                              |  0.197 |   -0.366 |     1149 |      0.160 |       -0.308 |
| RULE: price rules only (accumulation + not extended + not up 50%)           | nothing                                              |  0.193 |   -0.479 |      980 |      0.082 |       -0.273 |
| RULE: user's full method (inflection + price rules)                         | nothing                                              |  0.012 |   -0.249 |      224 |     -0.002 |       -0.140 |
| METHOD: user's method alone, no model (inflection + price rules)            | nothing                                              |  0.091 |   -0.263 |      583 |      0.033 |       -0.202 |
| METHOD: fundamental inflection alone, no model                              | nothing                                              |  0.152 |   -0.367 |      720 |      0.098 |       -0.242 |
| MODEL + fundamentals as features, top 10%                                   | nothing                                              |  0.241 |   -0.345 |     1198 |      0.218 |       -0.283 |
| SIZE: position scaled by 6% / ADR (x0.4-1.5)                                | nothing                                              |  0.242 |   -0.387 |     1175 |      0.168 |       -0.310 |
| (no gate)                                                                   | nothing                                              |  0.276 |   -0.342 |     1209 |      0.137 |       -0.331 |

## 11. Qullamaggie replication (per trade, out-of-sample 2018+; IS in brackets)

Scan = top 3% performer over 1, 3 or 6 months with ADR >= 4%. Regime = QQQ above its 10- and 20-day SMAs. qull_breakout = buy-stop above the flag high the next day (fill at the trigger or the gap open), stop at the tighter of the 3-day low and 1 ADR; a same-day touch of the stop counts as stopped out. Portfolio rows start with QULL in section 9.

| entry            | filter           | exit          |   IS_n |   IS_win |   IS_avgR |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:-----------------|:--------------|-------:|---------:|----------:|--------:|-------------:|----------:|-----------:|---------:|--------:|
| ep_gap10         | all              | bracket_20_10 |    549 |     0.46 |      0.18 |     962 |       109.50 |      0.41 |       0.11 |     1.18 |    2.40 |
| ep_gap10         | all              | qull_sma10    |    564 |     0.44 |     -0.01 |     962 |       109.50 |      0.44 |      -0.01 |     0.99 |   -0.14 |
| ep_gap10         | all              | qull_sma20    |    562 |     0.46 |     -0.04 |     962 |       109.50 |      0.44 |       0.06 |     1.11 |    1.00 |
| ep_gap10         | all              | sma50_close   |    553 |     0.29 |      0.13 |     962 |       109.50 |      0.31 |       0.45 |     1.69 |    3.46 |
| ep_gap10         | qull_scan        | bracket_20_10 |    128 |     0.36 |      0.04 |     272 |        30.96 |      0.43 |       0.22 |     1.37 |    2.46 |
| ep_gap10         | qull_scan        | qull_sma10    |    130 |     0.40 |     -0.05 |     272 |        30.96 |      0.42 |      -0.05 |     0.89 |   -0.73 |
| ep_gap10         | qull_scan        | qull_sma20    |    128 |     0.42 |     -0.09 |     272 |        30.96 |      0.44 |       0.11 |     1.21 |    0.99 |
| ep_gap10         | qull_scan        | sma50_close   |    126 |     0.21 |      0.00 |     272 |        30.96 |      0.31 |       0.69 |     2.03 |    2.40 |
| ep_gap10         | qull_scan_regime | bracket_20_10 |     84 |     0.33 |     -0.04 |     171 |        19.46 |      0.41 |       0.18 |     1.31 |    1.64 |
| ep_gap10         | qull_scan_regime | qull_sma10    |     85 |     0.42 |     -0.06 |     171 |        19.46 |      0.43 |      -0.05 |     0.91 |   -0.49 |
| ep_gap10         | qull_scan_regime | qull_sma20    |     85 |     0.45 |     -0.03 |     171 |        19.46 |      0.44 |       0.20 |     1.39 |    1.24 |
| ep_gap10         | qull_scan_regime | sma50_close   |     83 |     0.17 |      0.08 |     171 |        19.46 |      0.32 |       0.90 |     2.36 |    2.26 |
| ep_gap8_hold     | all              | bracket_20_10 |    764 |     0.48 |      0.20 |    1214 |       138.18 |      0.42 |       0.11 |     1.18 |    2.67 |
| ep_gap8_hold     | all              | qull_sma10    |    782 |     0.46 |      0.02 |    1214 |       138.18 |      0.45 |      -0.02 |     0.95 |   -0.65 |
| ep_gap8_hold     | all              | qull_sma20    |    779 |     0.48 |      0.02 |    1214 |       138.18 |      0.46 |       0.02 |     1.04 |    0.47 |
| ep_gap8_hold     | all              | sma50_close   |    771 |     0.33 |      0.24 |    1214 |       138.18 |      0.31 |       0.35 |     1.54 |    3.31 |
| ep_gap8_hold     | qull_scan        | bracket_20_10 |    153 |     0.36 |      0.03 |     292 |        33.24 |      0.44 |       0.24 |     1.42 |    2.80 |
| ep_gap8_hold     | qull_scan        | qull_sma10    |    156 |     0.42 |     -0.01 |     292 |        33.24 |      0.49 |       0.04 |     1.09 |    0.59 |
| ep_gap8_hold     | qull_scan        | qull_sma20    |    154 |     0.42 |     -0.04 |     292 |        33.24 |      0.50 |       0.18 |     1.38 |    1.73 |
| ep_gap8_hold     | qull_scan        | sma50_close   |    153 |     0.22 |      0.04 |     292 |        33.24 |      0.33 |       0.74 |     2.11 |    2.71 |
| ep_gap8_hold     | qull_scan_regime | bracket_20_10 |    106 |     0.35 |      0.01 |     184 |        20.94 |      0.42 |       0.21 |     1.34 |    1.88 |
| ep_gap8_hold     | qull_scan_regime | qull_sma10    |    108 |     0.44 |      0.00 |     184 |        20.94 |      0.49 |       0.02 |     1.05 |    0.26 |
| ep_gap8_hold     | qull_scan_regime | qull_sma20    |    107 |     0.43 |     -0.00 |     184 |        20.94 |      0.51 |       0.23 |     1.47 |    1.53 |
| ep_gap8_hold     | qull_scan_regime | sma50_close   |    106 |     0.20 |      0.14 |     184 |        20.94 |      0.33 |       0.91 |     2.37 |    2.41 |
| qull_breakout    | all              | bracket_20_10 |   2614 |     0.37 |      0.01 |    4553 |       518.22 |      0.41 |       0.15 |     1.24 |    6.73 |
| qull_breakout    | all              | qull_sma10    |   2625 |     0.33 |     -0.32 |    4553 |       518.22 |      0.33 |      -0.25 |     0.64 |  -11.08 |
| qull_breakout    | all              | qull_sma20    |   2623 |     0.33 |     -0.34 |    4553 |       518.22 |      0.34 |      -0.23 |     0.69 |   -8.50 |
| qull_breakout    | all              | sma50_close   |   2618 |     0.14 |     -0.38 |    4553 |       518.22 |      0.17 |       0.01 |     1.01 |    0.12 |
| qull_breakout    | qull_scan        | bracket_20_10 |    654 |     0.39 |      0.11 |    1231 |       140.11 |      0.38 |       0.08 |     1.12 |    1.82 |
| qull_breakout    | qull_scan        | qull_sma10    |    656 |     0.35 |     -0.27 |    1231 |       140.11 |      0.36 |      -0.17 |     0.73 |   -4.03 |
| qull_breakout    | qull_scan        | qull_sma20    |    656 |     0.35 |     -0.26 |    1231 |       140.11 |      0.36 |      -0.16 |     0.75 |   -3.33 |
| qull_breakout    | qull_scan        | sma50_close   |    654 |     0.17 |     -0.26 |    1231 |       140.11 |      0.17 |       0.04 |     1.05 |    0.32 |
| qull_breakout    | qull_scan_regime | bracket_20_10 |    447 |     0.38 |      0.08 |     791 |        90.03 |      0.41 |       0.18 |     1.29 |    3.32 |
| qull_breakout    | qull_scan_regime | qull_sma10    |    449 |     0.34 |     -0.30 |     791 |        90.03 |      0.38 |      -0.12 |     0.81 |   -2.12 |
| qull_breakout    | qull_scan_regime | qull_sma20    |    449 |     0.34 |     -0.28 |     791 |        90.03 |      0.38 |      -0.07 |     0.89 |   -1.09 |
| qull_breakout    | qull_scan_regime | sma50_close   |    447 |     0.17 |     -0.22 |     791 |        90.03 |      0.19 |       0.24 |     1.28 |    1.17 |
| qull_breakout_60 | all              | bracket_20_10 |    934 |     0.35 |      0.01 |    1947 |       221.61 |      0.42 |       0.19 |     1.31 |    5.52 |
| qull_breakout_60 | all              | qull_sma10    |    934 |     0.36 |     -0.31 |    1947 |       221.61 |      0.33 |      -0.25 |     0.65 |   -7.14 |
| qull_breakout_60 | all              | qull_sma20    |    934 |     0.36 |     -0.32 |    1947 |       221.61 |      0.33 |      -0.22 |     0.69 |   -5.65 |
| qull_breakout_60 | all              | sma50_close   |    934 |     0.14 |     -0.31 |    1947 |       221.61 |      0.17 |       0.11 |     1.12 |    0.79 |
| qull_breakout_60 | qull_scan        | bracket_20_10 |    392 |     0.36 |      0.05 |     872 |        99.25 |      0.39 |       0.10 |     1.16 |    2.06 |
| qull_breakout_60 | qull_scan        | qull_sma10    |    392 |     0.35 |     -0.29 |     872 |        99.25 |      0.35 |      -0.19 |     0.72 |   -3.61 |
| qull_breakout_60 | qull_scan        | qull_sma20    |    392 |     0.35 |     -0.27 |     872 |        99.25 |      0.35 |      -0.19 |     0.72 |   -3.24 |
| qull_breakout_60 | qull_scan        | sma50_close   |    392 |     0.16 |     -0.26 |     872 |        99.25 |      0.17 |       0.10 |     1.11 |    0.51 |
| qull_breakout_60 | qull_scan_regime | bracket_20_10 |    274 |     0.35 |      0.01 |     584 |        66.47 |      0.42 |       0.20 |     1.33 |    3.20 |
| qull_breakout_60 | qull_scan_regime | qull_sma10    |    274 |     0.33 |     -0.34 |     584 |        66.47 |      0.37 |      -0.16 |     0.76 |   -2.41 |
| qull_breakout_60 | qull_scan_regime | qull_sma20    |    274 |     0.33 |     -0.29 |     584 |        66.47 |      0.37 |      -0.12 |     0.82 |   -1.51 |
| qull_breakout_60 | qull_scan_regime | sma50_close   |    274 |     0.15 |     -0.27 |     584 |        66.47 |      0.18 |       0.25 |     1.28 |    0.92 |
| random_uptrend   | all              | bracket_20_10 |  30882 |     0.53 |      0.19 |   34624 |      3940.92 |      0.46 |       0.09 |     1.19 |   14.09 |
| random_uptrend   | all              | qull_sma10    |  31721 |     0.30 |     -0.15 |   34624 |      3940.92 |      0.30 |      -0.08 |     0.90 |   -6.39 |
| random_uptrend   | all              | qull_sma20    |  31673 |     0.29 |     -0.14 |   34624 |      3940.92 |      0.30 |      -0.08 |     0.90 |   -5.93 |
| random_uptrend   | all              | sma50_close   |  31488 |     0.15 |     -0.03 |   34624 |      3940.92 |      0.14 |      -0.02 |     0.98 |   -0.95 |
| random_uptrend   | qull_scan        | bracket_20_10 |   1028 |     0.37 |      0.06 |    2028 |       230.83 |      0.39 |       0.14 |     1.23 |    4.24 |
| random_uptrend   | qull_scan        | qull_sma10    |   1032 |     0.33 |     -0.04 |    2028 |       230.83 |      0.33 |       0.06 |     1.09 |    1.15 |
| random_uptrend   | qull_scan        | qull_sma20    |   1028 |     0.33 |     -0.03 |    2028 |       230.83 |      0.33 |       0.06 |     1.09 |    1.08 |
| random_uptrend   | qull_scan        | sma50_close   |   1026 |     0.15 |      0.09 |    2028 |       230.83 |      0.16 |       0.21 |     1.22 |    1.80 |
| random_uptrend   | qull_scan_regime | bracket_20_10 |    602 |     0.37 |      0.05 |    1224 |       139.32 |      0.40 |       0.16 |     1.26 |    3.71 |
| random_uptrend   | qull_scan_regime | qull_sma10    |    605 |     0.33 |     -0.08 |    1224 |       139.32 |      0.33 |       0.05 |     1.06 |    0.68 |
| random_uptrend   | qull_scan_regime | qull_sma20    |    604 |     0.32 |     -0.05 |    1224 |       139.32 |      0.33 |       0.02 |     1.03 |    0.27 |
| random_uptrend   | qull_scan_regime | sma50_close   |    603 |     0.14 |     -0.13 |    1224 |       139.32 |      0.16 |       0.11 |     1.12 |    0.88 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                                                                           |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:-------------------------------------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| wf_scan_pullback / wf_scan / bracket_20_10                                                                         |  -0.01 |    -0.46 |             -0.44 |   710.00 |   0.40 |            9.05 |             nan    |
| donchian_20 / all / bracket_20_10                                                                                  |   0.08 |    -0.45 |             -0.42 |   818.00 |   0.41 |            9.17 |               0.96 |
| pocket_pivot / all / bracket_20_10                                                                                 |   0.06 |    -0.35 |             -0.34 |   580.00 |   0.42 |            7.43 |               0.75 |
| wf_scan_base / all / bracket_20_10                                                                                 |   0.07 |    -0.27 |             -0.24 |   505.00 |   0.49 |            9.60 |               0.83 |
| donchian_55 / all / bracket_20_10                                                                                  |   0.02 |    -0.34 |             -0.31 |   774.00 |   0.40 |            9.13 |               2.68 |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                                                  |   0.13 |    -0.35 |             -0.31 |   679.00 |   0.45 |            8.40 |               0.62 |
| All setups, ranked by RS / bracket_20_10                                                                           |   0.19 |    -0.46 |             -0.43 |  1155.00 |   0.41 |            9.28 |               0.53 |
| All setups, random order / bracket_20_10                                                                           |   0.08 |    -0.39 |             -0.37 |   534.00 |   0.49 |            8.92 |               0.78 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                                                       |   0.12 |    -0.32 |             -0.32 |   862.00 |   0.41 |            8.97 |               0.80 |
| BASELINE random entries, ranked by RS / bracket_20_10                                                              |   0.02 |    -0.46 |             -0.42 |   638.00 |   0.39 |            7.43 |               3.16 |
| BASELINE random entries, random order / bracket_20_10                                                              |  -0.03 |    -0.48 |             -0.46 |   449.00 |   0.41 |            7.44 |             nan    |
| IS-selected setups (3), ranked by RS / bracket_20_10                                                               |   0.12 |    -0.31 |             -0.27 |   495.00 |   0.45 |            7.59 |               0.54 |
| IS-selected setups, only when SPY > 200d / bracket_20_10                                                           |   0.03 |    -0.35 |             -0.32 |   414.00 |   0.41 |            6.59 |               1.82 |
| IS-selected setups (28), ranked by RS / sma50_close                                                                |   0.02 |    -0.55 |             -0.48 |  1002.00 |   0.25 |            9.07 |               2.03 |
| IS-selected setups, only when SPY > 200d / sma50_close                                                             |   0.04 |    -0.57 |             -0.53 |   847.00 |   0.24 |            7.82 |               1.79 |
| All setups, ranked by RS / sma50_close                                                                             |   0.09 |    -0.53 |             -0.46 |  1192.00 |   0.27 |            8.85 |               0.63 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                                                        |   0.15 |    -0.27 |             -0.20 |   408.00 |   0.29 |            5.35 |               0.44 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                                                       |   0.10 |    -0.28 |             -0.25 |   435.00 |   0.29 |            5.57 |               0.60 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                                                       |   0.09 |    -0.37 |             -0.27 |   484.00 |   0.28 |            5.90 |               0.71 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)                                           |   0.09 |    -0.33 |             -0.18 |   487.00 |   0.29 |            6.14 |               0.62 |
| Top 20 by IS expectancy, ranked by superperformer model                                                            |   0.09 |    -0.37 |             -0.29 |   482.00 |   0.27 |            5.81 |               0.77 |
| All setups, ranked by superperformer model / bracket_20_10                                                         |   0.02 |    -0.57 |             -0.57 |  1476.00 |   0.36 |            9.24 |               3.86 |
| Only setups in the model's top 10% likely superperformers / sma50_close                                            |   0.14 |    -0.54 |             -0.46 |  1474.00 |   0.30 |            9.05 |               0.67 |
| CHECK random entries in the model's top 10% / sma50_close                                                          |   0.19 |    -0.50 |             -0.42 |   924.00 |   0.17 |            5.30 |               0.70 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close                                           |   0.17 |    -0.41 |             -0.34 |  1350.00 |   0.29 |            8.64 |               0.59 |
| Top 10% model + adaptive sizing / sma50_close                                                                      |   0.16 |    -0.45 |             -0.32 |  1508.00 |   0.30 |            9.31 |               0.69 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                                               |   0.17 |    -0.50 |             -0.43 |  1405.00 |   0.32 |            8.99 |               0.69 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                                                  |   0.26 |    -0.52 |             -0.50 |  1253.00 |   0.41 |            9.34 |               0.59 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                                                          |   0.23 |    -0.38 |             -0.38 |  1209.00 |   0.41 |            9.07 |               0.58 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                                                            |   0.24 |    -0.36 |             -0.36 |   985.00 |   0.41 |            8.83 |               0.63 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                                                |   0.16 |    -0.31 |             -0.29 |   822.00 |   0.42 |            8.34 |               0.63 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                                                  |   0.19 |    -0.34 |             -0.32 |  1347.00 |   0.57 |            8.45 |               0.48 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                                                          |   0.17 |    -0.29 |             -0.27 |  1306.00 |   0.57 |            8.14 |               0.51 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                                                            |   0.05 |    -0.46 |             -0.42 |  1057.00 |   0.54 |            7.43 |               1.32 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                                                |   0.08 |    -0.25 |             -0.24 |   908.00 |   0.55 |            7.16 |               0.92 |
| MENU top 10% model / +10% -10%                                                                                     |   0.15 |    -0.52 |             -0.50 |  2081.00 |   0.54 |            8.76 |               0.71 |
| MENU top 10% model / +20% -8% (IS best return per month)                                                           |   0.28 |    -0.44 |             -0.41 |  1401.00 |   0.36 |            8.48 |               0.42 |
| MENU top 10% model / +20% -10%                                                                                     |   0.28 |    -0.34 |             -0.33 |  1209.00 |   0.42 |            9.16 |               0.42 |
| MENU top 10% model / +30% -15% (IS best return per trade)                                                          |   0.18 |    -0.32 |             -0.28 |   723.00 |   0.45 |            9.43 |               0.54 |
| REGIME breadth (stocks above 50d): skip ['high (> 71%)', 'mid'] / +20% -10%                                        |   0.14 |    -0.40 |             -0.39 |   734.00 |   0.43 |            5.49 |               0.57 |
| REGIME breadth (stocks above 50d), S&P 500 point-in-time only / +20% -10%                                          |   0.10 |    -0.32 |             -0.26 |   443.00 |   0.43 |            4.54 |               0.60 |
| REGIME VIX level: skip ['15-20', '< 15'] / +20% -10%                                                               |   0.27 |    -0.29 |             -0.26 |   696.00 |   0.47 |            5.43 |               0.41 |
| REGIME VIX level, S&P 500 point-in-time only / +20% -10%                                                           |   0.21 |    -0.28 |             -0.23 |   464.00 |   0.50 |            4.74 |               0.48 |
| REGIME VIX / VIX3M: skip ['< 0.9 (calm)', '> 1.0 (stress)'] / +20% -10%                                            |   0.20 |    -0.39 |             -0.37 |   842.00 |   0.42 |            6.70 |               0.69 |
| REGIME VIX / VIX3M, S&P 500 point-in-time only / +20% -10%                                                         |   0.07 |    -0.30 |             -0.29 |   502.00 |   0.41 |            5.11 |               0.92 |
| REGIME SPY above 200d: skip ['yes'] / +20% -10%                                                                    |   0.07 |    -0.26 |             -0.23 |   343.00 |   0.43 |            2.41 |               0.72 |
| REGIME SPY above 200d, S&P 500 point-in-time only / +20% -10%                                                      |   0.07 |    -0.24 |             -0.19 |   222.00 |   0.45 |            1.88 |               0.80 |
| REGIME QQQ above 10 & 20 SMA: skip ['yes'] / +20% -10%                                                             |   0.22 |    -0.46 |             -0.42 |   930.00 |   0.43 |            7.19 |               0.60 |
| REGIME QQQ above 10 & 20 SMA, S&P 500 point-in-time only / +20% -10%                                               |   0.08 |    -0.27 |             -0.25 |   531.00 |   0.42 |            5.65 |               0.59 |
| REGIME SPY 1-month return: skip ['-3..0%', '> 3%'] / +20% -10%                                                     |   0.16 |    -0.41 |             -0.38 |   960.00 |   0.40 |            7.54 |               0.46 |
| REGIME SPY 1-month return, S&P 500 point-in-time only / +20% -10%                                                  |   0.04 |    -0.31 |             -0.27 |   521.00 |   0.40 |            5.81 |               1.31 |
| REGIME SPY vs 21/50 SMA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%                                       |   0.12 |    -0.40 |             -0.39 |   594.00 |   0.42 |            4.64 |               0.76 |
| REGIME SPY vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                                                    |   0.11 |    -0.27 |             -0.25 |   376.00 |   0.45 |            3.99 |               0.66 |
| REGIME QQQ vs 21/50 SMA: skip ['above 21 & 50'] / +20% -10%                                                        |   0.20 |    -0.31 |             -0.30 |   838.00 |   0.42 |            6.49 |               0.51 |
| REGIME QQQ vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                                                    |   0.04 |    -0.34 |             -0.32 |   509.00 |   0.39 |            5.40 |               1.17 |
| REGIME A/D line vs its 21/50 MA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%                               |   0.07 |    -0.41 |             -0.39 |   632.00 |   0.40 |            4.48 |               0.90 |
| REGIME A/D line vs its 21/50 MA, S&P 500 point-in-time only / +20% -10%                                            |   0.08 |    -0.30 |             -0.26 |   368.00 |   0.43 |            3.83 |               0.70 |
| REGIME % of stocks above 20d: skip ['40-60%', '> 60%'] / +20% -10%                                                 |   0.14 |    -0.37 |             -0.33 |   690.00 |   0.43 |            5.50 |               0.58 |
| REGIME % of stocks above 20d, S&P 500 point-in-time only / +20% -10%                                               |   0.07 |    -0.25 |             -0.22 |   399.00 |   0.42 |            4.37 |               0.66 |
| REGIME % above 50d, 10-day change: skip ['flat'] / +20% -10%                                                       |   0.31 |    -0.31 |             -0.28 |  1141.00 |   0.43 |            8.64 |               0.48 |
| REGIME % above 50d, 10-day change, S&P 500 point-in-time only / +20% -10%                                          |   0.12 |    -0.30 |             -0.27 |   714.00 |   0.42 |            7.01 |               0.63 |
| REGIME A/D line, 10-day change: skip ['flat', 'rising'] / +20% -10%                                                |   0.12 |    -0.43 |             -0.43 |   717.00 |   0.41 |            5.89 |               0.86 |
| REGIME A/D line, 10-day change, S&P 500 point-in-time only / +20% -10%                                             |   0.06 |    -0.26 |             -0.21 |   405.00 |   0.41 |            4.40 |               0.62 |
| REGIME sector & sub-industry today green: skip ['both', 'one of the two'] / +20% -10%                              |   0.17 |    -0.51 |             -0.49 |  1138.00 |   0.40 |            8.85 |               0.74 |
| REGIME sector & sub-industry today green, S&P 500 point-in-time only / +20% -10%                                   |   0.07 |    -0.32 |             -0.30 |   713.00 |   0.40 |            6.96 |               1.28 |
| REGIME sector & sub-industry up over 5 days: skip ['both'] / +20% -10%                                             |   0.22 |    -0.47 |             -0.45 |  1182.00 |   0.41 |            8.96 |               0.70 |
| REGIME sector & sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%                                |   0.12 |    -0.30 |             -0.27 |   716.00 |   0.42 |            7.08 |               0.87 |
| REGIME sector & sub-industry above 21 EMA: skip ['both', 'one of the two'] / +20% -10%                             |   0.24 |    -0.46 |             -0.44 |  1135.00 |   0.42 |            8.64 |               0.51 |
| REGIME sector & sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%                                  |   0.11 |    -0.29 |             -0.26 |   675.00 |   0.41 |            6.72 |               0.73 |
| REGIME distance above the 21 EMA: skip ['0-5%', '5-10%'] / +20% -10%                                               |   0.16 |    -0.45 |             -0.44 |  1195.00 |   0.40 |            8.98 |               0.64 |
| REGIME distance above the 21 EMA, S&P 500 point-in-time only / +20% -10%                                           |   0.14 |    -0.32 |             -0.27 |   716.00 |   0.42 |            7.24 |               0.63 |
| REGIME ADR%: skip ['< 3%'] / +20% -10%                                                                             |   0.27 |    -0.39 |             -0.36 |  1214.00 |   0.42 |            9.14 |               0.44 |
| REGIME ADR%, S&P 500 point-in-time only / +20% -10%                                                                |   0.18 |    -0.41 |             -0.38 |   807.00 |   0.43 |            7.51 |               0.59 |
| REGIME ADR% (only stocks trading >= $10M/day): skip ['< 3%'] / +20% -10%                                           |   0.30 |    -0.35 |             -0.32 |  1220.00 |   0.42 |            9.15 |               0.44 |
| REGIME ADR% (only stocks trading >= $10M/day), S&P 500 point-in-time only / +20% -10%                              |   0.18 |    -0.41 |             -0.38 |   807.00 |   0.43 |            7.51 |               0.59 |
| REGIME fundamental inflection (all 4): skip ['no', 'yes'] / +20% -10%                                              |   0.13 |    -0.32 |             -0.31 |   811.00 |   0.41 |            7.27 |               0.75 |
| REGIME fundamental inflection (all 4), S&P 500 point-in-time only / +20% -10%                                      |   0.07 |    -0.13 |             -0.08 |   134.00 |   0.53 |            1.76 |               0.53 |
| REGIME revenue growth accelerating: skip ['1 quarter', 'no (decelerating)'] / +20% -10%                            |   0.23 |    -0.44 |             -0.41 |  1080.00 |   0.42 |            8.46 |               0.58 |
| REGIME revenue growth accelerating, S&P 500 point-in-time only / +20% -10%                                         |   0.10 |    -0.27 |             -0.25 |   530.00 |   0.43 |            5.58 |               0.62 |
| REGIME operating income outgrowing revenue: skip ['yes'] / +20% -10%                                               |   0.26 |    -0.43 |             -0.41 |  1189.00 |   0.42 |            9.06 |               0.54 |
| REGIME operating income outgrowing revenue, S&P 500 point-in-time only / +20% -10%                                 |   0.15 |    -0.25 |             -0.24 |   706.00 |   0.43 |            7.16 |               0.60 |
| REGIME operating margin vs a year ago: skip ['expanding', 'shrinking'] / +20% -10%                                 |   0.14 |    -0.36 |             -0.33 |   952.00 |   0.41 |            8.41 |               0.60 |
| REGIME operating margin vs a year ago, S&P 500 point-in-time only / +20% -10%                                      |   0.16 |    -0.19 |             -0.18 |   361.00 |   0.52 |            4.41 |               0.53 |
| REGIME FCF margin vs a year ago: skip ['improving'] / +20% -10%                                                    |   0.13 |    -0.55 |             -0.52 |  1172.00 |   0.39 |            8.91 |               0.80 |
| REGIME FCF margin vs a year ago, S&P 500 point-in-time only / +20% -10%                                            |   0.10 |    -0.32 |             -0.29 |   695.00 |   0.41 |            6.90 |               0.81 |
| REGIME up/down volume, 50 days: skip ['1.0-1.3', '> 1.3 (accumulation)'] / +20% -10%                               |   0.15 |    -0.39 |             -0.37 |  1163.00 |   0.40 |            8.88 |               0.82 |
| REGIME up/down volume, 50 days, S&P 500 point-in-time only / +20% -10%                                             |   0.15 |    -0.31 |             -0.26 |   686.00 |   0.44 |            7.06 |               0.60 |
| REGIME price vs 200-day: skip ['0-10% above', '10-30% above', '30-50% above', '> 50% above'] / +20% -10%           |   0.13 |    -0.37 |             -0.35 |  1169.00 |   0.40 |            8.96 |               0.78 |
| REGIME price vs 200-day, S&P 500 point-in-time only / +20% -10%                                                    |   0.16 |    -0.28 |             -0.24 |   668.00 |   0.44 |            6.71 |               0.55 |
| REGIME 6-month gain: skip ['0-20%', '20-50%', '50-100%', '> 100%'] / +20% -10%                                     |   0.17 |    -0.38 |             -0.35 |  1145.00 |   0.41 |            8.92 |               0.59 |
| REGIME 6-month gain, S&P 500 point-in-time only / +20% -10%                                                        |   0.17 |    -0.30 |             -0.23 |   653.00 |   0.45 |            6.84 |               0.54 |
| REGIME sector (11 GICS, by median RS): skip ['bottom 3', 'top 3 (leading)'] / +20% -10%                            |   0.21 |    -0.52 |             -0.49 |  1167.00 |   0.41 |            8.99 |               0.54 |
| REGIME sector (11 GICS, by median RS), S&P 500 point-in-time only / +20% -10%                                      |   0.11 |    -0.30 |             -0.27 |   699.00 |   0.42 |            7.23 |               0.78 |
| REGIME sub-industry (by median RS): skip ['top 30% (leading)'] / +20% -10%                                         |   0.16 |    -0.49 |             -0.47 |  1209.00 |   0.40 |            9.07 |               0.66 |
| REGIME sub-industry (by median RS), S&P 500 point-in-time only / +20% -10%                                         |   0.15 |    -0.33 |             -0.31 |   757.00 |   0.42 |            7.46 |               0.70 |
| REGIME 3-day market model: skip ['rest'] / +20% -10%                                                               |   0.06 |    -0.15 |             -0.13 |   124.00 |   0.49 |            1.10 |               0.54 |
| REGIME 3-day market model, S&P 500 point-in-time only / +20% -10%                                                  |   0.02 |    -0.09 |             -0.04 |    39.00 |   0.54 |            0.41 |               0.63 |
| RULE top 3 sectors only, model top 10% / +20% -10%                                                                 |   0.22 |    -0.29 |             -0.27 |   899.00 |   0.43 |            7.93 |               0.48 |
| RULE top 3 sectors only, S&P 500 point-in-time only / +20% -10%                                                    |   0.07 |    -0.21 |             -0.19 |   375.00 |   0.43 |            4.15 |               0.40 |
| RULE top 30% sub-industries only, model top 10% / +20% -10%                                                        |   0.26 |    -0.29 |             -0.25 |   917.00 |   0.44 |            8.35 |               0.48 |
| RULE top 30% sub-industries only, S&P 500 point-in-time only / +20% -10%                                           |   0.08 |    -0.25 |             -0.22 |   421.00 |   0.44 |            5.12 |               0.60 |
| RULE top 3 sectors AND top 30% sub-industries, model top 10% / +20% -10%                                           |   0.22 |    -0.29 |             -0.28 |   793.00 |   0.44 |            7.04 |               0.46 |
| RULE top 3 sectors AND top 30% sub-industries, S&P 500 point-in-time only / +20% -10%                              |   0.04 |    -0.19 |             -0.17 |   256.00 |   0.41 |            3.02 |               0.59 |
| RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10%                                                          |   0.32 |    -0.32 |             -0.29 |   901.00 |   0.45 |            7.06 |               0.55 |
| RULE SPY above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                                             |   0.10 |    -0.19 |             -0.16 |   542.00 |   0.41 |            5.33 |               0.68 |
| RULE QQQ above its 21 & 50 SMA, model top 10% / +20% -10%                                                          |   0.27 |    -0.34 |             -0.30 |   900.00 |   0.44 |            6.95 |               0.62 |
| RULE QQQ above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                                             |   0.13 |    -0.21 |             -0.20 |   545.00 |   0.44 |            5.22 |               0.58 |
| RULE SPY above its 50 SMA (21 either way), model top 10% / +20% -10%                                               |   0.26 |    -0.33 |             -0.29 |   983.00 |   0.43 |            7.51 |               0.64 |
| RULE SPY above its 50 SMA (21 either way), S&P 500 point-in-time only / +20% -10%                                  |   0.14 |    -0.23 |             -0.22 |   595.00 |   0.43 |            5.89 |               0.48 |
| RULE A/D line above its 21 & 50 MA, model top 10% / +20% -10%                                                      |   0.19 |    -0.37 |             -0.35 |   897.00 |   0.42 |            7.07 |               0.70 |
| RULE A/D line above its 21 & 50 MA, S&P 500 point-in-time only / +20% -10%                                         |   0.13 |    -0.25 |             -0.21 |   534.00 |   0.44 |            5.38 |               0.62 |
| RULE > 50% of stocks above their 50d, model top 10% / +20% -10%                                                    |   0.21 |    -0.41 |             -0.39 |   917.00 |   0.42 |            7.07 |               0.54 |
| RULE > 50% of stocks above their 50d, S&P 500 point-in-time only / +20% -10%                                       |   0.10 |    -0.27 |             -0.21 |   555.00 |   0.42 |            5.57 |               0.57 |
| RULE % above 50d rising over 10 days, model top 10% / +20% -10%                                                    |   0.26 |    -0.30 |             -0.27 |   971.00 |   0.43 |            6.96 |               0.51 |
| RULE % above 50d rising over 10 days, S&P 500 point-in-time only / +20% -10%                                       |   0.05 |    -0.32 |             -0.30 |   538.00 |   0.41 |            5.18 |               1.26 |
| RULE sector AND sub-industry green today, model top 10% / +20% -10%                                                |   0.21 |    -0.33 |             -0.31 |  1017.00 |   0.42 |            8.36 |               0.69 |
| RULE sector AND sub-industry green today, S&P 500 point-in-time only / +20% -10%                                   |   0.11 |    -0.30 |             -0.25 |   516.00 |   0.43 |            5.75 |               0.59 |
| RULE sector AND sub-industry up over 5 days, model top 10% / +20% -10%                                             |   0.22 |    -0.35 |             -0.32 |  1015.00 |   0.42 |            8.34 |               0.46 |
| RULE sector AND sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%                                |   0.13 |    -0.26 |             -0.22 |   542.00 |   0.44 |            5.93 |               0.71 |
| RULE sector AND sub-industry above 21 EMA, model top 10% / +20% -10%                                               |   0.20 |    -0.41 |             -0.39 |   988.00 |   0.41 |            8.16 |               0.71 |
| RULE sector AND sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%                                  |   0.10 |    -0.25 |             -0.23 |   474.00 |   0.45 |            5.04 |               0.64 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, model top 10% / +20% -10%                                    |   0.24 |    -0.32 |             -0.29 |   798.00 |   0.44 |            6.62 |               0.45 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, S&P 500 point-in-time only / +20% -10%                       |   0.10 |    -0.16 |             -0.13 |   373.00 |   0.44 |            3.84 |               0.65 |
| RULE <= 10% above the 21 EMA (course rule), model top 10% / +20% -10%                                              |   0.26 |    -0.36 |             -0.34 |  1217.00 |   0.42 |            9.12 |               0.51 |
| RULE <= 10% above the 21 EMA (course rule), S&P 500 point-in-time only / +20% -10%                                 |   0.16 |    -0.33 |             -0.31 |   760.00 |   0.43 |            7.68 |               0.64 |
| RULE ADR% >= 5% (the infographic's minimum), model top 10% / +20% -10%                                             |   0.33 |    -0.48 |             -0.46 |  1467.00 |   0.41 |            8.46 |               0.50 |
| RULE ADR% >= 5% (the infographic's minimum), S&P 500 point-in-time only / +20% -10%                                |   0.08 |    -0.33 |             -0.32 |   494.00 |   0.40 |            2.96 |               0.92 |
| RULE ADR% 5-12% (the infographic's sweet spot), model top 10% / +20% -10%                                          |   0.35 |    -0.49 |             -0.47 |  1439.00 |   0.41 |            8.47 |               0.47 |
| RULE ADR% 5-12% (the infographic's sweet spot), S&P 500 point-in-time only / +20% -10%                             |   0.08 |    -0.33 |             -0.32 |   490.00 |   0.40 |            2.96 |               0.92 |
| RULE ADR% <= 15% (skip the wildest), model top 10% / +20% -10%                                                     |   0.28 |    -0.34 |             -0.33 |  1204.00 |   0.43 |            9.15 |               0.44 |
| RULE ADR% <= 15% (skip the wildest), S&P 500 point-in-time only / +20% -10%                                        |   0.14 |    -0.33 |             -0.31 |   779.00 |   0.42 |            7.75 |               0.66 |
| RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10%                                                         |   0.36 |    -0.51 |             -0.48 |  1443.00 |   0.41 |            8.26 |               0.48 |
| RULE ADR% 5-12% and >= $10M/day, S&P 500 point-in-time only / +20% -10%                                            |   0.08 |    -0.33 |             -0.32 |   490.00 |   0.40 |            2.96 |               0.92 |
| RULE fundamental inflection (rev accel 2q + op leverage + margin + FCF up), model top 10% / +20% -10%              |   0.16 |    -0.25 |             -0.21 |   571.00 |   0.44 |            5.91 |               0.54 |
| RULE fundamental inflection (rev accel 2q + op leverage + margin + FCF up), S&P 500 point-in-time only / +20% -10% |   0.04 |    -0.17 |             -0.15 |   183.00 |   0.43 |            2.08 |               0.73 |
| RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%                                            |   0.29 |    -0.33 |             -0.29 |  1033.00 |   0.44 |            8.19 |               0.43 |
| RULE revenue growth accelerating 2+ quarters, S&P 500 point-in-time only / +20% -10%                               |   0.08 |    -0.24 |             -0.23 |   486.00 |   0.43 |            5.36 |               0.71 |
| RULE accumulation (up/down volume 50d > 1), model top 10% / +20% -10%                                              |   0.25 |    -0.45 |             -0.42 |  1079.00 |   0.42 |            8.65 |               0.50 |
| RULE accumulation (up/down volume 50d > 1), S&P 500 point-in-time only / +20% -10%                                 |   0.08 |    -0.29 |             -0.26 |   637.00 |   0.40 |            6.41 |               0.72 |
| RULE not extended (< 30% above the 200-day), model top 10% / +20% -10%                                             |   0.19 |    -0.38 |             -0.37 |  1158.00 |   0.41 |            9.12 |               0.61 |
| RULE not extended (< 30% above the 200-day), S&P 500 point-in-time only / +20% -10%                                |   0.17 |    -0.32 |             -0.32 |   749.00 |   0.43 |            7.62 |               0.54 |
| RULE not already up 50%+ in 6 months, model top 10% / +20% -10%                                                    |   0.20 |    -0.37 |             -0.34 |  1149.00 |   0.41 |            9.18 |               0.57 |
| RULE not already up 50%+ in 6 months, S&P 500 point-in-time only / +20% -10%                                       |   0.16 |    -0.31 |             -0.29 |   746.00 |   0.43 |            7.67 |               0.58 |
| RULE price rules only (accumulation + not extended + not up 50%), model top 10% / +20% -10%                        |   0.19 |    -0.48 |             -0.44 |   980.00 |   0.42 |            8.45 |               0.58 |
| RULE price rules only (accumulation + not extended + not up 50%), S&P 500 point-in-time only / +20% -10%           |   0.08 |    -0.27 |             -0.26 |   551.00 |   0.41 |            5.85 |               0.72 |
| RULE user's full method (inflection + price rules), model top 10% / +20% -10%                                      |   0.01 |    -0.25 |             -0.24 |   224.00 |   0.39 |            2.83 |               1.74 |
| RULE user's full method (inflection + price rules), S&P 500 point-in-time only / +20% -10%                         |  -0.00 |    -0.14 |             -0.11 |    62.00 |   0.37 |            0.88 |             nan    |
| METHOD user's method alone, no model (inflection + price rules) / +20% -10%                                        |   0.09 |    -0.26 |             -0.25 |   583.00 |   0.46 |            9.09 |               0.72 |
| METHOD fundamental inflection alone, no model / +20% -10%                                                          |   0.15 |    -0.37 |             -0.31 |   720.00 |   0.46 |            9.47 |               0.51 |
| MODEL with fundamentals, top 10% / +20% -10%                                                                       |   0.24 |    -0.34 |             -0.32 |  1198.00 |   0.42 |            9.22 |               0.46 |
| SIZE model top 10%, position scaled by 6% / ADR / +20% -10%                                                        |   0.24 |    -0.39 |             -0.36 |  1175.00 |   0.42 |            8.76 |               0.50 |
| QULL scan+setups / qull_sma10                                                                                      |  -0.16 |    -0.81 |             -0.80 |  1152.00 |   0.38 |            3.38 |             nan    |
| QULL scan+setups / qull_sma20                                                                                      |  -0.13 |    -0.76 |             -0.74 |  1008.00 |   0.39 |            4.05 |             nan    |
| QULL scan+setups / sma50_close                                                                                     |   0.04 |    -0.51 |             -0.40 |   675.00 |   0.19 |            5.55 |               2.25 |
| QULL scan+setups / bracket_20_10                                                                                   |   0.06 |    -0.39 |             -0.39 |   723.00 |   0.39 |            5.74 |               1.39 |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma10                                                         |  -0.08 |    -0.56 |             -0.54 |   758.00 |   0.39 |            2.29 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma10                                                                   |  -0.06 |    -0.48 |             -0.46 |   852.00 |   0.39 |            2.57 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma20                                                         |  -0.04 |    -0.47 |             -0.46 |   691.00 |   0.40 |            2.90 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma20                                                                   |  -0.03 |    -0.44 |             -0.40 |   769.00 |   0.39 |            3.15 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / sma50_close                                                        |   0.15 |    -0.51 |             -0.37 |   484.00 |   0.21 |            4.25 |               0.71 |
| QULL ... + regime + adaptive sizing / sma50_close                                                                  |   0.12 |    -0.40 |             -0.30 |   509.00 |   0.22 |            4.56 |               0.84 |
| QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20                                                 |  -0.01 |    -0.26 |             -0.25 |    92.00 |   0.34 |            0.32 |             nan    |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (15125 signals) / sma50_close                                 |   0.34 |    -0.41 |             -0.28 |  1277.00 |   0.33 |            8.35 |               0.49 |
| SURVIVORSHIP S&P 500 names, only after joining the index (3928 signals) / sma50_close                              |   0.15 |    -0.45 |             -0.37 |   918.00 |   0.32 |            5.97 |               0.67 |
| WORKFLOW rockets as written (regime sizing) / wf_rocket                                                            |   0.02 |    -0.12 |             -0.08 |   192.00 |   0.30 |            2.35 |               0.66 |
| WORKFLOW rockets, no regime rule / wf_rocket                                                                       |   0.01 |    -0.12 |             -0.07 |   236.00 |   0.31 |            2.72 |               1.01 |
| WORKFLOW rockets, QQQ 21/50 regime / wf_rocket                                                                     |   0.01 |    -0.09 |             -0.08 |   193.00 |   0.31 |            2.43 |               1.45 |
| WORKFLOW rockets / sma50_close                                                                                     |   0.02 |    -0.11 |             -0.08 |   191.00 |   0.29 |            2.35 |               0.69 |
| WORKFLOW rockets / bracket_20_10                                                                                   |   0.03 |    -0.09 |             -0.08 |   175.00 |   0.45 |            2.42 |               0.74 |
| WORKFLOW BASELINE random entries, rocket filter + regime / wf_rocket                                               |   0.01 |    -0.21 |             -0.16 |   473.00 |   0.15 |            2.46 |               2.66 |
| WORKFLOW rockets as written, S&P 500 point-in-time only / wf_rocket                                                |   0.01 |    -0.07 |             -0.04 |   142.00 |   0.34 |            2.03 |               0.69 |
| WORKFLOW scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10                                       |   0.01 |    -0.17 |             -0.13 |   357.00 |   0.28 |            3.41 |               2.11 |
| WORKFLOW scanner PIT, no regime rule / wf_weekly10                                                                 |   0.00 |    -0.17 |             -0.14 |   419.00 |   0.31 |            3.93 |               6.65 |
| WORKFLOW scanner PIT, QQQ 21/50 regime / wf_weekly10                                                               |  -0.02 |    -0.25 |             -0.23 |   381.00 |   0.26 |            3.47 |             nan    |
| WORKFLOW scanner PIT / sma50_close                                                                                 |   0.01 |    -0.19 |             -0.19 |   394.00 |   0.27 |            3.35 |               1.72 |
| WORKFLOW BASELINE random entries, scanner filter + regime, PIT / wf_weekly10                                       |   0.03 |    -0.17 |             -0.11 |   518.00 |   0.16 |            3.30 |               0.69 |
| WORKFLOW scanner as written, full universe / wf_weekly10                                                           |   0.01 |    -0.23 |             -0.20 |   373.00 |   0.26 |            3.40 |               6.11 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY                                                       |   0.15 |    -0.40 |             -0.34 |   441.00 |   0.29 |            5.62 |               0.48 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY                                                       |   0.15 |    -0.46 |             -0.39 |   350.00 |   0.27 |            4.18 |               0.59 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY                                                       |   0.15 |    -0.46 |             -0.39 |   350.00 |   0.27 |            4.18 |               0.59 |
| SPY buy & hold                                                                                                     |   0.14 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.

Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):

| entry             | filter     | exit            |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_t |
|:------------------|:-----------|:----------------|-------:|----------:|--------:|-----------:|--------:|
| ep_gap8_neglected | wf_scan    | sma50_close     |    200 |      0.72 |     245 |       0.35 |    2.07 |
| ep_gap8_neglected | wf_scan    | wf_rocket       |    200 |      0.69 |     245 |       0.36 |    2.34 |
| ep_gap10_vol2     | rs80_mkt   | sma50_close     |    215 |      0.61 |     411 |       0.59 |    2.42 |
| ep_gap5           | rs80_early | wf_weekly10     |    333 |      0.59 |     474 |       0.42 |    2.41 |
| ep_gap8_neglected | wf_scan    | oneil_20_8      |    201 |      0.57 |     245 |       0.34 |    2.57 |
| ep_gap5           | rs80_early | sma50_close     |    333 |      0.57 |     474 |       0.39 |    2.36 |
| ep_gap10          | rs80_mkt   | chandelier_3atr |    200 |      0.56 |     354 |       0.13 |    1.05 |
| ep_gap8_neglected | rs80       | wf_weekly10     |    241 |      0.55 |     334 |       0.51 |    2.28 |
| ep_gap8_hold      | rs80_mkt   | wf_weekly10     |    298 |      0.54 |     433 |       0.43 |    1.88 |
| ep_gap10_vol2     | rs80_mkt   | chandelier_3atr |    217 |      0.52 |     411 |       0.20 |    1.66 |

Year-by-year returns (best 3 portfolios by CAGR vs SPY):

|      |   RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10% |   RULE ADR% 5-12% (the infographic's sweet spot), model top 10% / +20% -10% |   SURVIVORSHIP S&P 500 names, all dates, top 10% model (15125 signals) / sma50_close |   SPY |
|-----:|-------------------------------------------------------------:|----------------------------------------------------------------------------:|-------------------------------------------------------------------------------------:|------:|
| 2018 |                                                        -25.5 |                                                                       -24.1 |                                                                                  1.3 |  -5.2 |
| 2019 |                                                         61.0 |                                                                        60.7 |                                                                                 25.2 |  31.2 |
| 2020 |                                                         75.3 |                                                                        64.4 |                                                                                 87.5 |  18.3 |
| 2021 |                                                         33.9 |                                                                        40.7 |                                                                                  4.1 |  28.7 |
| 2022 |                                                        -36.7 |                                                                       -32.3 |                                                                                -16.7 | -18.2 |
| 2023 |                                                         46.2 |                                                                        53.7 |                                                                                 86.9 |  26.2 |
| 2024 |                                                         56.5 |                                                                        40.8 |                                                                                 81.8 |  24.9 |
| 2025 |                                                        108.4 |                                                                       106.3 |                                                                                 21.5 |  17.7 |
| 2026 |                                                         72.0 |                                                                        60.4 |                                                                                 55.1 |  12.8 |

## Appendix: entries and exits

| entry              | source / rule                                                             |   signals |
|:-------------------|:--------------------------------------------------------------------------|----------:|
| donchian_20        | Turtle 20-day breakout / trading-range break (Brock et al. 1992)          |    151358 |
| donchian_55        | Turtle 55-day breakout                                                    |    100732 |
| high52             | 52-week-high breakout (George & Hwang 2004)                               |     60694 |
| high52_fresh       | 52-week high after >= 20 days of consolidation                            |     16965 |
| base_25            | O'Neil/Darvas 5-week base breakout                                        |      4461 |
| base_50            | O'Neil 10-week base breakout                                              |      5065 |
| vcp                | Minervini volatility contraction pattern                                  |      2246 |
| flag_30            | Qullamaggie flag after a 30%+ move                                        |      3042 |
| flag_60            | Qullamaggie flag after a 60%+ move                                        |       986 |
| flag_30_early      | Qullamaggie flag, early entry inside the flag                             |      3265 |
| htf                | High tight flag (O'Neil / Bulkowski)                                      |       156 |
| ep_gap5            | Gap up >= 5% on 3x volume                                                 |      4331 |
| ep_gap10           | Episodic pivot: gap >= 10% on 3x volume                                   |      1526 |
| ep_gap8_neglected  | Episodic pivot from neglect (Qullamaggie)                                 |      1597 |
| ep_gap15           | Episodic pivot: gap >= 15% on 3x volume                                   |       565 |
| ep_gap10_vol2      | EP variant: gap >= 10% on only 2x volume                                  |      1868 |
| ep_gap10_vol5      | EP variant: gap >= 10% on 5x volume                                       |       804 |
| ep_gap8_hold       | EP variant: gap >= 8%, closes above the open                              |      1996 |
| pocket_pivot       | Morales & Kacher pocket pivot                                             |     99241 |
| asc_triangle       | Ascending triangle breakout (flat top, rising lows)                       |      2021 |
| desc_triangle      | Descending triangle, upside breakout                                      |      1510 |
| sym_triangle       | Symmetrical triangle breakout (pennant)                                   |      1834 |
| falling_wedge      | Falling wedge breakout                                                    |      2878 |
| rising_wedge       | Rising wedge, upside breakout                                             |      3913 |
| tight_coil_7       | 7-day coil: closes within 1 ADR, breakout on volume                       |     12036 |
| tight_coil_15      | 15-day coil: closes within 1.5 ADR, breakout on volume                    |      2368 |
| stage2             | Weinstein stage 2 breakout                                                |     11113 |
| ema_retest         | 8/21 EMA cross -> break -> retest (your playbook)                         |     30871 |
| multi_touch        | Multi-touch level breakout on volume (your playbook)                      |     23759 |
| undercut           | Undercut & rally (your playbook)                                          |     50380 |
| qull_breakout      | Qullamaggie breakout: buy-stop above the flag high next day               |      7181 |
| qull_breakout_60   | Qullamaggie breakout after a 60%+ move                                    |      2883 |
| wf_rocket_breakout | Workflow PDF rockets: 6-week base -> 52w high on 1.5x vol, stop -8%       |      5013 |
| wf_rocket_gap      | Workflow PDF rockets: gap >= 5% (2x vol) holding its low 2 days           |      7009 |
| wf_scan_pullback   | Workflow PDF scanner: uptrend pullback to 21EMA/50SMA, close > prior high |    143798 |
| wf_scan_base       | Workflow PDF scanner: uptrend, breakout from a 4-week base                |     58043 |
| tc_ema_cross_base  | Course: 21/50 EMA crossover, then the first base breakout                 |     14604 |
| tc_supertrend_ema  | Course: Supertrend flip + close above 21 EMA, same candle                 |     42689 |
| tc_reversal_base   | Course: reversal, 35%+ off the high, EMAs turned up, base breakout        |       333 |
| tc_ema200_2nd      | Course: second pullback to the 200 EMA after reclaiming it                |      2812 |
| random_uptrend     | BASELINE: random entries in an uptrend                                    |     66444 |

| exit            | rule                                                                                         |
|:----------------|:---------------------------------------------------------------------------------------------|
| trim_ema        | 1/4 at +2R then BE stop; 1/4 on close<8EMA, 1/4 <21EMA, rest <50EMA                          |
| qull_sma10      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<10SMA               |
| qull_sma20      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<20SMA               |
| oneil_20_8      | O'Neil: stop max 8% below entry, take all at +20%, time stop 60 days                         |
| fixed_3r_20d    | stop, target 3R, time stop 20 days                                                           |
| chandelier_3atr | trailing stop = highest close - 3 x ATR(20)                                                  |
| donchian_10low  | Turtle-style: exit on close below the prior 10-day low                                       |
| ema21_close     | exit on first close below the 21 EMA                                                         |
| sma50_close     | position trade: exit on first close below the 50 SMA                                         |
| bracket_10_10   | stop -10%, target +10%, close after 63 days if neither                                       |
| bracket_20_10   | stop -10%, target +20%, close after 63 days if neither                                       |
| wf_rocket       | workflow rockets: sell 1/3 at +25% and move the stop to entry, trail the rest on close<50SMA |
| wf_weekly10     | workflow scanner: exit on a weekly close below the 10-week MA (setup stop stays)             |

Caveats: index membership lists are current (plus former S&P 500 members Yahoo still serves), so survivorship bias remains; daily bars cannot reproduce intraday entries; one decision per signal, no slippage model beyond costs.