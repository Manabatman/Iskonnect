import type { ScholarshipSearchFilters } from "../types";

export type ActiveFilterChip = {
  key: keyof ScholarshipSearchFilters | "query";
  label: string;
};

const TIMING_LABELS: Record<string, string> = {
  open_now: "Open now",
  opening_soon: "Opening soon",
  expected_reopen: "Expected to reopen",
  closed: "Closed",
  previous_cycle: "Past cycle",
  needs_verification: "Needs verification",
  archived: "No longer offered",
};

const LIFE_STAGE_LABELS: Record<string, string> = {
  high_school: "High school",
  college: "College",
  graduate: "Graduate",
  tvet: "TVET",
};

const INCOME_LABELS: Record<number, string> = {
  250_000: "Below ₱250K",
  400_000: "₱250K - ₱400K",
  500_000: "₱400K - ₱500K",
  500_001: "Above ₱500K",
};

/** Build removable chips for the applied-filter summary bar. */
export function buildActiveFilterChips(
  filters: ScholarshipSearchFilters,
  query?: string
): ActiveFilterChip[] {
  const chips: ActiveFilterChip[] = [];
  const q = query?.trim();
  if (q) chips.push({ key: "query", label: `Search: ${q}` });
  if (filters.region) chips.push({ key: "region", label: `Region: ${filters.region}` });
  if (filters.education_level) chips.push({ key: "education_level", label: `Level: ${filters.education_level}` });
  if (filters.life_stage) {
    chips.push({
      key: "life_stage",
      label: `Level: ${LIFE_STAGE_LABELS[filters.life_stage] ?? filters.life_stage}`,
    });
  }
  if (filters.timing) {
    chips.push({ key: "timing", label: `Timing: ${TIMING_LABELS[filters.timing] ?? filters.timing}` });
  }
  if (filters.field) chips.push({ key: "field", label: `Study area: ${filters.field}` });
  if (filters.school) chips.push({ key: "school", label: `School: ${filters.school}` });
  if (filters.provider) chips.push({ key: "provider", label: `Provider: ${filters.provider}` });
  if (filters.max_income != null && filters.max_income >= 0) {
    const incomeLabel = INCOME_LABELS[filters.max_income] ?? `≤ ₱${filters.max_income.toLocaleString()}`;
    chips.push({ key: "max_income", label: `Income: ${incomeLabel}` });
  }
  if (filters.include_archived) chips.push({ key: "include_archived", label: "Including archived" });
  return chips;
}

export function removeFilterChip(
  filters: ScholarshipSearchFilters,
  key: ActiveFilterChip["key"]
): ScholarshipSearchFilters {
  if (key === "query") return filters;
  const next = { ...filters };
  delete next[key];
  return next;
}
