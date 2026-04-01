import { useCallback, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import { BookmarkButton } from "../components/BookmarkButton";
import { MatchScoreRing } from "../components/MatchScoreRing";
import { ScholarshipSearchFilters } from "../components/ScholarshipSearchFilters";
import { ScholarshipDetailPanel } from "../components/ScholarshipDetailPanel";
import {
  getUrgencyBadgeClasses,
  getUrgencyLevel,
  WhyYouMatchedSection,
} from "../components/scholarshipMatchDisplay";
import { useAuth } from "../contexts/AuthContext";
import { useScholarshipSearch } from "../hooks/useScholarshipSearch";
import type { MatchResult, ScholarshipInfo } from "../types";

function formatDeadlineLabel(deadline: string | null | undefined): string | null {
  if (!deadline?.trim()) return null;
  try {
    const d = new Date(deadline);
    if (Number.isNaN(d.getTime())) return null;
    return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
  } catch {
    return null;
  }
}

function SearchCard({
  s,
  matchInfo,
  onSelect,
}: {
  s: ScholarshipInfo;
  matchInfo?: MatchResult | null;
  onSelect: (s: ScholarshipInfo) => void;
}) {
  const link = s.link && s.link.trim() ? s.link : "#";
  const hasLink = !!link && link.startsWith("http");
  const regions = (s.regions ?? []).map((r) => r.trim()).filter(Boolean);
  const deadlineLabel = formatDeadlineLabel(s.application_deadline);

  const urgency = matchInfo
    ? getUrgencyLevel(matchInfo.application_deadline, matchInfo.application_open_date)
    : getUrgencyLevel(s.application_deadline, s.application_open_date);
  const urgencyBadgeClasses = getUrgencyBadgeClasses(urgency.level);

  const score = matchInfo != null ? (matchInfo.final_score ?? matchInfo.score) : null;
  const likelihood =
    matchInfo?.confidence === "high"
      ? "High likelihood"
      : matchInfo?.confidence === "medium"
        ? "Moderate likelihood"
        : matchInfo?.confidence === "low"
          ? "Lower likelihood"
          : null;

  return (
    <article
      role="button"
      tabIndex={0}
      onClick={() => onSelect(s)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelect(s);
        }
      }}
      className="flex cursor-pointer flex-col rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-5 shadow-md transition hover:-translate-y-0.5 hover:shadow-lg hover:ring-2 hover:ring-primary-300 dark:hover:ring-primary-700"
      aria-labelledby={`search-card-title-${s.id}`}
    >
      <div className="flex flex-1 flex-col">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0 flex-1">
            <h3
              id={`search-card-title-${s.id}`}
              className="text-lg font-semibold text-slate-900 dark:text-slate-100"
            >
              {s.title}
            </h3>
            <p className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">{s.provider ?? "—"}</p>
            {deadlineLabel ? (
              <p className="mt-1 text-xs font-medium text-slate-600 dark:text-slate-400">Deadline: {deadlineLabel}</p>
            ) : null}
            {likelihood ? (
              <p className="mt-1 text-xs font-medium text-primary-700 dark:text-primary-300">{likelihood}</p>
            ) : null}
          </div>
          <div className="flex shrink-0 flex-col items-end gap-2">
            <BookmarkButton scholarshipId={s.id} />
            {matchInfo != null && score != null ? <MatchScoreRing score={score} size={56} /> : null}
            {matchInfo != null ? (
              <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${urgencyBadgeClasses}`}>
                {urgency.label}
              </span>
            ) : null}
          </div>
        </div>

        {s.level && (
          <span className="mt-2 w-fit rounded-full bg-primary-100 dark:bg-primary-900 px-2.5 py-0.5 text-xs font-medium text-primary-800 dark:text-primary-300">
            {s.level}
          </span>
        )}

        <p className="mt-3 line-clamp-3 text-sm text-slate-700 dark:text-slate-300">
          {s.description || "No description available."}
        </p>

        <div className="mt-3 flex flex-wrap gap-1">
          {regions.slice(0, 4).map((r) => (
            <span
              key={r}
              className="rounded-full bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs text-slate-700 dark:text-slate-300"
            >
              {r}
            </span>
          ))}
          {regions.length > 4 && (
            <span className="rounded-full bg-slate-100 dark:bg-slate-700 px-2 py-0.5 text-xs text-slate-600 dark:text-slate-400">
              +{regions.length - 4} more
            </span>
          )}
        </div>

        {(s.min_age != null || s.max_age != null) && (
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Age: {s.min_age != null ? `Min ${s.min_age}` : ""}
            {s.min_age != null && s.max_age != null && " • "}
            {s.max_age != null ? `Max ${s.max_age}` : ""}
          </p>
        )}

        {matchInfo ? <WhyYouMatchedSection match={matchInfo} /> : null}
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onSelect(s);
          }}
          className="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
        >
          View Details
        </button>
        {hasLink ? (
          <a
            href={link}
            target="_blank"
            rel="noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Apply Now
          </a>
        ) : (
          <span className="rounded-lg bg-slate-200 dark:bg-slate-600 px-4 py-2 text-sm font-medium text-slate-500 dark:text-slate-400 cursor-not-allowed">
            Link unavailable
          </span>
        )}
      </div>
    </article>
  );
}

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
  const [matchById, setMatchById] = useState<Map<number, MatchResult> | null>(null);
  const [matchLoading, setMatchLoading] = useState(false);
  const [matchError, setMatchError] = useState<string | null>(null);

  const handleFindMyMatches = useCallback(async () => {
    if (!user) {
      navigate("/login", { state: { from: "/scholarships/search" } });
      return;
    }
    setMatchLoading(true);
    setMatchError(null);
    try {
      const res = await apiFetch("/api/v1/profiles", { headers: authHeaders() });
      if (!res.ok) throw new Error("Could not load your profile.");
      const profiles = (await res.json()) as Array<{ id: number }>;
      if (!Array.isArray(profiles) || profiles.length === 0) {
        setMatchError("Create a profile first to see personalized matches.");
        return;
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
      setMatchById(next);
    } catch (e) {
      setMatchError(e instanceof Error ? e.message : "Failed to load matches.");
    } finally {
      setMatchLoading(false);
    }
  }, [user, authHeaders, navigate]);

  const clearMatchOverlay = useCallback(() => {
    setMatchById(null);
    setMatchError(null);
  }, []);

  return (
    <section id="scholarship-search" className="py-8">
      <div className="mx-auto max-w-7xl px-4">
        <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Search Scholarships</h1>
          <div className="flex flex-wrap items-center gap-3">
            {matchById != null && matchById.size > 0 ? (
              <button
                type="button"
                onClick={clearMatchOverlay}
                className="rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                Clear match overlay
              </button>
            ) : null}
            <button
              type="button"
              onClick={handleFindMyMatches}
              disabled={matchLoading}
              className="rounded-xl bg-accent-600 px-6 py-3 font-semibold text-white shadow-md transition hover:bg-accent-700 focus:outline-none focus:ring-2 focus:ring-accent-500 focus:ring-offset-2 disabled:opacity-70 dark:focus:ring-offset-slate-900"
            >
              {matchLoading ? "Loading matches…" : "Find My Matches"}
            </button>
            <Link
              to="/profile-builder"
              className="w-fit rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white shadow-md transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Complete Your Profile
            </Link>
          </div>
        </div>

        {matchError ? (
          <div
            className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100"
            role="alert"
          >
            {matchError}
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
                className="rounded-lg border border-danger-200 bg-danger-50 px-3 py-2 text-sm text-danger-700 dark:bg-danger-900/30 dark:text-danger-300"
                role="alert"
              >
                {error}
              </div>
            )}

            {!loading && !error && (
              <>
                <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
                  {total} scholarship{total !== 1 ? "s" : ""} found
                  {matchById != null && matchById.size > 0 ? (
                    <span className="ml-2 text-primary-600 dark:text-primary-400">
                      · Match scores shown where available
                    </span>
                  ) : null}
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
                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
                      {results.map((s) => (
                        <SearchCard
                          key={s.id}
                          s={s}
                          matchInfo={matchById?.get(s.id) ?? null}
                          onSelect={setSelectedScholarship}
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
    </section>
  );
}
