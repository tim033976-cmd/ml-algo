# Daily picks — 2026-10-16

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 540,745 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.4% net per trade; break-even ~33%). +10% before -10%: 50% vs 47% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                  | sector     |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------|:-----------|
| AMG      |  383.76 |   31.80 |   52.10 |      345.38 |        422.14 |        460.51 |      3.00 |    100.00 |           -2.80 |         7.00 | wf_scan_pullback                    | nan        |
| GHC      | 1203.26 |   20.80 |   51.60 |     1082.93 |       1323.59 |       1443.91 |      2.10 |     76.50 |           -4.50 |         1.00 |                                     | nan        |
| CNO      |   54.71 |   16.10 |   49.20 |       49.24 |         60.18 |         65.65 |      2.00 |     94.10 |           -4.70 |         4.00 | wf_scan_pullback                    | Financials |
| OFG      |   52.64 |   14.30 |   48.70 |       47.38 |         57.90 |         63.17 |      1.90 |     82.40 |           -2.70 |         3.00 | wf_scan_pullback, tc_supertrend_ema | Financials |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                  | sector      |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------|:------------|
| ALG      |  150.66 |   34.60 |   42.90 |      135.59 |        165.73 |        180.79 |      3.00 |     17.60 |          -31.10 |         0.00 |                                     | Industrials |
| CNS      |   69.63 |   31.80 |   52.50 |       62.67 |         76.59 |         83.56 |      3.20 |     58.80 |          -19.60 |         0.00 |                                     | Financials  |
| AMG      |  383.76 |   31.80 |   52.10 |      345.38 |        422.14 |        460.51 |      3.00 |    100.00 |           -2.80 |         7.00 | wf_scan_pullback                    | nan         |
| SCL      |   62.03 |   28.20 |   50.50 |       55.83 |         68.23 |         74.44 |      2.50 |     88.20 |           -6.80 |         3.00 |                                     | Materials   |
| GHC      | 1203.26 |   20.80 |   51.60 |     1082.93 |       1323.59 |       1443.91 |      2.10 |     76.50 |           -4.50 |         1.00 |                                     | nan         |
| CNO      |   54.71 |   16.10 |   49.20 |       49.24 |         60.18 |         65.65 |      2.00 |     94.10 |           -4.70 |         4.00 | wf_scan_pullback                    | Financials  |
| CPF      |   36.48 |   16.10 |   50.40 |       32.83 |         40.13 |         43.78 |      2.00 |     70.60 |          -10.30 |         3.00 |                                     | Financials  |
| OGS      |   75.60 |   16.10 |   50.40 |       68.04 |         83.16 |         90.72 |      1.70 |     35.30 |          -15.30 |         0.00 |                                     | Utilities   |
| OFG      |   52.64 |   14.30 |   48.70 |       47.38 |         57.90 |         63.17 |      1.90 |     82.40 |           -2.70 |         3.00 | wf_scan_pullback, tc_supertrend_ema | Financials  |
| ABI      |   24.50 |    6.90 |   44.60 |       22.05 |         26.96 |         29.41 |      0.30 |     64.70 |           -0.70 |         2.00 | undercut, tc_supertrend_ema         | nan         |