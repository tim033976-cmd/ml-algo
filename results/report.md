# Strategy research report

Generated 2026-10-08 09:57 UTC in 22 min.
Universe: 1488 stocks with data (sp600: 591, sp500: 499, sp400: 398; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-06: 659,965.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.49). Top 20 by IS t-stat: +0.050R OOS; top 20 by IS avgR (n>=200): +0.323R; all strategies +0.042R; random entries -0.072R.
- Too few signals to judge (need 100+ per period): htf (IS 52, OOS 99).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.34R, OOS +0.32R), ep_gap8_hold (IS +0.21R, OOS +0.21R), desc_triangle (IS +0.21R, OOS +0.21R), ep_gap10_vol5 (IS +0.20R, OOS +0.25R), ep_gap8_neglected (IS +0.23R, OOS +0.18R), ep_gap5 (IS +0.16R, OOS +0.14R), falling_wedge (IS +0.27R, OOS +0.13R), ep_gap10 (IS +0.12R, OOS +0.26R), ep_gap10_vol2 (IS +0.09R, OOS +0.27R), donchian_20 (IS +0.12R, OOS +0.09R), undercut (IS +0.14R, OOS +0.09R), sym_triangle (IS +0.08R, OOS +0.13R), flag_60 (IS +0.07R, OOS +0.20R), ema_retest (IS +0.11R, OOS +0.07R), donchian_55 (IS +0.10R, OOS +0.07R), flag_30_early (IS +0.06R, OOS +0.17R), high52_fresh (IS +0.06R, OOS +0.05R).
- Entries with no edge over random entries: high52, multi_touch, stage2.
- Best exit out-of-sample (avg over entries): sma50_close (+0.114R); worst: qull_sma10 (-0.035R).
- Filters that help OOS: rs80_early (+0.121R), rs80_early_theme (+0.059R), early_stage (+0.048R), rs80 (+0.033R); that hurt: none.
- ML filter adds little: OOS rank corr 0.254, AUC 0.557, decile monotonicity 0.26, taken +0.019R vs skipped -0.002R.
- Features the model relies on most: risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.08R, OOS +0.03R), rs80_early (IS +0.05R, OOS +0.09R), rs80_early_theme (IS +0.09R, OOS +0.04R).
- Best readable rule that held OOS: `risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio <= 1.13` (IS +0.89R, OOS +0.07R, n=4637).
- Best portfolio 2018->today: All setups, ranked by RS / oneil_20_8 at 20.6% CAGR (max drawdown -45.9%) vs SPY 14.6%.
- Best return per unit of drawdown: Top 20 strategies by IS expectancy (own exits), ranked by RS (13.8% CAGR, -26.1% max DD).

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, stage2.
3. Focus development on: ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh (tune them on IS data only, re-check OOS).
4. Make rs80_early a default filter.
5. Inspect risk_adr and risk_pct: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                 | no_edge_entries             | best_exit   | helpful_filters                                           |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                              | filters_lifting_baseline                  |   rules_held | best_portfolio                        |   best_cagr |   spy_cagr | best_calmar                                                  |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------|:------------|:----------------------------------------------------------|---------:|---------------:|---------------:|---------:|:----------------------------------------------------------|:------------------------------------------|-------------:|:--------------------------------------|------------:|-----------:|:-------------------------------------------------------------|
| 2026-10-08 08:22 | inf      |      1488 |    633749 |        0.57 |        0.05 |          -0.07 | donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50                               | multi_touch, high52, stage2 | sma50_close | rs80_early, early_stage, rs80, rs80_mkt                   |     0.55 |           0.25 |          -0.07 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank       | early_stage, rs80_early                   |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | nan                                                          |
| 2026-10-08 08:22 | inf      |      1488 |    633749 |        0.57 |        0.05 |          -0.07 | donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50                               | multi_touch, high52, stage2 | sma50_close | rs80_early, early_stage, rs80, rs80_mkt                   |     0.55 |           0.25 |          -0.07 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank       | early_stage, rs80_early                   |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | nan                                                          |
| 2026-10-08 08:48 | 48a9d03  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank       | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8    |
| 2026-10-08 09:11 | fd50739  |      1488 |    633749 |        0.55 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, ep_gap10, ep_gap10_vol2, donchian_20, undercut, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh                                             | high52, multi_touch, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80, rs80_mkt |     0.55 |           0.25 |          -0.13 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank       | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | All setups + rs80_early filter, ranked by RS / oneil_20_8    |
| 2026-10-08 09:33 | 32c75da  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS |
| 2026-10-08 09:57 | 54a58fb  |      1488 |    659965 |        0.49 |        0.05 |          -0.07 | ep_gap15, ep_gap8_hold, desc_triangle, ep_gap10_vol5, ep_gap8_neglected, ep_gap5, falling_wedge, ep_gap10, ep_gap10_vol2, donchian_20, undercut, sym_triangle, flag_60, ema_retest, donchian_55, flag_30_early, high52_fresh | high52, multi_touch, stage2 | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80           |     0.56 |           0.25 |           0.26 |     0.02 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, above_52w_low | early_stage, rs80_early, rs80_early_theme |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 | Top 20 strategies by IS expectancy (own exits), ranked by RS |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 2511.000 |
| strategies_with_enough_trades | 2036.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.489 |
| rank_corr_IS_vs_OOS_t         |    0.502 |
| OOS_avgR_all_strategies       |    0.042 |
| OOS_avgR_top20_by_IS          |    0.050 |
| OOS_avgR_top20_by_IS_avgR     |    0.323 |
| OOS_avgR_random_baseline      |   -0.072 |
| share_top20_positive_OOS      |    0.950 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry         | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:--------------|:------------|:----------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| donchian_20   | all         | oneil_20_8      |  69752 |      0.17 |  21.85 |   78114 |      8915.98 |      0.30 |       0.04 |     1.06 |    6.22 |         377.85 |
| donchian_20   | early_stage | oneil_20_8      |  36654 |      0.22 |  20.71 |   47169 |      5383.90 |      0.31 |       0.08 |     1.11 |    9.18 |         432.31 |
| donchian_20   | mkt_ok      | oneil_20_8      |  57859 |      0.17 |  19.68 |   61630 |      7034.49 |      0.29 |       0.04 |     1.05 |    5.06 |         275.58 |
| donchian_55   | early_stage | oneil_20_8      |  19751 |      0.22 |  14.98 |   23762 |      2712.21 |      0.30 |       0.06 |     1.08 |    5.00 |         168.10 |
| donchian_55   | mkt_ok      | oneil_20_8      |  40475 |      0.14 |  13.36 |   40609 |      4635.14 |      0.29 |       0.02 |     1.03 |    2.36 |         104.74 |
| donchian_20   | early_stage | sma50_close     |  36539 |      0.14 |  12.78 |   47169 |      5383.90 |      0.29 |       0.07 |     1.12 |    6.91 |         395.23 |
| undercut      | all         | oneil_20_8      |  23171 |      0.27 |  10.78 |   26314 |      3003.50 |      0.18 |       0.08 |     1.09 |    4.02 |         254.89 |
| donchian_20   | all         | sma50_close     |  69460 |      0.08 |  10.29 |   78114 |      8915.98 |      0.28 |       0.04 |     1.06 |    4.41 |         327.82 |
| donchian_20   | theme       | oneil_20_8      |  23524 |      0.13 |  10.03 |   28217 |      3220.71 |      0.29 |       0.03 |     1.04 |    2.55 |          92.54 |
| ema_retest    | all         | oneil_20_8      |  14517 |      0.23 |   9.61 |   15672 |      1788.81 |      0.22 |       0.04 |     1.05 |    2.10 |          76.56 |
| donchian_55   | early_stage | sma50_close     |  19656 |      0.15 |   9.54 |   23762 |      2712.21 |      0.30 |       0.10 |     1.15 |    5.61 |         265.50 |
| donchian_20   | early_stage | donchian_10low  |  36664 |      0.09 |   9.15 |   47169 |      5383.90 |      0.34 |       0.04 |     1.06 |    4.34 |         199.74 |
| donchian_20   | mkt_ok      | sma50_close     |  57624 |      0.08 |   8.97 |   61630 |      7034.49 |      0.28 |       0.04 |     1.06 |    4.12 |         279.83 |
| ema_retest    | early_stage | oneil_20_8      |   5834 |      0.33 |   8.83 |    6805 |       776.73 |      0.24 |       0.14 |     1.16 |    4.24 |         105.18 |
| ema_retest    | mkt_ok      | oneil_20_8      |  12240 |      0.22 |   8.41 |   12389 |      1414.09 |      0.22 |       0.06 |     1.07 |    2.66 |          87.69 |
| donchian_20   | early_stage | chandelier_3atr |  36671 |      0.08 |   8.35 |   47169 |      5383.90 |      0.35 |       0.03 |     1.06 |    4.09 |         174.22 |
| donchian_20   | early_stage | fixed_3r_20d    |  36932 |      0.06 |   8.25 |   47169 |      5383.90 |      0.43 |       0.05 |     1.08 |    7.38 |         254.52 |
| donchian_20   | early_stage | trim_ema        |  36538 |      0.06 |   7.98 |   47169 |      5383.90 |      0.33 |       0.04 |     1.07 |    5.61 |         213.21 |
| falling_wedge | all         | oneil_20_8      |   1271 |      0.48 |   7.89 |    1506 |       171.90 |      0.34 |       0.19 |     1.27 |    3.60 |          32.14 |
| donchian_20   | all         | fixed_3r_20d    |  70387 |      0.04 |   7.63 |   78114 |      8915.98 |      0.41 |       0.01 |     1.02 |    2.89 |         128.47 |
| donchian_20   | rs80        | oneil_20_8      |  19657 |      0.10 |   7.09 |   22615 |      2581.29 |      0.29 |       0.04 |     1.05 |    3.25 |         105.95 |
| donchian_55   | all         | sma50_close     |  47449 |      0.07 |   7.00 |   50722 |      5789.44 |      0.29 |       0.03 |     1.05 |    2.95 |         197.13 |
| donchian_20   | rs80_mkt    | oneil_20_8      |  15291 |      0.11 |   6.78 |   16974 |      1937.42 |      0.29 |       0.05 |     1.06 |    3.30 |          94.57 |
| undercut      | all         | chandelier_3atr |  23194 |      0.15 |   6.57 |   26314 |      3003.50 |      0.23 |       0.09 |     1.10 |    4.01 |         264.22 |
| undercut      | theme       | oneil_20_8      |   7239 |      0.28 |   6.56 |    8786 |      1002.84 |      0.19 |       0.08 |     1.08 |    2.36 |          81.95 |
| undercut      | all         | donchian_10low  |  23195 |      0.15 |   6.39 |   26314 |      3003.50 |      0.22 |       0.08 |     1.09 |    3.65 |         243.54 |
| donchian_55   | early_stage | trim_ema        |  19656 |      0.07 |   6.36 |   23762 |      2712.21 |      0.35 |       0.05 |     1.08 |    4.33 |         129.45 |
| donchian_55   | rs80_early  | oneil_20_8      |   4659 |      0.18 |   6.22 |    6407 |       731.30 |      0.32 |       0.14 |     1.19 |    5.87 |         101.94 |
| donchian_55   | rs80        | oneil_20_8      |  17090 |      0.09 |   5.88 |   19277 |      2200.29 |      0.29 |       0.05 |     1.07 |    3.93 |         119.56 |
| ema_retest    | early_stage | sma50_close     |   5805 |      0.24 |   5.85 |    6805 |       776.73 |      0.26 |       0.16 |     1.19 |    4.01 |         120.44 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry         | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:--------------|:------------|:----------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| donchian_20   | all         | oneil_20_8      |  69752 |      0.17 |  21.85 |   78114 |      0.30 |       0.04 |     1.06 |    6.22 |
| donchian_20   | early_stage | oneil_20_8      |  36654 |      0.22 |  20.71 |   47169 |      0.31 |       0.08 |     1.11 |    9.18 |
| donchian_20   | mkt_ok      | oneil_20_8      |  57859 |      0.17 |  19.68 |   61630 |      0.29 |       0.04 |     1.05 |    5.06 |
| donchian_55   | all         | oneil_20_8      |  47704 |      0.15 |  15.81 |   50722 |      0.29 |       0.02 |     1.02 |    1.94 |
| donchian_55   | early_stage | oneil_20_8      |  19751 |      0.22 |  14.98 |   23762 |      0.30 |       0.06 |     1.08 |    5.00 |
| donchian_55   | mkt_ok      | oneil_20_8      |  40475 |      0.14 |  13.36 |   40609 |      0.29 |       0.02 |     1.03 |    2.36 |
| donchian_20   | early_stage | sma50_close     |  36539 |      0.14 |  12.78 |   47169 |      0.29 |       0.07 |     1.12 |    6.91 |
| undercut      | all         | oneil_20_8      |  23171 |      0.27 |  10.78 |   26314 |      0.18 |       0.08 |     1.09 |    4.02 |
| donchian_20   | all         | sma50_close     |  69460 |      0.08 |  10.29 |   78114 |      0.28 |       0.04 |     1.06 |    4.41 |
| donchian_20   | theme       | oneil_20_8      |  23524 |      0.13 |  10.03 |   28217 |      0.29 |       0.03 |     1.04 |    2.55 |
| ema_retest    | all         | oneil_20_8      |  14517 |      0.23 |   9.61 |   15672 |      0.22 |       0.04 |     1.05 |    2.10 |
| donchian_55   | early_stage | sma50_close     |  19656 |      0.15 |   9.54 |   23762 |      0.30 |       0.10 |     1.15 |    5.61 |
| donchian_20   | early_stage | donchian_10low  |  36664 |      0.09 |   9.15 |   47169 |      0.34 |       0.04 |     1.06 |    4.34 |
| donchian_20   | mkt_ok      | sma50_close     |  57624 |      0.08 |   8.97 |   61630 |      0.28 |       0.04 |     1.06 |    4.12 |
| ema_retest    | early_stage | oneil_20_8      |   5834 |      0.33 |   8.83 |    6805 |      0.24 |       0.14 |     1.16 |    4.24 |
| ema_retest    | mkt_ok      | oneil_20_8      |  12240 |      0.22 |   8.41 |   12389 |      0.22 |       0.06 |     1.07 |    2.66 |
| donchian_20   | early_stage | chandelier_3atr |  36671 |      0.08 |   8.35 |   47169 |      0.35 |       0.03 |     1.06 |    4.09 |
| donchian_20   | early_stage | fixed_3r_20d    |  36932 |      0.06 |   8.25 |   47169 |      0.43 |       0.05 |     1.08 |    7.38 |
| donchian_20   | early_stage | trim_ema        |  36538 |      0.06 |   7.98 |   47169 |      0.33 |       0.04 |     1.07 |    5.61 |
| tight_coil_7  | all         | oneil_20_8      |   6335 |      0.19 |   7.98 |    5359 |      0.30 |      -0.01 |     0.98 |   -0.54 |
| donchian_55   | theme       | oneil_20_8      |  18474 |      0.12 |   7.89 |   21367 |      0.28 |       0.00 |     1.00 |    0.06 |
| falling_wedge | all         | oneil_20_8      |   1271 |      0.48 |   7.89 |    1506 |      0.34 |       0.19 |     1.27 |    3.60 |
| donchian_20   | all         | fixed_3r_20d    |  70387 |      0.04 |   7.63 |   78114 |      0.41 |       0.01 |     1.02 |    2.89 |
| undercut      | early_stage | oneil_20_8      |   6980 |      0.34 |   7.21 |    8334 |      0.17 |       0.07 |     1.07 |    1.77 |
| donchian_20   | rs80        | oneil_20_8      |  19657 |      0.10 |   7.09 |   22615 |      0.29 |       0.04 |     1.05 |    3.25 |
| donchian_55   | all         | sma50_close     |  47449 |      0.07 |   7.00 |   50722 |      0.29 |       0.03 |     1.05 |    2.95 |
| donchian_20   | all         | chandelier_3atr |  69863 |      0.05 |   6.96 |   78114 |      0.33 |       0.00 |     1.00 |    0.31 |
| donchian_20   | rs80_mkt    | oneil_20_8      |  15291 |      0.11 |   6.78 |   16974 |      0.29 |       0.05 |     1.06 |    3.30 |
| undercut      | all         | chandelier_3atr |  23194 |      0.15 |   6.57 |   26314 |      0.23 |       0.09 |     1.10 |    4.01 |
| pocket_pivot  | all         | oneil_20_8      |  49369 |      0.12 |   6.57 |   48059 |      0.13 |      -0.07 |     0.94 |   -4.24 |

