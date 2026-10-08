# Strategy research report

Generated 2026-10-08 08:22 UTC in 17 min.
Universe: 1488 stocks with data (sp600: 591, sp500: 499, sp400: 398; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-06: 633,749.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- Selection is mostly noise: IS-vs-OOS rank correlation 0.57; the 20 best in-sample strategies averaged +0.054R out-of-sample vs +0.072R for all strategies and -0.068R for random entries.
- Too few signals to judge (need 100+ per period): htf (IS 52, OOS 99).
- Entries that beat random entries in both periods for most exits: donchian_55 (+0.07R OOS), donchian_20 (+0.09R OOS), ema_retest (+0.07R OOS), ep_gap5 (+0.14R OOS), ep_gap15 (+0.32R OOS), ep_gap10_vol5 (+0.25R OOS), ep_gap8_neglected (+0.18R OOS), high52_fresh (+0.05R OOS), ep_gap8_hold (+0.21R OOS), ep_gap10 (+0.26R OOS), undercut (+0.09R OOS), flag_60 (+0.20R OOS), flag_30_early (+0.17R OOS), ep_gap10_vol2 (+0.27R OOS), vcp (+0.05R OOS), base_50 (+0.13R OOS).
- Entries with no edge over random entries: multi_touch, high52, stage2.
- Best exit out-of-sample (avg over entries): sma50_close (+0.159R); worst: qull_sma10 (-0.038R).
- Filters that help OOS: rs80_early (+0.136R), early_stage (+0.070R), rs80 (+0.065R), rs80_mkt (+0.040R); that hurt: none.
- ML filter adds little: OOS rank corr 0.254, AUC 0.554, decile monotonicity -0.07, taken +0.011R vs skipped +0.001R.
- Features the model relies on most: risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): early_stage (IS +0.08R, OOS +0.03R), rs80_early (IS +0.05R, OOS +0.09R).
- Best readable rule that held OOS: `risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio <= 1.11` (IS +0.92R, OOS +0.05R, n=4480).
- Best portfolio 2018->today: All setups, ranked by RS / oneil_20_8 at 20.9% CAGR (max realized DD -47.2%) vs SPY 14.6%.

**Next steps for the strategy:**

