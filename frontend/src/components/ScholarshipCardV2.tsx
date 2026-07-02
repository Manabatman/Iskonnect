import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import type { MatchResult, ScholarshipInfo } from "../types";
import { BookmarkButton } from "./BookmarkButton";
import { LifecycleStatusBadge } from "./LifecycleStatusBadge";
import {
  EligibilityRequirementsList,
  QualificationStatusBadge,
  VerificationBadge,
} from "./QualificationStatusBadge";
import { MatchScoreRing } from "./MatchScoreRing";
import { ScholarshipTypeInfoModal } from "./ScholarshipTypeInfoModal";
import { getCardVisualClasses } from "../utils/cardImages";
import { getScholarshipHeroImageUrl } from "../utils/scholarshipHeroImage";
import { formatScholarshipLocation } from "../utils/normalizeLocation";
import { resolveApplicationStatus } from "../utils/scholarshipStatus";

function isMatchResult(s: ScholarshipInfo | MatchResult): s is MatchResult {
  return "score" in s && typeof (s as MatchResult).score === "number";
}

function asScholarshipInfo(s: ScholarshipInfo | MatchResult): ScholarshipInfo {
  return s as ScholarshipInfo;
}

function getEffectiveMatch(
  scholarship: ScholarshipInfo | MatchResult,
  matchOverlay?: MatchResult | null
): MatchResult | null {
  if (isMatchResult(scholarship)) return scholarship;
  return matchOverlay ?? null;
}

function canOpenMatchAnalysis(match: MatchResult): boolean {
  return !!(
    match.breakdown ||
    (match.explanation && match.explanation.length > 0) ||
    (match.suggestions && match.suggestions.length > 0) ||
    (match.why_not_higher && match.why_not_higher.length > 0)
  );
}

function formatVerifiedCompact(iso: string | null | undefined): string | null {
  if (!iso?.trim()) return null;
  try {
    const d = new Date(iso.slice(0, 10));
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  } catch {
    return null;
  }
}

function formatDeadlineLine(
  deadline: string | null | undefined,
  openDate: string | null | undefined
): string {
  if (deadline?.trim()) {
    const d = new Date(deadline.slice(0, 10));
    return `Deadline: ${d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}`;
  }
  if (openDate?.trim()) {
    const d = new Date(openDate.slice(0, 10));
    return `Opens: ${d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}`;
  }
  return "No deadline listed";
}

function IconBuilding({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
      />
    </svg>
  );
}