## 4. Each entry with its best in-sample exit/filter

| entry             | filter           | exit            |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------------|:-----------------|:----------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| base_50           | early_stage      | oneil_20_8      |    593 |       49.44 |     0.29 |      0.15 |   1.56 |     888 |       101.36 |      0.30 |       0.29 |     1.38 |    3.58 |          29.57 |
| ep_gap10          | rs80_mkt         | trim_ema        |    193 |       16.09 |     0.41 |      0.45 |   2.39 |     337 |        38.47 |      0.35 |       0.25 |     1.39 |    1.82 |           9.47 |
| desc_triangle     | all              | oneil_20_8      |    785 |       65.45 |     0.36 |      0.27 |   3.61 |     706 |        80.58 |      0.32 |       0.24 |     1.34 |    2.81 |          19.56 |
| ep_gap10_vol2     | rs80_mkt         | chandelier_3atr |    211 |       17.59 |     0.34 |      0.52 |   2.13 |     394 |        44.97 |      0.33 |       0.24 |     1.39 |    1.84 |          10.59 |
| ep_gap15          | mkt_ok           | trim_ema        |     96 |        8.00 |     0.41 |      0.62 |   2.46 |     235 |        26.82 |      0.38 |       0.22 |     1.36 |    1.48 |           5.95 |
| base_25           | rs80_early_theme | chandelier_3atr |    154 |       12.84 |     0.31 |      0.44 |   1.52 |     214 |        24.43 |      0.34 |       0.21 |     1.32 |    1.28 |           5.11 |
| falling_wedge     | all              | oneil_20_8      |   1271 |      105.97 |     0.42 |      0.48 |   7.89 |    1506 |       171.90 |      0.34 |       0.19 |     1.27 |    3.60 |          32.14 |
| ep_gap8_hold      | rs80_mkt         | trim_ema        |    286 |       23.84 |     0.43 |      0.38 |   2.77 |     418 |        47.71 |      0.35 |       0.14 |     1.23 |    1.32 |           6.84 |
| ep_gap8_neglected | all              | oneil_20_8      |    612 |       51.02 |     0.33 |      0.27 |   2.83 |     934 |       106.61 |      0.30 |       0.14 |     1.19 |    2.06 |          14.78 |
| sym_triangle      | all              | oneil_20_8      |    894 |       74.53 |     0.28 |      0.06 |   0.78 |     915 |       104.44 |      0.26 |       0.12 |     1.14 |    1.33 |          12.09 |
| undercut          | all              | oneil_20_8      |  23171 |     1931.80 |     0.20 |      0.27 |  10.78 |   26314 |      3003.50 |      0.18 |       0.08 |     1.09 |    4.02 |         254.89 |
| ep_gap10_vol5     | rs80_mkt         | fixed_3r_20d    |    136 |       11.34 |     0.51 |      0.30 |   2.47 |     191 |        21.80 |      0.39 |       0.06 |     1.11 |    0.63 |           1.41 |
| ep_gap5           | rs80_mkt         | oneil_20_8      |    606 |       50.52 |     0.33 |      0.33 |   3.27 |     736 |        84.01 |      0.29 |       0.06 |     1.08 |    0.81 |           4.80 |
| ema_retest        | all              | oneil_20_8      |  14517 |     1210.30 |     0.25 |      0.23 |   9.61 |   15672 |      1788.81 |      0.22 |       0.04 |     1.05 |    2.10 |          76.56 |
| donchian_20       | all              | oneil_20_8      |  69752 |     5815.32 |     0.32 |      0.17 |  21.85 |   78114 |      8915.98 |      0.30 |       0.04 |     1.06 |    6.22 |         377.85 |
| random_uptrend    | early_stage      | oneil_20_8      |  11111 |      926.34 |     0.13 |      0.18 |   4.36 |   13156 |      1501.63 |      0.12 |       0.02 |     1.02 |    0.57 |          30.07 |
| donchian_55       | all              | oneil_20_8      |  47704 |     3977.15 |     0.31 |      0.15 |  15.81 |   50722 |      5789.44 |      0.29 |       0.02 |     1.02 |    1.94 |          95.24 |
| high52_fresh      | all              | oneil_20_8      |   8213 |      684.73 |     0.21 |      0.14 |   4.06 |    8415 |       960.49 |      0.19 |       0.01 |     1.01 |    0.19 |           5.76 |
| vcp               | all              | oneil_20_8      |   1301 |      108.47 |     0.42 |      0.17 |   3.91 |     879 |       100.33 |      0.36 |       0.00 |     1.01 |    0.07 |           0.36 |
| tight_coil_7      | all              | oneil_20_8      |   6335 |      528.16 |     0.36 |      0.19 |   7.98 |    5359 |       611.68 |      0.30 |      -0.01 |     0.98 |   -0.54 |          -8.23 |
| rising_wedge      | early_stage      | oneil_20_8      |    803 |       66.95 |     0.32 |      0.14 |   1.92 |     778 |        88.80 |      0.30 |      -0.03 |     0.96 |   -0.44 |          -2.68 |
| asc_triangle      | theme            | oneil_20_8      |    326 |       27.18 |     0.34 |      0.32 |   2.30 |     284 |        32.42 |      0.32 |      -0.04 |     0.95 |   -0.31 |          -1.20 |
| flag_30_early     | rs80             | chandelier_3atr |    718 |       59.86 |     0.23 |      0.11 |   0.89 |    1005 |       114.71 |      0.23 |      -0.05 |     0.95 |   -0.51 |          -5.21 |
| tight_coil_15     | all              | oneil_20_8      |   1270 |      105.88 |     0.41 |      0.23 |   4.71 |    1039 |       118.59 |      0.32 |      -0.06 |     0.92 |   -1.12 |          -6.58 |
| pocket_pivot      | all              | oneil_20_8      |  49369 |     4115.96 |     0.15 |      0.12 |   6.57 |   48059 |      5485.48 |      0.13 |      -0.07 |     0.94 |   -4.24 |        -388.55 |
| multi_touch       | all              | oneil_20_8      |  12640 |     1053.81 |     0.22 |      0.17 |   5.85 |   10634 |      1213.77 |      0.19 |      -0.08 |     0.91 |   -2.93 |         -98.70 |
| high52            | all              | oneil_20_8      |  30340 |     2529.49 |     0.17 |      0.04 |   2.30 |   29119 |      3323.66 |      0.16 |      -0.09 |     0.91 |   -4.83 |        -290.99 |
| flag_30           | rs80_theme       | oneil_20_8      |    470 |       39.18 |     0.23 |      0.10 |   0.89 |     688 |        78.53 |      0.21 |      -0.09 |     0.90 |   -1.01 |          -6.88 |
| stage2            | all              | oneil_20_8      |   5997 |      499.98 |     0.26 |      0.23 |   5.80 |    4847 |       553.24 |      0.21 |      -0.12 |     0.87 |   -3.23 |         -66.97 |
| flag_60           | rs80_theme       | oneil_20_8      |    160 |       13.34 |     0.26 |      0.21 |   1.12 |     293 |        33.44 |      0.23 |      -0.13 |     0.86 |   -0.99 |          -4.31 |
| htf               | all              | sma50_close     |     52 |        4.34 |     0.17 |      0.41 |   0.66 |      99 |        11.30 |      0.11 |      -0.34 |     0.65 |   -1.17 |          -3.85 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |              0.06 |             0.05 |          0.02 |           0.09 |         0.04 |         0.04 |         0.01 |         -0.00 |       0.10 |
| base_25           |              0.12 |             0.09 |          0.10 |           0.08 |         0.10 |         0.04 |         0.07 |          0.23 |       0.13 |
| base_50           |              0.16 |             0.11 |          0.14 |           0.11 |         0.12 |         0.08 |         0.10 |          0.22 |       0.15 |
| desc_triangle     |              0.27 |             0.24 |          0.22 |           0.22 |         0.29 |         0.15 |         0.20 |          0.07 |       0.19 |
| donchian_20       |              0.10 |             0.08 |          0.09 |           0.11 |         0.09 |         0.08 |         0.08 |          0.07 |       0.11 |
| donchian_55       |              0.07 |             0.06 |          0.07 |           0.08 |         0.06 |         0.06 |         0.06 |          0.06 |       0.10 |
| ema_retest        |              0.07 |             0.05 |          0.07 |           0.09 |         0.09 |         0.07 |         0.05 |          0.07 |       0.10 |
| ep_gap10          |              0.25 |             0.35 |          0.27 |           0.20 |         0.15 |         0.11 |         0.17 |          0.52 |       0.32 |
| ep_gap10_vol2     |              0.31 |             0.36 |          0.26 |           0.18 |         0.21 |         0.13 |         0.18 |          0.51 |       0.31 |
| ep_gap10_vol5     |              0.26 |             0.33 |          0.22 |           0.20 |         0.12 |         0.09 |         0.12 |          0.53 |       0.34 |
| ep_gap15          |              0.30 |             0.34 |          0.27 |           0.25 |         0.27 |         0.12 |         0.15 |          0.74 |       0.39 |
| ep_gap5           |              0.15 |             0.17 |          0.15 |           0.12 |         0.10 |         0.09 |         0.10 |          0.21 |       0.16 |
| ep_gap8_hold      |              0.19 |             0.26 |          0.21 |           0.17 |         0.15 |         0.10 |         0.13 |          0.40 |       0.26 |
| ep_gap8_neglected |              0.14 |             0.18 |          0.22 |           0.18 |         0.18 |         0.10 |         0.13 |          0.29 |       0.24 |
| falling_wedge     |              0.21 |             0.17 |          0.09 |           0.19 |         0.23 |         0.07 |         0.08 |          0.03 |       0.08 |
| flag_30           |              0.07 |             0.13 |          0.14 |           0.06 |         0.03 |         0.08 |         0.08 |          0.28 |       0.15 |
| flag_30_early     |              0.18 |             0.16 |          0.17 |           0.15 |         0.22 |         0.13 |         0.13 |          0.25 |       0.19 |
| flag_60           |              0.19 |             0.16 |          0.18 |           0.10 |         0.11 |         0.13 |         0.11 |          0.53 |       0.32 |
| high52            |             -0.04 |            -0.05 |         -0.03 |          -0.03 |        -0.04 |        -0.03 |        -0.05 |         -0.05 |      -0.02 |
| high52_fresh      |              0.06 |             0.04 |          0.07 |           0.05 |         0.05 |         0.04 |         0.03 |          0.07 |       0.07 |
| htf               |             -0.19 |            -0.30 |         -0.14 |          -0.15 |        -0.17 |        -0.01 |        -0.10 |         -0.31 |      -0.07 |
| multi_touch       |             -0.03 |            -0.00 |         -0.02 |          -0.00 |        -0.04 |         0.01 |        -0.01 |         -0.06 |      -0.01 |
| pocket_pivot      |             -0.02 |            -0.02 |         -0.01 |           0.00 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.01 |
| rising_wedge      |             -0.02 |            -0.05 |         -0.02 |           0.04 |         0.03 |         0.07 |         0.03 |         -0.06 |       0.01 |
| stage2            |             -0.07 |            -0.07 |         -0.06 |          -0.02 |        -0.08 |        -0.02 |        -0.05 |         -0.10 |      -0.05 |
| sym_triangle      |              0.19 |             0.12 |          0.12 |           0.17 |         0.16 |         0.14 |         0.14 |          0.04 |       0.11 |
| tight_coil_15     |             -0.00 |            -0.03 |         -0.00 |           0.05 |        -0.01 |         0.06 |         0.03 |         -0.10 |       0.03 |
| tight_coil_7      |              0.02 |             0.01 |          0.03 |           0.07 |         0.03 |         0.06 |         0.04 |         -0.01 |       0.07 |
| undercut          |              0.18 |             0.16 |          0.02 |           0.08 |         0.13 |         0.09 |         0.08 |         -0.00 |       0.03 |
| vcp               |              0.06 |             0.04 |          0.04 |           0.10 |         0.05 |         0.07 |         0.06 |         -0.05 |       0.04 |

