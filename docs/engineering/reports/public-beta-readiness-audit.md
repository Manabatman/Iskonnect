# ISKONNECT Public Beta Readiness Audit

Date: 2026-08-03
Scope: full-stack production readiness review (accessibility, performance, security, error handling, release hygiene)
Method: static audit of `app/` and `frontend/`, plus live execution of the type, lint, unit, and backend test gates

---

## 0. Verified health signals (measured, not assumed)

| Gate | Command | Result |
| --- | --- | --- |
| Backend tests | `python -m pytest app/tests/ -q` | 694 passed, 2 skipped, coverage 72.63% (gate 70%) |
| Frontend unit tests | `npx vitest run` | 23 files, 69 tests, all passing |
| TypeScript | `npm run typecheck` | clean, 0 errors |
| ESLint | `npm run lint` | **FAILS** — 1 error, 33 warnings |

The engineering foundation is real. The problems found below are almost entirely in the
**release/asset layer**, not in application logic.

---

## 1. Critical Issues (must fix before public beta)

### C-1. Landing hero images are untracked in git — the first screen will 404 on deploy

`git status --porcelain frontend/public` reports:

```
?? frontend/public/images/hero/hero-desktop.png
?? frontend/public/images/hero/hero-mobile.png
?? frontend/public/images/hero/hero-tablet.png
AD frontend/public/images/hero/hero-1.jpg
```

All three hero files are **untracked**, so they exist only on the developer machine. Vercel builds
from the git repository, which means production serves `404` for every hero request.

Consumers of these exact paths:

- [frontend/index.html](frontend/index.html) lines 6-14 — three `<link rel="preload" as="image">` tags
- [frontend/src/constants/heroImages.ts](frontend/src/constants/heroImages.ts) lines 11, 17, 23
- [frontend/src/components/landing/HeroSection.tsx](frontend/src/components/landing/HeroSection.tsx) lines 13-27

Impact: the landing page renders white `text-white` headline copy over an empty image box with only
`HeroDirectionalOverlay` behind it, plus three failed network requests. This is the first thing every
new student sees and it is the single largest credibility risk in the audit.

`hero-1.jpg` is additionally in an inconsistent state (`AD` = staged for add, deleted from the
working tree) while the referenced auth fallback is `hero-1.svg`, which is tracked and present.

Fix: optimize the hero art (see C-2), commit the results, and add a build-time assertion that every
`preload` target in `index.html` resolves inside `dist/`.

### C-2. Hero and logo images are 10-36x over their documented budget

Actual bytes on disk versus the budget recorded in `docs/engineering/perf-baseline.md`:

- `images/hero/hero-mobile.png` — **2,889.8 KB**, 1587x2245, budget 80 KB (36x over)
- `images/hero/hero-desktop.png` — **2,648.0 KB**, 1920x1080, budget 120 KB (22x over)
- `images/hero/hero-tablet.png` — **1,105.9 KB**, budget 100 KB (11x over)
- `images/logo-dark.png` — **391.8 KB**, 1354x1251, tracked, ships today
- `images/logo-light.png` — **371.5 KB**, 1354x1236, tracked, ships today

Two compounding problems:

1. The hero is served as **PNG only**. There are no AVIF or WebP `<source>` entries, despite `sharp`
   already being a dependency and `npm run generate:hero-images` existing
   ([frontend/package.json](frontend/package.json) line 20, line 66). A photographic hero as PNG is
   the worst possible format choice.
2. All three are `rel="preload"` with `fetchPriority="high"`, so they sit directly on the LCP critical
   path. A mobile student on Philippine cellular data downloads 2.8 MB before the hero paints.

The logos render at roughly 32-40 px in the navbar but ship at 1354 px wide on every single page.
Combined logo weight is about 763 KB of pure waste per uncached visit.

Fix: generate AVIF + WebP at each breakpoint with a small PNG fallback, resize the logos to the
rendered size (plus 2x), and commit the results.

### C-3. `npm run lint` fails, which red-lights CI and blocks the deploy pipeline

