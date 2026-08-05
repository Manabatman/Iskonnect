import type { FreshnessChip, MatchResult } from "../types";
import {
  humanizeVerificationSource,
  resolveApplicationStatus,
} from "../utils/scholarshipStatus";

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
  application_status?: string | null;
  data_status?: string | null;
  is_active?: boolean | null;
  link_status?: string | null;
  last_verified_at?: string | null;
  verification_source?: string | null;
  freshness_chips?: FreshnessChip[];
}): FreshnessChip[] {
  const appStatus = resolveApplicationStatus(sch);
  if (sch.freshness_chips?.length) {
    if (appStatus === "needs_verification") {
      return sch.freshness_chips.filter(
        (chip) =>
          !/verified|verification source|official source/i.test(chip.label) &&
          chip.label !== "Not yet verified",
      );
    }
    return sch.freshness_chips;
  }
  const chips: FreshnessChip[] = [];

  if (appStatus === "needs_verification") {
    chips.push({ label: "Needs verification", tone: "warning" });
  } else {
    const verified = formatVerifiedDate(sch.last_verified_at);
    if (verified) {
      chips.push({ label: `Last verified ${verified}`, tone: "success" });
    } else {
      chips.push({ label: "Not yet verified", tone: "warning" });
    }

    const source = humanizeVerificationSource(sch.verification_source);
    if (source) {
      chips.push({ label: source, tone: "neutral" });
    }
  }
  if ((sch.link_status || "").toLowerCase() === "broken") {
    chips.push({ label: "Link issue", tone: "danger" });
  }
  return chips;
}

export function freshnessFromMatch(match: MatchResult): FreshnessChip[] {
  if (match.freshness_chips?.length) return match.freshness_chips;
  return freshnessFromScholarship(match);
}
