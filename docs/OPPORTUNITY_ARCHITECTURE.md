# Future Opportunity Architecture (Design Only)

ISKONNECT's long-term platform extends beyond scholarships using shared primitives:

## Core primitives (already in codebase)

- **Persistent profile** (`Student` model) — education, location, income, GWA, equity flags, documents
- **EligibilityResult contract** (`app/matching/eligibility_result.py`) — deterministic qualified/provisional/not eligible
- **Two-stage engine** — hard filters then weighted scoring (`hard_filters` + `MatchService`)
- **Data completeness & verification** (`data_completeness.py`, `verification_display.py`)

## Generic Opportunity abstraction (future)

```text
Opportunity (abstract)
├── opportunity_type: scholarship | internship | ojt | grant | fellowship | competition
├── core_fields: title, provider, link, deadline, description
├── eligibility_rules: JSON rule set (reuses hard filter evaluators)
└── benefits / requirements metadata
```

Scholarship remains the first concrete `opportunity_type`. New modules add datasets + rule mappings, not new engines.

## Module roadmap

| Module | Reuse | New data |
|--------|-------|----------|
| Graduate school matching | Full profile + eligibility | Program-level rules |
| Research grants / fellowships | Full | PI requirements, field |
| Internships / OJT | Profile + location + field | Employer rules |
| Competitions / volunteer | Profile extensions | Event metadata |
| Resume parsing | Separate ingestion → feeds profile | Parsing pipeline |

## Architectural rule

Do not fork matching. Extend `evaluate_eligibility` with opportunity-type-specific requirement evaluators registered in a rule registry.
