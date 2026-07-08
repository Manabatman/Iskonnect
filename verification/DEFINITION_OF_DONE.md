# Definition of Done — External Verification

## Scholarship-level verification

A scholarship is **verified** when ChatGPT confirms **all** of the following:

1. Official source identified (`.gov.ph`, `.edu.ph`, or foundation official domain)
2. Program still exists — or is explicitly marked discontinued with evidence and closure type
3. Program-specific page URL captured (not homepage-only unless that is the only official source)
4. Working application URL — or documented "no online application"
5. Eligibility fields confirmed or corrected (structured + description) **with evidence per changed field**
6. Benefits confirmed or corrected **with evidence**
7. Requirements / documents confirmed or corrected **with evidence**
8. Deadline / cycle status confirmed or corrected **with evidence**
9. Contact info captured if published (optional but recommended)
10. Recommended ISKONNECT updates listed field-by-field in `field_changes.csv`
11. Important notes captured in `important_notes.json` where applicable
12. Verification date + source URL recorded
13. **Import-ready files produced** requiring minimal manual editing before staging import

### Partial verification

Allowed only when the official source confirms existence but specific fields are unpublished. List each unknown explicitly — do not invent values.

## Bundle-level completion

A **bundle conversation** is **done** when all five deliverables exist under `verification/reports/{bundle_id}/`:

| # | File | Purpose |
|---|------|---------|
| 1 | `human_report.md` | Summary for human review |
| 2 | `field_changes.csv` | Corrections with evidence + change reason |
| 3 | `new_scholarships.json` | Missing programs from that provider |
| 4 | `schema_candidates.json` | Structured-field patterns (if any) |
| 5 | `important_notes.json` | FAQ-style rules (if any) |

## Admin review before import

After ChatGPT completes a bundle:

1. Review `human_report.md` for obvious errors
2. Spot-check high-priority corrections (`verification_priority=high` in export)
3. Confirm closure types — especially recurring programs closed for the season
4. Import via admin staging with `verification_source=manual`

## Re-export trigger

Re-run `python -m app.scripts.export_verification_package --active-only` when:

- Catalog rows are added or archived
- A new academic cycle begins (CHED, DOST, LGU deadlines)
- Link maintenance flags new broken URLs
