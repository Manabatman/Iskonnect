# Lesson 13 — Domain Taxonomies (Philippine Policy)

> **Prerequisite:** [12 — Scoring Engine Internals](12-scoring-engine-internals.md)

---

## Why domain modeling exists

Generic "scholarship matcher" fails in the Philippines because:

- GWA uses **multiple scales** (5.0, 4.0, percentage)
- Regions have **aliases** ("NCR", "Metro Manila")
- Laws define **priority groups** (PWD, IP, solo parent dependent)
- Courses map to **PSCED** taxonomy

Iskonnect encodes this in [`app/taxonomy/`](../../../app/taxonomy/) — not in routes.

---

## GWA normalization

[`gwa_normalizer.py`](../../../app/taxonomy/gwa_normalizer.py)

| Scale | Example raw | Normalized |
|-------|-------------|------------|
| 5.0_scale | 1.25 | ~96% equivalent |
| 4.0_scale | 3.5 | converted |
| percentage | 92 | 92 |

**Hardening:** Unknown scale + ambiguous value → `None` (not silent percentage default) — prevents mis-scoring 2.5 on 5.0 scale as 2.5%.

**Alias map:** `numeric_1_to_5` → `5.0_scale`, etc.

---

## Regions and provinces

[`regions.py`](../../../app/taxonomy/regions.py) — `normalize_region()` collapses aliases for matching.

[`provinces.py`](../../../app/taxonomy/provinces.py) — autocomplete for profile builder via [`suggestions.py`](../../../app/api/v1/suggestions.py).

**Current matching:** String/substring based. **Blueprint:** PSGC codes (migration 024 added `psgc_code` on students) for prefix matching (region=2 digits, etc.).

---

## PSCED fields

[`psced_fields.py`](../../../app/taxonomy/psced_fields.py) — `FIELD_HIERARCHY` links broad ↔ specific fields for match levels.

---

## Income brackets

[`income_brackets.py`](../../../app/taxonomy/income_brackets.py) — maps annual household income to bracket labels used in scoring and filters.

---

## Equity groups

[`equity_groups.py`](../../../app/taxonomy/equity_groups.py) — aligns profile flags with RA references (7277 PWD, 8371 IP, 11861 solo parent, etc.).

Profile columns on `students`: `is_pwd`, `is_indigenous_people`, `is_solo_parent_dependent`, `is_4ps_listahanan`, ...

Scholarship: `priority_groups` JSON list.

---

## Analogy

Taxonomies are the **dictionary** the matching engine speaks. Without them, "Region III" and "Central Luzon" are different planets.

---

## What breaks if taxonomies wrong?

- False positives: student sees ineligible scholarships
- False negatives: misses real matches
- Legal/policy misalignment for government programs

---

## Exercises

### Level 1 — Understanding

1. Why normalize GWA to comparable scale?
2. What is PSCED?

### Level 2 — Implementation

1. Call `normalize_region("NCR")` in Python REPL — record output.

### Level 3 — Debugging

1. Student GWA 2.5, scale missing — what should `gwa_normalized` be after hardening?

### Level 4 — Architecture

1. Plan PSGC backfill for existing students with only free-text `province`.

<details>
<summary>Solution</summary>

Scholarships compare min_gwa_normalized — need common unit. PSCED = Philippine Standard Classification of Education. Unknown scale → None + low confidence flag. Backfill: geocode script, nullable psgc_code, fuzzy match provinces.py, manual review queue for failures.
</details>

---

*Previous: [12 — Scoring](12-scoring-engine-internals.md) | Next: [14 — Redis, Cache & Rate Limiting](14-redis-cache-and-rate-limiting.md)*
