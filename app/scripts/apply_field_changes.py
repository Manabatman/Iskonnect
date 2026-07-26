"""
Apply verified field_changes.csv corrections to the scholarship catalog.

Usage:
  python -m app.scripts.apply_field_changes --csv verification/reports/dost/field_changes.csv
  python -m app.scripts.apply_field_changes --csv path/to/field_changes.csv --apply
  python -m app.scripts.apply_field_changes --csv path/to/field_changes.csv --report out/report.csv
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.db import SessionLocal
from app.utils.field_evidence import create_field_evidence
from app.utils.scholarship_versioning import record_scholarship_version
from app.verification.report_schema import FIELD_CHANGES_COLUMNS

logger = logging.getLogger(__name__)

APPLY_CONFIDENCE = frozenset({"verified", "partially_verified"})

CSV_FIELD_TO_COLUMN: dict[str, str] = {
    "primary_link": "link",
    "application_portal_url": "link",
}

DATE_COLUMNS = frozenset(
    {
        "application_open_date",
        "application_deadline",
        "last_open_date",
        "last_close_date",
    }
)

BOOL_COLUMNS = frozenset(
    {
        "is_active",
        "residency_required",
        "members_only",
        "benefit_tuition",
        "benefit_books",
        "has_qualifying_exam",
        "has_interview",
        "has_essay_requirement",
        "has_return_service",
    }
)

INT_COLUMNS = frozenset(
    {
        "max_income_threshold",
        "benefit_allowance_monthly",
        "benefit_total_value",
        "min_age",
        "max_age",
    }
)

FLOAT_COLUMNS = frozenset({"min_gwa_normalized"})

CONFIDENCE_SCORE: dict[str, float] = {
    "verified": 1.0,
    "partially_verified": 0.75,
}

BLOCKED_UPDATES: frozenset[tuple[int, str, str]] = frozenset(
    {
        (2, "application_open_date", "2024-10-13"),
        (2, "application_deadline", "2024-12-23"),
    }
)


@dataclass
class RowOutcome:
    line: int
    scholarship_id: int
    csv_field: str
    action: str
    result: str
    detail: str = ""


@dataclass
class ApplySummary:
    applied: int = 0
    skipped_confirm_unchanged: int = 0
    skipped_low_confidence: int = 0
    skipped_cannot_verify_value: int = 0
    skipped_blocked: int = 0
    skipped_drift: int = 0
    skipped_idempotent: int = 0
    skipped_missing_scholarship: int = 0
    skipped_unknown_field: int = 0
    flag_review: int = 0
    archived: int = 0
    dry_run: bool = True
    outcomes: list[RowOutcome] = field(default_factory=list)

    def to_counts_dict(self) -> dict[str, int | bool]:
        return {
            "applied": self.applied,
            "skipped_confirm_unchanged": self.skipped_confirm_unchanged,
            "skipped_low_confidence": self.skipped_low_confidence,
            "skipped_cannot_verify_value": self.skipped_cannot_verify_value,
            "skipped_blocked": self.skipped_blocked,
            "skipped_drift": self.skipped_drift,
            "skipped_idempotent": self.skipped_idempotent,
            "skipped_missing_scholarship": self.skipped_missing_scholarship,
            "skipped_unknown_field": self.skipped_unknown_field,
            "flag_review": self.flag_review,
            "archived": self.archived,
            "dry_run": self.dry_run,
        }


def _parse_date(value: str | None) -> date | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return date.fromisoformat(text[:10])


def _parse_verified_at(value: str | None) -> datetime | None:
    if not value or not value.strip():
        return None
    text = value.strip()
    if len(text) == 10:
        return datetime.fromisoformat(text)
    return datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)


def resolve_model_column(csv_field: str) -> str | None:
    key = (csv_field or "").strip()
    if not key:
        return None
    mapped = CSV_FIELD_TO_COLUMN.get(key, key)
    if not hasattr(models.Scholarship, mapped):
        return None
    return mapped


def map_application_status(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if text.lower() == "closed_for_this_cycle":
        return "expected_reopen"
    return text


def archive_application_status(closure_type: str | None) -> str:
    if (closure_type or "").strip().lower() == "permanently_discontinued":
        return "permanently_discontinued"
    return "archived"


def normalize_for_compare(column: str, value: Any) -> Any:
    if value is None:
        return None
    if column in DATE_COLUMNS:
        if isinstance(value, date):
            return value.isoformat()
        text = str(value).strip()
        return text[:10] if text else None
    if column in BOOL_COLUMNS:
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in ("true", "1", "yes"):
            return True
        if text in ("false", "0", "no"):
            return False
        return None
    if column in INT_COLUMNS:
        if value == "" or value is None:
            return None
        try:
            return int(float(str(value).strip()))
        except (TypeError, ValueError):
            return str(value).strip()
    if column in FLOAT_COLUMNS:
        if value == "" or value is None:
            return None
        try:
            return float(str(value).strip())
        except (TypeError, ValueError):
            return str(value).strip()
    if column == "application_status":
        return map_application_status(str(value))
    text = str(value).strip()
    return text if text else None


def coerce_official_value(column: str, official_value: str | None) -> Any:
    if official_value is None:
        return None
    text = official_value.strip()
    if not text:
        return None
    if text.lower() == "cannot_verify":
        return None
    if column in DATE_COLUMNS:
        return _parse_date(text)
    if column in BOOL_COLUMNS:
        lowered = text.lower()
        if lowered in ("true", "1", "yes"):
            return True
        if lowered in ("false", "0", "no"):
            return False
        return None
    if column in INT_COLUMNS:
        try:
            return int(float(text))
        except ValueError:
            return text
    if column in FLOAT_COLUMNS:
        try:
            return float(text)
        except ValueError:
            return text
    if column == "application_status":
        return map_application_status(text)
    return text


def serialize_db_value(column: str, value: Any) -> Any:
    if value is None:
        return None
    if column in DATE_COLUMNS and isinstance(value, date):
        return value.isoformat()
    if column in BOOL_COLUMNS:
        return bool(value)
    return value


def is_blocked_update(scholarship_id: int, csv_field: str, official_value: str | None) -> bool:
    column = resolve_model_column(csv_field) or csv_field
    official_norm = normalize_for_compare(column, official_value)
    for blocked_id, blocked_field, blocked_value in BLOCKED_UPDATES:
        if scholarship_id != blocked_id:
            continue
        if column != blocked_field:
            continue
        if official_norm == blocked_value:
            return True
    return False


def load_field_changes_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        missing = [c for c in FIELD_CHANGES_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing required columns {missing}: {path}")
        return [{k: (row.get(k) or "").strip() for k in FIELD_CHANGES_COLUMNS} for row in reader]


def _get_scholarship(db: Session, scholarship_id: int) -> models.Scholarship | None:
    return db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()


def _apply_archive(
    db: Session,
    scholarship: models.Scholarship,
    row: dict[str, str],
    *,
    dry_run: bool,
    summary: ApplySummary,
    line: int,
    version_changes: dict[str, dict[str, Any]],
    archived_ids: set[int],
) -> None:
    sid = scholarship.id
    if sid in archived_ids:
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            RowOutcome(line, sid, row.get("field", ""), "archive", "skipped_idempotent", "already archived this run")
        )
        return

    closure_type = row.get("closure_type") or ""
    target_status = archive_application_status(closure_type)
    changes: dict[str, dict[str, Any]] = {}

    if scholarship.is_active is not False:
        changes["is_active"] = {"from": scholarship.is_active, "to": False}
    if scholarship.editorial_state != "archived":
        changes["editorial_state"] = {"from": scholarship.editorial_state, "to": "archived"}
    if scholarship.application_status != target_status:
        changes["application_status"] = {"from": scholarship.application_status, "to": target_status}

    if not changes:
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            RowOutcome(line, sid, row.get("field", ""), "archive", "skipped_idempotent", "already archived in DB")
        )
        archived_ids.add(sid)
        return

    summary.archived += 1
    summary.outcomes.append(
        RowOutcome(line, sid, row.get("field", ""), "archive", "applied" if not dry_run else "dry_run", str(changes))
    )

    if dry_run:
        archived_ids.add(sid)
        version_changes.update(changes)
        return

    for column, diff in changes.items():
        setattr(scholarship, column, diff["to"])
    verified_at = _parse_verified_at(row.get("verified_at"))
    if verified_at:
        scholarship.last_verified_at = verified_at
    scholarship.verification_source = scholarship.verification_source or "field_changes_import"
    archived_ids.add(sid)
    version_changes.update(changes)


def _apply_flag_review(
    scholarship: models.Scholarship,
    row: dict[str, str],
    *,
    dry_run: bool,
    summary: ApplySummary,
    line: int,
    version_changes: dict[str, dict[str, Any]],
) -> None:
    sid = scholarship.id
    if scholarship.editorial_state == "needs_review":
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            RowOutcome(line, sid, row.get("field", ""), "flag_review", "skipped_idempotent", "already needs_review")
        )
        return

    diff = {"editorial_state": {"from": scholarship.editorial_state, "to": "needs_review"}}
    summary.flag_review += 1
    summary.outcomes.append(
        RowOutcome(line, sid, row.get("field", ""), "flag_review", "applied" if not dry_run else "dry_run")
    )
    if not dry_run:
        scholarship.editorial_state = "needs_review"
        verified_at = _parse_verified_at(row.get("verified_at"))
        if verified_at:
            scholarship.last_verified_at = verified_at
    version_changes.update(diff)


def _apply_field_update(
    db: Session,
    scholarship: models.Scholarship,
    row: dict[str, str],
    *,
    dry_run: bool,
    summary: ApplySummary,
    line: int,
    version_changes: dict[str, dict[str, Any]],
) -> None:
    sid = scholarship.id
    csv_field = row.get("field", "")
    column = resolve_model_column(csv_field)
    if column is None:
        summary.skipped_unknown_field += 1
        summary.outcomes.append(
            RowOutcome(line, sid, csv_field, "update", "skipped_unknown_field", f"unknown field {csv_field!r}")
        )
        return

    confidence = (row.get("confidence") or "").strip().lower()
    if confidence not in APPLY_CONFIDENCE:
        summary.skipped_low_confidence += 1
        summary.outcomes.append(
            RowOutcome(line, sid, csv_field, "update", "skipped_low_confidence", confidence or "(empty)")
        )
        return

    official_raw = row.get("official_value", "")
    if official_raw.strip().lower() == "cannot_verify":
        summary.skipped_cannot_verify_value += 1
        summary.outcomes.append(
            RowOutcome(line, sid, csv_field, "update", "skipped_cannot_verify_value", official_raw)
        )
        return

    if is_blocked_update(sid, csv_field, official_raw):
        summary.skipped_blocked += 1
        summary.outcomes.append(
            RowOutcome(line, sid, csv_field, "update", "skipped_blocked", f"hard-blocked official_value={official_raw!r}")
        )
        return

    isk_raw = row.get("iskconnect_value", "")
    current_raw = getattr(scholarship, column)
    expected = normalize_for_compare(column, isk_raw if isk_raw != "" else None)
    current = normalize_for_compare(column, serialize_db_value(column, current_raw))
    if expected != current:
        summary.skipped_drift += 1
        summary.outcomes.append(
            RowOutcome(
                line,
                sid,
                csv_field,
                "update",
                "skipped_drift",
                f"DB={current!r} expected iskconnect={expected!r}",
            )
        )
        logger.warning(
            "Drift skip scholarship_id=%s field=%s: DB=%r iskconnect_value=%r",
            sid,
            csv_field,
            current,
            expected,
        )
        return

    target = coerce_official_value(column, official_raw if official_raw != "" else None)
    if column in INT_COLUMNS | FLOAT_COLUMNS and isinstance(target, str):
        summary.skipped_cannot_verify_value += 1
        summary.outcomes.append(
            RowOutcome(
                line,
                sid,
                csv_field,
                "update",
                "skipped_unparseable_numeric",
                official_raw,
            )
        )
        return
    target_cmp = normalize_for_compare(column, target)
    if target_cmp == current:
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            RowOutcome(line, sid, csv_field, "update", "skipped_idempotent", "target matches DB")
        )
        return

    summary.applied += 1
    summary.outcomes.append(
        RowOutcome(
            line,
            sid,
            csv_field,
            "update",
            "applied" if not dry_run else "dry_run",
            f"{current!r} -> {target_cmp!r}",
        )
    )
    version_changes[column] = {"from": serialize_db_value(column, current_raw), "to": target_cmp}

    if not dry_run:
        setattr(scholarship, column, target)
        verified_at = _parse_verified_at(row.get("verified_at"))
        if verified_at:
            scholarship.last_verified_at = verified_at
        scholarship.verification_source = scholarship.verification_source or "field_changes_import"
        create_field_evidence(
            db,
            scholarship_id=sid,
            field_key=column,
            value_snapshot=target_cmp,
            source_url=row.get("source_url") or None,
            source_type="field_changes_import",
            evidence_snippet=row.get("evidence_snippet") or None,
            confidence=CONFIDENCE_SCORE.get(confidence),
        )


def apply_field_changes(
    db: Session,
    rows: list[dict[str, str]],
    *,
    dry_run: bool = True,
) -> ApplySummary:
    summary = ApplySummary(dry_run=dry_run)
    archived_ids: set[int] = set()
    version_batches: dict[int, dict[str, dict[str, Any]]] = {}

    for idx, row in enumerate(rows, start=2):
        action = (row.get("action") or "").strip().lower()
        sid_text = row.get("id", "").strip()
        if not sid_text.isdigit():
            summary.skipped_missing_scholarship += 1
            summary.outcomes.append(
                RowOutcome(idx, -1, row.get("field", ""), action, "skipped_missing_scholarship", "invalid id")
            )
            continue
        sid = int(sid_text)
        scholarship = _get_scholarship(db, sid)
        if scholarship is None:
            summary.skipped_missing_scholarship += 1
            summary.outcomes.append(
                RowOutcome(idx, sid, row.get("field", ""), action, "skipped_missing_scholarship", "not found")
            )
            continue

        version_changes = version_batches.setdefault(sid, {})

        if action == "confirm_unchanged":
            summary.skipped_confirm_unchanged += 1
            summary.outcomes.append(
                RowOutcome(idx, sid, row.get("field", ""), action, "skipped_confirm_unchanged")
            )
            continue

        if action == "archive":
            _apply_archive(
                db,
                scholarship,
                row,
                dry_run=dry_run,
                summary=summary,
                line=idx,
                version_changes=version_changes,
                archived_ids=archived_ids,
            )
            continue

        if action == "flag_review":
            _apply_flag_review(
                scholarship,
                row,
                dry_run=dry_run,
                summary=summary,
                line=idx,
                version_changes=version_changes,
            )
            continue

        if action == "update":
            _apply_field_update(
                db,
                scholarship,
                row,
                dry_run=dry_run,
                summary=summary,
                line=idx,
                version_changes=version_changes,
            )
            continue

        summary.outcomes.append(
            RowOutcome(idx, sid, row.get("field", ""), action, "skipped_unknown_action", action or "(empty)")
        )

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


def write_report(path: Path, summary: ApplySummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["line", "scholarship_id", "field", "action", "result", "detail"],
        )
        writer.writeheader()
        for outcome in summary.outcomes:
            writer.writerow(
                {
                    "line": outcome.line,
                    "scholarship_id": outcome.scholarship_id,
                    "field": outcome.csv_field,
                    "action": outcome.action,
                    "result": outcome.result,
                    "detail": outcome.detail,
                }
            )


def print_summary(summary: ApplySummary) -> None:
    counts = summary.to_counts_dict()
    mode = "DRY RUN" if summary.dry_run else "APPLIED"
    print(f"apply_field_changes ({mode})")
    for key, value in counts.items():
        if key == "dry_run":
            continue
        print(f"  {key}: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply field_changes.csv corrections to scholarships.")
    parser.add_argument("--csv", required=True, type=Path, help="Path to field_changes.csv")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Persist changes (default is dry-run)",
    )
    parser.add_argument("--report", type=Path, default=None, help="Optional CSV path for per-row outcomes")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    csv_path = args.csv
    if not csv_path.is_file():
        raise SystemExit(f"CSV not found: {csv_path}")

    dry_run = not args.apply
    if not dry_run:
        db_url = (settings.database_url or "").strip()
        if not db_url:
            raise SystemExit("DATABASE_URL is not configured.")

    rows = load_field_changes_csv(csv_path)
    db = SessionLocal()
    try:
        summary = apply_field_changes(db, rows, dry_run=dry_run)
    finally:
        if dry_run:
            db.rollback()
        db.close()

    print_summary(summary)
    if args.report:
        write_report(args.report, summary)
        print(f"  report: {args.report}")


if __name__ == "__main__":
    main()