1. In-sample rankings don't persist: test fewer, more different ideas instead of fine-tuning parameters.
2. Loosen the definitions of htf or widen the universe so they can be evaluated.
3. Drop or rework: multi_touch, high52, stage2.
4. Focus development on: donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50 (tune them on IS data only, re-check OOS).
5. Make rs80_early a default filter.
6. Inspect risk_adr and risk_pct: plot avgR by bucket and consider a hard rule.
7. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
8. Build the scan around rs80_early first; entries are the second layer.
9. Turn that rule into a scan filter and test it as its own strategy.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                   | no_edge_entries             | best_exit   | helpful_filters                         |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                        | filters_lifting_baseline   |   rules_held | best_portfolio                        |   best_cagr |   spy_cagr |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------|:------------|:----------------------------------------|---------:|---------------:|---------------:|---------:|:----------------------------------------------------|:---------------------------|-------------:|:--------------------------------------|------------:|-----------:|
| 2026-10-08 08:22 | 5e93689  |      1488 |    633749 |        0.57 |        0.05 |          -0.07 | donchian_55, donchian_20, ema_retest, ep_gap5, ep_gap15, ep_gap10_vol5, ep_gap8_neglected, high52_fresh, ep_gap8_hold, ep_gap10, undercut, flag_60, flag_30_early, ep_gap10_vol2, vcp, base_50 | multi_touch, high52, stage2 | sma50_close | rs80_early, early_stage, rs80, rs80_mkt |     0.55 |           0.25 |          -0.07 |     0.01 | risk_adr, risk_pct, mkt_ret_21, qqq_ret_21, rs_rank | early_stage, rs80_early    |            4 | All setups, ranked by RS / oneil_20_8 |        0.21 |       0.15 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 1296.000 |
| strategies_with_enough_trades | 1134.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.565 |
| rank_corr_IS_vs_OOS_t         |    0.578 |
| OOS_avgR_all_strategies       |    0.072 |
| OOS_avgR_top20_by_IS          |    0.054 |
| OOS_avgR_random_baseline      |   -0.068 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry       | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------|:------------|:----------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| donchian_20 | all         | oneil_20_8      |  69752 |      0.17 |  21.85 |   78114 |      8915.98 |      0.30 |       0.04 |     1.06 |    6.22 |         377.85 |
| donchian_20 | early_stage | oneil_20_8      |  36654 |      0.22 |  20.71 |   47169 |      5383.90 |      0.31 |       0.08 |     1.11 |    9.18 |         432.31 |
| donchian_20 | mkt_ok      | oneil_20_8      |  57859 |      0.17 |  19.68 |   61630 |      7034.49 |      0.29 |       0.04 |     1.05 |    5.06 |         275.58 |
| donchian_55 | early_stage | oneil_20_8      |  19751 |      0.22 |  14.98 |   23762 |      2712.21 |      0.30 |       0.06 |     1.08 |    5.00 |         168.10 |
| donchian_55 | mkt_ok      | oneil_20_8      |  40475 |      0.14 |  13.36 |   40609 |      4635.14 |      0.29 |       0.02 |     1.03 |    2.36 |         104.74 |
| donchian_20 | early_stage | sma50_close     |  36539 |      0.14 |  12.78 |   47169 |      5383.90 |      0.29 |       0.07 |     1.12 |    6.91 |         395.23 |
| undercut    | all         | oneil_20_8      |  23171 |      0.27 |  10.78 |   26314 |      3003.50 |      0.18 |       0.08 |     1.09 |    4.02 |         254.89 |
| donchian_20 | all         | sma50_close     |  69460 |      0.08 |  10.29 |   78114 |      8915.98 |      0.28 |       0.04 |     1.06 |    4.41 |         327.82 |
| ema_retest  | all         | oneil_20_8      |  14517 |      0.23 |   9.61 |   15672 |      1788.81 |      0.22 |       0.04 |     1.05 |    2.10 |          76.56 |
| donchian_55 | early_stage | sma50_close     |  19656 |      0.15 |   9.54 |   23762 |      2712.21 |      0.30 |       0.10 |     1.15 |    5.61 |         265.50 |
| donchian_20 | early_stage | donchian_10low  |  36664 |      0.09 |   9.15 |   47169 |      5383.90 |      0.34 |       0.04 |     1.06 |    4.34 |         199.74 |
| donchian_20 | mkt_ok      | sma50_close     |  57624 |      0.08 |   8.97 |   61630 |      7034.49 |      0.28 |       0.04 |     1.06 |    4.12 |         279.83 |
| ema_retest  | early_stage | oneil_20_8      |   5834 |      0.33 |   8.83 |    6805 |       776.73 |      0.24 |       0.14 |     1.16 |    4.24 |         105.18 |
| ema_retest  | mkt_ok      | oneil_20_8      |  12240 |      0.22 |   8.41 |   12389 |      1414.09 |      0.22 |       0.06 |     1.07 |    2.66 |          87.69 |
| donchian_20 | early_stage | chandelier_3atr |  36671 |      0.08 |   8.35 |   47169 |      5383.90 |      0.35 |       0.03 |     1.06 |    4.09 |         174.22 |
| donchian_20 | early_stage | fixed_3r_20d    |  36932 |      0.06 |   8.25 |   47169 |      5383.90 |      0.43 |       0.05 |     1.08 |    7.38 |         254.52 |
| donchian_20 | early_stage | trim_ema        |  36538 |      0.06 |   7.98 |   47169 |      5383.90 |      0.33 |       0.04 |     1.07 |    5.61 |         213.21 |
| donchian_20 | all         | fixed_3r_20d    |  70387 |      0.04 |   7.63 |   78114 |      8915.98 |      0.41 |       0.01 |     1.02 |    2.89 |         128.47 |
| donchian_20 | rs80        | oneil_20_8      |  19657 |      0.10 |   7.09 |   22615 |      2581.29 |      0.29 |       0.04 |     1.05 |    3.25 |         105.95 |
| donchian_55 | all         | sma50_close     |  47449 |      0.07 |   7.00 |   50722 |      5789.44 |      0.29 |       0.03 |     1.05 |    2.95 |         197.13 |
| donchian_20 | rs80_mkt    | oneil_20_8      |  15291 |      0.11 |   6.78 |   16974 |      1937.42 |      0.29 |       0.05 |     1.06 |    3.30 |          94.57 |
| undercut    | all         | chandelier_3atr |  23194 |      0.15 |   6.57 |   26314 |      3003.50 |      0.23 |       0.09 |     1.10 |    4.01 |         264.22 |
| undercut    | all         | donchian_10low  |  23195 |      0.15 |   6.39 |   26314 |      3003.50 |      0.22 |       0.08 |     1.09 |    3.65 |         243.54 |
| donchian_55 | early_stage | trim_ema        |  19656 |      0.07 |   6.36 |   23762 |      2712.21 |      0.35 |       0.05 |     1.08 |    4.33 |         129.45 |
| donchian_55 | rs80_early  | oneil_20_8      |   4659 |      0.18 |   6.22 |    6407 |       731.30 |      0.32 |       0.14 |     1.19 |    5.87 |         101.94 |
| donchian_55 | rs80        | oneil_20_8      |  17090 |      0.09 |   5.88 |   19277 |      2200.29 |      0.29 |       0.05 |     1.07 |    3.93 |         119.56 |
| ema_retest  | early_stage | sma50_close     |   5805 |      0.24 |   5.85 |    6805 |       776.73 |      0.26 |       0.16 |     1.19 |    4.01 |         120.44 |
| undercut    | rs80        | oneil_20_8      |   5203 |      0.27 |   5.70 |    6454 |       736.66 |      0.20 |       0.11 |     1.11 |    2.65 |          77.85 |
| donchian_20 | rs80_early  | oneil_20_8      |   5502 |      0.14 |   5.66 |    7619 |       869.64 |      0.32 |       0.14 |     1.19 |    6.35 |         120.07 |
| donchian_55 | mkt_ok      | sma50_close     |  40261 |      0.06 |   5.28 |   40609 |      4635.14 |      0.29 |       0.06 |     1.08 |    4.31 |         270.18 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry        | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-------------|:------------|:----------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| donchian_20  | all         | oneil_20_8      |  69752 |      0.17 |  21.85 |   78114 |      0.30 |       0.04 |     1.06 |    6.22 |
| donchian_20  | early_stage | oneil_20_8      |  36654 |      0.22 |  20.71 |   47169 |      0.31 |       0.08 |     1.11 |    9.18 |
| donchian_20  | mkt_ok      | oneil_20_8      |  57859 |      0.17 |  19.68 |   61630 |      0.29 |       0.04 |     1.05 |    5.06 |
| donchian_55  | all         | oneil_20_8      |  47704 |      0.15 |  15.81 |   50722 |      0.29 |       0.02 |     1.02 |    1.94 |
| donchian_55  | early_stage | oneil_20_8      |  19751 |      0.22 |  14.98 |   23762 |      0.30 |       0.06 |     1.08 |    5.00 |
| donchian_55  | mkt_ok      | oneil_20_8      |  40475 |      0.14 |  13.36 |   40609 |      0.29 |       0.02 |     1.03 |    2.36 |
| donchian_20  | early_stage | sma50_close     |  36539 |      0.14 |  12.78 |   47169 |      0.29 |       0.07 |     1.12 |    6.91 |
| undercut     | all         | oneil_20_8      |  23171 |      0.27 |  10.78 |   26314 |      0.18 |       0.08 |     1.09 |    4.02 |
| donchian_20  | all         | sma50_close     |  69460 |      0.08 |  10.29 |   78114 |      0.28 |       0.04 |     1.06 |    4.41 |
| ema_retest   | all         | oneil_20_8      |  14517 |      0.23 |   9.61 |   15672 |      0.22 |       0.04 |     1.05 |    2.10 |
| donchian_55  | early_stage | sma50_close     |  19656 |      0.15 |   9.54 |   23762 |      0.30 |       0.10 |     1.15 |    5.61 |
| donchian_20  | early_stage | donchian_10low  |  36664 |      0.09 |   9.15 |   47169 |      0.34 |       0.04 |     1.06 |    4.34 |
| donchian_20  | mkt_ok      | sma50_close     |  57624 |      0.08 |   8.97 |   61630 |      0.28 |       0.04 |     1.06 |    4.12 |
| ema_retest   | early_stage | oneil_20_8      |   5834 |      0.33 |   8.83 |    6805 |      0.24 |       0.14 |     1.16 |    4.24 |
| ema_retest   | mkt_ok      | oneil_20_8      |  12240 |      0.22 |   8.41 |   12389 |      0.22 |       0.06 |     1.07 |    2.66 |
| donchian_20  | early_stage | chandelier_3atr |  36671 |      0.08 |   8.35 |   47169 |      0.35 |       0.03 |     1.06 |    4.09 |
| donchian_20  | early_stage | fixed_3r_20d    |  36932 |      0.06 |   8.25 |   47169 |      0.43 |       0.05 |     1.08 |    7.38 |
| donchian_20  | early_stage | trim_ema        |  36538 |      0.06 |   7.98 |   47169 |      0.33 |       0.04 |     1.07 |    5.61 |
| donchian_20  | all         | fixed_3r_20d    |  70387 |      0.04 |   7.63 |   78114 |      0.41 |       0.01 |     1.02 |    2.89 |
| undercut     | early_stage | oneil_20_8      |   6980 |      0.34 |   7.21 |    8334 |      0.17 |       0.07 |     1.07 |    1.77 |
| donchian_20  | rs80        | oneil_20_8      |  19657 |      0.10 |   7.09 |   22615 |      0.29 |       0.04 |     1.05 |    3.25 |
| donchian_55  | all         | sma50_close     |  47449 |      0.07 |   7.00 |   50722 |      0.29 |       0.03 |     1.05 |    2.95 |
| donchian_20  | all         | chandelier_3atr |  69863 |      0.05 |   6.96 |   78114 |      0.33 |       0.00 |     1.00 |    0.31 |
| donchian_20  | rs80_mkt    | oneil_20_8      |  15291 |      0.11 |   6.78 |   16974 |      0.29 |       0.05 |     1.06 |    3.30 |
| undercut     | all         | chandelier_3atr |  23194 |      0.15 |   6.57 |   26314 |      0.23 |       0.09 |     1.10 |    4.01 |
| pocket_pivot | all         | oneil_20_8      |  49369 |      0.12 |   6.57 |   48059 |      0.13 |      -0.07 |     0.94 |   -4.24 |
| donchian_20  | mkt_ok      | fixed_3r_20d    |  58441 |      0.04 |   6.43 |   61630 |      0.41 |       0.00 |     1.01 |    0.63 |
| undercut     | all         | donchian_10low  |  23195 |      0.15 |   6.39 |   26314 |      0.22 |       0.08 |     1.09 |    3.65 |
| donchian_55  | early_stage | trim_ema        |  19656 |      0.07 |   6.36 |   23762 |      0.35 |       0.05 |     1.08 |    4.33 |
| donchian_55  | rs80_early  | oneil_20_8      |   4659 |      0.18 |   6.22 |    6407 |      0.32 |       0.14 |     1.19 |    5.87 |

