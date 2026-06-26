# Lesson 18 — React, Vite & TypeScript

> **Prerequisite:** [17 — Backend Testing](17-backend-testing-philosophy.md)

---

## Concept: Single Page Application (SPA)

### 1. Definition

An **SPA** loads one HTML shell; JavaScript swaps page content without full server round-trips.

### 2. Why for Iskonnect

Fast navigation between dashboard, matches, search — feels like an app.

### 3. Before SPAs

Each click = new HTML page from server (traditional PHP/Django).

### 4. Tradeoff

Initial JS bundle download; SEO needs care (landing pages are still crawlable).

---

## React

### 1. Definition

**React** builds UI from **components** — functions returning JSX.

### 2. Bootstrap — [`frontend/src/main.tsx`](../../../frontend/src/main.tsx)

```typescript
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

`StrictMode` double-invokes effects in dev to catch bugs.

Sentry init runs before render if `VITE_SENTRY_DSN` set.

---

## TypeScript

Adds **static types** — catches `profile.gwa_raw` typos at compile time.

```typescript
interface AuthUser {
  id: number;
  email: string;
  role: string;
  emailVerified: boolean;
}
```

Shared types often mirror backend schemas in [`frontend/src/types.ts`](../../../frontend/src/types.ts).

---

## Vite

### 1. Definition

**Vite** is a dev server + production bundler. Uses native ES modules in dev for instant HMR.

### 2. Commands

```bash
cd frontend
npm install          # read package.json, download node_modules
npm run dev          # vite dev server :5173
npm run build        # production bundle → dist/
npm run preview      # serve dist locally
```

| Command | Internal action |
|---------|-----------------|
| `npm install` | Reads `package-lock.json`, installs deps to `node_modules/` |
| `npm run dev` | Starts Vite, watches files, HMR |
| `npm run build` | Tree-shakes, minifies to `dist/` |

### 3. [`vite.config.ts`](../../../frontend/vite.config.ts)

- `@vitejs/plugin-react-swc` — fast React compile
- `vite-plugin-pwa` — service worker (lesson 21)
- `test` block — Vitest config

---

## Component hierarchy

```
main.tsx → App.tsx → Providers (Theme, Auth, Saved) → Router → Pages
```

**Pages** ([`frontend/src/pages/`](../../../frontend/src/pages/)) — route-level screens.

**Components** ([`frontend/src/components/`](../../../frontend/src/components/)) — reusable UI.

---

## Lazy loading

`App.tsx` uses `React.lazy()` for heavy pages (MatchResults, Admin) — smaller initial bundle.

```typescript
const MatchResultsPage = lazy(() => import("./pages/MatchResultsPage").then(...));
```

Wrapped in `<Suspense fallback={<RouteFallback />}>`.

---

## Exercises

### Level 1 — Understanding

1. SPA vs multi-page?
2. What does HMR do?

### Level 2 — Implementation

1. Create trivial component, import in `LandingPage`.

### Level 3 — Debugging

1. `npm run build` fails on TS error — read error, fix type.

### Level 4 — Architecture

1. Why lazy-load Admin pages but not Login?

<details>
<summary>Solution</summary>

SPA: client routing. HMR: hot module replacement without full reload. Admin rarely needed on first visit — code-split reduces landing page load time.
</details>

---

*Previous: [17 — Backend Testing](17-backend-testing-philosophy.md) | Next: [19 — Frontend Architecture](19-frontend-architecture-routing-state.md)*
