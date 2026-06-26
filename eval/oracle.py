"""
Independent eligibility oracle for the Iskonnect matching engine evaluation.

This encodes how a competent scholarship administrator would judge eligibility.
It does NOT import the engine's hard_filters; region normalization, level
bucketing, and field bridging are implemented here independently so the oracle
represents *correct* behaviour rather than the engine's behaviour.

Guiding principle (per the brief): missing a scholarship is worse than an extra
one, so when STUDENT data is missing we give the benefit of the doubt (eligible).
Scholarship restrictions that are present are enforced.
"""

from __future__ import annotations

# --- Region normalization (independent of engine) ---
_REGION_ALIASES = {
    "ncr": "ncr", "metro manila": "ncr", "national capital region": "ncr",
    "barmm": "barmm", "bangsamoro": "barmm",
    "car": "car", "cordillera": "car",
    "calabarzon": "region iv-a - calabarzon", "region iv-a - calabarzon": "region iv-a - calabarzon",
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


# --- Field taxonomy (independent, with broad<->specific bridge) ---
_PARENTS = {"engineering": ["stem"], "it": ["stem"], "science": ["stem"], "mathematics": ["stem"]}
_SPECIFIC_BY_BROAD = {
    "stem": ["bs biology", "bs chemistry", "bs physics", "bs mathematics", "bs computer science"],
    "engineering": ["bs civil engineering", "bs mechanical engineering", "bs electrical engineering"],
    "it": ["bs information technology", "bs computer science", "bs information systems"],
    "medical": ["bs nursing", "bs medicine", "bs pharmacy", "bs medical technology"],
    "business": ["bs accountancy", "bs business administration", "bs economics"],
    "education": ["beed", "bsed", "bs education"],
    "agriculture": ["bs agriculture", "bs forestry"],
    "arts": ["ba communication", "ba psychology", "ab political science"],
    "architecture": ["bs architecture"],
    "science": ["bs biology", "bs chemistry", "bs physics"],
    "mathematics": ["bs mathematics"],
    "humss": ["ab political science", "ab communication"],
    "tvl": ["cookery nc ii"],
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


def _field_eligible(profile: dict, sch: dict) -> bool:
    restr_psced = {str(c).strip().lower() for c in (sch.get("eligible_courses_psced") or []) if c}
    restr_spec = {str(c).strip().lower() for c in (sch.get("eligible_courses_specific") or []) if c}
    if not restr_psced and not restr_spec:
        return True
    broad = (profile.get("field_of_study_broad") or "").strip().lower()
    prefs = [str(p).strip().lower() for p in (profile.get("preferred_courses") or []) if p]
    spec = (profile.get("field_of_study_specific") or "").strip().lower()
    if spec:
        prefs.append(spec)
    if not broad and not prefs:
        return True  # no field data -> benefit of the doubt

    disc = set()
    if broad:
        disc.add(broad)
        disc.update(_PARENTS.get(broad, []))
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


def is_eligible(profile: dict, sch: dict) -> bool:
    """Return True if the admin would consider the student eligible for the scholarship."""
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

    # education level
    levels = [str(x).strip().lower() for x in (sch.get("eligible_levels") or []) if x]
    plevel = _bucket(profile.get("education_level") or profile.get("current_academic_stage"))
    if levels and plevel is not None:
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
        # residency-required city grants need a verifiable location
        if not matched:
            return False

    # school type
    est = [str(x).strip().lower() for x in (sch.get("eligible_school_types") or []) if x]
    pst = (profile.get("school_type") or "").strip().lower()
    if est and pst:
        if pst not in est:
            return False

    # income ceiling (a stated ceiling is a hard cap)
    ceil = sch.get("max_income_threshold")
    pinc = profile.get("household_income_annual")
    if ceil is not None and pinc is not None:
        if pinc > ceil:
            return False

    # GWA minimum
    mingwa = sch.get("min_gwa_normalized")
    pgwa = profile.get("gwa_normalized")
    if mingwa is not None and pgwa is not None:
        if pgwa < mingwa:
            return False

    # field of study
    if not _field_eligible(profile, sch):
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
