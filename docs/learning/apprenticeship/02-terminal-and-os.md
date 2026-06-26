# Lesson 02 — Terminal & Operating System

> **Prerequisite:** [01 — How Engineers Think](01-how-engineers-think.md)

---

## What this lesson teaches

Every command you run to build Iskonnect starts in a **terminal**. This lesson explains the shell, filesystem, processes, and ports — with every command dissected.

---

## Concept: Terminal and shell

### 1. Definition

A **terminal** is a text window where you type commands. The **shell** (PowerShell on your Windows machine, bash on Linux/Mac) interprets those commands and asks the OS to execute them.

### 2. Why it exists

GUIs are great for browsing files; terminals are faster for repetitive, precise, automatable work (install deps, run servers, deploy).

### 3. Problem solved

**Automation and reproducibility.** `pip install -r requirements.txt` does the same thing on every machine.

### 4. Before terminals

Punch cards → teletype printers → CRT terminals. Engineers typed commands because mice did not exist.

### 5. Alternatives

- IDE integrated terminal (Cursor's terminal — same shell underneath)
- GUI package managers (slower, less scriptable)

### 6. Tradeoffs

Terminal: fast, scriptable, steep learning curve. GUI: discoverable, hard to automate.

### Analogy

The terminal is the **cockpit** of development. Buttons on a website are for passengers; engineers fly the plane.

---

## Command reference (used in Iskonnect)

### `pwd` — Print Working Directory

| Aspect | Detail |
|--------|--------|
| **Syntax** | `pwd` |
| **Meaning** | Show the folder you are "standing in" |
| **Why used** | Confirm location before `cd` or `git` commands |
| **Internal** | Shell asks OS for current process working directory |
| **Output** | `C:\Iskonnect\scholarship-match` |
| **Mistakes** | Confusing drive letter case on Windows |
| **Variations** | PowerShell: `Get-Location` |
| **Discovery** | `man pwd`, Google "how to see current directory" |

### `mkdir` — Make Directory

| Aspect | Detail |
|--------|--------|
| **Syntax** | `mkdir scholarship-match` |
| **Meaning** | Create a new folder |
| **Why used** | Day 0 project genesis — first act of creation |
| **Internal** | OS allocates directory inode / folder entry in parent |
| **Output** | (none on success) |
| **Mistakes** | `mkdir scholarship-match/app` fails if parent missing — use `mkdir -p` on bash or nested `New-Item` on PowerShell |
| **Variations** | `mkdir -p a/b/c` (bash), `New-Item -ItemType Directory -Path a\b\c` (PowerShell) |
| **Discovery** | `--help` flag |

### `cd` — Change Directory

| Aspect | Detail |
|--------|--------|
| **Syntax** | `cd scholarship-match` or `cd ..` (parent) |
| **Meaning** | Move your shell's working directory |
| **Why used** | Navigate into `frontend/` before `npm install` |
| **Internal** | Shell updates its `cwd` environment variable; does not move files |
| **Mistakes** | `cd scholarship-match` when already inside it — use `cd frontend` not `cd scholarship-match/frontend` |
| **Variations** | `cd ~` (home), `cd -` (previous, bash) |

### `ls` / `dir` — List

| Aspect | Detail |
|--------|--------|
| **Syntax** | `ls` (bash), `Get-ChildItem` or `dir` (PowerShell) |
| **Meaning** | List files and folders in cwd |
| **Why used** | Verify `requirements.txt` exists before pip install |
| **Internal** | OS reads directory entries |
| **Output** | `app/`, `frontend/`, `requirements.txt`, ... |
| **Mistakes** | Hidden files (`.env`) not shown without `-a` / `-Force` |
| **Variations** | `ls -la`, `Get-ChildItem -Recurse` |

---

## Concept: Paths

### Absolute vs relative

- **Absolute:** `C:\Iskonnect\scholarship-match\app\main.py` — from root
- **Relative:** `app/main.py` — from cwd

Iskonnect imports use Python package paths (`from app.db import get_db`), not filesystem paths — but you still navigate with filesystem paths in the terminal.

### Path separators

Windows accepts `\` or `/` in most tools. Python and Git prefer `/`.

---

## Concept: Environment variables

### 1. Definition

**Environment variables** are key-value pairs inherited by child processes (e.g. `DATABASE_URL`, `SECRET_KEY`).

### 2. Why they exist

Secrets and config differ per machine (your laptop vs Render production) without changing code.

### 3. Iskonnect usage

Loaded from `.env` via `app/config.py` (pydantic-settings). See `.env.example` in project root.

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Postgres or SQLite connection string |
| `SECRET_KEY` | Signs JWT tokens |
| `AUTH_DISABLED` | `true` = skip auth locally |
| `CORS_ORIGINS` | Allowed frontend URLs |
| `REDIS_URL` | Shared cache + rate limits |

### 4. Before `.env` files

Hardcoded config in source code — leaked secrets in git history.

### 5. Command: set env for one command (bash)

```bash
AUTH_DISABLED=true uvicorn app.main:app --reload --port 8000
```

PowerShell:

```powershell
$env:AUTH_DISABLED="true"; uvicorn app.main:app --reload --port 8000
```

---

## Concept: Processes and ports

### 1. Definition

A **process** is a running program. A **port** is a numbered door (0–65535) where a process listens for network connections.

### 2. Why ports matter

Only one process can bind a port at a time. Iskonnect backend uses **8000** locally; frontend dev server uses **5173** (Vite default).

### 3. Iskonnect startup commands

**Backend** (from `scholarship-match/`):

```bash
uvicorn app.main:app --reload --port 8000
```

| Part | Meaning |
|------|---------|
| `uvicorn` | ASGI server program |
| `app.main:app` | Import `app` from `app/main.py`, use object named `app` |
| `--reload` | Restart on file changes (dev only) |
| `--port 8000` | Listen on localhost:8000 |

**Frontend** (from `scholarship-match/frontend/`):

```bash
npm run dev
```

Runs Vite on port 5173. Browser: `http://localhost:5173`.

**Windows shortcut:** `START_BOTH.bat` at repo root starts both (if present).

### 4. What happens internally

1. OS loads Python/Node binary into memory
2. Process binds TCP socket to port
3. Browser/client connects via `localhost` (loopback — stays on your machine)

### 5. Common mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Port already in use | `Address already in use` | Kill old process or change port |
| Wrong cwd | `ModuleNotFoundError: app` | `cd scholarship-match` first |
| Firewall block | Cannot reach from phone on LAN | Allow port or use `0.0.0.0` |

### 6. Check what's using a port (Windows)

```powershell
netstat -ano | findstr :8000
```

---

## Day-0 rebuild: first terminal session

```bash
# 1. Create workspace
mkdir Iskonnect
cd Iskonnect

# 2. Verify location
pwd

# 3. Create backend folder (Day 0 name might have been scholarship-match)
mkdir scholarship-match
cd scholarship-match

# 4. Verify empty project
ls
```

At this point you have an empty project folder — the same state as "commit zero."

---

## How engineers think

| Level | Behavior |
|-------|----------|
| Beginner | Copies commands without understanding cwd |
| Intermediate | Checks `pwd` when imports fail |
| Senior | Scripts cwd assumptions; documents required cwd in README |

**Production failure:** Deploy script runs `alembic upgrade` from wrong directory → `alembic.ini` not found → migration skipped → schema drift → 500 errors.

---

## Exercises

### Level 1 — Understanding

1. What is the difference between `cd scholarship-match` and `cd /scholarship-match` on Windows?
2. Why does `uvicorn app.main:app` fail if run from `C:\Iskonnect` instead of `C:\Iskonnect\scholarship-match`?

<details>
<summary>Solution</summary>

1. `cd scholarship-match` is relative to cwd. `cd /scholarship-match` would try root of current drive (often wrong on Windows).
2. Python looks for package `app` in cwd. Without `scholarship-match` as cwd, there is no `app/` folder on `PYTHONPATH`.
</details>

### Level 2 — Implementation

1. From empty folder, recreate the directory tree: `scholarship-match/app`, `scholarship-match/frontend`, `scholarship-match/docs`.
2. Create empty `requirements.txt` with `touch` or `New-Item`.

### Level 3 — Debugging

1. Start backend on 8000. Start a second terminal and try starting again. Capture the error. Kill the first process and retry successfully.

### Level 4 — Architecture

1. Production uses `gunicorn` with multiple workers ([`Procfile`](../../../Procfile)), not `uvicorn --reload`. Explain why `--reload` must never run in production.

<details>
<summary>Solution</summary>

`--reload` watches files and restarts workers — wastes CPU, causes mid-request restarts, and is a security risk if file watching is exploited. Production wants stable multi-worker processes behind a reverse proxy; code changes go through deploy, not hot reload.
</details>

---

*Previous: [01 — How Engineers Think](01-how-engineers-think.md) | Next: [03 — Git & Version Control](03-git-and-version-control.md)*
