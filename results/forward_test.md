# Forward test (paper trading record) — updated 2026-11-13

Every day the top 10 of each picks list is logged and scored as real prices arrive: bought at that day's close, +20% (or +10%) target vs -10% stop, 63 trading days max. This is the only fully out-of-sample test there is.

Logged picks: 457; finished (+20/-10): 205; still open: 252.

Finished trades, +20% before -10%:

| list    |       n |   hit_target |   stopped |   avg_return |
|:--------|--------:|-------------:|----------:|-------------:|
| all     | 114.000 |        0.289 |     0.711 |       -0.020 |
| leaders |  91.000 |        0.297 |     0.703 |       -0.025 |

Most recent picks and their status so far:

| date       | ticker   | list    |   close |   p_b20 | b20_result   |   b20_ret |
|:-----------|:---------|:--------|--------:|--------:|:-------------|----------:|
| 2026-11-12 | INTC     | all     |  61.200 |   0.357 | open         |    -0.025 |
| 2026-11-12 | CRSR     | all     |  12.280 |   0.357 | open         |    -0.041 |
| 2026-11-12 | AZTA     | all     |  43.860 |   0.357 | open         |     0.041 |
| 2026-11-12 | AMD      | all     | 585.300 |   0.357 | stop         |    -0.102 |
| 2026-11-12 | APP      | all     | 393.680 |   0.357 | open         |     0.000 |
| 2026-11-12 | SNDK     | all     | 937.460 |   0.357 | open         |     0.000 |
| 2026-11-12 | ALHC     | all     |   7.500 |   0.357 | open         |    -0.019 |
| 2026-11-12 | TNDM     | all     |  17.510 |   0.357 | open         |     0.146 |
| 2026-11-12 | EPAM     | all     | 163.830 |   0.357 | open         |     0.000 |
| 2026-11-12 | DFH      | all     |  11.010 |   0.357 | open         |    -0.032 |
| 2026-11-12 | AZTA     | leaders |  43.860 |   0.357 | open         |     0.041 |
| 2026-11-12 | AMD      | leaders | 585.300 |   0.357 | stop         |    -0.102 |
| 2026-11-12 | XNCR     | leaders |  38.130 |   0.357 | open         |    -0.027 |
| 2026-11-12 | PD       | leaders |  15.720 |   0.357 | open         |     0.015 |
| 2026-11-12 | CDW      | leaders | 172.790 |   0.357 | open         |     0.000 |
| 2026-11-12 | ANF      | leaders | 150.490 |   0.357 | open         |    -0.011 |
| 2026-11-12 | PAYC     | leaders | 248.840 |   0.357 | open         |     0.000 |
| 2026-11-12 | MTW      | leaders |  24.380 |   0.357 | open         |    -0.023 |
| 2026-11-12 | NSIT     | leaders | 172.850 |   0.357 | open         |    -0.024 |
| 2026-11-12 | ELF      | leaders | 113.530 |   0.355 | open         |     0.039 |
| 2026-11-13 | ALHC     | all     |   7.360 |   0.355 | open         |     0.000 |
| 2026-11-13 | LEU      | all     | 103.780 |   0.355 | open         |     0.000 |
| 2026-11-13 | CORT     | all     |  72.940 |   0.355 | open         |     0.000 |
| 2026-11-13 | ARWR     | all     |  47.780 |   0.355 | open         |     0.000 |
| 2026-11-13 | HIMS     | all     |  19.730 |   0.355 | open         |     0.000 |
| 2026-11-13 | OII      | all     |  35.630 |   0.355 | open         |     0.000 |
| 2026-11-13 | DOCS     | all     |  33.340 |   0.355 | open         |     0.000 |
| 2026-11-13 | DVA      | all     | 174.560 |   0.355 | open         |     0.000 |
| 2026-11-13 | MPC      | all     | 414.650 |   0.355 | open         |     0.000 |
| 2026-11-13 | ILMN     | all     | 207.010 |   0.355 | open         |     0.000 |
| 2026-11-13 | ACHC     | leaders |  37.780 |   0.355 | open         |     0.000 |
| 2026-11-13 | TRUP     | leaders |  34.480 |   0.355 | open         |     0.000 |
| 2026-11-13 | VAC      | leaders | 116.810 |   0.355 | open         |     0.000 |
| 2026-11-13 | PRGO     | leaders |  16.240 |   0.355 | open         |     0.000 |
| 2026-11-13 | NWL      | leaders |   5.780 |   0.355 | open         |     0.000 |
| 2026-11-13 | VCEL     | leaders |  56.960 |   0.355 | open         |     0.000 |
| 2026-11-13 | FTDR     | leaders |  96.640 |   0.355 | open         |     0.000 |
| 2026-11-13 | QNST     | leaders |  18.980 |   0.355 | open         |     0.000 |
| 2026-11-13 | SIG      | leaders | 113.980 |   0.355 | open         |     0.000 |
| 2026-11-13 | SWKS     | leaders |  89.940 |   0.355 | open         |     0.000 |