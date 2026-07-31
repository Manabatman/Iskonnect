"""Auth endpoints: register, login, refresh, logout, password reset, email verification."""

import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from sqlalchemy.exc import IntegrityError
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
    revoke_all_refresh_tokens_for_user,
    revoke_access_token,
    revoke_refresh_token_plain,
    consume_refresh_token_rotation,
    verify_password,
)
from app.config import settings
from app.db import get_db
from app.limiter import limiter
from app import models
from app.utils.email import send_email_verification_email, send_password_reset_email
from app.utils.email_abuse import can_send_transactional_email, record_transactional_email_sent
from app.utils.email_validation import validate_email_format
from app.utils.server_timing import ServerTiming
from app.utils.timezone import utc_now_naive

router = APIRouter()
logger = logging.getLogger(__name__)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format_field(cls, v: str) -> str:
        validate_email_format(str(v))
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format_field(cls, v: str) -> str:
        validate_email_format(str(v))
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
    email: str
    email_verified: bool = False
    require_email_verification: bool = True
    has_profile: bool = False


class RegisterResponse(BaseModel):
    """Registration may return tokens for new users only (non-enumerating for duplicates)."""

    detail: str
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"
    user_id: int | None = None
    role: str | None = None
    email: str | None = None
    email_verified: bool = False
    require_email_verification: bool = True
    has_profile: bool = False


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email_format_field(cls, v: str) -> str:
        validate_email_format(str(v))
        return v


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
    require_email_verification: bool = True
    has_profile: bool = False


def _maybe_send_verification_email(to_email: str, token: str) -> None:
    if not settings.require_email_verification:
        return
    if can_send_transactional_email("verify", to_email):
        if send_email_verification_email(to_email, token):
            record_transactional_email_sent("verify", to_email)
    else:
        logger.warning("email_verify_throttled to=%s", to_email)


def _maybe_send_password_reset_email(to_email: str, token: str) -> None:
    if can_send_transactional_email("reset", to_email):
        if send_password_reset_email(to_email, token):
            record_transactional_email_sent("reset", to_email)
    else:
        logger.warning("email_reset_throttled to=%s", to_email)


def _token_response(
    db: Session,
    user: models.User,
    access: str,
    refresh: str,
) -> TokenResponse:
    has_profile = (
        db.query(models.Student).filter(models.Student.user_id == user.id).first() is not None
    )
    verified = bool(getattr(user, "email_verified", False))
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user_id=user.id,
        role=getattr(user, "role", "student"),
        email=user.email,
        email_verified=verified,
        require_email_verification=settings.require_email_verification,
        has_profile=has_profile,
    )


def _tokens_for_user(db: Session, user: models.User) -> TokenResponse:
    role = getattr(user, "role", "student")
    access = create_access_token(user.id, role=role)
    refresh = issue_refresh_token(db, user.id)
    db.commit()
    return _token_response(db, user, access, refresh)


