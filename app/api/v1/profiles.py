import json
import logging
from datetime import date, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import assert_can_read_profile, create_profile_read_token, get_current_user_id, get_optional_user_id, get_profile_access_token
from app.utils.audit import log_action
from app.config import settings
from app.db import get_db
from app.utils.sanitize import strip_tags
from app.utils.json_helpers import parse_json

logger = logging.getLogger(__name__)
from app.limiter import limiter
from app.plan_cache import invalidate_plan_cache
from app.taxonomy.income_brackets import get_income_bracket
from app.taxonomy.gwa_normalizer import normalize_gwa
from app.taxonomy.school_registry import resolve_school_id
from app.matching.profile_enrichment import enrich_profile_dict

router = APIRouter()

_PII_AUDIT_KEYS = frozenset({"email", "full_name", "guardian_email", "contact_email", "name", "address"})


def _redact_audit_details_pii(details: dict | None) -> dict:
    """Remove PII keys from audit log details while preserving the record."""
    if not details:
        return {}
    return {k: v for k, v in details.items() if k not in _PII_AUDIT_KEYS}


def _anonymize_user_feedback(db: Session, user_id: int) -> None:
    """RA 10173 — anonymize product feedback linked to a deleted account."""
    db.query(models.ProductFeedback).filter(models.ProductFeedback.user_id == user_id).update(
        {
            models.ProductFeedback.user_id: None,
            models.ProductFeedback.contact_email: None,
        },
        synchronize_session=False,
    )


def _redact_user_audit_logs(db: Session, user_id: int) -> None:
    """Strip PII from audit log details for a user being erased."""
    rows = db.query(models.AuditLog).filter(models.AuditLog.actor_id == user_id).all()
    for row in rows:
        if not row.details:
            continue
        try:
            parsed = json.loads(row.details)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(parsed, dict):
            row.details = json.dumps(_redact_audit_details_pii(parsed))


