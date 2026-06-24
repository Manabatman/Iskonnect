# Iskonnect Active Learning Path

**Start here.** This is your day-by-day playbook for truly owning the `scholarship-match` codebase.

It is built on research-backed learning practices:

| Principle | What it means | How this guide uses it |
|-----------|---------------|------------------------|
| **Retrieval practice** | Recalling beats re-reading | Closed-book prompts before and after every session |
| **Spaced repetition** | Review at increasing intervals | Built-in review days at Day 3, 7, 14, and 30 |
| **Elaboration** | Connect new info to what you know | "Explain like a friend" and trace exercises |
| **Concrete tracing** | One real path beats 50 files skimmed | Every week traces a user action end-to-end |
| **Testing effect** | Tests reveal what you actually know | pytest + teach-back writeups as checkpoints |
| **Generation effect** | Writing your own version first helps | Diagram and notes *before* opening reference docs |
| **Interleaving** | Mix topics instead of one marathon block | Weeks alternate frontend, backend, matching, review |

**Time commitment:** 30–45 minutes per session. Consistency beats intensity.

**Companion docs** (reference only — do not read cover-to-cover first):

- [`LEARNING_GUIDE.md`](../LEARNING_GUIDE.md) — file map, API catalog, known bugs
- [`ENGINEERING_HANDBOOK.md`](ENGINEERING_HANDBOOK.md) — engineering skills + mini projects
- [`../ENGINEERING_HANDBOOK.md`](../ENGINEERING_HANDBOOK.md) — Iskonnect ops cheat sheet
- [`../../SOFTWARE_ENGINEERING_GUIDE.md`](../../SOFTWARE_ENGINEERING_GUIDE.md) — concepts when you get stuck

---

## Before Day 1 — Set up once (60–90 min)

Do this once, not as part of your daily habit.

### Step 0.1 — Create your learning log

Create a file: `scholarship-match/notes/learning-log.md`

Use this template for every session:

```markdown
## YYYY-MM-DD — [Topic]

**Retrieval (before):** What I think happens when...
**Did today:**
**Retrieval (after):** Without looking — list files, endpoints, tables involved
**Confused about:**
**Tomorrow:**
```

### Step 0.2 — Run the app (required)

You cannot own code you cannot run.

