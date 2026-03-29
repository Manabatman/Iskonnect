import type { ScholarshipInfo } from "../types";
import type { Opportunity } from "./mockOpportunities";

/** Map API scholarship rows to Opportunity cards (browser UI). */
export function scholarshipToOpportunity(s: ScholarshipInfo): Opportunity {
  const tags: string[] = [];
  if (s.level) tags.push(s.level);
  if (s.scholarship_type) tags.push(s.scholarship_type);
  if (s.provider_type) tags.push(s.provider_type);
  for (const r of s.regions ?? []) {
    const t = r.trim();
    if (t && !tags.includes(t)) tags.push(t);
  }
  if (tags.length === 0) tags.push("Scholarship");

  let stipend: string | undefined;
  if (s.benefit_allowance_monthly != null && s.benefit_allowance_monthly > 0) {
    stipend = `PHP ${s.benefit_allowance_monthly.toLocaleString()} / month`;
  } else if (s.benefit_total_value != null && s.benefit_total_value > 0) {
    stipend = `Up to PHP ${s.benefit_total_value.toLocaleString()} total`;
  }

  const openRaw = s.application_open_date;
  let isNew = false;
  if (openRaw) {
    const openMs = new Date(openRaw).getTime();
    if (!Number.isNaN(openMs)) {
      const days = (Date.now() - openMs) / (24 * 60 * 60 * 1000);
      isNew = days >= 0 && days <= 30;
    }
  }

  const deadline = s.application_deadline ?? undefined;
  const postedDate = (openRaw ?? deadline ?? new Date().toISOString()).slice(0, 10);

  const requirements: string[] = [];
  if (s.level) requirements.push(`Level: ${s.level}`);
  if (s.min_age != null || s.max_age != null) {
    const parts: string[] = [];
    if (s.min_age != null) parts.push(`min ${s.min_age}`);
    if (s.max_age != null) parts.push(`max ${s.max_age}`);
    requirements.push(`Age: ${parts.join(" • ")}`);
  }
  const regions = (s.regions ?? []).map((r) => r.trim()).filter(Boolean);
  if (regions.length) {
    requirements.push(
      `Regions: ${regions.slice(0, 5).join(", ")}${regions.length > 5 ? "…" : ""}`
    );
  }
  if (requirements.length === 0 && s.description) {
    const snippet = s.description.trim();
    requirements.push(snippet.length > 280 ? `${snippet.slice(0, 280)}…` : snippet);
  }
  if (requirements.length === 0) {
    requirements.push("See full description for requirements.");
  }

  const location =
    regions.length === 0
      ? "Nationwide"
      : regions.length <= 2
        ? regions.join(", ")
        : `${regions[0]} +${regions.length - 1} more`;

  return {
    id: s.id,
    title: s.title,
    organization: s.provider,
    location,
    description: s.description || "No description available.",
    tags: tags.slice(0, 6),
    stipend,
    deadline,
    requirements,
    link: s.link ?? undefined,
    isNew,
    postedDate,
  };
}