Same, in-sample:

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| asc_triangle      |              0.06 |             0.02 |          0.06 |           0.08 |         0.07 |         0.06 |         0.04 |         -0.01 |       0.10 |
| base_25           |             -0.03 |            -0.04 |         -0.00 |           0.07 |        -0.08 |         0.06 |         0.03 |          0.03 |       0.09 |
| base_50           |              0.00 |            -0.00 |          0.04 |           0.13 |        -0.04 |         0.08 |         0.05 |         -0.03 |       0.09 |
| desc_triangle     |              0.17 |             0.29 |          0.17 |           0.21 |         0.20 |         0.17 |         0.17 |          0.21 |       0.27 |
| donchian_20       |              0.11 |             0.11 |          0.14 |           0.15 |         0.09 |         0.10 |         0.11 |          0.12 |       0.17 |
| donchian_55       |              0.08 |             0.09 |          0.12 |           0.13 |         0.07 |         0.08 |         0.09 |          0.11 |       0.17 |
| ema_retest        |              0.09 |             0.09 |          0.12 |           0.12 |         0.15 |         0.06 |         0.07 |          0.15 |       0.13 |
| ep_gap10          |              0.16 |             0.10 |          0.15 |           0.10 |        -0.05 |         0.13 |         0.10 |          0.18 |       0.22 |
| ep_gap10_vol2     |              0.13 |             0.06 |          0.12 |           0.10 |        -0.05 |         0.10 |         0.07 |          0.13 |       0.18 |
| ep_gap10_vol5     |              0.23 |             0.18 |          0.18 |           0.20 |         0.03 |         0.22 |         0.17 |          0.29 |       0.33 |
| ep_gap15          |              0.43 |             0.32 |          0.33 |           0.30 |         0.11 |         0.32 |         0.30 |          0.45 |       0.48 |
| ep_gap5           |              0.17 |             0.12 |          0.17 |           0.15 |         0.08 |         0.14 |         0.13 |          0.25 |       0.23 |
| ep_gap8_hold      |              0.24 |             0.20 |          0.24 |           0.17 |         0.12 |         0.16 |         0.16 |          0.29 |       0.32 |
| ep_gap8_neglected |              0.27 |             0.22 |          0.25 |           0.19 |         0.19 |         0.16 |         0.19 |          0.32 |       0.29 |
| falling_wedge     |              0.35 |             0.36 |          0.23 |           0.30 |         0.40 |         0.21 |         0.23 |          0.13 |       0.20 |
| flag_30           |             -0.08 |            -0.10 |         -0.05 |           0.05 |        -0.11 |         0.02 |        -0.03 |         -0.09 |       0.01 |
| flag_30_early     |              0.11 |             0.08 |          0.12 |           0.05 |        -0.04 |         0.06 |         0.09 |          0.01 |       0.03 |
| flag_60           |              0.04 |             0.02 |          0.09 |           0.12 |        -0.02 |         0.15 |         0.09 |          0.07 |       0.12 |
| high52            |             -0.03 |            -0.04 |          0.01 |           0.02 |        -0.03 |        -0.02 |        -0.02 |         -0.03 |       0.00 |
| high52_fresh      |              0.06 |             0.05 |          0.09 |           0.08 |         0.07 |         0.04 |         0.05 |          0.07 |       0.08 |
| htf               |             -0.07 |             0.26 |          0.15 |           0.08 |        -0.09 |         0.14 |         0.20 |          0.45 |       0.29 |
| multi_touch       |              0.07 |             0.08 |          0.12 |           0.10 |         0.09 |         0.06 |         0.06 |          0.12 |       0.10 |
| pocket_pivot      |              0.05 |             0.06 |          0.07 |           0.03 |         0.04 |         0.03 |         0.03 |          0.07 |       0.04 |
| rising_wedge      |              0.00 |             0.02 |          0.07 |           0.08 |         0.01 |         0.04 |         0.03 |          0.03 |       0.10 |
| stage2            |              0.11 |             0.13 |          0.16 |           0.11 |         0.16 |         0.07 |         0.09 |          0.15 |       0.14 |
| sym_triangle      |              0.07 |             0.08 |          0.12 |           0.08 |        -0.02 |         0.11 |         0.09 |          0.06 |       0.11 |
| tight_coil_15     |              0.15 |             0.18 |          0.14 |           0.16 |         0.15 |         0.13 |         0.12 |          0.13 |       0.23 |
| tight_coil_7      |              0.13 |             0.16 |          0.15 |           0.15 |         0.12 |         0.10 |         0.10 |          0.17 |       0.22 |
| undercut          |              0.21 |             0.22 |          0.06 |           0.12 |         0.19 |         0.18 |         0.17 |          0.01 |       0.08 |
| vcp               |              0.07 |             0.08 |          0.12 |           0.13 |         0.10 |         0.10 |         0.09 |          0.09 |       0.17 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| sma50_close     |      0.09 |       0.11 |      0.26 |     1.17 |                       0.63 |
| oneil_20_8      |      0.14 |       0.04 |      0.26 |     1.06 |                       0.80 |
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
| rs80_early       |      0.08 |       0.14 |      0.36 |
| rs80_early_theme |      0.10 |       0.08 |      0.34 |
| early_stage      |      0.06 |       0.06 |      0.34 |
| rs80             |      0.04 |       0.05 |      0.34 |
| rs80_mkt         |      0.06 |       0.04 |      0.33 |
| rs80_theme       |      0.03 |       0.03 |      0.34 |
| all              |      0.03 |       0.02 |      0.33 |
| theme            |      0.02 |       0.01 |      0.33 |
| mkt_ok           |      0.04 |       0.01 |      0.33 |

