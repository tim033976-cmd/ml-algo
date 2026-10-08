# Strategy research report

Generated 2026-10-08 07:17 UTC in 10 min.
Universe: 1488 stocks with data (sp600: 591, sp500: 499, sp400: 398; 0 former S&P 500 members). Signals 2006-01-03 -> 2026-10-06: 628,659.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 1080.000 |
| strategies_with_enough_trades |  963.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.465 |
| rank_corr_IS_vs_OOS_t         |    0.553 |
| OOS_avgR_all_strategies       |    0.044 |
| OOS_avgR_top20_by_IS          |    0.052 |
| OOS_avgR_random_baseline      |   -0.068 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry       | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------|:------------|:----------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| donchian_20 | all         | oneil_20_8      |  69729 |      0.17 |  21.80 |   78107 |      8915.18 |      0.30 |       0.04 |     1.06 |    6.22 |         378.15 |
| donchian_20 | early_stage | oneil_20_8      |  36652 |      0.22 |  20.61 |   47166 |      5383.56 |      0.31 |       0.08 |     1.11 |    9.11 |         428.71 |
| donchian_20 | mkt_ok      | oneil_20_8      |  57837 |      0.17 |  19.56 |   61621 |      7033.46 |      0.29 |       0.04 |     1.05 |    5.05 |         274.99 |
| donchian_55 | early_stage | oneil_20_8      |  19743 |      0.22 |  14.92 |   23752 |      2711.07 |      0.30 |       0.06 |     1.08 |    4.74 |         159.09 |
| donchian_55 | mkt_ok      | oneil_20_8      |  40483 |      0.14 |  13.25 |   40600 |      4634.11 |      0.28 |       0.02 |     1.03 |    2.26 |         100.55 |
| donchian_20 | early_stage | sma50_close     |  36539 |      0.14 |  12.66 |   47166 |      5383.56 |      0.29 |       0.07 |     1.12 |    6.85 |         392.25 |
| undercut    | all         | oneil_20_8      |  23188 |      0.27 |  10.86 |   26315 |      3003.61 |      0.18 |       0.08 |     1.08 |    3.96 |         250.36 |
| donchian_20 | all         | sma50_close     |  69437 |      0.08 |  10.21 |   78107 |      8915.18 |      0.28 |       0.04 |     1.06 |    4.39 |         325.98 |
| donchian_55 | early_stage | sma50_close     |  19649 |      0.15 |   9.53 |   23752 |      2711.07 |      0.30 |       0.10 |     1.14 |    5.54 |         262.09 |
| donchian_20 | mkt_ok      | sma50_close     |  57602 |      0.08 |   8.85 |   61621 |      7033.46 |      0.28 |       0.04 |     1.06 |    4.12 |         279.86 |
| donchian_20 | early_stage | donchian_10low  |  36662 |      0.08 |   8.83 |   47166 |      5383.56 |      0.34 |       0.04 |     1.06 |    4.37 |         201.21 |
| ema_retest  | early_stage | oneil_20_8      |   5850 |      0.32 |   8.65 |    6804 |       776.61 |      0.24 |       0.13 |     1.16 |    4.22 |         104.29 |
| ema_retest  | mkt_ok      | oneil_20_8      |  12247 |      0.21 |   8.30 |   12391 |      1414.32 |      0.22 |       0.06 |     1.07 |    2.46 |          80.90 |
| donchian_20 | early_stage | chandelier_3atr |  36668 |      0.08 |   8.25 |   47166 |      5383.56 |      0.35 |       0.03 |     1.06 |    4.07 |         173.22 |
| donchian_20 | early_stage | fixed_3r_20d    |  36930 |      0.06 |   8.13 |   47166 |      5383.56 |      0.43 |       0.05 |     1.08 |    7.30 |         251.85 |
| donchian_20 | early_stage | trim_ema        |  36540 |      0.06 |   7.94 |   47166 |      5383.56 |      0.33 |       0.04 |     1.07 |    5.56 |         211.36 |
| donchian_20 | all         | fixed_3r_20d    |  70363 |      0.04 |   7.60 |   78107 |      8915.18 |      0.41 |       0.01 |     1.02 |    2.88 |         127.61 |
| donchian_20 | rs80        | oneil_20_8      |  19647 |      0.10 |   7.11 |   22612 |      2580.95 |      0.29 |       0.04 |     1.05 |    3.28 |         106.81 |
| donchian_55 | all         | sma50_close     |  47449 |      0.07 |   7.01 |   50716 |      5788.76 |      0.29 |       0.03 |     1.05 |    2.93 |         195.58 |
| donchian_20 | rs80_mkt    | oneil_20_8      |  15282 |      0.11 |   6.79 |   16968 |      1936.74 |      0.29 |       0.05 |     1.06 |    3.32 |          95.36 |
| undercut    | all         | chandelier_3atr |  23211 |      0.15 |   6.60 |   26315 |      3003.61 |      0.23 |       0.09 |     1.10 |    3.93 |         258.21 |
| undercut    | all         | donchian_10low  |  23213 |      0.15 |   6.52 |   26315 |      3003.61 |      0.22 |       0.08 |     1.09 |    3.56 |         236.88 |
| donchian_55 | early_stage | trim_ema        |  19649 |      0.07 |   6.36 |   23752 |      2711.07 |      0.35 |       0.05 |     1.07 |    4.24 |         126.85 |
| donchian_55 | rs80_early  | oneil_20_8      |   4661 |      0.17 |   6.04 |    6393 |       729.70 |      0.32 |       0.13 |     1.19 |    5.69 |          98.42 |
| donchian_55 | rs80        | oneil_20_8      |  17092 |      0.09 |   5.86 |   19274 |      2199.95 |      0.29 |       0.05 |     1.07 |    3.94 |         119.73 |
| undercut    | rs80        | oneil_20_8      |   5216 |      0.27 |   5.73 |    6453 |       736.55 |      0.20 |       0.11 |     1.11 |    2.68 |          78.74 |
| ema_retest  | early_stage | sma50_close     |   5821 |      0.23 |   5.67 |    6804 |       776.61 |      0.26 |       0.15 |     1.19 |    3.98 |         119.50 |
| donchian_20 | rs80_early  | oneil_20_8      |   5503 |      0.14 |   5.55 |    7612 |       868.84 |      0.32 |       0.13 |     1.19 |    6.20 |         116.96 |
| donchian_55 | mkt_ok      | sma50_close     |  40269 |      0.06 |   5.26 |   40600 |      4634.11 |      0.29 |       0.06 |     1.08 |    4.34 |         271.73 |
| donchian_55 | rs80_mkt    | oneil_20_8      |  13618 |      0.08 |   4.70 |   14787 |      1687.80 |      0.29 |       0.07 |     1.09 |    4.20 |         113.86 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry        | filter      | exit            |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-------------|:------------|:----------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| donchian_20  | all         | oneil_20_8      |  69729 |      0.17 |  21.80 |   78107 |      0.30 |       0.04 |     1.06 |    6.22 |
| donchian_20  | early_stage | oneil_20_8      |  36652 |      0.22 |  20.61 |   47166 |      0.31 |       0.08 |     1.11 |    9.11 |
| donchian_20  | mkt_ok      | oneil_20_8      |  57837 |      0.17 |  19.56 |   61621 |      0.29 |       0.04 |     1.05 |    5.05 |
| donchian_55  | all         | oneil_20_8      |  47703 |      0.15 |  15.76 |   50716 |      0.29 |       0.02 |     1.02 |    1.84 |
| donchian_55  | early_stage | oneil_20_8      |  19743 |      0.22 |  14.92 |   23752 |      0.30 |       0.06 |     1.08 |    4.74 |
| donchian_55  | mkt_ok      | oneil_20_8      |  40483 |      0.14 |  13.25 |   40600 |      0.28 |       0.02 |     1.03 |    2.26 |
| donchian_20  | early_stage | sma50_close     |  36539 |      0.14 |  12.66 |   47166 |      0.29 |       0.07 |     1.12 |    6.85 |
| undercut     | all         | oneil_20_8      |  23188 |      0.27 |  10.86 |   26315 |      0.18 |       0.08 |     1.08 |    3.96 |
| donchian_20  | all         | sma50_close     |  69437 |      0.08 |  10.21 |   78107 |      0.28 |       0.04 |     1.06 |    4.39 |
| ema_retest   | all         | oneil_20_8      |  14528 |      0.23 |   9.59 |   15673 |      0.22 |       0.04 |     1.05 |    1.97 |
| donchian_55  | early_stage | sma50_close     |  19649 |      0.15 |   9.53 |   23752 |      0.30 |       0.10 |     1.14 |    5.54 |
| donchian_20  | mkt_ok      | sma50_close     |  57602 |      0.08 |   8.85 |   61621 |      0.28 |       0.04 |     1.06 |    4.12 |
| donchian_20  | early_stage | donchian_10low  |  36662 |      0.08 |   8.83 |   47166 |      0.34 |       0.04 |     1.06 |    4.37 |
| ema_retest   | early_stage | oneil_20_8      |   5850 |      0.32 |   8.65 |    6804 |      0.24 |       0.13 |     1.16 |    4.22 |
| ema_retest   | mkt_ok      | oneil_20_8      |  12247 |      0.21 |   8.30 |   12391 |      0.22 |       0.06 |     1.07 |    2.46 |
| donchian_20  | early_stage | chandelier_3atr |  36668 |      0.08 |   8.25 |   47166 |      0.35 |       0.03 |     1.06 |    4.07 |
| donchian_20  | early_stage | fixed_3r_20d    |  36930 |      0.06 |   8.13 |   47166 |      0.43 |       0.05 |     1.08 |    7.30 |
| donchian_20  | early_stage | trim_ema        |  36540 |      0.06 |   7.94 |   47166 |      0.33 |       0.04 |     1.07 |    5.56 |
| donchian_20  | all         | fixed_3r_20d    |  70363 |      0.04 |   7.60 |   78107 |      0.41 |       0.01 |     1.02 |    2.88 |
| undercut     | early_stage | oneil_20_8      |   6988 |      0.35 |   7.35 |    8326 |      0.17 |       0.06 |     1.06 |    1.69 |
| donchian_20  | rs80        | oneil_20_8      |  19647 |      0.10 |   7.11 |   22612 |      0.29 |       0.04 |     1.05 |    3.28 |
| donchian_55  | all         | sma50_close     |  47449 |      0.07 |   7.01 |   50716 |      0.29 |       0.03 |     1.05 |    2.93 |
| donchian_20  | all         | chandelier_3atr |  69840 |      0.05 |   6.93 |   78107 |      0.33 |       0.00 |     1.00 |    0.31 |
| donchian_20  | rs80_mkt    | oneil_20_8      |  15282 |      0.11 |   6.79 |   16968 |      0.29 |       0.05 |     1.06 |    3.32 |
| undercut     | all         | chandelier_3atr |  23211 |      0.15 |   6.60 |   26315 |      0.23 |       0.09 |     1.10 |    3.93 |
| pocket_pivot | all         | oneil_20_8      |  49369 |      0.12 |   6.58 |   48059 |      0.13 |      -0.07 |     0.93 |   -4.32 |
| undercut     | all         | donchian_10low  |  23213 |      0.15 |   6.52 |   26315 |      0.22 |       0.08 |     1.09 |    3.56 |
| donchian_55  | early_stage | trim_ema        |  19649 |      0.07 |   6.36 |   23752 |      0.35 |       0.05 |     1.07 |    4.24 |
| donchian_20  | mkt_ok      | fixed_3r_20d    |  58419 |      0.04 |   6.33 |   61621 |      0.41 |       0.00 |     1.01 |    0.66 |
| multi_touch  | all         | oneil_20_8      |  12630 |      0.18 |   6.09 |   10634 |      0.19 |      -0.08 |     0.92 |   -2.90 |

