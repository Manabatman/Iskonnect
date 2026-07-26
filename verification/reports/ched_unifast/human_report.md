# CHED + UniFAST + BPMSP Verification Report

**Bundle:** `ched_unifast`  
**Verified at:** 2026-07-09  
**Scholarship IDs:** 1, 5, 6, 19, 76  
**Official domains checked:** ched.gov.ph, legacy.ched.gov.ph, unifast.gov.ph, bpms.ched.gov.ph

## Executive summary

Five records verified against official sources. **3 require substantive corrections**, **1 should be archived** (discontinued transition program), **1 is largely accurate** (BPMSP). Link checker over-flagged broken URLs; several official pages resolve on `legacy.ched.gov.ph` or `unifast.gov.ph/tes.html`.

| ID | Title | Verdict | Priority |
|----|-------|---------|----------|
| 1 | CHED Merit Scholarship Program | Correct URL, GWA, income, benefits, exam flags | High |
| 5 | CHED-Tulong Dulong Program | **Rename to TDP; reassign to UniFAST; fix benefits** | High |
| 6 | UniFAST Tertiary Education Subsidy | Fix benefit amounts and cycle; clarify HEI-based application | Normal |
| 19 | CHED K-12 Transition Scholarship | **Archive — program discontinued; wrong description** | High |
| 76 | BPMSP Higher Education Track | Confirm eligibility/benefits; fix link status | Normal |

## Per-scholarship findings

### ID 1 — CHED Merit Scholarship Program (CMSP)

- **Status:** Recurring program; AY 2025-2026 applications **closed** (deadline 20 June 2025). Keep active; `expected_reopen` appropriate.
- **Key corrections:** Primary link → `https://legacy.ched.gov.ph/merit-scholarship/`; min GWA 93%; income ceiling PhP500,000; max annual benefit PhP120,000 (private full); remove qualifying exam flag.
- **Evidence:** [legacy.ched.gov.ph/merit-scholarship](https://legacy.ched.gov.ph/merit-scholarship/)

### ID 5 — Tulong Dunong Program (mislabeled)

- **Status:** Active UniFAST program under TES umbrella.
- **Key corrections:** Fix title typo; change provider to UniFAST; link to TES page; benefit PhP15,000/AY (not PhP60,000); update documents and description.
- **Evidence:** [unifast.gov.ph/tes.html](https://unifast.gov.ph/tes.html)

### ID 6 — UniFAST Tertiary Education Subsidy (TES)

- **Status:** Ongoing grant-in-aid; application via HEI UniFAST focal person when call is issued.
- **Key corrections:** Benefit PhP20,000/AY (SUC/LUC) or PhP27,000/AY (private); set `cycle_type` annual; remove monthly allowance semantics.
- **Evidence:** [unifast.gov.ph/tes.html](https://unifast.gov.ph/tes.html)

### ID 19 — CHED K-12 Transition Scholarship

- **Status:** **Permanently discontinued.** Transition graduate scholarships for HEI personnel closed AY 2017-2018; K-12 transition period ended SY 2020-2021.
- **Action:** Archive (`is_active=false`); closure type `permanently_discontinued`. Current title/description are incorrect.
- **Evidence:** [legacy.ched.gov.ph/k-12-project-management-unit](https://legacy.ched.gov.ph/k-12-project-management-unit/), [chedk12.wordpress.com/sgs](https://chedk12.wordpress.com/sgs/)

### ID 76 — BPMSP Higher Education Track

- **Status:** Active national program (GAA FY 2026; JMC No. 1 s. 2026). Portal at bpms.ched.gov.ph operational.
- **Key corrections:** Clear broken link flag; confirm 95% GWA / PhP2M income / return service. Application dates for next cycle not confirmed in official FAQ — flagged for review.
- **Evidence:** [bpms.ched.gov.ph](https://bpms.ched.gov.ph/), [BPMSP FAQ PDF](https://caraga.ched.gov.ph/wp-content/uploads/2026/05/BPMSP_FAQ_0428.pdf)

## Missing programs discovered

1. **Free Higher Education (RA 10931)** — distinct from TES cash grant  
2. **Student Loan Program (SLPTE-ST)** — listed on UniFAST; applications currently suspended pending guideline review

TDP already in catalog as id 5 (needs relabeling, not duplicate entry).

## Human review flags

- **ID 19:** Confirm archive — do not treat as seasonal closure.  
- **ID 5 vs 6:** Ensure UI/search distinguishes TDP (fixed PhP7,500/sem, income ceiling, no concurrent StuFAPs) from TES (prioritized grant).  
- **ID 76 application dates:** Stored 2026-04-30 to 2026-06-30 not verified in official FAQ; confirm before displaying as open.

## Deliverables

| File | Status |
|------|--------|
| field_changes.csv | 47 rows |
| new_scholarships.json | 2 candidates |
| schema_candidates.json | 5 patterns |
| important_notes.json | 5 records |
| human_report.md | Complete |

**Next bundle:** `dost`
