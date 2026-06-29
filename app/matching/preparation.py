"""Preparation system: document checklist, readiness score, back-scheduled milestones."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from app.matching.temporal_state import classify_scholarship_temporal
from app.utils.json_helpers import parse_json_list


def _parse_date(val: Any) -> date | None:
    if val is None:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str) and val.strip():
        try:
            return date.fromisoformat(val.strip()[:10])
        except ValueError:
            return None
    return None


def build_document_checklist(scholarship: dict, profile: dict) -> list[dict]:
    """Auto checklist from required_documents vs profile.documents."""
    required = parse_json_list(scholarship.get("required_documents"))
    profile_docs = profile.get("documents") or []
    if isinstance(profile_docs, str):
        profile_docs = parse_json_list(profile_docs)
    have = {str(d.get("type", "")).strip().lower() for d in profile_docs if isinstance(d, dict)}
    checklist = []
    for doc in required:
        key = str(doc).strip()
        if not key:
            continue
        low = key.lower()
        status = "ready" if low in have or any(low in h or h in low for h in have) else "missing"
        checklist.append({"document": key, "status": status})
    return checklist


def compute_application_readiness(scholarship: dict, profile: dict) -> dict[str, Any]:
    """0–100 readiness from documents + profile completeness signals."""
    checklist = build_document_checklist(scholarship, profile)
    doc_score = 100.0
    if checklist:
        ready = sum(1 for c in checklist if c["status"] == "ready")
        doc_score = round(100.0 * ready / len(checklist), 1)

    profile_fields = [
        profile.get("gwa_normalized"),
        profile.get("household_income_annual") or profile.get("income_bracket"),
        profile.get("education_level"),
        profile.get("region"),
        profile.get("field_of_study_broad") or profile.get("field_of_study_specific"),
    ]
    filled = sum(1 for f in profile_fields if f not in (None, "", []))
    profile_score = round(100.0 * filled / len(profile_fields), 1)

    readiness = round(doc_score * 0.6 + profile_score * 0.4, 1)
    return {
        "readiness_score": readiness,
        "document_checklist": checklist,
        "documents_ready": sum(1 for c in checklist if c["status"] == "ready"),
        "documents_total": len(checklist),
        "profile_fields_filled": filled,
        "profile_fields_total": len(profile_fields),
    }


def build_preparation_milestones(scholarship: dict, profile: dict) -> list[dict]:
    """Back-schedule milestones from predicted open/deadline dates."""
    temporal = classify_scholarship_temporal(profile, scholarship)
    target = _parse_date(scholarship.get("application_deadline"))
    if not target:
        target = _parse_date(temporal.get("predicted_open"))
    if not target:
        open_d = _parse_date(scholarship.get("application_open_date"))
        if open_d and open_d > date.today():
            target = open_d
    if not target:
        return []

    today = date.today()
    milestones = [
        {
            "title": "Gather required documents",
            "due_date": (target - timedelta(days=45)).isoformat(),
            "priority": "high",
        },
        {
            "title": "Draft essays and personal statements",
            "due_date": (target - timedelta(days=30)).isoformat(),
            "priority": "medium",
        },
        {
            "title": "Request school certifications",
            "due_date": (target - timedelta(days=21)).isoformat(),
            "priority": "high",
        },
        {
            "title": "Review and submit application",
            "due_date": (target - timedelta(days=3)).isoformat(),
            "priority": "urgent",
        },
    ]
    return [m for m in milestones if _parse_date(m["due_date"]) and _parse_date(m["due_date"]) >= today]


def build_preparation_plan(profile: dict, scholarships: list[dict], limit: int = 20) -> dict:
    """Aggregate preparation data for top actionable scholarships."""
    plans = []
    for sch in scholarships[:limit]:
        temporal = classify_scholarship_temporal(profile, sch)
        if temporal["eligibility_state"] not in (
            "eligible_now",
            "eligible_soon",
            "prepare_now",
            "missing_one_requirement",
        ):
            continue
        prep = compute_application_readiness(sch, profile)
        plans.append(
            {
                "scholarship_id": sch.get("id"),
                "title": sch.get("title"),
                "eligibility_state": temporal["eligibility_state"],
                "next_action": temporal.get("next_action"),
                **prep,
                "milestones": build_preparation_milestones(sch, profile),
            }
        )
    plans.sort(key=lambda p: -p.get("readiness_score", 0))
    return {"items": plans, "count": len(plans)}
