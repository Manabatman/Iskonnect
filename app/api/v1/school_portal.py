"""School verifier APIs."""

from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.db import get_db
from app.limiter import limiter

router = APIRouter(tags=["school"])


def _school_for_user(db: Session, user: models.User) -> tuple[models.School, models.SchoolUser] | None:
    if getattr(user, "role", "") != "school_verifier":
        return None
    link = db.query(models.SchoolUser).filter(models.SchoolUser.user_id == user.id).first()
    if not link:
        return None
    sc = db.query(models.School).filter(models.School.id == link.school_id).first()
    if not sc:
        return None
    return sc, link


class VerificationOut(BaseModel):
    id: int
    application_id: int
    school_id: int
    verification_type: str
    status: str
    requested_at: datetime
    verified_at: Optional[datetime] = None
    notes: Optional[str] = None


class VerificationPatch(BaseModel):
    status: str
    notes: Optional[str] = None


@router.get("/school/verifications", response_model=list[VerificationOut])
@limiter.limit("60/minute")
def list_verifications(
    request: Request,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    pair = _school_for_user(db, user)
    if not pair:
        raise HTTPException(status_code=403, detail="School verifier access required")
    school, _ = pair
    rows = (
        db.query(models.VerificationRequest)
        .filter(models.VerificationRequest.school_id == school.id)
        .order_by(models.VerificationRequest.requested_at.desc())
        .all()
    )
    return [VerificationOut.model_validate(r) for r in rows]


@router.patch("/school/verifications/{verification_id}", response_model=VerificationOut)
@limiter.limit("30/minute")
def patch_verification(
    request: Request,
    verification_id: int,
    body: VerificationPatch,
    db: Session = Depends(get_db),
    user: Annotated[models.User | None, Depends(get_current_user)] = None,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    pair = _school_for_user(db, user)
    if not pair:
        raise HTTPException(status_code=403, detail="School verifier access required")
    school, _ = pair
    row = (
        db.query(models.VerificationRequest)
        .filter(
            models.VerificationRequest.id == verification_id,
            models.VerificationRequest.school_id == school.id,
        )
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Verification not found")
    row.status = body.status
    if body.notes is not None:
        row.notes = body.notes
    if body.status in ("approved", "rejected"):
        row.verified_at = datetime.now(timezone.utc)
        row.verifier_id = user.id
    db.commit()
    db.refresh(row)
    return VerificationOut.model_validate(row)