@router.post("/auth/register", response_model=RegisterResponse)
@limiter.limit("5/minute")
def register(
    request: Request,
    register_req: Annotated[RegisterRequest, Body()],
    db: Session = Depends(get_db),
):
    """Register a new user. Returns tokens for new accounts; generic 200 if email already exists."""
    existing = db.query(models.User).filter(models.User.email == register_req.email).first()
    if existing:
        logger.warning("auth_register_failed user_hash=%s reason=already_registered", hash(register_req.email) % 10_000)
        return RegisterResponse(
            detail="If this email is not already registered, your account has been created. Check your email to verify.",
        )
    auto_verify = not settings.require_email_verification
    user = models.User(
        email=register_req.email,
        password_hash=hash_password(register_req.password),
        email_verified=auto_verify,
        email_verified_at=utc_now_naive() if auto_verify else None,
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        logger.warning("auth_register_race user_hash=%s", hash(register_req.email) % 10_000)
        return RegisterResponse(
            detail="If this email is not already registered, your account has been created. Check your email to verify.",
        )
    if settings.require_email_verification:
        verify_jwt = create_email_verification_token(user.id)
        _maybe_send_verification_email(register_req.email, verify_jwt)
        db.commit()
        logger.info("auth_register_ok user_id=%s (verification required)", user.id)
        return RegisterResponse(
            detail="Account created. Check your email to verify your address before signing in.",
        )
    tokens = _tokens_for_user(db, user)
    logger.info("auth_register_ok user_id=%s", user.id)
    register_detail = (
        "Account created. You can sign in now."
        if auto_verify
        else "Account created. Check your email to verify your address."
    )
    return RegisterResponse(
        detail=register_detail,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user_id=tokens.user_id,
        role=tokens.role,
        email=tokens.email,
        email_verified=tokens.email_verified,
        require_email_verification=tokens.require_email_verification,
        has_profile=tokens.has_profile,
    )


@router.post("/auth/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    req: Annotated[LoginRequest, Body()],
    response: Response,
    db: Session = Depends(get_db),
):
    """Login with email and password."""
    timing = ServerTiming()
    with timing.measure("db_lookup"):
        user = db.query(models.User).filter(models.User.email == req.email).first()
    with timing.measure("bcrypt", desc="password verify"):
        password_ok = user is not None and verify_password(req.password, user.password_hash)
    if not user or not password_ok:
        logger.warning("auth_login_failed user_hash=%s reason=invalid_credentials", hash(req.email) % 10_000)
        timing.attach(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if settings.require_email_verification and not bool(getattr(user, "email_verified", False)):
        logger.info("auth_login_blocked_unverified user_id=%s", user.id)
        timing.attach(response)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before signing in. Check your inbox or request a new verification link.",
        )
    with timing.measure("token_issue"):
        tokens = _tokens_for_user(db, user)
    timing.attach(response)
    return tokens


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
    return _token_response(
        db,
        user,
        create_access_token(user.id, role=role),
        new_refresh,
    )


@router.post("/auth/logout")
@limiter.limit("30/minute")
def logout(
    request: Request,
    body: Annotated[LogoutRequest, Body()],
    db: Session = Depends(get_db),
):
    """Revoke refresh token and denylist access token when provided."""
    auth = request.headers.get("authorization") or ""
    if auth.lower().startswith("bearer "):
        revoke_access_token(auth.split(" ", 1)[1].strip())
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
    db: Session = Depends(get_db),
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
    has_profile = (
        db.query(models.Student).filter(models.Student.user_id == user.id).first() is not None
    )
    return UserMeResponse(
        id=user.id,
        email=user.email,
        role=getattr(user, "role", "student"),
        email_verified=verified,
        require_email_verification=settings.require_email_verification,
        has_profile=has_profile,
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
        user.password_reset_expires_at = utc_now_naive() + timedelta(hours=1)
        db.commit()
        _maybe_send_password_reset_email(user.email, raw)
        logger.info("password_reset_token_issued user_id=%s", user.id)
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
    if user.password_reset_expires_at < utc_now_naive():
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    user.password_hash = hash_password(body.new_password)
    user.password_reset_token_hash = None
    user.password_reset_expires_at = None
    auth = request.headers.get("authorization") or ""
    if auth.lower().startswith("bearer "):
        revoke_access_token(auth.split(" ", 1)[1].strip())
    revoke_all_refresh_tokens_for_user(db, user.id)
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
    user.email_verified_at = utc_now_naive()
    db.commit()
    return {"detail": "Email verified."}


@router.post("/auth/resend-verification")
@limiter.limit("3/minute")
def resend_verification(
    request: Request,
    user: Annotated[models.User | None, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Resend verification email for the authenticated user. Generic response when already verified."""
    generic = {"detail": "If your email is not verified, a new verification link has been sent."}
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not settings.require_email_verification:
        return generic
    if bool(getattr(user, "email_verified", False)):
        return generic
    verify_jwt = create_email_verification_token(user.id)
    _maybe_send_verification_email(user.email, verify_jwt)
    return generic

