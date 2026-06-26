"""Student applications to scholarships (server-backed lifecycle)."""

import json
import logging
from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.documents.readiness import _normalize_doc_type, _parse_user_docs
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
        "withdrawn",
    }
)

# Statuses students may set on their own applications (review outcomes are sponsor/school only).
STUDENT_SETTABLE_STATUS = frozenset({"preparing", "submitted", "withdrawn"})


class ApplicationCreate(BaseModel):
    scholarship_id: int


class ApplicationPatch(BaseModel):
    status: str
    notes: Optional[str] = None


class DocumentChecklistPatch(BaseModel):
    status: str
    notes: Optional[str] = None
    file_url: Optional[str] = None


class ApplicationDriveFolderPatch(BaseModel):
    drive_folder_url: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    scholarship_id: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    drive_folder_url: Optional[str] = None
    removed_at: Optional[datetime] = None
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


def _application_to_out(
    app: models.Application,
    sch: models.Scholarship | None,
    *,
    include_scholarship: bool = True,
) -> ApplicationOut:
    return ApplicationOut(
        id=app.id,
        user_id=app.user_id,
        scholarship_id=app.scholarship_id,
        status=app.status,
        notes=app.notes,
        created_at=app.created_at,
        updated_at=app.updated_at,
        drive_folder_url=app.drive_folder_url,
        removed_at=app.removed_at,
        scholarship=_scholarship_to_response(sch) if sch and include_scholarship else None,
    )


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


ALLOWED_DOC_CHECKLIST_STATUS = frozenset({"not_started", "in_progress", "ready", "submitted"})


def _sync_student_documents_from_checklists(db: Session, user_id: int) -> None:
    """
    Rebuild students.documents from all checklist rows for this user.
    Types present on any checklist are owned by checklists: only ready/submitted become profile entries.
    Other profile document entries (types not on any checklist) are preserved.
    """
    student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not student:
        return

    q = (
        db.query(models.DocumentChecklist, models.Application)
        .join(models.Application, models.DocumentChecklist.application_id == models.Application.id)
        .filter(models.Application.user_id == user_id)
    )
    q = q.filter(models.Application.removed_at.is_(None))

    rows = q.all()
    ready_set = frozenset({"ready", "submitted"})
    rank = {"ready": 1, "submitted": 2}
    all_checklist_norms: set[str] = set()
    best: dict[str, tuple[int, str, str]] = {}  # norm -> (rank, raw_type, checklist_status)

    for checklist_row, _app in rows:
        nt = _normalize_doc_type(checklist_row.document_type)
        all_checklist_norms.add(nt)
        if checklist_row.status not in ready_set:
            continue
        rnk = rank.get(checklist_row.status, 0)
        raw = checklist_row.document_type.strip()
        prev = best.get(nt)
        if prev is None or rnk > prev[0]:
            best[nt] = (rnk, raw, checklist_row.status)

    synced_entries = [{"type": t[1], "status": t[2]} for t in best.values()]
    existing = _parse_user_docs(student.documents)
    preserved: list[dict] = []
    for doc in existing:
        if not isinstance(doc, dict):
            continue
        dt = doc.get("type") or doc.get("doc_type")
        if not dt:
            continue
        if _normalize_doc_type(str(dt)) in all_checklist_norms:
            continue
        preserved.append(doc)

    merged = synced_entries + preserved
    student.documents = json.dumps(merged) if merged else None