function IconMapPin({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
      />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

export interface ScholarshipCardV2Props {
  scholarship: ScholarshipInfo | MatchResult;
  matchOverlay?: MatchResult | null;
  onShowAnalysis?: (match: MatchResult) => void;
  onCheckMatch?: (scholarshipId: number) => void;
  checkMatchLoading?: boolean;
  onCardBodyClick?: (scholarship: ScholarshipInfo) => void;
  className?: string;
}

export function ScholarshipCardV2({
  scholarship,
  matchOverlay,
  onShowAnalysis,
  onCheckMatch,
  checkMatchLoading = false,
  onCardBodyClick,
  className = "",
}: ScholarshipCardV2Props) {
  const [heroImageFailed, setHeroImageFailed] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [typeModalOpen, setTypeModalOpen] = useState(false);
  const base = scholarship;
  const match = getEffectiveMatch(scholarship, matchOverlay);
  const info = asScholarshipInfo(scholarship);

  const link = base.link && base.link.trim() ? base.link : "#";
  const hasLink = !!link && link.startsWith("http");

  const score = match != null ? (match.final_score ?? match.score) : null;
  const visualClass = getCardVisualClasses(base.provider_type, base.scholarship_type, base.provider);
  const dbImageUrl = info.image_url?.trim() || null;
  const categorySvgUrl = dbImageUrl ? null : getScholarshipHeroImageUrl(base.provider, base.provider_type);
  const displayImageUrl = heroImageFailed ? null : dbImageUrl || categorySvgUrl;
  const hasRealImage = Boolean(dbImageUrl && !heroImageFailed);

  useEffect(() => {
    setHeroImageFailed(false);
    setImageLoaded(false);
  }, [dbImageUrl]);

  const locationLabel = formatScholarshipLocation(base.regions, base.provider);
  const appStatus = resolveApplicationStatus({
    application_status: "application_status" in base ? base.application_status : undefined,
    data_status: "data_status" in base ? base.data_status : undefined,
    is_active: "is_active" in base ? base.is_active : undefined,
  });
  const deadlineLine = formatDeadlineLine(
    match?.application_deadline ?? base.application_deadline,
    match?.application_open_date ?? base.application_open_date
  );
  const lastVerified = formatVerifiedCompact(
    "last_verified_at" in base ? base.last_verified_at : undefined
  );
  const predictedOpen =
    match?.predicted_open ??
    ("predicted_next_open" in base ? base.predicted_next_open : undefined);

  const hasBenefits =
    base.benefit_tuition ||
    (base.benefit_allowance_monthly != null && base.benefit_allowance_monthly > 0) ||
    base.benefit_books ||
    (base.benefit_total_value != null && base.benefit_total_value > 0);

  const showSecondaryActionsRow =
    (match && canOpenMatchAnalysis(match) && onShowAnalysis) || (!match && onCheckMatch);

  const handleCardActivate = () => {
    onCardBodyClick?.(info);
  };

  const cardInteractive = !!onCardBodyClick;

  return (
    <>
      <article
        className={`group flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-md transition-all duration-200 hover:-translate-y-1 hover:shadow-xl dark:border-slate-700 dark:bg-slate-800 dark:shadow-slate-900/40 ${cardInteractive ? "cursor-pointer" : ""} ${className}`}
        aria-labelledby={`scholarship-card-title-${base.id}`}
        role={cardInteractive ? "button" : undefined}
        tabIndex={cardInteractive ? 0 : undefined}
        onClick={cardInteractive ? handleCardActivate : undefined}
        onKeyDown={
          cardInteractive
            ? (e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  handleCardActivate();
                }
              }
            : undefined
        }
      >
        <div className="relative aspect-video w-full shrink-0 overflow-hidden rounded-t-2xl">
          {displayImageUrl ? (
            <>
              {!imageLoaded ? (
                <div className="absolute inset-0 animate-pulse bg-gradient-to-br from-slate-600 to-slate-800" aria-hidden />
              ) : null}
              <img
                src={displayImageUrl}
                alt={info.image_alt?.trim() || base.title}
                loading="lazy"
                decoding="async"
                className={[
                  "absolute inset-0 h-full w-full object-cover transition-all duration-300 group-hover:scale-[1.02]",
                  imageLoaded ? "opacity-100" : "opacity-0",
                ].join(" ")}
                onLoad={() => setImageLoaded(true)}
                onError={() => setHeroImageFailed(true)}
              />
            </>
          ) : null}
          <div
            className={[
              "absolute inset-0 bg-gradient-to-br",
              visualClass,
              displayImageUrl && imageLoaded ? (hasRealImage ? "opacity-40" : "opacity-75") : "",
            ].join(" ")}
            aria-hidden
          />
          <div
            className="pointer-events-none absolute inset-0 opacity-[0.15]"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }}
            aria-hidden
          />

          <div
            className="absolute left-3 top-3 z-10 flex items-center gap-2 [&_button]:text-white [&_button:hover]:bg-white/15"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="rounded-lg bg-black/25 p-0.5 backdrop-blur-sm">
              <BookmarkButton scholarshipId={base.id} />
            </div>
          </div>

          {score != null ? (
            <div
              className="absolute right-3 top-3 z-10 rounded-2xl bg-black/30 px-2 py-2 backdrop-blur-md"
              onClick={(e) => e.stopPropagation()}
            >
              <MatchScoreRing score={score} size={64} variant="onDark" showMatchLabel />
            </div>
          ) : null}
        </div>

        <div className="flex flex-1 flex-col px-5 pt-4">
          <div className="flex flex-wrap items-center gap-2">
            <LifecycleStatusBadge
              application_status={"application_status" in base ? base.application_status : undefined}
              data_status={"data_status" in base ? base.data_status : undefined}
              is_active={"is_active" in base ? base.is_active : undefined}
            />
            {base.scholarship_type ? (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setTypeModalOpen(true);
                }}
                className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700 underline decoration-dotted underline-offset-2 transition hover:bg-slate-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600"
                aria-label={`What does ${base.scholarship_type} mean?`}
              >
                {base.scholarship_type}
              </button>
            ) : null}
            {"verification_badge_label" in base && base.verification_badge_label ? (
              <VerificationBadge badge={base.verification_badge} label={base.verification_badge_label} />
            ) : null}
          </div>

          <h3
            id={`scholarship-card-title-${base.id}`}
            className="mt-2 line-clamp-2 text-lg font-bold leading-snug text-slate-900 dark:text-slate-50"
          >
            {base.title}
          </h3>

          {match?.qualification_status ? (
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <QualificationStatusBadge status={match.qualification_status} className="text-xs" />
              {match.eligibility_confidence ? (
                <span className="text-[11px] text-slate-500 dark:text-slate-400">
                  {String(match.eligibility_confidence).replace(/_/g, " ")}
                </span>
              ) : null}
            </div>
          ) : null}

          <p className="mt-1 text-sm font-semibold text-slate-800 dark:text-slate-200">{deadlineLine}</p>

          <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-600 dark:text-slate-400">
            <span className="inline-flex min-w-0 items-center gap-1.5">
              <IconBuilding className="h-4 w-4 shrink-0 opacity-80" />
              <span className="truncate">{base.provider ?? "—"}</span>
            </span>
            {lastVerified ? (
              <span className="text-xs text-slate-500 dark:text-slate-400">Verified {lastVerified}</span>
            ) : appStatus !== "needs_verification" ? (
              <span className="text-xs text-amber-700 dark:text-amber-300">Not yet verified</span>
            ) : null}
          </div>

          {match ? (
            <EligibilityRequirementsList
              qualifying={match.qualifying_requirements}
              missing={match.missing_requirements}
              compact
            />
          ) : null}

          {match?.gap_reason ? (
            <p className="mt-2 text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              <span className="font-medium text-slate-800 dark:text-slate-200">Why this status: </span>
              {match.gap_reason}
            </p>
          ) : null}

          {match?.next_action ? (
            <p className="mt-1 text-xs font-medium text-primary-700 dark:text-primary-300">{match.next_action}</p>
          ) : null}

          {appStatus === "expected_reopen" && predictedOpen ? (
            <p className="mt-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-relaxed text-amber-900 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-100">
              Likely to reopen around{" "}
              {new Date(predictedOpen.slice(0, 10)).toLocaleDateString(undefined, {
                month: "long",
                year: "numeric",
              })}
              . Dates are estimates—confirm on the official site.
            </p>
          ) : null}

          {match?.deadline_passed ? (
            <p className="mt-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs leading-relaxed text-rose-900 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-100">
              You satisfy the eligibility requirements but the application deadline has already passed.
            </p>
          ) : null}

          <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
            {base.description || "No description available."}
          </p>

          <div className="mt-3 rounded-xl border border-primary-200 bg-primary-50 p-3 dark:border-slate-600 dark:bg-slate-800/80">
            <p className="text-[10px] font-bold uppercase tracking-wider text-primary-800 dark:text-primary-300">
              Max value
            </p>
            {base.benefit_total_value != null && base.benefit_total_value > 0 ? (
              <p className="mt-1 text-lg font-extrabold text-primary-900 dark:text-white">
                ₱{base.benefit_total_value.toLocaleString()}/yr
              </p>
            ) : (
              <p className="mt-1 text-sm font-semibold text-slate-600 dark:text-slate-300">See official site</p>
            )}
            {hasBenefits ? (
              <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-slate-600 dark:text-slate-300">
                {base.benefit_tuition ? <span>Tuition</span> : null}
                {base.benefit_allowance_monthly != null && base.benefit_allowance_monthly > 0 ? (
                  <span>Stipend ₱{base.benefit_allowance_monthly.toLocaleString()}/mo</span>
                ) : null}
                {base.benefit_books ? <span>Books</span> : null}
              </div>
            ) : null}
          </div>

          <div className="mt-3 flex flex-wrap items-start gap-3 text-xs text-slate-600 dark:text-slate-400">
            <span className="inline-flex items-center gap-1">
              <IconMapPin className="h-3.5 w-3.5 shrink-0 text-slate-400" />
              <span>{locationLabel}</span>
            </span>
            {(base.min_age != null || base.max_age != null) && (
              <span className="text-slate-500 dark:text-slate-400">
                Age {base.min_age != null ? `Min ${base.min_age}` : ""}
                {base.min_age != null && base.max_age != null ? " · " : ""}
                {base.max_age != null ? `Max ${base.max_age}` : ""}
              </span>
            )}
          </div>
        </div>

        <div className="mt-auto border-t border-slate-200 px-5 py-4 dark:border-slate-700" onClick={(e) => e.stopPropagation()}>
          {showSecondaryActionsRow ? (
            <div className="flex flex-wrap items-center gap-2">
              {match && canOpenMatchAnalysis(match) && onShowAnalysis ? (
                <button
                  type="button"
                  onClick={() => onShowAnalysis(match)}
                  className="text-sm font-semibold text-primary-600 underline-offset-2 hover:text-primary-700 hover:underline dark:text-primary-400 dark:hover:text-primary-300"
                >
                  See why you matched
                </button>
              ) : null}
              {!match && onCheckMatch ? (
                <button
                  type="button"
                  disabled={checkMatchLoading}
                  onClick={() => onCheckMatch(base.id)}
                  className="inline-flex items-center gap-2 text-sm font-semibold text-accent-600 underline-offset-2 transition hover:text-accent-700 hover:underline disabled:cursor-wait disabled:opacity-70 dark:text-accent-400 dark:hover:text-accent-300"
                >
                  {checkMatchLoading ? (
                    <>
                      <span
                        className="h-3.5 w-3.5 shrink-0 animate-spin rounded-full border-2 border-accent-400 border-t-transparent"
                        aria-hidden
                      />
                      <span>Checking…</span>
                    </>
                  ) : (
                    "Check my match"
                  )}
                </button>
              ) : null}
            </div>
          ) : null}

          <div className={`flex flex-col gap-2 sm:flex-row sm:flex-wrap ${showSecondaryActionsRow ? "mt-3" : ""}`}>
            {hasLink && appStatus === "open" && !match?.deadline_passed ? (
              <a
                href={link}
                target="_blank"
                rel="noreferrer"
                className="inline-flex flex-1 items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-center text-sm font-bold text-white shadow-lg shadow-primary-600/20 transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
                aria-label={`Apply now for ${base.title}`}
              >
                Apply Now
              </a>
            ) : appStatus !== "open" || match?.deadline_passed ? (
              <span
                className="inline-flex flex-1 cursor-not-allowed items-center justify-center rounded-xl bg-slate-200 px-4 py-2.5 text-center text-sm font-semibold text-slate-500 dark:bg-slate-600 dark:text-slate-400"
                title={
                  match?.deadline_passed
                    ? "Application deadline has passed"
                    : "Applications are not open for this cycle"
                }
              >
                {appStatus === "expected_reopen" ? "Not open yet" : "Apply when open"}
              </span>
            ) : (
              <span className="inline-flex flex-1 cursor-not-allowed items-center justify-center rounded-xl bg-slate-200 px-4 py-2.5 text-center text-sm font-semibold text-slate-500 dark:bg-slate-600 dark:text-slate-400">
                Link unavailable
              </span>
            )}
            <Link
              to={`/scholarship/${base.id}`}
              className="inline-flex flex-1 items-center justify-center rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-center text-sm font-semibold text-slate-800 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700 dark:focus:ring-offset-slate-900"
              aria-label={`View details for ${base.title}`}
            >
              View Details
            </Link>
            <BookmarkButton scholarshipId={base.id} variant="labeled" className="flex-1 justify-center" />
          </div>
        </div>
      </article>

      <ScholarshipTypeInfoModal
        scholarshipType={base.scholarship_type ?? null}
        open={typeModalOpen}
        onOpenChange={setTypeModalOpen}
      />
    </>
  );
}
