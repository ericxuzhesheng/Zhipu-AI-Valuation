from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
PAPER_PDF = PAPER_DIR / "main.pdf"
SUBMISSION_GLOB = "42353012_*.pdf"


def run_step(label: str, command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"[RUN] {label}", flush=True)
    proc = subprocess.run(command, cwd=cwd, text=True)
    if proc.returncode != 0:
        joined = " ".join(command)
        raise SystemExit(f"[FAIL] {label}: {joined} exited with {proc.returncode}")


def submission_pdf_path() -> Path:
    matches = sorted(ROOT.glob(SUBMISSION_GLOB))
    if len(matches) != 1:
        found = ", ".join(path.name for path in matches) or "none"
        raise SystemExit(
            f"[FAIL] expected exactly one root-level {SUBMISSION_GLOB} file; found {found}"
        )
    return matches[0]


def copy_submission_pdf() -> None:
    if not PAPER_PDF.exists():
        raise SystemExit(f"[FAIL] cannot copy missing PDF: {PAPER_PDF}")
    target = submission_pdf_path()
    shutil.copy2(PAPER_PDF, target)
    print(f"[OK] copied {PAPER_PDF.relative_to(ROOT)} -> {target.name}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate outputs, compile the paper PDF twice, copy the submission PDF, and validate."
    )
    parser.add_argument(
        "--skip-tex",
        action="store_true",
        help="Regenerate data/model outputs and run validation without recompiling LaTeX.",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip scripts/validate_outputs.py after the build.",
    )
    args = parser.parse_args()

    run_step("rebuild generated outputs", [sys.executable, "scripts/rebuild_outputs.py"])
    run_step("refresh beta bridge and reverse DCF", [sys.executable, "scripts/comps_beta_and_reverse_dcf.py"])

    if not args.skip_tex:
        if shutil.which("xelatex") is None:
            raise SystemExit("[FAIL] xelatex not found on PATH; install TeX Live or use --skip-tex")
        for pass_no in (1, 2):
            run_step(
                f"compile paper PDF pass {pass_no}",
                ["xelatex", "-interaction=nonstopmode", "main.tex"],
                cwd=PAPER_DIR,
            )
        copy_submission_pdf()

    if not args.skip_validate:
        run_step("validate outputs", [sys.executable, "scripts/validate_outputs.py"])

    print("[OK] build complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
