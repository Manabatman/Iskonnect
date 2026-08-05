# Iskonnect Matching Engine

**Project:** scholarship-match backend  
**Policy version:** v1.1  
**Exported for:** NotebookLM / Gemini research  
**As of:** 2026-08-05  
**Source of truth:** `app/matching/` + `app/scoring/`

The match score measures **eligibility fit**, not admission win probability. Hard eligibility runs first; only survivors are scored with five weighted soft components.

---

## 1. Core idea

```
Student profile + Scholarship catalog
        │
        ▼
┌───────────────────────┐
│  Hard eligibility     │  evaluate_eligibility()
│  (include / exclude)  │
└───────────┬───────────┘
            │ survivors only:
            │   qualified
            │   provisionally_qualified
            ▼
┌───────────────────────┐
│  Soft scoring         │  WeightedDeterministicScorer
│  5 components → 0–100 │
└───────────┬───────────┘
            │
            ▼
   Rank + explain + (optional) persist
```

**Almost qualified** scholarships are **not** scored into the main match list; they appear on the opportunity timeline as prepare/future items.

---

## 2. Where the code lives

### Matching (`app/matching/`)

| File | Role |
|------|------|
| `match_service.py` | Orchestrator: filter → score → explain → rank |
| `hard_filters.py` | Hard-filter loop + diagnostics |
| `eligibility_result.py` | **Single eligibility authority** |
| `field_match.py` | PSCED / course match levels |
| `scoring_port.py` | Scoring payload / result contracts |
| `eligibility_explanation.py` | Backend-authored UI copy |
| `temporal_state.py` | Temporal / UI eligibility labels |
| `opportunity_timeline.py` | Plan timeline lanes |
| `preparation.py` | Preparation plan |
| `profile_completeness.py` | Completeness payload |

### Scoring (`app/scoring/`)

| File | Role |
|------|------|
| `engine.py` | `WeightedDeterministicScorer` |
| `components.py` | Per-dimension formulas (0–1) |
| `config.py` | Default weights + `from_db()` |
| `explanation.py` | Breakdown, suggestions, confidence |

### Taxonomy helpers

| File | Role |
|------|------|
| `app/taxonomy/gwa_normalizer.py` | Raw GWA → 0–100 |
| `app/taxonomy/psced_fields.py` | Field hierarchy |
| `app/taxonomy/equity_groups.py` | Equity flag mapping |
| `app/taxonomy/priority_groups.py` | Priority group canonicalization |
| `app/taxonomy/education_levels.py` | Level compatibility |
| `app/taxonomy/regions.py` | Region normalization |

### API surfaces

| Endpoint | Behavior |
|----------|----------|
| `GET /api/v1/plan/{profile_id}` | Live match + timeline + prep (**not** DB-persisted; may cache) |
| `POST /api/v1/match-runs` | Run + **persist** `match_runs` / `match_results` |
| `GET /api/v1/match-runs` | List runs |
| `GET /api/v1/match-runs/{run_id}` | Load stored results |
| `GET /api/v1/match-runs/compare` | Compare two runs |
| `GET /api/v1/scholarships/{id}/eligibility` | Single-scholarship eligibility |
| `GET/PUT /api/v1/admin/scoring/weights` | Admin weight CRUD |

---

## 3. Hard eligibility

### 3.1 Qualification statuses

From `QualificationStatus` in `eligibility_result.py`:

| Status | Meaning | Enters scored matches? |
|--------|---------|------------------------|
| `qualified` | All hard checks MET or N/A | Yes |
| `provisionally_qualified` | Some UNKNOWN (missing profile/scholarship data) | Yes |
| `almost_qualified` | Exactly one achievable UNMET (GWA, level, year, enrollment, or field) | **No** (timeline only) |
| `not_eligible` | Hard UNMET(s) | No |

### 3.2 Hard requirement keys

All `kind="hard"`:

`data_status`, `age`, `education_level`, `region`, `school_type`, `school`, `school_category`, `year_level`, `enrollment_status`, `citizenship`, `income`, `gwa`, `field`, `members_only`

Missing profile fields generally yield `UNKNOWN` → **provisional**, not exclusion.

### 3.3 Notable hard rules

