"""Point-in-time fundamentals parsing (handcrafted SEC companyfacts JSON, mechanics only)."""
import numpy as np
import pandas as pd

from mlalgo.research import fundamentals as F


def _fact(start, end, val, filed, form="10-Q"):
    return {"start": start, "end": end, "val": val, "filed": filed, "form": form}


def _company(rev, op=None, ocf=None, capex=None):
    g = {"Revenues": {"units": {"USD": rev}}}
    if op:
        g["OperatingIncomeLoss"] = {"units": {"USD": op}}
    if ocf:
        g["NetCashProvidedByUsedInOperatingActivities"] = {"units": {"USD": ocf}}
    if capex:
        g["PaymentsToAcquirePropertyPlantAndEquipment"] = {"units": {"USD": capex}}
    return {"facts": {"us-gaap": g}}


def _year(y, qs, filed_lag=30, ytd=False):
    """Facts for one calendar fiscal year: Q1-Q3 from 10-Qs, the full year from the 10-K. With
    ytd=True the 10-Qs report year-to-date values (like cash flow statements)."""
    ends = [f"{y}-03-31", f"{y}-06-30", f"{y}-09-30"]
    out, cum = [], 0.0
    for i, (e, v) in enumerate(zip(ends, qs[:3])):
        cum += v
        filed = (pd.Timestamp(e) + pd.Timedelta(days=filed_lag)).strftime("%Y-%m-%d")
        start = f"{y}-01-01" if ytd or i == 0 else (pd.Timestamp(ends[i - 1]) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        out.append(_fact(start, e, cum if ytd else v, filed))
    out.append(_fact(f"{y}-01-01", f"{y}-12-31", sum(qs), f"{y + 1}-02-20", "10-K"))
    return out


def test_quarterly_derives_q4_and_ytd_quarters_and_keeps_first_filing():
    facts = _year(2020, [10, 11, 12, 13], ytd=True)
    # a later restatement of Q1 (filed a year later) must not replace the original value
    facts.append(_fact("2020-01-01", "2020-03-31", 99, "2021-05-01"))
    q = F.quarterly(F._facts(_company(facts), ["Revenues"]))
    assert list(q["val"]) == [10, 11, 12, 13]
    assert q.loc["2020-12-31", "filed"] == pd.Timestamp("2021-02-20")   # Q4 known only with the 10-K
    assert q.loc["2020-06-30", "filed"] == pd.Timestamp("2020-07-30")


def test_inflection_metrics_and_point_in_time_attach():
    # revenue growth YoY accelerating: 2019 flat at 100/quarter, 2020: 95, 99, 103, 108 -> 2021: faster
    rev = _year(2019, [100] * 4) + _year(2020, [95, 99, 103, 108]) + _year(2021, [104, 112, 122, 135])
    op = _year(2019, [10] * 4) + _year(2020, [8, 9, 11, 13]) + _year(2021, [12, 16, 20, 25])
    ocf = _year(2019, [12] * 4, ytd=True) + _year(2020, [10, 11, 13, 15], ytd=True) + _year(2021, [14, 18, 22, 27], ytd=True)
    capex = _year(2019, [2] * 4, ytd=True) + _year(2020, [2] * 4, ytd=True) + _year(2021, [2] * 4, ytd=True)
    m = F.company_metrics(_company(rev, op, ocf, capex)).set_index("end")
    q = m.loc["2021-06-30"]
    assert np.isclose(q["rev_yoy"], 112 / 99 - 1)
    assert np.isclose(q["rev_yoy_d1"], (112 / 99 - 1) - (104 / 95 - 1))
    assert q["rev_accel_q"] >= 2 and q["op_margin_chg"] > 0 and q["fcf_margin_chg"] > 0 and q["inflection"] == 1
    assert q["avail"] == pd.Timestamp("2021-07-31")      # the day after the 10-Q filing
    # attach: a row dated before the filing sees the previous quarter, after it sees this one
    fund = m.reset_index().assign(ticker="X")
    d = pd.DataFrame({"ticker": ["X", "X", "Y"], "date": pd.to_datetime(["2021-07-30", "2021-08-02", "2021-08-02"])})
    a = F.attach(d, fund)
    assert np.isclose(a.loc[0, "rev_yoy"], 104 / 95 - 1) and np.isclose(a.loc[1, "rev_yoy"], 112 / 99 - 1)
    assert np.isnan(a.loc[2, "rev_yoy"]) and list(a.index) == [0, 1, 2]
    assert a.loc[1, "fund_age"] == 2


def test_attach_without_data_adds_empty_columns():
    d = pd.DataFrame({"ticker": ["X"], "date": pd.to_datetime(["2021-01-04"])})
    a = F.attach(d, pd.DataFrame())
    assert set(F.FUND_FEATURES) <= set(a.columns) and a[F.FUND_FEATURES].isna().all().all()
