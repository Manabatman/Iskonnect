# ISKONNECT Verification — LGU — provincial / outside NCR

**Bundle ID:** `lgu_provincial`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/lgu_provincial.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export (3 records).

Scholarship IDs in this export: 39, 49, 51

Check archived variants listed in bundle export if present.

## Official domains to prioritize

cebu.gov.ph, bislig.gov.ph, tabuk.gov.ph

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

- P
- r
- o
- v
- i
- n
- c
- i
- a
- l
-  
- s
- c
- h
- o
- l
- a
- r
- s
- h
- i
- p
-  
- p
- r
- o
- g
- r
- a
- m
- s
-  
- n
- o
- t
-  
- y
- e
- t
-  
- i
- n
-  
- c
- a
- t
- a
- l
- o
- g

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
verification/reports/lgu_provincial/
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
