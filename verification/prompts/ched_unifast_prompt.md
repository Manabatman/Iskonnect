# ISKONNECT Verification — CHED + UniFAST + BPMSP (Higher Education)

**Bundle ID:** `ched_unifast`

## Before you start

1. Paste `verification/prompts/00_MASTER_INSTRUCTIONS.md` into this conversation first.
2. Attach `verification/export/bundles/ched_unifast.json` (generated export).
3. Enable web search.

## Scope

Verify **only** scholarships in this bundle export (5 records).

Scholarship IDs in this export: 1, 5, 6, 19, 76

Verify archived CHED/K-12 variants — confirm superseded or still offered.

## Official domains to prioritize

ched.gov.ph, unifast.gov.ph, bpms.ched.gov.ph

## Missing program search targets

Search the official provider site for programs not yet in ISKONNECT:

- CHED Merit Scholarship Program (current cycle)
- UniFAST Tertiary Education Subsidy (TES)
- Tulong Dunong Program (TDP)
- Bagong Pilipinas Merit Scholarship Program (BPMSP) HE track

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
verification/reports/ched_unifast/
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