## 4. Each entry with its best in-sample exit/filter

| entry             | filter      | exit            |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:------------------|:------------|:----------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| base_50           | early_stage | oneil_20_8      |    592 |       49.36 |     0.29 |      0.15 |   1.57 |     888 |       101.36 |      0.30 |       0.29 |     1.38 |    3.59 |          29.70 |
| ep_gap10          | rs80_mkt    | trim_ema        |    193 |       16.09 |     0.41 |      0.45 |   2.39 |     337 |        38.47 |      0.35 |       0.25 |     1.39 |    1.83 |           9.54 |
| ep_gap8_neglected | all         | oneil_20_8      |    612 |       51.02 |     0.33 |      0.27 |   2.83 |     934 |       106.61 |      0.30 |       0.14 |     1.19 |    2.06 |          14.78 |
| flag_60           | rs80_mkt    | oneil_20_8      |    208 |       17.34 |     0.25 |      0.18 |   1.08 |     371 |        42.35 |      0.26 |       0.08 |     1.10 |    0.68 |           3.58 |
| undercut          | all         | oneil_20_8      |  23188 |     1933.22 |     0.20 |      0.27 |  10.86 |   26315 |      3003.61 |      0.18 |       0.08 |     1.08 |    3.96 |         250.36 |
| base_25           | rs80_mkt    | sma50_close     |    944 |       78.70 |     0.26 |      0.17 |   1.54 |    1096 |       125.10 |      0.23 |       0.06 |     1.07 |    0.60 |           7.57 |
| ep_gap5           | rs80_mkt    | oneil_20_8      |    606 |       50.52 |     0.33 |      0.33 |   3.27 |     736 |        84.01 |      0.29 |       0.06 |     1.08 |    0.81 |           4.80 |
| donchian_20       | all         | oneil_20_8      |  69729 |     5813.40 |     0.32 |      0.17 |  21.80 |   78107 |      8915.18 |      0.30 |       0.04 |     1.06 |    6.22 |         378.15 |
| ema_retest        | all         | oneil_20_8      |  14528 |     1211.22 |     0.25 |      0.23 |   9.59 |   15673 |      1788.93 |      0.22 |       0.04 |     1.05 |    1.97 |          71.49 |
| random_uptrend    | early_stage | oneil_20_8      |  11113 |      926.51 |     0.13 |      0.18 |   4.40 |   13152 |      1501.18 |      0.12 |       0.02 |     1.02 |    0.62 |          32.44 |
| donchian_55       | all         | oneil_20_8      |  47703 |     3977.06 |     0.31 |      0.15 |  15.76 |   50716 |      5788.76 |      0.29 |       0.02 |     1.02 |    1.84 |          90.15 |
| high52_fresh      | all         | oneil_20_8      |   8213 |      684.73 |     0.21 |      0.15 |   4.33 |    8413 |       960.27 |      0.19 |       0.01 |     1.01 |    0.18 |           5.61 |
| vcp               | all         | oneil_20_8      |   1304 |      108.72 |     0.42 |      0.17 |   3.90 |     880 |       100.44 |      0.36 |       0.00 |     1.00 |    0.05 |           0.24 |
| flag_30           | mkt_ok      | oneil_20_8      |    892 |       74.37 |     0.24 |      0.06 |   0.72 |    1380 |       157.51 |      0.21 |      -0.03 |     0.97 |   -0.47 |          -4.70 |
| flag_30_early     | rs80        | chandelier_3atr |    719 |       59.94 |     0.23 |      0.12 |   0.98 |    1004 |       114.60 |      0.23 |      -0.05 |     0.94 |   -0.54 |          -5.47 |
| high52            | early_stage | oneil_20_8      |   8167 |      680.89 |     0.19 |      0.09 |   2.47 |    9514 |      1085.93 |      0.17 |      -0.06 |     0.94 |   -2.01 |         -69.05 |
| pocket_pivot      | all         | oneil_20_8      |  49369 |     4115.96 |     0.15 |      0.12 |   6.58 |   48059 |      5485.48 |      0.13 |      -0.07 |     0.93 |   -4.32 |        -395.22 |
| multi_touch       | all         | oneil_20_8      |  12630 |     1052.98 |     0.22 |      0.18 |   6.09 |   10634 |      1213.77 |      0.19 |      -0.08 |     0.92 |   -2.90 |         -97.92 |
| stage2            | all         | oneil_20_8      |   5998 |      500.06 |     0.26 |      0.24 |   5.89 |    4842 |       552.67 |      0.21 |      -0.12 |     0.87 |   -3.24 |         -67.11 |
| htf               | all         | sma50_close     |     53 |        4.42 |     0.17 |      0.39 |   0.63 |      98 |        11.19 |      0.11 |      -0.33 |     0.65 |   -1.13 |          -3.72 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| base_25           |              0.12 |             0.09 |          0.10 |           0.08 |         0.10 |         0.04 |         0.07 |          0.23 |       0.13 |
| base_50           |              0.16 |             0.11 |          0.14 |           0.10 |         0.12 |         0.08 |         0.10 |          0.22 |       0.15 |
| donchian_20       |              0.10 |             0.09 |          0.09 |           0.11 |         0.09 |         0.08 |         0.08 |          0.07 |       0.11 |
| donchian_55       |              0.07 |             0.06 |          0.07 |           0.08 |         0.06 |         0.07 |         0.06 |          0.06 |       0.10 |
| ema_retest        |              0.07 |             0.05 |          0.07 |           0.09 |         0.09 |         0.07 |         0.05 |          0.07 |       0.10 |
| ep_gap10          |              0.25 |             0.35 |          0.27 |           0.20 |         0.15 |         0.11 |         0.17 |          0.52 |       0.32 |
| ep_gap5           |              0.15 |             0.17 |          0.15 |           0.12 |         0.10 |         0.09 |         0.11 |          0.21 |       0.16 |
| ep_gap8_neglected |              0.14 |             0.18 |          0.22 |           0.18 |         0.18 |         0.11 |         0.13 |          0.29 |       0.24 |
| flag_30           |              0.07 |             0.13 |          0.14 |           0.06 |         0.04 |         0.08 |         0.08 |          0.28 |       0.15 |
| flag_30_early     |              0.18 |             0.16 |          0.17 |           0.15 |         0.21 |         0.13 |         0.13 |          0.25 |       0.19 |
| flag_60           |              0.19 |             0.16 |          0.18 |           0.10 |         0.11 |         0.12 |         0.11 |          0.53 |       0.32 |
| high52            |             -0.04 |            -0.05 |         -0.03 |          -0.03 |        -0.04 |        -0.03 |        -0.04 |         -0.04 |      -0.02 |
| high52_fresh      |              0.06 |             0.04 |          0.07 |           0.05 |         0.05 |         0.04 |         0.03 |          0.07 |       0.07 |
| htf               |             -0.18 |            -0.30 |         -0.13 |          -0.14 |        -0.17 |         0.01 |        -0.09 |         -0.30 |      -0.06 |
| multi_touch       |             -0.03 |            -0.00 |         -0.02 |          -0.00 |        -0.04 |         0.01 |        -0.01 |         -0.06 |      -0.01 |
| pocket_pivot      |             -0.02 |            -0.02 |         -0.01 |           0.01 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.01 |
| stage2            |             -0.07 |            -0.07 |         -0.06 |          -0.02 |        -0.08 |        -0.02 |        -0.05 |         -0.10 |      -0.05 |
| undercut          |              0.18 |             0.16 |          0.02 |           0.08 |         0.13 |         0.09 |         0.09 |         -0.00 |       0.03 |
| vcp               |              0.06 |             0.04 |          0.04 |           0.10 |         0.05 |         0.07 |         0.06 |         -0.05 |       0.04 |

