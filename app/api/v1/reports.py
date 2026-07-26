"""User reports on scholarships (admin review queue)."""

import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.schemas import ScholarshipReportCreate, ScholarshipReportResponse
from app.auth import get_optional_user_id, require_admin
from app.db import get_db
from app.limiter import limiter
from app.utils.audit import log_action
from app.utils.editorial_state import NEEDS_REVIEW, apply_editorial_state

logger = logging.getLogger(__name__)

router = APIRouter(tags=["reports"])


def _maybe_flag_scholarship_for_review(db: Session, scholarship_id: int, field_key: str | None) -> None:
    """When 3+ pending reports share scholarship+field_key, mark needs_review via editorial shim."""
    if not field_key:
        return
    pending_count = (
        db.query(func.count(models.ScholarshipReport.id))
        .filter(
            models.ScholarshipReport.scholarship_id == scholarship_id,
            models.ScholarshipReport.field_key == field_key,
            models.ScholarshipReport.status == "pending",
        )
        .scalar()
        or 0
    )
    if pending_count < 3:
        return
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if sch:
        apply_editorial_state(sch, NEEDS_REVIEW)


def _notify_reporter_resolved(db: Session, report: models.ScholarshipReport) -> None:
    """Optional in-app notification when a report with user_id is resolved."""
    if not report.user_id:
        return
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == report.scholarship_id).first()
    title = sch.title if sch else "Scholarship"
    db.add(
        models.Notification(
            user_id=report.user_id,
            type="report_resolved",
            title=f"Report resolved: {title[:80]}",
            body="Thank you — your correction report was reviewed and resolved.",
            scholarship_id=report.scholarship_id,
            is_read=False,
        )
    )


@router.post("/reports", response_model=ScholarshipReportResponse)
@limiter.limit("5/minute")
def create_report(
    request: Request,
    body: ScholarshipReportCreate,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
):
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == body.scholarship_id).first()
    if not sch:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    row = models.ScholarshipReport(
        user_id=user_id,
        scholarship_id=body.scholarship_id,
        issue_type=body.issue_type,
        description=body.description,
        field_key=body.field_key,
        proposed_value=body.proposed_value,
        evidence_url=body.evidence_url,
        status="pending",
    )
    db.add(row)
    db.flush()
    _maybe_flag_scholarship_for_review(db, body.scholarship_id, body.field_key)
    db.commit()
    db.refresh(row)
    return row


@router.get("/reports/pending", response_model=list[ScholarshipReportResponse])
@limiter.limit("60/minute")
def list_pending_reports(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    rows = (
        db.query(models.ScholarshipReport)
        .filter(models.ScholarshipReport.status == "pending")
        .order_by(models.ScholarshipReport.created_at.asc())
        .all()
    )
    return rows


@router.post("/reports/{report_id}/resolve")
@limiter.limit("30/minute")
def resolve_report(
    report_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    row = db.query(models.ScholarshipReport).filter(models.ScholarshipReport.id == report_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    row.status = "resolved"
    row.reviewed_at = datetime.now(timezone.utc)
    row.reviewer_id = admin.id if admin else None
    _notify_reporter_resolved(db, row)
    db.commit()
    client = request.client.host if request.client else None
    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action="report.resolve",
        resource_type="scholarship_report",
        resource_id=report_id,
        details={"scholarship_id": row.scholarship_id},
        ip_address=client,
    )
    return {"status": "resolved", "id": report_id}


@router.post("/reports/{report_id}/dismiss")
@limiter.limit("30/minute")
def dismiss_report(
    report_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    row = db.query(models.ScholarshipReport).filter(models.ScholarshipReport.id == report_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    row.status = "dismissed"
    row.reviewed_at = datetime.now(timezone.utc)
    row.reviewer_id = admin.id if admin else None
    db.commit()
    client = request.client.host if request.client else None
    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action="report.dismiss",
        resource_type="scholarship_report",
        resource_id=report_id,
        details={"scholarship_id": row.scholarship_id},
        ip_address=client,
    )
    return {"status": "dismissed", "id": report_id}
