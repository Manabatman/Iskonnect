# Iskonnect Learning Guide

> **Want a day-by-day study plan?** Start with [`docs/ACTIVE_LEARNING_PATH.md`](docs/ACTIVE_LEARNING_PATH.md) — retrieval practice, traces, and checkpoints. Use this guide as reference while you work through that path.

This document is a beginner-friendly reverse engineering guide for the `scholarship-match` project.

It does four jobs at once:

1. It explains what the whole system is and how it works.
2. It breaks down the important folders and files.
3. It teaches the concepts you need in order to understand the code.
4. It shows you where the current bugs, gaps, and risks are.

Important note:

- Your IDE tab points to `frontend/src/components/ProfileForm.tsx`, but that file does not exist in the current codebase. The profile form was replaced by `frontend/src/pages/ProfileBuilderPage.tsx` plus the files in `frontend/src/components/profile-builder/`.
- I reviewed the hand-written project files in the repo. I do not give a line-by-line breakdown of generated or vendor directories such as `frontend/node_modules`, `frontend/dist`, `.venv`, `venv`, `.git`, `__pycache__`, or `.pytest_cache`, because those are dependency/build folders rather than the project's own logic.

## 1. High-Level Architecture

### Simple idea first

Think of this project like a scholarship recommendation office with four parts:

- The frontend is the receptionist desk. It shows screens, forms, buttons, and results.
- The backend is the staff office. It receives requests, decides what to do, and applies the matching rules.
- The database is the filing cabinet. It stores students, scholarships, match history, saved items, reports, and admin data.
- The matching engine is the evaluator. It checks whether a student qualifies and ranks the scholarships that pass.

So the basic flow is:

`User -> React frontend -> FastAPI backend -> SQLAlchemy -> SQLite/PostgreSQL database`

### Technical view

This is a full-stack web application with:

- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI + Pydantic + SQLAlchemy
- Database: SQLite in local development, PostgreSQL-compatible deployment setup
- Matching domain logic: custom hard filters + weighted scoring engine
- Auth: JWT bearer token authentication
- Schema evolution: Alembic migrations

### Main user journeys

#### Flow A: Create or update a student profile

Simple version:

1. A user fills out the profile builder.
2. The frontend stores temporary form progress.
3. On save, the frontend sends the profile to the backend.
4. The backend validates the data and stores it in the database.

Technical version:

1. `ProfileBuilderPage.tsx` collects multi-step form state through a reducer in `profileBuilderState.ts`.
2. Draft state is kept in browser storage via `profileDraft.ts`.
3. On submit, `studentProfilePayload.ts` converts frontend form state into the backend payload shape.
4. The frontend calls `POST /api/v1/profiles`.
5. `app/api/v1/profiles.py` validates ownership and either creates or updates a `Student` row.
6. The row is stored through SQLAlchemy in the `students` table.

#### Flow B: Run scholarship matching

Simple version:

1. A user clicks to generate matches.
2. The backend loads the student's profile.
3. It removes scholarships that are clearly impossible.
4. It scores the remaining scholarships.
5. It saves the run and returns ranked results.

Technical version:

1. The frontend calls `POST /api/v1/match-runs`.
2. `app/api/v1/match_history.py` loads the user's profile and hands it to the matching service.
3. `app/matching/match_service.py` orchestrates filtering, scoring, explanations, and persistence.
4. `app/matching/hard_filters.py` removes ineligible scholarships.
5. `app/scoring/engine.py` and `app/scoring/components.py` compute a deterministic weighted score.
6. `app/scoring/explanation.py` builds the score breakdown, confidence, and suggestions.
7. `MatchRun` and `MatchResult` rows are written to the database.
8. The frontend later fetches the run and shows it in `MatchResultsPage.tsx`.

#### Flow C: Search for scholarships

Simple version:

1. The user types filters.
2. The frontend sends them to the backend.
3. The backend builds a database query and returns matching scholarships.

Technical version:

1. `ScholarshipSearchPage.tsx` and `ScholarshipSearchFilters.tsx` gather filters.
2. They call `GET /api/v1/scholarships/search` and `GET /api/v1/scholarships/search/filters`.
3. `app/api/v1/scholarship_search.py` builds SQLAlchemy query filters.
4. Matching scholarship rows are serialized into JSON and returned to the frontend.

#### Flow D: Save a scholarship

Simple version:

1. The user clicks the bookmark icon.
2. The frontend remembers that it is saving or unsaving.
3. The backend creates or deletes a saved record.

Technical version:

1. `BookmarkButton.tsx` talks to `SavedScholarshipsContext.tsx`.
2. That context calls `POST /api/v1/saved-scholarships` or `DELETE /api/v1/saved-scholarships/{id}`.
3. `app/api/v1/saved_scholarships.py` reads the token owner and writes to `saved_scholarships`.

## 2. Project Structure

### Top-level folders

- `app/`: The backend application.
- `frontend/`: The React web client.
- `alembic/`: Database migration scripts.
- `docs/`: Supporting documentation.

### Top-level idea

If you are new, remember this:

- `frontend/` decides what the user sees.
- `app/api/` decides what HTTP endpoints exist.
- `app/matching/` and `app/scoring/` decide how recommendations work.
- `app/models.py` decides what is stored in the database.
- `app/schemas.py` decides what shape data must have when moving through the API.

## 3. Folder and File Breakdown

This section focuses on the hand-written project files.

### Root files

- `README.md`: The main project introduction and quick-start instructions. It explains the goal of the app and the main stack. It is read by humans, not executed by the app.
- `requirements.txt`: Python backend dependencies. It is used when you install the backend packages.
- `.env.example`: Example environment variables. You copy this to `.env` when setting up the project.
- `.env`: Local environment configuration. It is read by the backend settings loader at startup.
- `alembic.ini`: Configuration file for Alembic migrations. Used when running `alembic upgrade head`.
- `start.py`: Small backend launcher. Used when you run `python start.py`.
- `start-backend.bat`: Windows helper script that creates a virtual environment, installs packages, seeds data, frees port 8000, and starts FastAPI.
- `seed_data.py`: Inserts sample scholarship records into the database. Used during local setup and demo data refresh.
- `free_port.py`: Utility script that frees a Windows port before starting a server. Called by the batch scripts.
- `SCORING_ENGINE.md`: Human documentation for the matching/scoring model. Useful for learning, but parts of it are currently outdated.
- `ENGINEERING_HANDBOOK.md`: Human engineering notes for working on the project.
- `PRODUCTION_AUDIT.md`: Human review notes about production-readiness concerns.
- `render.yaml`: Deployment configuration for Render.
- `railway.json`: Deployment configuration for Railway.
- `Procfile`: Process startup definition for some platforms.
- `runtime.txt`: Python runtime version for deployment services.
- `dev.db`: Local SQLite database file. This is data storage, not source code.

### `app/` backend package

#### Core backend files

