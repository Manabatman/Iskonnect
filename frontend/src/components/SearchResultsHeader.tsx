import { Button } from "@/components/ui/button";
import { SEARCH_SORT_OPTIONS, type SearchSortOption } from "../constants/searchSort";
import {
  buildActiveFilterChips,
  removeFilterChip,
  type ActiveFilterChip,
} from "./SearchAppliedFilterBar";
import type { ScholarshipSearchFilters } from "../types";

interface SearchResultsHeaderProps {
  total: number;
  query: string;
  sortBy: SearchSortOption;
  onSortChange: (sort: SearchSortOption) => void;
  filters: ScholarshipSearchFilters;
  onFiltersChange: (filters: ScholarshipSearchFilters) => void;
  onClearQuery: () => void;
}

function AppliedFilterChip({
  chip,
  onRemove,
}: {
  chip: ActiveFilterChip;
  onRemove: (chip: ActiveFilterChip) => void;
}) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-foreground">
      {chip.label}
      <button
        type="button"
        onClick={() => onRemove(chip)}
        className="focus-visible-ring rounded-full p-0.5 hover:bg-background"
        aria-label={`Remove ${chip.label}`}
      >
        <svg className="size-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden>
          <path
            fillRule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>
    </span>
  );
}

export function SearchResultsHeader({
  total,
  query,
  sortBy,
  onSortChange,
  filters,
  onFiltersChange,
  onClearQuery,
}: SearchResultsHeaderProps) {
  const chips = buildActiveFilterChips(filters, query);
  const trimmedQuery = query.trim();

  const handleRemoveChip = (chip: ActiveFilterChip) => {
    if (chip.key === "query") {
      onClearQuery();
      return;
    }
    onFiltersChange(removeFilterChip(filters, chip.key));
  };

  return (
    <div className="sticky top-0 z-10 -mx-1 mb-4 space-y-3 border-b border-border bg-background/95 px-1 py-3 backdrop-blur-sm">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div className="min-w-0">
          <h2 className="text-lg font-semibold text-foreground">Results</h2>
          <p className="text-sm text-muted-foreground">
            {total} scholarship{total !== 1 ? "s" : ""} found
            {trimmedQuery ? (
              <>
                {" "}
                for <span className="font-medium text-foreground">&ldquo;{trimmedQuery}&rdquo;</span>
              </>
            ) : null}
          </p>
        </div>
        <label className="flex min-h-[44px] shrink-0 items-center gap-2 text-sm text-muted-foreground">
          <span className="whitespace-nowrap">Sort by</span>
          <select
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value as SearchSortOption)}
            aria-label="Sort results"
            className="focus-visible-ring min-h-[44px] rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground"
          >
            {SEARCH_SORT_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {chips.length > 0 ? (
        <div
          className="flex flex-wrap items-center gap-2"
          role="region"
          aria-label="Applied filters"
        >
          <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Applied</span>
          {chips.map((chip) => (
            <AppliedFilterChip key={`${chip.key}-${chip.label}`} chip={chip} onRemove={handleRemoveChip} />
          ))}
          <Button
            type="button"
            variant="link"
            size="sm"
            className="h-auto px-1 py-0 text-xs"
            onClick={() => {
              onClearQuery();
              onFiltersChange({});
            }}
          >
            Clear all
          </Button>
        </div>
      ) : null}
    </div>
  );
}
