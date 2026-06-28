import logging
import traceback
from contextlib import asynccontextmanager

from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1 import (
    admin_extended,
    analytics,
    applications,
    audit_routes,
    auth_routes,
    feedback_routes,
    match_history,
    matches,
    notifications,
    profiles,
    reports,
    saved_scholarships,
    school_portal,
    scoring_admin,
    scholarship_search,
    scholarship_staging,
    scholarships,
    sponsor_portal,
    suggestions,
)
from app.config import settings
from app.auth import require_admin
from app.db import engine, get_db
from app import models
from app.limiter import limiter
from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def _db_label(url: str) -> str:
    """Short DB description for logs (never log credentials)."""
    u = (url or "").strip()
    if u.lower().startswith("sqlite"):
        return "sqlite (local dev.db)"
    try:
        host = u.split("@", 1)[1].split("/", 1)[0]
    except Exception:
        host = "?"
    return f"postgres @ {host}"


def _run_startup_migrations() -> None:
    if not settings.run_migrations_on_startup:
        return
    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        env = (settings.environment or "").strip().lower()
        if env in ("production", "staging", "prod"):
            logger.exception("alembic_upgrade_on_startup_failed: %s", e)
            raise
        logger.exception(
            "alembic_upgrade_on_startup_failed (dev — API still starts; fix DATABASE_URL or run "
            "`alembic upgrade head` manually): %s",
            e,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.structured_logging)
    settings.validate_for_production()
    logger.warning(
        "[startup] environment=%s database=%s cors_origins=%s",
        settings.environment,
        _db_label(settings.database_url),
        settings.cors_origins_list,
    )
    if settings.auth_disabled:
        logger.warning(
            "AUTH_DISABLED=true — JWT checks are bypassed on many routes; do not use in production."
        )
    _run_startup_migrations()
    yield


setup_logging(settings.structured_logging)
settings.validate_for_production()

if settings.sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=(settings.environment or "development").lower(),
    )

_env_lower = (settings.environment or "").strip().lower()
_docs_disabled = _env_lower in ("production", "staging", "prod")

app = FastAPI(
    title="Iskonnect",
    lifespan=lifespan,
    docs_url=None if _docs_disabled else "/docs",
    redoc_url=None if _docs_disabled else "/redoc",
    openapi_url=None if _docs_disabled else "/openapi.json",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", None) or request.headers.get("x-request-id", "unknown")
    if settings.sentry_dsn:
        try:
            import sentry_sdk

            with sentry_sdk.push_scope() as scope:
                scope.set_tag("request_id", str(rid))
                scope.set_tag("path", request.url.path)
                sentry_sdk.capture_exception(exc)
        except Exception:
            logger.exception("sentry_capture_failed")
    logger.error(
        "[%s] unhandled_exception path=%s method=%s err=%s\n%s",
        rid,
        request.url.path,
        request.method,
        exc,
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal error occurred. Please try again later.",
            "request_id": rid,
        },
        headers={"X-Request-ID": str(rid)},
    )


# Add CORS middleware - origins from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)

# Request logging for audit trail
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(feedback_routes.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(sponsor_portal.router, prefix="/api/v1")
app.include_router(school_portal.router, prefix="/api/v1")
app.include_router(profiles.router, prefix="/api/v1")
app.include_router(scholarship_search.router, prefix="/api/v1")
app.include_router(scholarships.router, prefix="/api/v1")
app.include_router(scholarship_staging.router, prefix="/api/v1")
app.include_router(matches.router, prefix="/api/v1")
app.include_router(match_history.router, prefix="/api/v1")
app.include_router(saved_scholarships.router, prefix="/api/v1")
app.include_router(suggestions.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(scoring_admin.router, prefix="/api/v1")
app.include_router(audit_routes.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(admin_extended.router, prefix="/api/v1")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    checks: dict = {"db": False, "cache": "skipped"}
    try:
        db.execute(text("SELECT 1"))
        checks["db"] = True
    except Exception as e:
        logger.warning("health_db_check_failed: %s", e)
    if settings.redis_url:
        try:
            import redis

            redis.from_url(
                settings.redis_url,
                socket_connect_timeout=2,
                socket_timeout=2,
            ).ping()
            checks["cache"] = True
        except Exception as e:
            logger.warning("health_redis_check_failed: %s", e)
            checks["cache"] = False
    else:
        checks["cache"] = "not_configured"

    scraper_last = None
    try:
        from app import models

        row = db.query(models.ScraperRun).order_by(models.ScraperRun.started_at.desc()).first()
        if row:
            scraper_last = {
                "source": row.source,
                "status": row.status,
                "started_at": row.started_at.isoformat() if row.started_at else None,
                "records_found": row.records_found,
            }
    except Exception:
        pass
    checks["scraper_last"] = scraper_last

    core_ok = checks.get("db") is True
    overall = "ok" if core_ok else "degraded"
    payload = {"status": overall, "checks": checks}
    if not core_ok:
        return JSONResponse(status_code=503, content=payload)
    return payload


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "not_ready"})


@app.get("/metrics")
def metrics(
    _admin: Annotated[models.User, Depends(require_admin)],
    db: Session = Depends(get_db),
):
    """Admin-only operational counters (not exposed to the public internet)."""

    try:
        scholarship_count = db.query(models.Scholarship).count()
        user_count = db.query(models.User).count()
        pending_staging = (
            db.query(models.ScholarshipStaging)
            .filter(models.ScholarshipStaging.status == "pending")
            .count()
        )
        return {
            "scholarships": scholarship_count,
            "users": user_count,
            "staging_pending": pending_staging,
        }
    except Exception as e:
        logger.warning("metrics_failed: %s", e)
        return JSONResponse(status_code=503, content={"detail": "metrics unavailable"})
