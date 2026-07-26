"""
Autocomplete suggestions API for profile form fields.
Endpoints: schools, courses, regions, provinces, scholarships.
"""

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user_id
from app.db import get_db
from app.limiter import limiter
from app.models import Scholarship
from app.taxonomy.provinces import ALL_PROVINCES, PROVINCES_BY_REGION
from app.taxonomy.psced_fields import PSCED_SPECIFIC_COURSES
from app.taxonomy.regions import PHILIPPINE_REGIONS
from app.taxonomy.schools import PHILIPPINE_SCHOOLS
from app.taxonomy.profile_constants import (
    ACADEMIC_STAGES,
    CITIZENSHIP_OPTIONS,
    EDUCATION_LEVELS,
    ENROLLMENT_STATUSES,
    GWA_SCALES,
    SCHOOL_TYPES,
    YEAR_LEVELS,
)
from app.utils.fuzzy_search import fuzzy_search

router = APIRouter(prefix="/suggestions", tags=["suggestions"])
logger = logging.getLogger(__name__)

# Flatten courses from PSCED taxonomy
ALL_COURSES: list[str] = []
for courses in PSCED_SPECIFIC_COURSES.values():
    for c in courses:
        if c not in ALL_COURSES:
            ALL_COURSES.append(c)


@router.get("/profile-options")
@limiter.limit("60/minute")
def get_profile_options(request: Request):
    """Profile builder constants shared with the frontend."""
    return {
        "education_levels": EDUCATION_LEVELS,
        "academic_stages": ACADEMIC_STAGES,
        "school_types": SCHOOL_TYPES,
        "gwa_scales": GWA_SCALES,
        "enrollment_statuses": ENROLLMENT_STATUSES,
        "year_levels": YEAR_LEVELS,
        "citizenship_options": CITIZENSHIP_OPTIONS,
    }


@router.get("/schools")
@limiter.limit("60/minute")
def get_school_suggestions(request: Request, q: str = ""):
    """Suggest schools matching query. Fuzzy search over curated HEI list."""
    logger.info("suggestions_schools q=%s", q[:50] if q else "")
    results = fuzzy_search(q, list(PHILIPPINE_SCHOOLS), limit=10)
    return {"suggestions": results}


@router.get("/courses")
@limiter.limit("60/minute")
def get_course_suggestions(request: Request, q: str = ""):
    """Suggest courses matching query. Fuzzy search over PSCED taxonomy."""
    logger.info("suggestions_courses q=%s", q[:50] if q else "")
    results = fuzzy_search(q, ALL_COURSES, limit=10)
    return {"suggestions": results}


@router.get("/regions")
@limiter.limit("60/minute")
def get_region_suggestions(request: Request, q: str = ""):
    """Suggest regions matching query. Fuzzy search over Philippine regions."""
    logger.info("suggestions_regions q=%s", q[:50] if q else "")
    results = fuzzy_search(q, list(PHILIPPINE_REGIONS), limit=10)
    return {"suggestions": results}


@router.get("/provinces")
@limiter.limit("60/minute")
def get_province_suggestions(request: Request, q: str = "", region: str = ""):
    """Suggest provinces matching query. Optionally filter by region."""
    logger.info("suggestions_provinces q=%s region=%s", q[:50] if q else "", region[:30] if region else "")
    pool = PROVINCES_BY_REGION.get(region.strip(), ALL_PROVINCES) if region and region.strip() else ALL_PROVINCES
    results = fuzzy_search(q, pool, limit=10)
    return {"suggestions": results}


@router.get("/scholarships")
@limiter.limit("60/minute")
def get_scholarship_suggestions(
    request: Request,
    q: str = "",
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Suggest scholarships by title. Queries DB with ILIKE."""
    logger.info("suggestions_scholarships q=%s", q[:50] if q else "")
    if not q or not q.strip():
        return {"suggestions": []}
    pattern = f"%{q.strip()}%"
    rows = (
        db.query(Scholarship.title)
        .filter(Scholarship.is_active == True, Scholarship.title.ilike(pattern))
        .limit(10)
        .all()
    )
    suggestions = [r[0] for r in rows if r[0]]
    return {"suggestions": suggestions}


@router.get("/readiness")
@limiter.limit("30/minute")
def readiness_suggestions(
    request: Request,
    profile_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """
    Deterministic, inspectable tips to improve application readiness (profile gaps).
    Not AI-ranked — rules-based only.
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    tips: list[str] = []
    if profile_id is None:
        tips.append("Open your profile and confirm region, education level, and field of study.")
        tips.append("Run a fresh match after updating your profile for up-to-date suggestions.")
        return {"suggestions": tips}

    prof = (
        db.query(models.Student)
        .filter(models.Student.id == profile_id, models.Student.user_id == user_id)
        .first()
    )
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")

    if not (prof.full_name or "").strip():
        tips.append("Add your full legal name — many forms require an exact match.")
    if not (prof.region or "").strip():
        tips.append("Set your region to unlock geo-filtered scholarships.")
    if not (prof.education_level or prof.current_academic_stage or "").strip():
        tips.append("Specify your education level or current stage.")
    if not (prof.field_of_study_broad or "").strip():
        tips.append("Add a field of study so course-based scholarships can match.")
    if prof.gwa_normalized is None and not (prof.gwa_raw or "").strip():
        tips.append("Enter your GWA so academic criteria can be evaluated.")
    if prof.household_income_annual is None and not (prof.income_bracket or "").strip():
        tips.append("Add household income or income bracket for need-based programs.")

    if not tips:
        tips.append("Profile looks complete for matching — track applications and document checklists next.")

    return {"suggestions": tips}
