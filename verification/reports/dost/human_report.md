# DOST-SEI Verification Report

**Bundle:** `dost`  
**Verified at:** 2026-07-09  
**Scholarship IDs:** 2, 3  
**Official domains checked:** science-scholarships.ph, ugrad.science-scholarships.ph, jlss.science-scholarships.ph, sei.dost.gov.ph

## Executive summary

Two records verified. **Undergraduate scholarship (id 2)** is active with fixable URL and benefit corrections. **Graduate scholarship (id 3)** is an oversimplified umbrella record that should be split or flagged — DOST-SEI operates multiple distinct graduate programs.

| ID | Title | Verdict | Priority |
|----|-------|---------|----------|
| 2 | DOST-SEI Undergraduate Scholarship | Fix portal URL, benefits, dates, income/GWA flags | High |
| 3 | DOST-SEI Graduate Scholarship | **Flag for restructuring** — conflates ASTHRDP/CBPSME/ERDT/STRAND | High |

## Per-scholarship findings

### ID 2 — DOST-SEI S&T Undergraduate Scholarships

- **Status:** Recurring annual program. Recent cycle closed 23 Dec 2024; qualifying exam Apr 5-6, 2025. Keep active with `expected_reopen`.
- **Key corrections:**
  - Primary link: `https://ugrad.science-scholarships.ph` (not `ugs.science-scholarships.ph`)
  - Monthly living allowance: PhP8,000 (not PhP7,000)
  - Total benefit value significantly higher than stored PhP120,000 when all allowances included
  - Income ceiling PhP400,000 applies only to RA 7687 track, not Merit track
  - Min GWA 92 not confirmed on official portal — flag for review
- **Evidence:** [science-scholarships.ph](https://www.science-scholarships.ph/), [2026 Application Form J PDF](https://www.science-scholarships.ph/pdf/forms/2026%20DOST-SEI%20S&T%20Undergraduate%20Application%20Form%20J.pdf)

### ID 3 — DOST-SEI Graduate Scholarship (generic)

- **Status:** Graduate programs remain active but are **not a single scholarship**. Official portal lists ASTHRDP, CBPSME, ERDT, STRAND, Foreign Graduate, and UAlberta programs separately.
- **Key corrections:**
  - Update description to reflect multi-program structure
  - Fix link status (portal works)
  - Benefit values cannot be verified as uniform PhP200,000 / PhP15,000 monthly
  - Application dates vary by university — stored single dates are unsupported
- **Recommended action:** `flag_review` — split into program-specific catalog entries or link id 3 as hub record
- **Evidence:** [science-scholarships.ph](https://www.science-scholarships.ph/), [ASTHRDP Brochure PDF](https://science-scholarships.ph/pdf/2025_ASTHRDP_Brochure.pdf)

## Missing programs discovered

1. **JLSS** — active; may exist archived in catalog (verify archived_reference bundle)  
2. **ASTHRDP** — separate graduate MS/PhD program  
3. **ERDT** — engineering graduate program  
4. **CBPSME** — science/math education graduate program  
5. **STRAND** — regional STEM graduate program  
6. **Separate Merit vs RA 7687 undergraduate tracks** — optional split from id 2

## Human review flags

- **ID 2:** Consider splitting Merit and RA 7687 into separate searchable records with different income rules.  
- **ID 3:** Do not apply uniform benefit/date fields; restructure before next import.  
- **Archived JLSS:** Confirm whether archived catalog entries duplicate JLSS before adding new record.

## Deliverables

| File | Status |
|------|--------|
| field_changes.csv | 28 rows |
| new_scholarships.json | 6 candidates |
| schema_candidates.json | 5 patterns |
| important_notes.json | 2 records |
| human_report.md | Complete |

**Pilot complete.** Remaining 13 bundles pending review before continuation.
