# tesda — automated link audit

**Generated:** 2026-07-26

This bundle received an automated HTTP HEAD link audit only.
Full provider verification (eligibility, dates, benefits) still requires
a ChatGPT session with `verification/prompts/tesda_prompt.md`.

## Link audit summary

- Scholarships checked: 2
- Links OK: 0
- Links broken: 2
- link_status updates proposed: 1

## Next steps

1. Run the bundle ChatGPT prompt for full field verification.
2. Merge human field_changes.csv with this automated file if needed.
3. Apply: `python -m app.scripts.apply_field_changes --csv verification/reports/tesda/field_changes.csv --apply`