Same, in-sample:

| entry             |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |
|:------------------|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|
| base_25           |             -0.02 |            -0.04 |          0.00 |           0.07 |        -0.06 |         0.06 |         0.03 |          0.04 |       0.09 |
| base_50           |              0.01 |            -0.00 |          0.04 |           0.13 |        -0.03 |         0.08 |         0.06 |         -0.02 |       0.09 |
| donchian_20       |              0.11 |             0.11 |          0.14 |           0.15 |         0.09 |         0.10 |         0.11 |          0.12 |       0.17 |
| donchian_55       |              0.08 |             0.09 |          0.12 |           0.13 |         0.07 |         0.08 |         0.09 |          0.11 |       0.16 |
| ema_retest        |              0.09 |             0.09 |          0.13 |           0.12 |         0.15 |         0.06 |         0.07 |          0.15 |       0.13 |
| ep_gap10          |              0.16 |             0.10 |          0.15 |           0.11 |        -0.05 |         0.13 |         0.10 |          0.18 |       0.22 |
| ep_gap5           |              0.17 |             0.13 |          0.17 |           0.15 |         0.08 |         0.14 |         0.13 |          0.25 |       0.23 |
| ep_gap8_neglected |              0.27 |             0.22 |          0.25 |           0.19 |         0.20 |         0.16 |         0.19 |          0.32 |       0.29 |
| flag_30           |             -0.09 |            -0.10 |         -0.05 |           0.05 |        -0.11 |         0.02 |        -0.03 |         -0.09 |       0.01 |
| flag_30_early     |              0.12 |             0.10 |          0.13 |           0.07 |        -0.02 |         0.07 |         0.11 |          0.02 |       0.05 |
| flag_60           |              0.04 |             0.02 |          0.08 |           0.12 |        -0.02 |         0.14 |         0.09 |          0.07 |       0.11 |
| high52            |             -0.03 |            -0.04 |          0.01 |           0.02 |        -0.03 |        -0.02 |        -0.02 |         -0.03 |       0.00 |
| high52_fresh      |              0.07 |             0.07 |          0.10 |           0.08 |         0.08 |         0.04 |         0.05 |          0.08 |       0.09 |
| htf               |             -0.08 |             0.24 |          0.13 |           0.06 |        -0.10 |         0.12 |         0.18 |          0.42 |       0.27 |
| multi_touch       |              0.07 |             0.09 |          0.12 |           0.10 |         0.10 |         0.06 |         0.06 |          0.12 |       0.11 |
| pocket_pivot      |              0.05 |             0.06 |          0.07 |           0.03 |         0.04 |         0.03 |         0.03 |          0.07 |       0.04 |
| stage2            |              0.11 |             0.13 |          0.16 |           0.12 |         0.16 |         0.07 |         0.09 |          0.15 |       0.14 |
| undercut          |              0.21 |             0.23 |          0.05 |           0.13 |         0.20 |         0.18 |         0.17 |          0.01 |       0.08 |
| vcp               |              0.07 |             0.08 |          0.12 |           0.13 |         0.10 |         0.10 |         0.09 |          0.09 |       0.17 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| sma50_close     |      0.07 |       0.08 |      0.24 |     1.12 |                       0.63 |
| oneil_20_8      |      0.12 |       0.01 |      0.24 |     1.02 |                       0.74 |
| trim_ema        |     -0.01 |       0.00 |      0.34 |     1.01 |                       0.74 |
| donchian_10low  |      0.01 |      -0.01 |      0.27 |     1.00 |                       0.74 |
| chandelier_3atr |      0.01 |      -0.02 |      0.27 |     0.98 |                       0.74 |
| ema21_close     |     -0.04 |      -0.03 |      0.29 |     0.96 |                       0.74 |
| fixed_3r_20d    |     -0.01 |      -0.03 |      0.35 |     0.97 |                       0.79 |
| qull_sma20      |     -0.05 |      -0.04 |      0.41 |     0.93 |                       0.74 |
| qull_sma10      |     -0.06 |      -0.05 |      0.41 |     0.92 |                       0.89 |

