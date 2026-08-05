# Report contradictions and source hygiene

**Generated:** 2026-08-05

Do not guess when sources disagree. Resolve with Tier-1 official source or manual review.

---

## Filename vs document body

| File name | Document title / body | Action |
|-----------|----------------------|--------|
| `DATABASE_V1_GROUPA.pdf` | Group **B** exhaustive audits (MSRS, GSIS, CoScho, QCSP) | Use body content; ignore filename |
| `DATABASE_V2_GROUPB.pdf` | Group **A** programs (DOST, BPMSP, Megaworld, SM) | Use body content; ignore filename |

---

## Live catalog vs report canonical values

| Topic | Report / canonical | Live DB | Resolution |
|-------|-------------------|---------|------------|
| MSRS income (#54) | ₱450,000 | ₱600,000 | Remediate to 450k |
| DOST Grad umbrella (#3) | Uncapped income; host GWA | max_income=500k; min_gwa=88 | Null both; route to child IDs 133–136 |
| Megaworld income (#61) | ₱400,000 (portal) | ₱400,000 | OK (legacy 300k superseded) |
| GSP benefits (#7) | ~₱60k/yr; ₱2k/mo stipend | May show higher totals | Fix benefit display fields |
| QCSP GWA (#88) | Multi-track: 1.75 / 2.50 / 3.00 | Single min_gwa≈88 | Needs track subtypes or split records |
| JLSS year (#130) | Apply as Y2; funding from Y3 | `eligible_year_levels` ambiguous vs [3] | Model application year vs award start |
| DOST UG enrollment (#73) | Never entered college / unenrolled | enroll includes `enrolled` + max_units=0 | Clarify zero-unit enrolled vs prior college |
| BPMSP vs CMSP (#76 vs #1) | Different GWA/income; CMSP weighted 70/30 | Separate rows; CMSP score not modeled | Keep two records; add scoring later |

---

## Internal implementation conflicts

| Topic | Conflict | Preferred architecture |
|-------|----------|------------------------|
| GSIS GSP (#7) | `members_only` + GSIS Dependent **and** affiliation model | Affiliations as source of truth; deprecate duplicate members_only over time |
| Public field evidence | Admin/research snippets on student detail | Student strip only; admin endpoint for evidence |
| GATE_* off | Data backfilled but evaluators return N/A | Temporary affiliation fallback when codes present |
