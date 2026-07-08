# ISKONNECT Verification — Archived / historical reference

**Bundle ID:** `archived_reference`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/archived_reference.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export (36 records).

Scholarship IDs in this export: 12, 30, 32, 35, 36, 37, 38, 42, 43, 44, 46, 47, 54, 58, 60, 64, 65, 66, 67, 68, 70, 72, 73, 74, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90

Check archived variants listed in bundle export if present.

## Official domains to prioritize

(varies)

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

- P
- r
- o
- g
- r
- a
- m
- s
-  
- m
- a
- r
- k
- e
- d
-  
- i
- n
- a
- c
- t
- i
- v
- e
-  
- —
-  
- c
- o
- n
- f
- i
- r
- m
-  
- d
- i
- s
- c
- o
- n
- t
- i
- n
- u
- e
- d
-  
- v
- s
-  
- s
- e
- a
- s
- o
- n
- a
- l
-  
- a
- r
- c
- h
- i
- v
- e
-  
- m
- i
- s
- t
- a
- k
- e

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
verification/reports/archived_reference/
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
