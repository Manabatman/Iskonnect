"""Shared scholarship row persistence from validated schemas."""

from __future__ import annotations

import json
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.sanitize import strip_tags
from app.utils.scholarship_versioning import (
    diff_snapshots,
    record_scholarship_version,
    snapshot_scholarship_row,
)
from app.utils.application_status import sync_application_status
from app.utils.opportunity_quality import apply_quality_scores
from app.utils.editorial_state import apply_editorial_state, sync_legacy_fields_from_editorial, PUBLISHED
from app.utils.timezone import utc_now_naive
from app.taxonomy.regions import canonical_region_label
from app.taxonomy.priority_groups import normalize_priority_groups
from app.taxonomy.school_registry import resolve_school_ids


class PersistResult:
    """Outcome of persist_scholarship_from_schema."""

    def __init__(self, row: models.Scholarship, *, created: bool):
        self.row = row
        self.created = created


def find_existing_scholarship(
    db: Session,
    scholarship: schemas.Scholarship,
) -> models.Scholarship | None:
    """Find live row by dedupe_key, then by normalized title + provider."""
    dedupe = scholarship_dedupe_key(scholarship.title, scholarship.provider, scholarship.link)
    row = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.dedupe_key == dedupe)
        .first()
    )
    if row:
        return row
    want_t = (scholarship.title or "").strip().lower()
    want_p = (scholarship.provider or "").strip().lower()
    if not want_t:
        return None
    candidates = (
        db.query(models.Scholarship)
        .filter(func.lower(func.trim(models.Scholarship.title)) == want_t)
        .all()
    )
    for candidate in candidates:
        if (candidate.provider or "").strip().lower() == want_p:
            return candidate
    return None


def _normalize_data_status_on_import(
    scholarship: schemas.Scholarship,
    existing: models.Scholarship | None,
) -> str:
    """Align legacy past_deadline with expired; reactivate on new future deadline."""
    deadline = scholarship.application_deadline
    if deadline and deadline >= date.today():
        return "active"
    if deadline and deadline < date.today():
        return "expired"
    if existing and existing.data_status:
        if existing.data_status == "past_deadline":
            return "expired"
        return existing.data_status
    return "active"


def apply_schema_to_row(
    row: models.Scholarship,
    scholarship: schemas.Scholarship,
    *,
    preserve_images: bool = True,
    verification_source: str | None = None,
    is_import: bool = False,
) -> None:
    """Apply validated schema fields onto an ORM row."""
    row.title = strip_tags(scholarship.title) or scholarship.title
    row.provider = strip_tags(scholarship.provider) or scholarship.provider if scholarship.provider else None
    row.source = strip_tags(scholarship.source) or scholarship.source if scholarship.source else None
    row.dedupe_key = scholarship_dedupe_key(scholarship.title, scholarship.provider, scholarship.link)
    row.countries = ",".join(scholarship.countries or [])
    row.regions = ",".join(
        canonical_region_label(r) or r for r in (scholarship.regions or []) if r
    )
    row.min_age = scholarship.min_age
    row.max_age = scholarship.max_age
    row.needs_tags = json.dumps(scholarship.needs_tags or [])
    row.level = scholarship.level
    row.link = scholarship.link
    row.description = (
        strip_tags(scholarship.description) or scholarship.description if scholarship.description else None
    )
    if not preserve_images or scholarship.image_url:
        if scholarship.image_url is not None:
            row.image_url = scholarship.image_url
    if not preserve_images or scholarship.image_alt:
        if scholarship.image_alt is not None:
            row.image_alt = strip_tags(scholarship.image_alt) or scholarship.image_alt
    row.provider_type = scholarship.provider_type
    row.scholarship_type = scholarship.scholarship_type
    row.eligible_levels = json.dumps(scholarship.eligible_levels or [])
    canon_regions = [
        canonical_region_label(r) or r
        for r in (scholarship.eligible_regions or scholarship.regions or [])
        if r and str(r).strip()
    ]
    row.eligible_regions = json.dumps(list(dict.fromkeys(canon_regions)))
    row.eligible_cities = json.dumps(scholarship.eligible_cities or [])
    row.residency_required = scholarship.residency_required or False
    row.eligible_school_types = json.dumps(scholarship.eligible_school_types or ["Public", "Private"])
    row.eligible_schools = json.dumps(resolve_school_ids(scholarship.eligible_schools or []))
    row.eligible_school_systems = json.dumps(scholarship.eligible_school_systems or [])
    row.eligible_school_categories = json.dumps(scholarship.eligible_school_categories or [])
    row.eligible_year_levels = json.dumps(scholarship.eligible_year_levels or [])
    row.eligible_enrollment_status = json.dumps(scholarship.eligible_enrollment_status or [])
    row.eligible_courses_psced = json.dumps(scholarship.eligible_courses_psced or [])
    row.eligible_courses_specific = json.dumps(scholarship.eligible_courses_specific or [])
    row.preferred_extracurriculars = json.dumps(scholarship.preferred_extracurriculars or [])
    row.preferred_awards = json.dumps(scholarship.preferred_awards or [])
    row.max_income_threshold = scholarship.max_income_threshold
    row.min_gwa_normalized = scholarship.min_gwa_normalized
    row.priority_groups = json.dumps(normalize_priority_groups(scholarship.priority_groups or []))
    row.members_only = scholarship.members_only or False
    row.benefit_tuition = scholarship.benefit_tuition or False
    row.benefit_allowance_monthly = scholarship.benefit_allowance_monthly
    row.benefit_books = scholarship.benefit_books or False
    row.benefit_miscellaneous = scholarship.benefit_miscellaneous
    row.benefit_total_value = scholarship.benefit_total_value
    row.required_documents = json.dumps(scholarship.required_documents or [])
    row.has_qualifying_exam = scholarship.has_qualifying_exam or False
    row.has_interview = scholarship.has_interview or False
    row.has_essay_requirement = scholarship.has_essay_requirement or False
    row.has_return_service = scholarship.has_return_service or False
    row.application_deadline = scholarship.application_deadline
    row.deadline_precision = scholarship.deadline_precision
    row.deadline_note = scholarship.deadline_note
    row.deadline_source_url = scholarship.deadline_source_url
    row.application_open_date = scholarship.application_open_date
    row.academic_year_target = scholarship.academic_year_target
    if scholarship.cycle_type is not None:
        row.cycle_type = scholarship.cycle_type
    if scholarship.last_open_date is not None:
        row.last_open_date = scholarship.last_open_date
    if scholarship.last_close_date is not None:
        row.last_close_date = scholarship.last_close_date
    if scholarship.is_active is not None:
        row.is_active = scholarship.is_active
    if scholarship.opportunity_type is not None:
        row.opportunity_type = scholarship.opportunity_type
    if scholarship.type_attributes is not None:
        row.type_attributes = json.dumps(scholarship.type_attributes)
    if scholarship.organization_id is not None:
        row.organization_id = scholarship.organization_id
    if scholarship.editorial_state is not None:
        apply_editorial_state(row, scholarship.editorial_state)
    elif not getattr(row, "editorial_state", None):
        apply_editorial_state(row, PUBLISHED if row.is_active else "archived")
    else:
        sync_legacy_fields_from_editorial(row)
    row.last_verified_at = utc_now_naive()
    if verification_source:
        row.verification_source = verification_source
    row.data_status = _normalize_data_status_on_import(scholarship, row if hasattr(row, "id") and row.id else None)
    sync_application_status(row)


