"""
Export ISKONNECT catalog data for external ChatGPT verification.

Usage:
  python -m app.scripts.export_verification_package
  python -m app.scripts.export_verification_package --active-only
  python -m app.scripts.export_verification_package --include-archived
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings
from app.db import SessionLocal
from app import models
from app.verification.bundles import (
    BUNDLE_DEFINITIONS,
    assign_verification_bundle,
    get_bundle_definition,
    ordered_bundle_ids,
)
from app.verification.export_schema import (
    VERIFICATION_EXPORT_COLUMNS,
    row_to_verification_export,
    verification_record_to_csv_row,
)
from app.verification.report_schema import (
    CHANGE_REASONS,
    CLOSURE_TYPES,
    FIELD_CHANGES_COLUMNS,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VERIFICATION_ROOT = PROJECT_ROOT / "verification"
EXPORT_ROOT = VERIFICATION_ROOT / "export"
BUNDLES_ROOT = EXPORT_ROOT / "bundles"
PROMPTS_ROOT = VERIFICATION_ROOT / "prompts"
TEMPLATES_ROOT = VERIFICATION_ROOT / "templates"
REPORTS_ROOT = VERIFICATION_ROOT / "reports"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(VERIFICATION_EXPORT_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _write_templates() -> None:
    TEMPLATES_ROOT.mkdir(parents=True, exist_ok=True)
    field_changes = TEMPLATES_ROOT / "field_changes.template.csv"
    with field_changes.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(FIELD_CHANGES_COLUMNS))
        writer.writeheader()
    _write_json(TEMPLATES_ROOT / "new_scholarships.template.json", [])
    _write_json(
        TEMPLATES_ROOT / "schema_candidates.template.json",
        [
            {
                "observed_rule": "",
                "example_scholarship_ids": [],
                "frequency_in_bundle": 0,
                "current_workaround": "description",
                "recommendation": "keep_free_text",
                "source_urls": [],
            }
        ],
    )
    _write_json(
        TEMPLATES_ROOT / "important_notes.template.json",
        [{"scholarship_id": 0, "notes": [], "source_url": ""}],
    )


def _master_instructions_text() -> str:
    change_reasons = ", ".join(f"`{r}`" for r in CHANGE_REASONS)
    closure_types = ", ".join(f"`{t}`" for t in CLOSURE_TYPES)
    return f"""# ISKONNECT External Verification — Master Instructions

Paste this at the start of **every** ChatGPT verification conversation (with web search enabled).

## Role

You are an external scholarship auditor for **ISKONNECT**, a Philippines scholarship matching platform. Your job is to verify catalog records against **official sources only** — not blogs, aggregators, or social media unless no official source exists.

## Rules

1. **Official sources first** — prefer `.gov.ph`, `.edu.ph`, and official foundation domains.
2. **Never guess** — if a field cannot be confirmed, mark it `cannot_verify` and leave `official_value` empty.
3. **Evidence required** — every field correction MUST include `source_url` and `evidence_snippet` (quote or announcement reference).
4. **Change reason required** — classify each correction using: {change_reasons}.
5. **Closure types** — when status changes, use: {closure_types}. Do NOT recommend archiving recurring programs that are merely closed for the season.
6. **Primary link** — ISKONNECT stores one URL as `primary_link`. Flag when it is a homepage vs a program-specific page. Capture separate application portal URLs in corrections or new scholarship entries.
7. **Schema gaps** — there is no `contact_email` or `contact_phone` in ISKONNECT today. Extract contacts when published and report as new fields in `field_changes.csv` or `important_notes.json`.

## Required deliverables (all five files)

Save outputs under `verification/reports/{{bundle_id}}/`:

| File | Purpose |
|------|---------|
| `human_report.md` | Summary for human admin review |
| `field_changes.csv` | One row per field correction with evidence |
| `new_scholarships.json` | Programs on official site but missing from ISKONNECT |
| `schema_candidates.json` | Recurring eligibility rules ISKONNECT cannot represent structurally |
| `important_notes.json` | FAQ-style rules not yet structured |

