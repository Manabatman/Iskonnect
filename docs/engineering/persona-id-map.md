# Persona ID map — Refinement PR-nn ↔ shipped slugs

**Task:** A2 (Phase 4 Track A) · **B5 complete:** 2026-08-01  
**Authority:** Refinement §14.4 defines PR-01…PR-41; CI uses **slug `id`** values in `persona_catalog.json`. The additive `pr_ids` field links each shipped persona to Refinement intent without renaming slugs.

## Rules

1. **Slug `id` stays canonical** for pytest parametrization (`test_persona_matching.py` ids=).
2. **`pr_ids` is additive only** — array of `PR-NN` strings, one primary Refinement persona per shipped slug.
3. **No PR id may appear on two shipped personas** — enforced by `test_persona_pr_ids_are_unique_and_present`.
4. New personas require all three assertion layers + golden before merge (B2/B5).

## Shipped mapping (41 of 41)

| Shipped slug (`id`) | Refinement PR | Rationale |
| --- | --- | --- |
| `maria_freshman_stem` | PR-01 | STEM college freshman, low income, NCR |
| `grade11_shs` | PR-02 | Grade 11 SHS — SHS grant include, college-only exclude |
| `ana_accountancy_2nd_year` | PR-03 | 2nd year accountancy, 5.0-scale GWA, private NCR |
| `miguel_graduating_civil` | PR-04 | Graduating civil engineering, Region VII |
| `grace_graduate_ms` | PR-05 | Graduate MS Biology |
| `ben_tvet_welding` | PR-06 | TVET welding trainee |
| `minimal_profile` | PR-07 | Sparse profile — fail-open provisional path |
| `carlo_transferee_it` | PR-08 | Transferee 3rd year IT, CALABARZON |
| `visayas_student` | PR-09 | Region VI resident — geographic + need overlap |
| `paolo_middle_income` | PR-10 | Middle income (₱380k) — need ceiling boundaries |
| `income_at_ceiling` | PR-11 | Income exactly ₱250k at need ceiling |
| `high_income_merit` | PR-12 | High income — need grant excluded |
| `high_gwa_mathematics` | PR-13 | High GWA + low income — large qualified set |
| `low_gwa` | PR-14 | GWA 80 — need included, high GWA merit excluded |
| `gwa_scale_parity` | PR-15 | GWA scale normalization (+ `test_pr15_gwa_scale_equivalence`) |
| `missing_gwa` | PR-16 | No GWA — provisional against GWA-gated fixtures |
| `public_university_student` | PR-17 | Public-only vs private-only school gates |
| `private_school` | PR-18 | Private HEI — mirror public/private open fixtures |
| `up_diliman_named_school` | PR-19 | Named-school + UP system registry |
| `suc_category_student` | PR-20 | SUC school category restriction |
| `ncr_no_city` | PR-21 | NCR resident without city |
| `mindanao_davao` | PR-22 | Davao Region XI vs BARMM exclusion |
| `barmm_resident` | PR-23 | BARMM alias handling |
| `calabarzon_alias` | PR-24 | CALABARZON alias (+ `test_pr24_region_aliases_produce_identical_matches`) |
| `engineering_student` | PR-25 | Engineering field vs STEM hierarchy |
| `devcom_student` | PR-26 | Development Communication — B6 taxonomy proof |
| `nursing_student` | PR-27 | Nursing / Medical broad matching |
| `agriculture_student` | PR-28 | Agriculture + Region II |
| `non_stem_field` | PR-29 | Business broad field scoring |
| `arts_literature` | PR-30 | BA Literature — Arts broad, not STEM over-match |
| `pwd_priority_student` | PR-31 | PWD equity priority ranking |
| `ip_priority_student` | PR-32 | IP priority, Region XI |
| `solo_parent_dependent` | PR-33 | Solo-parent dependent priority |
| `young_age` | PR-34 | Working student — part-time, evening program (DATA-08) |
| `student_athlete` | PR-35 | Varsity athlete with `athlete_level` (DATA-08) |
| `ofw_dependent` | PR-36 | OFW dependent priority |
| `farmer_fisher_dependent` | PR-37 | Farmer/fisher dependent, Region VI |
| `gsis_dependent_member` | PR-38 | GSIS members-only |
| `passed_deadline_visible` | PR-39 | Passed deadline still visible, sorted last |
| `needs_review_penalty` | PR-40 | `needs_review` ×0.65 scoring penalty |
| `over_constrained_near_miss` | PR-41 | Over-constrained profile never empty (+ `test_pr41_over_constrained_never_empty`) |

## Verification

```bash
pytest app/tests/test_persona_matching.py -v
pytest app/tests/test_persona_mutation.py -v
pytest app/tests/test_taxonomy.py -v
```
