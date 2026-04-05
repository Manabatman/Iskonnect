# ISKONNECT monitoring guide (beginner-friendly)

Use a **hybrid** approach: Supabase + platform logs + the in-app **Admin** UI (`/admin`, admin role).

## Daily (about 2 minutes)

1. **UptimeRobot** (or similar): confirm the monitor for `https://YOUR-API/health` is **Up**.
2. **Supabase → Table Editor → `scholarships_staging`**: sort by `created_at` descending. After the daily GitHub Action, you should see new pending rows (or unchanged count if the scraper returned nothing).

## Weekly

| Check | Where |
|--------|--------|
| New users | Supabase → `users` |
| Match activity | Supabase → `match_runs` or Admin → **Matches** tab |
| Product feedback | Admin → **Feedback** or Supabase → `product_feedback` |
| Scholarship issue reports | Admin → **Reports** or Supabase → `scholarship_reports` |
| Errors | Hugging Face (or host) **Logs**; optional **Sentry** |
| Scraper runs | Admin → **System** → Recent scraper runs, or Supabase → `scraper_runs` |

## Admin UI

Log in as a user with `role = admin`. Open **`/admin`**.

- **Scholarships**: list / deactivate.
- **Users**: recent accounts (id, email, role).
- **Matches**: recent match runs (Philippine time shown where available).
- **Feedback**: submitted messages.
- **Reports**: pending scholarship issue reports.
- **System**: raw **`/health`** JSON (includes `scraper_last` when migrations are applied) + scraper run table.

## Logging

- Set **`STRUCTURED_LOGGING=true`** on the API for JSON logs (easier to search in HF/Render logs).
- Set **`SENTRY_DSN`** on API and **`VITE_SENTRY_DSN`** on the frontend if you use Sentry.

## Validate matches are saved

1. From the app, use **Find My Matches** on Search or **Find my matches** on the Dashboard.
2. In Supabase, open **`match_runs`** — a new row should appear with your `user_id`.
3. On the dashboard, **Match history** should list the run (newest first).

## Validate scrapers

1. GitHub → **Actions** → **Daily scholarship scrape** → latest run: must be green.
2. Check **`scraper_runs`** in Supabase for `philscholar` / `philscholar_ingest` rows.
3. Admin → **System** tab for a quick view.

## Debugging quick reference

| Symptom | What to check |
|---------|----------------|
| API down | Host status, `/health`, recent deploy |
| 401 / login | `SECRET_KEY`, `AUTH_DISABLED=false`, CORS |
| Empty matches | `scholarships` table, `is_active`, hard filters in logs |
| DB errors | Supabase logs, `DATABASE_URL` (prefer **pooler** on free tier) |
| CORS errors | `CORS_ORIGINS` must include exact Vercel origin (https, no trailing slash) |
