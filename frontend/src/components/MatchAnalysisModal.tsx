import type { MatchBreakdown, MatchResult, EligibilityExplanation, EligibilityRequirementCheck } from "../types";
import { MatchConfidenceNote } from "./MatchConfidenceNote";
import { MatchScoreRing } from "./MatchScoreRing";
import {
  MatchStatusIcon,
  statusToFactorPercent,
} from "./scholarshipMatchDisplay";
import { UnverifiedRequirementsList } from "./QualificationStatusBadge";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";

function formatBreakdownKey(key: string): string {
  const k = String(key ?? "");
  return k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

const FACTOR_LABELS: Record<string, string> = {
  academic: "Academic (GWA / rank)",
  socioeconomic: "Financial eligibility",
  field_relevance: "Course alignment",
  geographic: "Region match",
  priority_group: "Priority group",
  prior_units: "Prior tertiary units",
  conflict_scope: "Grant exclusivity",
  required_affiliation: "Required affiliation",
  work_experience: "Work experience",
  age_as_of: "Age as of cutoff",
  residency_years: "Local residency",
  entry_path: "Entry path",
  parent_salary_grade: "Parent salary grade",
  marital_status: "Marital status",
};

const APPLICATION_WINDOW_LABELS: Record<string, string> = {
  open: "Applications open",
  closed: "Applications closed",
  rolling: "Rolling admissions",
  not_announced: "Application dates not announced",
  opens_later: "Opens later",
  unconfirmed: "Application status unconfirmed",
};

function modalTitle(explanation: EligibilityExplanation | null | undefined): string {
  if (!explanation) return "Why did I match?";
  if (explanation.status === "eligible_now") return "Why did I match?";
  return "Your eligibility";
}

function statusChipClass(status: string): string {
  if (status === "eligible_now") {
    return "border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-100";
  }
  if (status === "currently_not_eligible") {
    return "border-slate-300 bg-slate-100 text-slate-800 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200";
  }
  return "border-amber-200 bg-amber-50 text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100";
}

function RequirementRow({ req }: { req: EligibilityRequirementCheck }) {
  const result = (req.result ?? "").toLowerCase();
  const iconStatus = result === "met" ? "met" : result === "unmet" ? "not_met" : "partial";
  return (
    <li className="rounded-xl border border-slate-200 bg-slate-50/80 p-3 dark:border-slate-700 dark:bg-slate-800/50">
      <div className="flex items-start gap-3">
        <span className="mt-0.5 shrink-0 text-lg" aria-hidden>
          <MatchStatusIcon status={iconStatus} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">{req.label}</p>
          {req.evidence ? (
            <p className="mt-1 text-xs leading-relaxed text-slate-600 dark:text-slate-400">{req.evidence}</p>
          ) : null}
          {req.blocker_explanation ? (
            <p className="mt-2 text-xs leading-relaxed text-slate-700 dark:text-slate-300">{req.blocker_explanation}</p>
          ) : null}
          {req.change_hint ? (
            <p className="mt-2 text-xs leading-relaxed text-primary-800 dark:text-primary-200">{req.change_hint}</p>
          ) : null}
        </div>
      </div>
    </li>
  );
}

function EligibilityExplanationPanel({ explanation }: { explanation: EligibilityExplanation }) {
  const met = explanation.requirements.filter((r) => (r.result ?? "").toLowerCase() === "met");
  const unmet = explanation.requirements.filter((r) => (r.result ?? "").toLowerCase() === "unmet");
  const unknown = explanation.requirements.filter((r) => (r.result ?? "").toLowerCase() === "unknown");
  const windowLabel =
    APPLICATION_WINDOW_LABELS[explanation.application_window] ?? explanation.application_window;

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <span
          className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${statusChipClass(explanation.status)}`}
        >
          {explanation.status_label}
        </span>
        <p className="text-base font-medium leading-relaxed text-slate-900 dark:text-slate-100">
          {explanation.summary}
        </p>
        {explanation.reason ? (
          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">{explanation.reason}</p>
        ) : null}
        <p className="text-sm text-slate-600 dark:text-slate-400">
          <span className="font-medium text-slate-800 dark:text-slate-200">{windowLabel}</span>
        </p>
        {explanation.next_action ? (
          <p className="text-sm font-medium text-primary-800 dark:text-primary-200">{explanation.next_action}</p>
        ) : null}
      </div>

      {explanation.catalog_status &&
      explanation.catalog_status !== "included_in_recommendations" &&
      explanation.catalog_message ? (
        <div className="rounded-xl border border-slate-200 bg-slate-50/80 p-4 dark:border-slate-700 dark:bg-slate-800/50">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Availability in Match Results
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            {explanation.catalog_message}
          </p>
        </div>
      ) : null}

      {met.length > 0 ? (
        <div>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Requirements you already meet
          </h3>
          <ul className="space-y-3">
            {met.map((req) => (
              <RequirementRow key={req.key ?? req.label} req={req} />
            ))}
          </ul>
        </div>
      ) : null}

      {unmet.length > 0 ? (
        <div>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Requirements you don&apos;t currently meet
          </h3>
          <ul className="space-y-3">
            {unmet.map((req) => (
              <RequirementRow key={req.key ?? req.label} req={req} />
            ))}
          </ul>
        </div>
      ) : null}

      {unknown.length > 0 ? (
        <div>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Add to your profile to confirm
          </h3>
          <UnverifiedRequirementsList
            unverified={unknown.map((r) => r.label ?? "").filter(Boolean)}
            requirements={unknown}
          />
        </div>
      ) : null}

      <div className="border-t border-slate-200 pt-6 dark:border-slate-700">
        <MatchConfidenceNote className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/50" />
      </div>
    </div>
  );
}

interface MatchAnalysisModalProps {
  match: MatchResult | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Backend explanation object — when set, modal renders this verbatim (no client inference). */
  explanation?: EligibilityExplanation | null;
  explanationLoading?: boolean;
  explanationError?: string | null;
  /** When true, fit score ring is hidden (scholarship not in plan top results). */
  notCalculated?: boolean;
}

function BreakdownList({ breakdown }: { breakdown: MatchBreakdown }) {
  return (
    <ul className="space-y-3">
      {Object.entries(breakdown).map(([key, factor]) => {
        if (!factor || typeof factor !== "object") return null;
        const f = factor as {
          status?: string;
          user_value?: string;
          requirement_value?: string;
          weighted?: number;
          max_possible?: number;
        };
        const label = FACTOR_LABELS[key] ?? formatBreakdownKey(key);
        const status = (f.status ?? "").toLowerCase();
        const width = statusToFactorPercent(f.status);
        const isNA = status === "not_applicable";
        const barClass = isNA
          ? "bg-slate-300 dark:bg-slate-600"
          : "bg-primary-500 dark:bg-primary-400";
        return (
          <li
            key={key}
            className="rounded-xl border border-slate-200 bg-slate-50/80 p-3 dark:border-slate-700 dark:bg-slate-800/50"
          >
            <div className="flex items-start gap-3">
              <span className="mt-0.5 shrink-0 text-lg" aria-hidden>
                <MatchStatusIcon status={status} />
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">{label}</p>
                <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-600">
                  <div className={`h-full rounded-full transition-[width] duration-base ease-out-custom ${barClass}`} style={{ width: `${width}%` }} />
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-600 dark:text-slate-400">
                  <span className="font-medium text-slate-700 dark:text-slate-300">Your profile:</span>{" "}
                  {f.user_value ?? "—"}
                  <span className="mx-1 text-slate-400">·</span>
                  <span className="font-medium text-slate-700 dark:text-slate-300">Required:</span>{" "}
                  {f.requirement_value ?? "—"}
                </p>
                {typeof f.weighted === "number" && typeof f.max_possible === "number" && f.max_possible > 0 ? (
                  <p className="mt-1 text-body-sm text-slate-500 dark:text-slate-400">
                    Contribution: {f.weighted.toFixed(1)} / {f.max_possible.toFixed(1)} pts (this factor)
                  </p>
                ) : null}
                {isNA ? (
                  <p className="mt-1 text-body-sm italic text-slate-500 dark:text-slate-400">
                    Not part of this score — program has no restriction here.
                  </p>
                ) : null}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}

function LegacyMatchAnalysis({ match }: { match: MatchResult }) {
  const score = match.final_score ?? match.score;
  const hasContent =
    Boolean(
      match.breakdown ||
        (match.explanation && match.explanation.length > 0) ||
        (match.suggestions && match.suggestions.length > 0) ||
        (match.why_not_higher && match.why_not_higher.length > 0)
    );

  return (
    <>
      <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-200 bg-gradient-to-b from-primary-50 to-white py-8 dark:border-slate-700 dark:from-primary-950/40 dark:to-slate-900">
        <MatchScoreRing score={score} size={120} />
        <p className="mt-4 text-center text-xs font-bold uppercase tracking-widest text-primary-700 dark:text-primary-300">
          {Math.round(score)}% eligibility fit
        </p>
        {match.scoring_policy_version ? (
          <p className="mt-2 text-center text-body-sm text-slate-500 dark:text-slate-400">
            Scoring policy: {match.scoring_policy_version}
          </p>
        ) : null}
      </div>

      {!hasContent ? (
        <div className="mt-6 space-y-6">
          <p className="text-center text-sm text-slate-600 dark:text-slate-400">
            Detailed eligibility breakdown is not available for this scholarship yet.
          </p>
          <div className="border-t border-slate-200 pt-6 dark:border-slate-700">
            <MatchConfidenceNote className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/50" />
          </div>
        </div>
      ) : (
        <div className="mt-6 space-y-6">
          <UnverifiedRequirementsList
            unverified={match.unverified_requirements}
            requirements={match.requirements as Array<{ key?: string; result?: string; label?: string }> | undefined}
            provisionalReason={match.provisional_reason}
          />

          {match.breakdown ? (
            <div>
              <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Eligibility checklist
              </h3>
              <BreakdownList breakdown={match.breakdown} />
            </div>
          ) : null}

          {match.explanation && match.explanation.length > 0 ? (
            <div>
              <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Why you matched
              </h3>
              <ul className="space-y-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                {match.explanation.map((line, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary-500" aria-hidden />
                    <span>{line}</span>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {match.why_not_higher && match.why_not_higher.length > 0 ? (
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-800/40">
              <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-400">
                Why not higher
              </h3>
              <ul className="space-y-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                {match.why_not_higher.map((line, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-slate-400" aria-hidden />
                    <span>{line}</span>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {match.suggestions && match.suggestions.length > 0 ? (
            <div className="rounded-xl border border-primary-200 bg-primary-50/90 p-4 dark:border-primary-800 dark:bg-primary-950/40">
              <h3 className="text-xs font-semibold uppercase tracking-wide text-primary-800 dark:text-primary-200">
                Tips to improve
              </h3>
              <ul className="mt-2 space-y-1.5 text-sm text-primary-900 dark:text-primary-100">
                {match.suggestions.map((s, i) => (
                  <li key={i} className="flex gap-2">
                    <span aria-hidden>•</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          <div className="border-t border-slate-200 pt-6 dark:border-slate-700">
            <MatchConfidenceNote className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/50" />
          </div>
        </div>
      )}
    </>
  );
}

export function MatchAnalysisModal({
  match,
  open,
  onOpenChange,
  explanation = null,
  explanationLoading = false,
  explanationError = null,
  notCalculated = false,
}: MatchAnalysisModalProps) {
  const score = match != null ? (match.final_score ?? match.score) : 0;
  const showExplanation = Boolean(explanation);
  const title = modalTitle(explanation);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        hideCloseButton
        aria-describedby={match ? "match-analysis-desc" : undefined}
        className="fixed inset-0 z-[101] flex max-h-full w-full max-w-none translate-x-0 translate-y-0 flex-col gap-0 overflow-hidden border-0 p-0 shadow-2xl sm:inset-auto sm:left-[50%] sm:top-[50%] sm:max-h-[90vh] sm:max-w-lg sm:translate-x-[-50%] sm:translate-y-[-50%] sm:rounded-2xl sm:border sm:border-slate-200 sm:dark:border-slate-700"
      >
        <div className="flex h-full max-h-full min-h-0 w-full flex-col overflow-hidden bg-white dark:bg-slate-900">
          <div className="flex items-start justify-between gap-3 border-b border-slate-200 px-5 py-4 dark:border-slate-700">
            <div className="min-w-0">
              <DialogTitle className="text-lg font-bold text-slate-900 dark:text-slate-100">{title}</DialogTitle>
              {match ? (
                <DialogDescription id="match-analysis-desc" className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  How your profile lines up with{" "}
                  <span className="font-medium text-slate-800 dark:text-slate-200">{match.title}</span>.
                </DialogDescription>
              ) : (
                <DialogDescription className="sr-only">Match analysis</DialogDescription>
              )}
            </div>
            <DialogClose
              type="button"
              className="focus-visible-ring flex min-h-11 min-w-11 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
              aria-label="Close"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </DialogClose>
          </div>

          <div className="flex-1 overflow-y-auto px-5 py-5">
            {!match ? (
              <p className="text-sm text-slate-600 dark:text-slate-400">No match data to show.</p>
            ) : explanationLoading ? (
              <p className="text-sm text-slate-600 dark:text-slate-400">Loading eligibility details…</p>
            ) : explanationError ? (
              <p className="text-sm text-red-700 dark:text-red-300">{explanationError}</p>
            ) : showExplanation && explanation ? (
              <div className="space-y-6">
                {!notCalculated ? (
                  <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-200 bg-gradient-to-b from-primary-50 to-white py-6 dark:border-slate-700 dark:from-primary-950/40 dark:to-slate-900">
                    <MatchScoreRing score={score} size={96} />
                    <p className="mt-3 text-center text-xs font-bold uppercase tracking-widest text-primary-700 dark:text-primary-300">
                      {Math.round(score)}% eligibility fit
                    </p>
                  </div>
                ) : (
                  <p className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800/50 dark:text-slate-400">
                    Fit score not available — see eligibility below.
                  </p>
                )}
                <EligibilityExplanationPanel explanation={explanation} />
                {!notCalculated && match.breakdown ? (
                  <div className="border-t border-slate-200 pt-6 dark:border-slate-700">
                    <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                      Match score breakdown
                    </h3>
                    <BreakdownList breakdown={match.breakdown} />
                  </div>
                ) : null}
              </div>
            ) : (
              <LegacyMatchAnalysis match={match} />
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
