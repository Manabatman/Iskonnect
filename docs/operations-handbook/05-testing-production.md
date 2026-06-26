# Part 5 — Testing Production

> Systematic test procedures for every critical user journey — with expected outcomes, failure symptoms, logs, and debug commands.

Run these after every deploy and before announcing launch.

---

## Test environment setup

| Item | Value |
|------|-------|
| Frontend URL | Your Vercel or custom domain |
| API URL | Your Render or `api.` subdomain |
| Test email | Use a real inbox you control (not `test@test.com`) |
| Admin account | Created via `create_admin` script |
| Browser | Chrome/Edge with DevTools open (F12) |

**Keep a test log:**

```
Date: ____
Deploy: commit SHA ____
Tester: ____
Results: PASS/FAIL per section
```

---

## 1. Registration

### What we're testing
New user can create an account.

### Procedure
1. Open `/register`
2. Enter email + password (8+ chars)
3. Submit

### Expected outcome
- HTTP 200/201 from `POST /api/v1/auth/register`
- Redirect to dashboard or verification prompt
- Row in `users` table
- Verification email sent (if SMTP configured)

### curl test
```powershell
curl.exe -s -X POST https://YOUR_API/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"newuser@example.com","password":"SecurePass123!"}'
```

For register, use `/api/v1/auth/register` with same body shape.

### Failure symptoms
| Symptom | Likely cause |
|---------|--------------|
| 422 validation error | Password too short |
| 500 error | DB down; check `/health` |
| No email | SMTP misconfig; email abuse cap |
| Generic success but no user | Check Render logs for IntegrityError |

### Logs to inspect
- Render: `register`, `smtp`, `email_abuse`
- Sentry: unhandled exceptions on auth routes

### Debug commands
```sql
SELECT id, email, email_verified, created_at FROM users WHERE email = 'newuser@example.com';
```

---

## 2. Login

### Procedure
1. Open `/login`
2. Enter credentials
3. Submit

### Expected outcome
- `access_token` + `refresh_token` in response
- `localStorage` contains tokens
- Dashboard loads

### Verify in DevTools
Application → Local Storage → look for token keys used by `AuthContext`.

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| 401 Invalid credentials | Wrong password |
| 401 after deploy | `SECRET_KEY` changed — all old tokens invalid |
| Network error | CORS, cold start, wrong API URL |

### curl test
```powershell
curl.exe -s -X POST https://YOUR_API/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@yourdomain.com","password":"YourPass"}'
```

---

## 3. Email verification

### Procedure
1. Register new user
2. Open email link (`FRONTEND_URL/verify-email?token=...`)
3. Confirm success message

### Expected outcome
- `users.email_verified = true` in DB
- User can access features requiring verification (if enforced)

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| Link 404 | Wrong `FRONTEND_URL` |
| Token invalid | Expired token; clock skew |
| No email | SPF/DKIM; abuse cap; SMTP auth fail |

### Debug
```sql
SELECT email, email_verified FROM users WHERE email = '...';
```

Render logs: `send_email_verification_email`

### Email abuse limits (Redis)
- 1 email per purpose per 5 minutes per address
- 5 per purpose per day per address
- 2000 global per day

**Test cooldown:** Rapid resend should return non-enumerating message, not flood inbox.

---

## 4. Password reset

### Procedure
1. `/forgot-password` → enter email
2. Open reset link in email
3. Set new password
4. Login with new password

### Expected outcome
- Always returns generic message (no email enumeration)
- Reset link works once
- Old password rejected

### curl forgot-password
```powershell
curl.exe -s -X POST https://YOUR_API/api/v1/auth/forgot-password `
  -H "Content-Type: application/json" `
  -d '{"email":"user@example.com"}'
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| No email | SMTP; abuse cap |
| Token expired | Default TTL elapsed |
| 400 on reset | Password < 8 chars |

---

## 5. Profile builder and save

### Procedure
1. Login as student
2. Complete profile builder (education, region, income, etc.)
3. Save

### Expected outcome
- `POST/PATCH /api/v1/profiles/...` returns 200
- `students` row updated
- Dashboard shows profile completeness

### Verify DB
```sql
SELECT id, user_id, education_level, region, income_bracket FROM students WHERE user_id = <id>;
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| 403 | Token invalid; wrong user |
| 422 | Validation error — check response body |

