# ISKONNECT Verification — OWWA + DSWD + NCIP

**Bundle ID:** `owwa_dswd_ncip`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/owwa_dswd_ncip.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export (4 records).

Scholarship IDs in this export: 9, 52, 53, 57

Check archived variants listed in bundle export if present.

## Official domains to prioritize

owwa.gov.ph, dswd.gov.ph, ncip.gov.ph

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

- OWWA EDSP / Education and Training programs
- DSWD AICS educational assistance
- NCIP educational assistance programs

See also `verification/MISSING_SCHOLARSHIP_TARGETS.md` for cross-bundle targets.

## Verification workflow

Follow the master instructions workflow:

1. **Verify existing records** — compare each JSON row against official sources
2. **Identify corrections** — populate `field_changes.csv` with evidence + change reason
3. **Find missing scholarships** — populate `new_scholarships.json`
4. **Extract FAQs / important notes** — populate `important_notes.json`
5. **Flag schema candidates** — populate `schema_candidates.json` for recurring unmodeled rules
6. **Produce human summary** — `human_report.md` for admin review

## Output location

Save all five deliverables to:

```
verification/reports/owwa_dswd_ncip/
  human_report.md
  field_changes.csv
  new_scholarships.json
  schema_candidates.json
  important_notes.json
```

Match column/format conventions in `verification/templates/`.

## Do not

- Verify scholarships from other bundles in this conversation
- Recommend `is_active=false` for recurring programs merely closed for the cycle
- Submit field changes without `source_url` and `evidence_snippet`