## 7. Filters (averaged over all entry x exit combinations)

| filter      |   IS_avgR |   OOS_avgR |   OOS_win |
|:------------|----------:|-----------:|----------:|
| rs80_early  |      0.04 |       0.12 |      0.34 |
| early_stage |      0.03 |       0.06 |      0.33 |
| rs80        |      0.01 |       0.04 |      0.33 |
| rs80_mkt    |      0.02 |       0.03 |      0.32 |
| mkt_ok      |      0.00 |      -0.01 |      0.31 |
| all         |      0.00 |      -0.01 |      0.31 |

## 8. ML meta-labeling (exit: oneil_20_8, chosen in-sample; walk-forward, yearly retrain)

Out-of-sample AUC: 0.615 (0.5 = no skill). Taken (model's top third, causal threshold): n=99,721, avgR=0.032, win=0.301. Skipped: n=186,785, avgR=-0.014, win=0.190.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 28651.00 |  -0.12 |  0.10 |
|      1 | 28651.00 |  -0.01 |  0.13 |
|      2 | 28650.00 |  -0.00 |  0.16 |
|      3 | 28651.00 |   0.01 |  0.21 |
|      4 | 28651.00 |   0.03 |  0.24 |
|      5 | 28650.00 |   0.00 |  0.26 |
|      6 | 28650.00 |   0.03 |  0.28 |
|      7 | 28651.00 |   0.04 |  0.29 |
|      8 | 28650.00 |   0.04 |  0.30 |
|      9 | 28651.00 |  -0.00 |  0.31 |

Per entry (OOS):

| entry_name        |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:------------------|---------:|-----------:|----------:|-------------:|---------------:|
| flag_60           |   616.00 |       0.07 |    151.00 |         0.14 |           0.04 |
| ep_gap8_neglected |   934.00 |       0.14 |    548.00 |         0.10 |           0.20 |
| ep_gap5           |  2322.00 |       0.05 |   1326.00 |         0.09 |           0.01 |
| flag_30_early     |  1953.00 |       0.17 |    256.00 |         0.08 |           0.18 |
| undercut          | 26315.00 |       0.08 |   4011.00 |         0.06 |           0.09 |
| ep_gap10          |   933.00 |       0.11 |    543.00 |         0.06 |           0.18 |
| flag_30           |  1790.00 |      -0.01 |    398.00 |         0.06 |          -0.03 |
| donchian_20       | 78107.00 |       0.04 |  47208.00 |         0.05 |           0.03 |
| base_50           |  2664.00 |       0.07 |    983.00 |         0.04 |           0.09 |
| ema_retest        | 15673.00 |       0.04 |   3856.00 |         0.04 |           0.04 |
| base_25           |  2441.00 |       0.05 |    900.00 |         0.04 |           0.06 |
| donchian_55       | 50716.00 |       0.02 |  27552.00 |         0.02 |           0.01 |
| high52            | 29116.00 |      -0.08 |   3068.00 |        -0.00 |          -0.09 |
| vcp               |   880.00 |       0.00 |    775.00 |        -0.01 |           0.08 |
| pocket_pivot      | 48059.00 |      -0.07 |   2344.00 |        -0.03 |          -0.07 |
| multi_touch       | 10634.00 |      -0.08 |   2578.00 |        -0.04 |          -0.10 |
| high52_fresh      |  8413.00 |       0.01 |   1581.00 |        -0.07 |           0.02 |
| stage2            |  4842.00 |      -0.12 |   1618.00 |        -0.11 |          -0.13 |
| htf               |    98.00 |      -0.21 |     25.00 |        -0.35 |          -0.17 |

What the model relies on (permutation importance, OOS AUC drop):

| feature           |   auc_drop |
|:------------------|-----------:|
| risk_adr          |     0.0750 |
| risk_pct          |     0.0168 |
| mkt_ret_21        |     0.0114 |
| qqq_ret_21        |     0.0100 |
| rs_rank           |     0.0034 |
| above_52w_low     |     0.0033 |
| sma200_slope      |     0.0020 |
| mkt_ema_stack     |     0.0019 |
| atr_pct           |     0.0018 |
| gap               |     0.0015 |
| rates_rising      |     0.0014 |
| leg3_range        |     0.0010 |
| breadth_50        |     0.0009 |
| down_candle_exp_5 |     0.0007 |
| tight_10          |     0.0006 |
| mkt_above200      |     0.0005 |
| mkt_ok            |     0.0004 |
| leg1_range        |     0.0004 |
| dist_52w_high     |     0.0004 |
| close_std_10      |     0.0004 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                             |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:-----------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| risk_adr <= 0.64 AND breadth_50 <= 0.523 AND vol_ratio <= 1.11   |   2853 |      0.94 |    4576 |       0.06 |      0.10 |
| risk_adr > 0.64 AND rates_rising > 0.5 AND mkt_ema_stack <= 0.5  |  21228 |      0.60 |   34126 |       0.12 |      0.29 |
| risk_adr <= 0.64 AND breadth_50 <= 0.523 AND vol_ratio > 1.11    |   4134 |      0.26 |    5477 |       0.10 |      0.11 |
| risk_adr > 0.64 AND rates_rising > 0.5 AND mkt_ema_stack > 0.5   | 101104 |      0.24 |   74355 |      -0.08 |      0.22 |
| risk_adr > 0.64 AND rates_rising <= 0.5 AND qqq_ret_21 <= 0.0299 |  56194 |      0.15 |   68556 |       0.06 |      0.26 |
| risk_adr <= 0.64 AND breadth_50 > 0.523 AND leg3_range > 0.117   |   9964 |      0.06 |   14647 |      -0.03 |      0.11 |
| risk_adr <= 0.64 AND breadth_50 > 0.523 AND leg3_range <= 0.117  |  20257 |     -0.05 |   16240 |      -0.15 |      0.08 |
| risk_adr > 0.64 AND rates_rising <= 0.5 AND qqq_ret_21 > 0.0299  |  57264 |     -0.13 |   68529 |       0.00 |      0.25 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                             |   CAGR |   max_DD_realized |   trades |    win |   avg_positions |
|:-------------------------------------|-------:|------------------:|---------:|-------:|----------------:|
| donchian_20 / all / oneil_20_8       |   0.09 |             -0.30 |  1058.00 |   0.32 |            9.01 |
| donchian_55 / all / oneil_20_8       |  -0.02 |             -0.49 |  1063.00 |   0.28 |            8.74 |
| undercut / all / oneil_20_8          |   0.08 |             -0.48 |  1406.00 |   0.18 |            7.44 |
| ema_retest / all / oneil_20_8        |   0.01 |             -0.45 |   874.00 |   0.25 |            7.18 |
| pocket_pivot / all / oneil_20_8      |   0.12 |             -0.28 |  1374.00 |   0.18 |            6.67 |
| ML-selected, all setups / oneil_20_8 |   0.02 |             -0.31 |   816.00 |   0.34 |            9.05 |
| All setups, no ML / oneil_20_8       |   0.21 |             -0.42 |  1636.00 |   0.27 |            8.77 |
| BASELINE random entries / oneil_20_8 |   0.04 |             -0.49 |  1713.00 |   0.15 |            6.36 |
| SPY buy & hold                       |   0.15 |             -0.34 |   nan    | nan    |          nan    |

Equity is marked on closed trades only, so drawdowns are understated vs. daily mark-to-market.

## Appendix: entries and exits

| entry             | source / rule                                                    |   signals |
|:------------------|:-----------------------------------------------------------------|----------:|
| donchian_20       | Turtle 20-day breakout / trading-range break (Brock et al. 1992) |    148884 |
| donchian_55       | Turtle 55-day breakout                                           |     99224 |
| high52            | 52-week-high breakout (George & Hwang 2004)                      |     59819 |
| high52_fresh      | 52-week high after >= 20 days of consolidation                   |     16710 |
| base_25           | O'Neil/Darvas 5-week base breakout                               |      4374 |
| base_50           | O'Neil 10-week base breakout                                     |      4965 |
| vcp               | Minervini volatility contraction pattern                         |      2216 |
| flag_30           | Qullamaggie flag after a 30%+ move                               |      2953 |
| flag_60           | Qullamaggie flag after a 60%+ move                               |       953 |
| flag_30_early     | Qullamaggie flag, early entry inside the flag                    |      3170 |
| htf               | High tight flag (O'Neil / Bulkowski)                             |       151 |
| ep_gap5           | Gap up >= 5% on 3x volume                                        |      4214 |
| ep_gap10          | Episodic pivot: gap >= 10% on 3x volume                          |      1478 |
| ep_gap8_neglected | Episodic pivot from neglect (Qullamaggie)                        |      1553 |
| pocket_pivot      | Morales & Kacher pocket pivot                                    |     97988 |
| stage2            | Weinstein stage 2 breakout                                       |     10965 |
| ema_retest        | 8/21 EMA cross -> break -> retest (your playbook)                |     30399 |
| multi_touch       | Multi-touch level breakout on volume (your playbook)             |     23449 |
| undercut          | Undercut & rally (your playbook)                                 |     49712 |
| random_uptrend    | BASELINE: random entries in an uptrend                           |     65482 |

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