"""
Hard filter service - deal-breakers that exclude scholarships before scoring.
If any hard filter fails, the scholarship is not shown.
"""

import logging

from app.config import settings

logger = logging.getLogger(__name__)
from app.taxonomy.regions import normalize_region
from app.utils.json_helpers import parse_json_list


def _data_status_passes_for_matching(data_status: str | None) -> bool:
    """Exclude expired / broken_link from matching when feature flag is on."""
    if not data_status:
        return True
    return data_status not in ("expired", "broken_link")


def _level_matches(profile_level: str | None, eligible_levels: list, legacy_level: str | None) -> bool:
    """Check if profile education level matches scholarship eligibility."""
    if not profile_level or not profile_level.strip():
        return True  # No filter if profile has no level
    profile_lower = profile_level.strip().lower()

    # Map legacy level names to broader categories
    level_map = {
        "high school": ["high school", "grade 11", "grade 12"],
        "college": ["college", "college 1st year", "college 2nd year", "college 3rd year", "college 4th year"],
        "tvet": ["tvet", "vocational"],
        "graduate": ["graduate", "master's", "phd", "doctoral"],
    }

    levels_to_check = eligible_levels if eligible_levels else ([legacy_level] if legacy_level else [])
    if not levels_to_check:
        return True

    for el in levels_to_check:
        el_lower = str(el).strip().lower()
        if profile_lower == el_lower:
            return True
        # Check broad category
        for broad, variants in level_map.items():
            if el_lower == broad and profile_lower in variants:
                return True
            if profile_lower == broad and el_lower in variants:
                return True
    return False


def _region_matches(
    profile_region: str | None,
    profile_city: str | None,
    eligible_regions: list,
    eligible_cities: list,
    residency_required: bool,
    legacy_regions: list,
    scholarship_id: int | None = None,
) -> bool:
    """Check if profile location matches scholarship geographic eligibility."""
    regions = eligible_regions if eligible_regions else legacy_regions
    if not regions and not eligible_cities:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "region_match scholarship_id=%s nationwide=True",
                scholarship_id,
            )
        return True  # Nationwide

    # Residency-required programs with geographic lists: student must declare region or city
    if residency_required:
        geo_restricted = bool(regions or eligible_cities)
        has_profile_location = bool(
            (profile_region and str(profile_region).strip())
            or (profile_city and str(profile_city).strip())
        )
        if geo_restricted and not has_profile_location:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "region_match scholarship_id=%s fail=residency_required_no_location "
                    "eligible_regions=%s eligible_cities=%s",
                    scholarship_id,
                    regions,
                    eligible_cities,
                )
            return False

    profile_region_norm = normalize_region(profile_region or "")
    profile_city_lower = (profile_city or "").strip().lower()

    # City-level match (LGU)
    if eligible_cities:
        for ec in eligible_cities:
            if ec and profile_city_lower and ec.strip().lower() in profile_city_lower:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(
                        "region_match scholarship_id=%s pass=city_substring profile_city=%s ec=%s",
                        scholarship_id,
                        profile_city_lower,
                        ec,
                    )
                return True
            if ec and profile_city_lower and profile_city_lower in ec.strip().lower():
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(
                        "region_match scholarship_id=%s pass=city_reverse profile_city=%s ec=%s",
                        scholarship_id,
                        profile_city_lower,
                        ec,
                    )
                return True

    # Region-level match: use exact equality after normalization to avoid false positives
    # (e.g. "Region VI" must not substring-match "Region VII")
    for r in regions:
        if not r:
            continue
        r_norm = normalize_region(r)
        if profile_region_norm and profile_region_norm == r_norm:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "region_match scholarship_id=%s pass=region_norm profile_norm=%s sch_region=%s",
                    scholarship_id,
                    profile_region_norm,
                    r,
                )
            return True
        # Direct match when both normalize to same island group (e.g. NCR and Metro Manila)
        if profile_region and r and profile_region.strip().lower() == r.strip().lower():
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "region_match scholarship_id=%s pass=region_direct profile=%s sch=%s",
                    scholarship_id,
                    profile_region,
                    r,
                )
            return True

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "region_match scholarship_id=%s fail=no_match profile_region=%s profile_city=%s "
            "eligible_regions=%s eligible_cities=%s residency_required=%s",
            scholarship_id,
            profile_region,
            profile_city,
            regions,
            eligible_cities,
            residency_required,
        )
    return False


