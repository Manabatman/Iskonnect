"""User-facing verification badges and trust signals derived from scholarship data."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from app.utils.application_status import humanize_verification_source
from app.utils.trust_constants import STALE_VERIFICATION_DAYS, VERIFICATION_FRESH_DAYS
from app.utils.data_completeness import (
    completeness_tier,
    compute_data_completeness_score,
    public_completeness_label,
)


def _parse_dt(val: Any) -> datetime | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, date):
        return datetime(val.year, val.month, val.day)
    if isinstance(val, str) and val.strip():
        try:
            return datetime.fromisoformat(val.strip().replace("Z", "+00:00")[:19])
        except ValueError:
            return None
    return None


def verification_badge(row: Any, *, has_field_evidence: bool | None = None) -> str:
    """
    User-facing badge: verified | partially_verified | imported_unverified | needs_review
    """
    ds = (_get(row, "data_status") or "").strip().lower()
    editorial = (_get(row, "editorial_state") or "").strip().lower()
    if ds == "needs_review" or editorial == "needs_review":
        return "needs_review"
    score = _completeness(row)
    verified_at = _parse_dt(_get(row, "last_verified_at"))
    vsource = (_get(row, "verification_source") or "").strip().lower()
    evidence_ok = has_field_evidence if has_field_evidence is not None else False
    if (
        evidence_ok
        and verified_at
        and vsource in ("manual", "team_verified", "partner")
    ):
        age_days = (datetime.utcnow() - verified_at.replace(tzinfo=None)).days
        if age_days <= VERIFICATION_FRESH_DAYS and score >= 60:
            return "verified"
        if age_days <= STALE_VERIFICATION_DAYS:
            return "partially_verified"
    if vsource in ("csv_import", "csv_import_legacy", "gemini_research", "discovery_verification", ""):
        return "imported_unverified"
    if evidence_ok and score >= 85:
        return "partially_verified"
    return "needs_review"


def verification_badge_for_row(row: Any, db: Any) -> str:
    """Badge with field_evidence lookup when db session is available."""
    from app import models

    sid = _get(row, "id")
    has_evidence = False
    if sid and db is not None:
        has_evidence = (
            db.query(models.FieldEvidence)
            .filter(
                models.FieldEvidence.scholarship_id == sid,
                models.FieldEvidence.superseded_at.is_(None),
            )
            .first()
            is not None
        )
    return verification_badge(row, has_field_evidence=has_evidence)


def verification_badge_label(badge: str) -> str:
    """Internal/admin badge label (catalog health, admin dashboards)."""
    return {
        "verified": "Verified against official source",
        "partially_verified": "Partially verified",
        "imported_unverified": "Imported — not independently verified",
        "needs_review": "Needs review",
    }.get(badge, "Needs review")


def student_verification_status(row: Any, *, internal_badge: str | None = None) -> str:
    """
    Student-facing trust status: verified | needs_review | archived.
    Wording is about the scholarship opportunity, not database import state.
    """
    app_status = (_get(row, "application_status") or "").strip().lower()
    is_active = _get(row, "is_active")
    ds = (_get(row, "data_status") or "").strip().lower()
    if is_active is False or app_status in ("closed", "archived", "discontinued") or ds in (
        "expired",
        "past_deadline",
        "archived",
    ):
        return "archived"
    badge = internal_badge or verification_badge(
        row, has_field_evidence=bool(_get(row, "_has_field_evidence"))
    )
    if badge == "verified":
        return "verified"
    return "needs_review"


def student_verification_label(status: str) -> str:
    return {
        "verified": "Verified",
        "needs_review": "Needs Review",
        "archived": "Archived",
    }.get(status, "Needs Review")


def student_verification_message(status: str) -> str:
    messages = {
        "verified": "Information has been checked against an official source.",
        "needs_review": (
            "Some information could not be confirmed recently. "
            "Always confirm details on the official website before applying."
        ),
        "archived": "This opportunity is no longer accepting applications.",
    }
    return messages.get(status, messages["needs_review"])


def _official_website_host(row: Any) -> str | None:
    link = (_get(row, "link") or "").strip()
    if not link:
        return None
    try:
        from urllib.parse import urlparse

        parsed = urlparse(link if "://" in link else f"https://{link}")
        host = (parsed.netloc or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host or None
    except Exception:
        return None


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _completeness(row: Any) -> int:
    score = _get(row, "data_completeness_score")
    if score is not None:
        return int(score)
    return compute_data_completeness_score(row)


def attach_verification_fields(payload: dict[str, Any]) -> dict[str, Any]:
    """Add verification/trust fields to a scholarship payload."""
    evidence = payload.get("field_evidence")
    has_evidence = False
    if isinstance(evidence, list) and len(evidence) > 0:
        has_evidence = True
    elif payload.get("_has_field_evidence"):
        has_evidence = True
    payload["_has_field_evidence"] = has_evidence
    badge = verification_badge(payload, has_field_evidence=has_evidence)
    score = _completeness(payload)
    verified_at = _get(payload, "last_verified_at")
    vsource = _get(payload, "verification_source")
    payload["verification_badge"] = badge
    payload["verification_badge_label"] = verification_badge_label(badge)
    payload["verification_source_label"] = humanize_verification_source(vsource)
    payload["completeness_label"] = public_completeness_label(score)
    payload["completeness_tier"] = completeness_tier(score)
    student_status = student_verification_status(payload, internal_badge=badge)
    payload["student_verification_status"] = student_status
    payload["student_verification_label"] = student_verification_label(student_status)
    payload["student_verification_message"] = student_verification_message(student_status)
    link = (_get(payload, "link") or "").strip()
    if link:
        payload["official_website"] = link
        payload["official_website_host"] = _official_website_host(payload)
    if verified_at:
        dt = _parse_dt(verified_at)
        if dt:
            days = (datetime.utcnow() - dt.replace(tzinfo=None)).days
            if days == 0:
                payload["last_reviewed_label"] = "Verified today"
            elif days == 1:
                payload["last_reviewed_label"] = "Verified yesterday"
            elif days < STALE_VERIFICATION_DAYS:
                payload["last_reviewed_label"] = f"Verified {days} days ago"
            else:
                payload["last_reviewed_label"] = f"Last reviewed {days} days ago"
    return payload