## 8. ML meta-labeling (exit: oneil_20_8, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.254; AUC for R > 0: 0.557 (0.5 = no skill). Taken (model's top third, causal threshold): n=95,212, avgR=0.019, win=0.263. Skipped: n=206,643, avgR=-0.002, win=0.218.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 30186.00 |  -0.15 |  0.13 |
|      1 | 30185.00 |  -0.02 |  0.19 |
|      2 | 30186.00 |   0.04 |  0.22 |
|      3 | 30186.00 |   0.03 |  0.24 |
|      4 | 30185.00 |   0.03 |  0.25 |
|      5 | 30185.00 |   0.03 |  0.25 |
|      6 | 30185.00 |   0.05 |  0.26 |
|      7 | 30191.00 |   0.01 |  0.26 |
|      8 | 30180.00 |   0.05 |  0.27 |
|      9 | 30186.00 |  -0.03 |  0.26 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| falling_wedge     |  1506.00 |       0.19 |    978.00 |         0.25 |           0.06 |
| ep_gap10_vol2     |  1182.00 |       0.16 |    564.00 |         0.20 |           0.12 |
| ep_gap15          |   374.00 |       0.23 |    202.00 |         0.20 |           0.26 |
| desc_triangle     |   706.00 |       0.24 |    382.00 |         0.20 |           0.30 |
| ep_gap10          |   933.00 |       0.11 |    456.00 |         0.14 |           0.08 |
| ep_gap8_neglected |   934.00 |       0.14 |    449.00 |         0.13 |           0.15 |
| undercut          | 26314.00 |       0.08 |   8392.00 |         0.12 |           0.07 |
| ep_gap8_hold      |  1182.00 |       0.10 |    555.00 |         0.12 |           0.09 |
| flag_30_early     |  1955.00 |       0.17 |    532.00 |         0.09 |           0.20 |
| ep_gap5           |  2322.00 |       0.05 |   1086.00 |         0.08 |           0.03 |
| vcp               |   879.00 |       0.00 |    351.00 |         0.07 |          -0.04 |
| base_25           |  2444.00 |       0.05 |    874.00 |         0.05 |           0.06 |
| base_50           |  2665.00 |       0.07 |    944.00 |         0.05 |           0.08 |
| ep_gap10_vol5     |   454.00 |       0.08 |    243.00 |         0.05 |           0.11 |
| sym_triangle      |   915.00 |       0.12 |    385.00 |         0.03 |           0.18 |
| donchian_20       | 78114.00 |       0.04 |  31537.00 |         0.02 |           0.06 |
| flag_60           |   615.00 |       0.07 |    166.00 |         0.02 |           0.09 |
| flag_30           |  1786.00 |      -0.01 |    472.00 |         0.02 |          -0.02 |
| ema_retest        | 15672.00 |       0.04 |   5401.00 |         0.01 |           0.06 |
| donchian_55       | 50722.00 |       0.02 |  17536.00 |         0.00 |           0.02 |
| pocket_pivot      | 48059.00 |      -0.07 |   8192.00 |        -0.01 |          -0.08 |
| rising_wedge      |  1747.00 |      -0.01 |    641.00 |        -0.02 |          -0.01 |
| high52_fresh      |  8415.00 |       0.01 |   2138.00 |        -0.04 |           0.02 |
| tight_coil_7      |  5359.00 |      -0.01 |   2157.00 |        -0.04 |           0.01 |
| stage2            |  4847.00 |      -0.12 |   1584.00 |        -0.05 |          -0.16 |
| high52            | 29119.00 |      -0.09 |   5040.00 |        -0.05 |          -0.09 |
| tight_coil_15     |  1039.00 |      -0.06 |    456.00 |        -0.07 |          -0.04 |
| multi_touch       | 10634.00 |      -0.08 |   3067.00 |        -0.08 |          -0.08 |
| asc_triangle      |   863.00 |      -0.00 |    407.00 |        -0.10 |           0.08 |
| htf               |    99.00 |      -0.22 |     25.00 |        -0.34 |          -0.18 |

