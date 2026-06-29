"""
Synthetic evaluation dataset generator for the Iskonnect matching engine.

Produces 100 realistic Filipino student profiles and 200 realistic scholarship
records. Generation is deterministic (seeded) so runs are reproducible.

The same dict fields are consumed by both the engine and the independent oracle
(eval/oracle.py); ground-truth attributes that the engine does NOT read are
prefixed with ``gt_`` so they can never leak into engine inputs.
"""

from __future__ import annotations

import random
from datetime import date, timedelta

SEED = 20260625

# Region strings as a STUDENT would actually type them (aliases included).
# Scholarships, by contrast, are stored with canonical region names.
REGION_STUDENT_VARIANTS = {
    "NCR": ["NCR", "Metro Manila", "National Capital Region"],
    "BARMM": ["BARMM", "Bangsamoro"],
    "CAR": ["CAR", "Cordillera"],
    "Region IV-A - Calabarzon": ["Calabarzon", "Region IV-A - Calabarzon"],
    "Region VII - Central Visayas": ["Central Visayas", "Region VII - Central Visayas"],
    "Region XI - Davao": ["Davao", "Davao Region", "Region XI - Davao"],
    "Region III - Central Luzon": ["Central Luzon", "Region III - Central Luzon"],
    "Region VI - Western Visayas": ["Western Visayas", "Region VI - Western Visayas"],
}
CANONICAL_REGIONS = list(REGION_STUDENT_VARIANTS.keys())

CITY_BY_REGION = {
    "NCR": "Quezon City",
    "BARMM": "Cotabato City",
    "CAR": "Baguio City",
    "Region IV-A - Calabarzon": "Calamba",
    "Region VII - Central Visayas": "Cebu City",
    "Region XI - Davao": "Davao City",
    "Region III - Central Luzon": "Angeles City",
    "Region VI - Western Visayas": "Iloilo City",
}

# Field of study (broad). HUMSS / TVL deliberately included even though the
# engine taxonomy (FIELD_HIERARCHY / PSCED) does not model them as STEM children.
FIELDS = [
    ("Engineering", "BS Civil Engineering"),
    ("IT", "BS Information Technology"),
    ("Science", "BS Biology"),
    ("Mathematics", "BS Mathematics"),
    ("Medical", "BS Nursing"),
    ("Business", "BS Accountancy"),
    ("Education", "BEED"),
    ("Agriculture", "BS Agriculture"),
    ("Arts", "BA Communication"),
    ("Architecture", "BS Architecture"),
    ("HUMSS", "AB Political Science"),
    ("TVL", "Cookery NC II"),
]

# education_level is constrained by schemas.EducationLevel to these canonical values.
# current_academic_stage is free-form (granular) but the SQL prefilter ignores it.
LEVEL_GROUPS = {
    "College": {"education_level": ["College"], "stage": ["College 1st Year", "College 2nd Year", "College 3rd Year"]},
    "Senior High": {"education_level": ["Grade 11", "Grade 12", "High School"], "stage": ["Senior High School"]},
    "TVET": {"education_level": ["TVET"], "stage": ["Vocational"]},
}


def _pick_level(rng, group):
    g = LEVEL_GROUPS[group]
    return rng.choice(g["education_level"]), rng.choice(g["stage"])

SCHOOL_TYPES = ["Public", "Private"]

EQUITY_FLAG_FIELDS = [
    "is_pwd",
    "is_indigenous_people",
    "is_underprivileged",
    "is_solo_parent_dependent",
    "is_ofw_dependent",
    "is_farmer_fisher_dependent",
    "is_4ps_listahanan",
]

PRIORITY_GROUP_TO_FLAG = {
    "PWD": "is_pwd",
    "IP": "is_indigenous_people",
    "Underprivileged": "is_underprivileged",
    "Solo Parent Dependent": "is_solo_parent_dependent",
    "OFW Dependent": "is_ofw_dependent",
    "Farmer/Fisher Dependent": "is_farmer_fisher_dependent",
    "4Ps/Listahanan": "is_4ps_listahanan",
}
PRIORITY_GROUPS = list(PRIORITY_GROUP_TO_FLAG.keys())


