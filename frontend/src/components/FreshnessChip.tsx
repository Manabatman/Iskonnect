import type { FreshnessChip, MatchResult } from "../types";

const TONE_CLASSES: Record<string, string> = {
  success: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200",
  warning: "bg-amber-100 text-amber-900 dark:bg-amber-900/50 dark:text-amber-200",
  danger: "bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-200",
  neutral: "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200",
};

function formatVerifiedDate(iso: string | null | undefined): string | null {
  if (!iso?.trim()) return null;
  try {
    const d = new Date(iso.slice(0, 10));
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  } catch {
    return null;
  }
}

export function FreshnessChipBadge({ chip }: { chip: FreshnessChip }) {
  const tone = chip.tone || "neutral";
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium ${TONE_CLASSES[tone] ?? TONE_CLASSES.neutral}`}
    >
      {chip.label}
    </span>
  );
}

export function FreshnessChipRow({ chips }: { chips?: FreshnessChip[] }) {
  if (!chips?.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5" aria-label="Data freshness">
      {chips.map((chip) => (
        <FreshnessChipBadge key={`${chip.label}-${chip.tone}`} chip={chip} />
      ))}
    </div>
  );
}

export function freshnessFromScholarship(sch: {
  data_status?: string | null;
  last_verified_at?: string | null;
  verification_source?: string | null;
  freshness_chips?: FreshnessChip[];
}): FreshnessChip[] {
  if (sch.freshness_chips?.length) return sch.freshness_chips;
  const chips: FreshnessChip[] = [];
  if (sch.data_status === "needs_review") chips.push({ label: "Needs verification", tone: "warning" });
  if (sch.data_status === "expired" || sch.data_status === "past_deadline") {
    chips.push({ label: "Closed cycle", tone: "neutral" });
  }
  const verified = formatVerifiedDate(sch.last_verified_at);
  if (verified) chips.push({ label: `Last verified ${verified}`, tone: "success" });
  else chips.push({ label: "Not yet verified", tone: "warning" });
  if (sch.verification_source) {
    chips.push({ label: `Source: ${sch.verification_source.slice(0, 32)}`, tone: "neutral" });
  }
  return chips;
}

export function freshnessFromMatch(match: MatchResult): FreshnessChip[] {
  if (match.freshness_chips?.length) return match.freshness_chips;
  return freshnessFromScholarship(match);
}
