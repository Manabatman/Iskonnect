"""
Scholarship data completeness scoring (0–100).

Weighted field set prioritizes decision-critical structured eligibility data.
Used for publishability gates, admin data-quality dashboards, and user-facing
coarse completeness signals.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

# Weights sum to 100
COMPLETENESS_WEIGHTS: dict[str, int] = {
    "title": 5,
    "provider": 5,
    "official_link": 8,
    "deadline": 8,
    "structured_eligibility": 15,
    "residency_rules": 10,
    "income_rules": 8,
    "course_restrictions": 8,
    "education_levels": 7,
    "verification": 10,
    "benefits": 5,
    "documents": 4,
    "description": 4,
    "contact_info": 3,
}


def _get(row: Any, key: str, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _has_json_list(val: Any) -> bool:
    if not val:
        return False
    s = str(val).strip()
    return s not in ("[]", "", "null", "None")


def compute_data_completeness_score(row: dict[str, Any] | Any) -> int:
    """Return 0–100 completeness percentage."""
    score = 0

    if (_get(row, "title") or "").strip():
        score += COMPLETENESS_WEIGHTS["title"]
    if (_get(row, "provider") or "").strip():
        score += COMPLETENESS_WEIGHTS["provider"]
    link = (_get(row, "link") or "").strip()
    if link.startswith(("http://", "https://")):
        score += COMPLETENESS_WEIGHTS["official_link"]
    if _get(row, "application_deadline"):
        score += COMPLETENESS_WEIGHTS["deadline"]

    has_levels = _has_json_list(_get(row, "eligible_levels")) or bool(_get(row, "level"))
    has_regions = _has_json_list(_get(row, "eligible_regions")) or _has_json_list(_get(row, "regions"))
    has_cities = _has_json_list(_get(row, "eligible_cities"))
    has_income = _get(row, "max_income_threshold") is not None
    has_gwa = _get(row, "min_gwa_normalized") is not None
    has_courses = _has_json_list(_get(row, "eligible_courses_psced")) or _has_json_list(
        _get(row, "eligible_courses_specific")
    )
    if has_levels or has_regions or has_cities or has_income or has_gwa or has_courses:
        score += COMPLETENESS_WEIGHTS["structured_eligibility"]
    if has_regions or has_cities or _get(row, "residency_required"):
        if has_regions or has_cities:
            score += COMPLETENESS_WEIGHTS["residency_rules"]
    if has_income:
        score += COMPLETENESS_WEIGHTS["income_rules"]
    if has_courses:
        score += COMPLETENESS_WEIGHTS["course_restrictions"]
    if has_levels:
        score += COMPLETENESS_WEIGHTS["education_levels"]

    verified = _get(row, "last_verified_at")
    vsource = _get(row, "verification_source")
    if verified and vsource in ("manual", "team_verified", "partner", "csv_import"):
        if isinstance(verified, datetime):
            cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=90)
            if verified >= cutoff:
                score += COMPLETENESS_WEIGHTS["verification"]
        else:
            score += COMPLETENESS_WEIGHTS["verification"]
    elif verified:
        score += COMPLETENESS_WEIGHTS["verification"] // 2

    if _get(row, "benefit_tuition") or _get(row, "benefit_allowance_monthly") or _get(row, "benefit_total_value"):
        score += COMPLETENESS_WEIGHTS["benefits"]
    if _has_json_list(_get(row, "required_documents")):
        score += COMPLETENESS_WEIGHTS["documents"]
    desc = (_get(row, "description") or "").strip()
    if len(desc) >= 50:
        score += COMPLETENESS_WEIGHTS["description"]

    score = min(100, max(0, score))
    return score


def completeness_tier(score: int) -> str:
    """Human-readable tier for admin triage."""
    if score >= 90:
        return "verified_ready"
    if score >= 60:
        return "usable"
    return "needs_work"


def public_completeness_label(score: int) -> str:
    """Coarse user-facing signal (no exact percentage)."""
    if score >= 85:
        return "Complete eligibility info"
    if score >= 60:
        return "Most eligibility details available"
    return "Some details pending verification"


# Publishability: scholarships below this threshold are excluded from matches/search
PUBLISHABILITY_THRESHOLD = 40


def is_publishable(row: Any, *, threshold: int = PUBLISHABILITY_THRESHOLD) -> bool:
    """Whether a scholarship should appear in student-facing match/search results."""
    ds = _get(row, "data_status")
    if ds in ("expired", "broken_link", "past_deadline"):
        return False
    score = _get(row, "data_completeness_score")
    if score is None:
        score = compute_data_completeness_score(row)
    return int(score) >= threshold


def completeness_gaps(row: Any) -> list[str]:
    """Admin-only gap labels for data-quality dashboard."""
    gaps: list[str] = []
    if not (_get(row, "title") or "").strip():
        gaps.append("missing_title")
    if not (_get(row, "provider") or "").strip():
        gaps.append("missing_provider")
    if not _get(row, "application_deadline"):
        gaps.append("missing_deadline")
    link = (_get(row, "link") or "").strip()
    if not link.startswith(("http://", "https://")):
        gaps.append("missing_official_link")
    if not _has_json_list(_get(row, "eligible_regions")) and not _has_json_list(_get(row, "regions")):
        if not _has_json_list(_get(row, "eligible_cities")):
            gaps.append("missing_residency_rules")
    if _get(row, "max_income_threshold") is None:
        gaps.append("missing_income_rules")
    if not _has_json_list(_get(row, "eligible_courses_psced")) and not _has_json_list(
        _get(row, "eligible_courses_specific")
    ):
        gaps.append("missing_course_restrictions")
    if not _has_json_list(_get(row, "eligible_levels")) and not _get(row, "level"):
        gaps.append("missing_education_levels")
    if not _get(row, "last_verified_at"):
        gaps.append("missing_verification_date")
    return gaps
