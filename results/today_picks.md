# Daily picks — 2026-10-09

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 532,162 past snapshots of 1488 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.7% net per trade; break-even ~33%). +10% before -10%: 50% vs 49% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days       | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:-------------------------|:-----------------------|
| FORM     |  139.67 |   37.10 |   53.30 |      125.70 |        153.64 |        167.60 |      4.90 |     98.30 |          -12.90 |         1.00 |                          | Information Technology |
| NSIT     |  163.61 |   37.10 |   52.80 |      147.25 |        179.97 |        196.33 |      3.50 |     96.60 |           -2.90 |         2.00 |                          | Industrials            |
| AZTA     |   37.72 |   37.10 |   52.20 |       33.95 |         41.49 |         45.26 |      5.90 |     93.00 |          -18.70 |         1.00 |                          | Health Care            |
| P        |  154.49 |   37.10 |   53.10 |      139.04 |        169.94 |        185.39 |      5.20 |     99.00 |           -1.60 |         2.00 |                          | Information Technology |
| ONTO     |  294.53 |   35.60 |   53.30 |      265.08 |        323.98 |        353.44 |      4.30 |     91.00 |          -23.80 |         1.00 |                          | Information Technology |
| DAVE     |  368.42 |   35.60 |   51.10 |      331.58 |        405.26 |        442.10 |      5.80 |     94.60 |          -19.60 |         2.00 |                          | Financials             |
| ANF      |  142.58 |   35.60 |   49.70 |      128.32 |        156.84 |        171.10 |      3.70 |     96.40 |           -8.10 |         2.00 |                          | Consumer Discretionary |
| RXO      |   29.08 |   35.60 |   53.30 |       26.17 |         31.99 |         34.90 |      4.80 |     93.60 |           -2.70 |         1.00 | wf_rocket_gap            | Industrials            |
| BE       |  280.50 |   35.60 |   52.20 |      252.45 |        308.55 |        336.60 |      6.40 |     98.30 |          -20.10 |         2.00 |                          | Industrials            |
| MU       | 1029.00 |   35.60 |   52.60 |      926.10 |       1131.90 |       1234.80 |      3.90 |     99.70 |          -18.00 |         7.00 |                          | Information Technology |
| VIAV     |   45.46 |   35.60 |   53.30 |       40.91 |         50.01 |         54.55 |      5.80 |     97.60 |          -24.80 |         1.00 |                          | Information Technology |
| PENG     |   76.28 |   35.60 |   49.80 |       68.65 |         83.91 |         91.54 |      6.50 |     99.50 |          -15.10 |         2.00 | donchian_55, base_50     | Information Technology |
| MTRN     |  280.45 |   35.60 |   50.80 |      252.41 |        308.50 |        336.54 |      4.50 |     96.40 |          -13.70 |         7.00 |                          | Materials              |
| CAKE     |  108.45 |   35.60 |   52.80 |       97.60 |        119.29 |        130.14 |      3.30 |     96.80 |           -8.50 |         2.00 |                          | Consumer Discretionary |
| TER      |  402.68 |   35.60 |   52.60 |      362.41 |        442.95 |        483.22 |      4.30 |     96.60 |          -17.40 |        10.00 |                          | Information Technology |
| PDFS     |   54.40 |   35.60 |   53.30 |       48.96 |         59.84 |         65.28 |      4.30 |     93.80 |          -24.10 |         1.00 |                          | Information Technology |
| DDOG     |  293.26 |   35.60 |   50.40 |      263.93 |        322.59 |        351.91 |      4.50 |     97.60 |           -0.30 |         3.00 |                          | Information Technology |
| CVI      |   58.02 |   35.60 |   53.30 |       52.22 |         63.82 |         69.62 |      5.40 |     97.00 |           -5.00 |         3.00 |                          | Energy                 |
| QLYS     |  202.42 |   35.60 |   53.10 |      182.18 |        222.66 |        242.90 |      5.30 |     97.40 |           -1.00 |         3.00 |                          | Information Technology |
| PAYC     |  232.22 |   35.60 |   49.70 |      209.00 |        255.44 |        278.66 |      3.10 |     96.10 |           -5.20 |         0.00 |                          | Industrials            |
| ENTG     |  165.79 |   35.60 |   53.90 |      149.21 |        182.37 |        198.95 |      3.80 |     91.60 |          -11.20 |         2.00 |                          | Information Technology |
| FIVN     |   36.40 |   35.60 |   53.10 |       32.76 |         40.04 |         43.68 |      6.10 |     97.80 |           -9.00 |         3.00 | wf_scan_pullback         | Information Technology |
| SDGR     |   27.28 |   35.60 |   50.40 |       24.55 |         30.01 |         32.74 |      9.30 |     97.20 |          -19.20 |         2.00 |                          | Health Care            |
| CRSR     |   13.63 |   35.60 |   52.80 |       12.27 |         14.99 |         16.36 |      4.10 |     97.40 |           -9.00 |         2.00 |                          | Information Technology |
| PANW     |  418.78 |   35.60 |   52.60 |      376.90 |        460.66 |        502.54 |      4.50 |     98.00 |           -3.10 |         3.00 |                          | Information Technology |
| CRWD     |  275.04 |   35.60 |   53.10 |      247.54 |        302.54 |        330.05 |      4.70 |     99.20 |           -4.20 |         3.00 |                          | Information Technology |
| DOCU     |   71.08 |   35.60 |   53.90 |       63.97 |         78.19 |         85.30 |      3.80 |     90.90 |           -5.20 |         1.00 |                          | Information Technology |
| PLTR     |  209.05 |   35.60 |   50.80 |      188.15 |        229.96 |        250.86 |      3.30 |     94.00 |           -0.30 |         4.00 | donchian_20, donchian_55 | Information Technology |
| CLF      |   12.98 |   35.40 |   52.20 |       11.68 |         14.28 |         15.58 |      5.10 |     84.10 |          -22.30 |         0.00 |                          | Materials              |
| MTSI     |  330.06 |   35.40 |   52.60 |      297.05 |        363.07 |        396.07 |      4.70 |     95.80 |          -21.20 |         1.00 |                          | Information Technology |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:-----------------------|
| OI       |    6.08 |   37.10 |   50.00 |        5.47 |          6.69 |          7.30 |      4.10 |      1.00 |          -64.00 |         0.00 |                      | Materials              |
| MTZ      |  212.65 |   37.10 |   50.00 |      191.38 |        233.91 |        255.18 |      4.80 |      3.60 |          -51.80 |         0.00 |                      | Industrials            |
| SEDG     |   32.21 |   37.10 |   50.00 |       28.99 |         35.43 |         38.65 |      6.20 |      6.50 |          -60.40 |         0.00 |                      | Information Technology |
| ICHR     |   59.91 |   37.10 |   53.30 |       53.92 |         65.90 |         71.89 |      4.70 |     94.30 |          -47.30 |         0.00 |                      | Information Technology |
| PZZA     |   19.75 |   37.10 |   50.00 |       17.78 |         21.73 |         23.70 |      3.50 |      0.60 |          -63.20 |         0.00 |                      | Consumer Discretionary |
| MP       |   46.14 |   37.10 |   48.40 |       41.53 |         50.75 |         55.37 |      4.10 |     11.80 |          -54.00 |         0.00 |                      | Materials              |
| MKSI     |  264.50 |   37.10 |   49.70 |      238.05 |        290.95 |        317.40 |      3.70 |     78.80 |          -40.90 |         0.00 |                      | Information Technology |
| AMKR     |   49.12 |   37.10 |   49.70 |       44.21 |         54.03 |         58.94 |      4.30 |     53.70 |          -49.10 |         0.00 |                      | Information Technology |
| MARA     |    9.65 |   37.10 |   52.20 |        8.68 |         10.61 |         11.58 |      6.70 |      7.20 |          -58.80 |         0.00 |                      | Information Technology |
| LBRT     |   19.00 |   37.10 |   50.00 |       17.10 |         20.90 |         22.80 |      4.70 |     34.50 |          -44.50 |         0.00 |                      | Energy                 |
| WDC      |  397.28 |   37.10 |   52.20 |      357.55 |        437.01 |        476.74 |      5.00 |     96.30 |          -50.30 |         0.00 |                      | Information Technology |
| CENX     |   36.76 |   37.10 |   50.00 |       33.08 |         40.44 |         44.11 |      3.50 |     14.50 |          -47.80 |         0.00 |                      | Materials              |
| HL       |   17.07 |   37.10 |   50.00 |       15.36 |         18.78 |         20.48 |      3.90 |     65.30 |          -50.00 |         0.00 |                      | Materials              |
| AOSL     |   27.87 |   37.10 |   52.20 |       25.08 |         30.66 |         33.44 |      4.40 |     31.50 |          -48.70 |         0.00 |                      | Information Technology |
| ARWR     |   62.75 |   37.10 |   48.40 |       56.48 |         69.03 |         75.30 |      5.00 |     71.40 |          -34.30 |         0.00 |                      | Health Care            |
| FORM     |  139.67 |   37.10 |   53.30 |      125.70 |        153.64 |        167.60 |      4.90 |     98.30 |          -12.90 |         1.00 |                      | Information Technology |
| NSIT     |  163.61 |   37.10 |   52.80 |      147.25 |        179.97 |        196.33 |      3.50 |     96.60 |           -2.90 |         2.00 |                      | Industrials            |
| AZTA     |   37.72 |   37.10 |   52.20 |       33.95 |         41.49 |         45.26 |      5.90 |     93.00 |          -18.70 |         1.00 |                      | Health Care            |
| P        |  154.49 |   37.10 |   53.10 |      139.04 |        169.94 |        185.39 |      5.20 |     99.00 |           -1.60 |         2.00 |                      | Information Technology |
| UTI      |   20.64 |   35.60 |   50.00 |       18.58 |         22.70 |         24.77 |      5.00 |      0.70 |          -59.80 |         0.00 |                      | Consumer Discretionary |
| RUN      |    7.64 |   35.60 |   50.00 |        6.88 |          8.40 |          9.17 |      4.40 |      0.40 |          -66.00 |         0.00 |                      | Industrials            |
| HUBS     |  228.30 |   35.60 |   48.40 |      205.47 |        251.13 |        273.96 |      5.60 |     27.30 |          -54.20 |         0.00 |                      | Information Technology |
| CC       |   13.61 |   35.60 |   48.40 |       12.25 |         14.97 |         16.33 |      3.20 |      7.10 |          -52.10 |         0.00 |                      | Materials              |
| AHCO     |    6.06 |   35.60 |   50.00 |        5.45 |          6.67 |          7.27 |      4.00 |      1.10 |          -54.90 |         0.00 |                      | Health Care            |
| NWL      |    5.64 |   35.60 |   49.70 |        5.08 |          6.20 |          6.77 |      3.80 |     84.70 |          -20.00 |         2.00 |                      | Consumer Discretionary |
| ALHC     |    7.55 |   35.60 |   50.00 |        6.79 |          8.30 |          9.05 |      9.40 |      0.10 |          -70.00 |         0.00 |                      | Health Care            |
| ADMA     |   10.36 |   35.60 |   49.70 |        9.32 |         11.40 |         12.43 |      4.40 |     43.90 |          -49.40 |         0.00 |                      | Health Care            |
| GLW      |  156.68 |   35.60 |   49.70 |      141.01 |        172.35 |        188.02 |      4.60 |     75.70 |          -42.20 |         0.00 |                      | Information Technology |
| TTMI     |  121.01 |   35.60 |   52.80 |      108.91 |        133.11 |        145.21 |      5.80 |     86.30 |          -45.90 |         0.00 |                      | Information Technology |
| PSN      |   45.08 |   35.60 |   50.00 |       40.57 |         49.59 |         54.10 |      3.70 |      4.40 |          -49.60 |         0.00 |                      | Industrials            |