- `app/__init__.py`: Package marker for Python imports. It has no major runtime logic.
- `app/main.py`: The backend entry point. It creates the FastAPI app, applies middleware, includes routers, optionally runs migrations, and exposes `/health` and `/ready`. It runs when the backend server starts.
- `app/config.py`: Centralized settings loader. It reads environment variables like database URL, auth flags, rate limits, and feature toggles. It is imported by many backend files during startup and request handling.
- `app/db.py`: Database setup file. It creates the SQLAlchemy engine, session factory, base class, and `get_db()` dependency. It is used whenever the backend talks to the database.
- `app/models.py`: Database model definitions. It declares the tables and columns used by the app. It is used by routes, services, and migrations.
- `app/schemas.py`: Pydantic request and response schemas. It validates API inputs and outputs.
- `app/auth.py`: Auth and authorization helpers. It hashes passwords, creates JWTs, validates tokens, and enforces admin/profile ownership rules.
- `app/limiter.py`: Rate-limiter setup. It is used by selected API endpoints to slow down abuse.
- `app/scholarship_cache.py`: Scholarship list cache abstraction. It uses Redis if configured, otherwise an in-process cache. It speeds up repeated scholarship reads.

#### `app/api/`

- `app/api/__init__.py`: Package marker.
- `app/api/v1/__init__.py`: Package marker.

#### `app/api/v1/` route files

- `app/api/v1/auth_routes.py`: Register, login, and current-user endpoints. Called when the frontend signs users in or verifies a session.
- `app/api/v1/profiles.py`: Student profile create/read/list/delete routes. Called by the dashboard and profile builder.
- `app/api/v1/matches.py`: Direct match endpoint for a profile. Used for ranked results without full run history.
- `app/api/v1/match_history.py`: Match run creation, listing, detail, and comparison endpoints. Called by the dashboard, match results page, and compare page.
- `app/api/v1/scholarships.py`: Scholarship CRUD routes. Used by admin and scholarship detail flows.
- `app/api/v1/scholarship_search.py`: Scholarship search endpoint plus dynamic search-filter metadata endpoint. Used by search pages and the dashboard search box.
- `app/api/v1/suggestions.py`: Autocomplete and suggestion endpoints for schools, courses, regions, provinces, and scholarship names. Used by smart inputs in the frontend.
- `app/api/v1/saved_scholarships.py`: Save, unsave, list, and ID lookup endpoints for bookmarked scholarships.
- `app/api/v1/reports.py`: User report submission and admin moderation routes for incorrect scholarship data.
- `app/api/v1/analytics.py`: Admin analytics overview endpoint. Used by the admin analytics page.
- `app/api/v1/audit_routes.py`: Audit log endpoint for admins.
- `app/api/v1/scoring_admin.py`: Admin endpoints for viewing and editing scoring weights.
- `app/api/v1/scoring.py`: Legacy compatibility export around old scoring code. It is not a main router file.
- `app/api/v1/notifications.py`: Notification list, unread count, and mark-as-read routes.
- `app/api/v1/scholarship_staging.py`: Import-review workflow for staging scholarships before approval into the main list.

#### `app/matching/`

- `app/matching/__init__.py`: Package marker.
- `app/matching/hard_filters.py`: The strict eligibility gatekeeper. It removes scholarships that clearly do not fit the student before scoring happens. This is called during matching.
- `app/matching/match_service.py`: The main match orchestration service. It loads scholarships, runs hard filters, calls scoring, builds explanations, and optionally saves results.
- `app/matching/profile_completeness.py`: Computes how complete a student profile is. Useful for UX hints and readiness guidance.
- `app/matching/scoring_port.py`: Interface contract for scoring engines. It defines the input and output structure a scorer must follow.
- `app/matching/legacy_scorer.py`: Old rule-based scoring adapter kept for backward compatibility experiments.
- `app/matching/rules.py`: Older direct rule-scoring logic. Useful for understanding the project's scoring history, but not the main current path.

#### `app/scoring/`

- `app/scoring/__init__.py`: Package marker.
- `app/scoring/config.py`: Current scoring weights and configuration. This is where the weighted model is defined.
- `app/scoring/components.py`: Pure scoring functions for academic, income, field, geographic, and equity scoring pieces.
- `app/scoring/engine.py`: The current deterministic weighted scorer implementation.
- `app/scoring/explanation.py`: Builds the explanation text, component breakdown, confidence level, and suggestions shown to the user.

#### `app/documents/`

- `app/documents/__init__.py`: Package marker.
- `app/documents/readiness.py`: Compares required scholarship documents with the student's available documents. It calculates document readiness, even though readiness is no longer part of the main weighted score.

#### `app/prediction/`

- `app/prediction/__init__.py`: Package marker.
- `app/prediction/cycle_predictor.py`: Predicts likely reopening windows for scholarships that are currently closed or cyclical.

#### `app/middleware/`

- `app/middleware/__init__.py`: Package marker.
- `app/middleware/request_logger.py`: Request/response logging helpers. Used for observability.

#### `app/utils/`

- `app/utils/__init__.py`: Package marker.
- `app/utils/json_helpers.py`: Helper functions for safely reading and normalizing JSON-like text fields.
- `app/utils/sanitize.py`: Input cleaning and defensive formatting helpers.
- `app/utils/fuzzy_search.py`: Utility logic for fuzzy or approximate matching.
- `app/utils/logging_config.py`: Logging configuration helpers.
- `app/utils/audit.py`: Audit log creation helper used by admin/system events.
- `app/utils/notification_helpers.py`: Notification creation and related helper logic.
- `app/utils/scholarship_versioning.py`: Keeps version history for scholarship records after important changes.

#### `app/taxonomy/`

- `app/taxonomy/__init__.py`: Package marker.
- `app/taxonomy/psced_fields.py`: Education field mappings based on Philippine Standard Classification of Education concepts.
- `app/taxonomy/gwa_normalizer.py`: Helpers for normalizing grade formats into comparable values.
- `app/taxonomy/regions.py`: Region constants and normalization rules.
- `app/taxonomy/provinces.py`: Province constants used by forms and filters.
- `app/taxonomy/schools.py`: School suggestion/reference data.
- `app/taxonomy/income_brackets.py`: Income bracket reference definitions.
- `app/taxonomy/equity_groups.py`: Priority and equity-group definitions used in matching logic.

#### `app/jobs/`

- `app/jobs/__init__.py`: Package marker.
- `app/jobs/freshness_checker.py`: Background-style job that marks scholarships expired or stale for review.
- `app/jobs/link_checker.py`: Background-style job that checks scholarship URLs for broken links.
- `app/jobs/retention_cleanup.py`: Background-style scan that flags inactive user accounts for review through the audit system.

#### `app/scripts/`

- `app/scripts/__init__.py`: Package marker.
- `app/scripts/import_scholarships.py`: Script for importing scholarship data.
- `app/scripts/csv_to_staging.py`: Loads CSV scholarship data into the staging table for review.
- `app/scripts/create_admin.py`: Creates or upgrades an admin account from the command line.

#### `app/tests/`

- `app/tests/__init__.py`: Package marker.
- `app/tests/conftest.py`: Shared test fixtures and setup.
- `app/tests/test_matching.py`: Core matching behavior tests.
- `app/tests/test_matching_regression.py`: Regression tests for past matching bugs, including region matching edge cases.
- `app/tests/test_match_service_integration.py`: Higher-level tests for the match service.
- `app/tests/test_scoring_engine.py`: Unit tests for the scoring engine.
- `app/tests/test_profile_completeness.py`: Tests for profile completeness calculations.
- `app/tests/test_notification_helpers.py`: Tests for notification helper behavior.
- `app/tests/test_cycle_predictor.py`: Tests for reopening-cycle prediction.

