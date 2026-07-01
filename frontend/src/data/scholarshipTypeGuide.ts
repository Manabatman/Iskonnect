export interface ScholarshipTypeGuideEntry {
  title: string;
  summary: string;
  examples: string[];
}

export const SCHOLARSHIP_TYPE_GUIDE: Record<string, ScholarshipTypeGuideEntry> = {
  "Merit-based": {
    title: "Merit-based",
    summary:
      "Awarded mainly for academic achievement, talent, or excellence. Financial need may be considered separately but is not the primary criterion.",
    examples: [
      "University honors scholarships with GWA requirements",
      "DOST-SEI science and technology merit grants",
      "Academic excellence awards from private foundations",
    ],
  },
  Need: {
    title: "Financial need",
    summary:
      "Designed for students from lower-income households. Eligibility usually depends on household income, socioeconomic status, or documented financial hardship.",
    examples: [
      "4Ps-linked educational assistance",
      "LGU grants for indigent students",
      "TESDA programs for economically disadvantaged learners",
    ],
  },
  "Merit-and-Need": {
    title: "Merit and need",
    summary:
      "Combines academic performance with financial need. You typically need to meet both a grade threshold and an income ceiling.",
    examples: [
      "CHED priority programs with GWA and income requirements",
      "University grants for high-achieving students from low-income families",
    ],
  },
  Affiliation: {
    title: "Affiliation",
    summary:
      "Limited to members of a specific group, organization, community, or institution. Extra membership or affiliation requirements apply.",
    examples: [
      "Cooperative member scholarships",
      "Organization or alumni association grants",
      "Employee-dependent educational benefits",
    ],
  },
};

export function getScholarshipTypeGuide(type: string | null | undefined): ScholarshipTypeGuideEntry | null {
  if (!type?.trim()) return null;
  return SCHOLARSHIP_TYPE_GUIDE[type.trim()] ?? {
    title: type.trim(),
    summary: "This program uses a specific scholarship type defined by the provider. Check the official listing for full criteria.",
    examples: [],
  };
}
