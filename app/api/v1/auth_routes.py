"""Auth endpoints: register, login, refresh, logout, password reset, email verification."""

import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    create_email_verification_token,
    decode_email_verification_token,
    get_current_user,
    hash_password,
    hash_refresh_token,
    issue_refresh_token,
    new_refresh_token_plain,
    revoke_refresh_token_plain,
    consume_refresh_token_rotation,
    verify_password,
)
from app.config import settings
from app.db import get_db
from app.limiter import limiter
from app import models

router = APIRouter()
logger = logging.getLogger(__name__)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class VerifyEmailRequest(BaseModel):
    token: str


class UserMeResponse(BaseModel):
    id: int
    email: str
    role: str
    email_verified: bool = False


def _tokens_for_user(db: Session, user: models.User) -> TokenResponse:
    role = getattr(user, "role", "student")
    access = create_access_token(user.id, role=role)
    refresh = issue_refresh_token(db, user.id)
    db.commit()
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user_id=user.id,
        role=role,
    )


@router.post("/auth/register", response_model=TokenResponse)
@limiter.limit("5/minute")
def register(
    request: Request,
    register_req: Annotated[RegisterRequest, Body()],
    db: Session = Depends(get_db),
):
    """Register a new user. Returns access + refresh tokens."""
    existing = db.query(models.User).filter(models.User.email == register_req.email).first()
    if existing:
        logger.warning("auth_register_failed email=%s reason=already_registered", register_req.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = models.User(
        email=register_req.email,
        password_hash=hash_password(register_req.password),
        email_verified=False,
    )
    db.add(user)
    db.flush()
    verify_jwt = create_email_verification_token(user.id)
    logger.info(
        "auth_register_ok user_id=%s email_verify_jwt_prefix=%s... (send via email in production)",
        user.id,
        verify_jwt[:16],
    )
    return _tokens_for_user(db, user)


@router.post("/auth/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    req: Annotated[LoginRequest, Body()],
    db: Session = Depends(get_db),
):
    """Login with email and password."""
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        logger.warning("auth_login_failed email=%s reason=invalid_credentials", req.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return _tokens_for_user(db, user)


@router.post("/auth/refresh", response_model=TokenResponse)
@limiter.limit("30/minute")
def refresh_tokens(
    request: Request,
    body: Annotated[RefreshRequest, Body()],
    db: Session = Depends(get_db),
):
    """Exchange a valid refresh token for new access + refresh (rotation)."""
    out = consume_refresh_token_rotation(db, body.refresh_token.strip())
    if not out:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    user, new_refresh = out
    role = getattr(user, "role", "student")
    return TokenResponse(
        access_token=create_access_token(user.id, role=role),
        refresh_token=new_refresh,
        user_id=user.id,
        role=role,
    )


@router.post("/auth/logout")
@limiter.limit("30/minute")
def logout(
    request: Request,
    body: Annotated[LogoutRequest, Body()],
    db: Session = Depends(get_db),
):
    """Revoke a refresh token."""
    if revoke_refresh_token_plain(db, body.refresh_token.strip()):
        db.commit()
        return {"status": "ok"}
    db.rollback()
    return {"status": "ok"}  # idempotent logout


@router.get("/auth/me", response_model=UserMeResponse)
@limiter.limit("120/minute")
def get_me(
    request: Request,
    user: Annotated[models.User | None, Depends(get_current_user)],
):
    """Return current authenticated user info."""
    if user is None:
        logger.warning("auth_me_failed reason=not_authenticated")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    verified = bool(getattr(user, "email_verified", False))
    return UserMeResponse(
        id=user.id,
        email=user.email,
        role=getattr(user, "role", "student"),
        email_verified=verified,
    )


@router.post("/auth/forgot-password")
@limiter.limit("5/minute")
def forgot_password(
    request: Request,
    body: Annotated[ForgotPasswordRequest, Body()],
    db: Session = Depends(get_db),
):
    """Request password reset. Always returns 200 to avoid email enumeration."""
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if user:
        raw = new_refresh_token_plain()
        user.password_reset_token_hash = hash_refresh_token(raw)
        user.password_reset_expires_at = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        logger.info(
            "password_reset_token_issued user_id=%s token_prefix=%s... (email link in production)",
            user.id,
            raw[:12],
        )
    return {"detail": "If that email exists, reset instructions have been sent."}


@router.post("/auth/reset-password")
@limiter.limit("10/minute")
def reset_password(
    request: Request,
    body: Annotated[ResetPasswordRequest, Body()],
    db: Session = Depends(get_db),
):
    """Complete password reset using token from forgot-password email (or dev logs)."""
    h = hash_refresh_token(body.token.strip())
    user = db.query(models.User).filter(models.User.password_reset_token_hash == h).first()
    if not user or not user.password_reset_expires_at:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    if user.password_reset_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    user.password_hash = hash_password(body.new_password)
    user.password_reset_token_hash = None
    user.password_reset_expires_at = None
    db.commit()
    return {"detail": "Password updated. You can sign in."}


@router.post("/auth/verify-email")
@limiter.limit("10/minute")
def verify_email(
    request: Request,
    body: Annotated[VerifyEmailRequest, Body()],
    db: Session = Depends(get_db),
):
    """Mark email verified using JWT from registration (sent via email in production)."""
    uid = decode_email_verification_token(body.token.strip())
    if uid is None:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    user.email_verified_at = datetime.utcnow()
    db.commit()
    return {"detail": "Email verified."}

