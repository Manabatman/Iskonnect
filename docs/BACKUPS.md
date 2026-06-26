# Database backups (Supabase)

Iskonnect does not run backups inside the application. Use Supabase (or your own schedule) before public launch.

## Option A — Supabase Point-in-Time Recovery (recommended for production)

1. Supabase Dashboard → **Project Settings** → **Database** → **Backups**.
2. Enable **Point-in-Time Recovery (PITR)** on a paid plan if available for your region.
3. Note the retention window (e.g. 7 days) and recovery procedure in the dashboard.

**Verify:** Dashboard shows PITR enabled and a recent backup timestamp.

## Option B — Manual `pg_dump` (free tier / extra safety)

Use the **direct** connection string (port **5432**, not the transaction pooler) from Supabase → Settings → Database.

```powershell
# Windows (requires PostgreSQL client tools installed)
$env:PGPASSWORD = "<database-password>"
pg_dump -h db.<PROJECT_REF>.supabase.co -p 5432 -U postgres -d postgres -Fc -f iskonnect-backup-$(Get-Date -Format yyyyMMdd).dump
```

```bash
# macOS / Linux
export PGPASSWORD="<database-password>"
pg_dump -h db.<PROJECT_REF>.supabase.co -p 5432 -U postgres -d postgres -Fc -f "iskonnect-backup-$(date +%Y%m%d).dump"
```

Store the `.dump` file off-site (encrypted cloud storage). **Never commit dumps to git.**

**Verify restore (staging only):** `pg_restore --clean --if-exists -d <staging_db> iskonnect-backup-YYYYMMDD.dump`

## Option C — GitHub Actions scheduled dump (advanced)

Add a weekly workflow that runs `pg_dump` using a GitHub secret `DATABASE_URL_DIRECT` (direct port 5432) and uploads the artifact with a short retention. See Supabase docs for connection limits before automating.

## Before launch checklist

- [ ] At least one backup method enabled (PITR or scheduled dump).
- [ ] You have tested restoring to a **non-production** database once.
- [ ] Database password and dump files are stored in a password manager / secure vault, not in the repo.

## What to back up

| Asset | Where |
|-------|--------|
| Postgres data | Supabase (`pg_dump` or PITR) |
| Env vars / secrets | Render + Vercel dashboards + password manager |
| Source code | GitHub (`main` branch) |

After a bad migration or data incident: restore DB from backup, then redeploy the last known-good API commit (see `docs/operations-handbook/07-operations.md`).
