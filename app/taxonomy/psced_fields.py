"""
PSCED-aligned field-of-study taxonomy (DATA-01 / DATA-02 / B6).

Three levels: course alias -> normalized field -> broad discipline (+ sub-disciplines).
The ten legacy broad disciplines remain byte-identical.
"""

from __future__ import annotations

# Field hierarchy: child -> parent(s). Used for generous upward matching.
FIELD_HIERARCHY: dict[str, list[str]] = {
    "Engineering": ["STEM"],
    "IT": ["STEM"],
    "Science": ["STEM"],
    "Mathematics": ["STEM"],
    "Communication": ["Arts"],
    "Social Sciences": ["Arts"],
    "Tourism & Hospitality": ["Business"],
    "Maritime": ["Engineering"],
    "Aviation": ["Engineering"],
    "Sports Science": ["Education"],
}

# Broad disciplines (PSCED-aligned) - used for eligibility matching
PSCED_BROAD_DISCIPLINES: dict[str, str] = {
    "STEM": "Science, Technology, Engineering, Mathematics",
    "Engineering": "Engineering and Technology",
    "IT": "Information Technology",
    "Medical": "Medicine and Health Sciences",
    "Business": "Business and Accountancy",
    "Education": "Education and Teacher Training",
    "Agriculture": "Agriculture, Forestry, Fisheries",
    "Arts": "Arts and Humanities",
    "Law": "Law",
    "Architecture": "Architecture and Planning",
}

# Normalized field -> immediate parent (discipline or sub-discipline)
NORMALIZED_FIELDS: dict[str, str] = {}

# Course alias -> normalized field
COURSE_ALIASES: dict[str, str] = {}


def _register_fields(parent: str, fields: list[str]) -> None:
    for field in fields:
        NORMALIZED_FIELDS[field] = parent
        FIELD_HIERARCHY.setdefault(field, [parent])


def _register_aliases(mapping: dict[str, str]) -> None:
    for alias, field in mapping.items():
        COURSE_ALIASES[alias.strip().lower()] = field


# --- STEM sciences and mathematics (12) ---
_register_fields("STEM", [
    "Biology",
    "Chemistry",
    "Physics",
    "Mathematics",
    "Applied Mathematics",
    "Statistics",
    "Environmental Science",
    "Marine Biology",
    "Molecular Biology and Biotechnology",
    "Geology",
    "Meteorology",
    "Materials Science",
])

# --- IT (7) ---
_register_fields("IT", [
    "Computer Science",
    "Information Technology",
    "Information Systems",
    "Data Science",
    "Software Engineering",
    "Cybersecurity",
    "Game and Multimedia Development",
])

# --- Engineering (13) ---
_register_fields("Engineering", [
    "Civil Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Electronics Engineering",
    "Computer Engineering",
    "Chemical Engineering",
    "Industrial Engineering",
    "Geodetic Engineering",
    "Mining Engineering",
    "Metallurgical Engineering",
    "Sanitary Engineering",
    "Agricultural and Biosystems Engineering",
    "Aerospace Engineering",
])

# --- Medical and health sciences (14) ---
_register_fields("Medical", [
    "Medicine",
    "Nursing",
    "Pharmacy",
    "Medical Laboratory Science",
    "Physical Therapy",
    "Occupational Therapy",
    "Radiologic Technology",
    "Respiratory Therapy",
    "Midwifery",
    "Dentistry",
    "Optometry",
    "Veterinary Medicine",
    "Public Health",
    "Nutrition and Dietetics",
])

# --- Business and accountancy (13) ---
_register_fields("Business", [
    "Accountancy",
    "Management Accounting",
    "Business Administration",
    "Marketing Management",
    "Financial Management",
    "Human Resource Management",
    "Entrepreneurship",
    "Economics",
    "Office Administration",
    "Customs Administration",
    "Supply Chain and Logistics",
    "Business Analytics",
    "Real Estate Management",
])

# --- Tourism and hospitality sub-discipline (5) ---
_register_fields("Tourism & Hospitality", [
    "Tourism Management",
    "Hospitality Management",
    "Hotel and Restaurant Management",
    "Culinary Arts",
    "Travel Management",
])

# --- Education (8) ---
_register_fields("Education", [
    "Elementary Education",
    "Secondary Education",
    "Early Childhood Education",
    "Special Needs Education",
    "Physical Education",
    "Technology and Livelihood Education",
    "Guidance and Counseling",
    "Library and Information Science",
])

# --- Agriculture, forestry, fisheries (8) ---
_register_fields("Agriculture", [
    "Agribusiness",
    "Animal Science",
    "Crop Science",
    "Forestry",
    "Fisheries",
    "Food Science and Technology",
    "Agricultural Economics",
])
# "Agriculture" is both broad discipline and field name
NORMALIZED_FIELDS["Agriculture"] = "Agriculture"

