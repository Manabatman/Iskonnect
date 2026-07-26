"""
Apply verified link and link_status fixes to the scholarship catalog.

Reads link corrections from verification bundle field_changes.csv files and
applies common URL migration patterns for known broken links.

Usage:
  python -m app.scripts.fix_broken_links
  python -m app.scripts.fix_broken_links --apply
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.scripts.apply_field_changes import load_field_changes_csv
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.field_evidence import create_field_evidence

logger = logging.getLogger(__name__)

DEFAULT_CSVS = (
    Path("verification/reports/ched_unifast/field_changes.csv"),
    Path("verification/reports/dost/field_changes.csv"),
)

LINK_FIELDS = frozenset({"primary_link", "link"})
STATUS_FIELDS = frozenset({"link_status", "data_status"})
APPLY_CONFIDENCE = frozenset({"verified", "partially_verified"})

COMMON_LINK_REWRITES: tuple[tuple[str, str], ...] = (
    ("https://ched.gov.ph/merit-scholarship", "https://legacy.ched.gov.ph/merit-scholarship/"),
    ("https://ched.gov.ph", "https://legacy.ched.gov.ph/"),
    ("https://ugs.science-scholarships.ph", "https://ugrad.science-scholarships.ph"),
    ("https://science-scholarships.ph", "https://www.science-scholarships.ph/"),
    ("https://unifast.gov.ph", "https://unifast.gov.ph/tes.html"),
)


@dataclass
class LinkOutcome:
    scholarship_id: int
    field: str
    action: str
    result: str
    detail: str = ""


@dataclass
class LinkFixSummary:
    applied: int = 0
    skipped_idempotent: int = 0
    skipped_low_confidence: int = 0
    skipped_missing: int = 0
    skipped_drift: int = 0
    pattern_applied: int = 0
    dry_run: bool = True
    outcomes: list[LinkOutcome] = field(default_factory=list)


def _normalize_url(url: str | None) -> str:
    return (url or "").strip().rstrip("/")


def _rewrite_link(url: str | None) -> str | None:
    if not url:
        return None
    normalized = url.strip()
    for old, new in COMMON_LINK_REWRITES:
        old_base = old.rstrip("/")
        if normalized.rstrip("/") == old_base:
            return new
        prefix = old_base + "/"
        if normalized.startswith(prefix):
            suffix = normalized[len(old_base) :]
            # Avoid double-appending when the target path is already present.
            if new.rstrip("/") in normalized.rstrip("/"):
                return normalized
            return new.rstrip("/") + suffix
    parsed = urlparse(normalized)
    if parsed.netloc == "science-scholarships.ph":
        return normalized.replace("://science-scholarships.ph", "://www.science-scholarships.ph", 1)
    return None


def _extract_csv_fixes(csv_paths: list[Path]) -> list[dict[str, str]]:
    fixes: list[dict[str, str]] = []
    for path in csv_paths:
        if not path.exists():
            logger.warning("Skipping missing CSV: %s", path)
            continue
        rows = load_field_changes_csv(path)
        for row in rows:
            field_name = (row.get("field") or "").strip()
            if field_name not in LINK_FIELDS | STATUS_FIELDS:
                continue
            action = (row.get("action") or "").strip().lower()
            if action not in ("update", "confirm_unchanged"):
                continue
            if action == "confirm_unchanged":
                continue
            confidence = (row.get("confidence") or "").strip().lower()
            if confidence not in APPLY_CONFIDENCE:
                continue
            official = (row.get("official_value") or "").strip()
            if not official or official.lower() == "cannot_verify":
                continue
            fixes.append(row)
    return fixes


def _apply_value(
    db: Session,
    scholarship: models.Scholarship,
    column: str,
    new_value: Any,
    row: dict[str, str],
    *,
    dry_run: bool,
    summary: LinkFixSummary,
    action_label: str = "csv",
) -> None:
    sid = scholarship.id
    current = getattr(scholarship, column, None)
    if str(current or "").strip() == str(new_value or "").strip():
        summary.skipped_idempotent += 1
        summary.outcomes.append(
            LinkOutcome(sid, column, action_label, "skipped_idempotent", "already set")
        )
        return

    summary.applied += 1
    summary.outcomes.append(
        LinkOutcome(
            sid,
            column,
            action_label,
            "applied" if not dry_run else "dry_run",
            f"{current!r} -> {new_value!r}",
        )
    )
    if dry_run:
        return

    setattr(scholarship, column, new_value)
    scholarship.verification_source = scholarship.verification_source or "link_fix_import"
    create_field_evidence(
        db,
        scholarship_id=sid,
        field_key=column,
        value_snapshot=new_value,
        source_url=row.get("source_url") or None,
        source_type="link_fix_import",
        evidence_snippet=row.get("evidence_snippet") or None,
        confidence=1.0 if row.get("confidence") == "verified" else 0.75,
    )


def apply_link_fixes(
    db: Session,
    csv_paths: list[Path],
    *,
    dry_run: bool = True,
) -> LinkFixSummary:
    summary = LinkFixSummary(dry_run=dry_run)
    fixes = _extract_csv_fixes(csv_paths)
    touched_link_ids: set[int] = set()

    for row in fixes:
        sid_text = (row.get("id") or "").strip()
        if not sid_text.isdigit():
            continue
        sid = int(sid_text)
        scholarship = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if scholarship is None:
            summary.skipped_missing += 1
            summary.outcomes.append(
                LinkOutcome(sid, row.get("field", ""), "csv", "skipped_missing", "not found")
            )
            continue

        csv_field = (row.get("field") or "").strip()
        official = (row.get("official_value") or "").strip()
        isk_value = (row.get("iskconnect_value") or "").strip()

        if csv_field in LINK_FIELDS:
            column = "link"
            current = (scholarship.link or "").strip()
            if isk_value and current and _normalize_url(current) != _normalize_url(isk_value):
                summary.skipped_drift += 1
                summary.outcomes.append(
                    LinkOutcome(
                        sid,
                        column,
                        "csv",
                        "skipped_drift",
                        f"DB link {current!r} != CSV iskconnect_value {isk_value!r}",
                    )
                )
                continue
            _apply_value(db, scholarship, column, official, row, dry_run=dry_run, summary=summary)
            touched_link_ids.add(sid)
            if not dry_run:
                scholarship.dedupe_key = scholarship_dedupe_key(
                    scholarship.title or "",
                    scholarship.provider,
                    scholarship.link,
                )
        elif csv_field in STATUS_FIELDS:
            _apply_value(db, scholarship, csv_field, official, row, dry_run=dry_run, summary=summary)

    for scholarship in db.query(models.Scholarship).all():
        rewritten = _rewrite_link(scholarship.link)
        if not rewritten:
            continue
        current = (scholarship.link or "").strip()
        if _normalize_url(current) == _normalize_url(rewritten):
            continue
        pseudo_row = {
            "source_url": scholarship.link,
            "evidence_snippet": "common URL migration pattern",
            "confidence": "verified",
        }
        _apply_value(
            db,
            scholarship,
            "link",
            rewritten,
            pseudo_row,
            dry_run=dry_run,
            summary=summary,
            action_label="pattern",
        )
        summary.pattern_applied += 1
        if scholarship.link_status in (None, "", "broken", "timeout"):
            _apply_value(
                db,
                scholarship,
                "link_status",
                "ok",
                pseudo_row,
                dry_run=dry_run,
                summary=summary,
                action_label="pattern",
            )
        if not dry_run:
            scholarship.dedupe_key = scholarship_dedupe_key(
                scholarship.title or "",
                scholarship.provider,
                scholarship.link,
            )

    if not dry_run:
        db.commit()

    return summary


def print_summary(summary: LinkFixSummary) -> None:
    mode = "DRY RUN" if summary.dry_run else "APPLIED"
    print(f"fix_broken_links ({mode})")
    print(f"  applied: {summary.applied}")
    print(f"  pattern_applied: {summary.pattern_applied}")
    print(f"  skipped_idempotent: {summary.skipped_idempotent}")
    print(f"  skipped_drift: {summary.skipped_drift}")
    print(f"  skipped_missing: {summary.skipped_missing}")
    for outcome in summary.outcomes:
        if outcome.result not in ("skipped_idempotent",):
            print(
                f"  id={outcome.scholarship_id} {outcome.field} "
                f"[{outcome.action}] {outcome.result}: {outcome.detail}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix broken scholarship links from verification CSVs")
    parser.add_argument(
        "--csv",
        type=Path,
        action="append",
        dest="csvs",
        help="field_changes.csv path (repeatable; defaults to ched_unifast + dost)",
    )
    parser.add_argument("--apply", action="store_true", help="Persist changes (default dry-run)")
    args = parser.parse_args()

    csv_paths = args.csvs or list(DEFAULT_CSVS)
    db = SessionLocal()
    try:
        summary = apply_link_fixes(db, csv_paths, dry_run=not args.apply)
        print_summary(summary)
    finally:
        db.close()


if __name__ == "__main__":
    main()
