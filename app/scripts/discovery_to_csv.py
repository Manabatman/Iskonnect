"""
Convert validated discovery JSON to import-contract CSV (40 columns).

Usage:
  python -m app.scripts.discovery_to_csv
  python -m app.scripts.discovery_to_csv --include-partial
  python -m app.scripts.discovery_to_csv --input verification/discovery/validated_new_scholarships.json --output data/discovery_import.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS

DEFAULT_INPUT = Path("verification/discovery/validated_new_scholarships.json")
DEFAULT_OUTPUT = Path("data/discovery_import.csv")

DATE_COLUMNS = (
    "application_open_date",
    "application_deadline",
    "last_open_date",
    "last_close_date",
)


def _join_pipe(values: list | None) -> str:
    if not values:
        return ""
    return "|".join(str(v).strip() for v in values if str(v).strip())


def _bool_str(value: bool | None, default: bool = False) -> str:
    if value is None:
        return "true" if default else "false"
    return "true" if value else "false"


def _parse_benefit_total(benefits: str | None, benefit_summary: str | None) -> str:
    text = " ".join(filter(None, [benefits, benefit_summary]))
    if not text:
        return ""
    amounts: list[int] = []
    for match in re.finditer(r"php\s*([\d,]+)", text, re.IGNORECASE):
        try:
            amounts.append(int(match.group(1).replace(",", "")))
        except ValueError:
            continue
    if not amounts:
        return ""
    return str(max(amounts))


def _benefit_flags(benefits: str | None, benefit_summary: str | None) -> tuple[str, str]:
    text = " ".join(filter(None, [benefits, benefit_summary])).lower()
    tuition = "true" if any(k in text for k in ("tuition", "school fees", "tosf", "fee exemption")) else "false"
    books = "true" if "book" in text else "false"
    return tuition, books


def _is_active_from_status(status: str | None) -> str:
    normalized = (status or "").strip().lower()
    if normalized in ("open", "expected_reopen", "closed_for_this_cycle"):
        return "true"
    if normalized in ("closed", "permanently_discontinued", "archived"):
        return "false"
    return "true"


def _research_notes(entry: dict) -> str:
    parts = [
        f"verification_confidence={entry.get('verification_confidence', '')}",
        f"application_status={entry.get('application_status', '')}",
        f"discovery_classification={entry.get('discovery_classification', '')}",
    ]
    legal = entry.get("legal_basis")
    if legal:
        parts.append(f"legal_basis={legal}")
    aliases = entry.get("aliases") or []
    if aliases:
        parts.append(f"aliases={_join_pipe(aliases)}")
    portal = entry.get("application_portal_url")
    if portal:
        parts.append(f"application_portal_url={portal}")
    return " | ".join(p for p in parts if p)


def discovery_row_to_csv(entry: dict) -> dict[str, str]:
    benefits = entry.get("benefits")
    benefit_summary = entry.get("benefit_summary")
    benefit_tuition, benefit_books = _benefit_flags(benefits, benefit_summary)
    link = (entry.get("primary_link") or entry.get("application_portal_url") or "").strip()
    source_urls = entry.get("source_urls") or []
    if not link and source_urls:
        link = source_urls[0]

    row = {col: "" for col in CANONICAL_IMPORT_COLUMNS}
    row.update(
        {
            "title": (entry.get("title") or "").strip(),
            "provider": (entry.get("provider") or "").strip(),
            "source": "discovery_verification",
            "link": link,
            "description": (entry.get("description") or "").strip(),
            "provider_type": (entry.get("provider_type") or "").strip(),
            "scholarship_type": (entry.get("scholarship_type") or "").strip(),
            "eligible_levels": _join_pipe(entry.get("eligible_levels")),
            "eligible_regions": _join_pipe(entry.get("eligible_regions")),
            "eligible_courses_psced": _join_pipe(entry.get("eligible_courses_psced")),
            "eligible_courses_specific": _join_pipe(entry.get("eligible_courses_specific")),
            "max_income_threshold": str(entry["max_income_threshold"])
            if entry.get("max_income_threshold") is not None
            else "",
            "min_gwa_normalized": str(entry["min_gwa_normalized"])
            if entry.get("min_gwa_normalized") is not None
            else "",
            "priority_groups": _join_pipe(entry.get("priority_groups")),
            "members_only": _bool_str(entry.get("members_only"), default=False),
            "benefit_tuition": benefit_tuition,
            "benefit_books": benefit_books,
            "benefit_total_value": _parse_benefit_total(benefits, benefit_summary),
            "required_documents": _join_pipe(entry.get("required_documents")),
            "has_return_service": _bool_str(entry.get("has_return_service"), default=False),
            "application_open_date": (entry.get("application_open_date") or "").strip(),
            "application_deadline": (entry.get("application_deadline") or "").strip(),
            "cycle_type": (entry.get("cycle_type") or "").strip(),
            "is_active": _is_active_from_status(entry.get("application_status")),
            "source_slug": (entry.get("research_candidate_id") or "").strip(),
            "research_notes": _research_notes(entry),
            "source_urls": _join_pipe(source_urls),
            "dedupe_rationale": (entry.get("evidence_snippet") or "").strip(),
        }
    )
    return row


def convert_discovery_json(
    input_path: Path,
    *,
    include_partial: bool = False,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    with input_path.open(encoding="utf-8") as fh:
        entries = json.load(fh)
    if not isinstance(entries, list):
        raise ValueError(f"Expected JSON array in {input_path}")

    rows: list[dict[str, str]] = []
    stats = {"total": len(entries), "exported": 0, "skipped_partial": 0, "skipped_invalid": 0}

    for entry in entries:
        confidence = (entry.get("verification_confidence") or "").strip().lower()
        if confidence == "partially_verified" and not include_partial:
            stats["skipped_partial"] += 1
            continue
        if not (entry.get("title") or "").strip():
            stats["skipped_invalid"] += 1
            continue
        rows.append(discovery_row_to_csv(entry))
        stats["exported"] += 1

    return rows, stats


def write_discovery_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CANONICAL_IMPORT_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert validated discovery JSON to import CSV")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-partial",
        action="store_true",
        help="Include partially_verified entries (default: verified only)",
    )
    args = parser.parse_args()

    rows, stats = convert_discovery_json(args.input, include_partial=args.include_partial)
    write_discovery_csv(args.output, rows)

    print(f"discovery_to_csv -> {args.output}")
    print(f"  total: {stats['total']}")
    print(f"  exported: {stats['exported']}")
    print(f"  skipped_partial: {stats['skipped_partial']}")
    print(f"  skipped_invalid: {stats['skipped_invalid']}")


if __name__ == "__main__":
    main()
