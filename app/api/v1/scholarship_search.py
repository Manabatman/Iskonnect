"""
Scholarship search API - browse and filter scholarships without running the matching algorithm.
Endpoints: GET /scholarships/search, GET /scholarships/search/filters
"""

import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy import and_, case, func, or_
from sqlalchemy.orm import Session

from datetime import date

from app import models, schemas
from app.api.v1.scholarships import _scholarship_to_response, get_cached_scholarship_dicts
from app.db import get_db
from app.limiter import limiter
from app.utils.application_status import (
    ARCHIVED,
    CLOSED,
    EXPECTED_REOPEN,
    NEEDS_VERIFICATION,
    OPEN,
    PREVIOUS_CYCLE,
    TIMING_FILTER_MAP,
)
from app.utils.jsonb_filters import json_list_contains

router = APIRouter(prefix="/scholarships", tags=["scholarship-search"])
logger = logging.getLogger(__name__)

TIMING_OPTIONS = [
    "any",
    "open_now",
    "opening_soon",
    "closed",
    "previous_cycle",
    "expected_reopen",
    "needs_verification",
    "archived",
]


def _column_empty_json_list(col):
    """SQL expression: NULL, blank, or JSON empty list [] (stored as text)."""
    trimmed = func.trim(func.coalesce(col, ""))
    return or_(
        col.is_(None),
        trimmed == "",
        trimmed == "[]",
    )


def _column_empty_legacy_regions(col):
    """Legacy CSV `regions` column — empty means no region list."""
    trimmed = func.trim(func.coalesce(col, ""))
    return or_(
        col.is_(None),
        trimmed == "",
    )


def _nationwide_geo_sql():
    """No geographic restriction stored — treat as open to all regions (matches hard_filters nationwide)."""
    return and_(
        _column_empty_json_list(models.Scholarship.eligible_regions),
        _column_empty_legacy_regions(models.Scholarship.regions),
        _column_empty_json_list(models.Scholarship.eligible_cities),
    )


def apply_region_browse_filter(query, region: str):
    """Restrict query to rows that list the region or have no geo restriction (nationwide)."""
    val = region.strip()
    return query.filter(
        or_(
            models.Scholarship.eligible_regions.ilike(f'%"{val}"%'),
            models.Scholarship.regions.ilike(f"%{val}%"),
            _nationwide_geo_sql(),
        )
    )


def apply_education_level_browse_filter(query, education_level: str):
    val = education_level.strip()
    return query.filter(
        or_(
            models.Scholarship.eligible_levels.is_(None),
            models.Scholarship.eligible_levels == "",
            models.Scholarship.eligible_levels == "[]",
            json_list_contains(models.Scholarship.eligible_levels, val),
        )
    )


LIFE_STAGE_LEVELS = {
    "high_school": ["Senior High School", "Grade 11", "Grade 12"],
    "college": ["College", "Undergraduate"],
    "graduate": ["Graduate", "Masters", "Doctorate"],
    "tvet": ["TVET", "Technical-Vocational"],
}


def apply_timing_filter(query, timing: str, today: date | None = None):
    """Filter by authoritative application_status (with date fallback for unmigrated rows)."""
    today = today or date.today()
    t = timing.strip().lower()
    if t in ("", "any"):
        return query

    if t == "opening_soon":
        return query.filter(
            models.Scholarship.application_open_date > today,
            or_(
                models.Scholarship.application_status == OPEN,
                models.Scholarship.application_status.is_(None),
            ),
        )

    status_set = TIMING_FILTER_MAP.get(t)
    if status_set:
        clauses = [models.Scholarship.application_status.in_(sorted(status_set))]
        if OPEN in status_set:
            clauses.append(models.Scholarship.application_status.is_(None))
        return query.filter(or_(*clauses))

    return query


def apply_life_stage_filter(query, life_stage: str):
    stage = life_stage.strip().lower()
    levels = LIFE_STAGE_LEVELS.get(stage)
    if not levels:
        return query
    clauses = []
    for lit in levels:
        clauses.append(models.Scholarship.eligible_levels.ilike(f'%"{lit}"%'))
        clauses.append(models.Scholarship.level.ilike(f"%{lit}%"))
    return query.filter(or_(*clauses))


def _base_search_query(db: Session, *, include_archived: bool = False):
    """Default catalog: all non-archived scholarships, including needs_verification."""
    q = db.query(models.Scholarship)
    if not include_archived:
        q = q.filter(
            models.Scholarship.is_active != False,  # noqa: E712
            or_(
                models.Scholarship.application_status.is_(None),
                models.Scholarship.application_status != ARCHIVED,
            ),
        )
    return q


