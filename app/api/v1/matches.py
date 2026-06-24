import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app import models
from app.auth import assert_can_read_profile, get_current_user_id, get_profile_access_token
from app.db import get_db
from app.limiter import limiter
from app.api.v1.profiles import get_profile_dict
from app.api.v1.scholarships import get_cached_scholarship_dicts, _scholarship_to_response
from app.config import settings
from app.matching.match_service import MatchService
from app.matching.profile_completeness import profile_completeness_payload
from app.prediction.cycle_predictor import get_upcoming_scholarships
from app.scoring import WeightedDeterministicScorer
from app.scoring.config import ScoringConfig

router = APIRouter()
logger = logging.getLogger(__name__)
match_service = MatchService()


def _match_service_for_db(db: Session) -> MatchService:
    if settings.db_driven_weights:
        config = ScoringConfig.from_db(db)
        return MatchService(scoring_engine=WeightedDeterministicScorer(config=config))
    return match_service


def _prefilter_scholarships_query(db: Session, profile: dict):
    """SQL prefilter: active scholarships matching profile education level or nationwide."""
    q = db.query(models.Scholarship).filter(models.Scholarship.is_active != False)  # noqa: E712
    level = (profile.get("education_level") or "").strip()
    if level:
        q = q.filter(
            (models.Scholarship.eligible_levels.ilike(f'%"{level}"%'))
            | (models.Scholarship.eligible_levels.is_(None))
            | (models.Scholarship.eligible_levels == "")
            | (models.Scholarship.eligible_levels == "[]")
        )
    region = (profile.get("region") or "").strip()
    if region:
        q = q.filter(
            (models.Scholarship.eligible_regions.ilike(f'%"{region}"%'))
            | (models.Scholarship.regions.ilike(f"%{region}%"))
            | (models.Scholarship.eligible_regions.is_(None))
            | (models.Scholarship.eligible_regions == "")
            | (models.Scholarship.eligible_regions == "[]")
        )
    return q


def _scholarship_rows_to_dicts(rows: list[models.Scholarship]) -> list[dict]:
    return [_scholarship_to_response(r) for r in rows]


@router.get("/matches/{profile_id}")
@limiter.limit("30/minute")
def get_matches(
    request: Request,
    profile_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    """Return ranked scholarship matches for a student profile.

    Runs the two-stage pipeline: Stage 1 hard filters discard ineligible
    scholarships; Stage 2 scores survivors with the weighted deterministic matrix.
    Requires auth in production and profile ownership.
    """
    assert_can_read_profile(profile_id, db, user_id, profile_token)
    profile = get_profile_dict(profile_id, db)
    if not profile:
        logger.warning("matches_profile_not_found profile_id=%s", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")

    if settings.filter_expired_from_matches:
        prefetched = _prefilter_scholarships_query(db, profile).all()
        scholarship_dicts = _scholarship_rows_to_dicts(prefetched)
    else:
        scholarship_dicts = get_cached_scholarship_dicts(db)

    results, diagnostics = _match_service_for_db(db).get_matches(profile, scholarship_dicts)
    total = len(results)
    results = results[offset : offset + limit]

    # Legacy mobile clients expect ``score`` alongside ``final_score``.
    for r in results:
        if "final_score" in r and "score" not in r:
            r["score"] = r["final_score"]
        elif "score" in r and "final_score" not in r:
            r["final_score"] = r["score"]

    response = {
        "matches": results,
        "total": total,
        "limit": limit,
        "offset": offset,
        "profile_completeness": profile_completeness_payload(profile),
        "diagnostics": diagnostics,
    }
    if len(results) == 0:
        upcoming = get_upcoming_scholarships(profile, scholarship_dicts)
        if upcoming:
            logger.info("matches_empty_upcoming_shown profile_id=%s count=%d", profile_id, len(upcoming))
            response["upcoming_scholarships"] = upcoming
    return response
