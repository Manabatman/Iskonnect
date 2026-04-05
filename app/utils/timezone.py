"""
Philippine (Asia/Manila) display helpers and consistent UTC handling.

DB columns use naive UTC timestamps from PostgreSQL/SQLAlchemy server_default;
application code should write naive UTC using utc_now_naive() for compatibility.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo

    try:
        PH_TZ = ZoneInfo("Asia/Manila")
    except Exception:
        # Windows/minimal Python without tzdata package
        PH_TZ = timezone(timedelta(hours=8))
except ImportError:
    PH_TZ = timezone(timedelta(hours=8))


def utc_now_naive() -> datetime:
    """Current UTC as naive datetime (for ORM DateTime columns without timezone)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def ensure_utc(dt: datetime) -> datetime:
    """Treat naive datetimes as UTC; return timezone-aware UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_philippine_iso(dt: datetime | None) -> str | None:
    """ISO-8601 string in Asia/Manila for API display fields."""
    if dt is None:
        return None
    aware = ensure_utc(dt)
    return aware.astimezone(PH_TZ).isoformat()