### `frontend/`

#### Frontend config and tooling

- `frontend/package.json`: Frontend dependencies and scripts like `dev`, `build`, `preview`, and `lint`.
- `frontend/package-lock.json`: Exact npm dependency lockfile. It is generated but important for reproducible installs.
- `frontend/tsconfig.json`: TypeScript compiler configuration.
- `frontend/vite.config.ts`: Vite build/dev server configuration.
- `frontend/tailwind.config.js`: Tailwind CSS configuration.
- `frontend/postcss.config.js`: PostCSS configuration used by Tailwind.
- `frontend/index.html`: The HTML shell Vite serves before React mounts.
- `frontend/start-frontend.bat`: Windows helper script that installs frontend packages, frees port 5173, and starts the Vite dev server.

#### `frontend/public/`

- `frontend/public/logo_Iskonnect.png`: Logo asset for branding.
- `frontend/public/images/README.txt`: Notes about image assets.
- `frontend/public/images/logo.svg`: SVG logo asset.
- `frontend/public/images/hero/hero-1.svg`: Landing-page illustration asset.
- `frontend/public/images/hero/hero-2.svg`: Landing-page illustration asset.
- `frontend/public/images/hero/hero-3.svg`: Landing-page illustration asset.

#### Frontend entry files

- `frontend/src/main.tsx`: React entry point. It mounts the app and initializes optional Sentry monitoring.
- `frontend/src/App.tsx`: Main route tree. It connects public pages, protected dashboard pages, and providers.
- `frontend/src/index.css`: Global CSS and Tailwind layers.
- `frontend/src/types.ts`: Shared TypeScript types for scholarships, profiles, and related frontend data shapes.

#### `frontend/src/api/`

- `frontend/src/api/client.ts`: Common fetch wrapper. It adds the API base URL, timeout handling, retry behavior, and error logging.

#### `frontend/src/contexts/`

- `frontend/src/contexts/AuthContext.tsx`: Holds the auth token, current user, login/register/logout functions, and auth headers for API calls.
- `frontend/src/contexts/SavedScholarshipsContext.tsx`: Global saved-scholarship state. It loads saved IDs and handles optimistic save/unsave behavior.
- `frontend/src/contexts/ThemeContext.tsx`: Global light/dark/system theme state.

#### `frontend/src/hooks/`

- `frontend/src/hooks/useDebounce.ts`: Delays reacting to rapidly changing values like search text.

#### `frontend/src/utils/`

- `frontend/src/utils/profileDraft.ts`: Saves and restores in-progress profile builder drafts from browser storage.
- `frontend/src/utils/studentProfilePayload.ts`: Converts the profile builder state into the exact backend payload shape.
- `frontend/src/utils/formatDate.ts`: Small date formatting helper.

#### `frontend/src/constants/`

- `frontend/src/constants/profileOptions.ts`: Shared profile option lists used by the form.
- `frontend/src/constants/regions.ts`: Region list/constants used in the frontend.
- `frontend/src/constants/needsCategories.ts`: Categories used for need/preference-style UI.
- `frontend/src/constants/heroImages.ts`: Hero asset references for the landing page.

#### `frontend/src/data/`

- `frontend/src/data/changelog.ts`: Data source for the changelog page.
- `frontend/src/data/mockOpportunities.ts`: Fallback demo opportunity data when API data is unavailable.
- `frontend/src/data/scholarshipToOpportunity.ts`: Adapter that converts scholarship API data into the UI shape used by the opportunity browser.

#### `frontend/src/components/`

- `frontend/src/components/ErrorBoundary.tsx`: Catches React rendering errors and prevents the whole UI from crashing.
- `frontend/src/components/Navbar.tsx`: Main public-site navigation bar.
- `frontend/src/components/Footer.tsx`: Footer for public pages.
- `frontend/src/components/HeroCarousel.tsx`: Landing-page hero carousel.
- `frontend/src/components/SocialProofTicker.tsx`: Small trust/activity banner component.
- `frontend/src/components/AutocompleteInput.tsx`: Reusable text input with suggestions/autocomplete.
- `frontend/src/components/SelectedChips.tsx`: Displays selected items as removable chips.
- `frontend/src/components/NeedsCategoryAccordion.tsx`: Accordion UI for need-related categories.
- `frontend/src/components/BookmarkButton.tsx`: Save/unsave scholarship button.
- `frontend/src/components/MatchScoreRing.tsx`: Circular score display for match percentages.
- `frontend/src/components/ScholarshipCard.tsx`: Card UI for a matched scholarship.
- `frontend/src/components/UpcomingScholarshipCard.tsx`: Card UI for predicted upcoming scholarships.
- `frontend/src/components/ScholarshipList.tsx`: List rendering for scholarship collections.
- `frontend/src/components/ScholarshipDetailPanel.tsx`: Right-side detail panel in the scholarship search experience.
- `frontend/src/components/ScholarshipSearchFilters.tsx`: Search filter UI for the scholarship search page.
- `frontend/src/components/OpportunityCard.tsx`: Card UI in the opportunities browser.
- `frontend/src/components/OpportunityDetail.tsx`: Expanded detail view for an opportunity.
- `frontend/src/components/OpportunityList.tsx`: List wrapper for opportunity cards.

#### `frontend/src/components/layout/`

- `frontend/src/components/layout/PublicLayout.tsx`: Layout wrapper for public pages.
- `frontend/src/components/layout/SplitLayout.tsx`: Two-column auth page layout.
- `frontend/src/components/layout/DashboardLayout.tsx`: Main signed-in application shell.
- `frontend/src/components/layout/DashboardSidebar.tsx`: Left navigation for dashboard routes.
- `frontend/src/components/layout/DashboardTopbar.tsx`: Top search, quick actions, and page title area for dashboard routes.

#### `frontend/src/components/profile-builder/`

- `frontend/src/components/profile-builder/profileBuilderState.ts`: Reducer, actions, and initial state for the multi-step profile builder.
- `frontend/src/components/profile-builder/profileBuilderConstants.ts`: Step definitions and shared labels/constants for the builder.
- `frontend/src/components/profile-builder/StepperSidebar.tsx`: Sidebar that shows the current step and progress.
- `frontend/src/components/profile-builder/PersonalInfoStep.tsx`: Personal-information step of the profile builder.
- `frontend/src/components/profile-builder/EducationStep.tsx`: Education step of the profile builder.
- `frontend/src/components/profile-builder/LocationBackgroundStep.tsx`: Location and socioeconomic background step.
- `frontend/src/components/profile-builder/FieldOfStudyStep.tsx`: Course and field-of-study step.
- `frontend/src/components/profile-builder/EligibilityGoalsStep.tsx`: Final preference and goals step.

#### `frontend/src/pages/`