```
4:3  error  'footerLegalLinks' is defined but never used  @typescript-eslint/no-unused-vars
1 error, 33 warnings
```

The unused import is at [frontend/src/components/Footer.test.tsx](frontend/src/components/Footer.test.tsx)
line 4. `npm run lint` exits non-zero, and `.github/workflows/ci.yml` runs `npm run lint` before
`npm run build`, so the entire verification job fails before it reaches the build and bundle-budget
gates. Nothing can be shipped through CI in this state.

Fix: remove the unused import (or assert on it in the test alongside the other three link groups).

### C-4. No favicon, no meta description, and the web manifest is never linked

[frontend/index.html](frontend/index.html) contains no `<link rel="icon">`, no
`<link rel="manifest">`, no `<meta name="description">`, and no Open Graph or Twitter card tags.
Consequences:

- Browsers request `/favicon.ico`, get a 404, and show the generic default icon in the tab and in
  bookmarks. For a platform whose core value proposition is trustworthiness, this reads as unfinished.
- `frontend/public/manifest.webmanifest` is tracked and valid but unreachable, and
  [frontend/vite.config.ts](frontend/vite.config.ts) line 61 sets `manifest: false`, so
  `vite-plugin-pwa` does not inject one either. A service worker is registered with no manifest, so
  install prompts and the app name/theme colour never apply.
- The manifest declares `/images/logo-light.png` as `"sizes": "512x512"`, but the file is actually
  1354x1236. The declaration is wrong even once it is linked.
- With no meta description or OG image, every link a student shares on Facebook or Messenger renders
  as a bare URL. For a beta that depends on organic student word-of-mouth, this materially suppresses
  reach.

---

## 2. High Priority Issues

### H-1. No CAPTCHA exists anywhere, and email verification is about to be switched off

A repo-wide search for `recaptcha`, `captcha`, `hcaptcha`, `turnstile`, and `grecaptcha` returns
**zero matches**. Today, mandatory email verification
(`REQUIRE_EMAIL_VERIFICATION`, [app/config.py](app/config.py) lines 120-124) is the only thing making
automated signup expensive. Setting it to `false` for beta removes that barrier and leaves only the
SlowAPI limit of `5/minute` on registration
([app/api/v1/auth_routes.py](app/api/v1/auth_routes.py)), which a single host can sustain for 7,200
accounts a day, and which trivially scales with rotating IPs.

Recommendation: Cloudflare Turnstile with server-side siteverify on `POST /auth/register`, gated by a
`TURNSTILE_SECRET_KEY` env var so the check is a no-op when unconfigured (keeps local dev and CI
green). Turnstile needs no Google account and is free at beta scale.

### H-2. A failed lazy chunk after deploy traps users in an unrecoverable error screen

[frontend/src/App.tsx](frontend/src/App.tsx) lazy-loads roughly 30 routes. There is no handler
anywhere for `ChunkLoadError` or `Failed to fetch dynamically imported module` (zero matches in
`frontend/`). The recovery button in
[frontend/src/components/ErrorBoundary.tsx](frontend/src/components/ErrorBoundary.tsx) line 47 only
calls `this.setState({ error: null })` — it re-renders the same broken tree without reloading, so the
error returns immediately and the user is stuck in a loop.

This is not theoretical: `vite-plugin-pwa` uses `registerType: "autoUpdate"` and precaches
`**/*.{js,css,html,...}` ([frontend/vite.config.ts](frontend/vite.config.ts) line 63). A student with
the old service worker active who navigates after a deploy requests hashed chunks that no longer
exist. Every deploy during beta is an opportunity to brick returning users.

Fix: make the boundary's recovery action call `window.location.reload()` when the caught error is a
chunk/module load failure.

### H-3. A missing production env var produces a totally blank page

[frontend/src/api/client.ts](frontend/src/api/client.ts) lines 5-8 throw at **module scope**:

```ts
if (_isProd && !_apiBase) {
  throw new Error("VITE_API_BASE_URL must be set in production builds. ...");
}
```

