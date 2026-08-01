"""
Independent eligibility oracle for the Iskonnect matching engine evaluation.

This encodes how a competent scholarship administrator would judge eligibility.
It does NOT import the engine's hard_filters; region normalization, level
bucketing, and field bridging are implemented here independently so the oracle
represents *correct* behaviour rather than the engine's behaviour.

Guiding principle (lenient mode): missing a scholarship is worse than an extra
one, so when STUDENT data is missing we give the benefit of the doubt (eligible).
Scholarship restrictions that are present are enforced.

Strict mode (unknown_policy="strict") fails closed on missing student data so CI
can measure engine over-inclusion against a conservative baseline.
"""

from __future__ import annotations

from typing import Literal

UnknownPolicy = Literal["lenient", "strict"]

# --- Region normalization (independent of engine) ---
_REGION_ALIASES = {
    "ncr": "ncr", "metro manila": "ncr", "national capital region": "ncr",
    "barmm": "barmm", "bangsamoro": "barmm",
    "car": "car", "cordillera": "car",
    "calabarzon": "region iv-a - calabarzon", "region iv-a - calabarzon": "region iv-a - calabarzon",
    "region 4a": "region iv-a - calabarzon", "region 4a - calabarzon": "region iv-a - calabarzon",
    "region iv-a": "region iv-a - calabarzon",
    "central visayas": "region vii - central visayas", "region vii - central visayas": "region vii - central visayas",
    "davao": "region xi - davao", "davao region": "region xi - davao", "region xi - davao": "region xi - davao",
    "central luzon": "region iii - central luzon", "region iii - central luzon": "region iii - central luzon",
    "western visayas": "region vi - western visayas", "region vi - western visayas": "region vi - western visayas",
}


def _onorm(r: str | None) -> str:
    key = (r or "").strip().lower()
    return _REGION_ALIASES.get(key, key)


# --- Level bucketing (independent) ---
_LEVEL_BUCKET = {
    "college": "college",
    "college 1st year": "college", "college 2nd year": "college",
    "college 3rd year": "college", "college 4th year": "college",
    "senior high": "senior high", "senior high school": "senior high",
    "grade 11": "senior high", "grade 12": "senior high",
    "high school": "senior high",
    "tvet": "tvet", "vocational": "tvet",
}


def _bucket(level: str | None) -> str | None:
    if not level:
        return None
    return _LEVEL_BUCKET.get(level.strip().lower(), level.strip().lower())


from app.matching.field_match import profile_fields_for_matching, specific_course_matches
from app.taxonomy.psced_fields import PSCED_SPECIFIC_COURSES, resolve_normalized_field

# Oracle-specific course bridge (same vocabulary as engine; independent matching logic)
_SPECIFIC_BY_BROAD = {
    broad.lower(): [c.lower() for c in courses]
    for broad, courses in PSCED_SPECIFIC_COURSES.items()
}

_PRIORITY_GROUP_TO_FLAG = {
    "PWD": "is_pwd",
    "IP": "is_indigenous_people",
    "Underprivileged": "is_underprivileged",
    "Solo Parent Dependent": "is_solo_parent_dependent",
    "OFW Dependent": "is_ofw_dependent",
    "Farmer/Fisher Dependent": "is_farmer_fisher_dependent",
    "4Ps/Listahanan": "is_4ps_listahanan",
}

_MERIT_TYPES = ("merit", "merit-based", "academic")


def _strict_missing(*values) -> bool:
    return any(v is None or (isinstance(v, str) and not str(v).strip()) for v in values)


def _field_eligible(profile: dict, sch: dict, *, unknown_policy: UnknownPolicy) -> bool:
    restr_psced = {str(c).strip().lower() for c in (sch.get("eligible_courses_psced") or []) if c}
    restr_spec = {str(c).strip().lower() for c in (sch.get("eligible_courses_specific") or []) if c}
    if not restr_psced and not restr_spec:
        return True
    broad_raw = profile.get("field_of_study_broad") or ""
    broad = (resolve_normalized_field(broad_raw) or broad_raw).strip().lower()
    prefs = [str(p).strip().lower() for p in (profile.get("preferred_courses") or []) if p]
    spec = (profile.get("field_of_study_specific") or "").strip().lower()
    if spec:
        prefs.append(spec)
    if not broad and not prefs:
        if unknown_policy == "strict":
            return False
        return True  # no field data -> benefit of the doubt (lenient)

    disc = set(profile_fields_for_matching(broad_raw or broad))
    if disc & restr_psced:
        return True
    if restr_spec and any(p in restr_spec for p in prefs):
        return True
    if broad and restr_spec:
        if {s for s in _SPECIFIC_BY_BROAD.get(broad, [])} & restr_spec:
            return True
    if restr_psced:
        for p in prefs:
            for bcode, specs in _SPECIFIC_BY_BROAD.items():
                if p in specs and bcode in restr_psced:
                    return True
    return False


