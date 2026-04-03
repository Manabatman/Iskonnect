import { useCallback, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import { MatchAnalysisModal } from "../components/MatchAnalysisModal";
import { ScholarshipCardV2 } from "../components/ScholarshipCardV2";
import { ScholarshipSearchFilters } from "../components/ScholarshipSearchFilters";
import { ScholarshipDetailPanel } from "../components/ScholarshipDetailPanel";
import { useAuth } from "../contexts/AuthContext";
import { useScholarshipSearch } from "../hooks/useScholarshipSearch";
import type { MatchResult, ScholarshipInfo } from "../types";

export function ScholarshipSearchPage() {
  const navigate = useNavigate();
  const { user, authHeaders } = useAuth();
  const searchInputRef = useRef<HTMLInputElement>(null);

  const {
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
  } = useScholarshipSearch({
    limit: 20,
    enableSuggestions: true,
    syncUrlQuery: true,
  });

  const [selectedScholarship, setSelectedScholarship] = useState<ScholarshipInfo | null>(null);
  const [analysisMatch, setAnalysisMatch] = useState<MatchResult | null>(null);
  /** Cached bulk matches for “Check my match” (single API shape, client-side lookup). */
  const [matchCache, setMatchCache] = useState<Map<number, MatchResult> | null>(null);
  const [checkingMatchId, setCheckingMatchId] = useState<number | null>(null);
  const [checkMatchLoading, setCheckMatchLoading] = useState(false);
  const [checkMatchError, setCheckMatchError] = useState<string | null>(null);
  const [findMatchesNavLoading, setFindMatchesNavLoading] = useState(false);

  const inflightMatchMap = useRef<Promise<Map<number, MatchResult>> | null>(null);

  const handleAnalysisOpenChange = useCallback((open: boolean) => {
    if (!open) setAnalysisMatch(null);
  }, []);

  const handleGoToMatches = useCallback(async () => {
    if (!user) {
      navigate("/login", { state: { from: "/scholarships/search" } });
      return;
    }
    setFindMatchesNavLoading(true);
    try {
      const res = await apiFetch("/api/v1/profiles", { headers: authHeaders() });
      if (!res.ok) throw new Error("Could not load your profile.");
      const profiles = (await res.json()) as Array<{ id: number }>;
      if (!Array.isArray(profiles) || profiles.length === 0) {
        navigate("/profile-builder");
        return;
      }
      navigate(`/match/${profiles[0].id}`);
    } catch (e) {
      setCheckMatchError(e instanceof Error ? e.message : "Could not open matches.");
    } finally {
      setFindMatchesNavLoading(false);
    }
  }, [user, navigate, authHeaders]);

  const getOrFetchMatchMap = useCallback(async (): Promise<Map<number, MatchResult>> => {
    if (matchCache) return matchCache;
    if (!inflightMatchMap.current) {
      inflightMatchMap.current = (async () => {
        const res = await apiFetch("/api/v1/profiles", { headers: authHeaders() });
        if (!res.ok) throw new Error("Could not load your profile.");
        const profiles = (await res.json()) as Array<{ id: number }>;
        if (!Array.isArray(profiles) || profiles.length === 0) {
          navigate("/profile-builder");
          throw new Error("PROFILE_REQUIRED");
        }
        const profileId = profiles[0].id;
        const mRes = await apiFetch(`/api/v1/matches/${profileId}`, { headers: authHeaders() });
        if (mRes.status === 401 || mRes.status === 403) {
          throw new Error("Session expired. Please sign in again.");
        }
        if (!mRes.ok) throw new Error("Could not load matches.");
        const data = (await mRes.json()) as { matches?: MatchResult[] };
        const list = data.matches ?? [];
        const next = new Map<number, MatchResult>();
        for (const m of list) {
          if (m && typeof m.id === "number") next.set(m.id, m);
        }
        return next;
      })().finally(() => {
        inflightMatchMap.current = null;
      });
    }
    const map = await inflightMatchMap.current;
    setMatchCache(map);
    return map;
  }, [authHeaders, navigate, matchCache]);

  const handleCheckMatch = useCallback(
    async (scholarshipId: number) => {
      if (!user) {
        navigate("/login", { state: { from: "/scholarships/search" } });
        return;
      }
      setCheckMatchError(null);
      const row = results.find((r) => r.id === scholarshipId);
      const titleFallback = row?.title ?? "Scholarship";

      setCheckingMatchId(scholarshipId);
      setCheckMatchLoading(true);
      try {
        const map = await getOrFetchMatchMap();
        const found = map.get(scholarshipId);
        if (found) {
          setAnalysisMatch(found);
        } else {
          setAnalysisMatch({
            id: scholarshipId,
            title: titleFallback,
            score: 0,
            link: row?.link ?? null,
            description: row?.description ?? "",
            regions: row?.regions ?? [],
            min_age: row?.min_age ?? null,
            max_age: row?.max_age ?? null,
          });
        }
      } catch (e) {
        if (e instanceof Error && e.message === "PROFILE_REQUIRED") return;
        setCheckMatchError(e instanceof Error ? e.message : "Failed to load match.");
      } finally {
        setCheckMatchLoading(false);
        setCheckingMatchId(null);
      }
    },
    [user, navigate, results, getOrFetchMatchMap]
  );

  return (
    <section id="scholarship-search" className="py-8">
      <div className="mx-auto max-w-7xl px-4">
        <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Search Scholarships</h1>
          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={handleGoToMatches}
              disabled={findMatchesNavLoading}
              className="rounded-xl bg-accent-600 px-6 py-3 font-semibold text-white shadow-md transition hover:bg-accent-700 focus:outline-none focus:ring-2 focus:ring-accent-500 focus:ring-offset-2 disabled:opacity-70 dark:focus:ring-offset-slate-900"
            >
              {findMatchesNavLoading ? "Opening…" : "Find My Matches"}
            </button>
            <Link
              to="/profile-builder"
              className="w-fit rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white shadow-md transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Complete Your Profile
            </Link>
          </div>
        </div>

        {checkMatchError ? (
          <div
            className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100"
            role="alert"
          >
            {checkMatchError}
          </div>
        ) : null}

        <form onSubmit={handleSearchSubmit} className="relative mb-6">
          <label htmlFor="search-input" className="sr-only">
            Search scholarship names
          </label>
          <input
            ref={searchInputRef}
            id="search-input"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => query.trim() && suggestions.length > 0 && setSuggestionsOpen(true)}
            onBlur={() => setTimeout(() => setSuggestionsOpen(false), 150)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. DOST, CHED, Merit"
            className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-4 py-3 pr-10 text-slate-900 dark:text-slate-100 placeholder-slate-500 outline-none transition focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            autoComplete="off"
            aria-autocomplete="list"
            aria-expanded={suggestionsOpen}
          />
          {suggestionsOpen && suggestions.length > 0 && (
            <ul
              ref={suggestionsRef}
              role="listbox"
              className="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 py-1 shadow-lg"
            >
              {suggestions.map((item, i) => (
                <li
                  key={item}
                  role="option"
                  aria-selected={i === highlightIndex}
                  className={`cursor-pointer px-4 py-2 text-sm text-slate-900 dark:text-slate-100 ${
                    i === highlightIndex
                      ? "bg-primary-100 dark:bg-primary-900"
                      : "hover:bg-slate-100 dark:hover:bg-slate-700"
                  }`}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    handleSuggestionSelect(item);
                  }}
                >
                  {item}
                </li>
              ))}
            </ul>
          )}
        </form>

        <div className="flex flex-col gap-6 lg:flex-row">
          <div className="lg:w-64 lg:shrink-0">
            <ScholarshipSearchFilters filters={filters} onChange={handleFiltersChange} />
          </div>

          <div className="min-w-0 flex-1">
            {loading && (
              <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-md">
                <div
                  className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-primary-200 border-t-primary-600"
                  aria-hidden
                />
                <p className="mt-4 text-slate-600 dark:text-slate-400">Searching...</p>
              </div>
            )}

            {error && (
              <div
                className="rounded-lg border border-danger-200 bg-danger-50 px-3 py-2 text-sm text-danger-700 dark:border-red-800 dark:bg-red-900/40 dark:text-red-200"
                role="alert"
              >
                {error}
              </div>
            )}

            {!loading && !error && (
              <>
                <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
                  {total} scholarship{total !== 1 ? "s" : ""} found
                </p>

                {results.length === 0 ? (
                  <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-md">
                    <p className="text-slate-600 dark:text-slate-400">No scholarships match your search.</p>
                    <p className="mt-2 text-sm text-slate-500 dark:text-slate-500">
                      Try adjusting your filters or search query.
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-1 items-stretch gap-6 md:grid-cols-2 xl:grid-cols-3">
                      {results.map((s) => (
                        <ScholarshipCardV2
                          key={s.id}
                          scholarship={s}
                          onCheckMatch={handleCheckMatch}
                          checkMatchLoading={checkingMatchId === s.id && checkMatchLoading}
                          onCardBodyClick={setSelectedScholarship}
                          className="ring-2 ring-transparent hover:ring-primary-200 dark:hover:ring-primary-800"
                        />
                      ))}
                    </div>

                    {totalPages > 1 && (
                      <nav
                        className="mt-8 flex flex-wrap items-center justify-center gap-2"
                        aria-label="Pagination"
                      >
                        <button
                          type="button"
                          onClick={() => setPage((p) => Math.max(1, p - 1))}
                          disabled={page <= 1}
                          className="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 dark:hover:bg-slate-600"
                        >
                          Previous
                        </button>
                        <span className="px-4 py-2 text-sm text-slate-600 dark:text-slate-400">
                          Page {page} of {totalPages}
                        </span>
                        <button
                          type="button"
                          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                          disabled={page >= totalPages}
                          className="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 dark:hover:bg-slate-600"
                        >
                          Next
                        </button>
                      </nav>
                    )}
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {selectedScholarship && (
        <ScholarshipDetailPanel
          scholarship={selectedScholarship as Parameters<typeof ScholarshipDetailPanel>[0]["scholarship"]}
          onClose={() => setSelectedScholarship(null)}
          isOpen={!!selectedScholarship}
        />
      )}

      <MatchAnalysisModal match={analysisMatch} open={analysisMatch != null} onOpenChange={handleAnalysisOpenChange} />
    </section>
  );
}
