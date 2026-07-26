# Verification Bundle Status

**Last updated:** 2026-07-26  
**Total bundles:** 15 (from `verification/export/master_index.json`)

This tracker records which provider bundles have completed ChatGPT verification deliverables under `verification/reports/{bundle_id}/` and which remain pending.

## Summary

| Status | Count | Bundles |
|--------|------:|---------|
| Full verification complete | 2 | `ched_unifast`, `dost` |
| Link audit complete (full field verification pending) | 13 | all others below |

All 15 bundles now have the five-file scaffold under `verification/reports/{bundle_id}/`. The 13 pending bundles received an **automated HTTP HEAD link audit** on 2026-07-26 via `python -m app.scripts.run_verification_bundle --all-pending --apply-links`. Full eligibility, benefit, and cycle-date verification still requires a ChatGPT session with each bundle prompt.

---

## Full verification complete

| Bundle | Title | Scholarships | Reports |
|--------|-------|-------------:|---------|
| `ched_unifast` | CHED + UniFAST + BPMSP (Higher Education) | 5 | [human_report.md](ched_unifast/human_report.md), [field_changes.csv](ched_unifast/field_changes.csv) |
| `dost` | DOST-SEI | 2 | [human_report.md](dost/human_report.md), [field_changes.csv](dost/field_changes.csv) |

**Applied:** corrections via `apply_field_changes.py` and link fixes via `fix_broken_links.py`.

---

## Link audit complete — full verification pending (13)

Each bundle has `human_report.md`, `field_changes.csv` (link_status rows), and template JSON files. Run the ChatGPT bundle prompt to replace/extend `field_changes.csv` with full field verification, then apply.

| # | Bundle ID | Title | Scholarships | Link audit | Prompt |
|---|-----------|-------|-------------:|------------|--------|
| 1 | `tesda` | TESDA + BPMSP (TVET) | 2 | 2026-07-26 | [tesda_prompt.md](../prompts/tesda_prompt.md) |
| 2 | `gsis_sss` | GSIS + SSS | 3 | 2026-07-26 | [gsis_sss_prompt.md](../prompts/gsis_sss_prompt.md) |
| 3 | `owwa_dswd_ncip` | OWWA + DSWD + NCIP | 4 | 2026-07-26 | [owwa_dswd_ncip_prompt.md](../prompts/owwa_dswd_ncip_prompt.md) |
| 4 | `military_affiliation` | Military / uniformed service affiliation | 2 | 2026-07-26 | [military_affiliation_prompt.md](../prompts/military_affiliation_prompt.md) |
| 5 | `lgu_ncr` | LGU — NCR | 12 | 2026-07-26 | [lgu_ncr_prompt.md](../prompts/lgu_ncr_prompt.md) |
| 6 | `universities` | Universities and colleges | 7 | 2026-07-26 | [universities_prompt.md](../prompts/universities_prompt.md) |
| 7 | `private_foundations` | Private foundations (corporate) | 8 | 2026-07-26 | [private_foundations_prompt.md](../prompts/private_foundations_prompt.md) |
| 8 | `sm_foundation` | SM Foundation | 1 | 2026-07-26 | [sm_foundation_prompt.md](../prompts/sm_foundation_prompt.md) |
| 9 | `megaworld_foundation` | Megaworld Foundation | 1 | 2026-07-26 | [megaworld_foundation_prompt.md](../prompts/megaworld_foundation_prompt.md) |
| 10 | `other_government` | Other national government programs | 3 | 2026-07-26 | [other_government_prompt.md](../prompts/other_government_prompt.md) |
| 11 | `lgu_provincial` | LGU — provincial / outside NCR | 3 | 2026-07-26 | [lgu_provincial_prompt.md](../prompts/lgu_provincial_prompt.md) |
| 12 | `international` | International scholarships | 2 | 2026-07-26 | [international_prompt.md](../prompts/international_prompt.md) |
| 13 | `archived_reference` | Archived / historical reference | 36 | 2026-07-26 | [archived_reference_prompt.md](../prompts/archived_reference_prompt.md) |

---

## How to complete the next bundle

1. Paste [verification/prompts/00_MASTER_INSTRUCTIONS.md](../prompts/00_MASTER_INSTRUCTIONS.md) at the start of a ChatGPT session (web search enabled).
2. Attach `verification/export/bundles/{bundle_id}.csv`.
3. Run `verification/prompts/{bundle_id}_prompt.md`.
4. Merge human `field_changes.csv` with any automated link rows already present.
5. Apply (dry-run first):

```bash
python -m app.scripts.apply_field_changes --csv verification/reports/{bundle_id}/field_changes.csv
python -m app.scripts.apply_field_changes --csv verification/reports/{bundle_id}/field_changes.csv --apply
```

6. Move the bundle to **Full verification complete** above once human-reviewed.

---

## Related Phase 2 catalog growth scripts

| Script | Purpose |
|--------|---------|
| `python -m app.scripts.resolve_duplicate_scholarships` | Fix duplicate parent records |
| `python -m app.scripts.discovery_to_csv` | Export validated discovery JSON to import CSV |
| `python -m app.scripts.gemini_triage` | Classify Gemini CSV rows vs live catalog |
| `python -m app.scripts.fix_broken_links` | Apply link/link_status fixes from verification CSVs |
| `python -m app.scripts.approve_staging_batch --apply` | Promote pending staging rows after admin review |
| `python -m app.scripts.run_verification_bundle --all-pending` | Regenerate link-audit reports for pending bundles |

All database-mutating scripts default to **dry-run**; pass `--apply` to persist changes.
