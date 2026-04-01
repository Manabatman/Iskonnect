"""
Application configuration via environment variables.
Uses pydantic-settings for validation and .env file support.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
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
        default="change-me-in-production-use-openssl-rand-hex-32",
        validation_alias="SECRET_KEY",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

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

    # Feature flags (safe defaults: off)
    filter_expired_from_matches: bool = Field(
        default=False,
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

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
