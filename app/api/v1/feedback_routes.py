"""Product feedback (separate from scholarship issue reports)."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models
from app.auth import get_optional_user_id
from app.db import get_db
from app.limiter import limiter

router = APIRouter(tags=["feedback"])


class FeedbackCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=8000)
    contact_email: Optional[str] = Field(default=None, max_length=255)


class FeedbackResponse(BaseModel):
    id: int
    detail: str = "Thank you for your feedback."


@router.post("/feedback", response_model=FeedbackResponse)
@limiter.limit("10/minute")
def submit_feedback(
    request: Request,
    body: FeedbackCreate,
    db: Session = Depends(get_db),
    user_id: Annotated[int | None, Depends(get_optional_user_id)] = None,
):
    row = models.ProductFeedback(
        user_id=user_id,
        category=body.category.strip(),
        message=body.message.strip(),
        contact_email=body.contact_email.strip() if body.contact_email else None,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return FeedbackResponse(id=row.id)
