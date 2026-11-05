# Daily picks — 2026-11-04

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 541,787 past snapshots of 1535 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.6% net per trade; break-even ~33%). +10% before -10%: 50% vs 49% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                          | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:--------------------------------------------|:-----------------------|
| AZTA     |   39.14 |   34.70 |   51.40 |       35.23 |         43.05 |         46.97 |      5.80 |     97.20 |          -15.70 |         1.00 |                                             | Health Care            |
| SDGR     |   28.52 |   34.70 |   51.70 |       25.67 |         31.37 |         34.22 |      7.90 |     98.60 |          -15.60 |         2.00 |                                             | Health Care            |
| FIVN     |   36.35 |   34.30 |   51.70 |       32.71 |         39.98 |         43.62 |      6.00 |     95.80 |           -9.10 |         3.00 |                                             | Information Technology |
| EAT      |  220.44 |   34.30 |   50.50 |      198.40 |        242.48 |        264.53 |      5.20 |     96.00 |          -13.50 |         2.00 |                                             | Consumer Discretionary |
| GKOS     |  246.70 |   34.30 |   51.60 |      222.03 |        271.37 |        296.04 |      5.50 |     99.40 |           -3.30 |         2.00 |                                             | Health Care            |
| COCO     |   65.47 |   34.30 |   51.80 |       58.92 |         72.02 |         78.56 |      5.80 |     72.90 |          -23.70 |         0.00 |                                             | Consumer Staples       |
| XNCR     |   35.03 |   34.30 |   51.80 |       31.53 |         38.53 |         42.04 |      6.70 |     99.90 |           -0.10 |         2.00 | ema_retest, qull_breakout, qull_breakout_60 | Health Care            |
| MTW      |   23.20 |   32.70 |   50.50 |       20.88 |         25.52 |         27.84 |      4.30 |     99.30 |           -8.00 |         2.00 | pocket_pivot                                | nan                    |
| PD       |   17.00 |   32.70 |   51.50 |       15.30 |         18.70 |         20.40 |      3.80 |     98.50 |           -5.90 |         2.00 |                                             | nan                    |
| QLYS     |  210.89 |   32.70 |   51.40 |      189.80 |        231.98 |        253.07 |      5.70 |     98.40 |          -10.50 |         4.00 |                                             | Information Technology |
| SN       |  219.25 |   32.70 |   51.50 |      197.33 |        241.18 |        263.10 |      3.70 |     99.20 |           -2.40 |         4.00 |                                             | Consumer Discretionary |
| CRSR     |   13.32 |   32.70 |   51.40 |       11.99 |         14.65 |         15.98 |      5.40 |     97.30 |          -11.10 |         2.00 |                                             | Information Technology |
| DOCU     |   80.50 |   32.70 |   51.60 |       72.45 |         88.55 |         96.60 |      3.70 |     94.30 |           -6.30 |         2.00 |                                             | Information Technology |
| FTRE     |   20.83 |   32.70 |   51.50 |       18.75 |         22.91 |         25.00 |      6.10 |     96.30 |          -20.40 |         5.00 |                                             | Health Care            |
| CROX     |  159.84 |   32.70 |   51.50 |      143.86 |        175.82 |        191.81 |      3.60 |     97.00 |           -1.30 |         5.00 | wf_rocket_gap                               | Consumer Discretionary |
| YOU      |   59.08 |   32.70 |   51.70 |       53.17 |         64.99 |         70.90 |      4.60 |     90.50 |          -14.20 |         1.00 | donchian_20, donchian_55                    | Information Technology |
| PRGS     |   44.79 |   32.70 |   51.50 |       40.31 |         49.27 |         53.75 |      3.70 |     79.50 |           -5.20 |         1.00 |                                             | Information Technology |
| RGEN     |  178.20 |   32.70 |   51.70 |      160.38 |        196.02 |        213.84 |      5.00 |     80.80 |          -10.40 |         2.00 |                                             | Health Care            |
| HUM      |  417.42 |   32.70 |   51.80 |      375.68 |        459.16 |        500.90 |      3.80 |     94.70 |           -8.40 |         2.00 |                                             | Health Care            |
| RHI      |   44.95 |   32.70 |   50.50 |       40.46 |         49.45 |         53.94 |      5.00 |     97.60 |           -4.60 |         4.00 |                                             | nan                    |
| CRL      |  326.29 |   32.70 |   50.50 |      293.66 |        358.92 |        391.55 |      4.80 |     98.00 |          -14.10 |         4.00 |                                             | Health Care            |
| KSS      |   25.36 |   32.70 |   50.50 |       22.82 |         27.90 |         30.43 |      5.10 |     97.80 |           -0.30 |         1.00 | qull_breakout                               | nan                    |
| HRB      |   55.47 |   32.70 |   50.50 |       49.92 |         61.02 |         66.56 |      3.30 |     94.50 |           -4.60 |         3.00 |                                             | nan                    |
| BRKR     |   63.79 |   32.70 |   49.40 |       57.41 |         70.17 |         76.55 |      5.50 |     95.60 |           -7.50 |         4.00 |                                             | Health Care            |
| AGYS     |  122.64 |   32.70 |   51.40 |      110.38 |        134.90 |        147.17 |      4.10 |     87.20 |           -8.00 |         2.00 |                                             | Information Technology |
| ETSY     |   96.24 |   32.70 |   50.50 |       86.62 |        105.86 |        115.49 |      4.70 |     93.20 |           -1.60 |         3.00 | pocket_pivot                                | nan                    |
| VIR      |   11.77 |   32.70 |   51.70 |       10.59 |         12.95 |         14.12 |      5.80 |     96.70 |           -3.40 |         7.00 | pocket_pivot                                | Health Care            |
| CART     |   59.22 |   32.70 |   51.60 |       53.30 |         65.14 |         71.06 |      4.30 |     95.40 |           -4.50 |         3.00 | ema_retest                                  | Consumer Staples       |
| ANF      |  171.09 |   30.10 |   51.60 |      153.98 |        188.20 |        205.31 |      3.80 |     99.50 |           -0.40 |         3.00 |                                             | nan                    |
| CVLT     |  162.44 |   30.10 |   51.50 |      146.20 |        178.68 |        194.93 |      5.10 |     89.90 |           -6.80 |         2.00 |                                             | Information Technology |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:-----------------------|
| ICHR     |   33.71 |   34.70 |   51.70 |       30.34 |         37.08 |         40.45 |      7.10 |      8.10 |          -70.30 |         0.00 |                      | Information Technology |
| WDC      |  323.83 |   34.70 |   50.30 |      291.45 |        356.21 |        388.60 |      5.60 |     58.10 |          -59.50 |         0.00 |                      | Information Technology |
| INTC     |   58.27 |   34.70 |   51.70 |       52.44 |         64.10 |         69.92 |      5.10 |     10.70 |          -59.10 |         0.00 |                      | Information Technology |
| STX      |  557.06 |   34.70 |   50.10 |      501.35 |        612.77 |        668.47 |      6.20 |     59.10 |          -51.30 |         0.00 |                      | Information Technology |
| PANW     |  348.04 |   34.70 |   51.60 |      313.24 |        382.84 |        417.65 |      5.00 |     95.00 |          -19.50 |         3.00 |                      | Information Technology |
| SNDK     | 1037.40 |   34.70 |   51.40 |      933.66 |       1141.14 |       1244.88 |      6.20 |     99.70 |          -55.90 |         0.00 |                      | Information Technology |
| MTRN     |  187.26 |   34.70 |   51.70 |      168.53 |        205.99 |        224.71 |      6.60 |     45.80 |          -42.40 |         0.00 |                      | Materials              |
| AZTA     |   39.14 |   34.70 |   51.40 |       35.23 |         43.05 |         46.97 |      5.80 |     97.20 |          -15.70 |         1.00 |                      | Health Care            |
| SDGR     |   28.52 |   34.70 |   51.70 |       25.67 |         31.37 |         34.22 |      7.90 |     98.60 |          -15.60 |         2.00 |                      | Health Care            |
| SEZL     |  136.69 |   34.70 |   51.60 |      123.02 |        150.36 |        164.03 |      7.10 |     94.80 |          -30.20 |         3.00 |                      | Financials             |
| MRVL     |  159.80 |   34.70 |   50.80 |      143.82 |        175.78 |        191.76 |      6.70 |     60.40 |          -51.50 |         0.00 |                      | Information Technology |
| INSP     |   66.61 |   34.30 |   51.50 |       59.95 |         73.27 |         79.93 |      4.20 |     69.80 |          -54.70 |         1.00 | undercut             | Health Care            |
| PATH     |   13.51 |   34.30 |   51.80 |       12.16 |         14.86 |         16.21 |      4.10 |     41.30 |          -31.90 |         1.00 |                      | Information Technology |
| HIMS     |   26.66 |   34.30 |   51.60 |       23.99 |         29.33 |         31.99 |      7.00 |     11.50 |          -44.80 |         0.00 |                      | Health Care            |
| ON       |   71.24 |   34.30 |   51.70 |       64.12 |         78.36 |         85.49 |      4.70 |     32.30 |          -47.20 |         0.00 |                      | Information Technology |
| KD       |   16.84 |   34.30 |   50.50 |       15.16 |         18.52 |         20.21 |      5.80 |     44.60 |          -41.60 |         0.00 |                      | Information Technology |
| MCHP     |   75.34 |   34.30 |   51.80 |       67.81 |         82.87 |         90.41 |      4.30 |     35.00 |          -28.10 |         0.00 |                      | Information Technology |
| GLW      |  118.77 |   34.30 |   51.40 |      106.89 |        130.65 |        142.52 |      5.00 |     18.70 |          -56.20 |         0.00 |                      | Information Technology |
| FIVN     |   36.35 |   34.30 |   51.70 |       32.71 |         39.98 |         43.62 |      6.00 |     95.80 |           -9.10 |         3.00 |                      | Information Technology |
| COHR     |  195.09 |   34.30 |   51.80 |      175.58 |        214.60 |        234.11 |      7.70 |     12.20 |          -55.70 |         0.00 |                      | Information Technology |
| CRWD     |  241.00 |   34.30 |   51.80 |      216.90 |        265.10 |        289.20 |      5.30 |     98.20 |          -16.00 |         3.00 |                      | Information Technology |
| UCTT     |   44.04 |   34.30 |   50.80 |       39.64 |         48.44 |         52.85 |      7.70 |     11.20 |          -69.50 |         0.00 |                      | Information Technology |
| KLIC     |   68.44 |   34.30 |   51.40 |       61.60 |         75.28 |         82.13 |      5.00 |     43.90 |          -49.50 |         0.00 |                      | Information Technology |
| DOCN     |   84.02 |   34.30 |   51.70 |       75.62 |         92.42 |        100.82 |      8.70 |     44.00 |          -55.20 |         0.00 |                      | Information Technology |
| SITM     |  403.27 |   34.30 |   51.70 |      362.94 |        443.60 |        483.92 |      7.00 |     12.60 |          -55.30 |         0.00 |                      | Information Technology |
| DAVE     |  336.22 |   34.30 |   51.50 |      302.60 |        369.84 |        403.46 |      5.80 |     76.90 |          -26.60 |         2.00 |                      | Financials             |
| EFOR     |   36.98 |   34.30 |   50.50 |       33.28 |         40.68 |         44.38 |      5.50 |     84.40 |          -32.70 |         1.00 |                      | Information Technology |
| ESI      |   33.44 |   34.30 |   51.60 |       30.10 |         36.78 |         40.13 |      4.40 |     23.70 |          -31.90 |         0.00 |                      | Materials              |
| SMTC     |  110.96 |   34.30 |   51.80 |       99.86 |        122.06 |        133.15 |      8.10 |     57.90 |          -45.10 |         0.00 |                      | Information Technology |
| LITE     |  626.75 |   34.30 |   51.80 |      564.08 |        689.43 |        752.10 |      8.40 |     95.20 |          -45.20 |         0.00 |                      | Information Technology |