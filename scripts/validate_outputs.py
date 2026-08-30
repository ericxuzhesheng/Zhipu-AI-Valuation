from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

import openpyxl
import pandas as pd
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "main.tex"
SUBMISSION_GLOB = "42353012_*.pdf"


def fail(message: str) -> None:
    raise AssertionError(message)


def submission_pdf_path() -> Path:
    matches = sorted(ROOT.glob(SUBMISSION_GLOB))
    if len(matches) != 1:
        found = ", ".join(path.name for path in matches) or "none"
        fail(f"expected exactly one root-level {SUBMISSION_GLOB} file; found {found}")
    return matches[0]


def texcount_words() -> int:
    proc = subprocess.run(
        ["texcount", "-inc", "-sum", "main.tex"],
        cwd=ROOT / "paper",
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"texcount failed: {proc.stderr.strip() or proc.stdout.strip()}")
    match = re.search(r"Words in text:\s+(\d+)", proc.stdout)
    if not match:
        fail("texcount output did not include 'Words in text'")
    return int(match.group(1))


def abstract_words() -> int:
    text = PAPER.read_text(encoding="utf-8")
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    if not match:
        fail("abstract environment not found")
    abstract = match.group(1)
    abstract = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r" \1 ", abstract)
    abstract = re.sub(r"\$[^$]*\$", " ", abstract)
    abstract = re.sub(r"[^A-Za-z0-9'-]+", " ", abstract)
    return len([word for word in abstract.split() if re.search(r"[A-Za-z0-9]", word)])


def check_price_summary_dates() -> None:
    summary = pd.read_csv(ROOT / "data" / "price_summary.csv")
    specs = {
        "02513.HK": ROOT / "data" / "Zhipu_KnowledgeAtlas_daily.csv",
        "00100.HK": ROOT / "data" / "MiniMax_daily.csv",
        "01956.HK": ROOT / "data" / "WengeAI_daily.csv",
    }
    for code, path in specs.items():
        raw = pd.read_csv(path)
        expected = int(raw["trade_date"].max())
        actual_rows = summary.loc[summary["code"] == code, "latest_date"]
        if actual_rows.empty:
            fail(f"price_summary.csv missing {code}")
        actual = int(actual_rows.iloc[0])
        if actual != expected:
            fail(f"{code} latest_date mismatch: summary {actual}, raw {expected}")


def check_valuation_summary() -> None:
    csv_path = ROOT / "eventstudy" / "valuation_summary.csv"
    if not csv_path.exists():
        fail("eventstudy/valuation_summary.csv missing")
    with csv_path.open(newline="", encoding="utf-8") as f:
        csv_rows = {row["metric"]: row["value"] for row in csv.DictReader(f)}
    wb = openpyxl.load_workbook(ROOT / "model" / "valuation_model.xlsx", data_only=False, read_only=True)
    if "Audit Summary" not in wb.sheetnames:
        fail("model workbook missing Audit Summary sheet")
    sheet_rows = {
        str(metric): str(value)
        for metric, value in wb["Audit Summary"].iter_rows(min_row=1, max_col=2, values_only=True)
        if metric is not None
    }
    for metric, value in csv_rows.items():
        if metric not in sheet_rows:
            fail(f"Audit Summary missing metric {metric}")
        sheet_value = sheet_rows[metric]
        if value != sheet_value:
            try:
                if abs(float(value) - float(sheet_value)) <= 1e-9:
                    continue
            except ValueError:
                pass
            fail(f"valuation_summary mismatch for {metric}: csv {value}, workbook {sheet_value}")


