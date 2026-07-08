# ISKONNECT Verification Checklist

Use this checklist for **every scholarship** in a provider bundle conversation.

## Existence and status

- [ ] Does the program still exist under this name?
- [ ] Is it actively accepting applications, closed for the cycle, or discontinued?
- [ ] Has it been renamed, merged, or replaced by a newer program?

## URLs

- [ ] Is `primary_link` the correct official program page (not just a homepage)?
- [ ] Is there a separate application portal? Provide URL if different.
- [ ] Is the link working (HTTP 200, correct domain)?

## Eligibility (structured)

- [ ] Education levels (`eligible_levels`)
- [ ] Geography (`eligible_regions`, `eligible_cities`, `residency_required`)
- [ ] Income ceiling (`max_income_threshold`)
- [ ] GWA minimum (`min_gwa_normalized`)
- [ ] Age range (`min_age`, `max_age`)
- [ ] Priority groups / sector restrictions (`priority_groups`, `members_only`)
- [ ] Course / field restrictions
- [ ] Citizenship requirement (`citizenship_required`)

## Benefits and requirements

- [ ] Tuition, allowance, books, miscellaneous, total value
- [ ] Required documents
- [ ] Qualifying exam, interview, essay, return service flags

## Timeline

- [ ] Current open/close dates; recurring cycle (`cycle_type`, expected reopen)
- [ ] Correct `application_status` recommendation for ISKONNECT

## Contacts (extract if found)

- [ ] Official email, phone, office — not stored in ISKONNECT today

## Evidence (required for every change)

- [ ] Every correction cites an official `source_url`
- [ ] Every correction includes an `evidence_snippet` (quote or announcement reference)
- [ ] No field change accepted without evidence

## Change reason (required)

Classify each correction using [CHANGE_REASONS.md](CHANGE_REASONS.md).

## Closure type (required when status changes)

Classify using [CLOSURE_TYPES.md](CLOSURE_TYPES.md) — do not use "archived" alone.

## Page freshness

- [ ] Capture `official_last_updated` if visible on the page
- [ ] Capture `announcement_date` for deadline/cycle changes when visible

## Important notes (FAQ extraction)

Extract rules that do not fit structured fields, for example:

- Cannot hold another scholarship concurrently
- Full-time enrollment required
- Good moral character requirement
- Return service after graduation

Output in `important_notes.json`.

## Schema candidates

When eligibility rules recur but ISKONNECT has no structured field, log in `schema_candidates.json`:

- `observed_rule`
- `example_scholarship_ids`
- `frequency_in_bundle`
- `current_workaround` (usually description)
- `recommendation` (`keep_free_text` | `add_structured_field` | `add_to_priority_groups`)

## ISKONNECT action

- [ ] Fields to update, archive, or add as new scholarship
- [ ] Confidence: `verified` / `partially_verified` / `cannot_verify`

## Known schema gaps

- No `contact_email` or `contact_phone` columns — extract from official pages when published
- Single URL field (`primary_link`) — flag homepage-only links vs program-specific pages
