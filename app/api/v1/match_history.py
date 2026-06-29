"""Match history endpoints: save and retrieve past match runs."""
import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user_id, get_profile_access_token, require_profile_owner
from app.db import get_db
from app.limiter import limiter
from app.api.v1.matches import _match_service_for_db
from app.api.v1.profiles import get_profile_dict
from app.api.v1.scholarships import get_cached_scholarship_dicts
from app.matching.hard_filters import is_application_deadline_passed
from app.serialization.scholarship import (
    MATCH_MINIMAL_EXTRA_KEYS,
    build_match_result_payload,
    build_stored_match_scoring,
    scholarship_card_fields,
    scholarship_to_catalog_dict,
)
from app.utils.notification_helpers import create_notifications_for_match_results
from app.utils.timezone import to_philippine_iso

router = APIRouter()
logger = logging.getLogger(__name__)


def _json_list_from_db(raw: str | None) -> list:
    """Parse JSON list from DB text; return [] on empty or invalid."""
    if not raw:
        return []
    try:
        out = json.loads(raw)
        return out if isinstance(out, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _json_dict_from_db(raw: str | None) -> dict | None:
    """Parse JSON object from DB text; return None on empty or invalid."""
    if not raw:
        return None
    try:
        out = json.loads(raw)
        return out if isinstance(out, dict) else None
    except (json.JSONDecodeError, TypeError):
        logger.warning("match_history_invalid_json_dict")
        return None


def _require_user_id(user_id: int | None) -> int:
    """Raise 401 if not authenticated. Match history requires auth."""
    if user_id is None:
        logger.warning("match_history_denied reason=not_authenticated")
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


def _result_to_match_response(
    r: models.MatchResult,
    scholarship: models.Scholarship,
    *,
    fields: str = "full",
) -> dict:
    """Build match response dict from MatchResult + Scholarship for display."""
    catalog = scholarship_to_catalog_dict(scholarship)
    scoring = build_stored_match_scoring(
        r,
        explanation=_json_list_from_db(r.explanation),
        breakdown=_json_dict_from_db(r.breakdown),
        suggestions=_json_list_from_db(r.suggestions),
        why_not_higher=_json_list_from_db(r.why_not_higher),
    )
    scoring["deadline_passed"] = is_application_deadline_passed(catalog.get("application_deadline"))
    payload = build_match_result_payload(catalog, scoring=scoring)
    if fields == "minimal":
        card = scholarship_card_fields(catalog)
        minimal = {k: card.get(k) for k in ("id", "title", "provider", "image_url", "image_alt")}
        for key in MATCH_MINIMAL_EXTRA_KEYS:
            if key in payload:
                minimal[key] = payload[key]
        return minimal
    return payload


@router.post("/match-runs")
@limiter.limit("20/minute")
def create_match_run(
    request: Request,
    body: schemas.CreateMatchRunRequest,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
    profile_token: Annotated[str | None, Depends(get_profile_access_token)] = None,
):
    """Run matching for a profile, save results, return run + matches. Requires auth."""
    uid = _require_user_id(user_id)
    require_profile_owner(body.profile_id, uid, db, profile_access_token=profile_token)

    profile = get_profile_dict(body.profile_id, db)
    if not profile:
        logger.warning("match_run_profile_not_found profile_id=%s user_id=%s", body.profile_id, uid)
        raise HTTPException(status_code=404, detail="Profile not found")

    scholarship_dicts = get_cached_scholarship_dicts(db)
    results, diagnostics = _match_service_for_db(db).get_matches(profile, scholarship_dicts)

    for r in results:
        if "final_score" in r and "score" not in r:
            r["score"] = r["final_score"]
        elif "score" in r and "final_score" not in r:
            r["final_score"] = r["score"]

    run = models.MatchRun(user_id=uid, profile_id=body.profile_id)
    db.add(run)
    db.flush()  # assign run.id without committing (atomic with results below)

    for r in results:
        mr = models.MatchResult(
            run_id=run.id,
            scholarship_id=r["id"],
            score=r.get("score", r.get("final_score", 0)),
            final_score=r.get("final_score", r.get("score")),
            explanation=json.dumps(r.get("explanation") or []),
            breakdown=json.dumps(r.get("breakdown")) if r.get("breakdown") else None,
            suggestions=json.dumps(r.get("suggestions") or []),
            confidence=r.get("confidence"),
            why_not_higher=json.dumps(r.get("why_not_higher") or []),
            scoring_policy_version=r.get("scoring_policy_version"),
        )
        db.add(mr)
    db.commit()
    db.refresh(run)

    try:
        create_notifications_for_match_results(db, uid, results)
    except Exception as notify_err:
        logger.warning(
            "match_run_notifications_failed run_id=%s user_id=%s err=%s",
            run.id,
            uid,
            notify_err,
        )

    logger.info("match_run_created run_id=%s user_id=%s profile_id=%s results=%s", run.id, uid, body.profile_id, len(results))

    return {
        "run_id": run.id,
        "profile_id": body.profile_id,
        "created_at": run.created_at.isoformat(),
        "ph_created_at": to_philippine_iso(run.created_at),
        "matches": results,
        "diagnostics": diagnostics,
    }


@router.get("/match-runs/compare", response_model=schemas.MatchComparisonResponse)
@limiter.limit("30/minute")
def compare_match_runs(
    request: Request,
    run_a: int,
    run_b: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Compare two match runs side-by-side. Requires auth and ownership."""
    uid = _require_user_id(user_id)

    run_a_obj = db.query(models.MatchRun).filter(models.MatchRun.id == run_a, models.MatchRun.user_id == uid).first()
    run_b_obj = db.query(models.MatchRun).filter(models.MatchRun.id == run_b, models.MatchRun.user_id == uid).first()
    if not run_a_obj or not run_b_obj:
        logger.warning("match_compare_run_not_found run_a=%s run_b=%s user_id=%s", run_a, run_b, uid)
        raise HTTPException(status_code=404, detail="Match run not found")

    res_a = {r.scholarship_id: r for r in db.query(models.MatchResult).filter(models.MatchResult.run_id == run_a).all()}
    res_b = {r.scholarship_id: r for r in db.query(models.MatchResult).filter(models.MatchResult.run_id == run_b).all()}

    all_scholarship_ids = set(res_a.keys()) | set(res_b.keys())
    scholarships = {s.id: s for s in db.query(models.Scholarship).filter(models.Scholarship.id.in_(all_scholarship_ids)).all()}

    items = []
    for sid in all_scholarship_ids:
        s = scholarships.get(sid)
        if not s:
            continue
        ra = res_a.get(sid)
        rb = res_b.get(sid)
        score_a = (ra.final_score if ra and ra.final_score is not None else ra.score) if ra else None
        score_b = (rb.final_score if rb and rb.final_score is not None else rb.score) if rb else None
        score_diff = None
        if score_a is not None and score_b is not None:
            score_diff = score_b - score_a
        items.append(schemas.MatchComparisonItem(
            scholarship_id=sid,
            title=s.title,
            provider=s.provider,
            score_a=score_a,
            score_b=score_b,
            score_diff=score_diff,
        ))

    items.sort(key=lambda x: (abs(x.score_diff or 0), -(x.score_b or x.score_a or 0)), reverse=True)

    count_a = len(res_a)
    count_b = len(res_b)
    return schemas.MatchComparisonResponse(
        run_a=schemas.MatchRunSummary(
            id=run_a_obj.id,
            profile_id=run_a_obj.profile_id,
            created_at=run_a_obj.created_at,
            result_count=count_a,
            ph_created_at=to_philippine_iso(run_a_obj.created_at),
        ),
        run_b=schemas.MatchRunSummary(
            id=run_b_obj.id,
            profile_id=run_b_obj.profile_id,
            created_at=run_b_obj.created_at,
            result_count=count_b,
            ph_created_at=to_philippine_iso(run_b_obj.created_at),
        ),
        items=items,
    )


@router.get("/match-runs", response_model=list[schemas.MatchRunSummary])
@limiter.limit("60/minute")
def list_match_runs(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """List user's past match runs. Requires auth."""
    uid = _require_user_id(user_id)

    runs = db.query(models.MatchRun).filter(models.MatchRun.user_id == uid).order_by(models.MatchRun.created_at.desc()).all()
    if not runs:
        return []
    run_ids = [r.id for r in runs]
    counts = dict(
        db.query(models.MatchResult.run_id, func.count(models.MatchResult.id))
        .filter(models.MatchResult.run_id.in_(run_ids))
        .group_by(models.MatchResult.run_id)
        .all()
    )
    out = []
    for r in runs:
        count = int(counts.get(r.id, 0))
        out.append(
            schemas.MatchRunSummary(
                id=r.id,
                profile_id=r.profile_id,
                created_at=r.created_at,
                result_count=count,
                ph_created_at=to_philippine_iso(r.created_at),
            )
        )
    return out


@router.get("/match-runs/{run_id}", response_model=schemas.MatchRunDetail)
@limiter.limit("60/minute")
def get_match_run(
    request: Request,
    run_id: int,
    fields: str = Query("full", pattern="^(minimal|full)$"),
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Get results for a specific run. Use ``fields=minimal`` for lightweight payloads."""
    uid = _require_user_id(user_id)

    run = db.query(models.MatchRun).filter(models.MatchRun.id == run_id).first()
    if not run or run.user_id != uid:
        logger.warning("match_run_get_not_found run_id=%s user_id=%s", run_id, uid)
        raise HTTPException(status_code=404, detail="Match run not found")

    results = db.query(models.MatchResult).filter(models.MatchResult.run_id == run_id).order_by(models.MatchResult.score.desc()).all()
    scholarship_ids = [r.scholarship_id for r in results]
    scholarships = {s.id: s for s in db.query(models.Scholarship).filter(models.Scholarship.id.in_(scholarship_ids)).all()}

    match_responses = []
    for r in results:
        s = scholarships.get(r.scholarship_id)
        if s:
            match_responses.append(_result_to_match_response(r, s, fields=fields))

    return schemas.MatchRunDetail(
        id=run.id,
        profile_id=run.profile_id,
        created_at=run.created_at,
        results=match_responses,
        ph_created_at=to_philippine_iso(run.created_at),
    )


@router.delete("/match-runs/{run_id}")
@limiter.limit("30/minute")
def delete_match_run(
    request: Request,
    run_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Delete a match run and its results. Requires auth and ownership."""
    uid = _require_user_id(user_id)

    run = db.query(models.MatchRun).filter(models.MatchRun.id == run_id).first()
    if not run or run.user_id != uid:
        logger.warning("match_run_delete_not_found run_id=%s user_id=%s", run_id, uid)
        raise HTTPException(status_code=404, detail="Match run not found")

    db.query(models.MatchResult).filter(models.MatchResult.run_id == run_id).delete(
        synchronize_session=False
    )
    db.delete(run)
    db.commit()

    logger.info("match_run_deleted run_id=%s user_id=%s", run_id, uid)
    return {"status": "deleted"}
