# ISKONNECT Source Knowledge Base (V1–V3 Verification Reports)

**Generated:** 2026-08-05  
**Sources:** `verification/DATABASE_V1_GROUPA.pdf` through `DATABASE_V3_GROUPC_*.pdf`  
**Group C per-scholarship cards:** [`verification/export/groupc_by_pdf/`](../../export/groupc_by_pdf/)  
**Machine index:** [`knowledge_base_index.json`](knowledge_base_index.json)

---

## KB-A. Stage / academic model (V2 protocol)

Reports define a three-stage eligibility pipeline:

1. **Stage 1:** `year_level` ∈ `eligible_year_levels`; `incoming_year_only` ⇒ zero tertiary units; enrollment vs `requires_current_enrollment`.
2. **Stage 2:** `(gwa >= minimum_gwa) OR (class_rank <= rank_cutoff)`; income ≤ limit.
3. **Stage 3:** partner school + priority course checks.

### Report-recommended DDL (not all adopted)

| Report field | Code equivalent today |
|--------------|----------------------|
| `incoming_year_only` | `max_prior_tertiary_units=0` + `eligible_enrollment_status` |
| `requires_current_enrollment` | `eligible_enrollment_status` includes `enrolled` |
| `first_time_only` | `first_undergraduate_only` |
| `rank_cutoff_alternative` | `max_class_rank` + `academic_gate_mode=or` |
| `partner_school_restricted` | `eligible_schools` non-empty |
| `renewal_gwa` | **Not implemented** (renewal out of matching scope) |
| `parent_employment_restriction` | `max_parent_salary_grade` + affiliations |
| `sectoral_restriction` | `required_affiliation_codes` |
| `lgu_exclusivity_clause` | `conflict_scope_codes` includes `lgu_grant` |
| `return_service_required` | `has_return_service` (display; not hard gate) |
| `gender_restriction` | **Not implemented** (profile `gender` exists) |

---

## KB-B. Critical provider rule cards

Verified against live Supabase + report text. Full Group C detail in linked JSON/MD per PDF.

| ID | Provider | Report hard rules | Live status |
|----|----------|-------------------|-------------|
| 73 | DOST UG | Natural-born; RA7687 residency ≥4y; zero college units; STEM or top-5% non-STEM; Merit vs RA7687 income split; qualifying exam | units=0, residency=4, conflict `national_stufap`; gwa=92; enroll includes `enrolled`; no natural-born / top5% OR |
| 130 | JLSS | Apply Y2 / fund Y3; GWA≥83; no fails; priority S&T; **must be active** | **`is_active=false`**; empty structured fields |
| 76 | BPMSP HE | Incoming; 0 units; top5 OR GWA≥95; income≤2M | Data correct (OR mode, rank=5); `GATE_ACADEMIC_OR` off |
| 1 | CMSP | GWA≥93; income≤500k; weighted score 70/30 | gwa/income OK; no weighted score |
| 61 | Megaworld | Y1–3; GWA≥85; income≤400k; partner schools | gwa/income OK; **partners empty** |
| 10 | SM Foundation | Incoming; 0 units; GWA≥92; income≤250k; partner + priority courses; public/voucher SHS | units=0; **partners empty** |
| 54 | MSRS | Med Y1–4; income≤450k; return service; no other RS grant | income **600k** (wrong); conflict stufap |
| 78 | GSIS GSSP | GSIS parent SG≤15; SHS GWA≥90; STEM; incoming Y1 only | affiliation `gsis_member`; **max_parent_sg null** |
| 84 | GSIS GESP | GSIS dependent subsidy | affiliation `gsis_member`; gate off → N/A |
| 7 | GSIS GSP | members_only GSIS; age≤21; income≤500k; GWA≥80 | members_only + GSIS Dependent (parallel to affiliations) |
| 117 | CoScho | NCFRS; income≤300k; agriculture; no other gov scholarship | ncfrs + conflict present |
| 88/89 | QCSP | QCitizen; multi-track GWA; no other LGU grant | `lgu_grant` conflict; single GWA field |
| 16 | Gabay Guro | BEED/BSED; partner SUCs; teaching service | courses **STEM/Engineering (wrong)** |
| 14 | Pagpupugay | Medical frontliner dependent | no affiliation; broad STEM courses |
| 81/65 | MEXT/GKS | Abroad destination; age_as_of birthdate | age_as_of set; **countries empty** |
| 74/90/91 | Aus/Fulbright/Chevening | work_exp≥2; host country | work_exp=2; countries empty; gate off |
| 3/133–136 | DOST Grad | Consortium; sectoral faculty; uncapped income | 133/134 schools OK; **#3 wrong income/gwa** |
| 119 | Estatistikolar | BS Statistics only | courses=STEM (too broad) |
| 120 | SIKAP | HEI faculty only | priority_groups only; no hei_faculty join |
| 11 | Ayala U-Go | Female + SUC/LUC | no gender evaluator |

---

## KB-C. Cross-cutting rule classes

| Rule class | Report coverage | Engine status |
|------------|-----------------|---------------|
| Affiliations (ncfrs, gsis_member, sra, hei_faculty, …) | V1/V3 sectoral | Schema + seeds; **gated off** |
| Conflict scopes (national_stufap, lgu_grant) | V1/V3 | Partial assignments; **gated off** |
| Destination / host country | V3 International | **`countries` unused in matching** |
| Consortium schools | V2/V3 DOST Grad, Megaworld, SM, Gabay | Partial backfill |
| Renewal (GWA, no fails, full load) | All PDFs | **Not in matching** (by design) |
| Application timing / cycles | All PDFs | temporal_state + application_status |
| Natural-born citizenship | DOST UG/JLSS | Coarse Filipino only |
| Explanation wording | — | eligibility_explanation.py; new keys need copy when gates on |

---

## KB-D. Source document map

| PDF file | Actual content | Scholarship count (Group C extract) |
|----------|----------------|-----------------------------------|
| DATABASE_V1_GROUPA.pdf | Group B: MSRS, GSIS, CoScho, QCSP | — (see V2 for Group A IDs list) |
| DATABASE_V2_GROUPB.pdf | Group A: DOST, BPMSP, Megaworld, SM | — |
| DATABASE_V3_GROUPC_DOST_GRADUATE.pdf | DOST grad 3, 133–136 | 5 |
| DATABASE_V3_GROUPC_INTERNATIONAL.pdf | MEXT, GKS, Fulbright, etc. | 11 |
| DATABASE_V3_GROUPC_LGU_PART1.pdf | NCR LGU tracks | 18 |
| DATABASE_V3_GROUPC_LGU_PART2.pdf | Pasig, Cebu, Davao, QC | 16 |
| DATABASE_V3_GROUPC_OTHER_GOVERNMENT.pdf | GSIS, OWWA, TESDA, etc. | 15 |
| DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P1.pdf | Gabay Guro, Pagpupugay, GBF, … | 7 |
| DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P2.pdf | Security Bank, Caritas, … | 7 |
| DATABASE_V3_GROUPC_UNIFAST_CHED.pdf | TDP, TES, SIDA, Estatistikolar, SIKAP | 5 |
| DATABASE_V3_GROUPC_UNNIVERSITIES.pdf | UP, Ateneo, DLSU, UST, … | 19 |

**Total Group C extracted records:** 103 (see `knowledge_base_index.json`).
