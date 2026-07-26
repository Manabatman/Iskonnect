"""
Apply duplicate-parent scholarship corrections from verification discovery.

Usage:
  python -m app.scripts.resolve_duplicate_scholarships
  python -m app.scripts.resolve_duplicate_scholarships --apply
  python -m app.scripts.resolve_duplicate_scholarships --json path/to/duplicate_candidates.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.scripts.apply_field_changes import load_field_changes_csv
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.field_evidence import create_field_evidence
from app.utils.scholarship_versioning import record_scholarship_version

logger = logging.getLogger(__name__)

DEFAULT_JSON = Path("verification/discovery/duplicate_candidates.json")
DEFAULT_DOST_CSV = Path("verification/reports/dost/field_changes.csv")

CONFIDENCE_SCORE = {"verified": 1.0, "partially_verified": 0.75, "cannot_verify": 0.5}

ID_54_CORRECTIONS: dict[str, Any] = {
    "title": "CHED Medical Scholarship and Return Service (MSRS)",
    "provider": "Commission on Higher Education",
    "link": "https://legacy.ched.gov.ph/msrs/",
    "is_active": True,
    "editorial_state": "verified",
    "data_status": "verified",
    "link_status": "ok",
}

ID_3_FIELDS = ("title", "description")


@dataclass
class ChangeOutcome:
    scholarship_id: int
    field: str
    action: str
    result: str
    detail: str = ""


@dataclass
class ResolveSummary:
    applied: int = 0
    skipped_idempotent: int = 0
    skipped_missing: int = 0
    dry_run: bool = True
    outcomes: list[ChangeOutcome] = field(default_factory=list)


def _load_duplicate_candidates(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return data


def _build_duplicate_updates(candidates: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Map scholarship id -> field updates from duplicate_candidates.json."""
    updates: dict[int, dict[str, Any]] = {}
    for entry in candidates:
        matched_ids = entry.get("matched_ids") or []
        if not matched_ids:
            continue
        sid = int(matched_ids[0])
        if sid in (54, 3):
            continue

        reasoning = (entry.get("reasoning") or "").strip()
        resolution = (entry.get("recommended_resolution") or "").strip()
        description_parts = [p for p in (reasoning, resolution) if p]
        description = " ".join(description_parts) if description_parts else None

        source_urls = entry.get("source_urls") or []
        link = source_urls[0] if source_urls else None
        confidence = entry.get("verification_confidence") or "partially_verified"

        field_updates: dict[str, Any] = {
            "title": entry.get("research_title"),
            "provider": entry.get("research_provider"),
        }
        if link:
            field_updates["link"] = link
        if description:
            field_updates["description"] = description

        updates[sid] = {
            "fields": {k: v for k, v in field_updates.items() if v},
            "source_url": link,
            "evidence_snippet": reasoning[:500] if reasoning else resolution[:500],
            "confidence": confidence,
        }
    return updates


def _load_id3_updates(csv_path: Path) -> dict[str, Any]:
    rows = load_field_changes_csv(csv_path)
    fields: dict[str, Any] = {}
    source_url = None
    evidence_snippet = None
    confidence = "verified"
    for row in rows:
        if row.get("id") != "3":
            continue
        csv_field = row.get("field", "")
        if csv_field not in ID_3_FIELDS:
            continue
        if row.get("action") != "update":
            continue
        official = (row.get("official_value") or "").strip()
        if not official or official.lower() == "cannot_verify":
            continue
        column = "link" if csv_field == "primary_link" else csv_field
        fields[column] = official
        source_url = source_url or row.get("source_url") or None
        evidence_snippet = evidence_snippet or row.get("evidence_snippet") or None
        confidence = row.get("confidence") or confidence
    fields["editorial_state"] = "needs_review"
    return {
        "fields": fields,
        "source_url": source_url,
        "evidence_snippet": evidence_snippet,
        "confidence": confidence,
    }


def _serialize(value: Any) -> Any:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _apply_field_change(
    db: Session,
    scholarship: models.Scholarship,
    column: str,
    new_value: Any,
    *,
    source_url: str | None,
    evidence_snippet: str | None,
    confidence: str,
    dry_run: bool,
    summary: ResolveSummary,
) -> None:
    sid = scholarship.id
    current = getattr(scholarship, column, None)
    if _serialize(current) == _serialize(new_value):
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            ChangeOutcome(sid, column, "update", "skipped_idempotent", "already set")
        )
        return

    summary.applied += 1
    summary.outcomes.append(
        ChangeOutcome(
            sid,
            column,
            "update",
            "applied" if not dry_run else "dry_run",
            f"{_serialize(current)!r} -> {_serialize(new_value)!r}",
        )
    )
    if dry_run:
        return

    setattr(scholarship, column, new_value)
    scholarship.verification_source = scholarship.verification_source or "duplicate_resolution"
    create_field_evidence(
        db,
        scholarship_id=sid,
        field_key=column,
        value_snapshot=_serialize(new_value),
        source_url=source_url,
        source_type="duplicate_resolution",
        evidence_snippet=evidence_snippet,
        confidence=CONFIDENCE_SCORE.get(confidence),
    )


