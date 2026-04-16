/**
 * Static hero image paths under /public/images/scholarships/.
 * Extend SCHOLARSHIP_IMAGE_BY_PROVIDER with exact provider names from your catalog.
 */
const SCHOLARSHIP_IMAGE_BY_PROVIDER: Record<string, string> = {
  CHED: "/images/scholarships/government.svg",
  DOST: "/images/scholarships/government.svg",
  "DOST-SEI": "/images/scholarships/government.svg",
  TESDA: "/images/scholarships/government.svg",
};

const DEFAULT_HERO = "/images/scholarships/default.svg";

/**
 * Returns a public URL for the card header image, or null to use gradient-only header.
 */
export function getScholarshipHeroImageUrl(
  provider?: string | null,
  providerType?: string | null
): string | null {
  const p = (provider || "").trim();
  if (p) {
    const upper = p.toUpperCase();
    for (const [key, url] of Object.entries(SCHOLARSHIP_IMAGE_BY_PROVIDER)) {
      if (upper.includes(key)) return url;
    }
  }
  const t = `${providerType ?? ""}`.toLowerCase();
  if (t.includes("government") || t.includes("lgu")) {
    return "/images/scholarships/government.svg";
  }
  if (t.includes("private")) {
    return "/images/scholarships/private.svg";
  }
  return DEFAULT_HERO;
}
