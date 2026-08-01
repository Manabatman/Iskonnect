# Matching personas (QA-05 / B5)

Human-readable expectations for the **41-persona** CI suite. Each persona encodes a real student archetype and named scholarship fixtures from `app/tests/fixtures/persona_catalog.json`.

**Fixture catalog (MATCH-01 / B1):** 62 scholarships spanning all restriction types. Meta-test: `test_fixture_catalog_covers_all_restriction_types`.

**Assertion layers (MATCH-02/03 / B2):** Each persona carries `must_include` / `must_exclude` (layer 1), `expected_status` + optional `expected_detail_status` (layer 2), `ranking_invariants` (layer 3), and a committed golden at `app/tests/fixtures/golden/<persona_id>.json`. Regenerate goldens only via `python -m app.scripts.regenerate_persona_goldens` and review the diff in PR.

**Explanation quality (MATCH-06 / B3):** `test_every_match_has_explanation` and `test_provisional_names_unverified_requirement`.

**Weight mutation (MATCH-05 / B4):** `app/tests/test_persona_mutation.py` — zeroing or inverting any single scoring weight must break at least one ranking invariant.

**Taxonomy (B6):** PR-26 (`devcom_student`) proves Development Communication resolves upward to Communication → Arts after `DATA-01/02` expansion.

Refinement PR-01…PR-41 definitions live in `ISKONNECT_PRODUCT_REFINEMENT_MASTER_PLAN.md` §14.4. The full **slug → PR** table is in [`persona-id-map.md`](persona-id-map.md).

## Original twelve (still the core regression anchors)

| Slug | PR | Student | Must include | Must exclude | Why |
| --- | --- | --- | --- | --- | --- |
| maria_freshman_stem | PR-01 | STEM freshman, NCR, low income | Nationwide STEM, Need grant | Visayas-only, SHS-only | Region and level gates |
| grade11_shs | PR-02 | Grade 11 | SHS grant | College STEM | Education level |
| visayas_student | PR-09 | Visayas resident | Nationwide + regional | — | Regional eligibility |
| high_income_merit | PR-12 | High income | Merit / open fixtures | Need grant | Income ceiling |
| missing_gwa | PR-16 | No GWA | Nationwide (provisional) | Visayas, SHS | Fail-open GWA |
| low_gwa | PR-14 | GWA 80 | Need grant | High GWA merit | GWA threshold |
| income_at_ceiling | PR-11 | Income at 250k | Need grant | — | Boundary inclusion |
| ncr_no_city | PR-21 | Region without city | Nationwide | Visayas | Geographic gate |
| private_school | PR-18 | Private HEI | Nationwide | — | School type open |
| non_stem_field | PR-29 | Business major | Need grant | — | Field scoring |
| young_age | PR-34 | Age 16 college | Nationwide | — | Age band (partial PR-34) |
| minimal_profile | PR-07 | Sparse fields | Nationwide (provisional) | Visayas, SHS | Fail-open unknowns |

## B5 additions (29 personas)

See [`persona-id-map.md`](persona-id-map.md) for the complete PR-03…PR-41 mapping. Highlights:

- **Education stage:** accountancy sophomore, graduating engineer, graduate MS, TVET welder, transferee IT
- **Income / GWA:** middle income, high GWA mathematics, GWA scale parity
- **School / geo:** public vs private, UP Diliman named school, SUC category, Davao, BARMM, CALABARZON aliases
- **Field / taxonomy:** engineering, DevCom (B6 proof), nursing, agriculture, arts literature
- **Equity:** PWD, IP, solo-parent, OFW, farmer/fisher, GSIS member-only
- **Lifecycle / quality:** passed deadline visible, needs_review penalty, over-constrained near-miss safety

Run:

```bash
pytest app/tests/test_persona_matching.py -v
pytest app/tests/test_persona_mutation.py -v
pytest app/tests/test_taxonomy.py -v
pytest app/tests/test_eval_regression.py -q
```
