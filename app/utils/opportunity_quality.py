"""Unified opportunity quality score (0–100) merging confidence and completeness signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from app import models
from app.utils.data_completeness import compute_data_completeness_score
from app.utils.quality_score import compute_confidence_score

# Weights sum to 100; each key maps to a scholarship field or composite check.
QUALITY_WEIGHTS: dict[str, int] = {
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
    "image": 3,
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


def _field_has_value(row: Any, component: str) -> bool:
    if component == "title":
        return bool((_get(row, "title") or "").strip())
    if component == "provider":
        return bool((_get(row, "provider") or "").strip())
    if component == "official_link":
        link = (_get(row, "link") or "").strip()
        return link.startswith(("http://", "https://"))
    if component == "deadline":
        return _get(row, "application_deadline") is not None
    if component == "structured_eligibility":
        has_levels = _has_json_list(_get(row, "eligible_levels")) or bool(_get(row, "level"))
        has_regions = _has_json_list(_get(row, "eligible_regions")) or _has_json_list(_get(row, "regions"))
        has_cities = _has_json_list(_get(row, "eligible_cities"))
        has_income = _get(row, "max_income_threshold") is not None
        has_gwa = _get(row, "min_gwa_normalized") is not None
        has_courses = _has_json_list(_get(row, "eligible_courses_psced")) or _has_json_list(
            _get(row, "eligible_courses_specific")
        )
        return has_levels or has_regions or has_cities or has_income or has_gwa or has_courses
    if component == "residency_rules":
        return _has_json_list(_get(row, "eligible_regions")) or _has_json_list(
            _get(row, "eligible_cities")
        ) or _has_json_list(_get(row, "regions"))
    if component == "income_rules":
        return _get(row, "max_income_threshold") is not None
    if component == "course_restrictions":
        return _has_json_list(_get(row, "eligible_courses_psced")) or _has_json_list(
            _get(row, "eligible_courses_specific")
        )
    if component == "education_levels":
        return _has_json_list(_get(row, "eligible_levels")) or bool(_get(row, "level"))
    if component == "verification":
        verified = _get(row, "last_verified_at")
        vsource = _get(row, "verification_source")
        return bool(verified and vsource in ("manual", "team_verified", "partner", "csv_import"))
    if component == "benefits":
        return bool(
            _get(row, "benefit_tuition")
            or _get(row, "benefit_allowance_monthly")
            or _get(row, "benefit_total_value")
        )
    if component == "documents":
        return _has_json_list(_get(row, "required_documents"))
    if component == "description":
        return len((_get(row, "description") or "").strip()) >= 50
    if component == "image":
        return bool((_get(row, "image_url") or "").strip())
    return False


# Map quality components to field_evidence.field_key values.
COMPONENT_EVIDENCE_KEYS: dict[str, list[str]] = {
    "title": ["title"],
    "provider": ["provider"],
    "official_link": ["link"],
    "deadline": ["application_deadline"],
    "structured_eligibility": [
        "eligible_levels",
        "eligible_regions",
        "eligible_cities",
        "max_income_threshold",
        "min_gwa_normalized",
        "eligible_courses_psced",
        "eligible_courses_specific",
    ],
    "residency_rules": ["eligible_regions", "eligible_cities", "regions", "residency_required"],
    "income_rules": ["max_income_threshold"],
    "course_restrictions": ["eligible_courses_psced", "eligible_courses_specific"],
    "education_levels": ["eligible_levels", "level"],
    "verification": ["last_verified_at"],
    "benefits": ["benefit_tuition", "benefit_allowance_monthly", "benefit_total_value"],
    "documents": ["required_documents"],
    "description": ["description"],
    "image": ["image_url"],
}


def _load_evidence_keys(db: Session, scholarship_id: int) -> set[str]:
    rows = (
        db.query(models.FieldEvidence.field_key)
        .filter(
            models.FieldEvidence.scholarship_id == scholarship_id,
            models.FieldEvidence.superseded_at.is_(None),
            models.FieldEvidence.source_url.isnot(None),
            models.FieldEvidence.source_url != "",
        )
        .all()
    )
    return {r[0] for r in rows if r[0]}


def _component_evidence_backed(component: str, evidence_keys: set[str]) -> bool:
    keys = COMPONENT_EVIDENCE_KEYS.get(component, [])
    if not keys:
        return False
    return any(k in evidence_keys for k in keys)


@dataclass
class OpportunityQualityResult:
    score: int
    components: dict[str, int] = field(default_factory=dict)
    evidence_gated: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "components": self.components,
            "evidence_gated": self.evidence_gated,
        }


def compute_opportunity_quality(row: Any, db: Session | None = None) -> OpportunityQualityResult:
    """
    Return 0–100 quality score with per-component breakdown.
    Fields contribute only when backed by active field_evidence with source_url.
    When no evidence exists for a scholarship, falls back to legacy combined scoring.
    """
    scholarship_id = _get(row, "id")
    evidence_keys: set[str] = set()
    evidence_gated = False

    if db is not None and scholarship_id is not None:
        evidence_keys = _load_evidence_keys(db, int(scholarship_id))
        evidence_gated = bool(evidence_keys)

    if not evidence_gated:
        completeness = compute_data_completeness_score(row)
        confidence = compute_confidence_score(row)
        blended = round(completeness * 0.65 + confidence * 100 * 0.35)
        return OpportunityQualityResult(
            score=min(100, max(0, blended)),
            components={"legacy_completeness": completeness, "legacy_confidence": round(confidence * 100, 1)},
            evidence_gated=False,
        )

    components: dict[str, int] = {}
    total = 0
    for name, weight in QUALITY_WEIGHTS.items():
        if not _field_has_value(row, name):
            components[name] = 0
            continue
        if not _component_evidence_backed(name, evidence_keys):
            components[name] = 0
            continue
        components[name] = weight
        total += weight

    ds = (_get(row, "data_status") or "").strip().lower()
    if ds in ("expired", "broken_link", "past_deadline"):
        total = int(total * 0.5)
    elif ds == "needs_review":
        total = int(total * 0.75)

    score = min(100, max(0, total))
    return OpportunityQualityResult(score=score, components=components, evidence_gated=True)


def apply_quality_scores(row: Any, db: Session | None = None) -> OpportunityQualityResult:
    """Compute quality metrics and persist publishability-relevant completeness."""
    result = compute_opportunity_quality(row, db)
    completeness = compute_data_completeness_score(row)
    if hasattr(row, "data_completeness_score"):
        row.data_completeness_score = completeness
    if hasattr(row, "confidence_score"):
        row.confidence_score = compute_confidence_score(row)
    return result
