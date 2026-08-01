import type { MatchBreakdown, MatchResult } from "../types";
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
  academic: "Academic (GWA)",
  socioeconomic: "Financial eligibility",
  field_relevance: "Course alignment",
  geographic: "Region match",
  priority_group: "Priority group",
};

interface MatchAnalysisModalProps {
  match: MatchResult | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** When true, the scholarship is not in the student's computed plan (TRUST-05). */
  notCalculated?: boolean;
}

function NotCalculatedPanel({ title }: { title: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-6 text-center dark:border-slate-700 dark:bg-slate-800/50">
      <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">Not calculated yet</p>
      <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
        We have not scored <span className="font-medium text-slate-800 dark:text-slate-200">{title}</span> against
        your profile. Run a full match from your dashboard or complete your profile for personalized results.
      </p>
    </div>
  );
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
                  <div className={`h-full rounded-full transition-all ${barClass}`} style={{ width: `${width}%` }} />
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-600 dark:text-slate-400">
                  <span className="font-medium text-slate-700 dark:text-slate-300">Your profile:</span>{" "}
                  {f.user_value ?? "—"}
                  <span className="mx-1 text-slate-400">·</span>
                  <span className="font-medium text-slate-700 dark:text-slate-300">Required:</span>{" "}
                  {f.requirement_value ?? "—"}
                </p>
                {typeof f.weighted === "number" && typeof f.max_possible === "number" && f.max_possible > 0 ? (
                  <p className="mt-1 text-[11px] text-slate-500 dark:text-slate-400">
                    Contribution: {f.weighted.toFixed(1)} / {f.max_possible.toFixed(1)} pts (this factor)
                  </p>
                ) : null}
                {isNA ? (
                  <p className="mt-1 text-[11px] italic text-slate-500 dark:text-slate-400">
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

export function MatchAnalysisModal({
  match,
  open,
  onOpenChange,
  notCalculated = false,
}: MatchAnalysisModalProps) {
  const score = match != null ? (match.final_score ?? match.score) : 0;
  const hasContent =
    match != null &&
    Boolean(
      match.breakdown ||
        (match.explanation && match.explanation.length > 0) ||
        (match.suggestions && match.suggestions.length > 0) ||
        (match.why_not_higher && match.why_not_higher.length > 0)
    );

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
              <DialogTitle className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Match Analysis
              </DialogTitle>
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
              className="focus-visible-ring shrink-0 rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
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
            ) : notCalculated ? (
              <NotCalculatedPanel title={match.title} />
            ) : (
              <>
                <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-200 bg-gradient-to-b from-primary-50 to-white py-8 dark:border-slate-700 dark:from-primary-950/40 dark:to-slate-900">
                  <MatchScoreRing score={score} size={120} />
                  <p className="mt-4 text-center text-xs font-bold uppercase tracking-widest text-primary-700 dark:text-primary-300">
                    {Math.round(score)}% eligibility fit
                  </p>
                  <MatchConfidenceNote variant="full" className="mt-3 max-w-xs px-2 text-center" />
                  {match.scoring_policy_version ? (
                    <p className="mt-2 text-center text-[10px] text-slate-500 dark:text-slate-400">
                      Scoring policy: {match.scoring_policy_version}
                    </p>
                  ) : null}
                </div>

                {!hasContent ? (
                  <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
                    Detailed eligibility breakdown is not available for this scholarship yet.
                  </p>
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
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