def _profile_to_response(p, *, include_access_token: bool = False):
    out = {
        "id": p.id,
        "full_name": p.full_name,
        "email": p.email,
        "age": p.age,
        "region": p.region,
        "school": p.school,
        "needs": parse_json(p.needs),
        "education_level": p.education_level,
        "gender": getattr(p, "gender", None),
        "birthdate": p.birthdate.isoformat() if getattr(p, "birthdate", None) else None,
        "current_academic_stage": getattr(p, "current_academic_stage", None),
        "target_academic_year": getattr(p, "target_academic_year", None),
        "province": getattr(p, "province", None),
        "city_municipality": getattr(p, "city_municipality", None),
        "barangay": getattr(p, "barangay", None),
        "school_type": getattr(p, "school_type", None),
        "school_id": getattr(p, "school_id", None),
        "target_school_id": getattr(p, "target_school_id", None),
        "enrollment_status": getattr(p, "enrollment_status", None),
        "current_year_level": getattr(p, "current_year_level", None),
        "next_year_level": getattr(p, "next_year_level", None),
        "expected_graduation_date": p.expected_graduation_date.isoformat() if getattr(p, "expected_graduation_date", None) else None,
        "citizenship": getattr(p, "citizenship", None) or "Filipino",
        "target_school": getattr(p, "target_school", None),
        "gwa_raw": getattr(p, "gwa_raw", None),
        "gwa_scale": getattr(p, "gwa_scale", None),
        "gwa_normalized": getattr(p, "gwa_normalized", None),
        "field_of_study_broad": getattr(p, "field_of_study_broad", None),
        "field_of_study_specific": getattr(p, "field_of_study_specific", None),
        # Use shared parse_json (same as needs/documents); _parse_json was never defined in this module.
        "preferred_courses": parse_json(getattr(p, "preferred_courses", None), default=[]),
        "extracurriculars": parse_json(getattr(p, "extracurriculars", None)),
        "awards": parse_json(getattr(p, "awards", None)),
        "household_income_annual": getattr(p, "household_income_annual", None),
        "income_bracket": getattr(p, "income_bracket", None),
        "is_underprivileged": getattr(p, "is_underprivileged", False) or False,
        "is_pwd": getattr(p, "is_pwd", False) or False,
        "is_indigenous_people": getattr(p, "is_indigenous_people", False) or False,
        "ip_tribe_name": getattr(p, "ip_tribe_name", None),
        "is_solo_parent_dependent": getattr(p, "is_solo_parent_dependent", False) or False,
        "is_ofw_dependent": getattr(p, "is_ofw_dependent", False) or False,
        "ofw_parent_type": getattr(p, "ofw_parent_type", None),
        "is_farmer_fisher_dependent": getattr(p, "is_farmer_fisher_dependent", False) or False,
        "is_4ps_listahanan": getattr(p, "is_4ps_listahanan", False) or False,
        "is_military_dependent": getattr(p, "is_military_dependent", False) or False,
        "is_uniformed_service_dependent": getattr(p, "is_uniformed_service_dependent", False) or False,
        "is_gsis_dependent": getattr(p, "is_gsis_dependent", False) or False,
        "is_sss_dependent": getattr(p, "is_sss_dependent", False) or False,
        "is_medical_frontliner_dependent": getattr(p, "is_medical_frontliner_dependent", False) or False,
        "study_destination_preference": getattr(p, "study_destination_preference", None) or "PHILIPPINES_ONLY",
        "employment_status": getattr(p, "employment_status", None),
        "evening_weekend_program": getattr(p, "evening_weekend_program", None),
        "athlete_level": getattr(p, "athlete_level", None),
        "parent_occupation": getattr(p, "parent_occupation", None),
        "documents": parse_json(getattr(p, "documents", None), default=[]),
        "privacy_consent_at": p.privacy_consent_at.isoformat() if getattr(p, "privacy_consent_at", None) else None,
        "privacy_consent_version": getattr(p, "privacy_consent_version", None),
        "google_drive_folder_url": getattr(p, "google_drive_folder_url", None),
        "psgc_code": getattr(p, "psgc_code", None),
        "guardian_full_name": getattr(p, "guardian_full_name", None),
        "guardian_email": getattr(p, "guardian_email", None),
        "guardian_consent_at": p.guardian_consent_at.isoformat() if getattr(p, "guardian_consent_at", None) else None,
        "prior_tertiary_units": getattr(p, "prior_tertiary_units", None),
        "class_rank": getattr(p, "class_rank", None),
        "class_size": getattr(p, "class_size", None),
        "work_experience_years": getattr(p, "work_experience_years", None),
        "marital_status": getattr(p, "marital_status", None),
        "parent_salary_grade": getattr(p, "parent_salary_grade", None),
        "parent_status": getattr(p, "parent_status", None),
        "is_hei_faculty_or_staff": getattr(p, "is_hei_faculty_or_staff", None),
        "residency_years_in_locality": getattr(p, "residency_years_in_locality", None),
    }
    if include_access_token and getattr(p, "user_id", None) is None:
        out["profile_access_token"] = create_profile_read_token(p.id)
    return out


