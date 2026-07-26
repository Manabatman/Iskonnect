# ISKONNECT Database Quality Audit

**Audit date:** 2026-07-09  
**Source:** Live Supabase (`iskonnect-db`, read-only SELECT)  
**Scope:** Full `scholarships` table (91 records)

## Summary

| Metric | Count |
|--------|------:|
| Total scholarships | 91 |
| Active | 55 |
| Archived | 36 |
| Broken `link_status` | 31 |
| `data_status = broken_link` | 31 |
| `data_status = needs_review` | 2 |
| Missing `last_verified_at` | 0 |
| Duplicate titles (case-insensitive) | 0 |
| Invalid open > deadline dates | 0 |
| Outdated `academic_year_target` (< 2025-2026) | 0 |
| Active with all benefit fields null | 0 |
| Active missing `eligible_levels` or `description` | 0 |

## Findings

### 1. Broken or flagged links (high priority)

31 active records carry `link_status = broken` and `data_status = broken_link`. Many URLs are valid official domains but stored as homepage-only links, use deprecated paths (e.g. `ched.gov.ph/merit-scholarship` vs `legacy.ched.gov.ph/merit-scholarship`), or incorrect subdomains (e.g. `ugs.science-scholarships.ph` vs `ugrad.science-scholarships.ph`).

**Pilot bundle impact:** All 5 CHED/UniFAST records and both DOST records in this run are flagged broken except UniFAST TES (id 6, link ok).

**Recommendation:** Re-run link health check after URL corrections; distinguish HTTP failures from homepage-only URLs in `data_status`.

### 2. Duplicate URLs (shared primary_link)

| URL | Count | Scholarship IDs |
|-----|------:|-----------------|
| `https://www.ph.emb-japan.go.jp/itpr_en/00_000193.html` | 4 | 80, 81, 82, 83 |
| `https://tcu.edu.ph/lani-scholarship` | 4 | 27, 28, 29, 30 |
| `https://scholarship.owwa.gov.ph/` | 3 | 85, 86, 87 |
| `https://www.ateneo.edu` | 3 | 40, 41, 42 |
| `https://qceservices.quezoncity.gov.ph` | 2 | 88, 89 |
| `https://scholars.pasigcity.gov.ph` | 2 | 25, 26 |
| `https://www.dlsu.edu.ph` | 2 | 43, 44 |
| `https://www.gsis.gov.ph` | 2 | 78, 84 |
| `https://www.muntinlupacity.gov.ph` | 2 | 47, 48 |
| `https://www.pup.edu.ph/students/scholarships` | 2 | 68, 69 |
| `https://www.science-scholarships.ph/` | 2 | 73, 79 |
| `https://bpms.ched.gov.ph/` | 2 | 76, 77 |
| `https://www.studyinkorea.go.kr` | 2 | 64, 65 |
| `https://ched.gov.ph` | 2 | 5, 19 |
| `https://davaocity.gov.ph` | 2 | 37, 38 |
| `https://ncip.gov.ph` | 2 | 52, 53 |

Homepage-only duplicates (e.g. ids 5 and 19 both `ched.gov.ph`) often mask missing program-specific pages.

### 3. Application status distribution

| `application_status` | Count |
|----------------------|------:|
| `open` | 31 |
| `expected_reopen` | 3 |
| `previous_cycle` | 19 |

31 records marked `open` may overstate availability; several government programs (CMSP, DOST UG) are closed between cycles. Pilot verification recommends tightening status for seasonal programs.

### 4. Provider normalization

Multiple CHED-related provider strings exist: "Commission on Higher Education (CHED)", "Commission on Higher Education", "UniFAST / CHED", "Unified Student Financial Assistance System". DOST appears as both "Department of Science and Technology - SEI" and "DOST-SEI". Not blocking, but complicates search and bundle assignment.

### 5. Data integrity issues surfaced in pilot

| ID | Issue |
|----|-------|
| 5 | Title typo ("Tulong Dulong"); program is UniFAST Tulong Dunong (TDP), not standalone CHED |
| 19 | Title/description mismatch; K-12 Transition graduate scholarship closed; likely should be archived |
| 3 | Generic "Graduate Scholarship" conflates multiple DOST-SEI graduate programs (ASTHRDP, ERDT, etc.) |

### 6. Orphaned / missing provider websites

No scholarships have completely null `link` among active records. 31 have broken link flags pending re-verification.

### 7. PSCED / regions / eligibility

No active records with empty `eligible_levels` or empty `description`. Many government scholarships have empty `eligible_regions` (nationwide assumed)—acceptable but should be confirmed per program.

## Recommended follow-up (post-pilot)

1. Import URL and field corrections from `verification/reports/ched_unifast/field_changes.csv` and `verification/reports/dost/field_changes.csv` via admin staging.
2. Re-run automated link checker after URL updates.
3. Split or archive mislabeled records (ids 5, 19, 3) after human review.
4. Continue bundle verification for remaining 13 provider bundles.