def _empty_equity() -> dict:
    return {k: False for k in EQUITY_FLAG_FIELDS}


def generate_profiles() -> list[dict]:
    rng = random.Random(SEED)
    profiles: list[dict] = []
    pid = 0

    def add(p: dict) -> None:
        nonlocal pid
        pid += 1
        p["id"] = pid
        # ensure all equity flags present
        for k in EQUITY_FLAG_FIELDS:
            p.setdefault(k, False)
        profiles.append(p)

    # --- 1. Coverage matrix: region x field x level (guarantees diversity) ---
    for region in CANONICAL_REGIONS:
        for (fb, fs) in FIELDS:
            variant = rng.choice(REGION_STUDENT_VARIANTS[region])
            if fb in ("HUMSS", "TVL") and rng.random() < 0.5:
                level_group = "Senior High"
            else:
                level_group = rng.choice(["College", "College", "Senior High"])
            level, stage = _pick_level(rng, level_group)
            income = rng.choice([120_000, 180_000, 300_000, 450_000, 700_000])
            gwa = rng.choice([78.0, 83.0, 88.0, 92.0, 96.0])
            school = rng.choice(SCHOOL_TYPES)
            p = {
                "age": rng.choice([16, 17, 18, 19, 20, 21, 22]),
                "education_level": level,
                "current_academic_stage": stage,
                "region": variant,
                "city_municipality": CITY_BY_REGION[region],
                "school_type": school,
                "household_income_annual": income,
                "income_bracket": None,
                "gwa_normalized": gwa,
                "gwa_raw": str(gwa),
                "field_of_study_broad": fb,
                "field_of_study_specific": fs,
                "preferred_courses": [fs],
                "needs": [],
                **_empty_equity(),
                "gt_region_canonical": region,
            }
            add(p)
            if len(profiles) >= 96:
                break
        if len(profiles) >= 96:
            break

    # --- 2. Priority-group students (explicit) ---
    for grp in PRIORITY_GROUPS:
        flag = PRIORITY_GROUP_TO_FLAG[grp]
        region = rng.choice(CANONICAL_REGIONS)
        fb, fs = rng.choice(FIELDS)
        eq = _empty_equity()
        eq[flag] = True
        add({
            "age": 19,
            "education_level": "College",
            "current_academic_stage": "College",
            "region": rng.choice(REGION_STUDENT_VARIANTS[region]),
            "city_municipality": CITY_BY_REGION[region],
            "school_type": "Public",
            "household_income_annual": 110_000,
            "income_bracket": None,
            "gwa_normalized": 86.0,
            "gwa_raw": "86.0",
            "field_of_study_broad": fb,
            "field_of_study_specific": fs,
            "preferred_courses": [fs],
            "needs": [],
            **eq,
            "gt_region_canonical": region,
        })

    # --- 3. Incomplete profiles (sparse data) ---
    for _ in range(4):
        region = rng.choice(CANONICAL_REGIONS)
        add({
            "age": None,
            "education_level": None,
            "current_academic_stage": None,
            "region": rng.choice(REGION_STUDENT_VARIANTS[region]),
            "city_municipality": None,
            "school_type": None,
            "household_income_annual": None,
            "income_bracket": None,
            "gwa_normalized": None,
            "gwa_raw": None,
            "field_of_study_broad": None,
            "field_of_study_specific": None,
            "preferred_courses": [],
            "needs": [],
            **_empty_equity(),
            "gt_region_canonical": region,
        })

    # --- 4. Edge personas that target known engine risks ---
    # Architecture student (substring 'it' in 'architecture' risk)
    add({
        "age": 20, "education_level": "College", "current_academic_stage": "College",
        "region": "Metro Manila", "city_municipality": "Quezon City", "school_type": "Private",
        "household_income_annual": 600_000, "income_bracket": None,
        "gwa_normalized": 90.0, "gwa_raw": "90.0",
        "field_of_study_broad": "Architecture", "field_of_study_specific": "BS Architecture",
        "preferred_courses": ["BS Architecture"], "needs": [],
        **_empty_equity(), "gt_region_canonical": "NCR",
    })
    # Medical broad-only student, no preferred courses (broad-vs-specific FN risk)
    add({
        "age": 19, "education_level": "College", "current_academic_stage": "College",
        "region": "Davao", "city_municipality": "Davao City", "school_type": "Public",
        "household_income_annual": 150_000, "income_bracket": None,
        "gwa_normalized": 89.0, "gwa_raw": "89.0",
        "field_of_study_broad": "Medical", "field_of_study_specific": None,
        "preferred_courses": [], "needs": [],
        **_empty_equity(), "gt_region_canonical": "Region XI - Davao",
    })

    return profiles[:100]