## 4. Each entry with its best in-sample exit/filter

| entry             | filter      | exit            |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------------|:------------|:----------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| base_50           | early_stage | oneil_20_8      |    593 |       49.44 |     0.29 |      0.15 |   1.56 |     888 |       101.36 |      0.30 |       0.29 |     1.38 |    3.58 |          29.57 |
| ep_gap10          | rs80_mkt    | trim_ema        |    193 |       16.09 |     0.41 |      0.45 |   2.39 |     337 |        38.47 |      0.35 |       0.25 |     1.39 |    1.82 |           9.47 |
| ep_gap10_vol2     | rs80_mkt    | chandelier_3atr |    211 |       17.59 |     0.34 |      0.52 |   2.13 |     394 |        44.97 |      0.33 |       0.24 |     1.39 |    1.84 |          10.59 |
| ep_gap15          | mkt_ok      | trim_ema        |     96 |        8.00 |     0.41 |      0.62 |   2.46 |     235 |        26.82 |      0.38 |       0.22 |     1.36 |    1.48 |           5.95 |
| ep_gap8_hold      | rs80_mkt    | trim_ema        |    286 |       23.84 |     0.43 |      0.38 |   2.77 |     418 |        47.71 |      0.35 |       0.14 |     1.23 |    1.32 |           6.84 |
| ep_gap8_neglected | all         | oneil_20_8      |    612 |       51.02 |     0.33 |      0.27 |   2.83 |     934 |       106.61 |      0.30 |       0.14 |     1.19 |    2.06 |          14.78 |
| undercut          | all         | oneil_20_8      |  23171 |     1931.80 |     0.20 |      0.27 |  10.78 |   26314 |      3003.50 |      0.18 |       0.08 |     1.09 |    4.02 |         254.89 |
| flag_60           | rs80_mkt    | oneil_20_8      |    208 |       17.34 |     0.25 |      0.17 |   1.06 |     371 |        42.35 |      0.26 |       0.08 |     1.10 |    0.68 |           3.58 |
| ep_gap10_vol5     | rs80_mkt    | fixed_3r_20d    |    136 |       11.34 |     0.51 |      0.30 |   2.47 |     191 |        21.80 |      0.39 |       0.06 |     1.11 |    0.63 |           1.41 |
| base_25           | rs80_mkt    | sma50_close     |    946 |       78.87 |     0.26 |      0.16 |   1.44 |    1097 |       125.21 |      0.23 |       0.06 |     1.07 |    0.59 |           7.44 |
| ep_gap5           | rs80_mkt    | oneil_20_8      |    606 |       50.52 |     0.33 |      0.33 |   3.27 |     736 |        84.01 |      0.29 |       0.06 |     1.08 |    0.81 |           4.80 |
| ema_retest        | all         | oneil_20_8      |  14517 |     1210.30 |     0.25 |      0.23 |   9.61 |   15672 |      1788.81 |      0.22 |       0.04 |     1.05 |    2.10 |          76.56 |
| donchian_20       | all         | oneil_20_8      |  69752 |     5815.32 |     0.32 |      0.17 |  21.85 |   78114 |      8915.98 |      0.30 |       0.04 |     1.06 |    6.22 |         377.85 |
| random_uptrend    | early_stage | oneil_20_8      |  11111 |      926.34 |     0.13 |      0.18 |   4.36 |   13156 |      1501.63 |      0.12 |       0.02 |     1.02 |    0.57 |          30.07 |
| donchian_55       | all         | oneil_20_8      |  47704 |     3977.15 |     0.31 |      0.15 |  15.81 |   50722 |      5789.44 |      0.29 |       0.02 |     1.02 |    1.94 |          95.24 |
| high52_fresh      | all         | oneil_20_8      |   8213 |      684.73 |     0.21 |      0.14 |   4.06 |    8415 |       960.49 |      0.19 |       0.01 |     1.01 |    0.19 |           5.76 |
| vcp               | all         | oneil_20_8      |   1301 |      108.47 |     0.42 |      0.17 |   3.91 |     879 |       100.33 |      0.36 |       0.00 |     1.01 |    0.07 |           0.36 |
| flag_30           | mkt_ok      | oneil_20_8      |    895 |       74.62 |     0.23 |      0.05 |   0.63 |    1376 |       157.06 |      0.21 |      -0.03 |     0.96 |   -0.55 |          -5.43 |
| flag_30_early     | rs80        | chandelier_3atr |    718 |       59.86 |     0.23 |      0.11 |   0.89 |    1005 |       114.71 |      0.23 |      -0.05 |     0.95 |   -0.51 |          -5.21 |
| pocket_pivot      | all         | oneil_20_8      |  49369 |     4115.96 |     0.15 |      0.12 |   6.57 |   48059 |      5485.48 |      0.13 |      -0.07 |     0.94 |   -4.24 |        -388.55 |
| multi_touch       | all         | oneil_20_8      |  12640 |     1053.81 |     0.22 |      0.17 |   5.85 |   10634 |      1213.77 |      0.19 |      -0.08 |     0.91 |   -2.93 |         -98.70 |
| high52            | all         | oneil_20_8      |  30340 |     2529.49 |     0.17 |      0.04 |   2.30 |   29119 |      3323.66 |      0.16 |      -0.09 |     0.91 |   -4.83 |        -290.99 |
| stage2            | all         | oneil_20_8      |   5997 |      499.98 |     0.26 |      0.23 |   5.80 |    4847 |       553.24 |      0.21 |      -0.12 |     0.87 |   -3.23 |         -66.97 |
| htf               | all         | sma50_close     |     52 |        4.34 |     0.17 |      0.41 |   0.66 |      99 |        11.30 |      0.11 |      -0.34 |     0.65 |   -1.17 |          -3.85 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| base_25           |              0.12 |             0.09 |          0.10 |           0.08 |         0.10 |         0.04 |         0.07 |          0.23 |       0.13 |
| base_50           |              0.16 |             0.11 |          0.14 |           0.11 |         0.12 |         0.08 |         0.10 |          0.22 |       0.15 |
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
| flag_30           |              0.07 |             0.13 |          0.14 |           0.06 |         0.03 |         0.08 |         0.08 |          0.28 |       0.15 |
| flag_30_early     |              0.18 |             0.16 |          0.17 |           0.15 |         0.22 |         0.13 |         0.13 |          0.25 |       0.19 |
| flag_60           |              0.19 |             0.16 |          0.18 |           0.10 |         0.11 |         0.13 |         0.11 |          0.53 |       0.32 |
| high52            |             -0.04 |            -0.05 |         -0.03 |          -0.03 |        -0.04 |        -0.03 |        -0.05 |         -0.05 |      -0.02 |
| high52_fresh      |              0.06 |             0.04 |          0.07 |           0.05 |         0.05 |         0.04 |         0.03 |          0.07 |       0.07 |
| htf               |             -0.19 |            -0.30 |         -0.14 |          -0.15 |        -0.17 |        -0.01 |        -0.10 |         -0.31 |      -0.07 |
| multi_touch       |             -0.03 |            -0.00 |         -0.02 |          -0.00 |        -0.04 |         0.01 |        -0.01 |         -0.06 |      -0.01 |
| pocket_pivot      |             -0.02 |            -0.02 |         -0.01 |           0.00 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.01 |
| stage2            |             -0.07 |            -0.07 |         -0.06 |          -0.02 |        -0.08 |        -0.02 |        -0.05 |         -0.10 |      -0.05 |
| undercut          |              0.18 |             0.16 |          0.02 |           0.08 |         0.13 |         0.09 |         0.08 |         -0.00 |       0.03 |
| vcp               |              0.06 |             0.04 |          0.04 |           0.10 |         0.05 |         0.07 |         0.06 |         -0.05 |       0.04 |

