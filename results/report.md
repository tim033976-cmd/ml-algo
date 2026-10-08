# Strategy research report

Generated 2026-10-08 15:56 UTC in 36 min.
Universe: 1488 stocks with data (sp600: 591, sp500: 499, sp400: 398; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-06: 669,685.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.51). Top 20 by IS t-stat: +0.060R OOS; top 20 by IS avgR (n>=200): +0.323R; all strategies +0.043R; random entries -0.020R.
- Too few signals to judge (need 100+ per period): htf (IS 52, OOS 99).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.29R, OOS +0.27R), ep_gap10_vol5 (IS +0.17R, OOS +0.20R), desc_triangle (IS +0.18R, OOS +0.17R), ep_gap8_hold (IS +0.17R, OOS +0.17R), ep_gap8_neglected (IS +0.20R, OOS +0.15R), falling_wedge (IS +0.24R, OOS +0.11R), ep_gap5 (IS +0.13R, OOS +0.11R), ep_gap10 (IS +0.10R, OOS +0.21R), undercut (IS +0.12R, OOS +0.08R), donchian_20 (IS +0.10R, OOS +0.07R), ep_gap10_vol2 (IS +0.07R, OOS +0.22R), ema_retest (IS +0.09R, OOS +0.06R), sym_triangle (IS +0.06R, OOS +0.11R), donchian_55 (IS +0.08R, OOS +0.05R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
- Best exit out-of-sample (avg over entries): sma50_close (+0.111R); worst: qull_sma10 (-0.049R).
- Filters that help OOS: qull_scan_regime (+0.116R), rs80_early (+0.101R), qull_scan (+0.090R), rs80_early_theme (+0.050R), early_stage (+0.047R); that hurt: none.
- ML filter adds little: OOS rank corr 0.011, AUC 0.511, decile monotonicity -0.04, taken +0.096R vs skipped +0.059R.
- Features the model relies on most: sma200_slope, rates_rising, sector_rs, industry_rs, sma150_slope.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.07R, OOS +0.03R), rs80_early (IS +0.05R, OOS +0.08R), rs80_early_theme (IS +0.09R, OOS +0.04R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558` (IS +0.35R, OOS +0.13R, n=30343).
- Superperformer model: 30.5% of its top-10% picks gained >= 40% within 3 months vs 7.1% for all stocks (4.3x), AUC 0.835. Driven by: adr_pct, dist_52w_high, above_52w_low, atr_pct, mkt_above200.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 55% (break-even ~50%), avg net return per trade +1.3%. Point-in-time S&P 500 top 10%: 57%, +2.1% per trade (n=7044).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 37% (break-even ~33%), avg net return per trade +2.4%. Point-in-time S&P 500 top 10%: 37%, +3.4% per trade (n=4229).
- Best portfolio 2018->today: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close at 46.3% CAGR (max drawdown -30.5%) vs SPY 14.6%.
- Best return per unit of drawdown: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close (46.3% CAGR, -30.5% max DD).

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
3. Focus development on: ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55 (tune them on IS data only, re-check OOS).
4. Make qull_scan_regime a default filter.
5. Inspect sma200_slope and rates_rising: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                 | no_edge_entries                                                            | best_exit   | helpful_filters                                                        |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                     | filters_lifting_baseline                  |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                               |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:------------|:-----------------------------------------------------------------------|---------:|---------------:|---------------:|---------:|:-----------------------------------------------------------------|:------------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:-------------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|
| 2026-10-08 08:22 | 5e93689  |      1488 |    633749 |        0.57 |        0.05 |          -0.07 | donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50                               | multi_touch, high52, stage2                                                | sma50_close | rs80_early, early_stage, rs80, rs80_mkt                                |     0.55 |           0.25 |          -0.07 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank              | early_stage, rs80_early                   |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | nan                                                                               |      nan    |       nan    | nan                                                          |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 08:48 | 48a9d03  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt              |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank              | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                          |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:11 | fd50739  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt              |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank              | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                          |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:33 | 32c75da  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                          |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:57 | 54a58fb  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                          |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:25 | d8d63d9  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | Only setups in the model's top 10% likely superperformers / sma50_close           |        0.28 |       0.15 | Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)          |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct   |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:53 | d8399f4  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2                                                | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low        | early_stage, rs80_early, rs80_early_theme |            4 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct   |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 14:02 | 749e984  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct   |               0.56 |               0.02 |               0.38 |               0.03 |
| 2026-10-08 14:27 | e7af2f7  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                        |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct    | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct   |               0.56 |               0.02 |               0.38 |               0.03 |
| 2026-10-08 15:56 | f522ebc  |      1488 |    669685 |        0.51 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage |     0.51 |           0.01 |          -0.04 |     0.04 | sma200_slope, rates_rising, sector_rs, industry_rs, sma150_slope | early_stage, rs80_early, rs80_early_theme |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.46 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.83 |         4.29 | adr_pct, dist_52w_high, above_52w_low, atr_pct, mkt_above200 |               0.55 |               0.01 |               0.37 |               0.02 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 3993.000 |
| strategies_with_enough_trades | 3104.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.507 |
| rank_corr_IS_vs_OOS_t         |    0.554 |
| OOS_avgR_all_strategies       |    0.043 |
| OOS_avgR_top20_by_IS          |    0.060 |
| OOS_avgR_top20_by_IS_avgR     |    0.323 |
| OOS_avgR_random_baseline      |   -0.020 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry        | filter      | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-------------|:------------|:--------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| donchian_20  | all         | bracket_20_10 |  68945 |      0.16 |  38.02 |   78114 |      8915.98 |      0.45 |       0.07 |     1.14 |   16.27 |         644.85 |
| pocket_pivot | all         | bracket_20_10 |  48197 |      0.19 |  37.27 |   48059 |      5485.48 |      0.45 |       0.06 |     1.12 |   10.83 |         325.10 |
| pocket_pivot | all         | bracket_10_10 |  48603 |      0.15 |  37.14 |   48059 |      5485.48 |      0.53 |       0.05 |     1.11 |   10.42 |         251.29 |
| donchian_20  | all         | bracket_10_10 |  69384 |      0.13 |  36.38 |   78114 |      8915.98 |      0.53 |       0.05 |     1.11 |   13.40 |         419.12 |
| donchian_20  | mkt_ok      | bracket_20_10 |  57117 |      0.17 |  35.88 |   61630 |      7034.49 |      0.45 |       0.07 |     1.14 |   14.42 |         509.19 |
| donchian_20  | mkt_ok      | bracket_10_10 |  57510 |      0.13 |  34.02 |   61630 |      7034.49 |      0.53 |       0.05 |     1.11 |   11.89 |         331.47 |
| pocket_pivot | mkt_ok      | bracket_20_10 |  35045 |      0.18 |  31.92 |   33715 |      3848.25 |      0.46 |       0.06 |     1.11 |    8.47 |         211.83 |
| pocket_pivot | mkt_ok      | bracket_10_10 |  35395 |      0.15 |  31.68 |   33715 |      3848.25 |      0.53 |       0.05 |     1.10 |    8.61 |         173.85 |
| donchian_55  | all         | bracket_20_10 |  47071 |      0.16 |  31.65 |   50722 |      5789.44 |      0.45 |       0.06 |     1.11 |   10.39 |         326.89 |
| donchian_55  | all         | bracket_10_10 |  47425 |      0.13 |  31.32 |   50722 |      5789.44 |      0.52 |       0.03 |     1.07 |    6.93 |         172.87 |
| donchian_20  | early_stage | bracket_20_10 |  36312 |      0.19 |  30.63 |   47169 |      5383.90 |      0.45 |       0.09 |     1.18 |   16.29 |         509.47 |
| undercut     | all         | bracket_20_10 |  22886 |      0.23 |  29.39 |   26314 |      3003.50 |      0.46 |       0.12 |     1.25 |   16.20 |         375.29 |
| donchian_55  | mkt_ok      | bracket_20_10 |  39904 |      0.16 |  29.09 |   40609 |      4635.14 |      0.45 |       0.06 |     1.12 |    9.87 |         279.48 |
| donchian_55  | mkt_ok      | bracket_10_10 |  40219 |      0.13 |  28.48 |   40609 |      4635.14 |      0.53 |       0.03 |     1.07 |    6.88 |         154.09 |
| pocket_pivot | early_stage | bracket_20_10 |  17000 |      0.24 |  28.48 |   18398 |      2099.96 |      0.47 |       0.09 |     1.20 |   10.56 |         196.16 |
| donchian_20  | early_stage | bracket_10_10 |  36523 |      0.14 |  27.99 |   47169 |      5383.90 |      0.54 |       0.06 |     1.15 |   14.13 |         346.24 |
| pocket_pivot | early_stage | bracket_10_10 |  17151 |      0.19 |  27.73 |   18398 |      2099.96 |      0.54 |       0.06 |     1.14 |    8.33 |         123.84 |
| undercut     | all         | bracket_10_10 |  23014 |      0.17 |  27.44 |   26314 |      3003.50 |      0.55 |       0.09 |     1.21 |   14.65 |         264.02 |
| high52       | all         | bracket_10_10 |  29852 |      0.14 |  26.53 |   29119 |      3323.66 |      0.52 |       0.02 |     1.04 |    3.42 |          63.83 |
| high52       | all         | bracket_20_10 |  29591 |      0.16 |  25.79 |   29119 |      3323.66 |      0.44 |       0.04 |     1.08 |    5.80 |         135.20 |
| donchian_55  | early_stage | bracket_20_10 |  19519 |      0.19 |  24.26 |   23762 |      2712.21 |      0.46 |       0.09 |     1.17 |   10.88 |         236.40 |
| high52       | mkt_ok      | bracket_10_10 |  25383 |      0.13 |  23.71 |   23103 |      2636.99 |      0.52 |       0.03 |     1.06 |    3.97 |          66.43 |
| high52       | mkt_ok      | bracket_20_10 |  25146 |      0.16 |  23.27 |   23103 |      2636.99 |      0.45 |       0.04 |     1.09 |    5.65 |         118.19 |
| donchian_55  | early_stage | bracket_10_10 |  19675 |      0.15 |  23.03 |   23762 |      2712.21 |      0.53 |       0.05 |     1.10 |    7.28 |         124.46 |
| donchian_20  | all         | oneil_20_8    |  69752 |      0.17 |  21.85 |   78114 |      8915.98 |      0.30 |       0.04 |     1.06 |    6.22 |         377.85 |
| ema_retest   | all         | bracket_20_10 |  14294 |      0.20 |  21.13 |   15672 |      1788.81 |      0.46 |       0.08 |     1.15 |    7.87 |         136.52 |
| donchian_20  | early_stage | oneil_20_8    |  36654 |      0.22 |  20.71 |   47169 |      5383.90 |      0.31 |       0.08 |     1.11 |    9.18 |         432.31 |
| ema_retest   | all         | bracket_10_10 |  14395 |      0.15 |  20.19 |   15672 |      1788.81 |      0.53 |       0.05 |     1.10 |    5.92 |          81.37 |
| ema_retest   | mkt_ok      | bracket_20_10 |  12030 |      0.20 |  19.74 |   12389 |      1414.09 |      0.46 |       0.09 |     1.18 |    8.18 |         126.96 |
| donchian_20  | mkt_ok      | oneil_20_8    |  57859 |      0.17 |  19.68 |   61630 |      7034.49 |      0.29 |       0.04 |     1.05 |    5.06 |         275.58 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry          | filter      | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:---------------|:------------|:--------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| donchian_20    | all         | bracket_20_10 |  68945 |      0.16 |  38.02 |   78114 |      0.45 |       0.07 |     1.14 |   16.27 |
| pocket_pivot   | all         | bracket_20_10 |  48197 |      0.19 |  37.27 |   48059 |      0.45 |       0.06 |     1.12 |   10.83 |
| pocket_pivot   | all         | bracket_10_10 |  48603 |      0.15 |  37.14 |   48059 |      0.53 |       0.05 |     1.11 |   10.42 |
| donchian_20    | all         | bracket_10_10 |  69384 |      0.13 |  36.38 |   78114 |      0.53 |       0.05 |     1.11 |   13.40 |
| donchian_20    | mkt_ok      | bracket_20_10 |  57117 |      0.17 |  35.88 |   61630 |      0.45 |       0.07 |     1.14 |   14.42 |
| donchian_20    | mkt_ok      | bracket_10_10 |  57510 |      0.13 |  34.02 |   61630 |      0.53 |       0.05 |     1.11 |   11.89 |
| pocket_pivot   | mkt_ok      | bracket_20_10 |  35045 |      0.18 |  31.92 |   33715 |      0.46 |       0.06 |     1.11 |    8.47 |
| pocket_pivot   | mkt_ok      | bracket_10_10 |  35395 |      0.15 |  31.68 |   33715 |      0.53 |       0.05 |     1.10 |    8.61 |
| donchian_55    | all         | bracket_20_10 |  47071 |      0.16 |  31.65 |   50722 |      0.45 |       0.06 |     1.11 |   10.39 |
| donchian_55    | all         | bracket_10_10 |  47425 |      0.13 |  31.32 |   50722 |      0.52 |       0.03 |     1.07 |    6.93 |
| donchian_20    | early_stage | bracket_20_10 |  36312 |      0.19 |  30.63 |   47169 |      0.45 |       0.09 |     1.18 |   16.29 |
| undercut       | all         | bracket_20_10 |  22886 |      0.23 |  29.39 |   26314 |      0.46 |       0.12 |     1.25 |   16.20 |
| donchian_55    | mkt_ok      | bracket_20_10 |  39904 |      0.16 |  29.09 |   40609 |      0.45 |       0.06 |     1.12 |    9.87 |
| random_uptrend | all         | bracket_20_10 |  30431 |      0.19 |  28.94 |   34126 |      0.45 |       0.09 |     1.18 |   13.79 |
| donchian_55    | mkt_ok      | bracket_10_10 |  40219 |      0.13 |  28.48 |   40609 |      0.53 |       0.03 |     1.07 |    6.88 |
| pocket_pivot   | early_stage | bracket_20_10 |  17000 |      0.24 |  28.48 |   18398 |      0.47 |       0.09 |     1.20 |   10.56 |
| random_uptrend | all         | bracket_10_10 |  30621 |      0.15 |  28.11 |   34126 |      0.54 |       0.06 |     1.14 |   11.73 |
| donchian_20    | early_stage | bracket_10_10 |  36523 |      0.14 |  27.99 |   47169 |      0.54 |       0.06 |     1.15 |   14.13 |
| pocket_pivot   | early_stage | bracket_10_10 |  17151 |      0.19 |  27.73 |   18398 |      0.54 |       0.06 |     1.14 |    8.33 |
| undercut       | all         | bracket_10_10 |  23014 |      0.17 |  27.44 |   26314 |      0.55 |       0.09 |     1.21 |   14.65 |
| high52         | all         | bracket_10_10 |  29852 |      0.14 |  26.53 |   29119 |      0.52 |       0.02 |     1.04 |    3.42 |
| high52         | all         | bracket_20_10 |  29591 |      0.16 |  25.79 |   29119 |      0.44 |       0.04 |     1.08 |    5.80 |
| donchian_55    | early_stage | bracket_20_10 |  19519 |      0.19 |  24.26 |   23762 |      0.46 |       0.09 |     1.17 |   10.88 |
| high52         | mkt_ok      | bracket_10_10 |  25383 |      0.13 |  23.71 |   23103 |      0.52 |       0.03 |     1.06 |    3.97 |
| high52         | mkt_ok      | bracket_20_10 |  25146 |      0.16 |  23.27 |   23103 |      0.45 |       0.04 |     1.09 |    5.65 |
| random_uptrend | mkt_ok      | bracket_20_10 |  20413 |      0.18 |  23.16 |   23056 |      0.45 |       0.09 |     1.18 |   10.80 |
| donchian_55    | early_stage | bracket_10_10 |  19675 |      0.15 |  23.03 |   23762 |      0.53 |       0.05 |     1.10 |    7.28 |
| random_uptrend | mkt_ok      | bracket_10_10 |  20580 |      0.14 |  22.51 |   23056 |      0.54 |       0.06 |     1.14 |    9.15 |
| donchian_20    | all         | oneil_20_8    |  69752 |      0.17 |  21.85 |   78114 |      0.30 |       0.04 |     1.06 |    6.22 |
| random_uptrend | early_stage | bracket_20_10 |  10907 |      0.24 |  21.77 |   13156 |      0.47 |       0.12 |     1.25 |   11.35 |

## 4. Each entry with its best in-sample exit/filter

| entry             | filter           | exit          |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------------|:-----------------|:--------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| flag_60           | rs80_early       | bracket_20_10 |    111 |        9.25 |     0.49 |      0.31 |   2.36 |     208 |        23.74 |      0.44 |       0.26 |     1.46 |    2.51 |           6.24 |
| qull_breakout     | early_stage      | bracket_20_10 |    757 |       63.11 |     0.41 |      0.12 |   2.39 |    1513 |       172.69 |      0.44 |       0.23 |     1.41 |    6.16 |          39.88 |
| ep_gap15          | rs80_mkt         | bracket_20_10 |     62 |        5.17 |     0.56 |      0.58 |   3.26 |     140 |        15.98 |      0.44 |       0.20 |     1.36 |    1.67 |           3.24 |
| flag_30           | rs80_early_theme | bracket_20_10 |    159 |       13.26 |     0.47 |      0.26 |   2.36 |     236 |        26.94 |      0.42 |       0.17 |     1.30 |    1.83 |           4.70 |
| falling_wedge     | all              | bracket_20_10 |   1264 |      105.38 |     0.58 |      0.31 |   9.35 |    1506 |       171.90 |      0.48 |       0.17 |     1.37 |    5.35 |          29.25 |
| ep_gap10_vol2     | rs80_mkt         | bracket_20_10 |    207 |       17.26 |     0.48 |      0.26 |   2.73 |     394 |        44.97 |      0.42 |       0.15 |     1.25 |    2.05 |           6.53 |
| undercut          | all              | bracket_20_10 |  22886 |     1908.04 |     0.54 |      0.23 |  29.39 |   26314 |      3003.50 |      0.46 |       0.12 |     1.25 |   16.20 |         375.29 |
| ep_gap10          | rs80_mkt         | bracket_20_10 |    190 |       15.84 |     0.51 |      0.32 |   3.22 |     337 |        38.47 |      0.41 |       0.12 |     1.21 |    1.61 |           4.68 |
| ep_gap8_hold      | all              | bracket_20_10 |    733 |       61.11 |     0.48 |      0.21 |   4.22 |    1182 |       134.91 |      0.42 |       0.11 |     1.20 |    2.85 |          15.42 |
| desc_triangle     | all              | bracket_20_10 |    775 |       64.61 |     0.57 |      0.23 |   5.78 |     706 |        80.58 |      0.47 |       0.10 |     1.23 |    2.34 |           8.37 |
| random_uptrend    | all              | bracket_20_10 |  30431 |     2537.07 |     0.53 |      0.19 |  28.94 |   34126 |      3895.16 |      0.45 |       0.09 |     1.18 |   13.79 |         362.34 |
| base_25           | mkt_ok           | bracket_20_10 |   1475 |      122.97 |     0.46 |      0.14 |   3.98 |    1879 |       214.47 |      0.42 |       0.09 |     1.15 |    2.83 |          19.22 |
| ep_gap10_vol5     | rs80             | bracket_10_10 |    198 |       16.51 |     0.63 |      0.25 |   3.66 |     291 |        33.21 |      0.55 |       0.08 |     1.18 |    1.42 |           2.73 |
| ep_gap8_neglected | all              | bracket_20_10 |    605 |       50.44 |     0.50 |      0.25 |   4.55 |     934 |       106.61 |      0.41 |       0.08 |     1.14 |    1.83 |           8.69 |
| sym_triangle      | all              | bracket_10_10 |    889 |       74.12 |     0.58 |      0.12 |   3.78 |     915 |       104.44 |      0.55 |       0.08 |     1.19 |    2.43 |           8.10 |
| ema_retest        | all              | bracket_20_10 |  14294 |     1191.71 |     0.55 |      0.20 |  21.13 |   15672 |      1788.81 |      0.46 |       0.08 |     1.15 |    7.87 |         136.52 |
| donchian_20       | all              | bracket_20_10 |  68945 |     5748.04 |     0.52 |      0.16 |  38.02 |   78114 |      8915.98 |      0.45 |       0.07 |     1.14 |   16.27 |         644.85 |
| pocket_pivot      | all              | bracket_20_10 |  48197 |     4018.25 |     0.54 |      0.19 |  37.27 |   48059 |      5485.48 |      0.45 |       0.06 |     1.12 |   10.83 |         325.10 |
| asc_triangle      | all              | bracket_20_10 |   1082 |       90.21 |     0.57 |      0.20 |   6.23 |     863 |        98.50 |      0.46 |       0.06 |     1.12 |    1.49 |           5.79 |
| donchian_55       | all              | bracket_20_10 |  47071 |     3924.37 |     0.53 |      0.16 |  31.65 |   50722 |      5789.44 |      0.45 |       0.06 |     1.11 |   10.39 |         326.89 |
| vcp               | all              | bracket_20_10 |   1295 |      107.97 |     0.54 |      0.16 |   5.41 |     879 |       100.33 |      0.46 |       0.05 |     1.11 |    1.36 |           5.38 |
| flag_30_early     | mkt_ok           | bracket_10_10 |    850 |       70.87 |     0.56 |      0.10 |   2.84 |    1454 |       165.96 |      0.52 |       0.04 |     1.09 |    1.58 |           7.17 |
| high52_fresh      | all              | bracket_10_10 |   8107 |      675.89 |     0.61 |      0.16 |  16.80 |    8415 |       960.49 |      0.53 |       0.03 |     1.07 |    2.98 |          30.04 |
| base_50           | all              | bracket_10_10 |   2283 |      190.34 |     0.56 |      0.10 |   4.81 |    2665 |       304.18 |      0.52 |       0.03 |     1.05 |    1.29 |           7.65 |
| ep_gap5           | all              | bracket_10_10 |   1870 |      155.90 |     0.57 |      0.12 |   5.50 |    2322 |       265.03 |      0.52 |       0.02 |     1.05 |    1.07 |           5.99 |
| high52            | all              | bracket_10_10 |  29852 |     2488.80 |     0.59 |      0.14 |  26.53 |   29119 |      3323.66 |      0.52 |       0.02 |     1.04 |    3.42 |          63.83 |
| rising_wedge      | all              | bracket_10_10 |   2075 |      173.00 |     0.59 |      0.13 |   6.70 |    1747 |       199.40 |      0.52 |       0.02 |     1.04 |    0.83 |           3.75 |
| tight_coil_7      | all              | bracket_10_10 |   6304 |      525.57 |     0.59 |      0.15 |  13.46 |    5359 |       611.68 |      0.51 |       0.01 |     1.02 |    0.85 |           6.90 |
| multi_touch       | all              | bracket_10_10 |  12481 |     1040.56 |     0.59 |      0.14 |  16.94 |   10634 |      1213.77 |      0.51 |      -0.00 |     1.00 |   -0.08 |          -0.92 |
| qull_breakout_60  | rs80_theme       | bracket_10_10 |    340 |       28.35 |     0.54 |      0.08 |   1.49 |     813 |        92.80 |      0.51 |      -0.00 |     1.00 |   -0.02 |          -0.08 |
| stage2            | all              | bracket_10_10 |   5921 |      493.64 |     0.61 |      0.18 |  15.58 |    4847 |       553.24 |      0.51 |      -0.00 |     0.99 |   -0.29 |          -2.15 |
| tight_coil_15     | all              | bracket_10_10 |   1261 |      105.13 |     0.60 |      0.15 |   6.04 |    1039 |       118.59 |      0.49 |      -0.02 |     0.96 |   -0.70 |          -2.47 |
| htf               | all              | sma50_close   |     52 |        4.34 |     0.17 |      0.41 |   0.66 |      99 |        11.30 |      0.11 |      -0.34 |     0.65 |   -1.17 |          -3.85 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry             |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |           -0.04 |           -0.03 |              0.06 |             0.05 |          0.02 |           0.09 |         0.04 |         0.04 |         0.01 |         -0.00 |       0.10 |
| base_25           |           -0.02 |            0.02 |              0.12 |             0.09 |          0.10 |           0.08 |         0.10 |         0.04 |         0.07 |          0.23 |       0.13 |
| base_50           |           -0.04 |            0.00 |              0.16 |             0.11 |          0.14 |           0.11 |         0.12 |         0.08 |         0.10 |          0.22 |       0.15 |
| desc_triangle     |            0.02 |            0.01 |              0.27 |             0.24 |          0.22 |           0.22 |         0.29 |         0.15 |         0.20 |          0.07 |       0.19 |
| donchian_20       |           -0.01 |           -0.02 |              0.10 |             0.08 |          0.09 |           0.11 |         0.09 |         0.08 |         0.08 |          0.07 |       0.11 |
| donchian_55       |           -0.03 |           -0.04 |              0.07 |             0.06 |          0.07 |           0.08 |         0.06 |         0.06 |         0.06 |          0.06 |       0.10 |
| ema_retest        |           -0.02 |           -0.02 |              0.07 |             0.05 |          0.07 |           0.09 |         0.09 |         0.07 |         0.05 |          0.07 |       0.10 |
| ep_gap10          |           -0.04 |            0.01 |              0.25 |             0.35 |          0.27 |           0.20 |         0.15 |         0.11 |         0.17 |          0.52 |       0.32 |
| ep_gap10_vol2     |           -0.03 |            0.05 |              0.31 |             0.36 |          0.26 |           0.18 |         0.21 |         0.13 |         0.18 |          0.51 |       0.31 |
| ep_gap10_vol5     |           -0.06 |            0.02 |              0.26 |             0.33 |          0.22 |           0.20 |         0.12 |         0.09 |         0.12 |          0.53 |       0.34 |
| ep_gap15          |            0.01 |            0.12 |              0.30 |             0.34 |          0.27 |           0.25 |         0.27 |         0.12 |         0.15 |          0.74 |       0.39 |
| ep_gap5           |           -0.04 |           -0.01 |              0.15 |             0.17 |          0.15 |           0.12 |         0.10 |         0.09 |         0.10 |          0.21 |       0.16 |
| ep_gap8_hold      |           -0.02 |            0.02 |              0.19 |             0.26 |          0.21 |           0.17 |         0.15 |         0.10 |         0.13 |          0.40 |       0.26 |
| ep_gap8_neglected |           -0.03 |           -0.01 |              0.14 |             0.18 |          0.22 |           0.18 |         0.18 |         0.10 |         0.13 |          0.29 |       0.24 |
| falling_wedge     |            0.04 |            0.08 |              0.21 |             0.17 |          0.09 |           0.19 |         0.23 |         0.07 |         0.08 |          0.03 |       0.08 |
| flag_30           |           -0.04 |            0.03 |              0.07 |             0.13 |          0.14 |           0.06 |         0.03 |         0.08 |         0.08 |          0.28 |       0.15 |
| flag_30_early     |            0.00 |            0.09 |              0.18 |             0.16 |          0.17 |           0.15 |         0.22 |         0.13 |         0.13 |          0.25 |       0.19 |
| flag_60           |           -0.06 |            0.07 |              0.19 |             0.16 |          0.18 |           0.10 |         0.11 |         0.13 |         0.11 |          0.53 |       0.32 |
| high52            |           -0.04 |           -0.05 |             -0.04 |            -0.05 |         -0.03 |          -0.03 |        -0.04 |        -0.03 |        -0.05 |         -0.05 |      -0.02 |
| high52_fresh      |           -0.03 |           -0.04 |              0.06 |             0.04 |          0.07 |           0.05 |         0.05 |         0.04 |         0.03 |          0.07 |       0.07 |
| htf               |           -0.26 |           -0.17 |             -0.19 |            -0.30 |         -0.14 |          -0.15 |        -0.17 |        -0.01 |        -0.10 |         -0.31 |      -0.07 |
| multi_touch       |           -0.06 |           -0.08 |             -0.03 |            -0.00 |         -0.02 |          -0.00 |        -0.04 |         0.01 |        -0.01 |         -0.06 |      -0.01 |
| pocket_pivot      |           -0.02 |           -0.03 |             -0.02 |            -0.02 |         -0.01 |           0.00 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.01 |
| qull_breakout     |           -0.02 |            0.06 |             -0.07 |            -0.08 |         -0.07 |          -0.14 |        -0.10 |        -0.14 |        -0.12 |          0.05 |      -0.08 |
| qull_breakout_60  |           -0.01 |            0.10 |             -0.08 |            -0.09 |         -0.06 |          -0.12 |        -0.06 |        -0.14 |        -0.12 |          0.15 |      -0.08 |
| rising_wedge      |           -0.04 |           -0.05 |             -0.02 |            -0.05 |         -0.02 |           0.04 |         0.03 |         0.07 |         0.03 |         -0.06 |       0.01 |
| stage2            |           -0.07 |           -0.08 |             -0.07 |            -0.07 |         -0.06 |          -0.02 |        -0.08 |        -0.02 |        -0.05 |         -0.10 |      -0.05 |
| sym_triangle      |            0.02 |            0.01 |              0.19 |             0.12 |          0.12 |           0.17 |         0.16 |         0.14 |         0.14 |          0.04 |       0.11 |
| tight_coil_15     |           -0.08 |           -0.10 |             -0.00 |            -0.03 |         -0.00 |           0.05 |        -0.01 |         0.06 |         0.03 |         -0.10 |       0.03 |
| tight_coil_7      |           -0.05 |           -0.06 |              0.02 |             0.01 |          0.03 |           0.07 |         0.03 |         0.06 |         0.04 |         -0.01 |       0.07 |
| undercut          |            0.03 |            0.03 |              0.18 |             0.16 |          0.02 |           0.08 |         0.13 |         0.09 |         0.08 |         -0.00 |       0.03 |
| vcp               |           -0.01 |           -0.04 |              0.06 |             0.04 |          0.04 |           0.10 |         0.05 |         0.07 |         0.06 |         -0.05 |       0.04 |

Same, in-sample:

| entry             |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |            0.01 |            0.01 |              0.06 |             0.02 |          0.06 |           0.08 |         0.07 |         0.06 |         0.04 |         -0.01 |       0.10 |
| base_25           |           -0.07 |           -0.07 |             -0.03 |            -0.04 |         -0.00 |           0.07 |        -0.08 |         0.06 |         0.03 |          0.03 |       0.09 |
| base_50           |           -0.05 |           -0.07 |              0.00 |            -0.00 |          0.04 |           0.13 |        -0.04 |         0.08 |         0.05 |         -0.03 |       0.09 |
| desc_triangle     |            0.03 |            0.04 |              0.17 |             0.29 |          0.17 |           0.21 |         0.20 |         0.17 |         0.17 |          0.21 |       0.27 |
| donchian_20       |           -0.02 |           -0.03 |              0.11 |             0.11 |          0.14 |           0.15 |         0.09 |         0.10 |         0.11 |          0.12 |       0.17 |
| donchian_55       |           -0.02 |           -0.03 |              0.08 |             0.09 |          0.12 |           0.13 |         0.07 |         0.08 |         0.09 |          0.11 |       0.17 |
| ema_retest        |            0.00 |            0.01 |              0.09 |             0.09 |          0.12 |           0.12 |         0.15 |         0.06 |         0.07 |          0.15 |       0.13 |
| ep_gap10          |           -0.03 |           -0.00 |              0.16 |             0.10 |          0.15 |           0.10 |        -0.05 |         0.13 |         0.10 |          0.18 |       0.22 |
| ep_gap10_vol2     |           -0.05 |           -0.04 |              0.13 |             0.06 |          0.12 |           0.10 |        -0.05 |         0.10 |         0.07 |          0.13 |       0.18 |
| ep_gap10_vol5     |            0.03 |            0.05 |              0.23 |             0.18 |          0.18 |           0.20 |         0.03 |         0.22 |         0.17 |          0.29 |       0.33 |
| ep_gap15          |            0.06 |            0.12 |              0.43 |             0.32 |          0.33 |           0.30 |         0.11 |         0.32 |         0.30 |          0.45 |       0.48 |
| ep_gap5           |           -0.02 |           -0.03 |              0.17 |             0.12 |          0.17 |           0.15 |         0.08 |         0.14 |         0.13 |          0.25 |       0.23 |
| ep_gap8_hold      |           -0.01 |            0.02 |              0.24 |             0.20 |          0.24 |           0.17 |         0.12 |         0.16 |         0.16 |          0.29 |       0.32 |
| ep_gap8_neglected |            0.01 |            0.06 |              0.27 |             0.22 |          0.25 |           0.19 |         0.19 |         0.16 |         0.19 |          0.32 |       0.29 |
| falling_wedge     |            0.07 |            0.12 |              0.35 |             0.36 |          0.23 |           0.30 |         0.40 |         0.21 |         0.23 |          0.13 |       0.20 |
| flag_30           |           -0.14 |           -0.15 |             -0.08 |            -0.10 |         -0.05 |           0.05 |        -0.11 |         0.02 |        -0.03 |         -0.09 |       0.01 |
| flag_30_early     |           -0.09 |           -0.11 |              0.11 |             0.08 |          0.12 |           0.05 |        -0.04 |         0.06 |         0.09 |          0.01 |       0.03 |
| flag_60           |           -0.14 |           -0.12 |              0.04 |             0.02 |          0.09 |           0.12 |        -0.02 |         0.15 |         0.09 |          0.07 |       0.12 |
| high52            |           -0.01 |           -0.03 |             -0.03 |            -0.04 |          0.01 |           0.02 |        -0.03 |        -0.02 |        -0.02 |         -0.03 |       0.00 |
| high52_fresh      |            0.02 |            0.01 |              0.06 |             0.05 |          0.09 |           0.08 |         0.07 |         0.04 |         0.05 |          0.07 |       0.08 |
| htf               |           -0.21 |           -0.14 |             -0.07 |             0.26 |          0.15 |           0.08 |        -0.09 |         0.14 |         0.20 |          0.45 |       0.29 |
| multi_touch       |           -0.01 |           -0.02 |              0.07 |             0.08 |          0.12 |           0.10 |         0.09 |         0.06 |         0.06 |          0.12 |       0.10 |
| pocket_pivot      |            0.00 |           -0.00 |              0.05 |             0.06 |          0.07 |           0.03 |         0.04 |         0.03 |         0.03 |          0.07 |       0.04 |
| qull_breakout     |           -0.16 |           -0.18 |             -0.32 |            -0.33 |         -0.26 |          -0.21 |        -0.37 |        -0.18 |        -0.21 |         -0.35 |      -0.23 |
| qull_breakout_60  |           -0.16 |           -0.19 |             -0.26 |            -0.31 |         -0.24 |          -0.24 |        -0.35 |        -0.17 |        -0.19 |         -0.30 |      -0.20 |
| rising_wedge      |           -0.02 |           -0.04 |              0.00 |             0.02 |          0.07 |           0.08 |         0.01 |         0.04 |         0.03 |          0.03 |       0.10 |
| stage2            |            0.03 |            0.02 |              0.11 |             0.13 |          0.16 |           0.11 |         0.16 |         0.07 |         0.09 |          0.15 |       0.14 |
| sym_triangle      |           -0.03 |           -0.06 |              0.07 |             0.08 |          0.12 |           0.08 |        -0.02 |         0.11 |         0.09 |          0.06 |       0.11 |
| tight_coil_15     |            0.01 |           -0.01 |              0.15 |             0.18 |          0.14 |           0.16 |         0.15 |         0.13 |         0.12 |          0.13 |       0.23 |
| tight_coil_7      |            0.01 |           -0.00 |              0.13 |             0.16 |          0.15 |           0.15 |         0.12 |         0.10 |         0.10 |          0.17 |       0.22 |
| undercut          |            0.02 |            0.04 |              0.21 |             0.22 |          0.06 |           0.12 |         0.19 |         0.18 |         0.17 |          0.01 |       0.08 |
| vcp               |           -0.02 |           -0.03 |              0.07 |             0.08 |          0.12 |           0.13 |         0.10 |         0.10 |         0.09 |          0.09 |       0.17 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| sma50_close     |      0.06 |       0.11 |      0.26 |     1.16 |                       0.66 |
| bracket_20_10   |      0.16 |       0.09 |      0.43 |     1.17 |                       0.50 |
| oneil_20_8      |      0.11 |       0.03 |      0.26 |     1.05 |                       0.75 |
| bracket_10_10   |      0.12 |       0.03 |      0.52 |     1.07 |                       0.19 |
| trim_ema        |      0.00 |       0.01 |      0.34 |     1.03 |                       0.78 |
| donchian_10low  |      0.01 |       0.01 |      0.28 |     1.03 |                       0.72 |
| chandelier_3atr |      0.02 |       0.00 |      0.29 |     1.01 |                       0.72 |
| fixed_3r_20d    |     -0.01 |      -0.01 |      0.36 |     0.99 |                       0.81 |
| ema21_close     |     -0.04 |      -0.02 |      0.29 |     0.98 |                       0.72 |
| qull_sma20      |     -0.05 |      -0.04 |      0.42 |     0.94 |                       0.78 |
| qull_sma10      |     -0.05 |      -0.05 |      0.42 |     0.91 |                       0.84 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| qull_scan_regime |     -0.02 |       0.13 |      0.36 |
| rs80_early       |      0.07 |       0.12 |      0.37 |
| qull_scan        |     -0.03 |       0.11 |      0.35 |
| rs80_early_theme |      0.09 |       0.07 |      0.36 |
| early_stage      |      0.06 |       0.06 |      0.36 |
| rs80             |      0.04 |       0.04 |      0.36 |
| rs80_mkt         |      0.06 |       0.03 |      0.35 |
| rs80_theme       |      0.03 |       0.02 |      0.36 |
| all              |      0.03 |       0.02 |      0.35 |
| theme            |      0.03 |       0.01 |      0.36 |
| mkt_ok           |      0.04 |       0.01 |      0.35 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.011; AUC for R > 0: 0.511 (0.5 = no skill). Taken (model's top third, causal threshold): n=84,432, avgR=0.096, win=0.465. Skipped: n=223,670, avgR=0.059, win=0.441.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 30812.00 |   0.10 |  0.44 |
|      1 | 30810.00 |   0.09 |  0.44 |
|      2 | 30809.00 |   0.06 |  0.44 |
|      3 | 30810.00 |   0.04 |  0.43 |
|      4 | 30810.00 |   0.06 |  0.45 |
|      5 | 30810.00 |   0.05 |  0.45 |
|      6 | 30811.00 |   0.05 |  0.44 |
|      7 | 30809.00 |   0.05 |  0.45 |
|      8 | 30810.00 |   0.08 |  0.46 |
|      9 | 30811.00 |   0.12 |  0.48 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| flag_60           |   615.00 |       0.16 |    165.00 |         0.41 |           0.07 |
| flag_30           |  1786.00 |       0.12 |    450.00 |         0.29 |           0.06 |
| htf               |    99.00 |      -0.07 |     23.00 |         0.28 |          -0.18 |
| falling_wedge     |  1506.00 |       0.17 |    627.00 |         0.20 |           0.15 |
| qull_breakout_60  |  1862.00 |       0.19 |    414.00 |         0.19 |           0.19 |
| base_50           |  2665.00 |       0.10 |    766.00 |         0.18 |           0.06 |
| ep_gap10          |   933.00 |       0.11 |    398.00 |         0.18 |           0.06 |
| ep_gap15          |   374.00 |       0.21 |    182.00 |         0.17 |           0.24 |
| ep_gap10_vol2     |  1182.00 |       0.15 |    507.00 |         0.17 |           0.13 |
| base_25           |  2444.00 |       0.11 |    686.00 |         0.17 |           0.09 |
| flag_30_early     |  1955.00 |       0.18 |    452.00 |         0.17 |           0.19 |
| undercut          | 26314.00 |       0.12 |   9538.00 |         0.16 |           0.10 |
| qull_breakout     |  4385.00 |       0.15 |   1020.00 |         0.15 |           0.15 |
| ep_gap5           |  2322.00 |       0.08 |    899.00 |         0.15 |           0.03 |
| desc_triangle     |   706.00 |       0.10 |    221.00 |         0.14 |           0.09 |
| ep_gap8_neglected |   934.00 |       0.08 |    365.00 |         0.13 |           0.05 |
| ep_gap8_hold      |  1182.00 |       0.11 |    480.00 |         0.13 |           0.10 |
| tight_coil_15     |  1039.00 |      -0.01 |    281.00 |         0.13 |          -0.06 |
| ema_retest        | 15672.00 |       0.08 |   4246.00 |         0.12 |           0.06 |
| rising_wedge      |  1747.00 |       0.05 |    453.00 |         0.11 |           0.02 |
| vcp               |   879.00 |       0.05 |    205.00 |         0.11 |           0.04 |
| donchian_55       | 50722.00 |       0.06 |  12452.00 |         0.09 |           0.05 |
| ep_gap10_vol5     |   454.00 |       0.12 |    203.00 |         0.09 |           0.14 |
| pocket_pivot      | 48059.00 |       0.06 |  12988.00 |         0.08 |           0.05 |
| sym_triangle      |   915.00 |       0.11 |    272.00 |         0.08 |           0.12 |
| donchian_20       | 78114.00 |       0.07 |  21058.00 |         0.07 |           0.07 |
| high52            | 29119.00 |       0.04 |   6732.00 |         0.07 |           0.03 |
| asc_triangle      |   863.00 |       0.06 |    252.00 |         0.06 |           0.06 |
| stage2            |  4847.00 |       0.01 |   1481.00 |         0.06 |          -0.01 |
| multi_touch       | 10634.00 |       0.01 |   2937.00 |         0.05 |          -0.01 |
| tight_coil_7      |  5359.00 |       0.03 |   1411.00 |         0.05 |           0.02 |
| high52_fresh      |  8415.00 |       0.05 |   2268.00 |         0.04 |           0.06 |

- Same model on episodic pivots only / sma50_close: rank corr -0.012, taken avgR 0.330 (n=3,222) vs skipped 0.372 (n=4,159).
- Same model on your trim plan (trim_ema): rank corr 0.123, taken avgR 0.004 (n=91,334) vs skipped -0.057 (n=216,768).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature       |   rank_corr_drop |
|:--------------|-----------------:|
| sma200_slope  |           0.0081 |
| rates_rising  |           0.0081 |
| sector_rs     |           0.0055 |
| industry_rs   |           0.0055 |
| sma150_slope  |           0.0049 |
| above_52w_low |           0.0035 |
| adr_pct       |           0.0032 |
| mkt_ema_stack |           0.0030 |
| base_count    |           0.0025 |
| rs_rank       |           0.0024 |
| mkt_ret_21    |           0.0016 |
| mkt_above200  |           0.0015 |
| risk_pct      |           0.0011 |
| atr_ratio     |           0.0008 |
| updown_vol_50 |           0.0008 |
| risk_adr      |           0.0007 |
| leg3_range    |           0.0007 |
| dist_sma50    |           0.0007 |
| base_depth_60 |           0.0006 |
| close_std_10  |           0.0004 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.558    |   8108 |      0.64 |   11871 |       0.08 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558   |  17905 |      0.35 |   30343 |       0.13 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.483 |  67718 |      0.29 |   53758 |      -0.00 |      0.46 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 > 0.778    |   4242 |      0.28 |     441 |       0.99 |      0.73 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.483  |  52740 |      0.17 |   38622 |      -0.01 |      0.40 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 <= 0.0455   |  74673 |      0.16 |  105766 |       0.09 |      0.45 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 > 0.0455    |  41542 |      0.01 |   61976 |       0.09 |      0.44 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 <= 0.778   |  20416 |     -0.18 |    5325 |       0.22 |      0.47 |

## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?

Every stock every 10 trading days (n=279,586 out-of-sample rows). Base rate of a >= 40% gain within 3 months: 7.1%. The model's top 10% hit it 30.5% of the time (4.3x the base rate). AUC 0.835.

|   super_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 27959.000 |      0.001 |          -0.004 |              0.010 |              0.065 |
|            1 | 27959.000 |      0.004 |           0.008 |              0.014 |              0.051 |
|            2 | 27958.000 |      0.009 |           0.016 |              0.018 |              0.051 |
|            3 | 27959.000 |      0.016 |           0.020 |              0.020 |              0.056 |
|            4 | 27958.000 |      0.027 |           0.027 |              0.025 |              0.061 |
|            5 | 27959.000 |      0.041 |           0.033 |              0.029 |              0.070 |
|            6 | 27958.000 |      0.060 |           0.039 |              0.033 |              0.082 |
|            7 | 27959.000 |      0.097 |           0.051 |              0.042 |              0.099 |
|            8 | 27958.000 |      0.150 |           0.063 |              0.043 |              0.120 |
|            9 | 27959.000 |      0.305 |           0.116 |              0.075 |              0.148 |

What matters most (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| adr_pct       |     0.0973 |
| dist_52w_high |     0.0267 |
| above_52w_low |     0.0264 |
| atr_pct       |     0.0049 |
| mkt_above200  |     0.0049 |
| leg1_range    |     0.0044 |
| leg2_range    |     0.0042 |
| qull_rank     |     0.0040 |
| tight_10      |     0.0034 |
| sector_rs     |     0.0010 |
| sma200_slope  |     0.0008 |
| base_count    |     0.0008 |
| sma150_slope  |     0.0007 |
| dist_ema21    |     0.0006 |
| leg3_range    |     0.0005 |

Profile: future superperformers vs everything else, at the moment of the sample:

|               |   future superperformers (median) |   everything else (median) |
|:--------------|----------------------------------:|---------------------------:|
| adr_pct       |                             0.045 |                      0.026 |
| dist_52w_high |                            -0.275 |                     -0.128 |
| above_52w_low |                             0.585 |                      0.340 |
| atr_pct       |                             0.046 |                      0.027 |
| mkt_above200  |                             1.000 |                      1.000 |
| leg1_range    |                             0.184 |                      0.120 |
| leg2_range    |                             0.193 |                      0.120 |
| qull_rank     |                             0.776 |                      0.706 |
| tight_10      |                             0.153 |                      0.087 |
| sector_rs     |                             0.503 |                      0.502 |
| sma200_slope  |                             0.001 |                      0.009 |
| base_count    |                             0.000 |                      1.000 |

Readable rules (depth-3 tree fit before 2018, scored after):

| rule                                                                 |   IS_n |   IS_rate |   OOS_n |   OOS_rate |
|:---------------------------------------------------------------------|-------:|----------:|--------:|-----------:|
| dist_52w_high <= -0.542 AND dist_52w_high <= -0.633                  |   2145 |     0.466 |     889 |      0.447 |
| dist_52w_high <= -0.542 AND dist_52w_high > -0.633                   |   2655 |     0.297 |    1264 |      0.287 |
| dist_52w_high > -0.542 AND adr_pct > 0.032 AND above_52w_low > 1.03  |   8679 |     0.143 |    6216 |      0.238 |
| dist_52w_high > -0.542 AND adr_pct > 0.032 AND above_52w_low <= 1.03 |  37513 |     0.068 |   18792 |      0.126 |
| dist_52w_high > -0.542 AND adr_pct <= 0.032 AND adr_pct > 0.025      |  35365 |     0.026 |   18929 |      0.038 |
| dist_52w_high > -0.542 AND adr_pct <= 0.032 AND adr_pct <= 0.025     | 113643 |     0.005 |   33910 |      0.010 |

Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate 6.7%, model top 10% 27.6% (4.1x), AUC 0.829.

|   clean_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 27959.000 |      0.001 |          -0.002 |              0.011 |              0.062 |
|            1 | 27959.000 |      0.004 |           0.008 |              0.013 |              0.051 |
|            2 | 27958.000 |      0.009 |           0.016 |              0.018 |              0.051 |
|            3 | 27959.000 |      0.015 |           0.019 |              0.020 |              0.058 |
|            4 | 27958.000 |      0.026 |           0.026 |              0.025 |              0.063 |
|            5 | 27959.000 |      0.040 |           0.036 |              0.032 |              0.070 |
|            6 | 27958.000 |      0.060 |           0.042 |              0.035 |              0.081 |
|            7 | 27959.000 |      0.093 |           0.050 |              0.041 |              0.097 |
|            8 | 27958.000 |      0.148 |           0.066 |              0.046 |              0.120 |
|            9 | 27959.000 |      0.276 |           0.110 |              0.068 |              0.152 |

### Your goal: +10% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 50% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 27959.000 |       0.268 |        0.397 |      0.347 |            0.004 |           0.018 |
|       1 | 27959.000 |       0.356 |        0.448 |      0.341 |            0.010 |           0.038 |
|       2 | 27958.000 |       0.402 |        0.470 |      0.366 |            0.009 |           0.047 |
|       3 | 27959.000 |       0.437 |        0.475 |      0.389 |            0.007 |           0.047 |
|       4 | 27958.000 |       0.467 |        0.493 |      0.401 |            0.008 |           0.067 |
|       5 | 27959.000 |       0.494 |        0.505 |      0.404 |            0.009 |           0.098 |
|       6 | 27958.000 |       0.522 |        0.510 |      0.413 |            0.008 |           0.098 |
|       7 | 27959.000 |       0.554 |        0.508 |      0.422 |            0.007 |           0.098 |
|       8 | 27958.000 |       0.596 |        0.515 |      0.420 |            0.008 |           0.098 |
|       9 | 27959.000 |       0.687 |        0.546 |      0.399 |            0.013 |           0.098 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 279586.000 |        0.487 |      0.390 |            0.008 |
| top 10%    |  27959.000 |        0.546 |      0.399 |            0.013 |
| top 5%     |  13980.000 |        0.567 |      0.383 |            0.017 |
| top 2%     |   5592.000 |        0.609 |      0.358 |            0.024 |
| top 1%     |   2796.000 |        0.643 |      0.337 |            0.030 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91558.000 |        0.466 |      0.348 |            0.011 |
| top 10%    |  7044.000 |        0.569 |      0.345 |            0.021 |
| top 5%     |  3515.000 |        0.595 |      0.335 |            0.025 |
| top 2%     |  1516.000 |        0.633 |      0.322 |            0.030 |
| top 1%     |   826.000 |        0.655 |      0.321 |            0.033 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 14422.000 |       0.266 |        0.393 |      0.308 |            0.008 |           0.024 |
|       1 | 12596.000 |       0.355 |        0.432 |      0.303 |            0.012 |           0.038 |
|       2 | 10878.000 |       0.402 |        0.457 |      0.329 |            0.012 |           0.046 |
|       3 |  9497.000 |       0.437 |        0.455 |      0.358 |            0.009 |           0.040 |
|       4 |  8476.000 |       0.466 |        0.473 |      0.373 |            0.009 |           0.048 |
|       5 |  7629.000 |       0.494 |        0.491 |      0.378 |            0.010 |           0.068 |
|       6 |  7232.000 |       0.522 |        0.500 |      0.375 |            0.012 |           0.098 |
|       7 |  6947.000 |       0.554 |        0.488 |      0.398 |            0.008 |           0.061 |
|       8 |  6837.000 |       0.596 |        0.504 |      0.386 |            0.011 |           0.098 |
|       9 |  7044.000 |       0.689 |        0.569 |      0.345 |            0.021 |           0.098 |

### Your goal: +20% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 33% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 27959.000 |       0.044 |        0.061 |      0.325 |            0.003 |          -0.001 |
|       1 | 27959.000 |       0.079 |        0.116 |      0.359 |            0.010 |           0.000 |
|       2 | 27958.000 |       0.109 |        0.149 |      0.404 |            0.008 |          -0.010 |
|       3 | 27959.000 |       0.139 |        0.185 |      0.427 |            0.011 |          -0.017 |
|       4 | 27958.000 |       0.172 |        0.220 |      0.452 |            0.012 |          -0.028 |
|       5 | 27959.000 |       0.207 |        0.256 |      0.481 |            0.013 |          -0.050 |
|       6 | 27958.000 |       0.244 |        0.285 |      0.498 |            0.016 |          -0.083 |
|       7 | 27959.000 |       0.286 |        0.321 |      0.517 |            0.018 |          -0.102 |
|       8 | 27958.000 |       0.337 |        0.336 |      0.538 |            0.017 |          -0.102 |
|       9 | 27959.000 |       0.447 |        0.372 |      0.536 |            0.024 |          -0.102 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 279586.000 |        0.230 |      0.454 |            0.013 |
| top 10%    |  27959.000 |        0.372 |      0.536 |            0.024 |
| top 5%     |  13980.000 |        0.386 |      0.535 |            0.026 |
| top 2%     |   5592.000 |        0.414 |      0.519 |            0.034 |
| top 1%     |   2796.000 |        0.428 |      0.519 |            0.037 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91558.000 |        0.179 |      0.388 |            0.016 |
| top 10%    |  4229.000 |        0.375 |      0.477 |            0.034 |
| top 5%     |  2141.000 |        0.408 |      0.471 |            0.041 |
| top 2%     |   883.000 |        0.459 |      0.444 |            0.054 |
| top 1%     |   466.000 |        0.470 |      0.461 |            0.054 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 17158.000 |       0.044 |        0.058 |      0.300 |            0.007 |           0.006 |
|       1 | 14380.000 |       0.079 |        0.115 |      0.330 |            0.015 |           0.010 |
|       2 | 12324.000 |       0.108 |        0.143 |      0.377 |            0.012 |          -0.002 |
|       3 | 10679.000 |       0.139 |        0.176 |      0.401 |            0.014 |          -0.003 |
|       4 |  8996.000 |       0.172 |        0.202 |      0.423 |            0.015 |          -0.011 |
|       5 |  7584.000 |       0.207 |        0.242 |      0.446 |            0.017 |          -0.019 |
|       6 |  6278.000 |       0.243 |        0.262 |      0.453 |            0.020 |          -0.020 |
|       7 |  5321.000 |       0.285 |        0.311 |      0.464 |            0.026 |          -0.022 |
|       8 |  4609.000 |       0.337 |        0.331 |      0.478 |            0.027 |          -0.035 |
|       9 |  4229.000 |       0.450 |        0.375 |      0.477 |            0.034 |          -0.023 |

Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that survived. See the SURVIVORSHIP and CHECK rows in section 9.

Setup signals split by the model's score (OOS, exit bracket_20_10; last column sma50_close):

| super_prob   |          n |   avgR |   win |   avgR_sma50 |
|:-------------|-----------:|-------:|------:|-------------:|
| low          | 102704.000 | -0.000 | 0.475 |       -0.104 |
| mid          | 102698.000 |  0.059 | 0.446 |       -0.062 |
| high         | 102700.000 |  0.149 | 0.422 |        0.181 |

## 11. Qullamaggie replication (per trade, out-of-sample 2018+; IS in brackets)

Scan = top 3% performer over 1, 3 or 6 months with ADR >= 4%. Regime = QQQ above its 10- and 20-day SMAs. qull_breakout = buy-stop above the flag high the next day (fill at the trigger or the gap open), stop at the tighter of the 3-day low and 1 ADR; a same-day touch of the stop counts as stopped out. Portfolio rows start with QULL in section 9.

| entry            | filter           | exit          |   IS_n |   IS_win |   IS_avgR |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:-----------------|:--------------|-------:|---------:|----------:|--------:|-------------:|----------:|-----------:|---------:|--------:|
| ep_gap10         | all              | bracket_20_10 |    530 |     0.47 |      0.19 |     933 |       106.49 |      0.41 |       0.11 |     1.19 |    2.39 |
| ep_gap10         | all              | qull_sma10    |    545 |     0.44 |     -0.01 |     933 |       106.49 |      0.45 |       0.01 |     1.01 |    0.13 |
| ep_gap10         | all              | qull_sma20    |    543 |     0.45 |     -0.04 |     933 |       106.49 |      0.45 |       0.07 |     1.14 |    1.26 |
| ep_gap10         | all              | sma50_close   |    534 |     0.29 |      0.14 |     933 |       106.49 |      0.31 |       0.49 |     1.74 |    3.60 |
| ep_gap10         | qull_scan        | bracket_20_10 |    124 |     0.36 |      0.06 |     261 |        29.79 |      0.43 |       0.22 |     1.37 |    2.40 |
| ep_gap10         | qull_scan        | qull_sma10    |    126 |     0.40 |     -0.06 |     261 |        29.79 |      0.43 |      -0.04 |     0.93 |   -0.47 |
| ep_gap10         | qull_scan        | qull_sma20    |    124 |     0.42 |     -0.09 |     261 |        29.79 |      0.44 |       0.14 |     1.27 |    1.19 |
| ep_gap10         | qull_scan        | sma50_close   |    122 |     0.20 |      0.01 |     261 |        29.79 |      0.32 |       0.83 |     2.25 |    2.67 |
| ep_gap10         | qull_scan_regime | bracket_20_10 |     82 |     0.34 |     -0.01 |     160 |        18.26 |      0.41 |       0.19 |     1.31 |    1.59 |
| ep_gap10         | qull_scan_regime | qull_sma10    |     83 |     0.41 |     -0.08 |     160 |        18.26 |      0.43 |      -0.03 |     0.93 |   -0.33 |
| ep_gap10         | qull_scan_regime | qull_sma20    |     83 |     0.43 |     -0.04 |     160 |        18.26 |      0.45 |       0.23 |     1.46 |    1.38 |
| ep_gap10         | qull_scan_regime | sma50_close   |     81 |     0.17 |      0.10 |     160 |        18.26 |      0.33 |       1.01 |     2.54 |    2.36 |
| ep_gap8_hold     | all              | bracket_20_10 |    733 |     0.48 |      0.21 |    1182 |       134.91 |      0.42 |       0.11 |     1.20 |    2.85 |
| ep_gap8_hold     | all              | qull_sma10    |    750 |     0.46 |      0.01 |    1182 |       134.91 |      0.46 |      -0.01 |     0.98 |   -0.32 |
| ep_gap8_hold     | all              | qull_sma20    |    749 |     0.48 |      0.03 |    1182 |       134.91 |      0.46 |       0.04 |     1.07 |    0.79 |
| ep_gap8_hold     | all              | sma50_close   |    741 |     0.33 |      0.26 |    1182 |       134.91 |      0.32 |       0.37 |     1.58 |    3.45 |
| ep_gap8_hold     | qull_scan        | bracket_20_10 |    147 |     0.36 |      0.03 |     284 |        32.42 |      0.45 |       0.26 |     1.45 |    2.91 |
| ep_gap8_hold     | qull_scan        | qull_sma10    |    150 |     0.41 |     -0.08 |     284 |        32.42 |      0.50 |       0.06 |     1.14 |    0.84 |
| ep_gap8_hold     | qull_scan        | qull_sma20    |    149 |     0.42 |     -0.04 |     284 |        32.42 |      0.51 |       0.20 |     1.45 |    1.91 |
| ep_gap8_hold     | qull_scan        | sma50_close   |    148 |     0.22 |      0.05 |     284 |        32.42 |      0.34 |       0.85 |     2.30 |    2.95 |
| ep_gap8_hold     | qull_scan_regime | bracket_20_10 |    103 |     0.35 |     -0.01 |     175 |        19.97 |      0.43 |       0.23 |     1.39 |    2.02 |
| ep_gap8_hold     | qull_scan_regime | qull_sma10    |    105 |     0.42 |     -0.09 |     175 |        19.97 |      0.50 |       0.04 |     1.08 |    0.39 |
| ep_gap8_hold     | qull_scan_regime | qull_sma20    |    105 |     0.42 |     -0.01 |     175 |        19.97 |      0.51 |       0.25 |     1.55 |    1.66 |
| ep_gap8_hold     | qull_scan_regime | sma50_close   |    104 |     0.20 |      0.15 |     175 |        19.97 |      0.34 |       0.98 |     2.49 |    2.48 |
| qull_breakout    | all              | bracket_20_10 |   2543 |     0.37 |      0.00 |    4385 |       500.51 |      0.41 |       0.15 |     1.25 |    6.77 |
| qull_breakout    | all              | qull_sma10    |   2554 |     0.33 |     -0.32 |    4385 |       500.51 |      0.33 |      -0.25 |     0.64 |  -10.81 |
| qull_breakout    | all              | qull_sma20    |   2552 |     0.33 |     -0.34 |    4385 |       500.51 |      0.33 |      -0.22 |     0.69 |   -7.99 |
| qull_breakout    | all              | sma50_close   |   2547 |     0.14 |     -0.38 |    4385 |       500.51 |      0.17 |       0.02 |     1.02 |    0.24 |
| qull_breakout    | qull_scan        | bracket_20_10 |    647 |     0.39 |      0.11 |    1212 |       138.34 |      0.38 |       0.09 |     1.14 |    2.13 |
| qull_breakout    | qull_scan        | qull_sma10    |    649 |     0.35 |     -0.27 |    1212 |       138.34 |      0.36 |      -0.17 |     0.73 |   -4.06 |
| qull_breakout    | qull_scan        | qull_sma20    |    649 |     0.35 |     -0.26 |    1212 |       138.34 |      0.35 |      -0.15 |     0.77 |   -3.06 |
| qull_breakout    | qull_scan        | sma50_close   |    647 |     0.16 |     -0.29 |    1212 |       138.34 |      0.17 |       0.06 |     1.07 |    0.44 |
| qull_breakout    | qull_scan_regime | bracket_20_10 |    440 |     0.38 |      0.07 |     783 |        89.37 |      0.41 |       0.19 |     1.31 |    3.50 |
| qull_breakout    | qull_scan_regime | qull_sma10    |    442 |     0.34 |     -0.30 |     783 |        89.37 |      0.37 |      -0.13 |     0.80 |   -2.26 |
| qull_breakout    | qull_scan_regime | qull_sma20    |    442 |     0.35 |     -0.29 |     783 |        89.37 |      0.37 |      -0.06 |     0.91 |   -0.90 |
| qull_breakout    | qull_scan_regime | sma50_close   |    440 |     0.17 |     -0.27 |     783 |        89.37 |      0.19 |       0.28 |     1.33 |    1.33 |
| qull_breakout_60 | all              | bracket_20_10 |    914 |     0.35 |     -0.00 |    1862 |       212.53 |      0.42 |       0.19 |     1.32 |    5.60 |
| qull_breakout_60 | all              | qull_sma10    |    914 |     0.36 |     -0.31 |    1862 |       212.53 |      0.32 |      -0.25 |     0.64 |   -7.04 |
| qull_breakout_60 | all              | qull_sma20    |    914 |     0.35 |     -0.33 |    1862 |       212.53 |      0.32 |      -0.22 |     0.69 |   -5.36 |
| qull_breakout_60 | all              | sma50_close   |    914 |     0.14 |     -0.33 |    1862 |       212.53 |      0.17 |       0.12 |     1.13 |    0.85 |
| qull_breakout_60 | qull_scan        | bracket_20_10 |    389 |     0.37 |      0.06 |     850 |        97.02 |      0.39 |       0.12 |     1.19 |    2.38 |
| qull_breakout_60 | qull_scan        | qull_sma10    |    389 |     0.35 |     -0.28 |     850 |        97.02 |      0.35 |      -0.20 |     0.70 |   -3.83 |
| qull_breakout_60 | qull_scan        | qull_sma20    |    389 |     0.35 |     -0.26 |     850 |        97.02 |      0.35 |      -0.18 |     0.73 |   -3.04 |
| qull_breakout_60 | qull_scan        | sma50_close   |    389 |     0.16 |     -0.30 |     850 |        97.02 |      0.16 |       0.12 |     1.14 |    0.63 |
| qull_breakout_60 | qull_scan_regime | bracket_20_10 |    270 |     0.36 |      0.02 |     577 |        65.86 |      0.42 |       0.22 |     1.37 |    3.53 |
| qull_breakout_60 | qull_scan_regime | qull_sma10    |    270 |     0.33 |     -0.34 |     577 |        65.86 |      0.36 |      -0.18 |     0.73 |   -2.72 |
| qull_breakout_60 | qull_scan_regime | qull_sma20    |    270 |     0.33 |     -0.30 |     577 |        65.86 |      0.36 |      -0.11 |     0.83 |   -1.41 |
| qull_breakout_60 | qull_scan_regime | sma50_close   |    270 |     0.15 |     -0.34 |     577 |        65.86 |      0.18 |       0.29 |     1.33 |    1.07 |
| random_uptrend   | all              | bracket_20_10 |  30431 |     0.53 |      0.19 |   34126 |      3895.16 |      0.45 |       0.09 |     1.18 |   13.79 |
| random_uptrend   | all              | qull_sma10    |  31241 |     0.30 |     -0.14 |   34126 |      3895.16 |      0.30 |      -0.11 |     0.87 |   -8.49 |
| random_uptrend   | all              | qull_sma20    |  31198 |     0.30 |     -0.13 |   34126 |      3895.16 |      0.29 |      -0.10 |     0.88 |   -6.78 |
| random_uptrend   | all              | sma50_close   |  31018 |     0.15 |     -0.04 |   34126 |      3895.16 |      0.14 |      -0.03 |     0.97 |   -1.13 |
| random_uptrend   | qull_scan        | bracket_20_10 |    997 |     0.36 |      0.01 |    1998 |       228.05 |      0.40 |       0.15 |     1.24 |    4.50 |
| random_uptrend   | qull_scan        | qull_sma10    |   1000 |     0.31 |     -0.07 |    1998 |       228.05 |      0.31 |      -0.02 |     0.98 |   -0.30 |
| random_uptrend   | qull_scan        | qull_sma20    |    999 |     0.31 |     -0.05 |    1998 |       228.05 |      0.31 |       0.04 |     1.06 |    0.71 |
| random_uptrend   | qull_scan        | sma50_close   |    998 |     0.15 |     -0.19 |    1998 |       228.05 |      0.16 |       0.14 |     1.15 |    1.49 |
| random_uptrend   | qull_scan_regime | bracket_20_10 |    591 |     0.37 |      0.02 |    1198 |       136.74 |      0.41 |       0.18 |     1.29 |    4.11 |
| random_uptrend   | qull_scan_regime | qull_sma10    |    594 |     0.34 |     -0.11 |    1198 |       136.74 |      0.31 |      -0.02 |     0.97 |   -0.32 |
| random_uptrend   | qull_scan_regime | qull_sma20    |    593 |     0.33 |     -0.09 |    1198 |       136.74 |      0.32 |       0.04 |     1.06 |    0.53 |
| random_uptrend   | qull_scan_regime | sma50_close   |    592 |     0.15 |     -0.29 |    1198 |       136.74 |      0.16 |       0.19 |     1.19 |    1.41 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                                              |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:--------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| donchian_20 / all / bracket_20_10                                                     |   0.09 |    -0.44 |             -0.42 |   802.00 |   0.41 |            9.31 |               1.02 |
| pocket_pivot / all / bracket_20_10                                                    |   0.08 |    -0.35 |             -0.31 |   570.00 |   0.42 |            7.27 |               0.57 |
| donchian_55 / all / bracket_20_10                                                     |   0.03 |    -0.38 |             -0.34 |   744.00 |   0.41 |            9.05 |               2.12 |
| undercut / all / bracket_20_10                                                        |   0.20 |    -0.36 |             -0.30 |   599.00 |   0.45 |            7.75 |               0.63 |
| high52 / all / bracket_10_10                                                          |  -0.03 |    -0.53 |             -0.51 |  1007.00 |   0.51 |            7.56 |             nan    |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                     |   0.09 |    -0.31 |             -0.29 |   636.00 |   0.42 |            8.30 |               0.68 |
| All setups, ranked by RS / bracket_20_10                                              |   0.16 |    -0.36 |             -0.34 |  1075.00 |   0.41 |            9.02 |               0.55 |
| All setups, random order / bracket_20_10                                              |   0.05 |    -0.41 |             -0.35 |   483.00 |   0.43 |            7.88 |               1.03 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                          |   0.10 |    -0.28 |             -0.27 |   803.00 |   0.40 |            8.53 |               0.61 |
| BASELINE random entries, ranked by RS / bracket_20_10                                 |   0.08 |    -0.46 |             -0.44 |   662.00 |   0.41 |            7.68 |               1.02 |
| BASELINE random entries, random order / bracket_20_10                                 |   0.05 |    -0.36 |             -0.32 |   459.00 |   0.46 |            7.75 |               1.24 |
| IS-selected setups (3), ranked by RS / bracket_20_10                                  |   0.04 |    -0.40 |             -0.38 |   522.00 |   0.43 |            7.89 |               1.43 |
| IS-selected setups, only when SPY > 200d / bracket_20_10                              |  -0.02 |    -0.43 |             -0.42 |   421.00 |   0.39 |            6.76 |             nan    |
| IS-selected setups (21), ranked by RS / sma50_close                                   |   0.12 |    -0.53 |             -0.45 |   917.00 |   0.25 |            8.79 |               0.66 |
| IS-selected setups, only when SPY > 200d / sma50_close                                |   0.12 |    -0.52 |             -0.47 |   786.00 |   0.24 |            7.64 |               0.79 |
| All setups, ranked by RS / sma50_close                                                |   0.13 |    -0.53 |             -0.49 |  1188.00 |   0.26 |            8.75 |               0.71 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                           |   0.10 |    -0.33 |             -0.25 |   444.00 |   0.31 |            5.63 |               0.68 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                          |   0.13 |    -0.28 |             -0.19 |   616.00 |   0.34 |            7.70 |               0.57 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                          |   0.14 |    -0.26 |             -0.18 |   620.00 |   0.34 |            7.84 |               0.62 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)              |   0.17 |    -0.24 |             -0.16 |   607.00 |   0.35 |            7.97 |               0.59 |
| Top 20 by IS expectancy, ranked by superperformer model                               |   0.11 |    -0.25 |             -0.23 |   647.00 |   0.33 |            7.83 |               0.59 |
| All setups, ranked by superperformer model / bracket_20_10                            |   0.23 |    -0.44 |             -0.40 |  1362.00 |   0.40 |            9.02 |               0.59 |
| Only setups in the model's top 10% likely superperformers / sma50_close               |   0.21 |    -0.47 |             -0.43 |  1388.00 |   0.29 |            8.63 |               0.56 |
| CHECK random entries in the model's top 10% / sma50_close                             |   0.21 |    -0.45 |             -0.40 |   971.00 |   0.14 |            5.27 |               0.53 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close              |   0.12 |    -0.47 |             -0.39 |  1312.00 |   0.28 |            8.67 |               0.55 |
| Top 10% model + adaptive sizing / sma50_close                                         |   0.22 |    -0.42 |             -0.35 |  1482.00 |   0.30 |            9.13 |               0.52 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                  |   0.16 |    -0.41 |             -0.34 |  1364.00 |   0.30 |            8.90 |               0.74 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                     |   0.27 |    -0.37 |             -0.37 |  1235.00 |   0.42 |            9.43 |               0.54 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                             |   0.16 |    -0.44 |             -0.43 |  1207.00 |   0.41 |            9.22 |               0.76 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                               |   0.14 |    -0.37 |             -0.33 |   945.00 |   0.40 |            8.59 |               0.50 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                   |   0.15 |    -0.28 |             -0.24 |   748.00 |   0.42 |            8.05 |               0.73 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                     |   0.11 |    -0.36 |             -0.33 |  1260.00 |   0.56 |            8.38 |               0.58 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                             |   0.11 |    -0.36 |             -0.34 |  1233.00 |   0.56 |            8.11 |               0.55 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                               |   0.14 |    -0.32 |             -0.32 |  1024.00 |   0.56 |            6.93 |               0.70 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                   |   0.08 |    -0.25 |             -0.24 |   830.00 |   0.56 |            6.81 |               0.92 |
| QULL scan+setups / qull_sma10                                                         |  -0.14 |    -0.76 |             -0.76 |  1129.00 |   0.39 |            3.35 |             nan    |
| QULL scan+setups / qull_sma20                                                         |  -0.11 |    -0.71 |             -0.70 |   987.00 |   0.39 |            4.00 |             nan    |
| QULL scan+setups / sma50_close                                                        |   0.08 |    -0.48 |             -0.38 |   659.00 |   0.20 |            5.56 |               1.18 |
| QULL scan+setups / bracket_20_10                                                      |   0.05 |    -0.39 |             -0.38 |   715.00 |   0.39 |            5.61 |               1.63 |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma10                            |  -0.07 |    -0.52 |             -0.49 |   740.00 |   0.39 |            2.27 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma10                                      |  -0.07 |    -0.50 |             -0.47 |   838.00 |   0.39 |            2.53 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma20                            |  -0.02 |    -0.39 |             -0.35 |   661.00 |   0.41 |            2.83 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma20                                      |  -0.00 |    -0.34 |             -0.28 |   739.00 |   0.40 |            3.14 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / sma50_close                           |   0.18 |    -0.45 |             -0.32 |   463.00 |   0.23 |            4.18 |               0.63 |
| QULL ... + regime + adaptive sizing / sma50_close                                     |   0.14 |    -0.34 |             -0.25 |   484.00 |   0.24 |            4.41 |               0.79 |
| QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20                    |  -0.02 |    -0.29 |             -0.29 |    92.00 |   0.30 |            0.30 |             nan    |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close     |   0.46 |    -0.30 |             -0.23 |   865.00 |   0.33 |            6.88 |               0.39 |
| SURVIVORSHIP S&P 500 names, only after joining the index (2726 signals) / sma50_close |   0.18 |    -0.30 |             -0.24 |   710.00 |   0.32 |            5.27 |               0.79 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY                          |   0.15 |    -0.34 |             -0.27 |   610.00 |   0.34 |            7.63 |               0.52 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY                          |   0.13 |    -0.39 |             -0.32 |   479.00 |   0.34 |            5.98 |               0.64 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY                          |   0.13 |    -0.39 |             -0.32 |   479.00 |   0.34 |            5.98 |               0.64 |
| SPY buy & hold                                                                        |   0.15 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.

Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):

| entry             | filter      | exit            |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_t |
|:------------------|:------------|:----------------|-------:|----------:|--------:|-----------:|--------:|
| ep_gap10_vol2     | rs80_mkt    | sma50_close     |    209 |      0.61 |     394 |       0.64 |    2.53 |
| ep_gap5           | rs80_early  | sma50_close     |    324 |      0.57 |     462 |       0.40 |    2.36 |
| ep_gap8_hold      | rs80_mkt    | sma50_close     |    286 |      0.53 |     418 |       0.46 |    1.99 |
| ep_gap10_vol2     | rs80_mkt    | chandelier_3atr |    211 |      0.52 |     394 |       0.24 |    1.84 |
| ep_gap5           | rs80_mkt    | sma50_close     |    603 |      0.50 |     736 |       0.30 |    2.04 |
| ep_gap8_neglected | rs80        | sma50_close     |    233 |      0.50 |     324 |       0.60 |    2.66 |
| falling_wedge     | mkt_ok      | oneil_20_8      |    702 |      0.49 |     902 |       0.11 |    1.65 |
| falling_wedge     | all         | oneil_20_8      |   1271 |      0.48 |    1506 |       0.19 |    3.60 |
| ep_gap10_vol2     | rs80_mkt    | donchian_10low  |    212 |      0.43 |     394 |       0.31 |    2.18 |
| ep_gap8_hold      | early_stage | sma50_close     |    340 |      0.42 |     593 |       0.46 |    3.15 |

Year-by-year returns (best 3 portfolios by CAGR vs SPY):

|      |   SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |   GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10 |   All setups, ranked by superperformer model / bracket_20_10 |   SPY |
|-----:|------------------------------------------------------------------------------------:|--------------------------------------------------------------------:|-------------------------------------------------------------:|------:|
| 2018 |                                                                                11.2 |                                                               -15.9 |                                                        -10.5 |  -5.2 |
| 2019 |                                                                                39.0 |                                                                49.5 |                                                         85.8 |  31.2 |
| 2020 |                                                                                28.2 |                                                                96.4 |                                                         55.6 |  18.3 |
| 2021 |                                                                                28.0 |                                                                14.2 |                                                         32.3 |  28.7 |
| 2022 |                                                                                -5.1 |                                                                -9.5 |                                                        -20.2 | -18.2 |
| 2023 |                                                                                72.3 |                                                                 5.7 |                                                         39.7 |  26.2 |
| 2024 |                                                                                82.0 |                                                                26.8 |                                                         17.8 |  24.9 |
| 2025 |                                                                                91.0 |                                                                55.5 |                                                         41.1 |  17.7 |
| 2026 |                                                                                93.9 |                                                                47.6 |                                                         -3.7 |  14.9 |

## Appendix: entries and exits

| entry             | source / rule                                                    |   signals |
|:------------------|:-----------------------------------------------------------------|----------:|
| donchian_20       | Turtle 20-day breakout / trading-range break (Brock et al. 1992) |    148915 |
| donchian_55       | Turtle 55-day breakout                                           |     99232 |
| high52            | 52-week-high breakout (George & Hwang 2004)                      |     59825 |
| high52_fresh      | 52-week high after >= 20 days of consolidation                   |     16712 |
| base_25           | O'Neil/Darvas 5-week base breakout                               |      4385 |
| base_50           | O'Neil 10-week base breakout                                     |      4961 |
| vcp               | Minervini volatility contraction pattern                         |      2212 |
| flag_30           | Qullamaggie flag after a 30%+ move                               |      2954 |
| flag_60           | Qullamaggie flag after a 60%+ move                               |       951 |
| flag_30_early     | Qullamaggie flag, early entry inside the flag                    |      3175 |
| htf               | High tight flag (O'Neil / Bulkowski)                             |       151 |
| ep_gap5           | Gap up >= 5% on 3x volume                                        |      4215 |
| ep_gap10          | Episodic pivot: gap >= 10% on 3x volume                          |      1478 |
| ep_gap8_neglected | Episodic pivot from neglect (Qullamaggie)                        |      1553 |
| ep_gap15          | Episodic pivot: gap >= 15% on 3x volume                          |       535 |
| ep_gap10_vol2     | EP variant: gap >= 10% on only 2x volume                         |      1810 |
| ep_gap10_vol5     | EP variant: gap >= 10% on 5x volume                              |       774 |
| ep_gap8_hold      | EP variant: gap >= 8%, closes above the open                     |      1932 |
| pocket_pivot      | Morales & Kacher pocket pivot                                    |     97990 |
| asc_triangle      | Ascending triangle breakout (flat top, rising lows)              |      1996 |
| desc_triangle     | Descending triangle, upside breakout                             |      1500 |
| sym_triangle      | Symmetrical triangle breakout (pennant)                          |      1816 |
| falling_wedge     | Falling wedge breakout                                           |      2797 |
| rising_wedge      | Rising wedge, upside breakout                                    |      3874 |
| tight_coil_7      | 7-day coil: closes within 1 ADR, breakout on volume              |     11881 |
| tight_coil_15     | 15-day coil: closes within 1.5 ADR, breakout on volume           |      2352 |
| stage2            | Weinstein stage 2 breakout                                       |     10969 |
| ema_retest        | 8/21 EMA cross -> break -> retest (your playbook)                |     30387 |
| multi_touch       | Multi-touch level breakout on volume (your playbook)             |     23459 |
| undercut          | Undercut & rally (your playbook)                                 |     49694 |
| qull_breakout     | Qullamaggie breakout: buy-stop above the flag high next day      |      6942 |
| qull_breakout_60  | Qullamaggie breakout after a 60%+ move                           |      2778 |
| random_uptrend    | BASELINE: random entries in an uptrend                           |     65480 |

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