Because this runs during module evaluation, it fires before `ReactDOM.createRoot`, so nothing mounts
and no ErrorBoundary can catch it. A single misconfigured Vercel environment variable yields a pure
white screen with a developer-facing message visible only in the console. Given a beta launch will
involve environment changes, this failure mode is likely enough to matter.

Fix: keep the guard but render a static fallback into `#root` instead of throwing, or move the check
into `main.tsx` inside a try/catch that paints a human-readable message.

### H-4. Raw backend error strings and validation objects reach students

[frontend/src/constants/errorCopy.ts](frontend/src/constants/errorCopy.ts) lines 88-91 pass any
non-network `Error.message` straight through to the UI as long as it contains no dev-string marker:

```ts
const msg = err.message.trim();
if (msg && !containsDevString(msg)) return msg;
```

Since most call sites build their errors from the backend `detail` field, backend phrasing surfaces
verbatim. Confirmed paths include `ApplicationsPage.tsx` (lines 127, 137, 154, 159, 182, 192),
`DocumentsPage.tsx` (274, 299, 324), `ProfileDashboard.tsx` (224, 244), and
`ScholarshipSearchPage.tsx` (129, 134).

Worse, FastAPI returns `422` with `detail` as an **array of objects**, and
[frontend/src/pages/ProfileBuilderPage.tsx](frontend/src/pages/ProfileBuilderPage.tsx) line 239 assumes
a string. A validation failure while saving a profile renders `[object Object]` to the student. Only
the admin pages handle the array shape.

`SavedScholarshipsContext.tsx` line 66 leaks HTTP status codes into copy
(`"Could not load saved scholarships (403)."`).

### H-5. Session expiry redirects silently with no explanation

`ERROR_COPY.session_expired` exists but is never displayed.
[frontend/src/components/SessionExpiryHandler.tsx](frontend/src/components/SessionExpiryHandler.tsx)
lines 10-14 navigate to `/login` with no toast or banner. A student mid-way through a profile is
dropped onto the login screen with no stated reason, which reads as a bug or a data-loss event.

### H-6. CI has a JavaScript bundle gate but no image weight gate

[frontend/scripts/check-bundle-budget.mjs](frontend/scripts/check-bundle-budget.mjs) lines 13-17
enforces `entryJsGzipKb: 120`, `vendorJsGzipKb: 420`, `largestRouteChunkGzipKb: 180` — and those pass.
It inspects `dist/assets/*.js` only. This is precisely why 6.5 MB of images passed through every
green build unnoticed. The gate that exists created false confidence.

Fix: extend the script to assert total image weight and per-file caps under `dist/`, and to verify
that each `index.html` preload target exists.

---

## 3. Medium Priority Issues

### M-1. Three tables have RLS disabled

`organizations`, `field_evidence`, and `referral_click_daily` were created in migrations 038, 040, and
046 with plain `op.create_table` and never received `ENABLE ROW LEVEL SECURITY`. The blanket enable in
`alembic/versions/020_enable_rls_public_tables.py` lines 48-50 only covered tables existing at that
time, and `027_rls_sipp_tables.py` did the same for the SIPP set. No migration anywhere contains
`CREATE POLICY`.

Severity is medium, not critical, because of the architecture: RLS is not this application's
authorization layer. See section 8 for the full reasoning. Fix by adding a catch-up migration that
mirrors 020's loop, so the "enable RLS on every public table" invariant holds for new tables too.

### M-2. `fetchPriority` is a React 18 warning and the priority hint is silently dropped

[frontend/src/components/landing/HeroSection.tsx](frontend/src/components/landing/HeroSection.tsx)
line 21 uses camelCase `fetchPriority`, which React 19 supports but React 18.3.1 does not. The test
run emits:

```
Warning: React does not recognize the `fetchPriority` prop on a DOM element.
```

The attribute is dropped from the DOM, so the intended LCP priority hint never reaches the browser —
a performance fix that silently does nothing. Use lowercase `fetchpriority`.

### M-3. CSP is report-only and never enforced

