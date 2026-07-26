import { Link } from "react-router-dom";
import type { EliminatedScholarship, MatchDiagnostics } from "../types";

export interface ExcludedScholarshipsPanelProps {
  diagnostics: MatchDiagnostics | null;
  profileId?: string | number | null;
  className?: string;
}

function excludedList(diagnostics: MatchDiagnostics | null): EliminatedScholarship[] {
  if (!diagnostics) return [];
  return diagnostics.eliminated_scholarships ?? diagnostics.hard_exclusions ?? [];
}

export function ExcludedScholarshipsPanel({ diagnostics, profileId, className = "" }: ExcludedScholarshipsPanelProps) {
  const rows = excludedList(diagnostics);
  if (rows.length === 0) return null;

  const checked = diagnostics?.total_checked;
  const passed = diagnostics?.passed_hard_filters;

  return (
    <section
      className={`rounded-xl border border-slate-200 bg-slate-50/80 p-5 dark:border-slate-700 dark:bg-slate-900/40 ${className}`}
      aria-labelledby="excluded-scholarships-heading"
    >
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <h3 id="excluded-scholarships-heading" className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            Scholarships we ruled out
            <span className="ml-2 rounded-full bg-slate-200 px-2 py-0.5 text-sm font-medium text-slate-700 dark:bg-slate-700 dark:text-slate-200">
              {rows.length}
            </span>
          </h3>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            These did not pass hard eligibility checks for your profile. We show them so nothing is hidden.
          </p>
          {checked != null ? (
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              Checked {checked} program{checked === 1 ? "" : "s"}; {passed ?? 0} passed filters before scoring.
            </p>
          ) : null}
        </div>
      </div>

      <ul className="mt-4 divide-y divide-slate-200 dark:divide-slate-700">
        {rows.map((row) => {
          const id = row.scholarship_id;
          const detailHref =
            id != null
              ? profileId
                ? `/scholarship/${id}?profile_id=${profileId}#eligibility`
                : `/scholarship/${id}#eligibility`
              : null;
          return (
            <li key={`${id ?? row.title}-${row.filter}`} className="flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="min-w-0">
                <p className="font-medium text-slate-900 dark:text-slate-100">{row.title ?? "Scholarship"}</p>
                <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-400">
                  {row.reason ?? row.filter ?? "Did not meet eligibility requirements"}
                </p>
              </div>
              {detailHref ? (
                <Link
                  to={detailHref}
                  className="shrink-0 text-sm font-semibold text-primary-600 hover:underline dark:text-primary-400"
                >
                  Why not matched →
                </Link>
              ) : null}
            </li>
          );
        })}
      </ul>

      {diagnostics?.top_blockers && diagnostics.top_blockers.length > 0 ? (
        <div className="mt-4 border-t border-slate-200 pt-4 dark:border-slate-700">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Common blockers in your profile
          </p>
          <ul className="mt-2 list-inside list-disc text-sm text-slate-600 dark:text-slate-300">
            {diagnostics.top_blockers.map((b) => (
              <li key={b}>{b}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