- `frontend/src/pages/LandingPage.tsx`: Public homepage.
- `frontend/src/pages/LoginPage.tsx`: Login form page.
- `frontend/src/pages/RegisterPage.tsx`: Registration form page.
- `frontend/src/pages/AboutPage.tsx`: Public about page.
- `frontend/src/pages/HowItWorksPage.tsx`: Public explanation of the product workflow.
- `frontend/src/pages/TransparencyPage.tsx`: Public transparency page about how matching works.
- `frontend/src/pages/SuccessStoriesPage.tsx`: Public social-proof page with illustrative placeholder stories.
- `frontend/src/pages/TermsPage.tsx`: Public terms page.
- `frontend/src/pages/PrivacyPage.tsx`: Public privacy page.
- `frontend/src/pages/ChangelogPage.tsx`: Public release notes page.
- `frontend/src/pages/ScholarshipSearchPage.tsx`: Search-focused scholarship browser with filters and detail panel.
- `frontend/src/pages/ScholarshipDetailPage.tsx`: Full scholarship detail page with reporting flow.
- `frontend/src/pages/ProfileBuilderPage.tsx`: Main student profile creation/editing experience.
- `frontend/src/pages/ProfileDashboard.tsx`: Main signed-in home page showing profile summary, match history, reminders, and actions.
- `frontend/src/pages/MatchResultsPage.tsx`: Ranked scholarship results page for a specific profile/run.
- `frontend/src/pages/MatchComparisonPage.tsx`: Compares multiple match runs.
- `frontend/src/pages/OpportunityBrowserPage.tsx`: Alternative discovery-style browser built around opportunity cards.
- `frontend/src/pages/ApplicationsPage.tsx`: Tracks application statuses in local browser storage.
- `frontend/src/pages/DocumentsPage.tsx`: Placeholder page for future document management.
- `frontend/src/pages/SettingsPage.tsx`: Settings and preferences page.
- `frontend/src/pages/AdminPage.tsx`: Admin scholarship management page.
- `frontend/src/pages/AdminAnalyticsPage.tsx`: Admin analytics dashboard page.
- `frontend/src/pages/NotFoundPage.tsx`: Fallback 404 page.

### `alembic/`

- `alembic/env.py`: Alembic environment configuration that tells Alembic how to connect to the app models.
- `alembic/script.py.mako`: Template used when creating new migrations.

### `alembic/versions/`

- `001_initial_schema.py`: Creates the initial schema.
- `002_add_users_and_profile_ownership.py`: Adds users and profile ownership support.
- `003_add_preferred_courses.py`: Adds preferred course storage.
- `004_add_scholarship_source.py`: Adds source-related scholarship fields.
- `005_add_user_role.py`: Adds user role support such as admin.
- `006_add_match_history.py`: Adds match run history tables.
- `007_add_saved_scholarships.py`: Adds the saved scholarship table.
- `008_add_cycle_prediction_fields.py`: Adds fields for cycle prediction.
- `009_privacy_and_staging.py`: Adds privacy/staging related fields and tables.
- `010_add_data_freshness_and_link_integrity.py`: Adds freshness/link-health tracking.
- `011_add_reports_weights_versions_audit_notifications.py`: Adds reports, scoring weights, versioning, audit logs, and notifications.

### `docs/`

- `docs/DEPLOYMENT.md`: Deployment instructions for hosted environments.
- `docs/TEACHING.md`: Existing internal teaching notes for understanding the frontend and routing.

## 4. Frontend Deep Dive

### Simple idea first

The frontend is a React single-page application.

That means:

- The browser loads one main app.
- React changes the visible screen without fully reloading the page.
- Components are reusable UI building blocks.
- State is the data the UI is currently holding in memory.

If you click a button, React changes state, fetches data, and re-renders the necessary parts of the page.

### Framework and rendering

- Framework: React 18
- Build tool: Vite
- Language: TypeScript
- Router: `react-router-dom`
- Rendering mode: client-side rendering in the browser

How rendering works here:

1. `main.tsx` mounts React into `index.html`.
2. `App.tsx` defines the route tree.
3. React Router chooses which page component to render based on the current URL.
4. Layout components wrap those pages.
5. The page renders smaller components below it.

### Routing system

Public routes:

- `/`
- `/login`
- `/register`
- `/how-it-works`
- `/transparency`
- `/success-stories`
- `/about`
- `/terms`
- `/privacy`
- `/changelog`
- `/scholarships/search`

Dashboard routes:

- `/dashboard`
- `/match/:profileId`
- `/match-compare`
- `/scholarship/:id`
- `/opportunities`
- `/scholarships`
- `/profile-builder`
- `/settings`
- `/admin`
- `/admin/analytics`
- `/applications`
- `/documents`

### Components

Think of components like Lego pieces:

- Pages are large Lego boards.
- Components are smaller reusable pieces placed on those boards.

Examples:

- `ProfileDashboard.tsx` is a large page component.
- `ScholarshipCard.tsx` is a reusable result card.
- `MatchScoreRing.tsx` is a small visual component.
- `DashboardLayout.tsx` is the frame around multiple dashboard pages.

### State management

This project does not use Redux, Zustand, or another external state library.

It mainly uses:

- `useState`: for local screen data
- `useEffect`: for running side effects like API calls
- `useReducer`: for more structured multi-step form state in the profile builder
- props: for passing data from parent components to child components
- React Context: for global app-wide data like auth, theme, and saved scholarships

Where to look:

- Local page state: most page files
- Global auth state: `AuthContext.tsx`
- Global bookmark state: `SavedScholarshipsContext.tsx`
- Global theme state: `ThemeContext.tsx`
- Complex form state: `profileBuilderState.ts`

### UI libraries

This project does not currently use:

- shadcn/ui
- `lucide-react`
- `@heroicons/react`

Instead it uses:

- Tailwind CSS utility classes
- custom React components
- inline SVGs and static image assets

### Styling system

- Main styling approach: Tailwind CSS
- Global styles: `src/index.css`
- Theme support: light, dark, system via `ThemeContext.tsx`

How Tailwind works in simple terms:

- You style elements by adding class names directly in JSX, like `px-4`, `rounded-xl`, `text-slate-900`.
- Instead of writing lots of separate CSS files, most styling lives close to the component.

### How the frontend talks to the backend

The fetch wrapper is `frontend/src/api/client.ts`.

It:

- builds the base URL
- sets a timeout
- retries once for network-style failures
- logs non-OK API responses to the console

Pages and contexts use `apiFetch()` and often attach `Authorization: Bearer <token>` through `AuthContext.tsx`.

### Frontend areas that matter most for learning

If you want to understand the frontend in the best order, read these files first:

1. `frontend/src/main.tsx`
2. `frontend/src/App.tsx`
3. `frontend/src/contexts/AuthContext.tsx`
4. `frontend/src/pages/ProfileDashboard.tsx`
5. `frontend/src/pages/ProfileBuilderPage.tsx`
6. `frontend/src/api/client.ts`
7. `frontend/src/components/profile-builder/profileBuilderState.ts`

## 5. Backend and API Deep Dive

### Simple idea first

The backend is a FastAPI application.

FastAPI is the part that says:

- "If a request comes to this URL, call this Python function."
- "Make sure the input data is shaped correctly."
- "Read or write the database."
- "Return JSON back to the frontend."

### Request lifecycle in this project

1. Browser sends an HTTP request.
2. `app/main.py` receives it through FastAPI.
3. Middleware can log the request or apply rate limits.
4. The matching route file handles the request.
5. Pydantic schemas validate the input.
6. SQLAlchemy reads or writes the database.
7. Business logic services compute results if needed.
8. FastAPI returns JSON to the frontend.