def _profile_to_db_dict(profile: schemas.StudentProfile) -> dict:
    """Convert schema to DB model fields."""
    gwa_norm = profile.gwa_normalized
    if gwa_norm is None and profile.gwa_raw is not None:
        gwa_norm = normalize_gwa(profile.gwa_raw, profile.gwa_scale)

    income_bracket = profile.income_bracket
    if income_bracket is None and profile.household_income_annual is not None:
        income_bracket = get_income_bracket(profile.household_income_annual)

    return {
        "full_name": strip_tags(profile.full_name) or profile.full_name,
        "email": profile.email,
        "age": profile.age,
        "region": profile.region,
        "school": profile.school,
        "needs": json.dumps(profile.needs or []),
        "education_level": profile.education_level,
        "gender": profile.gender,
        "birthdate": profile.birthdate,
        "current_academic_stage": profile.current_academic_stage,
        "target_academic_year": profile.target_academic_year,
        "province": profile.province,
        "city_municipality": profile.city_municipality,
        "barangay": profile.barangay,
        "psgc_code": profile.psgc_code,
        "school_type": profile.school_type,
        "school_id": resolve_school_id(profile.school) or profile.school_id,
        "target_school_id": resolve_school_id(profile.target_school) or profile.target_school_id,
        "enrollment_status": profile.enrollment_status,
        "current_year_level": profile.current_year_level,
        "next_year_level": profile.next_year_level,
        "expected_graduation_date": profile.expected_graduation_date,
        "citizenship": profile.citizenship or "Filipino",
        "target_school": profile.target_school,
        "gwa_raw": profile.gwa_raw,
        "gwa_scale": profile.gwa_scale,
        "gwa_normalized": gwa_norm or profile.gwa_normalized,
        "field_of_study_broad": profile.field_of_study_broad,
        "field_of_study_specific": profile.field_of_study_specific,
        "preferred_courses": json.dumps((profile.preferred_courses or [])[:3]),
        "extracurriculars": json.dumps(profile.extracurriculars or []),
        "awards": json.dumps(profile.awards or []),
        "household_income_annual": profile.household_income_annual,
        "income_bracket": income_bracket or profile.income_bracket,
        "is_underprivileged": profile.is_underprivileged or False,
        "is_pwd": profile.is_pwd or False,
        "is_indigenous_people": profile.is_indigenous_people or False,
        "ip_tribe_name": profile.ip_tribe_name,
        "is_solo_parent_dependent": profile.is_solo_parent_dependent or False,
        "is_ofw_dependent": profile.is_ofw_dependent or False,
        "ofw_parent_type": profile.ofw_parent_type,
        "is_farmer_fisher_dependent": profile.is_farmer_fisher_dependent or False,
        "is_4ps_listahanan": profile.is_4ps_listahanan or False,
        "is_military_dependent": profile.is_military_dependent or False,
        "is_uniformed_service_dependent": profile.is_uniformed_service_dependent or False,
        "is_gsis_dependent": profile.is_gsis_dependent or False,
        "is_sss_dependent": profile.is_sss_dependent or False,
        "is_medical_frontliner_dependent": profile.is_medical_frontliner_dependent or False,
        "study_destination_preference": profile.study_destination_preference or "PHILIPPINES_ONLY",
        "employment_status": profile.employment_status,
        "evening_weekend_program": profile.evening_weekend_program,
        "athlete_level": profile.athlete_level,
        "parent_occupation": profile.parent_occupation,
        "guardian_full_name": strip_tags(profile.guardian_full_name) if profile.guardian_full_name else None,
        "guardian_email": str(profile.guardian_email) if profile.guardian_email else None,
        "guardian_consent_at": datetime.now(timezone.utc) if profile.guardian_consent else None,
        "documents": json.dumps(
            [d.model_dump() for d in (profile.documents or [])],
        ),
        "privacy_consent_at": datetime.now(timezone.utc) if profile.privacy_consent else None,
        "privacy_consent_version": profile.privacy_consent_version if profile.privacy_consent else None,
        "prior_tertiary_units": profile.prior_tertiary_units,
        "class_rank": profile.class_rank,
        "class_size": profile.class_size,
        "work_experience_years": profile.work_experience_years,
        "marital_status": profile.marital_status,
        "parent_salary_grade": profile.parent_salary_grade,
        "parent_status": profile.parent_status,
        "is_hei_faculty_or_staff": profile.is_hei_faculty_or_staff,
        "residency_years_in_locality": profile.residency_years_in_locality,
    }


def _sync_active_grant_scopes(db: Session, student_id: int, codes: list[str] | None) -> None:
    """Replace self-reported active grant scope rows for a student."""
    db.query(models.StudentActiveGrantScope).filter(
        models.StudentActiveGrantScope.student_id == student_id
    ).delete(synchronize_session=False)
    if not codes:
        return
    scope_rows = db.query(models.ConflictScope).filter(models.ConflictScope.code.in_(codes)).all()
    for scope in scope_rows:
        db.add(
            models.StudentActiveGrantScope(
                student_id=student_id,
                scope_id=scope.id,
                source="self_report",
                verified=False,
            )
        )


def _profile_response_enriched(p, db: Session, *, include_access_token: bool = False) -> dict:
    return enrich_profile_dict(_profile_to_response(p, include_access_token=include_access_token), db)


