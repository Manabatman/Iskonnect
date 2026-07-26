import { formatDateShort } from "./formatDate";

const PRECISION_LABELS: Record<string, string> = {
  exact: "exact date",
  estimated: "estimated — confirm on the official site",
  rolling: "rolling admissions",
  institution_dependent: "set by your school — check with your registrar",
};

/**
 * Format a scholarship deadline with precision qualifier — never a bare date alone.
 */
export function formatDeadlineDisplay(
  deadline: string | null | undefined,
  precision?: string | null,
  note?: string | null,
  verifiedAt?: string | null
): string {
  const p = (precision ?? "").trim().toLowerCase();

  if (p === "rolling") {
    return note?.trim() ? `Rolling admissions (${note.trim()})` : "Rolling admissions";
  }

  if (p === "not_announced") {
    return note?.trim() ? `Deadline not announced (${note.trim()})` : "Deadline not announced";
  }

  if (p === "institution_dependent") {
    return note?.trim()
      ? `Deadline set by your school (${note.trim()})`
      : "Deadline set by your school — check with your registrar";
  }

  if (!deadline?.trim()) {
    if (note?.trim()) return `Deadline unlisted (${note.trim()})`;
    return "Deadline not listed";
  }

  const formatted = formatDateShort(deadline);
  const qualifier = PRECISION_LABELS[p] ?? (p ? p.replace(/_/g, " ") : "unverified date");

  let line = `Deadline: ${formatted} (${qualifier})`;
  if (note?.trim()) {
    line += ` — ${note.trim()}`;
  }
  if (verifiedAt?.trim()) {
    try {
      const verified = formatDateShort(verifiedAt);
      line += ` · Verified ${verified}`;
    } catch {
      /* ignore */
    }
  }
  return line;
}

/** Open-date line with the same honesty rules as deadlines. */
export function formatOpenDateDisplay(
  openDate: string | null | undefined,
  precision?: string | null,
  note?: string | null
): string {
  if (!openDate?.trim()) {
    return note?.trim() ? `Opening date unlisted (${note.trim()})` : "Opening date not listed";
  }
  const formatted = formatDateShort(openDate);
  const p = (precision ?? "").trim().toLowerCase();
  if (p === "estimated") {
    return `Opens: ${formatted} (estimated — confirm on the official site)`;
  }
  if (p === "exact") {
    return `Opens: ${formatted} (exact date)`;
  }
  return `Opens: ${formatted} (confirm on official site)`;
}
