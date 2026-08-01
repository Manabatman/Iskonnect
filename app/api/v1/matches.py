import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app import models
from app.auth import assert_can_read_profile, get_optional_user_id, get_profile_access_token
from app.db import get_db
from app.limiter import limiter
from app.api.v1.profiles import get_profile_dict
from app.api.v1.scholarships import get_cached_scholarship_dicts, _scholarship_to_dict
from app.config import settings
from app.matching.match_service import MatchService
from app.matching.preparation import build_preparation_plan
from app.matching.profile_completeness import profile_completeness_payload
from app.matching.opportunity_timeline import build_opportunity_timeline
from app.plan_cache import get_cached_plan, plan_cache_key, set_cached_plan
from app.prediction.cycle_predictor import get_upcoming_scholarships
from app.scoring import WeightedDeterministicScorer
from app.scoring.config import ScoringConfig
from app.taxonomy.education_levels import level_search_literals
from app.utils.data_completeness import is_publishable
from app.utils.server_timing import ServerTiming

router = APIRouter()
logger = logging.getLogger(__name__)
match_service = MatchService()


def _match_service_for_db(db: Session) -> MatchService:
    if settings.db_driven_weights:
        config = ScoringConfig.from_db(db)
        return MatchService(scoring_engine=WeightedDeterministicScorer(config=config))
    return match_service


def _prefilter_scholarships_query(db: Session, profile: dict):
    """SQL prefilter: active scholarships; level synonyms OR nationwide level lists."""
    from sqlalchemy import or_

    from app.utils.jsonb_filters import json_list_contains, json_list_empty

    q = db.query(models.Scholarship).filter(models.Scholarship.is_active != False)  # noqa: E712
    level = (profile.get("education_level") or "").strip()
    if level:
        literals = level_search_literals(level)
        level_clauses = [json_list_empty(models.Scholarship.eligible_levels)]
        for lit in literals:
            level_clauses.append(json_list_contains(models.Scholarship.eligible_levels, lit))
        q = q.filter(or_(*level_clauses))
    return q


def _scholarship_rows_to_dicts(rows: list[models.Scholarship]) -> list[dict]:
    return [_scholarship_to_dict(r) for r in rows]


def _scholarship_dicts_for_profile(db: Session, profile: dict) -> list[dict]:
    if settings.plan_prefilter_enabled:
        rows = _prefilter_scholarships_query(db, profile).all()
        dicts = _scholarship_rows_to_dicts(rows)
        return [d for d in dicts if is_publishable(d)]
    return get_cached_scholarship_dicts(db)


def _normalize_match_scores(results: list[dict]) -> None:
    for r in results:
        if "final_score" in r and "score" not in r:
            r["score"] = r["final_score"]
        elif "score" in r and "final_score" not in r:
            r["final_score"] = r["score"]


def _build_plan_response(
    profile_id: int,
    profile: dict,
    scholarship_dicts: list[dict],
    db: Session,
    *,
    limit: int,
    offset: int,
) -> dict:
    svc = _match_service_for_db(db)
    all_results, diagnostics = svc.get_matches(profile, scholarship_dicts)
    _normalize_match_scores(all_results)

    timeline = build_opportunity_timeline(profile, scholarship_dicts, all_results)
    preparation = build_preparation_plan(profile, all_results)

    total = len(all_results)
    matches_page = all_results[offset : offset + limit]

    response = {
        "matches": matches_page,
        "total": total,
        "limit": limit,
        "offset": offset,
        "timeline": timeline,
        "preparation": preparation,
        "profile_completeness": profile_completeness_payload(profile),
        "diagnostics": diagnostics,
    }
    if total == 0:
        upcoming = get_upcoming_scholarships(profile, scholarship_dicts)
        if upcoming:
            logger.info("plan_empty_upcoming_shown profile_id=%s count=%d", profile_id, len(upcoming))
            response["upcoming_scholarships"] = upcoming
    return response


@router.get("/plan/{profile_id}")
@limiter.limit("30/minute")
def get_plan(
    request: Request,
    response: Response,
    profile_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    """Unified planning endpoint: matches, timeline, preparation, and diagnostics."""
    timing = ServerTiming()
    with timing.measure("auth"):
        assert_can_read_profile(profile_id, db, user_id, profile_token)
    with timing.measure("profile-load"):
        profile = get_profile_dict(profile_id, db)
    if not profile:
        logger.warning("plan_profile_not_found profile_id=%s", profile_id)
        timing.attach(response)
        raise HTTPException(status_code=404, detail="Profile not found")

    cache_key = plan_cache_key(profile_id, profile, limit=limit, offset=offset)
    with timing.measure("cache-lookup"):
        cached = get_cached_plan(cache_key)

    if cached is not None:
        with timing.measure("cache-hit"):
            timing.attach(response)
            return cached

    with timing.measure("scholarships"):
        scholarship_dicts = _scholarship_dicts_for_profile(db, profile)
    with timing.measure("match"):
        plan_response = _build_plan_response(
            profile_id,
            profile,
            scholarship_dicts,
            db,
            limit=limit,
            offset=offset,
        )
    with timing.measure("cache-store"):
        set_cached_plan(cache_key, plan_response)

    timing.attach(response)
    return plan_response
