# Strategy research report

Generated 2026-10-10 13:16 UTC in 80 min.
Universe: 1540 stocks with data (sp500: 657, sp600: 537, sp400: 346; 158 former S&P 500 members). Signals 2006-01-03 -> 2026-10-08: 952,523.
**In-sample (selection): trades closed before 2018-01-01. Out-of-sample (judgement): entries from 2018-01-01.**
R = profit in multiples of the initial risk (entry - stop). Costs: 0.1% per side. Entries at the signal-day close.

## What this run tells us

- In-sample rankings persist out-of-sample (rank correlation 0.48). Top 20 by IS t-stat: +0.063R OOS; top 20 by IS avgR (n>=200): +0.397R; all strategies +0.053R; random entries -0.005R.
- Too few signals to judge (need 100+ per period): htf (IS 53, OOS 102).
- Entries with a clear edge over random entries (>= +0.05R in both periods): ep_gap15 (IS +0.30R, OOS +0.32R), ep_gap8_hold (IS +0.19R, OOS +0.18R), ep_gap10_vol5 (IS +0.18R, OOS +0.22R), ep_gap8_neglected (IS +0.20R, OOS +0.16R), desc_triangle (IS +0.20R, OOS +0.15R), tc_supertrend_ema (IS +0.16R, OOS +0.12R), ep_gap5 (IS +0.14R, OOS +0.12R), wf_rocket_gap (IS +0.11R, OOS +0.21R), ep_gap10 (IS +0.10R, OOS +0.23R), falling_wedge (IS +0.23R, OOS +0.10R), ep_gap10_vol2 (IS +0.07R, OOS +0.25R), wf_rocket_breakout (IS +0.14R, OOS +0.07R), tc_ema_cross_base (IS +0.13R, OOS +0.07R), donchian_20 (IS +0.11R, OOS +0.07R), undercut (IS +0.12R, OOS +0.07R), wf_scan_pullback (IS +0.12R, OOS +0.06R), ema_retest (IS +0.10R, OOS +0.06R), wf_scan_base (IS +0.12R, OOS +0.05R), flag_60 (IS +0.05R, OOS +0.18R), sym_triangle (IS +0.05R, OOS +0.10R).
- Entries with no edge over random entries: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
- Best exit out-of-sample (avg over entries): wf_weekly10 (+0.099R); worst: qull_sma10 (-0.042R).
- Filters that help OOS: qull_scan_regime (+0.123R), rs80_early (+0.112R), qull_scan (+0.087R), rs80_early_theme (+0.073R), early_stage (+0.050R), wf_scan_green (+0.043R), wf_rocket_green (+0.038R), rs80 (+0.032R); that hurt: none.
- ML filter adds little: OOS rank corr 0.006, AUC 0.506, decile monotonicity -0.26, taken +0.083R vs skipped +0.072R.
- Features the model relies on most: rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope.
- Filters that improve even RANDOM entries in both periods (the stock selection itself is the edge): rs80_early_theme (IS +0.05R, OOS +0.11R).
- Best readable rule that held OOS: `rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.554` (IS +0.33R, OOS +0.13R, n=48868).
- Superperformer model: 30.4% of its top-10% picks gained >= 40% within 3 months vs 7.2% for all stocks (4.2x), AUC 0.834. Driven by: adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range.
- GOAL +10% before -10%: all stocks hit it 49% of the time; the model's top 10% 52% (break-even ~50%), avg net return per trade +0.7%. Point-in-time S&P 500 top 10%: 53%, +1.1% per trade (n=7387).
- GOAL +20% before -10%: all stocks hit it 23% of the time; the model's top 10% 37% (break-even ~33%), avg net return per trade +2.2%. Point-in-time S&P 500 top 10%: 37%, +2.9% per trade (n=5040).
- Best portfolio 2018->today: RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10% at 33.9% CAGR (max drawdown -35.4%) vs SPY 14.6%.
- Best return per unit of drawdown: REGIME 3-day market model: skip ['rest'] / +20% -10% (6.7% CAGR, -6.8% max DD).
- Workflow PDF rockets as written (regime sizing) / wf_rocket: 2.3% CAGR, -11% DD, 190 trades.
- Workflow PDF rockets, QQQ 21/50 regime / wf_rocket: 1.5% CAGR, -9% DD, 192 trades.
- Workflow PDF rockets as written, S&P 500 point-in-time only / wf_rocket: 1.4% CAGR, -7% DD, 142 trades.
- Workflow PDF scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10: 1.1% CAGR, -17% DD, 349 trades.
- Workflow PDF scanner PIT, QQQ 21/50 regime / wf_weekly10: -2.3% CAGR, -25% DD, 375 trades.
- Workflow PDF scanner as written, full universe / wf_weekly10: 0.8% CAGR, -21% DD, 368 trades.
- Workflow PDF split (40/25/15/20 cash): 6.6% CAGR, -17% DD vs SPY 14.6%, -34%.
- Volatility-matched check (goal model (full universe), OOS): model top 10% hit 39.0% vs 34.1% for same-ADR, same-momentum stocks; return +2.86% vs +1.98% per trade.
- Volatility-matched check (goal model, S&P 500 point-in-time, OOS): model top 10% hit 38.0% vs 32.4% for same-ADR, same-momentum stocks; return +3.19% vs +1.95% per trade.
- Bracket menu: in-sample best (return per month) is +30% / -5%. OOS top 10%: hit 16.0% (break-even 14%), +1.66% per trade, +1.95% per month held, vs +20/-10: hit 38.8%, +2.84%, +2.50%/month.
- Regime gate breadth (stocks above 50d) (skip high (> 71%), mid): 14.9% CAGR, -37% DD; point-in-time S&P 500 6.5%, -26%.
- Regime gate VIX level (skip 15-20, < 15): 23.9% CAGR, -27% DD; point-in-time S&P 500 12.6%, -31%.
- Regime gate VIX / VIX3M (skip < 0.9 (calm), > 1.0 (stress)): 16.5% CAGR, -34% DD; point-in-time S&P 500 7.8%, -30%.
- Regime gate SPY above 200d (skip yes): 10.7% CAGR, -27% DD; point-in-time S&P 500 5.4%, -21%.
- Regime gate QQQ above 10 & 20 SMA (skip yes): 20.8% CAGR, -37% DD; point-in-time S&P 500 -1.0%, -40%.
- Regime gate SPY 1-month return (skip -3..0%, > 3%): 13.6% CAGR, -46% DD; point-in-time S&P 500 8.7%, -27%.
- Regime gate SPY vs 21/50 SMA (skip above 21 & 50, above 50 only): 8.3% CAGR, -51% DD; point-in-time S&P 500 4.1%, -31%.
- Regime gate QQQ vs 21/50 SMA (skip above 21 & 50): 15.4% CAGR, -29% DD; point-in-time S&P 500 -2.1%, -48%.
- Regime gate A/D line vs its 21/50 MA (skip above 21 & 50, above 50 only): 14.3% CAGR, -35% DD; point-in-time S&P 500 6.9%, -23%.
- Regime gate % of stocks above 20d (skip 40-60%, > 60%): 13.8% CAGR, -36% DD; point-in-time S&P 500 2.7%, -33%.
- Regime gate % above 50d, 10-day change (skip flat): 22.8% CAGR, -34% DD; point-in-time S&P 500 11.5%, -30%.
- Regime gate A/D line, 10-day change (skip flat, rising): 11.0% CAGR, -40% DD; point-in-time S&P 500 2.7%, -33%.
- Regime gate sector & sub-industry today green (skip both, one of the two): 20.5% CAGR, -48% DD; point-in-time S&P 500 -1.3%, -37%.
- Regime gate sector & sub-industry up over 5 days (skip both): 20.6% CAGR, -40% DD; point-in-time S&P 500 7.3%, -32%.
- Regime gate sector & sub-industry above 21 EMA (skip both, one of the two): 23.4% CAGR, -40% DD; point-in-time S&P 500 3.7%, -31%.
- Regime gate distance above the 21 EMA (skip 0-5%, 5-10%, > 15%): 11.7% CAGR, -51% DD; point-in-time S&P 500 14.1%, -28%.
- Regime gate ADR% (skip < 3%): 23.1% CAGR, -40% DD; point-in-time S&P 500 15.2%, -33%.
- Regime gate ADR% (only stocks trading >= $10M/day) (skip < 3%): 21.4% CAGR, -42% DD; point-in-time S&P 500 15.2%, -32%.
- Regime gate fundamental inflection (all 4) (skip no, yes): 15.5% CAGR, -25% DD; point-in-time S&P 500 4.1%, -12%.
- Regime gate revenue growth accelerating (skip 1 quarter, no (decelerating)): 20.3% CAGR, -40% DD; point-in-time S&P 500 10.1%, -27%.
- Regime gate operating income outgrowing revenue (skip no, yes): 16.8% CAGR, -41% DD; point-in-time S&P 500 14.3%, -21%.
- Regime gate operating margin vs a year ago (skip expanding, shrinking): 16.1% CAGR, -41% DD; point-in-time S&P 500 14.3%, -21%.
- Regime gate FCF margin vs a year ago (skip improving, worse): 15.5% CAGR, -31% DD; point-in-time S&P 500 5.4%, -13%.
- Regime gate up/down volume, 50 days (skip 1.0-1.3, > 1.3 (accumulation)): 15.8% CAGR, -41% DD; point-in-time S&P 500 12.8%, -29%.
- Regime gate price vs 200-day (skip 0-10% above, 10-30% above, 30-50% above, > 50% above): 23.6% CAGR, -39% DD; point-in-time S&P 500 16.1%, -28%.
- Regime gate 6-month gain (skip 0-20%, 20-50%, 50-100%, > 100%): 26.1% CAGR, -36% DD; point-in-time S&P 500 13.5%, -31%.
- Regime gate sector (11 GICS, by median RS) (skip bottom 3, top 3 (leading)): 24.3% CAGR, -52% DD; point-in-time S&P 500 7.2%, -44%.
- Regime gate sub-industry (by median RS) (skip middle, top 30% (leading)): 21.4% CAGR, -50% DD; point-in-time S&P 500 9.2%, -31%.
- Regime gate 3-day market model (skip rest): 6.7% CAGR, -7% DD; point-in-time S&P 500 1.3%, -5%.
- Filter RULE: top 3 sectors only: 21.4% CAGR, -30% DD; point-in-time S&P 500 5.8%, -27%.
- Filter RULE: top 30% sub-industries only: 24.6% CAGR, -25% DD; point-in-time S&P 500 13.0%, -23%.
- Filter RULE: top 3 sectors AND top 30% sub-industries: 19.5% CAGR, -27% DD; point-in-time S&P 500 2.9%, -17%.
- Filter RULE: SPY above its 21 & 50 SMA: 23.8% CAGR, -34% DD; point-in-time S&P 500 17.2%, -23%.
- Filter RULE: QQQ above its 21 & 50 SMA: 19.1% CAGR, -30% DD; point-in-time S&P 500 16.8%, -22%.
- Filter RULE: SPY above its 50 SMA (21 either way): 22.3% CAGR, -40% DD; point-in-time S&P 500 14.5%, -31%.
- Filter RULE: A/D line above its 21 & 50 MA: 17.3% CAGR, -40% DD; point-in-time S&P 500 13.2%, -24%.
- Filter RULE: > 50% of stocks above their 50d: 13.4% CAGR, -38% DD; point-in-time S&P 500 11.1%, -29%.
- Filter RULE: % above 50d rising over 10 days: 19.8% CAGR, -43% DD; point-in-time S&P 500 12.3%, -26%.
- Filter RULE: sector AND sub-industry green today: 16.5% CAGR, -37% DD; point-in-time S&P 500 13.3%, -23%.
- Filter RULE: sector AND sub-industry up over 5 days: 10.5% CAGR, -43% DD; point-in-time S&P 500 10.8%, -33%.
- Filter RULE: sector AND sub-industry above 21 EMA: 13.9% CAGR, -36% DD; point-in-time S&P 500 15.9%, -23%.
- Filter RULE: SPY > 21 & 50 + sector & sub-industry up 5 days: 14.2% CAGR, -30% DD; point-in-time S&P 500 10.1%, -14%.
- Filter RULE: <= 10% above the 21 EMA (course rule): 21.4% CAGR, -45% DD; point-in-time S&P 500 11.7%, -32%.
- Filter RULE: ADR% >= 5% (the infographic's minimum): 21.7% CAGR, -55% DD; point-in-time S&P 500 11.7%, -25%.
- Filter RULE: ADR% 5-12% (the infographic's sweet spot): 21.6% CAGR, -52% DD; point-in-time S&P 500 11.4%, -26%.
- Filter RULE: ADR% <= 15% (skip the wildest): 26.9% CAGR, -45% DD; point-in-time S&P 500 10.7%, -33%.
- Filter RULE: ADR% 5-12% and >= $10M/day: 17.4% CAGR, -56% DD; point-in-time S&P 500 11.4%, -26%.
- Filter RULE: fundamental inflection (rev accel 2q + op leverage + margin + FCF up): 19.2% CAGR, -25% DD; point-in-time S&P 500 1.8%, -19%.
- Filter RULE: revenue growth accelerating 2+ quarters: 33.9% CAGR, -35% DD; point-in-time S&P 500 9.6%, -26%.
- Filter RULE: accumulation (up/down volume 50d > 1): 14.1% CAGR, -43% DD; point-in-time S&P 500 3.7%, -33%.
- Filter RULE: not extended (< 30% above the 200-day): 23.4% CAGR, -42% DD; point-in-time S&P 500 15.1%, -31%.
- Filter RULE: not already up 50%+ in 6 months: 27.8% CAGR, -45% DD; point-in-time S&P 500 16.0%, -31%.
- Filter RULE: price rules only (accumulation + not extended + not up 50%): 21.0% CAGR, -45% DD; point-in-time S&P 500 5.2%, -38%.
- Filter RULE: user's full method (inflection + price rules): 4.8% CAGR, -14% DD; point-in-time S&P 500 -0.6%, -16%.
- Filter METHOD: user's method alone, no model (inflection + price rules): 9.8% CAGR, -26% DD; point-in-time S&P 500 2.2%, -20%.
- Filter METHOD: fundamental inflection alone, no model: 11.2% CAGR, -38% DD; point-in-time S&P 500 8.9%, -27%.
- Filter MODEL + fundamentals as features, top 10%: 28.7% CAGR, -44% DD; point-in-time S&P 500 11.3%, -38%.
- Filter SIZE: position scaled by 6% / ADR (x0.4-1.5): 21.4% CAGR, -35% DD; point-in-time S&P 500 16.3%, -32%.
- Regime gate (no gate) (skip nothing): 27.0% CAGR, -40% DD; point-in-time S&P 500 10.5%, -33%.

**Next steps for the strategy:**

1. Loosen the definitions of htf or widen the universe so they can be evaluated.
2. Drop or rework: high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2.
3. Focus development on: ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle (tune them on IS data only, re-check OOS).
4. Make qull_scan_regime a default filter.
5. Inspect rates_rising and above_52w_low: plot avgR by bucket and consider a hard rule.
6. ML is weak here: prefer simple rules, or add new information (fundamentals, sector/theme, earnings dates).
7. Build the scan around rs80_early_theme first; entries are the second layer.
8. Turn that rule into a scan filter and test it as its own strategy.
9. Use the superperformer score in the daily scan to choose which stocks to watch for setups.

**Run history** (each run should move these numbers):

| run_utc          | commit   |   tickers |   signals |   rank_corr |   top20_oos |   baseline_oos | edge_entries                                                                                                                                                                                                                                                                                | no_edge_entries                                                            | best_exit   | helpful_filters                                                                                              |   ml_auc |   ml_rank_corr |   ml_monotonic |   ml_gap | top_features                                                       | filters_lifting_baseline                  |   rules_held | best_portfolio                                                                    |   best_cagr |   spy_cagr | best_calmar                                                                       |   super_auc |   super_lift | super_features                                                  |   goal_b10_top_hit |   goal_b10_top_ret |   goal_b20_top_hit |   goal_b20_top_ret | menu_choice   |   menu_choice_oos_ret |
|:-----------------|:---------|----------:|----------:|------------:|------------:|---------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:------------|:-------------------------------------------------------------------------------------------------------------|---------:|---------------:|---------------:|---------:|:-------------------------------------------------------------------|:------------------------------------------|-------------:|:----------------------------------------------------------------------------------|------------:|-----------:|:----------------------------------------------------------------------------------|------------:|-------------:|:----------------------------------------------------------------|-------------------:|-------------------:|-------------------:|-------------------:|:--------------|----------------------:|
| 2026-10-08 14:27 | e7af2f7  |      1488 |    659965 |        0.54 |        0.06 |          -0.04 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                                                                                      | high52, multi_touch, pocket_pivot, stage2                                  | sma50_close | rs80_early, rs80_early_theme, early_stage, rs80                                                              |     0.51 |           0.00 |          -0.30 |     0.02 | rates_rising, sma200_slope, above_52w_low, sector_rs, adr_pct      | early_stage, rs80_early, rs80_early_theme |            2 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5163 signals) / sma50_close |        0.83 |         4.28 | adr_pct, above_52w_low, dist_52w_high, leg2_range, atr_pct      |               0.56 |               0.02 |               0.38 |               0.03 | nan           |                nan    |
| 2026-10-08 15:56 | f522ebc  |      1488 |    669685 |        0.51 |        0.06 |          -0.02 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, falling_wedge, ep_gap5, ep_gap10, undercut, donchian_20, ep_gap10_vol2, ema_retest, sym_triangle, donchian_55                                                                                                      | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.04 |     0.04 | sma200_slope, rates_rising, sector_rs, industry_rs, sma150_slope   | early_stage, rs80_early, rs80_early_theme |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.46 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5238 signals) / sma50_close |        0.83 |         4.29 | adr_pct, dist_52w_high, above_52w_low, atr_pct, mkt_above200    |               0.55 |               0.01 |               0.37 |               0.02 | nan           |                nan    |
| 2026-10-09 05:05 | 00c2b0a  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                                                          | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok              | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | nan           |                nan    |
| 2026-10-09 11:57 | 4ad9589  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                                                          | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok              | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 12:54 | 5ce3166  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                                                          | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok              | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 14:16 | e1db28d  |      1488 |    669336 |        0.51 |        0.06 |          -0.01 | ep_gap15, ep_gap10_vol5, desc_triangle, ep_gap8_hold, ep_gap8_neglected, ep_gap10, ep_gap5, falling_wedge, sym_triangle, ep_gap10_vol2, undercut, donchian_20, ema_retest, flag_60                                                                                                          | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | sma50_close | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage                                       |     0.51 |           0.01 |          -0.36 |     0.01 | sma200_slope, adr_pct, above_52w_low, rs_rank, mkt_ok              | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.47 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (5316 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 15:34 | 246a119  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-09 16:26 | c39a032  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-10 02:25 | 404aae3  |      1488 |    880290 |        0.49 |        0.06 |          -0.02 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, ep_gap5, ep_gap10, wf_rocket_gap, falling_wedge, sym_triangle, ep_gap10_vol2, wf_rocket_breakout, donchian_20, undercut, wf_scan_pullback, ema_retest, flag_60, wf_scan_base                                       | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green       |     0.51 |           0.01 |          -0.16 |     0.03 | sma200_slope, above_52w_low, rates_rising, adr_pct, industry_rs    | early_stage, rs80_early_theme             |            1 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.43 |       0.15 | SURVIVORSHIP S&P 500 names, all dates, top 10% model (7203 signals) / sma50_close |        0.83 |         4.21 | adr_pct, dist_52w_high, above_52w_low, mkt_above200, leg1_range |               0.53 |               0.01 |               0.37 |               0.02 | +20% / -15%   |                  0.04 |
| 2026-10-10 13:16 | 7a7fe02  |      1540 |    952523 |        0.48 |        0.06 |          -0.01 | ep_gap15, ep_gap8_hold, ep_gap10_vol5, ep_gap8_neglected, desc_triangle, tc_supertrend_ema, ep_gap5, wf_rocket_gap, ep_gap10, falling_wedge, ep_gap10_vol2, wf_rocket_breakout, tc_ema_cross_base, donchian_20, undercut, wf_scan_pullback, ema_retest, wf_scan_base, flag_60, sym_triangle | high52, multi_touch, pocket_pivot, qull_breakout, qull_breakout_60, stage2 | wf_weekly10 | qull_scan_regime, rs80_early, qull_scan, rs80_early_theme, early_stage, wf_scan_green, wf_rocket_green, rs80 |     0.51 |           0.01 |          -0.26 |     0.01 | rates_rising, above_52w_low, sma200_slope, sector_rs, sma150_slope | rs80_early_theme                          |            2 | RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%           |        0.34 |       0.15 | REGIME 3-day market model: skip ['rest'] / +20% -10%                              |        0.83 |         4.22 | adr_pct, dist_52w_high, above_52w_low, atr_pct, leg2_range      |               0.52 |               0.01 |               0.37 |               0.02 | +30% / -5%    |                  0.02 |

## 1. Did picking the best in-sample strategies work out-of-sample?

|                               |    value |
|:------------------------------|---------:|
| strategies_tested             | 7995.000 |
| strategies_with_enough_trades | 6316.000 |
| rank_corr_IS_vs_OOS_avgR      |    0.477 |
| rank_corr_IS_vs_OOS_t         |    0.523 |
| OOS_avgR_all_strategies       |    0.053 |
| OOS_avgR_top20_by_IS          |    0.063 |
| OOS_avgR_top20_by_IS_avgR     |    0.397 |
| OOS_avgR_random_baseline      |   -0.005 |
| share_top20_positive_OOS      |    1.000 |

If the rank correlation is near 0, in-sample winners were mostly luck. If the top 20 by in-sample beat the average and the random baseline out-of-sample, the selection carries real information.

## 2. Robust strategies (IS t >= 3 and OOS t >= 2)

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  70493 |      0.18 |  44.56 |   67602 |      7711.31 |      0.47 |       0.09 |     1.18 |   19.13 |         676.33 |
| wf_scan_pullback | all           | bracket_20_10 |  71784 |      0.18 |  44.41 |   69683 |      7948.69 |      0.47 |       0.09 |     1.18 |   19.57 |         706.61 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70886 |      0.15 |  43.42 |   67602 |      7711.31 |      0.54 |       0.06 |     1.14 |   16.54 |         467.24 |
| wf_scan_pullback | all           | bracket_10_10 |  72182 |      0.14 |  43.29 |   69683 |      7948.69 |      0.54 |       0.06 |     1.14 |   16.66 |         479.11 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  61584 |      0.17 |  38.67 |   58697 |      6695.53 |      0.48 |       0.12 |     1.25 |   23.32 |         772.99 |
| donchian_20      | all           | bracket_20_10 |  69887 |      0.16 |  38.18 |   79170 |      9030.87 |      0.45 |       0.07 |     1.14 |   16.32 |         651.40 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61977 |      0.13 |  37.63 |   58697 |      6695.53 |      0.55 |       0.08 |     1.20 |   20.96 |         551.33 |
| pocket_pivot     | all           | bracket_20_10 |  48750 |      0.19 |  37.44 |   48603 |      5544.11 |      0.46 |       0.06 |     1.12 |   11.28 |         340.94 |
| pocket_pivot     | all           | bracket_10_10 |  49158 |      0.15 |  37.22 |   48603 |      5544.11 |      0.53 |       0.05 |     1.11 |   10.71 |         259.60 |
| donchian_20      | all           | bracket_10_10 |  70332 |      0.13 |  36.53 |   79170 |      9030.87 |      0.53 |       0.05 |     1.11 |   13.46 |         423.84 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57900 |      0.17 |  36.01 |   62453 |      7123.97 |      0.45 |       0.07 |     1.14 |   14.39 |         511.84 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  50442 |      0.17 |  35.49 |   47644 |      5434.72 |      0.46 |       0.07 |     1.15 |   13.56 |         403.66 |
| donchian_20      | mkt_ok        | bracket_10_10 |  58298 |      0.13 |  34.16 |   62453 |      7123.97 |      0.53 |       0.05 |     1.11 |   11.91 |         334.43 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50782 |      0.13 |  33.83 |   47644 |      5434.72 |      0.53 |       0.05 |     1.12 |   11.39 |         271.11 |
| wf_scan_base     | all           | bracket_20_10 |  31850 |      0.19 |  33.65 |   24901 |      2840.44 |      0.47 |       0.04 |     1.09 |    6.04 |         120.07 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  36204 |      0.15 |  33.52 |   32420 |      3698.13 |      0.53 |       0.05 |     1.11 |    9.01 |         176.04 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35886 |      0.19 |  33.11 |   32420 |      3698.13 |      0.46 |       0.06 |     1.13 |    9.39 |         226.48 |
| donchian_20      | wf_scan       | bracket_20_10 |  43259 |      0.17 |  32.68 |   41455 |      4728.74 |      0.45 |       0.05 |     1.11 |    9.29 |         258.37 |
| wf_scan_base     | all           | bracket_10_10 |  32068 |      0.16 |  32.59 |   24901 |      2840.44 |      0.53 |       0.04 |     1.09 |    6.20 |         103.13 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35471 |      0.18 |  32.14 |   34101 |      3889.88 |      0.46 |       0.06 |     1.11 |    8.77 |         220.82 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  25134 |      0.20 |  31.93 |   17538 |      2000.55 |      0.48 |       0.04 |     1.09 |    4.75 |          76.34 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35823 |      0.15 |  31.79 |   34101 |      3889.88 |      0.53 |       0.05 |     1.11 |    8.78 |         178.25 |
| donchian_20      | wf_scan       | bracket_10_10 |  43561 |      0.14 |  31.75 |   41455 |      4728.74 |      0.53 |       0.03 |     1.07 |    6.63 |         147.68 |
| donchian_55      | all           | bracket_20_10 |  47692 |      0.16 |  31.68 |   51411 |      5864.42 |      0.45 |       0.06 |     1.11 |   10.47 |         331.82 |
| donchian_55      | all           | bracket_10_10 |  48051 |      0.13 |  31.46 |   51411 |      5864.42 |      0.53 |       0.03 |     1.07 |    7.02 |         176.18 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25309 |      0.16 |  30.93 |   17538 |      2000.55 |      0.54 |       0.04 |     1.11 |    6.23 |          85.31 |
| donchian_20      | early_stage   | bracket_20_10 |  36869 |      0.19 |  30.72 |   47847 |      5457.88 |      0.45 |       0.09 |     1.18 |   16.17 |         509.67 |
| undercut         | all           | bracket_20_10 |  23149 |      0.23 |  29.53 |   26660 |      3041.09 |      0.47 |       0.13 |     1.26 |   16.43 |         383.17 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23380 |      0.21 |  29.52 |   25951 |      2960.21 |      0.47 |       0.10 |     1.21 |   13.41 |         296.07 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  27122 |      0.18 |  29.47 |   19864 |      2265.87 |      0.47 |       0.03 |     1.07 |    4.30 |          76.72 |

## 3. Top 30 strategies chosen on in-sample t-stat, with their out-of-sample results

| entry            | filter        | exit          |   IS_n |   IS_avgR |   IS_t |   OOS_n |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:--------------|:--------------|-------:|----------:|-------:|--------:|----------:|-----------:|---------:|--------:|
| wf_scan_pullback | wf_scan       | bracket_20_10 |  70493 |      0.18 |  44.56 |   67602 |      0.47 |       0.09 |     1.18 |   19.13 |
| wf_scan_pullback | all           | bracket_20_10 |  71784 |      0.18 |  44.41 |   69683 |      0.47 |       0.09 |     1.18 |   19.57 |
| wf_scan_pullback | wf_scan       | bracket_10_10 |  70886 |      0.15 |  43.42 |   67602 |      0.54 |       0.06 |     1.14 |   16.54 |
| wf_scan_pullback | all           | bracket_10_10 |  72182 |      0.14 |  43.29 |   69683 |      0.54 |       0.06 |     1.14 |   16.66 |
| wf_scan_pullback | wf_scan_green | bracket_20_10 |  61584 |      0.17 |  38.67 |   58697 |      0.48 |       0.12 |     1.25 |   23.32 |
| donchian_20      | all           | bracket_20_10 |  69887 |      0.16 |  38.18 |   79170 |      0.45 |       0.07 |     1.14 |   16.32 |
| wf_scan_pullback | wf_scan_green | bracket_10_10 |  61977 |      0.13 |  37.63 |   58697 |      0.55 |       0.08 |     1.20 |   20.96 |
| pocket_pivot     | all           | bracket_20_10 |  48750 |      0.19 |  37.44 |   48603 |      0.46 |       0.06 |     1.12 |   11.28 |
| pocket_pivot     | all           | bracket_10_10 |  49158 |      0.15 |  37.22 |   48603 |      0.53 |       0.05 |     1.11 |   10.71 |
| donchian_20      | all           | bracket_10_10 |  70332 |      0.13 |  36.53 |   79170 |      0.53 |       0.05 |     1.11 |   13.46 |
| donchian_20      | mkt_ok        | bracket_20_10 |  57900 |      0.17 |  36.01 |   62453 |      0.45 |       0.07 |     1.14 |   14.39 |
| wf_scan_pullback | mkt_ok        | bracket_20_10 |  50442 |      0.17 |  35.49 |   47644 |      0.46 |       0.07 |     1.15 |   13.56 |
| donchian_20      | mkt_ok        | bracket_10_10 |  58298 |      0.13 |  34.16 |   62453 |      0.53 |       0.05 |     1.11 |   11.91 |
| wf_scan_pullback | mkt_ok        | bracket_10_10 |  50782 |      0.13 |  33.83 |   47644 |      0.53 |       0.05 |     1.12 |   11.39 |
| wf_scan_base     | all           | bracket_20_10 |  31850 |      0.19 |  33.65 |   24901 |      0.47 |       0.04 |     1.09 |    6.04 |
| pocket_pivot     | wf_scan       | bracket_10_10 |  36204 |      0.15 |  33.52 |   32420 |      0.53 |       0.05 |     1.11 |    9.01 |
| pocket_pivot     | wf_scan       | bracket_20_10 |  35886 |      0.19 |  33.11 |   32420 |      0.46 |       0.06 |     1.13 |    9.39 |
| donchian_20      | wf_scan       | bracket_20_10 |  43259 |      0.17 |  32.68 |   41455 |      0.45 |       0.05 |     1.11 |    9.29 |
| wf_scan_base     | all           | bracket_10_10 |  32068 |      0.16 |  32.59 |   24901 |      0.53 |       0.04 |     1.09 |    6.20 |
| pocket_pivot     | mkt_ok        | bracket_20_10 |  35471 |      0.18 |  32.14 |   34101 |      0.46 |       0.06 |     1.11 |    8.77 |
| wf_scan_base     | wf_scan       | bracket_20_10 |  25134 |      0.20 |  31.93 |   17538 |      0.48 |       0.04 |     1.09 |    4.75 |
| pocket_pivot     | mkt_ok        | bracket_10_10 |  35823 |      0.15 |  31.79 |   34101 |      0.53 |       0.05 |     1.11 |    8.78 |
| donchian_20      | wf_scan       | bracket_10_10 |  43561 |      0.14 |  31.75 |   41455 |      0.53 |       0.03 |     1.07 |    6.63 |
| donchian_55      | all           | bracket_20_10 |  47692 |      0.16 |  31.68 |   51411 |      0.45 |       0.06 |     1.11 |   10.47 |
| donchian_55      | all           | bracket_10_10 |  48051 |      0.13 |  31.46 |   51411 |      0.53 |       0.03 |     1.07 |    7.02 |
| wf_scan_base     | wf_scan       | bracket_10_10 |  25309 |      0.16 |  30.93 |   17538 |      0.54 |       0.04 |     1.11 |    6.23 |
| donchian_20      | early_stage   | bracket_20_10 |  36869 |      0.19 |  30.72 |   47847 |      0.45 |       0.09 |     1.18 |   16.17 |
| undercut         | all           | bracket_20_10 |  23149 |      0.23 |  29.53 |   26660 |      0.47 |       0.13 |     1.26 |   16.43 |
| wf_scan_pullback | early_stage   | bracket_20_10 |  23380 |      0.21 |  29.52 |   25951 |      0.47 |       0.10 |     1.21 |   13.41 |
| wf_scan_base     | mkt_ok        | bracket_20_10 |  27122 |      0.18 |  29.47 |   19864 |      0.47 |       0.03 |     1.07 |    4.30 |

## 4. Each entry with its best in-sample exit/filter

| entry              | filter           | exit          |   IS_n |   IS_per_yr |   IS_win |   IS_avgR |   IS_t |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |   OOS_R_per_yr |
|:-------------------|:-----------------|:--------------|-------:|------------:|---------:|----------:|-------:|--------:|-------------:|----------:|-----------:|---------:|--------:|---------------:|
| ep_gap15           | rs80_mkt         | bracket_20_10 |     68 |        5.67 |     0.54 |      0.54 |   3.17 |     152 |        17.34 |      0.45 |       0.24 |     1.42 |    2.02 |           4.08 |
| flag_30            | rs80_early_theme | bracket_20_10 |    135 |       11.26 |     0.50 |      0.33 |   2.71 |     216 |        24.64 |      0.43 |       0.22 |     1.38 |    2.17 |           5.40 |
| flag_30_early      | wf_scan_green    | bracket_20_10 |    583 |       48.61 |     0.43 |      0.18 |   3.03 |    1035 |       118.06 |      0.43 |       0.19 |     1.33 |    4.19 |          21.99 |
| falling_wedge      | all              | bracket_20_10 |   1264 |      105.38 |     0.58 |      0.30 |   9.18 |    1532 |       174.75 |      0.48 |       0.17 |     1.37 |    5.34 |          29.31 |
| ep_gap8_neglected  | wf_scan_green    | bracket_10_10 |    165 |       13.76 |     0.69 |      0.35 |   5.10 |     213 |        24.30 |      0.58 |       0.16 |     1.40 |    2.38 |           3.84 |
| ep_gap10_vol5      | wf_scan_green    | bracket_10_10 |    145 |       12.09 |     0.66 |      0.30 |   3.87 |     181 |        20.65 |      0.59 |       0.16 |     1.39 |    2.17 |           3.26 |
| ep_gap10_vol2      | wf_scan_green    | bracket_10_10 |    219 |       18.26 |     0.63 |      0.25 |   3.83 |     399 |        45.51 |      0.58 |       0.15 |     1.36 |    3.02 |           6.80 |
| ep_gap10           | wf_scan_green    | bracket_10_10 |    202 |       16.84 |     0.62 |      0.23 |   3.43 |     332 |        37.87 |      0.58 |       0.14 |     1.33 |    2.58 |           5.28 |
| tc_supertrend_ema  | all              | bracket_20_10 |  18968 |     1581.39 |     0.53 |      0.21 |  24.55 |   23177 |      2643.78 |      0.47 |       0.14 |     1.28 |   16.43 |         364.97 |
| undercut           | all              | bracket_20_10 |  23149 |     1929.96 |     0.54 |      0.23 |  29.53 |   26660 |      3041.09 |      0.47 |       0.13 |     1.26 |   16.43 |         383.17 |
| desc_triangle      | all              | bracket_20_10 |    775 |       64.61 |     0.57 |      0.24 |   6.28 |     713 |        81.33 |      0.48 |       0.11 |     1.24 |    2.46 |           8.75 |
| wf_scan_pullback   | wf_scan          | bracket_20_10 |  70493 |     5877.10 |     0.54 |      0.18 |  44.56 |   67602 |      7711.31 |      0.47 |       0.09 |     1.18 |   19.13 |         676.33 |
| flag_60            | rs80_theme       | bracket_20_10 |    145 |       12.09 |     0.48 |      0.35 |   2.85 |     259 |        29.54 |      0.39 |       0.09 |     1.13 |    0.93 |           2.59 |
| base_25            | mkt_ok           | bracket_20_10 |   1506 |      125.56 |     0.47 |      0.15 |   4.47 |    1917 |       218.67 |      0.42 |       0.09 |     1.15 |    2.78 |          19.06 |
| ep_gap5            | wf_scan_green    | bracket_10_10 |    859 |       71.62 |     0.63 |      0.23 |   7.13 |     922 |       105.17 |      0.56 |       0.08 |     1.19 |    2.61 |           8.89 |
| ep_gap8_hold       | wf_scan_green    | bracket_10_10 |    303 |       25.26 |     0.64 |      0.26 |   4.74 |     436 |        49.73 |      0.55 |       0.08 |     1.18 |    1.68 |           3.98 |
| sym_triangle       | all              | bracket_10_10 |    885 |       73.78 |     0.57 |      0.12 |   3.59 |     925 |       105.51 |      0.55 |       0.08 |     1.19 |    2.45 |           8.19 |
| ema_retest         | all              | bracket_20_10 |  14510 |     1209.72 |     0.55 |      0.19 |  21.03 |   15872 |      1810.51 |      0.46 |       0.08 |     1.15 |    7.87 |         137.43 |
| donchian_20        | all              | bracket_20_10 |  69887 |     5826.58 |     0.52 |      0.16 |  38.18 |   79170 |      9030.87 |      0.45 |       0.07 |     1.14 |   16.32 |         651.40 |
| pocket_pivot       | all              | bracket_20_10 |  48750 |     4064.35 |     0.54 |      0.19 |  37.44 |   48603 |      5544.11 |      0.46 |       0.06 |     1.12 |   11.28 |         340.94 |
| donchian_55        | all              | bracket_20_10 |  47692 |     3976.15 |     0.53 |      0.16 |  31.68 |   51411 |      5864.42 |      0.45 |       0.06 |     1.11 |   10.47 |         331.82 |
| asc_triangle       | all              | bracket_20_10 |   1097 |       91.46 |     0.56 |      0.19 |   6.18 |     873 |        99.58 |      0.46 |       0.06 |     1.12 |    1.43 |           5.63 |
| random_uptrend     | all              | bracket_10_10 |  31055 |     2589.10 |     0.59 |      0.15 |  28.15 |   34706 |      3958.89 |      0.54 |       0.06 |     1.13 |   10.60 |         220.10 |
| wf_rocket_gap      | wf_scan_green    | bracket_10_10 |   1251 |      104.30 |     0.60 |      0.19 |   7.06 |    1478 |       168.59 |      0.54 |       0.05 |     1.11 |    2.00 |           8.56 |
| qull_breakout_60   | wf_scan_green    | bracket_10_10 |    354 |       29.51 |     0.56 |      0.14 |   2.31 |     998 |       113.84 |      0.53 |       0.05 |     1.10 |    1.46 |           5.58 |
| qull_breakout      | wf_scan_green    | bracket_10_10 |    904 |       75.37 |     0.57 |      0.14 |   4.02 |    2007 |       228.94 |      0.53 |       0.05 |     1.10 |    2.07 |          11.06 |
| wf_scan_base       | all              | bracket_20_10 |  31850 |     2655.38 |     0.57 |      0.19 |  33.65 |   24901 |      2840.44 |      0.47 |       0.04 |     1.09 |    6.04 |         120.07 |
| wf_rocket_breakout | all              | bracket_10_10 |   2433 |      202.84 |     0.61 |      0.17 |   8.97 |    2521 |       287.57 |      0.54 |       0.04 |     1.09 |    2.07 |          11.48 |
| tc_ema_cross_base  | all              | bracket_20_10 |   7374 |      614.78 |     0.54 |      0.17 |  13.67 |    6955 |       793.35 |      0.45 |       0.03 |     1.07 |    2.50 |          27.60 |
| high52_fresh       | all              | bracket_10_10 |   8213 |      684.73 |     0.61 |      0.17 |  16.94 |    8509 |       970.62 |      0.53 |       0.03 |     1.07 |    3.08 |          31.22 |
| high52             | all              | bracket_10_10 |  30219 |     2519.40 |     0.59 |      0.14 |  26.57 |   29496 |      3364.59 |      0.52 |       0.02 |     1.05 |    3.79 |          71.26 |
| base_50            | all              | bracket_10_10 |   2341 |      195.17 |     0.56 |      0.11 |   5.17 |    2714 |       309.58 |      0.52 |       0.02 |     1.04 |    0.99 |           5.92 |
| rising_wedge       | all              | bracket_10_10 |   2108 |      175.75 |     0.58 |      0.12 |   6.49 |    1763 |       201.10 |      0.52 |       0.02 |     1.04 |    0.82 |           3.72 |
| tight_coil_7       | all              | bracket_10_10 |   6385 |      532.33 |     0.59 |      0.15 |  13.30 |    5418 |       618.03 |      0.52 |       0.01 |     1.03 |    1.06 |           8.67 |
| vcp                | wf_scan          | bracket_20_10 |   1174 |       97.88 |     0.55 |      0.18 |   5.76 |     725 |        82.70 |      0.45 |       0.01 |     1.02 |    0.26 |           0.89 |
| multi_touch        | all              | bracket_10_10 |  12631 |     1053.06 |     0.59 |      0.14 |  16.77 |   10761 |      1227.50 |      0.51 |       0.00 |     1.00 |    0.09 |           0.98 |
| stage2             | all              | bracket_10_10 |   6000 |      500.23 |     0.61 |      0.18 |  15.56 |    4905 |       559.51 |      0.51 |      -0.00 |     0.99 |   -0.32 |          -2.44 |
| tc_ema200_2nd      | mkt_ok           | bracket_10_10 |    761 |       63.45 |     0.57 |      0.12 |   3.62 |    1073 |       122.40 |      0.50 |      -0.01 |     0.99 |   -0.18 |          -0.66 |
| tc_reversal_base   | mkt_ok           | bracket_10_10 |    153 |       12.76 |     0.72 |      0.45 |   5.59 |     134 |        15.29 |      0.50 |      -0.02 |     0.96 |   -0.25 |          -0.35 |
| tight_coil_15      | wf_scan          | bracket_10_10 |    892 |       74.37 |     0.62 |      0.19 |   6.44 |     688 |        78.48 |      0.49 |      -0.04 |     0.92 |   -1.10 |          -3.15 |
| htf                | all              | sma50_close   |     53 |        4.42 |     0.17 |      0.39 |   0.63 |     102 |        11.64 |      0.11 |      -0.36 |     0.63 |   -1.27 |          -4.19 |

## 5. Does the entry beat random entries? (OOS avgR minus baseline, same exit, no filter)

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |           -0.04 |           -0.03 |              0.05 |             0.07 |          0.02 |           0.09 |         0.07 |         0.04 |         0.01 |          0.01 |       0.09 |        0.03 |         -0.02 |
| base_25            |           -0.02 |            0.02 |              0.10 |             0.07 |          0.08 |           0.08 |         0.09 |         0.04 |         0.06 |          0.21 |       0.12 |        0.18 |          0.20 |
| base_50            |           -0.04 |            0.00 |              0.14 |             0.09 |          0.12 |           0.10 |         0.11 |         0.07 |         0.10 |          0.20 |       0.14 |        0.17 |          0.20 |
| desc_triangle      |            0.03 |            0.02 |              0.25 |             0.23 |          0.20 |           0.21 |         0.25 |         0.15 |         0.20 |          0.04 |       0.18 |        0.05 |          0.12 |
| donchian_20        |           -0.01 |           -0.02 |              0.09 |             0.08 |          0.08 |           0.11 |         0.09 |         0.08 |         0.08 |          0.06 |       0.10 |        0.06 |          0.05 |
| donchian_55        |           -0.03 |           -0.03 |              0.06 |             0.05 |          0.06 |           0.08 |         0.06 |         0.06 |         0.06 |          0.06 |       0.10 |        0.05 |          0.03 |
| ema_retest         |           -0.01 |           -0.01 |              0.07 |             0.05 |          0.06 |           0.08 |         0.08 |         0.07 |         0.05 |          0.07 |       0.10 |        0.07 |          0.05 |
| ep_gap10           |           -0.03 |            0.01 |              0.22 |             0.33 |          0.24 |           0.19 |         0.14 |         0.10 |         0.16 |          0.48 |       0.29 |        0.41 |          0.50 |
| ep_gap10_vol2      |           -0.03 |            0.05 |              0.28 |             0.34 |          0.24 |           0.18 |         0.19 |         0.12 |         0.17 |          0.48 |       0.29 |        0.42 |          0.52 |
| ep_gap10_vol5      |           -0.06 |            0.03 |              0.23 |             0.31 |          0.20 |           0.18 |         0.11 |         0.08 |         0.10 |          0.49 |       0.31 |        0.40 |          0.47 |
| ep_gap15           |            0.02 |            0.13 |              0.28 |             0.32 |          0.24 |           0.24 |         0.27 |         0.11 |         0.14 |          0.70 |       0.36 |        0.59 |          0.77 |
| ep_gap5            |           -0.03 |           -0.01 |              0.14 |             0.17 |          0.14 |           0.12 |         0.10 |         0.09 |         0.11 |          0.19 |       0.15 |        0.17 |          0.18 |
| ep_gap8_hold       |           -0.03 |            0.01 |              0.16 |             0.25 |          0.19 |           0.15 |         0.13 |         0.08 |         0.12 |          0.37 |       0.24 |        0.32 |          0.37 |
| ep_gap8_neglected  |           -0.03 |           -0.02 |              0.12 |             0.17 |          0.20 |           0.17 |         0.17 |         0.10 |         0.12 |          0.27 |       0.22 |        0.27 |          0.28 |
| falling_wedge      |            0.05 |            0.08 |              0.20 |             0.16 |          0.09 |           0.20 |         0.24 |         0.06 |         0.09 |          0.01 |       0.07 |        0.02 |         -0.01 |
| flag_30            |           -0.04 |            0.02 |              0.04 |             0.10 |          0.10 |           0.05 |         0.02 |         0.07 |         0.07 |          0.23 |       0.12 |        0.17 |          0.19 |
| flag_30_early      |            0.02 |            0.11 |              0.21 |             0.20 |          0.20 |           0.17 |         0.25 |         0.16 |         0.16 |          0.30 |       0.20 |        0.28 |          0.43 |
| flag_60            |           -0.06 |            0.06 |              0.16 |             0.14 |          0.14 |           0.08 |         0.09 |         0.11 |         0.10 |          0.49 |       0.27 |        0.35 |          0.35 |
| high52             |           -0.03 |           -0.05 |             -0.04 |            -0.05 |         -0.04 |          -0.03 |        -0.04 |        -0.03 |        -0.04 |         -0.05 |      -0.03 |       -0.04 |         -0.07 |
| high52_fresh       |           -0.02 |           -0.04 |              0.06 |             0.04 |          0.07 |           0.05 |         0.05 |         0.05 |         0.04 |          0.06 |       0.07 |        0.06 |          0.04 |
| htf                |           -0.26 |           -0.18 |             -0.22 |            -0.32 |         -0.16 |          -0.17 |        -0.20 |        -0.01 |        -0.10 |         -0.34 |      -0.10 |       -0.29 |         -0.33 |
| multi_touch        |           -0.06 |           -0.08 |             -0.03 |            -0.01 |         -0.03 |           0.00 |        -0.03 |         0.02 |        -0.01 |         -0.06 |      -0.01 |       -0.05 |         -0.08 |
| pocket_pivot       |           -0.01 |           -0.03 |             -0.02 |            -0.03 |         -0.02 |           0.00 |        -0.03 |         0.01 |        -0.01 |         -0.05 |      -0.01 |       -0.05 |         -0.06 |
| qull_breakout      |           -0.02 |            0.05 |             -0.09 |            -0.09 |         -0.09 |          -0.14 |        -0.11 |        -0.14 |        -0.12 |          0.04 |      -0.09 |       -0.02 |         -0.00 |
| qull_breakout_60   |           -0.01 |            0.09 |             -0.09 |            -0.09 |         -0.07 |          -0.12 |        -0.06 |        -0.14 |        -0.12 |          0.14 |      -0.09 |        0.06 |          0.03 |
| rising_wedge       |           -0.04 |           -0.04 |             -0.03 |            -0.05 |         -0.04 |           0.04 |         0.01 |         0.07 |         0.03 |         -0.08 |      -0.00 |       -0.05 |         -0.10 |
| stage2             |           -0.06 |           -0.08 |             -0.07 |            -0.07 |         -0.06 |          -0.02 |        -0.08 |        -0.03 |        -0.04 |         -0.11 |      -0.06 |       -0.10 |         -0.13 |
| sym_triangle       |            0.02 |            0.01 |              0.17 |             0.12 |          0.13 |           0.17 |         0.16 |         0.13 |         0.15 |          0.03 |       0.10 |        0.05 |          0.04 |
| tc_ema200_2nd      |           -0.04 |           -0.06 |              0.08 |             0.09 |          0.04 |           0.09 |         0.07 |         0.09 |         0.07 |         -0.00 |       0.06 |        0.00 |         -0.04 |
| tc_ema_cross_base  |           -0.02 |           -0.06 |              0.09 |             0.10 |          0.09 |           0.12 |         0.10 |         0.10 |         0.10 |          0.06 |       0.13 |        0.07 |          0.04 |
| tc_reversal_base   |           -0.01 |           -0.04 |              0.07 |             0.06 |         -0.04 |           0.12 |         0.05 |        -0.01 |        -0.00 |         -0.05 |       0.07 |       -0.04 |         -0.07 |
| tc_supertrend_ema  |            0.04 |            0.05 |              0.20 |             0.18 |          0.14 |           0.21 |         0.19 |         0.14 |         0.15 |          0.05 |       0.12 |        0.06 |          0.07 |
| tight_coil_15      |           -0.07 |           -0.10 |              0.00 |            -0.03 |         -0.00 |           0.06 |        -0.01 |         0.06 |         0.04 |         -0.10 |       0.02 |       -0.07 |         -0.12 |
| tight_coil_7       |           -0.04 |           -0.06 |              0.01 |             0.01 |          0.03 |           0.07 |         0.03 |         0.07 |         0.05 |         -0.02 |       0.06 |       -0.01 |         -0.02 |
| undercut           |            0.03 |            0.04 |              0.18 |             0.17 |          0.01 |           0.08 |         0.13 |         0.09 |         0.09 |         -0.01 |       0.02 |       -0.01 |          0.04 |
| vcp                |           -0.00 |           -0.04 |              0.06 |             0.05 |          0.04 |           0.10 |         0.05 |         0.07 |         0.07 |         -0.06 |       0.04 |       -0.03 |         -0.10 |
| wf_rocket_breakout |           -0.02 |           -0.04 |              0.08 |             0.09 |          0.09 |           0.11 |         0.07 |         0.10 |         0.09 |          0.08 |       0.13 |        0.08 |          0.06 |
| wf_rocket_gap      |            0.02 |            0.08 |              0.24 |             0.26 |          0.23 |           0.18 |         0.24 |         0.14 |         0.18 |          0.30 |       0.25 |        0.27 |          0.31 |
| wf_scan_base       |           -0.02 |           -0.05 |              0.09 |             0.07 |          0.08 |           0.10 |         0.08 |         0.09 |         0.09 |          0.02 |       0.10 |        0.03 |         -0.00 |
| wf_scan_pullback   |            0.01 |           -0.00 |              0.10 |             0.08 |          0.06 |           0.11 |         0.10 |         0.08 |         0.08 |          0.03 |       0.09 |        0.04 |          0.02 |

Same, in-sample:

| entry              |   bracket_10_10 |   bracket_20_10 |   chandelier_3atr |   donchian_10low |   ema21_close |   fixed_3r_20d |   oneil_20_8 |   qull_sma10 |   qull_sma20 |   sma50_close |   trim_ema |   wf_rocket |   wf_weekly10 |
|:-------------------|----------------:|----------------:|------------------:|-----------------:|--------------:|---------------:|-------------:|-------------:|-------------:|--------------:|-----------:|------------:|--------------:|
| asc_triangle       |            0.00 |            0.01 |              0.05 |            -0.01 |          0.06 |           0.08 |         0.08 |         0.06 |         0.04 |          0.00 |       0.11 |        0.03 |          0.01 |
| base_25            |           -0.06 |           -0.05 |             -0.00 |            -0.01 |          0.03 |           0.09 |        -0.02 |         0.08 |         0.06 |          0.06 |       0.11 |        0.05 |          0.07 |
| base_50            |           -0.04 |           -0.05 |              0.02 |             0.02 |          0.05 |           0.14 |         0.00 |         0.10 |         0.07 |         -0.01 |       0.11 |        0.01 |         -0.03 |
| desc_triangle      |            0.05 |            0.06 |              0.19 |             0.30 |          0.17 |           0.20 |         0.22 |         0.17 |         0.18 |          0.23 |       0.27 |        0.23 |          0.30 |
| donchian_20        |           -0.02 |           -0.02 |              0.11 |             0.12 |          0.15 |           0.15 |         0.12 |         0.11 |         0.11 |          0.12 |       0.18 |        0.13 |          0.14 |
| donchian_55        |           -0.02 |           -0.02 |              0.09 |             0.10 |          0.13 |           0.13 |         0.10 |         0.09 |         0.09 |          0.11 |       0.17 |        0.12 |          0.12 |
| ema_retest         |            0.00 |            0.01 |              0.09 |             0.09 |          0.13 |           0.12 |         0.17 |         0.06 |         0.07 |          0.15 |       0.14 |        0.16 |          0.17 |
| ep_gap10           |           -0.03 |           -0.00 |              0.15 |             0.10 |          0.15 |           0.11 |        -0.04 |         0.14 |         0.10 |          0.17 |       0.23 |        0.14 |          0.11 |
| ep_gap10_vol2      |           -0.05 |           -0.04 |              0.13 |             0.07 |          0.12 |           0.10 |        -0.04 |         0.10 |         0.07 |          0.12 |       0.18 |        0.10 |          0.07 |
| ep_gap10_vol5      |            0.03 |            0.06 |              0.23 |             0.18 |          0.19 |           0.20 |         0.04 |         0.22 |         0.18 |          0.28 |       0.33 |        0.25 |          0.17 |
| ep_gap15           |            0.07 |            0.13 |              0.42 |             0.32 |          0.34 |           0.31 |         0.12 |         0.32 |         0.30 |          0.42 |       0.49 |        0.38 |          0.31 |
| ep_gap5            |           -0.02 |           -0.03 |              0.17 |             0.13 |          0.17 |           0.15 |         0.09 |         0.14 |         0.13 |          0.24 |       0.23 |        0.21 |          0.23 |
| ep_gap8_hold       |           -0.01 |            0.02 |              0.23 |             0.21 |          0.24 |           0.19 |         0.13 |         0.17 |         0.16 |          0.28 |       0.32 |        0.27 |          0.27 |
| ep_gap8_neglected  |            0.01 |            0.05 |              0.25 |             0.24 |          0.24 |           0.18 |         0.18 |         0.15 |         0.18 |          0.29 |       0.28 |        0.29 |          0.30 |
| falling_wedge      |            0.07 |            0.12 |              0.35 |             0.37 |          0.24 |           0.30 |         0.41 |         0.23 |         0.23 |          0.13 |       0.21 |        0.14 |          0.25 |
| flag_30            |           -0.14 |           -0.15 |             -0.09 |            -0.09 |         -0.05 |           0.05 |        -0.10 |         0.03 |        -0.02 |         -0.09 |       0.02 |       -0.07 |         -0.14 |
| flag_30_early      |           -0.09 |           -0.09 |              0.13 |             0.11 |          0.13 |           0.06 |        -0.01 |         0.07 |         0.10 |          0.03 |       0.05 |        0.04 |          0.04 |
| flag_60            |           -0.13 |           -0.12 |              0.07 |             0.05 |          0.08 |           0.12 |        -0.01 |         0.15 |         0.10 |          0.10 |       0.13 |        0.11 |          0.01 |
| high52             |           -0.01 |           -0.02 |             -0.02 |            -0.03 |          0.03 |           0.02 |        -0.01 |        -0.01 |        -0.01 |         -0.02 |       0.01 |       -0.01 |         -0.03 |
| high52_fresh       |            0.02 |            0.02 |              0.06 |             0.06 |          0.10 |           0.08 |         0.09 |         0.04 |         0.05 |          0.08 |       0.09 |        0.09 |          0.06 |
| htf                |           -0.23 |           -0.16 |             -0.08 |             0.24 |          0.13 |           0.06 |        -0.08 |         0.12 |         0.19 |          0.43 |       0.28 |        0.25 |          0.41 |
| multi_touch        |           -0.01 |           -0.02 |              0.07 |             0.10 |          0.13 |           0.10 |         0.12 |         0.07 |         0.07 |          0.12 |       0.12 |        0.13 |          0.12 |
| pocket_pivot       |            0.00 |            0.00 |              0.06 |             0.06 |          0.08 |           0.04 |         0.07 |         0.03 |         0.03 |          0.07 |       0.06 |        0.07 |          0.09 |
| qull_breakout      |           -0.15 |           -0.17 |             -0.32 |            -0.32 |         -0.25 |          -0.20 |        -0.34 |        -0.17 |        -0.20 |         -0.35 |      -0.22 |       -0.32 |         -0.36 |
| qull_breakout_60   |           -0.15 |           -0.17 |             -0.22 |            -0.26 |         -0.21 |          -0.22 |        -0.31 |        -0.15 |        -0.18 |         -0.26 |      -0.17 |       -0.24 |         -0.29 |
| rising_wedge       |           -0.02 |           -0.04 |              0.00 |             0.02 |          0.07 |           0.08 |         0.02 |         0.04 |         0.04 |          0.03 |       0.11 |        0.03 |          0.04 |
| stage2             |            0.03 |            0.03 |              0.12 |             0.14 |          0.17 |           0.12 |         0.18 |         0.08 |         0.10 |          0.16 |       0.16 |        0.17 |          0.15 |
| sym_triangle       |           -0.03 |           -0.06 |              0.06 |             0.07 |          0.12 |           0.08 |         0.00 |         0.11 |         0.08 |          0.04 |       0.11 |        0.03 |          0.03 |
| tc_ema200_2nd      |           -0.05 |           -0.07 |              0.09 |             0.12 |          0.15 |           0.17 |         0.08 |         0.14 |         0.13 |          0.06 |       0.16 |        0.07 |          0.08 |
| tc_ema_cross_base  |           -0.01 |           -0.01 |              0.12 |             0.14 |          0.16 |           0.14 |         0.15 |         0.12 |         0.12 |          0.15 |       0.23 |        0.15 |          0.17 |
| tc_reversal_base   |            0.25 |            0.29 |              0.25 |             0.29 |          0.29 |           0.41 |         0.48 |         0.31 |         0.23 |          0.33 |       0.41 |        0.32 |          0.33 |
| tc_supertrend_ema  |            0.00 |            0.03 |              0.22 |             0.23 |          0.20 |           0.24 |         0.22 |         0.17 |         0.18 |          0.10 |       0.20 |        0.10 |          0.15 |
| tight_coil_15      |            0.01 |           -0.00 |              0.14 |             0.18 |          0.14 |           0.16 |         0.17 |         0.13 |         0.12 |          0.13 |       0.24 |        0.13 |          0.18 |
| tight_coil_7       |            0.01 |            0.00 |              0.13 |             0.17 |          0.16 |           0.16 |         0.14 |         0.11 |         0.11 |          0.17 |       0.23 |        0.17 |          0.19 |
| undercut           |            0.02 |            0.05 |              0.22 |             0.23 |          0.06 |           0.13 |         0.22 |         0.19 |         0.18 |          0.01 |       0.09 |        0.02 |          0.09 |
| vcp                |           -0.02 |           -0.02 |              0.07 |             0.08 |          0.12 |           0.13 |         0.11 |         0.10 |         0.09 |          0.09 |       0.17 |        0.09 |          0.11 |
| wf_rocket_breakout |            0.02 |            0.03 |              0.13 |             0.14 |          0.19 |           0.21 |         0.15 |         0.14 |         0.15 |          0.15 |       0.24 |        0.16 |          0.15 |
| wf_rocket_gap      |           -0.03 |           -0.04 |              0.13 |             0.10 |          0.14 |           0.14 |         0.09 |         0.13 |         0.12 |          0.15 |       0.20 |        0.14 |          0.11 |
| wf_scan_base       |            0.01 |            0.01 |              0.11 |             0.13 |          0.17 |           0.17 |         0.15 |         0.14 |         0.14 |          0.11 |       0.21 |        0.11 |          0.12 |
| wf_scan_pullback   |           -0.00 |           -0.00 |              0.15 |             0.16 |          0.15 |           0.18 |         0.14 |         0.13 |         0.13 |          0.10 |       0.18 |        0.10 |          0.12 |

## 6. Exit plans (averaged over all entries, no filter)

| exit            |   IS_avgR |   OOS_avgR |   OOS_win |   OOS_pf |   OOS_beats_baseline_share |
|:----------------|----------:|-----------:|----------:|---------:|---------------------------:|
| wf_weekly10     |      0.08 |       0.10 |      0.26 |     1.14 |                       0.62 |
| sma50_close     |      0.07 |       0.09 |      0.27 |     1.13 |                       0.70 |
| bracket_20_10   |      0.17 |       0.09 |      0.44 |     1.16 |                       0.45 |
| wf_rocket       |      0.07 |       0.06 |      0.27 |     1.10 |                       0.70 |
| oneil_20_8      |      0.14 |       0.04 |      0.28 |     1.06 |                       0.80 |
| bracket_10_10   |      0.13 |       0.03 |      0.53 |     1.08 |                       0.23 |
| trim_ema        |      0.02 |       0.01 |      0.34 |     1.03 |                       0.80 |
| donchian_10low  |      0.03 |       0.01 |      0.30 |     1.03 |                       0.78 |
| chandelier_3atr |      0.04 |       0.00 |      0.30 |     1.01 |                       0.80 |
| fixed_3r_20d    |      0.01 |      -0.01 |      0.38 |     1.01 |                       0.88 |
| ema21_close     |     -0.03 |      -0.02 |      0.30 |     0.97 |                       0.75 |
| qull_sma20      |     -0.04 |      -0.03 |      0.43 |     0.94 |                       0.80 |
| qull_sma10      |     -0.04 |      -0.04 |      0.43 |     0.92 |                       0.85 |

## 7. Filters (averaged over all entry x exit combinations)

| filter           |   IS_avgR |   OOS_avgR |   OOS_win |
|:-----------------|----------:|-----------:|----------:|
| qull_scan_regime |     -0.01 |       0.15 |      0.34 |
| rs80_early       |      0.11 |       0.14 |      0.37 |
| qull_scan        |     -0.02 |       0.11 |      0.34 |
| rs80_early_theme |      0.08 |       0.10 |      0.36 |
| early_stage      |      0.08 |       0.08 |      0.36 |
| wf_scan_green    |      0.06 |       0.07 |      0.36 |
| wf_rocket_green  |      0.04 |       0.06 |      0.35 |
| rs80             |      0.06 |       0.06 |      0.35 |
| wf_rocket        |      0.01 |       0.05 |      0.35 |
| rs80_mkt         |      0.08 |       0.05 |      0.35 |
| wf_scan          |      0.06 |       0.04 |      0.35 |
| rs80_theme       |      0.05 |       0.04 |      0.35 |
| all              |      0.05 |       0.03 |      0.35 |
| theme            |      0.05 |       0.02 |      0.35 |
| mkt_ok           |      0.06 |       0.02 |      0.34 |

## 8. ML meta-labeling (exit: bracket_20_10, chosen in-sample; walk-forward, yearly retrain)

The model predicts R (clipped (-2.0, 8.0)). Out-of-sample rank correlation with realized R: 0.006; AUC for R > 0: 0.506 (0.5 = no skill). Taken (model's top third, causal threshold): n=124,071, avgR=0.083, win=0.462. Skipped: n=321,413, avgR=0.072, win=0.451.

Out-of-sample avgR by predicted-probability decile (0 = lowest):

|   prob |        n |   avgR |   win |
|-------:|---------:|-------:|------:|
|      0 | 44549.00 |   0.10 |  0.45 |
|      1 | 44552.00 |   0.08 |  0.45 |
|      2 | 44545.00 |   0.06 |  0.44 |
|      3 | 44548.00 |   0.08 |  0.45 |
|      4 | 44548.00 |   0.08 |  0.46 |
|      5 | 44548.00 |   0.06 |  0.45 |
|      6 | 44549.00 |   0.07 |  0.46 |
|      7 | 44548.00 |   0.06 |  0.45 |
|      8 | 44548.00 |   0.06 |  0.45 |
|      9 | 44549.00 |   0.10 |  0.47 |

Per entry (OOS):

| entry_name         |    n_all |   avgR_all |   n_taken |   avgR_taken |   avgR_skipped |
|:-------------------|---------:|-----------:|----------:|-------------:|---------------:|
| ep_gap15           |   391.00 |       0.22 |    206.00 |         0.31 |           0.12 |
| wf_rocket_gap      |  4033.00 |       0.17 |   1271.00 |         0.30 |           0.11 |
| flag_60            |   640.00 |       0.15 |    165.00 |         0.25 |           0.11 |
| base_25            |  2489.00 |       0.11 |    661.00 |         0.25 |           0.06 |
| base_50            |  2714.00 |       0.09 |    740.00 |         0.24 |           0.04 |
| qull_breakout_60   |  1942.00 |       0.19 |    454.00 |         0.23 |           0.17 |
| falling_wedge      |  1532.00 |       0.17 |    524.00 |         0.22 |           0.14 |
| ep_gap10_vol2      |  1216.00 |       0.14 |    483.00 |         0.20 |           0.10 |
| ep_gap10           |   962.00 |       0.10 |    408.00 |         0.20 |           0.04 |
| ep_gap5            |  2381.00 |       0.08 |    867.00 |         0.19 |           0.02 |
| flag_30            |  1847.00 |       0.11 |    463.00 |         0.19 |           0.08 |
| tc_reversal_base   |   160.00 |       0.05 |     47.00 |         0.17 |           0.00 |
| ep_gap8_hold       |  1213.00 |       0.10 |    477.00 |         0.16 |           0.07 |
| undercut           | 26660.00 |       0.13 |   9517.00 |         0.16 |           0.11 |
| ep_gap8_neglected  |   955.00 |       0.07 |    368.00 |         0.14 |           0.03 |
| ep_gap10_vol5      |   471.00 |       0.12 |    222.00 |         0.14 |           0.10 |
| qull_breakout      |  4543.00 |       0.14 |   1008.00 |         0.12 |           0.15 |
| flag_30_early      |  2002.00 |       0.20 |    454.00 |         0.12 |           0.23 |
| wf_rocket_breakout |  2521.00 |       0.05 |    782.00 |         0.10 |           0.03 |
| tc_supertrend_ema  | 23177.00 |       0.14 |   8437.00 |         0.10 |           0.16 |
| tight_coil_15      |  1047.00 |      -0.00 |    299.00 |         0.09 |          -0.04 |
| vcp                |   887.00 |       0.05 |    203.00 |         0.09 |           0.04 |
| wf_scan_pullback   | 69683.00 |       0.09 |  19174.00 |         0.08 |           0.09 |
| ema_retest         | 15872.00 |       0.08 |   4613.00 |         0.08 |           0.07 |
| high52_fresh       |  8509.00 |       0.05 |   2307.00 |         0.08 |           0.05 |
| multi_touch        | 10761.00 |       0.01 |   2917.00 |         0.08 |          -0.02 |
| high52             | 29496.00 |       0.04 |   6989.00 |         0.07 |           0.03 |
| wf_scan_base       | 24901.00 |       0.04 |   6105.00 |         0.06 |           0.04 |
| pocket_pivot       | 48603.00 |       0.06 |  13144.00 |         0.06 |           0.06 |
| tight_coil_7       |  5418.00 |       0.03 |   1431.00 |         0.06 |           0.02 |
| donchian_20        | 79170.00 |       0.07 |  21060.00 |         0.05 |           0.08 |
| donchian_55        | 51411.00 |       0.06 |  13056.00 |         0.05 |           0.06 |
| stage2             |  4905.00 |       0.01 |   1491.00 |         0.05 |          -0.01 |
| desc_triangle      |   713.00 |       0.11 |    222.00 |         0.04 |           0.14 |
| rising_wedge       |  1763.00 |       0.05 |    484.00 |         0.04 |           0.05 |
| sym_triangle       |   925.00 |       0.10 |    235.00 |         0.03 |           0.13 |
| tc_ema_cross_base  |  6955.00 |       0.03 |   2013.00 |         0.00 |           0.05 |
| tc_ema200_2nd      |  1641.00 |       0.03 |    508.00 |        -0.02 |           0.05 |
| asc_triangle       |   873.00 |       0.06 |    246.00 |        -0.03 |           0.09 |
| htf                |   102.00 |      -0.09 |     20.00 |        -0.13 |          -0.08 |

- Same model on episodic pivots only / sma50_close: rank corr 0.018, taken avgR 0.507 (n=3,402) vs skipped 0.196 (n=4,187).
- Same model on your trim plan (trim_ema): rank corr 0.109, taken avgR 0.017 (n=127,902) vs skipped -0.042 (n=317,582).

What the model relies on (permutation importance: drop in OOS rank correlation when a feature is shuffled):

| feature              |   rank_corr_drop |
|:---------------------|-----------------:|
| rates_rising         |           0.0085 |
| above_52w_low        |           0.0074 |
| sma200_slope         |           0.0068 |
| sector_rs            |           0.0058 |
| sma150_slope         |           0.0040 |
| adr_pct              |           0.0039 |
| industry_rs          |           0.0031 |
| rs_rank              |           0.0030 |
| base_count           |           0.0025 |
| mkt_ok               |           0.0019 |
| mkt_ret_21           |           0.0018 |
| gap                  |           0.0016 |
| dist_sma50           |           0.0011 |
| ext_ema8_adr         |           0.0008 |
| ret_126              |           0.0006 |
| close_in_range_20    |           0.0004 |
| close_std_10         |           0.0004 |
| closes_below_e21_10  |           0.0004 |
| distribution_days_25 |           0.0002 |
| contraction_ratio    |           0.0002 |

Readable rules (depth-3 tree fit in-sample, scored out-of-sample):

| rule                                                                  |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|----------:|
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 > 0.554    |  12212 |      0.61 |   16802 |       0.08 |      0.47 |
| rates_rising > 0.5 AND mkt_ema_stack <= 0.5 AND breadth_50 <= 0.554   |  30786 |      0.33 |   48868 |       0.13 |      0.48 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low <= 0.429 |  85926 |      0.30 |   66680 |       0.01 |      0.47 |
| rates_rising <= 0.5 AND qqq_ret_21 <= 0.0297 AND breadth_50 > 0.647   |  38869 |      0.26 |   59444 |       0.09 |      0.45 |
| rates_rising > 0.5 AND mkt_ema_stack > 0.5 AND above_52w_low > 0.429  |  89004 |      0.18 |   63411 |      -0.00 |      0.42 |
| rates_rising <= 0.5 AND qqq_ret_21 <= 0.0297 AND breadth_50 <= 0.647  |  73014 |      0.08 |   68489 |       0.14 |      0.47 |
| rates_rising <= 0.5 AND qqq_ret_21 > 0.0297 AND mkt_ret_21 > 0.0141   |  91633 |      0.04 |  117377 |       0.08 |      0.45 |
| rates_rising <= 0.5 AND qqq_ret_21 > 0.0297 AND mkt_ret_21 <= 0.0141  |   6361 |     -0.47 |    4413 |       0.14 |      0.45 |

## 10. Superperformer model: what do stocks look like BEFORE a +40% move in 3 months?

Every stock every 10 trading days (n=284,804 out-of-sample rows). Base rate of a >= 40% gain within 3 months: 7.2%. The model's top 10% hit it 30.4% of the time (4.2x the base rate). AUC 0.834.

|   super_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28481.000 |      0.002 |          -0.006 |              0.009 |              0.069 |
|            1 | 28480.000 |      0.004 |           0.008 |              0.013 |              0.048 |
|            2 | 28480.000 |      0.009 |           0.016 |              0.018 |              0.051 |
|            3 | 28481.000 |      0.016 |           0.021 |              0.021 |              0.056 |
|            4 | 28480.000 |      0.027 |           0.028 |              0.026 |              0.061 |
|            5 | 28480.000 |      0.043 |           0.034 |              0.030 |              0.071 |
|            6 | 28481.000 |      0.064 |           0.042 |              0.036 |              0.081 |
|            7 | 28480.000 |      0.096 |           0.047 |              0.037 |              0.103 |
|            8 | 28480.000 |      0.157 |           0.064 |              0.043 |              0.124 |
|            9 | 28481.000 |      0.304 |           0.110 |              0.066 |              0.158 |

What matters most (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| adr_pct       |     0.0997 |
| dist_52w_high |     0.0273 |
| above_52w_low |     0.0268 |
| atr_pct       |     0.0064 |
| leg2_range    |     0.0055 |
| mkt_above200  |     0.0045 |
| leg1_range    |     0.0045 |
| qull_rank     |     0.0035 |
| tight_10      |     0.0017 |
| sma200_slope  |     0.0012 |
| base_depth_60 |     0.0012 |
| base_count    |     0.0010 |
| close_std_10  |     0.0007 |
| leg3_range    |     0.0006 |
| dist_ema21    |     0.0006 |

Profile: future superperformers vs everything else, at the moment of the sample:

|               |   future superperformers (median) |   everything else (median) |
|:--------------|----------------------------------:|---------------------------:|
| adr_pct       |                             0.045 |                      0.026 |
| dist_52w_high |                            -0.281 |                     -0.128 |
| above_52w_low |                             0.593 |                      0.341 |
| atr_pct       |                             0.047 |                      0.027 |
| leg2_range    |                             0.195 |                      0.120 |
| mkt_above200  |                             1.000 |                      1.000 |
| leg1_range    |                             0.186 |                      0.120 |
| qull_rank     |                             0.789 |                      0.709 |
| tight_10      |                             0.153 |                      0.087 |
| sma200_slope  |                             0.000 |                      0.009 |
| base_depth_60 |                             0.337 |                      0.204 |
| base_count    |                             0.000 |                      1.000 |

Readable rules (depth-3 tree fit before 2018, scored after):

| rule                                                                  |   IS_n |   IS_rate |   OOS_n |   OOS_rate |
|:----------------------------------------------------------------------|-------:|----------:|--------:|-----------:|
| dist_52w_high <= -0.518 AND dist_52w_high <= -0.626                   |   2310 |     0.459 |    1030 |      0.433 |
| dist_52w_high <= -0.518 AND dist_52w_high > -0.626                    |   3685 |     0.258 |    1861 |      0.290 |
| dist_52w_high > -0.518 AND adr_pct > 0.0321 AND above_52w_low > 1.05  |   8344 |     0.145 |    5904 |      0.241 |
| dist_52w_high > -0.518 AND adr_pct > 0.0321 AND above_52w_low <= 1.05 |  36781 |     0.066 |   18434 |      0.126 |
| dist_52w_high > -0.518 AND adr_pct <= 0.0321 AND adr_pct > 0.0252     |  34202 |     0.027 |   18150 |      0.040 |
| dist_52w_high > -0.518 AND adr_pct <= 0.0321 AND adr_pct <= 0.0252    | 114678 |     0.006 |   34621 |      0.009 |

Stricter label, +40% BEFORE a -20% drop (so plain volatility doesn't count): base rate 6.8%, model top 10% 27.7% (4.1x), AUC 0.826.

|   clean_prob |         n |   hit_rate |   avg_3m_return |   median_3m_return |   share_down_20pct |
|-------------:|----------:|-----------:|----------------:|-------------------:|-------------------:|
|            0 | 28481.000 |      0.001 |          -0.006 |              0.009 |              0.067 |
|            1 | 28480.000 |      0.006 |           0.011 |              0.016 |              0.049 |
|            2 | 28480.000 |      0.010 |           0.017 |              0.017 |              0.049 |
|            3 | 28481.000 |      0.016 |           0.022 |              0.022 |              0.057 |
|            4 | 28480.000 |      0.026 |           0.028 |              0.026 |              0.061 |
|            5 | 28480.000 |      0.039 |           0.035 |              0.032 |              0.069 |
|            6 | 28481.000 |      0.060 |           0.039 |              0.033 |              0.083 |
|            7 | 28480.000 |      0.095 |           0.050 |              0.039 |              0.101 |
|            8 | 28480.000 |      0.151 |           0.063 |              0.043 |              0.125 |
|            9 | 28481.000 |      0.277 |           0.105 |              0.061 |              0.160 |

### Your goal: +10% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 50% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28481.000 |       0.268 |        0.399 |      0.345 |            0.005 |           0.019 |
|       1 | 28480.000 |       0.352 |        0.447 |      0.347 |            0.009 |           0.037 |
|       2 | 28480.000 |       0.397 |        0.470 |      0.370 |            0.009 |           0.046 |
|       3 | 28481.000 |       0.431 |        0.479 |      0.391 |            0.007 |           0.050 |
|       4 | 28480.000 |       0.461 |        0.493 |      0.396 |            0.008 |           0.068 |
|       5 | 28480.000 |       0.489 |        0.511 |      0.397 |            0.010 |           0.098 |
|       6 | 28481.000 |       0.518 |        0.512 |      0.407 |            0.009 |           0.098 |
|       7 | 28480.000 |       0.550 |        0.521 |      0.407 |            0.010 |           0.098 |
|       8 | 28480.000 |       0.592 |        0.515 |      0.417 |            0.009 |           0.098 |
|       9 | 28481.000 |       0.682 |        0.518 |      0.432 |            0.007 |           0.098 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 284804.000 |        0.486 |      0.391 |            0.008 |
| top 10%    |  28481.000 |        0.518 |      0.432 |            0.007 |
| top 5%     |  14241.000 |        0.521 |      0.440 |            0.007 |
| top 2%     |   5697.000 |        0.552 |      0.426 |            0.011 |
| top 1%     |   2849.000 |        0.588 |      0.398 |            0.019 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97468.000 |        0.463 |      0.360 |            0.009 |
| top 10%    |  7387.000 |        0.525 |      0.397 |            0.011 |
| top 5%     |  3732.000 |        0.535 |      0.402 |            0.012 |
| top 2%     |  1541.000 |        0.571 |      0.398 |            0.016 |
| top 1%     |   790.000 |        0.606 |      0.377 |            0.023 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b10 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 14630.000 |       0.265 |        0.393 |      0.313 |            0.008 |           0.022 |
|       1 | 12657.000 |       0.352 |        0.427 |      0.323 |            0.010 |           0.034 |
|       2 | 11471.000 |       0.397 |        0.450 |      0.350 |            0.009 |           0.038 |
|       3 | 10056.000 |       0.431 |        0.460 |      0.366 |            0.008 |           0.040 |
|       4 |  9282.000 |       0.461 |        0.475 |      0.376 |            0.009 |           0.051 |
|       5 |  8706.000 |       0.489 |        0.486 |      0.384 |            0.009 |           0.059 |
|       6 |  8191.000 |       0.517 |        0.492 |      0.390 |            0.009 |           0.070 |
|       7 |  7590.000 |       0.550 |        0.509 |      0.381 |            0.011 |           0.098 |
|       8 |  7498.000 |       0.592 |        0.508 |      0.387 |            0.011 |           0.098 |
|       9 |  7387.000 |       0.683 |        0.525 |      0.397 |            0.011 |           0.098 |

### Your goal: +20% before -10% (daily chart, entry at the close, 63-day time limit)

Break-even hit rate is about 33% (before costs and timeouts). By decile of the model's probability, out-of-sample 2018+: how often the target came first, how often the -10% stop, and the average net return per trade (0.1% costs per side, timeouts included).

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 28481.000 |       0.045 |        0.062 |      0.331 |            0.002 |          -0.001 |
|       1 | 28480.000 |       0.081 |        0.114 |      0.362 |            0.008 |          -0.003 |
|       2 | 28480.000 |       0.111 |        0.145 |      0.401 |            0.008 |          -0.011 |
|       3 | 28481.000 |       0.143 |        0.178 |      0.431 |            0.009 |          -0.020 |
|       4 | 28480.000 |       0.176 |        0.221 |      0.455 |            0.012 |          -0.028 |
|       5 | 28480.000 |       0.211 |        0.258 |      0.476 |            0.015 |          -0.043 |
|       6 | 28481.000 |       0.248 |        0.292 |      0.497 |            0.017 |          -0.081 |
|       7 | 28480.000 |       0.288 |        0.322 |      0.518 |            0.018 |          -0.102 |
|       8 | 28480.000 |       0.338 |        0.345 |      0.537 |            0.019 |          -0.102 |
|       9 | 28481.000 |       0.443 |        0.371 |      0.545 |            0.022 |          -0.102 |

Higher confidence tiers (all stocks / point-in-time S&P 500):

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 284804.000 |        0.231 |      0.455 |            0.013 |
| top 10%    |  28481.000 |        0.371 |      0.545 |            0.022 |
| top 5%     |  14241.000 |        0.377 |      0.553 |            0.022 |
| top 2%     |   5697.000 |        0.388 |      0.559 |            0.022 |
| top 1%     |   2849.000 |        0.390 |      0.570 |            0.020 |

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97468.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5040.000 |        0.372 |      0.503 |            0.029 |
| top 5%     |  2556.000 |        0.386 |      0.518 |            0.028 |
| top 2%     |  1082.000 |        0.401 |      0.529 |            0.029 |
| top 1%     |   575.000 |        0.397 |      0.562 |            0.024 |

S&P 500 stocks only, and only after they joined the index (survivorship check):

|   p_b20 |         n |   predicted |   hit_target |   hit_stop |   avg_net_return |   median_return |
|--------:|----------:|------------:|-------------:|-----------:|-----------------:|----------------:|
|       0 | 17253.000 |       0.044 |        0.060 |      0.308 |            0.007 |           0.005 |
|       1 | 14716.000 |       0.080 |        0.109 |      0.346 |            0.011 |           0.002 |
|       2 | 12644.000 |       0.111 |        0.141 |      0.384 |            0.010 |          -0.005 |
|       3 | 11182.000 |       0.142 |        0.166 |      0.415 |            0.010 |          -0.013 |
|       4 |  9660.000 |       0.176 |        0.207 |      0.429 |            0.014 |          -0.014 |
|       5 |  8429.000 |       0.211 |        0.235 |      0.454 |            0.015 |          -0.027 |
|       6 |  7194.000 |       0.247 |        0.268 |      0.468 |            0.018 |          -0.031 |
|       7 |  6072.000 |       0.288 |        0.295 |      0.487 |            0.019 |          -0.051 |
|       8 |  5278.000 |       0.338 |        0.329 |      0.507 |            0.021 |          -0.102 |
|       9 |  5040.000 |       0.447 |        0.372 |      0.503 |            0.029 |          -0.102 |

Caution: the universe is today's index members, so beaten-down stocks in the sample are ones that survived. See the SURVIVORSHIP and CHECK rows in section 9.

Setup signals split by the model's score (OOS, exit bracket_20_10; last column sma50_close):

| super_prob   |          n |   avgR |   win |   avgR_sma50 |
|:-------------|-----------:|-------:|------:|-------------:|
| low          | 148496.000 |  0.008 | 0.481 |       -0.085 |
| mid          | 148493.000 |  0.072 | 0.455 |       -0.040 |
| high         | 148495.000 |  0.145 | 0.425 |        0.151 |

## 12. Short horizons: green day / next day / 3 days / week (out-of-sample 2018+)

Features: candle anatomy, gaps and fair value gaps, relative volume, round numbers / moving averages / swing support & resistance / 20-day trend line, completed-week structure, VIX (level, change, percentile, VIX/VIX3M), plus everything the earlier models use. Market-only = market + VIX + calendar features only. Retrained every 2 years. 'top/bottom' = actual up-rate in the model's highest/lowest 10%; spread = their difference in average return over the horizon.

| target                         | model   |   base rate |   AUC |   accuracy |   top 10% up |   bottom 10% up |   return spread |
|:-------------------------------|:--------|------------:|------:|-----------:|-------------:|----------------:|----------------:|
| next day green (close > open)  | all     |       0.493 | 0.519 |      0.514 |        0.527 |           0.474 |           0.007 |
| next day green (close > open)  | market  |       0.493 | 0.512 |      0.514 |        0.528 |           0.494 |           0.003 |
| up next day (close to close)   | all     |       0.500 | 0.508 |      0.503 |        0.539 |           0.498 |           0.003 |
| up next day (close to close)   | market  |       0.500 | 0.495 |      0.486 |        0.526 |           0.523 |          -0.001 |
| up over the next 3 days        | all     |       0.509 | 0.517 |      0.517 |        0.522 |           0.489 |           0.001 |
| up over the next 3 days        | market  |       0.509 | 0.531 |      0.522 |        0.592 |           0.444 |           0.011 |
| up over the next week (5 days) | all     |       0.514 | 0.508 |      0.512 |        0.478 |           0.538 |          -0.014 |
| up over the next week (5 days) | market  |       0.514 | 0.509 |      0.511 |        0.505 |           0.477 |          -0.003 |

Up over the next week, by decile of the full model:

|   s_up5 |          n |   predicted |   actual_up |   avg_return |
|--------:|-----------:|------------:|------------:|-------------:|
|       0 | 29274.0000 |      0.3579 |      0.5383 |       0.0045 |
|       1 | 29273.0000 |      0.4363 |      0.4843 |      -0.0008 |
|       2 | 29273.0000 |      0.4726 |      0.4858 |      -0.0009 |
|       3 | 29273.0000 |      0.4988 |      0.4965 |      -0.0001 |
|       4 | 29273.0000 |      0.5211 |      0.4972 |      -0.0002 |
|       5 | 29273.0000 |      0.5428 |      0.5086 |       0.0010 |
|       6 | 29273.0000 |      0.5654 |      0.5332 |       0.0035 |
|       7 | 29273.0000 |      0.5907 |      0.5587 |       0.0056 |
|       8 | 29273.0000 |      0.6241 |      0.5543 |       0.0061 |
|       9 | 29274.0000 |      0.7013 |      0.4783 |      -0.0095 |

What drives the 1-week prediction (permutation importance, drop in OOS AUC):

| feature       |   auc_drop |
|:--------------|-----------:|
| spy_ret_1     |     0.0160 |
| breadth_50    |     0.0068 |
| month         |     0.0047 |
| vix_chg_1     |     0.0024 |
| spy_ret_5     |     0.0015 |
| wk_ret_1      |     0.0013 |
| vix_chg_5     |     0.0013 |
| sector_rs     |     0.0009 |
| dist_sma50    |     0.0009 |
| rs_rank       |     0.0007 |
| atr_ratio     |     0.0005 |
| qqq_ok        |     0.0005 |
| mkt_above200  |     0.0005 |
| body_pct_prev |     0.0004 |
| leg2_range    |     0.0003 |

Do the new features improve the +20%/-10% goal model? (OOS tiers)

**original**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 284804.000 |        0.231 |      0.455 |            0.013 |
| top 10%    |  28481.000 |        0.371 |      0.545 |            0.022 |
| top 5%     |  14241.000 |        0.377 |      0.553 |            0.022 |
| top 2%     |   5697.000 |        0.388 |      0.559 |            0.022 |
| top 1%     |   2849.000 |        0.390 |      0.570 |            0.020 |

**with new features**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 284804.000 |        0.231 |      0.455 |            0.013 |
| top 10%    |  28481.000 |        0.385 |      0.526 |            0.027 |
| top 5%     |  14241.000 |        0.404 |      0.512 |            0.032 |
| top 2%     |   5697.000 |        0.452 |      0.474 |            0.045 |
| top 1%     |   2849.000 |        0.466 |      0.466 |            0.049 |

**with fundamentals**

| tier       |          n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|-----------:|-------------:|-----------:|-----------------:|
| all stocks | 284804.000 |        0.231 |      0.455 |            0.013 |
| top 10%    |  28481.000 |        0.392 |      0.523 |            0.029 |
| top 5%     |  14241.000 |        0.417 |      0.508 |            0.035 |
| top 2%     |   5697.000 |        0.456 |      0.484 |            0.044 |
| top 1%     |   2849.000 |        0.475 |      0.473 |            0.048 |

**with new features, point-in-time S&P 500**

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97468.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5437.000 |        0.371 |      0.488 |            0.031 |
| top 5%     |  2841.000 |        0.398 |      0.474 |            0.037 |
| top 2%     |  1220.000 |        0.454 |      0.434 |            0.051 |
| top 1%     |   622.000 |        0.457 |      0.441 |            0.051 |

**with fundamentals, point-in-time S&P 500**

| tier       |         n |   hit_target |   hit_stop |   avg_net_return |
|:-----------|----------:|-------------:|-----------:|-----------------:|
| all stocks | 97468.000 |        0.180 |      0.404 |            0.013 |
| top 10%    |  5078.000 |        0.382 |      0.486 |            0.033 |
| top 5%     |  2649.000 |        0.410 |      0.473 |            0.038 |
| top 2%     |  1092.000 |        0.460 |      0.442 |            0.051 |
| top 1%     |   565.000 |        0.485 |      0.446 |            0.053 |

## 16. Run 24: consolidated tests

### Earnings placebo: do gaps drift because of earnings news?
Gap setups split by whether an earnings release (SEC 8-K Item 2.02) was filed that day or up to 3 days before. If 'no earnings' gaps do as well, post-earnings drift is not the reason the setup works.

| group                    | earnings         |   IS_n |   OOS_n |   IS_avgR_sma50 |   OOS_avgR_sma50 |   IS_win_sma50 |   OOS_win_sma50 |   IS_avgR_b20 |   OOS_avgR_b20 |
|:-------------------------|:-----------------|-------:|--------:|----------------:|-----------------:|---------------:|----------------:|--------------:|---------------:|
| episodic pivots (ep_*)   | earnings release |   3512 |    5436 |           0.276 |            0.436 |          0.339 |           0.329 |         0.226 |          0.146 |
| episodic pivots (ep_*)   | no earnings      |   1561 |    2105 |           0.231 |            0.096 |          0.283 |           0.245 |         0.135 |          0.013 |
| gap >= 5% holding 2 days | earnings release |   1058 |    1263 |           0.107 |            0.135 |          0.323 |           0.315 |         0.130 |          0.087 |
| gap >= 5% holding 2 days | no earnings      |   1904 |    2739 |           0.162 |            0.341 |          0.315 |           0.322 |         0.168 |          0.207 |
| random entries           | earnings release |   1508 |    1652 |           0.045 |           -0.104 |          0.171 |           0.183 |         0.105 |          0.016 |
| random entries           | no earnings      |  30180 |   32821 |           0.070 |           -0.019 |          0.150 |           0.138 |         0.192 |          0.094 |

### Holding through earnings (course: don't, without a cushion)
Goal model top 10%, +20/-10, by days from entry to the next earnings release:

| next earnings in   |   IS_n |   OOS_n |   IS_hit |   OOS_hit |   IS_avg_ret |   OOS_avg_ret |
|:-------------------|-------:|--------:|---------:|----------:|-------------:|--------------:|
| <= 7 days          |   1632 |    2057 |    0.347 |     0.400 |        0.017 |         0.028 |
| 8-30 days          |   5600 |    7802 |    0.344 |     0.415 |        0.021 |         0.037 |
| 31-63 days         |   7071 |   10258 |    0.328 |     0.386 |        0.016 |         0.027 |
| > 63 days          |   6822 |    8049 |    0.304 |     0.368 |        0.011 |         0.023 |

### Survivorship: current members only vs incl. former S&P 500 members

| point-in-time S&P 500                     |   trades_OOS |   hit_OOS |   avg_ret_OOS |   CAGR |   max_DD |
|:------------------------------------------|-------------:|----------:|--------------:|-------:|---------:|
| current members only (as before)          |         3866 |     0.396 |         0.038 |  0.129 |   -0.261 |
| incl. former members (membership history) |         4597 |     0.380 |         0.032 |  0.105 |   -0.328 |

### Is the edge real? Year by year vs same-volatility, same-momentum stocks

|   year |    n |   hit |   matched_hit |   edge_hit |   edge_ret | sample                |
|-------:|-----:|------:|--------------:|-----------:|-----------:|:----------------------|
|   2008 | 1786 | 0.235 |         0.210 |      0.025 |      0.003 | full universe         |
|   2009 | 1626 | 0.381 |         0.385 |     -0.004 |      0.002 | full universe         |
|   2010 | 1753 | 0.475 |         0.346 |      0.130 |      0.030 | full universe         |
|   2011 | 1954 | 0.406 |         0.288 |      0.118 |      0.018 | full universe         |
|   2012 | 1918 | 0.400 |         0.340 |      0.061 |      0.012 | full universe         |
|   2013 | 2112 | 0.363 |         0.337 |      0.026 |     -0.002 | full universe         |
|   2014 | 2312 | 0.252 |         0.233 |      0.019 |     -0.008 | full universe         |
|   2015 | 2447 | 0.134 |         0.174 |     -0.040 |     -0.029 | full universe         |
|   2016 | 2561 | 0.347 |         0.332 |      0.015 |     -0.014 | full universe         |
|   2017 | 2739 | 0.334 |         0.311 |      0.023 |     -0.000 | full universe         |
|   2018 | 3000 | 0.262 |         0.269 |     -0.006 |     -0.009 | full universe         |
|   2019 | 3000 | 0.359 |         0.349 |      0.010 |     -0.004 | full universe         |
|   2020 | 3059 | 0.527 |         0.440 |      0.087 |      0.020 | full universe         |
|   2021 | 3275 | 0.386 |         0.303 |      0.083 |      0.018 | full universe         |
|   2022 | 3384 | 0.437 |         0.294 |      0.143 |      0.041 | full universe         |
|   2023 | 3448 | 0.333 |         0.331 |      0.002 |     -0.008 | full universe         |
|   2024 | 3686 | 0.381 |         0.335 |      0.046 |      0.008 | full universe         |
|   2025 | 3680 | 0.399 |         0.376 |      0.023 |      0.001 | full universe         |
|   2026 | 1953 | 0.439 |         0.388 |      0.052 |      0.013 | full universe         |
|   2008 |  473 | 0.216 |         0.211 |      0.004 |     -0.005 | S&P 500 point-in-time |
|   2009 |  615 | 0.389 |         0.388 |      0.000 |      0.004 | S&P 500 point-in-time |
|   2010 |  484 | 0.446 |         0.359 |      0.088 |      0.015 | S&P 500 point-in-time |
|   2011 |  460 | 0.439 |         0.291 |      0.148 |      0.027 | S&P 500 point-in-time |
|   2012 |  525 | 0.413 |         0.333 |      0.080 |      0.021 | S&P 500 point-in-time |
|   2013 |  417 | 0.374 |         0.321 |      0.053 |      0.000 | S&P 500 point-in-time |
|   2014 |  314 | 0.182 |         0.207 |     -0.025 |     -0.018 | S&P 500 point-in-time |
|   2015 |  594 | 0.098 |         0.161 |     -0.064 |     -0.033 | S&P 500 point-in-time |
|   2016 |  510 | 0.296 |         0.321 |     -0.025 |     -0.018 | S&P 500 point-in-time |
|   2017 |  344 | 0.215 |         0.281 |     -0.065 |     -0.024 | S&P 500 point-in-time |
|   2018 |  528 | 0.222 |         0.245 |     -0.024 |     -0.004 | S&P 500 point-in-time |
|   2019 |  365 | 0.356 |         0.318 |      0.038 |      0.003 | S&P 500 point-in-time |
|   2020 |  665 | 0.468 |         0.415 |      0.052 |      0.014 | S&P 500 point-in-time |
|   2021 |  373 | 0.429 |         0.282 |      0.147 |      0.033 | S&P 500 point-in-time |
|   2022 |  822 | 0.455 |         0.291 |      0.164 |      0.046 | S&P 500 point-in-time |
|   2023 |  519 | 0.304 |         0.304 |      0.000 |     -0.006 | S&P 500 point-in-time |
|   2024 |  404 | 0.297 |         0.321 |     -0.024 |     -0.014 | S&P 500 point-in-time |
|   2025 |  551 | 0.401 |         0.356 |      0.046 |      0.010 | S&P 500 point-in-time |
|   2026 |  370 | 0.424 |         0.382 |      0.042 |      0.005 | S&P 500 point-in-time |

### Market-adjusted (2018+): beta, alpha vs SPY, Sharpe, return / drawdown

| strategy (2018+)                                                   |   beta |   alpha_annual |   alpha_t |   sharpe |   spy_sharpe |   CAGR |   max_DD |   CAGR_per_DD |   worst_month |
|:-------------------------------------------------------------------|-------:|---------------:|----------:|---------:|-------------:|-------:|---------:|--------------:|--------------:|
| goal model top 10%, full universe                                  |  0.957 |          0.134 |     1.734 |    0.968 |        0.816 |  0.270 |   -0.401 |         0.674 |        -0.133 |
| goal model top 10%, S&P 500 PIT                                    |  0.717 |          0.015 |     0.236 |    0.553 |        0.816 |  0.105 |   -0.328 |         0.319 |        -0.148 |
| top 10, vol-adjusted (course 9.8), S&P 500 point-in-time           |  0.904 |          0.036 |     0.506 |    0.648 |        0.816 |  0.149 |   -0.412 |         0.361 |        -0.301 |
| top 20, vol-adjusted, S&P 500 point-in-time                        |  0.862 |          0.034 |     0.604 |    0.719 |        0.816 |  0.150 |   -0.326 |         0.460 |        -0.227 |
| top 10, raw momentum (not vol-adjusted), S&P 500 point-in-time     |  1.149 |          0.080 |     0.946 |    0.779 |        0.816 |  0.224 |   -0.410 |         0.547 |        -0.280 |
| SPY timed by breadth: buy < 20% above 20d, sell > 60% (course 2.2) |  0.539 |         -0.023 |    -0.709 |    0.436 |        0.816 |  0.052 |   -0.283 |         0.184 |        -0.125 |
| SPY timed by % above 50d (same thresholds)                         |  0.490 |         -0.009 |    -0.271 |    0.506 |        0.816 |  0.060 |   -0.283 |         0.212 |        -0.125 |
| SPY                                                                |  1.000 |         -0.000 |    -7.217 |    0.816 |        0.816 |  0.146 |   -0.337 |         0.434 |        -0.125 |

### Cost stress (0.3% per side)

| strategy                                                | costs         |   CAGR |   max_DD |
|:--------------------------------------------------------|:--------------|-------:|---------:|
| goal model top 10%, full universe                       | 0.1% per side |  0.270 |   -0.401 |
| goal model top 10%, full universe                       | 0.3% per side |  0.207 |   -0.439 |
| goal model top 10%, S&P 500 PIT                         | 0.1% per side |  0.105 |   -0.328 |
| goal model top 10%, S&P 500 PIT                         | 0.3% per side |  0.070 |   -0.405 |
| episodic pivots (gap 10% / 8% hold), RS top 20% / sma50 | 0.1% per side |  0.130 |   -0.247 |
| episodic pivots (gap 10% / 8% hold), RS top 20% / sma50 | 0.3% per side |  0.104 |   -0.257 |

### Replay of the daily picks tool's rule (top 10 per date, model retrained quarterly, 2023+)

| list    |   dates |   picks |   hit |   avg_ret |   median_ret |   share_dates_hit_ge_33% | model                                   |
|:--------|--------:|--------:|------:|----------:|-------------:|-------------------------:|:----------------------------------------|
| all     |      89 |     890 | 0.422 |     0.031 |       -0.102 |                    0.607 | picks tool as today (original features) |
| leaders |      89 |     890 | 0.375 |     0.021 |       -0.102 |                    0.494 | picks tool as today (original features) |
| all     |      89 |     890 | 0.418 |     0.029 |       -0.102 |                    0.629 | upgraded features (run-16 set)          |
| leaders |      89 |     890 | 0.390 |     0.024 |       -0.102 |                    0.607 | upgraded features (run-16 set)          |

### Course portfolios: volatility-adjusted momentum and breadth timing (IS 2007-2017, OOS 2018+)

| strategy                                                           |   IS_CAGR |   IS_maxDD |   OOS_CAGR |   OOS_maxDD |
|:-------------------------------------------------------------------|----------:|-----------:|-----------:|------------:|
| top 10, vol-adjusted (course 9.8), all stocks                      |     0.092 |     -0.573 |      0.324 |      -0.453 |
| top 10, vol-adjusted (course 9.8), S&P 500 point-in-time           |     0.061 |     -0.567 |      0.149 |      -0.412 |
| top 20, vol-adjusted, all stocks                                   |     0.090 |     -0.524 |      0.265 |      -0.427 |
| top 20, vol-adjusted, S&P 500 point-in-time                        |     0.061 |     -0.519 |      0.150 |      -0.326 |
| top 10, raw momentum (not vol-adjusted), all stocks                |     0.174 |     -0.660 |      0.526 |      -0.482 |
| top 10, raw momentum (not vol-adjusted), S&P 500 point-in-time     |     0.091 |     -0.610 |      0.224 |      -0.410 |
| SPY buy & hold                                                     |     0.082 |     -0.552 |      0.146 |      -0.337 |
| SPY timed by breadth: buy < 20% above 20d, sell > 60% (course 2.2) |     0.048 |     -0.289 |      0.052 |      -0.283 |
| SPY timed by % above 50d (same thresholds)                         |     0.014 |     -0.381 |      0.060 |      -0.283 |

### Course setups vs random entries (R multiples)

| entry             | filter   | exit          |   IS_n |   IS_avgR |   IS_win |   OOS_n |   OOS_avgR |   OOS_win |
|:------------------|:---------|:--------------|-------:|----------:|---------:|--------:|-----------:|----------:|
| random_uptrend    | all      | bracket_20_10 |  30841 |     0.182 |    0.531 |   34706 |      0.091 |     0.454 |
| tc_ema200_2nd     | all      | bracket_20_10 |   1136 |     0.114 |    0.493 |    1641 |      0.032 |     0.425 |
| tc_ema_cross_base | all      | bracket_20_10 |   7374 |     0.174 |    0.544 |    6955 |      0.035 |     0.451 |
| tc_reversal_base  | all      | bracket_20_10 |    172 |     0.469 |    0.576 |     160 |      0.050 |     0.412 |
| tc_supertrend_ema | all      | bracket_20_10 |  18968 |     0.212 |    0.529 |   23177 |      0.138 |     0.470 |
| random_uptrend    | all      | ema21_close   |  31610 |    -0.152 |    0.205 |   34706 |     -0.098 |     0.204 |
| tc_ema200_2nd     | all      | ema21_close   |   1156 |     0.004 |    0.345 |    1641 |     -0.055 |     0.303 |
| tc_ema_cross_base | all      | ema21_close   |   7547 |     0.007 |    0.368 |    6955 |     -0.005 |     0.357 |
| tc_reversal_base  | all      | ema21_close   |    171 |     0.136 |    0.462 |     160 |     -0.133 |     0.256 |
| tc_supertrend_ema | all      | ema21_close   |  19240 |     0.045 |    0.299 |   23177 |      0.043 |     0.291 |
| random_uptrend    | all      | sma50_close   |  31459 |    -0.040 |    0.144 |   34706 |     -0.023 |     0.140 |
| tc_ema200_2nd     | all      | sma50_close   |   1146 |     0.024 |    0.354 |    1641 |     -0.027 |     0.318 |
| tc_ema_cross_base | all      | sma50_close   |   7420 |     0.107 |    0.372 |    6955 |      0.040 |     0.346 |
| tc_reversal_base  | all      | sma50_close   |    169 |     0.286 |    0.420 |     160 |     -0.071 |     0.269 |
| tc_supertrend_ema | all      | sma50_close   |  19183 |     0.057 |    0.330 |   23177 |      0.026 |     0.333 |
| random_uptrend    | rs80     | bracket_20_10 |   9969 |     0.129 |    0.480 |   11870 |      0.101 |     0.435 |
| tc_ema200_2nd     | rs80     | bracket_20_10 |     38 |     0.105 |    0.447 |      49 |      0.315 |     0.490 |
| tc_ema_cross_base | rs80     | bracket_20_10 |   1447 |     0.141 |    0.500 |    1407 |      0.140 |     0.466 |
| tc_reversal_base  | rs80     | bracket_20_10 |      1 |     0.376 |    1.000 |       2 |      1.980 |     1.000 |
| tc_supertrend_ema | rs80     | bracket_20_10 |   2619 |     0.202 |    0.508 |    3019 |      0.070 |     0.431 |
| random_uptrend    | rs80     | ema21_close   |  10146 |    -0.157 |    0.197 |   11870 |     -0.065 |     0.200 |
| tc_ema200_2nd     | rs80     | ema21_close   |     38 |     0.031 |    0.421 |      49 |     -0.022 |     0.367 |
| tc_ema_cross_base | rs80     | ema21_close   |   1453 |     0.017 |    0.381 |    1407 |      0.051 |     0.372 |
| tc_reversal_base  | rs80     | ema21_close   |      1 |     0.064 |    1.000 |       2 |     -0.068 |     0.500 |
| tc_supertrend_ema | rs80     | ema21_close   |   2639 |     0.075 |    0.332 |    3019 |      0.029 |     0.301 |
| random_uptrend    | rs80     | sma50_close   |  10110 |    -0.125 |    0.139 |   11870 |      0.006 |     0.138 |
| tc_ema200_2nd     | rs80     | sma50_close   |     38 |     0.038 |    0.474 |      49 |      0.056 |     0.408 |
| tc_ema_cross_base | rs80     | sma50_close   |   1438 |     0.096 |    0.376 |    1407 |      0.213 |     0.367 |
| tc_reversal_base  | rs80     | sma50_close   |      1 |     0.023 |    1.000 |       2 |     -0.984 |     0.000 |
| tc_supertrend_ema | rs80     | sma50_close   |   2622 |     0.129 |    0.336 |    3019 |      0.065 |     0.310 |

## 15. ADR%, volatility-matched check, parabolic shorts (run 23)

Is the goal model only picking volatile, strong stocks? Its top 10% vs the average of all stocks in the same year, ADR decile and 6-month-return quintile (+20/-10). edge = actual - matched:

| period   |     n |   hit |   matched_hit |   ret |   matched_ret |   edge_hit |   edge_ret | sample                            |
|:---------|------:|------:|--------------:|------:|--------------:|-----------:|-----------:|:----------------------------------|
| IS       | 21208 | 0.326 |         0.293 | 0.016 |         0.016 |      0.034 |     -0.000 | goal model (full universe)        |
| OOS      | 28485 | 0.390 |         0.341 | 0.029 |         0.020 |      0.049 |      0.009 | goal model (full universe)        |
| IS       |  4736 | 0.311 |         0.291 | 0.015 |         0.018 |      0.020 |     -0.002 | goal model, S&P 500 point-in-time |
| OOS      |  4597 | 0.380 |         0.324 | 0.032 |         0.020 |      0.056 |      0.012 | goal model, S&P 500 point-in-time |

Setups by ADR% (stocks >= $10M/day, exit sma50_close, R multiples). The infographic says: < 5% too slow, 5-12% the sweet spot, > 15% often fails:

| setups                                  | ADR%   |       IS_n |   IS_avgR |   IS_win |      OOS_n |   OOS_avgR |   OOS_win |
|:----------------------------------------|:-------|-----------:|----------:|---------:|-----------:|-----------:|----------:|
| all setups                              | < 3%   | 300744.000 |     0.149 |    0.291 | 280212.000 |     -0.049 |     0.256 |
| all setups                              | 3-5%   |  55947.000 |     0.004 |    0.273 | 106279.000 |      0.121 |     0.274 |
| all setups                              | 5-8%   |   8359.000 |    -0.123 |    0.238 |  18410.000 |      0.213 |     0.269 |
| all setups                              | 8-12%  |    475.000 |    -0.354 |    0.131 |    892.000 |     -0.016 |     0.185 |
| all setups                              | 12-15% |     38.000 |    -0.792 |    0.105 |     60.000 |     -0.112 |     0.333 |
| all setups                              | > 15%  |     13.000 |    -0.595 |    0.462 |     13.000 |     -0.269 |     0.615 |
| breakouts (qull / rocket / base / flag) | < 3%   |   4469.000 |     0.135 |    0.333 |   4595.000 |      0.112 |     0.302 |
| breakouts (qull / rocket / base / flag) | 3-5%   |   5930.000 |    -0.062 |    0.237 |  11344.000 |      0.186 |     0.227 |
| breakouts (qull / rocket / base / flag) | 5-8%   |   1900.000 |    -0.233 |    0.181 |   4032.000 |      0.093 |     0.207 |
| breakouts (qull / rocket / base / flag) | 8-12%  |    264.000 |    -0.355 |    0.136 |    375.000 |     -0.257 |     0.133 |
| breakouts (qull / rocket / base / flag) | 12-15% |     11.000 |    -0.675 |    0.182 |     14.000 |     -0.572 |     0.143 |
| breakouts (qull / rocket / base / flag) | > 15%  |      3.000 |    -0.677 |    0.333 |      3.000 |     -0.346 |     0.333 |
| episodic pivots (ep_*)                  | < 3%   |   1728.000 |     0.166 |    0.329 |   1861.000 |      0.036 |     0.286 |
| episodic pivots (ep_*)                  | 3-5%   |   1872.000 |     0.416 |    0.332 |   3453.000 |      0.553 |     0.315 |
| episodic pivots (ep_*)                  | 5-8%   |    534.000 |     0.202 |    0.303 |   1448.000 |      0.319 |     0.312 |
| episodic pivots (ep_*)                  | 8-12%  |     83.000 |    -0.199 |    0.145 |    166.000 |     -0.448 |     0.187 |
| episodic pivots (ep_*)                  | 12-15% |     22.000 |    -0.923 |    0.045 |     32.000 |      0.453 |     0.531 |
| episodic pivots (ep_*)                  | > 15%  |      9.000 |    -0.328 |    0.556 |      8.000 |      0.150 |     0.875 |
| random entries                          | < 3%   |  21059.000 |     0.111 |    0.155 |  20932.000 |     -0.116 |     0.135 |
| random entries                          | 3-5%   |   4271.000 |    -0.113 |    0.142 |   8483.000 |      0.145 |     0.149 |
| random entries                          | 5-8%   |    820.000 |    -0.019 |    0.146 |   1896.000 |      0.355 |     0.168 |
| random entries                          | 8-12%  |    141.000 |    -0.710 |    0.099 |    220.000 |      0.220 |     0.205 |
| random entries                          | 12-15% |     18.000 |    -0.470 |    0.111 |     22.000 |     -1.102 |     0.000 |
| random entries                          | > 15%  |      9.000 |    -0.934 |    0.000 |      7.000 |     -1.246 |     0.000 |

Qullamaggie's parabolic shorts (up >= 50% in 10 days, >= 3 up closes of 4, >= 20% above the 10-day; entry = first close below the prior day's low within 3 days, or no_trigger = short the parabolic day itself; stop = high of the run; cover at the 10- or 20-day average or after 20 days; price >= $5, >= $10M/day; borrow fees not included):

| variant    | cover   | period   |   n |   win |   avgR |    PF |   avg_ret |
|:-----------|:--------|:---------|----:|------:|-------:|------:|----------:|
| no_trigger | sma10   | IS       | 162 | 0.247 |  3.316 | 3.369 |     0.003 |
| no_trigger | sma10   | OOS      | 371 | 0.286 |  3.716 | 2.652 |     0.015 |
| no_trigger | sma20   | IS       | 162 | 0.198 |  3.768 | 3.573 |     0.006 |
| no_trigger | sma20   | OOS      | 371 | 0.229 |  4.050 | 2.744 |     0.013 |
| trigger    | sma10   | IS       |  94 | 0.596 | -0.062 | 0.783 |    -0.003 |
| trigger    | sma10   | OOS      | 204 | 0.613 |  0.132 | 1.421 |     0.011 |
| trigger    | sma20   | IS       |  94 | 0.479 | -0.178 | 0.636 |    -0.017 |
| trigger    | sma20   | OOS      | 204 | 0.510 |  0.064 | 1.135 |     0.006 |

Parabolic shorts (trigger, cover at the 10-day) by ADR%: count and average R

| adr_pct   |   ('size', 'IS') |   ('size', 'OOS') |   ('mean', 'IS') |   ('mean', 'OOS') |
|:----------|-----------------:|------------------:|-----------------:|------------------:|
| < 3%      |            1.000 |           nan     |           -1.048 |           nan     |
| 3-5%      |            3.000 |            14.000 |            0.063 |            -0.302 |
| 5-8%      |           20.000 |            82.000 |           -0.408 |             0.260 |
| 8-12%     |           32.000 |            88.000 |           -0.074 |             0.116 |
| 12-15%    |           24.000 |            12.000 |            0.187 |             0.023 |
| > 15%     |           14.000 |             8.000 |            0.079 |            -0.080 |

## 14. Your Stock Selection Workflow PDF, price-testable rules (run 20)

Rules as written, nothing tuned. Rockets: 6-week base -> new 52w high on 1.5x volume (<= 5% above the pivot, stop -8%) or a >= 5% gap on 2x volume holding its low for 2 days (no earnings dates: volume is the proxy); price >= $10, >= $20M/day, top 20% 6-month return; exit = sell 1/3 at +25%, stop to entry, trail the 50 SMA. Scanner: above a rising 200d, 50d > 200d, within 15% of the 52w high; entry = pullback to the 21 EMA / 50 SMA then a close above the prior high, a 4-week base breakout, or a holding gap; stop under the pullback/base low, skipped if > 10%; ranked by RS (40) + stop distance (30); exit = weekly close below the 10-week MA. Regime (QQQ): green full size, yellow half, red no new entries. Sizing: rockets 0.5% risk x 3 positions, scanner 0.6% x 4, max 10% per stock. Not testable here: fundamentals (guidance, revenue, FCF, estimates), the Singapore part, the Nasdaq-100 membership itself.

Per trade vs random entries with the same filter and exit (R multiples):

| entry              | filter          | exit          |   IS_n |   IS_avgR |   IS_win |   OOS_n |   OOS_avgR |   OOS_win |   OOS_t |
|:-------------------|:----------------|:--------------|-------:|----------:|---------:|--------:|-----------:|----------:|--------:|
| wf_rocket_gap      | wf_rocket       | bracket_20_10 |    688 |     0.092 |    0.453 |    1254 |      0.126 |     0.430 |   3.241 |
| random_uptrend     | wf_rocket       | bracket_20_10 |   5552 |     0.146 |    0.499 |    8825 |      0.082 |     0.436 |   5.885 |
| wf_rocket_breakout | wf_rocket       | bracket_20_10 |    466 |     0.080 |    0.461 |     798 |      0.077 |     0.445 |   1.660 |
| wf_rocket_gap      | wf_rocket       | sma50_close   |    694 |     0.070 |    0.310 |    1254 |      0.249 |     0.308 |   2.385 |
| wf_rocket_breakout | wf_rocket       | sma50_close   |    467 |     0.049 |    0.379 |     798 |      0.147 |     0.335 |   2.051 |
| random_uptrend     | wf_rocket       | sma50_close   |   5650 |    -0.153 |    0.143 |    8825 |      0.003 |     0.141 |   0.053 |
| wf_rocket_gap      | wf_rocket       | wf_rocket     |    694 |     0.066 |    0.313 |    1254 |      0.209 |     0.315 |   2.550 |
| wf_rocket_breakout | wf_rocket       | wf_rocket     |    467 |     0.059 |    0.385 |     798 |      0.118 |     0.343 |   1.876 |
| random_uptrend     | wf_rocket       | wf_rocket     |   5650 |    -0.140 |    0.145 |    8825 |     -0.004 |     0.146 |  -0.082 |
| wf_rocket_gap      | wf_rocket       | wf_weekly10   |    692 |     0.022 |    0.288 |    1254 |      0.197 |     0.289 |   2.342 |
| wf_rocket_breakout | wf_rocket       | wf_weekly10   |    466 |     0.051 |    0.373 |     798 |      0.117 |     0.332 |   1.693 |
| random_uptrend     | wf_rocket       | wf_weekly10   |   5650 |    -0.171 |    0.133 |    8825 |      0.031 |     0.133 |   0.572 |
| wf_rocket_gap      | wf_rocket_green | bracket_20_10 |    531 |     0.131 |    0.469 |    1046 |      0.190 |     0.451 |   4.381 |
| wf_rocket_breakout | wf_rocket_green | bracket_20_10 |    361 |     0.163 |    0.485 |     635 |      0.116 |     0.460 |   2.197 |
| random_uptrend     | wf_rocket_green | bracket_20_10 |   4419 |     0.135 |    0.491 |    7124 |      0.105 |     0.440 |   6.646 |
| wf_rocket_gap      | wf_rocket_green | sma50_close   |    537 |     0.135 |    0.328 |    1046 |      0.307 |     0.314 |   2.514 |
| wf_rocket_breakout | wf_rocket_green | sma50_close   |    362 |     0.122 |    0.403 |     635 |      0.193 |     0.340 |   2.333 |
| random_uptrend     | wf_rocket_green | sma50_close   |   4517 |    -0.193 |    0.139 |    7124 |      0.021 |     0.140 |   0.368 |
| wf_rocket_gap      | wf_rocket_green | wf_rocket     |    537 |     0.135 |    0.331 |    1046 |      0.256 |     0.322 |   2.705 |
| wf_rocket_breakout | wf_rocket_green | wf_rocket     |    362 |     0.142 |    0.412 |     635 |      0.162 |     0.348 |   2.213 |
| random_uptrend     | wf_rocket_green | wf_rocket     |   4517 |    -0.176 |    0.141 |    7124 |      0.015 |     0.146 |   0.285 |
| wf_rocket_gap      | wf_rocket_green | wf_weekly10   |    535 |     0.077 |    0.307 |    1046 |      0.250 |     0.298 |   2.592 |
| wf_rocket_breakout | wf_rocket_green | wf_weekly10   |    361 |     0.097 |    0.391 |     635 |      0.158 |     0.335 |   1.958 |
| random_uptrend     | wf_rocket_green | wf_weekly10   |   4517 |    -0.222 |    0.128 |    7124 |      0.049 |     0.133 |   0.793 |
| wf_rocket_gap      | wf_scan         | bracket_20_10 |   1417 |     0.214 |    0.506 |    1624 |      0.104 |     0.443 |   3.220 |
| wf_scan_pullback   | wf_scan         | bracket_20_10 |  70493 |     0.183 |    0.545 |   67602 |      0.088 |     0.468 |  19.126 |
| random_uptrend     | wf_scan         | bracket_20_10 |  21936 |     0.186 |    0.544 |   22450 |      0.080 |     0.459 |   9.916 |
| wf_scan_base       | wf_scan         | bracket_20_10 |  25134 |     0.198 |    0.582 |   17538 |      0.038 |     0.482 |   4.747 |
| wf_rocket_gap      | wf_scan         | sma50_close   |   1428 |     0.236 |    0.315 |    1624 |      0.098 |     0.292 |   1.202 |
| wf_scan_pullback   | wf_scan         | sma50_close   |  71288 |     0.057 |    0.283 |   67602 |     -0.000 |     0.269 |  -0.029 |
| wf_scan_base       | wf_scan         | sma50_close   |  25308 |     0.074 |    0.340 |   17538 |     -0.008 |     0.305 |  -0.858 |
| random_uptrend     | wf_scan         | sma50_close   |  22443 |    -0.050 |    0.143 |   22450 |     -0.074 |     0.138 |  -2.507 |
| wf_rocket_gap      | wf_scan         | wf_rocket     |   1428 |     0.223 |    0.319 |    1624 |      0.089 |     0.299 |   1.352 |
| wf_scan_pullback   | wf_scan         | wf_rocket     |  71288 |     0.057 |    0.284 |   67602 |     -0.000 |     0.270 |  -0.006 |
| wf_scan_base       | wf_scan         | wf_rocket     |  25308 |     0.074 |    0.340 |   17538 |     -0.006 |     0.305 |  -0.748 |
| random_uptrend     | wf_scan         | wf_rocket     |  22443 |    -0.051 |    0.144 |   22450 |     -0.073 |     0.140 |  -2.639 |
| wf_rocket_gap      | wf_scan         | wf_weekly10   |   1427 |     0.206 |    0.305 |    1624 |      0.046 |     0.279 |   0.716 |
| wf_scan_pullback   | wf_scan         | wf_weekly10   |  71127 |     0.087 |    0.294 |   67602 |      0.010 |     0.276 |   1.110 |
| wf_scan_base       | wf_scan         | wf_weekly10   |  25195 |     0.096 |    0.368 |   17538 |     -0.009 |     0.323 |  -0.906 |
| random_uptrend     | wf_scan         | wf_weekly10   |  22435 |    -0.041 |    0.135 |   22450 |     -0.043 |     0.131 |  -1.295 |
| wf_rocket_gap      | wf_scan_green   | bracket_20_10 |   1240 |     0.233 |    0.513 |    1478 |      0.133 |     0.454 |   3.901 |
| wf_scan_pullback   | wf_scan_green   | bracket_20_10 |  61584 |     0.169 |    0.538 |   58697 |      0.115 |     0.477 |  23.319 |
| random_uptrend     | wf_scan_green   | bracket_20_10 |  19409 |     0.169 |    0.536 |   19780 |      0.102 |     0.466 |  11.714 |
| wf_scan_base       | wf_scan_green   | bracket_20_10 |  22556 |     0.173 |    0.568 |   15898 |      0.046 |     0.482 |   5.369 |
| wf_rocket_gap      | wf_scan_green   | sma50_close   |   1251 |     0.260 |    0.323 |    1478 |      0.119 |     0.296 |   1.354 |
| wf_scan_pullback   | wf_scan_green   | sma50_close   |  62379 |     0.019 |    0.278 |   58697 |      0.022 |     0.273 |   2.361 |
| wf_scan_base       | wf_scan_green   | sma50_close   |  22730 |     0.037 |    0.327 |   15898 |      0.005 |     0.307 |   0.540 |
| random_uptrend     | wf_scan_green   | sma50_close   |  19916 |    -0.111 |    0.140 |   19780 |     -0.051 |     0.140 |  -1.596 |
| wf_rocket_gap      | wf_scan_green   | wf_rocket     |   1251 |     0.247 |    0.327 |    1478 |      0.107 |     0.302 |   1.509 |
| wf_scan_pullback   | wf_scan_green   | wf_rocket     |  62379 |     0.019 |    0.278 |   58697 |      0.023 |     0.273 |   2.680 |
| wf_scan_base       | wf_scan_green   | wf_rocket     |  22730 |     0.038 |    0.327 |   15898 |      0.006 |     0.308 |   0.703 |
| random_uptrend     | wf_scan_green   | wf_rocket     |  19916 |    -0.110 |    0.140 |   19780 |     -0.050 |     0.142 |  -1.668 |
| wf_rocket_gap      | wf_scan_green   | wf_weekly10   |   1250 |     0.226 |    0.315 |    1478 |      0.061 |     0.284 |   0.887 |
| wf_scan_pullback   | wf_scan_green   | wf_weekly10   |  62218 |     0.035 |    0.287 |   58697 |      0.031 |     0.280 |   3.232 |
| wf_scan_base       | wf_scan_green   | wf_weekly10   |  22617 |     0.051 |    0.354 |   15898 |     -0.001 |     0.325 |  -0.138 |
| random_uptrend     | wf_scan_green   | wf_weekly10   |  19908 |    -0.111 |    0.131 |   19780 |     -0.024 |     0.132 |  -0.670 |

Per trade by Nasdaq-100 regime at entry (the PDF's own exits):

| part                    | regime           |      IS_n |   IS_avgR |   IS_win |     OOS_n |   OOS_avgR |   OOS_win |
|:------------------------|:-----------------|----------:|----------:|---------:|----------:|-----------:|----------:|
| rockets                 | PDF red          |   157.000 |    -0.174 |    0.293 |   258.000 |     -0.026 |     0.326 |
| rockets                 | PDF yellow       |   105.000 |    -0.222 |    0.229 |   113.000 |     -0.064 |     0.239 |
| rockets                 | PDF green (200d) |   927.000 |     0.180 |    0.376 |  1681.000 |      0.220 |     0.332 |
| rockets                 | QQQ < both       |   195.000 |     0.190 |    0.390 |   300.000 |      0.038 |     0.300 |
| rockets                 | QQQ > 50 only    |   107.000 |     0.095 |    0.299 |   173.000 |      0.252 |     0.318 |
| rockets                 | QQQ > 21 only    |    71.000 |    -0.040 |    0.394 |    97.000 |      0.224 |     0.330 |
| rockets                 | QQQ > 21 & 50    |   816.000 |     0.088 |    0.347 |  1482.000 |      0.189 |     0.332 |
| scanner                 | PDF red          |  6982.000 |     0.452 |    0.382 |  7685.000 |     -0.198 |     0.251 |
| scanner                 | PDF yellow       |  4682.000 |     0.456 |    0.361 |  3006.000 |      0.072 |     0.281 |
| scanner                 | PDF green (200d) | 88315.000 |     0.119 |    0.316 | 76073.000 |      0.025 |     0.290 |
| scanner                 | QQQ < both       | 14484.000 |     0.273 |    0.362 | 14914.000 |      0.052 |     0.306 |
| scanner                 | QQQ > 50 only    | 11418.000 |     0.171 |    0.306 |  8779.000 |     -0.058 |     0.273 |
| scanner                 | QQQ > 21 only    |  5020.000 |     0.379 |    0.407 |  3978.000 |      0.094 |     0.335 |
| scanner                 | QQQ > 21 & 50    | 69057.000 |     0.116 |    0.311 | 59093.000 |     -0.001 |     0.279 |
| random (rocket filter)  | PDF red          |   711.000 |     0.281 |    0.194 |  1258.000 |     -0.195 |     0.147 |
| random (rocket filter)  | PDF yellow       |   422.000 |    -0.454 |    0.102 |   443.000 |      0.243 |     0.151 |
| random (rocket filter)  | PDF green (200d) |  4582.000 |    -0.030 |    0.149 |  7124.000 |      0.015 |     0.146 |
| random (rocket filter)  | QQQ < both       |   959.000 |     0.451 |    0.193 |  1695.000 |     -0.245 |     0.135 |
| random (rocket filter)  | QQQ > 50 only    |   677.000 |    -0.049 |    0.154 |   841.000 |     -0.030 |     0.163 |
| random (rocket filter)  | QQQ > 21 only    |   299.000 |     0.318 |    0.244 |   390.000 |      0.251 |     0.174 |
| random (rocket filter)  | QQQ > 21 & 50    |  3780.000 |    -0.165 |    0.133 |  5899.000 |      0.053 |     0.145 |
| random (scanner filter) | PDF red          |  1435.000 |     0.568 |    0.176 |  1902.000 |     -0.358 |     0.116 |
| random (scanner filter) | PDF yellow       |  1092.000 |     0.419 |    0.145 |   768.000 |      0.247 |     0.128 |
| random (scanner filter) | PDF green (200d) | 20188.000 |     0.046 |    0.139 | 19780.000 |     -0.024 |     0.132 |
| random (scanner filter) | QQQ < both       |  3098.000 |     0.550 |    0.182 |  3955.000 |     -0.195 |     0.134 |
| random (scanner filter) | QQQ > 50 only    |  2720.000 |     0.036 |    0.136 |  2234.000 |     -0.077 |     0.133 |
| random (scanner filter) | QQQ > 21 only    |   914.000 |     0.656 |    0.208 |   867.000 |      0.195 |     0.160 |
| random (scanner filter) | QQQ > 21 & 50    | 15983.000 |    -0.012 |    0.131 | 15394.000 |     -0.013 |     0.127 |

Portfolios 2018+ (marked to market daily):

| strategy                                                            |   CAGR |   max_DD |   trades |   win |   avg_positions |
|:--------------------------------------------------------------------|-------:|---------:|---------:|------:|----------------:|
| rockets as written (regime sizing) / wf_rocket                      |  0.023 |   -0.106 |      190 | 0.305 |           2.339 |
| rockets, no regime rule / wf_rocket                                 |  0.012 |   -0.106 |      236 | 0.309 |           2.718 |
| rockets, QQQ 21/50 regime / wf_rocket                               |  0.015 |   -0.088 |      192 | 0.312 |           2.434 |
| rockets / sma50_close                                               |  0.026 |   -0.095 |      189 | 0.302 |           2.341 |
| rockets / bracket_20_10                                             |  0.028 |   -0.079 |      174 | 0.454 |           2.400 |
| BASELINE random entries, rocket filter + regime / wf_rocket         | -0.006 |   -0.243 |      496 | 0.155 |           2.467 |
| rockets as written, S&P 500 point-in-time only / wf_rocket          |  0.014 |   -0.070 |      142 | 0.345 |           2.027 |
| scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10 |  0.011 |   -0.172 |      349 | 0.287 |           3.403 |
| scanner PIT, no regime rule / wf_weekly10                           |  0.002 |   -0.171 |      421 | 0.314 |           3.932 |
| scanner PIT, QQQ 21/50 regime / wf_weekly10                         | -0.023 |   -0.248 |      375 | 0.269 |           3.469 |
| scanner PIT / sma50_close                                           |  0.006 |   -0.204 |      396 | 0.265 |           3.355 |
| BASELINE random entries, scanner filter + regime, PIT / wf_weekly10 |  0.037 |   -0.166 |      525 | 0.152 |           3.283 |
| scanner as written, full universe / wf_weekly10                     |  0.008 |   -0.214 |      368 | 0.264 |           3.390 |

The PDF's full split (Singapore part as cash; scanner and rockets point-in-time):

| portfolio (2018+, daily rebalanced)                       |   CAGR |   max_DD |   worst_year |
|:----------------------------------------------------------|-------:|---------:|-------------:|
| PDF split: 40% SPY / 25% scanner / 15% rockets / 20% cash |  0.066 |   -0.168 |       -0.091 |
| trading parts only, 25:15                                 |  0.013 |   -0.132 |       -0.055 |
| SPY 100%                                                  |  0.146 |   -0.337 |       -0.182 |

## 13. Bracket menu and market regime for the +20/-10 model's picks (runs 17-18)

Every stock every 10 days, entry at the close, 63-day limit, 0.1% costs per side. Stocks ranked by the +20/-10 goal model (walk-forward, so pre-2018 scores are also out-of-sample for their year). Top 10% = top 10% of scores within each year. Brackets are chosen on IS (walk-forward years before 2018) and judged on 2018+. IS choice: best return per month = m30_5, best return per trade = m30_15.

Model top 10%: hit rate, net return per trade, return per month held, days held (IS vs OOS):

| bracket     |   breakeven_hit |   hit_IS |   hit_OOS |   ret_IS |   ret_OOS |   per_month_IS |   per_month_OOS |   days_IS |   days_OOS |
|:------------|----------------:|---------:|----------:|---------:|----------:|---------------:|----------------:|----------:|-----------:|
| +5% / -5%   |           0.500 |    0.523 |     0.553 |    0.001 |     0.004 |          0.002 |           0.018 |     5.244 |      4.388 |
| +5% / -8%   |           0.615 |    0.638 |     0.672 |    0.002 |     0.006 |          0.004 |           0.022 |     7.510 |      6.241 |
| +5% / -10%  |           0.667 |    0.685 |     0.729 |    0.002 |     0.009 |          0.004 |           0.025 |     8.843 |      7.423 |
| +5% / -15%  |           0.750 |    0.760 |     0.813 |    0.003 |     0.013 |          0.005 |           0.028 |    11.953 |      9.905 |
| +10% / -5%  |           0.333 |    0.374 |     0.392 |    0.004 |     0.007 |          0.009 |           0.018 |     9.359 |      7.950 |
| +10% / -8%  |           0.444 |    0.483 |     0.515 |    0.006 |     0.012 |          0.010 |           0.022 |    13.570 |     11.508 |
| +10% / -10% |           0.500 |    0.533 |     0.578 |    0.007 |     0.016 |          0.010 |           0.024 |    15.982 |     13.774 |
| +10% / -15% |           0.600 |    0.609 |     0.676 |    0.010 |     0.024 |          0.010 |           0.027 |    21.228 |     18.420 |
| +15% / -5%  |           0.250 |    0.290 |     0.308 |    0.007 |     0.010 |          0.012 |           0.019 |    13.053 |     11.094 |
| +15% / -8%  |           0.348 |    0.379 |     0.419 |    0.011 |     0.018 |          0.012 |           0.023 |    18.796 |     16.122 |
| +15% / -10% |           0.400 |    0.419 |     0.475 |    0.012 |     0.023 |          0.012 |           0.025 |    21.979 |     19.294 |
| +15% / -15% |           0.500 |    0.482 |     0.562 |    0.016 |     0.034 |          0.012 |           0.028 |    28.544 |     25.451 |
| +20% / -5%  |           0.200 |    0.227 |     0.250 |    0.010 |     0.013 |          0.013 |           0.020 |    16.067 |     13.859 |
| +20% / -8%  |           0.286 |    0.297 |     0.342 |    0.014 |     0.022 |          0.013 |           0.023 |    22.775 |     20.025 |
| +20% / -10% |           0.333 |    0.326 |     0.388 |    0.016 |     0.028 |          0.013 |           0.025 |    26.454 |     23.811 |
| +20% / -15% |           0.429 |    0.373 |     0.461 |    0.020 |     0.041 |          0.012 |           0.028 |    33.815 |     30.992 |
| +30% / -5%  |           0.143 |    0.130 |     0.160 |    0.013 |     0.017 |          0.013 |           0.019 |    20.132 |     17.921 |
| +30% / -8%  |           0.211 |    0.167 |     0.219 |    0.018 |     0.027 |          0.013 |           0.023 |    28.056 |     25.561 |
| +30% / -10% |           0.250 |    0.182 |     0.248 |    0.020 |     0.035 |          0.013 |           0.024 |    32.252 |     30.042 |
| +30% / -15% |           0.333 |    0.207 |     0.294 |    0.024 |     0.050 |          0.013 |           0.027 |    40.405 |     38.373 |

OOS hit rate by tier (all stocks = no model):

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |        0.526 |     0.553 |    0.566 |
| +5% / -8%   |        0.640 |     0.672 |    0.686 |
| +5% / -10%  |        0.686 |     0.729 |    0.742 |
| +5% / -15%  |        0.744 |     0.813 |    0.835 |
| +10% / -5%  |        0.351 |     0.392 |    0.405 |
| +10% / -8%  |        0.446 |     0.515 |    0.532 |
| +10% / -10% |        0.486 |     0.578 |    0.596 |
| +10% / -15% |        0.539 |     0.676 |    0.701 |
| +15% / -5%  |        0.240 |     0.308 |    0.321 |
| +15% / -8%  |        0.309 |     0.419 |    0.438 |
| +15% / -10% |        0.338 |     0.475 |    0.496 |
| +15% / -15% |        0.377 |     0.562 |    0.596 |
| +20% / -5%  |        0.163 |     0.250 |    0.268 |
| +20% / -8%  |        0.210 |     0.342 |    0.366 |
| +20% / -10% |        0.231 |     0.388 |    0.415 |
| +20% / -15% |        0.259 |     0.461 |    0.501 |
| +30% / -5%  |        0.076 |     0.160 |    0.183 |
| +30% / -8%  |        0.099 |     0.219 |    0.247 |
| +30% / -10% |        0.110 |     0.248 |    0.280 |
| +30% / -15% |        0.125 |     0.294 |    0.335 |

OOS net return per trade by tier:

| bracket     |   all stocks |   top 10% |   top 2% |
|:------------|-------------:|----------:|---------:|
| +5% / -5%   |       0.0008 |    0.0038 |   0.0053 |
| +5% / -8%   |       0.0029 |    0.0065 |   0.0085 |
| +5% / -10%  |       0.0043 |    0.0088 |   0.0112 |
| +5% / -15%  |       0.0067 |    0.0133 |   0.0178 |
| +10% / -5%  |       0.0029 |    0.0068 |   0.0091 |
| +10% / -8%  |       0.0062 |    0.0118 |   0.0153 |
| +10% / -10% |       0.0083 |    0.0159 |   0.0200 |
| +10% / -15% |       0.0122 |    0.0239 |   0.0297 |
| +15% / -5%  |       0.0045 |    0.0101 |   0.0127 |
| +15% / -8%  |       0.0087 |    0.0175 |   0.0220 |
| +15% / -10% |       0.0112 |    0.0229 |   0.0281 |
| +15% / -15% |       0.0158 |    0.0338 |   0.0422 |
| +20% / -5%  |       0.0056 |    0.0131 |   0.0168 |
| +20% / -8%  |       0.0103 |    0.0221 |   0.0275 |
| +20% / -10% |       0.0130 |    0.0284 |   0.0350 |
| +20% / -15% |       0.0182 |    0.0413 |   0.0521 |
| +30% / -5%  |       0.0067 |    0.0166 |   0.0220 |
| +30% / -8%  |       0.0119 |    0.0274 |   0.0343 |
| +30% / -10% |       0.0149 |    0.0349 |   0.0430 |
| +30% / -15% |       0.0206 |    0.0497 |   0.0623 |

Portfolio 2018+ (top 10% model, 1% risk per trade = position size 1%/stop, max 10 positions, 20% cap):

| bracket     |   CAGR |   max_DD |   trades |   win |
|:------------|-------:|---------:|---------:|------:|
| +5% / -5%   | -0.051 |   -0.617 | 2876.000 | 0.511 |
| +5% / -8%   |  0.017 |   -0.533 | 3193.000 | 0.631 |
| +5% / -10%  |  0.054 |   -0.474 | 3143.000 | 0.686 |
| +5% / -15%  |  0.091 |   -0.342 | 2423.000 | 0.775 |
| +10% / -5%  |  0.049 |   -0.575 | 1989.000 | 0.371 |
| +10% / -8%  |  0.195 |   -0.425 | 2095.000 | 0.494 |
| +10% / -10% |  0.203 |   -0.425 | 1973.000 | 0.553 |
| +10% / -15% |  0.204 |   -0.309 | 1460.000 | 0.666 |
| +15% / -5%  |  0.188 |   -0.518 | 1521.000 | 0.304 |
| +15% / -8%  |  0.226 |   -0.453 | 1639.000 | 0.407 |
| +15% / -10% |  0.219 |   -0.477 | 1466.000 | 0.462 |
| +15% / -15% |  0.139 |   -0.373 | 1064.000 | 0.561 |
| +20% / -5%  |  0.145 |   -0.580 | 1325.000 | 0.249 |
| +20% / -8%  |  0.214 |   -0.511 | 1342.000 | 0.353 |
| +20% / -10% |  0.270 |   -0.401 | 1190.000 | 0.417 |
| +20% / -15% |  0.159 |   -0.386 |  880.000 | 0.517 |
| +30% / -5%  |  0.150 |   -0.573 | 1030.000 | 0.206 |
| +30% / -8%  |  0.229 |   -0.471 | 1040.000 | 0.303 |
| +30% / -10% |  0.154 |   -0.450 |  899.000 | 0.344 |
| +30% / -15% |  0.157 |   -0.387 |  686.000 | 0.456 |

Model top 10%, +20/-10, by market regime at entry (breadth terciles and the 3-day market model cut use IS data):

| regime                                 | bucket               |      IS_n |   IS_hit_target |   IS_avg_net_return |     OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|----------:|----------------:|--------------------:|----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         |  7169.000 |           0.321 |               0.022 |  5106.000 |            0.407 |                0.033 |
| breadth (stocks above 50d)             | low (< 53%)          |  7092.000 |           0.356 |               0.020 | 15173.000 |            0.385 |                0.029 |
| breadth (stocks above 50d)             | mid                  |  6947.000 |           0.302 |               0.005 |  8206.000 |            0.388 |                0.026 |
| VIX level                              | 15-20                |  6669.000 |           0.284 |               0.001 |  9876.000 |            0.349 |                0.015 |
| VIX level                              | 20-30                |  4301.000 |           0.447 |               0.049 | 12319.000 |            0.433 |                0.044 |
| VIX level                              | < 15                 |  7811.000 |           0.293 |               0.013 |  4807.000 |            0.323 |                0.003 |
| VIX level                              | > 30                 |  2427.000 |           0.337 |               0.011 |  1483.000 |            0.519 |                0.070 |
| VIX / VIX3M                            | 0.9-1.0              |  6654.000 |           0.376 |               0.032 | 12069.000 |            0.390 |                0.031 |
| VIX / VIX3M                            | < 0.9 (calm)         | 11781.000 |           0.301 |               0.010 | 12979.000 |            0.398 |                0.028 |
| VIX / VIX3M                            | > 1.0 (stress)       |  2773.000 |           0.313 |               0.003 |  3437.000 |            0.359 |                0.024 |
| SPY above 200d                         | no                   |  5905.000 |           0.350 |               0.016 |  7175.000 |            0.423 |                0.041 |
| SPY above 200d                         | yes                  | 15303.000 |           0.317 |               0.016 | 21310.000 |            0.378 |                0.024 |
| QQQ above 10 & 20 SMA                  | no                   |  9401.000 |           0.350 |               0.022 | 16008.000 |            0.381 |                0.027 |
| QQQ above 10 & 20 SMA                  | yes                  | 11807.000 |           0.308 |               0.011 | 12477.000 |            0.401 |                0.031 |
| SPY 1-month return                     | -3..0%               |  3853.000 |           0.287 |               0.001 |  5167.000 |            0.366 |                0.024 |
| SPY 1-month return                     | 0..3%                |  6802.000 |           0.337 |               0.022 |  7561.000 |            0.402 |                0.028 |
| SPY 1-month return                     | < -3%                |  3914.000 |           0.393 |               0.030 |  8447.000 |            0.379 |                0.028 |
| SPY 1-month return                     | > 3%                 |  6639.000 |           0.299 |               0.009 |  7310.000 |            0.406 |                0.032 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 12577.000 |           0.315 |               0.013 | 12972.000 |            0.390 |                0.026 |
| SPY vs 21/50 SMA                       | above 21 only        |   546.000 |           0.352 |               0.017 |  1740.000 |            0.434 |                0.046 |
| SPY vs 21/50 SMA                       | above 50 only        |  2453.000 |           0.225 |              -0.008 |  2781.000 |            0.370 |                0.022 |
| SPY vs 21/50 SMA                       | below both           |  5632.000 |           0.393 |               0.033 | 10992.000 |            0.387 |                0.031 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 12492.000 |           0.285 |               0.005 | 12775.000 |            0.385 |                0.026 |
| QQQ vs 21/50 SMA                       | above 21 only        |   780.000 |           0.408 |               0.036 |  1464.000 |            0.445 |                0.042 |
| QQQ vs 21/50 SMA                       | above 50 only        |  2011.000 |           0.342 |               0.023 |  3552.000 |            0.387 |                0.027 |
| QQQ vs 21/50 SMA                       | below both           |  5925.000 |           0.396 |               0.034 | 10694.000 |            0.388 |                0.030 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 12889.000 |           0.295 |               0.007 | 13028.000 |            0.399 |                0.031 |
| A/D line vs its 21/50 MA               | above 21 only        |   865.000 |           0.431 |               0.036 |  1217.000 |            0.319 |                0.003 |
| A/D line vs its 21/50 MA               | above 50 only        |  2762.000 |           0.301 |               0.014 |  3910.000 |            0.365 |                0.022 |
| A/D line vs its 21/50 MA               | below both           |  4692.000 |           0.408 |               0.037 | 10330.000 |            0.396 |                0.031 |
| % of stocks above 20d                  | 40-60%               |  4814.000 |           0.307 |               0.009 |  6571.000 |            0.340 |                0.010 |
| % of stocks above 20d                  | < 40%                |  5623.000 |           0.359 |               0.024 | 11539.000 |            0.392 |                0.031 |
| % of stocks above 20d                  | > 60%                | 10771.000 |           0.318 |               0.015 | 10375.000 |            0.419 |                0.037 |
| % above 50d, 10-day change             | falling (< -5 pts)   |  8606.000 |           0.355 |               0.026 | 13204.000 |            0.390 |                0.030 |
| % above 50d, 10-day change             | flat                 |  4816.000 |           0.263 |              -0.006 |  7339.000 |            0.369 |                0.021 |
| % above 50d, 10-day change             | rising (> +5 pts)    |  7786.000 |           0.334 |               0.018 |  7942.000 |            0.408 |                0.033 |
| A/D line, 10-day change                | flat                 |  5482.000 |           0.273 |              -0.003 |  7524.000 |            0.377 |                0.025 |
| A/D line, 10-day change                | falling              |  5979.000 |           0.393 |               0.037 | 10972.000 |            0.396 |                0.032 |
| A/D line, 10-day change                | rising               |  9747.000 |           0.315 |               0.014 |  9989.000 |            0.392 |                0.028 |
| sector & sub-industry today green      | both                 |  6356.000 |           0.310 |               0.010 |  9155.000 |            0.393 |                0.029 |
| sector & sub-industry today green      | neither              |  6916.000 |           0.350 |               0.025 | 10758.000 |            0.396 |                0.032 |
| sector & sub-industry today green      | one of the two       |  2527.000 |           0.317 |               0.013 |  3957.000 |            0.367 |                0.021 |
| sector & sub-industry up over 5 days   | both                 |  7121.000 |           0.296 |               0.007 |  9363.000 |            0.413 |                0.036 |
| sector & sub-industry up over 5 days   | neither              |  6073.000 |           0.363 |               0.028 | 10710.000 |            0.376 |                0.025 |
| sector & sub-industry up over 5 days   | one of the two       |  2603.000 |           0.337 |               0.018 |  3797.000 |            0.370 |                0.023 |
| sector & sub-industry above 21 EMA     | both                 |  7528.000 |           0.309 |               0.012 |  8802.000 |            0.402 |                0.032 |
| sector & sub-industry above 21 EMA     | neither              |  5611.000 |           0.354 |               0.024 | 10996.000 |            0.387 |                0.029 |
| sector & sub-industry above 21 EMA     | one of the two       |  2660.000 |           0.329 |               0.017 |  4072.000 |            0.371 |                0.022 |
| distance above the 21 EMA              | 0-5%                 |  6155.000 |           0.312 |               0.015 |  6695.000 |            0.387 |                0.030 |
| distance above the 21 EMA              | 10-15%               |   914.000 |           0.335 |               0.015 |   967.000 |            0.425 |                0.037 |
| distance above the 21 EMA              | 5-10%                |  2960.000 |           0.293 |               0.007 |  2806.000 |            0.403 |                0.032 |
| distance above the 21 EMA              | > 15%                |   475.000 |           0.333 |               0.009 |   561.000 |            0.396 |                0.025 |
| distance above the 21 EMA              | below                | 10704.000 |           0.343 |               0.019 | 17456.000 |            0.386 |                0.027 |
| ADR%                                   | > 15%                |    91.000 |           0.363 |               0.009 |    53.000 |            0.434 |                0.033 |
| ADR%                                   | 12-15%               |   123.000 |           0.415 |               0.025 |    75.000 |            0.453 |                0.053 |
| ADR%                                   | 3-5%                 | 11522.000 |           0.340 |               0.018 | 17272.000 |            0.386 |                0.029 |
| ADR%                                   | 5-8%                 |  3664.000 |           0.341 |               0.005 |  6659.000 |            0.435 |                0.033 |
| ADR%                                   | 8-12%                |   726.000 |           0.373 |               0.010 |   774.000 |            0.437 |                0.033 |
| ADR%                                   | < 3%                 |  5082.000 |           0.275 |               0.019 |  3652.000 |            0.312 |                0.020 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |    73.000 |           0.438 |               0.033 |    51.000 |            0.431 |                0.032 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |   100.000 |           0.400 |               0.021 |    72.000 |            0.444 |                0.051 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 |  9284.000 |           0.338 |               0.018 | 15476.000 |            0.384 |                0.027 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  2969.000 |           0.345 |               0.005 |  6109.000 |            0.434 |                0.032 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |   549.000 |           0.377 |               0.012 |   725.000 |            0.432 |                0.031 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 |  4112.000 |           0.278 |               0.021 |  3260.000 |            0.312 |                0.019 |
| fundamental inflection (all 4)         | no                   | 12380.000 |           0.326 |               0.019 | 24861.000 |            0.389 |                0.028 |
| fundamental inflection (all 4)         | yes                  |   593.000 |           0.331 |               0.025 |  1304.000 |            0.398 |                0.032 |
| revenue growth accelerating            | 1 quarter            |  3274.000 |           0.312 |               0.014 |  6224.000 |            0.404 |                0.033 |
| revenue growth accelerating            | 2+ quarters          |  2829.000 |           0.366 |               0.032 |  5781.000 |            0.391 |                0.028 |
| revenue growth accelerating            | no (decelerating)    |  6870.000 |           0.316 |               0.017 | 14160.000 |            0.382 |                0.026 |
| operating income outgrowing revenue    | no                   |  6240.000 |           0.330 |               0.018 | 13253.000 |            0.394 |                0.027 |
| operating income outgrowing revenue    | yes                  |  4584.000 |           0.317 |               0.018 |  9148.000 |            0.381 |                0.027 |
| operating margin vs a year ago         | expanding            |  5513.000 |           0.330 |               0.019 | 11897.000 |            0.379 |                0.024 |
| operating margin vs a year ago         | shrinking            |  5294.000 |           0.319 |               0.016 | 10456.000 |            0.400 |                0.030 |
| FCF margin vs a year ago               | improving            |  6192.000 |           0.317 |               0.017 | 13647.000 |            0.386 |                0.027 |
| FCF margin vs a year ago               | worse                |  5607.000 |           0.326 |               0.020 | 11944.000 |            0.397 |                0.030 |
| up/down volume, 50 days                | 0.8-1.0              |  4678.000 |           0.340 |               0.019 |  7177.000 |            0.391 |                0.029 |
| up/down volume, 50 days                | 1.0-1.3              |  5719.000 |           0.324 |               0.016 |  7288.000 |            0.386 |                0.027 |
| up/down volume, 50 days                | < 0.8 (distribution) |  5377.000 |           0.339 |               0.018 |  8434.000 |            0.390 |                0.028 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  5434.000 |           0.304 |               0.011 |  5586.000 |            0.391 |                0.030 |
| price vs 200-day                       | below                | 10267.000 |           0.345 |               0.018 | 16040.000 |            0.388 |                0.029 |
| price vs 200-day                       | 0-10% above          |  2670.000 |           0.305 |               0.014 |  3165.000 |            0.373 |                0.024 |
| price vs 200-day                       | 10-30% above         |  4654.000 |           0.303 |               0.016 |  4627.000 |            0.391 |                0.030 |
| price vs 200-day                       | 30-50% above         |  2410.000 |           0.319 |               0.014 |  2661.000 |            0.398 |                0.030 |
| price vs 200-day                       | > 50% above          |  1207.000 |           0.318 |               0.001 |  1992.000 |            0.415 |                0.030 |
| 6-month gain                           | 0-20%                |  3801.000 |           0.305 |               0.014 |  4410.000 |            0.388 |                0.030 |
| 6-month gain                           | 20-50%               |  4064.000 |           0.299 |               0.015 |  4396.000 |            0.392 |                0.030 |
| 6-month gain                           | 50-100%              |  2381.000 |           0.333 |               0.014 |  3203.000 |            0.415 |                0.034 |
| 6-month gain                           | < 0                  | 10152.000 |           0.344 |               0.018 | 14963.000 |            0.382 |                0.027 |
| 6-month gain                           | > 100%               |   810.000 |           0.317 |               0.000 |  1513.000 |            0.410 |                0.027 |
| sector (11 GICS, by median RS)         | bottom 3             |  4449.000 |           0.319 |               0.011 |  6150.000 |            0.384 |                0.029 |
| sector (11 GICS, by median RS)         | middle 5             |  8085.000 |           0.335 |               0.021 | 13012.000 |            0.398 |                0.032 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  4528.000 |           0.317 |               0.012 |  5670.000 |            0.379 |                0.023 |
| sub-industry (by median RS)            | bottom 30%           |  4930.000 |           0.349 |               0.022 |  8515.000 |            0.392 |                0.029 |
| sub-industry (by median RS)            | middle               |  5310.000 |           0.332 |               0.019 |  8538.000 |            0.386 |                0.029 |
| sub-industry (by median RS)            | top 30% (leading)    |  5521.000 |           0.307 |               0.011 |  6795.000 |            0.393 |                0.029 |
| 3-day market model                     | bottom 10% (skip?)   |  1468.000 |           0.442 |               0.045 |   421.000 |            0.665 |                0.110 |
| 3-day market model                     | rest                 | 19740.000 |           0.318 |               0.014 | 28064.000 |            0.386 |                0.027 |

Same, S&P 500 stocks only after they joined the index (point-in-time survivorship check):

| regime                                 | bucket               |     IS_n |   IS_hit_target |   IS_avg_net_return |    OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|---------:|----------------:|--------------------:|---------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         | 1600.000 |           0.304 |               0.020 |  729.000 |            0.418 |                0.044 |
| breadth (stocks above 50d)             | low (< 53%)          | 1596.000 |           0.338 |               0.023 | 2708.000 |            0.369 |                0.030 |
| breadth (stocks above 50d)             | mid                  | 1540.000 |           0.290 |               0.002 | 1160.000 |            0.383 |                0.029 |
| VIX level                              | 15-20                | 1589.000 |           0.262 |              -0.002 | 1316.000 |            0.333 |                0.015 |
| VIX level                              | 20-30                | 1137.000 |           0.437 |               0.055 | 2472.000 |            0.409 |                0.044 |
| VIX level                              | < 15                 | 1200.000 |           0.226 |              -0.000 |  468.000 |            0.274 |               -0.012 |
| VIX level                              | > 30                 |  810.000 |           0.354 |               0.018 |  341.000 |            0.504 |                0.073 |
| VIX / VIX3M                            | 0.9-1.0              | 1546.000 |           0.407 |               0.045 | 2199.000 |            0.370 |                0.032 |
| VIX / VIX3M                            | < 0.9 (calm)         | 2408.000 |           0.266 |               0.004 | 1718.000 |            0.412 |                0.035 |
| VIX / VIX3M                            | > 1.0 (stress)       |  782.000 |           0.258 |              -0.008 |  680.000 |            0.332 |                0.021 |
| SPY above 200d                         | no                   | 1719.000 |           0.344 |               0.018 | 1645.000 |            0.419 |                0.048 |
| SPY above 200d                         | yes                  | 3017.000 |           0.292 |               0.014 | 2952.000 |            0.358 |                0.023 |
| QQQ above 10 & 20 SMA                  | no                   | 2059.000 |           0.341 |               0.026 | 2795.000 |            0.367 |                0.028 |
| QQQ above 10 & 20 SMA                  | yes                  | 2677.000 |           0.287 |               0.007 | 1802.000 |            0.400 |                0.038 |
| SPY 1-month return                     | -3..0%               |  743.000 |           0.245 |              -0.007 |  690.000 |            0.352 |                0.026 |
| SPY 1-month return                     | 0..3%                | 1354.000 |           0.346 |               0.032 |  991.000 |            0.423 |                0.036 |
| SPY 1-month return                     | < -3%                | 1093.000 |           0.360 |               0.025 | 1795.000 |            0.363 |                0.030 |
| SPY 1-month return                     | > 3%                 | 1546.000 |           0.276 |               0.005 | 1121.000 |            0.388 |                0.034 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 2793.000 |           0.297 |               0.010 | 1753.000 |            0.390 |                0.031 |
| SPY vs 21/50 SMA                       | above 21 only        |  132.000 |           0.379 |               0.039 |  290.000 |            0.469 |                0.066 |
| SPY vs 21/50 SMA                       | above 50 only        |  498.000 |           0.181 |              -0.021 |  371.000 |            0.305 |                0.004 |
| SPY vs 21/50 SMA                       | below both           | 1313.000 |           0.383 |               0.037 | 2183.000 |            0.374 |                0.033 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 2736.000 |           0.254 |              -0.002 | 1785.000 |            0.380 |                0.032 |
| QQQ vs 21/50 SMA                       | above 21 only        |  199.000 |           0.452 |               0.056 |  233.000 |            0.468 |                0.053 |
| QQQ vs 21/50 SMA                       | above 50 only        |  401.000 |           0.347 |               0.028 |  553.000 |            0.353 |                0.022 |
| QQQ vs 21/50 SMA                       | below both           | 1400.000 |           0.391 |               0.040 | 2026.000 |            0.378 |                0.032 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 2835.000 |           0.268 |               0.002 | 1873.000 |            0.412 |                0.042 |
| A/D line vs its 21/50 MA               | above 21 only        |  249.000 |           0.410 |               0.036 |  185.000 |            0.216 |               -0.024 |
| A/D line vs its 21/50 MA               | above 50 only        |  526.000 |           0.314 |               0.023 |  533.000 |            0.300 |                0.006 |
| A/D line vs its 21/50 MA               | below both           | 1126.000 |           0.396 |               0.041 | 2006.000 |            0.387 |                0.034 |
| % of stocks above 20d                  | 40-60%               |  907.000 |           0.280 |               0.004 |  863.000 |            0.277 |               -0.008 |
| % of stocks above 20d                  | < 40%                | 1278.000 |           0.347 |               0.027 | 2181.000 |            0.378 |                0.033 |
| % of stocks above 20d                  | > 60%                | 2551.000 |           0.304 |               0.013 | 1553.000 |            0.441 |                0.052 |
| % above 50d, 10-day change             | falling (< -5 pts)   | 1821.000 |           0.347 |               0.031 | 2227.000 |            0.374 |                0.031 |
| % above 50d, 10-day change             | flat                 | 1057.000 |           0.205 |              -0.021 | 1146.000 |            0.340 |                0.019 |
| % above 50d, 10-day change             | rising (> +5 pts)    | 1858.000 |           0.336 |               0.021 | 1224.000 |            0.430 |                0.047 |
| A/D line, 10-day change                | flat                 | 1135.000 |           0.227 |              -0.016 | 1106.000 |            0.367 |                0.026 |
| A/D line, 10-day change                | falling              | 1351.000 |           0.395 |               0.045 | 2039.000 |            0.374 |                0.031 |
| A/D line, 10-day change                | rising               | 2250.000 |           0.302 |               0.013 | 1452.000 |            0.399 |                0.037 |
| sector & sub-industry today green      | both                 | 1014.000 |           0.301 |               0.014 | 1308.000 |            0.417 |                0.043 |
| sector & sub-industry today green      | neither              | 1287.000 |           0.353 |               0.033 | 1730.000 |            0.392 |                0.040 |
| sector & sub-industry today green      | one of the two       |  428.000 |           0.320 |               0.018 |  593.000 |            0.379 |                0.028 |
| sector & sub-industry up over 5 days   | both                 | 1206.000 |           0.281 |               0.008 | 1325.000 |            0.430 |                0.050 |
| sector & sub-industry up over 5 days   | neither              | 1055.000 |           0.385 |               0.042 | 1798.000 |            0.388 |                0.034 |
| sector & sub-industry up over 5 days   | one of the two       |  467.000 |           0.321 |               0.019 |  508.000 |            0.360 |                0.029 |
| sector & sub-industry above 21 EMA     | both                 | 1262.000 |           0.316 |               0.018 | 1106.000 |            0.436 |                0.049 |
| sector & sub-industry above 21 EMA     | neither              | 1021.000 |           0.348 |               0.031 | 1948.000 |            0.386 |                0.036 |
| sector & sub-industry above 21 EMA     | one of the two       |  446.000 |           0.318 |               0.021 |  577.000 |            0.376 |                0.031 |
| distance above the 21 EMA              | 0-5%                 | 1301.000 |           0.290 |               0.013 |  950.000 |            0.355 |                0.026 |
| distance above the 21 EMA              | 10-15%               |  192.000 |           0.385 |               0.032 |  122.000 |            0.434 |                0.041 |
| distance above the 21 EMA              | 5-10%                |  673.000 |           0.281 |               0.008 |  359.000 |            0.396 |                0.036 |
| distance above the 21 EMA              | > 15%                |   90.000 |           0.356 |               0.013 |   69.000 |            0.464 |                0.045 |
| distance above the 21 EMA              | below                | 2480.000 |           0.323 |               0.017 | 3097.000 |            0.382 |                0.033 |
| ADR%                                   | > 15%                |   45.000 |           0.400 |               0.015 |    3.000 |            0.333 |                0.066 |
| ADR%                                   | 12-15%               |   60.000 |           0.400 |               0.020 |    4.000 |            0.500 |                0.051 |
| ADR%                                   | 3-5%                 | 2388.000 |           0.324 |               0.014 | 2880.000 |            0.391 |                0.035 |
| ADR%                                   | 5-8%                 |  645.000 |           0.340 |               0.006 |  661.000 |            0.424 |                0.030 |
| ADR%                                   | 8-12%                |  187.000 |           0.374 |               0.012 |   60.000 |            0.517 |                0.055 |
| ADR%                                   | < 3%                 | 1411.000 |           0.261 |               0.022 |  989.000 |            0.311 |                0.021 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |   45.000 |           0.400 |               0.015 |    3.000 |            0.333 |                0.066 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |   60.000 |           0.400 |               0.020 |    4.000 |            0.500 |                0.051 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 | 2387.000 |           0.323 |               0.014 | 2880.000 |            0.391 |                0.035 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  644.000 |           0.339 |               0.005 |  661.000 |            0.424 |                0.030 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |  185.000 |           0.373 |               0.011 |   60.000 |            0.517 |                0.055 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 | 1410.000 |           0.261 |               0.022 |  986.000 |            0.311 |                0.021 |
| fundamental inflection (all 4)         | no                   | 2770.000 |           0.304 |               0.018 | 4215.000 |            0.382 |                0.032 |
| fundamental inflection (all 4)         | yes                  |   94.000 |           0.255 |               0.021 |  239.000 |            0.331 |                0.013 |
| revenue growth accelerating            | 1 quarter            |  775.000 |           0.272 |               0.009 | 1004.000 |            0.385 |                0.033 |
| revenue growth accelerating            | 2+ quarters          |  562.000 |           0.351 |               0.039 |  944.000 |            0.359 |                0.023 |
| revenue growth accelerating            | no (decelerating)    | 1527.000 |           0.299 |               0.015 | 2506.000 |            0.385 |                0.034 |
| operating income outgrowing revenue    | no                   | 1221.000 |           0.301 |               0.013 | 2031.000 |            0.397 |                0.033 |
| operating income outgrowing revenue    | yes                  |  898.000 |           0.297 |               0.019 | 1664.000 |            0.349 |                0.019 |
| operating margin vs a year ago         | expanding            |  967.000 |           0.297 |               0.018 | 1797.000 |            0.352 |                0.019 |
| operating margin vs a year ago         | shrinking            | 1151.000 |           0.302 |               0.013 | 1897.000 |            0.397 |                0.034 |
| FCF margin vs a year ago               | improving            | 1153.000 |           0.295 |               0.019 | 2080.000 |            0.358 |                0.024 |
| FCF margin vs a year ago               | worse                | 1410.000 |           0.292 |               0.014 | 2316.000 |            0.402 |                0.038 |
| up/down volume, 50 days                | 0.8-1.0              | 1125.000 |           0.333 |               0.023 | 1305.000 |            0.390 |                0.033 |
| up/down volume, 50 days                | 1.0-1.3              | 1269.000 |           0.318 |               0.017 | 1166.000 |            0.378 |                0.032 |
| up/down volume, 50 days                | < 0.8 (distribution) | 1344.000 |           0.292 |               0.010 | 1441.000 |            0.389 |                0.037 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  998.000 |           0.302 |               0.011 |  685.000 |            0.346 |                0.018 |
| price vs 200-day                       | below                | 2808.000 |           0.325 |               0.017 | 3050.000 |            0.376 |                0.033 |
| price vs 200-day                       | 0-10% above          |  490.000 |           0.296 |               0.011 |  464.000 |            0.405 |                0.033 |
| price vs 200-day                       | 10-30% above         |  870.000 |           0.276 |               0.013 |  592.000 |            0.397 |                0.035 |
| price vs 200-day                       | 30-50% above         |  444.000 |           0.295 |               0.011 |  265.000 |            0.355 |                0.026 |
| price vs 200-day                       | > 50% above          |  124.000 |           0.339 |               0.021 |  226.000 |            0.372 |                0.017 |
| 6-month gain                           | 0-20%                |  749.000 |           0.280 |               0.009 |  653.000 |            0.417 |                0.040 |
| 6-month gain                           | 20-50%               |  713.000 |           0.269 |               0.010 |  615.000 |            0.413 |                0.040 |
| 6-month gain                           | 50-100%              |  416.000 |           0.344 |               0.026 |  361.000 |            0.363 |                0.027 |
| 6-month gain                           | < 0                  | 2768.000 |           0.326 |               0.017 | 2813.000 |            0.369 |                0.031 |
| 6-month gain                           | > 100%               |   90.000 |           0.289 |               0.001 |  155.000 |            0.335 |               -0.001 |
| sector (11 GICS, by median RS)         | bottom 3             | 1030.000 |           0.300 |               0.008 | 1200.000 |            0.383 |                0.039 |
| sector (11 GICS, by median RS)         | middle 5             | 1316.000 |           0.355 |               0.036 | 1898.000 |            0.418 |                0.043 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  664.000 |           0.309 |               0.015 |  693.000 |            0.367 |                0.025 |
| sub-industry (by median RS)            | bottom 30%           | 1064.000 |           0.353 |               0.030 | 1578.000 |            0.411 |                0.043 |
| sub-industry (by median RS)            | middle               |  821.000 |           0.347 |               0.027 | 1245.000 |            0.398 |                0.038 |
| sub-industry (by median RS)            | top 30% (leading)    |  829.000 |           0.276 |               0.011 |  794.000 |            0.380 |                0.034 |
| 3-day market model                     | bottom 10% (skip?)   |  379.000 |           0.425 |               0.044 |   96.000 |            0.573 |                0.086 |
| 3-day market model                     | rest                 | 4357.000 |           0.301 |               0.013 | 4501.000 |            0.376 |                0.031 |

All stocks (no model), +20/-10, by the same splits: does a leading sector help on its own?

| regime                                 | bucket               |       IS_n |   IS_hit_target |   IS_avg_net_return |      OOS_n |   OOS_hit_target |   OOS_avg_net_return |
|:---------------------------------------|:---------------------|-----------:|----------------:|--------------------:|-----------:|-----------------:|---------------------:|
| breadth (stocks above 50d)             | high (> 71%)         |  72866.000 |           0.164 |               0.025 |  73103.000 |            0.209 |                0.008 |
| breadth (stocks above 50d)             | low (< 53%)          |  68458.000 |           0.219 |               0.020 | 108619.000 |            0.262 |                0.021 |
| breadth (stocks above 50d)             | mid                  |  70714.000 |           0.161 |               0.015 | 103082.000 |            0.213 |                0.009 |
| VIX level                              | 15-20                |  59979.000 |           0.164 |               0.018 | 108907.000 |            0.207 |                0.009 |
| VIX level                              | 20-30                |  44046.000 |           0.264 |               0.034 |  86582.000 |            0.274 |                0.021 |
| VIX level                              | < 15                 |  87578.000 |           0.135 |               0.019 |  71916.000 |            0.174 |                0.002 |
| VIX level                              | > 30                 |  20435.000 |           0.242 |               0.003 |  17399.000 |            0.395 |                0.046 |
| VIX / VIX3M                            | 0.9-1.0              |  69439.000 |           0.204 |               0.024 | 104632.000 |            0.244 |                0.017 |
| VIX / VIX3M                            | < 0.9 (calm)         | 120884.000 |           0.156 |               0.020 | 159974.000 |            0.212 |                0.009 |
| VIX / VIX3M                            | > 1.0 (stress)       |  21715.000 |           0.244 |               0.010 |  20198.000 |            0.311 |                0.024 |
| SPY above 200d                         | no                   |  46603.000 |           0.247 |               0.014 |  52617.000 |            0.279 |                0.015 |
| SPY above 200d                         | yes                  | 165435.000 |           0.162 |               0.022 | 232187.000 |            0.220 |                0.012 |
| QQQ above 10 & 20 SMA                  | no                   |  87333.000 |           0.203 |               0.020 | 122665.000 |            0.236 |                0.011 |
| QQQ above 10 & 20 SMA                  | yes                  | 124705.000 |           0.165 |               0.020 | 162139.000 |            0.227 |                0.015 |
| SPY 1-month return                     | -3..0%               |  41848.000 |           0.180 |               0.019 |  45384.000 |            0.226 |                0.015 |
| SPY 1-month return                     | 0..3%                |  76751.000 |           0.163 |               0.020 |  90714.000 |            0.217 |                0.010 |
| SPY 1-month return                     | < -3%                |  29007.000 |           0.261 |               0.021 |  45312.000 |            0.261 |                0.014 |
| SPY 1-month return                     | > 3%                 |  64432.000 |           0.166 |               0.021 | 103394.000 |            0.231 |                0.015 |
| SPY vs 21/50 SMA                       | above 21 & 50        | 130086.000 |           0.162 |               0.021 | 179616.000 |            0.214 |                0.010 |
| SPY vs 21/50 SMA                       | above 21 only        |   9044.000 |           0.204 |               0.015 |  17220.000 |            0.269 |                0.026 |
| SPY vs 21/50 SMA                       | above 50 only        |  22175.000 |           0.131 |               0.000 |  21797.000 |            0.226 |                0.010 |
| SPY vs 21/50 SMA                       | below both           |  50733.000 |           0.246 |               0.027 |  66171.000 |            0.268 |                0.020 |
| QQQ vs 21/50 SMA                       | above 21 & 50        | 128869.000 |           0.159 |               0.017 | 168384.000 |            0.218 |                0.012 |
| QQQ vs 21/50 SMA                       | above 21 only        |  11961.000 |           0.199 |               0.022 |  17141.000 |            0.254 |                0.020 |
| QQQ vs 21/50 SMA                       | above 50 only        |  20698.000 |           0.177 |               0.024 |  30085.000 |            0.224 |                0.009 |
| QQQ vs 21/50 SMA                       | below both           |  50510.000 |           0.233 |               0.025 |  69194.000 |            0.258 |                0.016 |
| A/D line vs its 21/50 MA               | above 21 & 50        | 133032.000 |           0.159 |               0.019 | 172286.000 |            0.210 |                0.009 |
| A/D line vs its 21/50 MA               | above 21 only        |   7870.000 |           0.188 |              -0.011 |   8179.000 |            0.304 |                0.019 |
| A/D line vs its 21/50 MA               | above 50 only        |  26408.000 |           0.164 |               0.021 |  39661.000 |            0.240 |                0.020 |
| A/D line vs its 21/50 MA               | below both           |  44728.000 |           0.255 |               0.028 |  64678.000 |            0.272 |                0.019 |
| % of stocks above 20d                  | 40-60%               |  50657.000 |           0.163 |               0.012 |  75564.000 |            0.206 |                0.003 |
| % of stocks above 20d                  | < 40%                |  50860.000 |           0.226 |               0.024 |  72891.000 |            0.274 |                0.024 |
| % of stocks above 20d                  | > 60%                | 110521.000 |           0.168 |               0.022 | 136349.000 |            0.221 |                0.013 |
| % above 50d, 10-day change             | falling (< -5 pts)   |  84063.000 |           0.193 |               0.024 | 104753.000 |            0.243 |                0.016 |
| % above 50d, 10-day change             | flat                 |  48344.000 |           0.147 |               0.008 |  76841.000 |            0.216 |                0.007 |
| % above 50d, 10-day change             | rising (> +5 pts)    |  79631.000 |           0.188 |               0.023 | 103210.000 |            0.229 |                0.014 |
| A/D line, 10-day change                | flat                 |  58839.000 |           0.166 |               0.014 |  76985.000 |            0.228 |                0.012 |
| A/D line, 10-day change                | falling              |  57110.000 |           0.214 |               0.024 |  78579.000 |            0.268 |                0.021 |
| A/D line, 10-day change                | rising               |  96089.000 |           0.170 |               0.022 | 129240.000 |            0.210 |                0.009 |
| sector & sub-industry today green      | both                 |  78847.000 |           0.163 |               0.019 | 111692.000 |            0.220 |                0.012 |
| sector & sub-industry today green      | neither              |  69656.000 |           0.189 |               0.023 |  95654.000 |            0.241 |                0.017 |
| sector & sub-industry today green      | one of the two       |  27232.000 |           0.177 |               0.023 |  41318.000 |            0.221 |                0.012 |
| sector & sub-industry up over 5 days   | both                 |  87758.000 |           0.161 |               0.020 | 122356.000 |            0.224 |                0.014 |
| sector & sub-industry up over 5 days   | neither              |  60074.000 |           0.195 |               0.022 |  84714.000 |            0.243 |                0.016 |
| sector & sub-industry up over 5 days   | one of the two       |  27887.000 |           0.177 |               0.022 |  41589.000 |            0.211 |                0.008 |
| sector & sub-industry above 21 EMA     | both                 |  96256.000 |           0.158 |               0.022 | 130100.000 |            0.208 |                0.010 |
| sector & sub-industry above 21 EMA     | neither              |  51407.000 |           0.210 |               0.022 |  76328.000 |            0.266 |                0.023 |
| sector & sub-industry above 21 EMA     | one of the two       |  28072.000 |           0.173 |               0.018 |  42236.000 |            0.220 |                0.010 |
| distance above the 21 EMA              | 0-5%                 | 103660.000 |           0.146 |               0.021 | 119405.000 |            0.190 |                0.009 |
| distance above the 21 EMA              | 10-15%               |   2884.000 |           0.289 |               0.012 |   6306.000 |            0.331 |                0.019 |
| distance above the 21 EMA              | 5-10%                |  18141.000 |           0.225 |               0.017 |  30517.000 |            0.264 |                0.014 |
| distance above the 21 EMA              | > 15%                |   1144.000 |           0.298 |              -0.001 |   3033.000 |            0.352 |                0.011 |
| distance above the 21 EMA              | below                |  86209.000 |           0.208 |               0.020 | 125543.000 |            0.254 |                0.016 |
| ADR%                                   | > 15%                |    341.000 |           0.282 |              -0.018 |    345.000 |            0.383 |                0.014 |
| ADR%                                   | 12-15%               |    614.000 |           0.282 |              -0.017 |    551.000 |            0.410 |                0.024 |
| ADR%                                   | 3-5%                 |  45444.000 |           0.299 |               0.018 |  88482.000 |            0.321 |                0.017 |
| ADR%                                   | 5-8%                 |  12466.000 |           0.319 |              -0.000 |  20615.000 |            0.404 |                0.025 |
| ADR%                                   | 8-12%                |   3362.000 |           0.282 |              -0.018 |   3579.000 |            0.450 |                0.038 |
| ADR%                                   | < 3%                 | 149811.000 |           0.130 |               0.024 | 171232.000 |            0.157 |                0.009 |
| ADR% (only stocks trading >= $10M/day) | > 15%                |    297.000 |           0.313 |              -0.008 |    322.000 |            0.385 |                0.015 |
| ADR% (only stocks trading >= $10M/day) | 12-15%               |    537.000 |           0.281 |              -0.018 |    513.000 |            0.409 |                0.024 |
| ADR% (only stocks trading >= $10M/day) | 3-5%                 |  36216.000 |           0.298 |               0.017 |  79372.000 |            0.320 |                0.016 |
| ADR% (only stocks trading >= $10M/day) | 5-8%                 |  10053.000 |           0.315 |              -0.001 |  18839.000 |            0.402 |                0.024 |
| ADR% (only stocks trading >= $10M/day) | 8-12%                |   2758.000 |           0.280 |              -0.018 |   3297.000 |            0.451 |                0.038 |
| ADR% (only stocks trading >= $10M/day) | < 3%                 | 128385.000 |           0.125 |               0.024 | 157032.000 |            0.156 |                0.009 |
| fundamental inflection (all 4)         | no                   | 127363.000 |           0.166 |               0.024 | 244649.000 |            0.234 |                0.013 |
| fundamental inflection (all 4)         | yes                  |   6638.000 |           0.171 |               0.034 |  14143.000 |            0.242 |                0.018 |
| revenue growth accelerating            | 1 quarter            |  35534.000 |           0.163 |               0.025 |  65701.000 |            0.241 |                0.018 |
| revenue growth accelerating            | 2+ quarters          |  31163.000 |           0.172 |               0.030 |  61139.000 |            0.230 |                0.013 |
| revenue growth accelerating            | no (decelerating)    |  67304.000 |           0.164 |               0.023 | 131952.000 |            0.233 |                0.011 |
| operating income outgrowing revenue    | no                   |  48874.000 |           0.187 |               0.027 | 102792.000 |            0.258 |                0.015 |
| operating income outgrowing revenue    | yes                  |  54039.000 |           0.154 |               0.024 | 102598.000 |            0.226 |                0.011 |
| operating margin vs a year ago         | expanding            |  56345.000 |           0.163 |               0.024 | 111510.000 |            0.236 |                0.011 |
| operating margin vs a year ago         | shrinking            |  46280.000 |           0.178 |               0.027 |  93709.000 |            0.250 |                0.016 |
| FCF margin vs a year ago               | improving            |  63479.000 |           0.162 |               0.027 | 134794.000 |            0.239 |                0.015 |
| FCF margin vs a year ago               | worse                |  57995.000 |           0.168 |               0.025 | 119602.000 |            0.231 |                0.012 |
| up/down volume, 50 days                | 0.8-1.0              |  49120.000 |           0.185 |               0.020 |  68542.000 |            0.238 |                0.015 |
| up/down volume, 50 days                | 1.0-1.3              |  65219.000 |           0.169 |               0.021 |  87642.000 |            0.215 |                0.011 |
| up/down volume, 50 days                | < 0.8 (distribution) |  40571.000 |           0.225 |               0.021 |  56145.000 |            0.275 |                0.018 |
| up/down volume, 50 days                | > 1.3 (accumulation) |  57128.000 |           0.158 |               0.019 |  72475.000 |            0.208 |                0.009 |
| price vs 200-day                       | below                |  70268.000 |           0.238 |               0.019 | 112421.000 |            0.267 |                0.015 |
| price vs 200-day                       | 0-10% above          |  64575.000 |           0.132 |               0.024 |  74268.000 |            0.175 |                0.010 |
| price vs 200-day                       | 10-30% above         |  65478.000 |           0.152 |               0.020 |  76023.000 |            0.203 |                0.011 |
| price vs 200-day                       | 30-50% above         |   9195.000 |           0.261 |               0.014 |  15787.000 |            0.307 |                0.017 |
| price vs 200-day                       | > 50% above          |   2522.000 |           0.305 |               0.002 |   6305.000 |            0.386 |                0.023 |
| 6-month gain                           | 0-20%                |  85410.000 |           0.133 |               0.024 |  97581.000 |            0.176 |                0.010 |
| 6-month gain                           | 20-50%               |  44404.000 |           0.169 |               0.018 |  55405.000 |            0.228 |                0.013 |
| 6-month gain                           | 50-100%              |   8458.000 |           0.268 |               0.011 |  15213.000 |            0.337 |                0.023 |
| 6-month gain                           | < 0                  |  71933.000 |           0.230 |               0.019 | 112484.000 |            0.260 |                0.014 |
| 6-month gain                           | > 100%               |   1833.000 |           0.315 |               0.005 |   4121.000 |            0.385 |                0.020 |
| sector (11 GICS, by median RS)         | bottom 3             |  44216.000 |           0.175 |               0.021 |  56370.000 |            0.229 |                0.015 |
| sector (11 GICS, by median RS)         | middle 5             |  92664.000 |           0.179 |               0.023 | 127476.000 |            0.232 |                0.015 |
| sector (11 GICS, by median RS)         | top 3 (leading)      |  51329.000 |           0.169 |               0.017 |  75343.000 |            0.220 |                0.011 |
| sub-industry (by median RS)            | bottom 30%           |  46312.000 |           0.191 |               0.023 |  68888.000 |            0.236 |                0.012 |
| sub-industry (by median RS)            | middle               |  75636.000 |           0.166 |               0.022 | 104740.000 |            0.220 |                0.016 |
| sub-industry (by median RS)            | top 30% (leading)    |  53137.000 |           0.174 |               0.018 |  74799.000 |            0.233 |                0.013 |
| 3-day market model                     | bottom 10% (skip?)   |  21312.000 |           0.224 |               0.023 |   3145.000 |            0.461 |                0.077 |
| 3-day market model                     | rest                 | 190726.000 |           0.176 |               0.020 | 281659.000 |            0.228 |                0.012 |

Regime gates, one family at a time: skip the buckets of that family that were below break-even in-sample (hit < 33% or negative return), then trade the model's top 10% with +20/-10. RULE rows keep only the picks that pass a rule fixed in advance: leading groups (run 19: top 3 of 11 sectors / top 30% of sub-industries by median RS) and the user's run-21 rules (SPY/QQQ vs 21 & 50 SMA, breadth, A/D line, sector & sub-industry green / up 5 days / above 21 EMA; groups = equal-weight median of member stocks). Portfolio 2018+:

| gate                                                                        | skipped (chosen IS)                                  |   CAGR |   max_DD |   trades |   PIT CAGR |   PIT max_DD |
|:----------------------------------------------------------------------------|:-----------------------------------------------------|-------:|---------:|---------:|-----------:|-------------:|
| breadth (stocks above 50d)                                                  | high (> 71%), mid                                    |  0.149 |   -0.374 |      716 |      0.065 |       -0.258 |
| VIX level                                                                   | 15-20, < 15                                          |  0.239 |   -0.273 |      677 |      0.126 |       -0.307 |
| VIX / VIX3M                                                                 | < 0.9 (calm), > 1.0 (stress)                         |  0.165 |   -0.343 |      791 |      0.078 |       -0.296 |
| SPY above 200d                                                              | yes                                                  |  0.107 |   -0.274 |      325 |      0.054 |       -0.210 |
| QQQ above 10 & 20 SMA                                                       | yes                                                  |  0.208 |   -0.371 |      907 |     -0.010 |       -0.402 |
| SPY 1-month return                                                          | -3..0%, > 3%                                         |  0.136 |   -0.458 |      956 |      0.087 |       -0.272 |
| SPY vs 21/50 SMA                                                            | above 21 & 50, above 50 only                         |  0.083 |   -0.511 |      546 |      0.041 |       -0.309 |
| QQQ vs 21/50 SMA                                                            | above 21 & 50                                        |  0.154 |   -0.287 |      813 |     -0.021 |       -0.484 |
| A/D line vs its 21/50 MA                                                    | above 21 & 50, above 50 only                         |  0.143 |   -0.350 |      590 |      0.069 |       -0.226 |
| % of stocks above 20d                                                       | 40-60%, > 60%                                        |  0.138 |   -0.359 |      668 |      0.027 |       -0.329 |
| % above 50d, 10-day change                                                  | flat                                                 |  0.228 |   -0.335 |     1132 |      0.115 |       -0.301 |
| A/D line, 10-day change                                                     | flat, rising                                         |  0.110 |   -0.401 |      695 |      0.027 |       -0.326 |
| sector & sub-industry today green                                           | both, one of the two                                 |  0.205 |   -0.478 |     1131 |     -0.013 |       -0.373 |
| sector & sub-industry up over 5 days                                        | both                                                 |  0.206 |   -0.403 |     1140 |      0.073 |       -0.322 |
| sector & sub-industry above 21 EMA                                          | both, one of the two                                 |  0.234 |   -0.396 |     1135 |      0.037 |       -0.308 |
| distance above the 21 EMA                                                   | 0-5%, 5-10%, > 15%                                   |  0.117 |   -0.505 |     1151 |      0.141 |       -0.279 |
| ADR%                                                                        | < 3%                                                 |  0.231 |   -0.396 |     1227 |      0.152 |       -0.329 |
| ADR% (only stocks trading >= $10M/day)                                      | < 3%                                                 |  0.214 |   -0.416 |     1220 |      0.152 |       -0.320 |
| fundamental inflection (all 4)                                              | no, yes                                              |  0.155 |   -0.252 |      741 |      0.041 |       -0.119 |
| revenue growth accelerating                                                 | 1 quarter, no (decelerating)                         |  0.203 |   -0.403 |     1080 |      0.101 |       -0.268 |
| operating income outgrowing revenue                                         | no, yes                                              |  0.168 |   -0.413 |      901 |      0.143 |       -0.212 |
| operating margin vs a year ago                                              | expanding, shrinking                                 |  0.161 |   -0.413 |      917 |      0.143 |       -0.212 |
| FCF margin vs a year ago                                                    | improving, worse                                     |  0.155 |   -0.307 |      817 |      0.054 |       -0.128 |
| up/down volume, 50 days                                                     | 1.0-1.3, > 1.3 (accumulation)                        |  0.158 |   -0.411 |     1126 |      0.128 |       -0.287 |
| price vs 200-day                                                            | 0-10% above, 10-30% above, 30-50% above, > 50% above |  0.236 |   -0.390 |     1106 |      0.161 |       -0.284 |
| 6-month gain                                                                | 0-20%, 20-50%, 50-100%, > 100%                       |  0.261 |   -0.364 |     1086 |      0.135 |       -0.314 |
| sector (11 GICS, by median RS)                                              | bottom 3, top 3 (leading)                            |  0.243 |   -0.517 |     1139 |      0.072 |       -0.439 |
| sub-industry (by median RS)                                                 | middle, top 30% (leading)                            |  0.214 |   -0.502 |     1119 |      0.092 |       -0.309 |
| 3-day market model                                                          | rest                                                 |  0.067 |   -0.068 |       69 |      0.013 |       -0.051 |
| RULE: top 3 sectors only                                                    | nothing                                              |  0.214 |   -0.295 |      890 |      0.058 |       -0.265 |
| RULE: top 30% sub-industries only                                           | nothing                                              |  0.246 |   -0.250 |      915 |      0.130 |       -0.230 |
| RULE: top 3 sectors AND top 30% sub-industries                              | nothing                                              |  0.195 |   -0.272 |      777 |      0.029 |       -0.172 |
| RULE: SPY above its 21 & 50 SMA                                             | nothing                                              |  0.238 |   -0.340 |      872 |      0.172 |       -0.235 |
| RULE: QQQ above its 21 & 50 SMA                                             | nothing                                              |  0.191 |   -0.296 |      850 |      0.168 |       -0.218 |
| RULE: SPY above its 50 SMA (21 either way)                                  | nothing                                              |  0.223 |   -0.402 |      939 |      0.145 |       -0.308 |
| RULE: A/D line above its 21 & 50 MA                                         | nothing                                              |  0.173 |   -0.400 |      862 |      0.132 |       -0.241 |
| RULE: > 50% of stocks above their 50d                                       | nothing                                              |  0.134 |   -0.376 |      862 |      0.111 |       -0.288 |
| RULE: % above 50d rising over 10 days                                       | nothing                                              |  0.198 |   -0.430 |      942 |      0.123 |       -0.260 |
| RULE: sector AND sub-industry green today                                   | nothing                                              |  0.165 |   -0.374 |     1004 |      0.133 |       -0.233 |
| RULE: sector AND sub-industry up over 5 days                                | nothing                                              |  0.105 |   -0.427 |      992 |      0.108 |       -0.331 |
| RULE: sector AND sub-industry above 21 EMA                                  | nothing                                              |  0.139 |   -0.355 |      954 |      0.159 |       -0.235 |
| RULE: SPY > 21 & 50 + sector & sub-industry up 5 days                       | nothing                                              |  0.142 |   -0.299 |      784 |      0.101 |       -0.141 |
| RULE: <= 10% above the 21 EMA (course rule)                                 | nothing                                              |  0.214 |   -0.447 |     1191 |      0.117 |       -0.315 |
| RULE: ADR% >= 5% (the infographic's minimum)                                | nothing                                              |  0.217 |   -0.545 |     1455 |      0.117 |       -0.246 |
| RULE: ADR% 5-12% (the infographic's sweet spot)                             | nothing                                              |  0.216 |   -0.521 |     1421 |      0.114 |       -0.257 |
| RULE: ADR% <= 15% (skip the wildest)                                        | nothing                                              |  0.269 |   -0.448 |     1183 |      0.107 |       -0.328 |
| RULE: ADR% 5-12% and >= $10M/day                                            | nothing                                              |  0.174 |   -0.555 |     1381 |      0.114 |       -0.257 |
| RULE: fundamental inflection (rev accel 2q + op leverage + margin + FCF up) | nothing                                              |  0.192 |   -0.253 |      570 |      0.018 |       -0.186 |
| RULE: revenue growth accelerating 2+ quarters                               | nothing                                              |  0.339 |   -0.354 |      984 |      0.096 |       -0.258 |
| RULE: accumulation (up/down volume 50d > 1)                                 | nothing                                              |  0.141 |   -0.427 |     1057 |      0.037 |       -0.334 |
| RULE: not extended (< 30% above the 200-day)                                | nothing                                              |  0.234 |   -0.425 |     1164 |      0.151 |       -0.309 |
| RULE: not already up 50%+ in 6 months                                       | nothing                                              |  0.278 |   -0.446 |     1186 |      0.160 |       -0.307 |
| RULE: price rules only (accumulation + not extended + not up 50%)           | nothing                                              |  0.210 |   -0.452 |      969 |      0.052 |       -0.377 |
| RULE: user's full method (inflection + price rules)                         | nothing                                              |  0.048 |   -0.137 |      242 |     -0.006 |       -0.159 |
| METHOD: user's method alone, no model (inflection + price rules)            | nothing                                              |  0.098 |   -0.257 |      579 |      0.022 |       -0.202 |
| METHOD: fundamental inflection alone, no model                              | nothing                                              |  0.112 |   -0.382 |      723 |      0.089 |       -0.273 |
| MODEL + fundamentals as features, top 10%                                   | nothing                                              |  0.287 |   -0.440 |     1194 |      0.113 |       -0.384 |
| SIZE: position scaled by 6% / ADR (x0.4-1.5)                                | nothing                                              |  0.214 |   -0.351 |     1159 |      0.163 |       -0.317 |
| (no gate)                                                                   | nothing                                              |  0.270 |   -0.401 |     1190 |      0.105 |       -0.328 |

## 11. Qullamaggie replication (per trade, out-of-sample 2018+; IS in brackets)

Scan = top 3% performer over 1, 3 or 6 months with ADR >= 4%. Regime = QQQ above its 10- and 20-day SMAs. qull_breakout = buy-stop above the flag high the next day (fill at the trigger or the gap open), stop at the tighter of the 3-day low and 1 ADR; a same-day touch of the stop counts as stopped out. Portfolio rows start with QULL in section 9.

| entry            | filter           | exit          |   IS_n |   IS_win |   IS_avgR |   OOS_n |   OOS_per_yr |   OOS_win |   OOS_avgR |   OOS_pf |   OOS_t |
|:-----------------|:-----------------|:--------------|-------:|---------:|----------:|--------:|-------------:|----------:|-----------:|---------:|--------:|
| ep_gap10         | all              | bracket_20_10 |    549 |     0.46 |      0.18 |     962 |       109.73 |      0.41 |       0.10 |     1.18 |    2.33 |
| ep_gap10         | all              | qull_sma10    |    564 |     0.44 |     -0.01 |     962 |       109.73 |      0.44 |      -0.01 |     0.99 |   -0.14 |
| ep_gap10         | all              | qull_sma20    |    562 |     0.46 |     -0.04 |     962 |       109.73 |      0.44 |       0.06 |     1.11 |    1.02 |
| ep_gap10         | all              | sma50_close   |    553 |     0.29 |      0.13 |     962 |       109.73 |      0.31 |       0.46 |     1.69 |    3.48 |
| ep_gap10         | qull_scan        | bracket_20_10 |    128 |     0.36 |      0.04 |     272 |        31.03 |      0.43 |       0.22 |     1.37 |    2.43 |
| ep_gap10         | qull_scan        | qull_sma10    |    130 |     0.40 |     -0.05 |     272 |        31.03 |      0.43 |      -0.05 |     0.90 |   -0.70 |
| ep_gap10         | qull_scan        | qull_sma20    |    128 |     0.42 |     -0.09 |     272 |        31.03 |      0.44 |       0.12 |     1.23 |    1.06 |
| ep_gap10         | qull_scan        | sma50_close   |    126 |     0.21 |      0.00 |     272 |        31.03 |      0.32 |       0.71 |     2.05 |    2.44 |
| ep_gap10         | qull_scan_regime | bracket_20_10 |     84 |     0.33 |     -0.04 |     171 |        19.51 |      0.42 |       0.18 |     1.30 |    1.62 |
| ep_gap10         | qull_scan_regime | qull_sma10    |     85 |     0.42 |     -0.06 |     171 |        19.51 |      0.43 |      -0.04 |     0.91 |   -0.45 |
| ep_gap10         | qull_scan_regime | qull_sma20    |     85 |     0.45 |     -0.03 |     171 |        19.51 |      0.45 |       0.21 |     1.41 |    1.31 |
| ep_gap10         | qull_scan_regime | sma50_close   |     83 |     0.17 |      0.08 |     171 |        19.51 |      0.32 |       0.92 |     2.39 |    2.30 |
| ep_gap8_hold     | all              | bracket_20_10 |    764 |     0.48 |      0.20 |    1213 |       138.37 |      0.42 |       0.10 |     1.18 |    2.62 |
| ep_gap8_hold     | all              | qull_sma10    |    782 |     0.46 |      0.02 |    1213 |       138.37 |      0.45 |      -0.02 |     0.95 |   -0.66 |
| ep_gap8_hold     | all              | qull_sma20    |    779 |     0.48 |      0.02 |    1213 |       138.37 |      0.46 |       0.02 |     1.04 |    0.48 |
| ep_gap8_hold     | all              | sma50_close   |    771 |     0.33 |      0.24 |    1213 |       138.37 |      0.31 |       0.35 |     1.54 |    3.32 |
| ep_gap8_hold     | qull_scan        | bracket_20_10 |    153 |     0.36 |      0.03 |     292 |        33.31 |      0.45 |       0.24 |     1.41 |    2.78 |
| ep_gap8_hold     | qull_scan        | qull_sma10    |    156 |     0.42 |     -0.01 |     292 |        33.31 |      0.49 |       0.04 |     1.09 |    0.59 |
| ep_gap8_hold     | qull_scan        | qull_sma20    |    154 |     0.42 |     -0.04 |     292 |        33.31 |      0.50 |       0.19 |     1.40 |    1.77 |
| ep_gap8_hold     | qull_scan        | sma50_close   |    153 |     0.22 |      0.04 |     292 |        33.31 |      0.33 |       0.75 |     2.13 |    2.74 |
| ep_gap8_hold     | qull_scan_regime | bracket_20_10 |    106 |     0.35 |      0.01 |     184 |        20.99 |      0.42 |       0.20 |     1.34 |    1.84 |
| ep_gap8_hold     | qull_scan_regime | qull_sma10    |    108 |     0.44 |      0.00 |     184 |        20.99 |      0.49 |       0.02 |     1.05 |    0.26 |
| ep_gap8_hold     | qull_scan_regime | qull_sma20    |    107 |     0.43 |     -0.00 |     184 |        20.99 |      0.51 |       0.23 |     1.49 |    1.57 |
| ep_gap8_hold     | qull_scan_regime | sma50_close   |    106 |     0.20 |      0.14 |     184 |        20.99 |      0.33 |       0.93 |     2.39 |    2.45 |
| qull_breakout    | all              | bracket_20_10 |   2606 |     0.37 |      0.01 |    4543 |       518.22 |      0.41 |       0.14 |     1.24 |    6.67 |
| qull_breakout    | all              | qull_sma10    |   2617 |     0.33 |     -0.32 |    4543 |       518.22 |      0.34 |      -0.25 |     0.64 |  -10.97 |
| qull_breakout    | all              | qull_sma20    |   2615 |     0.33 |     -0.34 |    4543 |       518.22 |      0.34 |      -0.22 |     0.69 |   -8.39 |
| qull_breakout    | all              | sma50_close   |   2610 |     0.14 |     -0.39 |    4543 |       518.22 |      0.17 |       0.01 |     1.01 |    0.16 |
| qull_breakout    | qull_scan        | bracket_20_10 |    651 |     0.39 |      0.10 |    1232 |       140.53 |      0.38 |       0.08 |     1.12 |    1.91 |
| qull_breakout    | qull_scan        | qull_sma10    |    653 |     0.35 |     -0.27 |    1232 |       140.53 |      0.36 |      -0.17 |     0.74 |   -3.91 |
| qull_breakout    | qull_scan        | qull_sma20    |    653 |     0.35 |     -0.26 |    1232 |       140.53 |      0.36 |      -0.16 |     0.76 |   -3.17 |
| qull_breakout    | qull_scan        | sma50_close   |    651 |     0.17 |     -0.26 |    1232 |       140.53 |      0.17 |       0.06 |     1.07 |    0.45 |
| qull_breakout    | qull_scan_regime | bracket_20_10 |    444 |     0.38 |      0.08 |     791 |        90.23 |      0.41 |       0.19 |     1.30 |    3.45 |
| qull_breakout    | qull_scan_regime | qull_sma10    |    446 |     0.34 |     -0.30 |     791 |        90.23 |      0.38 |      -0.11 |     0.82 |   -2.01 |
| qull_breakout    | qull_scan_regime | qull_sma20    |    446 |     0.34 |     -0.29 |     791 |        90.23 |      0.38 |      -0.06 |     0.90 |   -0.95 |
| qull_breakout    | qull_scan_regime | sma50_close   |    444 |     0.17 |     -0.22 |     791 |        90.23 |      0.19 |       0.26 |     1.30 |    1.26 |
| qull_breakout_60 | all              | bracket_20_10 |    932 |     0.35 |      0.01 |    1942 |       221.52 |      0.42 |       0.19 |     1.31 |    5.45 |
| qull_breakout_60 | all              | qull_sma10    |    932 |     0.36 |     -0.29 |    1942 |       221.52 |      0.33 |      -0.24 |     0.65 |   -6.97 |
| qull_breakout_60 | all              | qull_sma20    |    932 |     0.36 |     -0.32 |    1942 |       221.52 |      0.33 |      -0.22 |     0.70 |   -5.46 |
| qull_breakout_60 | all              | sma50_close   |    932 |     0.15 |     -0.30 |    1942 |       221.52 |      0.17 |       0.11 |     1.12 |    0.84 |
| qull_breakout_60 | qull_scan        | bracket_20_10 |    390 |     0.36 |      0.04 |     873 |        99.58 |      0.39 |       0.10 |     1.16 |    2.07 |
| qull_breakout_60 | qull_scan        | qull_sma10    |    390 |     0.35 |     -0.29 |     873 |        99.58 |      0.35 |      -0.18 |     0.72 |   -3.47 |
| qull_breakout_60 | qull_scan        | qull_sma20    |    390 |     0.35 |     -0.27 |     873 |        99.58 |      0.35 |      -0.18 |     0.73 |   -3.05 |
| qull_breakout_60 | qull_scan        | sma50_close   |    390 |     0.16 |     -0.26 |     873 |        99.58 |      0.17 |       0.12 |     1.13 |    0.62 |
| qull_breakout_60 | qull_scan_regime | bracket_20_10 |    272 |     0.35 |      0.01 |     584 |        66.62 |      0.42 |       0.20 |     1.33 |    3.22 |
| qull_breakout_60 | qull_scan_regime | qull_sma10    |    272 |     0.33 |     -0.34 |     584 |        66.62 |      0.37 |      -0.15 |     0.77 |   -2.26 |
| qull_breakout_60 | qull_scan_regime | qull_sma20    |    272 |     0.33 |     -0.30 |     584 |        66.62 |      0.37 |      -0.11 |     0.84 |   -1.34 |
| qull_breakout_60 | qull_scan_regime | sma50_close   |    272 |     0.15 |     -0.27 |     584 |        66.62 |      0.18 |       0.27 |     1.30 |    1.00 |
| random_uptrend   | all              | bracket_20_10 |  30841 |     0.53 |      0.18 |   34706 |      3958.89 |      0.45 |       0.09 |     1.18 |   13.52 |
| random_uptrend   | all              | qull_sma10    |  31697 |     0.30 |     -0.15 |   34706 |      3958.89 |      0.30 |      -0.11 |     0.87 |   -8.39 |
| random_uptrend   | all              | qull_sma20    |  31651 |     0.30 |     -0.14 |   34706 |      3958.89 |      0.29 |      -0.10 |     0.88 |   -7.09 |
| random_uptrend   | all              | sma50_close   |  31459 |     0.14 |     -0.04 |   34706 |      3958.89 |      0.14 |      -0.02 |     0.98 |   -0.89 |
| random_uptrend   | qull_scan        | bracket_20_10 |   1050 |     0.35 |     -0.02 |    2078 |       237.04 |      0.40 |       0.16 |     1.25 |    4.70 |
| random_uptrend   | qull_scan        | qull_sma10    |   1055 |     0.32 |     -0.12 |    2078 |       237.04 |      0.32 |       0.12 |     1.16 |    1.99 |
| random_uptrend   | qull_scan        | qull_sma20    |   1054 |     0.32 |     -0.11 |    2078 |       237.04 |      0.32 |       0.09 |     1.12 |    1.52 |
| random_uptrend   | qull_scan        | sma50_close   |   1051 |     0.13 |     -0.14 |    2078 |       237.04 |      0.16 |       0.23 |     1.24 |    2.21 |
| random_uptrend   | qull_scan_regime | bracket_20_10 |    603 |     0.34 |     -0.04 |    1256 |       143.27 |      0.41 |       0.19 |     1.31 |    4.50 |
| random_uptrend   | qull_scan_regime | qull_sma10    |    607 |     0.32 |     -0.13 |    1256 |       143.27 |      0.34 |       0.17 |     1.24 |    2.19 |
| random_uptrend   | qull_scan_regime | qull_sma20    |    606 |     0.32 |     -0.18 |    1256 |       143.27 |      0.33 |       0.12 |     1.16 |    1.48 |
| random_uptrend   | qull_scan_regime | sma50_close   |    606 |     0.13 |     -0.27 |    1256 |       143.27 |      0.17 |       0.34 |     1.36 |    2.34 |

## 9. Portfolio simulation, 2018 -> today ($100k, 1% risk/trade, max 10 positions, no leverage)

| strategy                                                                                                           |   CAGR |   max_DD |   max_DD_realized |   trades |    win |   avg_positions |   top2_years_share |
|:-------------------------------------------------------------------------------------------------------------------|-------:|---------:|------------------:|---------:|-------:|----------------:|-------------------:|
| wf_scan_pullback / wf_scan / bracket_20_10                                                                         |   0.00 |    -0.40 |             -0.39 |   691.00 |   0.41 |            9.01 |              21.56 |
| donchian_20 / all / bracket_20_10                                                                                  |   0.08 |    -0.45 |             -0.43 |   819.00 |   0.40 |            9.20 |               1.15 |
| pocket_pivot / all / bracket_20_10                                                                                 |   0.06 |    -0.35 |             -0.34 |   580.00 |   0.42 |            7.43 |               0.73 |
| wf_scan_base / all / bracket_20_10                                                                                 |   0.07 |    -0.24 |             -0.23 |   509.00 |   0.50 |            9.61 |               0.90 |
| donchian_55 / all / bracket_20_10                                                                                  |   0.05 |    -0.32 |             -0.30 |   778.00 |   0.40 |            9.02 |               1.19 |
| All setups, ML-filtered (top third), ranked by ML / bracket_20_10                                                  |   0.17 |    -0.30 |             -0.26 |   708.00 |   0.45 |            8.61 |               0.47 |
| All setups, ranked by RS / bracket_20_10                                                                           |   0.22 |    -0.46 |             -0.43 |  1148.00 |   0.42 |            9.31 |               0.44 |
| All setups, random order / bracket_20_10                                                                           |   0.05 |    -0.35 |             -0.31 |   525.00 |   0.45 |            8.53 |               1.15 |
| All setups + rs80_early filter, ranked by RS / bracket_20_10                                                       |   0.11 |    -0.29 |             -0.25 |   866.00 |   0.40 |            8.96 |               0.70 |
| BASELINE random entries, ranked by RS / bracket_20_10                                                              |   0.03 |    -0.47 |             -0.42 |   666.00 |   0.39 |            7.34 |               2.77 |
| BASELINE random entries, random order / bracket_20_10                                                              |   0.07 |    -0.34 |             -0.29 |   409.00 |   0.48 |            7.14 |               0.86 |
| IS-selected setups (5), ranked by RS / bracket_20_10                                                               |   0.06 |    -0.25 |             -0.20 |   528.00 |   0.44 |            8.21 |               0.84 |
| IS-selected setups, only when SPY > 200d / bracket_20_10                                                           |  -0.01 |    -0.30 |             -0.26 |   465.00 |   0.40 |            7.24 |             nan    |
| IS-selected setups (29), ranked by RS / sma50_close                                                                |   0.04 |    -0.55 |             -0.48 |   995.00 |   0.26 |            9.07 |               1.34 |
| IS-selected setups, only when SPY > 200d / sma50_close                                                             |   0.05 |    -0.57 |             -0.53 |   843.00 |   0.25 |            7.76 |               1.41 |
| All setups, ranked by RS / sma50_close                                                                             |   0.09 |    -0.53 |             -0.46 |  1192.00 |   0.28 |            8.88 |               0.61 |
| Top 5 strategies by IS expectancy (own exits), ranked by RS                                                        |   0.15 |    -0.27 |             -0.20 |   408.00 |   0.30 |            5.34 |               0.44 |
| Top 10 strategies by IS expectancy (own exits), ranked by RS                                                       |   0.10 |    -0.28 |             -0.25 |   435.00 |   0.30 |            5.56 |               0.59 |
| Top 20 strategies by IS expectancy (own exits), ranked by RS                                                       |   0.09 |    -0.38 |             -0.27 |   484.00 |   0.28 |            5.88 |               0.69 |
| Top 20 by IS expectancy, adaptive sizing (x0.5 / x1.5 by last 20 trades)                                           |   0.09 |    -0.33 |             -0.18 |   487.00 |   0.30 |            6.14 |               0.63 |
| Top 20 by IS expectancy, ranked by superperformer model                                                            |   0.10 |    -0.37 |             -0.29 |   483.00 |   0.28 |            5.86 |               0.66 |
| All setups, ranked by superperformer model / bracket_20_10                                                         |   0.19 |    -0.48 |             -0.48 |  1457.00 |   0.39 |            9.22 |               0.41 |
| Only setups in the model's top 10% likely superperformers / sma50_close                                            |   0.27 |    -0.51 |             -0.39 |  1389.00 |   0.30 |            8.98 |               0.56 |
| CHECK random entries in the model's top 10% / sma50_close                                                          |   0.08 |    -0.49 |             -0.42 |  1011.00 |   0.16 |            5.23 |               0.90 |
| CHECK top 10% model, leaders only (within 40% of 52w high) / sma50_close                                           |   0.16 |    -0.45 |             -0.34 |  1345.00 |   0.28 |            8.84 |               0.57 |
| Top 10% model + adaptive sizing / sma50_close                                                                      |   0.20 |    -0.54 |             -0.48 |  1473.00 |   0.29 |            9.28 |               0.81 |
| Top 10% CLEAN model (+40% before -20%) / sma50_close                                                               |   0.23 |    -0.53 |             -0.43 |  1408.00 |   0.31 |            8.93 |               0.70 |
| GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10                                                  |   0.29 |    -0.51 |             -0.48 |  1232.00 |   0.42 |            9.36 |               0.49 |
| GOAL b20: model top 10% + adaptive sizing / bracket_20_10                                                          |   0.29 |    -0.44 |             -0.41 |  1212.00 |   0.42 |            9.15 |               0.57 |
| GOAL b20: setups in the model's top 10% / bracket_20_10                                                            |   0.17 |    -0.33 |             -0.31 |  1002.00 |   0.40 |            8.73 |               0.55 |
| GOAL b20: model top 10%, S&P 500 point-in-time only / bracket_20_10                                                |   0.13 |    -0.35 |             -0.34 |   822.00 |   0.41 |            8.25 |               0.65 |
| GOAL b10: model's top 10% stocks, no setup needed / bracket_10_10                                                  |   0.16 |    -0.41 |             -0.39 |  1344.00 |   0.56 |            8.48 |               0.54 |
| GOAL b10: model top 10% + adaptive sizing / bracket_10_10                                                          |   0.12 |    -0.35 |             -0.32 |  1311.00 |   0.56 |            8.24 |               0.54 |
| GOAL b10: setups in the model's top 10% / bracket_10_10                                                            |   0.12 |    -0.37 |             -0.35 |  1019.00 |   0.56 |            7.21 |               0.73 |
| GOAL b10: model top 10%, S&P 500 point-in-time only / bracket_10_10                                                |   0.13 |    -0.26 |             -0.24 |   895.00 |   0.57 |            7.05 |               0.54 |
| MENU top 10% model / +10% -10%                                                                                     |   0.20 |    -0.42 |             -0.41 |  1973.00 |   0.55 |            8.65 |               0.63 |
| MENU top 10% model / +20% -10%                                                                                     |   0.27 |    -0.40 |             -0.38 |  1190.00 |   0.42 |            9.06 |               0.57 |
| MENU top 10% model / +30% -5% (IS best return per month)                                                           |   0.15 |    -0.57 |             -0.53 |  1030.00 |   0.21 |            5.77 |               0.91 |
| MENU top 10% model / +30% -15% (IS best return per trade)                                                          |   0.16 |    -0.39 |             -0.35 |   686.00 |   0.46 |            9.39 |               0.58 |
| REGIME breadth (stocks above 50d): skip ['high (> 71%)', 'mid'] / +20% -10%                                        |   0.15 |    -0.37 |             -0.36 |   716.00 |   0.41 |            5.53 |               0.46 |
| REGIME breadth (stocks above 50d), S&P 500 point-in-time only / +20% -10%                                          |   0.07 |    -0.26 |             -0.21 |   418.00 |   0.41 |            4.62 |               0.68 |
| REGIME VIX level: skip ['15-20', '< 15'] / +20% -10%                                                               |   0.24 |    -0.27 |             -0.24 |   677.00 |   0.45 |            5.39 |               0.47 |
| REGIME VIX level, S&P 500 point-in-time only / +20% -10%                                                           |   0.13 |    -0.31 |             -0.28 |   416.00 |   0.46 |            4.32 |               0.77 |
| REGIME VIX / VIX3M: skip ['< 0.9 (calm)', '> 1.0 (stress)'] / +20% -10%                                            |   0.17 |    -0.34 |             -0.32 |   791.00 |   0.42 |            6.41 |               0.67 |
| REGIME VIX / VIX3M, S&P 500 point-in-time only / +20% -10%                                                         |   0.08 |    -0.30 |             -0.26 |   475.00 |   0.42 |            4.89 |               0.96 |
| REGIME SPY above 200d: skip ['yes'] / +20% -10%                                                                    |   0.11 |    -0.27 |             -0.24 |   325.00 |   0.46 |            2.18 |               0.78 |
| REGIME SPY above 200d, S&P 500 point-in-time only / +20% -10%                                                      |   0.05 |    -0.21 |             -0.18 |   201.00 |   0.45 |            1.72 |               0.89 |
| REGIME QQQ above 10 & 20 SMA: skip ['yes'] / +20% -10%                                                             |   0.21 |    -0.37 |             -0.35 |   907.00 |   0.42 |            7.26 |               0.47 |
| REGIME QQQ above 10 & 20 SMA, S&P 500 point-in-time only / +20% -10%                                               |  -0.01 |    -0.40 |             -0.35 |   517.00 |   0.37 |            5.64 |             nan    |
| REGIME SPY 1-month return: skip ['-3..0%', '> 3%'] / +20% -10%                                                     |   0.14 |    -0.46 |             -0.42 |   956.00 |   0.40 |            7.52 |               0.68 |
| REGIME SPY 1-month return, S&P 500 point-in-time only / +20% -10%                                                  |   0.09 |    -0.27 |             -0.24 |   537.00 |   0.42 |            5.70 |               0.61 |
| REGIME SPY vs 21/50 SMA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%                                       |   0.08 |    -0.51 |             -0.50 |   546.00 |   0.40 |            4.38 |               0.69 |
| REGIME SPY vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                                                    |   0.04 |    -0.31 |             -0.30 |   351.00 |   0.41 |            3.88 |               1.12 |
| REGIME QQQ vs 21/50 SMA: skip ['above 21 & 50'] / +20% -10%                                                        |   0.15 |    -0.29 |             -0.27 |   813.00 |   0.41 |            6.45 |               0.47 |
| REGIME QQQ vs 21/50 SMA, S&P 500 point-in-time only / +20% -10%                                                    |  -0.02 |    -0.48 |             -0.44 |   501.00 |   0.36 |            5.25 |             nan    |
| REGIME A/D line vs its 21/50 MA: skip ['above 21 & 50', 'above 50 only'] / +20% -10%                               |   0.14 |    -0.35 |             -0.34 |   590.00 |   0.42 |            4.35 |               0.69 |
| REGIME A/D line vs its 21/50 MA, S&P 500 point-in-time only / +20% -10%                                            |   0.07 |    -0.23 |             -0.22 |   350.00 |   0.43 |            3.71 |               0.66 |
| REGIME % of stocks above 20d: skip ['40-60%', '> 60%'] / +20% -10%                                                 |   0.14 |    -0.36 |             -0.33 |   668.00 |   0.42 |            5.35 |               0.61 |
| REGIME % of stocks above 20d, S&P 500 point-in-time only / +20% -10%                                               |   0.03 |    -0.33 |             -0.28 |   391.00 |   0.39 |            4.47 |               1.42 |
| REGIME % above 50d, 10-day change: skip ['flat'] / +20% -10%                                                       |   0.23 |    -0.34 |             -0.29 |  1132.00 |   0.41 |            8.65 |               0.62 |
| REGIME % above 50d, 10-day change, S&P 500 point-in-time only / +20% -10%                                          |   0.12 |    -0.30 |             -0.27 |   658.00 |   0.42 |            6.84 |               0.74 |
| REGIME A/D line, 10-day change: skip ['flat', 'rising'] / +20% -10%                                                |   0.11 |    -0.40 |             -0.36 |   695.00 |   0.41 |            5.76 |               0.52 |
| REGIME A/D line, 10-day change, S&P 500 point-in-time only / +20% -10%                                             |   0.03 |    -0.33 |             -0.28 |   418.00 |   0.39 |            4.48 |               1.81 |
| REGIME sector & sub-industry today green: skip ['both', 'one of the two'] / +20% -10%                              |   0.20 |    -0.48 |             -0.47 |  1131.00 |   0.41 |            8.77 |               0.66 |
| REGIME sector & sub-industry today green, S&P 500 point-in-time only / +20% -10%                                   |  -0.01 |    -0.37 |             -0.34 |   667.00 |   0.37 |            6.64 |             nan    |
| REGIME sector & sub-industry up over 5 days: skip ['both'] / +20% -10%                                             |   0.21 |    -0.40 |             -0.37 |  1140.00 |   0.41 |            8.88 |               0.58 |
| REGIME sector & sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%                                |   0.07 |    -0.32 |             -0.28 |   667.00 |   0.40 |            6.82 |               1.12 |
| REGIME sector & sub-industry above 21 EMA: skip ['both', 'one of the two'] / +20% -10%                             |   0.23 |    -0.40 |             -0.36 |  1135.00 |   0.41 |            8.55 |               0.65 |
| REGIME sector & sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%                                  |   0.04 |    -0.31 |             -0.28 |   629.00 |   0.39 |            6.46 |               1.75 |
| REGIME distance above the 21 EMA: skip ['0-5%', '5-10%', '> 15%'] / +20% -10%                                      |   0.12 |    -0.51 |             -0.48 |  1151.00 |   0.39 |            8.90 |               0.93 |
| REGIME distance above the 21 EMA, S&P 500 point-in-time only / +20% -10%                                           |   0.14 |    -0.28 |             -0.24 |   680.00 |   0.43 |            6.96 |               0.58 |
| REGIME ADR%: skip ['< 3%'] / +20% -10%                                                                             |   0.23 |    -0.40 |             -0.39 |  1227.00 |   0.41 |            9.04 |               0.61 |
| REGIME ADR%, S&P 500 point-in-time only / +20% -10%                                                                |   0.15 |    -0.33 |             -0.32 |   740.00 |   0.43 |            7.14 |               0.64 |
| REGIME ADR% (only stocks trading >= $10M/day): skip ['< 3%'] / +20% -10%                                           |   0.21 |    -0.42 |             -0.41 |  1220.00 |   0.41 |            9.04 |               0.60 |
| REGIME ADR% (only stocks trading >= $10M/day), S&P 500 point-in-time only / +20% -10%                              |   0.15 |    -0.32 |             -0.31 |   740.00 |   0.43 |            7.14 |               0.64 |
| REGIME fundamental inflection (all 4): skip ['no', 'yes'] / +20% -10%                                              |   0.16 |    -0.25 |             -0.22 |   741.00 |   0.43 |            6.94 |               0.49 |
| REGIME fundamental inflection (all 4), S&P 500 point-in-time only / +20% -10%                                      |   0.04 |    -0.12 |             -0.08 |   101.00 |   0.50 |            1.32 |               0.55 |
| REGIME revenue growth accelerating: skip ['1 quarter', 'no (decelerating)'] / +20% -10%                            |   0.20 |    -0.40 |             -0.36 |  1080.00 |   0.42 |            8.50 |               0.67 |
| REGIME revenue growth accelerating, S&P 500 point-in-time only / +20% -10%                                         |   0.10 |    -0.27 |             -0.25 |   487.00 |   0.43 |            5.60 |               0.42 |
| REGIME operating income outgrowing revenue: skip ['no', 'yes'] / +20% -10%                                         |   0.17 |    -0.41 |             -0.38 |   901.00 |   0.42 |            8.26 |               0.68 |
| REGIME operating income outgrowing revenue, S&P 500 point-in-time only / +20% -10%                                 |   0.14 |    -0.21 |             -0.20 |   341.00 |   0.51 |            4.34 |               0.57 |
| REGIME operating margin vs a year ago: skip ['expanding', 'shrinking'] / +20% -10%                                 |   0.16 |    -0.41 |             -0.38 |   917.00 |   0.42 |            8.28 |               0.70 |
| REGIME operating margin vs a year ago, S&P 500 point-in-time only / +20% -10%                                      |   0.14 |    -0.21 |             -0.20 |   341.00 |   0.51 |            4.34 |               0.57 |
| REGIME FCF margin vs a year ago: skip ['improving', 'worse'] / +20% -10%                                           |   0.15 |    -0.31 |             -0.28 |   817.00 |   0.42 |            7.32 |               0.51 |
| REGIME FCF margin vs a year ago, S&P 500 point-in-time only / +20% -10%                                            |   0.05 |    -0.13 |             -0.10 |   130.00 |   0.50 |            1.79 |               0.46 |
| REGIME up/down volume, 50 days: skip ['1.0-1.3', '> 1.3 (accumulation)'] / +20% -10%                               |   0.16 |    -0.41 |             -0.37 |  1126.00 |   0.40 |            8.90 |               0.79 |
| REGIME up/down volume, 50 days, S&P 500 point-in-time only / +20% -10%                                             |   0.13 |    -0.29 |             -0.27 |   632.00 |   0.43 |            6.76 |               0.61 |
| REGIME price vs 200-day: skip ['0-10% above', '10-30% above', '30-50% above', '> 50% above'] / +20% -10%           |   0.24 |    -0.39 |             -0.35 |  1106.00 |   0.41 |            8.77 |               0.69 |
| REGIME price vs 200-day, S&P 500 point-in-time only / +20% -10%                                                    |   0.16 |    -0.28 |             -0.25 |   607.00 |   0.45 |            6.42 |               0.58 |
| REGIME 6-month gain: skip ['0-20%', '20-50%', '50-100%', '> 100%'] / +20% -10%                                     |   0.26 |    -0.36 |             -0.36 |  1086.00 |   0.42 |            8.76 |               0.62 |
| REGIME 6-month gain, S&P 500 point-in-time only / +20% -10%                                                        |   0.13 |    -0.31 |             -0.27 |   612.00 |   0.43 |            6.36 |               0.71 |
| REGIME sector (11 GICS, by median RS): skip ['bottom 3', 'top 3 (leading)'] / +20% -10%                            |   0.24 |    -0.52 |             -0.48 |  1139.00 |   0.42 |            8.87 |               0.64 |
| REGIME sector (11 GICS, by median RS), S&P 500 point-in-time only / +20% -10%                                      |   0.07 |    -0.44 |             -0.41 |   656.00 |   0.40 |            7.03 |               1.08 |
| REGIME sub-industry (by median RS): skip ['middle', 'top 30% (leading)'] / +20% -10%                               |   0.21 |    -0.50 |             -0.49 |  1119.00 |   0.41 |            8.74 |               0.67 |
| REGIME sub-industry (by median RS), S&P 500 point-in-time only / +20% -10%                                         |   0.09 |    -0.31 |             -0.28 |   638.00 |   0.41 |            6.46 |               0.74 |
| REGIME 3-day market model: skip ['rest'] / +20% -10%                                                               |   0.07 |    -0.07 |             -0.05 |    69.00 |   0.64 |            0.68 |               0.47 |
| REGIME 3-day market model, S&P 500 point-in-time only / +20% -10%                                                  |   0.01 |    -0.05 |             -0.05 |    25.00 |   0.52 |            0.29 |               0.87 |
| RULE top 3 sectors only, model top 10% / +20% -10%                                                                 |   0.21 |    -0.30 |             -0.27 |   890.00 |   0.43 |            7.70 |               0.44 |
| RULE top 3 sectors only, S&P 500 point-in-time only / +20% -10%                                                    |   0.06 |    -0.27 |             -0.23 |   352.00 |   0.43 |            4.04 |               0.64 |
| RULE top 30% sub-industries only, model top 10% / +20% -10%                                                        |   0.25 |    -0.25 |             -0.25 |   915.00 |   0.44 |            8.37 |               0.41 |
| RULE top 30% sub-industries only, S&P 500 point-in-time only / +20% -10%                                           |   0.13 |    -0.23 |             -0.19 |   414.00 |   0.47 |            5.01 |               0.47 |
| RULE top 3 sectors AND top 30% sub-industries, model top 10% / +20% -10%                                           |   0.19 |    -0.27 |             -0.25 |   777.00 |   0.44 |            7.02 |               0.45 |
| RULE top 3 sectors AND top 30% sub-industries, S&P 500 point-in-time only / +20% -10%                              |   0.03 |    -0.17 |             -0.14 |   244.00 |   0.41 |            2.90 |               0.56 |
| RULE SPY above its 21 & 50 SMA, model top 10% / +20% -10%                                                          |   0.24 |    -0.34 |             -0.27 |   872.00 |   0.43 |            7.14 |               0.63 |
| RULE SPY above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                                             |   0.17 |    -0.23 |             -0.22 |   494.00 |   0.46 |            4.87 |               0.59 |
| RULE QQQ above its 21 & 50 SMA, model top 10% / +20% -10%                                                          |   0.19 |    -0.30 |             -0.26 |   850.00 |   0.42 |            6.83 |               0.77 |
| RULE QQQ above its 21 & 50 SMA, S&P 500 point-in-time only / +20% -10%                                             |   0.17 |    -0.22 |             -0.21 |   488.00 |   0.46 |            4.94 |               0.51 |
| RULE SPY above its 50 SMA (21 either way), model top 10% / +20% -10%                                               |   0.22 |    -0.40 |             -0.38 |   939.00 |   0.43 |            7.49 |               0.64 |
| RULE SPY above its 50 SMA (21 either way), S&P 500 point-in-time only / +20% -10%                                  |   0.14 |    -0.31 |             -0.28 |   546.00 |   0.44 |            5.59 |               0.66 |
| RULE A/D line above its 21 & 50 MA, model top 10% / +20% -10%                                                      |   0.17 |    -0.40 |             -0.38 |   862.00 |   0.41 |            7.17 |               0.84 |
| RULE A/D line above its 21 & 50 MA, S&P 500 point-in-time only / +20% -10%                                         |   0.13 |    -0.24 |             -0.18 |   502.00 |   0.45 |            5.20 |               0.57 |
| RULE > 50% of stocks above their 50d, model top 10% / +20% -10%                                                    |   0.13 |    -0.38 |             -0.36 |   862.00 |   0.41 |            7.02 |               0.60 |
| RULE > 50% of stocks above their 50d, S&P 500 point-in-time only / +20% -10%                                       |   0.11 |    -0.29 |             -0.27 |   506.00 |   0.43 |            5.32 |               0.65 |
| RULE % above 50d rising over 10 days, model top 10% / +20% -10%                                                    |   0.20 |    -0.43 |             -0.41 |   942.00 |   0.41 |            6.94 |               0.74 |
| RULE % above 50d rising over 10 days, S&P 500 point-in-time only / +20% -10%                                       |   0.12 |    -0.26 |             -0.23 |   491.00 |   0.45 |            4.91 |               0.80 |
| RULE sector AND sub-industry green today, model top 10% / +20% -10%                                                |   0.17 |    -0.37 |             -0.36 |  1004.00 |   0.41 |            8.40 |               1.02 |
| RULE sector AND sub-industry green today, S&P 500 point-in-time only / +20% -10%                                   |   0.13 |    -0.23 |             -0.20 |   483.00 |   0.46 |            5.52 |               0.65 |
| RULE sector AND sub-industry up over 5 days, model top 10% / +20% -10%                                             |   0.11 |    -0.43 |             -0.40 |   992.00 |   0.39 |            8.19 |               0.95 |
| RULE sector AND sub-industry up over 5 days, S&P 500 point-in-time only / +20% -10%                                |   0.11 |    -0.33 |             -0.31 |   516.00 |   0.44 |            5.61 |               0.70 |
| RULE sector AND sub-industry above 21 EMA, model top 10% / +20% -10%                                               |   0.14 |    -0.36 |             -0.32 |   954.00 |   0.40 |            7.96 |               0.86 |
| RULE sector AND sub-industry above 21 EMA, S&P 500 point-in-time only / +20% -10%                                  |   0.16 |    -0.23 |             -0.21 |   448.00 |   0.48 |            4.85 |               0.62 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, model top 10% / +20% -10%                                    |   0.14 |    -0.30 |             -0.27 |   784.00 |   0.41 |            6.54 |               0.70 |
| RULE SPY > 21 & 50 + sector & sub-industry up 5 days, S&P 500 point-in-time only / +20% -10%                       |   0.10 |    -0.14 |             -0.12 |   325.00 |   0.45 |            3.42 |               0.71 |
| RULE <= 10% above the 21 EMA (course rule), model top 10% / +20% -10%                                              |   0.21 |    -0.45 |             -0.43 |  1191.00 |   0.40 |            9.06 |               0.68 |
| RULE <= 10% above the 21 EMA (course rule), S&P 500 point-in-time only / +20% -10%                                 |   0.12 |    -0.32 |             -0.30 |   714.00 |   0.42 |            7.36 |               0.78 |
| RULE ADR% >= 5% (the infographic's minimum), model top 10% / +20% -10%                                             |   0.22 |    -0.55 |             -0.53 |  1455.00 |   0.39 |            8.37 |               0.69 |
| RULE ADR% >= 5% (the infographic's minimum), S&P 500 point-in-time only / +20% -10%                                |   0.12 |    -0.25 |             -0.23 |   444.00 |   0.43 |            2.85 |               0.73 |
| RULE ADR% 5-12% (the infographic's sweet spot), model top 10% / +20% -10%                                          |   0.22 |    -0.52 |             -0.51 |  1421.00 |   0.39 |            8.37 |               0.66 |
| RULE ADR% 5-12% (the infographic's sweet spot), S&P 500 point-in-time only / +20% -10%                             |   0.11 |    -0.26 |             -0.23 |   441.00 |   0.43 |            2.84 |               0.74 |
| RULE ADR% <= 15% (skip the wildest), model top 10% / +20% -10%                                                     |   0.27 |    -0.45 |             -0.43 |  1183.00 |   0.42 |            9.07 |               0.58 |
| RULE ADR% <= 15% (skip the wildest), S&P 500 point-in-time only / +20% -10%                                        |   0.11 |    -0.33 |             -0.30 |   737.00 |   0.41 |            7.40 |               0.84 |
| RULE ADR% 5-12% and >= $10M/day, model top 10% / +20% -10%                                                         |   0.17 |    -0.56 |             -0.54 |  1381.00 |   0.39 |            8.23 |               0.85 |
| RULE ADR% 5-12% and >= $10M/day, S&P 500 point-in-time only / +20% -10%                                            |   0.11 |    -0.26 |             -0.23 |   441.00 |   0.43 |            2.84 |               0.74 |
| RULE fundamental inflection (rev accel 2q + op leverage + margin + FCF up), model top 10% / +20% -10%              |   0.19 |    -0.25 |             -0.20 |   570.00 |   0.46 |            5.91 |               0.49 |
| RULE fundamental inflection (rev accel 2q + op leverage + margin + FCF up), S&P 500 point-in-time only / +20% -10% |   0.02 |    -0.19 |             -0.17 |   172.00 |   0.41 |            1.96 |               1.13 |
| RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10%                                            |   0.34 |    -0.35 |             -0.34 |   984.00 |   0.45 |            8.11 |               0.40 |
| RULE revenue growth accelerating 2+ quarters, S&P 500 point-in-time only / +20% -10%                               |   0.10 |    -0.26 |             -0.24 |   473.00 |   0.43 |            5.48 |               0.41 |
| RULE accumulation (up/down volume 50d > 1), model top 10% / +20% -10%                                              |   0.14 |    -0.43 |             -0.43 |  1057.00 |   0.40 |            8.68 |               0.72 |
| RULE accumulation (up/down volume 50d > 1), S&P 500 point-in-time only / +20% -10%                                 |   0.04 |    -0.33 |             -0.31 |   607.00 |   0.38 |            6.40 |               1.37 |
| RULE not extended (< 30% above the 200-day), model top 10% / +20% -10%                                             |   0.23 |    -0.42 |             -0.41 |  1164.00 |   0.41 |            9.03 |               0.59 |
| RULE not extended (< 30% above the 200-day), S&P 500 point-in-time only / +20% -10%                                |   0.15 |    -0.31 |             -0.30 |   687.00 |   0.43 |            7.28 |               0.71 |
| RULE not already up 50%+ in 6 months, model top 10% / +20% -10%                                                    |   0.28 |    -0.45 |             -0.42 |  1186.00 |   0.42 |            9.05 |               0.59 |
| RULE not already up 50%+ in 6 months, S&P 500 point-in-time only / +20% -10%                                       |   0.16 |    -0.31 |             -0.30 |   686.00 |   0.44 |            7.26 |               0.70 |
| RULE price rules only (accumulation + not extended + not up 50%), model top 10% / +20% -10%                        |   0.21 |    -0.45 |             -0.44 |   969.00 |   0.42 |            8.41 |               0.60 |
| RULE price rules only (accumulation + not extended + not up 50%), S&P 500 point-in-time only / +20% -10%           |   0.05 |    -0.38 |             -0.36 |   521.00 |   0.39 |            5.90 |               1.13 |
| RULE user's full method (inflection + price rules), model top 10% / +20% -10%                                      |   0.05 |    -0.14 |             -0.14 |   242.00 |   0.44 |            3.01 |               0.58 |
| RULE user's full method (inflection + price rules), S&P 500 point-in-time only / +20% -10%                         |  -0.01 |    -0.16 |             -0.14 |    64.00 |   0.39 |            0.91 |             nan    |
| METHOD user's method alone, no model (inflection + price rules) / +20% -10%                                        |   0.10 |    -0.26 |             -0.22 |   579.00 |   0.46 |            9.10 |               0.65 |
| METHOD fundamental inflection alone, no model / +20% -10%                                                          |   0.11 |    -0.38 |             -0.33 |   723.00 |   0.44 |            9.45 |               0.58 |
| MODEL with fundamentals, top 10% / +20% -10%                                                                       |   0.29 |    -0.44 |             -0.43 |  1194.00 |   0.42 |            9.25 |               0.48 |
| SIZE model top 10%, position scaled by 6% / ADR / +20% -10%                                                        |   0.21 |    -0.35 |             -0.32 |  1159.00 |   0.41 |            8.74 |               0.51 |
| QULL scan+setups / qull_sma10                                                                                      |  -0.15 |    -0.80 |             -0.79 |  1151.00 |   0.38 |            3.39 |             nan    |
| QULL scan+setups / qull_sma20                                                                                      |  -0.12 |    -0.74 |             -0.72 |  1006.00 |   0.39 |            4.07 |             nan    |
| QULL scan+setups / sma50_close                                                                                     |   0.06 |    -0.49 |             -0.38 |   679.00 |   0.19 |            5.57 |               1.57 |
| QULL scan+setups / bracket_20_10                                                                                   |   0.06 |    -0.40 |             -0.41 |   722.00 |   0.39 |            5.71 |               1.50 |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma10                                                         |  -0.07 |    -0.54 |             -0.52 |   758.00 |   0.39 |            2.30 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma10                                                                   |  -0.06 |    -0.49 |             -0.47 |   851.00 |   0.39 |            2.58 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / qull_sma20                                                         |  -0.03 |    -0.45 |             -0.43 |   690.00 |   0.40 |            2.92 |             nan    |
| QULL ... + regime + adaptive sizing / qull_sma20                                                                   |  -0.03 |    -0.41 |             -0.36 |   766.00 |   0.39 |            3.15 |             nan    |
| QULL scan+setups, only when QQQ > 10 & 20 SMA / sma50_close                                                        |   0.18 |    -0.45 |             -0.32 |   479.00 |   0.22 |            4.23 |               0.68 |
| QULL ... + regime + adaptive sizing / sma50_close                                                                  |   0.14 |    -0.36 |             -0.30 |   502.00 |   0.22 |            4.52 |               0.73 |
| QULL scan+setups + regime, S&P 500 point-in-time only / qull_sma20                                                 |  -0.01 |    -0.26 |             -0.25 |    92.00 |   0.34 |            0.32 |             nan    |
| SURVIVORSHIP S&P 500 names, all dates, top 10% model (14891 signals) / sma50_close                                 |   0.24 |    -0.48 |             -0.36 |  1311.00 |   0.32 |            8.31 |               0.54 |
| SURVIVORSHIP S&P 500 names, only after joining the index (3853 signals) / sma50_close                              |   0.16 |    -0.39 |             -0.32 |   897.00 |   0.34 |            6.07 |               0.60 |
| WORKFLOW rockets as written (regime sizing) / wf_rocket                                                            |   0.02 |    -0.11 |             -0.08 |   190.00 |   0.31 |            2.34 |               0.61 |
| WORKFLOW rockets, no regime rule / wf_rocket                                                                       |   0.01 |    -0.11 |             -0.07 |   236.00 |   0.31 |            2.72 |               0.98 |
| WORKFLOW rockets, QQQ 21/50 regime / wf_rocket                                                                     |   0.01 |    -0.09 |             -0.08 |   192.00 |   0.31 |            2.43 |               1.40 |
| WORKFLOW rockets / sma50_close                                                                                     |   0.03 |    -0.10 |             -0.08 |   189.00 |   0.30 |            2.34 |               0.64 |
| WORKFLOW rockets / bracket_20_10                                                                                   |   0.03 |    -0.08 |             -0.07 |   174.00 |   0.45 |            2.40 |               0.70 |
| WORKFLOW BASELINE random entries, rocket filter + regime / wf_rocket                                               |  -0.01 |    -0.24 |             -0.21 |   496.00 |   0.16 |            2.47 |             nan    |
| WORKFLOW rockets as written, S&P 500 point-in-time only / wf_rocket                                                |   0.01 |    -0.07 |             -0.04 |   142.00 |   0.35 |            2.03 |               0.67 |
| WORKFLOW scanner as written, S&P 500 point-in-time (NDX proxy) / wf_weekly10                                       |   0.01 |    -0.17 |             -0.13 |   349.00 |   0.29 |            3.40 |               1.55 |
| WORKFLOW scanner PIT, no regime rule / wf_weekly10                                                                 |   0.00 |    -0.17 |             -0.14 |   421.00 |   0.31 |            3.93 |               7.87 |
| WORKFLOW scanner PIT, QQQ 21/50 regime / wf_weekly10                                                               |  -0.02 |    -0.25 |             -0.23 |   375.00 |   0.27 |            3.47 |             nan    |
| WORKFLOW scanner PIT / sma50_close                                                                                 |   0.01 |    -0.20 |             -0.19 |   396.00 |   0.27 |            3.36 |               2.41 |
| WORKFLOW BASELINE random entries, scanner filter + regime, PIT / wf_weekly10                                       |   0.04 |    -0.17 |             -0.12 |   525.00 |   0.15 |            3.28 |               0.69 |
| WORKFLOW scanner as written, full universe / wf_weekly10                                                           |   0.01 |    -0.21 |             -0.19 |   368.00 |   0.26 |            3.39 |               5.53 |
| Top 10 by IS expectancy, 1% risk, 10 slots, idle cash in SPY                                                       |   0.15 |    -0.40 |             -0.34 |   441.00 |   0.29 |            5.61 |               0.48 |
| Top 10 by IS expectancy, 2% risk, 10 slots, idle cash in SPY                                                       |   0.14 |    -0.46 |             -0.39 |   354.00 |   0.27 |            4.18 |               0.57 |
| Top 10 by IS expectancy, 2% risk, 15 slots, idle cash in SPY                                                       |   0.14 |    -0.46 |             -0.39 |   354.00 |   0.27 |            4.18 |               0.57 |
| SPY buy & hold                                                                                                     |   0.15 |    -0.34 |            nan    |   nan    | nan    |          nan    |             nan    |

max_DD is from equity marked to market every day (open positions at the close); max_DD_realized only counts closed trades. Partial exits (trim plans) are approximated as held in full until the final exit.

Strategies in the 'Top 10 by IS expectancy' portfolio (chosen on pre-2018 data only):

| entry             | filter     | exit            |   IS_n |   IS_avgR |   OOS_n |   OOS_avgR |   OOS_t |
|:------------------|:-----------|:----------------|-------:|----------:|--------:|-----------:|--------:|
| ep_gap8_neglected | wf_scan    | sma50_close     |    200 |      0.72 |     245 |       0.35 |    2.07 |
| ep_gap8_neglected | wf_scan    | wf_rocket       |    200 |      0.69 |     245 |       0.36 |    2.34 |
| ep_gap10_vol2     | rs80_mkt   | sma50_close     |    215 |      0.61 |     411 |       0.60 |    2.45 |
| ep_gap5           | rs80_early | wf_weekly10     |    333 |      0.59 |     472 |       0.44 |    2.46 |
| ep_gap8_neglected | wf_scan    | oneil_20_8      |    201 |      0.57 |     245 |       0.34 |    2.56 |
| ep_gap5           | rs80_early | sma50_close     |    333 |      0.57 |     472 |       0.40 |    2.41 |
| ep_gap10          | rs80_mkt   | chandelier_3atr |    200 |      0.56 |     354 |       0.14 |    1.10 |
| ep_gap8_neglected | rs80       | wf_weekly10     |    241 |      0.55 |     333 |       0.51 |    2.29 |
| ep_gap8_hold      | rs80_mkt   | wf_weekly10     |    298 |      0.54 |     433 |       0.44 |    1.90 |
| ep_gap10_vol2     | rs80_mkt   | chandelier_3atr |    217 |      0.52 |     411 |       0.21 |    1.69 |

Year-by-year returns (best 3 portfolios by CAGR vs SPY):

|      |   RULE revenue growth accelerating 2+ quarters, model top 10% / +20% -10% |   GOAL b20: model's top 10% stocks, no setup needed / bracket_20_10 |   MODEL with fundamentals, top 10% / +20% -10% |   SPY |
|-----:|--------------------------------------------------------------------------:|--------------------------------------------------------------------:|-----------------------------------------------:|------:|
| 2018 |                                                                       8.1 |                                                                -2.1 |                                           19.1 |  -5.2 |
| 2019 |                                                                      51.9 |                                                                53.7 |                                           37.5 |  31.2 |
| 2020 |                                                                      83.5 |                                                                81.2 |                                           81.6 |  18.3 |
| 2021 |                                                                      49.2 |                                                                25.0 |                                           13.8 |  28.7 |
| 2022 |                                                                       2.4 |                                                               -26.4 |                                          -18.0 | -18.2 |
| 2023 |                                                                      34.7 |                                                                66.6 |                                           31.6 |  26.2 |
| 2024 |                                                                       4.9 |                                                                26.0 |                                           58.1 |  24.9 |
| 2025 |                                                                      33.6 |                                                                44.0 |                                           38.3 |  17.7 |
| 2026 |                                                                      48.9 |                                                                23.6 |                                           14.3 |  15.1 |

## Appendix: entries and exits

| entry              | source / rule                                                             |   signals |
|:-------------------|:--------------------------------------------------------------------------|----------:|
| donchian_20        | Turtle 20-day breakout / trading-range break (Brock et al. 1992)          |    150933 |
| donchian_55        | Turtle 55-day breakout                                                    |    100559 |
| high52             | 52-week-high breakout (George & Hwang 2004)                               |     60578 |
| high52_fresh       | 52-week high after >= 20 days of consolidation                            |     16912 |
| base_25            | O'Neil/Darvas 5-week base breakout                                        |      4463 |
| base_50            | O'Neil 10-week base breakout                                              |      5068 |
| vcp                | Minervini volatility contraction pattern                                  |      2251 |
| flag_30            | Qullamaggie flag after a 30%+ move                                        |      3040 |
| flag_60            | Qullamaggie flag after a 60%+ move                                        |       988 |
| flag_30_early      | Qullamaggie flag, early entry inside the flag                             |      3250 |
| htf                | High tight flag (O'Neil / Bulkowski)                                      |       155 |
| ep_gap5            | Gap up >= 5% on 3x volume                                                 |      4328 |
| ep_gap10           | Episodic pivot: gap >= 10% on 3x volume                                   |      1526 |
| ep_gap8_neglected  | Episodic pivot from neglect (Qullamaggie)                                 |      1597 |
| ep_gap15           | Episodic pivot: gap >= 15% on 3x volume                                   |       565 |
| ep_gap10_vol2      | EP variant: gap >= 10% on only 2x volume                                  |      1867 |
| ep_gap10_vol5      | EP variant: gap >= 10% on 5x volume                                       |       804 |
| ep_gap8_hold       | EP variant: gap >= 8%, closes above the open                              |      1995 |
| pocket_pivot       | Morales & Kacher pocket pivot                                             |     99091 |
| asc_triangle       | Ascending triangle breakout (flat top, rising lows)                       |      2020 |
| desc_triangle      | Descending triangle, upside breakout                                      |      1507 |
| sym_triangle       | Symmetrical triangle breakout (pennant)                                   |      1823 |
| falling_wedge      | Falling wedge breakout                                                    |      2822 |
| rising_wedge       | Rising wedge, upside breakout                                             |      3925 |
| tight_coil_7       | 7-day coil: closes within 1 ADR, breakout on volume                       |     12021 |
| tight_coil_15      | 15-day coil: closes within 1.5 ADR, breakout on volume                    |      2367 |
| stage2             | Weinstein stage 2 breakout                                                |     11106 |
| ema_retest         | 8/21 EMA cross -> break -> retest (your playbook)                         |     30805 |
| multi_touch        | Multi-touch level breakout on volume (your playbook)                      |     23738 |
| undercut           | Undercut & rally (your playbook)                                          |     50305 |
| qull_breakout      | Qullamaggie breakout: buy-stop above the flag high next day               |      7163 |
| qull_breakout_60   | Qullamaggie breakout after a 60%+ move                                    |      2876 |
| wf_rocket_breakout | Workflow PDF rockets: 6-week base -> 52w high on 1.5x vol, stop -8%       |      5007 |
| wf_rocket_gap      | Workflow PDF rockets: gap >= 5% (2x vol) holding its low 2 days           |      7000 |
| wf_scan_pullback   | Workflow PDF scanner: uptrend pullback to 21EMA/50SMA, close > prior high |    143470 |
| wf_scan_base       | Workflow PDF scanner: uptrend, breakout from a 4-week base                |     57839 |
| tc_ema_cross_base  | Course: 21/50 EMA crossover, then the first base breakout                 |     14592 |
| tc_supertrend_ema  | Course: Supertrend flip + close above 21 EMA, same candle                 |     42520 |
| tc_reversal_base   | Course: reversal, 35%+ off the high, EMAs turned up, base breakout        |       332 |
| tc_ema200_2nd      | Course: second pullback to the 200 EMA after reclaiming it                |      2804 |
| random_uptrend     | BASELINE: random entries in an uptrend                                    |     66511 |

| exit            | rule                                                                                         |
|:----------------|:---------------------------------------------------------------------------------------------|
| trim_ema        | 1/4 at +2R then BE stop; 1/4 on close<8EMA, 1/4 <21EMA, rest <50EMA                          |
| qull_sma10      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<10SMA               |
| qull_sma20      | Qullamaggie: sell 1/3 on day 5 if green, stop to BE, trail rest on close<20SMA               |
| oneil_20_8      | O'Neil: stop max 8% below entry, take all at +20%, time stop 60 days                         |
| fixed_3r_20d    | stop, target 3R, time stop 20 days                                                           |
| chandelier_3atr | trailing stop = highest close - 3 x ATR(20)                                                  |
| donchian_10low  | Turtle-style: exit on close below the prior 10-day low                                       |
| ema21_close     | exit on first close below the 21 EMA                                                         |
| sma50_close     | position trade: exit on first close below the 50 SMA                                         |
| bracket_10_10   | stop -10%, target +10%, close after 63 days if neither                                       |
| bracket_20_10   | stop -10%, target +20%, close after 63 days if neither                                       |
| wf_rocket       | workflow rockets: sell 1/3 at +25% and move the stop to entry, trail the rest on close<50SMA |
| wf_weekly10     | workflow scanner: exit on a weekly close below the 10-week MA (setup stop stays)             |

Caveats: index membership lists are current (plus former S&P 500 members Yahoo still serves), so survivorship bias remains; daily bars cannot reproduce intraday entries; one decision per signal, no slippage model beyond costs.