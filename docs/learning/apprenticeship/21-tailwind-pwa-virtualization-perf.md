# Lesson 21 — Tailwind, PWA, Virtualization & Performance

> **Prerequisite:** [20 — Frontend Auth & Data Flow](20-frontend-auth-and-data-flow.md)

---

## Tailwind CSS

### 1. Definition

**Utility-first CSS** — compose styles from classes like `flex`, `px-4`, `dark:bg-slate-900`.

### 2. Why

Fast iteration, consistent spacing, dark mode via `dark:` variant ([`ThemeContext`](../../../frontend/src/contexts/ThemeContext.tsx)).

### 3. Config

[`frontend/tailwind.config.js`](../../../frontend/tailwind.config.js) — content paths, theme extensions.

[`frontend/src/index.css`](../../../frontend/src/index.css) — `@tailwind` directives.

---

## Virtualization

### Problem

[`MatchResultsPage.tsx`](../../../frontend/src/pages/MatchResultsPage.tsx) can render hundreds of match cards — O(n) DOM nodes → slow on mobile.

### Solution

`@tanstack/react-virtual` — only render visible rows in scroll viewport.

**Before:** 500 scholarships = 500 DOM subtrees.
**After:** ~15 visible rows + buffer.

---

## PWA (Progressive Web App)

[`vite.config.ts`](../../../frontend/vite.config.ts) — `vite-plugin-pwa`

- **Service worker** caches static assets (JS, CSS, HTML)
- **Runtime cache** `NetworkFirst` for `/api/v1/scholarships` — offline catalog fallback

```typescript
handler: "NetworkFirst",
networkTimeoutSeconds: 8,
```

**Analogy:** Service worker is a **waiter with a photocopy** of the menu — if kitchen (network) is slow, serve last copy.

**Limitation:** Auth endpoints not cached — security.

---

## Payload slimming

Backend list endpoints return minimal fields; detail pages fetch full scholarship.

Frontend [`types.ts`](../../../frontend/src/types.ts) should distinguish list vs detail shapes.

---

## Performance checklist

| Technique | Where |
|-----------|-------|
| Code splitting | `React.lazy` in App.tsx |
| Debounced search | `useDebounce` |
| API timeout + retry | `client.ts` |
| Virtual lists | MatchResults, large grids |
| Scholarship cache | Backend Redis 300s TTL |

---

## Exercises

### Level 1 — Understanding

1. NetworkFirst vs CacheFirst?
2. Why virtualize lists?

### Level 2 — Implementation

1. Enable Lighthouse PWA audit on production build.

### Level 3 — Debugging

1. Stale scholarship after admin edit — cache layers to invalidate?

### Level 4 — Architecture

1. Design IndexedDB layer for offline profile draft — pros/cons vs localStorage.

<details>
<summary>Solution</summary>

NetworkFirst: try network, fall back to cache — good for catalog freshness. Virtualize: constant DOM size. Invalidate: backend invalidate_scholarship_cache + PWA maxAge. IndexedDB: larger quota, structured data, async API — more complex than localStorage for draft JSON.
</details>

---

*Previous: [20 — Frontend Auth](20-frontend-auth-and-data-flow.md) | Next: [22 — Frontend Testing](22-frontend-testing.md)*