[frontend/index.html](frontend/index.html) lines 17-19 ship a
`Content-Security-Policy-Report-Only` meta tag, and
[app/middleware/security_headers.py](app/middleware/security_headers.py) deliberately omits CSP so
that `/docs` keeps working. [frontend/vercel.json](frontend/vercel.json) contains only an SPA rewrite
and no `headers` block, so the SPA host sets no CSP, HSTS, or `X-Frame-Options` at all. Combined with
M-4, an XSS bug would be fully exploitable.

### M-4. Tokens live in `localStorage`

`auth_token` and `auth_refresh_token` are stored in `localStorage`
([frontend/src/contexts/AuthContext.tsx](frontend/src/contexts/AuthContext.tsx) lines 19-20, 154-167),
readable by any injected script. Mitigating factors are strong: no `dangerouslySetInnerHTML`,
`innerHTML`, `eval`, or `new Function` anywhere in the frontend, and all nine `target="_blank"` links
carry `rel="noreferrer"`. Acceptable for beta given refresh-token rotation and the `jti` denylist, but
it raises the cost of any future XSS and should be paired with an enforcing CSP.

### M-5. Password policy is length-only, with no lockout

Minimum 10 characters is the sole rule, server-side
([app/api/v1/auth_routes.py](app/api/v1/auth_routes.py) lines 51-56) and client-side. There is no
common-password denylist, no bcrypt 72-byte truncation guard, and no account lockout after repeated
failed logins — only the `10/minute` per-IP login limit. Weak passwords plus credential stuffing is a
realistic beta risk once verification is off.

### M-6. Unverified sessions survive once issued

The `403` check on unverified accounts exists only on `POST /auth/login`
([app/api/v1/auth_routes.py](app/api/v1/auth_routes.py) lines 267-273). `POST /auth/refresh`,
`GET /auth/me`, and every other protected route check JWT validity only. Accounts created during beta
(auto-verified) keep working indefinitely after verification is re-enabled, and any unverified user
holding a refresh token can extend their session forever. Plan the re-enable migration deliberately.

### M-7. Weak loading states on two main student routes

`OpportunityPlannerPage.tsx` lines 70-77 show a bare text line, and `ScholarshipSearchPage.tsx` lines
319-326 show a spinner rather than a skeleton. `DashboardShellSkeleton`
([frontend/src/components/LoadingSkeletons.tsx](frontend/src/components/LoadingSkeletons.tsx) lines
18-35) is defined but has zero usages, so the dashboard renders an empty shell during load instead of
the skeleton that was built for it.

### M-8. Sentry has no PII scrubbing on either side

Neither [frontend/src/lib/sentry.ts](frontend/src/lib/sentry.ts) nor the backend init in
[app/main.py](app/main.py) lines 111-120 defines `before_send`/`beforeSend`. Since student profiles
carry heavy PII (income, guardian details, GWA), an exception with request context attached could ship
that data to Sentry. The privacy page asserts no intentional PII collection, so this is also a policy
consistency gap.

### M-9. `503` handler leaks an internal exception string

[app/api/v1/scholarships.py](app/api/v1/scholarships.py) lines 361-362 raise
`HTTPException(status_code=503, detail=str(exc))`. The global 500 handler correctly scrubs and returns
a generic message with a `request_id`, but this path bypasses it. Admin-only, hence medium.

---

## 4. Low Priority Issues

- **L-1.** `frontend/public/landing/screenshots/*.webp` (four files, ~27 KB) are untracked and
  referenced nowhere in `src/`. Dead assets — delete or wire up.
- **L-2.** 33 ESLint warnings remain (`react-refresh/only-export-components`,
  `jsx-a11y/click-events-have-key-events`, `react-hooks/exhaustive-deps`). None are user-visible; the
  `exhaustive-deps` ones are worth reviewing for stale-closure bugs.
- **L-3.** Two React Router v7 future-flag warnings on every test run (`v7_startTransition`,
  `v7_relativeSplatPath`). Console noise; opt in when convenient.