def persist_scholarship_from_schema(
    db: Session,
    scholarship: schemas.Scholarship,
    *,
    version_changed_by: int | None = None,
    auto_commit: bool = True,
    verification_source: str | None = None,
    allow_upsert: bool = False,
) -> PersistResult:
    """
    Insert or (when allow_upsert) update a Scholarship row from a validated schema.

    On upsert, preserves manually uploaded image_url/image_alt when incoming values are empty.
    """
    existing = find_existing_scholarship(db, scholarship)

    if existing and not allow_upsert:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=409,
            detail="Scholarship with same title, provider, and link already exists",
        )

    if existing and allow_upsert:
        old_snap = snapshot_scholarship_row(existing)
        apply_schema_to_row(
            existing,
            scholarship,
            preserve_images=True,
            verification_source=verification_source,
            is_import=True,
        )
        new_snap = snapshot_scholarship_row(existing)
        diff = diff_snapshots(old_snap, new_snap)
        if diff:
            record_scholarship_version(
                db,
                scholarship_id=existing.id,
                changes=diff,
                changed_by=version_changed_by,
            )
        apply_quality_scores(existing, db)
        if auto_commit:
            db.commit()
            db.refresh(existing)
        else:
            db.flush()
            db.refresh(existing)
        return PersistResult(existing, created=False)

    db_scholarship = models.Scholarship()
    apply_schema_to_row(
        db_scholarship,
        scholarship,
        preserve_images=False,
        verification_source=verification_source,
        is_import=False,
    )
    if db_scholarship.is_active is None:
        db_scholarship.is_active = scholarship.is_active if scholarship.is_active is not None else True
    if not db_scholarship.data_status:
        db_scholarship.data_status = "active"
    db.add(db_scholarship)
    db.flush()
    apply_quality_scores(db_scholarship, db)
    snap = snapshot_scholarship_row(db_scholarship)
    record_scholarship_version(
        db,
        scholarship_id=db_scholarship.id,
        changes={"action": "create", "snapshot": snap},
        changed_by=version_changed_by,
    )
    if auto_commit:
        db.commit()
        db.refresh(db_scholarship)
    else:
        db.flush()
        db.refresh(db_scholarship)
    return PersistResult(db_scholarship, created=True)
