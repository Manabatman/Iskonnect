/**
 * Deterministic gradient classes for scholarship card headers (no image URLs from API).
 * Combine with: className={`bg-gradient-to-br ${getCardVisualClasses(...)}`}
 */
export function getCardVisualClasses(
  providerType?: string | null,
  scholarshipType?: string | null,
  provider?: string | null
): string {
  const haystack = `${providerType ?? ""} ${scholarshipType ?? ""} ${provider ?? ""}`.toLowerCase();

  if (
    haystack.includes("stem") ||
    haystack.includes("engineering") ||
    haystack.includes("science") ||
    haystack.includes("technology")
  ) {
    return "from-teal-600 via-cyan-600 to-emerald-800";
  }
  if (haystack.includes("merit")) {
    return "from-emerald-600 via-green-600 to-teal-800";
  }
  if (
    haystack.includes("need") ||
    haystack.includes("equity") ||
    haystack.includes("financial aid") ||
    haystack.includes("underprivileged")
  ) {
    return "from-amber-600 via-orange-500 to-rose-700";
  }
  if (haystack.includes("private")) {
    return "from-violet-600 via-purple-600 to-indigo-800";
  }
  if (
    haystack.includes("government") ||
    haystack.includes("ched") ||
    haystack.includes("dost") ||
    haystack.includes("lgu") ||
    haystack.includes("tesda")
  ) {
    return "from-primary-600 via-blue-600 to-slate-900";
  }
  return "from-slate-600 via-slate-700 to-slate-900";
}
