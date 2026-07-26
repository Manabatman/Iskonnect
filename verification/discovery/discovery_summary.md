# Scholarship Discovery Summary

**Verification date:** 2026-07-09  
**Source:** Deep Research PDF — *Database Integration and Structural Mapping of the Philippine Higher Education Scholarship Ecosystem*  
**Method:** Candidate list from research → live Supabase dedup → official-source verification → classification

---

## Totals

| Metric | Count |
|--------|------:|
| **Total research candidates** | 29 |
| **Already in ISKONNECT** | 9 |
| **New scholarships approved** | 12 |
| **Rejected (not a scholarship / out of scope)** | 4 |
| **Programs requiring manual review** | 6 |
| **Duplicate / variant candidates** | 6 |
| **Records with missing metadata fields** | 5 |

---

## Classification breakdown

### Add immediately (12) → `validated_new_scholarships.json`

| # | Program | Confidence |
|---|---------|------------|
| 1 | CHED CoScho | verified |
| 2 | CHED SIDA-SGP | verified |
| 3 | CHED Estatistikolar | verified |
| 4 | CHED SIKAP (Graduate/Faculty) | verified |
| 5 | DOST JLSS — Merit Track | verified |
| 6 | DOST JLSS — RA 7687 Track | verified |
| 7 | DOST JLSS — RA 10612 Track | verified |
| 8 | OWWA ELAP | verified |
| 9 | Shell–PhilDev Scholarship | partially_verified |
| 10 | Iskolar ng LANDBANK | partially_verified ⚠ human review |
| 11 | UNILAB Foundation Educational Grant (Silliman) | partially_verified ⚠ human review |
| 12 | Analog Devices Academe Linkage | partially_verified ⚠ human review |

### Already exists (9) → `existing_scholarships.csv`

| Research candidate | ISKONNECT id | Notes |
|--------------------|-------------|-------|
| SM Foundation College | 10 | Verified; update cycle dates |
| Megaworld Foundation | 61 | Verified; SY 2024-2025 closed |
| Security Bank Scholars for Better Communities | 71 | Verified; align branding |
| ACEF-GIAHEP | 55 | Partially verified; check PHEI track |
| OWWA EDSP | 85 | Archived — reactivate review |
| OWWA ODSP | 86 | Archived — reactivate review |
| OWWA CMWSP | 87 | Archived — reactivate review |
| CHED MSRS | 54 | **Misattributed to DOH — correct, do not duplicate** |
| DOST JLSS (umbrella) | 79 | **Split into 3 tracks; un-archive** |

### Needs manual review — variant of generic parent (5) → `duplicate_candidates.json`

| Research name | Generic parent id | Action |
|---------------|-------------------|--------|
| Aboitiz Brights | 75 | Confirm vs Future Leaders branding |
| Ayala U-Go Scholar Grant | 11 | Update or split from generic Ayala record |
| Metrobank ACCESS | 13 | Rename/enrich generic Metrobank record |
| BPI Pagpupugay | 14 | Split or replace generic BPI record |
| PLDT Gabay Guro | 16 | Update to Gabay Guro specifics |

Plus **MSRS/id 54** misattribution (duplicate_candidates.json).

### Rejected (4) → `rejected_candidates.json`

| Program | Reason |
|---------|--------|
| CHED HUSAY / CPDSG | Faculty CPD/training — not student scholarship |
| SDG-RDIG | Research grant for HEI consortia |
| PCARI | Faculty/research collaboration program |
| Foreign Scholarships (generic) | Out of scope without per-program verification |

---

## Research validation findings

### Outdated information in Deep Research

1. **Cycle dates:** PDF cites 2024–2025 JLSS and DOST UG windows. As of July 2026, do **not** carry forward stale dates. Approved new records leave `application_open_date` / `application_deadline` empty unless officially confirmed for next cycle.
2. **BPI Pagpupugay:** Official page still shows AY 2022-2023 deadline (June 24, 2022). Program exists but cycle metadata is stale — flag for re-verification before import.
3. **Megaworld:** Site announces SY 2024-2025 applications closed — research implied ongoing open status.

