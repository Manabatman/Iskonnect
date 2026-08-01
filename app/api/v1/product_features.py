"""Onboarding sample matches (value-first preview before full profile)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.v1.scholarships import get_cached_scholarship_dicts
from app.db import get_db
from app.limiter import limiter
from app.matching.match_service import MatchService
from app.matching.opportunity_timeline import build_opportunity_timeline

router = APIRouter(tags=["product"])
match_service = MatchService()


def _partial_profile_from_query(
    education_level: str = "",
    region: str = "",
    age: int | None = None,
    gwa_normalized: float | None = None,
    household_income_annual: int | None = None,
    field_of_study_broad: str = "",
) -> dict:
    return {
        "education_level": education_level or None,
        "region": region or None,
        "age": age,
        "gwa_normalized": gwa_normalized,
        "household_income_annual": household_income_annual,
        "field_of_study_broad": field_of_study_broad or None,
    }


@router.get("/profiles/sample-matches")
@limiter.limit("20/minute")
def get_sample_matches(
    request: Request,
    education_level: str = "",
    region: str = "",
    age: int | None = None,
    gwa_normalized: float | None = None,
    household_income_annual: int | None = None,
    field_of_study_broad: str = "",
    limit: int = Query(6, ge=1, le=12),
    db: Session = Depends(get_db),
):
    """Value-first onboarding: preview matches from minimal fields (no consent required)."""
    profile = _partial_profile_from_query(
        education_level=education_level,
        region=region,
        age=age,
        gwa_normalized=gwa_normalized,
        household_income_annual=household_income_annual,
        field_of_study_broad=field_of_study_broad,
    )
    scholarships = get_cached_scholarship_dicts(db)
    results, _ = match_service.get_matches(profile, scholarships)
    timeline = build_opportunity_timeline(profile, scholarships, results)
    return {
        "sample_matches": results[:limit],
        "timeline": timeline,
        "disclaimer": "Preview only — complete your profile and consent for personalized matching.",
    }