## field_changes.csv columns

`id | field | iskconnect_value | official_value | action | change_reason | closure_type | confidence | source_url | evidence_snippet | official_last_updated | announcement_date | verified_at`

- **action**: `update`, `confirm_unchanged`, `archive`, or `flag_review`
- **confidence**: `verified`, `partially_verified`, or `cannot_verify`
- **closure_type**: required when changing `is_active`, `application_status`, or `data_status`

## Workflow order

1. Verify existing records in the attached bundle JSON
2. Populate `field_changes.csv` with evidence + change reason
3. Search official provider site for missing programs → `new_scholarships.json`
4. Extract FAQ / important notes → `important_notes.json`
5. Flag recurring unmodeled rules → `schema_candidates.json`
6. Write `human_report.md`
7. Do not proceed to the next provider until all five files are complete

## Reference docs

- `verification/CHECKLIST.md` — per-scholarship questions
- `verification/DEFINITION_OF_DONE.md` — completion criteria
- `verification/CHANGE_REASONS.md` — change reason taxonomy
- `verification/CLOSURE_TYPES.md` — closure type definitions
- `verification/MISSING_SCHOLARSHIP_TARGETS.md` — programs to search for
- `verification/templates/` — import-ready output templates
"""


def _bundle_prompt_text(bundle_id: str, scholarship_ids: list[int]) -> str:
    bundle = get_bundle_definition(bundle_id)
    if bundle is None:
        return f"# Bundle {bundle_id}\n\n(No bundle metadata found.)\n"
    domains = ", ".join(bundle.official_domains) if bundle.official_domains else "(varies)"
    targets = "\n".join(f"- {t}" for t in bundle.missing_search_targets) or "- (see MISSING_SCHOLARSHIP_TARGETS.md)"
    ids_str = ", ".join(str(i) for i in sorted(scholarship_ids)) or "(none in this export)"
    archived_note = bundle.archived_note or "Check archived variants listed in bundle export if present."

    return f"""# ISKONNECT Verification — {bundle.title}

**Bundle ID:** `{bundle_id}`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/{bundle_id}.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export ({len(scholarship_ids)} records).

Scholarship IDs in this export: {ids_str}

{archived_note}

## Official domains to prioritize

{domains}

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

{targets}

See also `verification/MISSING_SCHOLARSHIP_TARGETS.md` for cross-bundle targets.

## Verification workflow

Follow the master instructions workflow:

1. **Verify existing records** — compare each JSON row against official sources
2. **Identify corrections** — populate `field_changes.csv` with evidence + change reason
3. **Find missing scholarships** — populate `new_scholarships.json`
4. **Extract FAQs / important notes** — populate `important_notes.json`
5. **Flag schema candidates** — populate `schema_candidates.json` for recurring unmodeled rules
6. **Produce human summary** — `human_report.md` for admin review

## Output location

Save all five deliverables to:

```
verification/reports/{bundle_id}/
  human_report.md
  field_changes.csv
  new_scholarships.json
  schema_candidates.json
  important_notes.json
```

Match column/format conventions in `verification/templates/`.

## Do not

