"""Admin catalog management: permanent delete, merge, bulk actions, duplicate candidates."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models
from app.auth import require_admin
from app.db import get_db
from app.limiter import limiter
from app.services.duplicate_detection import find_duplicate_pairs
from app.services.scholarship_catalog_admin import (
    BulkAction,
    CatalogAdminError,
    merge_before_delete,
    permanently_delete_scholarship,
    run_bulk_action,
)
from app.utils.audit import log_action

router = APIRouter(tags=["admin-catalog"])


class MergeAndDeleteBody(BaseModel):
    canonical_id: int
    duplicate_id: int


class BulkScholarshipsBody(BaseModel):
    ids: list[int] = Field(..., min_length=1, max_length=200)
    action: BulkAction


@router.delete("/admin/scholarships/{scholarship_id}/permanent")
@limiter.limit("30/minute")
def permanent_delete_scholarship(
    request: Request,
    scholarship_id: int,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    try:
        result = permanently_delete_scholarship(db, scholarship_id)
        db.commit()
    except CatalogAdminError as exc:
        db.rollback()
        status = 404 if exc.code == "not_found" else 400
        raise HTTPException(status_code=status, detail=exc.message) from exc

    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action="scholarship.permanent_delete",
        resource_type="scholarship",
        resource_id=scholarship_id,
        details={"title": result.title, "cascaded_counts": result.cascaded_counts},
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    return {"status": "deleted", "scholarship_id": result.scholarship_id, "title": result.title}


@router.post("/admin/scholarships/merge-and-delete")
@limiter.limit("30/minute")
def merge_and_delete_scholarship(
    request: Request,
    payload: MergeAndDeleteBody,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    try:
        result = merge_before_delete(db, payload.canonical_id, payload.duplicate_id, dry_run=False)
        db.commit()
    except CatalogAdminError as exc:
        db.rollback()
        status = 404 if exc.code == "not_found" else 400
        raise HTTPException(status_code=status, detail=exc.message) from exc

    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action="scholarship.merge_and_delete",
        resource_type="scholarship",
        resource_id=payload.duplicate_id,
        details={
            "canonical_id": payload.canonical_id,
            "duplicate_id": payload.duplicate_id,
            "fields_merged": result.fields_merged,
            "saved_migrated": result.saved_migrated,
            "applications_migrated": result.applications_migrated,
        },
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    return {
        "status": "merged_and_deleted",
        "canonical_id": result.canonical_id,
        "duplicate_id": result.duplicate_id,
        "fields_merged": result.fields_merged,
        "saved_migrated": result.saved_migrated,
        "applications_migrated": result.applications_migrated,
        "evidence_migrated": result.evidence_migrated,
        "notifications_migrated": result.notifications_migrated,
    }


@router.post("/admin/scholarships/bulk")
@limiter.limit("20/minute")
def bulk_scholarship_actions(
    request: Request,
    payload: BulkScholarshipsBody,
    db: Session = Depends(get_db),
    admin: Annotated[models.User | None, Depends(require_admin)] = None,
):
    results = run_bulk_action(db, payload.ids, payload.action)
    succeeded = [r.id for r in results if r.status == "succeeded"]
    failed = [{"id": r.id, "reason": r.reason} for r in results if r.status == "failed"]
    db.commit()

    log_action(
        db,
        actor_id=admin.id if admin else None,
        actor_type="admin",
        action=f"scholarship.bulk_{payload.action}",
        resource_type="scholarship",
        resource_id=None,
        details={"ids": payload.ids, "succeeded": succeeded, "failed": failed},
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    return {"action": payload.action, "succeeded": succeeded, "failed": failed}


@router.get("/admin/duplicates/candidates")
@limiter.limit("30/minute")
def list_duplicate_candidates(
    request: Request,
    db: Session = Depends(get_db),
    _admin: Annotated[models.User | None, Depends(require_admin)] = None,
    min_confidence: float = 0.85,
    include_inactive: bool = True,
):
    pairs = find_duplicate_pairs(
        db,
        min_confidence=min_confidence,
        include_inactive=include_inactive,
    )
    return {"total": len(pairs), "pairs": pairs}
