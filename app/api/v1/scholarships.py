import json
import logging
import time
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user, require_admin
from app.config import settings
from app.db import get_db
from app.limiter import limiter
from app.utils.sanitize import strip_tags
from app.utils.json_helpers import parse_json
from app.utils.application_status import sync_application_status
from app.utils.audit import log_action
from app.utils.scholarship_persist import (
    PersistResult,
    apply_schema_to_row,
    find_existing_scholarship,
    persist_scholarship_from_schema as _persist_scholarship_from_schema,
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
from app.utils.scholarship_versioning import (
    diff_snapshots,
    record_scholarship_version,
    snapshot_scholarship_row,
)
from app.utils.quality_score import compute_confidence_score
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
from app.auth import assert_can_read_profile, get_optional_user_id, get_profile_access_token
from app.api.v1.profiles import get_profile_dict
from app.matching.preparation import compute_application_readiness
from app.utils.freshness_chips import build_freshness_chips


def _public_scholarship_payload(row) -> dict:
    """Student-facing scholarship payload without internal completeness score."""
    data = dict(_scholarship_to_response(row))
    data.pop("confidence_score", None)
    data["freshness_chips"] = build_freshness_chips(data)
    return data


def persist_scholarship_from_schema(
    db: Session,
    scholarship: schemas.Scholarship,
    *,
    version_changed_by: int | None = None,
    auto_commit: bool = True,
    verification_source: str | None = None,
    allow_upsert: bool = False,
) -> models.Scholarship:
    """Insert or update a Scholarship row; returns the ORM row."""
    result = _persist_scholarship_from_schema(
        db,
        scholarship,
        version_changed_by=version_changed_by,
        auto_commit=auto_commit,
        verification_source=verification_source,
        allow_upsert=allow_upsert,
    )
    if auto_commit:
        invalidate_scholarship_cache()
    return result.row



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


@router.get("/scholarships/{scholarship_id}")
@limiter.limit("120/minute")
def get_scholarship(
    request: Request,
    scholarship_id: int,
    profile_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        logger.warning("scholarships_get_not_found scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=404, detail="Scholarship not found")
    payload = _public_scholarship_payload(s)
    if profile_id is not None:
        assert_can_read_profile(profile_id, db, user_id, profile_token)
        profile = get_profile_dict(profile_id, db)
        if profile:
            sch_dict = _scholarship_to_dict(s)
            payload["preparation"] = compute_application_readiness(sch_dict, profile)
    return payload


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
    apply_schema_to_row(
        s,
        scholarship,
        preserve_images=True,
        verification_source=s.verification_source,
        is_import=False,
    )
    s.last_verified_at = utc_now_naive()
    s.confidence_score = compute_confidence_score(s)
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
    sync_application_status(s)
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