### Backend framework choices

- Web framework: FastAPI
- Validation: Pydantic
- ORM/database layer: SQLAlchemy
- Auth: JWT bearer tokens
- Migrations: Alembic

### Endpoint catalog

#### Authentication

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| POST | `/api/v1/auth/register` | Creates a new user and returns a token | email, password | JWT token, user id, role |
| POST | `/api/v1/auth/login` | Authenticates an existing user | email, password | JWT token, user id, role |
| GET | `/api/v1/auth/me` | Returns the currently logged-in user | bearer token | id, email, role |

Frontend callers:

- `LoginPage.tsx`
- `RegisterPage.tsx`
- `AuthContext.tsx`

#### Profiles

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/profiles` | Lists the current user's profiles | bearer token | array of profile objects |
| POST | `/api/v1/profiles` | Creates or updates a profile | profile payload | saved profile |
| GET | `/api/v1/profiles/{profile_id}` | Gets a single profile | profile id | profile object |
| DELETE | `/api/v1/profiles/me` | Deletes all profiles owned by current user | bearer token | confirmation |

Frontend callers:

- `ProfileBuilderPage.tsx`
- `ProfileDashboard.tsx`

#### Matching and history

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/matches/{profile_id}` | Returns computed matches for one profile | profile id | ranked scholarship matches |
| POST | `/api/v1/match-runs` | Creates and stores a match run | profile id and options | run metadata + results |
| GET | `/api/v1/match-runs` | Lists past match runs | auth/profile context | run summaries |
| GET | `/api/v1/match-runs/{run_id}` | Returns one saved run | run id | full run detail |
| GET | `/api/v1/match-runs/compare` | Compares multiple run ids | query params | comparison payload |

Frontend callers:

- `ProfileDashboard.tsx`
- `MatchResultsPage.tsx`
- `MatchComparisonPage.tsx`

Business logic location:

- `app/matching/match_service.py`
- `app/matching/hard_filters.py`
- `app/scoring/*`

#### Scholarships and search

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/scholarships` | Lists scholarships | query params | scholarship list |
| POST | `/api/v1/scholarships` | Creates a scholarship | scholarship payload | created scholarship |
| GET | `/api/v1/scholarships/{id}` | Gets one scholarship | scholarship id | scholarship detail |
| PUT | `/api/v1/scholarships/{id}` | Updates one scholarship | scholarship payload | updated scholarship |
| DELETE | `/api/v1/scholarships/{id}` | Soft-deactivates a scholarship | scholarship id | confirmation |
| GET | `/api/v1/scholarships/search/filters` | Returns dynamic search filter options | none | filter metadata |
| GET | `/api/v1/scholarships/search` | Searches scholarships | query params | filtered list |

Frontend callers:

- `ScholarshipSearchPage.tsx`
- `ScholarshipDetailPage.tsx`
- `DashboardTopbar.tsx`
- `AdminPage.tsx`
- `OpportunityBrowserPage.tsx`

#### Suggestions

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/suggestions/schools` | Suggests school names | query text | array of school names |
| GET | `/api/v1/suggestions/courses` | Suggests course names | query text | array of course names |
| GET | `/api/v1/suggestions/regions` | Suggests region names | query text | array of regions |
| GET | `/api/v1/suggestions/provinces` | Suggests province names | query text | array of provinces |
| GET | `/api/v1/suggestions/scholarships` | Suggests scholarship names | query text | array of scholarship titles |

Frontend callers:

- `AutocompleteInput.tsx`
- profile builder inputs
- scholarship search inputs

#### Saved scholarships

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/saved-scholarships/ids` | Returns only saved scholarship ids | bearer token | id array |
| POST | `/api/v1/saved-scholarships` | Saves a scholarship | scholarship id | saved record |
| GET | `/api/v1/saved-scholarships` | Lists saved scholarships | bearer token | saved scholarship list |
| DELETE | `/api/v1/saved-scholarships/{scholarship_id}` | Unsaves a scholarship | scholarship id | confirmation |

Frontend callers:

- `SavedScholarshipsContext.tsx`
- `BookmarkButton.tsx`
- dashboard saved sections

#### Reports

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| POST | `/api/v1/reports` | Submits a scholarship issue report | scholarship id, message, category | created report |
| GET | `/api/v1/reports/pending` | Lists unresolved reports for admins | admin token | report list |
| POST | `/api/v1/reports/{report_id}/resolve` | Marks a report resolved | report id | updated report |
| POST | `/api/v1/reports/{report_id}/dismiss` | Dismisses a report | report id | updated report |

Frontend callers:

- `ScholarshipDetailPage.tsx`
- admin moderation flows

#### Notifications

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/notifications` | Lists notifications for the current user | bearer token | notification list |
| GET | `/api/v1/notifications/unread-count` | Counts unread notifications | bearer token | count |
| POST | `/api/v1/notifications/{notification_id}/read` | Marks one notification read | notification id | updated notification |

