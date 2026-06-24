/**
 * Changelog for Iskonnect (MVP). Newest versions first.
 * To add a release: push a new ChangelogVersion object to the top of CHANGELOG_VERSIONS.
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
    version: "1.6.0",
    date: "April 2026",
    title: "Career Roadmap, AI Mode search, and UX polish",
    summary:
      "Career Roadmap returns on the dashboard with Google AI Mode links; Review Center Finder opens the same AI-style Google view with richer queries. Scraping cron is paused (manual runs still available). Lighter default theme, dark-mode logo swap, clearer profile labels, fewer redundant API calls, and CI on Node.js 24.",
    improvements: [
      {
        title: "Career Roadmap card",
        description:
          "Dashboard card builds a Philippines-focused career query and opens Google AI Mode in a new tab.",
      },
      {
        title: "Review Center Finder + Google AI Mode",
        description:
          "Links use udm=50 with queries that mention fees, schedules, passing rates, and reviews for better synthesized answers.",
      },
      {
        title: "Saved scholarships in one place",
        description:
          "SavedScholarshipsContext loads the full saved list once; dashboard and applications reuse it instead of duplicating GET /saved-scholarships.",
      },
      {
        title: "Notification badge polling",
        description:
          "Unread count refreshes every 60 seconds instead of on every route change.",
      },
    ],
    fixes: [
      {
        title: "Target education level wording",
        description:
          "Profile builder clarifies “Target education level for scholarship” vs current academic stage.",
      },
      {
        title: "Match score ring in dark mode",
        description:
          "Arc and track colors are slightly brighter on dark backgrounds for readability.",
      },
    ],
    behindTheScenes: [
      {
        title: "Scraping schedule",
        description:
          "Automated PhilScholar cron commented out in scraper.yml; re-enable by uncommenting schedule. Manual workflow_dispatch still runs scrape + ingest.",
      },
      {
        title: "CI Node version",
        description:
          "GitHub Actions frontend job uses Node.js 24.",
      },
    ],
  },
  {
    version: "1.5.0",
    date: "April 2026",
    title: "Stability, security, and deployment readiness",
    summary:
      "Auth isolation fixes, UI polish, smarter scraping, deadline maintenance, production deployment helpers, and removal of the experimental AI roadmap card.",
    fixes: [
      {
        title: "Review Center Finder dark mode",
        description:
          "The finder card now respects dark theme so it matches the rest of the dashboard.",
      },
      {
        title: "Financial Planner tuition coverage",
        description:
          "Catalog total benefit is no longer multiplied by term count; coverage is capped to your estimated annual tuition with clearer notes.",
      },
      {
        title: "Account / profile isolation",
        description:
          "Local auth defaults to JWT required; dashboard state resets when the signed-in user changes to avoid stale profile data.",
      },
    ],
    improvements: [
      {
        title: "Scraper change detection",
        description:
          "PhilScholar listing HTML is hashed; unchanged listings skip ingest. GitHub Actions validates DATABASE_URL and scrape output before ingest.",
      },
      {
        title: "Deadline maintenance",
        description:
          "Daily workflow deactivates scholarships whose application deadline is in the past (no re-scrape required).",
      },
      {
        title: "Scholarship card images",
        description:
          "Static hero images under /public/images/scholarships with provider-type fallback and graceful image error handling.",
      },
    ],
    behindTheScenes: [
      {
        title: "CI and tooling",
        description:
          "GitHub Actions frontend job uses Node.js 22. Render: add .python-version (3.11.x) to avoid Python 3.14 build failures. See docs/DEPLOYMENT.md.",
      },
      {
        title: "Admin monitoring",
        description:
          "GET /api/v1/admin/staging/stats for staging queue counts (admin). Existing scraper run list endpoint unchanged.",
      },
    ],
  },
  {
    version: "1.4.0",
    date: "March 2026",
    title: "Reliability and clearer errors",
    summary:
      "Fixed a backend bug that could break profile loading, and improved how the app explains connection problems so you know what to check.",
    fixes: [
      {
        title: "Profile list responses",
        description:
          "Resolved a server error when reading saved list fields (courses, activities, awards) from profiles. Listing and saving profiles should work reliably again.",
      },
      {
        title: "Dashboard and match errors",
        description:
          "When the API is unreachable, messages now point to checking that the server is running and that the app is pointed at the correct API URL—instead of only a generic failure.",
      },
    ],
    behindTheScenes: [
      {
        title: "Configuration check",
        description:
          "Confirmed CORS and frontend API base URL settings for typical local development (Vite + FastAPI).",
      },
    ],
  },
  {
    version: "1.3.0",
    date: "March 2026",
    title: "Unified dashboard and landing",
    summary:
      "Signed-in users get a consistent dashboard experience. Visitors see a clear landing page; logout returns home without odd mixed layouts.",
    improvements: [
      {
        title: "One layout when signed in",
        description:
          "Dashboard routes use a single sidebar layout. Unauthenticated visitors are redirected to sign in instead of seeing broken chrome.",
      },
      {
        title: "New landing page",
        description:
          "Public home explains the product and points to sign up or sign in without the old long-form profile on the same screen.",
      },
      {
        title: "Profile builder as the main path",
        description:
          "Links to create or edit a profile go to the step-by-step profile builder. Successful login and registration open the builder first.",
      },
    ],
    fixes: [
      {
        title: "Match results and auth",
        description:
          "Match requests include auth headers where the API expects them, reducing failed loads after you save a profile.",
      },
      {
        title: "Logout destination",
        description:
          "Signing out sends you to the public home instead of leaving you on a half-logged-in dashboard screen.",
      },
    ],
  },
  {
    version: "1.2.0",
    date: "March 2025",
    title: "Search and saved scholarships",
    summary: "Browse programs with filters and save the ones you care about to your dashboard.",
    improvements: [
      {
        title: "Scholarship search",
        description:
          "Browse scholarships with a search bar, filters (region, field, income, education level, provider), and pagination. A detail panel opens when you select a result.",
      },
      {
        title: "Save scholarships",
        description:
          "Bookmark scholarships with a save control. Saved items appear on your dashboard when you are signed in.",
      },
    ],
  },
  {
    version: "1.1.0",
    date: "March 2025",
    title: "Stronger profiles and clearer matches",
    summary: "Richer profile options, legal pages, and a clearer view of why a scholarship matched.",
    improvements: [
      {
        title: "Scholarship detail page",
        description:
          "View Details opens an internal page with eligibility, benefits, requirements, and timeline.",
      },
      {
        title: "Multiple course preferences",
        description: "Specify up to three preferred courses to improve how matches are ranked.",
      },
      {
        title: "Tiered form validation",
        description: "Required and recommended fields with clearer validation and confirmation where needed.",
      },
      {
        title: "Legal and account pages",
        description: "About, Terms, Privacy, Settings, and Changelog pages added.",
      },
      {
        title: "Region dropdown",
        description: "Region selection uses a dropdown of Philippine regions.",
      },
      {
        title: "Why you matched",
        description: "Match breakdown appears as a clearer, card-style scorecard.",
      },
      {
        title: "Nationwide scholarships",
        description: "Programs that apply nationwide display correctly when region lists are empty.",
      },
      {
        title: "Application timing",
        description: "Shows when an application window opens in the future (for example, opens in X days).",
      },
    ],
    fixes: [
      {
        title: "Duplicate questions",
        description: "Removed duplicate prompts for underprivileged status and OFW dependent where they appeared twice.",
      },
    ],
  },
  {
    version: "1.0.0",
    date: "March 2025",
    title: "Initial release",
    summary:
      "First MVP in development: build a student profile, run eligibility-based matching, and see ranked scholarship results.",
    improvements: [
      {
        title: "Core matching",
        description:
          "Profile builder, rule-based eligibility matching, and ranked results with explanations.",
      },
    ],
  },
];
