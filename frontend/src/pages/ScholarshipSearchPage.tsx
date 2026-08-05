import { useCallback, useEffect, useRef, useState, lazy, Suspense } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { apiFetch } from "../api/client";
import { LiveRegion } from "../components/a11y/LiveRegion";
import { ScholarshipCardV2 } from "../components/ScholarshipCardV2";
import { StatusGuideLink } from "../components/LifecycleStatusBadge";
import { ScholarshipSearchFilters, mostRestrictiveFilterHint } from "../components/ScholarshipSearchFilters";
import { SearchResultsHeader } from "../components/SearchResultsHeader";
import { buildActiveFilterChips } from "../components/SearchAppliedFilterBar";
import { StateMessage } from "../components/StateMessage";
import { ERROR_COPY } from "../constants/errorCopy";
import { ScholarshipDetailPanel } from "../components/ScholarshipDetailPanel";
import { useAuth } from "../contexts/AuthContext";
import { useScholarshipSearch } from "../hooks/useScholarshipSearch";
import type { EligibilityExplanation, MatchResult, ScholarshipInfo } from "../types";

const MatchAnalysisModal = lazy(() =>
  import("../components/MatchAnalysisModal").then((m) => ({ default: m.MatchAnalysisModal }))
);

export function ScholarshipSearchPage() {
  const navigate = useNavigate();
  const { user, authHeaders } = useAuth();
  const searchInputRef = useRef<HTMLInputElement>(null);

  const {
    query,
    setQuery,
    filters,
    sortBy,
    setSortBy,
    page,
    setPage,
    results,
    total,
    totalPages,
    loading,
    error,
    usingCached,
    suggestions,
    suggestionsOpen,
    setSuggestionsOpen,
    highlightIndex,
    suggestionsRef,
    handleSuggestionSelect,
    handleSearchSubmit,
    handleKeyDown,
    handleFiltersChange,
    clearQuery,
  } = useScholarshipSearch({
    limit: 20,
    enableSuggestions: true,
    syncUrlQuery: true,
    syncUrlSort: true,
  });

  const [selectedScholarship, setSelectedScholarship] = useState<ScholarshipInfo | null>(null);
  const [analysisMatch, setAnalysisMatch] = useState<MatchResult | null>(null);
  const [analysisExplanation, setAnalysisExplanation] = useState<EligibilityExplanation | null>(null);
  const [analysisExplanationLoading, setAnalysisExplanationLoading] = useState(false);
  const [analysisExplanationError, setAnalysisExplanationError] = useState<string | null>(null);
  const [analysisNotCalculated, setAnalysisNotCalculated] = useState(false);
  /** Cached bulk matches for “Check my match” (single API shape, client-side lookup). */
  const [matchCache, setMatchCache] = useState<Map<number, MatchResult> | null>(null);
  const [checkingMatchId, setCheckingMatchId] = useState<number | null>(null);
  const [checkMatchLoading, setCheckMatchLoading] = useState(false);
  const [checkMatchError, setCheckMatchError] = useState<string | null>(null);
  const [findMatchesNavLoading, setFindMatchesNavLoading] = useState(false);
  const [profileReady, setProfileReady] = useState<boolean | null>(null);
  const activeFilterChips = buildActiveFilterChips(filters, query);
  const restrictiveHint = mostRestrictiveFilterHint(filters);
  const resultCountMessage =
    loading || error
      ? ""
      : `${total} scholarship${total !== 1 ? "s" : ""} found`;

  useEffect(() => {
    if (!user) {
      setProfileReady(null);
      return;
    }
    let cancelled = false;
    apiFetch("/api/v1/profiles/me", { headers: authHeaders() })
      .then((res) => {
        if (!cancelled) setProfileReady(res.ok);
      })
      .catch(() => {
        if (!cancelled) setProfileReady(false);
      });
    return () => {
      cancelled = true;
    };
  }, [user, authHeaders]);

  const showFindMatchesCta = Boolean(user && profileReady !== false);

  const inflightMatchMap = useRef<Promise<Map<number, MatchResult>> | null>(null);

  const handleAnalysisOpenChange = useCallback((open: boolean) => {
    if (!open) {
      setAnalysisMatch(null);
      setAnalysisExplanation(null);
      setAnalysisExplanationLoading(false);
      setAnalysisExplanationError(null);
      setAnalysisNotCalculated(false);
    }
  }, []);

  const handleGoToMatches = useCallback(async () => {
    if (!user) {
      navigate("/login", { state: { from: "/scholarships/search" } });
      return;
    }
    setFindMatchesNavLoading(true);
    try {
      const res = await apiFetch("/api/v1/profiles/me", { headers: authHeaders() });
      if (res.status === 404) {
        navigate("/profile-builder");
        return;
      }
      if (!res.ok) throw new Error("Could not load your profile.");
      const profile = (await res.json()) as { id: number };
      if (!profile?.id) {
        navigate("/profile-builder");
        return;
      }
      const runRes = await apiFetch("/api/v1/match-runs", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ profile_id: profile.id }),
      });
      if (!runRes.ok) {
        const data = await runRes.json().catch(() => null);
        throw new Error((data as { detail?: string })?.detail ?? "Could not run matches.");
      }
      const data = (await runRes.json()) as { run_id: number };
      navigate(`/match/${profile.id}?run=${data.run_id}`);
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
        const res = await apiFetch("/api/v1/profiles/me", { headers: authHeaders() });
        if (res.status === 404) {
          navigate("/profile-builder");
          throw new Error("PROFILE_REQUIRED");
        }
        if (!res.ok) throw new Error("Could not load your profile.");
        const prof = (await res.json()) as { id: number };
        if (!prof?.id) {
          navigate("/profile-builder");
          throw new Error("PROFILE_REQUIRED");
        }
        const profileId = prof.id;
        const mRes = await apiFetch(`/api/v1/plan/${profileId}?limit=500`, { headers: authHeaders() });
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
      setAnalysisExplanation(null);
      setAnalysisExplanationError(null);
      setAnalysisExplanationLoading(true);
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

      try {
        const profRes = await apiFetch("/api/v1/profiles/me", { headers: authHeaders() });
        if (profRes.status === 404) {
          navigate("/profile-builder");
          return;
        }
        if (!profRes.ok) throw new Error("Could not load your profile.");
        const prof = (await profRes.json()) as { id: number };
        if (!prof?.id) {
          navigate("/profile-builder");
          return;
        }

        const [map, eligRes] = await Promise.all([
          getOrFetchMatchMap(),
          apiFetch(`/api/v1/scholarships/${scholarshipId}/eligibility?profile_id=${prof.id}`, {
            headers: authHeaders(),
          }),
        ]);

        if (!eligRes.ok) {
          const data = await eligRes.json().catch(() => null);
          throw new Error((data as { detail?: string })?.detail ?? "Could not load eligibility details.");
        }
        const explanation = (await eligRes.json()) as EligibilityExplanation;
        setAnalysisExplanation(explanation);

        const found = map.get(scholarshipId);
        if (found) {
          setAnalysisNotCalculated(false);
          setAnalysisMatch(found);
        } else {
          setAnalysisNotCalculated(true);
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
        const message = e instanceof Error ? e.message : "Failed to load match.";
        setCheckMatchError(message);
        setAnalysisExplanationError(message);
      } finally {
        setCheckMatchLoading(false);
        setAnalysisExplanationLoading(false);
        setCheckingMatchId(null);
      }
    },
    [user, navigate, results, getOrFetchMatchMap, authHeaders]
  );

  return (
    <section id="scholarship-search" className="py-8">
      <LiveRegion message={resultCountMessage} />
      <div className="mx-auto w-full max-w-none px-4 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <h1 className="sr-only">Scholarships</h1>

          <form onSubmit={handleSearchSubmit} className="relative min-w-0 flex-1">
            <label htmlFor="search-input" className="sr-only">
              Search scholarship names
            </label>
            <input
              ref={searchInputRef}
              id="search-input"
              type="text"
              role="combobox"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => query.trim() && suggestions.length > 0 && setSuggestionsOpen(true)}
              onBlur={() => setTimeout(() => setSuggestionsOpen(false), 150)}
              onKeyDown={handleKeyDown}
              placeholder="e.g. DOST, CHED, Merit"
              className="focus-visible-ring w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-4 py-3 pr-12 text-slate-900 dark:text-slate-100 placeholder-slate-500 outline-none transition focus:border-primary-500"
              autoComplete="off"
              aria-autocomplete="list"
              aria-expanded={suggestionsOpen}
              aria-controls="search-input-listbox"
              aria-activedescendant={
                highlightIndex >= 0 ? `search-input-opt-${highlightIndex}` : undefined
              }
            />
            {suggestionsOpen && suggestions.length > 0 && (
              <ul
                ref={suggestionsRef}
                id="search-input-listbox"
                role="listbox"
                className="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 py-1 shadow-lg"
              >
                {suggestions.map((item, i) => (
                  <li
                    key={item}
                    id={`search-input-opt-${i}`}
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

          <div className="flex shrink-0 flex-wrap items-center gap-2 sm:justify-end">
            {showFindMatchesCta ? (
              <Button type="button" onClick={handleGoToMatches} disabled={findMatchesNavLoading}>
                {findMatchesNavLoading ? "Opening…" : "Find my matches"}
              </Button>
            ) : null}
            <Button variant="outline" asChild>
              <Link
                to={user ? "/profile-builder" : "/login"}
                state={user ? undefined : { from: "/scholarships/search" }}
              >
                Complete your profile
              </Link>
            </Button>
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

        <div className="mb-4 lg:hidden">
          <ScholarshipSearchFilters filters={filters} onChange={handleFiltersChange} variant="drawer" />
        </div>

        <div className="flex flex-col gap-6 lg:flex-row">
          <div className="hidden lg:block lg:w-64 lg:shrink-0">
            <p className="mb-3 text-sm text-slate-600 dark:text-slate-400">
              Narrow by region, level, or field. <StatusGuideLink />
            </p>
            <ScholarshipSearchFilters filters={filters} onChange={handleFiltersChange} variant="sidebar" />
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

            {usingCached && !loading ? (
              <div
                className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100"
                role="status"
              >
                Showing saved results from your last visit. Reconnect to refresh the catalog.
              </div>
            ) : null}

            {error && (
              <StateMessage
                copy={ERROR_COPY.load_failed}
                action={
                  <button
                    type="button"
                    onClick={() => window.location.reload()}
                    className="rounded-xl bg-primary-600 px-5 py-3 text-sm font-semibold text-white hover:bg-primary-700"
                  >
                    {ERROR_COPY.load_failed.recoveryAction}
                  </button>
                }
              />
            )}

            {!loading && !error && (
              <>
                <SearchResultsHeader
                  total={total}
                  query={query}
                  sortBy={sortBy}
                  onSortChange={setSortBy}
                  filters={filters}
                  onFiltersChange={handleFiltersChange}
                  onClearQuery={clearQuery}
                />

                {results.length === 0 ? (
                  <StateMessage
                    copy={{
                      ...ERROR_COPY.search_no_results,
                      message: restrictiveHint
                        ? `${ERROR_COPY.search_no_results.message} ${restrictiveHint}`
                        : ERROR_COPY.search_no_results.message,
                    }}
                    action={
                      activeFilterChips.length > 0 ? (
                        <button
                          type="button"
                          onClick={() => {
                            clearQuery();
                            handleFiltersChange({});
                          }}
                          className="rounded-xl bg-primary-600 px-5 py-3 text-sm font-semibold text-white hover:bg-primary-700"
                        >
                          {ERROR_COPY.search_no_results.recoveryAction}
                        </button>
                      ) : (
                        <Link
                          to="/scholarships/search"
                          className="inline-flex rounded-xl border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
                        >
                          Browse all scholarships
                        </Link>
                      )
                    }
                  />
                ) : (
                  <>
                    <div className="grid grid-cols-1 items-stretch gap-4 sm:gap-6 md:grid-cols-2 xl:grid-cols-3">
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

      <Suspense fallback={null}>
        <MatchAnalysisModal
          match={analysisMatch}
          open={analysisMatch != null}
          onOpenChange={handleAnalysisOpenChange}
          explanation={analysisExplanation}
          explanationLoading={analysisExplanationLoading}
          explanationError={analysisExplanationError}
          notCalculated={analysisNotCalculated}
        />
      </Suspense>
    </section>
  );
}
