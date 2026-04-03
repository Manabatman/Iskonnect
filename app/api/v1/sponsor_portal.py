"""Sponsor-facing APIs: applications for scholarships owned by the sponsor org."""

from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.db import get_db
from app.limiter import limiter
from app.api.v1.scholarships import _scholarship_to_response

router = APIRouter(tags=["sponsor"])


def _sponsor_for_user(db: Session, user: models.User) -> tuple[models.Sponsor, models.SponsorUser] | None:
    if getattr(user, "role", "") != "sponsor":
        return None
    link = db.query(models.SponsorUser).filter(models.SponsorUser.user_id == user.id).first()
    if not link:
        return None
    sp = db.query(models.Sponsor).filter(models.Sponsor.id == link.sponsor_id).first()
    if not sp:
        return None
    return sp, link


SPONSOR_REVIEW_STATUSES = frozenset(
    {
        "preparing",
        "submitted",
        "under_review",
        "shortlisted",
        "accepted",
        "rejected",
        "waitlisted",
    }
)


class SponsorReviewBody(BaseModel):
    status: str
    note: Optional[str] = None


class SponsorApplicationOut(BaseModel):
    application_id: int
    user_id: int
    scholarship_id: int
    status: str
    scholarship_title: str
    updated_at: datetime


@router.get("/sponsor/applications", response_model=list[SponsorApplicationOut])
@limiter.limit("60/minute")
def list_sponsor_applications(
    request: Request,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    pair = _sponsor_for_user(db, user)
    if not pair:
        raise HTTPException(status_code=403, detail="Sponsor access required")
    sponsor, _ = pair
    sch_ids = [
        r[0]
        for r in db.query(models.Scholarship.id).filter(models.Scholarship.sponsor_id == sponsor.id).all()
    ]
    if not sch_ids:
        return []
    apps = (
        db.query(models.Application)
        .filter(models.Application.scholarship_id.in_(sch_ids))
        .order_by(models.Application.updated_at.desc())
        .all()
    )
    out: list[SponsorApplicationOut] = []
    for a in apps:
        sch = db.query(models.Scholarship).filter(models.Scholarship.id == a.scholarship_id).first()
        out.append(
            SponsorApplicationOut(
                application_id=a.id,
                user_id=a.user_id,
                scholarship_id=a.scholarship_id,
                status=a.status,
                scholarship_title=sch.title if sch else "?",
                updated_at=a.updated_at,
            )
        )
    return out


@router.get("/sponsor/scholarships")
@limiter.limit("60/minute")
def list_sponsor_scholarships(
    request: Request,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    pair = _sponsor_for_user(db, user)
    if not pair:
        raise HTTPException(status_code=403, detail="Sponsor access required")
    sponsor, _ = pair
    rows = db.query(models.Scholarship).filter(models.Scholarship.sponsor_id == sponsor.id).all()
    return [_scholarship_to_response(s) for s in rows]


@router.patch("/sponsor/applications/{application_id}/review", response_model=SponsorApplicationOut)
@limiter.limit("60/minute")
def sponsor_review_application(
    request: Request,
    application_id: int,
    body: SponsorReviewBody,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    """Update application status for a scholarship owned by this sponsor (creates status event)."""
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    pair = _sponsor_for_user(db, user)
    if not pair:
        raise HTTPException(status_code=403, detail="Sponsor access required")
    sponsor, _ = pair
    if body.status not in SPONSOR_REVIEW_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid status")

    app_row = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app_row.scholarship_id).first()
    if not sch or sch.sponsor_id != sponsor.id:
        raise HTTPException(status_code=403, detail="Not authorized for this application")

    prev = app_row.status
    app_row.status = body.status
    db.add(
        models.ApplicationStatusEvent(
            application_id=app_row.id,
            from_status=prev,
            to_status=body.status,
            actor_id=user.id,
            note=body.note.strip() if body.note else None,
        )
    )
    db.commit()
    db.refresh(app_row)
    return SponsorApplicationOut(
        application_id=app_row.id,
        user_id=app_row.user_id,
        scholarship_id=app_row.scholarship_id,
        status=app_row.status,
        scholarship_title=sch.title if sch else "?",
        updated_at=app_row.updated_at,
    )
