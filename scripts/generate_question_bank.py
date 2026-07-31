#!/usr/bin/env python3
"""Generate PROGRAMMING_MASTERY_QUESTION_BANK.md from ENGINEERING_KNOWLEDGE_PORTFOLIO.md."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "ENGINEERING_KNOWLEDGE_PORTFOLIO.md"
OUTPUT = ROOT / "PROGRAMMING_MASTERY_QUESTION_BANK.md"

TRACKER = """
- Confidence (1–5): ___
- Correct / Incorrect: ___
- Date Practiced: ___
- Next Review Date: ___
"""

_qid = 0


def q(text: str, qid_prefix: str = "GEN") -> str:
    global _qid
    _qid += 1
    return f"\n**Q-{qid_prefix}-{_qid:04d}:** {text}\n{TRACKER}"


def section(title: str, level: int, questions: list[str], prefix: str) -> str:
    lines = [f"\n### LEVEL {level} — {title}\n"]
    for text in questions:
        lines.append(q(text, prefix))
    return "".join(lines)


def parse_portfolio_headings() -> list[tuple[str, str]]:
    text = PORTFOLIO.read_text(encoding="utf-8")
    items: list[tuple[str, str]] = []
    current_section = ""
    for line in text.splitlines():
        if line.startswith("## SECTION"):
            current_section = line.replace("## ", "").strip()
        elif line.startswith("### ") and not line.startswith("### LEVEL"):
            subsection = line.replace("### ", "").strip()
            if subsection not in ("Present — with evidence", "Explicitly ABSENT — and why", "NOT Used (and why)"):
                items.append((current_section, subsection))
    return items


def build_coverage_index() -> str:
    rows = [
        ("SECTION 1 — Programming Concepts", "Python Fundamentals, OOP", "Q-PY, Q-OO"),
        ("SECTION 2 — Python Syntax", "Python Syntax", "Q-SY"),
        ("SECTION 3 — FastAPI", "FastAPI", "Q-FA"),
        ("SECTION 4 — SQLAlchemy", "SQLAlchemy", "Q-SA"),
        ("SECTION 5 — Pydantic", "Pydantic", "Q-PD"),
        ("SECTION 6 — Database Design", "Database Design, Migrations Deep Dive", "Q-DB, Q-MG"),
        ("SECTION 7 — Backend Architecture", "Software Architecture", "Q-AR"),
        ("SECTION 8 — Data Structures", "Data Structures", "Q-DS"),
        ("SECTION 9 — Algorithms", "Algorithms, ISKONNECT Domain", "Q-AL, Q-DM"),
        ("SECTION 10 — Big O", "Big O", "Q-BO"),
        ("SECTION 11 — HTTP/REST/JSON", "HTTP, REST, JSON", "Q-HR"),
        ("SECTION 12 — Security", "Authentication & JWT, Security", "Q-AU, Q-SE"),
        ("SECTION 13 — Principles", "Engineering Principles", "Q-PR"),
        ("SECTION 14 — Patterns", "Design Patterns", "Q-PT"),
        ("SECTION 15 — Testing", "Testing", "Q-TE"),
        ("SECTION 16 — DevOps", "DevOps & Deployment, Forgotten Details", "Q-DV, Q-FD"),
        ("SECTION 17 — Git", "Git", "Q-GT"),
        ("SECTION 18 — Glossary", "Engineering Vocabulary", "Q-VO"),
        ("SECTION 19 — Hidden Learning", "ISKONNECT Domain, Portfolio-Driven Recall", "Q-DM, Q-PF"),
        ("SECTION 21 — Frontend", "Frontend Appendix", "Q-FE"),
        ("Cross-cutting code & incidents", "Code Reading, Debugging, Interview, Professor", "Q-CR, Q-DG, Q-IV, Q-PFX"),
    ]
    lines = ["## Coverage Index (Portfolio → Topic → Question IDs)\n\n", "| Portfolio Section | Topic(s) | Question ID Prefix(es) |\n", "|---|---|---|\n"]
    for sec, topic, qids in rows:
        lines.append(f"| {sec} | {topic} | {qids} |\n")
    return "".join(lines)


def build_coverage_checklist(headings: list[tuple[str, str]]) -> str:
    lines = ["## Portfolio Coverage Checklist\n", "| Portfolio Section | Subsection | Covered |\n", "|---|---|---|\n"]
    for sec, sub in headings:
        lines.append(f"| {sec} | {sub} | [ ] |\n")
    return "".join(lines)


def ensure_all_levels(name: str, prefix: str, levels: dict[int, list[str]]) -> dict[int, list[str]]:
    """Ensure levels 1-16 exist with at least 3 prompts each (17 = inline tracker)."""
    fillers = {
        2: [
            f"Define the core concept of {name} as documented in ENGINEERING_KNOWLEDGE_PORTFOLIO.md.",
            f"Define one ISKONNECT-specific term central to {name}.",
            f"Define one boundary or 'absent' decision related to {name}.",
        ],
        3: [
            f"Why did ISKONNECT make the main architectural choice in {name}?",
            f"Why is the portfolio's 'If removed' consequence for {name} significant?",
            f"Why is the alternative listed in the portfolio rejected for {name}?",
        ],
        4: [
            f"Compare two approaches mentioned in {name} section of the portfolio.",
            f"Compare ISKONNECT's choice vs common tutorial default for {name}.",
            f"Compare two related files or modules under {name}.",
        ],
        5: [
            f"Explain step-by-step internal mechanics for one {name} flow in ISKONNECT.",
            f"Explain what happens at runtime when {name} code path executes.",
            f"Explain how data moves through components in {name}.",
        ],
        6: [
            f"Read one cited file in {name} — what is its single responsibility?",
            f"Read one cited function in {name} — what breaks if you delete the first line?",
            f"Read one cited config in {name} — which env var controls it?",
        ],
        7: [
            f"Reconstruct one missing function signature from {name} from memory.",
            f"Reconstruct one missing import block needed for {name}.",
            f"Reconstruct one missing decorator used in {name}.",
        ],
        8: [
            f"Type one CLI command documented for {name}.",
            f"Type one git command relevant to {name} workflow.",
            f"Type one pytest or alembic command relevant to {name}.",
        ],
        9: [
            f"Given a realistic {name} failure symptom from portfolio, diagnose root cause.",
            f"Given a test file guarding {name}, what regression does it prevent?",
            f"Given a production incident tied to {name}, what permanent test was added?",
        ],
        10: [
            f"From memory, reconstruct the {name} flow end-to-end in ISKONNECT.",
            f"From memory, list all files involved in {name}.",
            f"From memory, explain {name} to a new teammate in 60 seconds.",
        ],
        11: [
            f"Whiteboard: draw one diagram required to explain {name}.",
            f"Whiteboard: draw data flow for {name} without labels, then label from memory.",
            f"Whiteboard: draw component boxes for {name} only from memory.",
        ],
        12: [
            f"State Big-O of the dominant operation in {name} per portfolio §10.",
            f"Name one bottleneck in {name} and one listed optimization path.",
            f"Would a different data structure improve {name} per portfolio — why or why not?",
        ],
        13: [
            f"Build from scratch: implement one minimal {name} component with no notes.",
            f"Build from scratch: implement one test for {name} behavior.",
            f"Build from scratch: implement one config guard related to {name}.",
        ],
        14: [
            f"Senior backend interview: hardest question about {name} in ISKONNECT — answer aloud.",
            f"Senior backend interview: defend tradeoffs in {name} under scale.",
            f"Senior backend interview: what would you redesign in {name} for 10× traffic?",
        ],
        15: [
            f"Professor oral exam: connect {name} to a first-principles CS course concept.",
            f"Professor oral exam: where does {name} appear in your ISKONNECT defense?",
            f"Professor oral exam: what mistake did you make in {name} and how did tests fix it?",
        ],
        16: [
            f"Forgotten detail: default value or constant in {name}.",
            f"Forgotten detail: exact file path for {name}.",
            f"Forgotten detail: env var or flag for {name}.",
        ],
    }
    out = dict(levels)
    for lvl in range(1, 17):
        existing = out.get(lvl) or []
        if len(existing) < 3:
            need = 3 - len(existing)
            out[lvl] = existing + fillers[lvl][:need]
    return out


def code_reading_supplement() -> str:
    """Level 6/7 blocks with real ISKONNECT anchors."""
    snippets = [
        ("main.py lifespan", "What runs inside `async def lifespan` before `yield`? Name four calls/checks."),
        ("main.py routers", "Why is the comment about sample-matches critical? What HTTP error if violated?"),
        ("db.py get_db", "Write the full get_db function from memory including finally block."),
        ("auth.py create_access_token", "List JWT claims: sub, role, iat, exp, typ, jti — what does each mean?"),
        ("auth.py consume_refresh_token_rotation", "What happens to old refresh row during rotation?"),
        ("engine.py score", "Write the three-step score method: components, weighted sum, clamp."),
        ("engine.py _normalized_weights", "When is geographic weight zeroed? When field_alignment?"),
        ("match_service.py sort", "Write the full 5-element sort key tuple from memory."),
        ("eligibility_result.py _derive_status", "Write decision tree: UNMET → ? UNKNOWN → ? needs_review → ?"),
        ("duplicate_candidates.py", "Write _token_set_ratio formula and provider/link bonuses."),
        ("config.py validate_for_production", "List eight conditions that raise RuntimeError in production."),
        ("conftest.py api_with_db", "How is get_db overridden? When is override cleared?"),
        ("scholarship_cache.py", "Redis key name and TTL seconds?"),
        ("limiter.py", "What is storage URI when REDIS_URL unset?"),
        ("Procfile", "Write release and web lines from memory."),
        ("middleware request_logger", "How is X-Request-ID chosen if client sends none?"),
        ("jsonb_filters.py", "Why cast to Text before ilike?"),
        ("hard_filters.py filter_scholarships", "What tuple does it return besides eligible list?"),
        ("schemas.py split_pipe_lists", "What does mode='before' validator do to CSV strings?"),
        ("test_production_regressions.py", "Name all seven production incidents guarded."),
    ]
    out = ["\n# TOPIC: Code Reading and Completion (Cross-Cutting)\n\n### LEVEL 6 — Code Reading\n"]
    prefix = "CR"
    for title, qtext in snippets:
        out.append(q(f"[{title}] {qtext}", prefix))
    out.append("\n### LEVEL 7 — Code Completion\n")
    completions = [
        "Complete WeightedDeterministicScorer.score() weighted sum and clamp lines.",
        "Complete create_access_token jwt.encode call with algorithm from settings.",
        "Complete require_admin role check raising 403.",
        "Complete health endpoint db.execute(text('SELECT 1')).",
        "Complete scholarship search offset/limit with max 50 clamp.",
        "Complete revoke_access_token Redis setex with jti key pattern.",
        "Complete SessionLocal = sessionmaker(autocommit=..., autoflush=..., bind=engine).",
        "Complete CORSMiddleware registration with allow_credentials=True.",
        "Complete @limiter.limit decorator on a route with Request first param.",
        "Complete filter_scholarships return diagnostics dict structure.",
        "Complete field_validator empty_str_to_none for optional URL fields.",
        "Complete Alembic env.py target_metadata assignment.",
        "Complete issue_refresh_token db.add and flush before return raw.",
        "Complete invalidate_scholarship_cache Redis delete and process cache clear.",
        "Complete evaluate_eligibility loop over _evaluators_for_opportunity.",
    ]
    for c in completions:
        out.append(q(c, prefix))
    return "".join(out)


def debugging_supplement() -> str:
    scenarios = [
        ("Route shadowing", "GET /api/v1/profiles/sample-matches returns 422 Unprocessable Entity. Logs show validation on profile_id. Diagnose."),
        ("JSONB ilike", "Search works in CI SQLite tests but fails on Postgres production for combined JSONB filters. Diagnose."),
        ("Admin datetime", "GET /api/v1/admin/data-quality returns 500 after admin enters last_verified_at. Diagnose timezone handling."),
        ("Timeline NameError", "GET /api/v1/plan/{id} 500 for profiles with large catalog. Error mentions undefined name in timeline builder. Diagnose."),
        ("Default SECRET_KEY", "API starts on Render with ENVIRONMENT=production. Should it have booted? Which function failed?"),
        ("Rate limit workers", "Two gunicorn workers, no REDIS_URL. Clients report inconsistent 429 behavior. Diagnose."),
        ("Stale cache", "Admin updates scholarship title; public search shows old title for 5 minutes. Diagnose cache layer."),
        ("Alembic CI", "migrate-postgres job fails on downgrade base. What is CI testing and why?"),
        ("CORS Vercel", "Browser console CORS error calling Render API from Vercel frontend. List checks in order."),
        ("Refresh reuse", "Client reuses old refresh token after successful refresh. Should it work? Diagnose rotation logic."),
        ("Missing invalidation", "POST scholarship create succeeds but match run uses stale eligibility JSON. Diagnose cache invalidation."),
        ("Auth disabled prod", "Pen test finds AUTH_DISABLED=true in production env. What should have prevented boot?"),
        ("Pool timeout", "Intermittent 503 on /health during traffic spike. DB pool settings involved?"),
        ("Route rate limit", "429 on all endpoints from single IP behind university NAT. Which header/trust setting matters?"),
        ("Import contract", "CSV import passes locally but CI test_import_contract fails. What class of bug?"),
        ("Eval regression", "CI test_eval_regression fails recall below 0.99. What subsystem changed?"),
        ("Merge delete FK", "Admin merge-and-delete fails with FK violation on saved_scholarships. Expected admin flow step?"),
        ("SQLite FK", "Local test FK cascade does not work until engine connect event added. What pragma?"),
        ("OpenAPI prod", "Pen tester finds /docs on production URL. Should it exist per config?"),
        ("Email verify", "Users cannot login after register when REQUIRE_EMAIL_VERIFICATION true but SMTP unset. Expected prod guard?"),
    ]
    out = ["\n# TOPIC: Debugging Scenarios (Portfolio Incidents)\n\n### LEVEL 9 — Debugging\n"]
    for i, (title, text) in enumerate(scenarios, 1):
        out.append(q(f"Scenario {i} ({title}): {text}", "DG"))
    return "".join(out)


def interview_supplement() -> str:
    qs = [
        "Design ISKONNECT auth for 1M users with same JWT+refresh model — what breaks first?",
        "Explain why you chose weighted sum scoring over ML for regulated student data.",
        "How would you shard scholarship catalog search at 10M rows without losing filter invariants?",
        "Defend no SQLAlchemy relationships to a Django-experienced interviewer.",
        "How does your rate limiter behave under DDoS from rotating IPs behind CDN?",
        "Explain idempotency of PUT /profiles/me vs POST /match-runs to Stripe engineer.",
        "What is your disaster recovery story for Supabase Postgres + Render API?",
        "How would you observability-stack beyond Sentry for match latency SLO?",
        "Explain bcrypt cost vs user experience on login cold path.",
        "Why is explainability EligibilityResult a legal/product requirement not tech debt?",
        "Compare your staging import pipeline to event-sourced catalog — tradeoffs.",
        "How would you implement cursor pagination without breaking superset filter tests?",
        "Redis down — enumerate degraded behaviors across cache, rate limit, denylist.",
        "Security review: JWT in localStorage on frontend — accept or change?",
        "How do GitHub Action crons relate to at-least-once execution semantics?",
        "Walk through SQL injection defenses beyond ORM in admin raw analytics.",
        "Why gunicorn sync workers with async middleware — event loop implications?",
        "Capacity plan: match run CPU bound on 500 scholarships — vertical or horizontal?",
        "How would you test production config guards without deploying to prod?",
        "Design canary deploy for scoring weight change without user-visible rank shock.",
    ]
    out = ["\n# TOPIC: Senior Engineering Interview (Cross-Cutting)\n\n### LEVEL 14 — Engineering Interview\n"]
    for qtext in qs:
        out.append(q(qtext, "IV"))
    return "".join(out)


def professor_supplement() -> str:
    qs = [
        "Connect functions and modularity to your auth.py and matching/ modules.",
        "Where does abstraction appear beyond ScoringEnginePort? Give three examples.",
        "Where did dictionaries become essential — cache, indexes, payloads?",
        "How did Big-O thinking change your duplicate detection acceptance criteria?",
        "Where did if/elif control flow encode policy in eligibility_result.py?",
        "Explain encapsulation without ORM relationships — what boundaried modules?",
        "How does your project demonstrate ACID in application code not just Postgres?",
        "Where did you apply decomposition in the two-stage match pipeline?",
        "How would EEE 111 recursion concept apply or not apply to your evaluators?",
        "Where is state minimized vs stored deliberately in ISKONNECT?",
        "How did testing change your understanding of 'done' for backend features?",
        "Explain client-server model using Vercel + Render + Supabase diagram.",
        "Where did you learn separation of concerns — give folder-level evidence.",
        "How does your CSV import contract relate to schema validation theory?",
        "Connect hash functions lecture to dedupe_key and refresh token storage.",
        "Where did concurrency appear in gunicorn + Redis — not asyncio business logic?",
        "How does your growth section claim about invariants show engineering maturity?",
        "Defend your project as software engineering not just web development.",
        "What would you teach a junior using only ISKONNECT match_service.py?",
        "How does incident-to-test discipline embody professional software practice?",
    ]
    out = ["\n# TOPIC: Professor Oral Exam (Cross-Cutting)\n\n### LEVEL 15 — Professor Oral Exam\n"]
    for qtext in qs:
        out.append(q(qtext, "PFX"))
    return "".join(out)


def topic_block(name: str, prefix: str, levels: dict[int, list[str]]) -> str:
    out = [f"\n---\n\n# TOPIC: {name}\n"]
    level_names = {
        1: "Rapid Recall",
        2: "Definitions",
        3: "Explain Why",
        4: "Compare and Contrast",
        5: "Internal Mechanics",
        6: "Code Reading",
        7: "Code Completion",
        8: "Command Recall",
        9: "Debugging",
        10: "Architecture Reconstruction",
        11: "Whiteboard Exercises",
        12: "Big O",
        13: "Build From Scratch",
        14: "Engineering Interview",
        15: "Professor Oral Exam",
        16: "Forgotten Details",
    }
    for lvl in range(1, 17):
        if lvl in levels and levels[lvl]:
            out.append(section(level_names[lvl], lvl, levels[lvl], prefix))
    return "".join(out)


def wrap_topic(name: str, prefix: str, levels: dict[int, list[str]]) -> str:
    return topic_block(name, prefix, ensure_all_levels(name, prefix, levels))


# --- TOPIC DATA (from ENGINEERING_KNOWLEDGE_PORTFOLIO.md) ---

PYTHON_FUNDAMENTALS = {
    1: [
        "What file defines the module-level `settings` singleton?",
        "What does `yield` do in `get_db()`?",
        "Name one place ISKONNECT uses `global` and why.",
        "What is stored in `_EVALUATOR_REGISTRY`?",
        "What Python construct does FastAPI use for request-scoped DB cleanup?",
        "What is the difference between authentication and authorization in ISKONNECT?",
        "What does `from __future__ import annotations` enable?",
        "What library hashes passwords in ISKONNECT?",
        "What algorithm signs JWT access tokens?",
        "What is the default access token expiry in minutes?",
        "What file contains `QualificationStatus`?",
        "What ABC defines the scoring engine contract?",
        "What does `Depends(get_db)` inject into route handlers?",
        "What is the purpose of `app.dependency_overrides` in tests?",
        "What async construct wraps FastAPI startup/shutdown?",
        "What storage backs rate limits when `REDIS_URL` is unset?",
        "What is `StaticPool` used for?",
        "How many SQLAlchemy model classes exist in `models.py`?",
        "Does ISKONNECT use SQLAlchemy `relationship()`?",
        "What pattern does `get_db()` use instead of returning a session directly?",
    ],
    2: [
        "Define dependency injection in the context of FastAPI.",
        "Define a generator function as used in `get_db()`.",
        "Define module scope vs function scope using an ISKONNECT example.",
        "Define pure function using `score_academic()` as evidence.",
        "Define serialization vs deserialization in ISKONNECT.",
        "Define concurrency as it applies to gunicorn workers and Redis.",
        "Define immutability using `frozenset` in ISKONNECT.",
        "Define closure using `nonlocal pid` in eval data generation.",
        "Define reflection using `getattr` in catalog admin merge.",
        "Define statelessness in the ISKONNECT API.",
    ],
    3: [
        "Why is `settings = Settings()` a module singleton instead of `@lru_cache`?",
        "Why does `get_db()` use `yield` instead of `return`?",
        "Why are lazy imports used for `sentry_sdk` in `main.py`?",
        "Why does ISKONNECT use absolute imports only?",
        "Why is most matching/scoring logic synchronous inside an async FastAPI app?",
        "Why use `frozenset` for `_STOP_WORDS` and `APPLICATION_STATUSES`?",
        "Why store refresh tokens hashed but send access tokens as JWT?",
        "Why use explicit SQLAlchemy queries instead of ORM relationships?",
        "Why use a global exception handler in addition to `HTTPException`?",
        "Why log a warning when `AUTH_DISABLED=true` at startup?",
    ],
    4: [
        "Compare mutable dict match results vs immutable `frozenset` constants.",
        "Compare module-level singleton vs request-scoped session.",
        "Compare sync business logic vs async middleware in ISKONNECT.",
        "Compare `get_optional_user_id` vs `get_current_user_id` vs `require_admin`.",
        "Compare generator-based `get_db()` vs manual try/finally in every route.",
        "Compare inheritance (`ScoringEnginePort`) vs composition (`MatchService` injects scorer).",
    ],
    5: [
        "How does Python resolve `from app.config import settings` at import time?",
        "How does a generator-based dependency clean up after the request ends?",
        "How does `global _process_cache` interact with multiple gunicorn workers?",
        "How does FastAPI resolve nested `Depends()` chains?",
        "How does the identity map behave within one SQLAlchemy session per request?",
    ],
    6: [
        "Read `app/db.py` `get_db()`. What happens in `finally`? What breaks if removed?",
        "Read `app/main.py` lifespan. What runs before `yield`? What is `_run_startup_migrations()` gated by?",
        "Read `app/auth.py` `create_access_token`. List every JWT claim field.",
        "Read `app/matching/scoring_port.py`. What must any scorer implement?",
        "Read `app/scholarship_cache.py`. What happens on cache miss?",
    ],
    7: [
        "Complete `get_db()`: missing `yield`, `finally`, and `db.close()`.",
        "Complete `create_access_token` payload dict with all required keys.",
        "Complete the `require_admin` dependency: check for None user and role != admin.",
        "Complete a list comprehension that builds `scored_by_id = {m.get('id'): m for m in scored_matches}`.",
        "Complete `@asynccontextmanager async def lifespan(app):` startup validation calls.",
    ],
    8: [
        "Type the command to run all backend tests with verbose output and short tracebacks.",
        "Type the command to collect pytest tests without running them.",
        "Type the Alembic command to upgrade to latest migration.",
        "Type the command to run the API with uvicorn on port 8000 (local dev).",
        "Type the exact Procfile `release` command.",
        "Type the exact Procfile `web` gunicorn command pattern.",
        "Type the command to run link checker job module.",
        "Type the command to run catalog maintenance via expire script.",
        "Type `git log --oneline -5` purpose in one sentence, then run it mentally on this repo.",
        "Type the command used in CI for frontend tests.",
    ],
    9: [
        "Symptom: `GET /api/v1/profiles/sample-matches` returns 422. What route ordering bug causes this?",
        "Symptom: Rate limits seem 2× too generous with 2 gunicorn workers and no Redis. Diagnose.",
        "Symptom: API starts in production with default SECRET_KEY. Which function should have blocked this?",
        "Symptom: Scholarship list stale after admin edit. Which function should have been called?",
        "Symptom: Logout does not invalidate access token until expiry and no Redis. Why?",
    ],
    10: [
        "From memory, list the middleware order in `app/main.py`.",
        "From memory, trace POST `/api/v1/match-runs` from JWT to DB persist.",
        "From memory, draw the auth flow: login → access + refresh → protected route → refresh → logout.",
        "From memory, name every top-level folder under `app/` and one responsibility each.",
    ],
    11: [
        "Draw the FastAPI middleware stack in order.",
        "Draw the JWT access token lifecycle including optional Redis denylist.",
        "Draw the two-stage matching pipeline: hard filter → score → rank.",
        "Draw the deployment diagram: Browser → Vercel → Render → Supabase.",
    ],
    12: [
        "What is the time complexity of `filter_scholarships` over N scholarships with E evaluators?",
        "What is the complexity of sorting M match results in `match_service.py`?",
        "What is the complexity of fuzzy duplicate detection pairwise pass?",
        "What is the complexity of bcrypt verify vs JWT decode?",
        "What makes offset pagination expensive at high page numbers?",
    ],
    13: [
        "Build `get_db()` from scratch with SessionLocal, yield, and close in finally.",
        "Build `hash_password` and `verify_password` using bcrypt.",
        "Build `create_access_token` with sub, role, iat, exp, typ, jti using PyJWT HS256.",
        "Build `_normalized_weights` that zeroes geographic/field weights and renormalizes.",
        "Build `scholarship_dedupe_key(title, provider, link)` using SHA-256.",
        "Build a TTL cache get/set with Redis key `iskonnect:scholarships_json:v1` and 300s TTL.",
        "Build offset pagination: `offset = (page-1)*limit`, clamp limit to max 50.",
        "Build one `RequirementCheck` evaluator for income bracket vs threshold.",
    ],
    14: [
        "You have 2 gunicorn workers and in-memory rate limiting. What breaks in production?",
        "Why would you disable OpenAPI docs in production but keep them locally?",
        "Explain tradeoffs of no SQLAlchemy relationships in a 30-table schema.",
        "How would you scale duplicate detection beyond O(N²)?",
        "Defend weighted deterministic scoring vs ML for a scholarship product.",
    ],
    15: [
        "Professor: Where did functions improve modularity in your backend? Give three file examples.",
        "Professor: Where did dictionaries become essential? Give matching or cache examples.",
        "Professor: How did algorithmic thinking appear in your matching engine?",
        "Professor: Why was object-oriented programming useful if you avoided ORM relationships?",
        "Professor: Connect ACID properties to your application transaction pattern.",
    ],
    16: [
        "Default value of `ACCESS_TOKEN_EXPIRE_MINUTES`?",
        "Default value of `REFRESH_TOKEN_EXPIRE_DAYS`?",
        "Default `algorithm` for JWT in Settings?",
        "Default `WEB_CONCURRENCY`?",
        "Default scholarship cache TTL seconds?",
        "Default `db_pool_size` and `db_max_overflow`?",
        "What env var disables JWT checks for local dev?",
        "What env var must be false in production according to `validate_for_production()`?",
        "What is the Redis key prefix for revoked access tokens?",
        "What is the exact comment above `product_features.router` registration?",
    ],
}

PYTHON_SYNTAX = {
    1: [
        "Does ISKONNECT use `match`/`case`?",
        "Does ISKONNECT use the walrus operator `:=`?",
        "Does ISKONNECT use `@lru_cache`?",
        "Does ISKONNECT use `Protocol` or `TypeVar`?",
        "What PEP 604 syntax replaces `Optional[str]` in modern modules?",
        "Where is `Annotated[..., Depends(...)]` used?",
        "What does `# noqa: E712` silence in admin queues?",
        "Name one nested f-string location in the codebase.",
        "Name one `@dataclass(frozen=True)` location.",
        "Does ISKONNECT use relative imports (`from .`)?",
        "What set operator combines `LINK_FIELDS | STATUS_FIELDS`?",
        "What dict merge syntax appears in `opportunity_timeline.py`?",
        "What keyword-only parameter syntax uses `*` in signatures?",
        "Where is `nonlocal` used?",
        "Where is `raise ... from exc` used?",
    ],
    2: [
        "Define list comprehension vs generator expression with ISKONNECT examples.",
        "Define PEP 604 union syntax.",
        "Define `Literal` type alias as used in schemas.",
        "Define `TypedDict` as used for `SchoolEntry`.",
        "Define lazy import and why ISKONNECT uses it.",
    ],
    3: [
        "Why use generator expression in `sum(1 for r in rows if ...)` instead of len(list)?",
        "Why mix Pydantic v1 `class Config` with v2 `ConfigDict`?",
        "Why avoid walrus operator in this codebase style?",
        "Why use `field(default_factory=list)` instead of `= []`?",
        "Why cast JSONB columns to Text before ilike?",
    ],
    4: [
        "Compare `Optional[X]` vs `X | None`.",
        "Compare list comprehension vs explicit for-loop for readability here.",
        "Compare `{**a, **b}` vs `.update()` for timeline cards.",
        "Compare `@staticmethod` vs module-level function in scoring engine.",
        "Compare `sorted(key=lambda...)` vs implementing a heap (not used).",
    ],
    5: [
        "How does `@field_validator(mode='before')` change validation order?",
        "How does `@asynccontextmanager` transform a generator into a lifespan hook?",
        "How does `Annotated` metadata get consumed by FastAPI?",
    ],
    6: [
        "In `schemas.py`, what does `@field_validator` on pipe-separated lists accomplish?",
        "In `engine.py`, read `_normalized_weights`. What happens when all weights zero out?",
        "In `duplicate_candidates.py`, read `_token_set_ratio`. What formula is used?",
    ],
    7: [
        "Fill in missing `@field_validator` for splitting pipe-separated CSV lists.",
        "Fill in missing sort key tuple for match ranking.",
        "Fill in missing `Annotated[models.User, Depends(require_admin)]` parameter.",
        "Fill in missing `from __future__ import annotations` at top of auth module.",
    ],
    8: [
        "Type the module run command for `app.scripts.fix_gemini_csv`.",
        "Type the pattern `python -m app.jobs.<name>` for notification cleanup.",
        "Type pytest mark for parametrize (syntax only).",
    ],
    9: [
        "Bug: SQLAlchemy filter uses `== True` and linter complains. What noqa comment fixes it?",
        "Bug: Circular import between main and routes. What import strategy fixes it?",
        "Bug: Mutable default list on Pydantic model field. What pattern prevents shared state?",
    ],
    10: [
        "List Python syntax features ISKONNECT uses that you would reach for first in a new module.",
        "List syntax features explicitly absent and when you would introduce each.",
    ],
    11: [
        "Sketch the data flow from CSV pipe-string → field_validator → Python list → JSON in DB.",
    ],
    12: [
        "Complexity of list comprehension building catalog dicts size N?",
        "Complexity of set intersection in field token matching?",
    ],
    13: [
        "Implement `_token_set_ratio(a, b)` from memory.",
        "Implement a `@field_validator` that converts empty strings to None.",
        "Implement `cors_origins_list` property splitting comma-separated origins.",
    ],
    14: [
        "When would you add `@lru_cache` to ISKONNECT and why hasn't it been needed?",
        "When would `match/case` beat if/elif for eligibility status?",
    ],
    15: [
        "Professor: Show where type hints improved API documentation in FastAPI.",
        "Professor: Where did list comprehensions reduce bugs vs manual loops?",
    ],
    16: [
        "What Python version does `runtime.txt` pin?",
        "What is `DEFAULT_SECRET_KEY_VALUE` string used for guards?",
        "Name three stdlib modules used in CLI scripts (pathlib, argparse, ...).",
        "Is `typing.cast()` used for types or SQLAlchemy cast?",
        "Is `collections.Counter` used anywhere?",
    ],
}

FASTAPI = {
    1: [
        "How is the FastAPI app instantiated — factory or module-level?",
        "How many routers mount under `/api/v1`?",
        "What disables `/docs` in production?",
        "Name all four middleware layers in add order.",
        "What header carries request correlation ID?",
        "What library provides rate limiting?",
        "What must be the first parameter on rate-limited routes?",
        "What dependency provides DB session?",
        "What exception returns 429?",
        "What endpoint is public for uptime monitoring?",
        "What endpoint requires admin JWT for operational counts?",
        "Does ISKONNECT use `BackgroundTasks`?",
        "What is `app.state.limiter` for?",
        "What auth scheme uses `HTTPBearer(auto_error=False)`?",
        "What query param pattern validates `limit` with ge/le on match runs?",
    ],
    2: [
        "Define APIRouter in ISKONNECT.",
        "Define lifespan vs startup event.",
        "Define response_model purpose.",
        "Define CORSMiddleware role.",
        "Define slowapi key function purpose.",
    ],
    3: [
        "Why register `product_features` before `profiles`?",
        "Why disable OpenAPI in production?",
        "Why use SlowAPIMiddleware before CORS?",
        "Why require `request: Request` on limited routes?",
        "Why use global Exception handler instead of only HTTPException?",
        "Why not use BackgroundTasks for link checking?",
    ],
    4: [
        "Compare lifespan vs import-time initialization in main.py.",
        "Compare HTTPBearer auto_error False vs True.",
        "Compare public /health vs admin /metrics.",
        "Compare Query validation vs Pydantic body validation.",
    ],
    5: [
        "Describe FastAPI dependency resolution order for nested Depends.",
        "Describe middleware onion model for incoming vs outgoing requests.",
        "Describe how OpenAPI schema is generated from type hints.",
    ],
    6: [
        "Read main.py router includes. Which router must come before profiles and why?",
        "Read global_exception_handler. What is returned to client vs logged?",
        "Read SecurityHeadersMiddleware. Name three headers set.",
    ],
    7: [
        "Complete router registration block with product_features before profiles.",
        "Complete `@limiter.limit('60/minute')` decorator on a GET route skeleton.",
        "Complete CORSMiddleware allow_origins from settings.",
        "Complete health endpoint db.execute(text('SELECT 1')).",
    ],
    8: [
        "Type uvicorn command from docker-compose for local API.",
        "Type the import path string gunicorn uses in Procfile.",
        "Type curl path used by keepalive workflow (pattern).",
    ],
    9: [
        "422 on sample-matches — diagnose route shadowing.",
        "500 with request_id in body but no stack trace — which handler?",
        "429 without Redis in multi-worker — why inconsistent limits?",
        "CORS error from Vercel — which env var on Render?",
    ],
    10: [
        "Reconstruct full middleware + router + handler path for GET /api/v1/scholarships/search.",
        "List all top-level non-/api/v1 routes on app.",
    ],
    11: [
        "Draw dependency graph: require_admin → get_current_user → HTTPBearer.",
    ],
    12: [
        "Cost of running Pydantic validation on large POST body?",
        "Cost per request for 4 middleware layers?",
    ],
    13: [
        "Build minimal FastAPI app with CORSMiddleware and one GET /health.",
        "Build require_admin dependency chain from scratch.",
        "Build global exception handler returning request_id JSON.",
    ],
    14: [
        "Design rate limiting for 1000 req/s public search — extend current approach how?",
        "How would you version /api/v2 without breaking v1 clients?",
    ],
    15: [
        "Professor: How does FastAPI enforce separation between transport and domain logic in your project?",
        "Professor: Where does validation happen before business logic touches DB?",
    ],
    16: [
        "Exact string limit pattern on many routes (e.g. 60/minute)?",
        "What environments disable docs_url?",
        "What integration captures exceptions with request_id tag?",
        "File path for request logger middleware?",
        "File path for security headers middleware?",
    ],
}

# Additional compact topics - merge into generation

def glossary_questions() -> dict[int, list[str]]:
    terms = [
        "ACID", "Alembic", "API", "Async/Await", "Authentication", "BaseSettings", "bcrypt", "Big-O",
        "Bearer Token", "CASCADE", "CI/CD", "CORS", "CRUD", "Dataclass", "Dependency Injection", "DRY",
        "DTO", "EligibilityResult", "Enum", "ORM", "FastAPI", "Fixture", "Foreign Key", "Generator",
        "GIN Index", "Gunicorn", "Hard Filter", "HS256", "HTTP Status Code", "Idempotency", "Index",
        "SQL Injection", "JSON", "JSONB", "JWT", "Keyword-only argument", "Lazy Loading", "Lifespan",
        "Literal", "Middleware", "Migration", "MatchService", "Normalization", "Nullable", "OpenAPI",
        "Offset Pagination", "Parameterized Query", "Pydantic", "Primary Key", "PSCED",
        "QualificationStatus", "Rate Limiting", "Redis", "Referential Integrity", "Refresh Token",
        "REST", "RLS", "Schema", "Serialization", "Session", "SET NULL", "SOLID", "Sentry", "Staging",
        "StaticPool", "Transaction", "TTL Cache", "TypedDict", "Type Hint", "Unique Constraint",
        "Unit of Work", "Uvicorn", "Validation", "Vercel", "Weighted Scoring", "Worker",
        "X-Request-ID", "YAGNI",
    ]
    l1 = [f"What is {t} in ISKONNECT context?" for t in terms]
    l2 = [f"Define {t} precisely as used in ENGINEERING_KNOWLEDGE_PORTFOLIO.md." for t in terms]
    l3 = [f"Why does {t} matter for ISKONNECT architecture?" for t in terms[:30]]
    l16 = [f"What file or config in ISKONNECT best exemplifies {t}?" for t in terms]
    return {1: l1, 2: l2, 3: l3, 16: l16}


def env_var_questions() -> dict[int, list[str]]:
    vars_ = [
        "ENVIRONMENT", "DATABASE_URL", "CORS_ORIGINS", "SECRET_KEY", "ACCESS_TOKEN_EXPIRE_MINUTES",
        "REFRESH_TOKEN_EXPIRE_DAYS", "AUTH_DISABLED", "RUN_MIGRATIONS_ON_STARTUP", "REDIS_URL",
        "WEB_CONCURRENCY", "TRUST_PROXY_HEADERS", "SENTRY_DSN", "STRUCTURED_LOGGING",
        "ENABLE_LINK_CHECKER", "ENABLE_NOTIFICATIONS", "DB_DRIVEN_WEIGHTS", "RETENTION_INACTIVE_DAYS",
        "REQUIRE_EMAIL_VERIFICATION", "SMTP_HOST", "EMAIL_FROM", "FRONTEND_URL", "DB_POOL_SIZE",
        "DB_MAX_OVERFLOW", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SCHOLARSHIP_IMAGE_BUCKET",
        "SCHOLARSHIP_IMAGE_MAX_BYTES", "VITE_API_BASE_URL", "VITE_SENTRY_DSN", "FILTER_EXPIRED_FROM_MATCHES",
    ]
    l1 = [f"What is the purpose of env var `{v}`?" for v in vars_]
    l3 = [f"Why must `{v}` be set correctly in production?" for v in vars_[:20]]
    l16 = [f"What breaks if `{v}` is missing or wrong?" for v in vars_]
    l8 = [
        "Type the openssl command mentioned for generating SECRET_KEY.",
        "Type the Supabase pooler port number documented for DATABASE_URL.",
    ]
    return {1: l1, 3: l3, 8: l8, 16: l16}


def migration_questions() -> dict[int, list[str]]:
    migs = [
        ("001_initial_schema", "initial students and scholarships"),
        ("009_privacy_and_staging", "staging table"),
        ("011_add_reports_weights_versions_audit_notifications", "audit and versions"),
        ("013_students_unique_user_id", "duplicate student cleanup"),
        ("015_applications_and_feedback", "applications unique constraint"),
        ("017_performance_indexes", "is_active indexes"),
        ("019_application_drive_folder_and_soft_remove", "removed_at soft remove"),
        ("020_enable_rls_public_tables", "RLS enable"),
        ("022_fk_indexes_and_cascades", "FK cascades"),
        ("023_fk_cascades_dedupe_search", "dedupe_key and trgm"),
        ("029_jsonb_eligibility_gin", "JSONB GIN indexes"),
        ("034_catalog_audit_remediation", "data backfill"),
        ("035_school_eligibility", "school columns"),
        ("038_field_evidence", "field_evidence table"),
        ("043_scholarship_versions_cascade", "versions CASCADE FK"),
    ]
    l1 = [f"What did migration `{name}` introduce?" for name, _ in migs]
    l16 = [f"Migration file `{name}` — what problem did it solve?" for name, desc in migs]
    l3 = [f"Why was migration `{name}` needed?" for name, _ in migs[:10]]
    return {1: l1, 3: l3, 16: l16}


def generate_from_headings(headings: list[tuple[str, str]]) -> str:
    """One L1 question per portfolio subsection for coverage."""
    out = ["\n# TOPIC: Portfolio-Driven Recall (All Sections)\n\n### LEVEL 1 — Rapid Recall\n"]
    prefix = "PF"
    for sec, sub in headings:
        out.append(q(f"[{sec} / {sub}] State one testable fact from this subsection.", prefix))
        out.append(q(f"[{sec} / {sub}] Name one file, function, or config mentioned there.", prefix))
    out.append("\n### LEVEL 3 — Explain Why\n")
    for sec, sub in headings[:60]:
        out.append(q(f"[{sec} / {sub}] Why does this design choice exist in ISKONNECT?", prefix))
    return "".join(out)


def main() -> None:
    global _qid
    _qid = 0
    headings = parse_portfolio_headings()

    parts = [
        "# PROGRAMMING MASTERY QUESTION BANK — ISKONNECT\n\n",
        "> **Source:** [`ENGINEERING_KNOWLEDGE_PORTFOLIO.md`](ENGINEERING_KNOWLEDGE_PORTFOLIO.md) only.\n",
        "> **Purpose:** Active recall — no answers. Rebuild the backend from memory.\n",
        "> **Rule:** After every question, fill in the confidence tracker.\n\n",
        "## How to Use This Document\n\n",
        "1. Pick one **Topic**.\n",
        "2. Start at **LEVEL 1** — rapid fire without notes.\n",
        "3. Move up levels only when LEVEL 1–3 feel automatic.\n",
        "4. **LEVEL 13** means empty editor — no peeking.\n",
        "5. Spaced repetition: review `Next Review Date` weekly for scores ≤3.\n\n",
        "## Spaced Repetition Schedule (Suggested)\n\n",
        "| Confidence | Review interval |\n|---|---|\n| 1–2 | Next day |\n| 3 | 3 days |\n| 4 | 7 days |\n| 5 | 21 days |\n\n",
        build_coverage_checklist(headings),
        build_coverage_index(),
        "\n## Topic Index\n\n",
        "1. Python Fundamentals (`Q-PY`)\n2. Python Syntax (`Q-SY`)\n3. Object-Oriented Programming (`Q-OO`)\n",
        "4. Data Structures (`Q-DS`)\n5. Algorithms (`Q-AL`)\n6. Big O (`Q-BO`)\n7. Git (`Q-GT`)\n",
        "8. HTTP, REST, JSON (`Q-HR`)\n9. FastAPI (`Q-FA`)\n10. SQLAlchemy (`Q-SA`)\n11. Pydantic (`Q-PD`)\n",
        "12. Database Design (`Q-DB`)\n13. Authentication & JWT (`Q-AU`)\n14. Security (`Q-SE`)\n",
        "15. Software Architecture (`Q-AR`)\n16. Design Patterns (`Q-PT`)\n17. Engineering Principles (`Q-PR`)\n",
        "18. Testing (`Q-TE`)\n19. DevOps & Deployment (`Q-DV`)\n20. ISKONNECT Domain (`Q-DM`)\n",
        "21. Engineering Vocabulary (`Q-VO`)\n22. Forgotten Details (`Q-FD`)\n23. Migrations Deep Dive (`Q-MG`)\n",
        "24. Frontend Appendix (`Q-FE`)\n25. Code Reading & Completion (`Q-CR`)\n26. Debugging Scenarios (`Q-DG`)\n",
        "27. Senior Engineering Interview (`Q-IV`)\n28. Professor Oral Exam (`Q-PFX`)\n29. Portfolio-Driven Recall (`Q-PF`)\n\n",
    ]

    parts.append(wrap_topic("Python Fundamentals", "PY", PYTHON_FUNDAMENTALS))
    parts.append(wrap_topic("Python Syntax", "SY", PYTHON_SYNTAX))
    parts.append(wrap_topic("FastAPI", "FA", FASTAPI))

    # OOP topic (subset from fundamentals + patterns)
    OOP = {
        1: [
            "What class implements ScoringEnginePort?",
            "What ABC enforces score()?",
            "What dataclass holds scoring inputs?",
            "What enum defines NOT_ELIGIBLE?",
            "What middleware class extends BaseHTTPMiddleware?",
            "How many models inherit Base?",
            "What property computes FieldEvidence.is_active?",
            "What pattern does MatchService use for scoring_engine injection?",
        ],
        2: [
            "Define inheritance vs composition using MatchService.",
            "Define abstract method in ScoringEnginePort.",
            "Define encapsulation in catalog admin service.",
            "Define polymorphism via ScoringEnginePort.",
        ],
        3: [
            "Why MatchService depends on ScoringEnginePort not WeightedDeterministicScorer directly?",
            "Why str, Enum for QualificationStatus?",
            "Why no deep inheritance tree for models?",
        ],
        4: [
            "Compare inheritance vs composition for scoring.",
            "Compare dataclass vs Pydantic BaseModel.",
            "Compare ABC vs Protocol (Protocol absent — why ABC enough?).",
        ],
        13: [
            "Implement ScoringEnginePort ABC with one abstract score method.",
            "Implement ScoringPayload dataclass with all fields from portfolio.",
            "Implement MatchService constructor accepting optional ScoringEnginePort.",
        ],
        15: [
            "Professor: Where did abstraction help you swap or test scoring?",
            "Professor: Where would inheritance have hurt maintainability?",
        ],
    }
    parts.append(wrap_topic("Object-Oriented Programming", "OO", OOP))

    # Data structures
    DS = {
        1: [
            "What structure indexes matches by id in timeline?",
            "What structure dedupes timeline seen_ids?",
            "What structure holds token sets in field_match?",
            "What immutable structure stores APPLICATION_STATUSES?",
            "What structure groups duplicates by dedupe_key?",
            "Are heapq or deque used?",
            "Are Counter or OrderedDict used?",
        ],
        2: [
            "Define dict-as-index pattern in opportunity_timeline.",
            "Define frozenset constant pattern.",
            "Define adjacency via dict-of-lists in timeline lanes.",
        ],
        3: [
            "Why dict for scored_by_id not list scan?",
            "Why set intersection for tokens not nested loops only?",
            "Why frozenset for timing filter map values?",
            "Why no heap for top-k ranking?",
        ],
        4: [
            "Compare list vs dict for catalog iteration.",
            "Compare set vs list for membership tests.",
            "Compare tuple vs dict for sort keys.",
            "Compare defaultdict vs manual dict init in export scripts.",
        ],
        12: [
            "Average case dict lookup?",
            "Set intersection of two token sets size Ta, Tb?",
            "Space for storing full catalog dict cache?",
        ],
        13: [
            "Implement scored_by_id index from list of match dicts.",
            "Implement seen_ids dedupe in timeline bucket loop.",
            "Implement token set intersection for field match.",
        ],
        16: [
            "Name three modules using frozenset.",
            "Name module using defaultdict.",
        ],
    }
    parts.append(wrap_topic("Data Structures", "DS", DS))

    # Algorithms - comprehensive
    ALG = {
        1: [
            "How many evaluators in eligibility registry approx?",
            "What formula converts component scores to 0-100?",
            "What penalty applies when data_status is needs_review?",
            "What sort key tuple fields come before final_score?",
            "What fuzzy formula uses token sets (name)?",
            "What hash for dedupe_key?",
            "What max_per_lane default in timeline?",
            "What search pagination max limit?",
            "What completeness threshold for publishability?",
            "What default scoring weights for academic and income?",
        ],
        2: [
            "Define hard filter vs soft score in ISKONNECT.",
            "Define Sørensen–Dice token-set ratio as used.",
            "Define weight renormalization in scorer.",
            "Define top-k in timeline lanes.",
            "Define superset invariant for search filters.",
        ],
        3: [
            "Why two-stage filter then score?",
            "Why tuple sort key with deadline_passed first?",
            "Why 0.65 multiplier for needs_review?",
            "Why SHA-256 dedupe key include link?",
            "Why tiered fuzzy search scores?",
            "Why offset pagination not cursor?",
        ],
        4: [
            "Compare filtering vs ranking vs sorting in match pipeline.",
            "Compare exact dedupe vs fuzzy dedupe.",
            "Compare SQL search filter vs in-memory match filter.",
            "Compare token intersection vs SequenceMatcher use cases.",
        ],
        6: [
            "In match_service sort key — what does -final_score achieve?",
            "In components.py — what score when gwa_normalized is None?",
            "In duplicate_candidates — when does link_match force score 1.0?",
            "In hard_filters — what does _top_blockers return?",
        ],
        7: [
            "Complete weighted sum: base_score = sum(components[k]*norm[k] for k in components) * 100",
            "Complete token-set ratio formula.",
            "Complete needs_review final_score penalty line.",
            "Complete offset/limit pagination lines.",
        ],
        9: [
            "Matches include scholarships that should be filtered — which stage failed?",
            "Duplicate imports with different titles — which algorithm stage catches?",
            "Search timing=any smaller set than timing=archived — invariant violated?",
        ],
        10: [
            "Trace one scholarship through evaluate_eligibility → score → sort → persist.",
            "Trace CSV import → staging → approve → live catalog.",
        ],
        11: [
            "Draw six timeline lanes and where top-k trim happens.",
            "Draw eligibility evaluator registry by opportunity_type.",
        ],
        12: [
            "Overall match run complexity formula?",
            "Duplicate fuzzy pass complexity?",
            "Filter options endpoint that loads all rows in Python — complexity?",
        ],
        13: [
            "Implement _derive_status from RequirementCheck list.",
            "Implement score_academic with min_gwa_required branches.",
            "Implement find_duplicate_candidates threshold logic.",
            "Implement apply_timing_filter using TIMING_FILTER_MAP.",
            "Implement data_completeness weighted sum to 100.",
        ],
        14: [
            "How would you add ML scoring without breaking explainability contract?",
            "When does O(N²) duplicate detection become unacceptable?",
        ],
        15: [
            "Professor: Is your matching algorithm greedy, optimal, or heuristic? Defend.",
            "Professor: Where is deterministic reasoning preferable to ML?",
        ],
        16: [
            "Scoring policy version string in engine?",
            "Default weight for field_alignment?",
            "SOON_DAYS constant in temporal_state?",
            "PUBLISHABILITY_THRESHOLD value?",
            "Duplicate candidate return limit from fuzzy pass?",
        ],
    }
    parts.append(wrap_topic("Algorithms", "AL", ALG))

    # Big O dedicated topic
    BO = {
        1: [
            "Hard filter stage complexity in N and E?",
            "Sort matches complexity?",
            "bcrypt verify complexity class?",
            "JWT decode complexity?",
            "Redis denylist get complexity?",
        ],
        3: [
            "Why is O(N²) duplicate detection acceptable now?",
            "Why cache catalog as dicts — space tradeoff?",
            "Why statement_timeout 15s on Postgres?",
        ],
        4: [
            "Compare O(N) full catalog load vs indexed SQL prefilter.",
            "Compare O(offset) pagination vs cursor.",
        ],
        12: [
            "Fill complexity table row for load catalog cache hit.",
            "Fill complexity table row for persist match run.",
            "What optimization path mentions MinHash?",
            "What optimization path mentions materialized view for filter counts?",
        ],
        13: [
            "Implement naive O(N²) duplicate pair loop and state when to replace it.",
        ],
        16: [
            "pool_size default?",
            "statement_timeout ms value?",
        ],
    }
    parts.append(wrap_topic("Big O", "BO", BO))

    # Git
    GIT = {
        1: [
            "How many commits in repo at portfolio audit?",
            "Default branch name?",
            "Remote URL host?",
            "Are there merge commits?",
            "Are there tags?",
            "Name backup branch purpose.",
            "Most common commit prefix count?",
            "First commit message theme?",
        ],
        2: [
            "Define Conventional Commits as used here.",
            "Define HEAD.",
            "Define amend in context of reflog.",
            "Define linear history.",
        ],
        3: [
            "Why amend before push?",
            "Why backup branch before history rewrite?",
            "Why no merge commits in solo workflow?",
            "Why fix: commits forward instead of revert?",
        ],
        4: [
            "Compare merge vs rebase (what repo actually used).",
            "Compare amend vs new commit for typos.",
            "Compare reset vs revert for published history.",
        ],
        8: [
            "Type command to show last 30 commits oneline.",
            "Type command to show all branches.",
            "Type command to show reflog.",
            "Type command commit distribution by prefix (conceptually).",
        ],
        15: [
            "Professor: How does your commit history show engineering maturity?",
            "Professor: What would team workflow change in your git habits?",
        ],
        16: [
            "Commit hash cited for route shadowing fix?",
            "Branch rename seen in reflog?",
            "Count of feat: commits?",
        ],
    }
    parts.append(wrap_topic("Git", "GT", GIT))

    # SQLAlchemy, Pydantic, DB - compact but multi-level
    SA = {
        1: [
            "SessionLocal autocommit setting?",
            "SessionLocal autoflush setting?",
            "pool_pre_ping purpose?",
            "pool_recycle seconds?",
            "SQLite FK pragma enabled how?",
            "Does get_db auto-commit?",
            "Uses selectinload/joinedload?",
            "Uses relationship()?",
            "Alembic target_metadata source?",
            "Production migration via Procfile or RUN_MIGRATIONS_ON_STARTUP?",
        ],
        2: [
            "Define Unit of Work in SQLAlchemy session.",
            "Define Identity Map.",
            "Define flush vs commit.",
            "Define connection pool overflow.",
        ],
        3: [
            "Why autocommit=False?",
            "Why pool_pre_ping on Supabase?",
            "Why cast JSONB to Text for ilike?",
            "Why NullPool in Alembic env?",
            "Why no relationship() definitions?",
        ],
        6: [
            "Read db.py engine kwargs for Postgres — list five settings.",
            "What happens if route forgets db.commit()?",
        ],
        7: [
            "Complete get_db try/yield/finally/close.",
            "Complete query.filter with json_list_contains pattern.",
            "Write explicit join query for user applications without relationship().",
        ],
        8: [
            "Type alembic upgrade head.",
            "Type CI migration test sequence (upgrade, downgrade, upgrade).",
        ],
        13: [
            "Build engine with pool_pre_ping and pool_size from settings.",
            "Build Alembic env.py target_metadata wiring.",
        ],
        16: [
            "connect_timeout seconds?",
            "max_overflow default?",
            "Revision count?",
        ],
    }
    parts.append(wrap_topic("SQLAlchemy", "SA", SA))

    PYD = {
        1: [
            "Settings base class?",
            "validation_alias purpose?",
            "from_attributes used where?",
            "extra=ignore vs extra=allow examples?",
            "field_validator vs model_validator?",
            "EmailStr used where?",
            "Computed fields used?",
            "StudentProfile age Field constraints?",
        ],
        3: [
            "Why validate at API boundary?",
            "Why model_validator for guardian consent?",
            "Why split StudentProfile vs StudentProfileResponse?",
            "Why validate_for_production on Settings not Field validators?",
        ],
        7: [
            "Complete split_pipe_lists field_validator.",
            "Complete check_age_range model_validator.",
            "Complete Settings Field with validation_alias DATABASE_URL.",
        ],
        13: [
            "Build RegisterRequest with password field_validator min length.",
            "Build validate_for_production checking SECRET_KEY and SQLite URL.",
        ],
    }
    parts.append(wrap_topic("Pydantic", "PD", PYD))

    DB = {
        1: [
            "Name uq_students_user_id.",
            "Name uq_applications_user_scholarship.",
            "Name partial unique staging index.",
            "What ondelete on refresh_tokens.user_id?",
            "What ondelete on scholarships.sponsor_id?",
            "Soft remove column on applications?",
            "Evidence supersession column?",
            "Staging table name?",
            "Version history table?",
            "Audit log table?",
        ],
        3: [
            "Why JSON lists in Text/JSONB vs junction tables?",
            "Why empty eligible list means open?",
            "Why partial unique on staging dedupe_key?",
            "Why RLS enabled but bypassed as table owner?",
        ],
        10: [
            "Reconstruct ER relationships: User-Student-MatchRun-MatchResult-Scholarship.",
        ],
        11: [
            "Draw staging → approve → live catalog flow.",
        ],
        16: [
            "Migration number for RLS?",
            "Migration number for JSONB GIN?",
            "Constraint name on scholarship_versions CASCADE fix?",
        ],
    }
    parts.append(wrap_topic("Database Design", "DB", DB))

    AUTH = {
        1: [
            "JWT library?",
            "Password hash library?",
            "Refresh token stored how at rest?",
            "Refresh plain token generation?",
            "Access denylist Redis key pattern?",
            "Profile share header name?",
            "Roles in RBAC list four.",
            "HTTPBearer auto_error setting?",
        ],
        3: [
            "Why short access token + long refresh?",
            "Why hash refresh but not store access jti in DB only Redis?",
            "Why rotation on refresh?",
            "Why AUTH_DISABLED never in prod?",
        ],
        5: [
            "Walk through decode_token checking jti denylist.",
            "Walk through consume_refresh_token_rotation.",
        ],
        7: [
            "Complete revoke_access_token Redis setex TTL logic.",
            "Complete require_admin HTTPException statuses.",
        ],
        13: [
            "Build full login issuing access JWT + refresh row.",
            "Build refresh rotation endpoint logic.",
        ],
        16: [
            "jti length generation method?",
            "typ field value on access token?",
        ],
    }
    parts.append(wrap_topic("Authentication and JWT", "AU", AUTH))

    SEC = {
        1: [
            "CORS env var?",
            "Security headers middleware sets HSTS?",
            "SQL injection defense mechanism?",
            "CSRF relevance with Bearer JWT?",
            "Non-enumerating forgot password — why?",
            "Email abuse cooldown seconds?",
        ],
        3: [
            "Why CORS allow_credentials with Bearer not cookies?",
            "Why secrets never in Vercel?",
            "Why bcrypt not plaintext?",
        ],
        9: [
            "Production boots with AUTH_DISABLED true — which guard failed?",
            "XSS in scholarship description — mitigations in stack?",
        ],
        14: [
            "Threat model: stolen refresh token — impact and mitigation?",
            "Threat model: no Redis — logout effectiveness?",
        ],
    }
    parts.append(wrap_topic("Security", "SE", SEC))

    HTTP = {
        1: [
            "API base prefix?",
            "Idempotent PUT example route?",
            "Non-idempotent POST match-runs why?",
            "Status code for validation error?",
            "Status code for rate limit?",
            "Header for request ID?",
            "Public search method and path?",
        ],
        4: [
            "Compare GET vs POST for match-runs.",
            "Compare 401 vs 403 in ISKONNECT.",
            "Compare JSON request vs JSON response responsibilities.",
        ],
        8: [
            "Type full URL pattern for local OpenAPI docs.",
        ],
    }
    parts.append(wrap_topic("HTTP, REST, JSON", "HR", HTTP))

    ARCH = {
        1: [
            "How many api/v1 router modules?",
            "Where is MatchService?",
            "Where is scholarship cache?",
            "Where are cron jobs defined vs invoked?",
            "Vercel hosts what layer?",
            "Render hosts what layer?",
        ],
        10: [
            "List every app/ subfolder and responsibility from portfolio.",
            "Trace browser click Run Match to JSON response.",
        ],
        11: [
            "Draw layered architecture: api → matching → db.",
        ],
        13: [
            "Recreate folder tree from empty editor.",
        ],
    }
    parts.append(wrap_topic("Software Architecture", "AR", ARCH))

    PAT = {
        1: [
            "Strategy pattern example?",
            "Adapter pattern example?",
            "Facade pattern example?",
            "Singleton implicit examples?",
            "Repository pattern — formal or partial?",
            "Observer used?",
        ],
        3: [
            "Why Strategy for ScoringEnginePort?",
            "Why Adapter for Supabase storage?",
            "Why Facade for MatchService?",
        ],
        4: [
            "Compare Facade vs God object — why MatchService is former?",
            "Compare Unit of Work vs manual commit per query.",
        ],
    }
    parts.append(wrap_topic("Design Patterns", "PT", PAT))

    PRIN = {
        1: [
            "SOLID letter for Open/Closed example?",
            "DRY example file?",
            "KISS example vs ML?",
            "YAGNI three examples absent features?",
            "Fail fast example function?",
        ],
        3: [
            "Why YAGNI on BackgroundTasks?",
            "Why Fail Fast validate_for_production?",
            "Why defensive cast JSONB for SQLite tests?",
        ],
        15: [
            "Professor: Map one SOLID principle to a specific ISKONNECT module.",
            "Professor: Where did YAGNI prevent over-engineering?",
        ],
    }
    parts.append(wrap_topic("Engineering Principles", "PR", PRIN))

    TEST = {
        1: [
            "Backend test module count?",
            "Pytest case count approx?",
            "conftest db strategy?",
            "dependency_overrides used for?",
            "Eval recall threshold PROD?",
            "Regression file for production incidents?",
            "Contract file for CSV import?",
            "Superset test file for search?",
        ],
        3: [
            "Why StaticPool not transaction rollback?",
            "Why autouse rate limit reset fixture?",
            "Why eval harness separate from unit tests?",
        ],
        8: [
            "Type pytest command from CI.",
            "Type vitest command from frontend package.",
        ],
        9: [
            "test_production_regressions guards which incident list five?",
        ],
        13: [
            "Build conftest api_with_db fixture from memory.",
            "Build one parametrize test for GWA normalization.",
        ],
    }
    parts.append(wrap_topic("Testing", "TE", TEST))

    DEVOPS = {
        1: [
            "Docker base image?",
            "Docker user name?",
            "docker-compose postgres version?",
            "CI python version?",
            "CI postgres version for migrate job?",
            "Frontend node version in CI?",
            "keepalive cron expression?",
            "link-checker cron?",
            "Count GitHub workflows?",
            "Scraper workflow status?",
        ],
        8: [
            "Type docker compose service command for api dev.",
            "Type gunicorn worker class in Procfile.",
            "Type python -m app.jobs.link_checker.",
        ],
        16: [
            "HEALTHCHECK interval in Dockerfile?",
            "Redis key for scholarship cache?",
            "Structured logging env var?",
            "Deprecated deploy file name?",
        ],
    }
    parts.append(wrap_topic("DevOps and Deployment", "DV", DEVOPS))

    DOMAIN = {
        1: [
            "Two-stage matching pipeline stages?",
            "Five scoring components?",
            "QualificationStatus values list four.",
            "Editorial vs is_active distinction?",
            "Deadline passed vs deactivate catalog?",
            "Staging status values?",
            "Explainability fields on match result?",
        ],
        3: [
            "Why eligibility contract?",
            "Why incident to test discipline?",
            "Why empty means open domain rule?",
            "Why cron over BackgroundTasks for link check?",
        ],
        10: [
            "Explain sample-matches public endpoint purpose.",
            "Explain merge-before-delete admin flow.",
        ],
        15: [
            "Professor: Connect explainability to user trust.",
            "Professor: Why staging table for CSV imports?",
        ],
    }
    parts.append(wrap_topic("ISKONNECT Domain (Matching and Catalog)", "DM", DOMAIN))

    parts.append(wrap_topic("Engineering Vocabulary", "VO", glossary_questions()))
    parts.append(wrap_topic("Forgotten Details", "FD", env_var_questions()))
    parts.append(wrap_topic("Migrations Deep Dive", "MG", migration_questions()))

    FE = {
        1: [
            "Frontend test runner?",
            "VITE_API_BASE_URL required when?",
            "Fetch timeout ms for Render cold start?",
            "PWA plugin name?",
            "Vitest environment?",
        ],
        3: [
            "Why 70s fetch timeout?",
            "Why VITE_ prefix?",
        ],
        16: [
            "localStorage keys for auth tokens?",
            "Dev server port in vite config?",
        ],
    }
    parts.append(wrap_topic("Frontend Appendix", "FE", FE))

    parts.append(code_reading_supplement())
    parts.append(debugging_supplement())
    parts.append(interview_supplement())
    parts.append(professor_supplement())

    parts.append(generate_from_headings(headings))

    footer = f"\n\n---\n\n## Generation Metadata\n\n- Total questions: **{_qid}**\n"
    footer += "- Source: ENGINEERING_KNOWLEDGE_PORTFOLIO.md\n"
    footer += "- Answers: **intentionally omitted**\n"

    OUTPUT.write_text("".join(parts) + footer, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {_qid} questions")


if __name__ == "__main__":
    main()
