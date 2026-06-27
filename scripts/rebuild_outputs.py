from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
EVENTSTUDY = ROOT / "eventstudy"
MODEL = ROOT / "model" / "valuation_model.xlsx"


WACC = 0.135
TERMINAL_G = 0.04
TAX_RATE = 0.15
SHARES_M = 435
USD_HKD = 7.8
NET_CASH_USDM = 550
MARKET_PRICE_HKD = 2046
REV_2025_USDM = 102
REV_2026_USDM = 200


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    growth_start_2027: float
    growth_end_2035: float
    terminal_margin: float
    sales_to_capital: float


SCENARIOS = [
    Scenario("Bear", 0.35, 0.40, 0.06, 0.18, 2.0),
    Scenario("Base", 0.45, 0.56, 0.08, 0.28, 1.8),
    Scenario("Bull", 0.20, 0.85, 0.12, 0.35, 1.6),
]


def project_scenario(
    scenario: Scenario,
    *,
    wacc: float = WACC,
    terminal_margin: float | None = None,
    growth_start_2027: float | None = None,
) -> dict:
    terminal_margin = scenario.terminal_margin if terminal_margin is None else terminal_margin
    growth_start_2027 = (
        scenario.growth_start_2027 if growth_start_2027 is None else growth_start_2027
    )

    rows = []
    revenue = REV_2026_USDM
    previous_revenue = REV_2025_USDM
    nol = 0.0
    for i, year in enumerate(range(2026, 2036)):
        if year == 2026:
            growth = REV_2026_USDM / REV_2025_USDM - 1
        else:
            growth = growth_start_2027 + (scenario.growth_end_2035 - growth_start_2027) * (i - 1) / 8
            revenue = previous_revenue * (1 + growth)

        ebit_margin = -0.30 + (terminal_margin + 0.30) * i / 9
        ebit = revenue * ebit_margin
        beginning_nol = nol
        if ebit < 0:
            cash_tax = 0.0
            nol = beginning_nol - ebit
        else:
            nol_used = min(beginning_nol, ebit)
            taxable_income = ebit - nol_used
            cash_tax = taxable_income * TAX_RATE
            nol = beginning_nol - nol_used

        nopat = ebit - cash_tax
        reinvestment = max(revenue - previous_revenue, 0) / scenario.sales_to_capital
        fcff = nopat - reinvestment
        discount_factor = 1 / (1 + wacc) ** (i + 1)
        rows.append(
            {
                "year": year,
                "revenue": revenue,
                "growth_pct": growth * 100,
                "ebit_margin_pct": ebit_margin * 100,
                "ebit": ebit,
                "cash_tax": cash_tax,
                "nol_end": nol,
                "nopat": nopat,
                "reinvest": reinvestment,
                "fcff": fcff,
                "discount_factor": discount_factor,
                "pv_fcff": fcff * discount_factor,
            }
        )
        previous_revenue = revenue

    terminal_value = rows[-1]["fcff"] * (1 + TERMINAL_G) / (wacc - TERMINAL_G)
    pv_terminal = terminal_value * rows[-1]["discount_factor"]
    enterprise_value = sum(row["pv_fcff"] for row in rows) + pv_terminal
    equity_value = enterprise_value + NET_CASH_USDM
    per_share_hkd = equity_value / SHARES_M * USD_HKD

    return {
        "rows": rows,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share_hkd": per_share_hkd,
        "wacc": wacc,
        "terminal_margin": terminal_margin,
        "growth_start_2027": growth_start_2027,
    }


def write_base_projection_csv() -> None:
    base = project_scenario(SCENARIOS[1])["rows"]
    out = pd.DataFrame(base)[
        ["year", "revenue", "growth_pct", "ebit_margin_pct", "cash_tax", "nol_end", "nopat", "reinvest", "fcff"]
    ]
    for col in out.columns:
        if col != "year":
            out[col] = out[col].round(1)
    out.to_csv(EVENTSTUDY / "base_projection.csv", index=False)


