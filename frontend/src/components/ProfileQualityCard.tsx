import { Link } from "react-router-dom";
import type { ProfileCompleteness } from "../types";

const STEP_SLUG_TO_NUMBER: Record<string, number> = {
  personal: 1,
  education: 2,
  location: 3,
  field: 4,
  goals: 5,
};

function profileLinkToPath(link: string): string {
  if (link.startsWith("/")) return link;
  if (link.startsWith("profile-builder")) {
    const qs = link.includes("?") ? link.slice(link.indexOf("?")) : "";
    const params = new URLSearchParams(qs);
    const step = params.get("step");
    if (step && STEP_SLUG_TO_NUMBER[step]) {
      return `/profile-builder?step=${step}`;
    }
    return "/profile-builder";
  }
  return `/profile-builder`;
}

export interface ProfileQualityCardProps {
  completeness: ProfileCompleteness | null;
  className?: string;
}

export function ProfileQualityCard({ completeness, className = "" }: ProfileQualityCardProps) {
  if (!completeness) return null;

  const percent =
    completeness.quality_percent ??
    (completeness.total_fields > 0
      ? Math.round((completeness.filled_fields / completeness.total_fields) * 100)
      : 0);
  const missing = completeness.missing_fields ?? [];
  const hints = completeness.improvement_hints ?? [];
  const topHint = hints[0];
  const topMissing = missing[0];

  return (
    <div
      className={`rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-800 ${className}`}
      role="status"
    >
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        Improve your matches
      </h3>

      {topHint ? (
        <p className="mt-2 text-base font-medium leading-snug text-slate-900 dark:text-slate-100">{topHint}</p>
      ) : topMissing ? (
        <p className="mt-2 text-base font-medium leading-snug text-slate-900 dark:text-slate-100">
          Adding{" "}
          <Link
            to={profileLinkToPath(topMissing.profile_link)}
            className="text-primary-600 underline hover:text-primary-700 dark:text-primary-400"
          >
            {topMissing.label.toLowerCase()}
          </Link>{" "}
          helps us check more scholarships accurately.
        </p>
      ) : percent >= 80 ? (
        <p className="mt-2 text-base font-medium text-slate-900 dark:text-slate-100">
          Your profile has enough detail for reliable matching on most programs.
        </p>
      ) : (
        <p className="mt-2 text-base font-medium text-slate-900 dark:text-slate-100">
          Complete a few more matching fields to unlock more accurate eligibility checks.
        </p>
      )}

      {completeness.low_data_warning ? (
        <p className="mt-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100">
          With limited profile data, we can only check basic eligibility — many scholarships may be hidden until you add
          more details.
        </p>
      ) : null}

      {hints.length > 1 ? (
        <ul className="mt-4 space-y-1 text-sm text-slate-700 dark:text-slate-300">
          {hints.slice(1, 4).map((hint) => (
            <li key={hint} className="flex gap-2">
              <span className="text-primary-600 dark:text-primary-400" aria-hidden>
                ·
              </span>
              <span>{hint}</span>
            </li>
          ))}
        </ul>
      ) : null}

      {missing.length > 0 ? (
        <div className="mt-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Add these to improve matching
          </p>
          <ul className="mt-2 space-y-1">
            {missing.slice(0, 6).map((field) => (
              <li key={field.key}>
                <Link
                  to={profileLinkToPath(field.profile_link)}
                  className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
                >
                  {field.label}
                </Link>
              </li>
            ))}
          </ul>
          {missing.length > 6 ? (
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">+{missing.length - 6} more fields</p>
          ) : null}
        </div>
      ) : null}

      <div className="mt-4 flex items-center gap-3">
        <div className="h-1.5 min-w-0 flex-1 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
          <div
            className={`h-full rounded-full transition-all ${
              percent >= 80 ? "bg-emerald-500" : percent >= 50 ? "bg-amber-500" : "bg-rose-500"
            }`}
            style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
          />
        </div>
        <span className="shrink-0 text-xs text-slate-500 dark:text-slate-400">{percent}% matching fields</span>
      </div>
    </div>
  );
}
