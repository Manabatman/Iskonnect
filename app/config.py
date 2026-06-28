"""
Application configuration via environment variables.
Uses pydantic-settings for validation and .env file support.
"""

import logging

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# Must match the default Field value for secret_key (used for production guard)
DEFAULT_SECRET_KEY_VALUE = "change-me-in-production-use-openssl-rand-hex-32"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # development | staging | production — set ENVIRONMENT=production when deployed
    environment: str = Field(
        default="development",
        validation_alias="ENVIRONMENT",
    )

    # Database - set DATABASE_URL in env
    database_url: str = Field(
        default="sqlite:///./dev.db",
        validation_alias="DATABASE_URL",
    )

    # CORS - comma-separated list, set CORS_ORIGINS in env
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:5174,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:3000",
        validation_alias="CORS_ORIGINS",
    )

    # JWT
    secret_key: str = Field(
        default=DEFAULT_SECRET_KEY_VALUE,
        validation_alias="SECRET_KEY",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        default=14,
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # Production default: false (JWT required). Set AUTH_DISABLED=true in .env for local dev only.
    auth_disabled: bool = Field(
        default=False,
        validation_alias="AUTH_DISABLED",
    )

    # Sentry DSN - when set, error tracking is enabled
    sentry_dsn: str | None = Field(default=None, validation_alias="SENTRY_DSN")

    # Run Alembic on API startup (local dev convenience). Set false in production; use release command instead.
    run_migrations_on_startup: bool = Field(
        default=False,
        validation_alias="RUN_MIGRATIONS_ON_STARTUP",
    )

    # Optional Redis URL for shared scholarship cache across workers (e.g. redis://localhost:6379/0)
    redis_url: str | None = Field(default=None, validation_alias="REDIS_URL")

    # Gunicorn worker count (production); default 2
    web_concurrency: int = Field(default=2, validation_alias="WEB_CONCURRENCY")

    # Trust X-Forwarded-For for rate limits when behind Render/Railway reverse proxy
    trust_proxy_headers: bool = Field(default=False, validation_alias="TRUST_PROXY_HEADERS")

    # Feature flags (safe defaults: off)
    filter_expired_from_matches: bool = Field(
        default=True,
        validation_alias="FILTER_EXPIRED_FROM_MATCHES",
    )
    structured_logging: bool = Field(
        default=False,
        validation_alias="STRUCTURED_LOGGING",
    )
    enable_link_checker: bool = Field(
        default=False,
        validation_alias="ENABLE_LINK_CHECKER",
    )
    enable_notifications: bool = Field(
        default=False,
        validation_alias="ENABLE_NOTIFICATIONS",
    )
    db_driven_weights: bool = Field(
        default=False,
        validation_alias="DB_DRIVEN_WEIGHTS",
    )
    retention_inactive_days: int = Field(
        default=365,
        validation_alias="RETENTION_INACTIVE_DAYS",
    )

    # When false, users can sign in without verifying email (beta testing). SMTP not required in production.
    require_email_verification: bool = Field(
        default=True,
        validation_alias="REQUIRE_EMAIL_VERIFICATION",
    )

    # Email (SMTP) — required in production when REQUIRE_EMAIL_VERIFICATION=true
    smtp_host: str | None = Field(default=None, validation_alias="SMTP_HOST")
    smtp_port: int = Field(default=587, validation_alias="SMTP_PORT")
    smtp_user: str | None = Field(default=None, validation_alias="SMTP_USER")
    smtp_password: str | None = Field(default=None, validation_alias="SMTP_PASSWORD")
    smtp_use_tls: bool = Field(default=True, validation_alias="SMTP_USE_TLS")
    email_from: str | None = Field(default=None, validation_alias="EMAIL_FROM")
    frontend_url: str = Field(
        default="http://localhost:5173",
        validation_alias="FRONTEND_URL",
    )

    # SQLAlchemy pool (PostgreSQL multi-worker)
    db_pool_size: int = Field(default=5, validation_alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, validation_alias="DB_MAX_OVERFLOW")

    # Supabase Storage (scholarship images) — optional until admin uploads enabled
    supabase_url: str | None = Field(default=None, validation_alias="SUPABASE_URL")
    supabase_service_role_key: str | None = Field(
        default=None, validation_alias="SUPABASE_SERVICE_ROLE_KEY"
    )
    scholarship_image_bucket: str = Field(
        default="scholarship-images",
        validation_alias="SCHOLARSHIP_IMAGE_BUCKET",
    )
    scholarship_image_max_bytes: int = Field(
        default=5 * 1024 * 1024,
        validation_alias="SCHOLARSHIP_IMAGE_MAX_BYTES",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def cors_has_non_localhost_origin(self) -> bool:
        """True if at least one CORS origin is not localhost / 127.0.0.1."""
        for origin in self.cors_origins_list:
            lo = origin.lower()
            if "localhost" not in lo and "127.0.0.1" not in lo:
                return True
        return False

    def frontend_url_is_production_ready(self) -> bool:
        """True when FRONTEND_URL is not the localhost default."""
        lo = (self.frontend_url or "").strip().lower()
        return "localhost" not in lo and "127.0.0.1" not in lo

    def email_is_configured(self) -> bool:
        return bool(self.smtp_host and self.email_from)

    def validate_for_production(self) -> None:
        """
        Refuse unsafe configuration when ENVIRONMENT is production-like.
        Call from app startup (main.py), not at import of this module (keeps tests flexible).
        """
        env = (self.environment or "").strip().lower()
        if env not in ("production", "staging", "prod"):
            return
        errors: list[str] = []
        if self.secret_key == DEFAULT_SECRET_KEY_VALUE:
            errors.append("SECRET_KEY must not use the default placeholder in production")
        if self.auth_disabled:
            errors.append("AUTH_DISABLED must be false in production")
        if self.database_url.strip().lower().startswith("sqlite"):
            errors.append("DATABASE_URL must not be SQLite in production")
        if not self.cors_has_non_localhost_origin():
            errors.append(
                "CORS_ORIGINS must include at least one non-localhost origin in production"
            )
        if self.require_email_verification:
            if not self.email_is_configured():
                errors.append("SMTP_HOST and EMAIL_FROM must be set in production for auth emails")
            if not self.frontend_url_is_production_ready():
                errors.append(
                    "FRONTEND_URL must be a non-localhost URL in production (used in password reset / verify links)"
                )
        else:
            logger.warning(
                "REQUIRE_EMAIL_VERIFICATION=false — unverified users may sign in; re-enable before public launch"
            )
        if self.run_migrations_on_startup:
            errors.append(
                "RUN_MIGRATIONS_ON_STARTUP must be false in production; use release command: alembic upgrade head"
            )
        if not self.redis_url:
            errors.append(
                "REDIS_URL must be set in production for shared rate limits and scholarship cache"
            )
        if not self.trust_proxy_headers:
            errors.append(
                "TRUST_PROXY_HEADERS must be true in production when deployed behind Render/Railway"
            )
        if errors:
            raise RuntimeError("Invalid production configuration: " + "; ".join(errors))
        if not (self.supabase_url and self.supabase_service_role_key):
            logger.warning(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are not set — scholarship image uploads "
                "will return 503 until configured (create public bucket %s in Supabase Storage)",
                self.scholarship_image_bucket,
            )


settings = Settings()
