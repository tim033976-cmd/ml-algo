# Strategy research report

Generated 2026-10-08 14:27 UTC in 22 min.
Universe: 1488 stocks with data (sp600: 591, sp500: 499, sp400: 398; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-06: 659,965.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.54). Top 20 by IS t-stat: +0.060R OOS; top 20 by IS avgR (n>=200): +0.323R; all strategies +0.047R; random entries -0.042R.
- Too few signals to judge (need 100+ per period): htf (IS 52, OOS 99).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.29R, OOS +0.27R), ep_gap10_vol5 (IS +0.17R, OOS +0.20R), desc_triangle (IS +0.18R, OOS +0.17R), ep_gap8_hold (IS +0.17R, OOS +0.17R), ep_gap8_neglected (IS +0.20R, OOS +0.15R), falling_wedge (IS +0.24R, OOS +0.11R), ep_gap5 (IS +0.13R, OOS +0.11R), ep_gap10 (IS +0.10R, OOS +0.21R), undercut (IS +0.12R, OOS +0.08R), donchian_20 (IS +0.10R, OOS +0.07R), ep_gap10_vol2 (IS +0.07R, OOS +0.22R), ema_retest (IS +0.09R, OOS +0.06R), sym_triangle (IS +0.06R, OOS +0.11R), donchian_55 (IS +0.08R, OOS +0.05R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, stage2.
- Best exit out-of-sample (avg over entries): sma50_close (+0.114R); worst: qull_sma10 (-0.035R).
- Filters that help OOS: rs80_early (+0.109R), rs80_early_theme (+0.057R), early_stage (+0.045R), rs80 (+0.030R); that hurt: none.
- ML filter adds little: OOS rank corr 0.003, AUC 0.506, decile monotonicity -0.30, taken +0.078R vs skipped +0.063R.
- Features the model relies on most: rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.07R, OOS +0.03R), rs80_early (IS +0.05R, OOS +0.08R), rs80_early_theme (IS +0.09R, OOS +0.04R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558` (IS +0.35R, OOS +0.14R, n=29868).
- Superperformer model: 30.4% of its top-10% picks gained >= 40% within 3 months vs 7.1% for all stocks (4.3x), AUC 0.834. Driven by: adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 56% (break-even ~50%), avg net return per trade +1.5%. Point-in-time S&P 500 top 10%: 58%, +2.3% per trade (n=7002).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 38% (break-even ~33%), avg net return per trade +2.6%. Point-in-time S&P 500 top 10%: 39%, +3.9% per trade (n=4264).
- Best portfolio 2018->today: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close at 46.9% CAGR (max drawdown -31.5%) vs SPY 14.6%.
- Best return per unit of drawdown: SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close (46.9% CAGR, -31.5% max DD).

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, stage2.
3. Focus development on: ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55 (tune them on IS data only, re-check OOS).
4. Make rs80_early a default filter.
5. Inspect rates_rising and sma200_slope: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                 | no_edge_entries                           | best_exit   | helpful_filters                                           |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                  | filters_lifting_baseline                  |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                             |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------|:------------|:----------------------------------------------------------|---------:|---------------:|---------------:|---------:|:--------------------------------------------------------------|:------------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:-----------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|
| 2026-10-08 08:22 | 5e93689  |      1488 |    633749 |        0.57 |        0.05 |          -0.07 | donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50                               | multi_touch, high52, stage2               | sma50_close | rs80_early, early_stage, rs80, rs80_mkt                   |     0.55 |           0.25 |          -0.07 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank           | early_stage, rs80_early                   |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | nan                                                                               |      nan    |       nan    | nan                                                        |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 08:48 | 48a9d03  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank           | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                        |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:11 | fd50739  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank           | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8                         |      nan    |       nan    | nan                                                        |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:33 | 32c75da  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low     | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                        |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 09:57 | 54a58fb  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low     | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8                                             |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS                      |      nan    |       nan    | nan                                                        |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:25 | d8d63d9  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low     | early_stage, rs80_early, rs80_early_theme |            4 | Only setups in the model's top 10% likely superperformers / sma50_close           |        0.28 |       0.15 | Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)          |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 10:53 | d8399f4  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2               | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low     | early_stage, rs80_early, rs80_early_theme |            4 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct |             nan    |             nan    |             nan    |             nan    |
| 2026-10-08 14:02 | 749e984  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct |               0.56 |               0.02 |               0.38 |               0.03 |
| 2026-10-08 14:27 | e7af2f7  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                       | high52, multi_touch, pocket_pivot, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct |               0.56 |               0.02 |               0.38 |               0.03 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 3069.000 |
| strategies_with_enough_trades | 2488.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.537 |
| rank_corr_IS_vs_OOS_t         |    0.576 |
| OOS_avgR_all_strategies       |    0.047 |
| OOS_avgR_top20_by_IS          |    0.060 |
| OOS_avgR_top20_by_IS_avgR     |    0.323 |
| OOS_avgR_random_baseline      |   -0.042 |
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
| sma50_close     |      0.09 |       0.11 |      0.26 |     1.17 |                       0.63 |
| bracket_20_10   |      0.17 |       0.08 |      0.43 |     1.16 |                       0.47 |
| oneil_20_8      |      0.14 |       0.04 |      0.26 |     1.06 |                       0.80 |
| bracket_10_10   |      0.13 |       0.03 |      0.52 |     1.07 |                       0.20 |
| trim_ema        |      0.03 |       0.03 |      0.34 |     1.05 |                       0.83 |
| donchian_10low  |      0.04 |       0.02 |      0.29 |     1.05 |                       0.77 |
| chandelier_3atr |      0.05 |       0.01 |      0.29 |     1.03 |                       0.77 |
| fixed_3r_20d    |      0.01 |      -0.00 |      0.37 |     1.01 |                       0.87 |
| ema21_close     |     -0.02 |      -0.01 |      0.30 |     0.99 |                       0.77 |
| qull_sma20      |     -0.03 |      -0.03 |      0.43 |     0.96 |                       0.83 |
| qull_sma10      |     -0.04 |      -0.04 |      0.42 |     0.93 |                       0.90 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| rs80_early       |      0.10 |       0.13 |      0.38 |
| rs80_early_theme |      0.12 |       0.08 |      0.37 |
| early_stage      |      0.08 |       0.07 |      0.37 |
| rs80             |      0.06 |       0.05 |      0.37 |
| rs80_mkt         |      0.08 |       0.04 |      0.36 |
| rs80_theme       |      0.05 |       0.03 |      0.36 |
| all              |      0.05 |       0.02 |      0.36 |
| theme            |      0.05 |       0.02 |      0.36 |
| mkt_ok           |      0.06 |       0.02 |      0.35 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.003; AUC for R > 0: 0.506 (0.5 = no skill). Taken (model's top third, causal threshold): n=84,728, avgR=0.078, win=0.458. Skipped: n=217,127, avgR=0.063, win=0.445.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 30186.00 |   0.09 |  0.44 |
|      1 | 30185.00 |   0.09 |  0.44 |
|      2 | 30186.00 |   0.08 |  0.45 |
|      3 | 30185.00 |   0.05 |  0.44 |
|      4 | 30186.00 |   0.06 |  0.45 |
|      5 | 30185.00 |   0.07 |  0.45 |
|      6 | 30185.00 |   0.04 |  0.44 |
|      7 | 30186.00 |   0.04 |  0.45 |
|      8 | 30185.00 |   0.06 |  0.45 |
|      9 | 30186.00 |   0.10 |  0.47 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| flag_60           |   615.00 |       0.16 |    174.00 |         0.30 |           0.11 |
| flag_30           |  1786.00 |       0.12 |    473.00 |         0.23 |           0.08 |
| ep_gap15          |   374.00 |       0.21 |    195.00 |         0.23 |           0.19 |
| htf               |    99.00 |      -0.07 |     27.00 |         0.22 |          -0.18 |
| falling_wedge     |  1506.00 |       0.17 |    587.00 |         0.19 |           0.16 |
| undercut          | 26314.00 |       0.12 |   9849.00 |         0.16 |           0.10 |
| ep_gap5           |  2322.00 |       0.08 |    931.00 |         0.16 |           0.02 |
| flag_30_early     |  1955.00 |       0.18 |    492.00 |         0.15 |           0.19 |
| ep_gap8_hold      |  1182.00 |       0.11 |    494.00 |         0.14 |           0.09 |
| base_25           |  2444.00 |       0.11 |    722.00 |         0.14 |           0.10 |
| ep_gap10          |   933.00 |       0.11 |    416.00 |         0.13 |           0.09 |
| ep_gap10_vol5     |   454.00 |       0.12 |    218.00 |         0.13 |           0.11 |
| ep_gap8_neglected |   934.00 |       0.08 |    380.00 |         0.12 |           0.05 |
| ep_gap10_vol2     |  1182.00 |       0.15 |    520.00 |         0.12 |           0.17 |
| base_50           |  2665.00 |       0.10 |    788.00 |         0.11 |           0.09 |
| tight_coil_15     |  1039.00 |      -0.01 |    307.00 |         0.10 |          -0.06 |
| rising_wedge      |  1747.00 |       0.05 |    486.00 |         0.09 |           0.03 |
| ema_retest        | 15672.00 |       0.08 |   4440.00 |         0.08 |           0.07 |
| vcp               |   879.00 |       0.05 |    226.00 |         0.08 |           0.04 |
| pocket_pivot      | 48059.00 |       0.06 |  13027.00 |         0.07 |           0.06 |
| donchian_55       | 50722.00 |       0.06 |  12884.00 |         0.07 |           0.05 |
| high52            | 29119.00 |       0.04 |   6931.00 |         0.06 |           0.04 |
| donchian_20       | 78114.00 |       0.07 |  21133.00 |         0.06 |           0.08 |
| sym_triangle      |   915.00 |       0.11 |    249.00 |         0.05 |           0.13 |
| high52_fresh      |  8415.00 |       0.05 |   2297.00 |         0.04 |           0.06 |
| multi_touch       | 10634.00 |       0.01 |   2987.00 |         0.03 |          -0.00 |
| tight_coil_7      |  5359.00 |       0.03 |   1462.00 |         0.02 |           0.03 |
| stage2            |  4847.00 |       0.01 |   1564.00 |         0.02 |           0.01 |
| desc_triangle     |   706.00 |       0.10 |    226.00 |         0.02 |           0.14 |
| asc_triangle      |   863.00 |       0.06 |    243.00 |        -0.05 |           0.10 |

- Same model on episodic pivots only / sma50_close: rank corr 0.003, taken avgR 0.354 (n=3,279) vs skipped 0.353 (n=4,102).
- Same model on your trim plan (trim_ema): rank corr 0.117, taken avgR 0.001 (n=93,241) vs skipped -0.053 (n=208,614).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature       |   rank_corr_drop |
|:--------------|-----------------:|
| rates_rising  |           0.0114 |
| sma200_slope  |           0.0067 |
| above_52w_low |           0.0049 |
| sector_rs     |           0.0049 |
| adr_pct       |           0.0043 |
| rs_rank       |           0.0040 |
| industry_rs   |           0.0035 |
| mkt_ret_21    |           0.0031 |
| base_count    |           0.0026 |
| mkt_above200  |           0.0023 |
| risk_pct      |           0.0017 |
| atr_ratio     |           0.0013 |
| dist_sma50    |           0.0011 |
| risk_adr      |           0.0008 |
| industry_rank |           0.0008 |
| mkt_ok        |           0.0007 |
| atr_pct       |           0.0007 |
| updown_vol_50 |           0.0006 |
| leg2_range    |           0.0005 |
| ext_ema8_adr  |           0.0004 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.558    |   8044 |      0.64 |   11681 |       0.08 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.558   |  17784 |      0.35 |   29868 |       0.14 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.483 |  67596 |      0.29 |   53565 |      -0.00 |      0.46 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 > 0.754    |   4348 |      0.27 |     635 |       0.57 |      0.57 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.483  |  51985 |      0.17 |   37738 |      -0.01 |      0.40 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 <= 0.0455   |  73893 |      0.17 |  103591 |       0.09 |      0.45 |
| rates_rising <= 0.5 AND mkt_above200 > 0.5 AND qqq_ret_21 > 0.0455    |  41065 |      0.01 |   60069 |       0.09 |      0.44 |
| rates_rising <= 0.5 AND mkt_above200 <= 0.5 AND breadth_50 <= 0.754   |  19172 |     -0.17 |    4708 |       0.21 |      0.47 |

## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?

Every stock every 10 trading days (n=279,586 out-of-sample rows). Base rate of a >= 40% gain within 3 months: 7.1%. The model's top 10% hit it 30.4% of the time (4.3x the base rate). AUC 0.834.

|   super_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 27959.000 |      0.001 |          -0.005 |              0.009 |              0.068 |
|            1 | 27959.000 |      0.005 |           0.009 |              0.015 |              0.048 |
|            2 | 27958.000 |      0.010 |           0.015 |              0.018 |              0.053 |
|            3 | 27959.000 |      0.015 |           0.020 |              0.020 |              0.056 |
|            4 | 27958.000 |      0.026 |           0.026 |              0.024 |              0.062 |
|            5 | 27959.000 |      0.041 |           0.033 |              0.030 |              0.071 |
|            6 | 27958.000 |      0.063 |           0.041 |              0.034 |              0.082 |
|            7 | 27959.000 |      0.094 |           0.050 |              0.042 |              0.097 |
|            8 | 27958.000 |      0.152 |           0.064 |              0.045 |              0.120 |
|            9 | 27959.000 |      0.304 |           0.116 |              0.074 |              0.148 |

What matters most (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| adr_pct       |     0.0920 |
| above_52w_low |     0.0289 |
| dist_52w_high |     0.0222 |
| leg2_range    |     0.0052 |
| atr_pct       |     0.0051 |
| leg1_range    |     0.0050 |
| mkt_above200  |     0.0044 |
| tight_10      |     0.0024 |
| base_count    |     0.0014 |
| rs_rank       |     0.0009 |
| dist_ema21    |     0.0007 |
| sma150_slope  |     0.0007 |
| range_pos_12m |     0.0005 |
| sma200_slope  |     0.0004 |
| base_depth_60 |     0.0004 |

Profile: future superperformers vs everything else, at the moment of the sample:

|               |   future superperformers (median) |   everything else (median) |
|:--------------|----------------------------------:|---------------------------:|
| adr_pct       |                             0.045 |                      0.026 |
| above_52w_low |                             0.585 |                      0.340 |
| dist_52w_high |                            -0.275 |                     -0.128 |
| leg2_range    |                             0.193 |                      0.120 |
| atr_pct       |                             0.046 |                      0.027 |
| leg1_range    |                             0.184 |                      0.120 |
| mkt_above200  |                             1.000 |                      1.000 |
| tight_10      |                             0.153 |                      0.087 |
| base_count    |                             0.000 |                      1.000 |
| rs_rank       |                             0.503 |                      0.511 |
| dist_ema21    |                            -0.002 |                      0.006 |
| sma150_slope  |                             0.003 |                      0.008 |

Readable rules (depth-3 tree fit before 2018, scored after):

| rule                                                                 |   IS_n |   IS_rate |   OOS_n |   OOS_rate |
|:---------------------------------------------------------------------|-------:|----------:|--------:|-----------:|
| dist_52w_high <= -0.542 AND dist_52w_high <= -0.633                  |   2145 |     0.466 |     889 |      0.447 |
| dist_52w_high <= -0.542 AND dist_52w_high > -0.633                   |   2655 |     0.297 |    1264 |      0.287 |
| dist_52w_high > -0.542 AND adr_pct > 0.032 AND above_52w_low > 1.03  |   8679 |     0.143 |    6216 |      0.238 |
| dist_52w_high > -0.542 AND adr_pct > 0.032 AND above_52w_low <= 1.03 |  37513 |     0.068 |   18792 |      0.126 |
| dist_52w_high > -0.542 AND adr_pct <= 0.032 AND adr_pct > 0.025      |  35365 |     0.026 |   18929 |      0.038 |
| dist_52w_high > -0.542 AND adr_pct <= 0.032 AND adr_pct <= 0.025     | 113643 |     0.005 |   33910 |      0.010 |

Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate 6.7%, model top 10% 27.5% (4.1x), AUC 0.827.

|   clean_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 27959.000 |      0.001 |          -0.004 |              0.010 |              0.067 |
|            1 | 27959.000 |      0.005 |           0.010 |              0.015 |              0.049 |
|            2 | 27958.000 |      0.010 |           0.016 |              0.018 |              0.051 |
|            3 | 27959.000 |      0.016 |           0.019 |              0.019 |              0.056 |
|            4 | 27958.000 |      0.024 |           0.026 |              0.024 |              0.063 |
|            5 | 27959.000 |      0.038 |           0.034 |              0.030 |              0.069 |
|            6 | 27958.000 |      0.059 |           0.041 |              0.034 |              0.081 |
|            7 | 27959.000 |      0.094 |           0.051 |              0.042 |              0.099 |
|            8 | 27958.000 |      0.149 |           0.066 |              0.046 |              0.118 |
|            9 | 27959.000 |      0.275 |           0.111 |              0.069 |              0.152 |

### Your goal: +10% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 50% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 27959.000 |       0.266 |        0.396 |      0.351 |            0.004 |           0.017 |
|       1 | 27959.000 |       0.355 |        0.449 |      0.337 |            0.010 |           0.039 |
|       2 | 27958.000 |       0.401 |        0.468 |      0.366 |            0.009 |           0.046 |
|       3 | 27959.000 |       0.436 |        0.479 |      0.389 |            0.008 |           0.050 |
|       4 | 27958.000 |       0.466 |        0.486 |      0.406 |            0.007 |           0.057 |
|       5 | 27959.000 |       0.493 |        0.500 |      0.407 |            0.008 |           0.098 |
|       6 | 27958.000 |       0.521 |        0.510 |      0.410 |            0.009 |           0.098 |
|       7 | 27959.000 |       0.554 |        0.508 |      0.421 |            0.007 |           0.098 |
|       8 | 27958.000 |       0.597 |        0.513 |      0.422 |            0.008 |           0.098 |
|       9 | 27959.000 |       0.688 |        0.556 |      0.391 |            0.015 |           0.098 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 279586.000 |        0.487 |      0.390 |            0.008 |
| top 10%    |  27959.000 |        0.556 |      0.391 |            0.015 |
| top 5%     |  13980.000 |        0.578 |      0.374 |            0.019 |
| top 2%     |   5592.000 |        0.609 |      0.355 |            0.025 |
| top 1%     |   2796.000 |        0.628 |      0.351 |            0.027 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91558.000 |        0.466 |      0.348 |            0.011 |
| top 10%    |  7002.000 |        0.578 |      0.338 |            0.023 |
| top 5%     |  3541.000 |        0.604 |      0.328 |            0.027 |
| top 2%     |  1494.000 |        0.630 |      0.320 |            0.030 |
| top 1%     |   753.000 |        0.649 |      0.320 |            0.033 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 14276.000 |       0.264 |        0.394 |      0.308 |            0.008 |           0.024 |
|       1 | 12636.000 |       0.354 |        0.435 |      0.300 |            0.013 |           0.041 |
|       2 | 10827.000 |       0.401 |        0.454 |      0.327 |            0.012 |           0.045 |
|       3 |  9412.000 |       0.436 |        0.454 |      0.363 |            0.008 |           0.037 |
|       4 |  8593.000 |       0.465 |        0.464 |      0.386 |            0.007 |           0.042 |
|       5 |  7815.000 |       0.493 |        0.484 |      0.380 |            0.009 |           0.058 |
|       6 |  7314.000 |       0.521 |        0.499 |      0.373 |            0.012 |           0.087 |
|       7 |  6856.000 |       0.554 |        0.498 |      0.387 |            0.010 |           0.082 |
|       8 |  6827.000 |       0.597 |        0.503 |      0.388 |            0.010 |           0.098 |
|       9 |  7002.000 |       0.689 |        0.578 |      0.338 |            0.023 |           0.098 |

### Your goal: +20% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 33% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 27959.000 |       0.044 |        0.063 |      0.327 |            0.003 |          -0.001 |
|       1 | 27959.000 |       0.079 |        0.116 |      0.359 |            0.010 |          -0.000 |
|       2 | 27958.000 |       0.109 |        0.147 |      0.402 |            0.008 |          -0.010 |
|       3 | 27959.000 |       0.140 |        0.183 |      0.428 |            0.010 |          -0.019 |
|       4 | 27958.000 |       0.174 |        0.217 |      0.460 |            0.011 |          -0.032 |
|       5 | 27959.000 |       0.208 |        0.253 |      0.479 |            0.014 |          -0.047 |
|       6 | 27958.000 |       0.246 |        0.287 |      0.501 |            0.015 |          -0.102 |
|       7 | 27959.000 |       0.288 |        0.319 |      0.518 |            0.017 |          -0.102 |
|       8 | 27958.000 |       0.339 |        0.338 |      0.538 |            0.018 |          -0.102 |
|       9 | 27959.000 |       0.450 |        0.379 |      0.526 |            0.026 |          -0.102 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 279586.000 |        0.230 |      0.454 |            0.013 |
| top 10%    |  27959.000 |        0.379 |      0.526 |            0.026 |
| top 5%     |  13980.000 |        0.391 |      0.525 |            0.029 |
| top 2%     |   5592.000 |        0.410 |      0.524 |            0.032 |
| top 1%     |   2796.000 |        0.423 |      0.527 |            0.034 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 91558.000 |        0.179 |      0.388 |            0.016 |
| top 10%    |  4264.000 |        0.390 |      0.464 |            0.039 |
| top 5%     |  2144.000 |        0.407 |      0.468 |            0.041 |
| top 2%     |   893.000 |        0.441 |      0.465 |            0.047 |
| top 1%     |   472.000 |        0.443 |      0.496 |            0.044 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 17202.000 |       0.044 |        0.060 |      0.301 |            0.007 |           0.005 |
|       1 | 14377.000 |       0.079 |        0.112 |      0.330 |            0.015 |           0.010 |
|       2 | 12338.000 |       0.109 |        0.143 |      0.374 |            0.013 |           0.000 |
|       3 | 10685.000 |       0.140 |        0.174 |      0.405 |            0.013 |          -0.006 |
|       4 |  8924.000 |       0.173 |        0.200 |      0.431 |            0.013 |          -0.016 |
|       5 |  7564.000 |       0.208 |        0.238 |      0.438 |            0.019 |          -0.013 |
|       6 |  6312.000 |       0.246 |        0.263 |      0.461 |            0.018 |          -0.028 |
|       7 |  5283.000 |       0.287 |        0.314 |      0.456 |            0.027 |          -0.014 |
|       8 |  4609.000 |       0.338 |        0.332 |      0.479 |            0.027 |          -0.031 |
|       9 |  4264.000 |       0.453 |        0.390 |      0.464 |            0.039 |           0.003 |

Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that survived. See the SURVIVORSHIP and CHECK rows in section 9.

Setup signals split by the model's score (OOS, exit bracket_20_10; last column sma50_close):

| super_prob   |          n |   avgR |   win |   avgR_sma50 |
|:-------------|-----------:|-------:|------:|-------------:|
| low          | 100619.000 |  0.000 | 0.476 |       -0.102 |
| mid          | 100618.000 |  0.053 | 0.445 |       -0.074 |
| high         | 100618.000 |  0.149 | 0.424 |        0.188 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                                              |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:--------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| donchian_20 / all / bracket_20_10                                                     |   0.09 |    -0.44 |             -0.42 |   802.00 |   0.41 |            9.31 |               1.02 |
| pocket_pivot / all / bracket_20_10                                                    |   0.08 |    -0.35 |             -0.31 |   570.00 |   0.42 |            7.27 |               0.57 |
| donchian_55 / all / bracket_20_10                                                     |   0.03 |    -0.38 |             -0.34 |   744.00 |   0.41 |            9.05 |               2.12 |
| undercut / all / bracket_20_10                                                        |   0.20 |    -0.36 |             -0.30 |   599.00 |   0.45 |            7.75 |               0.63 |
| high52 / all / bracket_10_10                                                          |  -0.03 |    -0.53 |             -0.51 |  1007.00 |   0.51 |            7.56 |             nan    |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                     |   0.09 |    -0.42 |             -0.39 |   686.00 |   0.43 |            8.47 |               0.67 |
| All setups, ranked by RS / bracket_20_10                                              |   0.15 |    -0.40 |             -0.39 |  1058.00 |   0.39 |            9.07 |               0.52 |
| All setups, random order / bracket_20_10                                              |   0.00 |    -0.36 |             -0.33 |   516.00 |   0.44 |            8.31 |              16.06 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                          |   0.14 |    -0.30 |             -0.28 |   798.00 |   0.41 |            8.64 |               0.63 |
| BASELINE random entries, ranked by RS / bracket_20_10                                 |   0.08 |    -0.46 |             -0.44 |   662.00 |   0.41 |            7.68 |               1.02 |
| BASELINE random entries, random order / bracket_20_10                                 |   0.05 |    -0.36 |             -0.32 |   459.00 |   0.46 |            7.75 |               1.24 |
| IS-selected setups (3), ranked by RS / bracket_20_10                                  |   0.04 |    -0.40 |             -0.38 |   522.00 |   0.43 |            7.89 |               1.43 |
| IS-selected setups, only when SPY > 200d / bracket_20_10                              |  -0.02 |    -0.43 |             -0.42 |   421.00 |   0.39 |            6.76 |             nan    |
| IS-selected setups (21), ranked by RS / sma50_close                                   |   0.12 |    -0.53 |             -0.45 |   917.00 |   0.25 |            8.79 |               0.66 |
| IS-selected setups, only when SPY > 200d / sma50_close                                |   0.12 |    -0.52 |             -0.47 |   786.00 |   0.24 |            7.64 |               0.79 |
| All setups, ranked by RS / sma50_close                                                |   0.06 |    -0.54 |             -0.49 |  1189.00 |   0.26 |            8.59 |               1.29 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                           |   0.10 |    -0.33 |             -0.25 |   444.00 |   0.31 |            5.63 |               0.68 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                          |   0.13 |    -0.28 |             -0.19 |   616.00 |   0.34 |            7.70 |               0.57 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                          |   0.14 |    -0.26 |             -0.18 |   620.00 |   0.34 |            7.84 |               0.62 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)              |   0.17 |    -0.24 |             -0.16 |   607.00 |   0.35 |            7.97 |               0.59 |
| Top 20 by IS expectancy, ranked by superperformer model                               |   0.10 |    -0.26 |             -0.25 |   671.00 |   0.32 |            7.96 |               0.65 |
| All setups, ranked by superperformer model / bracket_20_10                            |   0.23 |    -0.43 |             -0.41 |  1330.00 |   0.39 |            9.14 |               0.69 |
| Only setups in the model's top 10% likely superperformers / sma50_close               |   0.28 |    -0.42 |             -0.36 |  1346.00 |   0.31 |            8.82 |               0.51 |
| CHECK random entries in the model's top 10% / sma50_close                             |   0.20 |    -0.43 |             -0.34 |   978.00 |   0.15 |            5.35 |               0.53 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close              |   0.32 |    -0.39 |             -0.31 |  1214.00 |   0.32 |            8.66 |               0.41 |
| Top 10% model + adaptive sizing / sma50_close                                         |   0.33 |    -0.31 |             -0.23 |  1375.00 |   0.32 |            9.03 |               0.45 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                  |   0.28 |    -0.33 |             -0.29 |  1308.00 |   0.32 |            8.78 |               0.43 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                     |   0.22 |    -0.41 |             -0.36 |  1145.00 |   0.41 |            9.45 |               0.58 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                             |   0.20 |    -0.34 |             -0.29 |  1138.00 |   0.42 |            9.33 |               0.63 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                               |   0.10 |    -0.39 |             -0.37 |   984.00 |   0.39 |            8.52 |               1.00 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                   |   0.18 |    -0.29 |             -0.27 |   730.00 |   0.43 |            8.02 |               0.67 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                     |   0.15 |    -0.34 |             -0.32 |  1300.00 |   0.56 |            8.31 |               0.66 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                             |   0.13 |    -0.32 |             -0.30 |  1261.00 |   0.57 |            8.06 |               0.64 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                               |   0.17 |    -0.32 |             -0.28 |  1030.00 |   0.55 |            7.03 |               0.62 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                   |   0.10 |    -0.26 |             -0.25 |   827.00 |   0.57 |            6.64 |               0.76 |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close     |   0.47 |    -0.32 |             -0.27 |   873.00 |   0.34 |            7.06 |               0.46 |
| SURVIVORSHIP S&P 500 names, only after joining the index (2705 signals) / sma50_close |   0.20 |    -0.32 |             -0.23 |   718.00 |   0.34 |            5.52 |               0.72 |
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

|      |   SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |   Top 10% model + adaptive sizing / sma50_close |   CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close |   SPY |
|-----:|------------------------------------------------------------------------------------:|------------------------------------------------:|---------------------------------------------------------------------------:|------:|
| 2018 |                                                                                 8.6 |                                             6.0 |                                                                       13.2 |  -5.2 |
| 2019 |                                                                                41.6 |                                            46.6 |                                                                       13.0 |  31.2 |
| 2020 |                                                                                40.8 |                                            63.8 |                                                                       72.4 |  18.3 |
| 2021 |                                                                                 7.4 |                                            -6.6 |                                                                       -4.8 |  28.7 |
| 2022 |                                                                                -6.3 |                                            -5.1 |                                                                       17.0 | -18.2 |
| 2023 |                                                                                64.9 |                                            83.4 |                                                                       36.1 |  26.2 |
| 2024 |                                                                               111.4 |                                            21.0 |                                                                       53.9 |  24.9 |
| 2025 |                                                                                71.8 |                                            42.0 |                                                                       53.8 |  17.7 |
| 2026 |                                                                               123.1 |                                            66.7 |                                                                       39.7 |  14.9 |

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