def _status_priority_order(today: date | None = None):
    """Canonical browse ordering: open → opening soon → expected reopen → past → closed → needs verification → archived."""
    today = today or date.today()
    open_status = or_(
        models.Scholarship.application_status == OPEN,
        models.Scholarship.application_status.is_(None),
    )
    return case(
        (
            and_(
                open_status,
                or_(
                    models.Scholarship.application_open_date.is_(None),
                    models.Scholarship.application_open_date <= today,
                ),
            ),
            0,
        ),
        (
            and_(open_status, models.Scholarship.application_open_date > today),
            1,
        ),
        (models.Scholarship.application_status == EXPECTED_REOPEN, 2),
        (models.Scholarship.application_status == PREVIOUS_CYCLE, 3),
        (models.Scholarship.application_status == CLOSED, 4),
        (models.Scholarship.application_status == NEEDS_VERIFICATION, 5),
        (models.Scholarship.application_status == ARCHIVED, 6),
        else_=7,
    )


def _apply_search_ordering(query, today: date | None = None):
    today = today or date.today()
    priority = _status_priority_order(today)
    deadline_sort = case(
        (models.Scholarship.application_deadline.is_(None), 1),
        else_=0,
    )
    return query.order_by(
        priority.asc(),
        deadline_sort.asc(),
        models.Scholarship.application_deadline.asc(),
        models.Scholarship.title.asc(),
        models.Scholarship.id.asc(),
    )


def _parse_json(val, default=None):
    """Parse JSON or CSV string to list."""
    if val is None:
        return default if default is not None else []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            p = json.loads(val)
            return p if isinstance(p, list) else (default or [])
        except (json.JSONDecodeError, TypeError):
            return [x.strip() for x in val.split(",") if x.strip()] or (default or [])
    return default or []


