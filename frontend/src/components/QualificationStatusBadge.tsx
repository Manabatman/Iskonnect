import type { QualificationStatus } from "../types";

const STATUS_CONFIG: Record<
  QualificationStatus,
  { label: string; className: string }
> = {
  qualified: {
    label: "Qualified",
    className:
      "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200",
  },
  provisionally_qualified: {
    label: "Provisionally qualified",
    className:
      "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-200",
  },
  almost_qualified: {
    label: "Almost qualified",
    className:
      "bg-sky-100 text-sky-900 dark:bg-sky-900/40 dark:text-sky-200",
  },
  not_eligible: {
    label: "Not eligible",
    className: "bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-200",
  },
};

export function QualificationStatusBadge({
  status,
  className = "",
}: {
  status?: QualificationStatus | string | null;
  className?: string;
}) {
  if (!status) return null;
  const key = status as QualificationStatus;
  const cfg = STATUS_CONFIG[key];
  if (!cfg) return null;
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-semibold ${cfg.className} ${className}`}
    >
      {cfg.label}
    </span>
  );
}

export function VerificationBadge({
  badge,
  label,
}: {
  badge?: string | null;
  label?: string | null;
}) {
  if (!badge && !label) return null;
  const tone =
    badge === "verified"
      ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200"
      : badge === "partially_verified"
        ? "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-200"
        : badge === "imported_unverified"
          ? "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300"
          : "bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300";
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${tone}`}>
      {label ?? badge}
    </span>
  );
}

export function EligibilityRequirementsList({
  qualifying,
  missing,
  compact = false,
}: {
  qualifying?: string[];
  missing?: string[];
  compact?: boolean;
}) {
  const q = qualifying ?? [];
  const m = missing ?? [];
  if (!q.length && !m.length) return null;
  const limit = compact ? 3 : 6;
  return (
    <div className="mt-2 space-y-1 text-xs text-slate-600 dark:text-slate-400">
      {q.slice(0, limit).map((item) => (
        <div key={`q-${item}`} className="text-emerald-700 dark:text-emerald-300">
          ✓ {item}
        </div>
      ))}
      {m.slice(0, limit).map((item) => (
        <div key={`m-${item}`} className="text-amber-800 dark:text-amber-200">
          ✗ {item}
        </div>
      ))}
    </div>
  );
}