#### Admin and analytics

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/admin/analytics/overview` | Returns admin dashboard stats | admin token | analytics summary |
| GET | `/api/v1/admin/audit/logs` | Returns audit logs | admin token | audit entries |
| GET | `/api/v1/admin/scoring/weights` | Returns active scoring weights | admin token | weight list |
| PUT | `/api/v1/admin/scoring/weights` | Updates scoring weights | weight payload | saved weights |

Frontend callers:

- `AdminAnalyticsPage.tsx`

#### Staging workflow

| Method | Endpoint | What it does | Input | Output |
|---|---|---|---|---|
| GET | `/api/v1/scholarships/staging/pending` | Lists staged scholarships awaiting review | admin token | staging list |
| POST | `/api/v1/scholarships/staging/import` | Imports staged scholarship data | import payload | summary |
| POST | `/api/v1/scholarships/staging/{id}/approve` | Approves staged record into main table | staging id | created/updated scholarship |
| POST | `/api/v1/scholarships/staging/{id}/reject` | Rejects staged record | staging id | updated staging record |

### Where the business logic lives

Business logic is the "actual rules of the app," not just HTTP plumbing.

In this project the most important business logic lives in:

- `app/matching/hard_filters.py`
- `app/matching/match_service.py`
- `app/scoring/components.py`
- `app/scoring/engine.py`
- `app/scoring/explanation.py`
- `app/documents/readiness.py`
- `app/prediction/cycle_predictor.py`

## 6. Database Layer

### Simple idea first

A database table is like a spreadsheet:

- A table is one spreadsheet.
- A row is one record.
- A column is one property.

Example:

- `students` is the spreadsheet of student profiles.
- Each student row stores details like name, education level, region, income, and preferences.

### Database type

- Local development: SQLite (`dev.db`)
- Deployable setup: SQL database through `DATABASE_URL`, commonly PostgreSQL on hosted environments

### Major tables

#### `users`

Purpose:

- Stores login accounts.

Important fields:

- `id`
- `email`
- `password_hash`
- `role`
- timestamps

Used when:

- registering
- logging in
- checking admin access

#### `students`

Purpose:

- Stores the main student profile used for matching.

Important fields include:

- identity info
- email
- age
- region/province/city
- education level
- school type
- course/field info
- GWA / academic metrics
- household income
- equity and priority flags
- available documents
- preferred courses
- ownership via `user_id`

Used when:

- saving a profile
- loading the dashboard
- generating matches

#### `scholarships`

Purpose:

- Stores active scholarship opportunities.

Important fields include:

- title
- provider
- description
- eligibility rules
- eligible regions
- education levels
- min GWA
- max income threshold
- required documents
- application deadline
- link/source metadata
- data quality fields like `data_status`, `last_verified_at`, and link-health fields

Used when:

- searching scholarships
- showing details
- generating matches
- admin editing

#### `scholarships_staging`

Purpose:

- Temporary holding area for imported scholarship data that needs review before going live.

#### `match_runs`

Purpose:

- Stores one execution of the matching engine for a user/profile.

Used when:

- showing match history
- comparing runs

#### `match_results`

Purpose:

- Stores the per-scholarship results for a match run, including score and explanations.

#### `saved_scholarships`

Purpose:

- Many-to-many style link between users and scholarships they bookmarked.

#### `scholarship_reports`

Purpose:

- User-submitted reports about bad data, broken links, or inaccurate scholarship details.

#### `scoring_weights`

Purpose:

- Stores configurable weights for score components so admins can tune the ranking behavior.

#### `scholarship_versions`

Purpose:

- Keeps historical versions of scholarship data for auditing or rollback-style inspection.

#### `audit_logs`

Purpose:

- Stores important actions for accountability and admin review.

#### `notifications`

Purpose:

- Stores user notifications.

### Relationships

The project uses foreign keys, but not many explicit SQLAlchemy relationship objects.

Main relationships:

- `students.user_id -> users.id`
- `match_runs.user_id -> users.id`
- `match_runs.profile_id -> students.id`
- `match_results.run_id -> match_runs.id`
- `match_results.scholarship_id -> scholarships.id`
- `saved_scholarships.user_id -> users.id`
- `saved_scholarships.scholarship_id -> scholarships.id`
- `scholarship_reports.user_id -> users.id`
- `scholarship_reports.scholarship_id -> scholarships.id`
- `notifications.user_id -> users.id`

### How querying works here

This app uses SQLAlchemy ORM queries.

That means Python code like this idea:

- start with `db.query(Model)`
- add `.filter(...)`
- get results with `.all()`, `.first()`, or `.scalar()`
- edit objects
- call `db.commit()`

One important design detail:

Several "list-like" fields are stored as JSON text inside normal text columns instead of separate relational tables. That makes some parts easier to build quickly, but it also means:

- more manual parsing
- weaker database-level structure
- harder filtering in some cases

Examples include fields like:

- preferred courses
- required documents
- priority groups
- some eligibility lists

## 7. Authentication and Security

### Simple idea first

Authentication answers:

- "Who are you?"

Authorization answers:

- "What are you allowed to do?"

In this app:

- login proves identity
- role checks and ownership checks decide permissions

### How login works

1. User submits email and password.
2. Backend checks the password against the stored hash.
3. Backend creates a JWT access token.
4. Frontend stores the token in `localStorage`.
5. Future requests send `Authorization: Bearer <token>`.
6. Backend decodes the token to identify the user.

### Security features present

- Password hashing with bcrypt
- JWT bearer token auth
- Admin role checks
- Profile ownership checks
- Endpoint rate limiting on auth routes
- CORS configuration
- Request logging

### Important weaknesses and risks

- Tokens are stored in `localStorage`, which is common but vulnerable to XSS if malicious scripts ever run in the page.
- The app supports `AUTH_DISABLED=true` for local development. That is convenient for dev, but dangerous if accidentally enabled in production.
- A weak/default `SECRET_KEY` would undermine JWT security.
- Consent is currently hardcoded in the profile payload instead of being clearly collected from the user. That is a legal and trust problem, not just a code problem.

## 8. Bugs, Issues, and Risks

This section does not auto-fix anything. It explains what is wrong, where it is, why it happens, and how you could fix it safely later.

### 1. Privacy consent is not actually collected

Severity:

- High

Where:

- `frontend/src/utils/studentProfilePayload.ts` lines 60-61

What is happening:

- The frontend always sends `privacy_consent: true` and a fixed consent version.

Why this is a problem:

- The user is not clearly giving consent in the UI.
- The system behaves as if consent happened even when no real consent interaction exists.

How to fix later:

1. Add an explicit consent checkbox in the profile builder.
2. Prevent form submission until the user checks it.
3. Send the real checkbox state and timestamp/version to the backend.

### 2. Frontend linting is currently broken

Severity:

- Medium

Where:

- `frontend/package.json` defines the lint script
- The repo has ESLint 9 installed, but there is no `eslint.config.js`

What is happening:

- `npm run lint` fails before it can check the code.

Why this is a problem:

- You lose a basic safety net for catching frontend mistakes early.

How to fix later:

1. Add an ESLint 9 flat config file such as `eslint.config.js`.
2. Or downgrade to an ESLint version that matches the old config format if the project intentionally used it before.

### 3. Theme listener cleanup is incorrect

Severity:

- Medium

Where:

- `frontend/src/contexts/ThemeContext.tsx` lines 35-36

What is happening:

- The code adds an event listener with one inline function and tries to remove it with a different inline function.

Why this is a problem:

- The cleanup does not remove the real listener.
- Over time this can create duplicate listeners or memory leaks.

How to fix later:

1. Store the listener in a named variable.
2. Pass the exact same function reference to both `addEventListener` and `removeEventListener`.

### 4. The Documents area is linked in the UI but not implemented

Severity:

- Medium

Where:

- `frontend/src/App.tsx`
- `frontend/src/components/layout/DashboardSidebar.tsx`
- `frontend/src/pages/DocumentsPage.tsx`

What is happening:

- The route exists and the sidebar invites users to visit it, but the page is only a placeholder.

Why this is a problem:

- Users are promised a workflow that does not exist yet.
- It creates a broken product expectation.

How to fix later:

1. Hide the route behind a feature flag until it is ready.
2. Or implement at least a minimal real document-tracking flow.

### 5. Dashboard search says it searches schools, but it mainly sends a title query

Severity:

- Medium

Where:

- Frontend placeholder: `frontend/src/components/layout/DashboardTopbar.tsx` line 273
- Frontend query navigation: same file around lines 164, 280, 321
- Backend search filtering: `app/api/v1/scholarship_search.py` lines 113 and 141-148

What is happening:

- The search box says "Search scholarships, schools..."
- But the topbar only passes a `query` parameter.
- The backend treats `query` mainly as a scholarship-title search.
- There is a separate `school` filter capability, but the topbar does not use it.

Why this is a problem:

- The UI promise and backend behavior do not match.

How to fix later:

1. Either change the placeholder text to reflect real behavior.
2. Or upgrade the topbar to send both `query` and `school` intelligently.

### 6. Search filter UI hardcodes education levels instead of using backend data

Severity:

- Medium

Where:

- Backend dynamic filter source: `app/api/v1/scholarship_search.py`
- Frontend hardcoded levels: `frontend/src/components/ScholarshipSearchFilters.tsx`

What is happening:

- The backend returns dynamic `education_levels`.
- The frontend fetches them but still renders a hardcoded list for the UI options.

Why this is a problem:

- Valid backend values can be missing from the visible filter choices.
- The filter UI can fall out of sync with real data.

How to fix later:

1. Render the backend-provided `education_levels`.
2. Keep a fallback list only if the API fails.

### 7. The backend supports multiple profiles per user, but the dashboard assumes only one

Severity:

- Medium

Where:

- `app/models.py` shows `students.user_id` is not unique
- `app/api/v1/profiles.py` lists profiles for a user
- `frontend/src/pages/ProfileDashboard.tsx` repeatedly uses `profiles[0]`

What is happening:

- A user can technically own multiple profiles.
- The dashboard always takes the first one.

Why this is a problem:

- If a user has more than one profile, the UI may show or match the wrong profile.

How to fix later:

1. Decide whether the product should allow multiple profiles.
2. If not, enforce one profile per user in both UI and backend.
3. If yes, add profile selection in the dashboard and route flows.

### 8. Scoring documentation is out of date

Severity:

- Low to medium

Where:

- `SCORING_ENGINE.md`
- `app/scoring/config.py`

What is happening:

- The docs still describe document readiness as part of the weighted score.
- The code comments in `app/scoring/config.py` show readiness was removed from scoring.

Why this is a problem:

- Developers and reviewers may misunderstand how ranking actually works.

How to fix later:

1. Update `SCORING_ENGINE.md` to match the real weights and formula.
2. Clearly mark readiness as a display/readiness helper instead of a scoring factor.

### 9. Placeholder trust content can be misleading

Severity:

- Low

Where:

- `frontend/src/pages/SuccessStoriesPage.tsx`
- `frontend/src/pages/ProfileDashboard.tsx`

What is happening:

- The success stories page says the stories are illustrative placeholders.
- But the same page still uses "Verified Scholar" wording, which sounds like a real validation badge.

Why this is a problem:

- It can confuse users about what is real data and what is mock content.

How to fix later:

1. Remove "verified" language from placeholders.
2. Add a stronger visual label saying "demo content" or "sample story".

### 10. Startup documentation is partly stale

Severity:

- Low

Where:

- `c:\Projects\START_HERE.md`
- `README.md`
- `c:\Projects\START_BOTH.bat`

What is happening:

- `START_HERE.md` still tells you to `cd Iskonnect-frontend`, which is the wrong path now.
- `README.md` mentions `START_BOTH.bat`, but that file lives one level above the repo.
- `START_BOTH.bat` still uses older "ISKOLAR" naming.

Why this is a problem:

- New contributors can get lost during setup.

How to fix later:

1. Update the docs to the real paths.
2. Move helper scripts into the repo if they are meant to be part of project onboarding.

### Region filter note

You specifically mentioned a possible region-filter problem.

What I found:

- I did not find an active "Region V" substring bug in the current code.
- The code in `app/matching/hard_filters.py` explicitly avoids false substring matches like `Region VI` accidentally matching `Region VII`.
- `app/tests/test_matching_regression.py` includes a regression test for this class of issue.

Conclusion:

- This appears to be a previously known problem that has already been fixed and protected by tests.

## 9. Beginner Learning Curriculum

This section teaches the concepts you need in order to understand the project, with project-specific examples.

### 9.1 Programming foundations

#### Variables

Simple idea:

- A variable is a labeled box that stores a value.

Project example:

- A React state variable may store the current email field.
- A Python variable may store `user_id` or `score`.

#### Functions

Simple idea:

- A function is a machine that takes input, does work, and returns output.

Project example:

- `login(email, password)` sends credentials to the backend.
- A backend function computes a scholarship score from profile data.

#### Conditionals

Simple idea:

- Conditionals let code choose between paths using `if`, `else if`, and `else`.

Project example:

- If the profile has no token, the UI may show a guest state.
- If income is above the scholarship threshold, a hard filter may reject the scholarship.

#### Loops

Simple idea:

- Loops repeat work for many items.

Project example:

- The backend loops through scholarships when generating matches.
- React loops through arrays using `.map()` to render cards.

#### Arrays and objects

Simple idea:

- An array is an ordered list.
- An object is a group of named properties.

Project example:

- A scholarship result list is an array.
- A profile object may contain fields like `name`, `region`, and `education_level`.

### 9.2 Frontend concepts

#### React basics

Simple idea:

- React lets you build the UI from components.

Project example:

- `ProfileDashboard.tsx` returns JSX describing what should appear on the dashboard.

#### Components

Simple idea:

- A component is a reusable piece of UI.

Project example:

- `ScholarshipCard.tsx` is reused for many results.

#### Props vs state

Simple idea:

- Props are inputs given to a component.
- State is data the component manages for itself.

Project example:

- A score card might receive a scholarship as props.
- The search page holds the current filter text in state.

#### Event handling

Simple idea:

- Event handling means "when the user does X, run Y."

Project example:

- Clicking "Save" triggers a submit handler.
- Typing into the search box updates local state and can trigger an API request.

#### Rendering flow

Simple idea:

- When state changes, React runs the component again and updates the visible UI.

Project example:

- After fetching matches, React re-renders the page with result cards.

#### Tailwind CSS

Simple idea:

- Tailwind is a utility-first CSS system.

Project example:

- Instead of writing a CSS rule called `.big-button`, you add classes like `rounded-xl px-4 py-2 bg-slate-900 text-white`.

#### UI system in this project

Simple idea:

- This project uses a custom UI layer, not a heavy component library.

Project example:

- Many UI pieces are hand-built in `src/components`.

### 9.3 API concepts

#### What is an API

Simple idea:

- An API is a waiter between two parts of a system.

Analogy:

- The frontend is the customer.
- The backend is the kitchen.
- The API is the order form.

#### HTTP methods

- `GET`: ask for data
- `POST`: create something or trigger an action
- `PUT`: replace or update
- `DELETE`: remove or deactivate

Project examples:

- `GET /api/v1/profiles`
- `POST /api/v1/auth/login`
- `PUT /api/v1/scholarships/{id}`
- `DELETE /api/v1/saved-scholarships/{id}`

#### Request/response cycle

Simple idea:

1. Frontend sends a request.
2. Backend receives it.
3. Backend does work.
4. Backend sends JSON back.
5. Frontend updates the UI.

#### JSON

Simple idea:

- JSON is the text format used to move structured data between frontend and backend.

Example:

```json
{
  "email": "student@example.com",
  "password": "secret123"
}
```

### 9.4 Backend concepts

#### FastAPI basics

Simple idea:

- FastAPI maps URLs to Python functions.

Project example:

- A function under `@router.post("/auth/login")` runs when the frontend posts login data.

#### Routing

Simple idea:

- Routing decides which backend function handles which URL.

Project example:

- `app/api/v1/profiles.py` owns profile-related routes.

#### Business logic

Simple idea:

- Business logic is the real domain behavior, not just input/output plumbing.

Project example:

- The scholarship scoring rules are business logic.

#### Middleware

Simple idea:

- Middleware runs before or after route handlers.

Project example:

- Logging middleware records request information.

### 9.5 Database concepts

#### Tables and rows

Simple idea:

- A table is a collection of similar records.
- A row is one record.

Project example:

- One row in `scholarships` means one scholarship entry.

#### Relationships

Simple idea:

- Relationships connect records from different tables.

Project example:

- A saved scholarship connects one user to one scholarship.

#### Queries

Simple idea:

- A query asks the database for data or tells it to change data.

Examples:

- `SELECT`: read
- `INSERT`: create
- `UPDATE`: change
- `DELETE`: remove

Project concept:

- Even though the app uses SQLAlchemy instead of raw SQL most of the time, it is still conceptually doing those same operations.

### 9.6 Auth and security

#### Authentication vs authorization

- Authentication: "Prove who you are."
- Authorization: "Check whether you may do this."

Project example:

- Login authenticates.
- `require_admin` authorizes admin-only routes.

#### Tokens

Simple idea:

- A token is like a temporary stamped pass.

Project example:

- After login, the backend gives a JWT token that the frontend sends on future requests.

#### Best practices to learn

- Never trust frontend input by itself.
- Validate on the backend.
- Hash passwords.
- Use strong secret keys.
- Be careful where tokens are stored.
- Separate admin actions from normal user actions.

### 9.7 Debugging skills

#### How to trace bugs

Simple method:

1. Start from the screen where the bug appears.
2. Find the page component.
3. Find the API call it makes.
4. Find the backend route that receives that call.
5. Find the service or database query behind that route.
6. Check logs, network responses, and test expectations.

#### Reading error messages

Simple idea:

- Error messages are clues, not enemies.

What to inspect:

- browser console
- network tab
- backend terminal logs
- stack traces
- failed test output

#### Console debugging

Project-specific tools:

- `console.log()` in React
- browser DevTools Network tab
- FastAPI logs in the terminal
- pytest failures for backend behavior

### 9.8 Git and version control

#### Why Git matters

Simple idea:

- Git is your time machine and collaboration record.

#### Core commands

Clone a repo:

```bash
git clone https://github.com/your-repo/scholarship-match.git
```

See current changes:

```bash
git status
```

Pull latest changes:

```bash
git pull
```

Stage files:

```bash
git add frontend/src/pages/ProfileDashboard.tsx
git add app/api/v1/profiles.py
```

Commit changes:

```bash
git commit -m "Improve dashboard profile loading"
```

Push changes:

```bash
git push
```

Create a new branch:

```bash
git checkout -b fix/profile-selection
```

#### Real example workflow

1. Pull the latest code.
2. Create a branch like `git checkout -b fix/theme-cleanup`.
3. Make a focused change.
4. Run tests and build.
5. `git add` the changed files.
6. `git commit -m "Fix ThemeContext listener cleanup"`.
7. `git push`.

### 9.9 System thinking

#### How to think like an engineer

Simple idea:

- Do not just look at one file.
- Ask where data came from, where it goes next, and which rules transformed it.

#### How to trace data flow

Use this pattern:

1. Find the visible UI field or button.
2. Find its event handler.
3. Find the API call.
4. Find the backend route.
5. Find the service and query.
6. Find the database model fields involved.
7. Trace the response all the way back to the rendered component.

#### How to debug large systems

Rules of thumb:

- Reproduce the issue consistently first.
- Narrow the failing layer: UI, network, backend, database, or data quality.
- Change one thing at a time.
- Trust logs and tests more than guesses.

## 10. How to Navigate This Project

### Best order to read the code

If you are new, use this exact order:

1. `README.md`
2. `frontend/src/main.tsx`
3. `frontend/src/App.tsx`
4. `frontend/src/pages/ProfileDashboard.tsx`
5. `frontend/src/pages/ProfileBuilderPage.tsx`
6. `frontend/src/contexts/AuthContext.tsx`
7. `frontend/src/api/client.ts`
8. `app/main.py`
9. `app/api/v1/profiles.py`
10. `app/api/v1/match_history.py`
11. `app/matching/match_service.py`
12. `app/matching/hard_filters.py`
13. `app/scoring/engine.py`
14. `app/models.py`
15. `app/schemas.py`

### How to run the project

Correct local development steps:

#### Backend

```bash
cd c:\Projects\scholarship-match
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