def is_eligible(profile: dict, sch: dict, *, unknown_policy: UnknownPolicy = "lenient") -> bool:
    """Return True if the admin would consider the student eligible for the scholarship."""
    strict = unknown_policy == "strict"

    # data quality gates (engine and reality agree)
    if sch.get("is_active") is False:
        return False
    if sch.get("data_status") in ("expired", "broken_link"):
        return False

    # age
    age = profile.get("age")
    if age is not None:
        if sch.get("min_age") is not None and age < sch["min_age"]:
            return False
        if sch.get("max_age") is not None and age > sch["max_age"]:
            return False
    elif strict and (sch.get("min_age") is not None or sch.get("max_age") is not None):
        return False

    # education level
    levels = [str(x).strip().lower() for x in (sch.get("eligible_levels") or []) if x]
    plevel = _bucket(profile.get("education_level") or profile.get("current_academic_stage"))
    if levels:
        if plevel is None:
            if strict:
                return False
        else:
            buckets = {_bucket(x) for x in levels}
            if plevel not in buckets and plevel not in levels:
                return False

    # region / city
    regions = [r for r in (sch.get("eligible_regions") or []) if r]
    cities = [c for c in (sch.get("eligible_cities") or []) if c]
    if regions or cities:
        pcity = (profile.get("city_municipality") or "").strip().lower()
        pregion = _onorm(profile.get("region"))
        matched = False
        if cities and pcity:
            for c in cities:
                if c.strip().lower() == pcity:
                    matched = True
                    break
        if not matched and regions and pregion:
            sch_regions = {_onorm(r) for r in regions}
            if pregion in sch_regions:
                matched = True
        if not matched:
            if strict and _strict_missing(profile.get("region"), profile.get("city_municipality")):
                return False
            if not strict and not pcity and not pregion:
                return True  # lenient: benefit of the doubt
            return False

    # school type
    est = [str(x).strip().lower() for x in (sch.get("eligible_school_types") or []) if x]
    pst = (profile.get("school_type") or "").strip().lower()
    if est:
        if not pst:
            if strict:
                return False
        elif pst not in est:
            return False

    # specific HEI / system
    eligible_schools = [str(x).strip() for x in (sch.get("eligible_schools") or []) if x]
    eligible_systems = [str(x).strip() for x in (sch.get("eligible_school_systems") or []) if x]
    if eligible_schools or eligible_systems:
        from app.taxonomy.school_registry import resolve_school_id
        from app.taxonomy.schools import get_school_entry

        school_id = profile.get("school_id") or resolve_school_id(profile.get("school"))
        target_id = profile.get("target_school_id") or resolve_school_id(profile.get("target_school"))
        profile_ids = [x for x in (school_id, target_id) if x]
        if not profile_ids:
            if strict:
                return False
            return True  # benefit of the doubt when school data missing (lenient)
        if eligible_schools and not any(pid in eligible_schools for pid in profile_ids):
            return False
        if eligible_systems:
            matched_system = False
            for pid in profile_ids:
                entry = get_school_entry(pid)
                if entry and entry.get("system_id") in eligible_systems:
                    matched_system = True
                    break
            if not matched_system:
                return False

    # school category
    eligible_categories = [str(x).strip().lower() for x in (sch.get("eligible_school_categories") or []) if x]
    if eligible_categories:
        from app.taxonomy.schools import school_category_for_profile

        cat = school_category_for_profile(profile)
        if not cat:
            if strict:
                return False
        elif cat.strip().lower() not in eligible_categories:
            return False

    # year level
    eligible_levels = []
    for raw in sch.get("eligible_year_levels") or []:
        try:
            eligible_levels.append(int(raw))
        except (TypeError, ValueError):
            continue
    if eligible_levels:
        current = profile.get("current_year_level")
        nxt = profile.get("next_year_level")
        if current is None and nxt is None:
            if strict:
                return False
        elif not any(int(v) in eligible_levels for v in (current, nxt) if v is not None):
            return False

    # enrollment status
    eligible_status = [str(x).strip().lower() for x in (sch.get("eligible_enrollment_status") or []) if x]
    status = (profile.get("enrollment_status") or "").strip().lower()
    if eligible_status:
        if not status:
            if strict:
                return False
        elif status not in eligible_status:
            return False

    # citizenship
    required_cit = (sch.get("citizenship_required") or "Filipino").strip().lower()
    if required_cit not in ("any", "none", "open", ""):
        pcit = (profile.get("citizenship") or "").strip().lower()
        if not pcit:
            if strict:
                return False
        elif pcit != required_cit:
            return False

    # income ceiling (a stated ceiling is a hard cap)
    ceil = sch.get("max_income_threshold")
    pinc = profile.get("household_income_annual")
    if ceil is not None:
        if pinc is None and not (profile.get("income_bracket") or "").strip():
            if strict:
                return False
        elif pinc is not None and pinc > ceil:
            return False

    # GWA minimum
    mingwa = sch.get("min_gwa_normalized")
    pgwa = profile.get("gwa_normalized")
    if mingwa is not None:
        if pgwa is None:
            if strict:
                return False
        elif pgwa < mingwa:
            return False

    # field of study
    if not _field_eligible(profile, sch, unknown_policy=unknown_policy):
        return False

    # exclusive priority groups (members-only)
    if sch.get("members_only"):
        groups = sch.get("priority_groups") or []
        member = False
        for g in groups:
            flag = _PRIORITY_GROUP_TO_FLAG.get(g)
            if flag and profile.get(flag):
                member = True
                break
        if not member:
            return False

    return True