def check_valuation_comps() -> None:
    input_path = ROOT / "data" / "valuation_comps_input.csv"
    output_path = ROOT / "data" / "valuation_comps.csv"
    for path in [input_path, output_path]:
        if not path.exists():
            fail(f"valuation comps file missing: {path}")
        if path.stat().st_size <= 0:
            fail(f"valuation comps file is empty: {path}")

    inputs = pd.read_csv(input_path, keep_default_na=False)
    comps = pd.read_csv(output_path, keep_default_na=False)
    required_input_columns = {
        "company",
        "ticker",
        "cohort",
        "valuation_date",
        "valuation_basis",
        "equity_value_bn",
        "revenue_bn",
        "currency",
        "revenue_basis",
        "include_in_private_range",
        "valuation_source_url",
        "revenue_source_url",
        "comparability_note",
    }
    missing_input = required_input_columns - set(inputs.columns)
    if missing_input:
        fail(f"valuation comps input missing columns: {sorted(missing_input)}")
    missing_output = required_input_columns.union({"multiple_x"}) - set(comps.columns)
    if missing_output:
        fail(f"valuation comps output missing columns: {sorted(missing_output)}")
    if "multiple_x" in inputs.columns:
        fail("valuation comps input must not hard-code multiple_x")
    if len(inputs) < 10 or len(comps) < 10:
        fail(f"valuation comps has too few rows: input {len(inputs)}, output {len(comps)}")
    if len(inputs) != len(comps):
        fail(f"valuation comps row-count mismatch: input {len(inputs)}, output {len(comps)}")

    required_companies = {
        "Zhipu",
        "MiniMax",
        "OpenAI",
        "Anthropic",
        "Mistral",
        "SenseTime",
        "Phancy",
        "Wenge AI",
        "Palantir",
        "Snowflake",
        "Cloudflare",
    }
    input_companies = set(inputs["company"].astype(str).str.strip())
    companies = set(comps["company"].astype(str).str.strip())
    if companies != input_companies:
        fail("valuation comps output company set does not match its input")
    missing_companies = required_companies - companies
    if missing_companies:
        fail(f"valuation comps missing companies: {sorted(missing_companies)}")
    if comps["company"].astype(str).str.strip().duplicated().any():
        fail("valuation comps contains duplicate company names")

    for column in ["equity_value_bn", "revenue_bn", "multiple_x", "include_in_private_range"]:
        comps[column] = pd.to_numeric(comps[column], errors="coerce")
        if comps[column].isna().any():
            fail(f"valuation comps has non-numeric {column}")
    if (comps[["equity_value_bn", "revenue_bn", "multiple_x"]] <= 0).any().any():
        fail("valuation comps equity value, revenue, and multiple must be positive")

    expected_multiples = comps["equity_value_bn"] / comps["revenue_bn"]
    multiple_error = (comps["multiple_x"] - expected_multiples).abs()
    if (multiple_error > 0.051).any():
        company = comps.loc[multiple_error.idxmax(), "company"]
        fail(f"valuation comps multiple_x is not equity_value_bn / revenue_bn for {company}")

    include_values = set(comps["include_in_private_range"])
    if not include_values.issubset({0, 1}):
        fail("include_in_private_range must contain only 0 or 1")
    included = set(
        comps.loc[comps["include_in_private_range"] == 1, "company"].astype(str).str.strip()
    )
    expected_included = {"OpenAI", "Anthropic", "Mistral"}
    if included != expected_included:
        fail(
            "private valuation range must include exactly OpenAI, Anthropic, and Mistral; "
            f"found {sorted(included)}"
        )
    secondary_included = comps.loc[
        (comps["cohort"] != "core_frontier") & (comps["include_in_private_range"] == 1),
        "company",
    ]
    if not secondary_included.empty:
        fail(
            "secondary valuation cohorts must not enter the private range: "
            f"{sorted(secondary_included.astype(str))}"
        )
    private_multiples = comps.loc[comps["include_in_private_range"] == 1, "multiple_x"]
    expected_stats = {"min": 20.5, "median": 34.1, "max": 39.0}
    actual_stats = {
        "min": float(private_multiples.min()),
        "median": float(private_multiples.median()),
        "max": float(private_multiples.max()),
    }
    for statistic, expected in expected_stats.items():
        if abs(actual_stats[statistic] - expected) > 0.15:
            fail(
                f"private valuation range {statistic} mismatch: "
                f"expected about {expected}, found {actual_stats[statistic]:.1f}"
            )

    minimax = comps.loc[comps["company"] == "MiniMax", "multiple_x"]
    if len(minimax) != 1 or abs(float(minimax.iloc[0]) - 81.4) > 0.15:
        fail("MiniMax valuation multiple should be about 81.4x")

    with (ROOT / "eventstudy" / "valuation_summary.csv").open(newline="", encoding="utf-8") as f:
        valuation_summary = {row["metric"]: row["value"] for row in csv.DictReader(f)}
    summary_metric = next(
        (
            metric
            for metric in [
                "Market equity value / FY2026E revenue",
                "Market EV / FY2026E revenue",
            ]
            if metric in valuation_summary
        ),
        None,
    )
    if summary_metric is None:
        fail("valuation_summary.csv missing market equity value / FY2026E revenue metric")
    zhipu = comps.loc[comps["company"] == "Zhipu", "multiple_x"]
    if len(zhipu) != 1:
        fail("valuation comps must contain exactly one Zhipu row")
    if abs(float(zhipu.iloc[0]) - float(valuation_summary[summary_metric])) > 0.051:
        fail("Zhipu valuation comp does not match valuation_summary market multiple")

    for table_name, table in [("input", inputs), ("output", comps)]:
        for column in ["valuation_source_url", "revenue_source_url"]:
            blank = table[column].astype(str).str.strip().eq("")
            if blank.any():
                company = table.loc[blank, "company"].iloc[0]
                fail(f"valuation comps {table_name} {column} is blank for {company}")


