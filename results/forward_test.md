# Forward test (paper trading record) — updated 2026-10-22

Every day the top 10 of each picks list is logged and scored as real prices arrive: bought at that day's close, +20% (or +10%) target vs -10% stop, 63 trading days max. This is the only fully out-of-sample test there is.

Logged picks: 157; finished (+20/-10): 19; still open: 138.

Finished trades, +20% before -10%:

| list    |      n |   hit_target |   stopped |   avg_return |
|:--------|-------:|-------------:|----------:|-------------:|
| all     | 12.000 |        0.083 |     0.917 |       -0.086 |
| leaders |  7.000 |        0.143 |     0.857 |       -0.067 |

Most recent picks and their status so far:

| date       | ticker   | list    |    close |   p_b20 | b20_result   |   b20_ret |
|:-----------|:---------|:--------|---------:|--------:|:-------------|----------:|
| 2026-10-16 | CNO      | all     |   54.710 |   0.161 | open         |     0.014 |
| 2026-10-16 | CPF      | all     |   36.480 |   0.161 | open         |     0.035 |
| 2026-10-16 | OGS      | all     |   75.600 |   0.161 | open         |     0.035 |
| 2026-10-16 | OFG      | all     |   52.640 |   0.143 | open         |    -0.024 |
| 2026-10-16 | ABI      | all     |   24.505 |   0.069 | open         |     0.003 |
| 2026-10-16 | AMG      | leaders |  383.760 |   0.318 | open         |     0.031 |
| 2026-10-16 | GHC      | leaders | 1203.260 |   0.208 | open         |     0.030 |
| 2026-10-16 | CNO      | leaders |   54.710 |   0.161 | open         |     0.014 |
| 2026-10-16 | OFG      | leaders |   52.640 |   0.143 | open         |    -0.024 |
| 2026-10-21 | ADEA     | all     |   22.560 |   0.352 | open         |    -0.057 |
| 2026-10-21 | WLY      | all     |   52.040 |   0.341 | open         |     0.039 |
| 2026-10-21 | ALG      | all     |  148.500 |   0.341 | open         |     0.000 |
| 2026-10-21 | AMG      | all     |  393.660 |   0.300 | open         |     0.005 |
| 2026-10-21 | HUBB     | all     |  460.760 |   0.250 | open         |    -0.032 |
| 2026-10-21 | SCL      | all     |   63.900 |   0.250 | open         |     0.007 |
| 2026-10-21 | GHC      | all     | 1223.430 |   0.231 | open         |     0.013 |
| 2026-10-21 | CPF      | all     |   36.860 |   0.158 | open         |     0.025 |
| 2026-10-21 | OFG      | all     |   50.500 |   0.158 | open         |     0.017 |
| 2026-10-21 | CNO      | all     |   55.410 |   0.121 | open         |     0.002 |
| 2026-10-21 | WLY      | leaders |   52.040 |   0.341 | open         |     0.039 |
| 2026-10-21 | AMG      | leaders |  393.660 |   0.300 | open         |     0.005 |
| 2026-10-21 | SCL      | leaders |   63.900 |   0.250 | open         |     0.007 |
| 2026-10-21 | GHC      | leaders | 1223.430 |   0.231 | open         |     0.013 |
| 2026-10-21 | CNO      | leaders |   55.410 |   0.121 | open         |     0.002 |
| 2026-10-22 | ADEA     | all     |   21.265 |   0.359 | open         |     0.000 |
| 2026-10-22 | WLY      | all     |   54.050 |   0.321 | open         |     0.000 |
| 2026-10-22 | AMG      | all     |  395.530 |   0.282 | open         |     0.000 |
| 2026-10-22 | HUBB     | all     |  445.800 |   0.267 | open         |     0.000 |
| 2026-10-22 | SCL      | all     |   64.320 |   0.236 | open         |     0.000 |
| 2026-10-22 | GHC      | all     | 1239.590 |   0.166 | open         |     0.000 |
| 2026-10-22 | OGS      | all     |   78.250 |   0.116 | open         |     0.000 |
| 2026-10-22 | OFG      | all     |   51.360 |   0.094 | open         |     0.000 |
| 2026-10-22 | CPF      | all     |   37.770 |   0.094 | open         |     0.000 |
| 2026-10-22 | CNO      | all     |   55.500 |   0.067 | open         |     0.000 |
| 2026-10-22 | WLY      | leaders |   54.050 |   0.321 | open         |     0.000 |
| 2026-10-22 | AMG      | leaders |  395.530 |   0.282 | open         |     0.000 |
| 2026-10-22 | SCL      | leaders |   64.320 |   0.236 | open         |     0.000 |
| 2026-10-22 | GHC      | leaders | 1239.590 |   0.166 | open         |     0.000 |
| 2026-10-22 | CPF      | leaders |   37.770 |   0.094 | open         |     0.000 |
| 2026-10-22 | CNO      | leaders |   55.500 |   0.067 | open         |     0.000 |