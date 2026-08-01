"""
Match service - orchestrates hard filtering, scoring, and result assembly.
"""

import logging

logger = logging.getLogger(__name__)
from app.matching.hard_filters import (
    DEADLINE_PASSED_MESSAGE,
    cities_match,
    filter_scholarships,
    is_application_deadline_passed,
)
from app.matching.scoring_port import ScoringEnginePort, ScoringPayload, ScoringResult
from app.scoring import WeightedDeterministicScorer
from app.taxonomy.regions import normalize_region
from app.taxonomy.income_brackets import get_income_bracket
from app.serialization.scholarship import build_match_result_payload
from app.matching.temporal_state import attach_temporal_fields
from app.utils.freshness_chips import attach_freshness_fields
from app.utils.verification_display import attach_verification_fields
from app.utils.json_helpers import parse_json


def _get_field_match_level(
    profile_field_broad: str | None,
    profile_field_specific: str | None,
    profile_preferred_courses: list,
    profile_needs: list,
    eligible_psced: list,
    eligible_specific: list,
    needs_tags: list,
) -> str:
    """Determine field match level: exact, sibling, discipline, partial, or none."""
    from app.matching.field_match import compute_field_match_level

    return compute_field_match_level(
        profile_field_broad,
        profile_field_specific,
        profile_preferred_courses,
        profile_needs,
        eligible_psced,
        eligible_specific,
        needs_tags,
    )


def _get_geographic_match_level(
    profile_region: str | None,
    profile_city: str | None,
    eligible_regions: list,
    eligible_cities: list,
    legacy_regions: list,
) -> str:
    """Determine geographic match level: city, region, island_group, none."""
    regions = eligible_regions or legacy_regions or []
    profile_region_norm = normalize_region(profile_region or "")
    profile_city_lower = (profile_city or "").strip().lower()

    if eligible_cities and profile_city_lower:
        for ec in eligible_cities:
            if ec and cities_match(profile_city, ec):
                return "city"

    for r in regions:
        if not r:
            continue
        r_norm = normalize_region(r)
        if profile_region_norm and (
            profile_region_norm == r_norm or profile_region_norm in r_norm or r_norm in profile_region_norm
        ):
            return "region"
        if profile_region and r and (profile_region.lower() in r.lower() or r.lower() in profile_region.lower()):
            return "region"

    # Island group fallback
    island_groups = {"metro manila": "luzon", "luzon": "luzon", "visayas": "visayas", "mindanao": "mindanao"}
    if profile_region_norm in island_groups:
        for r in regions:
            r_norm = normalize_region(r)
            if island_groups.get(r_norm) == island_groups.get(profile_region_norm):
                return "island_group"

    return "none"


def _get_equity_flags(profile: dict) -> dict[str, bool]:
    """Extract equity flags from profile for payload."""
    from app.taxonomy.profile_priority_groups import profile_student_athlete, profile_working_student

    return {
        "is_underprivileged": bool(profile.get("is_underprivileged")),
        "is_pwd": bool(profile.get("is_pwd")),
        "is_indigenous_people": bool(profile.get("is_indigenous_people")),
        "is_solo_parent_dependent": bool(profile.get("is_solo_parent_dependent")),
        "is_ofw_dependent": bool(profile.get("is_ofw_dependent")),
        "is_farmer_fisher_dependent": bool(profile.get("is_farmer_fisher_dependent")),
        "is_4ps_listahanan": bool(profile.get("is_4ps_listahanan")),
        "is_military_dependent": bool(profile.get("is_military_dependent")),
        "is_uniformed_service_dependent": bool(profile.get("is_uniformed_service_dependent")),
        "is_gsis_dependent": bool(profile.get("is_gsis_dependent")),
        "is_sss_dependent": bool(profile.get("is_sss_dependent")),
        "working_student": profile_working_student(profile),
        "student_athlete": profile_student_athlete(profile),
        "underprivileged": bool(profile.get("is_underprivileged")),
        "pwd": bool(profile.get("is_pwd")),
        "ip": bool(profile.get("is_indigenous_people")),
        "solo_parent_dependent": bool(profile.get("is_solo_parent_dependent")),
        "ofw_dependent": bool(profile.get("is_ofw_dependent")),
        "4ps_listahanan": bool(profile.get("is_4ps_listahanan")),
    }


