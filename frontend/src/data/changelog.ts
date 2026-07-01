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
    version: "1.0.0 Beta",
    date: "July 2026",
    title: "Public Beta",
    summary:
      "ISKONNECT is now in Public Beta—polished for real students, with clearer scholarship cards, faster search, and ongoing improvements guided by your feedback.",
    sections: [
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Cleaner scholarship cards",
            description:
              "Cards now highlight what matters most: status, deadline, provider, and scholarship type—without badge overload.",
          },
          {
            title: "Search that filters as you type",
            description:
              "Typing in search now updates results immediately, with filters that clearly show when they are active.",
          },
          {
            title: "Honest about being in beta",
            description:
              "We label ISKONNECT as Public Beta so you know the platform is usable today and still improving every week.",
          },
        ],
      },
      {
        heading: "More Reliable Scholarship Information",
        items: [
          {
            title: "Clearer status labels",
            description:
              "Scholarship statuses use one consistent vocabulary everywhere—from search cards to the status guide.",
          },
          {
            title: "Match score methodology explained",
            description:
              "A new page explains why match scores are weighted the way they are, including fairness principles and current limitations.",
          },
        ],
      },
    ],
  },
  {
    version: "0.8.0",
    date: "March–June 2026",
    title: "Building toward launch",
    summary:
      "Months of continuous development: matching engine, scholarship database, profile builder, search, admin tools, security, and accessibility.",
    sections: [
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "Eligibility-based matching",
            description:
              "Your profile is checked against real program rules before anything is ranked—so you see fewer dead ends.",
          },
          {
            title: "Opportunity timeline",
            description:
              "See what is open today, opening soon, and worth preparing for—not just a flat list.",
          },
        ],
      },
      {
        heading: "Easier to Use",
        items: [
          {
            title: "Scholarship search with filters",
            description: "Browse by region, field, income, education level, and application timing.",
          },
          {
            title: "Profile builder and dashboard",
            description: "Build your profile once and track matches, saved programs, and applications.",
          },
          {
            title: "Transparency page",
            description: "Learn how match scores are built and what the numbers mean.",
          },
        ],
      },
      {
        heading: "Faster & More Reliable",
        items: [
          {
            title: "Admin review tools",
            description: "Internal tools to verify listings, catch duplicates, and keep the catalog trustworthy.",
          },
          {
            title: "Security and accessibility improvements",
            description: "Stronger account controls, clearer layouts, and better mobile usability.",
          },
        ],
      },
    ],
  },
  {
    version: "0.5.0",
    date: "February 2026",
    title: "Full platform development begins",
    summary:
      "ISKONNECT expanded from experiments into a production-grade scholarship platform with active feature development.",
    sections: [
      {
        heading: "Easier to Use",
        items: [
          {
            title: "End-to-end student flows",
            description: "Registration, profiles, matching, and scholarship browsing wired together for real use.",
          },
        ],
      },
    ],
  },
  {
    version: "0.2.0",
    date: "January 2026",
    title: "Backend foundation",
    summary: "FastAPI backend, authentication research, and database architecture for a scalable catalog.",
    sections: [
      {
        heading: "Faster & More Reliable",
        items: [
          {
            title: "Authentication and data model",
            description: "Student accounts, profiles, and scholarship records designed for Philippine programs.",
          },
        ],
      },
    ],
  },
  {
    version: "0.1.0",
    date: "December 2025",
    title: "Where it started",
    summary:
      "Initial planning and backend experiments—a learning project to understand how scholarship matching could work.",
    sections: [
      {
        heading: "Smarter Scholarship Matches",
        items: [
          {
            title: "First prototype",
            description:
              "Early proof-of-concept: enter a profile and see ranked scholarship matches with basic explanations.",
          },
        ],
      },
    ],
  },
];

/** Latest semver for internal reference. */
export const APP_VERSION = "1.0.0";

/** Public-facing release label shown in Settings and Footer. */
export const APP_RELEASE_LABEL = "Public Beta";

export const APP_RELEASE_DATE = "July 2026";
