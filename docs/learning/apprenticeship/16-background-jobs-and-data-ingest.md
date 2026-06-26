# Lesson 16 — Background Jobs & Data Ingest

> **Prerequisite:** [15 — Middleware & Observability](15-middleware-observability-sentry.md)

---

## The data problem

Matching needs a **scholarship catalog**. Sources:

1. **Curated seed** — `seed_data.py`, 24 baseline scholarships
2. **CSV import** — [`app/scripts/import_scholarships.py`](../../../app/scripts/import_scholarships.py)
3. **Demo CSVs** — `python -m app.scripts.seed_demo_csvs`
4. **Web scrapers** — [`app/scrapers/`](../../../app/scrapers), GitHub Actions `scraper.yml`

---

## Concept: Sync vs async jobs

| Type | Iskonnect usage |
|------|-----------------|
| **Sync in request** | Match computation (CPU-bound, seconds max) |
| **Scheduled batch** | Scrapers, link checker, deadline maintenance |
| **CI workflow** | GitHub Actions runs scraper against production DB |

Scrapers are **not** in the hot request path — they write to DB via ingest scripts.

---

## Scraper stack

- [`app/scrapers/base.py`](../../../app/scrapers/base.py) — HTTP fetch, user-agent
- Sources: PhilScholar, SIKAP, etc.
- [`app/scripts/ingest_scraped.py`](../../../app/scripts/ingest_scraped.py) — load into `scholarships` or staging
- [`models.ScraperRun`](../../../app/models.py) — logged in `/health` as `scraper_last`

**Gated removal:** Scrapers tied to ops health — remove only with alternative data pipeline.

---

## Staging workflow

[`scholarship_staging.py`](../../../app/api/v1/scholarship_staging.py) — admin reviews scraped rows before publish (migration 009 privacy/staging).

---

## Link checker

[`app/jobs/link_checker.py`](../../../app/jobs/link_checker.py) — marks `broken_link` data_status → excluded from matching when flag on.

---

## Commands

```bash
# Import CSV
python -m app.scripts.import_scholarships --path data/raw/scholarships.csv

# Demo seed
python -m app.scripts.seed_demo_csvs

# Alembic before ingest on fresh DB
alembic upgrade head
```

---

## What breaks without ingest?

Empty `scholarships` table → match returns `[]` → product appears broken.

---

## Exercises

### Level 1 — Understanding

1. Why scrape to staging first?
2. What does `data_status=broken_link` affect?

### Level 2 — Implementation

1. Count scholarships in DB via `/metrics` or SQL.

### Level 3 — Debugging

1. `/health` shows old `scraper_last` — is scraper cron running? Check GitHub Actions secrets `DATABASE_URL`.

### Level 4 — Architecture

1. Replace scrapers with partner API feeds — diagram new ingest pipeline.

<details>
<summary>Solution</summary>

Staging prevents bad scraped data going live. broken_link excluded from matching via hard_filters when feature enabled. Partner API: fetch → validate → staging → admin approve → invalidate_scholarship_cache.
</details>

---

*Previous: [15 — Observability](15-middleware-observability-sentry.md) | Next: [17 — Backend Testing](17-backend-testing-philosophy.md)*