@router.get("/search/filters", response_model=schemas.ScholarshipFilterOptions)
@limiter.limit("60/minute")
def get_search_filter_options(
    request: Request,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Return distinct filter values for search UI dropdowns."""
    logger.info("scholarship_search_filters")
    scholarship_dicts = get_cached_scholarship_dicts(db)
    providers = set()
    education_levels = set()
    regions = set()
    fields_of_study = set()
    for d in scholarship_dicts:
        prov = d.get("provider")
        if prov and str(prov).strip():
            providers.add(str(prov).strip())
        for level in _parse_json(d.get("eligible_levels")):
            if level and str(level).strip():
                education_levels.add(str(level).strip())
        for r in _parse_json(d.get("eligible_regions")) or _parse_json(d.get("regions")):
            if r and str(r).strip():
                regions.add(str(r).strip())
        for f in _parse_json(d.get("eligible_courses_psced")):
            if f and str(f).strip():
                fields_of_study.add(str(f).strip())
    return schemas.ScholarshipFilterOptions(
        providers=sorted(providers),
        education_levels=sorted(education_levels),
        regions=sorted(regions),
        fields_of_study=sorted(fields_of_study),
        timing_options=TIMING_OPTIONS,
        life_stages=list(LIFE_STAGE_LEVELS.keys()),
    )


@router.get("/search", response_model=schemas.ScholarshipSearchResponse)
@limiter.limit("60/minute")
def search_scholarships(
    request: Request,
    query: str = "",
    region: str = "",
    field: str = "",
    education_level: str = "",
    provider: str = "",
    school: str = "",
    max_income: int | None = None,
    timing: str = "",
    life_stage: str = "",
    include_archived: bool = False,
    include_closed: bool = False,
    page: int = 1,
    limit: int = 20,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """
    Search scholarships with optional filters and pagination.
    Does not run the matching algorithm - browse-only.
    ``include_closed`` is deprecated; use ``timing=closed`` or ``include_archived``.
    """
    logger.info(
        "scholarship_search query=%s region=%s field=%s page=%s",
        query[:50] if query else "",
        region[:30] if region else "",
        field[:30] if field else "",
        page,
    )
    limit = min(max(1, limit), 50)
    page = max(1, page)
    offset = (page - 1) * limit

    show_archived = include_archived or (timing.strip().lower() == "archived")
    q = _base_search_query(db, include_archived=show_archived)

    if timing and timing.strip():
        q = apply_timing_filter(q, timing)
    elif include_closed:
        q = apply_timing_filter(q, "closed")

    if life_stage and life_stage.strip():
        q = apply_life_stage_filter(q, life_stage)

    if query and query.strip():
        pattern = f"%{query.strip()}%"
        q = q.filter(
            or_(
                models.Scholarship.title.ilike(pattern),
                models.Scholarship.description.ilike(pattern),
                models.Scholarship.provider.ilike(pattern),
            )
        )

    if region and region.strip():
        q = apply_region_browse_filter(q, region)

    if field and field.strip():
        val = field.strip()
        q = q.filter(
            or_(
                models.Scholarship.eligible_courses_psced.ilike(f'%"{val}"%'),
                models.Scholarship.eligible_courses_psced.ilike(f"%{val}%"),
            )
        )

    if education_level and education_level.strip():
        q = apply_education_level_browse_filter(q, education_level)

    if provider and provider.strip():
        pattern = f"%{provider.strip()}%"
        q = q.filter(models.Scholarship.provider.ilike(pattern))

    if school and school.strip():
        pattern = f"%{school.strip()}%"
        q = q.filter(
            or_(
                models.Scholarship.title.ilike(pattern),
                models.Scholarship.provider.ilike(pattern),
                models.Scholarship.description.ilike(pattern),
                models.Scholarship.eligible_school_types.ilike(pattern),
            )
        )

    if max_income is not None and max_income >= 0:
        q = q.filter(
            or_(
                models.Scholarship.max_income_threshold.is_(None),
                models.Scholarship.max_income_threshold >= max_income,
            )
        )

    q = _apply_search_ordering(q)
    total = q.count()
    scholarships = q.offset(offset).limit(limit).all()
    results = [_scholarship_to_response(s) for s in scholarships]
    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return schemas.ScholarshipSearchResponse(
        results=results,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )


@router.get("/search/semantic", response_model=schemas.ScholarshipSearchResponse)
@limiter.limit("60/minute")
def search_scholarships_semantic(
    request: Request,
    query: str = "",
    region: str = "",
    field: str = "",
    education_level: str = "",
    provider: str = "",
    school: str = "",
    max_income: int | None = None,
    timing: str = "",
    life_stage: str = "",
    include_archived: bool = False,
    include_closed: bool = False,
    page: int = 1,
    limit: int = 20,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Same filters as ``/search``, but text ``query`` matches title, description, or provider."""
    logger.info("scholarship_search_semantic query=%s page=%s", query[:50] if query else "", page)
    limit = min(max(1, limit), 50)
    page = max(1, page)
    offset = (page - 1) * limit

    show_archived = include_archived or (timing.strip().lower() == "archived")
    q = _base_search_query(db, include_archived=show_archived)

    if timing and timing.strip():
        q = apply_timing_filter(q, timing)
    elif include_closed:
        q = apply_timing_filter(q, "closed")

    if life_stage and life_stage.strip():
        q = apply_life_stage_filter(q, life_stage)

    if query and query.strip():
        pattern = f"%{query.strip()}%"
        q = q.filter(
            or_(
                models.Scholarship.title.ilike(pattern),
                models.Scholarship.description.ilike(pattern),
                models.Scholarship.provider.ilike(pattern),
            )
        )

    if region and region.strip():
        q = apply_region_browse_filter(q, region)

    if field and field.strip():
        val = field.strip()
        q = q.filter(
            or_(
                models.Scholarship.eligible_courses_psced.ilike(f'%"{val}"%'),
                models.Scholarship.eligible_courses_psced.ilike(f"%{val}%"),
            )
        )

    if education_level and education_level.strip():
        q = apply_education_level_browse_filter(q, education_level)

    if provider and provider.strip():
        pattern = f"%{provider.strip()}%"
        q = q.filter(models.Scholarship.provider.ilike(pattern))

    if school and school.strip():
        pattern = f"%{school.strip()}%"
        q = q.filter(
            or_(
                models.Scholarship.title.ilike(pattern),
                models.Scholarship.provider.ilike(pattern),
                models.Scholarship.description.ilike(pattern),
                models.Scholarship.eligible_school_types.ilike(pattern),
            )
        )

    if max_income is not None and max_income >= 0:
        q = q.filter(
            or_(
                models.Scholarship.max_income_threshold.is_(None),
                models.Scholarship.max_income_threshold >= max_income,
            )
        )

    q = _apply_search_ordering(q)
    total = q.count()
    scholarships = q.offset(offset).limit(limit).all()
    results = [_scholarship_to_response(s) for s in scholarships]
    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return schemas.ScholarshipSearchResponse(
        results=results,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )
