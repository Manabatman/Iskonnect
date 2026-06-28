import json
import logging
import time
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user, require_admin
from app.config import settings
from app.db import get_db
from app.limiter import limiter
from app.utils.sanitize import strip_tags
from app.utils.json_helpers import parse_json
from app.utils.audit import log_action
from app.utils.scholarship_versioning import (
    diff_snapshots,
    record_scholarship_version,
    snapshot_scholarship_row,
)
from app.scholarship_cache import get_cached_scholarship_dicts as _cache_fetch_dicts
from app.scholarship_cache import invalidate_scholarship_cache
from app.storage.supabase_storage import (
    StorageNotConfiguredError,
    delete_object,
    storage_path_from_public_url,
    upload_object,
)
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.image_processing import compress_scholarship_image
from app.utils.timezone import utc_now_naive

logger = logging.getLogger(__name__)


def _derive_verification_source(scholarship: schemas.Scholarship) -> str:
    """Map schema source string to a small set of provenance labels."""
    src = (scholarship.source or "").strip().lower()
    if src in ("philscholar", "scraper") or "phil" in src:
        return "scraper"
    if "csv" in src or src in ("import", "csv_import"):
        return "csv_import"
    return "manual"

router = APIRouter()


def _build_all_scholarship_dicts(db: Session) -> list[dict]:
    scholarships = db.query(models.Scholarship).filter(
        models.Scholarship.is_active != False  # noqa: E712
    ).all()
    return [_scholarship_to_dict(s) for s in scholarships]


def get_cached_scholarship_dicts(db: Session) -> list[dict]:
    """Return scholarship dicts from Redis/process cache, or DB on miss."""
    return _cache_fetch_dicts(db, _build_all_scholarship_dicts)


from app.serialization.scholarship import (
    scholarship_to_api_payload as _scholarship_to_response,
    scholarship_to_catalog_dict as _scholarship_to_dict,
)


def persist_scholarship_from_schema(
    db: Session,
    scholarship: schemas.Scholarship,
    *,
    version_changed_by: int | None = None,
    auto_commit: bool = True,
    verification_source: str | None = None,
) -> models.Scholarship:
    """Insert a Scholarship row from a validated schema (used by POST and staging approval).

    When auto_commit is False, caller must commit (e.g. single transaction with staging row update).
    """
    dedupe = scholarship_dedupe_key(scholarship.title, scholarship.provider, scholarship.link)
    dup = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.dedupe_key == dedupe)
        .first()
    )
    if dup:
        raise HTTPException(status_code=409, detail="Scholarship with same title, provider, and link already exists")

    db_scholarship = models.Scholarship(
        title=strip_tags(scholarship.title) or scholarship.title,
        provider=strip_tags(scholarship.provider) or scholarship.provider if scholarship.provider else None,
        source=strip_tags(scholarship.source) or scholarship.source if scholarship.source else None,
        dedupe_key=dedupe,
        countries=",".join(scholarship.countries or []),
        regions=",".join(scholarship.regions or []),
        min_age=scholarship.min_age,
        max_age=scholarship.max_age,
        needs_tags=json.dumps(scholarship.needs_tags or []),
        level=scholarship.level,
        link=scholarship.link,
        description=strip_tags(scholarship.description) or scholarship.description if scholarship.description else None,
        image_url=scholarship.image_url,
        image_alt=strip_tags(scholarship.image_alt) or scholarship.image_alt if scholarship.image_alt else None,
        provider_type=scholarship.provider_type,
        scholarship_type=scholarship.scholarship_type,
        eligible_levels=json.dumps(scholarship.eligible_levels or []),
        eligible_regions=json.dumps(scholarship.eligible_regions or scholarship.regions or []),
        eligible_cities=json.dumps(scholarship.eligible_cities or []),
        residency_required=scholarship.residency_required or False,
        eligible_school_types=json.dumps(scholarship.eligible_school_types or ["Public", "Private"]),
        eligible_courses_psced=json.dumps(scholarship.eligible_courses_psced or []),
        eligible_courses_specific=json.dumps(scholarship.eligible_courses_specific or []),
        preferred_extracurriculars=json.dumps(scholarship.preferred_extracurriculars or []),
        preferred_awards=json.dumps(scholarship.preferred_awards or []),
        max_income_threshold=scholarship.max_income_threshold,
        min_gwa_normalized=scholarship.min_gwa_normalized,
        priority_groups=json.dumps(scholarship.priority_groups or []),
        members_only=scholarship.members_only or False,
        benefit_tuition=scholarship.benefit_tuition or False,
        benefit_allowance_monthly=scholarship.benefit_allowance_monthly,
        benefit_books=scholarship.benefit_books or False,
        benefit_total_value=scholarship.benefit_total_value,
        required_documents=json.dumps(scholarship.required_documents or []),
        has_qualifying_exam=scholarship.has_qualifying_exam or False,
        has_interview=scholarship.has_interview or False,
        has_essay_requirement=scholarship.has_essay_requirement or False,
        has_return_service=scholarship.has_return_service or False,
        application_deadline=scholarship.application_deadline,
        application_open_date=scholarship.application_open_date,
        academic_year_target=scholarship.academic_year_target,
        is_active=scholarship.is_active if scholarship.is_active is not None else True,
        last_verified_at=utc_now_naive(),
        verification_source=verification_source,
        data_status="active",
    )
    db.add(db_scholarship)
    db.flush()
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
        invalidate_scholarship_cache()
    else:
        db.flush()
        db.refresh(db_scholarship)
    return db_scholarship


@router.post("/scholarships", response_model=schemas.ScholarshipResponse)
@limiter.limit("30/minute")
def create_scholarship(
    request: Request,
    scholarship: schemas.Scholarship,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    db_scholarship = persist_scholarship_from_schema(
        db,
        scholarship,
        version_changed_by=_admin.id if _admin else None,
    )
    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="scholarship.create",
        resource_type="scholarship",
        resource_id=db_scholarship.id,
        details={"title": db_scholarship.title},
        ip_address=request.client.host if request.client else None,
    )
    return _scholarship_to_response(db_scholarship)


@router.get("/scholarships", response_model=list[schemas.ScholarshipResponse])
@limiter.limit("60/minute")
def list_scholarships(
    request: Request,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    """List scholarships. Public for active only. include_inactive=true requires admin."""
    if include_inactive:
        if not settings.auth_disabled and (user is None or getattr(user, "role", "student") != "admin"):
            logger.warning("scholarships_list_include_inactive_denied reason=admin_required")
            raise HTTPException(status_code=403, detail="Admin role required")
        scholarships = db.query(models.Scholarship).all()
        return [_scholarship_to_response(s) for s in scholarships]
    return get_cached_scholarship_dicts(db)


@router.get("/scholarships/{scholarship_id}", response_model=schemas.ScholarshipResponse)
@limiter.limit("120/minute")
def get_scholarship(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        logger.warning("scholarships_get_not_found scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return _scholarship_to_response(s)


@router.put("/scholarships/{scholarship_id}", response_model=schemas.ScholarshipResponse)
@limiter.limit("30/minute")
def update_scholarship(
    request: Request,
    scholarship_id: int,
    scholarship: schemas.Scholarship,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        logger.warning("scholarships_update_not_found scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=404, detail="Scholarship not found")
    old_snap = snapshot_scholarship_row(s)
    s.title = strip_tags(scholarship.title) or scholarship.title
    s.provider = strip_tags(scholarship.provider) or scholarship.provider if scholarship.provider else None
    s.source = strip_tags(scholarship.source) or scholarship.source if scholarship.source else None
    s.countries = ",".join(scholarship.countries or [])
    s.regions = ",".join(scholarship.regions or [])
    s.min_age = scholarship.min_age
    s.max_age = scholarship.max_age
    s.needs_tags = json.dumps(scholarship.needs_tags or [])
    s.level = scholarship.level
    s.link = scholarship.link
    s.description = strip_tags(scholarship.description) or scholarship.description if scholarship.description else None
    if scholarship.image_url is not None:
        s.image_url = scholarship.image_url
    if scholarship.image_alt is not None:
        s.image_alt = strip_tags(scholarship.image_alt) or scholarship.image_alt
    s.provider_type = scholarship.provider_type
    s.scholarship_type = scholarship.scholarship_type
    s.eligible_levels = json.dumps(scholarship.eligible_levels or [])
    s.eligible_regions = json.dumps(scholarship.eligible_regions or scholarship.regions or [])
    s.eligible_cities = json.dumps(scholarship.eligible_cities or [])
    s.residency_required = scholarship.residency_required or False
    s.eligible_school_types = json.dumps(scholarship.eligible_school_types or ["Public", "Private"])
    s.eligible_courses_psced = json.dumps(scholarship.eligible_courses_psced or [])
    s.eligible_courses_specific = json.dumps(scholarship.eligible_courses_specific or [])
    s.preferred_extracurriculars = json.dumps(scholarship.preferred_extracurriculars or [])
    s.preferred_awards = json.dumps(scholarship.preferred_awards or [])
    s.max_income_threshold = scholarship.max_income_threshold
    s.min_gwa_normalized = scholarship.min_gwa_normalized
    s.priority_groups = json.dumps(scholarship.priority_groups or [])
    s.members_only = scholarship.members_only or False
    s.benefit_tuition = scholarship.benefit_tuition or False
    s.benefit_allowance_monthly = scholarship.benefit_allowance_monthly
    s.benefit_books = scholarship.benefit_books or False
    s.benefit_total_value = scholarship.benefit_total_value
    s.required_documents = json.dumps(scholarship.required_documents or [])
    s.has_qualifying_exam = scholarship.has_qualifying_exam or False
    s.has_interview = scholarship.has_interview or False
    s.has_essay_requirement = scholarship.has_essay_requirement or False
    s.has_return_service = scholarship.has_return_service or False
    s.application_deadline = scholarship.application_deadline
    s.application_open_date = scholarship.application_open_date
    s.academic_year_target = scholarship.academic_year_target
    if scholarship.is_active is not None:
        s.is_active = scholarship.is_active
    new_snap = snapshot_scholarship_row(s)
    diff = diff_snapshots(old_snap, new_snap)
    if diff:
        record_scholarship_version(
            db,
            scholarship_id=s.id,
            changes=diff,
            changed_by=_admin.id if _admin else None,
        )
    db.commit()
    db.refresh(s)
    invalidate_scholarship_cache()
    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="scholarship.update",
        resource_type="scholarship",
        resource_id=s.id,
        details={"title": s.title},
        ip_address=request.client.host if request.client else None,
    )
    return _scholarship_to_response(s)


@router.delete("/scholarships/{scholarship_id}")
@limiter.limit("30/minute")
def delete_scholarship(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        logger.warning("scholarships_delete_not_found scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=404, detail="Scholarship not found")
    s.is_active = False
    db.commit()
    invalidate_scholarship_cache()
    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="scholarship.deactivate",
        resource_type="scholarship",
        resource_id=scholarship_id,
        details={},
        ip_address=request.client.host if request.client else None,
    )
    return {"status": "deactivated"}


@router.post("/scholarships/{scholarship_id}/image", response_model=schemas.ScholarshipResponse)
@limiter.limit("20/minute")
async def upload_scholarship_image(
    request: Request,
    scholarship_id: int,
    file: UploadFile = File(...),
    image_alt: str | None = Form(default=None),
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Admin: upload a scholarship banner image to Supabase Storage."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    content_type = (file.content_type or "").split(";")[0].strip().lower()
    raw = await file.read()
    webp, digest = compress_scholarship_image(
        raw, content_type, settings.scholarship_image_max_bytes
    )
    object_path = f"{scholarship_id}/{digest}.webp"

    try:
        public_url = upload_object(object_path, webp, content_type="image/webp")
    except StorageNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("scholarship_image_upload_failed scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=502, detail="Image upload failed") from exc

    old_path = storage_path_from_public_url(s.image_url)
    s.image_url = public_url
    alt = (image_alt or s.title or "").strip()
    s.image_alt = alt[:300] if alt else None
    db.commit()
    db.refresh(s)
    invalidate_scholarship_cache()

    if old_path and old_path != object_path:
        try:
            delete_object(old_path)
        except Exception:
            logger.warning("scholarship_image_old_delete_failed path=%s", old_path)

    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="scholarship.image_upload",
        resource_type="scholarship",
        resource_id=scholarship_id,
        details={"image_url": public_url},
        ip_address=request.client.host if request.client else None,
    )
    return _scholarship_to_response(s)


@router.delete("/scholarships/{scholarship_id}/image", response_model=schemas.ScholarshipResponse)
@limiter.limit("20/minute")
def delete_scholarship_image(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Admin: remove scholarship image from storage and clear DB fields."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    old_path = storage_path_from_public_url(s.image_url)
    s.image_url = None
    s.image_alt = None
    db.commit()
    db.refresh(s)
    invalidate_scholarship_cache()

    if old_path:
        try:
            delete_object(old_path)
        except StorageNotConfiguredError:
            pass
        except Exception:
            logger.warning("scholarship_image_delete_failed path=%s", old_path)

    log_action(
        db,
        actor_id=_admin.id if _admin else None,
        actor_type="admin",
        action="scholarship.image_delete",
        resource_type="scholarship",
        resource_id=scholarship_id,
        details={},
        ip_address=request.client.host if request.client else None,
    )
    return _scholarship_to_response(s)
