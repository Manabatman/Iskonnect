import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";
import { useDebounce } from "./useDebounce";
import type {
  ScholarshipInfo,
  ScholarshipSearchResponse,
  ScholarshipSearchFilters,
} from "../types";
import { cacheSearchResults, readCachedSearchResults } from "../utils/offlineCache";

const DEBOUNCE_MS = 300;
const DEFAULT_LIMIT = 20;

export interface UseScholarshipSearchOptions {
  /** Page size for GET /api/v1/scholarships/search */
  limit?: number;
  /** Autocomplete via /api/v1/suggestions/scholarships */
  enableSuggestions?: boolean;
  /** Keep search input in sync with `?query=` URL param */
  syncUrlQuery?: boolean;
}

export function useScholarshipSearch(options: UseScholarshipSearchOptions = {}) {
  const { limit = DEFAULT_LIMIT, enableSuggestions = true, syncUrlQuery = false } = options;
  const [searchParams] = useSearchParams();

  const [query, setQuery] = useState(() => (syncUrlQuery ? (searchParams.get("query") ?? "") : ""));

  useEffect(() => {
    if (!syncUrlQuery) return;
    const q = searchParams.get("query");
    if (q != null) setQuery(q);
  }, [searchParams, syncUrlQuery]);

  const [filters, setFilters] = useState<ScholarshipSearchFilters>({});
  const [page, setPage] = useState(1);
  const [results, setResults] = useState<ScholarshipInfo[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [suggestionsOpen, setSuggestionsOpen] = useState(false);
  const [highlightIndex, setHighlightIndex] = useState(-1);
  const suggestionsRef = useRef<HTMLUListElement>(null);
  const justSelectedRef = useRef(false);

  const debouncedQuery = useDebounce(query, DEBOUNCE_MS);

  const fetchSearch = useCallback(
    async (searchQuery: string, searchFilters: ScholarshipSearchFilters, pageNum: number) => {
      const params = new URLSearchParams();
      if (searchQuery.trim()) params.set("query", searchQuery.trim());
      if (searchFilters.region) params.set("region", searchFilters.region);
      if (searchFilters.field) params.set("field", searchFilters.field);
      if (searchFilters.education_level) params.set("education_level", searchFilters.education_level);
      if (searchFilters.provider) params.set("provider", searchFilters.provider);
      if (searchFilters.max_income != null && searchFilters.max_income >= 0) {
        params.set("max_income", String(searchFilters.max_income));
      }
      if (searchFilters.school?.trim()) {
        params.set("school", searchFilters.school.trim());
      }
      if (searchFilters.timing) params.set("timing", searchFilters.timing);
      if (searchFilters.life_stage) params.set("life_stage", searchFilters.life_stage);
      if (searchFilters.include_archived) params.set("include_archived", "true");
      if (searchFilters.include_closed) params.set("include_closed", "true");
      params.set("page", String(pageNum));
      params.set("limit", String(limit));

      const res = await apiFetch(`/api/v1/scholarships/search?${params.toString()}`);
      if (!res.ok) throw new Error("Search failed");
      return (await res.json()) as ScholarshipSearchResponse;
    },
    [limit]
  );

  useEffect(() => {
    setPage(1);
  }, [debouncedQuery]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchSearch(debouncedQuery, filters, page)
      .then((data) => {
        if (!cancelled) {
          setResults(data.results ?? []);
          setTotal(data.total ?? 0);
          setTotalPages(data.total_pages ?? 0);
          void cacheSearchResults(`search:${debouncedQuery}:${page}`, data);
        }
      })
      .catch(async (err) => {
        if (!cancelled) {
          const cached = await readCachedSearchResults<ScholarshipSearchResponse>(
            `search:${debouncedQuery}:${page}`,
          );
          if (cached?.results) {
            setResults(cached.results);
            setTotal(cached.total ?? cached.results.length);
            setTotalPages(cached.total_pages ?? 1);
            setError(null);
          } else {
            setError(err instanceof Error ? err.message : "Search failed");
          }
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [debouncedQuery, filters, page, fetchSearch]);

  useEffect(() => {
    if (!enableSuggestions) return;
    if (justSelectedRef.current) {
      justSelectedRef.current = false;
      return;
    }
    if (!debouncedQuery.trim()) {
      setSuggestions([]);
      setSuggestionsOpen(false);
      return;
    }
    const params = new URLSearchParams({ q: debouncedQuery.trim() });
    apiFetch(`/api/v1/suggestions/scholarships?${params.toString()}`)
      .then((res) => (res.ok ? res.json() : { suggestions: [] }))
      .then((data: { suggestions?: string[] }) => {
        setSuggestions(data.suggestions ?? []);
        setHighlightIndex(-1);
        setSuggestionsOpen(true);
      })
      .catch(() => setSuggestions([]));
  }, [debouncedQuery, enableSuggestions]);

  const handleSuggestionSelect = useCallback((suggestion: string) => {
    justSelectedRef.current = true;
    setQuery(suggestion);
    setSuggestions([]);
    setSuggestionsOpen(false);
    setPage(1);
  }, []);

  const handleSearchSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    setSuggestionsOpen(false);
    setPage(1);
  }, []);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (!enableSuggestions) return;
      if (!suggestionsOpen || suggestions.length === 0) {
        if (e.key === "Escape") setSuggestionsOpen(false);
        return;
      }
      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          setHighlightIndex((i) => (i < suggestions.length - 1 ? i + 1 : 0));
          break;
        case "ArrowUp":
          e.preventDefault();
          setHighlightIndex((i) => (i > 0 ? i - 1 : suggestions.length - 1));
          break;
        case "Enter":
          e.preventDefault();
          if (highlightIndex >= 0 && highlightIndex < suggestions.length) {
            handleSuggestionSelect(suggestions[highlightIndex]);
          }
          break;
        case "Escape":
          e.preventDefault();
          setSuggestionsOpen(false);
          setHighlightIndex(-1);
          break;
      }
    },
    [enableSuggestions, suggestionsOpen, suggestions, highlightIndex, handleSuggestionSelect]
  );

  useEffect(() => {
    if (!enableSuggestions) return;
    if (highlightIndex >= 0 && suggestionsRef.current) {
      const el = suggestionsRef.current.children[highlightIndex] as HTMLElement;
      el?.scrollIntoView({ block: "nearest" });
    }
  }, [highlightIndex, enableSuggestions]);

  const handleFiltersChange = useCallback((newFilters: ScholarshipSearchFilters) => {
    setFilters(newFilters);
    setPage(1);
  }, []);

  return {
    query,
    setQuery,
    filters,
    page,
    setPage,
    results,
    total,
    totalPages,
    loading,
    error,
    suggestions,
    suggestionsOpen,
    setSuggestionsOpen,
    highlightIndex,
    suggestionsRef,
    handleSuggestionSelect,
    handleSearchSubmit,
    handleKeyDown,
    handleFiltersChange,
  };
}