def generate_scholarships() -> list[dict]:
    rng = random.Random(SEED + 1)
    sch: list[dict] = []
    sid = 0
    today = date.today()
    future = (today + timedelta(days=120)).isoformat()
    past = (today - timedelta(days=30)).isoformat()

    def add(s: dict) -> None:
        nonlocal sid
        sid += 1
        s["id"] = sid
        s.setdefault("is_active", True)
        s.setdefault("data_status", "active")
        s.setdefault("application_deadline", future)
        s.setdefault("residency_required", False)
        s.setdefault("scholarship_type", "Merit-and-Need")
        # members_only: exclusive priority scholarships (hard-filtered when True)
        s.setdefault("members_only", False)
        sch.append(s)

    # --- A. Nationwide generic (no restrictions) ---
    for i in range(30):
        st = rng.choice(["Merit-based", "Need", "Merit-and-Need"])
        add({
            "title": f"Nationwide Grant {i+1}", "provider": f"Foundation {i+1}",
            "scholarship_type": st,
            "eligible_levels": rng.choice([[], ["College"], ["College", "Senior High School"]]),
            "max_income_threshold": None if st == "Merit-based" else rng.choice([400_000, 500_000]),
            "min_gwa_normalized": rng.choice([None, 80.0, 85.0]),
        })

    # --- B. Region-restricted (stored CANONICAL; students may type aliases) ---
    for region in CANONICAL_REGIONS:
        for k in range(4):
            add({
                "title": f"{region} Scholars {k+1}", "provider": f"{region} Office",
                "scholarship_type": "Need",
                "eligible_regions": [region],
                "eligible_levels": ["College"],
                "max_income_threshold": 500_000,
                "min_gwa_normalized": rng.choice([None, 82.0]),
            })

    # --- C. Field-restricted via PSCED broad codes ---
    for code in ["STEM", "IT", "Medical", "Business", "Education", "Agriculture", "Arts", "Engineering"]:
        for k in range(3):
            add({
                "title": f"{code} Excellence {k+1}", "provider": f"{code} Council",
                "scholarship_type": rng.choice(["Merit-based", "Merit-and-Need"]),
                "eligible_courses_psced": [code],
                "eligible_levels": ["College"],
                "min_gwa_normalized": rng.choice([None, 85.0, 88.0]),
            })

    # --- D. Field-restricted via SPECIFIC courses only (no PSCED) ---
    for course in ["BS Nursing", "BS Civil Engineering", "BS Accountancy", "BEED", "BS Agriculture", "BS Biology"]:
        add({
            "title": f"{course} Award", "provider": "Specific Course Trust",
            "scholarship_type": "Merit-and-Need",
            "eligible_courses_specific": [course],
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- E. Level-restricted with EXACT 'College' (subtype-profile FN risk on SQL path) ---
    for k in range(6):
        add({
            "title": f"College-Only Fund {k+1}", "provider": "Tertiary Trust",
            "scholarship_type": "Need",
            "eligible_levels": ["College"],
            "max_income_threshold": 400_000,
        })
    # Realistic mix of how senior-high eligibility is stored across sources.
    _sh_tag_variants = [["Senior High School"], ["Grade 11", "Grade 12"], ["High School"], ["Senior High"]]
    for k in range(4):
        add({
            "title": f"Senior High Bridge {k+1}", "provider": "K12 Foundation",
            "scholarship_type": "Need",
            "eligible_levels": _sh_tag_variants[k % len(_sh_tag_variants)],
            "max_income_threshold": 400_000,
        })
    for k in range(2):
        add({
            "title": f"TVET Skills Grant {k+1}", "provider": "TESDA Partner",
            "scholarship_type": "Need",
            "eligible_levels": ["TVET"],
            "max_income_threshold": 400_000,
        })

    # --- F. Income-ceiling need-based (varying ceilings) ---
    for ceil in [250_000, 400_000, 500_000]:
        for k in range(4):
            add({
                "title": f"Need {ceil//1000}k Fund {k+1}", "provider": "UniFAST-like",
                "scholarship_type": "Need",
                "max_income_threshold": ceil,
                "eligible_levels": ["College"],
            })

    # --- G. Merit (high GWA, no income) ---
    for k in range(8):
        add({
            "title": f"Academic Merit {k+1}", "provider": "Merit Board",
            "scholarship_type": "Merit-based",
            "min_gwa_normalized": rng.choice([88.0, 90.0, 92.0]),
            "eligible_levels": ["College"],
        })

    # --- H. School-type restricted ---
    for stype in ["Public", "Private"]:
        for k in range(3):
            add({
                "title": f"{stype} School Grant {k+1}", "provider": f"{stype} Schools Assoc",
                "scholarship_type": "Need",
                "eligible_school_types": [stype],
                "eligible_levels": ["College"],
                "max_income_threshold": 500_000,
            })

    # --- I. Priority-group EXCLUSIVE (members-only) ---
    for grp in PRIORITY_GROUPS:
        add({
            "title": f"{grp} Exclusive Scholarship", "provider": f"{grp} Federation",
            "scholarship_type": "Need",
            "priority_groups": [grp],
            "members_only": True,
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- J. Priority-group PREFERENTIAL (open, just prioritized) ---
    for grp in rng.sample(PRIORITY_GROUPS, 4):
        add({
            "title": f"{grp} Preferred Grant", "provider": f"{grp} Trust",
            "scholarship_type": "Need",
            "priority_groups": [grp],
            "members_only": False,
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- K. LGU city-specific ---
    for region, city in list(CITY_BY_REGION.items())[:5]:
        add({
            "title": f"{city} LGU Scholarship", "provider": f"{city} Government",
            "scholarship_type": "Need",
            "eligible_cities": [city],
            "residency_required": True,
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- L. Age-restricted ---
    for k in range(3):
        add({
            "title": f"Youth Grant {k+1}", "provider": "Youth Council",
            "scholarship_type": "Need",
            "min_age": 18, "max_age": 21,
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- M. Deadline-passed (eligible but closed) for ranking test ---
    for k in range(6):
        add({
            "title": f"Closed Cycle Grant {k+1}", "provider": "Past Foundation",
            "scholarship_type": "Need",
            "application_deadline": past,
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })

    # --- N. Incomplete / scraper-damaged records ---
    for k in range(6):
        add({
            "title": f"Partial Record {k+1}", "provider": None,
            "scholarship_type": rng.choice([None, "Merit-and-Need"]),
            "eligible_levels": rng.choice([None, []]),
        })

    # Pad to 200 with more nationwide generics if needed
    i = 0
    while len(sch) < 200:
        add({
            "title": f"Extra Nationwide {i+1}", "provider": f"Extra {i+1}",
            "scholarship_type": "Merit-and-Need",
            "eligible_levels": ["College"],
            "max_income_threshold": 500_000,
        })
        i += 1

    return sch[:200]


if __name__ == "__main__":
    ps = generate_profiles()
    ss = generate_scholarships()
    print(f"profiles={len(ps)} scholarships={len(ss)}")