- Verify scholarships from other bundles in this conversation
- Recommend `is_active=false` for recurring programs merely closed for the cycle
- Submit field changes without `source_url` and `evidence_snippet`
"""


def _write_prompts(bundle_records: dict[str, list[dict]]) -> None:
    PROMPTS_ROOT.mkdir(parents=True, exist_ok=True)
    master_path = PROMPTS_ROOT / "00_MASTER_INSTRUCTIONS.md"
    master_path.write_text(_master_instructions_text(), encoding="utf-8")
    for bundle_id in ordered_bundle_ids(include_archived=True):
        ids = [int(r["id"]) for r in bundle_records.get(bundle_id, []) if r.get("id") is not None]
        prompt_path = PROMPTS_ROOT / f"{bundle_id}_prompt.md"
        prompt_path.write_text(_bundle_prompt_text(bundle_id, ids), encoding="utf-8")


def export_package(*, active_only: bool) -> dict:
    db_url = (settings.database_url or "").strip()
    if not db_url:
        raise SystemExit("DATABASE_URL is not configured.")

    db = SessionLocal()
    try:
        query = db.query(models.Scholarship).order_by(models.Scholarship.id)
        if active_only:
            query = query.filter(models.Scholarship.is_active.is_(True))
        rows = query.all()
    finally:
        db.close()

    records: list[dict] = []
    by_bundle: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        bundle_id = assign_verification_bundle(row)
        record = row_to_verification_export(row, verification_bundle=bundle_id)
        records.append(record)
        by_bundle[bundle_id].append(record)

    active_records = [r for r in records if r.get("is_active") is True]
    csv_rows = [verification_record_to_csv_row(r) for r in records]
    active_csv_rows = [verification_record_to_csv_row(r) for r in active_records]

    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    BUNDLES_ROOT.mkdir(parents=True, exist_ok=True)

    _write_csv(EXPORT_ROOT / "all_scholarships.csv", csv_rows)
    _write_json(EXPORT_ROOT / "all_scholarships.json", records)
    if active_only:
        _write_csv(EXPORT_ROOT / "all_active.csv", active_csv_rows)
        _write_json(EXPORT_ROOT / "all_active.json", active_records)

    bundle_index: dict[str, dict] = {}
    for bundle_id in ordered_bundle_ids(include_archived=True):
        bundle_rows = by_bundle.get(bundle_id, [])
        if not bundle_rows and bundle_id != "archived_reference":
            continue
        bundle_csv = [verification_record_to_csv_row(r) for r in bundle_rows]
        _write_csv(BUNDLES_ROOT / f"{bundle_id}.csv", bundle_csv)
        _write_json(BUNDLES_ROOT / f"{bundle_id}.json", bundle_rows)
        high_priority = sum(1 for r in bundle_rows if r.get("verification_priority") == "high")
        bundle_index[bundle_id] = {
            "title": get_bundle_definition(bundle_id).title if get_bundle_definition(bundle_id) else bundle_id,
            "count": len(bundle_rows),
            "high_priority_count": high_priority,
            "scholarship_ids": sorted(int(r["id"]) for r in bundle_rows if r.get("id") is not None),
        }

    exported_at = datetime.now(timezone.utc).isoformat()
    master_index = {
        "exported_at": exported_at,
        "active_only_filter": active_only,
        "total_exported": len(records),
        "active_count": sum(1 for r in records if r.get("is_active") is True),
        "archived_count": sum(1 for r in records if r.get("is_active") is False),
        "bundle_count": len(bundle_index),
        "bundles": bundle_index,
        "conversation_order": ordered_bundle_ids(include_archived=False),
    }
    _write_json(EXPORT_ROOT / "master_index.json", master_index)

    _write_templates()
    _write_prompts(by_bundle)

    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    for bundle_id in bundle_index:
        (REPORTS_ROOT / bundle_id).mkdir(parents=True, exist_ok=True)

    return {
        "total": len(records),
        "active": master_index["active_count"],
        "bundles": len(bundle_index),
        "export_root": str(EXPORT_ROOT),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export verification package for external ChatGPT audit")
    parser.add_argument(
        "--active-only",
        action="store_true",
        default=True,
        help="Export only active scholarships (default: true)",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived scholarships in export (overrides --active-only)",
    )
    args = parser.parse_args()
    active_only = not args.include_archived

    logging.basicConfig(level=logging.INFO)
    summary = export_package(active_only=active_only)
    print(
        f"Verification export complete: {summary['total']} scholarships "
        f"({summary['active']} active) across {summary['bundles']} bundles.\n"
        f"Output: {summary['export_root']}"
    )


if __name__ == "__main__":
    main()
