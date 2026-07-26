"""
Canonical registry of Philippine Higher Education Institutions (HEIs).

PHILIPPINE_SCHOOLS remains a sorted list of canonical names for backward-compatible autocomplete.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, TypedDict


class SchoolEntry(TypedDict):
    id: str
    canonical_name: str
    aliases: list[str]
    system_id: str | None
    category: str
    region: str | None


def _slug(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _entry(
    canonical_name: str,
    *,
    aliases: list[str] | None = None,
    system_id: str | None = None,
    category: str = "private",
    region: str | None = None,
    entry_id: str | None = None,
) -> SchoolEntry:
    sid = entry_id or _slug(canonical_name)
    alias_set = {canonical_name}
    if aliases:
        alias_set.update(aliases)
    return {
        "id": sid,
        "canonical_name": canonical_name,
        "aliases": sorted(alias_set - {canonical_name}, key=str.lower),
        "system_id": system_id,
        "category": category,
        "region": region,
    }


# --- School systems (referenced by system_id) ---
SCHOOL_SYSTEMS: dict[str, str] = {
    "up-system": "University of the Philippines System",
    "ateneo-network": "Ateneo Network",
    "dlsu-system": "De La Salle Philippines",
    "pup-system": "Polytechnic University of the Philippines",
    "state-u-luzon": "Luzon State Universities",
}

# Registry keyed by canonical school id
SCHOOL_REGISTRY: dict[str, SchoolEntry] = {}

_RAW_ENTRIES: list[SchoolEntry] = [
    _entry("Polytechnic University of the Philippines", aliases=["PUP"], system_id="pup-system", category="SUC", region="NCR"),
    _entry("University of Santo Tomas", aliases=["UST"], category="private_sectarian", region="NCR"),
    _entry("Ateneo de Manila University", aliases=["Ateneo", "ADMU"], system_id="ateneo-network", category="private_sectarian", region="NCR"),
    _entry("De La Salle University", aliases=["DLSU", "La Salle"], system_id="dlsu-system", category="private", region="NCR"),
    _entry("University of the Philippines Diliman", aliases=["UP Diliman", "UPD"], system_id="up-system", category="SUC", region="NCR"),
    _entry("University of the Philippines Manila", aliases=["UP Manila", "UPM"], system_id="up-system", category="SUC", region="NCR"),
    _entry("University of the Philippines Los Baños", aliases=["UP Los Baños", "UPLB"], system_id="up-system", category="SUC", region="Region IV-A - Calabarzon"),
    _entry("University of the Philippines Baguio", aliases=["UP Baguio"], system_id="up-system", category="SUC", region="CAR"),
    _entry("University of the Philippines Cebu", aliases=["UP Cebu"], system_id="up-system", category="SUC", region="Region VII - Central Visayas"),
    _entry("University of the Philippines Mindanao", aliases=["UP Mindanao"], system_id="up-system", category="SUC", region="Region XI - Davao"),
    _entry("University of the Philippines Open University", aliases=["UPOU"], system_id="up-system", category="SUC", region="Region IV-A - Calabarzon"),
    _entry("University of the Philippines Visayas", aliases=["UP Visayas", "UPV"], system_id="up-system", category="SUC", region="Region VI - Western Visayas"),
    _entry("University of the Philippines Tacloban", system_id="up-system", category="SUC", region="Region VIII - Eastern Visayas"),
    _entry("Pamantasan ng Lungsod ng Maynila", aliases=["PLM"], category="LUC", region="NCR"),
    _entry("Adamson University", category="private_sectarian", region="NCR"),
    _entry("Ateneo de Davao University", system_id="ateneo-network", category="private_sectarian", region="Region XI - Davao"),
    _entry("Ateneo de Naga University", system_id="ateneo-network", category="private_sectarian", region="Region V - Bicol"),
    _entry("Ateneo de Zamboanga University", system_id="ateneo-network", category="private_sectarian", region="Region IX - Zamboanga Peninsula"),
    _entry("Bicol University", category="SUC", region="Region V - Bicol"),
    _entry("Bulacan State University", aliases=["BulSU"], category="SUC", region="Region III - Central Luzon"),
    _entry("Cagayan State University", category="SUC", region="Region II - Cagayan Valley"),
    _entry("Central Luzon State University", aliases=["CLSU"], category="SUC", region="Region III - Central Luzon"),
    _entry("Central Philippine University", category="private_sectarian", region="Region VI - Western Visayas"),
    _entry("Centro Escolar University", aliases=["CEU"], category="private", region="NCR"),
    _entry("De La Salle-College of Saint Benilde", aliases=["CSB", "Benilde"], system_id="dlsu-system", category="private", region="NCR"),
    _entry("Don Mariano Marcos Memorial State University", category="SUC", region="Region I - Ilocos"),
    _entry("Far Eastern University", aliases=["FEU"], category="private", region="NCR"),
    _entry("Holy Angel University", category="private_sectarian", region="Region III - Central Luzon"),
    _entry("Ifugao State University", category="SUC", region="CAR"),
    _entry("Ilocos Sur Polytechnic State College", category="SUC", region="Region I - Ilocos"),
    _entry("Isabela State University", category="SUC", region="Region II - Cagayan Valley"),
    _entry("Jose Rizal University", aliases=["JRU"], category="private", region="NCR"),
    _entry("La Consolacion College Manila", category="private_sectarian", region="NCR"),
    _entry("La Salle University", system_id="dlsu-system", category="private", region="Region X - Northern Mindanao"),
    _entry("Lyceum of the Philippines University", aliases=["LPU"], category="private", region="NCR"),
    _entry("Mapua University", category="private", region="NCR"),
    _entry("Mariano Marcos State University", aliases=["MMSU"], category="SUC", region="Region I - Ilocos"),
    _entry("Mindanao State University", aliases=["MSU"], category="SUC", region="BARMM"),
    _entry("National University", category="private", region="NCR"),
    _entry("Negros Oriental State University", category="SUC", region="Region VII - Central Visayas"),
    _entry("Pangasinan State University", category="SUC", region="Region I - Ilocos"),
    _entry("Philippine Normal University", aliases=["PNU"], category="SUC", region="NCR"),
    _entry("Rizal Technological University", aliases=["RTU"], category="SUC", region="NCR"),
    _entry("San Beda University", category="private_sectarian", region="NCR"),
    _entry("San Sebastian College-Recoletos", category="private_sectarian", region="NCR"),
    _entry("Silliman University", category="private_sectarian", region="Region VII - Central Visayas"),
    _entry("Southern Luzon State University", category="SUC", region="Region IV-A - Calabarzon"),
    _entry("St. Louis University", aliases=["SLU Baguio"], category="private_sectarian", region="CAR"),
    _entry("St. Paul University Philippines", category="private_sectarian", region="Region II - Cagayan Valley"),
    _entry("Technological University of the Philippines", aliases=["TUP"], category="SUC", region="NCR"),
    _entry("University of Batangas", category="private", region="Region IV-A - Calabarzon"),
    _entry("University of Cebu", category="private", region="Region VII - Central Visayas"),
    _entry("University of Eastern Philippines", category="SUC", region="Region V - Bicol"),
    _entry("University of Mindanao", category="private", region="Region XI - Davao"),
    _entry("University of Negros Occidental-Recoletos", category="private_sectarian", region="Region VI - Western Visayas"),
    _entry("University of Northern Philippines", category="SUC", region="Region I - Ilocos"),
    _entry("University of Perpetual Help System DALTA", category="private", region="NCR"),
    _entry("University of San Carlos", category="private_sectarian", region="Region VII - Central Visayas"),
    _entry("University of the Cordilleras", category="private", region="CAR"),
    _entry("University of the East", aliases=["UE"], category="private", region="NCR"),
    _entry("University of the Philippines Iloilo", system_id="up-system", category="SUC", region="Region VI - Western Visayas"),
    _entry("University of the Philippines Visayas Tacloban College", system_id="up-system", category="SUC", region="Region VIII - Eastern Visayas"),
    _entry("University of the Philippines Visayas Miag-ao", system_id="up-system", category="SUC", region="Region VI - Western Visayas"),
    _entry("University of the Philippines Visayas Iloilo City", system_id="up-system", category="SUC", region="Region VI - Western Visayas"),
    _entry("Virgen Milagrosa University Foundation", category="private", region="Region I - Ilocos"),
    _entry("Visayas State University", category="SUC", region="Region VIII - Eastern Visayas"),
    _entry("Western Mindanao State University", category="SUC", region="Region IX - Zamboanga Peninsula"),
    _entry("Xavier University - Ateneo de Cagayan", aliases=["XU"], system_id="ateneo-network", category="private_sectarian", region="Region X - Northern Mindanao"),
    _entry("Arellano University", category="private", region="NCR"),
    _entry("Asian Institute of Management", aliases=["AIM"], category="private", region="NCR"),
    _entry("Asian Institute of Maritime Studies", category="private", region="NCR"),
    _entry("Assumption College", category="private_sectarian", region="NCR"),
    _entry("Bataan Peninsula State University", category="SUC", region="Region III - Central Luzon"),
    _entry("Batangas State University", aliases=["BatSU"], category="SUC", region="Region IV-A - Calabarzon"),
    _entry("Benguet State University", category="SUC", region="CAR"),
    _entry("Cavite State University", category="SUC", region="Region IV-A - Calabarzon"),
    _entry("Central Bicol State University of Agriculture", category="SUC", region="Region V - Bicol"),
    _entry("Central Mindanao University", category="SUC", region="Region X - Northern Mindanao"),
    _entry("Colegio de San Juan de Letran", category="private_sectarian", region="NCR"),
    _entry("Colegio de San Lorenzo", category="private_sectarian", region="NCR"),
    _entry("Don Honorio Ventura State University", category="SUC", region="Region III - Central Luzon"),
    _entry("Emilio Aguinaldo College", category="private", region="NCR"),
    _entry("Eulogio Amang Rodriguez Institute of Science and Technology", aliases=["EARIST"], category="SUC", region="NCR"),
    _entry("Father Saturnino Urios University", category="private_sectarian", region="Region XIII - Caraga"),
    _entry("FEU Institute of Technology", aliases=["FEU Tech"], category="private", region="NCR"),
    _entry("Filipino Academy of Cinematic Arts", category="private", region="NCR"),
    _entry("Holy Cross of Davao College", category="private_sectarian", region="Region XI - Davao"),
    _entry("International Academy of Management and Economics", category="private", region="NCR"),
    _entry("Jose Maria College", category="private", region="Region XI - Davao"),
    _entry("Laguna State Polytechnic University", category="SUC", region="Region IV-A - Calabarzon"),
    _entry("Leyte Normal University", category="SUC", region="Region VIII - Eastern Visayas"),
    _entry("Manuel L. Quezon University", aliases=["MLQU"], category="private", region="NCR"),
    _entry("Marikina Polytechnic College", category="technical", region="NCR"),
    _entry("Mindanao University of Science and Technology", category="SUC", region="Region X - Northern Mindanao"),
    _entry("Miriam College", category="private_sectarian", region="NCR"),
    _entry("New Era University", category="private_sectarian", region="NCR"),
    _entry("Northwestern University", category="private", region="Region I - Ilocos"),
    _entry("Notre Dame of Marbel University", category="private_sectarian", region="Region XII - SOCCSKSARGEN"),
    _entry("Palawan State University", category="SUC", region="MIMAROPA"),
    _entry("Partido State University", category="SUC", region="Region V - Bicol"),
    _entry("Philippine Christian University", category="private_sectarian", region="NCR"),
    _entry("Philippine Women's University", aliases=["PWU"], category="private", region="NCR"),
    _entry("Ramon Magsaysay Memorial Colleges", category="private", region="Region XII - SOCCSKSARGEN"),
    _entry("Saint Louis College", category="private_sectarian", region="Region I - Ilocos"),
    _entry("Saint Mary's University", category="private_sectarian", region="Region II - Cagayan Valley"),
    _entry("San Pedro College", category="private_sectarian", region="Region XI - Davao"),
    _entry("Sorsogon State University", category="SUC", region="Region V - Bicol"),
    _entry("Surigao del Norte State University", category="SUC", region="Region XIII - Caraga"),
    _entry("Tarlac Agricultural University", category="SUC", region="Region III - Central Luzon"),
    _entry("Tarlac State University", category="SUC", region="Region III - Central Luzon"),
    _entry("Technological Institute of the Philippines", aliases=["TIP"], category="private", region="NCR"),
    _entry("University of Asia and the Pacific", aliases=["UA&P"], category="private", region="NCR"),
    _entry("University of Makati", aliases=["UMAK"], category="LUC", region="NCR"),
    _entry("University of Manila", category="private", region="NCR"),
    _entry("University of Nueva Caceres", category="private", region="Region V - Bicol"),
    _entry("University of Pangasinan", category="private", region="Region I - Ilocos"),
    _entry("University of San Jose-Recoletos", category="private_sectarian", region="Region VII - Central Visayas"),
    _entry("University of Science and Technology of Southern Philippines", aliases=["USTP"], category="SUC", region="Region X - Northern Mindanao"),
    _entry("University of Southern Mindanao", category="SUC", region="Region XII - SOCCSKSARGEN"),
    _entry("University of Southeastern Philippines", category="SUC", region="Region XI - Davao"),
    _entry("University of the Assumption", category="private_sectarian", region="Region III - Central Luzon"),
    _entry("University of the Immaculate Conception", category="private_sectarian", region="Region XI - Davao"),
    _entry("West Visayas State University", category="SUC", region="Region VI - Western Visayas"),
    _entry("Zamboanga State College of Marine Sciences and Technology", category="SUC", region="Region IX - Zamboanga Peninsula"),
]

for _school in _RAW_ENTRIES:
    SCHOOL_REGISTRY[_school["id"]] = _school

# Backward-compatible export: sorted unique canonical names
PHILIPPINE_SCHOOLS: list[str] = sorted({e["canonical_name"] for e in SCHOOL_REGISTRY.values()})


def get_school_entry(school_id: str | None) -> SchoolEntry | None:
    if not school_id:
        return None
    return SCHOOL_REGISTRY.get(str(school_id).strip())


def school_category_for_profile(profile: dict[str, Any]) -> str | None:
    """Resolve HEI category from profile school_id or school name."""
    from app.taxonomy.school_registry import resolve_school_id

    sid = profile.get("school_id") or resolve_school_id(profile.get("school"))
    entry = get_school_entry(sid)
    return entry["category"] if entry else None
