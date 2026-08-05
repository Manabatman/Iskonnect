export type OpportunityJourneyStatus = "live" | "planned" | "exploring";

export type OpportunityTypeDef = {
  slug: string;
  label: string;
  available: boolean;
  description: string;
  roadmapNote: string;
  journeyStatus: OpportunityJourneyStatus;
  /** Target launch window for planned verticals, e.g. "Q3 2026". */
  plannedFor?: string;
  journeyOrder: number;
  /** Canonical browse route when this vertical is live. */
  searchPath?: string;
};

export const OPPORTUNITY_TYPES: OpportunityTypeDef[] = [
  {
    slug: "scholarships",
    label: "Scholarships",
    available: true,
    searchPath: "/scholarships/search",
    description: "Financial aid for tuition, allowances, and school expenses.",
    roadmapNote: "Live today with verified scholarships and explainable matching.",
    journeyStatus: "live",
    journeyOrder: 1,
  },
  {
    slug: "internships",
    label: "Internships",
    available: false,
    description: "Paid or credit-bearing work placements with employers.",
    roadmapNote: "Requires employer verification and application-cycle tracking.",
    journeyStatus: "planned",
    plannedFor: "December 2026 to January 2027",
    journeyOrder: 2,
  },
  {
    slug: "ojt-practicum",
    label: "OJT / Practicum",
    available: false,
    description: "On-the-job training required by academic programs.",
    roadmapNote: "Requires school-partner workflows and document tracking.",
    journeyStatus: "planned",
    plannedFor: "June to August 2027",
    journeyOrder: 3,
  },
  {
    slug: "research-grants",
    label: "Research Grants",
    available: false,
    description: "Funding for undergraduate or graduate research projects.",
    roadmapNote: "Requires different eligibility rules than scholarships.",
    journeyStatus: "planned",
    plannedFor: "June to August 2027",
    journeyOrder: 4,
  },
  {
    slug: "conferences",
    label: "Conferences",
    available: false,
    description: "Student conferences, symposiums, and academic gatherings.",
    roadmapNote: "Requires event-date and registration-fee modeling.",
    journeyStatus: "planned",
    plannedFor: "June to August 2027",
    journeyOrder: 5,
  },
  {
    slug: "competitions",
    label: "Competitions",
    available: false,
    description: "Academic, innovation, and skills competitions with prizes.",
    roadmapNote: "Requires team eligibility and submission-deadline tracking.",
    journeyStatus: "planned",
    plannedFor: "December 2027 to January 2028",
    journeyOrder: 6,
  },
  {
    slug: "hackathons",
    label: "Hackathons",
    available: false,
    description: "Time-bound coding and product-building events.",
    roadmapNote: "Requires short-cycle deadline and team-size rules.",
    journeyStatus: "planned",
    plannedFor: "December 2027 to January 2028",
    journeyOrder: 7,
  },
  {
    slug: "student-exchange",
    label: "Student Exchange",
    available: false,
    description: "Semester or year abroad through partner universities.",
    roadmapNote: "Requires bilateral program verification and visa timelines.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 8,
  },
  {
    slug: "fellowships",
    label: "Fellowships",
    available: false,
    description: "Structured programs combining funding, mentorship, and service.",
    roadmapNote: "Requires multi-year commitment and return-service tracking.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 9,
  },
  {
    slug: "bootcamps",
    label: "Bootcamps",
    available: false,
    description: "Intensive short-term skills training programs.",
    roadmapNote: "Requires cohort-based scheduling and outcome verification.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 10,
  },
  {
    slug: "trainings",
    label: "Trainings",
    available: false,
    description: "Workshops, certifications, and upskilling programs.",
    roadmapNote: "Requires provider verification and seat-capacity fields.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 11,
  },
  {
    slug: "leadership-programs",
    label: "Leadership Programs",
    available: false,
    description: "Youth leadership, civic engagement, and development programs.",
    roadmapNote: "Requires nomination and endorsement tracking.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 12,
  },
  {
    slug: "ngo-opportunities",
    label: "NGO Opportunities",
    available: false,
    description: "Programs from non-government organizations serving youth.",
    roadmapNote: "Requires org verification and geographic scope rules.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 13,
  },
  {
    slug: "volunteer-programs",
    label: "Volunteer Programs",
    available: false,
    description: "Service-learning and community volunteer placements.",
    roadmapNote: "Requires hours-based eligibility instead of GPA filters.",
    journeyStatus: "exploring",
    plannedFor: "2028",
    journeyOrder: 14,
  },
  {
    slug: "startup-incubators",
    label: "Startup Incubators",
    available: false,
    description: "Founder support, seed funding, and accelerator programs.",
    roadmapNote: "Requires venture-stage and team-composition fields.",
    journeyStatus: "exploring",
    plannedFor: "2029",
    journeyOrder: 15,
  },
  {
    slug: "government-youth-programs",
    label: "Government Youth Programs",
    available: false,
    description: "National and local youth development initiatives beyond scholarships.",
    roadmapNote: "Requires program-type taxonomy beyond financial aid.",
    journeyStatus: "exploring",
    plannedFor: "2029",
    journeyOrder: 16,
  },
  {
    slug: "student-organizations",
    label: "Student Organizations",
    available: false,
    description: "Campus orgs, councils, and extracurricular leadership roles.",
    roadmapNote: "Requires school-scoped discovery and membership rules.",
    journeyStatus: "exploring",
    plannedFor: "2029",
    journeyOrder: 17,
  },
];

/** Timeline order for journey UI (Wave 6). */
export const OPPORTUNITY_JOURNEY_ORDERED = [...OPPORTUNITY_TYPES].sort(
  (a, b) => a.journeyOrder - b.journeyOrder
);

export function getOpportunityType(slug: string): OpportunityTypeDef | undefined {
  return OPPORTUNITY_TYPES.find((t) => t.slug === slug);
}
