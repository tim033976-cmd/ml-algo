"""Builds docs/ML_Algo_Project_Overview.pdf: what the project is, how it works, what we learnt, where we are."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

OUT = str(__import__("pathlib").Path(__file__).with_name("ML_Algo_Project_Overview.pdf"))
INK, MUTED, ACCENT = colors.HexColor("#1b1f24"), colors.HexColor("#5b6470"), colors.HexColor("#1f6f5c")
GOOD, BAD, WARN = colors.HexColor("#e3f2ea"), colors.HexColor("#fbe7e6"), colors.HexColor("#fdf3dc")
LINE, HEAD = colors.HexColor("#d5dae0"), colors.HexColor("#eef1f4")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=17, textColor=INK, spaceBefore=4, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, textColor=ACCENT, spaceBefore=10, spaceAfter=5)
B = ParagraphStyle("B", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
SM = ParagraphStyle("SM", parent=B, fontSize=8.6, leading=11.2, textColor=MUTED)
CELL = ParagraphStyle("CELL", parent=B, fontSize=8.5, leading=11, spaceAfter=0)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold")
BUL = ParagraphStyle("BUL", parent=B, leftIndent=12, bulletIndent=2, spaceAfter=3)
TITLE = ParagraphStyle("T", parent=H1, fontSize=26, leading=30, spaceAfter=6)
SUB = ParagraphStyle("S", parent=B, fontSize=11.5, leading=15, textColor=MUTED)


def p(t, s=B):
    return Paragraph(t, s)


def bullets(items):
    return [Paragraph(t, BUL, bulletText="•") for t in items]


def table(rows, widths, head=True, shade=None, font=CELL):
    data = [[c if not isinstance(c, str) else Paragraph(c, CELLB if (head and i == 0) else font) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    for (r, col) in (shade or {}).items():
        st.append(("BACKGROUND", (0, r), (-1, r), col))
    t.setStyle(TableStyle(st))
    return t


def box(text, color=GOOD):
    t = Table([[Paragraph(text, B)]], colWidths=[174 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def flow(labels, sub, width=174 * mm, h=26 * mm, fill="#e8f1ee"):
    """A left-to-right chain of boxes with arrows."""
    d = Drawing(width, h)
    n = len(labels)
    gap = 5 * mm
    bw = (width - gap * (n - 1)) / n
    for i, (lab, s) in enumerate(zip(labels, sub)):
        x = i * (bw + gap)
        d.add(Rect(x, 6, bw, h - 10, fillColor=colors.HexColor(fill), strokeColor=ACCENT, strokeWidth=0.8, rx=4, ry=4))
        d.add(String(x + bw / 2, h - 16, lab, fontName="Helvetica-Bold", fontSize=8.6, fillColor=INK, textAnchor="middle"))
        for k, line in enumerate(s.split("\n")):
            d.add(String(x + bw / 2, h - 27 - k * 9, line, fontName="Helvetica", fontSize=7.2, fillColor=MUTED, textAnchor="middle"))
        if i < n - 1:
            ax = x + bw + 0.8
            y = 6 + (h - 10) / 2
            d.add(Line(ax, y, ax + gap - 2.5, y, strokeColor=ACCENT, strokeWidth=1))
            d.add(Polygon([ax + gap - 1, y, ax + gap - 4, y + 2.2, ax + gap - 4, y - 2.2], fillColor=ACCENT, strokeColor=ACCENT))
    return d


def footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, 10 * mm, "ml-algo: ML-tested stock strategies on real data  |  status as of 10 Oct 2026")
    c.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    c.restoreState()


S = []
W = 174 * mm

# ---------------------------------------------------------------- page 1: the one-page summary
S += [p("ml-algo", TITLE),
      p("Using machine learning to find stock-trading strategies that really work, tested honestly on real market data", SUB),
      Spacer(1, 6),
      p("<b>In one sentence:</b> we are building a daily-chart system that picks stocks the way top momentum traders do "
        "(Qullamaggie, Minervini, O'Neil), and we use machine learning and strict testing on 20 years of real data to "
        "find out which of their rules actually make money, and which only look good in hindsight."),
      Spacer(1, 4),
      p("The bottom line so far", H2),
      box("<b>1. A real but modest edge exists, mostly from three things:</b> owning the strongest stocks (momentum), "
          "buying stocks that gap up on earnings news (episodic pivots), and sizing positions by how volatile they are."),
      Spacer(1, 4),
      box("<b>2. Many popular trading rules do NOT add anything on real data:</b> chart patterns (VCP, triangles, "
          "flags, tightness), candle patterns, market-timing filters (21/50 averages, breadth, A/D line), hot "
          "sectors, and predicting next-day / next-week direction (a coin flip).", BAD),
      Spacer(1, 4),
      box("<b>3. Our biggest lesson was survivorship bias.</b> Testing only on today's stocks made results look about "
          "twice as good as reality. After adding stocks that later dropped out of the S&amp;P 500, our ML stock-picking "
          "model made 10.5% a year vs 14.6% for simply holding SPY. A simple momentum portfolio made 22% a year (but "
          "with deep drawdowns).", WARN),
      Spacer(1, 4),
      box("<b>4. Where we are now:</b> testing a concentrated portfolio of the top 3-5 leaders, run on top traders' "
          "rules and updated at every close, with fundamentals (sales and EPS growth) required to confirm each pick "
          "(runs 25-26, in progress). Then 3-6 months of paper trading before any real money.", colors.HexColor("#e7eef8")),
      Spacer(1, 8),
      p("Progress at a glance", H2),
      table([["Part", "Status", "Where it stands"],
             ["Finding what works (research)", "~80% done", "26 research runs; the main questions are answered"],
             ["Honest testing (no hidden bias)", "~75% done", "Survivorship mostly fixed; fully clean data still missing"],
             ["Final strategy design", "In progress", "Concentrated leader portfolio + fundamentals (runs 25-26)"],
             ["Daily tool (today's picks)", "Built, needs upgrade", "Works as promised in a replay (42% hit rate) but uses an older model"],
             ["Proof in real time (paper trading)", "Just started", "60 picks logged; needs 3-6 months"]],
            [58 * mm, 32 * mm, 84 * mm], shade={1: GOOD, 2: GOOD, 3: WARN, 4: WARN, 5: BAD}),
      PageBreak()]

# ---------------------------------------------------------------- page 2: goal and how it works
S += [p("1. What we are trying to do", H1),
      p("The goal, in the user's own terms:"),
      *bullets(["<b>Daily chart only</b>, no intraday trading.",
                "Follow the style of top momentum traders: buy strong leading stocks breaking out or gapping up on news, cut "
                "losers fast, let winners run.",
                "Catch big movers like NVDA, SNDK or PLTR <b>once they are going up</b> (no need to be early), with the "
                "fundamentals backing the move.",
                "Original target: a high chance of +10% to +20% before a -10% loss. (We learnt that 'high chance' is set by "
                "the bracket, not by skill: see page 6.)",
                "Hold a small, concentrated portfolio (3-5 stocks) that updates every day from the closing prices."]),
      p("How a strategy is built", H2),
      p("Every strategy we test follows the same chain. Each box is something we test many versions of:"),
      flow(["Universe", "Screen / rank", "Setup", "Entry", "Exit & size"],
           ["S&P 500/400/600\n~1,540 stocks", "momentum, RS,\nML model, fundamentals", "breakout, gap,\nbase, flag, VCP",
            "at the close\n(or next-day stop)", "trailing average,\nstop, position size"]),
      Spacer(1, 4),
      p("How the research works", H2),
      p("We never trust a rule because a famous trader uses it. Each idea goes through the same loop:"),
      flow(["Idea", "Code + tests", "Real-data run", "Report", "Decision + log"],
           ["from you, a book,\na course or a PDF", "rules written exactly;\nunit tests for bugs", "GitHub Actions,\nYahoo + SEC data",
            "results/report.md\n(~50 tables)", "results/LOG.md;\nkeep, drop or refine"], fill="#eef1f8"),
      p("Each research run takes about 1-1.5 hours on GitHub's servers, downloads 20 years of daily prices, tests "
        "hundreds of thousands of trades, and writes its findings back to the repository. 26 runs have been done.", SM),
      PageBreak()]

# ---------------------------------------------------------------- page 3: honesty rules
S += [p("2. How we keep the testing honest", H1),
      p("Most trading results online are too good to be true because of a few common mistakes. These are the rules we "
        "follow to avoid them:"),
      table([["Rule", "Why it matters"],
             ["<b>Real data only</b> (Yahoo prices, SEC filings)", "Made-up data can't tell us anything about real markets."],
             ["<b>Choose on 2006-2017, judge on 2018-today</b>", "If you pick the best rule using all the data, it will look "
              "great by luck. We pick on the first period and check on the second, which the choice never saw."],
             ["<b>Compare with random entries</b>", "A rule only has an edge if it beats buying random stocks in an uptrend with "
              "the same exit. Rising markets make almost everything look good."],
             ["<b>Point-in-time stocks, incl. former members</b>", "Testing only on today's S&amp;P 500 hides the stocks that "
              "crashed and were removed (survivorship bias). This inflated our results about 2x."],
             ["<b>No peeking at the future</b>", "Every signal uses only data known at that day's close; filings count from the "
              "day after they were filed. Automated tests check this."],
             ["<b>Realistic costs</b>", "0.1% per side by default, stress-tested at 0.3%."],
             ["<b>Write the rule down before testing</b>", "Rules from a source are tested exactly as written, and what would "
              "prove them wrong is decided in advance."],
             ["<b>Ask 'who is overpaying, and why?'</b>", "A real edge needs a counterparty with a reason (slow funds, forced "
              "sellers, underreaction to news). Indicators with no reason behind them usually fail."]],
            [62 * mm, 112 * mm]),
      Spacer(1, 6),
      p("Key terms used in this document", H2),
      table([["Term", "Meaning"],
             ["<b>R</b>", "Profit measured in units of the risk taken. +1R = made as much as was risked; -1R = lost the full risk."],
             ["<b>IS / OOS</b>", "In-sample (2006-2017, used to choose) and out-of-sample (2018-today, used to judge)."],
             ["<b>Point-in-time (PIT)</b>", "Only counting a stock while it was actually in the S&amp;P 500, including stocks "
              "later removed. The honest benchmark."],
             ["<b>CAGR / max drawdown</b>", "Average yearly growth / the worst fall from a peak."],
             ["<b>ADR</b>", "Average daily range: how much a stock typically moves in a day (5% = volatile)."],
             ["<b>Episodic pivot (EP)</b>", "A stock gapping up 8-10%+ on very high volume, usually on earnings news."],
             ["<b>Momentum / RS</b>", "How strongly a stock has risen vs others over 1-12 months."]],
            [42 * mm, 132 * mm]),
      PageBreak()]

# ---------------------------------------------------------------- page 4: scoreboard
S += [p("3. The honest scoreboard", H1),
      p("Portfolio results from 2018 to today, using only stocks that were in the S&amp;P 500 at the time (including "
        "ones later removed), 0.1% costs per side. This is the fairest comparison we can make with free data."),
      table([["Approach", "Return / year", "Worst drawdown", "Verdict"],
             ["Simple momentum portfolio (top 10 by 6m/1m return, monthly)", "22.4%", "-41%", "Best return, deep drops"],
             ["ML stock-picking model + size by volatility (ADR)", "16.3%", "-32%", "Beats SPY"],
             ["<b>SPY (S&amp;P 500 index fund)</b>", "<b>14.6%</b>", "<b>-34%</b>", "<b>The bar to beat</b>"],
             ["Episodic pivots (earnings gaps), strong stocks, 50-day exit", "13.0%", "-25%", "Lower risk"],
             ["ML stock-picking model, equal size", "10.5%", "-33%", "Doesn't beat SPY"],
             ["Same model, costs 0.3% per side", "7.0%", "-41%", "Costs matter"],
             ["Breadth timing of SPY (course idea)", "5.2%", "-28%", "Fails"],
             ["The workflow PDF's full plan, as written", "6.3%", "-17%", "Too small positions"]],
            [80 * mm, 26 * mm, 28 * mm, 40 * mm], shade={1: GOOD, 2: GOOD, 3: HEAD, 5: BAD, 6: BAD, 7: BAD, 8: BAD}),
      p("Note: in earlier runs the ML model showed 21-28% a year. Those numbers were inflated by survivorship bias "
        "(page 6). Numbers on all stocks without the point-in-time rule are still higher (about 27%) and should not be "
        "trusted.", SM),
      p("Per-trade edges that held up in both periods", H2),
      table([["Setup or rule", "Before 2018", "2018-today", "Random entries (same rules)"],
             ["Episodic pivot on an earnings day (50-day exit)", "+0.28R", "+0.44R", "about 0R"],
             ["Rocket breakouts (6-week base to new high / 5% gap holding)", "+0.06 to +0.07R", "+0.13 to +0.20R", "-0.14 / -0.06R"],
             ["21/50 EMA cross then base breakout, strong stocks (course)", "+0.10R", "+0.21R", "-0.13 / +0.01R"],
             ["Ranking same-day signals by relative strength", "", "about +16 points a year vs random order", ""]],
            [74 * mm, 30 * mm, 34 * mm, 36 * mm]),
      PageBreak()]

# ---------------------------------------------------------------- page 5: works / doesn't
S += [p("4. What works and what doesn't", H1),
      p("What held up on real data", H2),
      table([["Finding", "Evidence", "Who's overpaying (the reason)"],
             ["Momentum: own the strongest stocks", "Momentum portfolio 22%/yr PIT; RS filters help every setup",
              "Fund money arrives slowly; investors underreact"],
             ["Episodic pivots (gap up on earnings)", "+0.44R on earnings days vs +0.10R for other gaps",
              "Institutions take weeks to rebuild positions after a surprise"],
             ["Buy the fear", "Model picks hit +20% first 43% of the time when VIX is 20-30 vs about 30% when calm",
              "Forced sellers (margin calls, volatility-targeting funds)"],
             ["Close below the 50-day average as the exit", "Most robust exit in every run", "Lets big trends run"],
             ["Size by volatility (ADR) / adapt size to recent results", "PIT 16% vs 10.5%; adaptive sizing helped every time",
              "Risk control"],
             ["QQQ above its 200-day for breakouts", "Breakouts +0.2R in green markets, negative otherwise", "Breakouts need buyers"]],
            [52 * mm, 66 * mm, 56 * mm], shade={i: GOOD for i in range(1, 7)}),
      p("What did NOT hold up", H2),
      table([["Idea", "Result"],
             ["Chart patterns: VCP, flags, ascending triangles, tight coils, Darvas-style bases", "No edge over random entries"],
             ["Candles, gaps, fair-value gaps, round numbers, support/resistance for next-day direction", "Coin flip (51-52%)"],
             ["Market filters: SPY/QQQ vs 21/50 averages, breadth, A/D line", "Didn't raise the odds; mostly cut good trades"],
             ["Leading sectors / sub-industries (both strong, both green, top 3)", "Cut returns roughly in half"],
             ["Up/down volume 'accumulation', not chasing 10% above the 21 EMA", "No help"],
             ["Fundamental 'inflection' (accelerating sales, margins, FCF) as a filter", "No help as a filter; small help as an ML input"],
             ["Qullamaggie's fast 10/20-day exits on daily bars", "Lose money (his intraday entries can't be tested here)"],
             ["Supertrend + 21 EMA (claimed 60-70% win rate)", "29-47% win rate, small edge"],
             ["Parabolic shorts", "60% win rate but about 0% average return"],
             ["A 70% win rate on +20/-10", "Not realistic: see page 6"]],
            [110 * mm, 64 * mm], shade={i: BAD for i in range(1, 11)}),
      PageBreak()]

# ---------------------------------------------------------------- page 6: big lessons
S += [p("5. The three biggest lessons", H1),
      p("Lesson 1: survivorship bias can double your results", H2),
      p("If you test on today's S&amp;P 500 members, you only test companies that survived and grew. The ones that "
        "crashed were removed and are missing. In run 12, the same strategy made 47% a year on all dates but only 20% "
        "when a stock was traded only after it actually joined the index. In run 24, adding 158 former members cut the "
        "ML model from 21% to 10.5% a year."),
      table([["Same ML model, 2018-today", "Return / year", "Worst drawdown"],
             ["Today's members, all dates (run 18)", "21.3%*", "-30%"],
             ["Current members only, point-in-time (run 24)", "12.9%", "-26%"],
             ["Including former members (run 24, honest)", "10.5%", "-33%"],
             ["SPY", "14.6%", "-34%"]],
            [100 * mm, 36 * mm, 38 * mm], shade={1: BAD, 3: GOOD}),
      p("* Run 18 used today's member list. Stocks that bankrupted or were bought out are still missing, so even 10.5% "
        "may be slightly optimistic.", SM),
      p("Lesson 2: win rate is set by the bracket, not by skill", H2),
      p("A stock moving randomly hits +20% before -10% about a third of the time, because the target is twice as far as "
        "the stop. Our best picks did this 38-44% of the time. You can get a 70%+ win rate with +5/-10, but you lose twice "
        "as much each time you're wrong, so it earns the same or less. Top traders like Qullamaggie win only 25-30% of "
        "their trades and make their money on a few big winners."),
      table([["Target / stop", "Our hit rate", "Break-even", "Profit per trade"],
             ["+5% / -10%", "72%", "67%", "+0.8%"],
             ["+10% / -10%", "57%", "50%", "+1.5%"],
             ["+20% / -10%", "38%", "33%", "+2.6%"],
             ["+20% / -15%", "46%", "43%", "+4.0%"]],
            [44 * mm, 40 * mm, 40 * mm, 50 * mm]),
      p("Lesson 3: our ML edge was mostly risk, not skill", H2),
      p("Compared with random stocks of the same volatility and momentum, the ML model's picks earned only about +1% "
        "more per trade after 2018 and about 0% before; the edge was positive in only 10 of 19 years. After adjusting for "
        "market exposure, its extra return over SPY (+1.5% a year) was not statistically meaningful. In plain terms: the "
        "model mostly learnt 'volatile momentum stocks go up more in rising markets', which you are paid for by taking more "
        "risk. That is why we moved to a simpler, rule-based leader portfolio."),
      PageBreak()]

# ---------------------------------------------------------------- page 7: sources tested
S += [p("6. Ideas tested from the user's sources", H1),
      p("Every source was turned into exact rules and tested, not taken on trust:"),
      table([["Source", "What was tested", "Verdict"],
             ["Qullamaggie (breakouts, EPs, parabolic shorts)", "His scan (top 3% performers, ADR 4%+), flag breakouts, "
              "EPs, 10/20-day trailing exits, QQQ regime, parabolic shorts", "Scan + EPs work; fast exits fail on daily bars; shorts no edge"],
             ["Minervini / O'Neil (VCP, CAN SLIM)", "Trend template, VCP, bases, 7-8% stops, 50-day exit, 52-week highs",
              "50-day exit and stops work; VCP itself no edge"],
             ["Your multibagger / playbook notes", "8/21 EMA cross, retests, undercut, flags, trim exits", "Mostly no edge; RS filter helps"],
             ["Stock Selection Workflow PDF", "Rockets, Nasdaq-100 scanner, regime, sizing, 40/25/15/20 split",
              "Rockets work; scanner doesn't; plan as sized made 6%/yr"],
             ["Early fundamental inflection (video)", "Accelerating sales, operating leverage, margins, FCF, up/down volume, "
              "not extended", "No help as filters; small help inside the model"],
             ["ADR% infographic", "5% minimum, 5-12% sweet spot, $10M liquidity, size by ADR", "Sizing by ADR helps; buckets don't"],
             ["Techno Charts swing course (79 videos)", "21 EMA rules, breadth timing, momentum portfolio, Supertrend, "
              "EMA-cross bases, reversals", "Momentum portfolio and EMA-cross bases work; most else fails"],
             ["'Who is overpaying?' framework", "Earnings placebo, volatility-matched check, survivorship", "Confirmed EPs; exposed the ML model"],
             ["Short-term direction (green day, 3 days, week)", "Candles, gaps, FVGs, levels, VIX, weekly structure",
              "Coin flip (AUC 0.51-0.52)"]],
            [44 * mm, 80 * mm, 50 * mm]),
      PageBreak()]

# ---------------------------------------------------------------- page 8: timeline
S += [p("7. Timeline of the research runs", H1),
      table([["Run", "Question", "Answer"],
             ["1-3", "Which classic setups beat random entries?", "Episodic pivots (all variants); the 50-day exit; ranking by RS"],
             ["4-6", "Selection method, themes, honest drawdowns, patterns", "Pick by expected R; themes and most patterns don't help; drawdowns ~-50%"],
             ["10-12", "How do top traders beat the market?", "Stock selection model (4x hit rate) but survivorship inflates results"],
             ["13-14", "Your goal: +10/20% before -10%", "38-44% hit rate vs 33% break-even; first daily picks tool"],
             ["15", "Replicate Qullamaggie", "Scan and EPs work; fast exits fail on daily bars"],
             ["16", "Green day / next 3 days / next week", "Coin flip"],
             ["17-18", "Bracket menu, market regime, VIX", "Win rate set by geometry; buy the fear"],
             ["19, 21", "Leading sectors, 21/50 averages, breadth, A/D line", "None help"],
             ["20", "Your workflow PDF", "Rockets work, scanner doesn't, sizing too small"],
             ["22-24", "Fundamentals, ADR, earnings, survivorship, course ideas", "Big survivorship correction; momentum + EP + ADR sizing hold up"],
             ["25-26", "3-5 stock leader portfolio on traders' rules + fundamentals", "In progress"]],
            [16 * mm, 70 * mm, 88 * mm], shade={11: colors.HexColor("#e7eef8")}),
      PageBreak()]

# ---------------------------------------------------------------- page 9: current work and next steps
S += [p("8. What's happening now", H1),
      p("Runs 25-26: a concentrated leader portfolio on top traders' rules", H2),
      *bullets(["Hold <b>3 to 5 stocks</b>, equal weight, decided at each close.",
                "<b>Leaders only:</b> $10+, $20M+ traded a day, above a rising 50-day that's above the 200-day, within 25% of "
                "the 52-week high, ranked by momentum.",
                "<b>Entry:</b> the best-ranked leader fills an empty slot, optionally only on a setup day (EP, breakout, base, "
                "flag) and only while QQQ is above its 200-day.",
                "<b>Exit:</b> close below the 10/20/50-day average, 8% below entry, or dropping out of the top ranks.",
                "<b>Fundamentals must confirm</b> (run 26): sales growth 20%+, EPS growth 25%+, or a recent earnings gap up, "
                "so NVDA / SNDK-type moves are caught once they are underway.",
                "1,008 combinations; the winner is picked on 2007-2017 and judged on 2018-today; includes a case study of trades "
                "in NVDA, SNDK, PLTR, SMCI, META, AVGO, VRT, ANET, CRWD and APP."]),
      p("Tools already built", H2),
      table([["Tool", "What it does", "Status"],
             ["Research pipeline (research.py)", "Runs every test on GitHub and writes results/report.md", "Working"],
             ["Daily picks (picks.py)", "Ranks stocks each evening with stops and targets", "Works (42% hit rate in replay); old model"],
             ["Forward test log", "Records the daily top 10 and scores them as prices arrive", "60 picks logged, none finished yet"]],
            [46 * mm, 80 * mm, 48 * mm]),
      p("Next steps", H2),
      table([["#", "Step", "Why"],
             ["1", "Read runs 25-26; pick the leader-portfolio version", "Decide the final strategy on honest numbers"],
             ["2", "Turn the daily picks into a 'today's portfolio' list", "Hold these, sell when this level breaks"],
             ["3", "Merge to the main branch", "So the daily list and paper trading run automatically every evening"],
             ["4", "Paper trade for 3-6 months", "The only test the strategy has never seen"],
             ["5", "Verify on survivorship-free data (QuantConnect or paid data)", "Close the last big source of bias"]],
            [8 * mm, 86 * mm, 80 * mm]),
      p("Open decisions", H2),
      *bullets(["<b>Merge to main</b> (needed for the automatic daily run): waiting for the final strategy.",
                "<b>Data:</b> free data so far. QuantConnect (delisted stocks included) needs a new session with that "
                "website allowed. Alpha Vantage's free tier (25 requests a day) is too small for full tests; a premium "
                "key would add earnings surprises and some delisted prices.",
                "<b>Singapore:</b> not tested yet; Yahoo has SGX prices, but announcement dates are harder to get."]),
      PageBreak()]

# ---------------------------------------------------------------- page 10: limits and repo map
S += [p("9. Honest limits", H1),
      *bullets(["<b>Daily bars only:</b> intraday entries (Qullamaggie's opening-range high with a stop at the day's low) "
                "can't be tested, and that may be where some of his edge comes from.",
                "<b>Survivorship is reduced, not removed:</b> stocks that went bankrupt or were bought out have no free prices.",
                "<b>2018-today has now been looked at many times.</b> Anything chosen because it looked good after 2018 is not "
                "proven by it. Paper trading is the real final test.",
                "<b>Concentrated portfolios swing hard.</b> With 3-5 stocks at 20-33% each, one bad gap can cost 5-10% of the "
                "account. Drawdowns of 30-40% are realistic even for good versions.",
                "<b>This is research, not financial advice.</b> Nothing here guarantees future results."]),
      p("10. Where everything lives", H1),
      table([["File / folder", "What's in it"],
             ["results/report.md", "The latest full research report (all tables)"],
             ["results/LOG.md", "Every run: question, change, result, decision (newest first)"],
             ["results/today_picks.md, forward_test.md", "Daily picks and the paper-trading record"],
             ["CLAUDE.md", "Project rules and the list of known findings"],
             ["mlalgo/research/", "The code: entries (setups), engine (exits), analyze (tests), rotation (portfolio), "
              "fundamentals (SEC data), shorts"],
             ["research.py, picks.py", "Run the research / make today's picks"],
             [".github/workflows/", "Automatic runs on GitHub (research on every code change, picks daily)"]],
            [62 * mm, 112 * mm])]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                        title="ml-algo: project overview", author="ml-algo")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