| Key | Exclude when |
|-----|----------------|
| `data_status` | `expired` / `broken_link` / `past_deadline` (if `FILTER_EXPIRED_FROM_MATCHES` on) |
| `age` | Outside `min_age` / `max_age` |
| `education_level` | Incompatible with `eligible_levels` / legacy `level` |
| `region` | City list present but city mismatch; or region list mismatch |
| `income` | Annual income > `max_income_threshold`; or bracket entirely above ceiling |
| `gwa` | `gwa_normalized` < `min_gwa_normalized` |
| `field` | Restricted courses and no PSCED/specific/broad bridge match |
| `members_only` | `members_only=true` with `priority_groups` set and student matches none |
| school / type / category / year / enrollment / citizenship | Mismatch when restriction present |

**Not hard exclusions:**

- Deadline passed (flags + sorts lower; does not exclude)
- Nationwide / unrestricted fields
- Document readiness

### 3.4 Almost-qualified special case

If there is **exactly one** UNMET and that key is in:

`{gwa, education_level, year_level, enrollment_status, field}`

→ status = `almost_qualified`  
→ excluded from scored list, shown on timeline as something the student can work toward.

---

## 4. Soft scoring (v1.1)

### 4.1 Default weights

| Component | Weight | Share |
|-----------|--------|-------|
| `academic` | 0.30 | 30% |
| `income` | 0.28 | 28% |
| `field_alignment` | 0.22 | 22% |
| `geographic` | 0.10 | 10% |
| `equity_priority` | 0.10 | 10% |

Sum = 1.0. Policy version string: **`v1.1`**.

Weights can be loaded from `scoring_weights` when `DB_DRIVEN_WEIGHTS=true` (default is **false** → code defaults).

Admin PUT requires exactly these five components summing to 1.0 (±0.001).

### 4.2 Final score formula

```
each component ∈ [0, 1]

# Renormalize away N/A dimensions
if scholarship has no geographic restriction:
    weights["geographic"] = 0
if scholarship has no field restriction:
    weights["field_alignment"] = 0

norm[k] = weights[k] / sum(active weights)

base  = Σ (components[k] * norm[k]) * 100
final = clamp(base, 0, 100)   # rounded to 2 decimals

# Post-score reliability haircut (not a weight)
if data_status == "needs_review":
    final *= 0.65
```

**Deprecated / unused:** post-hoc equity multipliers (still in config for compatibility).  
**Not in score:** document readiness (`readiness_score` always 0 in scoring).

### 4.3 Component formulas

**Academic** (`score_academic`)

- No student GWA → `0.3`
- No scholarship min GWA → `min(1.0, 0.5 + gwa/200)`
- Below min → `0.25`
- At min → `0.75`; +10 points above min → `1.0` (linear in between)

**Income** (`score_income`)

- Merit / merit-based / academic types → `0.5` (income ignored)
- No ceiling → `0.5`
- No income on profile → `0.3`
- Need-based: `0.3 + 0.7 * (1 - income/ceiling)` clamped to [0,1]
- Income brackets use midpoints when annual income missing:
  - below_250k → 125k
  - 250k_400k → 325k
  - 400k_500k → 450k
  - above_500k → 600k

**Field** (`score_field`) from match level

| Level | Score |
|-------|-------|
| exact | 1.0 |
| sibling / broad | 0.75 |
| discipline | 0.6 |
| partial | 0.4 |
| none | 0.2 |

**Geographic** (`score_geographic`)

| Level | Score |
|-------|-------|
| city | 1.0 |
| region | 0.75 |
| island_group | 0.4 |
| none | 0.0 |

**Equity** (`score_equity`)

- Scholarship has no priority groups → `0.5`
- 2+ student matches → `1.0`
- 1 match → `0.75`
- 0 matches but groups required → `0.0`

### 4.4 Sort order after scoring

1. Active deadlines first (`deadline_passed` last)
2. No reliability warning first
3. Higher `final_score`
4. Stable tie-break: scholarship `id`, then `title`

---

## 5. Profile ↔ scholarship field map

