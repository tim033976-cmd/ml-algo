# Forward test (paper trading record) — updated 2026-10-21

Every day the top 10 of each picks list is logged and scored as real prices arrive: bought at that day's close, +20% (or +10%) target vs -10% stop, 63 trading days max. This is the only fully out-of-sample test there is.

Logged picks: 141; finished (+20/-10): 18; still open: 123.

Finished trades, +20% before -10%:

| list    |      n |   hit_target |   stopped |   avg_return |
|:--------|-------:|-------------:|----------:|-------------:|
| all     | 11.000 |        0.091 |     0.909 |       -0.084 |
| leaders |  7.000 |        0.143 |     0.857 |       -0.067 |

Most recent picks and their status so far:

| date       | ticker   | list    |    close |   p_b20 | b20_result   |   b20_ret |
|:-----------|:---------|:--------|---------:|--------:|:-------------|----------:|
| 2026-10-15 | CAR      | all     |  109.770 |   0.379 | stop         |    -0.102 |
| 2026-10-15 | NSP      | leaders |   50.800 |   0.379 | open         |    -0.015 |
| 2026-10-15 | EZPW     | leaders |   33.130 |   0.379 | open         |    -0.002 |
| 2026-10-15 | CAKE     | leaders |  116.590 |   0.379 | open         |    -0.001 |
| 2026-10-15 | AGYS     | leaders |  113.420 |   0.379 | open         |     0.026 |
| 2026-10-15 | DXC      | leaders |   13.790 |   0.379 | open         |     0.061 |
| 2026-10-15 | ARW      | leaders |  220.170 |   0.379 | open         |    -0.024 |
| 2026-10-15 | RGEN     | leaders |  184.170 |   0.379 | open         |    -0.029 |
| 2026-10-15 | SIG      | leaders |  118.160 |   0.351 | open         |    -0.021 |
| 2026-10-15 | TGTX     | leaders |   56.000 |   0.351 | open         |    -0.026 |
| 2026-10-15 | MORN     | leaders |  209.240 |   0.351 | open         |     0.012 |
| 2026-10-16 | ALG      | all     |  150.660 |   0.346 | open         |    -0.014 |
| 2026-10-16 | CNS      | all     |   69.630 |   0.318 | open         |     0.034 |
| 2026-10-16 | AMG      | all     |  383.760 |   0.318 | open         |     0.026 |
| 2026-10-16 | SCL      | all     |   62.030 |   0.282 | open         |     0.030 |
| 2026-10-16 | GHC      | all     | 1203.260 |   0.208 | open         |     0.017 |
| 2026-10-16 | CNO      | all     |   54.710 |   0.161 | open         |     0.013 |
| 2026-10-16 | CPF      | all     |   36.480 |   0.161 | open         |     0.010 |
| 2026-10-16 | OGS      | all     |   75.600 |   0.161 | open         |    -0.001 |
| 2026-10-16 | OFG      | all     |   52.640 |   0.143 | open         |    -0.041 |
| 2026-10-16 | ABI      | all     |   24.505 |   0.069 | open         |     0.001 |
| 2026-10-16 | AMG      | leaders |  383.760 |   0.318 | open         |     0.026 |
| 2026-10-16 | GHC      | leaders | 1203.260 |   0.208 | open         |     0.017 |
| 2026-10-16 | CNO      | leaders |   54.710 |   0.161 | open         |     0.013 |
| 2026-10-16 | OFG      | leaders |   52.640 |   0.143 | open         |    -0.041 |
| 2026-10-21 | ADEA     | all     |   22.560 |   0.352 | open         |     0.000 |
| 2026-10-21 | WLY      | all     |   52.040 |   0.341 | open         |     0.000 |
| 2026-10-21 | ALG      | all     |  148.500 |   0.341 | open         |     0.000 |
| 2026-10-21 | AMG      | all     |  393.660 |   0.300 | open         |     0.000 |
| 2026-10-21 | HUBB     | all     |  460.760 |   0.250 | open         |     0.000 |
| 2026-10-21 | SCL      | all     |   63.900 |   0.250 | open         |     0.000 |
| 2026-10-21 | GHC      | all     | 1223.430 |   0.231 | open         |     0.000 |
| 2026-10-21 | CPF      | all     |   36.860 |   0.158 | open         |     0.000 |
| 2026-10-21 | OFG      | all     |   50.500 |   0.158 | open         |     0.000 |
| 2026-10-21 | CNO      | all     |   55.410 |   0.121 | open         |     0.000 |
| 2026-10-21 | WLY      | leaders |   52.040 |   0.341 | open         |     0.000 |
| 2026-10-21 | AMG      | leaders |  393.660 |   0.300 | open         |     0.000 |
| 2026-10-21 | SCL      | leaders |   63.900 |   0.250 | open         |     0.000 |
| 2026-10-21 | GHC      | leaders | 1223.430 |   0.231 | open         |     0.000 |
| 2026-10-21 | CNO      | leaders |   55.410 |   0.121 | open         |     0.000 |