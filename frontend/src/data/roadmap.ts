/** Public roadmap columns (UX-12) — quarter-level, plans can change. */

export type RoadmapColumn = "planned" | "in_progress" | "shipped";

export type RoadmapItem = {
  id: string;
  title: string;
  column: RoadmapColumn;
};

export const ROADMAP_DISCLAIMER =
  "Quarter-level priorities for ISKONNECT. Plans can change as we learn from students and maintainers—direction, not fixed dates.";

export const ROADMAP_ITEMS: RoadmapItem[] = [
  { id: "catalog-300", title: "Catalog depth toward 300 verified listings", column: "in_progress" },
  { id: "land-perf", title: "Landing performance and accessibility gate (LAND-10)", column: "in_progress" },
  { id: "status-guide", title: "Two-layer scholarship status guide", column: "shipped" },
  { id: "trust-pages", title: "Consolidated trust pages (how matching works / how we verify)", column: "shipped" },
  { id: "public-stats", title: "Live public stats on landing", column: "shipped" },
  { id: "onboarding", title: "Profile completion payoff and onboarding polish", column: "planned" },
  { id: "feedback-triage", title: "Feedback triage workflow for maintainers", column: "in_progress" },
  { id: "referral-metrics", title: "Outbound referral click instrumentation", column: "in_progress" },
  { id: "persona-eval", title: "Expanded persona and eval coverage", column: "planned" },
];

export const ROADMAP_COLUMN_LABELS: Record<RoadmapColumn, string> = {
  planned: "Planned",
  in_progress: "In progress",
  shipped: "Shipped",
};