### Incorrect assumptions corrected

1. **MSRS provider:** Research correctly identifies CHED (RA 11509). ISKONNECT id **54** wrongly lists **DOH** as provider — must be corrected, not duplicated.
2. **JLSS consolidation:** Research correctly requires 3 legal tracks. ISKONNECT id **79** is a single archived umbrella — split into Merit / RA 7687 / RA 10612.
3. **Aboitiz Brights:** Could not confirm "Brights" branding on official site (503). id **75** uses "Future Leaders" — treat as naming variant pending site access.

### Missing scholarships the research overlooked

These were already identified in prior ISKONNECT verification passes and are **not** re-imported here:

- UniFAST Free Higher Education (RA 10931)
- UniFAST Student Loan Program (SLPTE-ST)
- DOST graduate programs (ASTHRDP, ERDT, CBPSME) — in `dost/new_scholarships.json`
- DOST UG Merit / RA 7687 split — in `dost/new_scholarships.json`

### Duplicate recommendations in research

- **ACEF-GIAHEP** recommended as new but **id 55** already exists.
- **OWWA EDSP/ODSP/CMWSP** exist as archived records (ids 85–87) — reactivate rather than create new.
- **MSRS** must not be added as new while id 54 exists.

### Discontinued / non-scholarship programs

- **HUSAY, SDG-RDIG, PCARI** confirmed on CHED legacy site as faculty/research programs — excluded from undergraduate matching engine per user decision.

### Renamed programs

- **Security Bank:** Official brand is "Scholars for Better Communities" with External/Internal/Agency sub-programs.
- **Aboitiz:** Official site uses "Future Leaders" not "Brights" (unconfirmed variant).

---

## Missing metadata (fields left empty / cannot_verify)

| Record | Missing fields |
|--------|----------------|
| CoScho, SIDA-SGP, Estatistikolar | National application portal URL (CHED RO-coordinated) |
| SIKAP | Contact email/phone; exact age cap from CMO |
| All JLSS tracks | 2026 cycle dates (not yet announced) |
| Shell-PhilDev | Income threshold; application portal; required documents |
| Iskolar ng LANDBANK | Official page content; 2026 cycle; partner SUC list |
| Unilab Silliman | Current MOA status; income/GWA thresholds |
| Analog Devices | Public portal (none by design); partner HEI full list |

---

## Additional scholarships discovered beyond PDF

| Program | Source | Note |
|---------|--------|------|
| CHED BPMSP HE Track | Already in DB (id 76) | Not in PDF candidate list |
| DOST UG Merit / RA 7687 split | science-scholarships.ph | Prior dost bundle report |
| UniFAST FHE / SLPTE | unifast.gov.ph | Prior ched_unifast report |

---

## Recommended next steps

1. **Human review** of 3 partially_verified additions (LANDBANK, Unilab, Analog Devices).
2. **Correct id 54** (MSRS provider/title) before any MSRS import.
3. **Split id 79** into 3 JLSS track records; un-archive.
4. **Reactivate** OWWA ids 85–87 after cycle verification.
5. **Resolve 5 variant duplicates** (update generic parent records vs split).
6. **Import** 12 approved records via admin staging after review.

---

## Output files

| File | Path |
|------|------|
| Schema | [verification/discovery/SCHEMA.md](SCHEMA.md) |
| New scholarships | [verification/discovery/validated_new_scholarships.json](validated_new_scholarships.json) |
| Existing matches | [verification/discovery/existing_scholarships.csv](existing_scholarships.csv) |
| Duplicate candidates | [verification/discovery/duplicate_candidates.json](duplicate_candidates.json) |
| Rejected | [verification/discovery/rejected_candidates.json](rejected_candidates.json) |
| This summary | [verification/discovery/discovery_summary.md](discovery_summary.md) |

**Guardrails observed:** Read-only Supabase; no production writes; official sources only; unconfirmed fields marked `cannot_verify` or left empty.
