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
      "Programs that may consider academic performance and/or financial need. Specific gates vary by provider — some use separate merit and need tracks, others combine criteria. Always check the official listing.",
    examples: [
      "University programs with both GWA and income guidelines",
      "Government grants with academic and socioeconomic criteria",
      "Institutional aid with multiple evaluation tracks",
    ],
  },
  Affiliation: {
    title: "Affiliation",
    summary:
      "Limited to members of a specific group, organization, community, or institution. Many affiliation programs also add merit, need, or residency requirements beyond membership.",
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