---

## 6. Scholarship matching

### Procedure
1. Ensure profile is sufficiently complete
2. Click **Find My Matches** (dashboard or search)
3. Wait for results page

### Expected outcome
- `POST /api/v1/matches/{profile_id}` returns 200
- `match_runs` row created with JSON results
- Results ranked by score with explanations

### Verify DB
```sql
SELECT id, student_id, created_at, jsonb_array_length(results::jsonb) AS match_count
FROM match_runs ORDER BY created_at DESC LIMIT 1;
```

### Verify API (with token)
```powershell
curl.exe -s -X POST https://YOUR_API/api/v1/matches/1 `
  -H "Authorization: Bearer TOKEN" `
  -H "Content-Type: application/json"
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| Empty matches | No active scholarships; all hard-filtered |
| 500 error | Bug in match_service; check Sentry |
| Very slow | Cold start + large catalog; Redis cache cold |
| 403 | User doesn't own profile |

### Logs
Render: `match`, `hard_filter`, `scoring`

---

## 7. Scholarship search

### Procedure
1. Navigate to `/scholarships/search`
2. Enter query; apply filters
3. Paginate

### Expected outcome
- `GET /api/v1/scholarships/search?q=...` returns paginated results
- Only `is_active=true` scholarships (unless admin)

### Verify
```powershell
curl.exe -s "https://YOUR_API/api/v1/scholarships/search?q=ched&limit=5"
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| Empty results | No data; all expired |
| Stale results after admin edit | Redis cache TTL 300s — wait or invalidate |

---

## 8. Admin approval (staging)

### What we're testing
Scraped/imported scholarships flow through human approval.

### Procedure
1. Login as **admin** user
2. Navigate to `/admin` → Staging tab
3. Review pending row → **Approve**

### Expected outcome
- `POST /api/v1/scholarships/staging/{id}/approve` → 200
- Row moves from `scholarships_staging` (status `approved`) to new `scholarships` row
- Scholarship appears in search
- Cache invalidated

### Verify DB
```sql
SELECT id, title, status FROM scholarships_staging WHERE status = 'pending' LIMIT 5;
SELECT id, title, is_active FROM scholarships ORDER BY created_at DESC LIMIT 5;
```

### Reject test
- Reject a staging row → status `rejected`; no live row created

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| 403 on admin routes | User role not `admin` |
| Approve 500 | Invalid payload in staging JSON |
| Approved but not in search | `is_active=false`; cache delay |

### Files involved
- `app/api/v1/scholarship_staging.py` — approve/reject endpoints
- `app/scholarship_cache.py` — invalidation on approve

---

## 9. Scraping pipeline

### Manual trigger test
1. GitHub → Actions → **Scholarship scrape and ingest** → **Run workflow**
2. Wait for completion (~5–15 min)

### Expected outcome
- Workflow green ✓
- `data/raw/philscholar_YYYY-MM-DD.json` created (in CI artifact or logs)
- New `scholarships_staging` rows OR skip if listing unchanged (`.skip` file)
- `scraper_runs` row logged
- `/health` → `scraper_last` updated

### Verify
```powershell
curl.exe -s https://YOUR_API/health
```

