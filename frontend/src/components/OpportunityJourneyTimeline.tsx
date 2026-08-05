import { Link } from "react-router-dom";
import {
  OPPORTUNITY_JOURNEY_ORDERED,
  type OpportunityJourneyStatus,
  type OpportunityTypeDef,
} from "../constants/opportunityTypes";

const STATUS_LABELS: Record<OpportunityJourneyStatus, string> = {
  live: "Live",
  planned: "Planned",
  exploring: "Exploring",
};

const STATUS_STYLES: Record<OpportunityJourneyStatus, string> = {
  live: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/50 dark:text-emerald-100",
  planned: "bg-primary-100 text-primary-900 dark:bg-primary-900/50 dark:text-primary-100",
  exploring: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
};

function JourneyStatusBadge({ status }: { status: OpportunityJourneyStatus }) {
  return (
    <span className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${STATUS_STYLES[status]}`}>
      {STATUS_LABELS[status]}
    </span>
  );
}

interface OpportunityJourneyTimelineProps {
  /** Highlight this slug in the timeline (coming-soon page). */
  selectedSlug?: string;
  /** Show links to each vertical's detail page. */
  linkItems?: boolean;
  compact?: boolean;
}

export function OpportunityJourneyTimeline({
  selectedSlug,
  linkItems = false,
  compact = false,
}: OpportunityJourneyTimelineProps) {
  return (
    <ol className="relative space-y-0 border-l-2 border-slate-200 pl-6 dark:border-slate-700">
      {OPPORTUNITY_JOURNEY_ORDERED.map((item, index) => (
        <JourneyTimelineItem
          key={item.slug}
          item={item}
          isLast={index === OPPORTUNITY_JOURNEY_ORDERED.length - 1}
          isSelected={item.slug === selectedSlug}
          linkItems={linkItems}
          compact={compact}
        />
      ))}
    </ol>
  );
}

function JourneyTimelineItem({
  item,
  isLast,
  isSelected,
  linkItems,
  compact,
}: {
  item: OpportunityTypeDef;
  isLast: boolean;
  isSelected: boolean;
  linkItems: boolean;
  compact: boolean;
}) {
  const isLive = item.journeyStatus === "live";
  const dotClass = isLive
    ? "border-primary-600 bg-primary-600"
    : isSelected
      ? "border-primary-500 bg-white dark:bg-slate-900"
      : "border-slate-300 bg-white dark:border-slate-600 dark:bg-slate-900";

  const body = (
    <>
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <p className={`font-semibold text-slate-900 dark:text-slate-100 ${compact ? "text-sm" : "text-base"}`}>
            {item.label}
          </p>
          {!compact ? (
            <p className="mt-0.5 text-sm text-slate-600 dark:text-slate-400">{item.description}</p>
          ) : null}
          {item.plannedFor && item.journeyStatus !== "live" ? (
            <p className="mt-1 text-xs font-medium text-primary-700 dark:text-primary-300">
              Planned for {item.plannedFor}
            </p>
          ) : null}
        </div>
        <JourneyStatusBadge status={item.journeyStatus} />
      </div>
    </>
  );

  return (
    <li className={`relative ${isLast ? "pb-0" : "pb-6"}`}>
      <span
        className={`absolute -left-[1.625rem] top-1.5 size-3 rounded-full border-2 ${dotClass}`}
        aria-hidden
      />
      <div
        className={[
          "rounded-xl border p-3 sm:p-4",
          isSelected
            ? "border-primary-300 bg-primary-50/80 dark:border-primary-700 dark:bg-primary-950/30"
            : "border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900/40",
        ].join(" ")}
      >
        {linkItems && !isLive ? (
          <Link
            to={`/opportunities/${item.slug}`}
            className="focus-visible-ring block rounded-lg hover:opacity-90"
          >
            {body}
          </Link>
        ) : isLive && item.searchPath ? (
          <Link to={item.searchPath} className="focus-visible-ring block rounded-lg hover:opacity-90">
            {body}
          </Link>
        ) : (
          body
        )}
      </div>
    </li>
  );
}

export function journeyStatusLabel(status: OpportunityJourneyStatus): string {
  return STATUS_LABELS[status];
}
