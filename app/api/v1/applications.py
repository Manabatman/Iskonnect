"""Student applications to scholarships (server-backed lifecycle)."""

import json
import logging
from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user_id
from app.db import get_db
from app.limiter import limiter
from app.api.v1.scholarships import _scholarship_to_response

router = APIRouter(tags=["applications"])
logger = logging.getLogger(__name__)


ALLOWED_STATUS = frozenset(
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


class ApplicationCreate(BaseModel):
    scholarship_id: int


class ApplicationPatch(BaseModel):
    status: str
    notes: Optional[str] = None


class DocumentChecklistPatch(BaseModel):
    status: str
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    scholarship_id: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    scholarship: Optional[dict[str, Any]] = None

    class Config:
        from_attributes = True


class StatusEventOut(BaseModel):
    id: int
    from_status: Optional[str] = None
    to_status: str
    actor_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentChecklistOut(BaseModel):
    id: int
    application_id: int
    document_type: str
    status: str
    notes: Optional[str] = None
    file_url: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True


def _require_uid(uid: int | None) -> int:
    if uid is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return uid


def _seed_checklist_from_scholarship(db: Session, app: models.Application, sch: models.Scholarship) -> None:
    if not sch.required_documents:
        return
    try:
        docs = json.loads(sch.required_documents) if isinstance(sch.required_documents, str) else sch.required_documents
    except (json.JSONDecodeError, TypeError):
        docs = []
    if not isinstance(docs, list):
        return
    for d in docs:
        if isinstance(d, str) and d.strip():
            db.add(
                models.DocumentChecklist(
                    application_id=app.id,
                    document_type=d.strip(),
                    status="not_started",
                )
            )


@router.get("/applications", response_model=list[ApplicationOut])
@limiter.limit("60/minute")
def list_applications(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    rows = (
        db.query(models.Application)
        .filter(models.Application.user_id == uid)
        .order_by(models.Application.updated_at.desc())
        .all()
    )
    out: list[ApplicationOut] = []
    for a in rows:
        sch = db.query(models.Scholarship).filter(models.Scholarship.id == a.scholarship_id).first()
        out.append(
            ApplicationOut(
                id=a.id,
                user_id=a.user_id,
                scholarship_id=a.scholarship_id,
                status=a.status,
                notes=a.notes,
                created_at=a.created_at,
                updated_at=a.updated_at,
                scholarship=_scholarship_to_response(sch) if sch else None,
            )
        )
    return out


@router.post("/applications", response_model=ApplicationOut)
@limiter.limit("30/minute")
def create_application(
    request: Request,
    body: ApplicationCreate,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == body.scholarship_id).first()
    if not sch:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    existing = (
        db.query(models.Application)
        .filter(
            models.Application.user_id == uid,
            models.Application.scholarship_id == body.scholarship_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Application already exists for this scholarship")
    app = models.Application(user_id=uid, scholarship_id=body.scholarship_id, status="preparing")
    db.add(app)
    db.flush()
    db.add(
        models.ApplicationStatusEvent(
            application_id=app.id,
            from_status=None,
            to_status="preparing",
            actor_id=uid,
        )
    )
    _seed_checklist_from_scholarship(db, app, sch)
    db.commit()
    db.refresh(app)
    return ApplicationOut(
        id=app.id,
        user_id=app.user_id,
        scholarship_id=app.scholarship_id,
        status=app.status,
        notes=app.notes,
        created_at=app.created_at,
        updated_at=app.updated_at,
        scholarship=_scholarship_to_response(sch),
    )


@router.get("/applications/{application_id}", response_model=ApplicationOut)
@limiter.limit("60/minute")
def get_application(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app.scholarship_id).first()
    return ApplicationOut(
        id=app.id,
        user_id=app.user_id,
        scholarship_id=app.scholarship_id,
        status=app.status,
        notes=app.notes,
        created_at=app.created_at,
        updated_at=app.updated_at,
        scholarship=_scholarship_to_response(sch) if sch else None,
    )


@router.patch("/applications/{application_id}", response_model=ApplicationOut)
@limiter.limit("30/minute")
def patch_application(
    request: Request,
    application_id: int,
    body: ApplicationPatch,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    if body.status not in ALLOWED_STATUS:
        raise HTTPException(status_code=422, detail="Invalid status")
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    prev = app.status
    app.status = body.status
    if body.notes is not None:
        app.notes = body.notes
    db.add(
        models.ApplicationStatusEvent(
            application_id=app.id,
            from_status=prev,
            to_status=body.status,
            actor_id=uid,
        )
    )
    db.commit()
    db.refresh(app)
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app.scholarship_id).first()
    return ApplicationOut(
        id=app.id,
        user_id=app.user_id,
        scholarship_id=app.scholarship_id,
        status=app.status,
        notes=app.notes,
        created_at=app.created_at,
        updated_at=app.updated_at,
        scholarship=_scholarship_to_response(sch) if sch else None,
    )


@router.get("/applications/{application_id}/events", response_model=list[StatusEventOut])
@limiter.limit("60/minute")
def list_application_events(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    evs = (
        db.query(models.ApplicationStatusEvent)
        .filter(models.ApplicationStatusEvent.application_id == application_id)
        .order_by(models.ApplicationStatusEvent.created_at.asc())
        .all()
    )
    return [StatusEventOut.model_validate(e) for e in evs]


@router.get("/applications/{application_id}/documents", response_model=list[DocumentChecklistOut])
@limiter.limit("60/minute")
def list_application_documents(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    rows = (
        db.query(models.DocumentChecklist)
        .filter(models.DocumentChecklist.application_id == application_id)
        .all()
    )
    return [DocumentChecklistOut.model_validate(r) for r in rows]


@router.patch("/applications/{application_id}/documents/{doc_id}", response_model=DocumentChecklistOut)
@limiter.limit("60/minute")
def patch_application_document(
    request: Request,
    application_id: int,
    doc_id: int,
    body: DocumentChecklistPatch,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    row = (
        db.query(models.DocumentChecklist)
        .filter(
            models.DocumentChecklist.id == doc_id,
            models.DocumentChecklist.application_id == application_id,
        )
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Document checklist row not found")
    row.status = body.status
    if body.notes is not None:
        row.notes = body.notes
    db.commit()
    db.refresh(row)
    return DocumentChecklistOut.model_validate(row)
