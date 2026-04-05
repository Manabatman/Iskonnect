import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1 import (
    admin_extended,
    ai_tools,
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
from app.db import engine, get_db
from app.limiter import limiter
from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

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

app = FastAPI(title="Scholarship Matcher (Phase 1.5)")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware - origins from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID", "Accept"],
)

# Request logging for audit trail
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(feedback_routes.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(ai_tools.router, prefix="/api/v1")
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

@app.on_event("startup")
def run_migrations():
    """
    Optional: run Alembic migrations on startup (local dev only).
    Production: set RUN_MIGRATIONS_ON_STARTUP=false and use release command: alembic upgrade head
    """
    if not settings.run_migrations_on_startup:
        return
    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        logger.exception("alembic_upgrade_on_startup_failed: %s", e)
        raise



@app.get("/health")
def health(db: Session = Depends(get_db)):
    checks: dict = {"db": False, "cache": False}
    try:
        db.execute(text("SELECT 1"))
        checks["db"] = True
    except Exception as e:
        logger.warning("health_db_check_failed: %s", e)
    if settings.redis_url:
        try:
            import redis

            redis.from_url(settings.redis_url).ping()
            checks["cache"] = True
        except Exception as e:
            logger.warning("health_redis_check_failed: %s", e)
    else:
        checks["cache"] = True

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

    core_ok = checks.get("db") and checks.get("cache")
    overall = "ok" if core_ok else "degraded"
    return {"status": overall, "checks": checks}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "not_ready"})