Alternative on Windows:

```bash
start-backend.bat
```

Backend URLs:

- App: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

#### Frontend

```bash
cd c:\Projects\scholarship-match\frontend
npm install
npm run dev
```

Alternative on Windows:

```bash
start-frontend.bat
```

Frontend URL:

- `http://localhost:5173`

### How to edit the UI safely

Safe frontend-first workflow:

1. Find the page component responsible for the screen.
2. Change layout, copy, spacing, or component composition there first.
3. Reuse existing props and data shapes whenever possible.
4. If you must change data shape, inspect the backend schema before editing.
5. Run the frontend build after changes.

### How to avoid breaking backend connections

Before changing any frontend payload or response handling:

1. Find the exact endpoint being called.
2. Check the backend schema or route implementation.
3. Compare the JSON keys carefully.
4. Keep optional vs required fields correct.
5. Test the network request in the browser DevTools.

### How to test changes

Backend tests:

```bash
cd c:\Projects\scholarship-match
python -m pytest app/tests -q
```

Frontend build:

```bash
cd c:\Projects\scholarship-match\frontend
npm run build
```

Frontend lint:

```bash
npm run lint
```

Important current note:

- `npm run lint` is presently broken because the repo has ESLint 9 without the required flat config file.

## 11. Safe Improvement Strategy

