import type { MatchResult, OpportunityTimeline } from "../types";
import { ScholarshipCardV2 } from "./ScholarshipCardV2";

const LANE_META: Record<
  keyof OpportunityTimeline["lanes"],
  { title: string; description: string; accent: string }
> = {
  available_now: {
    title: "Available now",
    description: "Open applications you can pursue today.",
    accent: "border-emerald-200 bg-emerald-50/60 dark:border-emerald-800 dark:bg-emerald-950/30",
  },
  opening_soon: {
    title: "Opening soon",
    description: "Expected to open within the next few months.",
    accent: "border-sky-200 bg-sky-50/60 dark:border-sky-800 dark:bg-sky-950/30",
  },
  prepare_for: {
    title: "Prepare for",
    description: "Start gathering requirements before deadlines.",
    accent: "border-violet-200 bg-violet-50/60 dark:border-violet-800 dark:bg-violet-950/30",
  },
  expected_reopening: {
    title: "Expected to reopen",
    description: "Closed now but likely to return on cycle.",
    accent: "border-amber-200 bg-amber-50/60 dark:border-amber-800 dark:bg-amber-950/30",
  },
  future_eligibility: {
    title: "Future eligibility",
    description: "May fit when you advance grade or standing.",
    accent: "border-slate-200 bg-slate-50/80 dark:border-slate-700 dark:bg-slate-800/50",
  },
  past_reference: {
    title: "Past reference",
    description: "Closed cycles kept for planning.",
    accent: "border-slate-200 bg-slate-50/50 dark:border-slate-700 dark:bg-slate-900/40",
  },
};

type LaneKey = keyof OpportunityTimeline["lanes"];

interface OpportunityTimelineProps {
  timeline: OpportunityTimeline;
  onShowAnalysis?: (match: MatchResult) => void;
  compact?: boolean;
}

function LaneSection({
  laneKey,
  items,
  count,
  onShowAnalysis,
  compact,
}: {
  laneKey: LaneKey;
  items: MatchResult[];
  count: number;
  onShowAnalysis?: (match: MatchResult) => void;
  compact?: boolean;
}) {
  if (count === 0) return null;
  const meta = LANE_META[laneKey];
  return (
    <section className={`rounded-2xl border p-4 sm:p-5 ${meta.accent}`} aria-labelledby={`lane-${laneKey}`}>
      <div className="mb-4 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h3 id={`lane-${laneKey}`} className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            {meta.title}
            <span className="ml-2 rounded-full bg-white/80 px-2 py-0.5 text-sm font-medium text-slate-700 dark:bg-slate-900/60 dark:text-slate-200">
              {count}
            </span>
          </h3>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{meta.description}</p>
        </div>
      </div>
      <div className={`grid gap-4 ${compact ? "grid-cols-1" : "grid-cols-1 md:grid-cols-2 xl:grid-cols-3"}`}>
        {items.map((item) => (
          <ScholarshipCardV2 key={`${laneKey}-${item.id}`} scholarship={item} onShowAnalysis={onShowAnalysis} />
        ))}
      </div>
    </section>
  );
}

export function OpportunityTimelineView({ timeline, onShowAnalysis, compact }: OpportunityTimelineProps) {
  const { summary, lanes, headline } = timeline;
  const hasActionable = summary.total_actionable > 0;

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-primary-200 bg-gradient-to-br from-primary-50 to-white p-5 dark:border-primary-800 dark:from-primary-950/40 dark:to-slate-900">
        <p className="text-sm font-medium uppercase tracking-wide text-primary-700 dark:text-primary-300">
          Your opportunity plan
        </p>
        <p className="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{headline}</p>
        {!hasActionable ? (
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Even when nothing is open today, ISKONNECT maps what is coming — complete your profile for sharper
            forecasts.
          </p>
        ) : null}
        <div className="mt-4 flex flex-wrap gap-2 text-sm">
          {summary.available_now > 0 ? (
            <span className="rounded-full bg-emerald-100 px-3 py-1 font-medium text-emerald-900 dark:bg-emerald-900/50 dark:text-emerald-100">
              {summary.available_now} now
            </span>
          ) : null}
          {summary.opening_soon > 0 ? (
            <span className="rounded-full bg-sky-100 px-3 py-1 font-medium text-sky-900 dark:bg-sky-900/50 dark:text-sky-100">
              {summary.opening_soon} soon
            </span>
          ) : null}
          {summary.prepare_for > 0 ? (
            <span className="rounded-full bg-violet-100 px-3 py-1 font-medium text-violet-900 dark:bg-violet-900/50 dark:text-violet-100">
              {summary.prepare_for} to prepare
            </span>
          ) : null}
          {summary.expected_reopening > 0 ? (
            <span className="rounded-full bg-amber-100 px-3 py-1 font-medium text-amber-900 dark:bg-amber-900/50 dark:text-amber-100">
              {summary.expected_reopening} reopening
            </span>
          ) : null}
        </div>
      </div>

      {(Object.keys(lanes) as LaneKey[]).map((key) => (
        <LaneSection
          key={key}
          laneKey={key}
          items={lanes[key]}
          count={summary[key]}
          onShowAnalysis={onShowAnalysis}
          compact={compact}
        />
      ))}
    </div>
  );
}
