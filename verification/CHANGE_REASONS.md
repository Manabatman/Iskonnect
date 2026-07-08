# Change Reason Taxonomy

Every field correction in `field_changes.csv` must include a `change_reason` from this list.

| Reason | When to use |
|--------|-------------|
| `annual_cycle_update` | Deadline, academic year, or open/close window changed for a recurring program |
| `policy_revision` | Eligibility, benefits, or requirements changed per official policy update |
| `provider_renamed_program` | Program renamed or rebranded; same or successor program |
| `application_portal_migrated` | Application moved to a new URL or portal |
| `website_redesign` | Content unchanged but URLs or page structure changed |
| `program_discontinued` | Program permanently ended; use with closure type `permanently_discontinued` |
| `temporary_suspension` | Program paused; may resume; use with closure type `temporarily_unavailable` |
| `eligibility_expansion` | New groups, regions, or levels added |
| `eligibility_restriction` | Groups, regions, or levels removed or narrowed |
| `typographical_correction` | Spelling, formatting, or data entry fix with no policy change |
| `unknown` | Reason cannot be determined — explain in `evidence_snippet` |

## Examples

- DOST Merit deadline moved to March 2026 → `annual_cycle_update`
- GSIS page now requires membership number → `policy_revision`
- CHED Merit renamed to BPMSP → `provider_renamed_program`
- OWWA portal moved from old subdomain → `application_portal_migrated`
- AFPSLAI grant page returns 404 indefinitely → `program_discontinued` + `permanently_discontinued`
