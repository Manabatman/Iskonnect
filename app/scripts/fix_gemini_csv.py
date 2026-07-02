"""
Normalize Gemini scholarship CSV for hardened staging import.

Reads a raw Gemini export, applies contract/schema fixes, writes import-ready CSV.

Usage:
  python -m app.scripts.fix_gemini_csv --input data/scholarships_gemini_raw.csv \\
      --output data/scholarships_gemini_corrected.csv
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import schemas
from app.scripts.import_scholarships import load_csv_strict
from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS
from app.utils.import_validation import summarize_import_report, validate_import_row

EXPECTED_COLS = len(CANONICAL_IMPORT_COLUMNS)
LEVELS_IDX = CANONICAL_IMPORT_COLUMNS.index("eligible_levels")
REGIONS_IDX = CANONICAL_IMPORT_COLUMNS.index("eligible_regions")
CITIES_IDX = CANONICAL_IMPORT_COLUMNS.index("eligible_cities")
RESIDENCY_IDX = CANONICAL_IMPORT_COLUMNS.index("residency_required")
BOOKS_IDX = CANONICAL_IMPORT_COLUMNS.index("benefit_books")
PROVIDER_TYPE_IDX = CANONICAL_IMPORT_COLUMNS.index("provider_type")
ACADEMIC_YEAR_IDX = CANONICAL_IMPORT_COLUMNS.index("academic_year_target")
LEVELS_COL = "eligible_levels"
ACTIVE_IDX = CANONICAL_IMPORT_COLUMNS.index("is_active")
NOTES_IDX = CANONICAL_IMPORT_COLUMNS.index("research_notes")
PRIORITY_IDX = CANONICAL_IMPORT_COLUMNS.index("priority_groups")
SOURCE_URLS_IDX = CANONICAL_IMPORT_COLUMNS.index("source_urls")
TUITION_IDX = CANONICAL_IMPORT_COLUMNS.index("benefit_tuition")
ALLOWANCE_IDX = CANONICAL_IMPORT_COLUMNS.index("benefit_allowance_monthly")
TOTAL_IDX = CANONICAL_IMPORT_COLUMNS.index("benefit_total_value")
BOOL_COL_IDXS = [
    CANONICAL_IMPORT_COLUMNS.index(c)
    for c in (
        "residency_required",
        "benefit_tuition",
        "has_qualifying_exam",
        "has_interview",
        "has_essay_requirement",
        "has_return_service",
        "is_active",
    )
]

_JUNK_PREFIXES = ("</", "<user_query", "====================================================")


def _is_junk_row(row: list[str]) -> bool:
    if not row or not row[0].strip():
        return True
    title = row[0].strip()
    return any(title.startswith(p) for p in _JUNK_PREFIXES)


def _merge_overflow_columns(row: list[str]) -> list[str]:
    """Rejoin columns split by unquoted commas in trailing metadata fields."""
    if len(row) <= EXPECTED_COLS:
        return row
    merged = row[: EXPECTED_COLS - 1]
    merged.append(",".join(row[EXPECTED_COLS - 1 :]))
    return merged


def _fix_missing_eligible_cities(row: list[str]) -> list[str]:
    """
    Insert empty eligible_cities when residency follows regions directly.

    Pattern: College,,true -> College,,,true
    """
    if len(row) != EXPECTED_COLS - 1:
        return row
    regions = row[REGIONS_IDX] if len(row) > REGIONS_IDX else ""
    cities_slot = row[CITIES_IDX] if len(row) > CITIES_IDX else ""
    residency = row[RESIDENCY_IDX] if len(row) > RESIDENCY_IDX else ""
    if cities_slot in ("true", "false") and residency not in ("true", "false"):
        row = row[:CITIES_IDX] + [""] + row[CITIES_IDX:]
    return row


def _region_block_shifted(row: list[str]) -> bool:
    return (
        len(row) > RESIDENCY_IDX + 2
        and row[RESIDENCY_IDX] == ""
        and row[RESIDENCY_IDX + 1] in ("true", "false")
        and row[RESIDENCY_IDX + 2] in ("Private", "Public", "Public|Private")
    )


def _fix_region_left_shift(row: list[str]) -> list[str]:
    """
    Repair extra empty field in the region block (College,,,,false,Private,...).

    For 40+ column rows, drop the spurious empty residency cell.
    For exactly 39 columns, shift values locally without dropping the row tail.
    """
    if not _region_block_shifted(row):
        return row
    if len(row) == EXPECTED_COLS:
        row[RESIDENCY_IDX] = row[RESIDENCY_IDX + 1]
        row[RESIDENCY_IDX + 1] = row[RESIDENCY_IDX + 2]
        row[RESIDENCY_IDX + 2] = row[RESIDENCY_IDX + 3]
        row[RESIDENCY_IDX + 3] = row[RESIDENCY_IDX + 4]
        row[RESIDENCY_IDX + 4] = ""
        gwa_idx = CANONICAL_IMPORT_COLUMNS.index("min_gwa_normalized")
        age_idx = CANONICAL_IMPORT_COLUMNS.index("min_age")
        if row[gwa_idx] == "" and row[age_idx] and str(row[age_idx]).replace(".", "").isdigit():
            row[gwa_idx] = row[age_idx]
            row[age_idx] = ""
        return row
    if len(row) >= EXPECTED_COLS:
        del row[RESIDENCY_IDX]
    return row


def _coerce_bool_cell(value: str) -> str:
    v = (value or "").strip().lower()
    if v in ("true", "1", "yes"):
        return "true"
    if v in ("false", "0", "no"):
        return "false"
    if not v:
        return "false"
    try:
        num = float(v.replace(",", ""))
        return "true" if num > 0 else "false"
    except ValueError:
        return "true"


def _map_provider_type(value: str) -> str:
    v = (value or "").strip()
    if v == "International":
        return "Government"
    return v


def _normalize_academic_year(value: str) -> str:
    v = (value or "").strip()
    m = re.fullmatch(r"(\d{4})-0(\d{3})", v)
    if m:
        start = int(m.group(1))
        return f"{start}-{start + 1}"
    if re.fullmatch(r"\d{4}-\d{4}", v):
        return v
    if re.fullmatch(r"\d{4}", v):
        y = int(v)
        return f"{y}-{y + 1}"
    return v


def _normalize_levels(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return v
    parts = [p.strip() for p in v.split("|")]
    out: list[str] = []
    for p in parts:
        if p.lower() == "senior high school":
            out.extend(["Grade 11", "Grade 12"])
        else:
            out.append(p)
    seen: set[str] = set()
    deduped: list[str] = []
    for p in out:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return "|".join(deduped)


def _normalize_priority_groups(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return v
    if "/" in v and "|" not in v:
        return "|".join(part.strip() for part in v.split("/") if part.strip())
    return v


def _sync_is_active(row: list[str]) -> None:
    notes = (row[NOTES_IDX] or "").lower()
    if "application_status=closed_reference" in notes:
        row[ACTIVE_IDX] = "false"


def _fix_source_urls(row: list[str]) -> None:
    urls = row[SOURCE_URLS_IDX] or ""
    if "feuhighschool.edu.ph" in urls.lower():
        row[SOURCE_URLS_IDX] = "https://www.afp.mil.ph|https://ched.gov.ph"


def _fix_owwa_benefits(row: list[str]) -> None:
    if not row[0].startswith("OWWA Educational Livelihood"):
        return
    if not (row[TUITION_IDX] or row[ALLOWANCE_IDX] or row[TOTAL_IDX]):
        row[TUITION_IDX] = "false"
        row[ALLOWANCE_IDX] = ""
        row[BOOKS_IDX] = "true"
        row[TOTAL_IDX] = "10000"


def _fix_row(row: list[str]) -> list[str]:
    if _region_block_shifted(row) and len(row) >= EXPECTED_COLS + 1:
        row = _fix_region_left_shift(row)
    row = _merge_overflow_columns(row)
    row = _fix_missing_eligible_cities(row)
    row = _fix_region_left_shift(row)
    if len(row) < EXPECTED_COLS:
        row = row + [""] * (EXPECTED_COLS - len(row))
    elif len(row) > EXPECTED_COLS:
        row = _merge_overflow_columns(row)
    for idx in BOOL_COL_IDXS + [BOOKS_IDX]:
        row[idx] = _coerce_bool_cell(row[idx])
    row[PROVIDER_TYPE_IDX] = _map_provider_type(row[PROVIDER_TYPE_IDX])
    row[ACADEMIC_YEAR_IDX] = _normalize_academic_year(row[ACADEMIC_YEAR_IDX])
    row[LEVELS_IDX] = _normalize_levels(row[LEVELS_IDX])
    row[PRIORITY_IDX] = _normalize_priority_groups(row[PRIORITY_IDX])
    _sync_is_active(row)
    _fix_source_urls(row)
    _fix_owwa_benefits(row)
    return row[:EXPECTED_COLS]


def fix_csv(input_path: Path, output_path: Path) -> dict:
    fixes_applied: list[str] = []
    with input_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if [h.strip() for h in header] != list(CANONICAL_IMPORT_COLUMNS):
            raise ValueError("Input header does not match canonical import contract")

        out_rows: list[list[str]] = []
        for line_no, raw in enumerate(reader, start=2):
            if _is_junk_row(raw):
                fixes_applied.append(f"line {line_no}: dropped junk row")
                continue
            before_len = len(raw)
            fixed = _fix_row(list(raw))
            if len(fixed) != EXPECTED_COLS:
                raise ValueError(f"line {line_no}: could not normalize to {EXPECTED_COLS} columns")
            if before_len != EXPECTED_COLS or fixed != raw[:EXPECTED_COLS]:
                fixes_applied.append(f"line {line_no}: normalized ({before_len} -> {EXPECTED_COLS})")
            out_rows.append(fixed)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CANONICAL_IMPORT_COLUMNS)
        for row in out_rows:
            writer.writerow(row)

    rows, structural = load_csv_strict(str(output_path))
    report_rows = list(structural.get("rejected_rows") or [])
    for row in rows:
        report_rows.append(validate_import_row(row))

    report = summarize_import_report(report_rows, structural=structural)
    report["fixes_applied"] = fixes_applied
    report["output_rows"] = len(out_rows)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix Gemini scholarship CSV for import")
    parser.add_argument("--input", required=True, help="Raw Gemini CSV path")
    parser.add_argument("--output", required=True, help="Corrected CSV output path")
    args = parser.parse_args()

    report = fix_csv(Path(args.input), Path(args.output))
    imported = report.get("imported") or {}
    invalid = imported.get("invalid", 0) + imported.get("rejected_structural", 0)
    print(f"Wrote {args.output} ({report.get('output_rows', 0)} rows)")
    print(
        f"Import preview: new={imported.get('new', 0)} "
        f"invalid={invalid} structural={imported.get('rejected_structural', 0)}"
    )
    if invalid:
        for r in report.get("rows") or []:
            if r.get("status") in ("invalid", "rejected_structural"):
                print(f"  FAIL: {r.get('title') or r.get('line')}: {r.get('error') or r.get('reason')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
