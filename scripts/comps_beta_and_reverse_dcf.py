#!/usr/bin/env python3
"""Generate comparable-company beta bridge (CSV + LaTeX table) and
reverse-DCF sensitivity heatmap for the valuation appendix.

Usage:
    python scripts/comps_beta_and_reverse_dcf.py

Outputs:
    data/comps_beta_bridge.csv
    eventstudy/reverse_dcf_sensitivity.csv
    figures/fig11_reverse_dcf_heatmap.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = ROOT / "data"
EVENTSTUDY = ROOT / "eventstudy"
COMPS_INPUT = DATA / "comps_beta_bridge_input.csv"

# ---- shared colour palette ----
C_RED = "#B22222"
C_BLUE = "#1F4E79"
C_INK = "#222222"

# ============================================================
# PART 1 - Comparable-company beta bridge (CSV + LaTeX)
# ============================================================

TAX_RATE_BETA = 0.21


def build_beta_bridge() -> tuple[pd.DataFrame, float]:
    """Compute debt/equity and unlevered beta from the snapshot."""
    required = {"Company", "Ticker", "Levered_beta", "Mcap_USD", "Total_debt_USD"}
    df_input = pd.read_csv(COMPS_INPUT)
    missing = sorted(required.difference(df_input.columns))
    if missing:
        raise ValueError(f"{COMPS_INPUT} missing required columns: {', '.join(missing)}")

    rows = []
    for c in df_input.to_dict("records"):
        mcap = float(c["Mcap_USD"])
        debt = float(c["Total_debt_USD"])
        de = debt / mcap if mcap > 0 else float("nan")
        bu = float(c["Levered_beta"]) / (1 + (1 - TAX_RATE_BETA) * de)
        rows.append({**c, "Debt_Equity": de, "Unlevered_beta": bu})
    df = pd.DataFrame(rows)
    median_bu = df["Unlevered_beta"].median()
    return df, median_bu


def write_beta_latex(df: pd.DataFrame, median_bu: float, path: Path) -> None:
    """Emit a LaTeX tabular ready for \\input{}."""
    snapshot_dates = sorted({str(d) for d in df.get("Snapshot_date", []) if pd.notna(d)})
    snapshot = snapshot_dates[-1] if snapshot_dates else "2026-08-31"
    if snapshot_dates:
        snapshot_day = pd.Timestamp(snapshot)
        snapshot_tex = f"{snapshot_day.day}~{snapshot_day.strftime('%B')}~{snapshot_day.year}"
    else:
        snapshot_tex = snapshot
    rows_tex = []
    for _, r in df.iterrows():
        de_pct = f"{r['Debt_Equity'] * 100:.1f}\\%" if r["Debt_Equity"] == r["Debt_Equity"] else "n/a"
        rows_tex.append(
            f"{r['Company']} & {r['Levered_beta']:.2f} & {de_pct} & "
            f"{r['Unlevered_beta']:.2f} \\\\"
        )
    body = "\n".join(rows_tex)
    tex = (
        "\\begin{table}[H]\n"
        "\\centering\n"
        f"\\caption{{Comparable-company beta bridge (60-month beta window ended {snapshot_tex}).}}\n"
        "\\label{tab:beta}\n"
        "\\begin{tabular}{lccc}\n"
        "\\toprule\n"
        "Comparable & Levered beta & Debt/equity & Unlevered beta \\\\\n"
        "\\midrule\n"
        f"{body}\n"
        "\\midrule\n"
        "\\textbf{Median} & --- & --- & "
        f"\\textbf{{{median_bu:.2f}}} \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )
    path.write_text(tex, encoding="utf-8")
    print(f"[OK] LaTeX table -> {path}")


# ============================================================
# PART 2 - Reverse-DCF sensitivity (required 2035 revenue grid)
# ============================================================

# Fixed assumptions
WACC_BASE = 0.135
TERM_G = 0.04
TAX = 0.15
SALES_TO_CAP = 1.8
SHARES_M = 465.62309
USD_HKD = 7.8
USD_CNY = 7.1
NET_CASH_USDM = (
    3993.722 + 506.139 - 2224.789 - 379.410
) / USD_CNY + 31374.95 / USD_HKD
REV_2025_USDM = 102
REV_2026_USDM = 700
START_OP_MARGIN = -1.00
GROWTH_END_2035 = 0.08

# Grid
WACC_GRID = np.array([0.10, 0.115, 0.13, 0.135, 0.15, 0.17, 0.20])
MARGIN_GRID = np.array([0.20, 0.28, 0.35, 0.40, 0.50])

def target_equity_usdm() -> float:
    """Derive target market equity from the latest local Zhipu price file."""
    prices = pd.read_csv(DATA / "Zhipu_KnowledgeAtlas_daily.csv")
    prices["date"] = pd.to_datetime(prices["trade_date"].astype(str))
    latest = prices.sort_values("date").iloc[-1]
    return float(latest["close"]) * SHARES_M / USD_HKD


TARGET_EQUITY_USDM = target_equity_usdm()
TARGET_EV_USDM = TARGET_EQUITY_USDM - NET_CASH_USDM


def enterprise_value_for_growth_start(
    wacc: float,
    term_margin: float,
    growth_start_2027: float,
) -> tuple[float, float]:
    """Return enterprise value and 2035 revenue with FY2026E fixed at the model base."""
    revenue = REV_2026_USDM
    previous_revenue = REV_2025_USDM
    nol = 0.0
    rows: list[tuple[float, float]] = []

    for i, year in enumerate(range(2026, 2036)):
        if year > 2026:
            growth = growth_start_2027 + (GROWTH_END_2035 - growth_start_2027) * (i - 1) / 8
            revenue = previous_revenue * (1 + growth)
        margin = START_OP_MARGIN + (term_margin - START_OP_MARGIN) * i / 9
        ebit = revenue * margin
        beginning_nol = nol
        if ebit < 0:
            cash_tax = 0.0
            nol = beginning_nol - ebit
        else:
            nol_used = min(beginning_nol, ebit)
            cash_tax = (ebit - nol_used) * TAX
            nol = beginning_nol - nol_used
        nopat = ebit - cash_tax
        reinvestment = max(revenue - previous_revenue, 0) / SALES_TO_CAP
        fcff = nopat - reinvestment
        discount_factor = 1 / (1 + wacc) ** (i + 1)
        rows.append((fcff, discount_factor))
        previous_revenue = revenue

    if wacc <= TERM_G:
        return float("inf"), revenue
    terminal_value = rows[-1][0] * (1 + TERM_G) / (wacc - TERM_G)
    enterprise_value = sum(fcff * df for fcff, df in rows) + terminal_value * rows[-1][1]
    return enterprise_value, revenue


def solve_required_path(wacc: float, term_margin: float) -> tuple[float, float]:
    """Solve the 2027 growth rate and 2035 revenue that match observed enterprise value."""
    low = -0.50
    high = 1.00
    high_value, _ = enterprise_value_for_growth_start(wacc, term_margin, high)
    while high_value < TARGET_EV_USDM and high < 10:
        high = high * 1.5 + 0.10
        high_value, _ = enterprise_value_for_growth_start(wacc, term_margin, high)
    if high_value < TARGET_EV_USDM:
        return float("inf"), float("inf")

    for _ in range(160):
        mid = (low + high) / 2
        mid_value, _ = enterprise_value_for_growth_start(wacc, term_margin, mid)
        if mid_value < TARGET_EV_USDM:
            low = mid
        else:
            high = mid

    required_growth = (low + high) / 2
    _, required_revenue = enterprise_value_for_growth_start(wacc, term_margin, required_growth)
    return required_growth, required_revenue


def compute_required_2035_rev(wacc: float, term_margin: float) -> float:
    """Return required 2035 revenue (US$m), anchored to the FY2026E revenue assumption."""
    return solve_required_path(wacc, term_margin)[1]


def build_sensitivity_grid() -> pd.DataFrame:
    """Build the WACC x margin grid of required 2035 revenue (US$bn)."""
    rows = []
    for w in WACC_GRID:
        for m in MARGIN_GRID:
            growth_start, rev = solve_required_path(w, m)
            rows.append(
                {
                    "WACC": w,
                    "Term_margin": m,
                    "Required_2027_growth": growth_start,
                    "Req_rev_2035_USDm": rev,
                    "Required_CAGR_2026_2035": (rev / REV_2026_USDM) ** (1 / 9) - 1,
                }
            )
    df = pd.DataFrame(rows)
    df["Req_rev_2035_USDbn"] = df["Req_rev_2035_USDm"] / 1000
    return df


def plot_sensitivity_heatmap(df: pd.DataFrame, path: Path) -> None:
    """Heatmap: WACC (y) x terminal margin (x), colour = required 2035 rev."""
    pivot = df.pivot(index="WACC", columns="Term_margin", values="Req_rev_2035_USDbn")
    pivot = pivot.sort_index(ascending=True)

    data = pivot.values.astype(float)
    data_capped = np.clip(data, 0, 500)

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(data_capped, cmap="YlOrRd", aspect="auto",
                   origin="lower", interpolation="nearest")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"{c:.0%}" for c in pivot.columns], fontsize=10)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f"{r:.1%}" for r in pivot.index], fontsize=10)
    ax.set_xlabel("Terminal operating margin", fontsize=11)
    ax.set_ylabel("WACC", fontsize=11)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = data[i, j]
            label = f"${val:.0f}B" if val < 1e6 else ">$1T"
            colour = "white" if val > 250 else C_INK
            ax.text(j, i, label, ha="center", va="center",
                    fontsize=9, fontweight="bold", color=colour)

    base_i = list(pivot.index).index(0.135) if 0.135 in pivot.index else None
    base_j = list(pivot.columns).index(0.40) if 0.40 in pivot.columns else None
    if base_i is not None and base_j is not None:
        ax.add_patch(plt.Rectangle((base_j - 0.5, base_i - 0.5), 1, 1,
                                   fill=False, edgecolor=C_RED, linewidth=2.5))

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Required 2035 revenue (US$bn)", fontsize=10)

    ax.set_title(
        f"Reverse-DCF sensitivity: 2035 revenue needed to justify US${TARGET_EQUITY_USDM / 1000:.0f}bn equity\n"
        "(red box = base-case WACC 13.5% / terminal margin 40%)",
        fontsize=12, fontweight="bold", pad=12,
    )
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Heatmap -> {path}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    DATA.mkdir(exist_ok=True)
    EVENTSTUDY.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)

    # ---- Part 1: Beta bridge ----
    print("[1/3] Building comparable-company beta bridge ...")
    df_beta, median_bu = build_beta_bridge()
    csv_beta = DATA / "comps_beta_bridge.csv"
    df_beta.to_csv(csv_beta, index=False)
    print(f"[OK] CSV -> {csv_beta}")
    tex_beta = ROOT / "paper" / "beta_bridge_auto.tex"
    write_beta_latex(df_beta, median_bu, tex_beta)

    # ---- Part 2: Reverse-DCF sensitivity ----
    print("[2/3] Computing sensitivity grid ...")
    df_sens = build_sensitivity_grid()
    csv_sens = EVENTSTUDY / "reverse_dcf_sensitivity.csv"
    df_sens.to_csv(csv_sens, index=False)
    print(f"[OK] CSV -> {csv_sens}")

    print("[3/3] Plotting sensitivity heatmap ...")
    fig_path = FIGURES / "fig11_reverse_dcf_heatmap.png"
    plot_sensitivity_heatmap(df_sens, fig_path)

    base_growth, base_rev = solve_required_path(WACC_BASE, 0.40)
    print(f"\n[Summary] Base case (WACC={WACC_BASE:.1%}, margin=40%): "
          f"required 2027 growth = {base_growth:.1%}; 2035 rev = US${base_rev / 1000:.0f}B")
    for w in [0.10, 0.15, 0.20]:
        r = compute_required_2035_rev(w, 0.40)
        print(f"  WACC={w:.0%}, margin=40%: US${r / 1000:.0f}B")
    for m in [0.28, 0.35, 0.50]:
        r = compute_required_2035_rev(WACC_BASE, m)
        print(f"  WACC={WACC_BASE:.1%}, margin={m:.0%}: US${r / 1000:.0f}B")


if __name__ == "__main__":
    main()