- Same model on episodic pivots only / sma50_close: rank corr 0.003, taken avgR 0.354 (n=3,279) vs skipped 0.353 (n=4,102).
- Same model on your trim plan (trim_ema): rank corr 0.117, taken avgR 0.001 (n=93,241) vs skipped -0.053 (n=208,614).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature           |   rank_corr_drop |
|:------------------|-----------------:|
| risk_adr          |           0.1273 |
| risk_pct          |           0.0833 |
| mkt_ret_21        |           0.0577 |
| qqq_ret_21        |           0.0360 |
| above_52w_low     |           0.0240 |
| leg3_range        |           0.0239 |
| rs_rank           |           0.0163 |
| dist_52w_high     |           0.0111 |
| gap               |           0.0104 |
| breadth_50        |           0.0099 |
| leg1_range        |           0.0060 |
| ext_ema8_adr      |           0.0054 |
| industry_rank     |           0.0050 |
| range_pos_12m     |           0.0049 |
| mkt_ema_stack     |           0.0046 |
| sma200_slope      |           0.0043 |
| qqq_ok            |           0.0037 |
| down_candle_exp_5 |           0.0023 |
| vol_dryup         |           0.0019 |
| updown_vol_50     |           0.0017 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                              |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio <= 1.13   |   2891 |      0.89 |    4637 |       0.07 |      0.10 |
| risk_adr > 0.633 AND rates_rising > 0.5 AND mkt_ema_stack <= 0.5  |  22790 |      0.60 |   36394 |       0.13 |      0.30 |
| risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio > 1.13    |   3975 |      0.26 |    5242 |       0.10 |      0.11 |
| risk_adr > 0.633 AND rates_rising > 0.5 AND mkt_ema_stack > 0.5   | 108499 |      0.24 |   79311 |      -0.07 |      0.23 |
| risk_adr > 0.633 AND rates_rising <= 0.5 AND qqq_ret_21 <= 0.0299 |  60064 |      0.16 |   73173 |       0.06 |      0.26 |
| risk_adr <= 0.633 AND breadth_50 > 0.523 AND leg3_range > 0.117   |   9762 |      0.06 |   14344 |      -0.04 |      0.11 |
| risk_adr <= 0.633 AND breadth_50 > 0.523 AND leg3_range <= 0.117  |  19829 |     -0.06 |   15936 |      -0.15 |      0.08 |
| risk_adr > 0.633 AND rates_rising <= 0.5 AND qqq_ret_21 > 0.0299  |  60794 |     -0.13 |   72818 |       0.00 |      0.25 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                       |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:---------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| donchian_20 / all / oneil_20_8                                 |   0.08 |    -0.34 |             -0.31 |  1044.00 |   0.32 |            8.82 |               0.84 |
| donchian_55 / all / oneil_20_8                                 |  -0.03 |    -0.53 |             -0.52 |  1075.00 |   0.28 |            8.75 |             nan    |
| undercut / all / oneil_20_8                                    |   0.10 |    -0.45 |             -0.44 |  1404.00 |   0.19 |            7.27 |               0.86 |
| ema_retest / all / oneil_20_8                                  |   0.01 |    -0.49 |             -0.47 |   880.00 |   0.25 |            7.07 |               9.88 |
| tight_coil_7 / all / oneil_20_8                                |   0.01 |    -0.39 |             -0.37 |   672.00 |   0.31 |            8.10 |               7.25 |
| All setups, ML-filtered (top third), ranked by ML / oneil_20_8 |   0.12 |    -0.26 |             -0.21 |   969.00 |   0.29 |            7.86 |               0.57 |
| All setups, ranked by RS / oneil_20_8                          |   0.21 |    -0.46 |             -0.43 |  1661.00 |   0.27 |            8.69 |               0.56 |
| All setups, random order / oneil_20_8                          |  -0.02 |    -0.42 |             -0.39 |   999.00 |   0.22 |            7.58 |             nan    |
| All setups + rs80_early filter, ranked by RS / oneil_20_8      |   0.10 |    -0.27 |             -0.28 |  1335.00 |   0.26 |            8.48 |               0.80 |
| BASELINE random entries, ranked by RS / oneil_20_8             |   0.04 |    -0.52 |             -0.49 |  1714.00 |   0.15 |            6.33 |               2.26 |
| BASELINE random entries, random order / oneil_20_8             |  -0.01 |    -0.49 |             -0.47 |  1383.00 |   0.12 |            6.08 |             nan    |
| IS-selected setups (17), ranked by RS / oneil_20_8             |   0.17 |    -0.52 |             -0.49 |  1464.00 |   0.29 |            8.94 |               0.64 |
| IS-selected setups, only when SPY > 200d / oneil_20_8          |   0.15 |    -0.42 |             -0.39 |  1213.00 |   0.30 |            7.77 |               0.75 |
| IS-selected setups (21), ranked by RS / sma50_close            |   0.12 |    -0.53 |             -0.45 |   917.00 |   0.25 |            8.79 |               0.66 |
| IS-selected setups, only when SPY > 200d / sma50_close         |   0.12 |    -0.52 |             -0.47 |   786.00 |   0.24 |            7.64 |               0.79 |
| All setups, ranked by RS / sma50_close                         |   0.06 |    -0.54 |             -0.49 |  1189.00 |   0.26 |            8.59 |               1.29 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS    |   0.10 |    -0.33 |             -0.25 |   444.00 |   0.31 |            5.63 |               0.68 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS   |   0.13 |    -0.28 |             -0.19 |   616.00 |   0.34 |            7.70 |               0.57 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS   |   0.14 |    -0.26 |             -0.18 |   620.00 |   0.34 |            7.84 |               0.62 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY   |   0.15 |    -0.34 |             -0.27 |   610.00 |   0.34 |            7.63 |               0.52 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY   |   0.13 |    -0.39 |             -0.32 |   479.00 |   0.34 |            5.98 |               0.64 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY   |   0.13 |    -0.39 |             -0.32 |   479.00 |   0.34 |            5.98 |               0.64 |
| SPY buy & hold                                                 |   0.15 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

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