```powershell
cd c:\Iskonnect\scholarship-match
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

New terminal:

```powershell
cd c:\Iskonnect\scholarship-match\frontend
npm install
npm run dev
```

Verify:

- [ ] Frontend: http://localhost:5173
- [ ] API docs: http://localhost:8000/docs
- [ ] Health: http://localhost:8000/health

### Step 0.3 — Bookmark these entry points

| Layer | File |
|-------|------|
| Backend entry | `app/main.py` |
| Frontend entry | `frontend/src/main.tsx` → `frontend/src/App.tsx` |
| API client | `frontend/src/api/client.ts` |
| Auth | `frontend/src/contexts/AuthContext.tsx` + `app/auth.py` |
| Matching brain | `app/matching/match_service.py` |
| Database blueprint | `app/models.py` |

---

## How every session works (non-negotiable ritual)

Repeat this **every** study day. Total: 30–45 min.

### Block A — Retrieve first (5 min)

Close all docs and code. Answer today's **Retrieval prompt** in your learning log. Write even if wrong — wrong guesses strengthen learning when you correct them.

### Block B — Active work (20–30 min)

Do exactly **one** step from the day below. No multitasking.

### Block C — Retrieve again (5 min)

Without looking at code or docs:

1. List the 3–5 files you touched.
2. Name the HTTP method + endpoint (if applicable).
3. Name the database table(s) involved (if applicable).
4. Write one sentence: "When the user does X, the system does Y."

### Block D — Log and schedule review (2 min)

Fill in **Confused about** and **Tomorrow**. If today introduced something new, add a calendar reminder to re-test yourself in 3 days.

---

## Phase 1 — Orient (Days 1–7)

**Goal:** Mental map of the system. No deep dives yet.

---

### Day 1 — What is this product?

**Retrieval prompt:** In 3 sentences, what does Iskonnect do for a student?

**Do:**

1. Open http://localhost:5173 and click through: landing → register → profile builder → dashboard.
2. Read only `README.md` (first 80 lines).
3. Draw on paper (or in your log) four boxes: `Frontend` → `API` → `Matching` → `Database`. Label each with one technology (React, FastAPI, etc.).

**Check yourself:**

- [ ] Can you name the four layers without looking?
- [ ] Can you explain "hard filters" vs "scoring" in plain language?

**If stuck:** Read `LEARNING_GUIDE.md` §1 (High-Level Architecture) — then close it and rewrite your diagram from memory.

---

### Day 2 — Backend front door

**Retrieval prompt:** What happens when the backend starts? What file runs first?

**Do:**

1. Open `app/main.py`.
2. List every `include_router` line — write the URL prefix for each.
3. Find `/health` and `/ready`. What is the difference?
4. Hit both URLs in the browser.

**Check yourself:**

- [ ] Can you list 5 API route groups (auth, profiles, scholarships, etc.) from memory?
- [ ] Where is CORS configured?

**Reference:** `LEARNING_GUIDE.md` §5 (Backend and API Deep Dive) — only if needed.

---

### Day 3 — Frontend front door

**Retrieval prompt:** How does the browser know which page to show for `/dashboard`?

**Do:**

1. Open `frontend/src/main.tsx` — what gets mounted?
2. Open `frontend/src/App.tsx` — find the route for `/dashboard`, `/profile-builder`, `/scholarships/search`.
3. Match 3 public routes and 3 dashboard routes to what you see in the UI.

**Check yourself:**

- [ ] What is the difference between a "page" and a "layout" component?
- [ ] Where is `DashboardLayout` used?

**Spaced review (15 min extra):** Re-draw Day 1 architecture from memory. Compare to Day 1 drawing.

---

### Day 4 — Data shapes

**Retrieval prompt:** What is the difference between `models.py` and `schemas.py`?

**Do:**

1. Open `app/models.py` — find `Student`, `Scholarship`, `User`. Write down 5 important fields each.
2. Open `app/schemas.py` — find the profile create/update schema. What fields are required?
3. Do not read every line — skim for structure only.

**Check yourself:**

- [ ] Model = database table, Schema = API contract. Can you explain why both exist?
- [ ] Which table stores match history?

---

### Day 5 — First full trace (login)

**Retrieval prompt:** When I click Login, what travels over the network?

**Do — trace in this exact order:**

1. `frontend/src/pages/LoginPage.tsx` — find the submit handler.
2. `frontend/src/contexts/AuthContext.tsx` — find `login()`. What URL? What JSON body?
3. Browser DevTools → Network tab → perform login → inspect the request/response.
4. `app/api/v1/auth_routes.py` — find the login handler.
5. `app/auth.py` — find password verify + JWT creation.
6. Where is the token stored in the browser?

**Deliverable:** A 10-line trace in your learning log:

```
Click Login → [file] → POST [endpoint] → [backend file] → [function] → token stored in [place]
```

**Check yourself:**

- [ ] Authentication vs authorization — which is login?
- [ ] What header does the frontend send on later requests?

---

### Day 6 — API client layer

**Retrieval prompt:** Why have `client.ts` instead of calling `fetch` everywhere?

**Do:**

1. Read `frontend/src/api/client.ts` fully (it is short).
2. List: base URL source, timeout, retry behavior, error handling.
3. Find one page that imports `apiFetch` — follow one call.

**Check yourself:**

- [ ] What env var sets the API base URL?
- [ ] What happens on a network failure?

---

### Day 7 — Week 1 review (retrieval only)

**No new code.** Close everything.

**Do (45 min):**

1. Draw full architecture from memory.
2. Write the login trace from memory.
3. List all tables you know from `models.py`.
4. Run the app and perform login + navigate to dashboard without notes.
5. Read your learning log — rewrite answers to anything you got wrong on Day 3.

**Checkpoint:** If you cannot do #1–#3, repeat Days 1–6 at one day each before continuing.

---

## Phase 2 — Core user journeys (Days 8–21)

**Goal:** Trace every critical product flow end-to-end. This is where ownership actually happens.

Each trace week follows the same **TRACE method:**

| Step | Action |
|------|--------|
| **T** | Trigger — what does the user click? |
| **R** | Request — method, URL, JSON body |
| **A** | API route — which `app/api/v1/*.py` handler? |
| **C** | Core logic — which service/functions? |
| **E** | Evidence — which DB tables / models? |

---

### Day 8 — TRACE: Save profile

**Retrieval prompt:** What happens when a student saves their profile?

**Do:**

1. Trigger: `ProfileBuilderPage.tsx` + `profile-builder/` components.
2. State: skim `profileBuilderState.ts` — what is a reducer doing here?
3. Payload: `frontend/src/utils/studentProfilePayload.ts` — what gets sent?
4. Request: `POST /api/v1/profiles`
5. Route: `app/api/v1/profiles.py`
6. Evidence: `students` table in `models.py`

**Deliverable:** TRACE writeup in learning log.

---

### Day 9 — Profile trace part 2 (validation)

**Retrieval prompt:** What stops bad data from reaching the database?

**Do:**

1. Find Pydantic validation on the profile endpoint.
2. Find one field that exists on the frontend but maps to a different backend name.
3. In DevTools, submit profile and inspect the JSON payload vs response.

**Check yourself:**

- [ ] Where is ownership enforced (user can only edit their profile)?

---

### Day 10 — Spaced review + interleave

**Retrieval prompt:** Login trace + profile trace — write both from memory.

**Do:**

1. 15 min — closed-book traces.
2. 15 min — re-walk login in the browser with Network tab.
3. 15 min — re-walk profile save.

Fix gaps only by opening code — then close and rewrite.

---

### Day 11 — TRACE: Generate matches

**Retrieval prompt:** What is the difference between `GET /matches/{id}` and `POST /match-runs`?

**Do:**

1. Trigger: `ProfileDashboard.tsx` — find "generate matches" or equivalent action.
2. Request: `POST /api/v1/match-runs`
3. Route: `app/api/v1/match_history.py`
4. Core: `app/matching/match_service.py` — read the main orchestration function top to bottom.
5. Evidence: `match_runs` + `match_results` tables.

**Do not** dive into scoring yet — just see the orchestration.

---

### Day 12 — Hard filters

**Retrieval prompt:** What kinds of scholarships get removed before scoring?

**Do:**

1. Read `app/matching/hard_filters.py`.
2. List every filter type (age, income, region, etc.).
3. Open `app/tests/test_matching_regression.py` — find one test that protects a filter bug.

**Deliverable:** Bullet list: "A scholarship is rejected if..."

**Teach-back:** Explain hard filters to an imaginary friend in 60 seconds (out loud).

---

### Day 13 — Scoring engine

**Retrieval prompt:** How is a match score calculated?

**Do:**

1. Read `app/scoring/config.py` — what are the weight components?
2. Skim `app/scoring/components.py` — pick **one** component (e.g. income) and read only that function.
3. Read `app/scoring/engine.py` — how are components combined?
4. Read `app/scoring/explanation.py` — what does the user see?

**Check yourself:**

- [ ] Is document readiness part of the weighted score? (Read the code, not old docs.)

**Reference:** `SCORING_ENGINE.md` may be outdated — trust the code.

---

### Day 14 — Week 2 review + run tests

**Retrieval prompt:** Describe the full match pipeline: profile → filters → score → save → display.

**Do:**

1. Closed-book: draw match pipeline with file names.
2. Run: `python -m pytest app/tests/test_matching.py app/tests/test_scoring_engine.py -v`
3. Pick **one failing or passing test** — read it and explain what behavior it proves.
4. Open `MatchResultsPage.tsx` — how does the UI receive run results?

**Checkpoint:** You should explain the match flow in under 2 minutes out loud.

---

### Day 15 — TRACE: Scholarship search

**Retrieval prompt:** How does search differ from matching?

**Do:**

1. UI: `ScholarshipSearchPage.tsx` + `ScholarshipSearchFilters.tsx`
2. Request: `GET /api/v1/scholarships/search`
3. Route: `app/api/v1/scholarship_search.py`
4. Evidence: `scholarships` table

**Check yourself:**

- [ ] Search = database query. Matching = profile + filters + scoring. Can you explain the difference?

---

### Day 16 — TRACE: Save scholarship (bookmark)

**Retrieval prompt:** What happens when I click the bookmark icon?

**Do:**

1. `BookmarkButton.tsx` → `SavedScholarshipsContext.tsx`
2. Endpoints: `POST` and `DELETE` `/api/v1/saved-scholarships`
3. Route: `app/api/v1/saved_scholarships.py`
4. Table: `saved_scholarships`

---

### Day 17 — Spaced review (Day 8 + 11 material)

**Retrieval only (30 min):**

1. Write profile TRACE from memory.
2. Write match TRACE from memory.
3. Run the app: profile → match → view results. Narrate each step aloud.

---

### Day 18 — Database migrations

**Retrieval prompt:** How does the database schema change over time?

**Do:**

1. List files in `alembic/versions/` — read only the **first** and **latest** migration filenames and their docstrings.
2. Read `alembic/env.py` — how does Alembic connect?
3. Answer: "If I add a column to `Student`, what two places must change?"

**Do not** create a migration yet — understand the discipline first.

---

### Day 19 — Auth deep dive

**Retrieval prompt:** How does the backend know who is making a request?

**Do:**

1. Re-read `app/auth.py` — find `get_current_user` or equivalent dependency.
2. Pick one protected route in `profiles.py` — what `Depends(...)` is used?
3. What happens if `AUTH_DISABLED=true` in `.env`? (Find in config — understand dev vs prod risk.)

---

### Day 20 — Frontend state patterns

**Retrieval prompt:** Where does global app state live vs page-local state?

**Do:**

1. Read `AuthContext.tsx`, `SavedScholarshipsContext.tsx`, `ThemeContext.tsx` — one paragraph each in your log.
2. Pick `ProfileDashboard.tsx` — find one `useState` and one `useEffect`. What is each for?

**Check yourself:**

- [ ] Why no Redux in this project?

---

### Day 21 — Phase 2 checkpoint

**Closed-book exam (write answers in learning log):**

1. Trace login (10 lines).
2. Trace profile save (10 lines).
3. Trace match generation (15 lines).
4. Name 8 database tables and their purpose.
5. Draw the match pipeline.

**Then** open code and grade yourself. Re-study any item below 70% confidence.

**Reward:** Mark Phase 2 complete. You now understand Iskonnect better than most contributors.

---

## Phase 3 — Own the edges (Days 22–35)

**Goal:** Bugs, tests, safe changes, and engineering habits.

---

### Day 22 — Read tests as specification

**Do:**

1. `pytest app/tests -q` — note pass count.
2. Read fully: `test_matching.py`, `test_scoring_engine.py`, `test_match_service_integration.py`.
3. For each file, write: "This file proves that..."

---

### Day 23 — Known bugs tour

**Do:**

1. Read `LEARNING_GUIDE.md` §8 (Bugs, Issues, and Risks).
2. Pick **bug #1** (privacy consent) — trace the files listed. Do not fix yet.
3. Write: user impact + files involved + what a fix would require.

---

### Day 24 — Known bugs tour 2

Pick bugs #5 and #7 from the same section. Repeat Day 23 process.

---

### Day 25 — Debugging practice

**Do:**

1. Read `../ENGINEERING_HANDBOOK.md` §14 (Debugging Guide).
2. Break something safely: change API base URL in frontend `.env` to wrong port.
3. Observe error in browser console + Network tab. Fix it.
4. Log: "Symptom → layer → cause → fix."

---

### Day 26 — First safe code change

**Prerequisite:** Phase 2 checkpoint passed.

**Do:**

1. Create a git branch: `learn/first-change`
2. Make a **documentation-only** fix: correct one stale path or comment in a README.
3. `git diff` before commit.
4. Write in log: every file you touched and why.

---

### Day 27 — Explain the system (Feynman day)

**No code for 30 min.**

Write a one-page explanation: "How Iskonnect works" for a new developer.

Must include: stack, 4 user journeys, match pipeline, auth, where bugs live.

Then compare to `LEARNING_GUIDE.md` §1 — what did you miss?

---

### Day 28 — Spaced review (Day 1 + 7 + 14 + 21)

Re-do all checkpoint exams from memory. This is the **testing effect** — retrieval is the study.

---

### Days 29–30 — Mini rebuild (generation effect)

**Do not rewrite the whole app.** Rebuild one function from scratch in a scratch file:

**Day 29:** Reimplement one function from `app/scoring/components.py` in `notes/scratch_scoring.py` without copy-paste. Compare.

**Day 30:** Reimplement JWT decode logic conceptually in `notes/scratch_auth.py` (pseudocode OK). Compare to `app/auth.py`.

---

### Days 31–32 — HTTP + API fluency

**Do:**

1. Use http://localhost:8000/docs to call `GET /api/v1/auth/me` with a token.
2. Use curl or DevTools to call `GET /health`.
3. Read `ENGINEERING_HANDBOOK.md` (docs) §5 — Backend fundamentals — complete one practice task.

---

### Days 33–34 — Deployment awareness

**Do:**

1. Read `docs/DEPLOYMENT.md` — skim only.
2. List: where frontend deploys, where backend deploys, where DB lives.
3. Find `.github/workflows/ci.yml` — what runs on every push?

---

### Day 35 — Phase 3 checkpoint

**You should now be able to:**

- [ ] Trace any of the 4 core flows without docs
- [ ] Run pytest and explain 3 tests
- [ ] Name 5 known bugs and where they live
- [ ] Make a small change on a branch with `git diff` review
- [ ] Explain the full system in 3 minutes out loud

---

## Phase 4 — Maintenance mode (ongoing)

After Day 35, switch to a **weekly cycle** (pick one per day, ~30 min):

| Weekday | Focus |
|---------|-------|
| **Mon** | Retrieval: draw architecture + one trace from memory |
| **Tue** | Read one file you have never opened in `app/api/v1/` |
| **Wed** | Run tests; read one test file you have not read |
| **Thu** | One bug from `LEARNING_GUIDE.md` §8 — trace only |
| **Fri** | Teach-back: write or record 2-min explanation of one subsystem |
| **Sat** | Optional: `ENGINEERING_HANDBOOK.md` mini project milestone |
| **Sun** | Rest or spaced review of weakest trace |

### Spaced repetition schedule

Whenever you learn something new, mark it in your log and review on:

| Interval | Action |
|----------|--------|
| **+3 days** | Closed-book recall of that trace |
| **+7 days** | Explain it out loud; run related test |
| **+14 days** | Re-trace in browser with Network tab |
| **+30 days** | Full checkpoint: diagram + trace + tables |

---

## 30-minute morning version (busy days)

If you only have 30 minutes, use this compressed ritual:

1. **5 min** — Retrieval prompt (from today's day above).
2. **20 min** — One TRACE step only (e.g. only the API route, or only the service).
3. **5 min** — Closed-book log: files, endpoint, one sentence.

**Rule:** Never skip Block A and Block C. They are where learning actually happens.

---

## Rules that protect real learning

1. **No highlighting sprees.** If you are only reading, you are not learning.
2. **AI after 15 minutes stuck** — not before you guess.
3. **One flow per day** beats ten files skimmed.
4. **Wrong answers are useful** — correct them in Block C, not by re-reading.
5. **Do not rewrite the app from scratch** until you pass the Day 21 checkpoint.
6. **Trust code over docs** when they conflict — then note the doc bug in your log.

---

## Quick reference — TRACE cheat sheet

Copy this into every trace writeup:

```markdown
## TRACE: [Feature name]

**T — Trigger:** [Page / button / user action]
**R — Request:** [METHOD /api/v1/...] + key JSON fields
**A — API handler:** app/api/v1/[file].py → function name
**C — Core logic:** app/[service].py → function name
**E — Evidence:** tables: [table1, table2]

**Response shape:** [main fields returned]
**Frontend display:** [page/component that renders result]
```

---

## Progress tracker

Copy to your learning log and check off:

### Phase 1 — Orient
- [ ] Day 1 — Product + architecture
- [ ] Day 2 — `main.py`
- [ ] Day 3 — `App.tsx` routes
- [ ] Day 4 — models vs schemas
- [ ] Day 5 — Login trace
- [ ] Day 6 — `client.ts`
- [ ] Day 7 — Week 1 review

### Phase 2 — Core journeys
- [ ] Day 8–9 — Profile trace
- [ ] Day 10 — Spaced review
- [ ] Day 11–13 — Match pipeline
- [ ] Day 14 — Week 2 review + tests
- [ ] Day 15 — Search trace
- [ ] Day 16 — Bookmark trace
- [ ] Day 17 — Spaced review
- [ ] Day 18 — Migrations
- [ ] Day 19 — Auth deep dive
- [ ] Day 20 — Frontend state
- [ ] Day 21 — Phase 2 checkpoint

### Phase 3 — Ownership
- [ ] Day 22 — Tests as spec
- [ ] Day 23–24 — Known bugs
- [ ] Day 25 — Debugging practice
- [ ] Day 26 — First safe change
- [ ] Day 27 — Feynman writeup
- [ ] Day 28 — Spaced review
- [ ] Day 29–30 — Mini rebuild
- [ ] Day 31–32 — API fluency
- [ ] Day 33–34 — Deployment
- [ ] Day 35 — Phase 3 checkpoint

### Phase 4 — Maintenance mode started
- [ ] Weekly cycle running
- [ ] Spaced repetition reminders set

---

## What to do right now

1. Complete **Before Day 1** (setup + learning log).
2. Start **Day 1** tomorrow morning with Block A retrieval — not with reading `LEARNING_GUIDE.md`.
3. After Day 7, honestly assess the checkpoint. Do not rush to Phase 2 if Week 1 recall is weak.

You are not trying to memorize files. You are trying to **predict, trace, test, and explain** the system until it feels like yours.