# --- Arts and humanities (10) ---
_register_fields("Arts", [
    "Literature",
    "History",
    "Philosophy",
    "Languages and Linguistics",
    "Fine Arts",
    "Music",
    "Theater Arts",
    "Film and Media Arts",
    "Industrial Design",
    "Interior Design",
])

# --- Communication sub-discipline (6) ---
_register_fields("Communication", [
    "Journalism",
    "Broadcasting",
    "Communication Research",
    "Advertising",
    "Development Communication",
    "Communication Arts",
])

# --- Social sciences sub-discipline (9) ---
_register_fields("Social Sciences", [
    "Psychology",
    "Sociology",
    "Anthropology",
    "Political Science",
    "Public Administration",
    "Social Work",
    "Criminology",
    "International Studies",
    "Community Development",
])

# --- Law (2) ---
_register_fields("Law", [
    "Law",
    "Legal Management",
])

# --- Architecture and planning (3) ---
_register_fields("Architecture", [
    "Architecture",
    "Urban and Regional Planning",
    "Environmental Planning",
])

# --- Maritime sub-discipline (3) ---
_register_fields("Maritime", [
    "Marine Transportation",
    "Marine Engineering",
    "Naval Architecture",
])

# --- Aviation sub-discipline (2) ---
_register_fields("Aviation", [
    "Aeronautical Engineering",
    "Aircraft Maintenance Technology",
])

# --- Sports science sub-discipline (2) ---
_register_fields("Sports Science", [
    "Sports Science",
    "Exercise and Sports Sciences",
])

_register_aliases({
    "bsit": "Information Technology",
    "b.s. information technology": "Information Technology",
    "info tech": "Information Technology",
    "bs accountancy": "Accountancy",
    "bs nursing": "Nursing",
    "bs agriculture": "Agriculture",
    "bsdevcom": "Development Communication",
    "ba development communication": "Development Communication",
    "devcom": "Development Communication",
    "bs civil engineering": "Civil Engineering",
    "bs computer engineering": "Computer Engineering",
    "bs electronics engineering": "Electronics Engineering",
    "bs computer science": "Computer Science",
    "bs statistics": "Statistics",
    "bs applied statistics": "Statistics",
    "ba literature": "Literature",
    "welding nc ii": "Shielded Metal Arc Welding NC II",
    "doctor of medicine (md)": "Medicine",
    "doctor of medicine": "Medicine",
    "juris doctor (jd)": "Law",
    "juris doctor": "Law",
    "bachelor of advertising and public relations": "Advertising",
    "digital design": "Industrial Design",
    "performing arts": "Theater Arts",
    "agricultural engineering": "Agricultural and Biosystems Engineering",
    "agribusiness management": "Agribusiness",
    "agricultural mechanics": "Agriculture",
    "sugarcane technology": "Agriculture",
    "filipino language and literature": "Languages and Linguistics",
    "space science and technology applications": "Environmental Science",
})

# Legacy hierarchy-only codes promoted to selectable fields (pre-B6 drift)
_register_fields("STEM", ["Science"])

# Specific course names - sample mapping for detailed matching
PSCED_SPECIFIC_COURSES: dict[str, list[str]] = {
    "STEM": [
        "BS Biology",
        "BS Chemistry",
        "BS Physics",
        "BS Mathematics",
        "BS Statistics",
        "BS Computer Science",
        "BS Data Science",
    ],
    "Engineering": [
        "BS Civil Engineering",
        "BS Mechanical Engineering",
        "BS Electrical Engineering",
        "BS Electronics Engineering",
        "BS Chemical Engineering",
        "BS Geodetic Engineering",
        "BS Industrial Engineering",
        "BS Computer Engineering",
    ],
    "IT": [
        "BS Information Technology",
        "BS Information Systems",
        "BS Computer Science",
    ],
    "Medical": [
        "BS Nursing",
        "BS Medicine",
        "BS Pharmacy",
        "BS Medical Technology",
        "BS Physical Therapy",
    ],
    "Business": [
        "BS Business Administration",
        "BS Accountancy",
        "BS Internal Auditing",
        "BS Economics",
        "BS Marketing Management",
    ],
    "Education": [
        "BS Education",
        "BEED",
        "BSED",
        "BSE",
    ],
    "Agriculture": [
        "BS Agriculture",
        "BS Agricultural Engineering",
        "BS Forestry",
    ],
    "Arts": [
        "BA Communication",
        "BA Psychology",
        "BA Sociology",
        "BA Literature",
        "BA Development Communication",
    ],
    "Communication": [
        "BA Development Communication",
        "BA Journalism",
        "BA Broadcasting",
    ],
}