def _age_matches(profile_age: int | None, min_age: int | None, max_age: int | None) -> bool:
    """Check if profile age is within scholarship range."""
    if profile_age is None:
        return True
    if min_age is not None and profile_age < min_age:
        return False
    if max_age is not None and profile_age > max_age:
        return False
    return True


def _school_type_matches(profile_school_type: str | None, eligible_school_types: list) -> bool:
    """Check if profile school type is eligible."""
    if not eligible_school_types:
        return True
    if not profile_school_type or not profile_school_type.strip():
        return True
    profile_st = profile_school_type.strip().lower()
    for st in eligible_school_types:
        if st and st.strip().lower() == profile_st:
            return True
    return False  # Profile school type not in eligible list


def _income_matches(
    profile_income: int | None,
    profile_bracket: str | None,
    max_income_threshold: int | None,
) -> bool:
    """Check if profile income is below scholarship ceiling."""
    if max_income_threshold is None:
        return True
    if profile_income is not None and profile_income <= max_income_threshold:
        return True
    # Fallback: use bracket if income not provided
    if profile_bracket == "below_250k" and max_income_threshold >= 250_000:
        return True
    if profile_bracket == "250k_400k" and max_income_threshold >= 400_000:
        return True
    if profile_bracket == "400k_500k" and max_income_threshold >= 500_000:
        return True
    if profile_income is None:
        return True  # Cannot disqualify without data
    return False


def _gwa_matches(profile_gwa: float | None, min_gwa_required: float | None) -> bool:
    """Check if profile GWA meets minimum."""
    if min_gwa_required is None:
        return True
    if profile_gwa is None:
        return True  # Cannot disqualify without data
    return profile_gwa >= min_gwa_required


def _field_matches(
    profile_field_broad: str | None,
    profile_preferred_courses: list,
    eligible_courses_psced: list,
    eligible_courses_specific: list,
) -> bool:
    """Check if profile field of study matches scholarship course eligibility.
    Uses FIELD_HIERARCHY so e.g. Engineering matches STEM-eligible scholarships.
    Also checks preferred_courses against eligible_courses_specific."""
    if not eligible_courses_psced and not eligible_courses_specific:
        return True
    has_profile_data = (profile_field_broad and profile_field_broad.strip()) or (profile_preferred_courses and any(p for p in profile_preferred_courses if p))
    if not has_profile_data:
        return True
    from app.taxonomy.psced_fields import FIELD_HIERARCHY

    profile_f = profile_field_broad.strip().lower()
    profile_fields_to_check = [profile_f]
    parents = FIELD_HIERARCHY.get(profile_field_broad.strip())
    if parents:
        profile_fields_to_check.extend(p.strip().lower() for p in parents)

    for ec in eligible_courses_psced:
        if not ec:
            continue
        ec_lower = ec.strip().lower()
        for pf in profile_fields_to_check:
            if ec_lower in pf or pf in ec_lower:
                return True

    for pc in (profile_preferred_courses or []):
        if not pc:
            continue
        pc_lower = str(pc).strip().lower()
        for ec in (eligible_courses_specific or []):
            if ec and (pc_lower in str(ec).lower() or str(ec).lower() in pc_lower):
                return True
    return False


def _missing_profile_fields(profile: dict) -> list[str]:
    """Fields commonly needed for accurate hard filtering (informational for API clients)."""
    missing: list[str] = []
    if profile.get("age") is None:
        missing.append("age")
    pl = profile.get("education_level") or profile.get("current_academic_stage")
    if not pl or not str(pl).strip():
        missing.append("education_level")
    has_region = profile.get("region") and str(profile.get("region")).strip()
    has_city = profile.get("city_municipality") and str(profile.get("city_municipality")).strip()
    if not has_region and not has_city:
        missing.append("region_or_city")
    st = profile.get("school_type")
    if not st or not str(st).strip():
        missing.append("school_type")
    if profile.get("household_income_annual") is None and not profile.get("income_bracket"):
        missing.append("income")
    if profile.get("gwa_normalized") is None and not (
        profile.get("gwa_raw") and str(profile.get("gwa_raw")).strip()
    ):
        missing.append("gwa")
    broad = profile.get("field_of_study_broad")
    prefs = parse_json_list(profile.get("preferred_courses"))
    if not (broad and str(broad).strip()) and not any(prefs):
        missing.append("field_of_study")
    return missing