def _refresh_dedupe_key(
    scholarship: models.Scholarship,
    *,
    dry_run: bool,
    summary: ResolveSummary,
) -> None:
    new_key = scholarship_dedupe_key(
        scholarship.title or "",
        scholarship.provider,
        scholarship.link,
    )
    if scholarship.dedupe_key == new_key:
        return
    summary.applied += 1
    summary.outcomes.append(
        ChangeOutcome(
            scholarship.id,
            "dedupe_key",
            "update",
            "applied" if not dry_run else "dry_run",
            f"{scholarship.dedupe_key!r} -> {new_key!r}",
        )
    )
    if not dry_run:
        scholarship.dedupe_key = new_key


def resolve_duplicates(
    db: Session,
    *,
    duplicate_json: Path,
    dost_csv: Path,
    dry_run: bool = True,
) -> ResolveSummary:
    summary = ResolveSummary(dry_run=dry_run)
    candidates = _load_duplicate_candidates(duplicate_json)
    duplicate_updates = _build_duplicate_updates(candidates)
    id3_update = _load_id3_updates(dost_csv)

    planned: dict[int, dict[str, Any]] = {}
    planned[54] = {
        "fields": dict(ID_54_CORRECTIONS),
        "source_url": "https://legacy.ched.gov.ph/msrs/",
        "evidence_snippet": "MSRS (RA 11509) administered by CHED; correct misattributed DOH record id 54",
        "confidence": "verified",
    }
    planned[3] = id3_update
    planned.update(duplicate_updates)

    version_batches: dict[int, dict[str, dict[str, Any]]] = {}

    for sid in sorted(planned):
        scholarship = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if scholarship is None:
            summary.skipped_missing += 1
            summary.outcomes.append(
                ChangeOutcome(sid, "*", "update", "skipped_missing", "scholarship not found")
            )
            continue

        before = {k: getattr(scholarship, k, None) for k in ("title", "provider", "link", "description", "is_active", "editorial_state")}
        bundle = planned[sid]
        fields = bundle["fields"]
        version_changes: dict[str, dict[str, Any]] = {}

        for column, new_value in fields.items():
            old_value = getattr(scholarship, column, None)
            _apply_field_change(
                db,
                scholarship,
                column,
                new_value,
                source_url=bundle.get("source_url"),
                evidence_snippet=bundle.get("evidence_snippet"),
                confidence=bundle.get("confidence") or "partially_verified",
                dry_run=dry_run,
                summary=summary,
            )
            if _serialize(old_value) != _serialize(new_value):
                version_changes[column] = {"from": _serialize(old_value), "to": _serialize(new_value)}

        if any(k in fields for k in ("title", "provider", "link")):
            _refresh_dedupe_key(scholarship, dry_run=dry_run, summary=summary)

        if version_changes:
            version_batches[sid] = version_changes

        after = {k: getattr(scholarship, k, None) for k in before}
        if before != after and not dry_run:
            logger.info("Scholarship %s updated: %s", sid, list(fields.keys()))

    if not dry_run:
        for sid, changes in version_batches.items():
            if changes:
                record_scholarship_version(
                    db,
                    scholarship_id=sid,
                    changes=changes,
                    changed_by=None,
                )
        db.commit()

    return summary


def print_summary(summary: ResolveSummary) -> None:
    mode = "DRY RUN" if summary.dry_run else "APPLIED"
    print(f"resolve_duplicate_scholarships ({mode})")
    print(f"  applied: {summary.applied}")
    print(f"  skipped_idempotent: {summary.skipped_idempotent}")
    print(f"  skipped_missing: {summary.skipped_missing}")
    for outcome in summary.outcomes:
        if outcome.result not in ("skipped_idempotent",):
            print(
                f"  id={outcome.scholarship_id} {outcome.field} "
                f"{outcome.result}: {outcome.detail}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve duplicate parent scholarship records")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="duplicate_candidates.json path")
    parser.add_argument("--dost-csv", type=Path, default=DEFAULT_DOST_CSV, help="DOST field_changes.csv for id 3")
    parser.add_argument("--apply", action="store_true", help="Persist changes (default dry-run)")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        summary = resolve_duplicates(
            db,
            duplicate_json=args.json,
            dost_csv=args.dost_csv,
            dry_run=not args.apply,
        )
        print_summary(summary)
    finally:
        db.close()


if __name__ == "__main__":
    main()
