"""
Taxonomy migration dry-run (DATA-05 / B8).

Enumerates distinct stored field values in profiles and scholarships; asserts each
resolves in the B6 taxonomy. Scholarship rows are report-only — no writes.

Usage:
  python -m app.scripts.taxonomy_migration_dryrun
  python -m app.scripts.taxonomy_migration_dryrun --report docs/engineering/reports/taxonomy-migration-dryrun.md
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

from app.db import SessionLocal
from app.models import Scholarship, Student
from app.taxonomy.psced_fields import taxonomy_value_resolves
from app.utils.json_helpers import parse_json_list

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT = REPO_ROOT / "docs" / "engineering" / "reports" / "taxonomy-migration-dryrun.md"


def collect_distinct_values(db) -> dict[str, Counter]:
    counters: dict[str, Counter] = {
        "profile_field_of_study_broad": Counter(),
        "profile_field_of_study_specific": Counter(),
        "scholarship_eligible_courses_psced": Counter(),
        "scholarship_eligible_courses_specific": Counter(),
    }

    for row in db.query(Student.field_of_study_broad, Student.field_of_study_specific).all():
        if row.field_of_study_broad:
            counters["profile_field_of_study_broad"][row.field_of_study_broad.strip()] += 1
        if row.field_of_study_specific:
            counters["profile_field_of_study_specific"][row.field_of_study_specific.strip()] += 1

    for row in db.query(Scholarship.eligible_courses_psced, Scholarship.eligible_courses_specific).all():
        for value in parse_json_list(row.eligible_courses_psced):
            if value:
                counters["scholarship_eligible_courses_psced"][str(value).strip()] += 1
        for value in parse_json_list(row.eligible_courses_specific):
            if value:
                counters["scholarship_eligible_courses_specific"][str(value).strip()] += 1

    return counters


def analyze_values(counters: dict[str, Counter]) -> dict:
    unresolved: dict[str, list[str]] = {}
    resolved_counts: dict[str, int] = {}
    for bucket, counter in counters.items():
        bad = sorted(v for v in counter if not taxonomy_value_resolves(v))
        unresolved[bucket] = bad
        resolved_counts[bucket] = sum(counter.values()) - sum(counter[v] for v in bad)
    total_values = sum(sum(c.values()) for c in counters.values())
    total_unresolved = sum(sum(counters[b][v] for v in unresolved[b]) for b in counters)
    return {
        "counters": counters,
        "unresolved": unresolved,
        "resolved_counts": resolved_counts,
        "total_values": total_values,
        "total_unresolved": total_unresolved,
        "ok": total_unresolved == 0,
    }


def render_report(result: dict) -> str:
    lines = [
        "# Taxonomy migration dry-run",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Status:** {'PASS — 100% resolve' if result['ok'] else 'FAIL — unresolved values present'}",
        "",
        "## Summary",
        "",
        f"- Total stored field values scanned: **{result['total_values']}**",
        f"- Unresolved occurrences: **{result['total_unresolved']}**",
        "",
        "## By source",
        "",
    ]
    for bucket, counter in result["counters"].items():
        lines.append(f"### `{bucket}`")
        lines.append("")
        if not counter:
            lines.append("_No values in database._")
            lines.append("")
            continue
        bad = set(result["unresolved"][bucket])
        for value, count in counter.most_common():
            status = "OK" if value not in bad else "UNRESOLVED"
            lines.append(f"- `{value}` × {count} — {status}")
        lines.append("")
    if not result["ok"]:
        lines.append("## Action required")
        lines.append("")
        lines.append("Add aliases or field entries in `app/taxonomy/psced_fields.py` for every UNRESOLVED value above.")
    return "\n".join(lines) + "\n"


def run_dryrun(db=None) -> dict:
    owns_session = db is None
    if owns_session:
        db = SessionLocal()
    try:
        counters = collect_distinct_values(db)
        return analyze_values(counters)
    finally:
        if owns_session:
            db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Taxonomy migration dry-run report")
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Markdown report output path",
    )
    args = parser.parse_args()

    result = run_dryrun()
    report = render_report(result)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(report)
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
