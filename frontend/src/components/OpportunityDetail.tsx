import { BookmarkButton } from "./BookmarkButton";
import type { Opportunity } from "../data/mockOpportunities";
import { formatDate } from "../utils/formatDate";

export interface OpportunityDetailProps {
  opportunity: Opportunity | null;
}

export function OpportunityDetail({ opportunity }: OpportunityDetailProps) {
  if (!opportunity) {
    return (
      <div className="flex min-h-[280px] flex-col items-center justify-center px-4 py-12 text-center">
        <div className="mb-4 rounded-full bg-slate-100 p-4 dark:bg-slate-700" aria-hidden>
          <svg className="h-10 w-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
        </div>
        <p className="text-base font-medium text-slate-700 dark:text-slate-200">Select an opportunity</p>
        <p className="mt-1 max-w-sm text-sm text-slate-500 dark:text-slate-400">
          Choose an item from the list on the left to view full details, requirements, and how to apply.
        </p>
      </div>
    );
  }

  const hasLink = opportunity.link && opportunity.link.startsWith("http");

  return (
    <div className="flex min-h-0 flex-col">
      <div className="sticky top-0 z-10 -mx-4 -mt-4 mb-4 border-b border-slate-200 bg-white/95 px-4 pb-4 pt-4 backdrop-blur dark:border-slate-700 dark:bg-slate-800/95">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              {opportunity.isNew ? (
                <span className="rounded-full bg-primary-100 px-2 py-0.5 text-xs font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                  New
                </span>
              ) : null}
              {opportunity.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600 dark:bg-slate-700 dark:text-slate-300"
                >
                  {tag}
                </span>
              ))}
            </div>
            <h2 className="mt-2 text-xl font-bold leading-tight text-slate-900 dark:text-slate-100">
              {opportunity.title}
            </h2>
            <p className="mt-1 text-sm font-medium text-slate-600 dark:text-slate-300">{opportunity.organization}</p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <BookmarkButton scholarshipId={opportunity.id} className="rounded-lg" />
            {hasLink ? (
              <a
                href={opportunity.link}
                target="_blank"
                rel="noreferrer"
                className="rounded-lg bg-primary-600 px-4 py-2.5 text-center text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
              >
                Apply
              </a>
            ) : (
              <span className="rounded-lg bg-slate-200 px-4 py-2.5 text-center text-sm font-medium text-slate-500 dark:bg-slate-600 dark:text-slate-400">
                Link unavailable
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="space-y-6 pb-4">
        <section>
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Description</h3>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">{opportunity.description}</p>
        </section>

        <section className="grid gap-4 sm:grid-cols-2">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Location</h3>
            <p className="mt-1 text-sm text-slate-800 dark:text-slate-200">{opportunity.location}</p>
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Deadline</h3>
            <p className="mt-1 text-sm text-slate-800 dark:text-slate-200">{formatDate(opportunity.deadline)}</p>
          </div>
          {opportunity.stipend ? (
            <div className="sm:col-span-2">
              <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Stipend / value
              </h3>
              <p className="mt-1 text-sm font-medium text-primary-700 dark:text-primary-300">{opportunity.stipend}</p>
            </div>
          ) : null}
        </section>

        <section>
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Requirements</h3>
          <ul className="mt-2 list-inside list-disc space-y-1.5 text-sm text-slate-700 dark:text-slate-300">
            {opportunity.requirements.map((req) => (
              <li key={req}>{req}</li>
            ))}
          </ul>
        </section>

        <div className="border-t border-slate-200 pt-4 dark:border-slate-700">
          {hasLink ? (
            <a
              href={opportunity.link}
              target="_blank"
              rel="noreferrer"
              className="block w-full rounded-lg bg-primary-600 px-4 py-3 text-center text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
            >
              Apply now
            </a>
          ) : (
            <p className="text-center text-sm text-slate-500 dark:text-slate-400">
              No external application link for this listing.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