def write_workbook() -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Assumptions"
    assumptions = [
        ("GLOBAL ASSUMPTIONS", None, None),
        ("WACC", WACC, None),
        ("Terminal growth g", TERMINAL_G, None),
        ("Tax rate", TAX_RATE, None),
        ("Shares outstanding (m)", SHARES_M, None),
        ("USD/HKD", USD_HKD, None),
        (
            "Net cash (US$m)",
            NET_CASH_USDM,
            "net IPO proceeds plus pre-IPO cash; preferred shares convert at IPO",
        ),
        ("Market price (HK$)", MARKET_PRICE_HKD, None),
        ("2025 revenue (US$m)", REV_2025_USDM, None),
        ("2026E revenue (US$m)", REV_2026_USDM, None),
    ]
    for row in assumptions:
        ws.append(row)
    ws["A1"].font = Font(bold=True)

    for scenario in SCENARIOS:
        ws = wb.create_sheet(scenario.name)
        ws.append([f"DCF - {scenario.name} scenario"])
        ws.append(["growth start (2027)", scenario.growth_start_2027])
        ws.append(["growth end (2035)", scenario.growth_end_2035])
        ws.append(["start op margin", -0.30])
        ws.append(["terminal op margin", scenario.terminal_margin])
        ws.append(["sales-to-capital", scenario.sales_to_capital])
        ws.append([])
        headers = [
            "Year",
            "i",
            "growth",
            "revenue",
            "op margin",
            "EBIT",
            "cash tax",
            "NOL end",
            "NOPAT",
            "dRev",
            "reinvest",
            "FCFF",
            "disc",
            "PV",
        ]
        ws.append(headers)
        for i, year in enumerate(range(2026, 2036), start=0):
            r = 9 + i
            prev_r = r - 1
            if year == 2026:
                growth_formula = "=Assumptions!$B$10/Assumptions!$B$9-1"
                revenue_formula = "=Assumptions!$B$10"
                drev_formula = "=D9-Assumptions!$B$9"
                prior_nol = "0"
            else:
                growth_formula = f"=$B$2+($B$3-$B$2)*(B{r}-1)/8"
                revenue_formula = f"=D{prev_r}*(1+C{r})"
                drev_formula = f"=D{r}-D{prev_r}"
                prior_nol = f"H{prev_r}"
            ws.append(
                [
                    year,
                    i,
                    growth_formula,
                    revenue_formula,
                    f"=$B$4+($B$5-$B$4)*B{r}/9",
                    f"=D{r}*E{r}",
                    f"=IF(F{r}<0,0,MAX(F{r}-{prior_nol},0)*Assumptions!$B$4)",
                    f"=IF(F{r}<0,{prior_nol}-F{r},MAX({prior_nol}-F{r},0))",
                    f"=F{r}-G{r}",
                    drev_formula,
                    f"=MAX(J{r},0)/$B$6",
                    f"=I{r}-K{r}",
                    f"=1/(1+Assumptions!$B$2)^(B{r}+1)",
                    f"=L{r}*M{r}",
                ]
            )

        ws.append([])
        ws.append(["Sum PV (explicit)", "=SUM(N9:N18)"])
        ws.append(["Terminal value", "=L18*(1+Assumptions!$B$3)/(Assumptions!$B$2-Assumptions!$B$3)"])
        ws.append(["PV terminal", "=B21*M18"])
        ws.append(["Enterprise value", "=B20+B22"])
        ws.append(["Equity value (US$m)", "=B23+Assumptions!$B$7"])
        ws.append(["Per share (US$)", "=B24/Assumptions!$B$5"])
        ws.append(["Per share (HK$)", "=B25*Assumptions!$B$6"])

        for cell in ws[8]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill("solid", fgColor="D9EAF7")

    ws = wb.create_sheet("Summary")
    ws.append(["VALUATION SUMMARY"])
    ws.append(["Scenario", "Prob", "Equity (US$m)", "Per share (HK$)"])
    for i, scenario in enumerate(SCENARIOS, start=3):
        ws.append([scenario.name, scenario.probability, f"={scenario.name}!B24", f"={scenario.name}!B26"])
    ws.append(["PROB-WEIGHTED", None, "=SUMPRODUCT(B3:B5,C3:C5)/SUM(B3:B5)", "=SUMPRODUCT(B3:B5,D3:D5)/SUM(B3:B5)"])
    ws.append(["Market price (HK$)", "=Assumptions!B8"])
    ws.append(["DCF value as % of market", "=D6/B7"])
    ws.append(["Market equity value / revenue", "=(Assumptions!B8*Assumptions!B5/Assumptions!B6)/Assumptions!B10"])

    for sheet in wb.worksheets:
        for col in range(1, sheet.max_column + 1):
            sheet.column_dimensions[get_column_letter(col)].width = 16
        sheet.freeze_panes = "A2"

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.save(MODEL)


def per_share_for_base(**kwargs: float) -> float:
    return project_scenario(SCENARIOS[1], **kwargs)["per_share_hkd"]


