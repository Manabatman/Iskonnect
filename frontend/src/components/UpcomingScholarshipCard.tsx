import type { UpcomingScholarship } from "../types";

function formatDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  } catch {
    return iso;
  }
}

function formatMonthYear(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", { month: "long", year: "numeric" });
  } catch {
    return iso;
  }
}

interface UpcomingScholarshipCardProps {
  scholarship: UpcomingScholarship;
}

export function UpcomingScholarshipCard({ scholarship }: UpcomingScholarshipCardProps) {
  const link = scholarship.link && scholarship.link.trim() ? scholarship.link : "#";
  const hasLink = !!link && link.startsWith("http");

  return (
    <article
      className="flex flex-col rounded-xl border border-slate-200 bg-white p-5 shadow-md transition hover:-translate-y-0.5 hover:shadow-lg dark:border-slate-700 dark:bg-slate-800"
      aria-labelledby={`upcoming-title-${scholarship.id}`}
    >
      <div className="flex flex-1 flex-col">
        <h3
          id={`upcoming-title-${scholarship.id}`}
          className="text-lg font-semibold text-slate-900 dark:text-slate-100"
        >
          {scholarship.title}
        </h3>
        {scholarship.provider && (
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{scholarship.provider}</p>
        )}

        <div className="mt-4 flex flex-col gap-2">
          {scholarship.last_open_date && (
            <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
              <svg
                className="h-4 w-4 flex-shrink-0 text-slate-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <span>Last opened: {formatDate(scholarship.last_open_date)}</span>
            </div>
          )}
          {scholarship.predicted_next_open && (
            <div className="rounded-lg bg-blue-50 dark:bg-blue-900/30 px-3 py-2">
              <p className="text-sm font-medium text-blue-800 dark:text-blue-300">
                Expected to reopen: ~{formatMonthYear(scholarship.predicted_next_open)}
              </p>
            </div>
          )}
        </div>

        {scholarship.description && (
          <p className="mt-3 line-clamp-3 text-sm text-slate-600 dark:text-slate-400">
            {scholarship.description}
          </p>
        )}

        <div className="mt-4 flex flex-wrap gap-2">
          {scholarship.benefit_tuition && (
            <span className="rounded bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800 dark:bg-green-900 dark:text-green-300">
              Tuition
            </span>
          )}
          {scholarship.benefit_total_value != null && scholarship.benefit_total_value > 0 && (
            <span className="rounded bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-700 dark:bg-slate-600 dark:text-slate-300">
              Up to PHP {(scholarship.benefit_total_value / 1000).toFixed(0)}k
            </span>
          )}
        </div>

        {hasLink && (
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center text-sm font-medium text-primary-600 transition hover:text-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:text-primary-400 dark:hover:text-primary-300"
          >
            View Details
            <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
              />
            </svg>
          </a>
        )}
      </div>
    </article>
  );
}