### Safest places to edit first

These are good beginner-friendly areas:

- text and copy in public pages
- visual styling in React components
- dashboard card layouts
- reusable presentational components
- placeholder content labels
- docs like `README.md` and setup guides

### Medium-risk areas

These require more caution:

- `frontend/src/utils/studentProfilePayload.ts`
- `frontend/src/types.ts`
- `frontend/src/api/client.ts`
- `app/schemas.py`
- `app/api/v1/profiles.py`
- `app/api/v1/scholarship_search.py`

Why:

- They define data contracts between frontend and backend.

### High-risk areas for now

Do not change these casually until you fully understand the system:

- `app/models.py`
- Alembic migration files
- `app/auth.py`
- `app/matching/hard_filters.py`
- `app/matching/match_service.py`
- `app/scoring/*`

Why:

- These files control persistence, security, and recommendation behavior.
- Small mistakes there can create silent data corruption or wrong matching decisions.

### Good strategy for making changes safely

1. Make one small change at a time.
2. Prefer UI-only changes first.
3. If you change an API contract, update both frontend and backend together.
4. Run backend tests.
5. Run frontend build.
6. Test the exact user journey in the browser.

## 12. What I Verified While Reviewing

I checked the project, not just the file names.

What passed:

- Backend test suite: `68 passed`
- Frontend production build: passed

What failed:

- Frontend lint script: failed because ESLint 9 flat config is missing

Additional note:

- The frontend build warns that the main JavaScript chunk is large, so bundle splitting may be worth improving later.

## 13. Short Mental Model to Remember

If you forget everything else, remember this:

- `frontend/` is what the user sees.
- `app/api/` is the door the frontend knocks on.
- `app/matching/` and `app/scoring/` are the brain of the product.
- `app/models.py` is the database blueprint.
- `alembic/` is the database history.
- Bugs often happen when one layer expects data in a different shape than another layer sends.

That is the core system.
