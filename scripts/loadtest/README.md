# ISKONNECT read-path load test

Scripts for Phase 4 public beta validation.

## Quick start (Python — no extra deps)

```bash
# Warm the instance first (Render free tier sleeps after ~15 min idle)
curl -fsS https://YOUR_API.onrender.com/health

python scripts/loadtest/read_paths.py \
  --base-url https://YOUR_API.onrender.com \
  --users 30 50 100 \
  --report scripts/loadtest/results.json
```

## k6 (optional)

```bash
k6 run -e BASE_URL=https://YOUR_API.onrender.com scripts/loadtest/read_paths.k6.js
```

## What it measures

- Virtual user ramps at 30, 50, and 100 concurrent sessions
- Read paths: `/health`, search, list, detail
- 1.5 s think time between requests per user
- Outputs avg latency, p95, error rate to `results.json`

## 2026-07-26 run notes

A run against `https://iskonnect-api.onrender.com` returned **HTTP 404** on all paths during this session. Set the GitHub `RENDER_API_URL` secret to your live Render service URL (see Render dashboard → Web Service → URL) and re-run after deploying. The script and k6 file are ready; results must be re-captured against the warmed production host.

When the API is reachable, also watch during ramps:

- Render CPU / memory (dashboard)
- Supabase pooler connections
- slowapi rate-limit rejections (429s are not capacity failures)

## 30-person university session

If the 30-user ramp shows **error rate ≤ 1%** and **p95 ≤ 3000 ms** on a warmed instance, a concurrent read-only demo session is likely acceptable on the free tier. Match/write endpoints were not load-tested here.
