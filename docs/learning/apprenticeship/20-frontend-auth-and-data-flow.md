# Lesson 20 — Frontend Auth & Data Flow

> **Prerequisite:** [19 — Frontend Architecture](19-frontend-architecture-routing-state.md)

---

## AuthContext

[`frontend/src/contexts/AuthContext.tsx`](../../../frontend/src/contexts/AuthContext.tsx) is the **single source of truth** for session state.

### Storage keys

```typescript
const AUTH_TOKEN_KEY = "auth_token";
const AUTH_REFRESH_KEY = "auth_refresh_token";
```

Tokens in **localStorage** — survive page refresh.

### Login flow

1. `POST /api/v1/auth/login` with email/password
2. Store `access_token` + `refresh_token`
3. `fetchUser()` → `GET /api/v1/auth/me`
4. Dispatch `AUTH_USER_CHANGED_EVENT` — dashboards clear stale cache

### Token refresh

`tryRefreshAccessToken()` → `POST /api/v1/auth/refresh`

On 401 from `/me`, attempt refresh before logout.

### `authHeaders()`

```typescript
{ Authorization: `Bearer ${token}` }
```

Passed to all protected `apiFetch` calls.

---

## Profile builder draft

[`profileBuilderState.ts`](../../../frontend/src/components/profile-builder/profileBuilderState.ts)

- Key: `iskonnect_profile_draft`
- Saves multi-step form locally — user does not lose progress on refresh

**Tradeoff:** localStorage not encrypted — no highly sensitive docs in draft.

---

## Protected routes

Dashboard routes assume `AuthProvider` wrapped in `App.tsx`:

```typescript
<AuthProvider>
  <AppRoutes />
</AuthProvider>
```

Pages call `useAuth()` — if `!user && !loading`, redirect to `/login`.

---

## Email flows

| Page | API |
|------|-----|
| `VerifyEmailPage` | token in URL → verify endpoint |
| `ForgotPasswordPage` | request reset email |
| `ResetPasswordPage` | new password + token |

Cooldown messaging shown when rate limited (launch hardening).

---

## Logout

Clears tokens, user state, calls revoke if implemented, dispatches auth changed event.

---

## Common failures

| Symptom | Cause |
|---------|-------|
| Logged out on tab focus | Refresh token expired |
| Infinite loading | `/me` failing, network error |
| 403 on dashboard | Wrong user role |

---

## Exercises

### Level 1 — Understanding

1. Why dispatch `AUTH_USER_CHANGED_EVENT`?
2. Access vs refresh token storage?

### Level 2 — Implementation

1. Trace login button click → `AuthContext.login` → API in DevTools Network tab.

### Level 3 — Debugging

1. Clear localStorage — confirm app shows logged-out state.

### Level 4 — Architecture

1. Move tokens to httpOnly cookies — what changes on frontend and backend?

<details>
<summary>Solution</summary>

Event lets SavedScholarships and dashboard reset without prop drilling. Both tokens in localStorage today. httpOnly cookies: remove localStorage token reads, backend Set-Cookie on login, credentials: 'include' on fetch, CORS allow_credentials already true, CSRF token needed for POST.
</details>

---

*Previous: [19 — Frontend Architecture](19-frontend-architecture-routing-state.md) | Next: [21 — Tailwind, PWA & Performance](21-tailwind-pwa-virtualization-perf.md)*