- **L-4.** Vitest coverage thresholds are set to `lines: 14`, `statements: 14`
  ([frontend/vite.config.ts](frontend/vite.config.ts) lines 114-119). This is a floor-locking
  baseline, not a quality gate, and could mislead a future reader into thinking frontend coverage is
  enforced.
- **L-5.** `frontend/vercel.json` sets no `Cache-Control` headers, so non-hashed `public/` assets
  (logos, hero art) are revalidated on each visit instead of served from a long-lived immutable cache.
- **L-6.** `RegisterPage.tsx` shows only a top-level error banner, while `LoginPage.tsx` has proper
  inline per-field errors. Minor inconsistency in form error presentation.
- **L-7.** Two migration paths lack RLS wiring by convention rather than by enforcement; consider a
  test that asserts every table in `models.py` has RLS enabled.

---

## 5. What is genuinely solid

Worth stating plainly, because it is the majority of the system.

**Security architecture.** `app/config.py` `validate_for_production()` refuses to boot outside
development with a placeholder `SECRET_KEY`, `AUTH_DISABLED=true`, a SQLite `DATABASE_URL`,
localhost-only CORS, a missing `REDIS_URL`, `TRUST_PROXY_HEADERS=false`, or
`RUN_MIGRATIONS_ON_STARTUP=true`. Unset or unrecognised `ENVIRONMENT` is treated as production for
validation, which is the correct fail-safe direction. This is better than most production systems.

**Authentication.** bcrypt hashing, HS256 access tokens with `jti`, 48-byte refresh tokens stored as
SHA-256 hashes and rotated on use, a Redis `jti` denylist that **fails closed in production** when
Redis is unreachable, and full refresh-token revocation on password reset. `forgot-password` always
returns `200` to prevent account enumeration.

**Authorization.** `require_admin` ([app/auth.py](app/auth.py) lines 320-339) loads the user from the
database rather than trusting the JWT `role` claim, so roles cannot be spoofed client-side. The
frontend `AdminGuard`/`SponsorGuard`/`SchoolGuard` components are cosmetic routing only, which is the
correct division. `app/tests/test_authz_isolation.py` proves cross-user isolation on profiles,
applications, match runs, deletions, and saved scholarships.

**Rate limiting.** SlowAPI on all nine auth endpoints plus roughly 20 other route modules, Redis-backed
in production (mandatory via config guard) so limits are shared across workers, with separate
per-email cooldowns and daily caps in `app/utils/email_abuse.py`.

**Error plumbing.** A 70-second fetch timeout with `AbortController`, one automatic retry on
idempotent GET/HEAD only, automatic 401 refresh-and-replay, a global 500 handler that logs the
traceback server-side and returns only `{detail, request_id}`, nested ErrorBoundaries at app, dashboard,
search, public, and card level, a real 404 route, an offline banner, and a cold-start warmup banner
honestly calibrated to the 70-second timeout.

**Accessibility.** Wave 8 landed axe-core scans across 12 routes in CI, plus dedicated
`zoom-reflow.spec.ts` (200% and 400%) and `modal-focus.spec.ts` (focus trap, Escape, focus return)
suites, semantic `<fieldset>`/`<legend>` filter groups, combobox ARIA, `<ul>`/`<li>` notification
semantics, 44x44 px touch targets, and focus-visible rings on bottom nav. `<html lang="en">` is set.
The outstanding item is the manual screen-reader pass tracked in
`docs/engineering/a11y-manual-pass.md`.

**Input validation.** Every POST/PUT body in `app/api/` uses a Pydantic schema. No raw
`request.json()` or `dict = Body` handlers exist.

---

## 6. Accessibility verdict against WCAG AA

Automated coverage is unusually good for a pre-beta product, and I found no new violations in code
review. Two caveats:

1. **Hero text contrast is unverified in the failure case.** The `text-white` headline sits on
   `HeroDirectionalOverlay` plus the photo. With the photo 404ing (C-1), the effective background
   changes, so the measured contrast ratio no longer applies. Re-verify after C-1 lands.
