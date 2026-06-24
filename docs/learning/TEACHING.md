# Iskonnect — Teaching Documentation

This document explains how the Iskonnect frontend is structured, how to edit it safely, and how it talks to the backend. Use it alongside the code in `scholarship-match/frontend/`.

---

## 1. File structure (what lives where)

| Area | Path | Role |
|------|------|------|
| App entry | `frontend/src/main.tsx` | Mounts React to `#root`, imports global CSS. |
| Routing | `frontend/src/App.tsx` | Defines all routes (`BrowserRouter`, `Routes`, `Route`). |
| API client | `frontend/src/api/client.ts` | `apiFetch()` — base URL, timeout, retry, error logging. |
| Auth | `frontend/src/contexts/AuthContext.tsx` | Login, register, token storage, `authHeaders()` for protected calls. |
| Theme | `frontend/src/contexts/ThemeContext.tsx` | Light / dark / system; toggles `class="dark"` on `<html>`. |
| Types | `frontend/src/types.ts` | TypeScript shapes for API responses (do not rename fields used by the API). |
| Pages | `frontend/src/pages/*.tsx` | One file per route screen (e.g. `LandingPage`, `LoginPage`, `ProfileDashboard`). |
| Shared UI | `frontend/src/components/*.tsx` | Reusable pieces (e.g. `ScholarshipCard`, `HeroCarousel`). |
| Layout | `frontend/src/components/layout/*.tsx` | Public navbar, dashboard sidebar/topbar. |
| Global styles | `frontend/src/index.css` | Tailwind layers + custom utilities (e.g. glassmorphism). |
| Tailwind config | `frontend/tailwind.config.js` | Colors, fonts, animations, content paths. |
| Static assets | `frontend/public/` | Images referenced as `/images/...` (not bundled by Vite). See `public/images/README.txt`. |
| Hero carousel config | `frontend/src/constants/heroImages.ts` | Image paths and interval for the landing page carousel. |

**Mental model:** `App.tsx` picks a layout and a page. Pages load data with `apiFetch` + `authHeaders()` and pass plain objects into components as **props**.

---

## 2. How to edit (what controls what)

- **Route URL → page component:** Open `App.tsx` and find the `<Route path="..." element={...} />` line. Change `path` or `element` to point at a different page.
- **Copy on a page:** Edit the JSX in the matching `pages/*.tsx` file — headings, paragraphs, buttons are usually plain text or Tailwind `className` strings.
- **Colors:** Prefer `tailwind.config.js` (`theme.extend.colors`) and optional CSS variables in `index.css`. Use `bg-primary-600`, `text-slate-700`, `dark:` variants for dark mode.
- **Images in `public/`:** Put files under `public/images/` and reference them as `src="/images/your-file.png"`. Change the file on disk and keep the same filename, or update the `src` path in JSX.
- **Component-specific layout:** The outer `className` on the root `<div>` or `<section>` of a page usually controls max width (`max-w-6xl`), padding (`px-4`), and vertical spacing (`py-12`).

When you change **API field names** in TypeScript or in the UI, the app can break silently. Prefer **display-only** mapping (formatting dates, rounding numbers) unless the backend contract changes.

---

## 3. Core concepts

### React components and props

A **component** is a function that returns JSX. **Props** are inputs:

```tsx
function HeroCarousel({ images }: { images: string[] }) {
  return <img src={images[0]} alt="" />;
}
```

Parent passes data: `<HeroCarousel images={['/images/hero/hero-1.jpg']} />`.

### `useState` (local UI state)

Use for things that change on the client without a new API call: open/closed panels, current carousel index, form fields.

```tsx
const [index, setIndex] = useState(0);
```

### `useEffect` (side effects)

Runs after render. Common uses: **syncing to URL**, **timers**, **fetching data** when dependencies change.

```tsx
useEffect(() => {
  const id = window.setInterval(() => setIndex((i) => (i + 1) % 3), 5000);
  return () => window.clearInterval(id);
}, []);
```

Always **clear intervals** in the cleanup function to avoid leaks.

### Tailwind utility classes

Classes like `flex`, `gap-4`, `rounded-2xl`, `bg-white/70` map to CSS. You compose them in `className` without writing separate CSS files for every element.

### Glassmorphism

Typically: semi-transparent background + blur + light border:

