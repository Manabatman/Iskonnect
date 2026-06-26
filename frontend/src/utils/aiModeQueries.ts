/** Normalize location text and avoid duplicate "Philippines" tokens in AI Mode queries. */
export function normalizePhilippinesLocation(raw: string): string {
  const trimmed = raw.trim();
  if (!trimmed) return "Philippines";
  const lower = trimmed.toLowerCase();
  if (lower === "philippines" || lower.endsWith(", philippines") || lower.endsWith(" philippines")) {
    return trimmed.replace(/\s*,?\s*philippines\s*$/i, "").trim() || "Philippines";
  }
  return trimmed;
}

function withPhilippinesContext(location: string): string {
  const loc = normalizePhilippinesLocation(location);
  if (loc.toLowerCase() === "philippines") return "Philippines";
  return `${loc}, Philippines`;
}

/** Structured query for Review Center Finder → Google AI Mode. */
export function buildReviewCenterAiModeQuery(location: string, examFocus?: string | null): string {
  const locPhrase = withPhilippinesContext(location);
  const exam = examFocus?.trim();
  if (exam) {
    return [
      `${exam} review centers near ${locPhrase}.`,
      "Compare tuition fees, class schedules (weekend, daily, online),",
      "passing rates, teaching style, and recent student reviews.",
    ].join(" ");
  }
  return [
    `College entrance exam review centers near ${locPhrase}.`,
    "Compare fees, schedules, passing rates, and student reviews",
    "for UPCAT, DCAT, ACET, and similar programs.",
  ].join(" ");
}

const EDUCATION_LEVEL_LABELS: Record<string, string> = {
  "Senior High School": "a senior high school student",
  "College / University": "a college or university student",
  "Graduate School": "a graduate school applicant",
  "TVET / Technical-Vocational": "a TVET or technical-vocational student",
};

function educationLevelPhrase(level: string): string {
  const trimmed = level.trim();
  if (!trimmed) return "a Filipino student";
  return EDUCATION_LEVEL_LABELS[trimmed] ?? `a Filipino student at ${trimmed} level`;
}

/** Structured query for Career Roadmap → Google AI Mode. */
export function buildCareerRoadmapQuery(career: string, educationLevel: string): string {
  const job = career.trim() || "undecided career path";
  const audience = educationLevelPhrase(educationLevel);
  return [
    `Career roadmap for ${job} in the Philippines for ${audience}.`,
    "Include typical job roles, day-to-day tasks, required skills,",
    "entry requirements, salary range in PHP, career progression,",
    "common challenges, and recommended courses or certifications.",
  ].join(" ");
}
