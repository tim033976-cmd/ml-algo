# Daily picks — 2026-10-14

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 540,663 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.6% net per trade; break-even ~33%). +10% before -10%: 50% vs 49% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                                               | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:-----------------------------------------------------------------|:-----------------------|
| EZPW     |   32.72 |   37.00 |   50.80 |       29.45 |         35.99 |         39.26 |      3.50 |     87.60 |          -11.90 |         8.00 |                                                                  | Financials             |
| FDS      |  289.74 |   37.00 |   50.80 |      260.77 |        318.71 |        347.69 |      3.80 |     73.10 |           -9.60 |         2.00 |                                                                  | Financials             |
| ACHC     |   31.67 |   37.00 |   52.20 |       28.50 |         34.84 |         38.00 |      4.10 |     72.10 |          -11.60 |         3.00 | donchian_20                                                      | Health Care            |
| CVLT     |  154.33 |   37.00 |   50.50 |      138.90 |        169.76 |        185.20 |      3.80 |     78.60 |          -13.20 |         1.00 |                                                                  | Information Technology |
| AVT      |   95.85 |   37.00 |   52.80 |       86.26 |        105.43 |        115.02 |      3.60 |     95.30 |          -11.80 |         3.00 | wf_scan_pullback                                                 | Information Technology |
| KSS      |   21.15 |   37.00 |   52.50 |       19.03 |         23.26 |         25.38 |      5.00 |     93.30 |          -13.60 |         1.00 | donchian_55                                                      | nan                    |
| ROG      |  139.72 |   37.00 |   52.80 |      125.75 |        153.69 |        167.66 |      4.20 |     88.90 |          -17.30 |        10.00 |                                                                  | Information Technology |
| SMTC     |  160.26 |   37.00 |   50.50 |      144.23 |        176.29 |        192.31 |      6.20 |     98.20 |          -20.70 |        11.00 |                                                                  | Information Technology |
| TGTX     |   54.37 |   37.00 |   52.80 |       48.93 |         59.81 |         65.24 |      3.80 |     92.30 |           -8.30 |         2.00 |                                                                  | Health Care            |
| CRL      |  302.00 |   37.00 |   52.20 |      271.80 |        332.20 |        362.40 |      4.00 |     97.00 |           -9.40 |         3.00 |                                                                  | Health Care            |
| NEOG     |   12.13 |   37.00 |   49.80 |       10.92 |         13.34 |         14.56 |      5.70 |     95.90 |          -14.90 |         6.00 |                                                                  | Health Care            |
| MUR      |   39.31 |   37.00 |   52.30 |       35.38 |         43.24 |         47.17 |      3.10 |     80.50 |           -7.60 |         1.00 | wf_scan_pullback                                                 | nan                    |
| GME      |   27.15 |   37.00 |   52.80 |       24.43 |         29.86 |         32.58 |      4.30 |     78.30 |           -3.80 |         1.00 | high52, high52_fresh                                             | nan                    |
| EL       |  101.59 |   37.00 |   51.50 |       91.43 |        111.75 |        121.91 |      3.20 |     84.90 |          -15.60 |         1.00 |                                                                  | Consumer Staples       |
| HALO     |  116.82 |   37.00 |   50.50 |      105.14 |        128.50 |        140.18 |      3.30 |     97.90 |           -2.00 |         2.00 |                                                                  | Health Care            |
| APA      |   47.37 |   37.00 |   51.70 |       42.63 |         52.11 |         56.84 |      3.00 |     97.30 |           -2.50 |         8.00 | donchian_20, donchian_55, high52                                 | Energy                 |
| MPC      |  484.92 |   37.00 |   50.50 |      436.43 |        533.41 |        581.90 |      3.90 |     99.70 |           -0.10 |         6.00 |                                                                  | Energy                 |
| VLO      |  459.78 |   37.00 |   50.50 |      413.80 |        505.76 |        551.74 |      4.30 |     99.60 |           -0.40 |        11.00 |                                                                  | Energy                 |
| CBRL     |   62.72 |   37.00 |   52.80 |       56.45 |         68.99 |         75.26 |      5.00 |     97.60 |            0.00 |         3.00 | donchian_55, high52, high52_fresh                                | Consumer Discretionary |
| MOH      |  209.19 |   37.00 |   52.50 |      188.27 |        230.11 |        251.03 |      3.90 |     71.30 |          -14.60 |         0.00 |                                                                  | nan                    |
| ECPG     |  100.86 |   37.00 |   51.10 |       90.77 |        110.95 |        121.03 |      3.20 |     96.40 |           -4.80 |        10.00 | donchian_20, donchian_55, high52, high52_fresh, wf_scan_pullback | Financials             |
| BBY      |   89.10 |   37.00 |   50.80 |       80.19 |         98.01 |        106.92 |      2.90 |     83.90 |           -7.70 |         2.00 |                                                                  | Consumer Discretionary |
| SCSC     |   60.56 |   37.00 |   52.30 |       54.50 |         66.62 |         72.67 |      3.00 |     93.40 |           -9.30 |         2.00 |                                                                  | Information Technology |
| DINO     |  127.69 |   37.00 |   51.70 |      114.92 |        140.46 |        153.23 |      4.10 |     99.50 |           -1.30 |        11.00 |                                                                  | Energy                 |
| SIG      |  107.96 |   37.00 |   52.50 |       97.16 |        118.76 |        129.55 |      3.30 |     77.10 |           -1.30 |         2.00 | donchian_20, donchian_55, wf_scan_base                           | nan                    |
| HUM      |  427.40 |   37.00 |   52.10 |      384.66 |        470.14 |        512.88 |      3.90 |     97.00 |           -6.40 |         2.00 |                                                                  | Health Care            |
| MANH     |  220.04 |   37.00 |   51.70 |      198.04 |        242.04 |        264.05 |      2.80 |     94.30 |           -3.10 |         2.00 | donchian_20, tight_coil_7, wf_scan_base, tc_supertrend_ema       | Information Technology |
| CAKE     |  112.85 |   35.10 |   50.20 |      101.56 |        124.13 |        135.42 |      3.00 |     98.40 |           -4.70 |         3.00 | donchian_20                                                      | Consumer Discretionary |
| ENTG     |  153.08 |   35.10 |   52.50 |      137.77 |        168.39 |        183.70 |      3.90 |     90.10 |          -18.00 |         2.00 |                                                                  | Information Technology |
| NSIT     |  166.01 |   35.10 |   51.50 |      149.41 |        182.61 |        199.21 |      3.70 |     98.00 |           -6.40 |         3.00 | donchian_20, donchian_55, high52                                 | Industrials            |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:-----------------------|
| DAN      |   27.98 |   37.00 |   51.10 |       25.18 |         30.78 |         33.58 |      3.60 |     72.00 |          -28.70 |         0.00 |                      | Consumer Discretionary |
| FIX      | 1541.68 |   37.00 |   50.20 |     1387.51 |       1695.85 |       1850.02 |      4.20 |     81.20 |          -25.60 |         0.00 |                      | Industrials            |
| NSP      |   49.58 |   37.00 |   50.20 |       44.62 |         54.54 |         59.50 |      4.00 |     90.50 |          -10.30 |         1.00 | wf_scan_pullback     | Industrials            |
| BJRI     |   59.55 |   37.00 |   50.80 |       53.59 |         65.50 |         71.46 |      3.50 |     94.90 |          -20.20 |         1.00 |                      | Consumer Discretionary |
| AEO      |   17.60 |   37.00 |   50.20 |       15.84 |         19.36 |         21.12 |      3.60 |     54.60 |          -36.50 |         0.00 |                      | Consumer Discretionary |
| ENS      |  173.45 |   37.00 |   50.20 |      156.10 |        190.79 |        208.14 |      2.90 |     63.00 |          -28.80 |         0.00 |                      | Industrials            |
| OLED     |   74.95 |   37.00 |   52.50 |       67.45 |         82.44 |         89.94 |      3.20 |      7.80 |          -50.10 |         0.00 |                      | Information Technology |
| ECHO     |   87.86 |   37.00 |   51.10 |       79.07 |         96.65 |        105.43 |      3.30 |     29.50 |          -40.30 |         0.00 |                      | Communication Services |
| WGO      |   23.09 |   37.00 |   50.20 |       20.78 |         25.40 |         27.71 |      3.20 |      7.50 |          -52.30 |         0.00 |                      | Consumer Discretionary |
| CROX     |  117.54 |   37.00 |   50.80 |      105.79 |        129.29 |        141.05 |      3.30 |     70.20 |          -16.80 |         4.00 |                      | Consumer Discretionary |
| WINA     |  297.97 |   37.00 |   50.20 |      268.17 |        327.77 |        357.56 |      3.50 |      7.30 |          -38.60 |         0.00 |                      | Consumer Discretionary |
| LSCC     |  115.00 |   37.00 |   52.30 |      103.50 |        126.50 |        138.00 |      4.00 |     78.50 |          -26.80 |         1.00 |                      | Information Technology |
| APTV     |   43.83 |   37.00 |   47.90 |       39.45 |         48.21 |         52.60 |      2.70 |      4.40 |          -50.70 |         0.00 |                      | Consumer Discretionary |
| PRIM     |   78.03 |   37.00 |   51.50 |       70.23 |         85.83 |         93.64 |      4.80 |      3.80 |          -62.00 |         0.00 |                      | Industrials            |
| MAN      |   51.96 |   37.00 |   50.80 |       46.76 |         57.16 |         62.35 |      4.10 |     92.80 |          -18.70 |         1.00 |                      | Industrials            |
| FN       |  392.95 |   37.00 |   52.10 |      353.66 |        432.25 |        471.54 |      5.40 |     13.90 |          -47.50 |         0.00 |                      | Information Technology |
| THO      |   65.47 |   37.00 |   50.80 |       58.92 |         72.02 |         78.56 |      3.30 |     11.40 |          -46.00 |         0.00 |                      | Consumer Discretionary |
| TPR      |  115.03 |   37.00 |   50.20 |      103.53 |        126.53 |        138.04 |      2.70 |     18.20 |          -29.90 |         0.00 |                      | Consumer Discretionary |
| EZPW     |   32.72 |   37.00 |   50.80 |       29.45 |         35.99 |         39.26 |      3.50 |     87.60 |          -11.90 |         8.00 |                      | Financials             |
| CE       |   45.82 |   37.00 |   51.10 |       41.24 |         50.40 |         54.98 |      3.90 |     34.80 |          -35.10 |         0.00 |                      | nan                    |
| NKTR     |   36.89 |   37.00 |   50.20 |       33.20 |         40.58 |         44.27 |      7.10 |      0.90 |          -66.20 |         0.00 |                      | nan                    |
| MPWR     | 1243.11 |   37.00 |   52.80 |     1118.80 |       1367.42 |       1491.73 |      3.90 |     55.40 |          -27.30 |         0.00 |                      | Information Technology |
| ORA      |   88.19 |   37.00 |   47.90 |       79.37 |         97.01 |        105.83 |      2.70 |     13.40 |          -39.70 |         0.00 |                      | Utilities              |
| DAR      |   62.38 |   37.00 |   50.20 |       56.14 |         68.62 |         74.86 |      3.70 |     92.90 |          -10.90 |         4.00 | wf_scan_pullback     | Consumer Staples       |
| DKS      |  136.96 |   37.00 |   50.20 |      123.26 |        150.66 |        164.35 |      3.10 |      2.20 |          -43.40 |         0.00 |                      | Consumer Discretionary |
| G        |   35.33 |   37.00 |   50.20 |       31.80 |         38.86 |         42.40 |      2.80 |     52.10 |          -26.20 |         0.00 |                      | Industrials            |
| DLX      |   22.68 |   37.00 |   50.80 |       20.41 |         24.95 |         27.22 |      2.70 |     41.10 |          -27.50 |         0.00 |                      | Industrials            |
| PMT      |    6.87 |   37.00 |   50.80 |        6.18 |          7.56 |          8.24 |      3.10 |      4.20 |          -43.60 |         0.00 |                      | Real Estate            |
| CF       |  119.46 |   37.00 |   50.80 |      107.51 |        131.41 |        143.35 |      3.30 |     70.90 |          -15.70 |         0.00 |                      | Materials              |
| DXPE     |  178.31 |   37.00 |   51.50 |      160.48 |        196.14 |        213.97 |      3.40 |     84.30 |          -14.30 |         5.00 |                      | Industrials            |