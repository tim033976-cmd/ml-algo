"""Point-in-time fundamentals from SEC EDGAR XBRL filings (run 22).

The SEC publishes every company's reported numbers with the date each filing was made
(companyfacts.zip, free). For each quarter we keep the FIRST reported value (later restatements
would be lookahead) and only use it from the day after it was filed. Quarters reported only as
year-to-date figures (cash flow, fiscal Q4) are derived by differencing consecutive YTD values.

Metrics follow the user's "early fundamental inflection" method: revenue growth accelerating,
operating income growing faster than revenue (operating leverage), operating margin expanding,
free cash flow improving.
"""
from __future__ import annotations

import io
import json
import os
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

BULK_URL = "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
# SEC asks automated clients to identify themselves; override with the SEC_USER_AGENT env var
USER_AGENT = os.environ.get("SEC_USER_AGENT", "ml-algo-research research-bot@users.noreply.github.com")

CONCEPTS = {  # metric -> us-gaap tags, in order of preference (companies switch tags over time)
    "rev": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
            "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet", "RevenuesNetOfInterestExpense"],
    "opinc": ["OperatingIncomeLoss"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
FUND_FEATURES = ["rev_yoy", "rev_yoy_d1", "rev_accel_q", "op_margin", "op_margin_chg", "op_lev",
                 "op_turn_pos", "fcf_margin", "fcf_margin_chg", "inflection", "fund_age"]


def _get(url: str, dest: Path | None = None, tries: int = 4) -> bytes | None:
    import requests
    for i in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"},
                             timeout=600, stream=dest is not None)
            r.raise_for_status()
            if dest is None:
                return r.content
            with open(dest, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
            return b""
        except Exception as e:  # network errors, 403/429: back off and retry
            print(f"[fund] {url}: {e} (try {i + 1}/{tries})")
            time.sleep(5 * 2 ** i)
    return None


def _facts(company: dict, tags: list[str]) -> pd.DataFrame:
    """Duration facts in USD for the tags, one row per (start, end) using the most preferred tag that
    reports it and the earliest filing of that value."""
    gaap = company.get("facts", {}).get("us-gaap", {})
    rows = []
    for rank, tag in enumerate(tags):
        for f in gaap.get(tag, {}).get("units", {}).get("USD", []):
            if "start" in f and f.get("val") is not None and str(f.get("form", "")).startswith(("10-Q", "10-K")):
                rows.append((f["start"], f["end"], float(f["val"]), f["filed"], rank))
    if not rows:
        return pd.DataFrame(columns=["start", "end", "val", "filed"])
    d = pd.DataFrame(rows, columns=["start", "end", "val", "filed", "rank"])
    for c in ("start", "end", "filed"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna(subset=["start", "end", "filed"])
    # one value per period: its first filing under any of the tags (restatements come later; ties go
    # to the more preferred tag)
    d = d.sort_values(["start", "end", "filed", "rank"]).drop_duplicates(["start", "end"], keep="first")
    return d.drop(columns="rank").reset_index(drop=True)


def quarterly(facts: pd.DataFrame) -> pd.DataFrame:
    """Standalone 3-month values indexed by quarter end, with the date they became known.
    Direct 3-month facts first; otherwise YTD(k) - YTD(k-1) for YTD facts sharing a start date."""
    if facts.empty:
        return pd.DataFrame(columns=["val", "filed"])
    f = facts.assign(dur=(facts["end"] - facts["start"]).dt.days)
    q = f[f["dur"].between(80, 100)][["end", "val", "filed"]]
    out = {r.end: (r.val, r.filed) for r in q.itertuples()}
    for _, g in f[f["dur"].between(80, 380)].groupby("start"):
        g = g.sort_values("end")
        prev = None
        for r in g.itertuples():
            if prev is not None and 80 <= (r.end - prev.end).days <= 100 and r.end not in out:
                out[r.end] = (r.val - prev.val, max(r.filed, prev.filed))
            if r.dur >= 80:
                prev = r
    # fiscal Q4 when the 10-Qs report standalone quarters only: full year - (Q1 + Q2 + Q3)
    for r in f[f["dur"].between(350, 380)].itertuples():
        if r.end in out:
            continue
        prior = [e for e in out if r.start <= e < r.end and (r.end - e).days >= 60]
        if len(prior) == 3 and min(prior) - r.start <= pd.Timedelta(days=100):
            out[r.end] = (r.val - sum(out[e][0] for e in prior), max([r.filed] + [out[e][1] for e in prior]))
    if not out:
        return pd.DataFrame(columns=["val", "filed"])
    res = pd.DataFrame.from_dict(out, orient="index", columns=["val", "filed"]).sort_index()
    res.index.name = "end"
    return res


def _lag(s: pd.Series, ends: pd.Index, days: int, tol: int = 25) -> pd.Series:
    """Value of `s` at the quarter end ~`days` earlier than each end (NaN when that quarter is missing)."""
    src = pd.Series(s.to_numpy(), index=ends)
    want = ends - pd.Timedelta(days=days)
    pos = src.index.get_indexer(want, method="nearest", tolerance=pd.Timedelta(days=tol))
    vals = np.where(pos >= 0, src.to_numpy()[np.clip(pos, 0, None)], np.nan)
    return pd.Series(vals, index=ends)


def _ttm(s: pd.Series, ends: pd.Index) -> pd.Series:
    """Sum of the last 4 quarters, only when all 4 exist and are ~3 months apart."""
    parts = [_lag(s, ends, 91 * k) for k in range(4)]
    return sum(parts)


def metrics(q: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per quarter end: the inflection metrics, and `avail` = the first day all of them were known."""
    if q.get("rev") is None or q["rev"].empty:
        return pd.DataFrame()
    ends = q["rev"].index
    get = lambda k: q[k]["val"].reindex(ends) if k in q and not q[k].empty else pd.Series(np.nan, index=ends)
    rev, op, ocf, cap = get("rev"), get("opinc"), get("ocf"), get("capex")
    m = pd.DataFrame(index=ends)
    prev_rev = _lag(rev, ends, 364)
    m["rev_yoy"] = np.where(prev_rev > 0, rev / prev_rev - 1, np.nan)
    yoy = pd.Series(m["rev_yoy"].to_numpy(), index=ends)
    m["rev_yoy_d1"] = yoy - _lag(yoy, ends, 91)
    # consecutive quarters of accelerating YoY growth (-5% -> -1% -> 3% -> 8% = 3)
    acc = np.zeros(len(ends))
    d1 = m["rev_yoy_d1"].to_numpy()
    for i in range(len(ends)):
        acc[i] = (acc[i - 1] + 1 if i > 0 and (ends[i] - ends[i - 1]).days <= 100 else 1) if d1[i] > 0 else 0
    m["rev_accel_q"] = np.where(np.isnan(d1), np.nan, np.minimum(acc, 4))
    t_rev, t_op = _ttm(rev, ends), _ttm(op, ends)
    t_fcf = _ttm(ocf, ends) - _ttm(cap.fillna(0), ends)
    m["op_margin"] = np.where(t_rev > 0, t_op / t_rev, np.nan)
    om = pd.Series(m["op_margin"].to_numpy(), index=ends)
    m["op_margin_chg"] = om - _lag(om, ends, 364)
    t_rev4, t_op4 = _lag(t_rev, ends, 364), _lag(t_op, ends, 364)
    rev_g = np.where(t_rev4 > 0, t_rev / t_rev4 - 1, np.nan)
    op_g = np.where(t_op4 > 0, t_op / t_op4 - 1, np.nan)
    m["op_lev"] = op_g - rev_g                                   # > 0: operating income outgrowing revenue
    m["op_turn_pos"] = ((t_op > 0) & (t_op4 <= 0)).astype(float).where(t_op.notna() & t_op4.notna())
    m["fcf_margin"] = np.where(t_rev > 0, t_fcf / t_rev, np.nan)
    fm = pd.Series(m["fcf_margin"].to_numpy(), index=ends)
    m["fcf_margin_chg"] = fm - _lag(fm, ends, 364)
    lev_ok = (m["op_lev"] > 0) | (m["op_turn_pos"] == 1)
    m["inflection"] = ((m["rev_accel_q"] >= 2) & lev_ok & (m["op_margin_chg"] > 0)
                       & (m["fcf_margin_chg"] > 0)).astype(float).where(m["rev_accel_q"].notna())
    filed = pd.concat([q[k]["filed"].reindex(ends) for k in ("rev", "opinc", "ocf", "capex") if k in q and not q[k].empty], axis=1)
    m["avail"] = filed.max(axis=1) + pd.Timedelta(days=1)       # usable from the day after the filing
    m.index.name = "end"
    return m.reset_index()


def company_metrics(company: dict) -> pd.DataFrame:
    return metrics({k: quarterly(_facts(company, tags)) for k, tags in CONCEPTS.items()})


def load_fundamentals(cache_dir: str, tickers: list[str], max_age_days: int = 6) -> pd.DataFrame:
    """Quarterly metrics for `tickers` (cached parquet). Empty frame if the SEC can't be reached."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / "fundamentals.parquet"
    if out.exists() and (time.time() - out.stat().st_mtime) < max_age_days * 86400:
        return pd.read_parquet(out)
    raw = _get(TICKERS_URL)
    if raw is None:
        print("[fund] could not get the SEC ticker list; fundamentals skipped")
        return pd.DataFrame()
    cik = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in json.loads(raw).values()}
    zpath = cache / "companyfacts.zip"
    if _get(BULK_URL, dest=zpath) is None:
        print("[fund] could not download companyfacts.zip; fundamentals skipped")
        return pd.DataFrame()
    frames, missing = [], 0
    with zipfile.ZipFile(zpath) as z:
        names = set(z.namelist())
        for t in tickers:
            c = cik.get(t.upper())
            name = f"CIK{c:010d}.json" if c else None
            if name not in names:
                missing += 1
                continue
            try:
                m = company_metrics(json.load(io.TextIOWrapper(z.open(name), encoding="utf-8")))
            except Exception as e:
                print(f"[fund] {t}: {e}")
                continue
            if len(m):
                frames.append(m.assign(ticker=t))
    zpath.unlink(missing_ok=True)
    print(f"[fund] metrics for {len(frames)} tickers ({missing} without SEC data)")
    if not frames:
        return pd.DataFrame()
    f = pd.concat(frames, ignore_index=True)
    f = f.astype({c: "float32" for c in f.select_dtypes("float64").columns})
    f.to_parquet(out, index=False)
    return f


def attach(d: pd.DataFrame, fund: pd.DataFrame, max_stale_days: int = 200) -> pd.DataFrame:
    """Add the latest metrics known on each row's date (as-of the filing date, never later)."""
    if fund is None or fund.empty or d.empty:
        return d.assign(**{c: np.nan for c in FUND_FEATURES})
    # several quarters can become known on the same day (a first XBRL filing with comparatives):
    # keep the most recent quarter
    f = fund.dropna(subset=["avail"]).sort_values(["avail", "end"])
    f = f.drop_duplicates(["ticker", "avail"], keep="last")
    left = d.reset_index().rename(columns={"index": "_row"}).sort_values("date")
    m = pd.merge_asof(left, f[["ticker", "avail"] + [c for c in FUND_FEATURES if c in f and c != "fund_age"]],
                      left_on="date", right_on="avail", by="ticker",
                      tolerance=pd.Timedelta(days=max_stale_days), direction="backward")
    m = m.assign(fund_age=(m["date"] - m["avail"]).dt.days).astype({c: "float32" for c in FUND_FEATURES})
    return m.drop(columns="avail").sort_values("_row").set_index("_row").rename_axis(None)
