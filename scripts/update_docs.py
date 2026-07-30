#!/usr/bin/env python3
"""
Auto-update README.md, DATA_TABLES.md, and paper/main.tex with the latest
market data from generated CSVs.

Run after rebuild_outputs.py — reads data/price_summary.csv and
eventstudy/valuation_summary.csv, then patches hardcoded numbers.

Usage:
    python scripts/update_docs.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# ---- helpers ----

def _read_metric(csv_path: Path, metric: str) -> str:
    df = pd.read_csv(csv_path)
    row = df[df["metric"] == metric]
    if row.empty:
        raise KeyError(f"metric '{metric}' not found in {csv_path}")
    return str(row.iloc[0]["value"])


def _load_snapshot() -> dict:
    """Return a dict of computed values from current data."""
    summary = pd.read_csv(ROOT / "data" / "price_summary.csv")
    zhipu = summary[summary["code"] == "02513.HK"].iloc[0]
    minimax = summary[summary["code"] == "00100.HK"].iloc[0]
    wenge = summary[summary["code"] == "01956.HK"].iloc[0]

    price_hkd = float(zhipu["latest_close"])
    ipo = float(zhipu["ipo_price"])
    ret_pct = (price_hkd / ipo - 1) * 100
    ann_vol = float(zhipu["ann_vol_pct"])
    latest_date = str(zhipu["latest_date"])
    date_display = f"{latest_date[:4]}-{latest_date[4:6]}-{latest_date[6:8]}"

    # Shares and FX from rebuild_outputs.py constants
    SHARES_M = 445.843
    USD_HKD = 7.8
    REV_2026_USDM = 200

    equity_value_usdm = price_hkd * SHARES_M / USD_HKD
    revenue_multiple = equity_value_usdm / REV_2026_USDM

    # DCF gap from valuation_summary
    dcf_gap = _read_metric(ROOT / "eventstudy" / "valuation_summary.csv",
                           "DCF value as % of market")
    dcf_gap_pct = round((1 - float(dcf_gap)) * 100, 0)

    # Reverse DCF: approximate required 2035 revenue
    # From rebuild: at WACC 13.5%, terminal margin 40%, equity ~US$102bn-equivalent
    # The reverse DCF grid is in eventstudy/reverse_dcf_sensitivity.csv
    rev_req = None
    rev_grid_path = ROOT / "eventstudy" / "reverse_dcf_sensitivity.csv"
    if rev_grid_path.exists():
        rev_grid = pd.read_csv(rev_grid_path)
        base_row = rev_grid[(rev_grid["WACC"].round(1) == 0.135) &
                            (rev_grid["Term_margin"].round(1) == 0.4)]
        if len(base_row) > 0:
            rev_req = float(base_row.iloc[0]["Req_rev_2035_USDbn"])

    # Price per share from valuation
    prob_weighted = _read_metric(ROOT / "eventstudy" / "valuation_summary.csv",
                                 "Probability-weighted per share (HK$)")

    # Market equity from valuation_summary
    market_equity = _read_metric(ROOT / "eventstudy" / "valuation_summary.csv",
                                 "Market equity value (US$m)")

    return {
        "date_display": date_display,
        "price_hkd": price_hkd,
        "price_hkd_fmt": f"{price_hkd:,.0f}",
        "ipo_price": ipo,
        "ret_pct": ret_pct,
        "ret_pct_fmt": f"{ret_pct:+.0f}",
        "ret_vs_ipo_fmt": f"{round(ret_pct):+d}%",
        "ann_vol_pct": ann_vol,
        "ann_vol_fmt": f"{ann_vol:.0f}",
        "equity_value_usdm": equity_value_usdm,
        "equity_value_usdb": equity_value_usdm / 1000,
        "equity_value_fmt": f"US${equity_value_usdm/1000:.1f}B",
        "market_cap_hkd": price_hkd * SHARES_M,
        "market_cap_hkd_fmt": f"HK${price_hkd * SHARES_M / 1000:.1f}B",
        "revenue_multiple": revenue_multiple,
        "revenue_multiple_fmt": f"{revenue_multiple:.0f}",
        "dcf_gap_pct": dcf_gap_pct,
        "dcf_gap_fmt": f"~{dcf_gap_pct:.0f}%",
        "prob_weighted_hkd": round(float(prob_weighted)),
        "rev_req_usd_bn": rev_req,
        "rev_req_fmt": f"US${rev_req:.0f} 亿" if rev_req else "N/A",
        # CAGR to reach rev_req over 2026-2035 (9 years from US$200M base)
        "cagr_fmt": f"{((rev_req * 1000 / 0.2) ** (1/9) - 1) * 100:.0f}%" if rev_req else "N/A",
        # MiniMax data
        "minimax_price": float(minimax["latest_close"]),
        "minimax_ret": (float(minimax["latest_close"]) / float(minimax["ipo_price"]) - 1) * 100,
        # Wenge data
        "wenge_price": float(wenge["latest_close"]),
        "wenge_ret": (float(wenge["latest_close"]) / float(wenge["ipo_price"]) - 1) * 100,
    }


def _replace_between(content: str, marker_start: str, marker_end: str,
                     replacement: str) -> str:
    """Replace everything between two markers (inclusive of markers themselves)."""
    pattern = re.escape(marker_start) + r".*?" + re.escape(marker_end)
    return re.sub(pattern, marker_start + replacement + marker_end, content,
                  flags=re.DOTALL)


def update_readme(snap: dict) -> None:
    path = ROOT / "README.md"
    content = path.read_text(encoding="utf-8")

    # Badge: revenue multiple and DCF gap
    content = re.sub(
        r'收入倍数-~?\d+x · DCF缺口~?\d+%',
        f'收入倍数-~{snap["revenue_multiple_fmt"]}x · DCF缺口~{snap["dcf_gap_pct"]:.0f}%',
        content,
    )
    content = re.sub(
        r'Revenue multiple ~?\d+x · DCF gap ~?\d+%',
        f'Revenue multiple ~{snap["revenue_multiple_fmt"]}x · DCF gap ~{snap["dcf_gap_pct"]:.0f}%',
        content,
    )

    # Core data as of date
    content = re.sub(
        r'\*\*核心数据截至 / Core data as of:\*\* \d{4}-\d{2}-\d{2}',
        f'**核心数据截至 / Core data as of:** {snap["date_display"]}',
        content,
    )

    # 一句话概览中的市值和倍数 (Chinese)
    # "市值达约 707 亿美元（股权价值/收入约 354 倍）"
    content = re.sub(
        r'市值达约 [\d.,]+ 亿美元（股权价值/收入约 [\d.,]+ 倍）',
        f'市值达约 {snap["equity_value_usdm"]/100:.0f} 亿美元（股权价值/收入约 {snap["revenue_multiple_fmt"]} 倍）',
        content,
    )

    # 一句话概览中的市值和倍数 (English)
    content = re.sub(
        r'market cap of ~US\$\d+\.?\d*[Bb](?:illion)?[,.]?\s*(?:equity value[^)]*~?\d+x)',
        f'market cap of ~US${snap["equity_value_usdb"]:.0f}B, equity value / revenue ~{snap["revenue_multiple_fmt"]}×',
        content,
    )

    # DCF table market row — Chinese section
    # | *市价 (2026-07-24)* | — | — | *$70.7B* | *1,237* |
    content = re.sub(
        r'\|\s*\*市价\s*\(\d{4}-\d{2}-\d{2}\)\*\s*\|[^|]*\|[^|]*\|\s*\*\$[\d.]+B\*\s*\|\s*\*[\d,]+\*\s*\|',
        f'| *市价 ({snap["date_display"]})* | — | — | *${snap["equity_value_usdb"]:.1f}B* | *{snap["price_hkd_fmt"]}* |',
        content,
    )

    # Reverse DCF paragraph — Chinese
    # "2035 年收入约 US$730 亿" → update
    content = re.sub(
        r'2035 年收入约 \*\*US\$\d+ 亿\*\*（约 \*\*\d+%\*\* 的年复合增速，约 \d+ 倍 FY26E）',
        f'2035 年收入约 **US${snap["rev_req_usd_bn"]:.0f} 亿**（约 **{snap["cagr_fmt"]}** 的年复合增速，约 {snap["revenue_multiple_fmt"]} 倍 FY26E）'
        if snap["rev_req_usd_bn"] else content,
        content,
    )

    # "市场股权价值/收入约 354×"
    content = re.sub(
        r'市场股权价值/收入约 \*\*[\d,]+×\*\*',
        f'市场股权价值/收入约 **{snap["revenue_multiple_fmt"]}×**',
        content,
    )

    # 截至日期 in event study section
    content = re.sub(
        r'截至 \d{4}-\d{2}-\d{2}，GLM-5\.2',
        f'截至 {snap["date_display"]}，GLM-5.2',
        content,
    )

    # 港股AI新股 table — Zhipu row
    # | 智谱AI | 2513.HK | ... | IPO HK$116.20 → HK$1,237（+965%） |
    content = re.sub(
        r'(智谱AI\s*\|\s*2513\.HK\s*\|.*IPO HK\$\d+\.\d+ → HK\$)[\d,]+（[+\-][\d]+%）',
        f'\\g<1>{snap["price_hkd_fmt"]}（{snap["ret_vs_ipo_fmt"]}）',
        content,
    )

    # ---- English section ----
    # Market row in DCF table
    content = re.sub(
        r'\|\s*\*Market\s*\(\d{4}-\d{2}-\d{2}\)\*\s*\|[^|]*\|[^|]*\|\s*\*\$[\d.]+B\*\s*\|\s*\*[\d,]+\*\s*\|',
        f'| *Market ({snap["date_display"]})* | — | — | *${snap["equity_value_usdb"]:.1f}B* | *{snap["price_hkd_fmt"]}* |',
        content,
    )

    # Reverse DCF English
    content = re.sub(
        r'requires ~US\$\d+\.?\d*[Bb] revenue by 2035 \(~\d+% annual over 2026–2035, ~\d+×FY26E\)',
        f'requires ~US${snap["rev_req_usd_bn"]:.0f}B revenue by 2035 (~{snap["cagr_fmt"]} annual over 2026–2035, ~{snap["revenue_multiple_fmt"]}×FY26E)'
        if snap["rev_req_usd_bn"] else content,
        content,
    )

    # Market equity value / revenue ≈ NNN×
    content = re.sub(
        r'Market equity value / revenue ≈ \d+×',
        f'Market equity value / revenue ≈ {snap["revenue_multiple_fmt"]}×',
        content,
    )

    # As of date in English event study section
    content = re.sub(
        r'As of \d{4}-\d{2}-\d{2}, GLM-5\.2',
        f'As of {snap["date_display"]}, GLM-5.2',
        content,
    )

    # Zhipu row in English table
    content = re.sub(
        r'(Zhipu AI\s*\|\s*2513\.HK\s*\|.*IPO HK\$\d+\.\d+ → HK\$)[\d,]+（[+\-][\d]+%）（',
        f'\\g<1>{snap["price_hkd_fmt"]}（{snap["ret_vs_ipo_fmt"]}）（',
        content,
    )

    # Equity value / revenue in English
    content = re.sub(
        r'\(≈\d+x equity value / revenue\)',
        f'(≈{snap["revenue_multiple_fmt"]}x equity value / revenue)',
        content,
    )

    path.write_text(content, encoding="utf-8")
    print(f"[OK] Updated README.md with data as of {snap['date_display']}")


def update_data_tables(snap: dict) -> None:
    path = ROOT / "DATA_TABLES.md"
    content = path.read_text(encoding="utf-8")

    # Header date
    content = re.sub(
        r'\*\*as of \d{4}-\d{2}-\d{2}\*\*',
        f'**as of {snap["date_display"]}**',
        content,
    )
    content = re.sub(
        r'through \d{4}-\d{2}-\d{2}\.',
        f'through {snap["date_display"]}.',
        content,
    )
    content = re.sub(
        r'latest available Hong Kong trading day, \d{4}-\d{2}-\d{2}\.',
        f'latest available Hong Kong trading day, {snap["date_display"]}.',
        content,
    )

    # Table D2 title
    content = re.sub(
        r'### Table D2 - Market Performance \(IPO to \d{4}-\d{2}-\d{2}\)',
        f'### Table D2 - Market Performance (IPO to {snap["date_display"]})',
        content,
    )

    # Zhipu latest close in D2
    # | Latest close (HK$) | 1,237.0 (2026-07-24) | ...
    content = re.sub(
        r'(Latest close \(HK\$\)\s*\|\s*)[\d,]+\.?\d*\s*\(\d{4}-\d{2}-\d{2}\)\s*\|',
        f'\\g<1>{snap["price_hkd"]:.1f} ({snap["date_display"]}) |',
        content,
    )

    # MiniMax latest close
    # MiniMax price is second pipe in the row
    # This is trickier — the row has multiple pipes
    content = re.sub(
        r'(Latest close \(HK\$\)\s*\|[^|]+\|)\s*[\d,]+\.?\d*\s*\(\d{4}-\d{2}-\d{2}\)\s*\|',
        f'\\g<1> {snap["minimax_price"]:.1f} ({snap["date_display"]}) |',
        content,
    )

    # Wenge latest close
    content = re.sub(
        r'(Latest close \(HK\$\)\s*\|[^|]+\|[^|]+\|)\s*[\d,]+\.?\d*\s*\(\d{4}-\d{2}-\d{2}\)\s*\|',
        f'\\g<1> {snap["wenge_price"]:.1f} ({snap["date_display"]}) |',
        content,
    )

    # Return vs IPO row — Zhipu
    content = re.sub(
        r'(Return vs IPO\s*\|\s*\*\*)[+\-][\d]+%\s*\(~?[\d.]+x\)\*\*\s*\|',
        f'\\g<1>{snap["ret_vs_ipo_fmt"]} (~{abs(snap["ret_pct"])/100+1:.1f}x)** |',
        content,
    )

    # Return vs IPO row — MiniMax
    content = re.sub(
        r'(Return vs IPO\s*\|[^|]+\|\s*)[+\-][\d]+%\s*\|',
        f'\\g<1>{snap["minimax_ret"]:+.0f}% |',
        content,
    )

    # Return vs IPO row — Wenge
    content = re.sub(
        r'(Return vs IPO\s*\|[^|]+\|[^|]+\|\s*)[+\-][\d]+%\s*\|',
        f'\\g<1>{snap["wenge_ret"]:+.0f}% |',
        content,
    )

    # Period high/low — Zhipu
    # We don't recalculate these from historical data easily, keep manual

    # Latest market cap — Zhipu
    content = re.sub(
        r'(Latest market cap\s*\|\s*\*\*~HK\$\d+\.?\d*[Bb]\s*\(~US\$\d+\.?\d*[Bb]\)\*\*\s*\|)',
        f'**~{snap["market_cap_hkd_fmt"]} (~{snap["equity_value_fmt"]})** |',
        content,
    )

    # Equity value / revenue
    content = re.sub(
        r'(Equity value / revenue[^|]*\|\s*\*\*~)\d+x\*\*\s*\|',
        f'\\g<1>{snap["revenue_multiple_fmt"]}x** |',
        content,
    )
    content = re.sub(
        r'Equity value / revenue ≈ [\d.,]+x',
        f'Equity value / revenue ≈ {snap["revenue_multiple_fmt"]}x',
        content,
    )

    # Table D3 — Annualized volatility
    content = re.sub(
        r'(Annualized volatility[^|]*\|\s*\*\*~)\d+%\*\*\s*\|',
        f'\\g<1>{snap["ann_vol_fmt"]}%** |',
        content,
    )

    # Table D6 title
    content = re.sub(
        r'through \d{4}-\d{2}-\d{2}\)',
        f'through {snap["date_display"]})',
        content,
    )

    # As-of dates in notes
    content = re.sub(
        r'as of \d{4}-\d{2}-\d{2}\.',
        f'as of {snap["date_display"]}.',
        content,
    )

    # Implied market equity line
    content = re.sub(
        r'\*\*Implied market equity value / revenue ~= \d+x FY26E\*\* \(US\$\d+\.?\d*B / US\$200M\)',
        f'**Implied market equity value / revenue ~= {snap["revenue_multiple_fmt"]}x FY26E** (US${snap["equity_value_usdb"]:.1f}B / US$200M)',
        content,
    )

    path.write_text(content, encoding="utf-8")
    print(f"[OK] Updated DATA_TABLES.md with data as of {snap['date_display']}")


def update_paper_tex(snap: dict) -> None:
    """Update hardcoded market values in paper/main.tex.

    Only updates the DCF table market row and key numeric mentions in the
    abstract/intro/conclusion.  Narrative text is left intact; only numbers
    that come directly from market data are touched.

    Uses lambda replacements throughout because re.sub() interprets escape
    sequences (\\t, \\a, …) in string replacements, which wrecks LaTeX commands
    like \\textit and \\approx.
    """
    path = ROOT / "paper" / "main.tex"
    content = path.read_text(encoding="utf-8")

    price_tex = f"{snap['price_hkd']:,.0f}".replace(",", "{,}")
    equity_bn = snap["equity_value_usdb"]
    mult = snap["revenue_multiple_fmt"]
    vol = snap["ann_vol_fmt"]
    ret_tex = f"{snap['ret_pct']:+,.0f}".replace(",", "{,}")
    fold = round(snap["price_hkd"] / snap["ipo_price"])
    date_tex = snap["date_display"].replace("-", "~")
    date_dash = snap["date_display"]

    # ---- DCF table market row ----
    content = re.sub(
        r'\\textit\{Market \(\d{4}-\d{2}-\d{2}\)\} & --- & --- & '
        r'\\textit\{US\\\$\d+\.?\d*B\} & '
        r'\\textit\{\d[\d,\{\}]*\} \\\\',
        lambda _: (
            rf'\textit{{Market ({date_dash})}} & --- & --- & '
            rf'\textit{{US\${equity_bn:.1f}B}} & '
            rf'\textit{{{price_tex}}} \\'
        ),
        content,
    )

    # ---- Caption date ----
    content = re.sub(
        r'Market row at \d{4}-\d{2}-\d{2}\.',
        lambda _: f'Market row at {date_dash}.',
        content,
    )

    # ---- Intro: nineteen-fold? fourteen-fold? → recompute ----
    content = re.sub(
        r'about \w+?-fold to a market capitalisation near US\\\$\d+bn',
        lambda _: f'about {fold}-fold to a market capitalisation near US\\${equity_bn:.0f}bn',
        content,
    )

    # ---- equity value roughly NNN times ----
    content = re.sub(
        r'equity value roughly \d+ times',
        lambda _: f'equity value roughly {mult} times',
        content,
    )

    # ---- Intro: near US\$NNNbn ----
    content = re.sub(
        r'near US\\\$\d+bn on FY2026 expected revenue',
        lambda _: f'near US\\${equity_bn:.0f}bn on FY2026 expected revenue',
        content,
    )

    # ---- Intro: ~fourteen-fold ----
    content = re.sub(
        r'roughly \w+?-fold to a market',
        lambda _: f'roughly {fold}-fold to a market',
        content,
    )

    # ---- multiple near NNN$\times$ ----
    content = re.sub(
        r'multiple near \d+\$\\times\$',
        lambda _: f'multiple near {mult}$\\times$',
        content,
    )

    # ---- Conclusion HK\$ price ----
    content = re.sub(
        r'HK\\\$\d[\d,\{\}]* market price \(\d+~[A-Z][a-z]+~2026\)',
        lambda _: f'HK\\${price_tex} market price ({date_tex})',
        content,
    )

    # ---- US\$NNNbn-revenue outcome ----
    if snap["rev_req_usd_bn"]:
        rev_req = int(snap["rev_req_usd_bn"])
        content = re.sub(
            r'US\\\$\d+bn-revenue outcome',
            lambda _: f'US\\${rev_req}bn-revenue outcome',
            content,
        )

    # ---- re-rated to about HK\$NNN by DATE ----
    content = re.sub(
        r're-rated to about HK\\\$\d[\d,\{\}]* by \d+~[A-Z][a-z]+~2026',
        lambda _: f're-rated to about HK\\${price_tex} by {date_tex}',
        content,
    )

    # ---- return vs IPO ----
    content = re.sub(
        r'\$\\approx \+[\d,\{\}]+\\%\$ versus IPO',
        lambda _: f'$\\approx {ret_tex}\\%$ versus IPO',
        content,
    )

    # ---- realised annualised volatility near NNN% ----
    content = re.sub(
        r'realised annualised volatility near \d+\%',
        lambda _: f'realised annualised volatility near {vol}\\%',
        content,
    )

    # ---- volatility ($\approx$NNN% annualised) ----
    content = re.sub(
        r'\\\$\\approx\$[\d.]+\% annualised',
        lambda _: f'$\\approx${vol}\\% annualised',
        content,
    )

    # ---- NNN$\times$ equity value / revenue ----
    content = re.sub(
        r'\d+\$\\times\$ equity value / revenue',
        lambda _: f'{mult}$\\times$ equity value / revenue',
        content,
    )

    # ---- Zhipu's $\approx$NNN$\times$ ----
    content = re.sub(
        r'Zhipu\'s \$\\approx\$[\d.]+\$\\times\$',
        lambda _: f"Zhipu's $\\approx${mult}$\\times$",
        content,
    )

    # ---- near \textbf{NNN$\times$} ----
    content = re.sub(
        r'near \\textbf\{\d+\$\\times\$\}',
        lambda _: f'near \\textbf{{{mult}$\\times$}}',
        content,
    )

    # ---- US\$NNNbn equity value (reverse DCF) ----
    content = re.sub(
        r'US\\\$\d+bn equity value',
        lambda _: f'US\\${equity_bn:.0f}bn equity value',
        content,
    )

    # ---- about US\$NNNbn of 2035 revenue ----
    if snap["rev_req_usd_bn"]:
        rev_req = int(snap["rev_req_usd_bn"])
        content = re.sub(
            r'about US\\\$\d+bn of 2035 revenue',
            lambda _: f'about US\\${rev_req}bn of 2035 revenue',
            content,
        )

    # ---- Figure captions: through YYYY-MM-DD) ----
    content = re.sub(
        r'through \d{4}-\d{2}-\d{2}\)',
        lambda _: f'through {date_dash})',
        content,
    )

    path.write_text(content, encoding="utf-8")
    print(f"[OK] Updated paper/main.tex with data as of {snap['date_display']}")


def main() -> None:
    snap = _load_snapshot()
    print(f"Market snapshot as of {snap['date_display']}:")
    print(f"  Zhipu:  HK${snap['price_hkd_fmt']}  ({snap['ret_vs_ipo_fmt']} vs IPO)")
    print(f"  MiniMax: HK${snap['minimax_price']:.1f}  ({snap['minimax_ret']:+.0f}%)")
    print(f"  Wenge:   HK${snap['wenge_price']:.1f}  ({snap['wenge_ret']:+.0f}%)")
    print(f"  Equity:  {snap['equity_value_fmt']}")
    print(f"  EV/Rev:  {snap['revenue_multiple_fmt']}x")
    print(f"  DCF gap: {snap['dcf_gap_fmt']}")
    print(f"  Vol:     ~{snap['ann_vol_fmt']}%")
    if snap["rev_req_usd_bn"]:
        print(f"  Rev req: US${snap['rev_req_usd_bn']:.0f}bn ({snap['cagr_fmt']} CAGR)")
    print()

    update_readme(snap)
    update_data_tables(snap)
    update_paper_tex(snap)

    print("\n[DONE] All docs updated. Review changes before committing.")


if __name__ == "__main__":
    main()
