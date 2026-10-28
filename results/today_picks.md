# Daily picks — 2026-10-27

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 542,140 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 35% (avg +1.3% net per trade; break-even ~33%). +10% before -10%: 50% vs 50% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                                         | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:-----------------------------------------------------------|:-----------------------|
| WS       |   42.71 |   35.60 |   51.40 |       38.44 |         46.98 |         51.25 |      5.30 |     87.00 |          -12.00 |         0.00 | donchian_55, pocket_pivot                                  | Materials              |
| TALO     |   18.19 |   34.90 |   49.40 |       16.37 |         20.01 |         21.83 |      3.60 |     97.80 |           -3.00 |        10.00 | pocket_pivot, rising_wedge, qull_breakout                  | Energy                 |
| XNCR     |   29.99 |   34.30 |   51.40 |       26.99 |         32.99 |         35.99 |      6.40 |    100.00 |          -10.70 |         2.00 | donchian_20, multi_touch                                   | Health Care            |
| ZD       |   57.03 |   33.30 |   53.10 |       51.33 |         62.73 |         68.44 |      2.60 |     84.80 |           -5.70 |         6.00 |                                                            | Communication Services |
| AMG      |  391.99 |   27.80 |   50.20 |      352.79 |        431.19 |        470.39 |      2.90 |     91.30 |           -1.80 |         7.00 |                                                            | nan                    |
| XHR      |   20.27 |   26.30 |   51.40 |       18.24 |         22.30 |         24.32 |      2.40 |     89.10 |           -7.40 |         7.00 |                                                            | Real Estate            |
| WKC      |   36.38 |   22.10 |   50.00 |       32.74 |         40.02 |         43.66 |      2.20 |     80.40 |          -11.10 |         4.00 |                                                            | Energy                 |
| SXT      |  131.89 |   19.90 |   50.00 |      118.70 |        145.08 |        158.27 |      2.40 |     73.90 |           -5.00 |         3.00 |                                                            | Materials              |
| SCL      |   65.21 |   13.70 |   50.90 |       58.69 |         71.73 |         78.25 |      2.30 |     82.60 |           -2.00 |         3.00 |                                                            | Materials              |
| STBA     |   50.59 |    9.70 |   50.90 |       45.53 |         55.65 |         60.71 |      2.00 |     71.70 |           -4.70 |         7.00 |                                                            | Financials             |
| WSFS     |   78.85 |    9.70 |   50.90 |       70.96 |         86.73 |         94.62 |      1.80 |     76.10 |           -4.70 |         5.00 | donchian_20, desc_triangle, wf_scan_pullback, wf_scan_base | Financials             |
| CNO      |   54.44 |    6.60 |   49.80 |       49.00 |         59.88 |         65.33 |      1.70 |     78.30 |           -5.20 |         5.00 |                                                            | Financials             |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                        | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------------|:-----------------------|
| WRBY     |   25.07 |   36.10 |   53.10 |       22.56 |         27.58 |         30.08 |      5.20 |     60.90 |          -19.10 |         0.00 |                                           | Consumer Discretionary |
| YELP     |   18.75 |   35.60 |   51.40 |       16.88 |         20.62 |         22.50 |      4.50 |      6.50 |          -45.60 |         0.00 |                                           | Communication Services |
| UPWK     |    9.07 |   35.60 |   53.10 |        8.16 |          9.98 |         10.88 |      3.50 |     19.60 |          -60.30 |         0.00 |                                           | Industrials            |
| YOU      |   45.53 |   35.60 |   51.30 |       40.98 |         50.08 |         54.64 |      3.10 |     43.50 |          -33.90 |         0.00 |                                           | Information Technology |
| WRLD     |  169.83 |   35.60 |   50.20 |      152.85 |        186.81 |        203.80 |      3.20 |     54.30 |          -25.40 |         2.00 |                                           | Financials             |
| WS       |   42.71 |   35.60 |   51.40 |       38.44 |         46.98 |         51.25 |      5.30 |     87.00 |          -12.00 |         0.00 | donchian_55, pocket_pivot                 | Materials              |
| XPEL     |   42.91 |   34.90 |   53.10 |       38.62 |         47.20 |         51.49 |      2.90 |     47.80 |          -23.30 |         0.00 |                                           | Consumer Discretionary |
| WINA     |  281.00 |   34.90 |   52.20 |      252.90 |        309.10 |        337.20 |      4.00 |     13.00 |          -42.10 |         0.00 |                                           | Consumer Discretionary |
| WT       |   21.23 |   34.90 |   49.40 |       19.11 |         23.35 |         25.48 |      3.60 |     95.70 |          -18.10 |         5.00 |                                           | Financials             |
| SRPT     |   18.89 |   34.90 |   52.20 |       17.00 |         20.78 |         22.67 |      5.00 |     41.30 |          -23.50 |         0.00 |                                           | Health Care            |
| TALO     |   18.19 |   34.90 |   49.40 |       16.37 |         20.01 |         21.83 |      3.60 |     97.80 |           -3.00 |        10.00 | pocket_pivot, rising_wedge, qull_breakout | Energy                 |
| XNCR     |   29.99 |   34.30 |   51.40 |       26.99 |         32.99 |         35.99 |      6.40 |    100.00 |          -10.70 |         2.00 | donchian_20, multi_touch                  | Health Care            |
| WSC      |   17.65 |   33.30 |   52.20 |       15.88 |         19.41 |         21.18 |      4.40 |     10.90 |          -40.50 |         0.00 |                                           | Industrials            |
| TPC      |   80.81 |   33.30 |   53.10 |       72.73 |         88.89 |         96.97 |      3.40 |     52.20 |          -20.90 |         0.00 |                                           | Industrials            |
| ZD       |   57.03 |   33.30 |   53.10 |       51.33 |         62.73 |         68.44 |      2.60 |     84.80 |           -5.70 |         6.00 |                                           | Communication Services |
| WWW      |   19.70 |   33.30 |   51.40 |       17.73 |         21.67 |         23.64 |      3.70 |     32.60 |          -23.00 |         3.00 |                                           | Consumer Discretionary |
| WHD      |   65.56 |   33.30 |   50.20 |       59.00 |         72.12 |         78.67 |      3.30 |     93.50 |          -11.30 |         1.00 | wf_scan_pullback                          | Energy                 |
| TNC      |   66.02 |   33.00 |   50.70 |       59.42 |         72.62 |         79.22 |      2.80 |     17.40 |          -27.90 |         0.00 |                                           | Industrials            |
| SNDR     |   31.11 |   29.40 |   51.40 |       28.00 |         34.22 |         37.33 |      2.80 |     58.70 |          -20.50 |         0.00 |                                           | Industrials            |
| AMG      |  391.99 |   27.80 |   50.20 |      352.79 |        431.19 |        470.39 |      2.90 |     91.30 |           -1.80 |         7.00 |                                           | nan                    |
| UVV      |   39.56 |   27.80 |   51.40 |       35.60 |         43.52 |         47.47 |      2.50 |      8.70 |          -29.90 |         0.00 |                                           | Consumer Staples       |
| VRTS     |  121.06 |   27.40 |   50.20 |      108.95 |        133.17 |        145.27 |      3.10 |     15.20 |          -29.60 |         0.00 |                                           | Financials             |
| VTOL     |   40.97 |   26.30 |   50.60 |       36.87 |         45.07 |         49.16 |      3.50 |     28.30 |          -18.20 |         0.00 |                                           | Energy                 |
| XHR      |   20.27 |   26.30 |   51.40 |       18.24 |         22.30 |         24.32 |      2.40 |     89.10 |           -7.40 |         7.00 |                                           | Real Estate            |
| WOR      |   63.40 |   23.60 |   50.20 |       57.06 |         69.74 |         76.08 |      2.30 |     69.60 |           -6.10 |         0.00 |                                           | Industrials            |
| WKC      |   36.38 |   22.10 |   50.00 |       32.74 |         40.02 |         43.66 |      2.20 |     80.40 |          -11.10 |         4.00 |                                           | Energy                 |
| SXT      |  131.89 |   19.90 |   50.00 |      118.70 |        145.08 |        158.27 |      2.40 |     73.90 |           -5.00 |         3.00 |                                           | Materials              |
| GHC      | 1186.71 |   18.50 |   49.40 |     1068.04 |       1305.38 |       1424.05 |      2.20 |     50.00 |           -5.80 |         1.00 |                                           | nan                    |
| ZWS      |   49.15 |   16.00 |   50.60 |       44.24 |         54.07 |         58.98 |      2.60 |     39.10 |          -10.40 |         1.00 |                                           | Industrials            |
| WSBC     |   38.75 |   13.70 |   48.80 |       34.88 |         42.62 |         46.50 |      2.00 |     63.00 |           -9.10 |         5.00 |                                           | Financials             |