- `backdrop-blur-xl bg-white/70 border border-white/20`
- Dark mode: `dark:bg-slate-800/60 dark:border-white/10`

Defined once in `index.css` as `.glass` / `.glass-dark` for consistency.

### Image carousel with `setInterval`

- Store **current slide index** in `useState`.
- In `useEffect`, start `setInterval` every 5000 ms (5 seconds) to advance the index (wrap with modulo for a loop).
- For a **white fade**: animate **opacity** of the active image and/or a white overlay layer with CSS `transition` (e.g. `transition-opacity duration-500`), or use discrete “phase” state (fade out → white → fade in next image).

---

## 4. Commands (development and Git)

From `scholarship-match/frontend/`:

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies from `package.json` (run after clone or when deps change). |
| `npm run dev` | Start Vite dev server (default port 5173). Hot reload on save. |
| `npm run build` | Production build to `frontend/dist/`. |
| `npm run preview` | Serve the production build locally to verify. |
| `npm run lint` | Run ESLint on `src/`. |

From the repo root (Git):

| Command | Purpose |
|---------|---------|
| `git pull` | Fetch and merge remote changes. |
| `git add <files>` | Stage files for commit. |
| `git commit -m "message"` | Create a commit with a clear message. |
| `git push` | Push commits to the remote. |

---

## 5. Debugging

### Reading errors

- **Browser Console (F12 → Console):** JavaScript errors, network failures, and `console.log` / `console.error` output. Red stack traces point to file names and line numbers in dev builds.
- **Network tab (F12 → Network):** Filter by **Fetch/XHR**. Click a request to see **status code**, **request URL**, **response body**. Failed requests often show `4xx`/`5xx` and JSON `detail` from FastAPI.

### Common issues

- **Blank page:** Check Console for a runtime error (often a missing import or undefined access).
- **CORS / 401:** Backend URL must match `VITE_API_BASE_URL` in `.env`; protected routes need a valid token from login.
- **Stale UI:** Hard refresh (Ctrl+Shift+R) or clear `localStorage` key for auth if testing login flows.

---

## 6. Backend connection (`apiFetch`, endpoints, auth)

### How `apiFetch` works

`src/api/client.ts` builds a full URL:

`API_BASE_URL + path` (e.g. `http://localhost:8000` + `/api/v1/profiles`).

It uses native `fetch`, a timeout, one retry on network failure, and logs non-OK responses to the console.

### Where endpoints are defined

- **Frontend:** Any string passed to `apiFetch('/api/v1/...')` in pages/contexts. Search the codebase for `apiFetch(` to list them.
- **Backend:** FastAPI route modules under `app/api/v1/` (e.g. `profiles.py`, `matches.py`). The path prefix is mounted in `app/main.py`.

### `authHeaders()`

From `AuthContext`: returns headers like `Authorization: Bearer <token>` for protected routes. If you remove or break this, the API returns **401 Unauthorized**.

### Data flow

1. Page calls `apiFetch` with `headers: { ...authHeaders() }`.
2. Response JSON is parsed and typed (see `types.ts`).
3. Results are stored in `useState` and passed to child components as props.

**Rule:** Change **display** (formatting, layout) freely; change **field names** only when the API contract and `types.ts` are updated together.

---

## 7. Image handling: `/public` vs `src/assets`

| Approach | Location | How to reference |
|----------|----------|------------------|
| **Public** | `frontend/public/images/foo.png` | `<img src="/images/foo.png" />` — URL is stable; good for many images and user-swappable assets. |
| **Imported** | `frontend/src/assets/foo.png` | `import img from '../assets/foo.png'` then `<img src={img} />` — Vite hashes filenames in production; good for icons bundled with the app. |

**Sizing:** Use Tailwind `w-*`, `h-*`, `max-w-*`, `object-cover` (fills box, crops), `object-contain` (fits entire image). Example: `className="h-64 w-full rounded-2xl object-cover"`.

---

## 8. Safe iteration checklist

1. **Where is this data coming from?** (API vs static constant.)
2. **What shape does the API return?** (See `types.ts` and Network tab.)
3. **Am I only changing display, or renaming fields?** (Renaming fields risks breaking the API.)

---

*This file is part of the Iskonnect project documentation. Update it when you add major features or change the API contract.*
