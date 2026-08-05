# Implementation backlog (source review 2026-08-05)

## Already completed

- Alembic 048 schema; affiliation/conflict taxonomies; gate-flagged evaluators
- Migration v1 backfill (critical providers)
- Post-migration audit: **GO — Data Ready, Gates Off**
- Provider acceptance scaffold (`test_provider_acceptance_live.py`)
- Always-on hard filters (region, school, field, enrollment, income, citizenship, members_only, temporal)
- Field evidence machinery (correct for **admin**; was wrongly exposed to students)
- Group C extraction artifacts (`verification/export/groupc_by_pdf/`)

---

## High-priority before public beta

| # | Item | P | Owner |
|---|------|---|-------|
| 1 | Student verification strip; hide field evidence / “Imported” / change history on public detail | P0 | frontend+backend |
| 2 | Supabase Storage env for admin image uploads | P0 | config |
| 3 | Catalog remediation: #16, #14, #81/#65, #130, #61/#10, #54 | P0 | data |
| 4 | Affiliation gate-off fallback (no members_only duplication) | P0 | backend |
| 5 | Destination evaluator + `study_destination_preference` enum | P0 | backend+frontend |
| 6 | Enrich Detail + `/eligibility` with join fields | P0 | backend |
| 7 | FP + TP acceptance tests; Top25×10 matrix | P0 | tests |
| 8 | DOST #3, Estatistikolar, SIKAP, GSSP SG, consortium completion | P1 | data |
| 9 | Gender gate (#11); JLSS application-year model | P1 | backend |
| 10 | Gradual GATE rollout (after green acceptance) | P1 | ops |

---

## Recommended after public beta

- Collapsible “How was this verified?” transparency panel (if not in P0 strip)
- Natural-born citizenship distinction
- QCSP track subtypes + QCitizen ID
- CMSP weighted selection score
- Megaworld/SM partner CSV maintenance job
- LGU residency / voter / one-scholar-per-family (Group C depth)
- Return-service exclusivity conflict scope
- GSP benefit figure corrections
- Explanation copy for new gate keys

---

## Future enhancements

- Developer debug mode for raw verification metadata
- Renewal evaluator / `renewal_gwa`
- Document checklist soft signals (NBI, undertaking forms)
- Deprecate `members_only` where affiliations exist (#7)
- Full Group C catalog remediation (100+ rows)
- Automated report-vs-live diff from `groupc_by_pdf/*.json`
