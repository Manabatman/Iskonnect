# ISKONNECT Verification — Megaworld Foundation

**Bundle ID:** `megaworld_foundation`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/megaworld_foundation.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export (1 records).

Scholarship IDs in this export: 61

Check archived variants listed in bundle export if present.

## Official domains to prioritize

megaworldfoundation.com, megaworldcorp.com

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

- M
- e
- g
- a
- w
- o
- r
- l
- d
-  
- F
- o
- u
- n
- d
- a
- t
- i
- o
- n
-  
- p
- a
- r
- t
- n
- e
- r
-  
- u
- n
- i
- v
- e
- r
- s
- i
- t
- y
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
- s

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
verification/reports/megaworld_foundation/
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
