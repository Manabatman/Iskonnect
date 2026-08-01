"""
Explainable eligibility contract — single source of truth for scholarship-student eligibility.

Every surface (matches, search, timeline, detail) consumes EligibilityResult produced here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.config import settings
from app.matching.field_match import (
    broad_maps_to_specific_eligible,
    profile_fields_for_matching,
    psced_code_matches,
    specific_course_matches,
)
from app.taxonomy.education_levels import education_levels_compatible
from app.taxonomy.equity_groups import EQUITY_GROUPS
from app.taxonomy.priority_groups import resolve_priority_group
from app.taxonomy.income_brackets import INCOME_BRACKETS
from app.taxonomy.regions import normalize_region
from app.taxonomy.school_registry import resolve_school_id
from app.taxonomy.schools import get_school_entry, school_category_for_profile
from app.utils.json_helpers import parse_json_list


class QualificationStatus(str, Enum):
    QUALIFIED = "qualified"
    PROVISIONALLY_QUALIFIED = "provisionally_qualified"
    ALMOST_QUALIFIED = "almost_qualified"
    NOT_ELIGIBLE = "not_eligible"


class RequirementResult(str, Enum):
    MET = "met"
    UNMET = "unmet"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class RequirementVerification(str, Enum):
    VERIFIED = "verified"
    PARTIAL = "partial"
    UNVERIFIED = "unverified"


@dataclass
class RequirementCheck:
    key: str
    label: str
    kind: str  # hard | soft
    result: RequirementResult
    verified: RequirementVerification
    evidence: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "kind": self.kind,
            "result": self.result.value,
            "verified": self.verified.value,
            "evidence": self.evidence,
        }


# Requirement keys whose single UNMET failure is achievable (student can close the gap).
_ACHIEVABLE_UNMET_KEYS = frozenset(
    {"gwa", "education_level", "year_level", "enrollment_status", "field"}
)

_REQUIREMENT_STUDENT_LABELS: dict[str, str] = {
    "age": "your age",
    "education_level": "your education level",
    "region": "your location",
    "school_type": "your school type",
    "school": "your school",
    "school_category": "your school category",
    "year_level": "your year level",
    "enrollment_status": "your enrollment status",
    "citizenship": "your citizenship",
    "income": "your household income",
    "gwa": "your GWA",
    "field": "your field of study",
    "members_only": "your priority group membership",
}


def derive_provisional_disclosure(requirements: list[RequirementCheck]) -> tuple[list[str], str]:
    """Human labels and summary reason from UNKNOWN requirement checks."""
    applicable = [r for r in requirements if r.result != RequirementResult.NOT_APPLICABLE]
    unknowns = [r for r in applicable if r.result == RequirementResult.UNKNOWN]
    labels: list[str] = []
    for req in unknowns:
        label = _REQUIREMENT_STUDENT_LABELS.get(req.key, req.label.lower())
        if label not in labels:
            labels.append(label)
    reason = f"We could not verify: {', '.join(labels)}" if labels else ""
    return labels, reason


@dataclass
class EligibilityResult:
    status: QualificationStatus
    requirements: list[RequirementCheck] = field(default_factory=list)
    missing_requirements: list[str] = field(default_factory=list)
    qualifying_requirements: list[str] = field(default_factory=list)
    confidence: str = "partially_verified"  # verified_requirements | partially_verified | needs_manual_review
    unverified_requirements: list[str] = field(default_factory=list)
    provisional_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "qualification_status": self.status.value,
            "requirements": [r.to_dict() for r in self.requirements],
            "missing_requirements": self.missing_requirements,
            "qualifying_requirements": self.qualifying_requirements,
            "eligibility_confidence": self.confidence,
            "unverified_requirements": self.unverified_requirements,
            "provisional_reason": self.provisional_reason,
        }

    @property
    def passes_for_matching(self) -> bool:
        """Scholarships that may appear in scored match results."""
        return self.status in (
            QualificationStatus.QUALIFIED,
            QualificationStatus.PROVISIONALLY_QUALIFIED,
        )


# --- City normalization (reduces substring false positives) ---

_CITY_ALIASES: dict[str, str] = {
    "quezon city": "quezon city",
    "qc": "quezon city",
    "city of quezon": "quezon city",
    "pasig": "pasig",
    "pasig city": "pasig",
    "city of pasig": "pasig",
    "manila": "manila",
    "city of manila": "manila",
    "makati": "makati",
    "makati city": "makati",
    "taguig": "taguig",
    "taguig city": "taguig",
    "san juan": "san juan",
    "san juan city": "san juan",
    "san juan del monte": "san juan del monte",
    "mandaluyong": "mandaluyong",
    "mandaluyong city": "mandaluyong",
    "marikina": "marikina",
    "marikina city": "marikina",
    "paranaque": "paranaque",
    "paranaque city": "paranaque",
    "las pinas": "las pinas",
    "las pinas city": "las pinas",
    "muntinlupa": "muntinlupa",
    "muntinlupa city": "muntinlupa",
    "caloocan": "caloocan",
    "caloocan city": "caloocan",
    "valenzuela": "valenzuela",
    "valenzuela city": "valenzuela",
    "malabon": "malabon",
    "malabon city": "malabon",
    "navotas": "navotas",
    "navotas city": "navotas",
    "pasay": "pasay",
    "pasay city": "pasay",
    "pateros": "pateros",
}


def normalize_city(city: str | None) -> str:
    if not city or not str(city).strip():
        return ""
    raw = str(city).strip().lower()
    raw = raw.replace("city of ", "").replace(" municipality", "").replace(" municipal", "")
    return _CITY_ALIASES.get(raw, raw)


def cities_match(profile_city: str | None, eligible_city: str | None) -> bool:
    """Exact match after canonicalization — avoids San Juan vs San Juan del Monte false positives."""
    pc = normalize_city(profile_city)
    ec = normalize_city(eligible_city)
    if not pc or not ec:
        return False
    return pc == ec


def _bracket_bounds(bracket: str | None) -> tuple[int | None, int | None]:
    """Return (lower_inclusive, upper_inclusive) annual household income for a bracket."""
    if not bracket:
        return None, None
    info = INCOME_BRACKETS.get(bracket)
    if info:
        return info.get("min"), info.get("max")
    return None, None


def _scholarship_data_verified(sch: dict) -> RequirementVerification:
    ds = sch.get("data_status")
    if ds == "needs_review":
        return RequirementVerification.UNVERIFIED
    verified_at = sch.get("last_verified_at")
    vsource = sch.get("verification_source")
    if verified_at and vsource in ("manual", "team_verified", "partner", "csv_import"):
        return RequirementVerification.VERIFIED
    if verified_at:
        return RequirementVerification.PARTIAL
    return RequirementVerification.UNVERIFIED


def _evaluate_data_status(sch: dict) -> RequirementCheck | None:
    if not settings.filter_expired_from_matches:
        return None
    ds = sch.get("data_status")
    if ds in ("expired", "broken_link", "past_deadline"):
        return RequirementCheck(
            key="data_status",
            label="Scholarship listing status",
            kind="hard",
            result=RequirementResult.UNMET,
            verified=RequirementVerification.VERIFIED,
            evidence=f"Listing marked as {ds}",
        )
    return RequirementCheck(
        key="data_status",
        label="Scholarship listing status",
        kind="hard",
        result=RequirementResult.MET,
        verified=_scholarship_data_verified(sch),
        evidence="Active listing",
    )


def _evaluate_age(profile: dict, sch: dict) -> RequirementCheck:
    age = profile.get("age")
    min_age = sch.get("min_age")
    max_age = sch.get("max_age")
    if min_age is None and max_age is None:
        return RequirementCheck("age", "Age requirement", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    if age is None:
        return RequirementCheck("age", "Age requirement", "hard", RequirementResult.UNKNOWN, RequirementVerification.UNVERIFIED, "Age not provided in profile")
    if min_age is not None and age < min_age:
        return RequirementCheck("age", f"Minimum age {min_age}", "hard", RequirementResult.UNMET, RequirementVerification.VERIFIED, f"Your age is {age}")
    if max_age is not None and age > max_age:
        return RequirementCheck("age", f"Maximum age {max_age}", "hard", RequirementResult.UNMET, RequirementVerification.VERIFIED, f"Your age is {age}")
    parts = []
    if min_age is not None:
        parts.append(f"≥ {min_age}")
    if max_age is not None:
        parts.append(f"≤ {max_age}")
    return RequirementCheck("age", "Age requirement", "hard", RequirementResult.MET, RequirementVerification.VERIFIED, f"Meets {' / '.join(parts)}")


def _evaluate_education_level(profile: dict, sch: dict) -> RequirementCheck:
    profile_level = profile.get("education_level") or profile.get("current_academic_stage")
    eligible_levels = parse_json_list(sch.get("eligible_levels") or sch.get("level"))
    legacy_level = sch.get("level")
    levels_to_check = eligible_levels if eligible_levels else ([legacy_level] if legacy_level else [])
    if not levels_to_check:
        return RequirementCheck("education_level", "Education level", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    if not profile_level or not str(profile_level).strip():
        labels = ", ".join(str(x) for x in levels_to_check if x)
        return RequirementCheck(
            "education_level",
            f"Education level ({labels})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Education level not provided",
        )
    for el in levels_to_check:
        if el and education_levels_compatible(profile_level, str(el)):
            return RequirementCheck(
                "education_level",
                f"Education level ({el})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your level: {profile_level}",
            )
    labels = ", ".join(str(x) for x in levels_to_check if x)
    return RequirementCheck(
        "education_level",
        f"Education level ({labels})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your level: {profile_level}",
    )


def _evaluate_region(profile: dict, sch: dict) -> RequirementCheck:
    eligible_regions = parse_json_list(sch.get("eligible_regions"))
    eligible_cities = parse_json_list(sch.get("eligible_cities"))
    legacy_regions = parse_json_list(sch.get("regions"))
    regions = eligible_regions if eligible_regions else legacy_regions
    residency_required = bool(sch.get("residency_required"))
    profile_region = profile.get("region")
    profile_city = profile.get("city_municipality")
    sch_verified = _scholarship_data_verified(sch)

    if not regions and not eligible_cities:
        return RequirementCheck("region", "Location / residency", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED, "Nationwide")

    has_location = bool((profile_region and str(profile_region).strip()) or (profile_city and str(profile_city).strip()))
    if residency_required and not has_location:
        return RequirementCheck(
            "region",
            "Location / residency",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Region or city required but not provided",
        )

    # City-level exact match
    if eligible_cities and profile_city:
        for ec in eligible_cities:
            if ec and cities_match(profile_city, ec):
                return RequirementCheck(
                    "region",
                    f"Residency ({ec})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your city: {profile_city}",
                )
        city_labels = ", ".join(str(c) for c in eligible_cities if c)
        return RequirementCheck(
            "region",
            f"Residency ({city_labels})",
            "hard",
            RequirementResult.UNMET,
            RequirementVerification.VERIFIED,
            f"Your city: {profile_city}",
        )

    # Region-level exact match
    profile_region_norm = normalize_region(profile_region or "")
    if regions and profile_region_norm:
        for r in regions:
            if not r:
                continue
            r_norm = normalize_region(r)
            if profile_region_norm == r_norm:
                return RequirementCheck(
                    "region",
                    f"Region ({r})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your region: {profile_region}",
                )
            if profile_region and profile_region.strip().lower() == r.strip().lower():
                return RequirementCheck(
                    "region",
                    f"Region ({r})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your region: {profile_region}",
                )

    if regions or eligible_cities:
        if not has_location:
            return RequirementCheck(
                "region",
                "Location / residency",
                "hard",
                RequirementResult.UNKNOWN,
                RequirementVerification.UNVERIFIED,
                "Location not provided",
            )
        loc_parts = []
        if eligible_cities:
            loc_parts.append(", ".join(str(c) for c in eligible_cities if c))
        if regions:
            loc_parts.append(", ".join(str(r) for r in regions if r))
        your = profile_city or profile_region or ""
        return RequirementCheck(
            "region",
            f"Location ({' / '.join(loc_parts)})",
            "hard",
            RequirementResult.UNMET,
            sch_verified,
            f"Your location: {your}",
        )

    return RequirementCheck("region", "Location / residency", "hard", RequirementResult.UNKNOWN, RequirementVerification.UNVERIFIED)


def _profile_school_ids(profile: dict) -> tuple[str | None, str | None]:
    school_id = profile.get("school_id") or resolve_school_id(profile.get("school"))
    target_id = profile.get("target_school_id") or resolve_school_id(profile.get("target_school"))
    return school_id, target_id


def _evaluate_school(profile: dict, sch: dict) -> RequirementCheck:
    eligible_schools = parse_json_list(sch.get("eligible_schools"))
    eligible_systems = parse_json_list(sch.get("eligible_school_systems"))
    if not eligible_schools and not eligible_systems:
        return RequirementCheck("school", "School / HEI", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)

    school_id, target_id = _profile_school_ids(profile)
    profile_ids = [x for x in (school_id, target_id) if x]
    sch_verified = _scholarship_data_verified(sch)

    if eligible_schools:
        if not profile_ids:
            labels = ", ".join(str(x) for x in eligible_schools if x)
            return RequirementCheck(
                "school",
                f"School ({labels})",
                "hard",
                RequirementResult.UNKNOWN,
                RequirementVerification.UNVERIFIED,
                "School not provided in profile",
            )
        for sid in profile_ids:
            if sid in eligible_schools:
                entry = get_school_entry(sid)
                name = entry["canonical_name"] if entry else sid
                return RequirementCheck(
                    "school",
                    f"School ({name})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your school: {profile.get('school') or name}",
                )
        labels = ", ".join(str(x) for x in eligible_schools if x)
        return RequirementCheck(
            "school",
            f"School ({labels})",
            "hard",
            RequirementResult.UNMET,
            sch_verified,
            f"Your school: {profile.get('school') or school_id or '—'}",
        )

    if eligible_systems:
        if not profile_ids:
            labels = ", ".join(str(x) for x in eligible_systems if x)
            return RequirementCheck(
                "school",
                f"School system ({labels})",
                "hard",
                RequirementResult.UNKNOWN,
                RequirementVerification.UNVERIFIED,
                "School not provided in profile",
            )
        for sid in profile_ids:
            entry = get_school_entry(sid)
            system_id = entry.get("system_id") if entry else None
            if system_id and system_id in eligible_systems:
                return RequirementCheck(
                    "school",
                    f"School system ({system_id})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your school system: {system_id}",
                )
        labels = ", ".join(str(x) for x in eligible_systems if x)
        return RequirementCheck(
            "school",
            f"School system ({labels})",
            "hard",
            RequirementResult.UNMET,
            sch_verified,
            "Your school is outside the required system",
        )

    return RequirementCheck("school", "School / HEI", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)


def _evaluate_school_category(profile: dict, sch: dict) -> RequirementCheck:
    eligible = parse_json_list(sch.get("eligible_school_categories"))
    if not eligible:
        return RequirementCheck("school_category", "School category", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    category = school_category_for_profile(profile)
    if not category:
        labels = ", ".join(str(x) for x in eligible if x)
        return RequirementCheck(
            "school_category",
            f"School category ({labels})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "School category could not be determined — add your school",
        )
    cat_lower = category.strip().lower()
    for ec in eligible:
        if ec and str(ec).strip().lower() == cat_lower:
            return RequirementCheck(
                "school_category",
                f"School category ({ec})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your school category: {category}",
            )
    labels = ", ".join(str(x) for x in eligible if x)
    return RequirementCheck(
        "school_category",
        f"School category ({labels})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your school category: {category}",
    )


def _evaluate_year_level(profile: dict, sch: dict) -> RequirementCheck:
    eligible = parse_json_list(sch.get("eligible_year_levels"))
    if not eligible:
        return RequirementCheck("year_level", "Year level", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    current = profile.get("current_year_level")
    nxt = profile.get("next_year_level")
    levels: list[int] = []
    for raw in eligible:
        try:
            levels.append(int(raw))
        except (TypeError, ValueError):
            continue
    if not levels:
        return RequirementCheck("year_level", "Year level", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    if current is None and nxt is None:
        label = ", ".join(str(x) for x in levels)
        return RequirementCheck(
            "year_level",
            f"Year level ({label})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Year level not provided in profile",
        )
    for val in (current, nxt):
        if val is not None and int(val) in levels:
            return RequirementCheck(
                "year_level",
                f"Year level ({val})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your year level: {val}",
            )
    label = ", ".join(str(x) for x in levels)
    shown = current if current is not None else nxt
    return RequirementCheck(
        "year_level",
        f"Year level ({label})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your year level: {shown}",
    )


def _evaluate_enrollment_status(profile: dict, sch: dict) -> RequirementCheck:
    eligible = parse_json_list(sch.get("eligible_enrollment_status"))
    if not eligible:
        return RequirementCheck("enrollment_status", "Enrollment status", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    status = (profile.get("enrollment_status") or "").strip()
    if not status:
        labels = ", ".join(str(x) for x in eligible if x)
        return RequirementCheck(
            "enrollment_status",
            f"Enrollment status ({labels})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Enrollment status not provided",
        )
    status_lower = status.lower()
    for es in eligible:
        if es and str(es).strip().lower() == status_lower:
            return RequirementCheck(
                "enrollment_status",
                f"Enrollment status ({es})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your status: {status}",
            )
    labels = ", ".join(str(x) for x in eligible if x)
    return RequirementCheck(
        "enrollment_status",
        f"Enrollment status ({labels})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your status: {status}",
    )


def _evaluate_citizenship(profile: dict, sch: dict) -> RequirementCheck:
    required = (sch.get("citizenship_required") or "Filipino").strip()
    if not required or required.lower() in ("any", "none", "open"):
        return RequirementCheck("citizenship", "Citizenship", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    citizenship = (profile.get("citizenship") or "").strip()
    if not citizenship:
        return RequirementCheck(
            "citizenship",
            f"Citizenship ({required})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Citizenship not provided",
        )
    if citizenship.lower() == required.lower():
        return RequirementCheck(
            "citizenship",
            f"Citizenship ({required})",
            "hard",
            RequirementResult.MET,
            RequirementVerification.VERIFIED,
            f"Your citizenship: {citizenship}",
        )
    return RequirementCheck(
        "citizenship",
        f"Citizenship ({required})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your citizenship: {citizenship}",
    )


def _evaluate_school_type(profile: dict, sch: dict) -> RequirementCheck:
    eligible = parse_json_list(sch.get("eligible_school_types"))
    if not eligible:
        return RequirementCheck("school_type", "School type", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    profile_st = profile.get("school_type")
    if not profile_st or not str(profile_st).strip():
        labels = ", ".join(str(x) for x in eligible if x)
        return RequirementCheck(
            "school_type",
            f"School type ({labels})",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "School type not provided",
        )
    profile_st_lower = profile_st.strip().lower()
    for st in eligible:
        if st and st.strip().lower() == profile_st_lower:
            return RequirementCheck(
                "school_type",
                f"School type ({st})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your school type: {profile_st}",
            )
    labels = ", ".join(str(x) for x in eligible if x)
    return RequirementCheck(
        "school_type",
        f"School type ({labels})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your school type: {profile_st}",
    )


def _evaluate_income(profile: dict, sch: dict) -> RequirementCheck:
    threshold = sch.get("max_income_threshold")
    if threshold is None:
        return RequirementCheck("income", "Household income ceiling", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    income = profile.get("household_income_annual")
    bracket = profile.get("income_bracket")
    sch_verified = _scholarship_data_verified(sch)

    if income is not None:
        if income <= threshold:
            return RequirementCheck(
                "income",
                f"Income ≤ ₱{threshold:,}",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"Your household income: ₱{income:,}",
            )
        return RequirementCheck(
            "income",
            f"Income ≤ ₱{threshold:,}",
            "hard",
            RequirementResult.UNMET,
            RequirementVerification.VERIFIED,
            f"Your household income: ₱{income:,}",
        )

    if bracket:
        lower, upper = _bracket_bounds(bracket)
        if lower is not None and lower > threshold:
            return RequirementCheck(
                "income",
                f"Income ≤ ₱{threshold:,}",
                "hard",
                RequirementResult.UNMET,
                RequirementVerification.PARTIAL,
                f"Your income bracket ({bracket}) may exceed the ceiling",
            )
        if upper is not None and upper <= threshold:
            return RequirementCheck(
                "income",
                f"Income ≤ ₱{threshold:,}",
                "hard",
                RequirementResult.MET,
                RequirementVerification.PARTIAL,
                f"Your income bracket ({bracket}) is within the ceiling",
            )
        return RequirementCheck(
            "income",
            f"Income ≤ ₱{threshold:,}",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            f"Income bracket ({bracket}) overlaps the ceiling — exact income needed",
        )

    return RequirementCheck(
        "income",
        f"Income ≤ ₱{threshold:,}",
        "hard",
        RequirementResult.UNKNOWN,
        RequirementVerification.UNVERIFIED,
        "Household income not provided",
    )


def _evaluate_gwa(profile: dict, sch: dict) -> RequirementCheck:
    min_gwa = sch.get("min_gwa_normalized")
    if min_gwa is None:
        return RequirementCheck("gwa", "GWA / academic minimum", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    gwa = profile.get("gwa_normalized")
    if gwa is None:
        return RequirementCheck(
            "gwa",
            f"GWA ≥ {min_gwa}%",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "GWA not provided",
        )
    if gwa >= min_gwa:
        return RequirementCheck(
            "gwa",
            f"GWA ≥ {min_gwa}%",
            "hard",
            RequirementResult.MET,
            RequirementVerification.VERIFIED,
            f"Your GWA: {gwa}%",
        )
    return RequirementCheck(
        "gwa",
        f"GWA ≥ {min_gwa}%",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your GWA: {gwa}%",
    )


def _evaluate_field(profile: dict, sch: dict) -> RequirementCheck:
    eligible_psced = parse_json_list(sch.get("eligible_courses_psced"))
    eligible_specific = parse_json_list(sch.get("eligible_courses_specific"))
    if not eligible_psced and not eligible_specific:
        return RequirementCheck("field", "Field of study / course", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)

    profile_broad = profile.get("field_of_study_broad")
    preferred = parse_json_list(profile.get("preferred_courses"))
    has_profile = (profile_broad and str(profile_broad).strip()) or any(p for p in preferred if p)
    if not has_profile:
        return RequirementCheck(
            "field",
            "Field of study / course",
            "hard",
            RequirementResult.UNKNOWN,
            RequirementVerification.UNVERIFIED,
            "Field of study not provided",
        )

    profile_fields = profile_fields_for_matching(profile_broad)
    for ec in eligible_psced:
        if not ec:
            continue
        for pf in profile_fields:
            if psced_code_matches(pf, str(ec)):
                return RequirementCheck(
                    "field",
                    f"Course / field ({ec})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your field: {profile_broad or preferred[0] if preferred else ''}",
                )
    for pc in preferred:
        if not pc:
            continue
        for ec in eligible_specific:
            if ec and specific_course_matches(str(pc), str(ec)):
                return RequirementCheck(
                    "field",
                    f"Course ({ec})",
                    "hard",
                    RequirementResult.MET,
                    RequirementVerification.VERIFIED,
                    f"Your course: {pc}",
                )
    if broad_maps_to_specific_eligible(profile_broad, eligible_specific):
        return RequirementCheck(
            "field",
            "Field of study / course",
            "hard",
            RequirementResult.MET,
            RequirementVerification.PARTIAL,
            f"Your field: {profile_broad}",
        )

    field_label = profile_broad or (preferred[0] if preferred else "")
    req_label = ", ".join(str(x) for x in (eligible_specific or eligible_psced)[:3] if x)
    return RequirementCheck(
        "field",
        f"Course / field ({req_label})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        f"Your field: {field_label}",
    )


def _evaluate_members_only(profile: dict, sch: dict) -> RequirementCheck:
    if not sch.get("members_only"):
        return RequirementCheck("members_only", "Priority group membership", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    groups = parse_json_list(sch.get("priority_groups"))
    if not groups:
        return RequirementCheck("members_only", "Priority group membership", "hard", RequirementResult.NOT_APPLICABLE, RequirementVerification.VERIFIED)
    from app.taxonomy.profile_priority_groups import (
        STUDENT_ATHLETE,
        WORKING_STUDENT,
        profile_student_athlete,
        profile_working_student,
    )

    profile_priority_checks = {
        WORKING_STUDENT: profile_working_student,
        STUDENT_ATHLETE: profile_student_athlete,
    }
    for group in groups:
        if not group:
            continue
        canon = resolve_priority_group(str(group))
        check_fn = profile_priority_checks.get(canon)
        if check_fn and check_fn(profile):
            return RequirementCheck(
                "members_only",
                f"Membership ({canon})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"You declared: {canon}",
            )
        info = EQUITY_GROUPS.get(canon, {})
        flag = info.get("profile_flag")
        if not flag:
            flag_key = str(canon).lower().replace(" ", "_").replace("/", "_")
            flag = f"is_{flag_key}"
        if profile.get(flag):
            return RequirementCheck(
                "members_only",
                f"Membership ({canon})",
                "hard",
                RequirementResult.MET,
                RequirementVerification.VERIFIED,
                f"You declared: {canon}",
            )
    labels = ", ".join(resolve_priority_group(str(g)) for g in groups if g)
    return RequirementCheck(
        "members_only",
        f"Membership ({labels})",
        "hard",
        RequirementResult.UNMET,
        RequirementVerification.VERIFIED,
        "Required priority group not declared in profile",
    )


# Registry of evaluators keyed by opportunity_type. Default scholarship uses all current evaluators.
_EVALUATOR_REGISTRY: dict[str, list] = {
    "scholarship": [
        _evaluate_data_status,
        _evaluate_age,
        _evaluate_education_level,
        _evaluate_region,
        _evaluate_school_type,
        _evaluate_school,
        _evaluate_school_category,
        _evaluate_year_level,
        _evaluate_enrollment_status,
        _evaluate_citizenship,
        _evaluate_income,
        _evaluate_gwa,
        _evaluate_field,
        _evaluate_members_only,
    ],
}


def _evaluators_for_opportunity(scholarship: dict) -> list:
    opp_type = (scholarship.get("opportunity_type") or "scholarship").strip().lower()
    evaluators = _EVALUATOR_REGISTRY.get(opp_type)
    if evaluators is not None:
        return evaluators
    return _EVALUATOR_REGISTRY["scholarship"]


def _derive_status(requirements: list[RequirementCheck], sch: dict) -> QualificationStatus:
    applicable = [r for r in requirements if r.result != RequirementResult.NOT_APPLICABLE]
    unmet = [r for r in applicable if r.result == RequirementResult.UNMET]
    if len(unmet) == 1 and unmet[0].key in _ACHIEVABLE_UNMET_KEYS:
        return QualificationStatus.ALMOST_QUALIFIED
    if unmet:
        return QualificationStatus.NOT_ELIGIBLE
    unknowns = [r for r in applicable if r.result == RequirementResult.UNKNOWN]
    if unknowns:
        return QualificationStatus.PROVISIONALLY_QUALIFIED
    if sch.get("data_status") == "needs_review":
        return QualificationStatus.PROVISIONALLY_QUALIFIED
    unverified = [r for r in applicable if r.result == RequirementResult.MET and r.verified != RequirementVerification.VERIFIED]
    if unverified:
        return QualificationStatus.PROVISIONALLY_QUALIFIED
    return QualificationStatus.QUALIFIED


def _derive_confidence(requirements: list[RequirementCheck], sch: dict) -> str:
    if sch.get("data_status") == "needs_review":
        return "needs_manual_review"
    applicable = [r for r in requirements if r.result != RequirementResult.NOT_APPLICABLE]
    if not applicable:
        return "partially_verified"
    all_verified = all(
        r.verified == RequirementVerification.VERIFIED or r.result == RequirementResult.NOT_APPLICABLE
        for r in applicable
    )
    any_unknown = any(r.result == RequirementResult.UNKNOWN for r in applicable)
    if all_verified and not any_unknown:
        return "verified_requirements"
    if any_unknown or any(r.verified == RequirementVerification.PARTIAL for r in applicable):
        return "partially_verified"
    return "partially_verified"


def evaluate_eligibility(profile: dict, scholarship: dict) -> EligibilityResult:
    """Evaluate full eligibility for a profile-scholarship pair. Single authority for all surfaces."""
    requirements: list[RequirementCheck] = []
    for evaluator in _evaluators_for_opportunity(scholarship):
        if evaluator is _evaluate_data_status:
            ds_check = evaluator(scholarship)
            if ds_check:
                requirements.append(ds_check)
        else:
            requirements.append(evaluator(profile, scholarship))

    status = _derive_status(requirements, scholarship)
    confidence = _derive_confidence(requirements, scholarship)

    qualifying: list[str] = []
    missing: list[str] = []
    for req in requirements:
        if req.result == RequirementResult.NOT_APPLICABLE:
            continue
        if req.result == RequirementResult.MET:
            qualifying.append(req.label)
        elif req.result == RequirementResult.UNMET:
            missing.append(req.label)
        elif req.result == RequirementResult.UNKNOWN:
            missing.append(f"{req.label} (not verified — add to profile)")

    unverified, provisional_reason = derive_provisional_disclosure(requirements)

    return EligibilityResult(
        status=status,
        requirements=requirements,
        missing_requirements=missing,
        qualifying_requirements=qualifying,
        confidence=confidence,
        unverified_requirements=unverified,
        provisional_reason=provisional_reason,
    )