def write_sensitivity_chart() -> None:
    base = per_share_for_base()
    cases = [
        ("WACC", per_share_for_base(wacc=0.15), per_share_for_base(wacc=0.12), "15% / 12%"),
        (
            "Terminal margin",
            per_share_for_base(terminal_margin=0.23),
            per_share_for_base(terminal_margin=0.33),
            "23% / 33%",
        ),
        (
            "2027 revenue growth",
            per_share_for_base(growth_start_2027=0.46),
            per_share_for_base(growth_start_2027=0.66),
            "46% / 66%",
        ),
    ]

    fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=150)
    y = np.arange(len(cases))
    for i, (label, low, high, range_label) in enumerate(cases):
        left = min(low, high)
        width = abs(high - low)
        ax.barh(i, width, left=left, height=0.45, color="#4C78A8")
        ax.plot([base, base], [i - 0.34, i + 0.34], color="#111111", linewidth=1.2)
        ax.text(max(low, high) + 1.0, i, f"{range_label}: HK${low:.0f}-{high:.0f}", va="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([case[0] for case in cases])
    ax.invert_yaxis()
    ax.set_xlabel("DCF value per share (HK$)")
    ax.set_title("Base-case DCF sensitivity")
    ax.axvline(base, color="#111111", linewidth=1, linestyle="--")
    ax.text(base + 0.35, -0.48, f"Base HK${base:.0f}", fontsize=8, va="center")
    ax.grid(axis="x", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig7_sensitivity.png", bbox_inches="tight")
    plt.close(fig)


def write_football_field() -> None:
    results = {s.name: project_scenario(s) for s in SCENARIOS}
    weighted = sum(s.probability * results[s.name]["per_share_hkd"] for s in SCENARIOS)
    rows = [
        ("Scenario DCF", results["Bear"]["per_share_hkd"], results["Bull"]["per_share_hkd"]),
        ("Valuation / revenue", 30 * REV_2026_USDM / SHARES_M * USD_HKD, 40 * REV_2026_USDM / SHARES_M * USD_HKD),
        ("Market", MARKET_PRICE_HKD, MARKET_PRICE_HKD),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 3.6), dpi=150)
    y = np.arange(len(rows))
    for i, (label, low, high) in enumerate(rows):
        ax.hlines(i, low, high, color="#4C78A8", linewidth=9)
        ax.text(low, i + 0.18, f"HK${low:.0f}", ha="center", fontsize=8)
        if high != low:
            ax.text(high, i + 0.18, f"HK${high:.0f}", ha="center", fontsize=8)
    ax.scatter([weighted], [0], marker="D", color="#F58518", zorder=3, label="Prob.-weighted DCF")
    comp_mid = 35 * REV_2026_USDM / SHARES_M * USD_HKD
    ax.scatter([comp_mid], [1], marker="D", color="#54A24B", zorder=3, label="Multiple midpoint")
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels([row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlabel("HK$ per share (log scale)")
    ax.set_title("Valuation football field")
    ax.grid(axis="x", which="both", alpha=0.25)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig5_football_field.png", bbox_inches="tight")
    plt.close(fig)


def write_comps_chart() -> None:
    names = ["MiniMax", "OpenAI / Anthropic", "Zhipu"]
    values = [35, 35, MARKET_PRICE_HKD * SHARES_M / USD_HKD / REV_2026_USDM]
    colors = ["#72B7B2", "#54A24B", "#E45756"]
    fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=150)
    ax.bar(names, values, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("Equity value / revenue (x, log scale)")
    ax.set_title("Revenue multiple comparison")
    for i, v in enumerate(values):
        ax.text(i, v * 1.12, f"{v:.0f}x", ha="center", fontsize=9)
    ax.grid(axis="y", which="both", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig6_ps_comps.png", bbox_inches="tight")
    plt.close(fig)


def event_car_series() -> dict[str, pd.Series]:
    prices = pd.read_csv(ROOT / "data" / "Zhipu_KnowledgeAtlas_daily.csv")
    prices["trade_date"] = pd.to_datetime(prices["trade_date"].astype(str))
    prices["ret"] = prices["close"].pct_change()
    events = {
        "GLM-5": "2026-02-11",
        "GLM-5-Turbo": "2026-03-16",
        "GLM-5.1": "2026-04-08",
        "GLM-5.2": "2026-06-15",
    }
    series = {}
    for name, date in events.items():
        idx = prices.index[prices["trade_date"] == pd.Timestamp(date)][0]
        expected = prices.loc[idx - 20 : idx - 6, "ret"].mean()
        rel_days = []
        ars = []
        for rel in range(-5, 11):
            loc = idx + rel
            if 0 <= loc < len(prices):
                rel_days.append(rel)
                ars.append((prices.loc[loc, "ret"] - expected) * 100)
        series[name] = pd.Series(ars, index=rel_days).cumsum()
    return series


def write_event_chart() -> None:
    series = event_car_series()
    full_days = [day for day in range(-5, 11) if all(day in s.index for s in series.values())]
    avg = pd.concat([s.loc[full_days] for s in series.values()], axis=1).mean(axis=1)
    fig, ax = plt.subplots(figsize=(8.5, 5.0), dpi=150)
    for name, s in series.items():
        ax.plot(s.index, s.values, alpha=0.55, linewidth=1.3, label=name)
    ax.plot(avg.index, avg.values, color="#111111", linewidth=2.5, label="Average (n=4)")
    ax.axvline(0, color="#555555", linestyle="--", linewidth=1)
    ax.axhline(0, color="#777777", linewidth=0.8)
    ax.set_xlim(-5, 10)
    ax.set_xlabel("Event day")
    ax.set_ylabel("CAR (%)")
    ax.set_title("Average CAR in event time")
    ax.text(8.1, ax.get_ylim()[0] + 2, "n falls after +8", fontsize=8)
    ax.legend(fontsize=8, ncol=2, loc="upper left")
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig3_car_eventtime.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    write_base_projection_csv()
    write_workbook()
    write_sensitivity_chart()
    write_football_field()
    write_comps_chart()
    write_event_chart()


if __name__ == "__main__":
    main()
