# ADR-004: Taxonomy model

**Status:** Accepted  
**Date:** 2026-08-01  
**Phase:** 4 — Data expansion (B6)

## Context

Profile and scholarship fields used a flat list of ten PSCED broad disciplines plus ~35 sample courses. Students in Journalism, Development Communication, Hospitality, Criminology, TVET trades, and other fields could not describe themselves accurately. Frontend `profileOptions.ts` and backend `app/taxonomy/` duplicated values with drift.

## Decision

Adopt a **three-level additive model** with one backend source of truth in `app/taxonomy/psced_fields.py`:

1. **Course alias** — free text (`BSDevCom`, `BSIT`, …) mapped via `COURSE_ALIASES`
2. **Normalized field** — ~90 entries in `NORMALIZED_FIELDS`, each with exactly one parent
3. **Broad discipline** — the existing ten PSCED buckets plus six **sub-disciplines** linked through `FIELD_HIERARCHY`

### Hard rules

1. The existing ten broad disciplines remain **byte-identical** (no renames, no removals).
2. Six sub-disciplines declare parents: `Communication→Arts`, `Social Sciences→Arts`, `Tourism & Hospitality→Business`, `Maritime→Engineering`, `Aviation→Engineering`, `Sports Science→Education`. Legacy `Engineering`/`IT`/`Science`/`Mathematics→STEM` edges are preserved.
3. Resolution is **generous upward only**: a scholarship restricted to `Arts` matches a Journalism student; a scholarship restricted to `Journalism` does not exclude a generic Arts student (lower field-match level in B7, not hard exclusion).
4. TVET qualifications live in `app/taxonomy/tvet_qualifications.py` (~18 TESDA entries), offered **only** when academic stage is TVET.
5. A new **top-level** discipline requires its own ADR; additions within existing disciplines map to an existing parent.

### Consumers

- Matching: `profile_fields_for_matching()` walks transitive `FIELD_HIERARCHY` ancestors.
- Eval oracle: independent logic, **shared vocabulary** from `psced_fields` (not duplicated `_PARENTS` tables).
- Frontend options: server-served in B8 (`DATA-04`); static fallback retained until then.

## Consequences

- Persona PR-26 (Development Communication) selects `Development Communication` and still matches Arts- and Communication-restricted fixtures.
- Legacy stored broad strings remain valid; no profile migration required in B6.
- B7 will add four-level field-match scoring on top of this hierarchy.

## References

- `ISKONNECT_PRODUCT_REFINEMENT_MASTER_PLAN.md` §15.1 (DATA-01…DATA-06)
- `app/taxonomy/psced_fields.py`, `app/taxonomy/tvet_qualifications.py`
- `app/tests/test_taxonomy.py`, persona suite (zero-loss gate)
