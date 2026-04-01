import { Link } from "react-router-dom";
import type { MatchResult } from "../types";
import { BookmarkButton } from "./BookmarkButton";
import { MatchScoreRing } from "./MatchScoreRing";
import {
  getUrgencyBadgeClasses,
  getUrgencyLevel,
  providerInitials,
  WhyYouMatchedSection,
} from "./scholarshipMatchDisplay";

interface ScholarshipCardProps {
  match: MatchResult;
}

export function ScholarshipCard({ match }: ScholarshipCardProps) {
  const score = match.final_score ?? match.score;
  const link = match.link && match.link.trim() ? match.link : "#";
  const hasLink = !!link && link.startsWith("http");
  const regions = (match.regions ?? []).map((r) => r.trim()).filter(Boolean);
  const urgency = getUrgencyLevel(match.application_deadline, match.application_open_date);
  const urgencyBadgeClasses = getUrgencyBadgeClasses(urgency.level);

  const likelihood =
    match.confidence === "high"
      ? "High likelihood"
      : match.confidence === "medium"
        ? "Moderate likelihood"
        : match.confidence === "low"
          ? "Lower likelihood"
          : null;

  return (
    <article
      className="glass flex flex-col rounded-2xl p-5 shadow-md transition hover:-translate-y-0.5 hover:shadow-xl dark:shadow-slate-900/40"
      aria-labelledby={`scholarship-title-${match.id}`}
    >
      <div className="flex flex-1 flex-col">
        <div className="flex items-start gap-3">
          <div
            className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 text-sm font-bold text-white shadow-inner"
            aria-hidden
          >
            {providerInitials(match.provider)}
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h3
                id={`scholarship-title-${match.id}`}
                className="text-lg font-semibold text-slate-900 dark:text-slate-100"
              >
                {match.title}
              </h3>
              {match.provider_type && (
                <span className="rounded bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs font-medium text-slate-600 dark:text-slate-400">
                  {match.provider_type}
                </span>
              )}
              {match.scholarship_type && (
                <span className="rounded bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs font-medium text-slate-600 dark:text-slate-400">
                  {match.scholarship_type}
                </span>
              )}
              {match.verification_source ? (
                <span
                  className="rounded bg-emerald-100 dark:bg-emerald-900/50 px-2 py-0.5 text-xs font-medium text-emerald-800 dark:text-emerald-300"
                  title={`Source: ${match.verification_source}`}
                >
                  Verified data
                </span>
              ) : null}
              {match.data_status === "expired" ? (
                <span className="rounded bg-red-100 dark:bg-red-900/50 px-2 py-0.5 text-xs font-medium text-red-800 dark:text-red-300">
                  Expired
                </span>
              ) : null}
              {match.link_status === "broken" ? (
                <span className="rounded bg-amber-100 dark:bg-amber-900/50 px-2 py-0.5 text-xs font-medium text-amber-900 dark:text-amber-200">
                  Broken link
                </span>
              ) : null}
            </div>
            <p className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">{match.provider ?? "—"}</p>
            {likelihood ? (
              <p className="mt-1 text-xs font-medium text-primary-700 dark:text-primary-300">{likelihood}</p>
            ) : null}
          </div>
          <div className="flex shrink-0 flex-col items-end gap-2">
            <BookmarkButton scholarshipId={match.id} />
            <MatchScoreRing score={score} size={64} />
            <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${urgencyBadgeClasses}`}>
              {urgency.label}
            </span>
          </div>
        </div>

        <p className="mt-3 line-clamp-3 text-sm text-slate-700 dark:text-slate-300">
          {match.description || "No description available."}
        </p>

        {(match.benefit_tuition || match.benefit_allowance_monthly || match.benefit_books || match.benefit_total_value) && (
          <div className="mt-2 flex flex-wrap gap-2 text-xs text-slate-600 dark:text-slate-400">
            {match.benefit_tuition && (
              <span className="flex items-center gap-1" title="Tuition">
                <span aria-hidden>🎓</span> Tuition
              </span>
            )}
            {match.benefit_allowance_monthly != null && match.benefit_allowance_monthly > 0 && (
              <span className="flex items-center gap-1" title="Monthly allowance">
                <span aria-hidden>💰</span> ₱{match.benefit_allowance_monthly.toLocaleString()}/mo
              </span>
            )}
            {match.benefit_books && (
              <span className="flex items-center gap-1" title="Books">
                <span aria-hidden>📚</span> Books
              </span>
            )}
            {match.benefit_total_value != null && match.benefit_total_value > 0 && (
              <span className="font-medium text-primary-700 dark:text-primary-400">
                Up to ₱{match.benefit_total_value.toLocaleString()}/yr
              </span>
            )}
          </div>
        )}

        <div className="mt-3 flex flex-wrap gap-1">
          {regions.length === 0 ? (
            <span className="rounded-full bg-green-100 dark:bg-green-900 px-2 py-0.5 text-xs font-medium text-green-800 dark:text-green-300">
              Nationwide
            </span>
          ) : (
            <>
              {regions.slice(0, 4).map((r) => (
                <span
                  key={r}
                  className="rounded-full bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs text-slate-700 dark:text-slate-300"
                >
                  {r}
                </span>
              ))}
              {regions.length > 4 && (
                <span className="rounded-full bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs text-slate-600 dark:text-slate-400">
                  +{regions.length - 4} more
                </span>
              )}
            </>
          )}
        </div>

        {(match.min_age != null || match.max_age != null) && (
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Age: {match.min_age != null ? `Min ${match.min_age}` : ""}
            {match.min_age != null && match.max_age != null && " • "}
            {match.max_age != null ? `Max ${match.max_age}` : ""}
          </p>
        )}

        <WhyYouMatchedSection match={match} />
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <Link
          to={`/scholarship/${match.id}`}
          className="rounded-xl border border-slate-300 bg-white/80 px-4 py-2.5 text-sm font-semibold text-slate-800 backdrop-blur transition hover:bg-white dark:border-slate-600 dark:bg-slate-800/80 dark:text-slate-200 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          aria-label={`View details for ${match.title}`}
        >
          View details
        </Link>
        {hasLink ? (
          <a
            href={link}
            target="_blank"
            rel="noreferrer"
            className="rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            aria-label={`Apply now for ${match.title}`}
          >
            Apply now
          </a>
        ) : (
          <span className="rounded-lg bg-slate-200 dark:bg-slate-600 px-4 py-2 text-sm font-medium text-slate-500 dark:text-slate-400 cursor-not-allowed">
            Link unavailable
          </span>
        )}
      </div>
    </article>
  );
}
