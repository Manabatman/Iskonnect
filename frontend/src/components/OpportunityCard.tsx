import { memo, type KeyboardEvent } from "react";
import { BookmarkButton } from "./BookmarkButton";
import type { Opportunity } from "../data/mockOpportunities";

export interface OpportunityCardProps {
  opportunity: Opportunity;
  selected: boolean;
  onSelect: (id: number) => void;
}

function OpportunityCardInner({ opportunity, selected, onSelect }: OpportunityCardProps) {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onSelect(opportunity.id);
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => onSelect(opportunity.id)}
      onKeyDown={handleKeyDown}
      aria-current={selected ? "true" : undefined}
      className={[
        "cursor-pointer rounded-xl border p-4 text-left transition-all duration-150",
        "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800",
        selected
          ? "border-primary-300 bg-primary-50 shadow-md ring-2 ring-primary-500 dark:border-primary-600 dark:bg-primary-900/25"
          : "border-slate-200 bg-white shadow-sm hover:border-slate-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-800/80 dark:hover:border-slate-600",
      ].join(" ")}
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="text-sm font-semibold leading-snug text-slate-900 dark:text-slate-100">
          {opportunity.title}
        </h3>
        <div className="flex shrink-0 items-center gap-1">
          {opportunity.isNew ? (
            <span className="rounded-full bg-primary-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
              New
            </span>
          ) : null}
          <BookmarkButton scholarshipId={opportunity.id} />
        </div>
      </div>
      <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{opportunity.organization}</p>
      <p className="mt-0.5 text-xs text-slate-600 dark:text-slate-300">{opportunity.location}</p>
      {opportunity.stipend ? (
        <p className="mt-2 text-xs font-medium text-primary-700 dark:text-primary-300">{opportunity.stipend}</p>
      ) : null}
      <div className="mt-2 flex flex-wrap gap-1">
        {opportunity.tags.map((tag) => (
          <span
            key={tag}
            className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600 dark:bg-slate-700 dark:text-slate-300"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}

export const OpportunityCard = memo(OpportunityCardInner);
