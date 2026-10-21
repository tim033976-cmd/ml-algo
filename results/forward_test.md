# Forward test (paper trading record) — updated 2026-10-20

Every day the top 10 of each picks list is logged and scored as real prices arrive: bought at that day's close, +20% (or +10%) target vs -10% stop, 63 trading days max. This is the only fully out-of-sample test there is.

Logged picks: 126; finished (+20/-10): 16; still open: 110.

Finished trades, +20% before -10%:

| list    |     n |   hit_target |   stopped |   avg_return |
|:--------|------:|-------------:|----------:|-------------:|
| all     | 9.000 |        0.111 |     0.889 |       -0.080 |
| leaders | 7.000 |        0.143 |     0.857 |       -0.067 |

Most recent picks and their status so far:

| date       | ticker   | list    |    close |   p_b20 | b20_result   |   b20_ret |
|:-----------|:---------|:--------|---------:|--------:|:-------------|----------:|
| 2026-10-14 | AVT      | leaders |   95.850 |   0.370 | open         |    -0.041 |
| 2026-10-14 | KSS      | leaders |   21.150 |   0.370 | open         |     0.014 |
| 2026-10-14 | ROG      | leaders |  139.720 |   0.370 | open         |    -0.036 |
| 2026-10-14 | SMTC     | leaders |  160.260 |   0.370 | stop         |    -0.102 |
| 2026-10-14 | TGTX     | leaders |   54.370 |   0.370 | open         |    -0.020 |
| 2026-10-14 | CRL      | leaders |  302.000 |   0.370 | open         |    -0.007 |
| 2026-10-15 | BJRI     | all     |   60.220 |   0.379 | open         |    -0.023 |
| 2026-10-15 | GPK      | all     |    8.730 |   0.379 | open         |    -0.036 |
| 2026-10-15 | EAT      | all     |  204.910 |   0.379 | open         |    -0.034 |
| 2026-10-15 | FUN      | all     |    8.550 |   0.379 | open         |    -0.028 |
| 2026-10-15 | OI       | all     |    5.920 |   0.379 | open         |    -0.003 |
| 2026-10-15 | WD       | all     |   33.320 |   0.379 | open         |    -0.050 |
| 2026-10-15 | NSP      | all     |   50.800 |   0.379 | open         |    -0.035 |
| 2026-10-15 | GEO      | all     |   29.330 |   0.379 | open         |    -0.053 |
| 2026-10-15 | LEU      | all     |  127.010 |   0.379 | stop         |    -0.102 |
| 2026-10-15 | CAR      | all     |  109.770 |   0.379 | stop         |    -0.102 |
| 2026-10-15 | NSP      | leaders |   50.800 |   0.379 | open         |    -0.035 |
| 2026-10-15 | EZPW     | leaders |   33.130 |   0.379 | open         |    -0.011 |
| 2026-10-15 | CAKE     | leaders |  116.590 |   0.379 | open         |    -0.004 |
| 2026-10-15 | AGYS     | leaders |  113.420 |   0.379 | open         |    -0.010 |
| 2026-10-15 | DXC      | leaders |   13.790 |   0.379 | open         |     0.034 |
| 2026-10-15 | ARW      | leaders |  220.170 |   0.379 | open         |    -0.018 |
| 2026-10-15 | RGEN     | leaders |  184.170 |   0.379 | open         |    -0.042 |
| 2026-10-15 | SIG      | leaders |  118.160 |   0.351 | open         |    -0.012 |
| 2026-10-15 | TGTX     | leaders |   56.000 |   0.351 | open         |    -0.048 |
| 2026-10-15 | MORN     | leaders |  209.240 |   0.351 | open         |    -0.017 |
| 2026-10-16 | ALG      | all     |  150.660 |   0.346 | open         |    -0.013 |
| 2026-10-16 | CNS      | all     |   69.630 |   0.318 | open         |    -0.018 |
| 2026-10-16 | AMG      | all     |  383.760 |   0.318 | open         |     0.003 |
| 2026-10-16 | SCL      | all     |   62.030 |   0.282 | open         |     0.006 |
| 2026-10-16 | GHC      | all     | 1203.260 |   0.208 | open         |     0.006 |
| 2026-10-16 | CNO      | all     |   54.710 |   0.161 | open         |    -0.012 |
| 2026-10-16 | CPF      | all     |   36.480 |   0.161 | open         |    -0.005 |
| 2026-10-16 | OGS      | all     |   75.600 |   0.161 | open         |    -0.013 |
| 2026-10-16 | OFG      | all     |   52.640 |   0.143 | open         |    -0.009 |
| 2026-10-16 | ABI      | all     |   24.505 |   0.069 | open         |     0.000 |
| 2026-10-16 | AMG      | leaders |  383.760 |   0.318 | open         |     0.003 |
| 2026-10-16 | GHC      | leaders | 1203.260 |   0.208 | open         |     0.006 |
| 2026-10-16 | CNO      | leaders |   54.710 |   0.161 | open         |    -0.012 |
| 2026-10-16 | OFG      | leaders |   52.640 |   0.143 | open         |    -0.009 |