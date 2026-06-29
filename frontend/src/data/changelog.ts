/**
 * Changelog for ISKONNECT — written for students, not developers.
 *
 * Writing philosophy (use for every future release):
 * - Lead with student benefit: preparation, trust, reliability, ease of use, accessibility.
 * - Ask "Why should I care?" not "What changed technically?"
 * - Avoid jargon: API, cache, endpoint, migration, JSON, deduplication, backend, schema.
 * - Group items under friendly section headings (e.g. "Plan Ahead, Not Just Search").
 * - Be honest about limitations; never oversell.
 */

export interface ChangelogItem {
  title: string;
  description: string;
}

export interface ChangelogSection {
  heading: string;
  items: ChangelogItem[];
}

export interface ChangelogVersion {
  version: string;
  date: string;
  title: string;
  summary: string;
  sections: ChangelogSection[];
}

export const CHANGELOG_VERSIONS: ChangelogVersion[] = [
  {
    version: "2.1.0",
    date: "June 2026",
    title: "Your scholarship plan, not just a list",
    summary:
      "ISKONNECT now helps you see what's open today, what's coming soon, and what to prepare for—so you're less likely to miss an opportunity you qualify for.",
    sections: [
      {
        heading: "Plan Ahead, Not Just Search",
        items: [
          {
            title: "Your opportunity timeline",
            description:
              "Instead of an empty screen when nothing is open right now, you see a forward-looking plan: scholarships available today, opening soon, worth preparing for, and expected to reopen.",
          },
          {
            title: "Clearer next steps",
            description:
              "Each scholarship shows what you can do next—apply now, gather documents, or plan for when you become eligible—so you always know how to move forward.",
          },
        ],
      },
      {
        heading: "More Reliable Scholarship Information",
        items: [
          {
            title: "Transparent freshness labels",
            description:
              "See when a scholarship was last verified and where the information came from, so you can judge whether details are current before you apply.",
          },
          {
            title: "Careful review before listings go live",
            description:
              "New and updated scholarships are checked more carefully before they appear in your search, helping reduce duplicate or outdated entries.",
          },
        ],
      },
      {
        heading: "Better Mobile Experience",
        items: [
          {
            title: "Easier browsing on your phone",
            description:
              "Bottom navigation, larger tap targets, and a full-screen filter sheet make it simpler to search and plan on mobile.",
          },
        ],
      },
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "Preview matches while building your profile",
            description:
              "After you enter your region and education level, you can see sample matches before finishing every step—so you know ISKONNECT is working for you early.",
          },
          {
            title: "Document checklist on scholarship pages",
            description:
              "When you're signed in, scholarship details can show which required documents you still need—helping you prepare before deadlines arrive.",
          },
        ],
      },
    ],
  },
  {
    version: "2.0.0",
    date: "June 2026",
    title: "Ready for more students",
    summary:
      "A stronger, more trustworthy experience—better account controls, clearer layouts, and scholarship information you can rely on when planning applications.",
    sections: [
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Delete your account anytime",
            description:
              "You can remove your account and data from Settings whenever you choose, in line with your privacy rights.",
          },
          {
            title: "Clearer match results",
            description:
              "Your scholarship matches use the same easy-to-scan card layout as search, so you can compare options faster.",
          },
          {
            title: "Plain-language guidance",
            description:
              "Financial planning tools, save buttons, and profile steps use clearer wording so you always know what to do next.",
          },
        ],
      },
      {
        heading: "More Reliable Scholarship Information",
        items: [
          {
            title: "More accurate profile completion",
            description:
              "Optional fields no longer block you from reaching 100% profile completion, so your progress reflects what actually matters for matching.",
          },
          {
            title: "Safer, more private accounts",
            description:
              "Sign-in and account security were strengthened so your profile and saved scholarships stay protected.",
          },
        ],
      },
    ],
  },
  {
    version: "1.6.0",
    date: "June 2026",
    title: "Fairer, clearer matching",
    summary:
      "Matching became more accurate for Philippine programs, with better support for education levels, regions, and exclusive member-only scholarships.",
    sections: [
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "More accurate eligibility checks",
            description:
              "Programs are matched using clearer rules for your education level, region, and background—so you're less likely to see scholarships you can't actually apply for.",
          },
          {
            title: "Members-only programs",
            description:
              "Scholarships limited to specific groups (such as organization members) are labeled clearly so you know when extra requirements apply.",
          },
          {
            title: "Finer location matching",
            description:
              "Your city and guardian information can improve how regional scholarships are matched to you.",
          },
        ],
      },
    ],
  },
  {
    version: "1.5.0",
    date: "April 2026",
    title: "A steadier dashboard",
    summary:
      "Layout improvements, helpful planning tools on your dashboard, and notifications that keep you closer to deadlines and saved programs.",
    sections: [
      {
        heading: "Preparation & Planning",
        items: [
          {
            title: "Career planning shortcuts",
            description:
              "Explore career paths and review centers with guided searches tailored to the Philippines—useful when choosing courses and scholarships together.",
          },
          {
            title: "Saved scholarships in one place",
            description:
              "Programs you bookmark appear consistently across your dashboard and applications, so you don't lose track of what you're pursuing.",
          },
        ],
      },
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Clearer financial planning",
            description:
              "The financial planner compares scholarship benefits to your estimated school costs more accurately, with notes you can understand at a glance.",
          },
          {
            title: "Your data stays yours when you switch accounts",
            description:
              "Signing in as a different user no longer shows another person's profile by mistake.",
          },
        ],
      },
    ],
  },
  {
    version: "1.4.0",
    date: "April 2026",
    title: "Track applications and documents",
    summary:
      "Tools to organize requirements, compare costs, and follow applications—from first save to submission.",
    sections: [
      {
        heading: "Preparation & Planning",
        items: [
          {
            title: "Document checklists",
            description:
              "See which files each application needs and track what you've already gathered.",
          },
          {
            title: "Applications tracker",
            description:
              "Follow where each application stands with a simple timeline and linked documents.",
          },
          {
            title: "Financial planner",
            description:
              "Compare your estimated annual school costs against the benefits of scholarships you've saved.",
          },
        ],
      },
      {
        heading: "More Reliable Scholarship Information",
        items: [
          {
            title: "Reviewed before going live",
            description:
              "New scholarships from external sources are reviewed before they appear in your catalog, helping keep listings accurate.",
          },
          {
            title: "Expired programs marked clearly",
            description:
              "Scholarships whose deadlines have passed are updated automatically so you're not misled by closed windows.",
          },
        ],
      },
    ],
  },
  {
    version: "1.3.0",
    date: "April 2026",
    title: "Trust you can see",
    summary:
      "We explained how matching works, made it easier to send feedback, and redesigned scholarship cards so scores and deadlines are clearer.",
    sections: [
      {
        heading: "More Reliable Scholarship Information",
        items: [
          {
            title: "Transparency page",
            description:
              "Learn what your match score means, how it's built, and why it can change—so you always understand the numbers.",
          },
          {
            title: "Send feedback easily",
            description:
              "Report problems or suggest improvements directly from the app.",
          },
        ],
      },
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Redesigned scholarship cards",
            description:
              "Match scores, urgency labels, and detailed breakdowns help you decide which programs to prioritize.",
          },
        ],
      },
    ],
  },
  {
    version: "1.2.0",
    date: "March 2026",
    title: "Search, save, and stay organized",
    summary:
      "Browse scholarships with filters, save favorites, and manage everything from one dashboard.",
    sections: [
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Scholarship search with filters",
            description:
              "Find programs by region, field of study, income, and education level—without running a full match first.",
          },
          {
            title: "Save scholarships",
            description:
              "Bookmark programs you're interested in and find them quickly on your dashboard.",
          },
          {
            title: "One dashboard for everything",
            description:
              "Signed-in students get a consistent home for matches, saved programs, and profile tools.",
          },
        ],
      },
    ],
  },
  {
    version: "1.1.0",
    date: "March 2026",
    title: "Accounts and a growing catalog",
    summary:
      "Create an account, sign in securely, and access a scholarship catalog that stays up to date as new programs are added.",
    sections: [
      {
        heading: "Faster & More Reliable",
        items: [
          {
            title: "Scholarship pages load faster",
            description:
              "Browsing and matching feel snappier, even as the catalog grows.",
          },
        ],
      },
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Sign in to save your progress",
            description:
              "Create an account so your profile and matches are there whenever you return.",
          },
        ],
      },
    ],
  },
  {
    version: "1.0.0",
    date: "February 2026",
    title: "ISKONNECT launches",
    summary:
      "The first public version: match Filipino students to scholarships using real eligibility rules—not guesswork.",
    sections: [
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "Eligibility-based matching",
            description:
              "Your profile is checked against actual program rules for level, region, income, and field of study.",
          },
          {
            title: "Browse before you match",
            description:
              "Explore the scholarship catalog and filter programs on your own.",
          },
        ],
      },
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Built for Filipino students",
            description:
              "National branding, dark mode, and a design focused on clarity—not clutter.",
          },
        ],
      },
    ],
  },
  {
    version: "0.1.0",
    date: "January 2026",
    title: "Where it started",
    summary:
      "The first prototype: create a profile, see ranked scholarship matches, and understand why each program fits.",
    sections: [
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "Profile-based matching",
            description:
              "Enter your details once and see which scholarships you may qualify for, with explanations for each result.",
          },
        ],
      },
    ],
  },
];

/** Latest version string for Settings and other UI surfaces. */
export const APP_VERSION = CHANGELOG_VERSIONS[0]?.version ?? "2.1.0";
