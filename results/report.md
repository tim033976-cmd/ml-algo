# Strategy research report

Generated 2026-10-09 05:05 UTC in 53 min.
Universe: 1488 stocks with data (sp600: 590, sp500: 499, sp400: 399; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-07: 669,336.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.51). Top 20 by IS t-stat: +0.061R OOS; top 20 by IS avgR (n>=200): +0.322R; all strategies +0.042R; random entries -0.013R.
- Too few signals to judge (need 100+ per period): htf (IS 53, OOS 99).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.30R, OOS +0.27R), ep_gap10_vol5 (IS +0.19R, OOS +0.20R), desc_triangle (IS +0.20R, OOS +0.18R), ep_gap8_hold (IS +0.19R, OOS +0.17R), ep_gap8_neglected (IS +0.21R, OOS +0.15R), ep_gap10 (IS +0.11R, OOS +0.21R), ep_gap5 (IS +0.14R, OOS +0.11R), falling_wedge (IS +0.24R, OOS +0.10R), sym_triangle (IS +0.09R, OOS +0.11R), ep_gap10_vol2 (IS +0.08R, OOS +0.22R), undercut (IS +0.13R, OOS +0.08R), donchian_20 (IS +0.11R, OOS +0.07R), ema_retest (IS +0.10R, OOS +0.06R), flag_60 (IS +0.05R, OOS +0.16R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
- Best exit out-of-sample (avg over entries): sma50_close (+0.109R); worst: qull_sma10 (-0.049R).
- Filters that help OOS: qull_scan_regime (+0.117R), rs80_early (+0.102R), qull_scan (+0.090R), rs80_early_theme (+0.054R), early_stage (+0.046R); that hurt: none.
- ML filter adds little: OOS rank corr 0.005, AUC 0.507, decile monotonicity -0.36, taken +0.080R vs skipped +0.066R.
- Features the model relies on most: sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.06R, OOS +0.03R), rs80_early_theme (IS +0.08R, OOS +0.03R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558` (IS +0.35R, OOS +0.13R, n=30369).
- Superperformer model: 29.8% of its top-10% picks gained >= 40% within 3 months vs 7.1% for all stocks (4.2x), AUC 0.835. Driven by: adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 53% (break-even ~50%), avg net return per trade +0.9%. Point-in-time S&P 500 top 10%: 54%, +1.4% per trade (n=7041).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 37% (break-even ~33%), avg net return per trade +2.4%. Point-in-time S&P 500 top 10%: 39%, +3.6% per trade (n=4335).
- Best portfolio 2018->today: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close at 47.2% CAGR (max drawdown -42.5%) vs SPY 14.5%.
- Best return per unit of drawdown: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close (47.2% CAGR, -42.5% max DD).

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
3. Focus development on: ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60 (tune them on IS data only, re-check OOS).
4. Make qull_scan_regime a default filter.
5. Inspect sma200_slope and adr_pct: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early_theme first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                 | no_edge_entries                                                            | best_exit   | helpful_filters                                                        |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                     | filters_lifting_baseline                  |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                                  |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:------------|:-----------------------------------------------------------------------|---------:|---------------:|---------------:|---------:|:-----------------------------------------------------------------|:------------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:----------------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|
| 2026-10-08 08:48 | 48a9d03  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt              |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank              | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                             |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:11 | fd50739  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt              |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank              | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                             |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:33 | 32c75da  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                             |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:57 | 54a58fb  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                             |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:25 | d8d63d9  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | Only setups in the model's top 10% likely superperformers / sma50_close           |        0.28 |       0.15 | Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)          |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:53 | d8399f4  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 14:02 | 749e984  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |               0.56 |               0.02 |               0.38 |               0.03 |
| 2026-10-08 14:27 | e7af2f7  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |               0.56 |               0.02 |               0.38 |               0.03 |
| 2026-10-08 15:56 | f522ebc  |      1488 |    669685 |        0.51 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage |     0.51 |           0.01 |          -0.04 |     0.04 | sma200_slope, rates_rising, sector_rs, industry_rs, sma150_slope | early_stage, rs80_early, rs80_early_theme |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.46 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.83 |         4.29 | adr_pct, dist_52w_high, above_52w_low, atr_pct, mkt_above200    |               0.55 |               0.01 |               0.37 |               0.02 |
| 2026-10-09 05:05 | 00c2b0a  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                           | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok            | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 3993.000 |
| strategies_with_enough_trades | 3104.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.511 |
| rank_corr_IS_vs_OOS_t         |    0.556 |
| OOS_avgR_all_strategies       |    0.042 |
| OOS_avgR_top20_by_IS          |    0.061 |
| OOS_avgR_top20_by_IS_avgR     |    0.322 |
| OOS_avgR_random_baseline      |   -0.013 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry        | filter      | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-------------|:------------|:--------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| donchian_20  | all         | bracket_20_10 |  68853 |      0.16 |  38.02 |   78126 |      8914.56 |      0.45 |       0.07 |     1.14 |   16.40 |         649.43 |
| pocket_pivot | all         | bracket_20_10 |  48141 |      0.19 |  37.28 |   48061 |      5484.00 |      0.45 |       0.06 |     1.12 |   11.02 |         330.58 |
| pocket_pivot | all         | bracket_10_10 |  48547 |      0.15 |  37.15 |   48061 |      5484.00 |      0.53 |       0.05 |     1.11 |   10.60 |         255.64 |
| donchian_20  | all         | bracket_10_10 |  69295 |      0.13 |  36.32 |   78126 |      8914.56 |      0.53 |       0.05 |     1.11 |   13.49 |         421.85 |
| donchian_20  | mkt_ok      | bracket_20_10 |  57045 |      0.17 |  35.79 |   61637 |      7033.09 |      0.45 |       0.07 |     1.14 |   14.45 |         510.12 |
| donchian_20  | mkt_ok      | bracket_10_10 |  57441 |      0.13 |  33.85 |   61637 |      7033.09 |      0.53 |       0.05 |     1.11 |   11.88 |         331.06 |
| pocket_pivot | mkt_ok      | bracket_20_10 |  35003 |      0.18 |  31.93 |   33711 |      3846.59 |      0.46 |       0.06 |     1.11 |    8.56 |         213.96 |
| pocket_pivot | mkt_ok      | bracket_10_10 |  35353 |      0.15 |  31.68 |   33711 |      3846.59 |      0.53 |       0.05 |     1.11 |    8.70 |         175.61 |
| donchian_55  | all         | bracket_20_10 |  47020 |      0.16 |  31.59 |   50721 |      5787.52 |      0.45 |       0.06 |     1.11 |   10.41 |         327.41 |
| donchian_55  | all         | bracket_10_10 |  47376 |      0.13 |  31.17 |   50721 |      5787.52 |      0.52 |       0.03 |     1.07 |    6.91 |         172.04 |
| donchian_20  | early_stage | bracket_20_10 |  36256 |      0.19 |  30.54 |   47186 |      5384.16 |      0.46 |       0.09 |     1.19 |   16.35 |         511.13 |
| undercut     | all         | bracket_20_10 |  22854 |      0.23 |  29.31 |   26333 |      3004.73 |      0.47 |       0.13 |     1.26 |   16.48 |         381.72 |
| donchian_55  | mkt_ok      | bracket_20_10 |  39875 |      0.16 |  29.02 |   40623 |      4635.29 |      0.45 |       0.06 |     1.12 |    9.86 |         279.03 |
| pocket_pivot | early_stage | bracket_20_10 |  16970 |      0.24 |  28.57 |   18405 |      2100.10 |      0.47 |       0.09 |     1.20 |   10.70 |         198.54 |
| donchian_55  | mkt_ok      | bracket_10_10 |  40192 |      0.13 |  28.29 |   40623 |      4635.29 |      0.53 |       0.03 |     1.07 |    6.81 |         152.53 |
| donchian_20  | early_stage | bracket_10_10 |  36468 |      0.14 |  27.87 |   47186 |      5384.16 |      0.54 |       0.06 |     1.15 |   14.18 |         347.43 |
| pocket_pivot | early_stage | bracket_10_10 |  17120 |      0.19 |  27.84 |   18405 |      2100.10 |      0.54 |       0.06 |     1.14 |    8.50 |         126.29 |
| undercut     | all         | bracket_10_10 |  22983 |      0.17 |  27.35 |   26333 |      3004.73 |      0.55 |       0.09 |     1.21 |   15.03 |         270.80 |
| high52       | all         | bracket_10_10 |  29829 |      0.14 |  26.48 |   29131 |      3323.99 |      0.52 |       0.02 |     1.04 |    3.48 |          65.00 |
| high52       | all         | bracket_20_10 |  29566 |      0.16 |  25.79 |   29131 |      3323.99 |      0.45 |       0.04 |     1.08 |    5.86 |         136.57 |
| donchian_55  | early_stage | bracket_20_10 |  19494 |      0.19 |  24.21 |   23763 |      2711.48 |      0.46 |       0.09 |     1.17 |   10.82 |         234.54 |
| high52       | mkt_ok      | bracket_10_10 |  25367 |      0.13 |  23.66 |   23118 |      2637.88 |      0.52 |       0.03 |     1.06 |    3.99 |          66.72 |
| high52       | mkt_ok      | bracket_20_10 |  25129 |      0.16 |  23.28 |   23118 |      2637.88 |      0.45 |       0.04 |     1.09 |    5.64 |         117.95 |
| donchian_55  | early_stage | bracket_10_10 |  19650 |      0.15 |  22.88 |   23763 |      2711.48 |      0.53 |       0.05 |     1.10 |    7.23 |         123.30 |
| donchian_20  | all         | oneil_20_8    |  69664 |      0.17 |  21.81 |   78126 |      8914.56 |      0.30 |       0.04 |     1.06 |    6.24 |         379.10 |
| ema_retest   | all         | bracket_20_10 |  14308 |      0.19 |  21.04 |   15672 |      1788.25 |      0.46 |       0.08 |     1.16 |    8.05 |         139.59 |
| donchian_20  | early_stage | oneil_20_8    |  36599 |      0.22 |  20.65 |   47186 |      5384.16 |      0.31 |       0.08 |     1.11 |    9.15 |         430.94 |
| ema_retest   | all         | bracket_10_10 |  14409 |      0.15 |  20.10 |   15672 |      1788.25 |      0.53 |       0.05 |     1.11 |    6.09 |          83.67 |
| ema_retest   | mkt_ok      | bracket_20_10 |  12047 |      0.20 |  19.62 |   12390 |      1413.76 |      0.46 |       0.09 |     1.18 |    8.26 |         128.09 |
| donchian_20  | mkt_ok      | oneil_20_8    |  57791 |      0.17 |  19.62 |   61637 |      7033.09 |      0.29 |       0.04 |     1.05 |    5.04 |         274.84 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry          | filter      | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:---------------|:------------|:--------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| donchian_20    | all         | bracket_20_10 |  68853 |      0.16 |  38.02 |   78126 |      0.45 |       0.07 |     1.14 |   16.40 |
| pocket_pivot   | all         | bracket_20_10 |  48141 |      0.19 |  37.28 |   48061 |      0.45 |       0.06 |     1.12 |   11.02 |
| pocket_pivot   | all         | bracket_10_10 |  48547 |      0.15 |  37.15 |   48061 |      0.53 |       0.05 |     1.11 |   10.60 |
| donchian_20    | all         | bracket_10_10 |  69295 |      0.13 |  36.32 |   78126 |      0.53 |       0.05 |     1.11 |   13.49 |
| donchian_20    | mkt_ok      | bracket_20_10 |  57045 |      0.17 |  35.79 |   61637 |      0.45 |       0.07 |     1.14 |   14.45 |
| donchian_20    | mkt_ok      | bracket_10_10 |  57441 |      0.13 |  33.85 |   61637 |      0.53 |       0.05 |     1.11 |   11.88 |
| pocket_pivot   | mkt_ok      | bracket_20_10 |  35003 |      0.18 |  31.93 |   33711 |      0.46 |       0.06 |     1.11 |    8.56 |
| pocket_pivot   | mkt_ok      | bracket_10_10 |  35353 |      0.15 |  31.68 |   33711 |      0.53 |       0.05 |     1.11 |    8.70 |
| donchian_55    | all         | bracket_20_10 |  47020 |      0.16 |  31.59 |   50721 |      0.45 |       0.06 |     1.11 |   10.41 |
| donchian_55    | all         | bracket_10_10 |  47376 |      0.13 |  31.17 |   50721 |      0.52 |       0.03 |     1.07 |    6.91 |
| donchian_20    | early_stage | bracket_20_10 |  36256 |      0.19 |  30.54 |   47186 |      0.46 |       0.09 |     1.19 |   16.35 |
| undercut       | all         | bracket_20_10 |  22854 |      0.23 |  29.31 |   26333 |      0.47 |       0.13 |     1.26 |   16.48 |
| random_uptrend | all         | bracket_20_10 |  30366 |      0.19 |  29.07 |   34140 |      0.46 |       0.10 |     1.20 |   14.93 |
| donchian_55    | mkt_ok      | bracket_20_10 |  39875 |      0.16 |  29.02 |   40623 |      0.45 |       0.06 |     1.12 |    9.86 |
| pocket_pivot   | early_stage | bracket_20_10 |  16970 |      0.24 |  28.57 |   18405 |      0.47 |       0.09 |     1.20 |   10.70 |
| donchian_55    | mkt_ok      | bracket_10_10 |  40192 |      0.13 |  28.29 |   40623 |      0.53 |       0.03 |     1.07 |    6.81 |
| random_uptrend | all         | bracket_10_10 |  30549 |      0.15 |  27.98 |   34140 |      0.54 |       0.07 |     1.16 |   13.10 |
| donchian_20    | early_stage | bracket_10_10 |  36468 |      0.14 |  27.87 |   47186 |      0.54 |       0.06 |     1.15 |   14.18 |
| pocket_pivot   | early_stage | bracket_10_10 |  17120 |      0.19 |  27.84 |   18405 |      0.54 |       0.06 |     1.14 |    8.50 |
| undercut       | all         | bracket_10_10 |  22983 |      0.17 |  27.35 |   26333 |      0.55 |       0.09 |     1.21 |   15.03 |
| high52         | all         | bracket_10_10 |  29829 |      0.14 |  26.48 |   29131 |      0.52 |       0.02 |     1.04 |    3.48 |
| high52         | all         | bracket_20_10 |  29566 |      0.16 |  25.79 |   29131 |      0.45 |       0.04 |     1.08 |    5.86 |
| donchian_55    | early_stage | bracket_20_10 |  19494 |      0.19 |  24.21 |   23763 |      0.46 |       0.09 |     1.17 |   10.82 |
| random_uptrend | mkt_ok      | bracket_20_10 |  20481 |      0.19 |  24.03 |   23145 |      0.46 |       0.10 |     1.20 |   11.95 |
| high52         | mkt_ok      | bracket_10_10 |  25367 |      0.13 |  23.66 |   23118 |      0.52 |       0.03 |     1.06 |    3.99 |
| high52         | mkt_ok      | bracket_20_10 |  25129 |      0.16 |  23.28 |   23118 |      0.45 |       0.04 |     1.09 |    5.64 |
| random_uptrend | mkt_ok      | bracket_10_10 |  20648 |      0.15 |  23.08 |   23145 |      0.54 |       0.07 |     1.15 |   10.23 |
| donchian_55    | early_stage | bracket_10_10 |  19650 |      0.15 |  22.88 |   23763 |      0.53 |       0.05 |     1.10 |    7.23 |
| random_uptrend | early_stage | bracket_20_10 |  10848 |      0.24 |  22.29 |   13192 |      0.47 |       0.12 |     1.25 |   11.43 |
| donchian_20    | all         | oneil_20_8    |  69664 |      0.17 |  21.81 |   78126 |      0.30 |       0.04 |     1.06 |    6.24 |

## 4. Each entry with its best in-sample exit/filter

| entry             | filter           | exit          |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------------|:-----------------|:--------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| qull_breakout_60  | early_stage      | bracket_20_10 |    310 |       25.85 |     0.40 |      0.13 |   1.52 |     749 |        85.46 |      0.46 |       0.31 |     1.55 |    5.61 |          26.08 |
| qull_breakout     | early_stage      | bracket_20_10 |    759 |       63.28 |     0.41 |      0.13 |   2.41 |    1510 |       172.30 |      0.44 |       0.23 |     1.41 |    6.16 |          39.86 |
| ep_gap15          | rs80_mkt         | bracket_20_10 |     62 |        5.17 |     0.56 |      0.58 |   3.26 |     140 |        15.97 |      0.44 |       0.21 |     1.36 |    1.70 |           3.29 |
| flag_30           | rs80_early_theme | bracket_20_10 |    160 |       13.34 |     0.47 |      0.27 |   2.42 |     238 |        27.16 |      0.42 |       0.18 |     1.30 |    1.86 |           4.80 |
| falling_wedge     | all              | bracket_20_10 |   1255 |      104.63 |     0.58 |      0.30 |   9.23 |    1522 |       173.67 |      0.48 |       0.16 |     1.33 |    4.93 |          26.94 |
| ep_gap10_vol2     | rs80_mkt         | bracket_20_10 |    206 |       17.17 |     0.48 |      0.26 |   2.72 |     394 |        44.96 |      0.42 |       0.15 |     1.26 |    2.07 |           6.58 |
| undercut          | all              | bracket_20_10 |  22854 |     1905.37 |     0.54 |      0.23 |  29.31 |   26333 |      3004.73 |      0.47 |       0.13 |     1.26 |   16.48 |         381.72 |
| ep_gap10          | rs80_mkt         | bracket_20_10 |    189 |       15.76 |     0.50 |      0.33 |   3.22 |     337 |        38.45 |      0.41 |       0.12 |     1.22 |    1.63 |           4.74 |
| desc_triangle     | all              | bracket_20_10 |    765 |       63.78 |     0.57 |      0.24 |   6.11 |     705 |        80.44 |      0.48 |       0.12 |     1.26 |    2.64 |           9.45 |
| ep_gap8_hold      | all              | bracket_20_10 |    733 |       61.11 |     0.48 |      0.21 |   4.22 |    1182 |       134.87 |      0.42 |       0.11 |     1.20 |    2.86 |          15.48 |
| random_uptrend    | all              | bracket_20_10 |  30366 |     2531.66 |     0.53 |      0.19 |  29.07 |   34140 |      3895.54 |      0.46 |       0.10 |     1.20 |   14.93 |         392.63 |
| base_25           | mkt_ok           | bracket_20_10 |   1476 |      123.06 |     0.46 |      0.14 |   4.04 |    1879 |       214.40 |      0.42 |       0.09 |     1.15 |    2.77 |          18.75 |
| ep_gap10_vol5     | rs80             | bracket_10_10 |    197 |       16.42 |     0.63 |      0.25 |   3.66 |     291 |        33.20 |      0.55 |       0.08 |     1.19 |    1.43 |           2.74 |
| ep_gap8_neglected | all              | bracket_20_10 |    604 |       50.36 |     0.50 |      0.24 |   4.49 |     934 |       106.57 |      0.41 |       0.08 |     1.14 |    1.84 |           8.73 |
| ema_retest        | all              | bracket_20_10 |  14308 |     1192.88 |     0.55 |      0.19 |  21.04 |   15672 |      1788.25 |      0.46 |       0.08 |     1.16 |    8.05 |         139.59 |
| sym_triangle      | all              | bracket_10_10 |    882 |       73.53 |     0.58 |      0.13 |   4.11 |     917 |       104.63 |      0.55 |       0.08 |     1.18 |    2.42 |           8.07 |
| donchian_20       | all              | bracket_20_10 |  68853 |     5740.37 |     0.52 |      0.16 |  38.02 |   78126 |      8914.56 |      0.45 |       0.07 |     1.14 |   16.40 |         649.43 |
| flag_60           | rs80_theme       | bracket_20_10 |    165 |       13.76 |     0.45 |      0.28 |   2.43 |     294 |        33.55 |      0.37 |       0.07 |     1.11 |    0.82 |           2.43 |
| asc_triangle      | all              | bracket_20_10 |   1075 |       89.62 |     0.57 |      0.19 |   6.07 |     860 |        98.13 |      0.47 |       0.07 |     1.14 |    1.64 |           6.41 |
| pocket_pivot      | all              | bracket_20_10 |  48141 |     4013.58 |     0.54 |      0.19 |  37.28 |   48061 |      5484.00 |      0.45 |       0.06 |     1.12 |   11.02 |         330.58 |
| donchian_55       | all              | bracket_20_10 |  47020 |     3920.12 |     0.53 |      0.16 |  31.59 |   50721 |      5787.52 |      0.45 |       0.06 |     1.11 |   10.41 |         327.41 |
| vcp               | all              | bracket_20_10 |   1299 |      108.30 |     0.54 |      0.16 |   5.47 |     880 |       100.41 |      0.46 |       0.05 |     1.11 |    1.36 |           5.39 |
| flag_30_early     | mkt_ok           | bracket_10_10 |    847 |       70.62 |     0.56 |      0.10 |   2.92 |    1446 |       165.00 |      0.52 |       0.05 |     1.10 |    1.70 |           7.68 |
| high52_fresh      | all              | bracket_10_10 |   8097 |      675.06 |     0.61 |      0.16 |  16.73 |    8423 |       961.11 |      0.53 |       0.03 |     1.07 |    3.00 |          30.23 |
| base_50           | all              | bracket_10_10 |   2289 |      190.84 |     0.56 |      0.10 |   4.89 |    2666 |       304.20 |      0.52 |       0.02 |     1.05 |    1.19 |           7.05 |
| ep_gap5           | all              | bracket_10_10 |   1867 |      155.65 |     0.57 |      0.12 |   5.43 |    2322 |       264.95 |      0.52 |       0.02 |     1.05 |    1.06 |           5.93 |
| high52            | all              | bracket_10_10 |  29829 |     2486.88 |     0.59 |      0.14 |  26.48 |   29131 |      3323.99 |      0.52 |       0.02 |     1.04 |    3.48 |          65.00 |
| rising_wedge      | all              | bracket_10_10 |   2065 |      172.16 |     0.58 |      0.13 |   6.46 |    1730 |       197.40 |      0.52 |       0.02 |     1.04 |    0.82 |           3.71 |
| tight_coil_7      | all              | bracket_10_10 |   6285 |      523.99 |     0.59 |      0.15 |  13.44 |    5356 |       611.15 |      0.51 |       0.01 |     1.03 |    0.98 |           7.97 |
| multi_touch       | all              | bracket_10_10 |  12466 |     1039.31 |     0.59 |      0.14 |  16.93 |   10634 |      1213.39 |      0.51 |      -0.00 |     1.00 |   -0.13 |          -1.48 |
| stage2            | all              | bracket_10_10 |   5907 |      492.47 |     0.61 |      0.18 |  15.78 |    4847 |       553.07 |      0.51 |      -0.00 |     0.99 |   -0.29 |          -2.19 |
| tight_coil_15     | all              | bracket_10_10 |   1263 |      105.30 |     0.60 |      0.15 |   6.02 |    1039 |       118.56 |      0.49 |      -0.02 |     0.96 |   -0.61 |          -2.16 |
| htf               | all              | sma50_close   |     53 |        4.42 |     0.17 |      0.39 |   0.63 |      99 |        11.30 |      0.11 |      -0.34 |     0.65 |   -1.17 |          -3.85 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry             |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |           -0.04 |           -0.04 |              0.05 |             0.06 |          0.03 |           0.10 |         0.05 |         0.04 |         0.02 |         -0.00 |       0.10 |
| base_25           |           -0.03 |            0.01 |              0.10 |             0.08 |          0.09 |           0.08 |         0.09 |         0.04 |         0.07 |          0.22 |       0.13 |
| base_50           |           -0.05 |           -0.01 |              0.14 |             0.10 |          0.13 |           0.11 |         0.11 |         0.07 |         0.10 |          0.21 |       0.15 |
| desc_triangle     |            0.02 |            0.02 |              0.27 |             0.26 |          0.23 |           0.23 |         0.29 |         0.16 |         0.21 |          0.07 |       0.20 |
| donchian_20       |           -0.02 |           -0.03 |              0.09 |             0.08 |          0.10 |           0.12 |         0.08 |         0.08 |         0.09 |          0.06 |       0.12 |
| donchian_55       |           -0.04 |           -0.04 |              0.06 |             0.05 |          0.07 |           0.09 |         0.06 |         0.06 |         0.06 |          0.06 |       0.11 |
| ema_retest        |           -0.02 |           -0.02 |              0.06 |             0.05 |          0.07 |           0.10 |         0.08 |         0.07 |         0.06 |          0.07 |       0.11 |
| ep_gap10          |           -0.04 |            0.01 |              0.24 |             0.35 |          0.27 |           0.20 |         0.15 |         0.11 |         0.18 |          0.51 |       0.32 |
| ep_gap10_vol2     |           -0.04 |            0.05 |              0.30 |             0.36 |          0.27 |           0.19 |         0.20 |         0.13 |         0.18 |          0.50 |       0.31 |
| ep_gap10_vol5     |           -0.07 |            0.02 |              0.25 |             0.33 |          0.23 |           0.21 |         0.12 |         0.10 |         0.12 |          0.53 |       0.34 |
| ep_gap15          |            0.01 |            0.11 |              0.30 |             0.34 |          0.28 |           0.26 |         0.27 |         0.12 |         0.16 |          0.74 |       0.39 |
| ep_gap5           |           -0.05 |           -0.02 |              0.14 |             0.17 |          0.15 |           0.13 |         0.09 |         0.09 |         0.11 |          0.20 |       0.16 |
| ep_gap8_hold      |           -0.03 |            0.01 |              0.18 |             0.27 |          0.22 |           0.17 |         0.14 |         0.10 |         0.14 |          0.40 |       0.26 |
| ep_gap8_neglected |           -0.04 |           -0.02 |              0.13 |             0.18 |          0.22 |           0.19 |         0.18 |         0.10 |         0.13 |          0.29 |       0.24 |
| falling_wedge     |            0.03 |            0.05 |              0.18 |             0.14 |          0.10 |           0.19 |         0.20 |         0.06 |         0.09 |          0.02 |       0.08 |
| flag_30           |           -0.05 |            0.02 |              0.05 |             0.12 |          0.13 |           0.07 |         0.03 |         0.07 |         0.07 |          0.27 |       0.15 |
| flag_30_early     |           -0.01 |            0.08 |              0.16 |             0.15 |          0.15 |           0.15 |         0.20 |         0.13 |         0.13 |          0.23 |       0.18 |
| flag_60           |           -0.07 |            0.06 |              0.17 |             0.15 |          0.18 |           0.10 |         0.10 |         0.12 |         0.11 |          0.51 |       0.31 |
| high52            |           -0.05 |           -0.06 |             -0.05 |            -0.05 |         -0.03 |          -0.02 |        -0.04 |        -0.03 |        -0.04 |         -0.05 |      -0.02 |
| high52_fresh      |           -0.04 |           -0.05 |              0.05 |             0.04 |          0.08 |           0.06 |         0.05 |         0.04 |         0.04 |          0.07 |       0.08 |
| htf               |           -0.26 |           -0.17 |             -0.20 |            -0.30 |         -0.13 |          -0.14 |        -0.18 |        -0.01 |        -0.09 |         -0.32 |      -0.07 |
| multi_touch       |           -0.07 |           -0.09 |             -0.04 |            -0.01 |         -0.02 |           0.01 |        -0.04 |         0.01 |        -0.01 |         -0.07 |      -0.01 |
| pocket_pivot      |           -0.02 |           -0.04 |             -0.03 |            -0.03 |         -0.01 |           0.01 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.00 |
| qull_breakout     |           -0.03 |            0.05 |             -0.09 |            -0.09 |         -0.07 |          -0.13 |        -0.10 |        -0.14 |        -0.12 |          0.04 |      -0.08 |
| qull_breakout_60  |           -0.02 |            0.10 |             -0.09 |            -0.09 |         -0.05 |          -0.11 |        -0.06 |        -0.14 |        -0.11 |          0.14 |      -0.07 |
| rising_wedge      |           -0.05 |           -0.06 |             -0.04 |            -0.05 |         -0.02 |           0.05 |         0.02 |         0.08 |         0.04 |         -0.07 |       0.01 |
| stage2            |           -0.07 |           -0.09 |             -0.08 |            -0.07 |         -0.06 |          -0.01 |        -0.08 |        -0.02 |        -0.04 |         -0.11 |      -0.05 |
| sym_triangle      |            0.01 |            0.00 |              0.19 |             0.12 |          0.13 |           0.18 |         0.16 |         0.13 |         0.15 |          0.03 |       0.10 |
| tight_coil_15     |           -0.09 |           -0.11 |             -0.01 |            -0.03 |          0.00 |           0.06 |        -0.01 |         0.06 |         0.04 |         -0.10 |       0.03 |
| tight_coil_7      |           -0.06 |           -0.07 |              0.01 |             0.01 |          0.04 |           0.08 |         0.03 |         0.07 |         0.05 |         -0.02 |       0.07 |
| undercut          |            0.02 |            0.03 |              0.17 |             0.16 |          0.03 |           0.09 |         0.12 |         0.09 |         0.09 |         -0.01 |       0.03 |
| vcp               |           -0.02 |           -0.05 |              0.05 |             0.04 |          0.04 |           0.11 |         0.04 |         0.07 |         0.07 |         -0.06 |       0.05 |

Same, in-sample:

| entry             |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |            0.01 |            0.00 |              0.03 |             0.01 |          0.05 |           0.07 |         0.06 |         0.06 |         0.04 |         -0.02 |       0.09 |
| base_25           |           -0.07 |           -0.07 |             -0.02 |            -0.02 |          0.01 |           0.07 |        -0.05 |         0.08 |         0.06 |          0.05 |       0.10 |
| base_50           |           -0.04 |           -0.06 |              0.01 |             0.03 |          0.05 |           0.14 |        -0.02 |         0.10 |         0.07 |         -0.01 |       0.11 |
| desc_triangle     |            0.04 |            0.05 |              0.21 |             0.34 |          0.18 |           0.23 |         0.25 |         0.19 |         0.19 |          0.27 |       0.29 |
| donchian_20       |           -0.02 |           -0.03 |              0.11 |             0.13 |          0.15 |           0.16 |         0.11 |         0.12 |         0.12 |          0.14 |       0.19 |
| donchian_55       |           -0.02 |           -0.03 |              0.09 |             0.11 |          0.13 |           0.13 |         0.09 |         0.10 |         0.10 |          0.12 |       0.18 |
| ema_retest        |            0.00 |            0.01 |              0.10 |             0.11 |          0.14 |           0.12 |         0.17 |         0.07 |         0.08 |          0.17 |       0.15 |
| ep_gap10          |           -0.03 |           -0.00 |              0.16 |             0.13 |          0.16 |           0.11 |        -0.03 |         0.15 |         0.11 |          0.20 |       0.24 |
| ep_gap10_vol2     |           -0.05 |           -0.04 |              0.14 |             0.09 |          0.13 |           0.10 |        -0.03 |         0.12 |         0.09 |          0.15 |       0.20 |
| ep_gap10_vol5     |            0.03 |            0.05 |              0.23 |             0.20 |          0.19 |           0.21 |         0.04 |         0.24 |         0.19 |          0.32 |       0.34 |
| ep_gap15          |            0.06 |            0.12 |              0.44 |             0.34 |          0.34 |           0.31 |         0.13 |         0.33 |         0.31 |          0.46 |       0.49 |
| ep_gap5           |           -0.02 |           -0.03 |              0.18 |             0.15 |          0.18 |           0.15 |         0.10 |         0.15 |         0.15 |          0.27 |       0.24 |
| ep_gap8_hold      |           -0.01 |            0.02 |              0.25 |             0.25 |          0.25 |           0.18 |         0.14 |         0.17 |         0.17 |          0.31 |       0.33 |
| ep_gap8_neglected |            0.01 |            0.05 |              0.26 |             0.27 |          0.26 |           0.19 |         0.20 |         0.17 |         0.20 |          0.34 |       0.31 |
| falling_wedge     |            0.07 |            0.11 |              0.34 |             0.38 |          0.24 |           0.31 |         0.40 |         0.22 |         0.24 |          0.15 |       0.21 |
| flag_30           |           -0.14 |           -0.14 |             -0.08 |            -0.08 |         -0.04 |           0.05 |        -0.10 |         0.03 |        -0.01 |         -0.07 |       0.02 |
| flag_30_early     |           -0.09 |           -0.11 |              0.11 |             0.08 |          0.11 |           0.05 |        -0.03 |         0.06 |         0.10 |         -0.01 |       0.03 |
| flag_60           |           -0.13 |           -0.10 |              0.06 |             0.05 |          0.10 |           0.12 |        -0.00 |         0.15 |         0.11 |          0.10 |       0.13 |
| high52            |           -0.01 |           -0.03 |             -0.03 |            -0.02 |          0.03 |           0.02 |        -0.02 |        -0.01 |        -0.01 |         -0.01 |       0.01 |
| high52_fresh      |            0.02 |            0.01 |              0.06 |             0.08 |          0.10 |           0.08 |         0.08 |         0.05 |         0.06 |          0.09 |       0.10 |
| htf               |           -0.23 |           -0.17 |             -0.08 |             0.26 |          0.14 |           0.06 |        -0.09 |         0.13 |         0.20 |          0.44 |       0.28 |
| multi_touch       |           -0.01 |           -0.02 |              0.07 |             0.11 |          0.13 |           0.11 |         0.11 |         0.08 |         0.07 |          0.14 |       0.12 |
| pocket_pivot      |            0.01 |           -0.00 |              0.06 |             0.08 |          0.08 |           0.04 |         0.06 |         0.04 |         0.04 |          0.09 |       0.06 |
| qull_breakout     |           -0.16 |           -0.18 |             -0.33 |            -0.32 |         -0.25 |          -0.20 |        -0.36 |        -0.17 |        -0.20 |         -0.34 |      -0.22 |
| qull_breakout_60  |           -0.15 |           -0.18 |             -0.26 |            -0.28 |         -0.22 |          -0.23 |        -0.35 |        -0.15 |        -0.18 |         -0.29 |      -0.19 |
| rising_wedge      |           -0.02 |           -0.04 |              0.02 |             0.04 |          0.08 |           0.09 |         0.01 |         0.06 |         0.05 |          0.06 |       0.12 |
| stage2            |            0.03 |            0.02 |              0.11 |             0.15 |          0.17 |           0.12 |         0.17 |         0.09 |         0.11 |          0.17 |       0.16 |
| sym_triangle      |           -0.01 |           -0.04 |              0.10 |             0.13 |          0.14 |           0.12 |         0.04 |         0.13 |         0.11 |          0.11 |       0.14 |
| tight_coil_15     |            0.01 |           -0.01 |              0.15 |             0.20 |          0.15 |           0.16 |         0.17 |         0.14 |         0.14 |          0.15 |       0.25 |
| tight_coil_7      |            0.01 |           -0.01 |              0.13 |             0.19 |          0.16 |           0.16 |         0.13 |         0.12 |         0.11 |          0.18 |       0.24 |
| undercut          |            0.02 |            0.04 |              0.22 |             0.25 |          0.06 |           0.13 |         0.21 |         0.19 |         0.18 |          0.03 |       0.09 |
| vcp               |           -0.01 |           -0.03 |              0.08 |             0.11 |          0.13 |           0.14 |         0.11 |         0.11 |         0.10 |          0.11 |       0.18 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| sma50_close     |      0.07 |       0.11 |      0.26 |     1.16 |                       0.66 |
| bracket_20_10   |      0.16 |       0.09 |      0.43 |     1.17 |                       0.47 |
| oneil_20_8      |      0.11 |       0.03 |      0.26 |     1.05 |                       0.75 |
| bracket_10_10   |      0.12 |       0.03 |      0.52 |     1.07 |                       0.16 |
| trim_ema        |      0.00 |       0.01 |      0.34 |     1.03 |                       0.78 |
| donchian_10low  |      0.02 |       0.01 |      0.28 |     1.03 |                       0.72 |
| chandelier_3atr |      0.02 |      -0.00 |      0.29 |     1.01 |                       0.72 |
| fixed_3r_20d    |     -0.01 |      -0.01 |      0.36 |     0.99 |                       0.84 |
| ema21_close     |     -0.04 |      -0.02 |      0.29 |     0.98 |                       0.75 |
| qull_sma20      |     -0.05 |      -0.04 |      0.42 |     0.94 |                       0.78 |
| qull_sma10      |     -0.05 |      -0.05 |      0.42 |     0.91 |                       0.84 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| qull_scan_regime |     -0.02 |       0.13 |      0.36 |
| rs80_early       |      0.07 |       0.12 |      0.37 |
| qull_scan        |     -0.03 |       0.10 |      0.35 |
| rs80_early_theme |      0.08 |       0.07 |      0.36 |
| early_stage      |      0.06 |       0.06 |      0.36 |
| rs80             |      0.04 |       0.04 |      0.36 |
| rs80_mkt         |      0.06 |       0.03 |      0.35 |
| rs80_theme       |      0.03 |       0.02 |      0.36 |
| all              |      0.03 |       0.01 |      0.35 |
| theme            |      0.03 |       0.01 |      0.36 |
| mkt_ok           |      0.04 |       0.01 |      0.35 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.005; AUC for R > 0: 0.507 (0.5 = no skill). Taken (model's top third, causal threshold): n=84,571, avgR=0.080, win=0.459. Skipped: n=223,581, avgR=0.066, win=0.445.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 30817.00 |   0.09 |  0.44 |
|      1 | 30814.00 |   0.08 |  0.44 |
|      2 | 30815.00 |   0.06 |  0.44 |
|      3 | 30815.00 |   0.08 |  0.45 |
|      4 | 30815.00 |   0.06 |  0.45 |
|      5 | 30815.00 |   0.07 |  0.45 |
|      6 | 30815.00 |   0.05 |  0.45 |
|      7 | 30816.00 |   0.04 |  0.44 |
|      8 | 30814.00 |   0.06 |  0.45 |
|      9 | 30816.00 |   0.10 |  0.47 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| ep_gap15          |   374.00 |       0.21 |    179.00 |         0.31 |           0.12 |
| ep_gap8_hold      |  1182.00 |       0.11 |    451.00 |         0.21 |           0.05 |
| ep_gap8_neglected |   934.00 |       0.08 |    345.00 |         0.21 |           0.01 |
| flag_30           |  1790.00 |       0.12 |    443.00 |         0.20 |           0.09 |
| ep_gap10_vol2     |  1181.00 |       0.15 |    469.00 |         0.19 |           0.12 |
| qull_breakout_60  |  1865.00 |       0.20 |    451.00 |         0.18 |           0.20 |
| falling_wedge     |  1522.00 |       0.16 |    601.00 |         0.17 |           0.15 |
| flag_60           |   618.00 |       0.16 |    163.00 |         0.17 |           0.16 |
| ep_gap10          |   933.00 |       0.11 |    379.00 |         0.17 |           0.07 |
| ep_gap5           |  2322.00 |       0.08 |    881.00 |         0.17 |           0.03 |
| base_25           |  2445.00 |       0.11 |    683.00 |         0.16 |           0.09 |
| undercut          | 26333.00 |       0.13 |   9897.00 |         0.16 |           0.11 |
| ep_gap10_vol5     |   454.00 |       0.12 |    209.00 |         0.15 |           0.09 |
| qull_breakout     |  4386.00 |       0.15 |   1056.00 |         0.14 |           0.15 |
| desc_triangle     |   705.00 |       0.12 |    241.00 |         0.12 |           0.11 |
| vcp               |   880.00 |       0.05 |    220.00 |         0.12 |           0.03 |
| base_50           |  2666.00 |       0.09 |    749.00 |         0.11 |           0.09 |
| flag_30_early     |  1946.00 |       0.19 |    442.00 |         0.10 |           0.21 |
| sym_triangle      |   917.00 |       0.10 |    256.00 |         0.09 |           0.11 |
| ema_retest        | 15672.00 |       0.08 |   4261.00 |         0.08 |           0.08 |
| tight_coil_15     |  1039.00 |      -0.01 |    295.00 |         0.07 |          -0.04 |
| rising_wedge      |  1730.00 |       0.04 |    476.00 |         0.07 |           0.03 |
| high52            | 29131.00 |       0.04 |   6745.00 |         0.07 |           0.03 |
| pocket_pivot      | 48061.00 |       0.06 |  12879.00 |         0.07 |           0.06 |
| high52_fresh      |  8423.00 |       0.05 |   2276.00 |         0.06 |           0.05 |
| donchian_55       | 50721.00 |       0.06 |  12551.00 |         0.06 |           0.05 |
| donchian_20       | 78126.00 |       0.07 |  20794.00 |         0.05 |           0.08 |
| multi_touch       | 10634.00 |       0.01 |   2911.00 |         0.05 |          -0.01 |
| stage2            |  4847.00 |       0.01 |   1550.00 |         0.04 |          -0.01 |
| tight_coil_7      |  5356.00 |       0.03 |   1442.00 |         0.02 |           0.04 |
| asc_triangle      |   860.00 |       0.07 |    249.00 |        -0.05 |           0.11 |
| htf               |    99.00 |      -0.07 |     27.00 |        -0.07 |          -0.07 |

- Same model on episodic pivots only / sma50_close: rank corr 0.012, taken avgR 0.425 (n=3,153) vs skipped 0.302 (n=4,227).
- Same model on your trim plan (trim_ema): rank corr 0.126, taken avgR 0.012 (n=92,507) vs skipped -0.061 (n=215,645).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature       |   rank_corr_drop |
|:--------------|-----------------:|
| sma200_slope  |           0.0059 |
| adr_pct       |           0.0053 |
| above_52w_low |           0.0051 |
| rs_rank       |           0.0046 |
| mkt_ok        |           0.0041 |
| rates_rising  |           0.0037 |
| industry_rs   |           0.0037 |
| sma150_slope  |           0.0030 |
| mkt_ema_stack |           0.0028 |
| mkt_above200  |           0.0022 |
| base_count    |           0.0021 |
| sector_rs     |           0.0020 |
| gap           |           0.0015 |
| atr_ratio     |           0.0012 |
| qqq_trend     |           0.0011 |
| risk_pct      |           0.0008 |
| risk_adr      |           0.0006 |
| higher_lows   |           0.0006 |
| tight_10      |           0.0005 |
| industry_rank |           0.0005 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.558    |   8089 |      0.64 |   11872 |       0.08 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558   |  17883 |      0.35 |   30369 |       0.13 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.483 |  67656 |      0.29 |   53743 |       0.00 |      0.46 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 > 0.779    |   4247 |      0.28 |     441 |       0.98 |      0.72 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.483  |  52699 |      0.17 |   38632 |      -0.01 |      0.40 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 <= 0.0455   |  74580 |      0.16 |  105769 |       0.09 |      0.45 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 > 0.0455    |  41492 |      0.01 |   61996 |       0.09 |      0.44 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 <= 0.779   |  20364 |     -0.18 |    5330 |       0.22 |      0.47 |

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
| low          | 102718.000 | -0.001 | 0.475 |       -0.101 |
| mid          | 102717.000 |  0.061 | 0.448 |       -0.075 |
| high         | 102717.000 |  0.150 | 0.423 |        0.191 |

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

| strategy                                                                              |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:--------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| donchian_20 / all / bracket_20_10                                                     |   0.09 |    -0.44 |             -0.42 |   792.00 |   0.41 |            9.29 |               0.98 |
| pocket_pivot / all / bracket_20_10                                                    |   0.07 |    -0.35 |             -0.31 |   574.00 |   0.41 |            7.27 |               0.63 |
| donchian_55 / all / bracket_20_10                                                     |   0.01 |    -0.41 |             -0.38 |   747.00 |   0.40 |            9.09 |               4.43 |
| undercut / all / bracket_20_10                                                        |   0.14 |    -0.36 |             -0.30 |   591.00 |   0.43 |            7.61 |               0.77 |
| high52 / all / bracket_10_10                                                          |  -0.03 |    -0.54 |             -0.52 |  1011.00 |   0.51 |            7.53 |             nan    |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                     |   0.07 |    -0.35 |             -0.33 |   666.00 |   0.42 |            8.46 |               0.65 |
| All setups, ranked by RS / bracket_20_10                                              |   0.15 |    -0.36 |             -0.34 |  1080.00 |   0.40 |            9.03 |               0.60 |
| All setups, random order / bracket_20_10                                              |   0.07 |    -0.41 |             -0.40 |   547.00 |   0.44 |            8.45 |               0.86 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                          |   0.09 |    -0.33 |             -0.32 |   807.00 |   0.40 |            8.62 |               0.71 |
| BASELINE random entries, ranked by RS / bracket_20_10                                 |   0.04 |    -0.51 |             -0.47 |   689.00 |   0.40 |            7.64 |               1.59 |
| BASELINE random entries, random order / bracket_20_10                                 |   0.05 |    -0.38 |             -0.35 |   424.00 |   0.45 |            7.13 |               1.23 |
| IS-selected setups (4), ranked by RS / bracket_20_10                                  |  -0.02 |    -0.51 |             -0.49 |   528.00 |   0.40 |            8.15 |             nan    |
| IS-selected setups, only when SPY > 200d / bracket_20_10                              |  -0.04 |    -0.51 |             -0.49 |   428.00 |   0.39 |            7.01 |             nan    |
| IS-selected setups (22), ranked by RS / sma50_close                                   |   0.13 |    -0.52 |             -0.43 |   922.00 |   0.25 |            8.85 |               0.54 |
| IS-selected setups, only when SPY > 200d / sma50_close                                |   0.09 |    -0.51 |             -0.46 |   777.00 |   0.24 |            7.63 |               0.84 |
| All setups, ranked by RS / sma50_close                                                |   0.14 |    -0.53 |             -0.48 |  1188.00 |   0.26 |            8.71 |               0.67 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                           |   0.10 |    -0.33 |             -0.25 |   444.00 |   0.30 |            5.63 |               0.68 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                          |   0.11 |    -0.26 |             -0.15 |   606.00 |   0.34 |            7.51 |               0.52 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                          |   0.15 |    -0.27 |             -0.20 |   627.00 |   0.33 |            7.81 |               0.54 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)              |   0.15 |    -0.22 |             -0.18 |   632.00 |   0.34 |            7.95 |               0.45 |
| Top 20 by IS expectancy, ranked by superperformer model                               |   0.13 |    -0.26 |             -0.21 |   682.00 |   0.31 |            7.81 |               0.63 |
| All setups, ranked by superperformer model / bracket_20_10                            |   0.25 |    -0.41 |             -0.41 |  1353.00 |   0.41 |            9.08 |               0.60 |
| Only setups in the model's top 10% likely superperformers / sma50_close               |   0.11 |    -0.61 |             -0.50 |  1428.00 |   0.29 |            8.55 |               1.12 |
| CHECK random entries in the model's top 10% / sma50_close                             |   0.08 |    -0.54 |             -0.47 |   979.00 |   0.15 |            5.30 |               1.07 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close              |   0.09 |    -0.60 |             -0.53 |  1336.00 |   0.28 |            8.42 |               1.16 |
| Top 10% model + adaptive sizing / sma50_close                                         |   0.08 |    -0.51 |             -0.41 |  1487.00 |   0.30 |            9.27 |               1.25 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                  |   0.16 |    -0.39 |             -0.35 |  1350.00 |   0.29 |            8.84 |               0.66 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                     |   0.21 |    -0.61 |             -0.59 |  1216.00 |   0.41 |            9.41 |               0.70 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                             |   0.19 |    -0.51 |             -0.49 |  1189.00 |   0.40 |            9.14 |               0.75 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                               |   0.11 |    -0.50 |             -0.48 |  1006.00 |   0.40 |            8.71 |               0.70 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                   |   0.12 |    -0.35 |             -0.33 |   780.00 |   0.40 |            7.98 |               0.90 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                     |   0.09 |    -0.30 |             -0.29 |  1313.00 |   0.54 |            8.33 |               0.67 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                             |   0.05 |    -0.29 |             -0.27 |  1287.00 |   0.54 |            8.13 |               0.90 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                               |   0.09 |    -0.33 |             -0.30 |  1013.00 |   0.54 |            6.94 |               0.80 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                   |   0.08 |    -0.31 |             -0.27 |   835.00 |   0.55 |            6.70 |               1.06 |
| QULL scan+setups / qull_sma10                                                         |  -0.15 |    -0.77 |             -0.77 |  1130.00 |   0.38 |            3.35 |             nan    |
| QULL scan+setups / qull_sma20                                                         |  -0.11 |    -0.70 |             -0.70 |   989.00 |   0.39 |            4.00 |             nan    |
| QULL scan+setups / sma50_close                                                        |   0.08 |    -0.49 |             -0.38 |   658.00 |   0.20 |            5.57 |               1.22 |
| QULL scan+setups / bracket_20_10                                                      |   0.05 |    -0.38 |             -0.37 |   711.00 |   0.39 |            5.58 |               1.52 |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma10                            |  -0.08 |    -0.58 |             -0.56 |   743.00 |   0.39 |            2.26 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma10                                      |  -0.06 |    -0.49 |             -0.47 |   838.00 |   0.39 |            2.53 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma20                            |  -0.03 |    -0.43 |             -0.41 |   665.00 |   0.41 |            2.84 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma20                                      |  -0.01 |    -0.35 |             -0.30 |   742.00 |   0.40 |            3.15 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / sma50_close                           |   0.17 |    -0.46 |             -0.32 |   465.00 |   0.23 |            4.20 |               0.64 |
| QULL ... + regime + adaptive sizing / sma50_close                                     |   0.14 |    -0.34 |             -0.25 |   482.00 |   0.23 |            4.42 |               0.78 |
| QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20                    |  -0.01 |    -0.29 |             -0.29 |    92.00 |   0.30 |            0.30 |             nan    |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close     |   0.47 |    -0.42 |             -0.34 |   851.00 |   0.31 |            6.82 |               0.44 |
| SURVIVORSHIP S&P 500 names, only after joining the index (2740 signals) / sma50_close |   0.16 |    -0.36 |             -0.30 |   697.00 |   0.32 |            5.30 |               0.80 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY                          |   0.13 |    -0.35 |             -0.27 |   604.00 |   0.34 |            7.48 |               0.45 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY                          |   0.09 |    -0.36 |             -0.28 |   479.00 |   0.33 |            5.75 |               0.96 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY                          |   0.09 |    -0.36 |             -0.28 |   479.00 |   0.33 |            5.75 |               0.96 |
| SPY buy & hold                                                                        |   0.15 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.

Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):

| entry             | filter     | exit            |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_t |
|:------------------|:-----------|:----------------|-------:|----------:|--------:|-----------:|--------:|
| ep_gap10_vol2     | rs80_mkt   | sma50_close     |    208 |      0.62 |     394 |       0.65 |    2.54 |
| ep_gap5           | rs80_early | sma50_close     |    324 |      0.57 |     462 |       0.40 |    2.37 |
| ep_gap10_vol2     | rs80_mkt   | chandelier_3atr |    210 |      0.53 |     394 |       0.24 |    1.86 |
| ep_gap8_hold      | rs80_mkt   | sma50_close     |    286 |      0.53 |     418 |       0.47 |    1.99 |
| ep_gap5           | rs80_mkt   | sma50_close     |    603 |      0.51 |     736 |       0.30 |    2.05 |
| ep_gap8_neglected | rs80       | sma50_close     |    233 |      0.50 |     324 |       0.60 |    2.66 |
| falling_wedge     | all        | oneil_20_8      |   1262 |      0.47 |    1522 |       0.16 |    3.18 |
| falling_wedge     | mkt_ok     | oneil_20_8      |    701 |      0.44 |     910 |       0.10 |    1.49 |
| ep_gap8_hold      | rs80_mkt   | donchian_10low  |    289 |      0.44 |     418 |       0.18 |    1.48 |
| ep_gap10_vol2     | rs80_mkt   | donchian_10low  |    211 |      0.44 |     394 |       0.31 |    2.20 |

Year-by-year returns (best 3 portfolios by CAGR vs SPY):

|      |   SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |   All setups, ranked by superperformer model / bracket_20_10 |   GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10 |   SPY |
|-----:|------------------------------------------------------------------------------------:|-------------------------------------------------------------:|--------------------------------------------------------------------:|------:|
| 2018 |                                                                                12.3 |                                                          9.1 |                                                               -14.3 |  -5.2 |
| 2019 |                                                                                33.4 |                                                         60.5 |                                                                44.1 |  31.2 |
| 2020 |                                                                                60.8 |                                                         59.0 |                                                                57.0 |  18.3 |
| 2021 |                                                                                16.8 |                                                        103.0 |                                                                 3.8 |  28.7 |
| 2022 |                                                                               -22.6 |                                                        -27.5 |                                                               -44.8 | -18.2 |
| 2023 |                                                                                68.5 |                                                         11.7 |                                                                19.7 |  26.2 |
| 2024 |                                                                                89.9 |                                                         16.5 |                                                                88.2 |  24.9 |
| 2025 |                                                                                85.0 |                                                         15.7 |                                                                70.3 |  17.7 |
| 2026 |                                                                               130.4 |                                                         15.5 |                                                                25.1 |  14.4 |

## Appendix: entries and exits

| entry             | source / rule                                                    |   signals |
|:------------------|:-----------------------------------------------------------------|----------:|
| donchian_20       | Turtle 20-day breakout / trading-range break (Brock et al. 1992) |    148839 |
| donchian_55       | Turtle 55-day breakout                                           |     99185 |
| high52            | 52-week-high breakout (George & Hwang 2004)                      |     59816 |
| high52_fresh      | 52-week high after >= 20 days of consolidation                   |     16711 |
| base_25           | O'Neil/Darvas 5-week base breakout                               |      4382 |
| base_50           | O'Neil 10-week base breakout                                     |      4968 |
| vcp               | Minervini volatility contraction pattern                         |      2217 |
| flag_30           | Qullamaggie flag after a 30%+ move                               |      2954 |
| flag_60           | Qullamaggie flag after a 60%+ move                               |       960 |
| flag_30_early     | Qullamaggie flag, early entry inside the flag                    |      3162 |
| htf               | High tight flag (O'Neil / Bulkowski)                             |       152 |
| ep_gap5           | Gap up >= 5% on 3x volume                                        |      4212 |
| ep_gap10          | Episodic pivot: gap >= 10% on 3x volume                          |      1477 |
| ep_gap8_neglected | Episodic pivot from neglect (Qullamaggie)                        |      1552 |
| ep_gap15          | Episodic pivot: gap >= 15% on 3x volume                          |       535 |
| ep_gap10_vol2     | EP variant: gap >= 10% on only 2x volume                         |      1808 |
| ep_gap10_vol5     | EP variant: gap >= 10% on 5x volume                              |       773 |
| ep_gap8_hold      | EP variant: gap >= 8%, closes above the open                     |      1932 |
| pocket_pivot      | Morales & Kacher pocket pivot                                    |     97934 |
| asc_triangle      | Ascending triangle breakout (flat top, rising lows)              |      1984 |
| desc_triangle     | Descending triangle, upside breakout                             |      1490 |
| sym_triangle      | Symmetrical triangle breakout (pennant)                          |      1811 |
| falling_wedge     | Falling wedge breakout                                           |      2803 |
| rising_wedge      | Rising wedge, upside breakout                                    |      3846 |
| tight_coil_7      | 7-day coil: closes within 1 ADR, breakout on volume              |     11860 |
| tight_coil_15     | 15-day coil: closes within 1.5 ADR, breakout on volume           |      2353 |
| stage2            | Weinstein stage 2 breakout                                       |     10957 |
| ema_retest        | 8/21 EMA cross -> break -> retest (your playbook)                |     30400 |
| multi_touch       | Multi-touch level breakout on volume (your playbook)             |     23443 |
| undercut          | Undercut & rally (your playbook)                                 |     49679 |
| qull_breakout     | Qullamaggie breakout: buy-stop above the flag high next day      |      6949 |
| qull_breakout_60  | Qullamaggie breakout after a 60%+ move                           |      2785 |
| random_uptrend    | BASELINE: random entries in an uptrend                           |     65407 |

| exit            | rule                                                                           |
|:----------------|:-------------------------------------------------------------------------------|
| trim_ema        | 1/4 at +2R then BE stop; 1/4 on close<8EMA, 1/4 <21EMA, rest <50EMA            |
| qull_sma10      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<10SMA |
| qull_sma20      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<20SMA |
| oneil_20_8      | O'Neil: stop max 8% below entry, take all at +20%, time stop 60 days           |
| fixed_3r_20d    | stop, target 3R, time stop 20 days                                             |
| chandelier_3atr | trailing stop = highest close - 3 x ATR(20)                                    |
| donchian_10low  | Turtle-style: exit on close below the prior 10-day low                         |
| ema21_close     | exit on first close below the 21 EMA                                           |
| sma50_close     | position trade: exit on first close below the 50 SMA                           |
| bracket_10_10   | stop -10%, target +10%, close after 63 days if neither                         |
| bracket_20_10   | stop -10%, target +20%, close after 63 days if neither                         |

Caveats: index membership lists are current (plus former S&P 500 members Yahoo still serves), so survivorship bias remains; daily bars cannot reproduce intraday entries; one decision per signal, no slippage model beyond costs.