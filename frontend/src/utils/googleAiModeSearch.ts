/**
 * Builds a Google Search URL that opens in AI Mode (synthesized answer view).
 * Uses udm=50 — Google's AI Mode parameter (may evolve; see docs/architecture.md).
 */
export function buildGoogleAiModeSearchUrl(query: string): string {
  const params = new URLSearchParams({
    q: query,
    udm: "50",
    hl: "en",
    gl: "ph",
  });
  return `https://www.google.com/search?${params.toString()}`;
}
