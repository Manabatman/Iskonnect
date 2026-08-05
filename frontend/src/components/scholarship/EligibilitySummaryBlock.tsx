import { useState } from "react";
import { GlossaryTerm } from "../GlossaryTerm";

const COLLAPSE_THRESHOLD = 5;

interface EligibilitySummaryBlockProps {
  eligibleLevels?: string[];
  eligibleSchoolTypes?: string[];
  eligibleCourses?: string[];
  minGwa?: number | null;
  maxIncome?: number | null;
  minAge?: number | null;
  maxAge?: number | null;
  isNationwide?: boolean;
  eligibleCities?: string[];
  regions?: string[];
  className?: string;
}

function CollapsibleList({ label, items }: { label: string; items: string[] }) {
  const [expanded, setExpanded] = useState(false);
  if (items.length === 0) return null;
  const needsCollapse = items.length > COLLAPSE_THRESHOLD;
  const visible = needsCollapse && !expanded ? items.slice(0, COLLAPSE_THRESHOLD) : items;

  return (
    <li>
      {label}: {visible.join(", ")}
      {needsCollapse ? (
        <>
          {!expanded ? ` (+${items.length - COLLAPSE_THRESHOLD} more)` : null}
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            className="focus-visible-ring ml-1 text-xs font-semibold text-primary-600 underline-offset-2 hover:underline dark:text-primary-400"
          >
            {expanded ? "Show less" : "Show all"}
          </button>
        </>
      ) : null}
    </li>
  );
}

/** Compact eligibility summary — above fold on mobile (Wave 5). */
export function EligibilitySummaryBlock({
  eligibleLevels,
  eligibleSchoolTypes,
  eligibleCourses,
  minGwa,
  maxIncome,
  minAge,
  maxAge,
  isNationwide,
  eligibleCities,
  regions,
  className = "",
}: EligibilitySummaryBlockProps) {
  const hasContent =
    (eligibleLevels?.length ?? 0) > 0 ||
    (eligibleSchoolTypes?.length ?? 0) > 0 ||
    (eligibleCourses?.length ?? 0) > 0 ||
    minGwa != null ||
    maxIncome != null ||
    minAge != null ||
    maxAge != null ||
    isNationwide ||
    (eligibleCities?.length ?? 0) > 0 ||
    (regions?.length ?? 0) > 0;

  if (!hasContent) return null;

  return (
    <section
      className={`rounded-xl border border-slate-200 bg-slate-50/80 p-4 dark:border-slate-600 dark:bg-slate-900/40 ${className}`}
      aria-labelledby="eligibility-summary-heading"
    >
      <h2
        id="eligibility-summary-heading"
        className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400"
      >
        Eligibility summary
      </h2>
      <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
        {eligibleLevels?.length ? (
          <CollapsibleList label="Education level" items={eligibleLevels} />
        ) : null}
        {eligibleSchoolTypes?.length ? (
          <CollapsibleList label="School type" items={eligibleSchoolTypes} />
        ) : null}
        {eligibleCourses?.length ? (
          <li>
            Eligible courses (<GlossaryTerm term="PSCED">PSCED</GlossaryTerm>):{" "}
            <CollapsibleInlineList items={eligibleCourses} />
          </li>
        ) : null}
        {minGwa != null ? (
          <li>
            Minimum <GlossaryTerm term="GWA">GWA</GlossaryTerm>: {minGwa}%
          </li>
        ) : null}
        {maxIncome != null ? (
          <li>Income ceiling: PHP {maxIncome.toLocaleString()}/year</li>
        ) : null}
        {(minAge != null || maxAge != null) && (
          <li>
            Age: {minAge != null ? `Min ${minAge}` : ""}
            {minAge != null && maxAge != null && " · "}
            {maxAge != null ? `Max ${maxAge}` : ""}
          </li>
        )}
        {isNationwide ? (
          <li>Region: Nationwide</li>
        ) : eligibleCities?.length ? (
          <CollapsibleList label="City" items={eligibleCities} />
        ) : regions?.length ? (
          <CollapsibleList label="Region" items={regions} />
        ) : null}
      </ul>
    </section>
  );
}

function CollapsibleInlineList({ items }: { items: string[] }) {
  const [expanded, setExpanded] = useState(false);
  const needsCollapse = items.length > COLLAPSE_THRESHOLD;
  const visible = needsCollapse && !expanded ? items.slice(0, COLLAPSE_THRESHOLD) : items;

  return (
    <>
      {visible.join(", ")}
      {needsCollapse ? (
        <>
          {!expanded ? ` (+${items.length - COLLAPSE_THRESHOLD} more)` : null}
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            className="focus-visible-ring ml-1 text-xs font-semibold text-primary-600 underline-offset-2 hover:underline dark:text-primary-400"
          >
            {expanded ? "Show less" : "Show all"}
          </button>
        </>
      ) : null}
    </>
  );
}