|      |   All setups, ranked by RS / oneil_20_8 |   IS-selected setups (17), ranked by RS / oneil_20_8 |   Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY |   SPY |
|-----:|----------------------------------------:|-----------------------------------------------------:|---------------------------------------------------------------:|------:|
| 2018 |                                   -11.6 |                                                -13.3 |                                                           -3.4 |  -5.2 |
| 2019 |                                    14.4 |                                                 22.1 |                                                           37.7 |  31.2 |
| 2020 |                                    14.3 |                                                  0.7 |                                                           27.6 |  18.3 |
| 2021 |                                    15.0 |                                                 24.1 |                                                           25.4 |  28.7 |
| 2022 |                                     1.0 |                                                 -3.8 |                                                           -8.4 | -18.2 |
| 2023 |                                    53.4 |                                                 32.3 |                                                           23.6 |  26.2 |
| 2024 |                                    63.5 |                                                 84.8 |                                                           16.4 |  24.9 |
| 2025 |                                    31.6 |                                                  4.3 |                                                          -11.9 |  17.7 |
| 2026 |                                    16.4 |                                                 23.4 |                                                           36.5 |  14.9 |

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

Caveats: index membership lists are current (plus former S&P 500 members Yahoo still serves), so survivorship bias remains; daily bars cannot reproduce intraday entries; one decision per signal, no slippage model beyond costs.