"""Provider bundle assignment for external verification conversations."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Manual overrides: scholarship id -> bundle id
ID_OVERRIDES: dict[int, str] = {
    6: "ched_unifast",  # UniFAST TES
    56: "military_affiliation",  # AFPEBSO DND CHED PASUC (title contains CHED)
    76: "ched_unifast",  # BPMSP HE track
    77: "tesda",  # BPMSP TVET track
    91: "international",  # Chevening
}

_MILITARY_PATTERNS = (
    r"armed forces",
    r"\bafp",
    r"afpslai",
    r"afpebso",
    r"afpeebso",
)


@dataclass(frozen=True)
class BundleDefinition:
    bundle_id: str
    title: str
    conversation_order: int
    official_domains: tuple[str, ...]
    missing_search_targets: tuple[str, ...] = ()
    archived_note: str = ""
    provider_patterns: tuple[str, ...] = field(default_factory=tuple)


BUNDLE_DEFINITIONS: tuple[BundleDefinition, ...] = (
    BundleDefinition(
        "ched_unifast",
        "CHED + UniFAST + BPMSP (Higher Education)",
        1,
        ("ched.gov.ph", "unifast.gov.ph", "bpms.ched.gov.ph"),
        (
            "CHED Merit Scholarship Program (current cycle)",
            "UniFAST Tertiary Education Subsidy (TES)",
            "Tulong Dunong Program (TDP)",
            "Bagong Pilipinas Merit Scholarship Program (BPMSP) HE track",
        ),
        "Verify archived CHED/K-12 variants — confirm superseded or still offered.",
        (r"commission on higher education", r"\bched\b", r"unifast", r"unified student financial"),
    ),
    BundleDefinition(
        "dost",
        "DOST-SEI",
        2,
        ("science-scholarships.ph", "sei.dost.gov.ph", "dost.gov.ph"),
        (
            "DOST-SEI Undergraduate (RA 7687 and Merit tracks)",
            "DOST-SEI Junior Level Science Scholarship (JLSS)",
            "DOST-SEI Graduate Scholarship",
        ),
        "JLSS and RA 7687/Merit may be archived — verify current offering status.",
        (r"department of science and technology", r"\bdost\b", r"\bsei\b"),
    ),
    BundleDefinition(
        "tesda",
        "TESDA + BPMSP (TVET)",
        3,
        ("tesda.gov.ph", "bpms.ched.gov.ph"),
        ("TESDA scholarship programs (specific brands beyond homepage)", "BPMSP TVET track"),
        provider_patterns=(r"tesda", r"technical education and skills"),
    ),
    BundleDefinition(
        "gsis_sss",
        "GSIS + SSS",
        4,
        ("gsis.gov.ph", "sss.gov.ph"),
        (
            "GSIS Educational Subsidy Program (GESP)",
            "GSIS Subsidy for STEM Program (GSSP)",
            "SSS educational assistance / loan programs",
        ),
        provider_patterns=(r"gsis", r"government service insurance", r"social security system", r"\bsss\b"),
    ),
    BundleDefinition(
        "owwa_dswd_ncip",
        "OWWA + DSWD + NCIP",
        5,
        ("owwa.gov.ph", "dswd.gov.ph", "ncip.gov.ph"),
        (
            "OWWA EDSP / Education and Training programs",
            "DSWD AICS educational assistance",
            "NCIP educational assistance programs",
        ),
        provider_patterns=(
            r"overseas workers welfare",
            r"\bowwa\b",
            r"social welfare and development",
            r"\bdswd\b",
            r"indigenous peoples",
            r"\bncip\b",
        ),
    ),
    BundleDefinition(
        "other_government",
        "Other national government programs",
        11,
        ("deped.gov.ph", "da.gov.ph", "erc.gov.ph", "energy.gov.ph"),
        ("DepEd SHS Voucher", "DA ACEF programs", "ERC graduate fellowships"),
        provider_patterns=(
            r"department of education",
            r"\bdeped\b",
            r"department of agriculture",
            r"energy regulatory",
            r"\berc\b",
        ),
    ),
    BundleDefinition(
        "military_affiliation",
        "Military / uniformed service affiliation",
        6,
        ("afpslai.com.ph", "afpebso.org", "afp.mil.ph"),
        ("AFPSLAI Educational Grant", "AFPEBSO DND CHED PASUC", "PVAO educational benefits"),
        provider_patterns=(r"armed forces", r"\bafp", r"afpslai", r"afpebso", r"afpeebso"),
    ),
    BundleDefinition(
        "sm_foundation",
        "SM Foundation",
        10,
        ("sm-foundation.org", "smfoundation.org"),
        ("SM Foundation college scholarship", "SM tech-voc scholarship tracks"),
        provider_patterns=(r"sm foundation",),
    ),
    BundleDefinition(
        "megaworld_foundation",
        "Megaworld Foundation",
        10,
        ("megaworldfoundation.com", "megaworldcorp.com"),
        ("Megaworld Foundation partner university scholarships"),
        provider_patterns=(r"megaworld foundation",),
    ),
    BundleDefinition(
        "private_foundations",
        "Private foundations (corporate)",
        9,
        (
            "aboitiz.com",
            "ayalafoundation.org",
            "bpifoundation.org",
            "caritasmanila.org.ph",
            "metrobank-foundation.org",
            "pldtsmartfoundation.org",
            "sanmiguel.com.ph",
            "securitybank.com",
        ),
        (
            "Aboitiz Future Leaders",
            "Ayala Foundation scholarships",
            "BPI Foundation",
            "Metrobank Foundation",
            "PLDT-Smart Foundation",
            "San Miguel Foundation",
        ),
        provider_patterns=(
            r"foundation",
            r"aboitiz",
            r"ayala",
            r"\bbpi\b",
            r"caritas",
            r"metrobank",
            r"pldt",
            r"san miguel",
            r"security bank",
        ),
    ),
    BundleDefinition(
        "lgu_ncr",
        "LGU — NCR",
        7,
        (
            "pasigcity.gov.ph",
            "scholars.pasigcity.gov.ph",
            "taguig.gov.ph",
            "tcu.edu.ph",
            "makati.gov.ph",
            "quezoncity.gov.ph",
            "qceservices.quezoncity.gov.ph",
            "valenzuela.gov.ph",
            "muntinlupacity.gov.ph",
            "navotas.gov.ph",
            "paranaquecity.gov.ph",
        ),
        (
            "Manila city scholarship programs",
            "Caloocan LGU scholarships",
            "Las Piñas LGU scholarships",
        ),
        provider_patterns=(
            r"pasig",
            r"taguig",
            r"makati",
            r"quezon city",
            r"valenzuela",
            r"muntinlupa",
            r"navotas",
            r"parañaque",
            r"paranaque",
        ),
    ),
    BundleDefinition(
        "lgu_provincial",
        "LGU — provincial / outside NCR",
        11,
        ("cebu.gov.ph", "bislig.gov.ph", "tabuk.gov.ph"),
        ("Provincial scholarship programs not yet in catalog"),
        provider_patterns=(r"provincial government", r"provincial", r"city government"),
    ),
    BundleDefinition(
        "universities",
        "Universities and colleges",
        8,
        ("up.edu.ph", "ateneo.edu", "ust.edu.ph", "pup.edu.ph", "pnu.edu.ph", "dlsu.edu.ph"),
        (
            "UP System scholarship grants",
            "Ateneo financial aid programs",
            "DLSU scholarship programs",
            "UST grant types beyond equity scholarship",
        ),
        provider_patterns=(r"university", r"\bup\b", r"ateneo", r"ust", r"\bpup\b", r"normal university", r"\bcollege\b"),
    ),
    BundleDefinition(
        "international",
        "International scholarships",
        12,
        ("erasmus-plus.ec.europa.eu", "chevening.org", "studyinkorea.go.kr", "jasso.go.jp"),
        ("JASSO", "MEXT", "Australia Awards", "Fulbright Philippines"),
        provider_patterns=(r"european union", r"erasmus", r"chevening", r"uk government", r"fcdo", r"embassy of"),
    ),
    BundleDefinition(
        "archived_reference",
        "Archived / historical reference",
        13,
        (),
        ("Programs marked inactive — confirm discontinued vs seasonal archive mistake"),
    ),
)

_BUNDLE_BY_ID = {b.bundle_id: b for b in BUNDLE_DEFINITIONS}


def _norm(text: str | None) -> str:
    return (text or "").strip().lower()


def assign_verification_bundle(row: Any) -> str:
    """Return bundle id for a scholarship ORM row or dict."""
    sid = getattr(row, "id", None) if not isinstance(row, dict) else row.get("id")
    if sid is not None and int(sid) in ID_OVERRIDES:
        return ID_OVERRIDES[int(sid)]

    is_active = getattr(row, "is_active", True) if not isinstance(row, dict) else row.get("is_active")
    if is_active is False:
        return "archived_reference"

    provider = _norm(getattr(row, "provider", None) if not isinstance(row, dict) else row.get("provider"))
    provider_type = _norm(
        getattr(row, "provider_type", None) if not isinstance(row, dict) else row.get("provider_type")
    )
    title = _norm(getattr(row, "title", None) if not isinstance(row, dict) else row.get("title"))

    haystack = f"{provider} {title}"

    for pattern in _MILITARY_PATTERNS:
        if re.search(pattern, haystack):
            return "military_affiliation"

    # LGU NCR before generic LGU provincial
    for bundle in BUNDLE_DEFINITIONS:
        if bundle.bundle_id == "archived_reference":
            continue
        if bundle.bundle_id == "lgu_provincial" and provider_type == "lgu":
            ncr_markers = ("pasig", "taguig", "makati", "quezon", "valenzuela", "muntinlupa", "navotas", "para")
            if any(m in haystack for m in ncr_markers):
                continue
            return "lgu_provincial"
        for pattern in bundle.provider_patterns:
            if re.search(pattern, haystack):
                if bundle.bundle_id == "private_foundations":
                    if any(x in haystack for x in ("sm foundation", "megaworld foundation")):
                        continue
                if bundle.bundle_id == "universities" and provider_type == "lgu":
                    continue
                return bundle.bundle_id

    if provider_type == "lgu":
        return "lgu_provincial"
    if provider_type == "institutional":
        return "universities"
    if provider_type == "government":
        return "other_government"
    if provider_type == "private":
        return "private_foundations"
    return "private_foundations"


def get_bundle_definition(bundle_id: str) -> BundleDefinition | None:
    return _BUNDLE_BY_ID.get(bundle_id)


def ordered_bundle_ids(*, include_archived: bool = True) -> list[str]:
    bundles = sorted(BUNDLE_DEFINITIONS, key=lambda b: b.conversation_order)
    ids = [b.bundle_id for b in bundles]
    if not include_archived:
        ids = [i for i in ids if i != "archived_reference"]
    return ids