Same, in-sample:

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| base_25           |             -0.03 |            -0.04 |         -0.00 |           0.07 |        -0.08 |         0.06 |         0.03 |          0.03 |       0.09 |
| base_50           |              0.00 |            -0.00 |          0.04 |           0.13 |        -0.04 |         0.08 |         0.05 |         -0.03 |       0.09 |
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
| flag_30           |             -0.08 |            -0.10 |         -0.05 |           0.05 |        -0.11 |         0.02 |        -0.03 |         -0.09 |       0.01 |
| flag_30_early     |              0.11 |             0.08 |          0.12 |           0.05 |        -0.04 |         0.06 |         0.09 |          0.01 |       0.03 |
| flag_60           |              0.04 |             0.02 |          0.09 |           0.12 |        -0.02 |         0.15 |         0.09 |          0.07 |       0.12 |
| high52            |             -0.03 |            -0.04 |          0.01 |           0.02 |        -0.03 |        -0.02 |        -0.02 |         -0.03 |       0.00 |
| high52_fresh      |              0.06 |             0.05 |          0.09 |           0.08 |         0.07 |         0.04 |         0.05 |          0.07 |       0.08 |
| htf               |             -0.07 |             0.26 |          0.15 |           0.08 |        -0.09 |         0.14 |         0.20 |          0.45 |       0.29 |
| multi_touch       |              0.07 |             0.08 |          0.12 |           0.10 |         0.09 |         0.06 |         0.06 |          0.12 |       0.10 |
| pocket_pivot      |              0.05 |             0.06 |          0.07 |           0.03 |         0.04 |         0.03 |         0.03 |          0.07 |       0.04 |
| stage2            |              0.11 |             0.13 |          0.16 |           0.11 |         0.16 |         0.07 |         0.09 |          0.15 |       0.14 |
| undercut          |              0.21 |             0.22 |          0.06 |           0.12 |         0.19 |         0.18 |         0.17 |          0.01 |       0.08 |
| vcp               |              0.07 |             0.08 |          0.12 |           0.13 |         0.10 |         0.10 |         0.09 |          0.09 |       0.17 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| sma50_close     |      0.10 |       0.16 |      0.25 |     1.23 |                       0.70 |
| trim_ema        |      0.02 |       0.04 |      0.35 |     1.07 |                       0.78 |
| oneil_20_8      |      0.12 |       0.04 |      0.25 |     1.05 |                       0.78 |
| donchian_10low  |      0.03 |       0.03 |      0.28 |     1.07 |                       0.78 |
| chandelier_3atr |      0.04 |       0.01 |      0.28 |     1.03 |                       0.78 |
| ema21_close     |     -0.02 |      -0.00 |      0.30 |     1.01 |                       0.78 |
| fixed_3r_20d    |      0.01 |      -0.01 |      0.36 |     1.00 |                       0.83 |
| qull_sma20      |     -0.03 |      -0.03 |      0.42 |     0.96 |                       0.78 |
| qull_sma10      |     -0.04 |      -0.04 |      0.41 |     0.93 |                       0.87 |