2. **Screen-reader flow is still unverified by a human.** Automated axe catches roughly 30-40% of WCAG
   issues; announcement quality, focus-order sanity, and error-announcement clarity need the manual
   pass already scheduled.

Nothing here blocks a beta, provided the hero fix is verified for contrast afterward.

---

## 7. Production Readiness Score

- **UI/UX — 85/100.** Feature-complete, coherent design system, real error copy. Loses points for the
  broken hero, missing favicon, and bare social previews.
- **Accessibility — 88/100.** Strong automated coverage in CI; manual SR pass outstanding.
- **Reliability — 80/100.** Excellent error plumbing, undermined by the chunk-load trap (H-2) and the
  blank-page env failure mode (H-3).
- **Performance — 55/100.** JS budgets enforced and passing; images are 10-36x over budget, on the LCP
  critical path, and ungated by CI. Weakest dimension by a wide margin.
- **Security — 82/100.** Genuinely strong config guards, token handling, and authorization. Loses
  points for no CAPTCHA once verification is off, report-only CSP, and the three RLS gaps.
- **Mobile Experience — 72/100.** Good responsive work and touch targets, but a 2.8 MB preloaded
  mobile hero is a serious failure on Philippine cellular data.
- **Code Quality — 88/100.** 694 backend tests at 72.6% coverage, 69 frontend tests, clean typecheck,
  ADRs, design tokens, CI gates. Loses points for the lint error that breaks CI.

**Overall: 78/100.**

---

## 8. Answer: are the GitHub/Supabase warnings caused by the admin panel?

**No.** They are not caused by the admin panel, or by any application code path.

The browser never talks to Supabase's database. `frontend/package.json` has no `@supabase/*`
dependency, and repo-wide searches for `createClient`, `SUPABASE_ANON`, and `VITE_SUPABASE` in
`frontend/` return nothing. `frontend/.env` contains only `VITE_API_BASE_URL`. The admin panel is no
different from any other page — `AdminPage.tsx` calls `apiFetch("/api/v1/admin/...")` against FastAPI.

The backend reaches Postgres through SQLAlchemy + psycopg2 using `DATABASE_URL` as the `postgres`
owner role ([app/db.py](app/db.py) lines 21-25). **Table owners bypass RLS** unless
`FORCE ROW LEVEL SECURITY` is set, which it is not. So RLS is not, and was never, this application's
authorization layer. `require_admin` and the per-route ownership checks are — and they are backed by
`app/tests/test_authz_isolation.py`. This posture is deliberate and documented in
`docs/engineering/adr/ADR-009-rls-posture.md`.

Supabase's Security Advisor performs static analysis on the database. It is describing what would be
reachable **if** someone used the Supabase anon/publishable key against PostgREST directly. Mapping
that to your specific warnings:

- **"RLS disabled" on `organizations`, `field_evidence`, `referral_click_daily`** — the only finding
  with substance. These three were created after migration 020's blanket enable and were missed. If
  the anon key were ever obtained or added to a frontend env, these would be readable and possibly
  writable through PostgREST. The data is low-sensitivity (provider names/logos, catalog field
  provenance, aggregate click counts with no PII), which is why this is M-1 rather than critical. Fix
  it anyway; it closes the hole cheaply and restores the invariant.
- **"Public/signed-in users can see object in GraphQL schema"** — informational. Your reading is
  correct: schema visibility is not data access. Additionally, GraphQL is **not used anywhere** —
  `graphql`, `pg_graphql`, and `/graphql` all return zero matches repo-wide. Disabling the Supabase
  Data API entirely is therefore a free hardening step with no application impact, and it makes this
  whole warning class disappear rather than requiring per-table triage.
- **`pg_trgm` extension in public** — ignore, as you concluded. Standard fuzzy-search extension,
  relocating it risks breaking search for no security gain.
- The pre-020 tables (`users`, `students`, `applications`, `match_results`, `notifications`,
  `audit_logs`, and so on) **do** have RLS enabled with **no policies**, which is deny-all for
  `anon`/`authenticated` through PostgREST while the owner-role backend continues to work. That is a
  coherent configuration, not an oversight.

