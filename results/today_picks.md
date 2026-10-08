# Daily picks — 2026-10-08

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 532,501 past snapshots of 1488 stocks. Probabilities are in %.

Historically (training data): all stocks hit +20% before -10% 20% of the time; the model's top 10% 59%. +10% before -10%: 48% vs 82%. Out-of-sample (2018+) the top 10% hit +20% first about 38-39% of the time vs a ~33% break-even (see results/report.md). Training-data rates are optimistic; trust the out-of-sample ones.

Sorted by p_b20 = model probability of +20% before -10%. `setups_last_3_days` lists setups that fired (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

| ticker   |   close |   p_b20 |   p_b10 |   stop_-10% |   target_+10% |   target_+20% |   adr_pct |   rs_rank |   dist_52w_high |   base_count | setups_last_3_days   | sector                 |
|:---------|--------:|--------:|--------:|------------:|--------------:|--------------:|----------:|----------:|----------------:|-------------:|:---------------------|:-----------------------|
| CC       |   14.06 |   60.00 |   70.80 |       12.65 |         15.47 |         16.87 |      3.20 |     10.00 |          -50.50 |         0.00 |                      | Materials              |
| ECHO     |   95.41 |   57.90 |   70.90 |       85.87 |        104.95 |        114.49 |      3.10 |     50.60 |          -35.20 |         0.00 |                      | Communication Services |
| RSI      |   20.40 |   57.70 |   78.30 |       18.36 |         22.44 |         24.48 |      5.00 |     20.00 |          -40.90 |         0.00 |                      | Consumer Discretionary |
| MP       |   46.27 |   57.10 |   71.50 |       41.64 |         50.90 |         55.52 |      4.10 |     10.20 |          -53.80 |         0.00 |                      | Materials              |
| RYAN     |   37.53 |   57.10 |   73.70 |       33.78 |         41.29 |         45.04 |      3.80 |     23.70 |          -35.60 |         0.00 |                      | Financials             |
| KD       |   11.66 |   56.70 |   71.50 |       10.50 |         12.83 |         14.00 |      4.40 |      8.80 |          -61.50 |         0.00 |                      | Information Technology |
| CENX     |   36.44 |   56.10 |   73.50 |       32.80 |         40.08 |         43.73 |      3.60 |     21.60 |          -48.30 |         0.00 |                      | Materials              |
| UTI      |   19.89 |   55.60 |   75.70 |       17.90 |         21.88 |         23.87 |      4.90 |      0.50 |          -61.30 |         0.00 |                      | Consumer Discretionary |
| LUMN     |    5.77 |   55.30 |   70.90 |        5.19 |          6.35 |          6.92 |      4.70 |     13.80 |          -51.70 |         0.00 |                      | Communication Services |
| MTZ      |  217.00 |   55.30 |   70.50 |      195.30 |        238.70 |        260.40 |      4.60 |      5.20 |          -50.80 |         0.00 |                      | Industrials            |
| WRBY     |   24.88 |   55.00 |   71.50 |       22.39 |         27.37 |         29.86 |      6.20 |     48.20 |          -19.70 |         0.00 |                      | Consumer Discretionary |
| FOUR     |   38.80 |   54.90 |   68.40 |       34.92 |         42.68 |         46.56 |      4.90 |      5.70 |          -52.10 |         0.00 |                      | Financials             |
| DUOL     |  150.50 |   54.80 |   70.70 |      135.45 |        165.55 |        180.60 |      4.20 |     71.20 |          -57.40 |         1.00 |                      | Consumer Discretionary |
| OLN      |   16.06 |   54.80 |   70.60 |       14.45 |         17.67 |         19.27 |      3.40 |      3.50 |          -46.30 |         0.00 |                      | Materials              |
| ALB      |  101.33 |   54.80 |   73.70 |       91.20 |        111.47 |        121.60 |      3.00 |     15.70 |          -53.90 |         0.00 |                      | Materials              |
| HUBS     |  221.80 |   54.60 |   71.80 |      199.62 |        243.98 |        266.16 |      5.30 |     24.70 |          -55.50 |         0.00 |                      | Information Technology |
| HLNE     |   84.52 |   54.60 |   70.60 |       76.07 |         92.97 |        101.42 |      3.90 |     25.60 |          -44.60 |         0.00 |                      | Financials             |
| CCOI     |    9.71 |   54.60 |   67.50 |        8.74 |         10.68 |         11.65 |      8.30 |      0.30 |          -78.60 |         0.00 |                      | Communication Services |
| COIN     |  176.72 |   54.60 |   71.60 |      159.05 |        194.39 |        212.06 |      5.50 |     24.60 |          -56.10 |         0.00 |                      | Financials             |
| IBP      |  181.74 |   54.50 |   70.20 |      163.57 |        199.92 |        218.09 |      4.10 |      6.70 |          -47.30 |         0.00 |                      | Consumer Discretionary |
| CE       |   44.51 |   54.30 |   72.00 |       40.06 |         48.97 |         53.42 |      3.80 |     26.30 |          -37.00 |         0.00 |                      | Materials              |
| OI       |    5.85 |   54.30 |   65.00 |        5.26 |          6.43 |          7.02 |      3.80 |      0.70 |          -65.40 |         0.00 |                      | Materials              |
| RDDT     |  153.83 |   54.00 |   72.30 |      138.45 |        169.21 |        184.60 |      4.20 |     20.40 |          -41.60 |         0.00 |                      | Communication Services |
| SNEX     |   60.04 |   53.80 |   70.60 |       54.04 |         66.05 |         72.05 |      4.00 |     48.90 |          -36.60 |         0.00 |                      | Financials             |
| BL       |   28.33 |   53.80 |   74.90 |       25.50 |         31.16 |         34.00 |      3.40 |     13.40 |          -52.40 |         0.00 |                      | Information Technology |
| CAVA     |   53.92 |   53.80 |   67.90 |       48.53 |         59.32 |         64.71 |      4.00 |      6.50 |          -45.40 |         0.00 |                      | Consumer Discretionary |
| SEDG     |   32.57 |   53.80 |   74.90 |       29.31 |         35.83 |         39.08 |      6.10 |      6.30 |          -59.90 |         0.00 |                      | Information Technology |
| HL       |   16.50 |   53.70 |   69.80 |       14.85 |         18.15 |         19.80 |      3.90 |     65.60 |          -51.70 |         0.00 |                      | Materials              |
| PZZA     |   19.43 |   53.60 |   73.20 |       17.49 |         21.37 |         23.32 |      3.50 |      0.60 |          -63.80 |         0.00 |                      | Consumer Discretionary |
| UNIT     |    7.66 |   53.50 |   72.70 |        6.90 |          8.43 |          9.20 |      3.80 |     21.90 |          -40.80 |         0.00 |                      | Communication Services |