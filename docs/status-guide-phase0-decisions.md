# Scholarship Status Guide — Phase 0 Decisions

## Architecture decision

**Implementation evolves toward the guide**, with two vocabulary refinements based on student comprehension:

| Guide term (before) | Agreed term | API key |
|---------------------|-------------|---------|
| Previous cycle | **Past cycle** | `previous_cycle` |
| Archived | **No longer offered** | `archived` |
| Needs review (admin) | **Needs verification** | `needs_verification` |

**Source of truth:** `Scholarship.application_status` — an explicit column synced at write time (import, catalog maintenance, admin verify/deactivate). Not recomputed from scattered fields on every API read except as a migration fallback when the column is null.

**Orthogonal fields (unchanged):**

- `link_status` — link health (broken/ok), shown as “Link issue”
- `last_verified_at`, `verification_source` — trust metadata
- `data_status` — retained for pipeline/jobs; lifecycle display uses `application_status`

**MVP placement:** `application_status` lives on `Scholarship` (one row ≈ one cycle today). Future `ScholarshipCycle` entity can own the field when identity/cycle split lands.

## Why not derived `lifecycle_status`?

Guessing lifecycle from `is_active + data_status + dates + …` at render time created label drift (“Expired”, “Closed cycle”, “Deadline passed” on one card). The explicit column is written once when underlying facts change, then read everywhere.

## Behavioral policy changes

1. **Deadline expiry** no longer sets `is_active=False` — scholarships stay searchable with `application_status` of `closed`, `previous_cycle`, or `expected_reopen`.
2. **Default search** shows `needs_verification` listings (with warning), not silently hidden.
3. **Archived** (`is_active=False`) hidden by default; optional `include_archived` / `timing=archived` filter.

## Minimal field set going forward

| Layer | Field |
|-------|--------|
| Lifecycle (student) | `application_status` |
| Trust | `last_verified_at`, `verification_source`, `data_status` (pipeline) |
| Link | `link_status` |
| Cycle prediction | `cycle_type`, `last_open_date`, `last_close_date` |
| Per-student fit | `ui_state`, `gap_reason`, `next_action` (match API only) |
