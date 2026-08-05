/** Plain-language definitions for Philippine education and aid terms (CLARITY-02). */

export type GlossaryEntry = {
  term: string;
  definition: string;
  /** Optional Tagalog gloss when clearer for students. */
  tagalog?: string;
};

export const GLOSSARY = {
  GWA: {
    term: "GWA",
    definition:
      "General Weighted Average — your overall grade average across subjects, often shown as a percentage or on a 1.0–5.0 scale.",
    tagalog: "Kabuuang average ng mga grado mo sa lahat ng subject.",
  },
  TVET: {
    term: "TVET",
    definition:
      "Technical-Vocational Education and Training — skills programs (often through TESDA) that lead to certificates or national certifications.",
  },
  ALS: {
    term: "ALS",
    definition:
      "Alternative Learning System — a DepEd program for out-of-school youth and adults to complete basic education outside the regular classroom.",
    tagalog: "Alternatibong paraan para makatapos ng high school o elementary.",
  },
  LOA: {
    term: "LOA",
    definition:
      "Leave of Absence — a formal pause from enrollment while keeping your student status, usually with school approval.",
  },
  "4Ps": {
    term: "4Ps",
    definition:
      "Pantawid Pamilyang Pilipino Program — a government cash aid program for low-income households, often linked to Listahanan (the national poverty registry).",
    tagalog: "Pantawid Pamilya — tulong-pinansyal mula sa gobyerno para sa mga mahihirap na pamilya.",
  },
  PSCED: {
    term: "PSCED",
    definition:
      "Philippine Standard Classification of Education — the official list of course and field-of-study codes used by CHED and scholarship providers.",
  },
  SUC: {
    term: "SUC",
    definition: "State University or College — a public higher-education institution run by the national government.",
    tagalog: "Pampublikong unibersidad ng gobyerno.",
  },
  LUC: {
    term: "LUC",
    definition: "Local University or College — a public college established and funded by a local government unit (LGU).",
  },
  HEI: {
    term: "HEI",
    definition: "Higher Education Institution — any college or university authorized to offer degree programs.",
  },
  CHED: {
    term: "CHED",
    definition:
      "Commission on Higher Education — the national agency that regulates colleges and universities in the Philippines.",
  },
  "DOST-SEI": {
    term: "DOST-SEI",
    definition:
      "Department of Science and Technology — Science Education Institute — the DOST arm that administers science and technology scholarships.",
  },
  TESDA: {
    term: "TESDA",
    definition:
      "Technical Education and Skills Development Authority — the agency overseeing technical-vocational training and certifications.",
  },
  LGU: {
    term: "LGU",
    definition: "Local Government Unit — your city, municipality, or province; many LGUs offer local scholarship grants.",
    tagalog: "Pamahalaang lokal — lungsod, bayan, o probinsya mo.",
  },
  scholarship: {
    term: "Scholarship",
    definition:
      "A financial aid program you may apply for if you meet its rules. On ISKONNECT we use scholarship for any verified opportunity in the catalog.",
  },
  match: {
    term: "Match",
    definition:
      "A ranked recommendation showing how well your profile fits a program's published rules—not your odds of winning.",
  },
  profile: {
    term: "Profile",
    definition:
      "The information you save about your education, location, and goals. We compare it to each program's eligibility rules.",
  },
} as const satisfies Record<string, GlossaryEntry>;

export type GlossaryTermKey = keyof typeof GLOSSARY;