## 7. Filters (averaged over all entry x exit combinations)

| filter      |   IS_avgR |   OOS_avgR |   OOS_win |
|:------------|----------:|-----------:|----------:|
| rs80_early  |      0.08 |       0.16 |      0.36 |
| early_stage |      0.06 |       0.09 |      0.34 |
| rs80        |      0.04 |       0.09 |      0.34 |
| rs80_mkt    |      0.09 |       0.06 |      0.33 |
| all         |      0.02 |       0.02 |      0.32 |
| mkt_ok      |      0.05 |       0.02 |      0.32 |

## 8. ML meta-labeling (exit: oneil_20_8, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.254; AUC for R > 0: 0.554 (0.5 = no skill). Taken (model's top third, causal threshold): n=93,785, avgR=0.011, win=0.260. Skipped: n=195,935, avgR=0.001, win=0.214.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 28972.00 |  -0.10 |  0.13 |
|      1 | 28973.00 |   0.01 |  0.19 |
|      2 | 28971.00 |   0.05 |  0.22 |
|      3 | 28972.00 |   0.04 |  0.24 |
|      4 | 28973.00 |   0.02 |  0.24 |
|      5 | 28971.00 |   0.02 |  0.25 |
|      6 | 28972.00 |  -0.01 |  0.25 |
|      7 | 28972.00 |   0.03 |  0.26 |
|      8 | 28972.00 |   0.02 |  0.26 |
|      9 | 28972.00 |  -0.03 |  0.26 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| ep_gap15          |   374.00 |       0.23 |    212.00 |         0.29 |           0.15 |
| flag_60           |   615.00 |       0.07 |    192.00 |         0.25 |          -0.02 |
| ep_gap8_neglected |   934.00 |       0.14 |    466.00 |         0.25 |           0.03 |
| ep_gap10_vol2     |  1182.00 |       0.16 |    597.00 |         0.24 |           0.08 |
| ep_gap10          |   933.00 |       0.11 |    466.00 |         0.21 |           0.01 |
| flag_30_early     |  1955.00 |       0.17 |    554.00 |         0.17 |           0.17 |
| ep_gap8_hold      |  1182.00 |       0.10 |    592.00 |         0.16 |           0.04 |
| ep_gap10_vol5     |   454.00 |       0.08 |    242.00 |         0.13 |           0.02 |
| undercut          | 26314.00 |       0.08 |   8744.00 |         0.12 |           0.07 |
| ep_gap5           |  2322.00 |       0.05 |   1133.00 |         0.09 |           0.01 |
| vcp               |   879.00 |       0.00 |    373.00 |         0.05 |          -0.03 |
| base_50           |  2665.00 |       0.07 |    971.00 |         0.04 |           0.09 |
| donchian_20       | 78114.00 |       0.04 |  33096.00 |         0.02 |           0.06 |
| base_25           |  2444.00 |       0.05 |    913.00 |         0.01 |           0.08 |
| donchian_55       | 50722.00 |       0.02 |  18307.00 |         0.00 |           0.02 |
| flag_30           |  1786.00 |      -0.01 |    521.00 |        -0.01 |          -0.01 |
| ema_retest        | 15672.00 |       0.04 |   5500.00 |        -0.03 |           0.08 |
| pocket_pivot      | 48059.00 |      -0.07 |   8528.00 |        -0.03 |          -0.08 |
| high52            | 29119.00 |      -0.09 |   5300.00 |        -0.07 |          -0.09 |
| high52_fresh      |  8415.00 |       0.01 |   2268.00 |        -0.08 |           0.04 |
| stage2            |  4847.00 |      -0.12 |   1665.00 |        -0.08 |          -0.14 |
| multi_touch       | 10634.00 |      -0.08 |   3114.00 |        -0.11 |          -0.07 |
| htf               |    99.00 |      -0.22 |     31.00 |        -0.32 |          -0.18 |

