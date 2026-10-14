# Daily picks — 2026-10-13

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 539,851 past snapshots of 1538 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 35% (avg +1.2% net per trade; break-even ~33%). +10% before -10%: 50% vs 48% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   |   sector |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|---------:|
| AMG      |  379.01 |   25.40 |   51.60 |      341.11 |        416.91 |        454.81 |      3.00 |    100.00 |           -4.00 |         7.00 |                      |      nan |
| GHC      | 1173.98 |   14.80 |   50.80 |     1056.58 |       1291.38 |       1408.78 |      2.20 |     71.40 |           -7.00 |         1.00 |                      |      nan |

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector      |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:------------|
| ALG      |  155.17 |   25.40 |   51.60 |      139.65 |        170.69 |        186.20 |      3.10 |      7.10 |          -29.10 |         0.00 |                      | Industrials |
| AMG      |  379.01 |   25.40 |   51.60 |      341.11 |        416.91 |        454.81 |      3.00 |    100.00 |           -4.00 |         7.00 |                      | nan         |
| SCL      |   62.01 |   23.90 |   51.50 |       55.81 |         68.21 |         74.41 |      2.50 |     85.70 |           -6.80 |         3.00 | undercut             | Materials   |
| CNS      |   68.86 |   18.20 |   51.50 |       61.97 |         75.75 |         82.63 |      2.90 |     50.00 |          -20.40 |         0.00 |                      | Financials  |
| GHC      | 1173.98 |   14.80 |   50.80 |     1056.58 |       1291.38 |       1408.78 |      2.20 |     71.40 |           -7.00 |         1.00 |                      | nan         |
| CNO      |   53.42 |   12.00 |   46.30 |       48.08 |         58.76 |         64.10 |      2.00 |     92.90 |           -6.90 |         4.00 |                      | Financials  |
| CPF      |   35.61 |   12.00 |   46.30 |       32.05 |         39.17 |         42.73 |      2.10 |     64.30 |          -12.40 |         3.00 |                      | Financials  |
| OFG      |   50.86 |    9.80 |   46.30 |       45.77 |         55.95 |         61.03 |      1.80 |     78.60 |           -6.00 |         2.00 |                      | Financials  |
| OGS      |   74.54 |    6.90 |   46.30 |       67.09 |         81.99 |         89.45 |      1.70 |     28.60 |          -16.50 |         0.00 |                      | Utilities   |
| ABI      |   24.49 |    6.90 |   44.70 |       22.04 |         26.93 |         29.38 |      0.30 |     57.10 |           -0.70 |         2.00 | wf_scan_pullback     | nan         |