def check_pdfs() -> None:
    for path in [ROOT / "paper" / "main.pdf", submission_pdf_path()]:
        if not path.exists():
            fail(f"PDF missing: {path}")
        if path.stat().st_size < 100_000:
            fail(f"PDF too small: {path}")
        pages = len(PdfReader(path).pages)
        if pages <= 0:
            fail(f"PDF has no pages: {path}")


def check_event_panel() -> None:
    panel = ROOT / "eventstudy" / "event_panel.csv"
    catalog = ROOT / "eventstudy" / "event_catalog.csv"
    summary = ROOT / "eventstudy" / "event_panel_summary.csv"
    input_catalog = ROOT / "data" / "event_catalog_input.csv"
    for path in [input_catalog, panel, catalog, summary]:
        if not path.exists():
            fail(f"event-study output missing: {path}")
    panel_rows = pd.read_csv(panel)
    if len(panel_rows) < 9:
        fail(f"event panel has too few computable events: {len(panel_rows)}")
    catalog_rows = pd.read_csv(catalog)
    input_rows = pd.read_csv(input_catalog, keep_default_na=False)
    if len(catalog_rows) < len(panel_rows):
        fail("event catalog should include all panel rows and excluded candidates")
    if len(catalog_rows) != len(input_rows):
        fail(f"event catalog row count {len(catalog_rows)} does not match input {len(input_rows)}")


def check_appendix_outputs() -> None:
    required = [
        ROOT / "data" / "comps_beta_bridge_input.csv",
        ROOT / "data" / "comps_beta_bridge.csv",
        ROOT / "paper" / "beta_bridge_auto.tex",
        ROOT / "eventstudy" / "reverse_dcf_sensitivity.csv",
        ROOT / "figures" / "fig11_reverse_dcf_heatmap.png",
    ]
    for path in required:
        if not path.exists():
            fail(f"appendix output missing: {path}")
        if path.stat().st_size <= 0:
            fail(f"appendix output is empty: {path}")
    beta = pd.read_csv(ROOT / "data" / "comps_beta_bridge.csv")
    if len(beta) < 5:
        fail(f"comps beta bridge has too few rows: {len(beta)}")
    reverse = pd.read_csv(ROOT / "eventstudy" / "reverse_dcf_sensitivity.csv")
    if len(reverse) < 20:
        fail(f"reverse DCF grid has too few rows: {len(reverse)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated project outputs.")
    parser.add_argument(
        "--skip-tex-checks",
        action="store_true",
        help="Skip checks that require TeX tooling or freshly compiled PDFs.",
    )
    args = parser.parse_args()

    checks = [
        ("price_summary dates match raw data", check_price_summary_dates),
        ("valuation_summary matches Excel Audit Summary", check_valuation_summary),
        ("valuation comps are complete and auditable", check_valuation_comps),
        ("event panel outputs exist", check_event_panel),
        ("appendix outputs exist", check_appendix_outputs),
    ]
    if not args.skip_tex_checks:
        checks = [
            ("texcount text words <= 3000", lambda: texcount_words() <= 3000),
            ("abstract words < 400", lambda: abstract_words() < 400),
            ("PDF files exist and have pages", check_pdfs),
            *checks,
        ]
    for label, check in checks:
        result = check()
        if result is False:
            fail(label)
        print(f"OK: {label}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