| Student field(s) | Scholarship field(s) | Role |
|------------------|----------------------|------|
| `age` | `min_age`, `max_age` | Hard |
| `education_level` / `current_academic_stage` | `eligible_levels` / `level` | Hard |
| `region`, `city_municipality` | `eligible_regions`, `eligible_cities`, legacy `regions`; `residency_required` | Hard (+ soft geo) |
| `school_type` | `eligible_school_types` | Hard |
| `school` / `school_id`, `target_school*` | `eligible_schools`, `eligible_school_systems` | Hard |
| derived school category | `eligible_school_categories` | Hard |
| `current_year_level`, `next_year_level` | `eligible_year_levels` | Hard |
| `enrollment_status` | `eligible_enrollment_status` | Hard |
| `citizenship` | `citizenship_required` | Hard |
| `household_income_annual` / `income_bracket` | `max_income_threshold` | Hard + soft |
| `gwa_normalized` (from `gwa_raw` + `gwa_scale`) | `min_gwa_normalized` | Hard + soft |
| `field_of_study_broad`, `preferred_courses` | `eligible_courses_psced`, `eligible_courses_specific` | Hard + soft |
| Equity / priority flags | `priority_groups`; `members_only` | Soft equity; hard if members_only |

---

## 6. Pipeline (accurate to code)

```
function get_matches(profile, scholarships):
  candidates = []
  for sch in scholarships:
    elig = evaluate_eligibility(profile, sch)
    if elig.status not in {QUALIFIED, PROVISIONALLY_QUALIFIED}:
      record_exclusion(elig)
      continue
    candidates.append(sch annotated with elig)

  results = []
  for sch in candidates:
    field_lvl = compute_field_match_level(...)
    geo_lvl   = geographic_match_level(...)  # city > region > island_group > none
    payload   = ScoringPayload(...)
    s = WeightedDeterministicScorer(config).score(payload)
    if sch.data_status == "needs_review":
      s.final_score *= 0.65
    attach temporal / freshness / verification labels
    results.append(match_result)

  sort by (deadline_passed ASC, has_warning ASC, -final_score, id, title)
  return results + diagnostics
```

Optional: `PLAN_PREFILTER_ENABLED` SQL-prefilters by education level before the full scan.

---

## 7. Persistence model

### Live plan (`GET /plan/{profile_id}`)

- Computes in memory
- May use Redis/process cache
- **Does not write** match history

### Persisted run (`POST /match-runs`)

Writes:

```
match_runs(id, user_id, profile_id, created_at)
match_results(
  run_id, scholarship_id,
  score, final_score,
  explanation, breakdown, suggestions,
  confidence, why_not_higher,
  scoring_policy_version
)
```

Stored runs may re-evaluate eligibility on read for display freshness.

---

## 8. Edge cases worth knowing

1. **`members_only`** — hard gate on priority membership; non-members-only programs use equity only as soft score.
2. **Residency** — if `residency_required` and location missing → UNKNOWN (provisional). City matching uses exact canonical names.
3. **GWA scales** — `5.0_scale` (1.0 best), `4.0_scale` (4.0 best), `percentage`. Ambiguous values in (1,5) without scale → `None`.
4. **Field short codes** — length ≤ 3 require exact equality (prevents “IT” matching inside “architecture”).
5. **`needs_review` data_status** — provisional + **35% score haircut** + reliability warning.
6. **Weight renormalization** — open-to-all geo/field scholarships redistribute those weights to remaining dimensions.
7. **Document readiness** — tracked on profile/detail pages; never affects `final_score`.
8. **Deadlines** — do not hard-exclude; they deprioritize in sort and flag `deadline_passed`.

---

## 9. How to research / audit this engine

Useful questions for NotebookLM or Gemini:

1. Given a sample student profile and scholarship row, what hard checks fire and what status results?
2. Does the soft-score math for academic/income/field match the formulas above?
3. Are any DB fields unused by matching but shown in the UI?
4. Are `almost_qualified` programs correctly excluded from scored matches but included in timeline?
5. Do live catalog rows marked `needs_review` get the 0.65 haircut when matched?

Companion schema doc: `01_database_schema.md`  
Companion catalog dump: `live_scholarships_for_gemini.csv` / `.json`

---

## 10. Source file checklist

```
app/matching/match_service.py
app/matching/hard_filters.py
app/matching/eligibility_result.py
app/matching/field_match.py
app/matching/scoring_port.py
app/matching/temporal_state.py
app/matching/opportunity_timeline.py
app/scoring/engine.py
app/scoring/components.py
app/scoring/config.py
app/scoring/explanation.py
app/taxonomy/gwa_normalizer.py
app/api/v1/matches.py
app/api/v1/match_history.py
app/api/v1/scoring_admin.py
app/models.py  (MatchRun, MatchResult, ScoringWeight, Student, Scholarship)
```
