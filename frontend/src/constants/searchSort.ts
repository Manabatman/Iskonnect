/** Search results sort options (Wave 4 — synced with GET /scholarships/search?sort=). */
export const SEARCH_SORT_VALUES = ["relevance", "deadline", "title", "verified"] as const;

export type SearchSortOption = (typeof SEARCH_SORT_VALUES)[number];

export const SEARCH_SORT_OPTIONS: { value: SearchSortOption; label: string }[] = [
  { value: "relevance", label: "Relevance" },
  { value: "deadline", label: "Deadline (soonest)" },
  { value: "title", label: "Title (A–Z)" },
  { value: "verified", label: "Recently verified" },
];

export function parseSearchSort(value: string | null | undefined): SearchSortOption {
  if (value && SEARCH_SORT_VALUES.includes(value as SearchSortOption)) {
    return value as SearchSortOption;
  }
  return "relevance";
}
