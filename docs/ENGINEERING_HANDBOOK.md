# Engineering Learning Handbook

**A personal playbook for becoming a competent backend engineer**  
**Audience:** You built **ISKONNECT** (`scholarship-match`) with AI help and want real understanding—not copy-paste skills.  
**Timeline:** Follow for **3–6 months** (1–2 focused hours/day beats weekend marathons).  
**Philosophy:** Learn by doing. Build from scratch. Debug on purpose. Understand before optimizing. Simplicity over complexity.

---

## How to use this document

- [ ] Read the roadmap once, then work **in order** unless you already mastered a stage.
- [ ] Turn every **Practice** item into a dated entry in a learning log.
- [ ] Rebuild small projects **without** AI first; use AI only after you are stuck for 30+ minutes.
- [ ] Revisit sections after you ship something—retention comes from spaced repetition.

---

## Table of contents

1. [Learning roadmap](#1-learning-roadmap)
2. [Terminal and command line mastery](#2-terminal-and-command-line-mastery)
3. [Git mastery](#3-git-mastery)
4. [Python mastery](#4-python-mastery)
5. [Backend engineering core concepts](#5-backend-engineering-core-concepts)
6. [Database fundamentals](#6-database-fundamentals)
7. [How the web works](#7-how-the-web-works)
8. [Building from scratch](#8-building-from-scratch)
9. [Best practices](#9-best-practices)
10. [Debugging skills](#10-debugging-skills)
11. [Mini projects](#11-mini-projects)
12. [Connection to ISKONNECT](#12-connection-to-iskonnect)
13. [How to study effectively](#13-how-to-study-effectively)

---

## 1. Learning roadmap

### Stage overview (order matters)

| Stage | Weeks (guide) | Outcome |
|-------|-----------------|---------|
| 1. Foundations | 2–4 | Terminal, Git, editor fluency; run other people’s code confidently |
| 2. Python mastery | 4–8 | Read/write real Python; data structures; errors; small scripts |
| 3. Backend fundamentals | 4–8 | HTTP, APIs, JSON, auth basics; FastAPI CRUD |
| 4. Full system view | 4–8 | Frontend talks to API; DB persistence; env vars; one full trace end-to-end |
| 5. Deployment and DevOps basics | 2–4 | Run locally with Docker; deploy to staging; read CI logs |
| 6. System design fundamentals | Ongoing | Draw diagrams; tradeoffs; caching, scaling vocabulary |

---

### Stage 1 — Foundations

**What to learn**

- Terminal: navigation, files, environment variables, running programs
- Git: clone, status, diff, add, commit, push, pull, branches
- Editor: search in project, multi-cursor, integrated terminal, debugger basics
- “Reading code” skill: jump to definition, find references, follow imports

**Why it matters**

Everything else sits on top of these. Backend work is mostly: read logs, run commands, commit changes, reproduce bugs.

**How it connects to real systems**

Production systems are edited locally, tested, committed, reviewed, merged, built in CI, deployed. Miss Git or the shell and you leak hours daily.

**Practice tasks**

- [ ] Clone ISKONNECT, run backend + frontend locally (see [Section 8](#8-building-from-scratch))
- [ ] Create a branch, make a tiny change (comment), open a PR (even to yourself)
- [ ] Use `git diff` before every commit for one week

---

### Stage 2 — Python mastery

**What to learn**

- Types, control flow, functions, modules, packages
- Data structures: list, dict, set, tuple; when to choose which
- Errors: exceptions, `try/except/finally`, raising errors intentionally
- OOP: classes, methods, inheritance (enough to read SQLAlchemy models)
- File I/O and context managers (`with open(...)`)
- Virtual environments and `pip`

**Why it matters**

ISKONNECT’s backend is Python. You cannot debug FastAPI/SQLAlchemy without solid Python.

**How it connects**

`app/models.py` (classes + relationships), `app/schemas.py` (Pydantic models), `app/auth.py` (functions + crypto + JWT).

**Practice tasks**

- [ ] Reimplement one small function from ISKONNECT in a scratch file **without** copy-paste
- [ ] Write a CLI script that reads a JSON file and prints summary stats
- [ ] Complete exercises in [Section 4](#4-python-mastery)

---

### Stage 3 — Backend fundamentals

**What to learn**

- HTTP: methods, status codes, headers, cookies
- REST-ish JSON APIs: resources, CRUD, pagination basics
- FastAPI: routes, dependency injection, request/response models
- Auth: passwords (hashing), JWT access tokens, refresh rotation (conceptual)

**Why it matters**

This is the job: translate product behavior into reliable HTTP + data rules.

**How it connects**

`app/main.py` mounts routers; `app/api/v1/*.py` defines endpoints; `app/auth.py` secures them.

**Practice tasks**

- [ ] Build Mini Project 2 in [Section 11](#11-mini-projects)
- [ ] Call your API with `curl` and document one happy path + one error path

---

### Stage 4 — Full system understanding (frontend + backend + DB)

**What to learn**

- How a SPA fetches data (`fetch`), base URLs, CORS
- SQL basics + ORM mental model (tables ↔ classes, rows ↔ objects)
- Migrations (schema evolves over time)
- Environment variables per environment (local/staging/prod)

**Why it matters**

Bugs often live **between** layers (wrong URL, CORS, stale migration, wrong env).

**How it connects**

Frontend: `frontend/src/api/client.ts`, contexts. Backend: `app/db.py`, `app/models.py`. DB: Postgres (Supabase) + Alembic.

**Practice tasks**

- [ ] Trace login in browser DevTools (Network tab) end-to-end
- [ ] Add a trivial endpoint and call it from the UI (or with `fetch` in console)

---

### Stage 5 — Deployment and DevOps basics

**What to learn**

- Containers vs bare metal (high level)
- `docker compose` for local stacks
- CI: what a workflow does, how to read failure logs
- Health checks (`/health`, `/ready`) and logs as primary interfaces

**Why it matters**

“Works on my machine” is not shipping. Deployment teaches constraints: ports, env vars, migrations, cold starts.

**How it connects**

`docs/DEPLOYMENT.md`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/`.

**Practice tasks**

- [ ] Run API + Postgres via compose; verify `/health`
- [ ] Intentionally break CI on a branch; read the log; fix it

---

### Stage 6 — System design fundamentals

**What to learn**

- Latency vs throughput; caching; idempotency; backpressure (vocabulary)
- Data modeling tradeoffs; indexes; N+1 query problem (concept)
- Reliability: retries, timeouts, rate limits
- Security basics: secrets, least privilege, OWASP Top 10 awareness

**Why it matters**

Senior engineers communicate in tradeoffs, not tutorials.

**How it connects**

Rate limiting (`slowapi`), CORS config, optional Redis, Sentry for observability.

**Practice tasks**

- [ ] Draw ISKONNECT architecture (boxes + arrows) from memory weekly
- [ ] Write a 1-page “if we 10x users” note: what breaks first?

---

### Roadmap progress checklist (copy to your notes)

- [ ] Stage 1 complete
- [ ] Stage 2 complete
- [ ] Stage 3 complete
- [ ] Stage 4 complete
- [ ] Stage 5 complete
- [ ] Stage 6 started (never “finished”—iterate)

---

## 2. Terminal and command line mastery

**Mental model:** The shell is a **REPL for your computer**. You type commands; the shell runs programs; programs read stdin, write stdout/stderr, return exit codes (`0` = success).

### 2.1 Navigation and location

| Command | What it does | When to use it | Example |
|---------|----------------|-----------------|---------|
| `pwd` | Print working directory | You are lost | `pwd` |
| `cd <dir>` | Change directory | Move into project | `cd scholarship-match` |
| `cd ..` | Parent directory | Go up one level | `cd ..` |
| `cd ~` | Home directory | Jump home | `cd ~` |
| `ls` | List files (macOS/Linux) | See contents | `ls -la` |
| `dir` | List files (Windows CMD) | See contents | `dir` |
| `Get-ChildItem` | List files (PowerShell) | See contents | `Get-ChildItem` |

**PowerShell equivalents (Windows)**

- `cd` works like Unix for most daily use.
- `ls` is often an alias for `Get-ChildItem`.

**Practice**

- [ ] From repo root, `cd` into `app` and back without using a GUI.

---

### 2.2 File and directory operations

| Command | What it does | When to use it | Example |
|---------|----------------|-----------------|---------|
| `mkdir <name>` | Create directory | New folder | `mkdir notes` |
| `touch file` | Create empty file (Unix) | Placeholder file | `touch README.local.md` |
| `New-Item file` | Create file (PowerShell) | Placeholder | `New-Item scratch.py` |
| `cp a b` | Copy | Backup / duplicate | `cp .env.example .env` |
| `Copy-Item a b` | Copy (PowerShell) | Same | `Copy-Item .env.example .env` |
| `mv a b` | Move/rename | Rename | `mv old.py new.py` |
| `rm file` | Delete file (Unix) | Remove | `rm tmp.log` |
| `rm -rf dir` | Delete tree (dangerous) | Only when sure | **Avoid** unless expert |
| `Remove-Item` | Delete (PowerShell) | Remove | `Remove-Item tmp.log` |

**Rules**

- Treat `rm -rf` like a power tool without a guard: verify path twice.
- Prefer moving mistakes to a trash folder during learning.

**Practice**

- [ ] Duplicate a file, rename it, delete the duplicate.

---

### 2.3 Viewing and editing text in terminal

| Command | What it does | When to use it | Example |
|---------|----------------|-----------------|---------|
| `cat file` | Print entire file | Small files | `cat README.md` |
| `less file` | Page through file | Big logs | `less logs.txt` |
| `head -n 20 file` | First lines | Quick peek | `head -n 20 app/main.py` |
| `tail -n 50 file` | Last lines | Recent log lines | `tail -n 50 uvicorn.log` |
| `tail -f file` | Follow file | Streaming logs | `tail -f /var/log/syslog` |

**Practice**

- [ ] Open a large log with `less`, search with `/` (less search).

---

### 2.4 Finding things (superpowers)

| Command | What it does | When to use it | Example |
|---------|----------------|-----------------|---------|
| `find` | Find files by pattern (Unix) | Locate files | `find . -name "*.py"` |
| `grep -R "text" .` | Search contents recursively | Find symbol usage | `grep -R "get_db" app` |

**Modern alternative:** use your editor’s global search first; use `grep`/`rg` when automating.

**Practice**

- [ ] Find every file importing `FastAPI` in `app/`.

---

### 2.5 Processes and ports

| Command | What it does | When to use it | Example |
|---------|----------------|-----------------|---------|
| `Ctrl+C` | Stop foreground process | Stop dev server | In terminal running uvicorn |
| `ps` / `Get-Process` | List processes | “What is running?” | `Get-Process python` |
| `kill <pid>` | Stop process by id | Stuck server | `kill 12345` |

**Port conflicts**

- If “address already in use”, something else owns the port—find and stop it.

**Practice**

- [ ] Start uvicorn, stop it, restart on a different port (`--port 8001`).

---

### 2.6 Environment variables

| Concept | Meaning |
|---------|---------|
| `PATH` | Directories searched for executables |
| `DATABASE_URL` | Connection string for DB |
| `VITE_API_BASE_URL` | Frontend build-time API base URL (Vite) |

**Unix**

```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/db"
echo $DATABASE_URL
```

**PowerShell**

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://user:pass@host:5432/db"
echo $env:DATABASE_URL
```

**Practice**

- [ ] Print `DATABASE_URL` in a shell **without** putting secrets in chat logs.

---

### 2.7 Python environment and package management

| Command | What it does | When to use it |
|---------|----------------|------------------|
| `python -V` | Python version | Verify version matches project |
| `python -m venv .venv` | Create virtual env | Isolate dependencies |
| `source .venv/bin/activate` | Activate (Unix) | Before pip install |
| `.venv\Scripts\Activate.ps1` | Activate (PowerShell) | Before pip install |
| `pip install -r requirements.txt` | Install deps | First setup / updates |
| `pip freeze` | List installed versions | Debug mismatches |

**Practice**

- [ ] Create `.venv`, install requirements, run `python -c "import fastapi"`.

---

### 2.8 Node / npm basics (frontend)

| Command | What it does | When to use it |
|---------|----------------|------------------|
| `node -v` | Node version | Verify toolchain |
| `npm install` | Install deps from lockfile/package | After pulling changes |
| `npm run dev` | Start Vite dev server | Local UI development |
| `npm run build` | Production build | CI / deploy checks |
| `npm run lint` | Lint (if configured) | Catch issues early |

**Practice**

- [ ] From `frontend/`, run dev server and load the app in browser.

---

### 2.9 Running servers (ISKONNECT-style)

**Backend (FastAPI)**

```bash
# from repo root, with venv active
uvicorn app.main:app --reload --port 8000
```

**Frontend (Vite)**

```bash
cd frontend
npm run dev
```

**Database migrations (Alembic)**

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

**Docker Compose (full stack local)**

```bash
docker compose up --build
```

---

### 2.10 Debugging-oriented commands

| Command | What it does | When to use it |
|---------|----------------|------------------|
| `curl -i URL` | HTTP request + headers | Test API quickly |
| `curl -X POST -H "Content-Type: application/json" -d "{}" URL` | POST JSON | Auth/login experiments |
| `nc -vz host port` | Check TCP connectivity | “Is DB port reachable?” |
| `Test-NetConnection host -Port 5432` | PowerShell connectivity | Same idea |

**Practice**

- [ ] `curl -i http://localhost:8000/health` and explain each header you recognize.

---

### Terminal mastery checklist

- [ ] Navigate any repo tree comfortably
- [ ] Create/copy/move/delete files safely
- [ ] Manage Python venv + pip installs
- [ ] Run `uvicorn`, `npm run dev`, and `alembic`
- [ ] Use `curl` to hit an endpoint and read status codes

---

## 3. Git mastery

### 3.1 Mental model (this is the whole game)

Think of Git as **four places**:

1. **Working tree** — files on disk (editable)
2. **Staging index** — proposed next snapshot (`git add`)
3. **Local repository** — committed history (`git commit`)
4. **Remote repository** — shared history (`git push` / `git pull`)

```text
edit files → git add → git commit → git push
                ↑            ↑
           staging       local history
```

**Why staging exists:** lets you craft a coherent commit from messy work.

---

### 3.2 Core commands

| Command | What it does | Example |
|---------|----------------|---------|
| `git clone <url>` | Copy remote repo locally | `git clone https://github.com/org/repo.git` |
| `git status` | Show changed/untracked files | `git status` |
| `git diff` | Unstaged changes | `git diff` |
| `git diff --staged` | Staged changes | `git diff --staged` |
| `git add <path>` | Stage changes | `git add app/main.py` |
| `git commit -m "msg"` | Save snapshot | `git commit -m "Fix CORS origins parsing"` |
| `git push` | Upload commits | `git push -u origin feature/x` |
| `git pull` | Download + integrate | `git pull --ff-only` (safe habit) |
| `git log --oneline --graph -n 20` | History view | readability |

**Practice**

- [ ] Make two separate commits from two logical changes (not one giant commit).

---

### 3.3 Branching

| Command | What it does | Example |
|---------|----------------|---------|
| `git branch` | List branches | `git branch` |
| `git switch -c feat/x` | Create + switch branch | `git switch -c feat/add-endpoint` |
| `git switch main` | Switch branch | `git switch main` |
| `git merge feat/x` | Merge branch into current | on `main`: `git merge feat/x` |

**Feature branch workflow (recommended)**

```text
main → update: git pull
     → branch: git switch -c feat/task
     → commit small slices
     → push branch
     → open PR
     → merge after review/CI
```

**Practice**

- [ ] Create a branch, push it, open PR, merge—repeat until boring.

---

### 3.4 Rebase basics (use carefully)

| Command | What it does | When |
|---------|----------------|------|
| `git fetch origin` | Update remote refs | Before integrating |
| `git rebase origin/main` | Replay commits atop updated main | Keep linear history (team rules vary) |

**Rule:** Never rebase commits already pushed **unless** you understand force-push implications.

---

### 3.5 Undoing mistakes

| Situation | Prefer | Command pattern |
|-----------|--------|-------------------|
| Unstage file | Safe | `git restore --staged path` |
| Discard local edits to file | Destructive | `git restore path` |
| Amend last commit message | Safe if not pushed | `git commit --amend` |
| Undo a pushed bad commit | Safer for shared branches | `git revert <sha>` |
| Reset local branch to remote | Destructive | `git reset --hard origin/main` |

**`git reset --hard` warning:** permanently discards uncommitted work.

**Stash (context switch)**

```bash
git stash push -m "wip"
git switch main
git pull
git switch -
git stash pop
```

---

### 3.6 `.gitignore` mental model

Ignore generated artifacts:

- virtual env (`.venv/`)
- `node_modules/`
- `.env` (secrets)
- build outputs (`dist/`, `__pycache__/`)

**Practice**

- [ ] Verify `.env` is ignored: `git status` should not list it.

---

### 3.7 Real workflows

**Daily dev loop**

```bash
git switch main
git pull
git switch -c feat/thing
# edit
git status
git diff
git add -p   # optional: stage interactively
git commit -m "feat: thing"
git push -u origin feat/thing
```

**Code review mindset**

- Small PRs, clear description, test plan (“I ran X, saw Y”).

---

### 3.8 Common mistakes and fixes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Committed secret | Secret in history | Rotate secret immediately; remove from future commits; follow org policy for history rewrite |
| Merge conflicts | `<<<<<<<` markers | Edit files manually, `git add`, `git commit` |
| Wrong branch commits | Commits on `main` | `git switch -c rescue`, cherry-pick, or reset depending on push state |
| Huge accidental `git add .` | Staged junk | `git restore --staged path` |

---

### 3.9 Connection to ISKONNECT

- CI workflows live in `.github/workflows/`—every PR teaches you to read logs.
- Treat failing CI as a lesson: reproduce locally first.

**Git checklist**

- [ ] Comfortable with branch + PR workflow
- [ ] Can read `git diff` and craft meaningful commits
- [ ] Knows revert vs reset conceptually
- [ ] Never commits `.env`

---

## 4. Python mastery

### 4.1 Syntax and fundamentals

**Variables and types**

```python
name: str = "Ada"
count: int = 3
ratio: float = 0.25
enabled: bool = True
```

**Control flow**

```python
if enabled and count > 0:
    print("go")
elif count == 0:
    print("empty")
else:
    print("stop")

for i in range(count):
    print(i)

while count > 0:
    count -= 1
```

**Comprehensions (readability first)**

```python
squares = [n * n for n in range(5)]
unique = {x for x in [1, 1, 2]}
```

---

### 4.2 Data structures (choose deliberately)

| Structure | Properties | Typical use |
|-----------|------------|-------------|
| `list` | Ordered, mutable | Sequences, stacks |
| `tuple` | Ordered, immutable | Fixed records, dict keys |
| `dict` | Key→value map | JSON-like records, indexes |
| `set` | Unique elements | membership tests, dedupe |

**Practice**

- [ ] Given a list of scholarships with `id`, compute a dict `id → scholarship`.

---

### 4.3 Functions and scope

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str, *, loud: bool = False) -> str:
    msg = f"Hello, {name}"
    return msg.upper() if loud else msg
```

- `*args` / `**kwargs` exist—use sparingly for clarity.

---

### 4.4 OOP (what you need to read frameworks)

```python
class User:
    def __init__(self, user_id: int, email: str) -> None:
        self.user_id = user_id
        self.email = email

    def mask_email(self) -> str:
        local, _, domain = self.email.partition("@")
        return f"{local[0]}***@{domain}"
```

**Dunder methods (taste)**

- `__repr__` helps debugging
- `__eq__` defines equality

---

### 4.5 File handling

```python
from pathlib import Path

p = Path("data.json")
text = p.read_text(encoding="utf-8")
```

Prefer `pathlib` over string paths.

---

### 4.6 Error handling

```python
def parse_int(x: str) -> int:
    try:
        return int(x)
    except ValueError as e:
        raise ValueError(f"not an int: {x!r}") from e
```

**Engineering rule:** catch **specific** exceptions; avoid bare `except:`.

---

### 4.7 Context managers (`with`)

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
# file closed automatically
```

SQLAlchemy sessions are also context-managed patterns.

---

### 4.8 Decorators (FastAPI is built on this idea)

Conceptually: a function that wraps another function.

```python
from functools import wraps
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])

def log_calls(fn: F) -> F:
    @wraps(fn)
    def wrapper(*args: object, **kwargs: object) -> object:
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)

    return wrapper  # type: ignore[return-value]

@log_calls
def add(a: int, b: int) -> int:
    return a + b
```

FastAPI route functions are normal functions with metadata attached.

---

### 4.9 Type hints and Pydantic mindset

Types are **documentation + tooling**. They are not always enforced at runtime unless you use validation libraries (Pydantic does).

---

### 4.10 Modules and packages

- `import package.module`
- `if __name__ == "__main__":` guard for runnable scripts
- `__init__.py` (still common) marks packages

---

### 4.11 Standard library essentials

| Module | Use |
|--------|-----|
| `datetime`, `zoneinfo` | timestamps |
| `json` | JSON encode/decode |
| `os`, `sys` | environment/process |
| `subprocess` | run commands (carefully) |
| `logging` | production prints |
| `pathlib` | paths |
| `itertools`, `functools` | expressive loops/utilities |

---

### 4.12 Apply Python to backend (FastAPI preview)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello() -> dict[str, str]:
    return {"msg": "world"}
```

**Practice**

- [ ] Add query params, return a typed dict, validate with Pydantic models.

---

### 4.13 Connection to ISKONNECT files

| File | Python ideas to study |
|------|------------------------|
| `app/config.py` | settings, env parsing |
| `app/db.py` | sessions, generators, dependencies |
| `app/models.py` | classes, relationships |
| `app/schemas.py` | Pydantic models |
| `app/auth.py` | functions, exceptions, security-sensitive code |

---

### Python mastery checklist

- [ ] Comfortable with dict/list comprehensions
- [ ] Can explain `try/except/finally` with examples
- [ ] Can read a class-based SQLAlchemy model
- [ ] Can write a small FastAPI route returning JSON

---

## 5. Backend engineering core concepts

### 5.1 What is an API?

An **API** is a contract: “If you send requests like this, I respond like that.”

For web backends, usually **HTTP + JSON**.

---

### 5.2 HTTP methods (most common)

| Method | Typical meaning | Should be safe/idempotent? |
|--------|-----------------|----------------------------|
| GET | Read resource | Safe; should not change server state |
| POST | Create / trigger action | Not necessarily idempotent |
| PUT | Replace resource | Often idempotent |
| PATCH | Partial update | Varies |
| DELETE | Delete | Often idempotent |

**Reality:** teams vary—always read docs/code.

---

### 5.3 Status codes (learn these first)

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No content |
| 400 | Bad request (client mistake) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (authenticated but not allowed) |
| 404 | Not found |
| 409 | Conflict |
| 422 | Validation error (common in FastAPI) |
| 429 | Too many requests (rate limit) |
| 500 | Server error |

---

### 5.4 Request/response lifecycle

```text
Client                                 Server
  |                                      |
  |--- TCP connect ---------------------->|
  |--- TLS handshake (https) ----------->|
  |--- HTTP request (method/path) ------>|
  |       headers: Host, Authorization    |
  |       body: JSON (optional)           |
  |                                      | route matching
  |                                      | middleware
  |                                      | handler
  |                                      | DB / logic
  |<-- HTTP response ---------------------|
        status + headers + JSON body
```

---

### 5.5 JSON

JSON maps cleanly to Python:

- object ↔ dict
- array ↔ list
- string ↔ str
- number ↔ int/float
- boolean ↔ bool
- null ↔ None

```python
import json

payload = {"ok": True, "count": 3}
json.dumps(payload)
json.loads('{"ok": true}')
```

---

### 5.6 Authentication basics

**Sessions (classic web)**

- Server stores session; browser holds cookie.

**Tokens (common for SPAs)**

- Server signs a token; client stores it; client sends `Authorization: Bearer ...`.

**JWT (JSON Web Token)**

- Three parts: header.payload.signature (commonly)
- Server can **verify signature** without DB lookup (but revocation is harder)

**Refresh tokens**

- Short-lived access token + longer-lived refresh token
- Refresh endpoint rotates refresh token (ISKONNECT pattern)

---

### 5.7 CORS (why your frontend “can’t reach” API)

Browsers block cross-origin requests unless server allows them via CORS headers.

Symptoms: browser console CORS error, but `curl` works.

---

### 5.8 Middleware

Functions that wrap requests/responses: logging, auth, security headers, timing.

---

### 5.9 Rate limiting

Protects APIs from abuse / accidents. Too many requests → `429`.

---

### 5.10 Build a simple API from scratch (minimal)

```bash
mkdir mini-api && cd mini-api
python -m venv .venv
# activate venv
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)

items: dict[int, Item] = {}
next_id = 1

@app.post("/items", status_code=201)
def create_item(item: Item) -> dict:
    global next_id
    item_id = next_id
    next_id += 1
    items[item_id] = item
    return {"id": item_id, "item": item.model_dump()}

@app.get("/items/{item_id}")
def read_item(item_id: int) -> dict:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="not found")
    return {"id": item_id, "item": items[item_id].model_dump()}
```

```bash
uvicorn main:app --reload
```

**Practice**

- [ ] Add `GET /items` list endpoint with pagination query params.

---

### 5.11 Connection to ISKONNECT

| Concept | Where it shows up |
|---------|-------------------|
| Routers | `app/api/v1/*.py` |
| App wiring | `app/main.py` |
| JWT | `app/auth.py`, `app/api/v1/auth_routes.py` |
| CORS | `app/main.py` + settings in `app/config.py` |
| Rate limiting | `slowapi` integration |

---

### Backend core checklist

- [ ] Can explain GET vs POST with examples
- [ ] Can read HTTP status codes and pick correct ones
- [ ] Can describe JWT + refresh flow at a high level
- [ ] Can debug a CORS issue systematically

---

## 6. Database fundamentals

### 6.1 What is a database?

A **database** stores durable data with rules: types, constraints, concurrent access, query language.

**Relational DB (Postgres)** stores tables with rows and columns, supports SQL joins.

---

### 6.2 SQL basics

**SELECT**

```sql
SELECT id, email
FROM users
WHERE is_active = true
ORDER BY created_at DESC
LIMIT 50;
```

**INSERT**

```sql
INSERT INTO users (email, password_hash)
VALUES ('ada@example.com', '...hash...');
```

**UPDATE**

```sql
UPDATE users
SET last_login_at = NOW()
WHERE id = 123;
```

**DELETE**

```sql
DELETE FROM saved_scholarships
WHERE user_id = 123 AND scholarship_id = 456;
```

---

### 6.3 Relationships and foreign keys

A **foreign key** enforces: “this column must reference an existing row.”

Example idea:

- `profiles.user_id` → `users.id`

This prevents orphan rows (if enforced).

---

### 6.4 JOINs

```sql
SELECT u.email, p.display_name
FROM users u
JOIN profiles p ON p.user_id = u.id
WHERE u.id = 123;
```

---

### 6.5 Indexes

An **index** speeds lookups (like a book index). Tradeoff: faster reads, slower writes, more storage.

Common rule: index foreign keys and frequent filter columns.

---

### 6.6 ORM mental model (SQLAlchemy)

```text
Python class (Model)   ↔   table
instance               ↔   row
attribute              ↔   column
session.add/commit     ↔   INSERT/UPDATE
session.query/select   ↔   SELECT
```

---

### 6.7 Migrations (Alembic)

Schema evolves in versioned steps:

```bash
alembic revision --autogenerate -m "add column"
alembic upgrade head
```

**Engineering habit:** migrations are code review items—bad migrations can lock tables.

---

### 6.8 Supabase in this project

Supabase here is primarily **managed Postgres** + dashboard tooling. The API connects via `DATABASE_URL` using SQLAlchemy/psycopg2—not necessarily the Supabase client libraries.

---

### 6.9 Practice queries (generic scholarship app)

> Names are illustrative—map to your real tables by inspecting `app/models.py`.

```sql
-- Count active users
SELECT COUNT(*) FROM users WHERE is_active = true;

-- Scholarships created in last 7 days
SELECT id, title, created_at
FROM scholarships
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;

-- Top 10 scholarships by saved count (if such a table exists)
SELECT scholarship_id, COUNT(*) AS saves
FROM saved_scholarships
GROUP BY scholarship_id
ORDER BY saves DESC
LIMIT 10;
```

**Practice**

- [ ] Pick one endpoint in `app/api/v1/` and find the ORM query it triggers.

---

### Database fundamentals checklist

- [ ] Can write CRUD SQL for a 2-table schema
- [ ] Can explain foreign keys + why they matter
- [ ] Can explain what a migration is
- [ ] Can connect Supabase Postgres URL to local env safely

---

## 7. How the web works

### 7.1 Big picture flow

```text
User browser
   |
   | DNS: hostname -> IP
   v
HTTPS request to hosting (Vercel / Render / etc.)
   |
   +--> Static frontend (HTML/JS/CSS)  (Vite build output)
   |
   +--> API server (FastAPI)  JSON /auth /profiles ...
            |
            v
        PostgreSQL (Supabase)
```

---

### 7.2 What happens when a user clicks “Login” (conceptual)

```text
UI button
  -> React event handler
     -> AuthContext calls apiFetch("/api/v1/auth/login")
        -> browser sends HTTP POST JSON {email, password}
           -> FastAPI route validates payload (Pydantic)
              -> DB query: find user by email
                 -> bcrypt verifies password hash
                    -> create JWT access token (+ refresh token persisted)
                       <- JSON {access_token, refresh_token, user...}
          <- 401 if invalid
     <- parse response / store tokens (localStorage in this app)
  -> UI navigates to dashboard route
```

---

### 7.3 Deployment mental model (ISKONNECT)

```mermaid
flowchart LR
  user[UserBrowser]
  vercel[Vercel_StaticReact]
  render[Render_FastAPI]
  db[Supabase_Postgres]

  user -->|HTTPS_HTML_JS| vercel
  user -->|HTTPS_API_JSON| render
  render -->|SQL_TCP_SSL| db
```

**Important detail:** Vite uses `VITE_API_BASE_URL` so the browser calls the Render URL directly (typical SPA pattern).

---

### 7.4 Text diagram (copy into notes)

```text
[Browser]
   |  GET https://<vercel>/assets/*
   v
[Vercel CDN] serves built React app

[Browser]
   |  POST https://<render>/api/v1/auth/login
   v
[Render Web Service] uvicorn -> FastAPI -> SQLAlchemy
   |
   v
[Supabase Postgres]
```

---

### Web fundamentals checklist

- [ ] Can explain DNS + HTTPS at a high level
- [ ] Can trace a request in DevTools Network tab
- [ ] Can explain why env vars differ between Vercel and Render

---

## 8. Building from scratch

This section is the antidote to “I generated a repo and it’s magic.” You should be able to **recreate the shape** of a system without AI.

### 8.1 What to install first (recommended order)

- [ ] **Git** (version control)
- [ ] **Python 3.11+** (match ISKONNECT `.python-version` when possible)
- [ ] **Node.js LTS** (for Vite/React)
- [ ] **Docker Desktop** (optional early; required for realistic local DB parity)
- [ ] **Editor** (VS Code / Cursor) + Python + ESLint/Prettier extensions as needed

**Verify installs**

```bash
git --version
python -V
node -v
npm -v
docker --version
```

---

### 8.2 Create a backend from zero (FastAPI)

```bash
mkdir my-api && cd my-api
python -m venv .venv
# activate:
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# mac/linux: source .venv/bin/activate

pip install fastapi uvicorn[standard] pydantic-settings
```

**Folder shape (simple monolith)**

```text
my-api/
  app/
    __init__.py
    main.py
  requirements.txt
```

`app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Run:

```bash
uvicorn app.main:app --reload --port 8000
```

---

### 8.3 Add a database (Postgres + SQLAlchemy) — minimal pattern

Install:

```bash
pip install sqlalchemy psycopg2-binary alembic
```

Typical env:

```bash
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/mydb
```

**Engineering steps**

1. Define models (`Base`, tables)
2. Wire `SessionLocal` + `get_db()`
3. Create migration baseline
4. Run `alembic upgrade head`
5. Use DB sessions in routes

ISKONNECT already implements this pattern in `app/db.py` + `app/models.py` + `alembic/`.

---

### 8.4 Create a frontend from zero (Vite + React + TS)

```bash
npm create vite@latest my-ui -- --template react-ts
cd my-ui
npm install
npm run dev
```

**Call your API**

```ts
const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/health`);
console.log(await res.json());
```

Set `VITE_API_BASE_URL` in `.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

### 8.5 Connect frontend ↔ backend (local dev)

**CORS checklist**

- [ ] Backend allows `http://localhost:5173` (or your Vite port) in CORS origins
- [ ] Frontend uses correct base URL (scheme + host + port)
- [ ] You are not mixing `http` UI with `https` API unintentionally

**Cookie vs Bearer note:** ISKONNECT SPA commonly uses **Bearer JWT** from `localStorage` (see frontend `AuthContext`).

---

### 8.6 ISKONNECT-specific setup pointers

Read in this order:

1. [SETUP.md](../SETUP.md) (if present in your checkout)
2. [DEPLOYMENT.md](DEPLOYMENT.md)
3. `docker-compose.yml` for local `api + postgres (+ redis)`

**Common commands (repo root)**

```bash
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload

cd frontend
npm install
npm run dev
```

**Docker**

```bash
docker compose up --build
```

---

### Building from scratch checklist

- [ ] Created a throwaway FastAPI app with `/health`
- [ ] Created a throwaway Vite app
- [ ] Successfully called API from browser code locally
- [ ] Explained each env var you needed

---

## 9. Best practices

### 9.1 Clean code principles (practical, not dogmatic)

- **Names reveal intent:** `get_user_by_email` beats `get`
- **Small functions:** if you can’t name it, it’s doing too much
- **Single responsibility:** a route handler shouldn’t contain 200 lines of business logic—extract services
- **DRY carefully:** duplication is cheaper than wrong abstraction
- **KISS:** default to the simplest design that meets requirements

---

### 9.2 Python naming (PEP 8 highlights)

| Thing | Style | Example |
|-------|--------|---------|
| modules | snake_case | `auth_routes.py` |
| functions/vars | snake_case | `access_token` |
| classes | PascalCase | `Scholarship` |
| constants | UPPER_SNAKE | `DEFAULT_PAGE_SIZE` |

---

### 9.3 Folder structure patterns (backend monolith)

Good separation:

- `api/` HTTP translation (parse/validate/status codes)
- `services/` business rules (pure-ish functions)
- `models/` ORM definitions
- `schemas/` Pydantic IO models
- `jobs/` background/cron-like tasks

ISKONNECT uses `app/api/v1/` + domain packages (`matching/`, `scoring/`, …).

---

### 9.4 Error handling strategy

- Validate inputs early (Pydantic)
- Convert unexpected exceptions into **500** with safe client messages
- Log detailed server-side context (never leak secrets)

---

### 9.5 Logging (prefer `logging` over `print`)

```python
import logging

log = logging.getLogger(__name__)

def do_work(user_id: int) -> None:
    log.info("work_started", extra={"user_id": user_id})
    try:
        ...
    except Exception:
        log.exception("work_failed", extra={"user_id": user_id})
        raise
```

**Structured logs** (JSON) are ideal in production—grow into them.

---

### 9.6 Maintainability habits

- Write a **test plan** in PR description
- Add migration when schema changes
- Keep secrets out of repo
- Prefer feature flags for risky behavior (`AUTH_DISABLED` is a sharp tool—treat as dangerous)

---

### Best practices checklist

- [ ] Every new function has a clear name + type hints
- [ ] Errors are categorized (validation vs auth vs server)
- [ ] Logging includes correlation identifiers where possible

---

## 10. Debugging skills

### 10.1 How to read Python tracebacks

Read bottom-up:

1. **Exception type + message** (what failed)
2. **Your code frames** (where in your project)
3. **Library frames** (often noise unless you misuse API)

**Practice**

- [ ] Force an error (`1/0`) in a route and read the traceback until you can predict it.

---

### 10.2 Browser debugging (frontend)

- **Console:** JS errors, logs
- **Network:** request URL, status, response JSON, timing
- **Sources:** breakpoints

**Practice**

- [ ] Find a failing request and compare **request headers** vs backend expectations.

---

### 10.3 Isolate problems (binary search)

1. Reproduce reliably
2. Remove half the system (bypass UI, call API with curl)
3. If API works, problem is UI/config; if not, backend/db
4. Repeat

---

### 10.4 Test APIs with curl

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/ready

curl -i -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"you@example.com\",\"password\":\"yourpassword\"}"
```

**Windows PowerShell note:** quoting JSON is painful—prefer `curl.exe` or a file:

```powershell
curl.exe -i -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d "{\"email\":\"you@example.com\",\"password\":\"yourpassword\"}"
```

---

### 10.5 Logging vs print

- `print` is okay for 5-minute experiments
- `logging` is for anything you might need in prod

---

### 10.6 Python debugger

```python
x = compute()
breakpoint()  # execution stops here in dev
print(x)
```

---

### 10.7 Common error patterns

| Symptom | Likely cause |
|---------|----------------|
| `401` everywhere | missing/expired token, wrong `Authorization` header |
| `422` | Pydantic validation mismatch (shape/types) |
| CORS errors | API not allowing frontend origin |
| DB connection errors | wrong `DATABASE_URL`, SSL mode, IP allowlist |
| `ModuleNotFoundError` | venv not activated / wrong cwd |

---

### 10.8 Connection to ISKONNECT

- Use `/health` and `/ready` as sanity checks when debugging deploy issues.
- Sentry (if enabled) is for **production signals**—learn to attach user/request context responsibly (PII rules).

---

### Debugging checklist

- [ ] Can reproduce a bug in 3 steps or fewer
- [ ] Can decide “UI vs API vs DB” in 10 minutes
- [ ] Uses Network tab + curl as default tools

---

## 11. Mini projects

Each project should be rebuilt until you can do it **without notes**.

### Project 1 — CLI todo app (Python fundamentals)

**Goal:** file persistence + basic commands.

**Requirements**

- Commands: `add`, `list`, `done`, `delete`
- Store todos in `todos.json`

**Stretch**

- Add `due_date` validation

**Reinforces:** file I/O, JSON, functions, error handling

---

### Project 2 — Tiny JSON API (FastAPI, in-memory)

**Goal:** CRUD for `books` without DB.

**Endpoints**

- `POST /books`
- `GET /books`
- `GET /books/{id}`
- `PATCH /books/{id}`
- `DELETE /books/{id}`

**Reinforces:** HTTP methods, status codes, Pydantic models

---

### Project 3 — CRUD API + Postgres + SQLAlchemy

**Goal:** persist `books` table.

**Steps**

1. Model + schema
2. Session dependency
3. Alembic init + migration
4. Wire routes

**Reinforces:** ORM, migrations, transactions

---

### Project 4 — Auth system (JWT + bcrypt)

**Goal:** register/login/me/refresh logout (subset of real systems).

**Rules**

- Never store plaintext passwords
- Store refresh token **hashed** if persisted
- Access token short TTL

**Reinforces:** crypto primitives, auth dependencies, security mindset

**ISKONNECT parallel:** read `app/auth.py` + `app/api/v1/auth_routes.py` after you build yours.

---

### Project 5 — Full-stack mini app (React + FastAPI + Supabase Postgres)

**Goal:** a single workflow end-to-end:

- UI form → POST → DB row → GET list page

**Reinforces:** CORS, env vars, API client wrapper, deployment thinking

---

### Mini project completion checklist

- [ ] Project 1 shipped to a private GitHub repo
- [ ] Project 2 documented with curl examples
- [ ] Project 3 has migrations committed
- [ ] Project 4 has threat model notes (even 5 bullets)
- [ ] Project 5 deployed to free tiers OR runs identically in Docker locally

---

## 12. Connection to ISKONNECT

ISKONNECT in this workspace is the `scholarship-match` repository: a **modular monolith** FastAPI backend + Vite/React SPA + Postgres (often Supabase-managed).

### 12.1 Architecture map (study until you can redraw)

```text
frontend/ (Vite + React + TS)
  src/api/client.ts        fetch wrapper, base URL, retries
  src/contexts/*           auth + domain state
  src/pages/*              route screens

app/ (FastAPI)
  main.py                  app wiring, middleware, routers, health
  config.py                environment settings
  db.py                    engine + sessions
  models.py                SQLAlchemy tables
  schemas.py               Pydantic models (API shapes)
  auth.py                  JWT + bcrypt + dependencies
  api/v1/*.py              HTTP routers (/api/v1/...)
  matching/ scoring/ ...  domain logic

PostgreSQL
  Supabase in prod (typical)

CI/CD
  .github/workflows/*

Deploy (typical)
  Vercel -> static frontend
  Render -> FastAPI
  Supabase -> Postgres
```

---

### 12.2 Concept → file mapping

| Concept | ISKONNECT location |
|---------|--------------------|
| HTTP routing | `app/main.py`, `app/api/v1/*.py` |
| Validation | Pydantic models in `app/schemas.py` (+ local schemas) |
| Persistence | `app/models.py` + SQLAlchemy queries |
| Auth | `app/auth.py`, `app/api/v1/auth_routes.py` |
| DB connection | `app/db.py`, `DATABASE_URL` |
| Migrations | `alembic/`, `alembic.ini` |
| Rate limits | `slowapi` wiring (see `app/limiter.py` / usage) |
| Frontend API calls | `frontend/src/api/client.ts` |
| Login/session UX | `frontend/src/contexts/AuthContext.tsx` |
| Deploy docs | `docs/DEPLOYMENT.md` |

---

### 12.3 Guided reading exercises (do these weekly)

**Exercise A — request enters backend**

1. Open `app/main.py`
2. Pick one router include path, e.g. `/api/v1/...`
3. Open matching `app/api/v1/<module>.py`
4. Find one `@router.get` / `@router.post`
5. Trace: handler → schema → DB session → models → response

**Exercise B — login trace**

1. Frontend: `AuthContext.tsx` → find login function
2. Note URL + JSON body + headers
3. Backend: `auth_routes.py` → locate login handler
4. Follow calls into `auth.py` (hashing/JWT)
5. Identify DB tables touched

**Exercise C — schema change discipline**

1. Pick a column concept you understand (even if you don’t implement)
2. Describe migration steps: model change → alembic revision → upgrade
3. Describe rollback story (`downgrade`)

---

### 12.4 Suggested “confidence builder” changes (safe if you use a branch)

- Add a `/api/v1/debug/ping` route locally (guard behind env flag; never ship insecure debug)
- Add structured logs around a single expensive operation
- Add one pytest that hits `/health`
- Add a tiny UI label change and trace it through build

---

### ISKONNECT integration checklist

- [ ] Can draw architecture from memory
- [ ] Can trace one user action across 3 layers
- [ ] Knows where auth is enforced (dependencies + routes)

---

## 13. How to study effectively

### 13.1 Daily routine (60–120 minutes)

**Block A (20–40 min): fundamentals**

- One small lesson + 5 retrieval questions (write answers without notes)

**Block B (40–80 min): deliberate build**

- Mini project milestone OR read ISKONNECT code with a goal

**Block C (10 min): log**

- What you learned (3 bullets)
- What confused you (1 bullet)
- Tomorrow’s first step (1 bullet)

---

### 13.2 Weekly routine

- [ ] 1 mini project milestone completed OR 1 PR-sized contribution planned
- [ ] 1 “teach-back” writeup: explain a subsystem as if to a peer
- [ ] Review flashcards/commands for 15 minutes

---

### 13.3 How to practice (what actually works)

- **Type code** by hand from a blank file, then compare
- **Break things on purpose** (wrong URL, wrong env) and predict failure modes
- **Timebox confusion:** 20 minutes struggle → hint → 20 more → solution

---

### 13.4 Reducing over-reliance on AI (graduated policy)

| Level | Policy |
|-------|--------|
| 0 | AI writes everything (starting point) |
| 1 | You write skeleton; AI fills gaps |
| 2 | You implement; AI reviews |
| 3 | You implement + you explain tradeoffs; AI only for obscure errors |

Your goal is **Level 2–3** for backend tasks within 3–6 months.

**Rule:** If AI generates a chunk, you must be able to **delete it and rewrite it** within 30 minutes within a week.

---

### 13.5 Retention techniques

- **Feynman technique:** explain simply without jargon; expose gaps
- **Spaced repetition:** revisit prior week’s commands/projects
- **Interleaving:** alternate reading, coding, debugging—not only tutorials

---

### 13.6 Anti-patterns (avoid)

- Tutorial hopping without building
- Copy-paste without prediction (“I’ll understand later”)
- Optimizing before measuring
- Skipping Git fundamentals (“I’ll just click buttons”)

---

### 13.7 Weekly review checklist

- [ ] Did I ship a tangible artifact (code/docs/diagram)?
- [ ] Did I read an error message fully before searching?
- [ ] Did I practice 10 terminal commands from memory?
- [ ] Did I write down one security lesson?

---

## Closing: your engineering identity

Competence is not “I memorized FastAPI.” Competence is:

- You can **localize** problems quickly
- You can **reason** about tradeoffs
- You can **build** small systems from scratch
- You can **read** large codebases without panic

ISKONNECT is your gym. Use the handbook as a barbell: repeat lifts.

---

## Appendix A — Quick reference card (print me)

```text
Git:        status diff add commit push pull branch switch merge stash
Python:     venv pip pytest logging pathlib typing
HTTP:       GET POST PUT PATCH DELETE + status codes
FastAPI:    app=FastAPI() router Depends() HTTPException pydantic
DB:         SQL SELECT/INSERT/UPDATE + JOIN + FK + index + migration
Debug:      reproduce -> isolate layer -> curl -> logs -> minimal repro
```

---

## Appendix B — Glossary (short)

| Term | Meaning |
|------|---------|
| API | Contract for how software talks to software |
| SPA | Single-page app; loads JS once; navigates client-side |
| ORM | Maps DB rows to objects; generates SQL |
| Migration | Versioned schema change |
| JWT | Signed token carrying claims |
| CORS | Browser security rules for cross-origin requests |
| CI | Automated tests/builds on each change |

---

**End of handbook** — revise monthly as you grow.
