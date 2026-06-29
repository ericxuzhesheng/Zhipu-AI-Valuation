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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = ROOT / "data"
EVENTSTUDY = ROOT / "eventstudy"

# ---- shared colour palette ----
C_RED = "#B22222"
C_BLUE = "#1F4E79"
C_INK = "#222222"

# ============================================================
# PART 1 - Comparable-company beta bridge (CSV + LaTeX)
# ============================================================

# Comparable-company snapshot (last verified 2026-06-28).
# Update these values when refreshing the beta bridge.
COMPS = [
    {"Company": "Salesforce", "Ticker": "CRM",  "Levered_beta": 1.151,
     "Mcap_USD": 129_705_025_536, "Total_debt_USD": 42_547_998_720},
    {"Company": "Palantir",   "Ticker": "PLTR", "Levered_beta": 1.515,
     "Mcap_USD": 270_728_445_952, "Total_debt_USD": 211_976_992},
    {"Company": "Snowflake",  "Ticker": "SNOW", "Levered_beta": 1.355,
     "Mcap_USD": 86_289_539_072,  "Total_debt_USD": 2_772_094_976},
    {"Company": "Datadog",    "Ticker": "DDOG", "Levered_beta": 1.553,
     "Mcap_USD": 85_348_573_184,  "Total_debt_USD": 1_285_052_032},
    {"Company": "MongoDB",    "Ticker": "MDB",  "Levered_beta": 1.553,
     "Mcap_USD": 25_256_429_568,  "Total_debt_USD": 58_635_000},
    {"Company": "Cloudflare", "Ticker": "NET",  "Levered_beta": 1.674,
     "Mcap_USD": 84_205_862_912,  "Total_debt_USD": 3_524_536_064},
    {"Company": "C3.ai",      "Ticker": "AI",   "Levered_beta": 2.033,
     "Mcap_USD": 1_383_498_496,   "Total_debt_USD": 58_681_000},
]

TAX_RATE_BETA = 0.21


def build_beta_bridge() -> pd.DataFrame:
    """Compute debt/equity and unlevered beta from the snapshot."""
    rows = []
    for c in COMPS:
        mcap = c["Mcap_USD"]
        debt = c["Total_debt_USD"]
        de = debt / mcap if mcap > 0 else float("nan")
        bu = c["Levered_beta"] / (1 + (1 - TAX_RATE_BETA) * de)
        rows.append({**c, "Debt_Equity": de, "Unlevered_beta": bu})
    df = pd.DataFrame(rows)
    median_bu = df["Unlevered_beta"].median()
    return df, median_bu


def write_beta_latex(df: pd.DataFrame, median_bu: float, path: Path) -> None:
    """Emit a LaTeX tabular ready for \\input{}."""
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
        f"\\caption{{Comparable-company beta bridge (accessed 28~June~2026).}}\n"
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
SHARES_M = 435
USD_HKD = 7.8
NET_CASH_USDM = 550
REV_2026_USDM = 200

# Grid
WACC_GRID = np.array([0.10, 0.115, 0.13, 0.135, 0.15, 0.17, 0.20])
MARGIN_GRID = np.array([0.20, 0.28, 0.35, 0.40, 0.50])

# Target equity value (market, 2026-06-26)
TARGET_EQUITY_USDM = 114_000
TARGET_EV_USDM = TARGET_EQUITY_USDM - NET_CASH_USDM


def growth_path(base_rev: float) -> list[float]:
    """Base-case revenue growth rates 2026-2035 (9 intervals)."""
    return [0.56, 0.50, 0.44, 0.38, 0.32, 0.26, 0.20, 0.14, 0.08]


def compute_required_2035_rev(wacc: float, term_margin: float) -> float:
    """Solve for 2035 revenue (US$m) that makes EV = TARGET_EV_USDM."""
    g_path = growth_path(1.0)
    revs = [1.0]
    for g in reversed(g_path):
        revs.insert(0, revs[0] / (1 + g))

    n = len(revs)
    margins = np.linspace(-0.30, term_margin, n)
    fcf_unit = []
    pv_unit = 0.0
    for i in range(n):
        rev_i = revs[i]
        ebit_i = rev_i * margins[i]
        tax_i = max(0, ebit_i * TAX)
        nopat_i = ebit_i - tax_i
        if i == 0:
            reinvest_i = rev_i / SALES_TO_CAP
        else:
            reinvest_i = (rev_i - revs[i - 1]) / SALES_TO_CAP
        fcff_i = nopat_i - reinvest_i
        pv_unit += fcff_i / (1 + wacc) ** (i + 1)
        fcf_unit.append(fcff_i)

    fcff_term = fcf_unit[-1]
    if wacc <= TERM_G:
        return float("inf")
    tv_unit = fcff_term * (1 + TERM_G) / (wacc - TERM_G)
    pv_tv_unit = tv_unit / (1 + wacc) ** n

    ev_per_unit = pv_unit + pv_tv_unit
    if ev_per_unit <= 0:
        return float("inf")

    return TARGET_EV_USDM / ev_per_unit


def build_sensitivity_grid() -> pd.DataFrame:
    """Build the WACC x margin grid of required 2035 revenue (US$bn)."""
    rows = []
    for w in WACC_GRID:
        for m in MARGIN_GRID:
            rev = compute_required_2035_rev(w, m)
            rows.append({"WACC": w, "Term_margin": m, "Req_rev_2035_USDm": rev})
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
        "Reverse-DCF sensitivity: 2035 revenue needed to justify US$114bn equity\n"
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

    base_rev = compute_required_2035_rev(WACC_BASE, 0.40)
    print(f"\n[Summary] Base case (WACC={WACC_BASE:.1%}, margin=40%): "
          f"required 2035 rev = US${base_rev / 1000:.0f}B")
    for w in [0.10, 0.15, 0.20]:
        r = compute_required_2035_rev(w, 0.40)
        print(f"  WACC={w:.0%}, margin=40%: US${r / 1000:.0f}B")
    for m in [0.28, 0.35, 0.50]:
        r = compute_required_2035_rev(WACC_BASE, m)
        print(f"  WACC={WACC_BASE:.1%}, margin={m:.0%}: US${r / 1000:.0f}B")


if __name__ == "__main__":
    main()
