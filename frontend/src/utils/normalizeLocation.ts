/**
 * Display-only normalization for scholarship regions.
 * CHED and DOST national programs should always read as Nationwide.
 * If regions cover Luzon, Visayas, and Mindanao (with or without NCR/Metro Manila), treat as Nationwide.
 */
function coversMajorIslandGroups(regionsLower: string): boolean {
  const hasNcr = regionsLower.includes("ncr") || regionsLower.includes("metro manila");
  const hasLuzon = regionsLower.includes("luzon");
  const hasVisayas = regionsLower.includes("visayas");
  const hasMindanao = regionsLower.includes("mindanao");
  const groups = [hasNcr, hasLuzon, hasVisayas, hasMindanao].filter(Boolean).length;
  // At least 3 of the 4 major groups (NCR/Metro Manila, Luzon, Visayas, Mindanao)
  return groups >= 3;
}

export function normalizeScholarshipRegions(
  regions: string[] | undefined | null,
  provider: string | null | undefined
): string[] {
  const p = (provider ?? "").toUpperCase();
  if (p.includes("CHED") || p.includes("DOST")) {
    return ["Nationwide"];
  }
  const cleaned = (regions ?? []).map((r) => r.trim()).filter(Boolean);
  const combined = cleaned.join(" ").toLowerCase();
  if (coversMajorIslandGroups(combined)) {
    return ["Nationwide"];
  }
  return cleaned;
}

/** Single line for cards: Nationwide when empty after normalization. */
export function formatScholarshipLocation(
  regions: string[] | undefined | null,
  provider: string | null | undefined
): string {
  const norm = normalizeScholarshipRegions(regions, provider);
  if (norm.length === 0) return "Nationwide";
  return norm.join(" · ");
}