def _top_blockers(eliminated: dict[str, int], missing: list[str]) -> list[str]:
    """Short human-readable hints when matches are empty or sparse."""
    blockers: list[str] = []
    if "gwa" in missing:
        blockers.append(
            "Your profile is missing GWA; merit thresholds could not be evaluated strictly."
        )
    if "income" in missing:
        blockers.append(
            "Household income or bracket is missing; income ceilings may not filter accurately."
        )
    if "field_of_study" in missing:
        blockers.append(
            "Add your field of study or preferred courses to match course-specific scholarships."
        )
    if "region_or_city" in missing:
        blockers.append(
            "Region or city helps LGU and location-restricted scholarships match accurately."
        )
    labels = {
        "data_status": "expired or broken-link data status",
        "age": "age requirements",
        "education_level": "education level",
        "region": "region or city location",
        "school_type": "school type (public/private)",
        "income": "household income limits",
        "gwa": "GWA / academic minimums",
        "field": "field of study or course alignment",
    }
    for key, count in sorted(eliminated.items(), key=lambda x: -x[1]):
        if count <= 0:
            continue
        blockers.append(f"{count} scholarship(s) excluded by {labels.get(key, key)}.")
        if len(blockers) >= 6:
            break
    return blockers[:6]


def _hard_filter_failure_stage(profile: dict, sch: dict) -> str | None:
    """Return the first failed filter name, or None if the scholarship passes all hard filters."""
    sid = sch.get("id")
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "hard_filter scholarship_id=%s profile_region=%s profile_city=%s",
            sid,
            profile.get("region"),
            profile.get("city_municipality"),
        )
    if settings.filter_expired_from_matches:
        ds = sch.get("data_status")
        if not _data_status_passes_for_matching(ds):
            return "data_status"
    if not _age_matches(
        profile.get("age"),
        sch.get("min_age"),
        sch.get("max_age"),
    ):
        return "age"
    if not _level_matches(
        profile.get("education_level") or profile.get("current_academic_stage"),
        parse_json_list(sch.get("eligible_levels") or sch.get("level")),
        sch.get("level"),
    ):
        return "education_level"
    if not _region_matches(
        profile.get("region"),
        profile.get("city_municipality"),
        parse_json_list(sch.get("eligible_regions")),
        parse_json_list(sch.get("eligible_cities")),
        sch.get("residency_required", False),
        parse_json_list(sch.get("regions")),
        scholarship_id=sid,
    ):
        return "region"
    if not _school_type_matches(
        profile.get("school_type"),
        parse_json_list(sch.get("eligible_school_types")),
    ):
        return "school_type"
    if not _income_matches(
        profile.get("household_income_annual"),
        profile.get("income_bracket"),
        sch.get("max_income_threshold"),
    ):
        return "income"
    if not _gwa_matches(
        profile.get("gwa_normalized"),
        sch.get("min_gwa_normalized"),
    ):
        return "gwa"
    if not _field_matches(
        profile.get("field_of_study_broad"),
        parse_json_list(profile.get("preferred_courses")),
        parse_json_list(sch.get("eligible_courses_psced")),
        parse_json_list(sch.get("eligible_courses_specific")),
    ):
        return "field"
    return None


def filter_scholarships(profile: dict, scholarships: list) -> tuple[list, dict]:
    """
    Return scholarships that pass all hard filters and a diagnostics dict.
    profile and scholarships are dicts (from API/DB layer).
    """
    result: list = []
    eliminated: dict[str, int] = {
        "data_status": 0,
        "age": 0,
        "education_level": 0,
        "region": 0,
        "school_type": 0,
        "income": 0,
        "gwa": 0,
        "field": 0,
    }
    for sch in scholarships:
        stage = _hard_filter_failure_stage(profile, sch)
        if stage:
            eliminated[stage] = eliminated.get(stage, 0) + 1
            continue
        result.append(sch)

    missing = _missing_profile_fields(profile)
    diagnostics = {
        "total_checked": len(scholarships),
        "passed_hard_filters": len(result),
        "eliminated_by_filter": {k: v for k, v in eliminated.items() if v},
        "missing_profile_fields": missing,
        "top_blockers": _top_blockers(eliminated, missing),
    }
    return result, diagnostics