One genuinely higher-risk item that the advisor does not flag: `SUPABASE_SERVICE_ROLE_KEY` is used
server-side for Storage uploads ([app/storage/supabase_storage.py](app/storage/supabase_storage.py)
lines 48-56, 76-80). That key bypasses everything. It is correctly server-only today and never
reaches the bundle — keep it that way, and never add an anon key to Vercel.

---

## 9. Answer: the email verification bypass for beta

Good news: **this requires no code change.** The flag already exists and is already wired end to end.

```120:124:app/config.py
    # When false, users can sign in without verifying email (beta testing). SMTP not required in production.
    require_email_verification: bool = Field(
        default=True,
        validation_alias="REQUIRE_EMAIL_VERIFICATION",
    )
```

Setting `REQUIRE_EMAIL_VERIFICATION=false` in the production environment:

- Auto-verifies new accounts and returns tokens immediately at registration
  ([app/api/v1/auth_routes.py](app/api/v1/auth_routes.py) lines 202-225).
- Skips the login `403` ([app/api/v1/auth_routes.py](app/api/v1/auth_routes.py) lines 267-273).
- Drops the SMTP and production-`FRONTEND_URL` startup requirements
  ([app/config.py](app/config.py) lines 251-263) and logs a warning instead of erroring.
- Hides the dashboard verification banner, since the frontend keys off
  `user.requireEmailVerification` ([frontend/src/pages/ProfileDashboard.tsx](frontend/src/pages/ProfileDashboard.tsx)
  lines 372-377).

The verification infrastructure stays fully intact: the token generator, the verify endpoint, the
resend endpoint, `/verify-email`, and the `email_verified` column are all untouched. Password hashing,
token issuance, protected routes, and every authorization check are unaffected. `app/tests/test_auth_extended.py`
already covers both flag states.

**What must change back for production:** set `REQUIRE_EMAIL_VERIFICATION=true`, configure
`SMTP_HOST` and `EMAIL_FROM`, point `FRONTEND_URL` at the real domain, and decide what to do about
the cohort of beta accounts that were auto-verified — they will remain `email_verified=true` and will
never be prompted (see M-6). A backfill setting beta-era rows to `email_verified=false` is the honest
choice, but it will lock out real users, so it needs a communication plan.

**What is missing:** the abuse protection that verification was implicitly providing. See H-1 —
Cloudflare Turnstile on registration with server-side siteverify, behind a `TURNSTILE_SECRET_KEY`
that no-ops when unset. The beta notice copy requested is also not yet present anywhere in
`RegisterPage.tsx`.

---

## 10. Final Verdict

### Ready with Minor Fixes

Not "Ready for Public Beta" as it stands: deploying the current `main` produces a landing page with a
broken hero image, and CI cannot go green because of a one-line lint error.

Not "Not Ready" either, and this distinction matters. Every critical finding is a **mechanical release
hygiene fix** — commit optimized images, delete an unused import, add four `<link>`/`<meta>` tags to
`index.html`. None require redesign, new features, refactoring, or architectural change. Total effort
is measured in hours.

The evidence for the underlying system being sound: 694 backend tests passing at 72.6% coverage with a
41-persona matching suite and a recall/precision regression gate; 69 frontend tests passing; a clean
typecheck; axe scans across 12 routes plus zoom/reflow and modal-focus suites in CI; production config
guards that refuse to boot insecurely; refresh-token rotation with a fail-closed revocation denylist;
and proven cross-user isolation. The application logic, matching engine, and security architecture are
beta-grade.

**Would a first-time student trust this platform?** After C-1 through C-4, yes. Before them, no — a
broken hero image and a default browser favicon on the first screen undermine trust before a single
feature is evaluated.

**Are there blockers that could damage credibility?** Yes, four, all in the release layer, all listed
in section 1.

**Is the application stable enough for public testing?** Yes. The gap is presentation and release
hygiene, not stability.

Ship the four criticals plus H-1, H-2, and H-3, then launch.