class MatchService:
    """Orchestrates hard filter -> score -> explain -> rank."""

    def __init__(self, scoring_engine: ScoringEnginePort | None = None):
        self.scoring_engine = scoring_engine or WeightedDeterministicScorer()

    def get_matches(self, profile: dict, scholarships: list, *, attach_temporal: bool = True) -> tuple[list[dict], dict]:
        """
        Return ranked match results with breakdown and explanation, plus filter/scoring diagnostics.
        profile and scholarships are dicts (from API/DB).
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("match_service: filter input scholarships=%d", len(scholarships))

        candidates, filter_diagnostics = filter_scholarships(profile, scholarships)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("match_service: after hard filters candidates=%d", len(candidates))

        results = []

        for sch in candidates:
            payload = self._build_scoring_payload(profile, sch)
            scoring_result = self.scoring_engine.score(payload)
            match_result = self._build_match_result(sch, scoring_result, profile)
            ds = sch.get("data_status")
            if ds == "needs_review":
                penalty = 0.65
                match_result["final_score"] = round(match_result.get("final_score", 0) * penalty, 2)
                match_result["score"] = match_result["final_score"]
                match_result["reliability_warning"] = "This scholarship needs admin review — verify details before applying."
                expl = match_result.get("explanation") or []
                if match_result["reliability_warning"] not in expl:
                    match_result["explanation"] = [match_result["reliability_warning"]] + list(expl)
            if attach_temporal:
                match_result = attach_temporal_fields(match_result, profile)
                match_result = attach_freshness_fields(match_result)
            match_result = attach_verification_fields(match_result)
            results.append(match_result)

        results.sort(
            key=lambda m: (
                1 if m.get("deadline_passed") else 0,
                1 if m.get("reliability_warning") else 0,
                -m.get("final_score", 0),
                m.get("id") or 0,
                (m.get("title") or "").lower(),
            ),
        )

        deadline_passed_matches = [m for m in results if m.get("deadline_passed")]
        active_matches = [m for m in results if not m.get("deadline_passed")]

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "match_service: scored results=%d (active=%d deadline_passed=%d)",
                len(results),
                len(active_matches),
                len(deadline_passed_matches),
            )

        diagnostics = {
            **filter_diagnostics,
            "scored_match_count": len(results),
            "active_match_count": len(active_matches),
            "deadline_passed_match_count": len(deadline_passed_matches),
        }
        return results, diagnostics

    def _build_scoring_payload(self, profile: dict, scholarship: dict) -> ScoringPayload:
        """Build ScoringPayload from profile and scholarship dicts."""
        eligible_levels = parse_json(scholarship.get("eligible_levels"))
        legacy_level = scholarship.get("level")
        profile_level = profile.get("education_level") or profile.get("current_academic_stage")

        income = profile.get("household_income_annual")
        if income is None and profile.get("income_bracket"):
            pass  # Keep income as None, bracket is separate
        income_bracket = profile.get("income_bracket") or (get_income_bracket(income) if income is not None else None)

        eligible_psced = parse_json(scholarship.get("eligible_courses_psced"))
        eligible_specific = parse_json(scholarship.get("eligible_courses_specific"))
        eligible_regions = parse_json(scholarship.get("eligible_regions"))
        legacy_regions = parse_json(scholarship.get("regions"))
        eligible_cities = parse_json(scholarship.get("eligible_cities"))
        has_field_restriction = bool(eligible_psced or eligible_specific)
        has_geographic_restriction = bool(eligible_regions or eligible_cities or legacy_regions)

        field_match = _get_field_match_level(
            profile.get("field_of_study_broad"),
            profile.get("field_of_study_specific"),
            parse_json(profile.get("preferred_courses")),
            parse_json(profile.get("needs")),
            eligible_psced,
            eligible_specific,
            parse_json(scholarship.get("needs_tags")),
        )

        geo_match = _get_geographic_match_level(
            profile.get("region"),
            profile.get("city_municipality"),
            eligible_regions,
            eligible_cities,
            legacy_regions,
        )

        elig = scholarship.get("_eligibility_result") or {}
        qual_status = elig.get("qualification_status", "qualified")
        is_provisional = qual_status == "provisionally_qualified"

        return ScoringPayload(
            gwa_normalized=profile.get("gwa_normalized"),
            household_income_annual=income,
            income_bracket=income_bracket,
            field_match_level=field_match,
            geographic_match_level=geo_match,
            equity_flags=_get_equity_flags(profile),
            scholarship_type=scholarship.get("scholarship_type") or "",
            min_gwa_required=scholarship.get("min_gwa_normalized"),
            max_income_threshold=scholarship.get("max_income_threshold"),
            priority_groups=parse_json(scholarship.get("priority_groups")),
            profile_region=profile.get("region"),
            profile_city=profile.get("city_municipality"),
            eligible_regions=eligible_regions or legacy_regions,
            eligible_cities=eligible_cities,
            has_geographic_restriction=has_geographic_restriction,
            has_field_restriction=has_field_restriction,
            is_provisional=is_provisional,
        )

    def _build_match_result(self, scholarship: dict, scoring_result: ScoringResult, profile: dict | None = None) -> dict:
        """Build API response dict from scholarship and scoring result."""
        deadline_passed = is_application_deadline_passed(scholarship.get("application_deadline"))
        elig = scholarship.get("_eligibility_result") or {}
        qual_status = elig.get("qualification_status", "qualified")
        # Eligibility status derives from EligibilityResult, not scorer
        eligibility_status = (
            qual_status in ("qualified", "provisionally_qualified", "almost_qualified")
            and not deadline_passed
        )
        explanation = list(scoring_result.explanation)
        if deadline_passed and DEADLINE_PASSED_MESSAGE not in explanation:
            explanation.insert(0, DEADLINE_PASSED_MESSAGE)
        # Prepend qualifying/missing requirements to explanation
        qualifying = elig.get("qualifying_requirements") or []
        missing = elig.get("missing_requirements") or []
        if qualifying:
            for q in qualifying[:5]:
                line = f"✓ {q}"
                if line not in explanation:
                    explanation.append(line)
        if missing and qual_status in ("provisionally_qualified", "almost_qualified"):
            for m in missing[:5]:
                line = f"✗ {m}"
                if line not in explanation:
                    explanation.append(line)

        unverified = elig.get("unverified_requirements") or []
        provisional_reason = elig.get("provisional_reason") or ""
        if provisional_reason and provisional_reason not in explanation:
            explanation.insert(0, provisional_reason)

        scoring = {
            "score": scoring_result.final_score,
            "final_score": scoring_result.final_score,
            "eligibility_status": eligibility_status,
            "deadline_passed": deadline_passed,
            "readiness_score": scoring_result.readiness_score,
            "explanation": explanation,
            "breakdown": scoring_result.breakdown,
            "confidence": elig.get("eligibility_confidence") or scoring_result.confidence,
            "suggestions": getattr(scoring_result, "suggestions", None) or [],
            "why_not_higher": getattr(scoring_result, "why_not_higher", None) or [],
            "scoring_policy_version": getattr(scoring_result, "scoring_policy_version", None) or "",
            "qualification_status": qual_status,
            "qualifying_requirements": qualifying,
            "missing_requirements": missing,
            "eligibility_confidence": elig.get("eligibility_confidence"),
            "requirements": elig.get("requirements") or [],
            "unverified_requirements": unverified,
            "provisional_reason": provisional_reason,
        }
        return build_match_result_payload(scholarship, scoring=scoring)