```sql
SELECT source, status, records_found, started_at FROM scraper_runs ORDER BY started_at DESC LIMIT 3;
SELECT COUNT(*) FROM scholarships_staging WHERE status = 'pending';
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| Workflow red | Missing `DATABASE_URL` secret |
| 0 new staging rows | All duplicates; listing unchanged |
| Scraper timeout | PhilScholar HTML structure changed |

### Logs
GitHub Actions step logs for `scrape_philscholar` and `ingest_scraped`

---

## 10. Scoring correctness

### What we're testing
Scores are deterministic and explained.

### Procedure
1. Run matches for a profile with known attributes (e.g. NCR, STEM, low income)
2. Inspect top match `breakdown` and `explanation` fields

### Expected outcome
- Scores between 0–100 (or documented range)
- `breakdown` shows components: academic, income, field_alignment, geographic, equity_priority
- Weights sum per [app/scoring/config.py](../../app/scoring/config.py):
  - academic 0.30, income 0.28, field_alignment 0.22, geographic 0.10, equity_priority 0.10

### Regression test (local/CI)
```powershell
python -m pytest app/tests/test_scoring_engine.py -v
python -m pytest app/tests/test_match_service_integration.py -v
```

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| All scores identical | Profile data missing |
| Unexpected zero | Hard filter eliminated; check diagnostics |
| Scores changed after deploy | Weight config or GWA normalization change |

---

## 11. Authorization (cross-user access)

### What we're testing
User A cannot access User B's data.

### Automated tests (CI)
```powershell
python -m pytest app/tests/ -k authz -v
```

### Manual procedure
1. Login as User A; note `profile_id`, create match run
2. Login as User B
3. Attempt `GET /api/v1/profiles/{A_profile_id}` with B's token

### Expected outcome
- **403 Forbidden** or **404 Not Found** (non-enumerating)

### Endpoints to test
| Endpoint | Must deny cross-user |
|----------|---------------------|
| `/api/v1/profiles/{id}` | Yes |
| `/api/v1/applications/...` | Yes |
| `/api/v1/match-runs/...` | Yes |
| `/api/v1/saved-scholarships/...` | Yes |
| `/api/v1/documents/...` | Yes |

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| 200 with other user's data | **Critical security bug** — stop traffic, fix immediately |

---

## 12. Rate limiting

### What we're testing
API rejects excessive requests per IP.

### Configuration
- `app/limiter.py` — slowapi with Redis storage
- `TRUST_PROXY_HEADERS=true` — uses real client IP behind Render

### Procedure
Rapid-fire requests to a limited endpoint (e.g. login):

```powershell
1..20 | ForEach-Object {
  curl.exe -s -o NUL -w "%{http_code}`n" -X POST https://YOUR_API/api/v1/auth/login `
    -H "Content-Type: application/json" `
    -d '{"email":"test@example.com","password":"wrong"}'
}
```

### Expected outcome
- First N requests: 401 (wrong password)
- Eventually: **429 Too Many Requests**

### Failure symptoms
| Symptom | Cause |
|---------|-------|
| Never 429 | Redis not connected; `memory://` per worker |
| Everyone blocked | Shared IP (corporate NAT); tune limits |

### Verify Redis
`/health` → `cache: true`

---

## 13. Saved scholarships and applications

### Procedure
1. From match results, save a scholarship
2. Check dashboard saved list
3. Create application record (if using application flow)

### Expected
- Sort by newest saved first
- Cross-user access denied (authz tests)

---

## 14. Cold start UX

### Procedure
1. Wait 15+ minutes with no API traffic (free Render)
2. Load dashboard

### Expected
- "Connecting to server…" banner may appear briefly
- Request completes within 30s (`FETCH_TIMEOUT_MS` in client.ts)

### Failure
- Timeout error → consider paid Render or uptime ping

---

## Production smoke test checklist (printable)

```
REGISTRATION     [ ] PASS  [ ] FAIL  Notes: ___________
LOGIN            [ ] PASS  [ ] FAIL  Notes: ___________
EMAIL VERIFY     [ ] PASS  [ ] FAIL  Notes: ___________
PASSWORD RESET   [ ] PASS  [ ] FAIL  Notes: ___________
PROFILE SAVE     [ ] PASS  [ ] FAIL  Notes: ___________
MATCHING         [ ] PASS  [ ] FAIL  Notes: ___________
SEARCH           [ ] PASS  [ ] FAIL  Notes: ___________
ADMIN APPROVE    [ ] PASS  [ ] FAIL  Notes: ___________
SCRAPER (manual) [ ] PASS  [ ] FAIL  Notes: ___________
AUTHZ            [ ] PASS  [ ] FAIL  Notes: ___________
RATE LIMIT       [ ] PASS  [ ] FAIL  Notes: ___________
/health          [ ] PASS  [ ] FAIL  Notes: ___________
```

---

*Previous: [Part 4 — Domains and DNS](04-domains-and-dns.md) · Next: [Part 6 — Data Pipeline](06-data-pipeline.md)*
