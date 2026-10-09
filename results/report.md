# Strategy research report

Generated 2026-10-09 16:26 UTC in 51 min.
Universe: 1488 stocks with data (sp600: 590, sp500: 499, sp400: 399; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-07: 880,290.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.49). Top 20 by IS t-stat: +0.063R OOS; top 20 by IS avgR (n>=200): +0.401R; all strategies +0.055R; random entries -0.020R.
- Too few signals to judge (need 100+ per period): htf (IS 53, OOS 99).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.31R, OOS +0.34R), ep_gap8_hold (IS +0.20R, OOS +0.20R), ep_gap10_vol5 (IS +0.19R, OOS +0.24R), ep_gap8_neglected (IS +0.23R, OOS +0.17R), desc_triangle (IS +0.22R, OOS +0.17R), ep_gap5 (IS +0.15R, OOS +0.12R), ep_gap10 (IS +0.11R, OOS +0.25R), wf_rocket_gap (IS +0.11R, OOS +0.21R), falling_wedge (IS +0.24R, OOS +0.09R), sym_triangle (IS +0.09R, OOS +0.10R), ep_gap10_vol2 (IS +0.09R, OOS +0.26R), wf_rocket_breakout (IS +0.15R, OOS +0.07R), donchian_20 (IS +0.11R, OOS +0.07R), undercut (IS +0.12R, OOS +0.07R), wf_scan_pullback (IS +0.12R, OOS +0.06R), ema_retest (IS +0.11R, OOS +0.06R), flag_60 (IS +0.05R, OOS +0.19R), wf_scan_base (IS +0.13R, OOS +0.05R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
- Best exit out-of-sample (avg over entries): wf_weekly10 (+0.117R); worst: qull_sma10 (-0.043R).
- Filters that help OOS: qull_scan_regime (+0.127R), rs80_early (+0.113R), qull_scan (+0.098R), rs80_early_theme (+0.065R), early_stage (+0.053R), wf_scan_green (+0.042R), wf_rocket_green (+0.030R); that hurt: none.
- ML filter adds little: OOS rank corr 0.015, AUC 0.512, decile monotonicity -0.16, taken +0.094R vs skipped +0.064R.
- Features the model relies on most: sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.07R, OOS +0.04R), rs80_early_theme (IS +0.07R, OOS +0.06R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558` (IS +0.34R, OOS +0.13R, n=41976).
- Superperformer model: 29.8% of its top-10% picks gained >= 40% within 3 months vs 7.1% for all stocks (4.2x), AUC 0.835. Driven by: adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 53% (break-even ~50%), avg net return per trade +0.9%. Point-in-time S&P 500 top 10%: 54%, +1.4% per trade (n=7041).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 37% (break-even ~33%), avg net return per trade +2.4%. Point-in-time S&P 500 top 10%: 39%, +3.6% per trade (n=4335).
- Best portfolio 2018->today: SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close at 43.4% CAGR (max drawdown -38.2%) vs SPY 14.5%.
- Best return per unit of drawdown: SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close (43.4% CAGR, -38.2% max DD).
- Workflow PDF rockets as written (regime sizing) / wf_rocket: 1.7% CAGR, -10% DD, 189 trades.
- Workflow PDF rockets, QQQ 21/50 regime / wf_rocket: 0.2% CAGR, -12% DD, 203 trades.
- Workflow PDF rockets as written, S&P 500 point-in-time only / wf_rocket: -0.2% CAGR, -8% DD, 147 trades.
- Workflow PDF scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10: 1.0% CAGR, -17% DD, 349 trades.
- Workflow PDF scanner PIT, QQQ 21/50 regime / wf_weekly10: -1.6% CAGR, -22% DD, 372 trades.
- Workflow PDF scanner as written, full universe / wf_weekly10: 0.3% CAGR, -23% DD, 379 trades.
- Workflow PDF split (40/25/15/20 cash): 6.3% CAGR, -17% DD vs SPY 14.6%, -34%.
- Bracket menu: in-sample best (return per month) is +20% / -15%. OOS top 10%: hit 45.9% (break-even 43%), +3.98% per trade, +2.70% per month held, vs +20/-10: hit 38.3%, +2.63%, +2.34%/month.
- Regime gate breadth (stocks above 50d) (skip high (> 71%), mid): 12.5% CAGR, -41% DD; point-in-time S&P 500 9.2%, -27%.
- Regime gate VIX level (skip 15-20, < 15): 25.6% CAGR, -46% DD; point-in-time S&P 500 21.3%, -30%.
- Regime gate VIX / VIX3M (skip < 0.9 (calm), > 1.0 (stress)): 13.4% CAGR, -46% DD; point-in-time S&P 500 14.9%, -27%.
- Regime gate SPY above 200d (skip yes): 9.2% CAGR, -31% DD; point-in-time S&P 500 5.9%, -22%.
- Regime gate QQQ above 10 & 20 SMA (skip yes): 16.3% CAGR, -46% DD; point-in-time S&P 500 12.0%, -29%.
- Regime gate SPY 1-month return (skip -3..0%, > 3%): 17.6% CAGR, -40% DD; point-in-time S&P 500 16.8%, -28%.
- Regime gate SPY vs 21/50 SMA (skip above 21 & 50, above 50 only): 11.6% CAGR, -41% DD; point-in-time S&P 500 8.5%, -36%.
- Regime gate QQQ vs 21/50 SMA (skip above 21 & 50): 15.9% CAGR, -47% DD; point-in-time S&P 500 5.6%, -32%.
- Regime gate A/D line vs its 21/50 MA (skip above 21 & 50, above 50 only): 7.9% CAGR, -40% DD; point-in-time S&P 500 3.7%, -33%.
- Regime gate % of stocks above 20d (skip 40-60%, > 60%): 15.2% CAGR, -44% DD; point-in-time S&P 500 9.4%, -25%.
- Regime gate % above 50d, 10-day change (skip flat, rising (> +5 pts)): 9.4% CAGR, -49% DD; point-in-time S&P 500 12.2%, -25%.
- Regime gate A/D line, 10-day change (skip flat, rising): 14.0% CAGR, -33% DD; point-in-time S&P 500 7.4%, -29%.
- Regime gate sector & sub-industry today green (skip both, one of the two): 29.0% CAGR, -44% DD; point-in-time S&P 500 14.6%, -23%.
- Regime gate sector & sub-industry up over 5 days (skip both): 16.2% CAGR, -43% DD; point-in-time S&P 500 13.7%, -27%.
- Regime gate sector & sub-industry above 21 EMA (skip both, one of the two): 27.9% CAGR, -36% DD; point-in-time S&P 500 10.8%, -27%.
- Regime gate sub-industry (by median RS) (skip middle, top 30% (leading)): 21.1% CAGR, -34% DD; point-in-time S&P 500 16.4%, -27%.
- Regime gate 3-day market model (skip rest): 7.5% CAGR, -16% DD; point-in-time S&P 500 1.0%, -5%.
- Filter RULE: top 3 sectors only: 12.4% CAGR, -34% DD; point-in-time S&P 500 11.4%, -21%.
- Filter RULE: top 30% sub-industries only: 23.2% CAGR, -31% DD; point-in-time S&P 500 11.2%, -27%.
- Filter RULE: top 3 sectors AND top 30% sub-industries: 18.1% CAGR, -37% DD; point-in-time S&P 500 4.7%, -25%.
- Filter RULE: SPY above its 21 & 50 SMA: 21.3% CAGR, -35% DD; point-in-time S&P 500 14.5%, -26%.
- Filter RULE: QQQ above its 21 & 50 SMA: 24.0% CAGR, -30% DD; point-in-time S&P 500 17.3%, -22%.
- Filter RULE: SPY above its 50 SMA (21 either way): 17.2% CAGR, -41% DD; point-in-time S&P 500 15.1%, -33%.
- Filter RULE: A/D line above its 21 & 50 MA: 13.8% CAGR, -55% DD; point-in-time S&P 500 20.9%, -20%.
- Filter RULE: > 50% of stocks above their 50d: 13.2% CAGR, -38% DD; point-in-time S&P 500 13.8%, -27%.
- Filter RULE: % above 50d rising over 10 days: 19.5% CAGR, -33% DD; point-in-time S&P 500 17.7%, -26%.
- Filter RULE: sector AND sub-industry green today: 22.3% CAGR, -46% DD; point-in-time S&P 500 20.1%, -24%.
- Filter RULE: sector AND sub-industry up over 5 days: 11.9% CAGR, -52% DD; point-in-time S&P 500 17.6%, -39%.
- Filter RULE: sector AND sub-industry above 21 EMA: 15.2% CAGR, -49% DD; point-in-time S&P 500 18.1%, -26%.
- Filter RULE: SPY > 21 & 50 + sector & sub-industry up 5 days: 15.0% CAGR, -36% DD; point-in-time S&P 500 16.1%, -17%.
- Regime gate (no gate) (skip nothing): 25.3% CAGR, -45% DD; point-in-time S&P 500 21.3%, -30%.

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
3. Focus development on: ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base (tune them on IS data only, re-check OOS).
4. Make qull_scan_regime a default filter.
5. Inspect sma200_slope and above_52w_low: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early_theme first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                                          | no_edge_entries                                                            | best_exit   | helpful_filters                                                                                        |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                     | filters_lifting_baseline                  |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                                  |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret | menu_choice   |   menu_choice_oos_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:------------|:-------------------------------------------------------------------------------------------------------|---------:|---------------:|---------------:|---------:|:-----------------------------------------------------------------|:------------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:----------------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|:--------------|----------------------:|
| 2026-10-08 10:53 | d8399f4  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                          | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                                                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |             nan    |             nan    |             nan    |             nan    | nan           |                nan    |
| 2026-10-08 14:02 | 749e984  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                                                | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                                                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |               0.56 |               0.02 |               0.38 |               0.03 | nan           |                nan    |
| 2026-10-08 14:27 | e7af2f7  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                                                | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                                                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |               0.56 |               0.02 |               0.38 |               0.03 | nan           |                nan    |
| 2026-10-08 15:56 | f522ebc  |      1488 |    669685 |        0.51 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                                                | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                 |     0.51 |           0.01 |          -0.04 |     0.04 | sma200_slope, rates_rising, sector_rs, industry_rs, sma150_slope | early_stage, rs80_early, rs80_early_theme |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.46 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.83 |         4.29 | adr_pct, dist_52w_high, above_52w_low, atr_pct, mkt_above200    |               0.55 |               0.01 |               0.37 |               0.02 | nan           |                nan    |
| 2026-10-09 05:05 | 00c2b0a  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                 |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok            | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | nan           |                nan    |
| 2026-10-09 11:57 | 4ad9589  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                 |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok            | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 12:54 | 5ce3166  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                 |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok            | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 14:16 | e1db28d  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                    | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                 |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok            | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 15:34 | 246a119  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs  | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 16:26 | c39a032  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs  | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 7215.000 |
| strategies_with_enough_trades | 5839.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.491 |
| rank_corr_IS_vs_OOS_t         |    0.522 |
| OOS_avgR_all_strategies       |    0.055 |
| OOS_avgR_top20_by_IS          |    0.063 |
| OOS_avgR_top20_by_IS_avgR     |    0.401 |
| OOS_avgR_random_baseline      |   -0.020 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  69655 |      0.18 |  44.38 |   66903 |      7633.96 |      0.47 |       0.09 |     1.18 |   18.84 |         662.71 |
| wf_scan_pullback | all           | bracket_20_10 |  70921 |      0.18 |  44.24 |   68948 |      7867.31 |      0.47 |       0.09 |     1.18 |   19.22 |         689.91 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70047 |      0.15 |  43.44 |   66903 |      7633.96 |      0.54 |       0.06 |     1.14 |   16.31 |         458.47 |
| wf_scan_pullback | all           | bracket_10_10 |  71318 |      0.15 |  43.32 |   68948 |      7867.31 |      0.54 |       0.06 |     1.14 |   16.38 |         468.74 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  60848 |      0.17 |  38.51 |   58101 |      6629.61 |      0.48 |       0.11 |     1.25 |   23.06 |         760.10 |
| donchian_20      | all           | bracket_20_10 |  68853 |      0.16 |  38.02 |   78126 |      8914.56 |      0.45 |       0.07 |     1.14 |   16.40 |         649.43 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61240 |      0.14 |  37.69 |   58101 |      6629.61 |      0.55 |       0.08 |     1.20 |   20.71 |         541.88 |
| pocket_pivot     | all           | bracket_20_10 |  48141 |      0.19 |  37.28 |   48061 |      5484.00 |      0.45 |       0.06 |     1.12 |   11.02 |         330.58 |
| pocket_pivot     | all           | bracket_10_10 |  48547 |      0.15 |  37.15 |   48061 |      5484.00 |      0.53 |       0.05 |     1.11 |   10.60 |         255.64 |
| donchian_20      | all           | bracket_10_10 |  69295 |      0.13 |  36.32 |   78126 |      8914.56 |      0.53 |       0.05 |     1.11 |   13.49 |         421.85 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57045 |      0.17 |  35.79 |   61637 |      7033.09 |      0.45 |       0.07 |     1.14 |   14.45 |         510.12 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  49850 |      0.17 |  35.45 |   47149 |      5379.94 |      0.46 |       0.07 |     1.15 |   13.36 |         395.47 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50189 |      0.13 |  33.98 |   47149 |      5379.94 |      0.53 |       0.05 |     1.12 |   11.23 |         266.09 |
| donchian_20      | mkt_ok        | bracket_10_10 |  57441 |      0.13 |  33.85 |   61637 |      7033.09 |      0.53 |       0.05 |     1.11 |   11.88 |         331.06 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  35792 |      0.16 |  33.53 |   32098 |      3662.54 |      0.53 |       0.05 |     1.11 |    8.78 |         170.74 |
| wf_scan_base     | all           | bracket_20_10 |  31524 |      0.19 |  33.50 |   24702 |      2818.62 |      0.47 |       0.04 |     1.09 |    5.89 |         116.52 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35476 |      0.19 |  33.05 |   32098 |      3662.54 |      0.46 |       0.06 |     1.12 |    9.04 |         216.87 |
| donchian_20      | wf_scan       | bracket_20_10 |  42702 |      0.17 |  32.56 |   41007 |      4679.10 |      0.45 |       0.05 |     1.11 |    9.03 |         249.59 |
| wf_scan_base     | all           | bracket_10_10 |  31742 |      0.16 |  32.47 |   24702 |      2818.62 |      0.53 |       0.04 |     1.09 |    6.09 |         100.99 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35003 |      0.18 |  31.93 |   33711 |      3846.59 |      0.46 |       0.06 |     1.11 |    8.56 |         213.96 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  24900 |      0.20 |  31.85 |   17385 |      1983.71 |      0.48 |       0.04 |     1.09 |    4.70 |          75.33 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35353 |      0.15 |  31.68 |   33711 |      3846.59 |      0.53 |       0.05 |     1.11 |    8.70 |         175.61 |
| donchian_55      | all           | bracket_20_10 |  47020 |      0.16 |  31.59 |   50721 |      5787.52 |      0.45 |       0.06 |     1.11 |   10.41 |         327.41 |
| donchian_20      | wf_scan       | bracket_10_10 |  43003 |      0.14 |  31.58 |   41007 |      4679.10 |      0.53 |       0.03 |     1.07 |    6.44 |         142.77 |
| donchian_55      | all           | bracket_10_10 |  47376 |      0.13 |  31.17 |   50721 |      5787.52 |      0.52 |       0.03 |     1.07 |    6.91 |         172.04 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25076 |      0.16 |  30.84 |   17385 |      1983.71 |      0.53 |       0.04 |     1.11 |    6.14 |          83.82 |
| donchian_20      | early_stage   | bracket_20_10 |  36256 |      0.19 |  30.54 |   47186 |      5384.16 |      0.46 |       0.09 |     1.19 |   16.35 |         511.13 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23063 |      0.21 |  29.40 |   25684 |      2930.67 |      0.47 |       0.10 |     1.20 |   13.03 |         285.65 |
| undercut         | all           | bracket_20_10 |  22854 |      0.23 |  29.31 |   26333 |      3004.73 |      0.47 |       0.13 |     1.26 |   16.48 |         381.72 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  26857 |      0.18 |  29.29 |   19721 |      2250.26 |      0.47 |       0.03 |     1.07 |    4.09 |          72.79 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  69655 |      0.18 |  44.38 |   66903 |      0.47 |       0.09 |     1.18 |   18.84 |
| wf_scan_pullback | all           | bracket_20_10 |  70921 |      0.18 |  44.24 |   68948 |      0.47 |       0.09 |     1.18 |   19.22 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70047 |      0.15 |  43.44 |   66903 |      0.54 |       0.06 |     1.14 |   16.31 |
| wf_scan_pullback | all           | bracket_10_10 |  71318 |      0.15 |  43.32 |   68948 |      0.54 |       0.06 |     1.14 |   16.38 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  60848 |      0.17 |  38.51 |   58101 |      0.48 |       0.11 |     1.25 |   23.06 |
| donchian_20      | all           | bracket_20_10 |  68853 |      0.16 |  38.02 |   78126 |      0.45 |       0.07 |     1.14 |   16.40 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61240 |      0.14 |  37.69 |   58101 |      0.55 |       0.08 |     1.20 |   20.71 |
| pocket_pivot     | all           | bracket_20_10 |  48141 |      0.19 |  37.28 |   48061 |      0.45 |       0.06 |     1.12 |   11.02 |
| pocket_pivot     | all           | bracket_10_10 |  48547 |      0.15 |  37.15 |   48061 |      0.53 |       0.05 |     1.11 |   10.60 |
| donchian_20      | all           | bracket_10_10 |  69295 |      0.13 |  36.32 |   78126 |      0.53 |       0.05 |     1.11 |   13.49 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57045 |      0.17 |  35.79 |   61637 |      0.45 |       0.07 |     1.14 |   14.45 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  49850 |      0.17 |  35.45 |   47149 |      0.46 |       0.07 |     1.15 |   13.36 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50189 |      0.13 |  33.98 |   47149 |      0.53 |       0.05 |     1.12 |   11.23 |
| donchian_20      | mkt_ok        | bracket_10_10 |  57441 |      0.13 |  33.85 |   61637 |      0.53 |       0.05 |     1.11 |   11.88 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  35792 |      0.16 |  33.53 |   32098 |      0.53 |       0.05 |     1.11 |    8.78 |
| wf_scan_base     | all           | bracket_20_10 |  31524 |      0.19 |  33.50 |   24702 |      0.47 |       0.04 |     1.09 |    5.89 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35476 |      0.19 |  33.05 |   32098 |      0.46 |       0.06 |     1.12 |    9.04 |
| donchian_20      | wf_scan       | bracket_20_10 |  42702 |      0.17 |  32.56 |   41007 |      0.45 |       0.05 |     1.11 |    9.03 |
| wf_scan_base     | all           | bracket_10_10 |  31742 |      0.16 |  32.47 |   24702 |      0.53 |       0.04 |     1.09 |    6.09 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35003 |      0.18 |  31.93 |   33711 |      0.46 |       0.06 |     1.11 |    8.56 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  24900 |      0.20 |  31.85 |   17385 |      0.48 |       0.04 |     1.09 |    4.70 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35353 |      0.15 |  31.68 |   33711 |      0.53 |       0.05 |     1.11 |    8.70 |
| donchian_55      | all           | bracket_20_10 |  47020 |      0.16 |  31.59 |   50721 |      0.45 |       0.06 |     1.11 |   10.41 |
| donchian_20      | wf_scan       | bracket_10_10 |  43003 |      0.14 |  31.58 |   41007 |      0.53 |       0.03 |     1.07 |    6.44 |
| donchian_55      | all           | bracket_10_10 |  47376 |      0.13 |  31.17 |   50721 |      0.52 |       0.03 |     1.07 |    6.91 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25076 |      0.16 |  30.84 |   17385 |      0.53 |       0.04 |     1.11 |    6.14 |
| donchian_20      | early_stage   | bracket_20_10 |  36256 |      0.19 |  30.54 |   47186 |      0.46 |       0.09 |     1.19 |   16.35 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23063 |      0.21 |  29.40 |   25684 |      0.47 |       0.10 |     1.20 |   13.03 |
| undercut         | all           | bracket_20_10 |  22854 |      0.23 |  29.31 |   26333 |      0.47 |       0.13 |     1.26 |   16.48 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  26857 |      0.18 |  29.29 |   19721 |      0.47 |       0.03 |     1.07 |    4.09 |

## 4. Each entry with its best in-sample exit/filter

| entry              | filter           | exit          |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-------------------|:-----------------|:--------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| ep_gap15           | rs80_mkt         | bracket_20_10 |     62 |        5.17 |     0.56 |      0.58 |   3.26 |     140 |        15.97 |      0.44 |       0.21 |     1.36 |    1.70 |           3.29 |
| flag_30            | rs80_early_theme | bracket_20_10 |    160 |       13.34 |     0.47 |      0.27 |   2.42 |     238 |        27.16 |      0.42 |       0.18 |     1.30 |    1.86 |           4.80 |
| ep_gap10_vol5      | wf_scan_green    | bracket_10_10 |    143 |       11.92 |     0.66 |      0.31 |   3.91 |     175 |        19.97 |      0.59 |       0.16 |     1.39 |    2.13 |           3.16 |
| falling_wedge      | all              | bracket_20_10 |   1255 |      104.63 |     0.58 |      0.30 |   9.23 |    1522 |       173.67 |      0.48 |       0.16 |     1.33 |    4.93 |          26.94 |
| ep_gap8_neglected  | wf_scan_green    | bracket_10_10 |    159 |       13.26 |     0.69 |      0.34 |   4.91 |     206 |        23.51 |      0.58 |       0.15 |     1.38 |    2.26 |           3.61 |
| ep_gap10_vol2      | wf_scan_green    | bracket_10_10 |    214 |       17.84 |     0.63 |      0.25 |   3.82 |     388 |        44.27 |      0.58 |       0.15 |     1.35 |    2.90 |           6.47 |
| ep_gap10           | wf_scan_green    | bracket_10_10 |    197 |       16.42 |     0.62 |      0.23 |   3.41 |     321 |        36.63 |      0.58 |       0.14 |     1.32 |    2.46 |           4.97 |
| undercut           | all              | bracket_20_10 |  22854 |     1905.37 |     0.54 |      0.23 |  29.31 |   26333 |      3004.73 |      0.47 |       0.13 |     1.26 |   16.48 |         381.72 |
| desc_triangle      | all              | bracket_20_10 |    765 |       63.78 |     0.57 |      0.24 |   6.11 |     705 |        80.44 |      0.48 |       0.12 |     1.26 |    2.64 |           9.45 |
| random_uptrend     | all              | bracket_20_10 |  30366 |     2531.66 |     0.53 |      0.19 |  29.07 |   34140 |      3895.54 |      0.46 |       0.10 |     1.20 |   14.93 |         392.63 |
| base_25            | mkt_ok           | bracket_20_10 |   1476 |      123.06 |     0.46 |      0.14 |   4.04 |    1879 |       214.40 |      0.42 |       0.09 |     1.15 |    2.77 |          18.75 |
| wf_scan_pullback   | wf_scan          | bracket_20_10 |  69655 |     5807.23 |     0.55 |      0.18 |  44.38 |   66903 |      7633.96 |      0.47 |       0.09 |     1.18 |   18.84 |         662.71 |
| ep_gap8_hold       | wf_scan_green    | bracket_10_10 |    291 |       24.26 |     0.64 |      0.26 |   4.65 |     425 |        48.49 |      0.55 |       0.08 |     1.19 |    1.75 |           4.11 |
| ema_retest         | all              | bracket_20_10 |  14308 |     1192.88 |     0.55 |      0.19 |  21.04 |   15672 |      1788.25 |      0.46 |       0.08 |     1.16 |    8.05 |         139.59 |
| sym_triangle       | all              | bracket_10_10 |    882 |       73.53 |     0.58 |      0.13 |   4.11 |     917 |       104.63 |      0.55 |       0.08 |     1.18 |    2.42 |           8.07 |
| ep_gap5            | wf_scan_green    | bracket_10_10 |    837 |       69.78 |     0.62 |      0.22 |   6.82 |     900 |       102.69 |      0.55 |       0.08 |     1.18 |    2.34 |           7.90 |
| donchian_20        | all              | bracket_20_10 |  68853 |     5740.37 |     0.52 |      0.16 |  38.02 |   78126 |      8914.56 |      0.45 |       0.07 |     1.14 |   16.40 |         649.43 |
| flag_60            | rs80_theme       | bracket_20_10 |    165 |       13.76 |     0.45 |      0.28 |   2.43 |     294 |        33.55 |      0.37 |       0.07 |     1.11 |    0.82 |           2.43 |
| asc_triangle       | all              | bracket_20_10 |   1075 |       89.62 |     0.57 |      0.19 |   6.07 |     860 |        98.13 |      0.47 |       0.07 |     1.14 |    1.64 |           6.41 |
| pocket_pivot       | all              | bracket_20_10 |  48141 |     4013.58 |     0.54 |      0.19 |  37.28 |   48061 |      5484.00 |      0.45 |       0.06 |     1.12 |   11.02 |         330.58 |
| qull_breakout_60   | wf_scan_green    | bracket_10_10 |    349 |       29.10 |     0.56 |      0.13 |   2.20 |     954 |       108.86 |      0.53 |       0.06 |     1.12 |    1.74 |           6.42 |
| donchian_55        | all              | bracket_20_10 |  47020 |     3920.12 |     0.53 |      0.16 |  31.59 |   50721 |      5787.52 |      0.45 |       0.06 |     1.11 |   10.41 |         327.41 |
| wf_rocket_breakout | all              | bracket_20_10 |   2370 |      197.59 |     0.55 |      0.21 |   8.90 |    2489 |       284.01 |      0.45 |       0.05 |     1.11 |    2.23 |          15.41 |
| qull_breakout      | wf_scan_green    | bracket_10_10 |    883 |       73.62 |     0.57 |      0.13 |   3.69 |    1932 |       220.45 |      0.53 |       0.05 |     1.11 |    2.20 |          11.50 |
| wf_rocket_gap      | wf_scan_green    | bracket_10_10 |   1227 |      102.30 |     0.60 |      0.19 |   6.86 |    1458 |       166.37 |      0.54 |       0.05 |     1.11 |    1.92 |           8.17 |
| flag_30_early      | mkt_ok           | bracket_10_10 |    847 |       70.62 |     0.56 |      0.10 |   2.92 |    1446 |       165.00 |      0.52 |       0.05 |     1.10 |    1.70 |           7.68 |
| wf_scan_base       | all              | bracket_20_10 |  31524 |     2628.20 |     0.57 |      0.19 |  33.50 |   24702 |      2818.62 |      0.47 |       0.04 |     1.09 |    5.89 |         116.52 |
| high52_fresh       | all              | bracket_10_10 |   8097 |      675.06 |     0.61 |      0.16 |  16.73 |    8423 |       961.11 |      0.53 |       0.03 |     1.07 |    3.00 |          30.23 |
| base_50            | all              | bracket_10_10 |   2289 |      190.84 |     0.56 |      0.10 |   4.89 |    2666 |       304.20 |      0.52 |       0.02 |     1.05 |    1.19 |           7.05 |
| high52             | all              | bracket_10_10 |  29829 |     2486.88 |     0.59 |      0.14 |  26.48 |   29131 |      3323.99 |      0.52 |       0.02 |     1.04 |    3.48 |          65.00 |
| rising_wedge       | all              | bracket_10_10 |   2065 |      172.16 |     0.58 |      0.13 |   6.46 |    1730 |       197.40 |      0.52 |       0.02 |     1.04 |    0.82 |           3.71 |
| tight_coil_7       | all              | bracket_10_10 |   6285 |      523.99 |     0.59 |      0.15 |  13.44 |    5356 |       611.15 |      0.51 |       0.01 |     1.03 |    0.98 |           7.97 |
| vcp                | wf_scan          | bracket_20_10 |   1152 |       96.04 |     0.56 |      0.19 |   5.91 |     721 |        82.27 |      0.45 |       0.01 |     1.02 |    0.22 |           0.74 |
| multi_touch        | all              | bracket_10_10 |  12466 |     1039.31 |     0.59 |      0.14 |  16.93 |   10634 |      1213.39 |      0.51 |      -0.00 |     1.00 |   -0.13 |          -1.48 |
| stage2             | all              | bracket_10_10 |   5907 |      492.47 |     0.61 |      0.18 |  15.78 |    4847 |       553.07 |      0.51 |      -0.00 |     0.99 |   -0.29 |          -2.19 |
| tight_coil_15      | wf_scan          | bracket_10_10 |    890 |       74.20 |     0.62 |      0.19 |   6.50 |     685 |        78.16 |      0.48 |      -0.05 |     0.90 |   -1.25 |          -3.57 |
| htf                | all              | sma50_close   |     53 |        4.42 |     0.17 |      0.39 |   0.63 |      99 |        11.30 |      0.11 |      -0.34 |     0.65 |   -1.17 |          -3.85 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |           -0.04 |           -0.04 |              0.05 |             0.06 |          0.03 |           0.10 |         0.05 |         0.04 |         0.02 |         -0.00 |       0.10 |        0.03 |         -0.05 |
| base_25            |           -0.03 |            0.01 |              0.10 |             0.08 |          0.09 |           0.08 |         0.09 |         0.04 |         0.07 |          0.22 |       0.13 |        0.19 |          0.19 |
| base_50            |           -0.05 |           -0.01 |              0.14 |             0.10 |          0.13 |           0.11 |         0.11 |         0.07 |         0.10 |          0.21 |       0.15 |        0.19 |          0.20 |
| desc_triangle      |            0.02 |            0.02 |              0.27 |             0.26 |          0.23 |           0.23 |         0.29 |         0.16 |         0.21 |          0.07 |       0.20 |        0.08 |          0.15 |
| donchian_20        |           -0.02 |           -0.03 |              0.09 |             0.08 |          0.10 |           0.12 |         0.08 |         0.08 |         0.09 |          0.06 |       0.12 |        0.07 |          0.04 |
| donchian_55        |           -0.04 |           -0.04 |              0.06 |             0.05 |          0.07 |           0.09 |         0.06 |         0.06 |         0.06 |          0.06 |       0.11 |        0.06 |          0.03 |
| ema_retest         |           -0.02 |           -0.02 |              0.06 |             0.05 |          0.07 |           0.10 |         0.08 |         0.07 |         0.06 |          0.07 |       0.11 |        0.07 |          0.04 |
| ep_gap10           |           -0.04 |            0.01 |              0.24 |             0.35 |          0.27 |           0.20 |         0.15 |         0.11 |         0.18 |          0.51 |       0.32 |        0.44 |          0.52 |
| ep_gap10_vol2      |           -0.04 |            0.05 |              0.30 |             0.36 |          0.27 |           0.19 |         0.20 |         0.13 |         0.18 |          0.50 |       0.31 |        0.44 |          0.54 |
| ep_gap10_vol5      |           -0.07 |            0.02 |              0.25 |             0.33 |          0.23 |           0.21 |         0.12 |         0.10 |         0.12 |          0.53 |       0.34 |        0.43 |          0.50 |
| ep_gap15           |            0.01 |            0.11 |              0.30 |             0.34 |          0.28 |           0.26 |         0.27 |         0.12 |         0.16 |          0.74 |       0.39 |        0.62 |          0.81 |
| ep_gap5            |           -0.05 |           -0.02 |              0.14 |             0.17 |          0.15 |           0.13 |         0.09 |         0.09 |         0.11 |          0.20 |       0.16 |        0.18 |          0.18 |
| ep_gap8_hold       |           -0.03 |            0.01 |              0.18 |             0.27 |          0.22 |           0.17 |         0.14 |         0.10 |         0.14 |          0.40 |       0.26 |        0.34 |          0.39 |
| ep_gap8_neglected  |           -0.04 |           -0.02 |              0.13 |             0.18 |          0.22 |           0.19 |         0.18 |         0.10 |         0.13 |          0.29 |       0.24 |        0.29 |          0.30 |
| falling_wedge      |            0.03 |            0.05 |              0.18 |             0.14 |          0.10 |           0.19 |         0.20 |         0.06 |         0.09 |          0.02 |       0.08 |        0.03 |         -0.01 |
| flag_30            |           -0.05 |            0.02 |              0.05 |             0.12 |          0.13 |           0.07 |         0.03 |         0.07 |         0.07 |          0.27 |       0.15 |        0.19 |          0.21 |
| flag_30_early      |           -0.01 |            0.08 |              0.16 |             0.15 |          0.15 |           0.15 |         0.20 |         0.13 |         0.13 |          0.23 |       0.18 |        0.23 |          0.35 |
| flag_60            |           -0.07 |            0.06 |              0.17 |             0.15 |          0.18 |           0.10 |         0.10 |         0.12 |         0.11 |          0.51 |       0.31 |        0.37 |          0.37 |
| high52             |           -0.05 |           -0.06 |             -0.05 |            -0.05 |         -0.03 |          -0.02 |        -0.04 |        -0.03 |        -0.04 |         -0.05 |      -0.02 |       -0.04 |         -0.08 |
| high52_fresh       |           -0.04 |           -0.05 |              0.05 |             0.04 |          0.08 |           0.06 |         0.05 |         0.04 |         0.04 |          0.07 |       0.08 |        0.07 |          0.04 |
| htf                |           -0.26 |           -0.17 |             -0.20 |            -0.30 |         -0.13 |          -0.14 |        -0.18 |        -0.01 |        -0.09 |         -0.32 |      -0.07 |       -0.27 |         -0.32 |
| multi_touch        |           -0.07 |           -0.09 |             -0.04 |            -0.01 |         -0.02 |           0.01 |        -0.04 |         0.01 |        -0.01 |         -0.07 |      -0.01 |       -0.05 |         -0.09 |
| pocket_pivot       |           -0.02 |           -0.04 |             -0.03 |            -0.03 |         -0.01 |           0.01 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.00 |       -0.04 |         -0.06 |
| qull_breakout      |           -0.03 |            0.05 |             -0.09 |            -0.09 |         -0.07 |          -0.13 |        -0.10 |        -0.14 |        -0.12 |          0.04 |      -0.08 |       -0.01 |         -0.00 |
| qull_breakout_60   |           -0.02 |            0.10 |             -0.09 |            -0.09 |         -0.05 |          -0.11 |        -0.06 |        -0.14 |        -0.11 |          0.14 |      -0.07 |        0.07 |          0.04 |
| rising_wedge       |           -0.05 |           -0.06 |             -0.04 |            -0.05 |         -0.02 |           0.05 |         0.02 |         0.08 |         0.04 |         -0.07 |       0.01 |       -0.04 |         -0.10 |
| stage2             |           -0.07 |           -0.09 |             -0.08 |            -0.07 |         -0.06 |          -0.01 |        -0.08 |        -0.02 |        -0.04 |         -0.11 |      -0.05 |       -0.10 |         -0.13 |
| sym_triangle       |            0.01 |            0.00 |              0.19 |             0.12 |          0.13 |           0.18 |         0.16 |         0.13 |         0.15 |          0.03 |       0.10 |        0.06 |          0.04 |
| tight_coil_15      |           -0.09 |           -0.11 |             -0.01 |            -0.03 |          0.00 |           0.06 |        -0.01 |         0.06 |         0.04 |         -0.10 |       0.03 |       -0.07 |         -0.13 |
| tight_coil_7       |           -0.06 |           -0.07 |              0.01 |             0.01 |          0.04 |           0.08 |         0.03 |         0.07 |         0.05 |         -0.02 |       0.07 |       -0.01 |         -0.03 |
| undercut           |            0.02 |            0.03 |              0.17 |             0.16 |          0.03 |           0.09 |         0.12 |         0.09 |         0.09 |         -0.01 |       0.03 |        0.00 |          0.04 |
| vcp                |           -0.02 |           -0.05 |              0.05 |             0.04 |          0.04 |           0.11 |         0.04 |         0.07 |         0.07 |         -0.06 |       0.05 |       -0.03 |         -0.11 |
| wf_rocket_breakout |           -0.03 |           -0.05 |              0.08 |             0.09 |          0.10 |           0.12 |         0.07 |         0.10 |         0.10 |          0.08 |       0.14 |        0.08 |          0.05 |
| wf_rocket_gap      |            0.01 |            0.07 |              0.24 |             0.26 |          0.24 |           0.20 |         0.25 |         0.14 |         0.19 |          0.30 |       0.26 |        0.28 |          0.31 |
| wf_scan_base       |           -0.03 |           -0.06 |              0.09 |             0.07 |          0.09 |           0.11 |         0.08 |         0.09 |         0.09 |          0.02 |       0.10 |        0.03 |         -0.01 |
| wf_scan_pullback   |           -0.01 |           -0.01 |              0.10 |             0.08 |          0.07 |           0.11 |         0.10 |         0.09 |         0.08 |          0.03 |       0.10 |        0.04 |          0.01 |

Same, in-sample:

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |            0.01 |            0.00 |              0.03 |             0.01 |          0.05 |           0.07 |         0.06 |         0.06 |         0.04 |         -0.02 |       0.09 |       -0.00 |         -0.00 |
| base_25            |           -0.07 |           -0.07 |             -0.02 |            -0.02 |          0.01 |           0.07 |        -0.05 |         0.08 |         0.06 |          0.05 |       0.10 |        0.03 |          0.05 |
| base_50            |           -0.04 |           -0.06 |              0.01 |             0.03 |          0.05 |           0.14 |        -0.02 |         0.10 |         0.07 |         -0.01 |       0.11 |        0.01 |         -0.04 |
| desc_triangle      |            0.04 |            0.05 |              0.21 |             0.34 |          0.18 |           0.23 |         0.25 |         0.19 |         0.19 |          0.27 |       0.29 |        0.26 |          0.34 |
| donchian_20        |           -0.02 |           -0.03 |              0.11 |             0.13 |          0.15 |           0.16 |         0.11 |         0.12 |         0.12 |          0.14 |       0.19 |        0.13 |          0.14 |
| donchian_55        |           -0.02 |           -0.03 |              0.09 |             0.11 |          0.13 |           0.13 |         0.09 |         0.10 |         0.10 |          0.12 |       0.18 |        0.12 |          0.12 |
| ema_retest         |            0.00 |            0.01 |              0.10 |             0.11 |          0.14 |           0.12 |         0.17 |         0.07 |         0.08 |          0.17 |       0.15 |        0.17 |          0.17 |
| ep_gap10           |           -0.03 |           -0.00 |              0.16 |             0.13 |          0.16 |           0.11 |        -0.03 |         0.15 |         0.11 |          0.20 |       0.24 |        0.16 |          0.14 |
| ep_gap10_vol2      |           -0.05 |           -0.04 |              0.14 |             0.09 |          0.13 |           0.10 |        -0.03 |         0.12 |         0.09 |          0.15 |       0.20 |        0.13 |          0.09 |
| ep_gap10_vol5      |            0.03 |            0.05 |              0.23 |             0.20 |          0.19 |           0.21 |         0.04 |         0.24 |         0.19 |          0.32 |       0.34 |        0.28 |          0.19 |
| ep_gap15           |            0.06 |            0.12 |              0.44 |             0.34 |          0.34 |           0.31 |         0.13 |         0.33 |         0.31 |          0.46 |       0.49 |        0.41 |          0.35 |
| ep_gap5            |           -0.02 |           -0.03 |              0.18 |             0.15 |          0.18 |           0.15 |         0.10 |         0.15 |         0.15 |          0.27 |       0.24 |        0.24 |          0.24 |
| ep_gap8_hold       |           -0.01 |            0.02 |              0.25 |             0.25 |          0.25 |           0.18 |         0.14 |         0.17 |         0.17 |          0.31 |       0.33 |        0.29 |          0.30 |
| ep_gap8_neglected  |            0.01 |            0.05 |              0.26 |             0.27 |          0.26 |           0.19 |         0.20 |         0.17 |         0.20 |          0.34 |       0.31 |        0.33 |          0.34 |
| falling_wedge      |            0.07 |            0.11 |              0.34 |             0.38 |          0.24 |           0.31 |         0.40 |         0.22 |         0.24 |          0.15 |       0.21 |        0.15 |          0.26 |
| flag_30            |           -0.14 |           -0.14 |             -0.08 |            -0.08 |         -0.04 |           0.05 |        -0.10 |         0.03 |        -0.01 |         -0.07 |       0.02 |       -0.06 |         -0.14 |
| flag_30_early      |           -0.09 |           -0.11 |              0.11 |             0.08 |          0.11 |           0.05 |        -0.03 |         0.06 |         0.10 |         -0.01 |       0.03 |        0.01 |          0.00 |
| flag_60            |           -0.13 |           -0.10 |              0.06 |             0.05 |          0.10 |           0.12 |        -0.00 |         0.15 |         0.11 |          0.10 |       0.13 |        0.11 |         -0.01 |
| high52             |           -0.01 |           -0.03 |             -0.03 |            -0.02 |          0.03 |           0.02 |        -0.02 |        -0.01 |        -0.01 |         -0.01 |       0.01 |       -0.01 |         -0.03 |
| high52_fresh       |            0.02 |            0.01 |              0.06 |             0.08 |          0.10 |           0.08 |         0.08 |         0.05 |         0.06 |          0.09 |       0.10 |        0.09 |          0.05 |
| htf                |           -0.23 |           -0.17 |             -0.08 |             0.26 |          0.14 |           0.06 |        -0.09 |         0.13 |         0.20 |          0.44 |       0.28 |        0.26 |          0.41 |
| multi_touch        |           -0.01 |           -0.02 |              0.07 |             0.11 |          0.13 |           0.11 |         0.11 |         0.08 |         0.07 |          0.14 |       0.12 |        0.14 |          0.12 |
| pocket_pivot       |            0.01 |           -0.00 |              0.06 |             0.08 |          0.08 |           0.04 |         0.06 |         0.04 |         0.04 |          0.09 |       0.06 |        0.08 |          0.09 |
| qull_breakout      |           -0.16 |           -0.18 |             -0.33 |            -0.32 |         -0.25 |          -0.20 |        -0.36 |        -0.17 |        -0.20 |         -0.34 |      -0.22 |       -0.32 |         -0.37 |
| qull_breakout_60   |           -0.15 |           -0.18 |             -0.26 |            -0.28 |         -0.22 |          -0.23 |        -0.35 |        -0.15 |        -0.18 |         -0.29 |      -0.19 |       -0.27 |         -0.33 |
| rising_wedge       |           -0.02 |           -0.04 |              0.02 |             0.04 |          0.08 |           0.09 |         0.01 |         0.06 |         0.05 |          0.06 |       0.12 |        0.06 |          0.07 |
| stage2             |            0.03 |            0.02 |              0.11 |             0.15 |          0.17 |           0.12 |         0.17 |         0.09 |         0.11 |          0.17 |       0.16 |        0.17 |          0.15 |
| sym_triangle       |           -0.01 |           -0.04 |              0.10 |             0.13 |          0.14 |           0.12 |         0.04 |         0.13 |         0.11 |          0.11 |       0.14 |        0.10 |          0.07 |
| tight_coil_15      |            0.01 |           -0.01 |              0.15 |             0.20 |          0.15 |           0.16 |         0.17 |         0.14 |         0.14 |          0.15 |       0.25 |        0.15 |          0.19 |
| tight_coil_7       |            0.01 |           -0.01 |              0.13 |             0.19 |          0.16 |           0.16 |         0.13 |         0.12 |         0.11 |          0.18 |       0.24 |        0.18 |          0.19 |
| undercut           |            0.02 |            0.04 |              0.22 |             0.25 |          0.06 |           0.13 |         0.21 |         0.19 |         0.18 |          0.03 |       0.09 |        0.02 |          0.09 |
| vcp                |           -0.01 |           -0.03 |              0.08 |             0.11 |          0.13 |           0.14 |         0.11 |         0.11 |         0.10 |          0.11 |       0.18 |        0.11 |          0.12 |
| wf_rocket_breakout |            0.02 |            0.02 |              0.14 |             0.15 |          0.20 |           0.21 |         0.15 |         0.15 |         0.17 |          0.16 |       0.25 |        0.17 |          0.15 |
| wf_rocket_gap      |           -0.04 |           -0.05 |              0.13 |             0.12 |          0.14 |           0.14 |         0.09 |         0.14 |         0.14 |          0.17 |       0.21 |        0.15 |          0.12 |
| wf_scan_base       |            0.01 |            0.00 |              0.12 |             0.15 |          0.17 |           0.17 |         0.15 |         0.14 |         0.15 |          0.12 |       0.22 |        0.12 |          0.12 |
| wf_scan_pullback   |           -0.00 |           -0.01 |              0.15 |             0.17 |          0.15 |           0.18 |         0.14 |         0.14 |         0.14 |          0.11 |       0.19 |        0.11 |          0.12 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| wf_weekly10     |      0.08 |       0.12 |      0.26 |     1.17 |                       0.64 |
| sma50_close     |      0.07 |       0.11 |      0.26 |     1.16 |                       0.69 |
| bracket_20_10   |      0.16 |       0.09 |      0.44 |     1.17 |                       0.44 |
| wf_rocket       |      0.06 |       0.08 |      0.27 |     1.12 |                       0.72 |
| oneil_20_8      |      0.12 |       0.04 |      0.27 |     1.06 |                       0.78 |
| bracket_10_10   |      0.12 |       0.03 |      0.52 |     1.08 |                       0.17 |
| trim_ema        |      0.01 |       0.02 |      0.34 |     1.04 |                       0.81 |
| donchian_10low  |      0.02 |       0.01 |      0.29 |     1.03 |                       0.75 |
| chandelier_3atr |      0.03 |       0.00 |      0.29 |     1.02 |                       0.75 |
| fixed_3r_20d    |     -0.00 |      -0.01 |      0.37 |     1.00 |                       0.86 |
| ema21_close     |     -0.04 |      -0.02 |      0.30 |     0.98 |                       0.78 |
| qull_sma20      |     -0.04 |      -0.03 |      0.43 |     0.95 |                       0.81 |
| qull_sma10      |     -0.05 |      -0.04 |      0.42 |     0.92 |                       0.86 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| qull_scan_regime |     -0.03 |       0.16 |      0.34 |
| rs80_early       |      0.09 |       0.14 |      0.37 |
| qull_scan        |     -0.04 |       0.13 |      0.34 |
| rs80_early_theme |      0.10 |       0.10 |      0.35 |
| early_stage      |      0.07 |       0.08 |      0.36 |
| wf_scan_green    |      0.06 |       0.07 |      0.35 |
| wf_rocket_green  |      0.05 |       0.06 |      0.35 |
| rs80             |      0.05 |       0.06 |      0.35 |
| wf_scan          |      0.06 |       0.05 |      0.35 |
| rs80_mkt         |      0.07 |       0.04 |      0.34 |
| wf_rocket        |      0.01 |       0.04 |      0.34 |
| rs80_theme       |      0.04 |       0.04 |      0.35 |
| all              |      0.04 |       0.03 |      0.34 |
| theme            |      0.04 |       0.03 |      0.35 |
| mkt_ok           |      0.05 |       0.03 |      0.34 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.015; AUC for R > 0: 0.512 (0.5 = no skill). Taken (model's top third, causal threshold): n=112,140, avgR=0.094, win=0.468. Skipped: n=296,094, avgR=0.064, win=0.447.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 40824.00 |   0.07 |  0.44 |
|      1 | 40823.00 |   0.06 |  0.44 |
|      2 | 40823.00 |   0.08 |  0.45 |
|      3 | 40824.00 |   0.07 |  0.45 |
|      4 | 40823.00 |   0.07 |  0.45 |
|      5 | 40823.00 |   0.08 |  0.46 |
|      6 | 40824.00 |   0.06 |  0.45 |
|      7 | 40823.00 |   0.05 |  0.45 |
|      8 | 40823.00 |   0.06 |  0.46 |
|      9 | 40824.00 |   0.13 |  0.49 |

Per entry (OOS):

| entry_name         |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:-------------------|---------:|-----------:|----------:|-------------:|---------------:|
| ep_gap15           |   374.00 |       0.21 |    181.00 |         0.31 |           0.12 |
| wf_rocket_gap      |  3943.00 |       0.17 |   1288.00 |         0.29 |           0.12 |
| ep_gap8_neglected  |   934.00 |       0.08 |    361.00 |         0.23 |          -0.01 |
| ep_gap10_vol2      |  1181.00 |       0.15 |    480.00 |         0.23 |           0.10 |
| ep_gap10_vol5      |   454.00 |       0.12 |    201.00 |         0.23 |           0.03 |
| ep_gap10           |   933.00 |       0.11 |    384.00 |         0.22 |           0.03 |
| falling_wedge      |  1522.00 |       0.16 |    576.00 |         0.21 |           0.12 |
| qull_breakout_60   |  1865.00 |       0.20 |    424.00 |         0.20 |           0.20 |
| ep_gap8_hold       |  1182.00 |       0.11 |    470.00 |         0.20 |           0.06 |
| ep_gap5            |  2322.00 |       0.08 |    843.00 |         0.19 |           0.01 |
| base_25            |  2445.00 |       0.11 |    696.00 |         0.18 |           0.08 |
| flag_30_early      |  1946.00 |       0.19 |    424.00 |         0.17 |           0.19 |
| undercut           | 26333.00 |       0.13 |   9502.00 |         0.17 |           0.10 |
| base_50            |  2666.00 |       0.09 |    791.00 |         0.15 |           0.07 |
| rising_wedge       |  1730.00 |       0.04 |    477.00 |         0.12 |           0.01 |
| vcp                |   880.00 |       0.05 |    233.00 |         0.12 |           0.03 |
| qull_breakout      |  4386.00 |       0.15 |   1023.00 |         0.11 |           0.16 |
| tight_coil_15      |  1039.00 |      -0.01 |    291.00 |         0.10 |          -0.05 |
| wf_scan_pullback   | 68948.00 |       0.09 |  19108.00 |         0.10 |           0.08 |
| flag_30            |  1790.00 |       0.12 |    408.00 |         0.09 |           0.13 |
| ema_retest         | 15672.00 |       0.08 |   4419.00 |         0.08 |           0.08 |
| high52             | 29131.00 |       0.04 |   6828.00 |         0.08 |           0.03 |
| donchian_55        | 50721.00 |       0.06 |  12612.00 |         0.08 |           0.05 |
| donchian_20        | 78126.00 |       0.07 |  20923.00 |         0.07 |           0.07 |
| multi_touch        | 10634.00 |       0.01 |   3017.00 |         0.07 |          -0.02 |
| wf_rocket_breakout |  2489.00 |       0.05 |    792.00 |         0.07 |           0.05 |
| wf_scan_base       | 24702.00 |       0.04 |   6247.00 |         0.07 |           0.03 |
| pocket_pivot       | 48061.00 |       0.06 |  13013.00 |         0.07 |           0.06 |
| high52_fresh       |  8423.00 |       0.05 |   2323.00 |         0.06 |           0.05 |
| flag_60            |   618.00 |       0.16 |    148.00 |         0.06 |           0.19 |
| tight_coil_7       |  5356.00 |       0.03 |   1420.00 |         0.05 |           0.02 |
| sym_triangle       |   917.00 |       0.10 |    248.00 |         0.05 |           0.12 |
| desc_triangle      |   705.00 |       0.12 |    223.00 |         0.03 |           0.16 |
| stage2             |  4847.00 |       0.01 |   1513.00 |         0.03 |           0.00 |
| asc_triangle       |   860.00 |       0.07 |    241.00 |        -0.05 |           0.11 |
| htf                |    99.00 |      -0.07 |     12.00 |        -0.28 |          -0.04 |

- Same model on episodic pivots only / sma50_close: rank corr 0.002, taken avgR 0.422 (n=3,294) vs skipped 0.299 (n=4,086).
- Same model on your trim plan (trim_ema): rank corr 0.112, taken avgR 0.024 (n=117,140) vs skipped -0.050 (n=291,094).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature          |   rank_corr_drop |
|:-----------------|-----------------:|
| sma200_slope     |           0.0082 |
| above_52w_low    |           0.0074 |
| rates_rising     |           0.0061 |
| adr_pct          |           0.0041 |
| industry_rs      |           0.0035 |
| rs_rank          |           0.0032 |
| sma150_slope     |           0.0025 |
| sector_rs        |           0.0025 |
| mkt_ok           |           0.0023 |
| mkt_ret_21       |           0.0016 |
| mkt_above200     |           0.0014 |
| gap              |           0.0007 |
| days_since_pivot |           0.0006 |
| close_std_10     |           0.0005 |
| ext_ema8_adr     |           0.0005 |
| leg3_range       |           0.0005 |
| close_strength   |           0.0005 |
| mkt_ema_stack    |           0.0004 |
| industry_rank    |           0.0004 |
| base_count       |           0.0004 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.558    |  11001 |      0.62 |   14950 |       0.07 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558   |  27117 |      0.34 |   41976 |       0.13 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.429 |  78674 |      0.30 |   60012 |       0.01 |      0.47 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 > 0.779    |   4654 |      0.27 |     477 |       0.97 |      0.72 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.429  |  84644 |      0.18 |   60163 |      -0.00 |      0.42 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 <= 0.0312   |  83600 |      0.18 |  115160 |       0.11 |      0.46 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 > 0.0312    |  79245 |      0.03 |  108380 |       0.07 |      0.44 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 <= 0.779   |  25735 |     -0.15 |    7116 |       0.22 |      0.48 |

## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?

Every stock every 10 trading days (n=280,518 out-of-sample rows). Base rate of a >= 40% gain within 3 months: 7.1%. The model's top 10% hit it 29.8% of the time (4.2x the base rate). AUC 0.835.

|   super_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28052.000 |      0.001 |          -0.004 |              0.011 |              0.064 |
|            1 | 28052.000 |      0.004 |           0.007 |              0.012 |              0.051 |
|            2 | 28052.000 |      0.008 |           0.016 |              0.018 |              0.049 |
|            3 | 28051.000 |      0.016 |           0.020 |              0.020 |              0.056 |
|            4 | 28052.000 |      0.025 |           0.026 |              0.026 |              0.062 |
|            5 | 28052.000 |      0.041 |           0.035 |              0.032 |              0.072 |
|            6 | 28051.000 |      0.064 |           0.040 |              0.033 |              0.085 |
|            7 | 28052.000 |      0.097 |           0.051 |              0.041 |              0.096 |
|            8 | 28052.000 |      0.155 |           0.066 |              0.046 |              0.119 |
|            9 | 28052.000 |      0.298 |           0.111 |              0.065 |              0.151 |

What matters most (permutation importance, drop in OOS AUC):

| feature           |   auc_drop |
|:------------------|-----------:|
| adr_pct           |     0.1279 |
| dist_52w_high     |     0.0258 |
| above_52w_low     |     0.0208 |
| mkt_above200      |     0.0059 |
| leg1_range        |     0.0051 |
| atr_pct           |     0.0047 |
| qull_rank         |     0.0039 |
| leg2_range        |     0.0031 |
| tight_10          |     0.0013 |
| sma200_slope      |     0.0013 |
| base_count        |     0.0010 |
| close_in_range_20 |     0.0010 |
| sma150_slope      |     0.0009 |
| contraction_ratio |     0.0007 |
| industry_rs       |     0.0006 |

Profile: future superperformers vs everything else, at the moment of the sample:

|                   |   future superperformers (median) |   everything else (median) |
|:------------------|----------------------------------:|---------------------------:|
| adr_pct           |                             0.045 |                      0.026 |
| dist_52w_high     |                            -0.271 |                     -0.127 |
| above_52w_low     |                             0.579 |                      0.340 |
| mkt_above200      |                             1.000 |                      1.000 |
| leg1_range        |                             0.185 |                      0.120 |
| atr_pct           |                             0.046 |                      0.027 |
| qull_rank         |                             0.779 |                      0.708 |
| leg2_range        |                             0.195 |                      0.120 |
| tight_10          |                             0.155 |                      0.087 |
| sma200_slope      |                             0.001 |                      0.009 |
| base_count        |                             0.000 |                      1.000 |
| close_in_range_20 |                             0.378 |                      0.473 |

Readable rules (depth-3 tree fit before 2018, scored after):

| rule                                                                 |   IS_n |   IS_rate |   OOS_n |   OOS_rate |
|:---------------------------------------------------------------------|-------:|----------:|--------:|-----------:|
| dist_52w_high <= -0.515 AND dist_52w_high <= -0.627                  |   2240 |     0.463 |     940 |      0.419 |
| dist_52w_high <= -0.515 AND dist_52w_high > -0.627                   |   3680 |     0.260 |    1849 |      0.294 |
| dist_52w_high > -0.515 AND adr_pct > 0.032 AND above_52w_low > 1.27  |   6084 |     0.157 |    4507 |      0.251 |
| dist_52w_high > -0.515 AND adr_pct > 0.032 AND above_52w_low <= 1.27 |  39049 |     0.067 |   19935 |      0.131 |
| dist_52w_high > -0.515 AND adr_pct <= 0.032 AND adr_pct > 0.025      |  35359 |     0.026 |   18672 |      0.037 |
| dist_52w_high > -0.515 AND adr_pct <= 0.032 AND adr_pct <= 0.025     | 113588 |     0.005 |   34097 |      0.009 |

Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate 6.7%, model top 10% 27.1% (4.0x), AUC 0.825.

|   clean_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28052.000 |      0.001 |          -0.006 |              0.010 |              0.069 |
|            1 | 28052.000 |      0.004 |           0.010 |              0.015 |              0.047 |
|            2 | 28052.000 |      0.010 |           0.017 |              0.018 |              0.049 |
|            3 | 28051.000 |      0.017 |           0.022 |              0.023 |              0.054 |
|            4 | 28052.000 |      0.026 |           0.027 |              0.024 |              0.063 |
|            5 | 28052.000 |      0.039 |           0.034 |              0.029 |              0.071 |
|            6 | 28051.000 |      0.060 |           0.041 |              0.035 |              0.082 |
|            7 | 28052.000 |      0.092 |           0.048 |              0.039 |              0.097 |
|            8 | 28052.000 |      0.150 |           0.064 |              0.045 |              0.121 |
|            9 | 28052.000 |      0.271 |           0.109 |              0.066 |              0.151 |

### Your goal: +10% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 50% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28052.000 |       0.263 |        0.410 |      0.342 |            0.006 |           0.022 |
|       1 | 28052.000 |       0.351 |        0.438 |      0.344 |            0.008 |           0.032 |
|       2 | 28052.000 |       0.400 |        0.469 |      0.361 |            0.010 |           0.048 |
|       3 | 28051.000 |       0.436 |        0.479 |      0.386 |            0.008 |           0.051 |
|       4 | 28052.000 |       0.467 |        0.504 |      0.387 |            0.011 |           0.098 |
|       5 | 28052.000 |       0.495 |        0.510 |      0.399 |            0.010 |           0.098 |
|       6 | 28051.000 |       0.523 |        0.515 |      0.408 |            0.009 |           0.098 |
|       7 | 28052.000 |       0.555 |        0.509 |      0.422 |            0.007 |           0.098 |
|       8 | 28052.000 |       0.598 |        0.507 |      0.429 |            0.006 |           0.098 |
|       9 | 28052.000 |       0.688 |        0.525 |      0.423 |            0.009 |           0.098 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 280518.000 |        0.487 |      0.390 |            0.008 |
| top 10%    |  28052.000 |        0.525 |      0.423 |            0.009 |
| top 5%     |  14026.000 |        0.541 |      0.418 |            0.011 |
| top 2%     |   5611.000 |        0.554 |      0.416 |            0.013 |
| top 1%     |   2806.000 |        0.554 |      0.429 |            0.011 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91950.000 |        0.465 |      0.348 |            0.011 |
| top 10%    |  7041.000 |        0.539 |      0.380 |            0.014 |
| top 5%     |  3657.000 |        0.563 |      0.375 |            0.017 |
| top 2%     |  1531.000 |        0.592 |      0.366 |            0.021 |
| top 1%     |   770.000 |        0.591 |      0.386 |            0.019 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 14140.000 |       0.261 |        0.395 |      0.306 |            0.008 |           0.024 |
|       1 | 12608.000 |       0.351 |        0.424 |      0.306 |            0.011 |           0.035 |
|       2 | 11059.000 |       0.399 |        0.459 |      0.323 |            0.013 |           0.050 |
|       3 |  9703.000 |       0.436 |        0.470 |      0.352 |            0.011 |           0.052 |
|       4 |  8684.000 |       0.467 |        0.484 |      0.362 |            0.012 |           0.064 |
|       5 |  7924.000 |       0.495 |        0.496 |      0.371 |            0.012 |           0.077 |
|       6 |  7157.000 |       0.523 |        0.500 |      0.378 |            0.011 |           0.098 |
|       7 |  6884.000 |       0.555 |        0.495 |      0.389 |            0.009 |           0.072 |
|       8 |  6750.000 |       0.598 |        0.491 |      0.400 |            0.008 |           0.062 |
|       9 |  7041.000 |       0.690 |        0.539 |      0.380 |            0.014 |           0.098 |

### Your goal: +20% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 33% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28052.000 |       0.045 |        0.058 |      0.340 |           -0.000 |          -0.005 |
|       1 | 28052.000 |       0.081 |        0.109 |      0.362 |            0.008 |          -0.002 |
|       2 | 28052.000 |       0.111 |        0.145 |      0.397 |            0.009 |          -0.010 |
|       3 | 28051.000 |       0.142 |        0.179 |      0.431 |            0.009 |          -0.020 |
|       4 | 28052.000 |       0.175 |        0.215 |      0.459 |            0.011 |          -0.031 |
|       5 | 28052.000 |       0.210 |        0.257 |      0.473 |            0.015 |          -0.040 |
|       6 | 28051.000 |       0.248 |        0.291 |      0.494 |            0.017 |          -0.069 |
|       7 | 28052.000 |       0.290 |        0.323 |      0.514 |            0.019 |          -0.102 |
|       8 | 28053.000 |       0.342 |        0.348 |      0.532 |            0.020 |          -0.102 |
|       9 | 28051.000 |       0.453 |        0.374 |      0.535 |            0.024 |          -0.102 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 280518.000 |        0.230 |      0.454 |            0.013 |
| top 10%    |  28053.000 |        0.374 |      0.535 |            0.024 |
| top 5%     |  14026.000 |        0.389 |      0.529 |            0.027 |
| top 2%     |   5611.000 |        0.406 |      0.522 |            0.031 |
| top 1%     |   2806.000 |        0.428 |      0.516 |            0.037 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91950.000 |        0.179 |      0.389 |            0.015 |
| top 10%    |  4337.000 |        0.388 |      0.474 |            0.036 |
| top 5%     |  2220.000 |        0.404 |      0.471 |            0.039 |
| top 2%     |   953.000 |        0.426 |      0.465 |            0.044 |
| top 1%     |   501.000 |        0.457 |      0.465 |            0.052 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 17153.000 |       0.045 |        0.056 |      0.309 |            0.005 |           0.003 |
|       1 | 14427.000 |       0.080 |        0.109 |      0.332 |            0.013 |           0.008 |
|       2 | 12303.000 |       0.111 |        0.138 |      0.371 |            0.013 |          -0.000 |
|       3 | 10577.000 |       0.142 |        0.171 |      0.403 |            0.013 |          -0.006 |
|       4 |  9067.000 |       0.175 |        0.201 |      0.425 |            0.015 |          -0.011 |
|       5 |  7677.000 |       0.210 |        0.240 |      0.435 |            0.020 |          -0.007 |
|       6 |  6396.000 |       0.248 |        0.277 |      0.445 |            0.023 |          -0.010 |
|       7 |  5331.000 |       0.290 |        0.313 |      0.458 |            0.027 |          -0.014 |
|       8 |  4684.000 |       0.341 |        0.338 |      0.485 |            0.026 |          -0.043 |
|       9 |  4335.000 |       0.457 |        0.388 |      0.475 |            0.036 |          -0.018 |

Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that survived. See the SURVIVORSHIP and CHECK rows in section 9.

Setup signals split by the model's score (OOS, exit bracket_20_10; last column sma50_close):

| super_prob   |          n |   avgR |   win |   avgR_sma50 |
|:-------------|-----------:|-------:|------:|-------------:|
| low          | 136078.000 |  0.005 | 0.480 |       -0.083 |
| mid          | 136078.000 |  0.065 | 0.454 |       -0.061 |
| high         | 136078.000 |  0.146 | 0.425 |        0.164 |

## 12. Short horizons: green day / next day / 3 days / week (out-of-sample 2018+)

Features: candle anatomy, gaps and fair value gaps, relative volume, round numbers / moving averages / swing support & resistance / 20-day trend line, completed-week structure, VIX (level, change, percentile, VIX/VIX3M), plus everything the earlier models use. Market-only = market + VIX + calendar features only. Retrained every 2 years. 'top/bottom' = actual up-rate in the model's highest/lowest 10%; spread = their difference in average return over the horizon.

| target                         | model   |   base rate |   AUC |   accuracy |   top 10% up |   bottom 10% up |   return spread |
|:-------------------------------|:--------|------------:|------:|-----------:|-------------:|----------------:|----------------:|
| next day green (close > open)  | all     |       0.493 | 0.514 |      0.509 |        0.516 |           0.460 |           0.007 |
| next day green (close > open)  | market  |       0.493 | 0.516 |      0.511 |        0.491 |           0.504 |           0.004 |
| up next day (close to close)   | all     |       0.500 | 0.514 |      0.512 |        0.515 |           0.482 |           0.003 |
| up next day (close to close)   | market  |       0.500 | 0.517 |      0.512 |        0.517 |           0.443 |           0.005 |
| up over the next 3 days        | all     |       0.509 | 0.520 |      0.518 |        0.532 |           0.451 |           0.006 |
| up over the next 3 days        | market  |       0.509 | 0.521 |      0.516 |        0.521 |           0.445 |           0.006 |
| up over the next week (5 days) | all     |       0.514 | 0.508 |      0.513 |        0.510 |           0.549 |          -0.008 |
| up over the next week (5 days) | market  |       0.514 | 0.508 |      0.517 |        0.502 |           0.512 |          -0.008 |

Up over the next week, by decile of the full model:

|   s_up5 |          n |   predicted |   actual_up |   avg_return |
|--------:|-----------:|------------:|------------:|-------------:|
|       0 | 28831.0000 |      0.3482 |      0.5491 |       0.0047 |
|       1 | 28830.0000 |      0.4324 |      0.4805 |      -0.0019 |
|       2 | 28830.0000 |      0.4692 |      0.4717 |      -0.0020 |
|       3 | 28830.0000 |      0.4960 |      0.5019 |       0.0002 |
|       4 | 28831.0000 |      0.5197 |      0.5157 |       0.0013 |
|       5 | 28830.0000 |      0.5425 |      0.5155 |       0.0015 |
|       6 | 28830.0000 |      0.5670 |      0.5276 |       0.0026 |
|       7 | 28830.0000 |      0.5952 |      0.5313 |       0.0033 |
|       8 | 28830.0000 |      0.6320 |      0.5359 |       0.0029 |
|       9 | 28831.0000 |      0.7083 |      0.5096 |      -0.0033 |

What drives the 1-week prediction (permutation importance, drop in OOS AUC):

| feature          |   auc_drop |
|:-----------------|-----------:|
| spy_ret_1        |     0.0131 |
| breadth_50       |     0.0067 |
| vix_chg_1        |     0.0048 |
| month            |     0.0036 |
| vix_chg_5        |     0.0025 |
| vix_term         |     0.0023 |
| wk_ret_1         |     0.0013 |
| days_since_pivot |     0.0010 |
| dist_sma50       |     0.0009 |
| mkt_above200     |     0.0007 |
| rs_rank          |     0.0007 |
| spy_ret_5        |     0.0006 |
| trend_slope_20   |     0.0006 |
| rates_rising     |     0.0005 |
| dist_support     |     0.0004 |

Do the new features improve the +20%/-10% goal model? (OOS tiers)

**original**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 280518.000 |        0.230 |      0.454 |            0.013 |
| top 10%    |  28053.000 |        0.374 |      0.535 |            0.024 |
| top 5%     |  14026.000 |        0.389 |      0.529 |            0.027 |
| top 2%     |   5611.000 |        0.406 |      0.522 |            0.031 |
| top 1%     |   2806.000 |        0.428 |      0.516 |            0.037 |

**with new features**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 280518.000 |        0.230 |      0.454 |            0.013 |
| top 10%    |  28052.000 |        0.383 |      0.533 |            0.026 |
| top 5%     |  14026.000 |        0.397 |      0.526 |            0.029 |
| top 2%     |   5611.000 |        0.416 |      0.514 |            0.034 |
| top 1%     |   2806.000 |        0.442 |      0.494 |            0.042 |

## 14. Your Stock Selection Workflow PDF, price-testable rules (run 20)

Rules as written, nothing tuned. Rockets: 6-week base -> new 52w high on 1.5x volume (<= 5% above the pivot, stop -8%) or a >= 5% gap on 2x volume holding its low for 2 days (no earnings dates: volume is the proxy); price >= $10, >= $20M/day, top 20% 6-month return; exit = sell 1/3 at +25%, stop to entry, trail the 50 SMA. Scanner: above a rising 200d, 50d > 200d, within 15% of the 52w high; entry = pullback to the 21 EMA / 50 SMA then a close above the prior high, a 4-week base breakout, or a holding gap; stop under the pullback/base low, skipped if > 10%; ranked by RS (40) + stop distance (30); exit = weekly close below the 10-week MA. Regime (QQQ): green full size, yellow half, red no new entries. Sizing: rockets 0.5% risk x 3 positions, scanner 0.6% x 4, max 10% per stock. Not testable here: fundamentals (guidance, revenue, FCF, estimates), the Singapore part, the Nasdaq-100 membership itself.

Per trade vs random entries with the same filter and exit (R multiples):

| entry              | filter          | exit          |   IS_n |   IS_avgR |   IS_win |   OOS_n |   OOS_avgR |   OOS_win |   OOS_t |
|:-------------------|:----------------|:--------------|-------:|----------:|---------:|--------:|-----------:|----------:|--------:|
| wf_rocket_gap      | wf_rocket       | bracket_20_10 |    672 |     0.078 |    0.449 |    1226 |      0.131 |     0.432 |   3.318 |
| wf_rocket_breakout | wf_rocket       | bracket_20_10 |    454 |     0.095 |    0.465 |     789 |      0.092 |     0.451 |   1.992 |
| random_uptrend     | wf_rocket       | bracket_20_10 |   5517 |     0.144 |    0.497 |    8590 |      0.085 |     0.437 |   6.021 |
| wf_rocket_gap      | wf_rocket       | sma50_close   |    678 |     0.057 |    0.308 |    1226 |      0.236 |     0.308 |   2.245 |
| wf_rocket_breakout | wf_rocket       | sma50_close   |    455 |     0.064 |    0.382 |     789 |      0.158 |     0.341 |   2.188 |
| random_uptrend     | wf_rocket       | sma50_close   |   5608 |    -0.147 |    0.139 |    8590 |     -0.062 |     0.136 |  -1.252 |
| wf_rocket_gap      | wf_rocket       | wf_rocket     |    678 |     0.056 |    0.311 |    1226 |      0.199 |     0.314 |   2.404 |
| wf_rocket_breakout | wf_rocket       | wf_rocket     |    455 |     0.074 |    0.389 |     789 |      0.129 |     0.349 |   2.031 |
| random_uptrend     | wf_rocket       | wf_rocket     |   5608 |    -0.140 |    0.140 |    8590 |     -0.062 |     0.140 |  -1.399 |
| wf_rocket_gap      | wf_rocket       | wf_weekly10   |    676 |     0.021 |    0.290 |    1226 |      0.174 |     0.287 |   2.116 |
| wf_rocket_breakout | wf_rocket       | wf_weekly10   |    454 |     0.067 |    0.377 |     789 |      0.125 |     0.337 |   1.802 |
| random_uptrend     | wf_rocket       | wf_weekly10   |   5607 |    -0.152 |    0.130 |    8590 |     -0.035 |     0.130 |  -0.667 |
| wf_rocket_gap      | wf_rocket_green | bracket_20_10 |    519 |     0.122 |    0.466 |    1022 |      0.190 |     0.452 |   4.349 |
| wf_rocket_breakout | wf_rocket_green | bracket_20_10 |    349 |     0.186 |    0.490 |     629 |      0.131 |     0.466 |   2.474 |
| random_uptrend     | wf_rocket_green | bracket_20_10 |   4388 |     0.138 |    0.491 |    6966 |      0.112 |     0.441 |   7.043 |
| wf_rocket_gap      | wf_rocket_green | sma50_close   |    525 |     0.147 |    0.330 |    1022 |      0.289 |     0.312 |   2.349 |
| wf_rocket_breakout | wf_rocket_green | sma50_close   |    350 |     0.144 |    0.409 |     629 |      0.201 |     0.347 |   2.416 |
| random_uptrend     | wf_rocket_green | sma50_close   |   4479 |    -0.175 |    0.135 |    6966 |     -0.061 |     0.135 |  -1.092 |
| wf_rocket_gap      | wf_rocket_green | wf_rocket     |    525 |     0.148 |    0.333 |    1022 |      0.241 |     0.320 |   2.530 |
| wf_rocket_breakout | wf_rocket_green | wf_rocket     |    350 |     0.164 |    0.417 |     629 |      0.169 |     0.353 |   2.307 |
| random_uptrend     | wf_rocket_green | wf_rocket     |   4479 |    -0.168 |    0.135 |    6966 |     -0.058 |     0.139 |  -1.155 |
| wf_rocket_gap      | wf_rocket_green | wf_weekly10   |    523 |     0.103 |    0.312 |    1022 |      0.220 |     0.295 |   2.339 |
| wf_rocket_breakout | wf_rocket_green | wf_weekly10   |    349 |     0.119 |    0.395 |     629 |      0.163 |     0.340 |   2.022 |
| random_uptrend     | wf_rocket_green | wf_weekly10   |   4478 |    -0.188 |    0.126 |    6966 |     -0.036 |     0.129 |  -0.626 |
| wf_rocket_gap      | wf_scan         | bracket_20_10 |   1393 |     0.210 |    0.504 |    1601 |      0.105 |     0.444 |   3.221 |
| random_uptrend     | wf_scan         | bracket_20_10 |  21673 |     0.197 |    0.547 |   22052 |      0.091 |     0.463 |  11.140 |
| wf_scan_pullback   | wf_scan         | bracket_20_10 |  69655 |     0.183 |    0.545 |   66903 |      0.087 |     0.467 |  18.845 |
| wf_scan_base       | wf_scan         | bracket_20_10 |  24900 |     0.199 |    0.582 |   17385 |      0.038 |     0.482 |   4.699 |
| wf_rocket_gap      | wf_scan         | sma50_close   |   1403 |     0.232 |    0.313 |    1601 |      0.101 |     0.292 |   1.230 |
| wf_scan_pullback   | wf_scan         | sma50_close   |  70451 |     0.058 |    0.284 |   66903 |     -0.001 |     0.269 |  -0.154 |
| wf_scan_base       | wf_scan         | sma50_close   |  25076 |     0.075 |    0.341 |   17385 |     -0.007 |     0.304 |  -0.850 |
| random_uptrend     | wf_scan         | sma50_close   |  22133 |    -0.049 |    0.146 |   22052 |     -0.109 |     0.135 |  -3.710 |
| wf_rocket_gap      | wf_scan         | wf_rocket     |   1403 |     0.220 |    0.316 |    1601 |      0.092 |     0.299 |   1.374 |
| wf_scan_pullback   | wf_scan         | wf_rocket     |  70451 |     0.058 |    0.284 |   66903 |     -0.001 |     0.270 |  -0.138 |
| wf_scan_base       | wf_scan         | wf_rocket     |  25076 |     0.075 |    0.341 |   17385 |     -0.006 |     0.305 |  -0.747 |
| random_uptrend     | wf_scan         | wf_rocket     |  22133 |    -0.047 |    0.147 |   22052 |     -0.104 |     0.137 |  -3.765 |
| wf_rocket_gap      | wf_scan         | wf_weekly10   |   1402 |     0.207 |    0.305 |    1601 |      0.051 |     0.278 |   0.776 |
| wf_scan_pullback   | wf_scan         | wf_weekly10   |  70286 |     0.088 |    0.294 |   66903 |      0.006 |     0.276 |   0.693 |
| wf_scan_base       | wf_scan         | wf_weekly10   |  24962 |     0.098 |    0.368 |   17385 |     -0.011 |     0.322 |  -1.099 |
| random_uptrend     | wf_scan         | wf_weekly10   |  22120 |    -0.028 |    0.139 |   22052 |     -0.071 |     0.129 |  -2.151 |
| wf_rocket_gap      | wf_scan_green   | bracket_20_10 |   1217 |     0.228 |    0.510 |    1458 |      0.132 |     0.454 |   3.845 |
| random_uptrend     | wf_scan_green   | bracket_20_10 |  19169 |     0.183 |    0.541 |   19506 |      0.115 |     0.471 |  13.147 |
| wf_scan_pullback   | wf_scan_green   | bracket_20_10 |  60848 |     0.169 |    0.538 |   58101 |      0.115 |     0.477 |  23.056 |
| wf_scan_base       | wf_scan_green   | bracket_20_10 |  22356 |     0.173 |    0.569 |   15760 |      0.045 |     0.482 |   5.296 |
| wf_rocket_gap      | wf_scan_green   | sma50_close   |   1227 |     0.256 |    0.320 |    1458 |      0.121 |     0.295 |   1.359 |
| wf_scan_pullback   | wf_scan_green   | sma50_close   |  61644 |     0.020 |    0.278 |   58101 |      0.021 |     0.272 |   2.240 |
| wf_scan_base       | wf_scan_green   | sma50_close   |  22532 |     0.038 |    0.328 |   15760 |      0.005 |     0.307 |   0.512 |
| random_uptrend     | wf_scan_green   | sma50_close   |  19629 |    -0.104 |    0.144 |   19506 |     -0.097 |     0.136 |  -3.131 |
| wf_rocket_gap      | wf_scan_green   | wf_rocket     |   1227 |     0.243 |    0.324 |    1458 |      0.108 |     0.301 |   1.502 |
| wf_scan_pullback   | wf_scan_green   | wf_rocket     |  61644 |     0.020 |    0.278 |   58101 |      0.022 |     0.273 |   2.554 |
| wf_scan_base       | wf_scan_green   | wf_rocket     |  22532 |     0.039 |    0.328 |   15760 |      0.006 |     0.308 |   0.666 |
| random_uptrend     | wf_scan_green   | wf_rocket     |  19629 |    -0.100 |    0.144 |   19506 |     -0.089 |     0.137 |  -3.052 |
| wf_rocket_gap      | wf_scan_green   | wf_weekly10   |   1226 |     0.228 |    0.316 |    1458 |      0.064 |     0.283 |   0.918 |
| wf_scan_pullback   | wf_scan_green   | wf_weekly10   |  61479 |     0.036 |    0.287 |   58101 |      0.027 |     0.280 |   2.847 |
| wf_scan_base       | wf_scan_green   | wf_weekly10   |  22418 |     0.052 |    0.354 |   15760 |     -0.004 |     0.324 |  -0.339 |
| random_uptrend     | wf_scan_green   | wf_weekly10   |  19616 |    -0.086 |    0.135 |   19506 |     -0.061 |     0.129 |  -1.744 |

Per trade by Nasdaq-100 regime at entry (the PDF's own exits):

| part                    | regime           |      IS_n |   IS_avgR |   IS_win |     OOS_n |   OOS_avgR |   OOS_win |
|:------------------------|:-----------------|----------:|----------:|---------:|----------:|-----------:|----------:|
| rockets                 | PDF red          |   153.000 |    -0.262 |    0.281 |   256.000 |     -0.013 |     0.328 |
| rockets                 | PDF yellow       |   105.000 |    -0.222 |    0.229 |   108.000 |     -0.041 |     0.250 |
| rockets                 | PDF green (200d) |   901.000 |     0.192 |    0.378 |  1651.000 |      0.214 |     0.333 |
| rockets                 | QQQ < both       |   191.000 |     0.186 |    0.382 |   297.000 |      0.053 |     0.306 |
| rockets                 | QQQ > 50 only    |   107.000 |     0.095 |    0.299 |   171.000 |      0.256 |     0.322 |
| rockets                 | QQQ > 21 only    |    69.000 |    -0.096 |    0.391 |    96.000 |      0.182 |     0.323 |
| rockets                 | QQQ > 21 & 50    |   792.000 |     0.089 |    0.348 |  1451.000 |      0.185 |     0.333 |
| scanner                 | PDF red          |  6903.000 |     0.459 |    0.383 |  7596.000 |     -0.198 |     0.251 |
| scanner                 | PDF yellow       |  4624.000 |     0.459 |    0.361 |  2974.000 |      0.062 |     0.278 |
| scanner                 | PDF green (200d) | 87345.000 |     0.118 |    0.316 | 75319.000 |      0.022 |     0.289 |
| scanner                 | QQQ < both       | 14169.000 |     0.279 |    0.363 | 14749.000 |      0.048 |     0.306 |
| scanner                 | QQQ > 50 only    | 11292.000 |     0.168 |    0.306 |  8688.000 |     -0.064 |     0.272 |
| scanner                 | QQQ > 21 only    |  5096.000 |     0.361 |    0.403 |  3948.000 |      0.099 |     0.336 |
| scanner                 | QQQ > 21 & 50    | 68315.000 |     0.116 |    0.312 | 58504.000 |     -0.004 |     0.279 |
| random (rocket filter)  | PDF red          |   702.000 |     0.276 |    0.192 |  1193.000 |     -0.304 |     0.137 |
| random (rocket filter)  | PDF yellow       |   427.000 |    -0.529 |    0.101 |   431.000 |      0.532 |     0.174 |
| random (rocket filter)  | PDF green (200d) |  4546.000 |     0.006 |    0.144 |  6966.000 |     -0.058 |     0.139 |
| random (rocket filter)  | QQQ < both       |   978.000 |     0.383 |    0.182 |  1687.000 |     -0.267 |     0.141 |
| random (rocket filter)  | QQQ > 50 only    |   673.000 |     0.155 |    0.156 |   829.000 |     -0.101 |     0.148 |
| random (rocket filter)  | QQQ > 21 only    |   287.000 |     0.249 |    0.216 |   375.000 |      0.321 |     0.173 |
| random (rocket filter)  | QQQ > 21 & 50    |  3737.000 |    -0.148 |    0.131 |  5699.000 |     -0.022 |     0.137 |
| random (scanner filter) | PDF red          |  1431.000 |     0.523 |    0.173 |  1753.000 |     -0.371 |     0.120 |
| random (scanner filter) | PDF yellow       |  1073.000 |     0.305 |    0.156 |   793.000 |      0.344 |     0.140 |
| random (scanner filter) | PDF green (200d) | 19886.000 |     0.055 |    0.142 | 19506.000 |     -0.061 |     0.129 |
| random (scanner filter) | QQQ < both       |  3133.000 |     0.458 |    0.181 |  3829.000 |     -0.295 |     0.130 |
| random (scanner filter) | QQQ > 50 only    |  2634.000 |     0.246 |    0.147 |  2208.000 |     -0.080 |     0.132 |
| random (scanner filter) | QQQ > 21 only    |   899.000 |     0.442 |    0.202 |   821.000 |      0.208 |     0.152 |
| random (scanner filter) | QQQ > 21 & 50    | 15724.000 |    -0.020 |    0.134 | 15194.000 |     -0.029 |     0.127 |

Portfolios 2018+ (marked to market daily):

| strategy                                                            |   CAGR |   max_DD |   trades |   win |   avg_positions |
|:--------------------------------------------------------------------|-------:|---------:|---------:|------:|----------------:|
| rockets as written (regime sizing) / wf_rocket                      |  0.017 |   -0.098 |      189 | 0.323 |           2.347 |
| rockets, no regime rule / wf_rocket                                 |  0.014 |   -0.098 |      233 | 0.322 |           2.725 |
| rockets, QQQ 21/50 regime / wf_rocket                               |  0.002 |   -0.123 |      203 | 0.300 |           2.404 |
| rockets / sma50_close                                               |  0.019 |   -0.088 |      188 | 0.319 |           2.348 |
| rockets / bracket_20_10                                             |  0.027 |   -0.088 |      175 | 0.434 |           2.409 |
| BASELINE random entries, rocket filter + regime / wf_rocket         |  0.003 |   -0.256 |      478 | 0.165 |           2.465 |
| rockets as written, S&P 500 point-in-time only / wf_rocket          | -0.002 |   -0.079 |      147 | 0.272 |           1.899 |
| scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10 |  0.010 |   -0.173 |      349 | 0.281 |           3.440 |
| scanner PIT, no regime rule / wf_weekly10                           |  0.001 |   -0.177 |      409 | 0.296 |           3.930 |
| scanner PIT, QQQ 21/50 regime / wf_weekly10                         | -0.016 |   -0.223 |      372 | 0.274 |           3.482 |
| scanner PIT / sma50_close                                           |  0.013 |   -0.172 |      374 | 0.291 |           3.388 |
| BASELINE random entries, scanner filter + regime, PIT / wf_weekly10 |  0.026 |   -0.166 |      539 | 0.148 |           3.299 |
| scanner as written, full universe / wf_weekly10                     |  0.003 |   -0.226 |      379 | 0.248 |           3.404 |

The PDF's full split (Singapore part as cash; scanner and rockets point-in-time):

| portfolio (2018+, daily rebalanced)                       |   CAGR |   max_DD |   worst_year |
|:----------------------------------------------------------|-------:|---------:|-------------:|
| PDF split: 40% SPY / 25% scanner / 15% rockets / 20% cash |  0.063 |   -0.167 |       -0.085 |
| trading parts only, 25:15                                 |  0.006 |   -0.121 |       -0.056 |
| SPY 100%                                                  |  0.146 |   -0.337 |       -0.182 |

## 13. Bracket menu and market regime for the +20/-10 model's picks (runs 17-18)

Every stock every 10 days, entry at the close, 63-day limit, 0.1% costs per side. Stocks ranked by the +20/-10 goal model (walk-forward, so pre-2018 scores are also out-of-sample for their year). Top 10% = top 10% of scores within each year. Brackets are chosen on IS (walk-forward years before 2018) and judged on 2018+. IS choice: best return per month = m20_15, best return per trade = m30_15.

Model top 10%: hit rate, net return per trade, return per month held, days held (IS vs OOS):

| bracket     |   breakeven_hit |   hit_IS |   hit_OOS |   ret_IS |   ret_OOS |   per_month_IS |   per_month_OOS |   days_IS |   days_OOS |
|:------------|----------------:|---------:|----------:|---------:|----------:|---------------:|----------------:|----------:|-----------:|
| +5% / -5%   |           0.500 |    0.520 |     0.554 |    0.000 |     0.004 |          0.001 |           0.019 |     5.328 |      4.364 |
| +5% / -8%   |           0.615 |    0.636 |     0.669 |    0.001 |     0.006 |          0.004 |           0.020 |     7.667 |      6.210 |
| +5% / -10%  |           0.667 |    0.684 |     0.724 |    0.002 |     0.008 |          0.004 |           0.023 |     9.072 |      7.392 |
| +5% / -15%  |           0.750 |    0.762 |     0.810 |    0.003 |     0.013 |          0.006 |           0.027 |    12.246 |      9.966 |
| +10% / -5%  |           0.333 |    0.375 |     0.394 |    0.004 |     0.007 |          0.010 |           0.019 |     9.472 |      7.893 |
| +10% / -8%  |           0.444 |    0.485 |     0.513 |    0.007 |     0.011 |          0.011 |           0.021 |    13.762 |     11.402 |
| +10% / -10% |           0.500 |    0.535 |     0.574 |    0.008 |     0.015 |          0.011 |           0.023 |    16.212 |     13.654 |
| +10% / -15% |           0.600 |    0.613 |     0.675 |    0.011 |     0.023 |          0.011 |           0.026 |    21.503 |     18.410 |
| +15% / -5%  |           0.250 |    0.289 |     0.308 |    0.007 |     0.010 |          0.012 |           0.019 |    13.203 |     11.116 |
| +15% / -8%  |           0.348 |    0.379 |     0.415 |    0.011 |     0.016 |          0.012 |           0.021 |    19.028 |     16.048 |
| +15% / -10% |           0.400 |    0.419 |     0.469 |    0.013 |     0.021 |          0.012 |           0.023 |    22.293 |     19.183 |
| +15% / -15% |           0.500 |    0.483 |     0.560 |    0.017 |     0.032 |          0.012 |           0.027 |    28.934 |     25.488 |
| +20% / -5%  |           0.200 |    0.225 |     0.250 |    0.010 |     0.013 |          0.013 |           0.020 |    16.176 |     13.830 |
| +20% / -8%  |           0.286 |    0.294 |     0.339 |    0.014 |     0.021 |          0.013 |           0.022 |    22.997 |     19.900 |
| +20% / -10% |           0.333 |    0.324 |     0.383 |    0.016 |     0.026 |          0.012 |           0.023 |    26.779 |     23.623 |
| +20% / -15% |           0.429 |    0.374 |     0.459 |    0.021 |     0.040 |          0.013 |           0.027 |    34.236 |     31.002 |
| +30% / -5%  |           0.143 |    0.127 |     0.165 |    0.012 |     0.018 |          0.012 |           0.021 |    20.229 |     17.803 |
| +30% / -8%  |           0.211 |    0.163 |     0.221 |    0.017 |     0.027 |          0.012 |           0.022 |    28.272 |     25.276 |
| +30% / -10% |           0.250 |    0.178 |     0.249 |    0.018 |     0.034 |          0.012 |           0.024 |    32.594 |     29.696 |
| +30% / -15% |           0.333 |    0.203 |     0.295 |    0.024 |     0.049 |          0.012 |           0.027 |    40.890 |     38.257 |

OOS hit rate by tier (all stocks = no model):

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |        0.526 |     0.554 |    0.566 |
| +5% / -8%   |        0.640 |     0.669 |    0.678 |
| +5% / -10%  |        0.686 |     0.724 |    0.728 |
| +5% / -15%  |        0.745 |     0.810 |    0.823 |
| +10% / -5%  |        0.351 |     0.394 |    0.411 |
| +10% / -8%  |        0.446 |     0.513 |    0.531 |
| +10% / -10% |        0.487 |     0.574 |    0.587 |
| +10% / -15% |        0.538 |     0.675 |    0.702 |
| +15% / -5%  |        0.240 |     0.308 |    0.329 |
| +15% / -8%  |        0.309 |     0.415 |    0.440 |
| +15% / -10% |        0.337 |     0.469 |    0.491 |
| +15% / -15% |        0.376 |     0.560 |    0.597 |
| +20% / -5%  |        0.162 |     0.250 |    0.277 |
| +20% / -8%  |        0.210 |     0.339 |    0.374 |
| +20% / -10% |        0.230 |     0.383 |    0.418 |
| +20% / -15% |        0.258 |     0.459 |    0.510 |
| +30% / -5%  |        0.075 |     0.165 |    0.197 |
| +30% / -8%  |        0.098 |     0.221 |    0.263 |
| +30% / -10% |        0.109 |     0.249 |    0.293 |
| +30% / -15% |        0.123 |     0.295 |    0.352 |

OOS net return per trade by tier:

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |       0.0008 |    0.0040 |   0.0051 |
| +5% / -8%   |       0.0029 |    0.0060 |   0.0073 |
| +5% / -10%  |       0.0044 |    0.0080 |   0.0088 |
| +5% / -15%  |       0.0068 |    0.0127 |   0.0153 |
| +10% / -5%  |       0.0030 |    0.0071 |   0.0098 |
| +10% / -8%  |       0.0063 |    0.0112 |   0.0149 |
| +10% / -10% |       0.0084 |    0.0148 |   0.0175 |
| +10% / -15% |       0.0123 |    0.0232 |   0.0288 |
| +15% / -5%  |       0.0046 |    0.0101 |   0.0142 |
| +15% / -8%  |       0.0088 |    0.0163 |   0.0221 |
| +15% / -10% |       0.0113 |    0.0210 |   0.0253 |
| +15% / -15% |       0.0160 |    0.0323 |   0.0399 |
| +20% / -5%  |       0.0057 |    0.0130 |   0.0184 |
| +20% / -8%  |       0.0104 |    0.0208 |   0.0282 |
| +20% / -10% |       0.0132 |    0.0263 |   0.0322 |
| +20% / -15% |       0.0183 |    0.0398 |   0.0500 |
| +30% / -5%  |       0.0067 |    0.0177 |   0.0258 |
| +30% / -8%  |       0.0120 |    0.0270 |   0.0372 |
| +30% / -10% |       0.0151 |    0.0337 |   0.0423 |
| +30% / -15% |       0.0208 |    0.0491 |   0.0621 |

Portfolio 2018+ (top 10% model, 1% risk per trade = position size 1%/stop, max 10 positions, 20% cap):

| bracket     |   CAGR |   max_DD |   trades |   win |
|:------------|-------:|---------:|---------:|------:|
| +5% / -5%   | -0.031 |   -0.666 | 2813.000 | 0.510 |
| +5% / -8%   |  0.070 |   -0.565 | 3087.000 | 0.638 |
| +5% / -10%  |  0.159 |   -0.487 | 3099.000 | 0.699 |
| +5% / -15%  |  0.098 |   -0.427 | 2353.000 | 0.775 |
| +10% / -5%  |  0.052 |   -0.631 | 1937.000 | 0.358 |
| +10% / -8%  |  0.136 |   -0.498 | 2087.000 | 0.484 |
| +10% / -10% |  0.222 |   -0.529 | 1933.000 | 0.557 |
| +10% / -15% |  0.128 |   -0.404 | 1470.000 | 0.642 |
| +15% / -5%  |  0.142 |   -0.649 | 1544.000 | 0.294 |
| +15% / -8%  |  0.189 |   -0.501 | 1599.000 | 0.409 |
| +15% / -10% |  0.171 |   -0.494 | 1429.000 | 0.456 |
| +15% / -15% |  0.135 |   -0.463 | 1096.000 | 0.556 |
| +20% / -5%  |  0.225 |   -0.545 | 1334.000 | 0.255 |
| +20% / -8%  |  0.224 |   -0.487 | 1330.000 | 0.350 |
| +20% / -10% |  0.253 |   -0.447 | 1189.000 | 0.421 |
| +20% / -15% |  0.196 |   -0.363 |  893.000 | 0.518 |
| +30% / -5%  |  0.226 |   -0.638 | 1069.000 | 0.222 |
| +30% / -8%  |  0.234 |   -0.510 | 1018.000 | 0.314 |
| +30% / -10% |  0.220 |   -0.467 |  910.000 | 0.353 |
| +30% / -15% |  0.197 |   -0.335 |  690.000 | 0.459 |

Model top 10%, +20/-10, by market regime at entry (breadth terciles and the 3-day market model cut use IS data):

| regime                               | bucket             |      IS_n |   IS_hit_target |   IS_avg_net_return |     OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:-------------------------------------|:-------------------|----------:|----------------:|--------------------:|----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)           | high (> 71%)       |  7011.000 |           0.327 |               0.024 |  5531.000 |            0.398 |                0.031 |
| breadth (stocks above 50d)           | low (< 53%)        |  6930.000 |           0.351 |               0.019 | 14349.000 |            0.368 |                0.023 |
| breadth (stocks above 50d)           | mid                |  6934.000 |           0.293 |               0.004 |  8175.000 |            0.402 |                0.030 |
| VIX level                            | 15-20              |  6610.000 |           0.279 |               0.001 |  9426.000 |            0.344 |                0.013 |
| VIX level                            | 20-30              |  4250.000 |           0.437 |               0.044 | 12342.000 |            0.428 |                0.043 |
| VIX level                            | < 15               |  7593.000 |           0.296 |               0.015 |  5214.000 |            0.320 |                0.002 |
| VIX level                            | > 30               |  2422.000 |           0.335 |               0.009 |  1073.000 |            0.536 |                0.069 |
| VIX / VIX3M                          | 0.9-1.0            |  6617.000 |           0.367 |               0.030 | 11802.000 |            0.374 |                0.026 |
| VIX / VIX3M                          | < 0.9 (calm)       | 11491.000 |           0.299 |               0.010 | 13526.000 |            0.394 |                0.026 |
| VIX / VIX3M                          | > 1.0 (stress)     |  2767.000 |           0.322 |               0.003 |  2727.000 |            0.376 |                0.027 |
| SPY above 200d                       | no                 |  5876.000 |           0.352 |               0.016 |  6175.000 |            0.413 |                0.037 |
| SPY above 200d                       | yes                | 14999.000 |           0.313 |               0.016 | 21880.000 |            0.376 |                0.023 |
| QQQ above 10 & 20 SMA                | no                 |  9230.000 |           0.346 |               0.021 | 15391.000 |            0.373 |                0.025 |
| QQQ above 10 & 20 SMA                | yes                | 11645.000 |           0.306 |               0.012 | 12664.000 |            0.397 |                0.028 |
| SPY 1-month return                   | -3..0%             |  3540.000 |           0.274 |              -0.002 |  5226.000 |            0.352 |                0.020 |
| SPY 1-month return                   | 0..3%              |  6844.000 |           0.334 |               0.023 |  7708.000 |            0.388 |                0.024 |
| SPY 1-month return                   | < -3%              |  3839.000 |           0.390 |               0.028 |  7549.000 |            0.367 |                0.024 |
| SPY 1-month return                   | > 3%               |  6652.000 |           0.301 |               0.011 |  7572.000 |            0.419 |                0.036 |
| SPY vs 21/50 SMA                     | above 21 & 50      | 12471.000 |           0.313 |               0.013 | 13439.000 |            0.387 |                0.024 |
| SPY vs 21/50 SMA                     | above 21 only      |   519.000 |           0.347 |               0.024 |  1781.000 |            0.403 |                0.034 |
| SPY vs 21/50 SMA                     | above 50 only      |  2419.000 |           0.231 |              -0.004 |  2923.000 |            0.360 |                0.021 |
| SPY vs 21/50 SMA                     | below both         |  5466.000 |           0.387 |               0.029 |  9912.000 |            0.383 |                0.030 |
| QQQ vs 21/50 SMA                     | above 21 & 50      | 12426.000 |           0.288 |               0.006 | 13117.000 |            0.384 |                0.024 |
| QQQ vs 21/50 SMA                     | above 21 only      |   870.000 |           0.385 |               0.034 |  1392.000 |            0.394 |                0.026 |
| QQQ vs 21/50 SMA                     | above 50 only      |  1907.000 |           0.341 |               0.026 |  3545.000 |            0.368 |                0.021 |
| QQQ vs 21/50 SMA                     | below both         |  5672.000 |           0.387 |               0.030 | 10001.000 |            0.388 |                0.031 |
| A/D line vs its 21/50 MA             | above 21 & 50      | 12709.000 |           0.292 |               0.008 | 12961.000 |            0.400 |                0.030 |
| A/D line vs its 21/50 MA             | above 21 only      |   871.000 |           0.413 |               0.032 |  1298.000 |            0.320 |                0.005 |
| A/D line vs its 21/50 MA             | above 50 only      |  2673.000 |           0.305 |               0.017 |  4338.000 |            0.365 |                0.024 |
| A/D line vs its 21/50 MA             | below both         |  4622.000 |           0.404 |               0.034 |  9458.000 |            0.380 |                0.025 |
| % of stocks above 20d                | 40-60%             |  5076.000 |           0.314 |               0.012 |  6022.000 |            0.342 |                0.011 |
| % of stocks above 20d                | < 40%              |  5286.000 |           0.348 |               0.019 | 11468.000 |            0.378 |                0.026 |
| % of stocks above 20d                | > 60%              | 10513.000 |           0.316 |               0.016 | 10565.000 |            0.415 |                0.035 |
| % above 50d, 10-day change           | falling (< -5 pts) |  8402.000 |           0.346 |               0.024 | 13323.000 |            0.385 |                0.029 |
| % above 50d, 10-day change           | flat               |  4433.000 |           0.270 |              -0.003 |  7154.000 |            0.363 |                0.018 |
| % above 50d, 10-day change           | rising (> +5 pts)  |  8040.000 |           0.330 |               0.017 |  7578.000 |            0.401 |                0.030 |
| A/D line, 10-day change              | flat               |  5576.000 |           0.280 |              -0.001 |  7267.000 |            0.389 |                0.028 |
| A/D line, 10-day change              | falling            |  5957.000 |           0.382 |               0.034 | 10862.000 |            0.385 |                0.029 |
| A/D line, 10-day change              | rising             |  9342.000 |           0.312 |               0.014 |  9926.000 |            0.379 |                0.023 |
| sector & sub-industry today green    | both               |  7741.000 |           0.308 |               0.011 | 10583.000 |            0.380 |                0.024 |
| sector & sub-industry today green    | neither            |  8529.000 |           0.340 |               0.021 | 12091.000 |            0.398 |                0.032 |
| sector & sub-industry today green    | one of the two     |  3171.000 |           0.327 |               0.015 |  4527.000 |            0.358 |                0.017 |
| sector & sub-industry up over 5 days | both               |  8974.000 |           0.294 |               0.007 | 10707.000 |            0.396 |                0.029 |
| sector & sub-industry up over 5 days | neither            |  7230.000 |           0.360 |               0.026 | 12007.000 |            0.381 |                0.027 |
| sector & sub-industry up over 5 days | one of the two     |  3235.000 |           0.336 |               0.018 |  4487.000 |            0.367 |                0.019 |
| sector & sub-industry above 21 EMA   | both               |  9511.000 |           0.304 |               0.010 | 10377.000 |            0.398 |                0.030 |
| sector & sub-industry above 21 EMA   | neither            |  6624.000 |           0.353 |               0.023 | 12170.000 |            0.384 |                0.028 |
| sector & sub-industry above 21 EMA   | one of the two     |  3306.000 |           0.330 |               0.018 |  4654.000 |            0.355 |                0.016 |
| sector (11 GICS, by median RS)       | bottom 3           |  5204.000 |           0.331 |               0.015 |  6436.000 |            0.374 |                0.024 |
| sector (11 GICS, by median RS)       | middle 5           |  9815.000 |           0.326 |               0.018 | 14741.000 |            0.389 |                0.028 |
| sector (11 GICS, by median RS)       | top 3 (leading)    |  5856.000 |           0.313 |               0.012 |  6878.000 |            0.383 |                0.024 |
| sub-industry (by median RS)          | bottom 30%         |  5973.000 |           0.342 |               0.021 |  9478.000 |            0.382 |                0.025 |
| sub-industry (by median RS)          | middle             |  6513.000 |           0.330 |               0.018 |  9464.000 |            0.385 |                0.028 |
| sub-industry (by median RS)          | top 30% (leading)  |  6909.000 |           0.307 |               0.011 |  8220.000 |            0.387 |                0.027 |
| 3-day market model                   | bottom 10% (skip?) |  1626.000 |           0.409 |               0.035 |   201.000 |            0.478 |                0.057 |
| 3-day market model                   | rest               | 19249.000 |           0.317 |               0.014 | 27854.000 |            0.383 |                0.026 |

Same, S&P 500 stocks only after they joined the index (point-in-time survivorship check):

| regime                               | bucket             |     IS_n |   IS_hit_target |   IS_avg_net_return |    OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:-------------------------------------|:-------------------|---------:|----------------:|--------------------:|---------:|-----------------:|---------------------:|
| breadth (stocks above 50d)           | high (> 71%)       |  949.000 |           0.325 |               0.034 |  568.000 |            0.442 |                0.051 |
| breadth (stocks above 50d)           | low (< 53%)        | 1074.000 |           0.324 |               0.021 | 2132.000 |            0.360 |                0.028 |
| breadth (stocks above 50d)           | mid                | 1008.000 |           0.275 |               0.002 | 1059.000 |            0.428 |                0.042 |
| VIX level                            | 15-20              |  953.000 |           0.225 |              -0.008 | 1051.000 |            0.356 |                0.021 |
| VIX level                            | 20-30              |  691.000 |           0.444 |               0.059 | 2086.000 |            0.413 |                0.048 |
| VIX level                            | < 15               |  717.000 |           0.254 |               0.019 |  429.000 |            0.310 |               -0.004 |
| VIX level                            | > 30               |  670.000 |           0.343 |               0.016 |  193.000 |            0.534 |                0.073 |
| VIX / VIX3M                          | 0.9-1.0            | 1025.000 |           0.390 |               0.046 | 1802.000 |            0.372 |                0.035 |
| VIX / VIX3M                          | < 0.9 (calm)       | 1433.000 |           0.273 |               0.012 | 1510.000 |            0.421 |                0.038 |
| VIX / VIX3M                          | > 1.0 (stress)     |  573.000 |           0.248 |              -0.014 |  447.000 |            0.369 |                0.030 |
| SPY above 200d                       | no                 | 1237.000 |           0.346 |               0.019 | 1200.000 |            0.417 |                0.047 |
| SPY above 200d                       | yes                | 1794.000 |           0.281 |               0.018 | 2559.000 |            0.380 |                0.030 |
| QQQ above 10 & 20 SMA                | no                 | 1330.000 |           0.327 |               0.024 | 2289.000 |            0.375 |                0.032 |
| QQQ above 10 & 20 SMA                | yes                | 1701.000 |           0.293 |               0.014 | 1470.000 |            0.417 |                0.040 |
| SPY 1-month return                   | -3..0%             |  413.000 |           0.184 |              -0.018 |  605.000 |            0.337 |                0.024 |
| SPY 1-month return                   | 0..3%              |  879.000 |           0.349 |               0.033 |  858.000 |            0.427 |                0.044 |
| SPY 1-month return                   | < -3%              |  741.000 |           0.347 |               0.023 | 1332.000 |            0.365 |                0.030 |
| SPY 1-month return                   | > 3%               |  998.000 |           0.294 |               0.018 |  964.000 |            0.432 |                0.043 |
| SPY vs 21/50 SMA                     | above 21 & 50      | 1766.000 |           0.297 |               0.015 | 1486.000 |            0.415 |                0.036 |
| SPY vs 21/50 SMA                     | above 21 only      |   79.000 |           0.354 |               0.047 |  268.000 |            0.474 |                0.070 |
| SPY vs 21/50 SMA                     | above 50 only      |  290.000 |           0.186 |              -0.008 |  366.000 |            0.287 |                0.006 |
| SPY vs 21/50 SMA                     | below both         |  896.000 |           0.365 |               0.032 | 1639.000 |            0.380 |                0.036 |
| QQQ vs 21/50 SMA                     | above 21 & 50      | 1755.000 |           0.267 |               0.007 | 1501.000 |            0.410 |                0.038 |
| QQQ vs 21/50 SMA                     | above 21 only      |  168.000 |           0.357 |               0.029 |  161.000 |            0.391 |                0.028 |
| QQQ vs 21/50 SMA                     | above 50 only      |  214.000 |           0.308 |               0.027 |  477.000 |            0.327 |                0.015 |
| QQQ vs 21/50 SMA                     | below both         |  894.000 |           0.378 |               0.038 | 1620.000 |            0.394 |                0.040 |
| A/D line vs its 21/50 MA             | above 21 & 50      | 1739.000 |           0.264 |               0.006 | 1522.000 |            0.442 |                0.050 |
| A/D line vs its 21/50 MA             | above 21 only      |  171.000 |           0.444 |               0.048 |  149.000 |            0.282 |               -0.009 |
| A/D line vs its 21/50 MA             | above 50 only      |  343.000 |           0.283 |               0.023 |  547.000 |            0.329 |                0.020 |
| A/D line vs its 21/50 MA             | below both         |  778.000 |           0.387 |               0.038 | 1541.000 |            0.374 |                0.031 |
| % of stocks above 20d                | 40-60%             |  658.000 |           0.284 |               0.007 |  632.000 |            0.324 |                0.008 |
| % of stocks above 20d                | < 40%              |  798.000 |           0.318 |               0.023 | 1827.000 |            0.368 |                0.031 |
| % of stocks above 20d                | > 60%              | 1575.000 |           0.312 |               0.021 | 1300.000 |            0.457 |                0.055 |
| % above 50d, 10-day change           | falling (< -5 pts) | 1141.000 |           0.316 |               0.028 | 1894.000 |            0.388 |                0.036 |
| % above 50d, 10-day change           | flat               |  558.000 |           0.224 |              -0.015 |  916.000 |            0.348 |                0.021 |
| % above 50d, 10-day change           | rising (> +5 pts)  | 1332.000 |           0.336 |               0.025 |  949.000 |            0.440 |                0.049 |
| A/D line, 10-day change              | flat               |  738.000 |           0.222 |              -0.015 |  893.000 |            0.414 |                0.040 |
| A/D line, 10-day change              | falling            |  925.000 |           0.366 |               0.039 | 1707.000 |            0.374 |                0.033 |
| A/D line, 10-day change              | rising             | 1368.000 |           0.314 |               0.023 | 1159.000 |            0.400 |                0.037 |
| sector & sub-industry today green    | both               | 1026.000 |           0.279 |               0.010 | 1339.000 |            0.412 |                0.039 |
| sector & sub-industry today green    | neither            | 1295.000 |           0.341 |               0.032 | 1699.000 |            0.403 |                0.042 |
| sector & sub-industry today green    | one of the two     |  467.000 |           0.293 |               0.014 |  583.000 |            0.334 |                0.016 |
| sector & sub-industry up over 5 days | both               | 1242.000 |           0.266 |               0.009 | 1254.000 |            0.410 |                0.040 |
| sector & sub-industry up over 5 days | neither            | 1050.000 |           0.376 |               0.041 | 1823.000 |            0.389 |                0.036 |
| sector & sub-industry up over 5 days | one of the two     |  495.000 |           0.281 |               0.008 |  544.000 |            0.381 |                0.031 |
| sector & sub-industry above 21 EMA   | both               | 1303.000 |           0.288 |               0.014 | 1158.000 |            0.446 |                0.051 |
| sector & sub-industry above 21 EMA   | neither            |  987.000 |           0.339 |               0.031 | 1902.000 |            0.375 |                0.032 |
| sector & sub-industry above 21 EMA   | one of the two     |  498.000 |           0.311 |               0.019 |  561.000 |            0.358 |                0.024 |
| sector (11 GICS, by median RS)       | bottom 3           | 1000.000 |           0.317 |               0.016 | 1027.000 |            0.382 |                0.035 |
| sector (11 GICS, by median RS)       | middle 5           | 1286.000 |           0.313 |               0.024 | 1959.000 |            0.398 |                0.037 |
| sector (11 GICS, by median RS)       | top 3 (leading)    |  745.000 |           0.286 |               0.012 |  773.000 |            0.389 |                0.033 |
| sub-industry (by median RS)          | bottom 30%         | 1035.000 |           0.335 |               0.028 | 1472.000 |            0.417 |                0.043 |
| sub-industry (by median RS)          | middle             |  864.000 |           0.309 |               0.018 | 1254.000 |            0.382 |                0.032 |
| sub-industry (by median RS)          | top 30% (leading)  |  874.000 |           0.283 |               0.015 |  878.000 |            0.378 |                0.034 |
| 3-day market model                   | bottom 10% (skip?) |  293.000 |           0.382 |               0.032 |   18.000 |            0.444 |                0.050 |
| 3-day market model                   | rest               | 2738.000 |           0.300 |               0.017 | 3741.000 |            0.391 |                0.035 |

All stocks (no model), +20/-10, by the same splits: does a leading sector help on its own?

| regime                               | bucket             |       IS_n |   IS_hit_target |   IS_avg_net_return |      OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:-------------------------------------|:-------------------|-----------:|----------------:|--------------------:|-----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)           | high (> 71%)       |  71732.000 |           0.163 |               0.025 |  73183.000 |            0.209 |                0.009 |
| breadth (stocks above 50d)           | low (< 53%)        |  67297.000 |           0.218 |               0.020 | 106675.000 |            0.261 |                0.021 |
| breadth (stocks above 50d)           | mid                |  69689.000 |           0.160 |               0.015 | 100660.000 |            0.212 |                0.009 |
| VIX level                            | 15-20              |  59022.000 |           0.163 |               0.018 | 107145.000 |            0.206 |                0.009 |
| VIX level                            | 20-30              |  43347.000 |           0.263 |               0.034 |  85329.000 |            0.273 |                0.021 |
| VIX level                            | < 15               |  86178.000 |           0.135 |               0.019 |  70893.000 |            0.174 |                0.002 |
| VIX level                            | > 30               |  20171.000 |           0.241 |               0.003 |  17151.000 |            0.396 |                0.046 |
| VIX / VIX3M                          | 0.9-1.0            |  68343.000 |           0.203 |               0.024 | 103129.000 |            0.244 |                0.018 |
| VIX / VIX3M                          | < 0.9 (calm)       | 118980.000 |           0.155 |               0.020 | 157497.000 |            0.211 |                0.009 |
| VIX / VIX3M                          | > 1.0 (stress)     |  21395.000 |           0.243 |               0.010 |  19892.000 |            0.311 |                0.024 |
| SPY above 200d                       | no                 |  45920.000 |           0.246 |               0.014 |  51862.000 |            0.279 |                0.016 |
| SPY above 200d                       | yes                | 162798.000 |           0.161 |               0.022 | 228656.000 |            0.219 |                0.013 |
| QQQ above 10 & 20 SMA                | no                 |  85959.000 |           0.203 |               0.020 | 120794.000 |            0.235 |                0.011 |
| QQQ above 10 & 20 SMA                | yes                | 122759.000 |           0.164 |               0.020 | 159724.000 |            0.226 |                0.015 |
| SPY 1-month return                   | -3..0%             |  41194.000 |           0.179 |               0.019 |  44690.000 |            0.225 |                0.015 |
| SPY 1-month return                   | 0..3%              |  75549.000 |           0.162 |               0.020 |  89375.000 |            0.216 |                0.010 |
| SPY 1-month return                   | < -3%              |  28564.000 |           0.261 |               0.021 |  44664.000 |            0.261 |                0.014 |
| SPY 1-month return                   | > 3%               |  63411.000 |           0.165 |               0.021 | 101789.000 |            0.231 |                0.015 |
| SPY vs 21/50 SMA                     | above 21 & 50      | 128047.000 |           0.161 |               0.021 | 176873.000 |            0.213 |                0.010 |
| SPY vs 21/50 SMA                     | above 21 only      |   8902.000 |           0.204 |               0.015 |  16994.000 |            0.269 |                0.026 |
| SPY vs 21/50 SMA                     | above 50 only      |  21828.000 |           0.131 |               0.001 |  21415.000 |            0.225 |                0.010 |
| SPY vs 21/50 SMA                     | below both         |  49941.000 |           0.245 |               0.027 |  65236.000 |            0.268 |                0.020 |
| QQQ vs 21/50 SMA                     | above 21 & 50      | 126854.000 |           0.158 |               0.017 | 165855.000 |            0.217 |                0.012 |
| QQQ vs 21/50 SMA                     | above 21 only      |  11791.000 |           0.198 |               0.022 |  16899.000 |            0.254 |                0.021 |
| QQQ vs 21/50 SMA                     | above 50 only      |  20354.000 |           0.177 |               0.025 |  29649.000 |            0.222 |                0.009 |
| QQQ vs 21/50 SMA                     | below both         |  49719.000 |           0.232 |               0.025 |  68115.000 |            0.258 |                0.017 |
| A/D line vs its 21/50 MA             | above 21 & 50      | 131737.000 |           0.157 |               0.019 | 169798.000 |            0.209 |                0.009 |
| A/D line vs its 21/50 MA             | above 21 only      |   7717.000 |           0.189 |              -0.010 |   8948.000 |            0.304 |                0.024 |
| A/D line vs its 21/50 MA             | above 50 only      |  25278.000 |           0.164 |               0.022 |  39217.000 |            0.240 |                0.020 |
| A/D line vs its 21/50 MA             | below both         |  43986.000 |           0.255 |               0.028 |  62555.000 |            0.271 |                0.019 |
| % of stocks above 20d                | 40-60%             |  49663.000 |           0.167 |               0.013 |  72871.000 |            0.201 |                0.002 |
| % of stocks above 20d                | < 40%              |  49408.000 |           0.224 |               0.024 |  72914.000 |            0.275 |                0.025 |
| % of stocks above 20d                | > 60%              | 109647.000 |           0.166 |               0.022 | 134733.000 |            0.221 |                0.013 |
| % above 50d, 10-day change           | falling (< -5 pts) |  83415.000 |           0.191 |               0.025 | 103046.000 |            0.242 |                0.016 |
| % above 50d, 10-day change           | flat               |  46083.000 |           0.149 |               0.010 |  75622.000 |            0.214 |                0.007 |
| % above 50d, 10-day change           | rising (> +5 pts)  |  79220.000 |           0.186 |               0.022 | 101850.000 |            0.229 |                0.014 |
| A/D line, 10-day change              | flat               |  57613.000 |           0.166 |               0.014 |  76536.000 |            0.225 |                0.010 |
| A/D line, 10-day change              | falling            |  56238.000 |           0.214 |               0.024 |  76386.000 |            0.269 |                0.022 |
| A/D line, 10-day change              | rising             |  94867.000 |           0.168 |               0.022 | 127596.000 |            0.210 |                0.010 |
| sector & sub-industry today green    | both               |  88243.000 |           0.167 |               0.018 | 121675.000 |            0.221 |                0.011 |
| sector & sub-industry today green    | neither            |  78150.000 |           0.192 |               0.022 | 105754.000 |            0.243 |                0.017 |
| sector & sub-industry today green    | one of the two     |  30420.000 |           0.182 |               0.022 |  44306.000 |            0.225 |                0.012 |
| sector & sub-industry up over 5 days | both               |  98181.000 |           0.165 |               0.020 | 132962.000 |            0.227 |                0.014 |
| sector & sub-industry up over 5 days | neither            |  67112.000 |           0.199 |               0.021 |  93454.000 |            0.245 |                0.016 |
| sector & sub-industry up over 5 days | one of the two     |  31511.000 |           0.183 |               0.021 |  45312.000 |            0.211 |                0.006 |
| sector & sub-industry above 21 EMA   | both               | 107573.000 |           0.161 |               0.021 | 140980.000 |            0.211 |                0.009 |
| sector & sub-industry above 21 EMA   | neither            |  58174.000 |           0.215 |               0.022 |  84518.000 |            0.268 |                0.022 |
| sector & sub-industry above 21 EMA   | one of the two     |  31066.000 |           0.174 |               0.016 |  46237.000 |            0.221 |                0.009 |
| sector (11 GICS, by median RS)       | bottom 3           |  49082.000 |           0.183 |               0.021 |  61610.000 |            0.230 |                0.014 |
| sector (11 GICS, by median RS)       | middle 5           | 102206.000 |           0.183 |               0.022 | 137458.000 |            0.234 |                0.014 |
| sector (11 GICS, by median RS)       | top 3 (leading)    |  57430.000 |           0.172 |               0.017 |  81450.000 |            0.223 |                0.011 |
| sub-industry (by median RS)          | bottom 30%         |  52119.000 |           0.195 |               0.022 |  75142.000 |            0.238 |                0.011 |
| sub-industry (by median RS)          | middle             |  84123.000 |           0.170 |               0.022 | 113554.000 |            0.222 |                0.015 |
| sub-industry (by median RS)          | top 30% (leading)  |  59994.000 |           0.179 |               0.018 |  82724.000 |            0.234 |                0.013 |
| 3-day market model                   | bottom 10% (skip?) |  21518.000 |           0.232 |               0.026 |   4965.000 |            0.352 |                0.043 |
| 3-day market model                   | rest               | 187200.000 |           0.174 |               0.020 | 275553.000 |            0.228 |                0.013 |

Regime gates, one family at a time: skip the buckets of that family that were below break-even in-sample (hit < 33% or negative return), then trade the model's top 10% with +20/-10. RULE rows keep only the picks that pass a rule fixed in advance: leading groups (run 19: top 3 of 11 sectors / top 30% of sub-industries by median RS) and the user's run-21 rules (SPY/QQQ vs 21 & 50 SMA, breadth, A/D line, sector & sub-industry green / up 5 days / above 21 EMA; groups = equal-weight median of member stocks). Portfolio 2018+:

| gate                                                  | skipped (chosen IS)                 |    CAGR |   max_DD |   trades |   PIT CAGR |   PIT max_DD |
|:------------------------------------------------------|:------------------------------------|--------:|---------:|---------:|-----------:|-------------:|
| breadth (stocks above 50d)                            | high (> 71%), mid                   |   0.125 |   -0.415 |  707.000 |      0.092 |       -0.266 |
| VIX level                                             | 15-20, < 15                         |   0.256 |   -0.459 |  664.000 |      0.213 |       -0.296 |
| VIX / VIX3M                                           | < 0.9 (calm), > 1.0 (stress)        |   0.134 |   -0.455 |  801.000 |      0.149 |       -0.268 |
| SPY above 200d                                        | yes                                 |   0.092 |   -0.308 |  320.000 |      0.059 |       -0.217 |
| QQQ above 10 & 20 SMA                                 | yes                                 |   0.163 |   -0.458 |  907.000 |      0.120 |       -0.289 |
| SPY 1-month return                                    | -3..0%, > 3%                        |   0.176 |   -0.398 |  928.000 |      0.168 |       -0.285 |
| SPY vs 21/50 SMA                                      | above 21 & 50, above 50 only        |   0.116 |   -0.406 |  554.000 |      0.085 |       -0.365 |
| QQQ vs 21/50 SMA                                      | above 21 & 50                       |   0.159 |   -0.471 |  784.000 |      0.056 |       -0.322 |
| A/D line vs its 21/50 MA                              | above 21 & 50, above 50 only        |   0.079 |   -0.397 |  554.000 |      0.037 |       -0.329 |
| % of stocks above 20d                                 | 40-60%, > 60%                       |   0.152 |   -0.442 |  645.000 |      0.094 |       -0.250 |
| % above 50d, 10-day change                            | flat, rising (> +5 pts)             |   0.094 |   -0.487 |  802.000 |      0.122 |       -0.251 |
| A/D line, 10-day change                               | flat, rising                        |   0.140 |   -0.334 |  672.000 |      0.074 |       -0.290 |
| sector & sub-industry today green                     | both, one of the two                |   0.290 |   -0.441 | 1029.000 |      0.146 |       -0.228 |
| sector & sub-industry up over 5 days                  | both                                |   0.162 |   -0.426 | 1068.000 |      0.137 |       -0.275 |
| sector & sub-industry above 21 EMA                    | both, one of the two                |   0.279 |   -0.363 |  958.000 |      0.108 |       -0.266 |
| sector (11 GICS, by median RS)                        | bottom 3, middle 5, top 3 (leading) | nan     |  nan     |  nan     |    nan     |      nan     |
| sub-industry (by median RS)                           | middle, top 30% (leading)           |   0.211 |   -0.338 | 1024.000 |      0.164 |       -0.268 |
| 3-day market model                                    | rest                                |   0.075 |   -0.162 |  130.000 |      0.010 |       -0.053 |
| RULE: top 3 sectors only                              | nothing                             |   0.124 |   -0.342 |  909.000 |      0.114 |       -0.213 |
| RULE: top 30% sub-industries only                     | nothing                             |   0.232 |   -0.312 |  933.000 |      0.112 |       -0.270 |
| RULE: top 3 sectors AND top 30% sub-industries        | nothing                             |   0.181 |   -0.372 |  810.000 |      0.047 |       -0.254 |
| RULE: SPY above its 21 & 50 SMA                       | nothing                             |   0.213 |   -0.352 |  892.000 |      0.145 |       -0.263 |
| RULE: QQQ above its 21 & 50 SMA                       | nothing                             |   0.240 |   -0.300 |  845.000 |      0.173 |       -0.215 |
| RULE: SPY above its 50 SMA (21 either way)            | nothing                             |   0.172 |   -0.408 |  929.000 |      0.151 |       -0.328 |
| RULE: A/D line above its 21 & 50 MA                   | nothing                             |   0.138 |   -0.546 |  896.000 |      0.209 |       -0.196 |
| RULE: > 50% of stocks above their 50d                 | nothing                             |   0.132 |   -0.380 |  870.000 |      0.138 |       -0.274 |
| RULE: % above 50d rising over 10 days                 | nothing                             |   0.195 |   -0.325 |  927.000 |      0.177 |       -0.260 |
| RULE: sector AND sub-industry green today             | nothing                             |   0.223 |   -0.461 | 1026.000 |      0.201 |       -0.245 |
| RULE: sector AND sub-industry up over 5 days          | nothing                             |   0.119 |   -0.518 |  991.000 |      0.176 |       -0.386 |
| RULE: sector AND sub-industry above 21 EMA            | nothing                             |   0.152 |   -0.490 |  968.000 |      0.181 |       -0.259 |
| RULE: SPY > 21 & 50 + sector & sub-industry up 5 days | nothing                             |   0.150 |   -0.358 |  818.000 |      0.161 |       -0.169 |
| (no gate)                                             | nothing                             |   0.253 |   -0.447 | 1189.000 |      0.213 |       -0.303 |

## 11. Qullamaggie replication (per trade, out-of-sample 2018+; IS in brackets)

Scan = top 3% performer over 1, 3 or 6 months with ADR >= 4%. Regime = QQQ above its 10- and 20-day SMAs. qull_breakout = buy-stop above the flag high the next day (fill at the trigger or the gap open), stop at the tighter of the 3-day low and 1 ADR; a same-day touch of the stop counts as stopped out. Portfolio rows start with QULL in section 9.

| entry            | filter           | exit          |   IS_n |   IS_win |   IS_avgR |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:-----------------|:--------------|-------:|---------:|----------:|--------:|-------------:|----------:|-----------:|---------:|--------:|
| ep_gap10         | all              | bracket_20_10 |    529 |     0.47 |      0.19 |     933 |       106.46 |      0.41 |       0.11 |     1.19 |    2.42 |
| ep_gap10         | all              | qull_sma10    |    544 |     0.44 |     -0.01 |     933 |       106.46 |      0.45 |       0.01 |     1.01 |    0.15 |
| ep_gap10         | all              | qull_sma20    |    542 |     0.46 |     -0.03 |     933 |       106.46 |      0.45 |       0.07 |     1.15 |    1.28 |
| ep_gap10         | all              | sma50_close   |    533 |     0.29 |      0.14 |     933 |       106.46 |      0.31 |       0.49 |     1.74 |    3.61 |
| ep_gap10         | qull_scan        | bracket_20_10 |    124 |     0.36 |      0.06 |     261 |        29.78 |      0.43 |       0.22 |     1.38 |    2.42 |
| ep_gap10         | qull_scan        | qull_sma10    |    126 |     0.40 |     -0.06 |     261 |        29.78 |      0.43 |      -0.03 |     0.93 |   -0.44 |
| ep_gap10         | qull_scan        | qull_sma20    |    124 |     0.42 |     -0.09 |     261 |        29.78 |      0.45 |       0.14 |     1.28 |    1.21 |
| ep_gap10         | qull_scan        | sma50_close   |    122 |     0.20 |      0.01 |     261 |        29.78 |      0.32 |       0.83 |     2.26 |    2.68 |
| ep_gap10         | qull_scan_regime | bracket_20_10 |     82 |     0.34 |     -0.01 |     160 |        18.26 |      0.42 |       0.19 |     1.31 |    1.62 |
| ep_gap10         | qull_scan_regime | qull_sma10    |     83 |     0.41 |     -0.08 |     160 |        18.26 |      0.44 |      -0.03 |     0.94 |   -0.29 |
| ep_gap10         | qull_scan_regime | qull_sma20    |     83 |     0.43 |     -0.04 |     160 |        18.26 |      0.46 |       0.24 |     1.48 |    1.41 |
| ep_gap10         | qull_scan_regime | sma50_close   |     81 |     0.17 |      0.10 |     160 |        18.26 |      0.33 |       1.01 |     2.55 |    2.37 |
| ep_gap8_hold     | all              | bracket_20_10 |    733 |     0.48 |      0.21 |    1182 |       134.87 |      0.42 |       0.11 |     1.20 |    2.86 |
| ep_gap8_hold     | all              | qull_sma10    |    750 |     0.46 |      0.01 |    1182 |       134.87 |      0.46 |      -0.01 |     0.98 |   -0.32 |
| ep_gap8_hold     | all              | qull_sma20    |    749 |     0.48 |      0.03 |    1182 |       134.87 |      0.46 |       0.04 |     1.08 |    0.79 |
| ep_gap8_hold     | all              | sma50_close   |    741 |     0.33 |      0.26 |    1182 |       134.87 |      0.31 |       0.37 |     1.58 |    3.45 |
| ep_gap8_hold     | qull_scan        | bracket_20_10 |    147 |     0.36 |      0.03 |     284 |        32.41 |      0.45 |       0.26 |     1.45 |    2.93 |
| ep_gap8_hold     | qull_scan        | qull_sma10    |    150 |     0.41 |     -0.08 |     284 |        32.41 |      0.50 |       0.06 |     1.14 |    0.84 |
| ep_gap8_hold     | qull_scan        | qull_sma20    |    149 |     0.42 |     -0.04 |     284 |        32.41 |      0.51 |       0.21 |     1.45 |    1.92 |
| ep_gap8_hold     | qull_scan        | sma50_close   |    148 |     0.22 |      0.05 |     284 |        32.41 |      0.33 |       0.85 |     2.30 |    2.95 |
| ep_gap8_hold     | qull_scan_regime | bracket_20_10 |    103 |     0.35 |     -0.01 |     175 |        19.97 |      0.43 |       0.23 |     1.39 |    2.03 |
| ep_gap8_hold     | qull_scan_regime | qull_sma10    |    105 |     0.42 |     -0.09 |     175 |        19.97 |      0.50 |       0.04 |     1.08 |    0.39 |
| ep_gap8_hold     | qull_scan_regime | qull_sma20    |    105 |     0.42 |     -0.01 |     175 |        19.97 |      0.51 |       0.26 |     1.55 |    1.66 |
| ep_gap8_hold     | qull_scan_regime | sma50_close   |    104 |     0.20 |      0.15 |     175 |        19.97 |      0.34 |       0.98 |     2.49 |    2.48 |
| qull_breakout    | all              | bracket_20_10 |   2549 |     0.37 |      0.01 |    4386 |       500.46 |      0.41 |       0.15 |     1.25 |    6.83 |
| qull_breakout    | all              | qull_sma10    |   2560 |     0.33 |     -0.33 |    4386 |       500.46 |      0.33 |      -0.25 |     0.64 |  -10.85 |
| qull_breakout    | all              | qull_sma20    |   2558 |     0.33 |     -0.34 |    4386 |       500.46 |      0.33 |      -0.22 |     0.69 |   -8.13 |
| qull_breakout    | all              | sma50_close   |   2553 |     0.14 |     -0.39 |    4386 |       500.46 |      0.17 |       0.01 |     1.01 |    0.19 |
| qull_breakout    | qull_scan        | bracket_20_10 |    648 |     0.39 |      0.12 |    1211 |       138.18 |      0.38 |       0.09 |     1.13 |    2.04 |
| qull_breakout    | qull_scan        | qull_sma10    |    650 |     0.35 |     -0.28 |    1211 |       138.18 |      0.36 |      -0.17 |     0.73 |   -4.02 |
| qull_breakout    | qull_scan        | qull_sma20    |    650 |     0.35 |     -0.26 |    1211 |       138.18 |      0.36 |      -0.15 |     0.77 |   -3.03 |
| qull_breakout    | qull_scan        | sma50_close   |    648 |     0.16 |     -0.29 |    1211 |       138.18 |      0.17 |       0.06 |     1.07 |    0.44 |
| qull_breakout    | qull_scan_regime | bracket_20_10 |    440 |     0.38 |      0.08 |     782 |        89.23 |      0.41 |       0.18 |     1.30 |    3.37 |
| qull_breakout    | qull_scan_regime | qull_sma10    |    442 |     0.34 |     -0.31 |     782 |        89.23 |      0.37 |      -0.12 |     0.80 |   -2.22 |
| qull_breakout    | qull_scan_regime | qull_sma20    |    442 |     0.35 |     -0.29 |     782 |        89.23 |      0.37 |      -0.06 |     0.91 |   -0.87 |
| qull_breakout    | qull_scan_regime | sma50_close   |    440 |     0.17 |     -0.28 |     782 |        89.23 |      0.19 |       0.28 |     1.33 |    1.33 |
| qull_breakout_60 | all              | bracket_20_10 |    918 |     0.35 |      0.01 |    1865 |       212.81 |      0.42 |       0.20 |     1.33 |    5.70 |
| qull_breakout_60 | all              | qull_sma10    |    918 |     0.36 |     -0.31 |    1865 |       212.81 |      0.32 |      -0.25 |     0.64 |   -7.06 |
| qull_breakout_60 | all              | qull_sma20    |    918 |     0.35 |     -0.33 |    1865 |       212.81 |      0.32 |      -0.22 |     0.69 |   -5.34 |
| qull_breakout_60 | all              | sma50_close   |    918 |     0.14 |     -0.34 |    1865 |       212.81 |      0.17 |       0.12 |     1.13 |    0.85 |
| qull_breakout_60 | qull_scan        | bracket_20_10 |    391 |     0.37 |      0.08 |     849 |        96.88 |      0.39 |       0.12 |     1.19 |    2.35 |
| qull_breakout_60 | qull_scan        | qull_sma10    |    391 |     0.35 |     -0.28 |     849 |        96.88 |      0.35 |      -0.20 |     0.70 |   -3.79 |
| qull_breakout_60 | qull_scan        | qull_sma20    |    391 |     0.35 |     -0.25 |     849 |        96.88 |      0.35 |      -0.18 |     0.73 |   -2.98 |
| qull_breakout_60 | qull_scan        | sma50_close   |    391 |     0.16 |     -0.30 |     849 |        96.88 |      0.16 |       0.12 |     1.14 |    0.64 |
| qull_breakout_60 | qull_scan_regime | bracket_20_10 |    271 |     0.36 |      0.04 |     576 |        65.72 |      0.42 |       0.22 |     1.36 |    3.47 |
| qull_breakout_60 | qull_scan_regime | qull_sma10    |    271 |     0.33 |     -0.33 |     576 |        65.72 |      0.36 |      -0.17 |     0.73 |   -2.67 |
| qull_breakout_60 | qull_scan_regime | qull_sma20    |    271 |     0.33 |     -0.29 |     576 |        65.72 |      0.36 |      -0.11 |     0.84 |   -1.35 |
| qull_breakout_60 | qull_scan_regime | sma50_close   |    271 |     0.15 |     -0.33 |     576 |        65.72 |      0.18 |       0.30 |     1.34 |    1.09 |
| random_uptrend   | all              | bracket_20_10 |  30366 |     0.53 |      0.19 |   34140 |      3895.54 |      0.46 |       0.10 |     1.20 |   14.93 |
| random_uptrend   | all              | qull_sma10    |  31158 |     0.30 |     -0.16 |   34140 |      3895.54 |      0.29 |      -0.11 |     0.87 |   -8.40 |
| random_uptrend   | all              | qull_sma20    |  31119 |     0.30 |     -0.15 |   34140 |      3895.54 |      0.29 |      -0.10 |     0.88 |   -7.26 |
| random_uptrend   | all              | sma50_close   |  30938 |     0.15 |     -0.05 |   34140 |      3895.54 |      0.14 |      -0.02 |     0.98 |   -0.92 |
| random_uptrend   | qull_scan        | bracket_20_10 |   1009 |     0.37 |      0.05 |    1978 |       225.70 |      0.39 |       0.13 |     1.21 |    3.94 |
| random_uptrend   | qull_scan        | qull_sma10    |   1014 |     0.31 |     -0.12 |    1978 |       225.70 |      0.31 |      -0.01 |     0.99 |   -0.14 |
| random_uptrend   | qull_scan        | qull_sma20    |   1013 |     0.31 |     -0.10 |    1978 |       225.70 |      0.31 |       0.04 |     1.05 |    0.65 |
| random_uptrend   | qull_scan        | sma50_close   |   1013 |     0.14 |     -0.15 |    1978 |       225.70 |      0.15 |       0.15 |     1.16 |    1.47 |
| random_uptrend   | qull_scan_regime | bracket_20_10 |    580 |     0.38 |      0.07 |    1200 |       136.93 |      0.41 |       0.18 |     1.28 |    3.96 |
| random_uptrend   | qull_scan_regime | qull_sma10    |    584 |     0.34 |     -0.12 |    1200 |       136.93 |      0.33 |       0.03 |     1.04 |    0.40 |
| random_uptrend   | qull_scan_regime | qull_sma20    |    583 |     0.33 |     -0.12 |    1200 |       136.93 |      0.33 |       0.08 |     1.11 |    1.00 |
| random_uptrend   | qull_scan_regime | sma50_close   |    583 |     0.14 |     -0.19 |    1200 |       136.93 |      0.16 |       0.26 |     1.27 |    1.77 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                                                     |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:---------------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| wf_scan_pullback / wf_scan / bracket_20_10                                                   |  -0.01 |    -0.41 |             -0.40 |   692.00 |   0.39 |            8.87 |             nan    |
| donchian_20 / all / bracket_20_10                                                            |   0.09 |    -0.44 |             -0.42 |   792.00 |   0.41 |            9.29 |               0.98 |
| pocket_pivot / all / bracket_20_10                                                           |   0.07 |    -0.35 |             -0.31 |   574.00 |   0.41 |            7.27 |               0.63 |
| wf_scan_base / all / bracket_20_10                                                           |   0.08 |    -0.21 |             -0.20 |   505.00 |   0.50 |            9.60 |               0.70 |
| donchian_55 / all / bracket_20_10                                                            |   0.01 |    -0.41 |             -0.38 |   747.00 |   0.40 |            9.09 |               4.43 |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                            |   0.06 |    -0.34 |             -0.30 |   646.00 |   0.41 |            8.25 |               0.97 |
| All setups, ranked by RS / bracket_20_10                                                     |   0.18 |    -0.41 |             -0.38 |  1104.00 |   0.41 |            9.12 |               0.54 |
| All setups, random order / bracket_20_10                                                     |   0.01 |    -0.45 |             -0.42 |   552.00 |   0.43 |            8.86 |               7.80 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                                 |   0.14 |    -0.29 |             -0.28 |   849.00 |   0.42 |            8.90 |               0.61 |
| BASELINE random entries, ranked by RS / bracket_20_10                                        |   0.04 |    -0.51 |             -0.47 |   689.00 |   0.40 |            7.64 |               1.59 |
| BASELINE random entries, random order / bracket_20_10                                        |   0.05 |    -0.38 |             -0.35 |   424.00 |   0.45 |            7.13 |               1.23 |
| IS-selected setups (4), ranked by RS / bracket_20_10                                         |  -0.02 |    -0.51 |             -0.49 |   528.00 |   0.40 |            8.15 |             nan    |
| IS-selected setups, only when SPY > 200d / bracket_20_10                                     |  -0.04 |    -0.51 |             -0.49 |   428.00 |   0.39 |            7.01 |             nan    |
| IS-selected setups (26), ranked by RS / sma50_close                                          |   0.05 |    -0.55 |             -0.48 |   982.00 |   0.26 |            8.99 |               1.25 |
| IS-selected setups, only when SPY > 200d / sma50_close                                       |   0.06 |    -0.49 |             -0.45 |   812.00 |   0.25 |            7.74 |               1.03 |
| All setups, ranked by RS / sma50_close                                                       |   0.15 |    -0.53 |             -0.46 |  1156.00 |   0.28 |            8.84 |               0.58 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                                  |   0.09 |    -0.26 |             -0.20 |   416.00 |   0.30 |            5.37 |               0.67 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                                 |   0.07 |    -0.34 |             -0.25 |   464.00 |   0.29 |            5.78 |               0.80 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                                 |   0.09 |    -0.24 |             -0.16 |   617.00 |   0.31 |            7.70 |               0.62 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)                     |   0.11 |    -0.21 |             -0.12 |   609.00 |   0.33 |            7.64 |               0.49 |
| Top 20 by IS expectancy, ranked by superperformer model                                      |   0.10 |    -0.27 |             -0.25 |   640.00 |   0.32 |            7.59 |               0.51 |
| All setups, ranked by superperformer model / bracket_20_10                                   |   0.23 |    -0.41 |             -0.39 |  1369.00 |   0.40 |            9.14 |               0.52 |
| Only setups in the model's top 10% likely superperformers / sma50_close                      |   0.13 |    -0.52 |             -0.45 |  1415.00 |   0.29 |            8.95 |               0.93 |
| CHECK random entries in the model's top 10% / sma50_close                                    |   0.08 |    -0.54 |             -0.47 |   979.00 |   0.15 |            5.30 |               1.07 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close                     |   0.15 |    -0.50 |             -0.43 |  1333.00 |   0.28 |            8.60 |               0.88 |
| Top 10% model + adaptive sizing / sma50_close                                                |   0.06 |    -0.52 |             -0.40 |  1513.00 |   0.29 |            9.31 |               1.47 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                         |   0.16 |    -0.43 |             -0.38 |  1412.00 |   0.30 |            9.10 |               0.72 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                            |   0.21 |    -0.61 |             -0.59 |  1216.00 |   0.41 |            9.41 |               0.70 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                                    |   0.19 |    -0.51 |             -0.49 |  1189.00 |   0.40 |            9.14 |               0.75 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                                      |   0.14 |    -0.42 |             -0.41 |  1011.00 |   0.39 |            8.66 |               0.63 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                          |   0.12 |    -0.35 |             -0.33 |   780.00 |   0.40 |            7.98 |               0.90 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                            |   0.09 |    -0.30 |             -0.29 |  1313.00 |   0.54 |            8.33 |               0.67 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                                    |   0.05 |    -0.29 |             -0.27 |  1287.00 |   0.54 |            8.13 |               0.90 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                                      |   0.12 |    -0.31 |             -0.30 |  1056.00 |   0.55 |            7.18 |               0.60 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                          |   0.08 |    -0.31 |             -0.27 |   835.00 |   0.55 |            6.70 |               1.06 |
| MENU top 10% model / +10% -10%                                                               |   0.22 |    -0.53 |             -0.52 |  1933.00 |   0.56 |            8.68 |               0.75 |
| MENU top 10% model / +20% -10%                                                               |   0.25 |    -0.45 |             -0.43 |  1189.00 |   0.42 |            9.07 |               0.65 |
| MENU top 10% model / +20% -15% (IS best return per month)                                    |   0.20 |    -0.36 |             -0.35 |   893.00 |   0.52 |            9.26 |               0.53 |
| MENU top 10% model / +30% -15% (IS best return per trade)                                    |   0.20 |    -0.33 |             -0.33 |   690.00 |   0.46 |            9.37 |               0.53 |
| REGIME breadth (stocks above 50d): skip ['high (> 71%)', 'mid'] / +20% -10%                  |   0.12 |    -0.41 |             -0.40 |   707.00 |   0.41 |            5.57 |               0.64 |
| REGIME breadth (stocks above 50d), S&P 500 point-in-time only / +20% -10%                    |   0.09 |    -0.27 |             -0.25 |   413.00 |   0.45 |            4.64 |               0.66 |
| REGIME VIX level: skip ['15-20', '< 15'] / +20% -10%                                         |   0.26 |    -0.46 |             -0.44 |   664.00 |   0.47 |            5.53 |               0.50 |
| REGIME VIX level, S&P 500 point-in-time only / +20% -10%                                     |   0.21 |    -0.30 |             -0.26 |   426.00 |   0.52 |            4.71 |               0.50 |
| REGIME VIX / VIX3M: skip ['< 0.9 (calm)', '> 1.0 (stress)'] / +20% -10%                      |   0.13 |    -0.46 |             -0.43 |   801.00 |   0.41 |            6.61 |               0.87 |
| REGIME VIX / VIX3M, S&P 500 point-in-time only / +20% -10%                                   |   0.15 |    -0.27 |             -0.24 |   472.00 |   0.47 |            4.94 |               0.62 |
| REGIME SPY above 200d: skip ['yes'] / +20% -10%                                              |   0.09 |    -0.31 |             -0.29 |   320.00 |   0.44 |            2.40 |               0.77 |
| REGIME SPY above 200d, S&P 500 point-in-time only / +20% -10%                                |   0.06 |    -0.22 |             -0.18 |   190.00 |   0.47 |            1.73 |               0.88 |
| REGIME QQQ above 10 & 20 SMA: skip ['yes'] / +20% -10%                                       |   0.16 |    -0.46 |             -0.44 |   907.00 |   0.41 |            7.34 |               0.42 |
| REGIME QQQ above 10 & 20 SMA, S&P 500 point-in-time only / +20% -10%                         |   0.12 |    -0.29 |             -0.25 |   507.00 |   0.46 |            5.68 |               0.54 |
| REGIME SPY 1-month return: skip ['-3..0%', '> 3%'] / +20% -10%                               |   0.18 |    -0.40 |             -0.39 |   928.00 |   0.41 |            7.63 |               0.57 |
| REGIME SPY 1-month return, S&P 500 point-in-time only / +20% -10%                            |   0.17 |    -0.28 |             -0.24 |   504.00 |   0.47 |            5.68 |               0.42 |
| REGIME SPY vs 21/50 SMA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%                 |   0.12 |    -0.41 |             -0.38 |   554.00 |   0.42 |            4.49 |               0.58 |
| REGIME SPY vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                              |   0.09 |    -0.36 |             -0.31 |   350.00 |   0.45 |            3.92 |               0.74 |
| REGIME QQQ vs 21/50 SMA: skip ['above 21 & 50'] / +20% -10%                                  |   0.16 |    -0.47 |             -0.42 |   784.00 |   0.42 |            6.33 |               0.56 |
| REGIME QQQ vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                              |   0.06 |    -0.32 |             -0.27 |   473.00 |   0.42 |            5.27 |               0.96 |
| REGIME A/D line vs its 21/50 MA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%         |   0.08 |    -0.40 |             -0.38 |   554.00 |   0.40 |            4.48 |               0.85 |
| REGIME A/D line vs its 21/50 MA, S&P 500 point-in-time only / +20% -10%                      |   0.04 |    -0.33 |             -0.27 |   341.00 |   0.42 |            3.71 |               1.26 |
| REGIME % of stocks above 20d: skip ['40-60%', '> 60%'] / +20% -10%                           |   0.15 |    -0.44 |             -0.43 |   645.00 |   0.43 |            5.45 |               0.49 |
| REGIME % of stocks above 20d, S&P 500 point-in-time only / +20% -10%                         |   0.09 |    -0.25 |             -0.21 |   381.00 |   0.45 |            4.52 |               0.68 |
| REGIME % above 50d, 10-day change: skip ['flat', 'rising (> +5 pts)'] / +20% -10%            |   0.09 |    -0.49 |             -0.47 |   802.00 |   0.39 |            6.57 |               1.06 |
| REGIME % above 50d, 10-day change, S&P 500 point-in-time only / +20% -10%                    |   0.12 |    -0.25 |             -0.22 |   456.00 |   0.45 |            5.27 |               0.67 |
| REGIME A/D line, 10-day change: skip ['flat', 'rising'] / +20% -10%                          |   0.14 |    -0.33 |             -0.32 |   672.00 |   0.42 |            5.77 |               0.61 |
| REGIME A/D line, 10-day change, S&P 500 point-in-time only / +20% -10%                       |   0.07 |    -0.29 |             -0.24 |   388.00 |   0.44 |            4.56 |               0.69 |
| REGIME sector & sub-industry today green: skip ['both', 'one of the two'] / +20% -10%        |   0.29 |    -0.44 |             -0.40 |  1029.00 |   0.44 |            8.53 |               0.54 |
| REGIME sector & sub-industry today green, S&P 500 point-in-time only / +20% -10%             |   0.15 |    -0.23 |             -0.25 |   536.00 |   0.46 |            6.02 |               0.54 |
| REGIME sector & sub-industry up over 5 days: skip ['both'] / +20% -10%                       |   0.16 |    -0.43 |             -0.41 |  1068.00 |   0.40 |            8.71 |               0.79 |
| REGIME sector & sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%          |   0.14 |    -0.27 |             -0.26 |   582.00 |   0.44 |            6.54 |               0.56 |
| REGIME sector & sub-industry above 21 EMA: skip ['both', 'one of the two'] / +20% -10%       |   0.28 |    -0.36 |             -0.35 |   958.00 |   0.44 |            8.05 |               0.47 |
| REGIME sector & sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%            |   0.11 |    -0.27 |             -0.24 |   511.00 |   0.44 |            5.68 |               0.74 |
| REGIME sub-industry (by median RS): skip ['middle', 'top 30% (leading)'] / +20% -10%         |   0.21 |    -0.34 |             -0.31 |  1024.00 |   0.42 |            8.49 |               0.61 |
| REGIME sub-industry (by median RS), S&P 500 point-in-time only / +20% -10%                   |   0.16 |    -0.27 |             -0.25 |   518.00 |   0.47 |            5.86 |               0.52 |
| REGIME 3-day market model: skip ['rest'] / +20% -10%                                         |   0.08 |    -0.16 |             -0.13 |   130.00 |   0.52 |            1.23 |               0.70 |
| REGIME 3-day market model, S&P 500 point-in-time only / +20% -10%                            |   0.01 |    -0.05 |             -0.02 |    18.00 |   0.56 |            0.26 |               0.82 |
| RULE top 3 sectors only, model top 10% / +20% -10%                                           |   0.12 |    -0.34 |             -0.31 |   909.00 |   0.41 |            7.83 |               0.78 |
| RULE top 3 sectors only, S&P 500 point-in-time only / +20% -10%                              |   0.11 |    -0.21 |             -0.21 |   386.00 |   0.47 |            4.63 |               0.46 |
| RULE top 30% sub-industries only, model top 10% / +20% -10%                                  |   0.23 |    -0.31 |             -0.26 |   933.00 |   0.43 |            8.47 |               0.54 |
| RULE top 30% sub-industries only, S&P 500 point-in-time only / +20% -10%                     |   0.11 |    -0.27 |             -0.25 |   424.00 |   0.46 |            5.28 |               0.55 |
| RULE top 3 sectors AND top 30% sub-industries, model top 10% / +20% -10%                     |   0.18 |    -0.37 |             -0.34 |   810.00 |   0.43 |            7.36 |               0.51 |
| RULE top 3 sectors AND top 30% sub-industries, S&P 500 point-in-time only / +20% -10%        |   0.05 |    -0.25 |             -0.24 |   254.00 |   0.45 |            3.25 |               0.72 |
| RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10%                                    |   0.21 |    -0.35 |             -0.30 |   892.00 |   0.42 |            7.06 |               0.70 |
| RULE SPY above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                       |   0.15 |    -0.26 |             -0.23 |   456.00 |   0.45 |            4.60 |               0.62 |
| RULE QQQ above its 21 & 50 SMA, model top 10% / +20% -10%                                    |   0.24 |    -0.30 |             -0.27 |   845.00 |   0.43 |            7.10 |               0.59 |
| RULE QQQ above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                       |   0.17 |    -0.22 |             -0.20 |   442.00 |   0.47 |            4.69 |               0.57 |
| RULE SPY above its 50 SMA (21 either way), model top 10% / +20% -10%                         |   0.17 |    -0.41 |             -0.39 |   929.00 |   0.41 |            7.55 |               0.77 |
| RULE SPY above its 50 SMA (21 either way), S&P 500 point-in-time only / +20% -10%            |   0.15 |    -0.33 |             -0.31 |   509.00 |   0.45 |            5.20 |               0.60 |
| RULE A/D line above its 21 & 50 MA, model top 10% / +20% -10%                                |   0.14 |    -0.55 |             -0.51 |   896.00 |   0.40 |            7.14 |               0.87 |
| RULE A/D line above its 21 & 50 MA, S&P 500 point-in-time only / +20% -10%                   |   0.21 |    -0.20 |             -0.18 |   469.00 |   0.50 |            4.80 |               0.44 |
| RULE > 50% of stocks above their 50d, model top 10% / +20% -10%                              |   0.13 |    -0.38 |             -0.33 |   870.00 |   0.40 |            7.04 |               0.74 |
| RULE > 50% of stocks above their 50d, S&P 500 point-in-time only / +20% -10%                 |   0.14 |    -0.27 |             -0.24 |   487.00 |   0.46 |            5.02 |               0.58 |
| RULE % above 50d rising over 10 days, model top 10% / +20% -10%                              |   0.19 |    -0.33 |             -0.29 |   927.00 |   0.41 |            7.06 |               0.66 |
| RULE % above 50d rising over 10 days, S&P 500 point-in-time only / +20% -10%                 |   0.18 |    -0.26 |             -0.21 |   443.00 |   0.49 |            4.60 |               0.52 |
| RULE sector AND sub-industry green today, model top 10% / +20% -10%                          |   0.22 |    -0.46 |             -0.44 |  1026.00 |   0.43 |            8.50 |               0.79 |
| RULE sector AND sub-industry green today, S&P 500 point-in-time only / +20% -10%             |   0.20 |    -0.24 |             -0.23 |   538.00 |   0.48 |            5.99 |               0.52 |
| RULE sector AND sub-industry up over 5 days, model top 10% / +20% -10%                       |   0.12 |    -0.52 |             -0.51 |   991.00 |   0.40 |            8.26 |               0.94 |
| RULE sector AND sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%          |   0.18 |    -0.39 |             -0.34 |   521.00 |   0.48 |            5.74 |               0.57 |
| RULE sector AND sub-industry above 21 EMA, model top 10% / +20% -10%                         |   0.15 |    -0.49 |             -0.46 |   968.00 |   0.41 |            8.15 |               0.81 |
| RULE sector AND sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%            |   0.18 |    -0.26 |             -0.20 |   457.00 |   0.50 |            4.90 |               0.52 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, model top 10% / +20% -10%              |   0.15 |    -0.36 |             -0.32 |   818.00 |   0.41 |            6.60 |               0.79 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, S&P 500 point-in-time only / +20% -10% |   0.16 |    -0.17 |             -0.13 |   336.00 |   0.50 |            3.67 |               0.49 |
| QULL scan+setups / qull_sma10                                                                |  -0.15 |    -0.77 |             -0.77 |  1130.00 |   0.38 |            3.35 |             nan    |
| QULL scan+setups / qull_sma20                                                                |  -0.11 |    -0.70 |             -0.70 |   989.00 |   0.39 |            4.00 |             nan    |
| QULL scan+setups / sma50_close                                                               |   0.08 |    -0.49 |             -0.38 |   658.00 |   0.20 |            5.57 |               1.22 |
| QULL scan+setups / bracket_20_10                                                             |   0.05 |    -0.38 |             -0.37 |   711.00 |   0.39 |            5.58 |               1.52 |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma10                                   |  -0.08 |    -0.58 |             -0.56 |   743.00 |   0.39 |            2.26 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma10                                             |  -0.06 |    -0.49 |             -0.47 |   838.00 |   0.39 |            2.53 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma20                                   |  -0.03 |    -0.43 |             -0.41 |   665.00 |   0.41 |            2.84 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma20                                             |  -0.01 |    -0.35 |             -0.30 |   742.00 |   0.40 |            3.15 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / sma50_close                                  |   0.17 |    -0.46 |             -0.32 |   465.00 |   0.23 |            4.20 |               0.64 |
| QULL ... + regime + adaptive sizing / sma50_close                                            |   0.14 |    -0.34 |             -0.25 |   482.00 |   0.23 |            4.42 |               0.78 |
| QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20                           |  -0.01 |    -0.29 |             -0.29 |    92.00 |   0.30 |            0.30 |             nan    |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close            |   0.43 |    -0.38 |             -0.32 |   935.00 |   0.32 |            7.19 |               0.47 |
| SURVIVORSHIP S&P 500 names, only after joining the index (3826 signals) / sma50_close        |   0.18 |    -0.41 |             -0.36 |   810.00 |   0.32 |            6.02 |               0.80 |
| WORKFLOW rockets as written (regime sizing) / wf_rocket                                      |   0.02 |    -0.10 |             -0.07 |   189.00 |   0.32 |            2.35 |               0.67 |
| WORKFLOW rockets, no regime rule / wf_rocket                                                 |   0.01 |    -0.10 |             -0.06 |   233.00 |   0.32 |            2.73 |               1.01 |
| WORKFLOW rockets, QQQ 21/50 regime / wf_rocket                                               |   0.00 |    -0.12 |             -0.12 |   203.00 |   0.30 |            2.40 |               8.38 |
| WORKFLOW rockets / sma50_close                                                               |   0.02 |    -0.09 |             -0.07 |   188.00 |   0.32 |            2.35 |               0.60 |
| WORKFLOW rockets / bracket_20_10                                                             |   0.03 |    -0.09 |             -0.08 |   175.00 |   0.43 |            2.41 |               0.85 |
| WORKFLOW BASELINE random entries, rocket filter + regime / wf_rocket                         |   0.00 |    -0.26 |             -0.15 |   478.00 |   0.17 |            2.46 |              11.52 |
| WORKFLOW rockets as written, S&P 500 point-in-time only / wf_rocket                          |  -0.00 |    -0.08 |             -0.06 |   147.00 |   0.27 |            1.90 |             nan    |
| WORKFLOW scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10                 |   0.01 |    -0.17 |             -0.13 |   349.00 |   0.28 |            3.44 |               1.64 |
| WORKFLOW scanner PIT, no regime rule / wf_weekly10                                           |   0.00 |    -0.18 |             -0.16 |   409.00 |   0.30 |            3.93 |              15.72 |
| WORKFLOW scanner PIT, QQQ 21/50 regime / wf_weekly10                                         |  -0.02 |    -0.22 |             -0.20 |   372.00 |   0.27 |            3.48 |             nan    |
| WORKFLOW scanner PIT / sma50_close                                                           |   0.01 |    -0.17 |             -0.15 |   374.00 |   0.29 |            3.39 |               1.18 |
| WORKFLOW BASELINE random entries, scanner filter + regime, PIT / wf_weekly10                 |   0.03 |    -0.17 |             -0.16 |   539.00 |   0.15 |            3.30 |               0.86 |
| WORKFLOW scanner as written, full universe / wf_weekly10                                     |   0.00 |    -0.23 |             -0.20 |   379.00 |   0.25 |            3.40 |              12.76 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY                                 |   0.13 |    -0.39 |             -0.33 |   464.00 |   0.29 |            5.77 |               0.55 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY                                 |   0.16 |    -0.41 |             -0.35 |   368.00 |   0.29 |            4.53 |               0.59 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY                                 |   0.16 |    -0.41 |             -0.35 |   368.00 |   0.29 |            4.53 |               0.59 |
| SPY buy & hold                                                                               |   0.15 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.

Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):

| entry             | filter     | exit            |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_t |
|:------------------|:-----------|:----------------|-------:|----------:|--------:|-----------:|--------:|
| ep_gap10_vol2     | rs80_mkt   | sma50_close     |    208 |      0.62 |     394 |       0.65 |    2.54 |
| ep_gap5           | rs80_early | wf_weekly10     |    324 |      0.61 |     462 |       0.44 |    2.44 |
| ep_gap8_neglected | rs80       | wf_weekly10     |    233 |      0.60 |     324 |       0.55 |    2.38 |
| ep_gap8_hold      | rs80_mkt   | wf_weekly10     |    286 |      0.57 |     418 |       0.48 |    2.00 |
| ep_gap5           | rs80_early | sma50_close     |    324 |      0.57 |     462 |       0.40 |    2.37 |
| ep_gap10_vol2     | rs80_mkt   | chandelier_3atr |    210 |      0.53 |     394 |       0.24 |    1.86 |
| ep_gap8_hold      | rs80_mkt   | sma50_close     |    286 |      0.53 |     418 |       0.47 |    1.99 |
| ep_gap5           | rs80_mkt   | wf_weekly10     |    603 |      0.52 |     736 |       0.32 |    2.09 |
| ep_gap10_vol2     | rs80_mkt   | wf_rocket       |    208 |      0.52 |     394 |       0.52 |    2.68 |
| ep_gap5           | rs80_mkt   | sma50_close     |    603 |      0.51 |     736 |       0.30 |    2.05 |

Year-by-year returns (best 3 portfolios by CAGR vs SPY):

|      |   SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |   REGIME sector & sub-industry today green: skip ['both', 'one of the two'] / +20% -10% |   REGIME sector & sub-industry above 21 EMA: skip ['both', 'one of the two'] / +20% -10% |   SPY |
|-----:|------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------------:|------:|
| 2018 |                                                                                12.3 |                                                                                     8.1 |                                                                                      2.9 |  -5.2 |
| 2019 |                                                                                37.7 |                                                                                    56.6 |                                                                                     17.7 |  31.2 |
| 2020 |                                                                                65.5 |                                                                                   101.9 |                                                                                     67.7 |  18.3 |
| 2021 |                                                                                -4.0 |                                                                                    28.8 |                                                                                     62.9 |  28.7 |
| 2022 |                                                                               -17.1 |                                                                                   -23.4 |                                                                                    -26.7 | -18.2 |
| 2023 |                                                                                81.9 |                                                                                    19.5 |                                                                                     33.7 |  26.2 |
| 2024 |                                                                                59.0 |                                                                                    29.5 |                                                                                     31.2 |  24.9 |
| 2025 |                                                                                63.6 |                                                                                    66.2 |                                                                                     42.2 |  17.7 |
| 2026 |                                                                               144.1 |                                                                                     7.4 |                                                                                     42.6 |  14.4 |

## Appendix: entries and exits

| entry              | source / rule                                                             |   signals |
|:-------------------|:--------------------------------------------------------------------------|----------:|
| donchian_20        | Turtle 20-day breakout / trading-range break (Brock et al. 1992)          |    148839 |
| donchian_55        | Turtle 55-day breakout                                                    |     99185 |
| high52             | 52-week-high breakout (George & Hwang 2004)                               |     59816 |
| high52_fresh       | 52-week high after >= 20 days of consolidation                            |     16711 |
| base_25            | O'Neil/Darvas 5-week base breakout                                        |      4382 |
| base_50            | O'Neil 10-week base breakout                                              |      4968 |
| vcp                | Minervini volatility contraction pattern                                  |      2217 |
| flag_30            | Qullamaggie flag after a 30%+ move                                        |      2954 |
| flag_60            | Qullamaggie flag after a 60%+ move                                        |       960 |
| flag_30_early      | Qullamaggie flag, early entry inside the flag                             |      3162 |
| htf                | High tight flag (O'Neil / Bulkowski)                                      |       152 |
| ep_gap5            | Gap up >= 5% on 3x volume                                                 |      4212 |
| ep_gap10           | Episodic pivot: gap >= 10% on 3x volume                                   |      1477 |
| ep_gap8_neglected  | Episodic pivot from neglect (Qullamaggie)                                 |      1552 |
| ep_gap15           | Episodic pivot: gap >= 15% on 3x volume                                   |       535 |
| ep_gap10_vol2      | EP variant: gap >= 10% on only 2x volume                                  |      1808 |
| ep_gap10_vol5      | EP variant: gap >= 10% on 5x volume                                       |       773 |
| ep_gap8_hold       | EP variant: gap >= 8%, closes above the open                              |      1932 |
| pocket_pivot       | Morales & Kacher pocket pivot                                             |     97934 |
| asc_triangle       | Ascending triangle breakout (flat top, rising lows)                       |      1984 |
| desc_triangle      | Descending triangle, upside breakout                                      |      1490 |
| sym_triangle       | Symmetrical triangle breakout (pennant)                                   |      1811 |
| falling_wedge      | Falling wedge breakout                                                    |      2803 |
| rising_wedge       | Rising wedge, upside breakout                                             |      3846 |
| tight_coil_7       | 7-day coil: closes within 1 ADR, breakout on volume                       |     11860 |
| tight_coil_15      | 15-day coil: closes within 1.5 ADR, breakout on volume                    |      2353 |
| stage2             | Weinstein stage 2 breakout                                                |     10957 |
| ema_retest         | 8/21 EMA cross -> break -> retest (your playbook)                         |     30400 |
| multi_touch        | Multi-touch level breakout on volume (your playbook)                      |     23443 |
| undercut           | Undercut & rally (your playbook)                                          |     49679 |
| qull_breakout      | Qullamaggie breakout: buy-stop above the flag high next day               |      6949 |
| qull_breakout_60   | Qullamaggie breakout after a 60%+ move                                    |      2785 |
| wf_rocket_breakout | Workflow PDF rockets: 6-week base -> 52w high on 1.5x vol, stop -8%       |      4932 |
| wf_rocket_gap      | Workflow PDF rockets: gap >= 5% (2x vol) holding its low 2 days           |      6847 |
| wf_scan_pullback   | Workflow PDF scanner: uptrend pullback to 21EMA/50SMA, close > prior high |    141862 |
| wf_scan_base       | Workflow PDF scanner: uptrend, breakout from a 4-week base                |     57313 |
| random_uptrend     | BASELINE: random entries in an uptrend                                    |     65407 |

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