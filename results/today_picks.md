# Daily picks — 2026-10-21

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 541,867 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 36% (avg +1.7% net per trade; break-even ~33%). +10% before -10%: 50% vs 48% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:-----------------------|
| WLY      |   52.04 |   34.10 |   50.70 |       46.84 |         57.24 |         62.45 |      2.90 |     90.00 |           -8.70 |         5.00 |                      | Communication Services |
| AMG      |  393.66 |   30.00 |   51.70 |      354.29 |        433.03 |        472.39 |      2.80 |    100.00 |           -0.60 |         7.00 |                      | nan                    |
| SCL      |   63.90 |   25.00 |   52.20 |       57.51 |         70.29 |         76.68 |      2.40 |     95.00 |           -4.00 |         3.00 | wf_scan_pullback     | Materials              |
| GHC      | 1223.43 |   23.10 |   53.50 |     1101.09 |       1345.77 |       1468.12 |      2.10 |     80.00 |           -2.90 |         1.00 | wf_scan_pullback     | nan                    |
| CNO      |   55.41 |   12.10 |   50.00 |       49.87 |         60.95 |         66.49 |      1.70 |     85.00 |           -3.50 |         5.00 |                      | Financials             |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days                  | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:------------------------------------|:-----------------------|
| ADEA     |   22.56 |   35.20 |   49.30 |       20.30 |         24.82 |         27.07 |      4.20 |     50.00 |          -34.10 |         0.00 |                                     | Information Technology |
| WLY      |   52.04 |   34.10 |   50.70 |       46.84 |         57.24 |         62.45 |      2.90 |     90.00 |           -8.70 |         5.00 |                                     | Communication Services |
| ALG      |  148.50 |   34.10 |   49.30 |      133.65 |        163.35 |        178.20 |      2.90 |     20.00 |          -32.00 |         0.00 |                                     | Industrials            |
| AMG      |  393.66 |   30.00 |   51.70 |      354.29 |        433.03 |        472.39 |      2.80 |    100.00 |           -0.60 |         7.00 |                                     | nan                    |
| HUBB     |  460.76 |   25.00 |   47.10 |      414.68 |        506.84 |        552.91 |      2.60 |     40.00 |          -18.00 |         0.00 |                                     | Industrials            |
| SCL      |   63.90 |   25.00 |   52.20 |       57.51 |         70.29 |         76.68 |      2.40 |     95.00 |           -4.00 |         3.00 | wf_scan_pullback                    | Materials              |
| GHC      | 1223.43 |   23.10 |   53.50 |     1101.09 |       1345.77 |       1468.12 |      2.10 |     80.00 |           -2.90 |         1.00 | wf_scan_pullback                    | nan                    |
| CPF      |   36.86 |   15.80 |   53.10 |       33.17 |         40.55 |         44.23 |      1.90 |     75.00 |           -9.40 |         3.00 | wf_scan_pullback, tc_supertrend_ema | Financials             |
| OFG      |   50.50 |   15.80 |   49.10 |       45.45 |         55.55 |         60.60 |      2.10 |     70.00 |           -6.60 |         3.00 |                                     | Financials             |
| CNO      |   55.41 |   12.10 |   50.00 |       49.87 |         60.95 |         66.49 |      1.70 |     85.00 |           -3.50 |         5.00 |                                     | Financials             |
| OGS      |   75.55 |   12.10 |   53.50 |       68.00 |         83.11 |         90.66 |      1.70 |     35.00 |          -15.40 |         0.00 |                                     | Utilities              |
| ABI      |   24.52 |    7.20 |   48.00 |       22.07 |         26.98 |         29.43 |      0.40 |     65.00 |           -0.60 |         2.00 |                                     | nan                    |