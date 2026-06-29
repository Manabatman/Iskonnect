"""Scholarship data quality / confidence scoring."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from app import models


def compute_confidence_score(row: models.Scholarship | dict[str, Any]) -> float:
    """
    Compute 0.0–1.0 quality score from completeness and freshness signals.
    """

    def _get(key: str, default=None):
        if isinstance(row, dict):
            return row.get(key, default)
        return getattr(row, key, default)

    score = 0.0
    weights = {
        "title": 0.12,
        "provider": 0.10,
        "deadline": 0.15,
        "link": 0.12,
        "description": 0.08,
        "eligibility": 0.15,
        "benefits": 0.08,
        "documents": 0.05,
        "image": 0.10,
        "verified": 0.05,
    }

    if (_get("title") or "").strip():
        score += weights["title"]
    if (_get("provider") or "").strip():
        score += weights["provider"]
    if _get("application_deadline"):
        score += weights["deadline"]
    if (_get("link") or "").strip().startswith(("http://", "https://")):
        score += weights["link"]
    if (_get("description") or "").strip() and len(str(_get("description"))) >= 50:
        score += weights["description"]
    levels = _get("eligible_levels")
    regions = _get("eligible_regions") or _get("regions")
    has_levels = bool(levels and str(levels) not in ("[]", "", "null"))
    has_regions = bool(regions and str(regions) not in ("[]", "", "null"))
    if has_levels or has_regions or _get("max_income_threshold") or _get("min_gwa_normalized"):
        score += weights["eligibility"]
    if _get("benefit_tuition") or _get("benefit_allowance_monthly") or _get("benefit_total_value"):
        score += weights["benefits"]
    docs = _get("required_documents")
    if docs and str(docs) not in ("[]", "", "null"):
        score += weights["documents"]
    if (_get("image_url") or "").strip():
        score += weights["image"]
    verified = _get("last_verified_at")
    if verified:
        if isinstance(verified, datetime):
            cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=90)
            if verified >= cutoff:
                score += weights["verified"]
        else:
            score += weights["verified"] * 0.5

    ds = _get("data_status")
    if ds in ("expired", "broken_link", "past_deadline"):
        score *= 0.5
    elif ds == "needs_review":
        score *= 0.75

    return round(min(1.0, max(0.0, score)), 3)


def needs_review_reasons(row: models.Scholarship) -> list[str]:
    reasons: list[str] = []
    if not row.provider:
        reasons.append("missing_provider")
    if not row.application_deadline:
        reasons.append("missing_deadline")
    if not row.link:
        reasons.append("missing_link")
    if not row.image_url:
        reasons.append("missing_image")
    if row.data_status == "needs_review":
        reasons.append("stale_verification")
    if row.link_status == "broken":
        reasons.append("broken_link")
    if row.application_deadline and row.application_deadline < date.today() and row.is_active:
        reasons.append("past_deadline_still_active")
    if compute_confidence_score(row) < 0.5:
        reasons.append("low_quality_score")
    return reasons