@router.get("/profiles", response_model=list[schemas.StudentProfileResponse])
@limiter.limit("60/minute")
def list_profiles(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """List profiles. Only returns the current user's profiles; unauthenticated requests get an empty list."""
    if user_id is None:
        return []
    query = db.query(models.Student).filter(models.Student.user_id == user_id)
    profiles = query.all()
    return [_profile_to_response(p) for p in profiles]


@router.get("/profiles/me", response_model=schemas.StudentProfileResponse)
@limiter.limit("60/minute")
def get_my_profile(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Return the single profile for the authenticated user."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    p = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not p:
        raise HTTPException(
            status_code=404,
            detail="No profile yet. Complete the profile builder.",
        )
    return _profile_to_response(p)


@router.put("/profiles/me", response_model=schemas.StudentProfileResponse)
@limiter.limit("20/minute")
def put_my_profile(
    request: Request,
    profile: schemas.StudentProfile,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Update the authenticated user's profile (email is taken from the account, not the body)."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="No profile yet. Use POST /profiles to create one.",
        )
    data = _profile_to_db_dict(profile)
    data["user_id"] = user_id
    data["email"] = u.email
    for k, v in data.items():
        setattr(existing, k, v)
    _sync_active_grant_scopes(db, existing.id, profile.active_grant_scope_codes)
    db.commit()
    db.refresh(existing)
    invalidate_plan_cache(existing.id)
    log_action(
        db,
        actor_id=user_id,
        actor_type="user",
        action="profile.update",
        resource_type="student",
        resource_id=existing.id,
        details={"user_id": user_id},
        ip_address=request.client.host if request.client else None,
    )
    return _profile_response_enriched(existing, db)


@router.get("/profiles/me/export")
@limiter.limit("10/minute")
def export_my_data(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """RA 10173 data portability — JSON export of profile and associated student data."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    p = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="No profile to export")
    profile = _profile_to_response(p)
    saved = (
        db.query(models.SavedScholarship)
        .filter(models.SavedScholarship.user_id == user_id)
        .all()
    )
    apps = db.query(models.Application).filter(models.Application.user_id == user_id).all()
    runs = db.query(models.MatchRun).filter(models.MatchRun.user_id == user_id).all()
    log_action(
        db,
        actor_id=user_id,
        actor_type="user",
        action="profile.export",
        resource_type="student",
        resource_id=p.id,
        details={},
        ip_address=request.client.host if request.client else None,
    )
    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "saved_scholarship_ids": [s.scholarship_id for s in saved],
        "applications": [
            {"scholarship_id": a.scholarship_id, "status": a.status, "created_at": a.created_at.isoformat() if a.created_at else None}
            for a in apps
        ],
        "match_run_count": len(runs),
    }


@router.patch("/profiles/me/vault", response_model=schemas.StudentProfileResponse)
@limiter.limit("30/minute")
def patch_drive_vault(
    request: Request,
    body: schemas.GoogleDriveVaultUpdate,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Set or clear the Google Drive folder URL used for the document vault."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    existing = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="No profile yet. Complete the profile builder.")
    existing.google_drive_folder_url = body.google_drive_folder_url
    db.commit()
    db.refresh(existing)
    log_action(
        db,
        actor_id=user_id,
        actor_type="user",
        action="profile.vault_update",
        resource_type="student",
        resource_id=existing.id,
        details={"has_url": bool(body.google_drive_folder_url)},
        ip_address=request.client.host if request.client else None,
    )
    return _profile_to_response(existing)


@router.delete("/profiles/me")
@limiter.limit("3/minute")
def delete_my_data(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """RA 10173 — right to erasure: delete account and associated profile data."""
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    client = request.client.host if request.client else None
    log_action(
        db,
        actor_id=user_id,
        actor_type="user",
        action="user.delete_self",
        resource_type="user",
        resource_id=user_id,
        details={"erasure": True},
        ip_address=client,
    )

    run_ids = [r[0] for r in db.query(models.MatchRun.id).filter(models.MatchRun.user_id == user_id).all()]
    if run_ids:
        db.query(models.MatchResult).filter(models.MatchResult.run_id.in_(run_ids)).delete(
            synchronize_session=False
        )
    db.query(models.MatchRun).filter(models.MatchRun.user_id == user_id).delete(synchronize_session=False)
    db.query(models.SavedScholarship).filter(models.SavedScholarship.user_id == user_id).delete(
        synchronize_session=False
    )
    db.query(models.Application).filter(models.Application.user_id == user_id).delete(
        synchronize_session=False
    )
    db.query(models.Notification).filter(models.Notification.user_id == user_id).delete(synchronize_session=False)
    db.query(models.ScholarshipReport).filter(models.ScholarshipReport.user_id == user_id).delete(
        synchronize_session=False
    )
    db.query(models.ScholarshipReport).filter(models.ScholarshipReport.reviewer_id == user_id).update(
        {models.ScholarshipReport.reviewer_id: None},
        synchronize_session=False,
    )
    db.query(models.ScoringWeight).filter(models.ScoringWeight.updated_by == user_id).update(
        {models.ScoringWeight.updated_by: None},
        synchronize_session=False,
    )
    db.query(models.ScholarshipVersion).filter(models.ScholarshipVersion.changed_by == user_id).update(
        {models.ScholarshipVersion.changed_by: None},
        synchronize_session=False,
    )
    _anonymize_user_feedback(db, user_id)
    _redact_user_audit_logs(db, user_id)
    db.query(models.Student).filter(models.Student.user_id == user_id).delete(synchronize_session=False)
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return {"status": "deleted"}


@router.post("/profiles", response_model=schemas.StudentProfileResponse)
@limiter.limit("20/minute")
def create_profile(
    request: Request,
    profile: schemas.StudentProfile,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Create or update profile. Requires auth when AUTH_DISABLED=false."""
    if not settings.auth_disabled and user_id is None:
        logger.warning("profile_create_denied user_id=%s reason=not_authenticated", user_id)
        raise HTTPException(status_code=401, detail="Not authenticated")

    data = _profile_to_db_dict(profile)
    if user_id is not None:
        u = db.query(models.User).filter(models.User.id == user_id).first()
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        data["user_id"] = user_id
        data["email"] = u.email
        existing_user_profile = (
            db.query(models.Student).filter(models.Student.user_id == user_id).first()
        )
        if existing_user_profile:
            for k, v in data.items():
                setattr(existing_user_profile, k, v)
            _sync_active_grant_scopes(db, existing_user_profile.id, profile.active_grant_scope_codes)
            db.commit()
            db.refresh(existing_user_profile)
            invalidate_plan_cache(existing_user_profile.id)
            log_action(
                db,
                actor_id=user_id,
                actor_type="user",
                action="profile.update",
                resource_type="student",
                resource_id=existing_user_profile.id,
                details={"user_id": user_id},
                ip_address=request.client.host if request.client else None,
            )
            return _profile_response_enriched(existing_user_profile, db)

    logger.info("profile_create user_id=%s", user_id)

    # Try insert first. On duplicate email, update only when the caller owns the row
    # (or both sides are anonymous); never silently overwrite another user's profile.
    try:
        db_profile = models.Student(**data)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        _sync_active_grant_scopes(db, db_profile.id, profile.active_grant_scope_codes)
        db.commit()
        invalidate_plan_cache(db_profile.id)
        log_action(
            db,
            actor_id=user_id,
            actor_type="user",
            action="profile.create",
            resource_type="student",
            resource_id=db_profile.id,
            details={"user_id": user_id},
            ip_address=request.client.host if request.client else None,
        )
        return _profile_response_enriched(db_profile, db, include_access_token=user_id is None)
    except IntegrityError:
        db.rollback()
        logger.warning("profile_create_integrity_conflict user_id=%s", user_id)
        existing = db.query(models.Student).filter(
            models.Student.email == profile.email
        ).first()
        if not existing:
            raise HTTPException(status_code=500, detail="Profile conflict")
        if existing.user_id is not None:
            if user_id is None:
                raise HTTPException(
                    status_code=409,
                    detail="A profile with this email already exists. Sign in to update it.",
                )
            if existing.user_id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="A profile with this email already exists under another account.",
                )
        if user_id is not None:
            data["user_id"] = user_id
        for k, v in data.items():
            setattr(existing, k, v)
        _sync_active_grant_scopes(db, existing.id, profile.active_grant_scope_codes)
        db.commit()
        db.refresh(existing)
        log_action(
            db,
            actor_id=user_id,
            actor_type="user",
            action="profile.update",
            resource_type="student",
            resource_id=existing.id,
            details={"user_id": user_id},
            ip_address=request.client.host if request.client else None,
        )
        return _profile_response_enriched(existing, db)


@router.get("/profiles/{profile_id}", response_model=schemas.StudentProfileResponse)
@limiter.limit("60/minute")
def get_profile(
    request: Request,
    profile_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    assert_can_read_profile(profile_id, db, user_id, profile_token)
    profile = db.query(models.Student).filter(models.Student.id == profile_id).first()
    if not profile:
        logger.warning("profile_get_not_found profile_id=%s", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    return _profile_response_enriched(profile, db)


def get_profile_dict(profile_id: int, db: Session) -> dict | None:
    """Helper: get profile as dict for matching."""
    profile = db.query(models.Student).filter(models.Student.id == profile_id).first()
    if not profile:
        return None
    return enrich_profile_dict(_profile_to_response(profile), db)
