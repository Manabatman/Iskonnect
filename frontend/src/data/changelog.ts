/**
 * Changelog for ISKONNECT (MVP). Newest versions first.
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
      "First public MVP: build a student profile, run eligibility-based matching, and see ranked scholarship results.",
    improvements: [
      {
        title: "Core matching",
        description:
          "Profile builder, rule-based eligibility matching, and ranked results with explanations.",
      },
    ],
  },
];
