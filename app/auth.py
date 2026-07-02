"""
JWT authentication for protected endpoints.
Set AUTH_DISABLED=true for local development to bypass auth.
Uses PyJWT for access tokens; refresh tokens are stored hashed in the database.
"""
from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

from app.utils.timezone import utc_now_naive
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app import models

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _token_expiry_epoch(minutes: int) -> int:
    return int((datetime.now(timezone.utc) + timedelta(minutes=minutes)).timestamp())


def create_access_token(user_id: int, role: str = "student") -> str:
    now = int(datetime.now(timezone.utc).timestamp())
    exp = _token_expiry_epoch(settings.access_token_expire_minutes)
    jti = secrets.token_urlsafe(16)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": exp,
        "typ": "access",
        "jti": jti,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _redis_client():
    if not settings.redis_url:
        return None
    try:
        import redis

        return redis.from_url(settings.redis_url, decode_responses=True)
    except Exception:
        return None


def revoke_access_token(token: str) -> None:
    """Add access token jti to denylist until natural expiry (logout / password reset)."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False},
        )
        jti = payload.get("jti")
        exp = payload.get("exp")
        if not jti or not exp:
            return
        r = _redis_client()
        if r is None:
            return
        ttl = max(int(exp) - int(datetime.now(timezone.utc).timestamp()), 1)
        r.setex(f"auth:revoked:{jti}", ttl, "1")
    except Exception as e:
        logger.warning("revoke_access_token_failed: %s", e)


def _access_token_revoked(jti: str | None) -> bool:
    if not jti:
        return False
    r = _redis_client()
    if r is None:
        return False
    try:
        return bool(r.get(f"auth:revoked:{jti}"))
    except Exception:
        return False


def create_email_verification_token(user_id: int) -> str:
    exp = _token_expiry_epoch(60 * 24 * 7)  # 7 days
    now = int(datetime.now(timezone.utc).timestamp())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "typ": "email_verify",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_email_verification_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("typ") != "email_verify":
            return None
        sub = payload.get("sub")
        return int(sub) if sub else None
    except (ExpiredSignatureError, InvalidTokenError, ValueError, TypeError):
        return None


def create_profile_read_token(profile_id: int) -> str:
    """Short-lived token for anonymous profile read access (prevents IDOR on profile_id)."""
    exp = _token_expiry_epoch(60 * 24 * 7)  # 7 days
    now = int(datetime.now(timezone.utc).timestamp())
    payload = {
        "sub": str(profile_id),
        "iat": now,
        "exp": exp,
        "typ": "profile_read",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_profile_read_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("typ") != "profile_read":
            return None
        sub = payload.get("sub")
        return int(sub) if sub else None
    except (ExpiredSignatureError, InvalidTokenError, ValueError, TypeError):
        return None


def hash_refresh_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def new_refresh_token_plain() -> str:
    return secrets.token_urlsafe(48)


def issue_refresh_token(db: Session, user_id: int) -> str:
    """Create refresh token row and return plaintext (show once to client)."""
    raw = new_refresh_token_plain()
    exp = utc_now_naive() + timedelta(days=settings.refresh_token_expire_days)
    row = models.RefreshToken(
        user_id=user_id,
        token_hash=hash_refresh_token(raw),
        expires_at=exp,
    )
    db.add(row)
    db.flush()
    return raw


def revoke_refresh_token_plain(db: Session, raw: str) -> bool:
    h = hash_refresh_token(raw)
    row = db.query(models.RefreshToken).filter(models.RefreshToken.token_hash == h).first()
    if not row or row.revoked_at is not None:
        return False
    row.revoked_at = utc_now_naive()
    return True


def revoke_all_refresh_tokens_for_user(db: Session, user_id: int) -> int:
    """Revoke all active refresh tokens for a user. Returns count revoked."""
    now = utc_now_naive()
    rows = (
        db.query(models.RefreshToken)
        .filter(
            models.RefreshToken.user_id == user_id,
            models.RefreshToken.revoked_at.is_(None),
        )
        .all()
    )
    for row in rows:
        row.revoked_at = now
    return len(rows)


def consume_refresh_token_rotation(db: Session, raw: str) -> tuple[models.User, str] | None:
    """
    Validate refresh token, revoke it, issue a new refresh token (rotation).
    Returns (user, new_refresh_plain) or None.
    """
    h = hash_refresh_token(raw)
    row = (
        db.query(models.RefreshToken)
        .filter(
            models.RefreshToken.token_hash == h,
            models.RefreshToken.revoked_at.is_(None),
        )
        .first()
    )
    if not row:
        return None
    # DB stores naive UTC datetimes for expires_at
    if row.expires_at < utc_now_naive():
        return None

    user = db.query(models.User).filter(models.User.id == row.user_id).first()
    if not user:
        return None

    row.revoked_at = utc_now_naive()
    new_plain = issue_refresh_token(db, user.id)
    db.commit()
    return user, new_plain


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("typ") not in (None, "access"):
            return None
        if _access_token_revoked(payload.get("jti")):
            return None
        sub = payload.get("sub")
        return int(sub) if sub else None
    except (ExpiredSignatureError, InvalidTokenError, ValueError, TypeError):
        return None


def _get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials | None,
    db: Session,
) -> int | None:
    if not credentials:
        return None
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        return None
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user_id if user else None


def get_optional_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> int | None:
    """Return user id from Bearer token if valid; otherwise None (never raises)."""
    return _get_user_id_from_token(credentials, db)


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> int | None:
    """
    Dependency: return user_id if authenticated.
    When AUTH_DISABLED=true, returns None (endpoints allow unauthenticated access).
    When AUTH_DISABLED=false, raises 401 if no valid token.
    """
    if settings.auth_disabled:
        return _get_user_id_from_token(credentials, db) if credentials else None
    user_id = _get_user_id_from_token(credentials, db)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> models.User | None:
    """
    Dependency: return full User object if authenticated.
    Returns None when no valid token. Respects AUTH_DISABLED for optional auth.
    """
    if not credentials:
        return None
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        return None
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def require_admin(
    user: Annotated[models.User | None, Depends(get_current_user)],
) -> models.User:
    """
    Dependency: require admin role for protected endpoints.
    Raises 401 if not authenticated, 403 if not admin.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = getattr(user, "role", "student")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return user


