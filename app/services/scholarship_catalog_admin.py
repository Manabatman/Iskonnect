"""Admin catalog operations: permanent delete, merge, restore, bulk actions."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

from sqlalchemy.orm import Session

from app import models
from app.scholarship_cache import invalidate_scholarship_cache
from app.storage.supabase_storage import StorageNotConfiguredError, delete_object, storage_path_from_public_url
from app.utils.application_status import sync_application_status
from app.utils.editorial_state import ARCHIVED, NEEDS_REVIEW, PUBLISHED, apply_editorial_state
from app.utils.field_evidence import create_field_evidence
from app.utils.opportunity_quality import apply_quality_scores
from app.utils.publishability_rules import validate_scholarship_publish_rules
from app.utils.scholarship_versioning import diff_snapshots, record_scholarship_version, snapshot_scholarship_row
from app.utils.timezone import utc_now_naive

logger = logging.getLogger(__name__)

BulkAction = Literal["deactivate", "permanent_delete", "restore", "verify", "needs_review"]

MERGEABLE_SCALAR_FIELDS: tuple[str, ...] = (
    "description",
    "link",
    "provider",
    "source",
    "provider_type",
    "scholarship_type",
    "deadline_note",
    "deadline_source_url",
    "deadline_precision",
    "verification_source",
    "eligible_levels",
    "eligible_regions",
    "eligible_cities",
    "eligible_school_types",
    "eligible_schools",
    "eligible_school_systems",
    "eligible_school_categories",
    "eligible_year_levels",
    "eligible_enrollment_status",
    "eligible_courses_psced",
    "eligible_courses_specific",
    "max_income_threshold",
    "min_gwa_normalized",
    "min_age",
    "max_age",
    "priority_groups",
    "required_documents",
    "benefit_miscellaneous",
    "benefit_total_value",
    "benefit_allowance_monthly",
    "cycle_type",
    "academic_year_target",
    "image_url",
    "image_alt",
)


class CatalogAdminError(Exception):
    """Raised when a catalog admin operation is rejected."""

    def __init__(self, message: str, *, code: str = "invalid") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


@dataclass
class DeleteResult:
    scholarship_id: int
    title: str
    cascaded_counts: dict[str, int] = field(default_factory=dict)


@dataclass
class MergeDeleteResult:
    canonical_id: int
    duplicate_id: int
    fields_merged: list[str] = field(default_factory=list)
    saved_migrated: int = 0
    applications_migrated: int = 0
    evidence_migrated: int = 0
    notifications_migrated: int = 0
    deleted: bool = False
    dry_run: bool = True


@dataclass
class BulkItemResult:
    id: int
    status: Literal["succeeded", "failed"]
    reason: str = ""


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, bool):
        return False
    return False


def can_permanently_delete(scholarship: models.Scholarship) -> bool:
    if scholarship.is_active is False:
        return True
    return (scholarship.editorial_state or "").strip().lower() == ARCHIVED


def _related_counts(db: Session, scholarship_id: int) -> dict[str, int]:
    return {
        "field_evidence": db.query(models.FieldEvidence)
        .filter(models.FieldEvidence.scholarship_id == scholarship_id)
        .count(),
        "match_results": db.query(models.MatchResult)
        .filter(models.MatchResult.scholarship_id == scholarship_id)
        .count(),
        "saved_scholarships": db.query(models.SavedScholarship)
        .filter(models.SavedScholarship.scholarship_id == scholarship_id)
        .count(),
        "scholarship_reports": db.query(models.ScholarshipReport)
        .filter(models.ScholarshipReport.scholarship_id == scholarship_id)
        .count(),
        "scholarship_versions": db.query(models.ScholarshipVersion)
        .filter(models.ScholarshipVersion.scholarship_id == scholarship_id)
        .count(),
        "notifications": db.query(models.Notification)
        .filter(models.Notification.scholarship_id == scholarship_id)
        .count(),
        "applications": db.query(models.Application)
        .filter(models.Application.scholarship_id == scholarship_id)
        .count(),
    }


def deactivate_scholarship(db: Session, scholarship: models.Scholarship) -> None:
    scholarship.is_active = False
    sync_application_status(scholarship)


def _assert_rule_publishable(scholarship: models.Scholarship, db: Session) -> None:
    from app.matching.scholarship_enrichment import attach_scholarship_join_fields
    from app.serialization.scholarship import scholarship_to_catalog_dict

    payload = attach_scholarship_join_fields(db, scholarship_to_catalog_dict(scholarship))
    errors = validate_scholarship_publish_rules(payload)
    if errors:
        raise CatalogAdminError("; ".join(errors))


def restore_scholarship(db: Session, scholarship: models.Scholarship) -> None:
    _assert_rule_publishable(scholarship, db)
    apply_editorial_state(scholarship, PUBLISHED)
    sync_application_status(scholarship)
    apply_quality_scores(scholarship, db)


def mark_needs_review(db: Session, scholarship: models.Scholarship) -> None:
    apply_editorial_state(scholarship, NEEDS_REVIEW)
    scholarship.data_status = "needs_review"
    sync_application_status(scholarship)


def verify_refresh(db: Session, scholarship: models.Scholarship) -> None:
    _assert_rule_publishable(scholarship, db)
    scholarship.last_verified_at = utc_now_naive()
    apply_editorial_state(scholarship, PUBLISHED)
    apply_quality_scores(scholarship, db)
    sync_application_status(scholarship)


def _delete_storage_image(scholarship: models.Scholarship) -> None:
    old_path = storage_path_from_public_url(scholarship.image_url)
    if not old_path:
        return
    try:
        delete_object(old_path)
    except StorageNotConfiguredError:
        pass
    except Exception:
        logger.warning("scholarship_storage_delete_failed path=%s", old_path)


def _migrate_saved_references(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
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


def _migrate_applications(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.Application).filter(models.Application.scholarship_id == from_id).all()
    count = 0
    for row in rows:
        exists = (
            db.query(models.Application)
            .filter(
                models.Application.user_id == row.user_id,
                models.Application.scholarship_id == to_id,
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


def _migrate_field_evidence(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.FieldEvidence).filter(models.FieldEvidence.scholarship_id == from_id).all()
    if not dry_run:
        for row in rows:
            row.scholarship_id = to_id
    return len(rows)


def _migrate_notifications(db: Session, *, from_id: int, to_id: int, dry_run: bool) -> int:
    rows = db.query(models.Notification).filter(models.Notification.scholarship_id == from_id).all()
    if not dry_run:
        for row in rows:
            row.scholarship_id = to_id
    return len(rows)


def _merge_richer_fields(
    db: Session,
    canonical: models.Scholarship,
    duplicate: models.Scholarship,
    *,
    dry_run: bool,
) -> list[str]:
    merged: list[str] = []
    before = snapshot_scholarship_row(canonical)
    for field_name in MERGEABLE_SCALAR_FIELDS:
        if not hasattr(canonical, field_name):
            continue
        canon_val = getattr(canonical, field_name)
        dup_val = getattr(duplicate, field_name)
        if _is_empty(canon_val) and not _is_empty(dup_val):
            merged.append(field_name)
            if not dry_run:
                setattr(canonical, field_name, dup_val)
    if merged and not dry_run:
        after = snapshot_scholarship_row(canonical)
        changes = diff_snapshots(before, after)
        if changes:
            record_scholarship_version(db, scholarship_id=canonical.id, changes=changes, changed_by=None)
        create_field_evidence(
            db,
            scholarship_id=canonical.id,
            field_key="merge",
            value_snapshot=f"merged_from:{duplicate.id}",
            source_url=duplicate.link,
            source_type="duplicate_merge",
            evidence_snippet=f"Merged {len(merged)} field(s) from scholarship id={duplicate.id} before delete",
            confidence=1.0,
        )
    return merged


def _delete_related_rows(db: Session, scholarship_id: int) -> None:
    """Remove dependent rows when DB CASCADE is missing or incomplete."""
    db.query(models.SavedScholarship).filter(
        models.SavedScholarship.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.Application).filter(
        models.Application.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.FieldEvidence).filter(
        models.FieldEvidence.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.Notification).filter(
        models.Notification.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.MatchResult).filter(
        models.MatchResult.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.ScholarshipReport).filter(
        models.ScholarshipReport.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)
    db.query(models.ScholarshipVersion).filter(
        models.ScholarshipVersion.scholarship_id == scholarship_id
    ).delete(synchronize_session=False)


def permanently_delete_scholarship(
    db: Session,
    scholarship_id: int,
    *,
    skip_inactive_guard: bool = False,
) -> DeleteResult:
    scholarship = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise CatalogAdminError("Scholarship not found", code="not_found")
    if not skip_inactive_guard and not can_permanently_delete(scholarship):
        raise CatalogAdminError(
            "Deactivate this scholarship before permanent deletion",
            code="still_active",
        )

    title = scholarship.title or ""
    cascaded = _related_counts(db, scholarship_id)
    _delete_storage_image(scholarship)
    _delete_related_rows(db, scholarship_id)
    db.delete(scholarship)
    db.flush()
    invalidate_scholarship_cache()
    return DeleteResult(scholarship_id=scholarship_id, title=title, cascaded_counts=cascaded)


def merge_before_delete(
    db: Session,
    canonical_id: int,
    duplicate_id: int,
    *,
    dry_run: bool = False,
) -> MergeDeleteResult:
    if canonical_id == duplicate_id:
        raise CatalogAdminError("Canonical and duplicate ids must differ")

    canonical = db.query(models.Scholarship).filter(models.Scholarship.id == canonical_id).first()
    duplicate = db.query(models.Scholarship).filter(models.Scholarship.id == duplicate_id).first()
    if not canonical:
        raise CatalogAdminError(f"Canonical scholarship {canonical_id} not found", code="not_found")
    if not duplicate:
        raise CatalogAdminError(f"Duplicate scholarship {duplicate_id} not found", code="not_found")

    result = MergeDeleteResult(
        canonical_id=canonical_id,
        duplicate_id=duplicate_id,
        dry_run=dry_run,
    )
    result.fields_merged = _merge_richer_fields(db, canonical, duplicate, dry_run=dry_run)
    result.saved_migrated = _migrate_saved_references(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
    result.applications_migrated = _migrate_applications(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
    result.evidence_migrated = _migrate_field_evidence(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)
    result.notifications_migrated = _migrate_notifications(db, from_id=duplicate_id, to_id=canonical_id, dry_run=dry_run)

    if not dry_run:
        if can_permanently_delete(duplicate) is False:
            apply_editorial_state(duplicate, ARCHIVED)
            duplicate.is_active = False
            duplicate.application_status = "archived"
            duplicate.data_status = "expired"
            sync_application_status(duplicate)
        db.flush()
        permanently_delete_scholarship(db, duplicate_id, skip_inactive_guard=True)
        result.deleted = True

    return result


def run_bulk_action(db: Session, ids: list[int], action: BulkAction) -> list[BulkItemResult]:
    results: list[BulkItemResult] = []
    for sid in ids:
        scholarship = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if not scholarship:
            results.append(BulkItemResult(id=sid, status="failed", reason="not found"))
            continue
        try:
            if action == "deactivate":
                deactivate_scholarship(db, scholarship)
            elif action == "permanent_delete":
                if not can_permanently_delete(scholarship):
                    results.append(
                        BulkItemResult(id=sid, status="failed", reason="still active — deactivate first")
                    )
                    continue
                permanently_delete_scholarship(db, sid, skip_inactive_guard=True)
            elif action == "restore":
                restore_scholarship(db, scholarship)
            elif action == "verify":
                verify_refresh(db, scholarship)
            elif action == "needs_review":
                mark_needs_review(db, scholarship)
            else:
                results.append(BulkItemResult(id=sid, status="failed", reason=f"unknown action: {action}"))
                continue
            results.append(BulkItemResult(id=sid, status="succeeded"))
        except CatalogAdminError as exc:
            results.append(BulkItemResult(id=sid, status="failed", reason=exc.message))
        except Exception as exc:
            results.append(BulkItemResult(id=sid, status="failed", reason=str(exc)))
    invalidate_scholarship_cache()
    return results
