# Lesson 22 — Frontend Testing

> **Prerequisite:** [21 — Tailwind, PWA & Performance](21-tailwind-pwa-virtualization-perf.md)

---

## Vitest + React Testing Library

### 1. Definition

- **Vitest** — Vite-native test runner (Jest-compatible API)
- **RTL** — renders components as users see them, queries by role/label

### 2. Config

[`vite.config.ts`](../../../frontend/vite.config.ts):

```typescript
test: {
  environment: "jsdom",
  setupFiles: "./src/test/setup.ts",
  globals: true,
}
```

[`frontend/src/test/setup.ts`](../../../frontend/src/test/setup.ts) — `@testing-library/jest-dom` matchers.

### 3. Command

```bash
cd frontend
npm test              # vitest run
npm test -- --watch   # development loop
```

---

## Existing auth page tests

Launch hardening added:

- [`ForgotPasswordPage.test.tsx`](../../../frontend/src/pages/ForgotPasswordPage.test.tsx)
- [`ResetPasswordPage.test.tsx`](../../../frontend/src/pages/ResetPasswordPage.test.tsx)
- [`VerifyEmailPage.test.tsx`](../../../frontend/src/pages/VerifyEmailPage.test.tsx)

Plus AuthContext tests for token refresh/expiry/logout.

**Why auth tests:** Registration/login bugs block all users — high blast radius.

---

## Mocking API

```typescript
vi.mock("../api/client", () => ({
  apiFetch: vi.fn(),
}));
```

Tests control `apiFetch` responses without hitting real backend.

---

## What to test on frontend

| Priority | Example |
|----------|---------|
| High | Auth flows, form validation messages |
| Medium | Guard redirects, error states |
| Lower | Pixel-perfect CSS |

**Do not** test implementation details (internal state variable names).

---

## CI integration

`.github/workflows/ci.yml` frontend job:

- Node 22
- `npm ci` in `frontend/`
- `npm run build`
- `npm test`

---

## Exercises

### Level 1 — Understanding

1. jsdom vs real browser?
2. Why mock apiFetch?

### Level 2 — Implementation

1. Run `npm test` — all green?

### Level 3 — Debugging

1. Test fails "not wrapped in router" — wrap with `MemoryRouter`.

### Level 4 — Architecture

1. Add test for LoginPage submit — outline arrange/act/assert steps.

<details>
<summary>Solution</summary>

jsdom: simulated DOM in Node, fast, incomplete browser APIs. Mock: isolate component from network. Arrange: render LoginPage with AuthProvider mock. Act: fill email/password, click submit. Assert: apiFetch called with POST /api/v1/auth/login.
</details>

---

*Previous: [21 — Performance](21-tailwind-pwa-virtualization-perf.md) | Next: [23 — CI/CD & Docker](23-ci-cd-and-docker.md)*