@router.get("/applications", response_model=list[ApplicationOut])
@limiter.limit("60/minute")
def list_applications(
    request: Request,
    include_scholarship: bool = True,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    rows = (
        db.query(models.Application)
        .filter(models.Application.user_id == uid, models.Application.removed_at.is_(None))
        .order_by(models.Application.updated_at.desc())
        .all()
    )
    out: list[ApplicationOut] = []
    for a in rows:
        sch = db.query(models.Scholarship).filter(models.Scholarship.id == a.scholarship_id).first()
        out.append(_application_to_out(a, sch, include_scholarship=include_scholarship))
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
        if existing.removed_at is not None:
            prev_status = existing.status
            existing.removed_at = None
            existing.status = "preparing"
            existing.updated_at = datetime.utcnow()
            db.add(
                models.ApplicationStatusEvent(
                    application_id=existing.id,
                    from_status=prev_status,
                    to_status="preparing",
                    actor_id=uid,
                    note="Restored after remove",
                )
            )
            has_rows = (
                db.query(models.DocumentChecklist)
                .filter(models.DocumentChecklist.application_id == existing.id)
                .first()
            )
            if not has_rows:
                _seed_checklist_from_scholarship(db, existing, sch)
            db.commit()
            db.refresh(existing)
            return _application_to_out(existing, sch)
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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        dup = (
            db.query(models.Application)
            .filter(
                models.Application.user_id == uid,
                models.Application.scholarship_id == body.scholarship_id,
            )
            .first()
        )
        if dup and dup.removed_at is None:
            raise HTTPException(status_code=409, detail="Application already exists for this scholarship")
        raise HTTPException(status_code=409, detail="Application conflict")
    db.refresh(app)
    return _application_to_out(app, sch)


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
    if not app or app.user_id != uid or app.removed_at is not None:
        raise HTTPException(status_code=404, detail="Application not found")
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app.scholarship_id).first()
    return _application_to_out(app, sch)


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
    if body.status not in STUDENT_SETTABLE_STATUS:
        raise HTTPException(
            status_code=403,
            detail="Only preparing, submitted, or withdrawn may be set by students",
        )
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid or app.removed_at is not None:
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
    return _application_to_out(app, sch)


@router.patch("/applications/{application_id}/drive-folder", response_model=ApplicationOut)
@limiter.limit("30/minute")
def patch_application_drive_folder(
    request: Request,
    application_id: int,
    body: ApplicationDriveFolderPatch,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid or app.removed_at is not None:
        raise HTTPException(status_code=404, detail="Application not found")
    url = (body.drive_folder_url or "").strip()
    if url.startswith("http://"):
        url = "https://" + url[7:]
    app.drive_folder_url = url or None
    db.commit()
    db.refresh(app)
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app.scholarship_id).first()
    return _application_to_out(app, sch)


@router.delete("/applications/{application_id}")
@limiter.limit("30/minute")
def delete_application_permanently(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Permanently delete application and cascaded timeline/checklists."""
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    _sync_student_documents_from_checklists(db, uid)
    db.commit()
    return {"status": "deleted"}


@router.post("/applications/{application_id}/remove", response_model=ApplicationOut)
@limiter.limit("30/minute")
def remove_application_entry(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    """Soft-remove: row kept for audit; hidden from default lists."""
    uid = _require_uid(user_id)
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app or app.user_id != uid:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.removed_at is not None:
        raise HTTPException(status_code=400, detail="Application already removed")
    prev = app.status
    now = datetime.utcnow()
    app.removed_at = now
    app.updated_at = now
    db.add(
        models.ApplicationStatusEvent(
            application_id=app.id,
            from_status=prev,
            to_status="removed",
            actor_id=uid,
            note="Remove this entry (soft delete; history preserved)",
        )
    )
    _sync_student_documents_from_checklists(db, uid)
    db.commit()
    db.refresh(app)
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == app.scholarship_id).first()
    return _application_to_out(app, sch)


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
    if app.removed_at is not None:
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
    if not app or app.user_id != uid or app.removed_at is not None:
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
    if not app or app.user_id != uid or app.removed_at is not None:
        raise HTTPException(status_code=404, detail="Application not found")
    if body.status not in ALLOWED_DOC_CHECKLIST_STATUS:
        raise HTTPException(status_code=422, detail="Invalid document checklist status")
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
    if body.file_url is not None:
        url = body.file_url.strip()
        if url and not url.lower().startswith("https://"):
            raise HTTPException(status_code=422, detail="Document URL must be an HTTPS link to external storage")
        row.file_url = url or None
    _sync_student_documents_from_checklists(db, uid)
    db.commit()
    db.refresh(row)
    return DocumentChecklistOut.model_validate(row)