def require_profile_owner(
    profile_id: int,
    user_id: int,
    db: Session,
    profile_access_token: str | None = None,
) -> None:
    """Raise 403 if profile does not belong to user. Anonymous profiles require profile read token."""
    profile = db.query(models.Student).filter(models.Student.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile.user_id is None:
        if settings.auth_disabled:
            return
        token_pid = decode_profile_read_token(profile_access_token) if profile_access_token else None
        if token_pid != profile_id:
            raise HTTPException(status_code=403, detail="Profile access token required")
        return
    if profile.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")


def get_profile_access_token(request: Request) -> str | None:
    """Optional header for anonymous profile read access."""
    raw = request.headers.get("x-profile-access-token")
    return raw.strip() if raw else None


def assert_can_read_profile(
    profile_id: int,
    db: Session,
    user_id: int | None,
    profile_access_token: str | None = None,
) -> None:
    """
    Enforce read access for a profile.
    - Anonymous profiles: require valid X-Profile-Access-Token from creation.
    - Claimed profiles: only the owning user (valid JWT) may read.
    """
    profile = db.query(models.Student).filter(models.Student.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile.user_id is not None:
        if user_id is None:
            raise HTTPException(status_code=403, detail="Access denied")
        if profile.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        return
    # Anonymous profile — require profile read token unless auth is disabled (local dev)
    if settings.auth_disabled:
        return
    token_pid = decode_profile_read_token(profile_access_token) if profile_access_token else None
    if token_pid != profile_id:
        raise HTTPException(status_code=403, detail="Profile access token required")
