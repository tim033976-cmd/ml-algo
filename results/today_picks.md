# Daily picks — 2026-10-20

Goal: **+20% (or +10%) before a -10% loss**, daily chart, buy near the close, exit after 63 trading days at the latest.
Model trained on 541,809 past snapshots of 1541 stocks. Probabilities are in %.

**Probabilities are calibrated out-of-sample** (model trained before 2023, checked on 2023-today). On those held-out years: all stocks hit +20% before -10% 25% of the time; the model's top 10% 35% (avg +1.3% net per trade; break-even ~33%). +10% before -10%: 50% vs 49% (break-even ~50%).

Columns: p_b20 / p_b10 = chance (%) of +20% / +10% before -10%. `setups_last_3_days` = setups that fired recently (e.g. ep_gap10 = episodic pivot, falling_wedge, desc_triangle). Not financial advice; paper trade first.

## Leaders (your style): RS in the top 30%, within 25% of the 52-week high, above the 50-day

_No leaders today._

## All stocks (the model's overall favourites; often beaten-down, volatile names)

| ticker   | close   | p_b20   | p_b10   | stop_-10%   | target_+10%   | target_+20%   | adr_pct   | rs_rank   | dist_52w_high   | base_count   | setups_last_3_days   | sector   |
|----------|---------|---------|---------|-------------|---------------|---------------|-----------|-----------|-----------------|--------------|----------------------|----------|