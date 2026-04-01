import { useState } from "react";
import type { MatchResult } from "../types";

export function providerInitials(provider: string | null | undefined): string {
  const clean = (provider ?? "").replace(/[^a-zA-Z0-9]/g, "").slice(0, 2);
  return clean.length ? clean.toUpperCase() : "?";
}

export function statusToFactorPercent(status: string | undefined): number {
  const s = (status ?? "").toLowerCase();
  if (s === "met" || s === "exceeded" || s === "ready") return 100;
  if (s === "partial") return 50;
  return 0;
}

export function getUrgencyLevel(
  deadline: string | null | undefined,
  openDate?: string | null
): { level: string; label: string } {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (openDate) {
    try {
      const open = new Date(openDate);
      open.setHours(0, 0, 0, 0);
      const daysUntilOpen = Math.ceil((open.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
      if (daysUntilOpen > 0) {
        if (daysUntilOpen <= 7) return { level: "upcoming", label: `Opens in ${daysUntilOpen}d` };
        return { level: "upcoming", label: "Opens soon" };
      }
    } catch {
      /* ignore */
    }
  }

  if (!deadline) return { level: "unknown", label: "No deadline" };
  try {
    const d = new Date(deadline);
    d.setHours(0, 0, 0, 0);
    const diffMs = d.getTime() - today.getTime();
    const daysLeft = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    if (daysLeft < 0) return { level: "closed", label: "Closed" };
    if (daysLeft <= 3) return { level: "critical", label: `Closes in ${daysLeft}d` };
    if (daysLeft <= 7) return { level: "urgent", label: `Closes in ${daysLeft}d` };
    if (daysLeft <= 30) return { level: "soon", label: "Closing Soon" };
    return { level: "open", label: "Open" };
  } catch {
    return { level: "unknown", label: "No deadline" };
  }
}

export function getUrgencyBadgeClasses(level: string): string {
  switch (level) {
    case "critical":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
    case "urgent":
      return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300";
    case "soon":
      return "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300";
    case "open":
      return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
    case "closed":
      return "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-400";
    case "upcoming":
      return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300";
    default:
      return "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400";
  }
}

export function MatchStatusIcon({ status }: { status: string }) {
  switch (status) {
    case "met":
    case "exceeded":
    case "ready":
      return (
        <span className="text-green-600" aria-label="Met">
          ✓
        </span>
      );
    case "partial":
      return (
        <span className="text-amber-600" aria-label="Partial">
          ◐
        </span>
      );
    case "missing":
    case "disqualified":
      return (
        <span className="text-red-600" aria-label="Missing">
          ✗
        </span>
      );
    default:
      return <span className="text-slate-400">—</span>;
  }
}

function formatBreakdownKey(key: string): string {
  const k = String(key ?? "");
  return k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Expandable "Why you matched" — shared by match results page and search enhancement. */
export function WhyYouMatchedSection({ match }: { match: MatchResult }) {
  const [showBreakdown, setShowBreakdown] = useState(false);

  if (
    !match.breakdown &&
    !(match.explanation && match.explanation.length > 0) &&
    !(match.suggestions && match.suggestions.length > 0)
  ) {
    return null;
  }

  return (
    <div className="mt-3 border-t border-slate-200 dark:border-slate-700 pt-3">
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setShowBreakdown(!showBreakdown);
        }}
        className="flex w-full items-center justify-between text-left text-sm font-medium text-primary-600 hover:text-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-inset rounded"
        aria-expanded={showBreakdown}
      >
        Why you matched
        <svg
          className={`h-4 w-4 transition-transform ${showBreakdown ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {showBreakdown && (
        <div className="mt-2 space-y-3">
          {match.breakdown && (
            <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 p-3 space-y-2">
              <p className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                Your Match Breakdown
              </p>
              {Object.entries(match.breakdown).map(([key, factor]) => {
                if (!factor || typeof factor !== "object") return null;
                const f = factor as { status?: string; user_value?: string; requirement_value?: string };
                const labels: Record<string, string> = {
                  academic: "Academic (GWA)",
                  socioeconomic: "Financial Eligibility",
                  field_relevance: "Course Alignment",
                  geographic: "Region Match",
                  priority_group: "Priority Group",
                };
                const label = labels[key] ?? formatBreakdownKey(key);
                return (
                  <div key={key} className="flex items-start gap-2 text-xs">
                    <span className="mt-0.5 shrink-0">
                      <MatchStatusIcon status={(f.status ?? "").toLowerCase()} />
                    </span>
                    <div className="min-w-0 flex-1">
                      <span className="font-medium text-slate-700 dark:text-slate-300">{label}</span>
                      <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-600">
                        <div
                          className="h-full rounded-full bg-primary-500 transition-all dark:bg-primary-400"
                          style={{ width: `${statusToFactorPercent(f.status)}%` }}
                        />
                      </div>
                      <p className="mt-1 text-slate-600 dark:text-slate-400">
                        Your data: {f.user_value ?? "—"} • Requirement: {f.requirement_value ?? "—"}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
          {match.explanation && match.explanation.length > 0 && (
            <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-400 space-y-0.5">
              {match.explanation.map((line, i) => (
                <li key={i}>{line}</li>
              ))}
            </ul>
          )}
          {match.suggestions && match.suggestions.length > 0 ? (
            <div className="rounded-lg border border-primary-200 bg-primary-50/80 p-3 dark:border-primary-800 dark:bg-primary-950/30">
              <p className="text-xs font-semibold text-primary-800 dark:text-primary-200">Tips to improve</p>
              <ul className="mt-1 list-inside list-disc text-xs text-primary-900 dark:text-primary-100">
                {match.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}
