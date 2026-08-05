"""
ISKONNECT Public Beta audit remediation orchestrator.

Idempotent, phased remediation per verification audit (2026-08-03).

Usage:
  python -m app.scripts.audit_remediation
  python -m app.scripts.audit_remediation --apply
  python -m app.scripts.audit_remediation --phase merge --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.jobs.link_checker import _head_status
from app.scholarship_cache import invalidate_scholarship_cache
from app.scripts.apply_field_changes import apply_field_changes, load_field_changes_csv
from app.services.scholarship_catalog_admin import CatalogAdminError, merge_before_delete
from app.utils.application_status import sync_application_status
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.editorial_state import ARCHIVED, PUBLISHED, apply_editorial_state
from app.utils.field_evidence import create_field_evidence
from app.utils.scholarship_versioning import record_scholarship_version

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "verification" / "reports" / "audit_2026_08" / "remediation_manifest.json"
REPORT_PATH = ROOT / "data" / "audit_remediation_report.json"


@dataclass
class ChangeLogEntry:
    scholarship_id: int
    title: str
    fields_changed: list[str]
    reason: str
    audit_reference: str
    live_verified: bool = False


@dataclass
class RemediationReport:
    dry_run: bool = True
    started_at: str = ""
    finished_at: str = ""
    merged: list[dict[str, Any]] = field(default_factory=list)
    archived: list[dict[str, Any]] = field(default_factory=list)
    created: list[dict[str, Any]] = field(default_factory=list)
    urls_repaired: list[dict[str, Any]] = field(default_factory=list)
    metadata_applied: dict[str, int] = field(default_factory=dict)
    skipped: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    manual_review: list[dict[str, Any]] = field(default_factory=list)
    change_log: list[ChangeLogEntry] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=dict)


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _is_archived(row: models.Scholarship) -> bool:
    return row.is_active is False or (row.editorial_state or "").strip().lower() == ARCHIVED


def _migrate_match_results(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.MatchResult).filter(models.MatchResult.scholarship_id == from_id).all()
    if not dry_run:
        for row in rows:
            row.scholarship_id = to_id
    return len(rows)


def _migrate_saved(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.SavedScholarship).filter(models.SavedScholarship.scholarship_id == from_id).all()
    count = 0
    for row in rows:
        exists = (
            db.query(models.SavedScholarship)
            .filter(
                models.SavedScholarship.user_id == row.user_id,
                models.SavedScholarship.scholarship_id == to_id,
            )
            .first()
        )
        if not dry_run:
            if exists:
                db.delete(row)
            else:
                row.scholarship_id = to_id
        count += 1
    return count


def _archive_row(
    db: Session,
    row: models.Scholarship,
    *,
    reason: str,
    dry_run: bool,
    report: RemediationReport,
) -> None:
    if _is_archived(row):
        report.skipped.append({"id": row.id, "action": "archive", "reason": "already archived"})
        return
    report.archived.append({"id": row.id, "title": row.title, "reason": reason})
    report.change_log.append(
        ChangeLogEntry(
            scholarship_id=row.id,
            title=row.title or "",
            fields_changed=["editorial_state", "is_active", "application_status"],
            reason=reason,
            audit_reference="Program Archival",
        )
    )
    if dry_run:
        return
    apply_editorial_state(row, ARCHIVED)
    row.is_active = False
    row.application_status = "archived"
    sync_application_status(row)
    create_field_evidence(
        db,
        scholarship_id=row.id,
        field_key="archive",
        value_snapshot="archived",
        source_type="audit_remediation",
        evidence_snippet=reason,
        confidence=1.0,
    )


def phase_merge(db: Session, manifest: dict[str, Any], *, dry_run: bool, report: RemediationReport) -> None:
    pairs = manifest.get("merge_pairs") or {}
    for canonical_s, duplicate_s in pairs.items():
        canonical_id = int(canonical_s)
        duplicate_id = int(duplicate_s)
        canonical = db.query(models.Scholarship).filter(models.Scholarship.id == canonical_id).first()
        duplicate = db.query(models.Scholarship).filter(models.Scholarship.id == duplicate_id).first()
        if not canonical or not duplicate:
            if canonical and not duplicate:
                report.skipped.append(
                    {
                        "id": duplicate_id,
                        "action": "merge",
                        "reason": f"duplicate already removed; canonical {canonical_id} retained",
                    }
                )
                continue
            report.errors.append(
                {"phase": "merge", "canonical_id": canonical_id, "duplicate_id": duplicate_id, "error": "missing row"}
            )
            continue

        if _is_archived(duplicate) and duplicate_id in {131, 132, 130}:
            migrated_mr = _migrate_match_results(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
            migrated_sv = _migrate_saved(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
            report.skipped.append(
                {
                    "id": duplicate_id,
                    "action": "merge",
                    "reason": f"already archived; migrated match_results={migrated_mr}, saved={migrated_sv}",
                }
            )
            report.merged.append(
                {
                    "canonical_id": canonical_id,
                    "duplicate_id": duplicate_id,
                    "status": "fk_migrated_only",
                    "match_results": migrated_mr,
                    "saved": migrated_sv,
                }
            )
            continue

        if _is_archived(duplicate):
            migrated_mr = _migrate_match_results(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
            migrated_sv = _migrate_saved(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
            report.merged.append(
                {
                    "canonical_id": canonical_id,
                    "duplicate_id": duplicate_id,
                    "status": "archived_duplicate_fk_migrated",
                    "match_results": migrated_mr,
                    "saved": migrated_sv,
                }
            )
            if not dry_run:
                create_field_evidence(
                    db,
                    scholarship_id=duplicate_id,
                    field_key="merge",
                    value_snapshot=str(canonical_id),
                    source_type="audit_remediation",
                    evidence_snippet=f"FK refs migrated to canonical {canonical_id}",
                    confidence=1.0,
                )
            continue

        try:
            result = merge_before_delete(db, canonical_id, duplicate_id, dry_run=dry_run)
            report.merged.append(
                {
                    "canonical_id": canonical_id,
                    "duplicate_id": duplicate_id,
                    "fields_merged": result.fields_merged,
                    "deleted": result.deleted,
                    "dry_run": result.dry_run,
                }
            )
            report.change_log.append(
                ChangeLogEntry(
                    scholarship_id=canonical_id,
                    title=canonical.title or "",
                    fields_changed=["merge"] + result.fields_merged,
                    reason=f"Merged duplicate id={duplicate_id}",
                    audit_reference="Duplicate Consolidation",
                )
            )
        except CatalogAdminError as exc:
            report.errors.append(
                {
                    "phase": "merge",
                    "canonical_id": canonical_id,
                    "duplicate_id": duplicate_id,
                    "error": exc.message,
                }
            )


def _children_exist(db: Session, child_ids: list[int]) -> bool:
    if not child_ids:
        return True
    if isinstance(child_ids[0], str):
        return False
    count = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.id.in_(child_ids), models.Scholarship.is_active != False)  # noqa: E712
        .scalar()
    )
    return (count or 0) >= len(child_ids)


def phase_archive(db: Session, manifest: dict[str, Any], *, dry_run: bool, report: RemediationReport) -> None:
    umbrella = manifest.get("umbrella_archive_when_children_exist") or {}
    for sid in manifest.get("archive_ids") or []:
        row = db.query(models.Scholarship).filter(models.Scholarship.id == int(sid)).first()
        if not row:
            report.errors.append({"phase": "archive", "id": sid, "error": "not found"})
            continue
        child_key = str(sid)
        if child_key in umbrella:
            children = umbrella[child_key]
            if isinstance(children[0], str):
                pass
            elif not _children_exist(db, children):
                report.skipped.append({"id": sid, "action": "archive", "reason": "child records missing"})
                continue
        _archive_row(db, row, reason="Audit archival directive", dry_run=dry_run, report=report)

    for sid in manifest.get("archive_after_split_ids") or []:
        row = db.query(models.Scholarship).filter(models.Scholarship.id == int(sid)).first()
        if not row:
            continue
        child_spec = umbrella.get(str(sid), [])
        if isinstance(child_spec[0], str):
            titles = {c.upper() for c in child_spec}
            found = (
                db.query(func.count(models.Scholarship.id))
                .filter(
                    models.Scholarship.is_active != False,  # noqa: E712
                    models.Scholarship.title.ilike("%ASTHRDP%")
                    | models.Scholarship.title.ilike("%ERDT%")
                    | models.Scholarship.title.ilike("%CBPSME%")
                    | models.Scholarship.title.ilike("%STRAND%"),
                )
                .scalar()
            )
            if (found or 0) < len(titles):
                report.skipped.append({"id": sid, "action": "archive", "reason": "DOST graduate splits incomplete"})
                continue
        _archive_row(db, row, reason="Umbrella superseded by split records", dry_run=dry_run, report=report)


def _normalize_url(url: str) -> str:
    return (url or "").strip().rstrip("/")


def phase_urls(db: Session, manifest: dict[str, Any], *, dry_run: bool, report: RemediationReport) -> None:
    for entry in manifest.get("url_replacements") or []:
        replacement = entry["replacement"]
        status, _detail = _head_status(replacement)
        live_ok = status == "ok"
        for sid in entry.get("scholarship_ids") or []:
            row = db.query(models.Scholarship).filter(models.Scholarship.id == int(sid)).first()
            if not row or not row.link:
                continue
            current = row.link.strip()
            matched = any(sub in current for sub in entry.get("match_substrings") or [])
            if entry.get("exact_only") and _normalize_url(current) == _normalize_url(replacement):
                report.skipped.append({"id": sid, "action": "url", "reason": "already updated"})
                continue
            if not matched and _normalize_url(current) != _normalize_url(replacement):
                if not any(sub in current for sub in entry.get("match_substrings") or []):
                    continue
            if _normalize_url(current) == _normalize_url(replacement):
                report.skipped.append({"id": sid, "action": "url", "reason": "already correct"})
                continue
            if entry.get("require_broken") and (row.link_status or "").lower() not in ("broken", "timeout", "unchecked", ""):
                if _normalize_url(current) != _normalize_url(replacement):
                    pass
            if not live_ok:
                report.manual_review.append(
                    {"id": sid, "field": "link", "proposed": replacement, "reason": f"replacement HEAD={status}"}
                )
                continue
            report.urls_repaired.append({"id": sid, "from": current, "to": replacement, "live_verified": True})
            report.change_log.append(
                ChangeLogEntry(
                    scholarship_id=sid,
                    title=row.title or "",
                    fields_changed=["link", "link_status"],
                    reason="Audit URL remediation",
                    audit_reference="Endpoint Remediation",
                    live_verified=True,
                )
            )
            if dry_run:
                continue
            row.link = replacement
            row.link_status = "ok"
            row.data_status = "active" if (row.data_status or "") == "broken_link" else row.data_status
            row.dedupe_key = scholarship_dedupe_key(row.title or "", row.provider, row.link)
            create_field_evidence(
                db,
                scholarship_id=sid,
                field_key="link",
                value_snapshot=replacement,
                source_url=replacement,
                source_type="audit_remediation",
                evidence_snippet="Audit-verified URL replacement with live HEAD check",
                confidence=1.0,
            )


def phase_dost_splits(db: Session, manifest: dict[str, Any], *, dry_run: bool, report: RemediationReport) -> None:
    for spec in manifest.get("dost_graduate_splits") or []:
        title = spec["title"]
        link = spec.get("link")
        existing = (
            db.query(models.Scholarship)
            .filter(models.Scholarship.title.ilike(title[:40] + "%"))
            .first()
        )
        if existing:
            report.skipped.append({"title": title, "action": "create_split", "reason": f"exists id={existing.id}"})
            continue
        dedupe = scholarship_dedupe_key(title, spec.get("provider"), link)
        collision = db.query(models.Scholarship).filter(models.Scholarship.dedupe_key == dedupe).first()
        if collision:
            report.skipped.append({"title": title, "action": "create_split", "reason": f"dedupe_key match id={collision.id}"})
            continue
        report.created.append({"title": title, "provider": spec.get("provider")})
        report.change_log.append(
            ChangeLogEntry(
                scholarship_id=-1,
                title=title,
                fields_changed=["*"],
                reason="DOST Graduate umbrella decomposition",
                audit_reference="Umbrella Decomposition",
            )
        )
        if dry_run:
            continue
        levels = spec.get("eligible_levels") or ["Graduate"]
        row = models.Scholarship(
            title=title,
            provider=spec.get("provider"),
            provider_type=spec.get("provider_type"),
            scholarship_type=spec.get("scholarship_type"),
            link=link,
            description=spec.get("description"),
            eligible_levels=json.dumps(levels),
            cycle_type=spec.get("cycle_type"),
            deadline_precision=spec.get("deadline_precision"),
            is_active=True,
            editorial_state="published",
            application_status="expected_reopen",
            data_status="active",
            link_status="ok",
            verification_source="audit_remediation",
            last_verified_at=datetime.now(timezone.utc).replace(tzinfo=None),
            dedupe_key=dedupe,
            opportunity_type="scholarship",
        )
        db.add(row)
        db.flush()
        create_field_evidence(
            db,
            scholarship_id=row.id,
            field_key="title",
            value_snapshot=title,
            source_url=spec.get("source_url"),
            source_type="audit_remediation",
            evidence_snippet=spec.get("evidence_snippet"),
            confidence=1.0,
        )
        report.created[-1]["id"] = row.id
        report.change_log[-1].scholarship_id = row.id


def _consolidate_field_changes(manifest: dict[str, Any]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    rows: list[dict[str, str]] = []
    for rel in manifest.get("field_changes_csv_sources") or []:
        path = ROOT / rel
        if not path.exists():
            continue
        for row in load_field_changes_csv(path):
            key = (row.get("id", ""), row.get("field", ""))
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def phase_metadata(db: Session, manifest: dict[str, Any], *, dry_run: bool, report: RemediationReport) -> None:
    rows = _consolidate_field_changes(manifest)
    summary = apply_field_changes(db, rows, dry_run=dry_run)
    report.metadata_applied = {
        "applied": summary.applied,
        "skipped_idempotent": summary.skipped_idempotent,
        "skipped_confirm_unchanged": summary.skipped_confirm_unchanged,
        "skipped_missing_scholarship": summary.skipped_missing_scholarship,
    }
    for outcome in summary.outcomes:
        if outcome.result in ("applied", "dry_run"):
            report.change_log.append(
                ChangeLogEntry(
                    scholarship_id=outcome.scholarship_id,
                    title="",
                    fields_changed=[outcome.csv_field],
                    reason=outcome.detail,
                    audit_reference="Field Changes Bundle",
                )
            )

    for item in manifest.get("closed_cycle_updates") or []:
        sid = int(item["id"])
        row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if not row:
            continue
        target = item["application_status"]
        if (row.application_status or "") == target:
            report.skipped.append({"id": sid, "action": "closed_cycle", "reason": "already set"})
            continue
        if dry_run:
            report.metadata_applied.setdefault("closed_cycle", 0)
            report.metadata_applied["closed_cycle"] += 1
            continue
        row.application_status = target
        sync_application_status(row)
        if target == "archived":
            apply_editorial_state(row, ARCHIVED)
            row.is_active = False


def phase_promote(db: Session, *, dry_run: bool, report: RemediationReport) -> None:
    rows = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.is_active != False)  # noqa: E712
        .filter(models.Scholarship.editorial_state == "needs_review")
        .filter(models.Scholarship.link_status == "ok")
        .all()
    )
    promoted = 0
    for row in rows:
        if (row.link_status or "").lower() == "broken":
            continue
        if (row.application_status or "") in ("needs_verification",):
            continue
        promoted += 1
        if not dry_run:
            apply_editorial_state(row, PUBLISHED)
            sync_application_status(row)
    report.metadata_applied["promoted_to_published"] = promoted


def run_validation(db: Session) -> dict[str, Any]:
    dup_titles = db.execute(
        text(
            """
            SELECT title, COUNT(*) AS n FROM scholarships
            WHERE is_active IS NOT FALSE GROUP BY title HAVING COUNT(*) > 1
            """
        )
    ).fetchall()
    orphan_mr = db.execute(
        text(
            """
            SELECT COUNT(*) FROM match_results mr
            WHERE NOT EXISTS (SELECT 1 FROM scholarships s WHERE s.id = mr.scholarship_id)
            """
        )
    ).scalar()
    archived_visible = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active != False, models.Scholarship.editorial_state == ARCHIVED)  # noqa: E712
        .scalar()
    )
    broken_active = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active != False, models.Scholarship.link_status == "broken")  # noqa: E712
        .scalar()
    )
    active = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active != False)  # noqa: E712
        .scalar()
    )
    archived = (
        db.query(func.count(models.Scholarship.id))
        .filter(models.Scholarship.is_active == False)  # noqa: E712
        .scalar()
    )
    return {
        "duplicate_active_titles": [{"title": r[0], "count": r[1]} for r in dup_titles],
        "orphan_match_results": int(orphan_mr or 0),
        "archived_still_active_flag": int(archived_visible or 0),
        "broken_links_active": int(broken_active or 0),
        "active_count": int(active or 0),
        "archived_count": int(archived or 0),
    }


def phase_migration_v1(db: Session, *, dry_run: bool, report: RemediationReport) -> None:
    """Apply migration v1 eligibility backfill after audit metadata phase."""
    from app.scripts.migration_v1_backfill import run_backfill

    backfill = run_backfill(apply=not dry_run, db=db)
    report.metadata_applied["migration_v1_field_updates"] = len(backfill.field_updates)
    report.metadata_applied["migration_v1_consortium"] = len(backfill.consortium_updates)
    report.metadata_applied["migration_v1_conflicts"] = len(backfill.conflict_links)
    report.metadata_applied["migration_v1_affiliations"] = len(backfill.affiliation_links)
    report.errors.extend(backfill.errors)


PHASES = ("merge", "archive", "split", "urls", "metadata", "migration_v1", "promote", "validate")


def run_remediation(*, apply: bool = False, phases: list[str] | None = None) -> RemediationReport:
    manifest = _load_manifest()
    selected = phases or list(PHASES)
    report = RemediationReport(dry_run=not apply, started_at=datetime.now(timezone.utc).isoformat())
    db = SessionLocal()
    try:
        if "merge" in selected:
            phase_merge(db, manifest, dry_run=not apply, report=report)
        if "split" in selected:
            phase_dost_splits(db, manifest, dry_run=not apply, report=report)
        if "urls" in selected:
            phase_urls(db, manifest, dry_run=not apply, report=report)
        if "metadata" in selected:
            phase_metadata(db, manifest, dry_run=not apply, report=report)
        if "migration_v1" in selected:
            phase_migration_v1(db, dry_run=not apply, report=report)
        if "archive" in selected:
            phase_archive(db, manifest, dry_run=not apply, report=report)
        if "promote" in selected:
            phase_promote(db, dry_run=not apply, report=report)
        if apply:
            db.commit()
            invalidate_scholarship_cache()
        else:
            db.rollback()
        if "validate" in selected:
            report.validation = run_validation(db)
    except Exception as exc:
        db.rollback()
        report.errors.append({"phase": "fatal", "error": str(exc)})
        raise
    finally:
        report.finished_at = datetime.now(timezone.utc).isoformat()
        db.close()
    if report.errors and not apply:
        pass  # dry-run may log expected probe errors
    return report


def write_report(report: RemediationReport) -> None:
    payload = asdict(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path = ROOT / "data" / "audit_remediation_report.md"
    lines = [
        "# ISKONNECT Audit Remediation Report",
        "",
        f"**Started:** {report.started_at}",
        f"**Finished:** {report.finished_at}",
        f"**Mode:** {'APPLY' if not report.dry_run else 'DRY RUN'}",
        "",
        "## Summary",
        "",
        f"- Merged: {len(report.merged)}",
        f"- Archived: {len(report.archived)}",
        f"- Created: {len(report.created)}",
        f"- URLs repaired: {len(report.urls_repaired)}",
        f"- Skipped: {len(report.skipped)}",
        f"- Errors: {len(report.errors)}",
        f"- Manual review: {len(report.manual_review)}",
        "",
        "## Data Quality",
        "",
        json.dumps(report.validation, indent=2),
        "",
        "## Metadata",
        "",
        json.dumps(report.metadata_applied, indent=2),
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit remediation orchestrator")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--phase", action="append", choices=PHASES, dest="phases")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    report = run_remediation(apply=args.apply, phases=args.phases)
    write_report(report)
    print(json.dumps(asdict(report), indent=2, default=str))
    fatal = [e for e in report.errors if e.get("phase") == "fatal"]
    if fatal:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
