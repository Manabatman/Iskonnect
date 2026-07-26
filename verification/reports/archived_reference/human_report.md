# archived_reference — automated link audit

**Generated:** 2026-07-26

This bundle received an automated HTTP HEAD link audit only.
Full provider verification (eligibility, dates, benefits) still requires
a ChatGPT session with `verification/prompts/archived_reference_prompt.md`.

## Link audit summary

- Scholarships checked: 36
- Links OK: 24
- Links broken: 12
- link_status updates proposed: 35

## Next steps

1. Run the bundle ChatGPT prompt for full field verification.
2. Merge human field_changes.csv with this automated file if needed.
3. Apply: `python -m app.scripts.apply_field_changes --csv verification/reports/archived_reference/field_changes.csv --apply`
