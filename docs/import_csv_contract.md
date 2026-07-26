# ISKONNECT Scholarship CSV Import Contract

This document defines the **exact** CSV format that the Gemini ΓåÆ Cursor generation step must produce before running `python -m app.scripts.csv_to_staging`.

The importer enforces this contract strictly. Rows or headers that violate it are **rejected with an explanation** ΓÇö never silently corrected.

## Header row (required)

The first row must contain column names in this **exact order** (39 columns):

```
title,provider,source,link,description,provider_type,scholarship_type,eligible_levels,eligible_regions,eligible_cities,residency_required,eligible_school_types,eligible_courses_psced,eligible_courses_specific,max_income_threshold,min_gwa_normalized,min_age,max_age,priority_groups,benefit_tuition,benefit_allowance_monthly,benefit_books,benefit_total_value,required_documents,has_qualifying_exam,has_interview,has_essay_requirement,has_return_service,application_open_date,application_deadline,academic_year_target,cycle_type,last_open_date,last_close_date,is_active,source_slug,research_notes,source_urls,dedupe_rationale
```

Canonical definition lives in `app/utils/import_contract.py` (`CANONICAL_IMPORT_COLUMNS`).

## Critical rule: equal field count per row

**Every data row must have exactly the same number of fields as the header row.**

Empty values are allowed, but the comma separators must still be present. A missing empty field causes silent column left-shift in naive parsers and is **rejected** by `load_csv_strict`.

### Wrong (missing empty `eligible_cities`)

```csv
title,...,eligible_regions,residency_required,...
Pasig Scholarship,...,NCR,true,...
```

Here `residency_required` receives the value meant for `eligible_cities`, and all following columns shift left.

### Correct

```csv
title,...,eligible_regions,eligible_cities,residency_required,...
Pasig Scholarship,...,NCR,,true,...
```

## Column reference

### Required columns

| Column | Type | Notes |
|--------|------|-------|
| `title` | string | Non-empty scholarship name |

### Recommended columns (warnings if missing)

`provider`, `link`, `scholarship_type`, `provider_type`, `eligible_levels`

### Schema columns (35)

| Column | Type | Format |
|--------|------|--------|
| `provider` | string | Organization name |
| `source` | string | e.g. `gemini_research` |
| `link` | URL | `http://` or `https://` |
| `description` | string | Quote if contains commas |
| `provider_type` | enum | `Government`, `Private`, `LGU`, `Institutional` |
| `scholarship_type` | enum | `Merit-based`, `Need`, `Merit-and-Need`, `Affiliation` |
| `eligible_levels` | pipe-list | e.g. `College\|TVET` |
| `eligible_regions` | pipe-list | e.g. `NCR\|Region VII - Central Visayas` |
| `eligible_cities` | pipe-list | e.g. `Pasig` (empty = nationwide within region) |
| `residency_required` | boolean | `true` / `false` |
| `eligible_school_types` | pipe-list | `Public\|Private` |
| `eligible_courses_psced` | pipe-list | `STEM\|Engineering\|IT\|...` |
| `eligible_courses_specific` | pipe-list | Free-text course names |
| `max_income_threshold` | integer | Annual PHP, e.g. `300000` |
| `min_gwa_normalized` | decimal | 0ΓÇô100 percentage scale |
| `min_age` | integer | Empty if not applicable |
| `max_age` | integer | Empty if not applicable |
| `priority_groups` | pipe-list | e.g. `PWD\|4Ps` |
| `benefit_tuition` | boolean | `true` / `false` |
| `benefit_allowance_monthly` | integer | PHP per month |
| `benefit_books` | boolean | `true` / `false` (not a peso amount) |
| `benefit_total_value` | integer | Total annual/semester value in PHP |
| `required_documents` | pipe-list | e.g. `TOR\|ITR\|BARANGAY_CERT` |
| `has_qualifying_exam` | boolean | |
| `has_interview` | boolean | |
| `has_essay_requirement` | boolean | |
| `has_return_service` | boolean | |
| `application_open_date` | date | `YYYY-MM-DD` |
| `application_deadline` | date | `YYYY-MM-DD` |
| `academic_year_target` | string | e.g. `2026-2027` |
| `cycle_type` | string | `annual`, `semester`, or `rolling` |
| `last_open_date` | date | `YYYY-MM-DD` |
| `last_close_date` | date | `YYYY-MM-DD` |
| `is_active` | boolean | Catalog visibility flag |

### Import metadata columns (4)

Stored in staging `payload_json`; not part of the public scholarship schema today.

| Column | Type | Notes |
|--------|------|-------|
| `source_slug` | string | Stable import identifier |
| `research_notes` | string | e.g. `application_status=open \| confidence=high` |
| `source_urls` | pipe-list | Verification URLs |
| `dedupe_rationale` | string | Why this row is distinct |

## List fields (pipe-delimited)

Multi-value columns use `|` as separator, no spaces required:

```
eligible_levels=College|Senior High School
required_documents=TOR|ITR|BARANGAY_CERT
```

## Boolean fields

Use lowercase `true` or `false`. Empty cells become `null`.

## Date fields

Use ISO `YYYY-MM-DD`. Empty cells become `null`.

## Quoting

Wrap fields containing commas, quotes, or newlines in double quotes. Escape internal quotes by doubling them (`""`).

## Import command

```bash
python -m app.scripts.csv_to_staging --csv path/to/scholarships.csv --report import_report.json
```

### Abort conditions (entire file rejected)

- Unknown column names
- Missing required column (`title`)
- Duplicate normalized column names

### Per-row rejection

- `column_count_mismatch (expected N, got M)` ΓÇö fix empty-field commas before re-import

## Validation report fields

After import, the JSON report includes:

- `imported` ΓÇö counts: `new`, `updated_candidate`, `skipped`, `invalid`, `rejected_structural`
- `rejected_structural` ΓÇö rows failed field-count check
- `unknown_columns`, `missing_columns` ΓÇö header problems
- `invalid_urls`, `invalid_dates` ΓÇö aggregated row warnings
- `auto_normalizations` ΓÇö e.g. `normalized_scholarship_type:Merit-based`
- `structural_rejections` ΓÇö per-line rejection details

Nothing is silently ignored.
