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
from app.utils.opportunity_quality import apply_quality_scores
from app.utils.timezone import utc_now_naive

logger = logging.getLogger(__name__)


def _derive_verification_source(scholarship: schemas.Scholarship) -> str:
    """Map schema source string to a small set of provenance labels."""
    src = (scholarship.source or "").strip().lower()
    if src in ("philscholar", "scraper") or "phil" in src:
        return "team_verified"
    if "csv" in src or src in ("import", "csv_import"):
        return "csv_import"
    return "manual"

router = APIRouter()


def _build_all_scholarship_dicts(db: Session, *, publishable_only: bool = False) -> list[dict]:
    from app.utils.data_completeness import is_publishable
    from app.matching.scholarship_enrichment import enrich_scholarship_dicts

    scholarships = db.query(models.Scholarship).filter(
        models.Scholarship.is_active != False  # noqa: E712
    ).all()
    dicts = enrich_scholarship_dicts(db, [_scholarship_to_dict(s) for s in scholarships])
    if publishable_only:
        dicts = [d for d in dicts if is_publishable(d)]
    return dicts


def get_cached_scholarship_dicts(db: Session) -> list[dict]:
    """Return publishable scholarship dicts for matching (completeness gate applied)."""
    return _cache_fetch_dicts(db, lambda d: _build_all_scholarship_dicts(d, publishable_only=True))


from app.serialization.scholarship import (
    scholarship_to_api_payload as _scholarship_to_response,
    scholarship_to_catalog_dict as _scholarship_to_dict,
)
from app.auth import assert_can_read_profile, get_current_user, get_optional_user_id, get_profile_access_token
from app.api.v1.profiles import get_profile_dict
from app.matching.eligibility_result import evaluate_eligibility
from app.matching.eligibility_explanation import build_eligibility_explanation
from app.matching.preparation import compute_application_readiness
from app.matching.scholarship_enrichment import attach_scholarship_join_fields
from app.utils.freshness_chips import build_freshness_chips
from app.utils.verification_display import attach_verification_fields

_STUDENT_INTERNAL_STRIP = (
    "verification_badge",
    "verification_badge_label",
    "completeness_label",
    "completeness_tier",
    "completeness_signal",
    "last_reviewed_label",
    "_has_field_evidence",
    "field_evidence",
    "confidence_score",
    "data_completeness_score",
)


def _public_scholarship_payload(row, db: Session | None = None) -> dict:
    """Student-facing scholarship payload without internal completeness or evidence."""
    data = dict(_scholarship_to_response(row))
    data.pop("confidence_score", None)
    data.pop("data_completeness_score", None)
    data["freshness_chips"] = build_freshness_chips(data)
    if db is not None and row.id:
        data["_has_field_evidence"] = (
            db.query(models.FieldEvidence)
            .filter(
                models.FieldEvidence.scholarship_id == row.id,
                models.FieldEvidence.superseded_at.is_(None),
            )
            .first()
            is not None
        )
    attach_verification_fields(data)
    for key in _STUDENT_INTERNAL_STRIP:
        data.pop(key, None)
    return data


def _admin_scholarship_payload(row, db: Session | None = None) -> dict:
    """Admin/reviewer payload retains internal verification and completeness fields."""
    data = dict(_scholarship_to_response(row))
    data["freshness_chips"] = build_freshness_chips(data)
    if db is not None and row.id:
        data["_has_field_evidence"] = (
            db.query(models.FieldEvidence)
            .filter(
                models.FieldEvidence.scholarship_id == row.id,
                models.FieldEvidence.superseded_at.is_(None),
            )
            .first()
            is not None
        )
    attach_verification_fields(data)
    data.pop("_has_field_evidence", None)
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
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        logger.warning("scholarships_get_not_found scholarship_id=%s", scholarship_id)
        raise HTTPException(status_code=404, detail="Scholarship not found")
    is_admin = user is not None and getattr(user, "role", "student") == "admin"
    payload = _admin_scholarship_payload(s, db) if is_admin else _public_scholarship_payload(s, db)
    if profile_id is not None:
        assert_can_read_profile(profile_id, db, user_id, profile_token)
        profile = get_profile_dict(profile_id, db)
        if profile:
            sch_dict = attach_scholarship_join_fields(db, _scholarship_to_dict(s))
            payload["preparation"] = compute_application_readiness(sch_dict, profile)
            payload.update(evaluate_eligibility(profile, sch_dict).to_dict())
    return payload


@router.get("/admin/scholarships/{scholarship_id}/evidence")
@limiter.limit("60/minute")
def get_scholarship_evidence_admin(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    """Admin-only field evidence trail for catalog review."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    from app.utils.field_evidence import list_admin_field_evidence

    return {
        "scholarship_id": scholarship_id,
        "field_evidence": list_admin_field_evidence(db, scholarship_id),
    }


@router.get("/scholarships/{scholarship_id}/history", response_model=list[schemas.ScholarshipVersionHistoryItem])
@limiter.limit("60/minute")
def get_scholarship_history(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
):
    """Public change history for a scholarship (field-level diffs)."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    rows = (
        db.query(models.ScholarshipVersion)
        .filter(models.ScholarshipVersion.scholarship_id == scholarship_id)
        .order_by(models.ScholarshipVersion.version_number.desc())
        .limit(50)
        .all()
    )
    out: list[dict] = []
    for row in rows:
        try:
            changes = json.loads(row.changes) if isinstance(row.changes, str) else row.changes
        except (json.JSONDecodeError, TypeError):
            changes = {}
        out.append(
            {
                "version_number": row.version_number,
                "changed_at": row.changed_at.isoformat() if row.changed_at else None,
                "changes": changes if isinstance(changes, dict) else {},
            }
        )
    return out


@router.get("/scholarships/{scholarship_id}/eligibility", response_model=schemas.ScholarshipEligibilityResponse)
@limiter.limit("120/minute")
def get_scholarship_eligibility(
    request: Request,
    scholarship_id: int,
    profile_id: int = Query(...),
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    """Full eligibility evaluation for any scholarship — matched or not."""
    s = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    assert_can_read_profile(profile_id, db, user_id, profile_token)
    profile = get_profile_dict(profile_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    sch_dict = attach_scholarship_join_fields(db, _scholarship_to_dict(s))
    elig = evaluate_eligibility(profile, sch_dict)
    explanation = build_eligibility_explanation(profile, sch_dict, elig)
    return {
        "scholarship_id": scholarship_id,
        "profile_id": profile_id,
        **explanation,
    }


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
    apply_quality_scores(s, db)
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
