# Iskonnect Database Schema — Scholarships & Matching

**Project:** iskonnect-db (Supabase / PostgreSQL 17)  
**Source of truth:** `app/models.py` + Alembic migrations in `alembic/versions/`  
**Exported for:** NotebookLM / Gemini research  
**As of:** 2026-08-05

This document describes the live catalog and matching-related schema. Status fields are mostly plain strings (no DB CHECKs); allowed values are enforced in application code.

---

## 1. Entity overview

```
users
  ├── students (1 profile per user)
  ├── match_runs ──► match_results ──► scholarships
  ├── saved_scholarships ──► scholarships
  ├── scholarship_reports ──► scholarships
  ├── applications ──► scholarships
  └── scoring_weights.updated_by

organizations ◄── scholarships.organization_id
sponsors      ◄── scholarships.sponsor_id

scholarships
  ├── field_evidence (per-field provenance)
  ├── scholarship_versions (change history)
  ├── scholarships_staging (import queue; no FK)
  └── referral_click_daily
```

**Live catalog size (approx.):** ~120 rows in `scholarships`, linked to ~62 `organizations`.

---

## 2. Table: `scholarships`

ORM class: `Scholarship`  
Alias: `Opportunity = Scholarship` (all opportunity types live in this table for now).

### 2.1 Core identity

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | Auto-increment |
| `title` | String NOT NULL | Program name |
| `provider` | String | Display provider name (legacy; prefer org) |
| `source` | String | Provenance: philscholar, sikap, csv_import, etc. |
| `link` | String | Application / info URL |
| `dedupe_key` | String UNIQUE | Import dedup identity |
| `description` | Text | Long description |
| `image_url` | String(2048) | Catalog image |
| `image_alt` | String(300) | Alt text |
| `countries` | String | Legacy CSV |

### 2.2 Hard-filter eligibility fields

Used by the matching engine to include/exclude before scoring.

| Column | Type | Notes |
|--------|------|-------|
| `regions` | String | Legacy CSV |
| `eligible_levels` | JSONB | e.g. `["College","Graduate"]` |
| `eligible_regions` | JSONB | Region list |
| `eligible_cities` | JSONB | LGU city list |
| `residency_required` | Boolean | Must live in eligible area |
| `eligible_school_types` | JSONB | `["Public","Private"]` |
| `eligible_schools` | JSONB | Registry school IDs |
| `eligible_school_systems` | JSONB | System IDs |
| `eligible_school_categories` | JSONB | SUC, LUC, private, etc. |
| `eligible_year_levels` | JSONB | Integer year levels |
| `eligible_enrollment_status` | JSONB | Status codes |
| `eligible_courses_psced` | JSONB | PSCED broad codes |
| `eligible_courses_specific` | JSONB | Specific course names |
| `citizenship_required` | String | Default Filipino |
| `max_income_threshold` | Integer | Max household income (PHP/year) |
| `min_gwa_normalized` | Float | Min GWA on 0–100 scale |
| `min_age` / `max_age` | Integer | Age bounds |

### 2.3 Scoring / classification inputs

| Column | Type | Allowed / notes |
|--------|------|-----------------|
| `provider_type` | String | Government \| Private \| LGU \| Institutional |
| `scholarship_type` | String | Merit-based \| Need \| Merit-and-Need \| Affiliation |
| `priority_groups` | JSONB | Equity / affiliation tags |
| `members_only` | Boolean NOT NULL default false | Hard gate when true |
| `preferred_extracurriculars` | JSONB | Soft preference |
| `preferred_awards` | JSONB | Soft preference |

### 2.4 Benefit package

| Column | Type | Notes |
|--------|------|-------|
| `benefit_tuition` | Boolean | Covers tuition |
| `benefit_allowance_monthly` | Integer | Monthly stipend |
| `benefit_books` | Boolean | Book allowance |
| `benefit_miscellaneous` | Text | Other benefits |
| `benefit_total_value` | Integer | Estimated annual/total value |

### 2.5 Process requirements

| Column | Type |
|--------|------|
| `required_documents` | JSONB list |
| `has_qualifying_exam` | Boolean |
| `has_interview` | Boolean |
| `has_essay_requirement` | Boolean |
| `has_return_service` | Boolean |

### 2.6 Timeline & cycle

| Column | Type | Allowed / notes |
|--------|------|-----------------|
| `application_deadline` | Date | Close date |
| `deadline_precision` | String | exact \| estimated \| rolling \| not_announced |
| `deadline_note` | Text | Human note |
| `deadline_source_url` | String | Evidence URL |
| `application_open_date` | Date | |
| `academic_year_target` | String | e.g. 2026-2027 |
| `last_open_date` / `last_close_date` | Date | Cycle history |
| `cycle_type` | String | annual \| semester \| rolling |

### 2.7 Catalog lifecycle & data reliability

| Column | Type | Allowed values |
|--------|------|----------------|
| `is_active` | Boolean | Legacy visibility (synced from editorial_state) |
| `level` | String | Legacy single level |
| `needs_tags` | JSONB | Legacy |
| `sponsor_id` | FK → sponsors | SET NULL |
| `opportunity_type` | String NOT NULL | default `scholarship` |
| `type_attributes` | Text/JSON | Per-type bag |
| `organization_id` | FK → organizations | SET NULL |
| `editorial_state` | String | draft \| imported \| needs_review \| verified \| published \| archived |
| `last_verified_at` | DateTime | |
| `verified_by` | FK → users | |
| `next_review_date` | DateTime | |
| `verification_source` | String | manual \| scraper \| partner \| csv_import |
| `confidence_score` | Float | Data confidence |
| `data_completeness_score` | Integer | 0–100 |
| `data_status` | String | active \| expiring_soon \| expired \| needs_review \| broken_link |
| `application_status` | String indexed | open \| closed \| previous_cycle \| expected_reopen \| archived \| needs_verification |
| `link_status` | String | ok \| broken \| timeout \| unchecked |
| `link_last_checked_at` | DateTime | |
| `link_failure_count` | Integer | |

