# Daily picks — 2026-10-22

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 542,008 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.6% net per trade; break-even ~33%). +10% before -10%: 50% vs 47% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                  | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------|:-----------------------|
| WLY      |   54.05 |   32.10 |   53.70 |       48.64 |         59.45 |         64.86 |      2.90 |     95.00 |           -5.20 |         5.00 |                                     | Communication Services |
| AMG      |  395.53 |   28.20 |   51.90 |      355.98 |        435.08 |        474.64 |      2.90 |    100.00 |           -0.40 |         7.00 |                                     | nan                    |
| SCL      |   64.32 |   23.60 |   49.90 |       57.89 |         70.75 |         77.18 |      2.40 |     90.00 |           -3.30 |         3.00 | wf_scan_pullback                    | Materials              |
| GHC      | 1239.59 |   16.60 |   49.20 |     1115.63 |       1363.55 |       1487.51 |      2.10 |     75.00 |           -1.60 |         1.00 | wf_scan_pullback                    | nan                    |
| CPF      |   37.77 |    9.40 |   48.30 |       33.99 |         41.55 |         45.32 |      1.90 |     80.00 |           -7.10 |         4.00 | wf_scan_pullback, tc_supertrend_ema | Financials             |
| CNO      |   55.50 |    6.70 |   48.20 |       49.95 |         61.05 |         66.60 |      1.70 |     85.00 |           -3.30 |         5.00 | donchian_20, wf_scan_base           | Financials             |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                  | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------|:-----------------------|
| ADEA     |   21.26 |   35.90 |   50.70 |       19.14 |         23.39 |         25.52 |      4.30 |     30.00 |          -37.80 |         0.00 |                                     | Information Technology |
| WLY      |   54.05 |   32.10 |   53.70 |       48.64 |         59.45 |         64.86 |      2.90 |     95.00 |           -5.20 |         5.00 |                                     | Communication Services |
| AMG      |  395.53 |   28.20 |   51.90 |      355.98 |        435.08 |        474.64 |      2.90 |    100.00 |           -0.40 |         7.00 |                                     | nan                    |
| HUBB     |  445.80 |   26.70 |   53.30 |      401.22 |        490.38 |        534.96 |      2.70 |     40.00 |          -20.70 |         0.00 |                                     | Industrials            |
| SCL      |   64.32 |   23.60 |   49.90 |       57.89 |         70.75 |         77.18 |      2.40 |     90.00 |           -3.30 |         3.00 | wf_scan_pullback                    | Materials              |
| GHC      | 1239.59 |   16.60 |   49.20 |     1115.63 |       1363.55 |       1487.51 |      2.10 |     75.00 |           -1.60 |         1.00 | wf_scan_pullback                    | nan                    |
| OGS      |   78.25 |   11.60 |   52.20 |       70.42 |         86.08 |         93.90 |      1.70 |     45.00 |          -12.30 |         1.00 |                                     | Utilities              |
| OFG      |   51.36 |    9.40 |   49.30 |       46.22 |         56.50 |         61.63 |      2.20 |     70.00 |           -5.10 |         3.00 |                                     | Financials             |
| CPF      |   37.77 |    9.40 |   48.30 |       33.99 |         41.55 |         45.32 |      1.90 |     80.00 |           -7.10 |         4.00 | wf_scan_pullback, tc_supertrend_ema | Financials             |
| CNO      |   55.50 |    6.70 |   48.20 |       49.95 |         61.05 |         66.60 |      1.70 |     85.00 |           -3.30 |         5.00 | donchian_20, wf_scan_base           | Financials             |
| ABI      |   24.58 |    6.70 |   45.90 |       22.13 |         27.04 |         29.50 |      0.40 |     65.00 |           -0.30 |         2.00 |                                     | nan                    |