Same model on your trim plan (trim_ema): rank corr 0.124, taken avgR 0.016 vs skipped -0.062.

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature       |   rank_corr_drop |
|:--------------|-----------------:|
| risk_adr      |           0.1412 |
| risk_pct      |           0.0645 |
| mkt_ret_21    |           0.0411 |
| qqq_ret_21    |           0.0309 |
| rs_rank       |           0.0203 |
| above_52w_low |           0.0181 |
| gap           |           0.0137 |
| leg3_range    |           0.0110 |
| breadth_50    |           0.0086 |
| mkt_ema_stack |           0.0080 |
| dist_52w_high |           0.0079 |
| sma200_slope  |           0.0069 |
| vol_dryup     |           0.0065 |
| leg1_range    |           0.0063 |
| ext_ema8_adr  |           0.0043 |
| tight_10      |           0.0036 |
| close_std_10  |           0.0030 |
| mkt_above200  |           0.0026 |
| qqq_ok        |           0.0025 |
| mkt_ok        |           0.0021 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                              |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio <= 1.11   |   2779 |      0.92 |    4480 |       0.05 |      0.10 |
| risk_adr > 0.633 AND rates_rising > 0.5 AND mkt_ema_stack <= 0.5  |  21516 |      0.60 |   34798 |       0.13 |      0.29 |
| risk_adr <= 0.633 AND breadth_50 <= 0.523 AND vol_ratio > 1.11    |   4080 |      0.26 |    5384 |       0.12 |      0.11 |
| risk_adr > 0.633 AND rates_rising > 0.5 AND mkt_ema_stack > 0.5   | 102097 |      0.24 |   75340 |      -0.08 |      0.22 |
| risk_adr > 0.633 AND rates_rising <= 0.5 AND qqq_ret_21 <= 0.0299 |  56924 |      0.16 |   69801 |       0.06 |      0.26 |
| risk_adr <= 0.633 AND breadth_50 > 0.523 AND leg3_range > 0.117   |   9758 |      0.06 |   14337 |      -0.04 |      0.11 |
| risk_adr <= 0.633 AND breadth_50 > 0.523 AND leg3_range <= 0.117  |  19784 |     -0.06 |   15910 |      -0.15 |      0.08 |
| risk_adr > 0.633 AND rates_rising <= 0.5 AND qqq_ret_21 > 0.0299  |  57912 |     -0.13 |   69670 |       0.00 |      0.25 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                       |   CAGR |   max_DD_realized |   trades |    win |   avg_positions |
|:---------------------------------------------------------------|-------:|------------------:|---------:|-------:|----------------:|
| donchian_20 / all / oneil_20_8                                 |   0.08 |             -0.31 |  1044.00 |   0.32 |            8.84 |
| donchian_55 / all / oneil_20_8                                 |  -0.03 |             -0.52 |  1075.00 |   0.28 |            8.80 |
| undercut / all / oneil_20_8                                    |   0.10 |             -0.44 |  1404.00 |   0.19 |            7.37 |
| ema_retest / all / oneil_20_8                                  |   0.01 |             -0.47 |   880.00 |   0.25 |            7.18 |
| pocket_pivot / all / oneil_20_8                                |   0.12 |             -0.28 |  1356.00 |   0.18 |            6.63 |
| All setups, ML-filtered (top third), ranked by ML / oneil_20_8 |   0.13 |             -0.29 |   953.00 |   0.29 |            7.73 |
| All setups, ranked by ML prediction / oneil_20_8               |   0.13 |             -0.29 |   995.00 |   0.28 |            7.83 |
| All setups, ranked by RS / oneil_20_8                          |   0.21 |             -0.47 |  1645.00 |   0.27 |            8.71 |
| All setups, random order / oneil_20_8                          |   0.05 |             -0.33 |  1060.00 |   0.22 |            7.88 |
| All setups + rs80_early filter, ranked by RS / oneil_20_8      |   0.13 |             -0.29 |  1341.00 |   0.26 |            8.54 |
| BASELINE random entries, ranked by RS / oneil_20_8             |   0.04 |             -0.49 |  1714.00 |   0.15 |            6.36 |
| BASELINE random entries, random order / oneil_20_8             |  -0.01 |             -0.47 |  1383.00 |   0.12 |            6.11 |
| SPY buy & hold                                                 |   0.15 |             -0.34 |   nan    | nan    |          nan    |

Equity is marked on closed trades only, so drawdowns are understated vs. daily mark-to-market.

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