**Primary lifecycle signal for publishing:** `editorial_state`  
**Primary student-facing open/closed signal:** `application_status`

---

## 3. Related tables

### 3.1 `organizations`

Canonical provider branding/grouping.

| Column | Notes |
|--------|-------|
| `id`, `slug` (unique), `canonical_name` | Identity |
| `aliases` | JSON list of alt names |
| `org_type` | Classification |
| `official_domains`, `website`, `logo_url` | Web presence |
| `verification_status` | e.g. unverified / verified |
| `created_at` | |

### 3.2 `field_evidence`

Per-field provenance for verified scholarship values.

| Column | Notes |
|--------|-------|
| `scholarship_id` | CASCADE |
| `field_key` | Which column was evidenced |
| `value_snapshot` | Value at verification time |
| `source_url`, `source_type`, `evidence_snippet` | Citation |
| `confidence`, `retrieved_at`, `reviewer_id` | QA |
| `superseded_at` | NULL = currently active evidence |

### 3.3 `scholarships_staging`

Import / CSV approval queue (no FK to live catalog).

| Column | Notes |
|--------|-------|
| `title`, `provider`, `source` | Preview fields |
| `payload_json` | Full row payload |
| `status` | pending \| approved \| rejected |
| `dedupe_key` | Partial unique among pending rows |

### 3.4 `match_runs` / `match_results`

Persisted matching history.

**`match_runs`:** `id`, `user_id`, `profile_id` → students, `created_at`

**`match_results`:**

| Column | Notes |
|--------|-------|
| `run_id`, `scholarship_id` | CASCADE FKs |
| `score`, `final_score` | Float scores |
| `explanation` | JSON list |
| `breakdown` | JSON dict of component scores |
| `suggestions` | JSON |
| `confidence` | Float |
| `why_not_higher` | JSON |
| `scoring_policy_version` | e.g. v1.1 |

### 3.5 `saved_scholarships`

User bookmarks. Unique `(user_id, scholarship_id)`.

### 3.6 `scholarship_versions`

Admin change history: `scholarship_id`, `version_number`, `changes`, `changed_by`, `changed_at`. ON DELETE CASCADE.

### 3.7 `scoring_weights`

Admin-editable scoring component weights.

| Column | Notes |
|--------|-------|
| `component` | UNIQUE: academic, income, field_alignment, geographic, equity_priority |
| `weight` | Float; five weights should sum to 1.0 |
| `updated_at`, `updated_by` | Audit |

### 3.8 `students` (matching profile peer)

Hard-filter and scoring inputs mirrored against scholarship eligibility:

- Location: `region`, `province`, `city_municipality`, `barangay`, `psgc_code`
- School: `school_type`, `school`, `school_id`, `target_school*`, year/enrollment
- Academics: `gwa_raw`, `gwa_scale`, `gwa_normalized`, `field_of_study_broad`, `preferred_courses`
- Income: `household_income_annual`, `income_bracket`
- Equity flags: PWD, IP, solo parent, OFW, farmer/fisher, 4Ps, military, GSIS/SSS, etc.
- Docs: `documents` JSON inventory (readiness; not used in score)

---

## 4. Notable indexes & constraints

- `uq_scholarships_dedupe_key` — unique dedupe
- `ix_scholarships_application_status` — lifecycle filters
- GIN indexes on JSONB eligibility/scoring list columns
- Trigram GIN on `title` (`pg_trgm`) for search
- Partial unique on staging: one pending row per `dedupe_key`
- `uq_saved_scholarships_user_scholarship`

---

## 5. Schema evolution (Alembic highlights)

| Migration | Change |
|-----------|--------|
| 001 | Initial `students` + `scholarships` |
| 006 | `match_runs`, `match_results` |
| 007 | `saved_scholarships` |
| 008 | Cycle prediction dates |
| 009 | `scholarships_staging` |
| 010 | Verification / link integrity fields |
| 011 | Reports, `scoring_weights`, versions, audit, notifications |
| 012 | Match extras: suggestions, confidence, why_not_higher, policy version |
| 023 | `dedupe_key`, cascades, title trigram |
| 026 | `members_only` |
| 028 | Image fields |
| 029 | Eligibility lists → JSONB + GIN |
| 030 | `application_status` |
| 031 | `data_completeness_score` |
| 035–036 | School / year / enrollment eligibility |
| 037 | Deadline precision / note / source URL |
| 038 | `field_evidence`, `verified_by`, `next_review_date` |
| 039 | `opportunity_type`, `type_attributes` |
| 040 | `organizations` + `organization_id` |
| 041 | `editorial_state` |
| 043 | Version cascade on scholarship delete |

---

## 6. How to verify against live DB

Supabase project: **iskonnect-db** (`ykrinwegrgabjaltbbwz`)

Useful checks:

```sql
-- Column inventory
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'scholarships'
ORDER BY ordinal_position;

-- Status distribution
SELECT application_status, editorial_state, data_status, COUNT(*)
FROM scholarships
GROUP BY 1, 2, 3
ORDER BY COUNT(*) DESC;
```

Companion export of live rows: `live_scholarships_for_gemini.csv` / `.json` in this folder.

---

## 7. Security note (for operators)

As of export, RLS is enabled on most public tables but **disabled** on:

- `field_evidence`
- `organizations`
- `referral_click_daily`

Those tables are API-exposed without row policies until RLS is enabled with appropriate policies.