def _case_insensitive_hierarchy_key(field: str) -> str | None:
    if field in FIELD_HIERARCHY:
        return field
    lower = field.lower()
    for key in FIELD_HIERARCHY:
        if key.lower() == lower:
            return key
    return None


def resolve_normalized_field(field_or_alias: str | None) -> str | None:
    """Map free text or alias to a normalized field name."""
    if not field_or_alias or not str(field_or_alias).strip():
        return None
    raw = str(field_or_alias).strip()
    if raw in NORMALIZED_FIELDS:
        return raw
    alias = COURSE_ALIASES.get(raw.lower())
    if alias:
        return alias
    lower = raw.lower()
    for name in NORMALIZED_FIELDS:
        if name.lower() == lower:
            return name
    for broad in PSCED_BROAD_DISCIPLINES:
        if broad.lower() == lower:
            return broad
    return raw


def resolve_field_ancestors(field: str | None) -> list[str]:
    """Return normalized field and ancestors (lowercase), nearest first."""
    if not field or not str(field).strip():
        return []
    current = resolve_normalized_field(str(field).strip())
    if not current:
        return []
    chain: list[str] = []
    seen: set[str] = set()
    while current:
        norm = current.lower()
        if norm in seen:
            break
        seen.add(norm)
        chain.append(norm)
        key = _case_insensitive_hierarchy_key(current)
        if not key:
            break
        parents = FIELD_HIERARCHY.get(key) or []
        if not parents:
            break
        current = parents[0]
    return chain


def all_normalized_field_names() -> list[str]:
    names = set(NORMALIZED_FIELDS.keys()) | set(PSCED_BROAD_DISCIPLINES.keys())
    names.update({"Communication", "Social Sciences", "Tourism & Hospitality", "Maritime", "Aviation", "Sports Science"})
    return sorted(names)


def taxonomy_value_resolves(value: str | None) -> bool:
    """Return True when a stored profile or scholarship field value maps in this taxonomy."""
    if value is None or not str(value).strip():
        return True
    raw = str(value).strip()
    resolved = resolve_normalized_field(raw)
    known = {name.lower() for name in all_normalized_field_names()}
    if resolved and resolved.lower() in known:
        return True

    lower = raw.lower()
    open_phrases = (
        "all undergraduate",
        "all undergrad",
        "all courses",
        "all approved",
        "all available",
        "all accredited",
        "all standard",
        "all educational",
        "all university",
        "all umak",
        "all admu",
        "all ust",
        "board or bar",
        "master's and doctoral",
        "short term",
        "short courses",
        "tvet",
        "als and",
        "community livelihood",
        "priority fields",
        "priority s&t",
        "priority courses",
        "dost-sei",
        "ched tanyag",
        "top-tier",
        "top tier",
        "elite institutional",
        "high priority developmental",
        "european joint master",
        "suc and luc",
        "suc and lcu",
        "identified heis",
        "developmental tracks",
        "national courses",
        "degree programs",
        "degree courses",
        "college programs",
        "college courses",
        "college paths",
        "undergraduate paths",
        "undergraduate pathways",
        "undergraduate tracks",
        "undergraduate programs",
        "undergraduate offerings",
        "undergraduate majors",
        "undergraduate degrees",
        "undergraduate degree",
    )
    if any(phrase in lower for phrase in open_phrases):
        return True

    for name in all_normalized_field_names():
        if name.lower() in lower:
            return True
    return False


def build_fields_of_study_options() -> list[dict[str, object]]:
    """Grouped field-of-study options for profile-options API (DATA-04 / B8)."""
    groups: list[dict[str, object]] = []

    groups.append(
        {
            "label": "Broad disciplines",
            "options": [
                {"value": code, "label": label}
                for code, label in PSCED_BROAD_DISCIPLINES.items()
            ],
        }
    )

    sub_disciplines = [
        "Communication",
        "Social Sciences",
        "Tourism & Hospitality",
        "Maritime",
        "Aviation",
        "Sports Science",
    ]
    for sub in sub_disciplines:
        fields = sorted(f for f, parent in NORMALIZED_FIELDS.items() if parent == sub)
        if fields:
            groups.append(
                {
                    "label": sub,
                    "options": [{"value": name, "label": name} for name in fields],
                }
            )

    for broad in LEGACY_BROAD_DISCIPLINES:
        fields = sorted(
            f
            for f, parent in NORMALIZED_FIELDS.items()
            if parent == broad and f not in PSCED_BROAD_DISCIPLINES
        )
        if fields:
            groups.append(
                {
                    "label": f"{broad} fields",
                    "options": [{"value": name, "label": name} for name in fields],
                }
            )

    return groups


LEGACY_BROAD_DISCIPLINES = (
    "STEM",
    "Engineering",
    "IT",
    "Medical",
    "Business",
    "Education",
    "Agriculture",
    "Arts",
    "Law",
    "Architecture",
)
