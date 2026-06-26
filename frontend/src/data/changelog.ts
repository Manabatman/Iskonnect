/**
 * Changelog for Iskonnect. Newest versions first.
 * Grounded in repository git history (Jan 2026 – Jun 2026).
 */

export interface ChangelogItem {
  title: string;
  description: string;
}

export interface ChangelogVersion {
  version: string;
  date: string;
  title: string;
  summary: string;
  fixes?: ChangelogItem[];
  improvements?: ChangelogItem[];
  behindTheScenes?: ChangelogItem[];
}

export const CHANGELOG_VERSIONS: ChangelogVersion[] = [
  {
    version: "2.0.0",
    date: "June 2026",
    title: "Launch readiness and production hardening",
    summary:
      "Production deployment fixes, database migration corrections, security hardening, admin-only metrics, email-verification gate at login, and deployment documentation aligned with the live stack (Vercel + Render + Supabase).",
    fixes: [
      {
        title: "Database migration 023",
        description:
          "Fixed scholarships_staging index name, enabled pgcrypto for dedupe backfill, and removed silent failure on duplicate dedupe keys so migrations apply cleanly on Supabase.",
      },
      {
        title: "Profile completion accuracy",
        description:
          "Optional fields such as parent occupation no longer block 100% profile completion; income bracket and annual income count as one satisfied signal.",
      },
    ],
    improvements: [
      {
        title: "Account deletion",
        description:
          "Settings now supports self-service account deletion with confirmation, aligned with RA 10173 right to erasure.",
      },
      {
        title: "Match results layout",
        description:
          "Active match results use the same responsive card grid as scholarship search for easier scanning.",
      },
      {
        title: "Launch polish",
        description:
          "Plain-language Financial Planner copy, clearer save-scholarship actions, consent modal, trust banner palette, and consistent profile CTAs.",
      },
    ],
    behindTheScenes: [
      {
        title: "RLS on SIPP/OJT tables",
        description:
          "Row Level Security enabled on hte_partners, internship_opportunities, and ojt_compliance_vault for Supabase Data API hardening.",
      },
      {
        title: "Admin-only /metrics",
        description:
          "Operational counters require an admin JWT instead of being publicly accessible.",
      },
      {
        title: "Supabase pooler compatibility",
        description:
          "Postgres connection uses prepare_threshold=0 for the transaction pooler; ACCESS_TOKEN_EXPIRE_MINUTES is env-configurable.",
      },
    ],
  },
  {
    version: "1.6.0",
    date: "June 2026",
    title: "Matching engine remediation and Iskonnect branding",
    summary:
      "Matching engine hardening, education-level taxonomy, members-only scholarships, guardian/PSGC fields, auth isolation tests, and production sanitation for public launch.",
    improvements: [
      {
        title: "Matching engine remediation",
        description:
          "Hard filters, field matching, and scoring explanations refined; eval regression gate added to CI.",
      },
      {
        title: "Members-only scholarships",
        description:
          "Scholarships can be flagged members_only for exclusive priority-group programs.",
      },
      {
        title: "Guardian and PSGC fields",
        description:
          "Student profiles support guardian consent and PSGC location codes for finer regional matching.",
      },
    ],
    behindTheScenes: [
      {
        title: "Auth isolation tests",
        description:
          "Automated tests verify users cannot access each other's profiles, matches, or saved scholarships.",
      },
    ],
  },
  {
    version: "1.5.0",
    date: "April 2026",
    title: "Stability, dashboard layout, and theme UX",
    summary:
      "Dashboard layout refinements, theme UX polish, Career Roadmap and Review Center Finder with Google AI Mode, saved-scholarships context deduplication, and notification polling improvements.",
    improvements: [
      {
        title: "Career Roadmap card",
        description:
          "Dashboard card builds a Philippines-focused career query and opens Google AI Mode in a new tab.",
      },
      {
        title: "Review Center Finder",
        description:
          "Location- and exam-aware queries open Google AI Mode with fees, schedules, passing rates, and reviews.",
      },
      {
        title: "Saved scholarships in one place",
        description:
          "SavedScholarshipsContext loads the full saved list once; dashboard and applications reuse it.",
      },
    ],
    fixes: [
      {
        title: "Financial Planner tuition coverage",
        description:
          "Scholarship benefit value is capped to estimated annual tuition (not multiplied by term count) with clearer notes.",
      },
      {
        title: "Account / profile isolation",
        description:
          "Dashboard state resets when the signed-in user changes to avoid stale profile data.",
      },
    ],
    behindTheScenes: [
      {
        title: "Scraper schedule",
        description:
          "PhilScholar scrape runs Mon and Thu via GitHub Actions (workflow_dispatch also available). Listing change detection skips ingest when HTML is unchanged.",
      },
      {
        title: "CI Node version",
        description: "GitHub Actions frontend job uses Node.js 24.",
      },
    ],
  },
  {
    version: "1.4.0",
    date: "April 2026",
    title: "Documents, financial planner, and AI tools",
    summary:
      "Document vault workflow, financial planner on the dashboard, applications timeline, sponsor/school portals, and scraper pipeline with admin staging approval.",
    improvements: [
      {
        title: "Documents workflow",
        description:
          "Per-application document checklists, Drive folder links, and profile document sync from application progress.",
      },
      {
        title: "Financial Planner",
        description:
          "Compare your estimated annual costs against saved scholarship benefit amounts.",
      },
      {
        title: "Applications tracker",
        description:
          "Track scholarship applications with status timeline and document links.",
      },
      {
        title: "Scraper and staging",
        description:
          "PhilScholar scraper ingests into a staging queue; admins approve rows before they enter the live catalog.",
      },
    ],
    behindTheScenes: [
      {
        title: "Refresh tokens",
        description:
          "Rotating refresh tokens stored hashed in the database; shorter-lived access tokens.",
      },
      {
        title: "Deadline maintenance",
        description:
          "Daily GitHub Action expires scholarships whose application deadline has passed.",
      },
    ],
  },
  {
    version: "1.3.0",
    date: "April 2026",
    title: "Trust-focused UX and transparency",
    summary:
      "Feedback modal, transparency page explaining match scores, scholarship card redesign, and marketing landing improvements.",
    improvements: [
      {
        title: "Transparency page",
        description:
          "Explains what match scores mean, scoring weights, and why scores can change.",
      },
      {
        title: "Feedback",
        description: "In-app feedback modal sends suggestions and bug reports to the team.",
      },
      {
        title: "Scholarship cards",
        description: "Redesigned cards with score rings, urgency badges, and match analysis modal.",
      },
    ],
  },
  {
    version: "1.2.0",
    date: "March 2026",
    title: "Unified dashboard, search, and admin",
    summary:
      "Unified dashboard layout, scholarship search with filters, saved scholarships, admin analytics, and profile builder as the main onboarding path.",
    improvements: [
      {
        title: "Scholarship search",
        description:
          "Browse programs with search, filters (region, field, income, education level), and pagination.",
      },
      {
        title: "Save scholarships",
        description: "Bookmark scholarships; saved items appear on your dashboard.",
      },
      {
        title: "Unified dashboard",
        description:
          "Signed-in users get a consistent sidebar layout; visitors see a dedicated landing page.",
      },
      {
        title: "Admin analytics",
        description: "Admin overview of scholarships, profiles, match runs, and staging queue.",
      },
    ],
    fixes: [
      {
        title: "Profile list responses",
        description:
          "Resolved server errors when reading list fields (courses, activities, awards) from profiles.",
      },
      {
        title: "Registration and profile persistence",
        description:
          "Fixed registration fetch failures and improved profile save reliability.",
      },
    ],
  },
  {
    version: "1.1.0",
    date: "March 2026",
    title: "Production readiness foundation",
    summary:
      "PostgreSQL with Alembic migrations, JWT authentication, Sentry error tracking, React Router, admin UI, rate limiting, and scholarship cache with TTL.",
    improvements: [
      {
        title: "PostgreSQL and migrations",
        description:
          "Alembic migration chain replaces SQLite-only dev; Supabase-compatible schema.",
      },
      {
        title: "JWT authentication",
        description: "Register, login, and protected API routes with bcrypt password hashing.",
      },
      {
        title: "Scholarship cache",
        description: "Redis-backed scholarship list cache with TTL and invalidation on catalog changes.",
      },
    ],
    behindTheScenes: [
      {
        title: "CI pipeline",
        description:
          "GitHub Actions runs pytest, Postgres migration round-trip, and frontend lint/test/build.",
      },
    ],
  },
  {
    version: "1.0.0",
    date: "February 2026",
    title: "Policy-aligned matching and national branding",
    summary:
      "Philippine scholarship policy alignment, domain-layer scoring refactor, needs picker, scholarship browser, and Iskonnect national branding.",
    improvements: [
      {
        title: "Policy-aligned matching",
        description:
          "Eligibility rules aligned with Philippine scholarship programs; improved level and region handling.",
      },
      {
        title: "Scholarship browser",
        description: "Browse and filter scholarships before the full search experience.",
      },
      {
        title: "Iskonnect branding",
        description: "National Filipino branding, component structure, and dark mode support.",
      },
    ],
    fixes: [
      {
        title: "Scoring architecture",
        description: "Moved scoring logic to a dedicated domain layer with test coverage.",
      },
      {
        title: "CORS and region field",
        description: "Removed duplicate CORS middleware; fixed region field styling.",
      },
    ],
  },
  {
    version: "0.1.0",
    date: "January 2026",
    title: "Project genesis",
    summary:
      "FastAPI skeleton with profile creation, rule-based scholarship scoring, SQLite persistence, and initial React frontend.",
    improvements: [
      {
        title: "Core matching MVP",
        description:
          "Student profile creation, eligibility-based matching, and ranked results with explanations.",
      },
      {
        title: "API foundation",
        description: "FastAPI with profiles and scholarships CRUD; health endpoint.",
      },
    ],
  },
];

/** Latest version string for Settings and other UI surfaces. */
export const APP_VERSION = CHANGELOG_VERSIONS[0]?.version ?? "2.0.0";
