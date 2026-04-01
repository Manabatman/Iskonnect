import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.auth import assert_can_read_profile, get_current_user_id
from app.db import get_db
from app.limiter import limiter
from app.api.v1.profiles import get_profile_dict
from app.api.v1.scholarships import get_cached_scholarship_dicts
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


@router.get("/matches/{profile_id}")
@limiter.limit("30/minute")
def get_matches(
    request: Request,
    profile_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Get ranked matches for a profile. Requires auth in production; must own profile."""
    assert_can_read_profile(profile_id, db, user_id)
    profile = get_profile_dict(profile_id, db)
    if not profile:
        logger.warning("matches_profile_not_found profile_id=%s", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")

    scholarship_dicts = get_cached_scholarship_dicts(db)

    results = _match_service_for_db(db).get_matches(profile, scholarship_dicts)

    # Ensure backward compatibility: score alias
    for r in results:
        if "final_score" in r and "score" not in r:
            r["score"] = r["final_score"]
        elif "score" in r and "final_score" not in r:
            r["final_score"] = r["score"]

    response = {
        "matches": results,
        "profile_completeness": profile_completeness_payload(profile),
    }
    if len(results) == 0:
        upcoming = get_upcoming_scholarships(profile, scholarship_dicts)
        if upcoming:
            logger.info("matches_empty_upcoming_shown profile_id=%s count=%d", profile_id, len(upcoming))
            response["upcoming_scholarships"] = upcoming
    return response
