import { useEffect, useState, useCallback } from "react";
import { Link, useParams, useNavigate, useSearchParams } from "react-router-dom";
import type { MatchResult, ProfileCompleteness, OpportunityTimeline, MatchDiagnostics } from "../types";
import { ScholarshipCardV2 } from "../components/ScholarshipCardV2";
import { MatchAnalysisModal } from "../components/MatchAnalysisModal";
import { OpportunityTimelineView } from "../components/OpportunityTimeline";
import { ProfileQualityCard } from "../components/ProfileQualityCard";
import { ExcludedScholarshipsPanel } from "../components/ExcludedScholarshipsPanel";
import { useAuth } from "../contexts/AuthContext";
import { NetworkError, apiFetch } from "../api/client";
import { ErrorBoundary } from "../components/ErrorBoundary";

function fetchErrorMessage(err: unknown, fallback: string): string {
  if (err instanceof NetworkError) {
    return "Unable to reach the server. Check that the API is running and VITE_API_BASE_URL is correct.";
  }
  if (err instanceof Error) {
    if (err.message === "Failed to fetch" || err.name === "TypeError") {
      return "Unable to reach the server. Check that the API is running and VITE_API_BASE_URL is correct.";
    }
    return err.message;
  }
  return fallback;
}

export function MatchResultsPage() {
  const { profileId } = useParams<{ profileId: string }>();
  const [searchParams] = useSearchParams();
  const runId = searchParams.get("run");
  const { authHeaders } = useAuth();
  const navigate = useNavigate();
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [opportunityTimeline, setOpportunityTimeline] = useState<OpportunityTimeline | null>(null);
  const [profileCompleteness, setProfileCompleteness] = useState<ProfileCompleteness | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysisMatch, setAnalysisMatch] = useState<MatchResult | null>(null);
  const [diagnostics, setDiagnostics] = useState<MatchDiagnostics | null>(null);

  useEffect(() => {
    if (runId) {
      let cancelled = false;
      setLoading(true);
      setError(null);
      apiFetch(`/api/v1/match-runs/${runId}`, {
        headers: authHeaders(),
      })
        .then((res) => {
          if (res.status === 401 || res.status === 403) {
            throw new Error("Session expired or not authorized. Please sign in again.");
          }
          if (!res.ok) throw new Error("Unable to fetch match run");
          return res.json();
        })
        .then((data) => {
          if (!cancelled) {
            setMatches(data.results ?? []);
            setOpportunityTimeline(null);
            setProfileCompleteness(null);
            setDiagnostics(null);
          }
        })
        .catch((err) => {
          if (!cancelled) setError(fetchErrorMessage(err, "Something went wrong"));
        })
        .finally(() => {
          if (!cancelled) setLoading(false);
        });
      return () => {
        cancelled = true;
      };
    }
    if (!profileId) {
      setLoading(false);
      setError("Invalid profile");
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFetch(`/api/v1/plan/${profileId}`, {
      headers: authHeaders(),
    })
      .then((res) => {
        if (res.status === 401 || res.status === 403) {
          throw new Error("Session expired or not authorized. Please sign in again.");
        }
        if (!res.ok) throw new Error("Unable to fetch matches");
        return res.json();
      })
      .then((data) => {
        if (!cancelled) {
          setMatches(data.matches ?? []);
          setOpportunityTimeline(data.timeline ?? null);
          setProfileCompleteness(data.profile_completeness ?? null);
          setDiagnostics(data.diagnostics ?? null);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(fetchErrorMessage(err, "Something went wrong"));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [profileId, runId, authHeaders]);

  const handleReset = () => navigate("/profile-builder");

  const handleAnalysisOpenChange = useCallback((open: boolean) => {
    if (!open) setAnalysisMatch(null);
  }, []);

  const activeMatches = matches.filter((m) => !m.deadline_passed);
  const deadlinePassedMatches = matches.filter((m) => m.deadline_passed);
  const hasExcluded = (diagnostics?.eliminated_scholarships ?? diagnostics?.hard_exclusions ?? []).length > 0;

  if (loading) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">Loading your match results…</p>
          <div className="animate-pulse rounded-xl border border-slate-200 bg-white p-12 dark:border-slate-700 dark:bg-slate-800">
            <div className="h-6 w-48 rounded bg-slate-200 dark:bg-slate-700" />
            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-48 rounded-lg bg-slate-100 dark:bg-slate-700" />
              ))}
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <div className="rounded-xl border border-red-200 bg-red-50 p-8 text-center dark:border-red-800 dark:bg-red-950/40">
            <p className="font-medium text-red-800 dark:text-red-200">We couldn&apos;t load your match results</p>
            <p className="mt-2 text-sm text-red-700 dark:text-red-300">{error}</p>
            <button
              type="button"
              onClick={handleReset}
              className="mt-4 rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700"
            >
              Update your profile
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="scholarships" className="py-12">
      <div className="mx-auto max-w-6xl px-4">
        <ProfileQualityCard completeness={profileCompleteness} className="mb-6" />

        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
            Your Match Results
            <span className="ml-2 rounded-full bg-primary-100 px-2.5 py-0.5 text-sm font-medium text-primary-800 dark:bg-primary-900 dark:text-primary-300">
              {opportunityTimeline?.summary.total_actionable ?? activeMatches.length}
            </span>
          </h2>
          <div className="flex flex-wrap items-center gap-3">
            {profileId && !runId ? (
              <Link
                to={`/planner/${profileId}`}
                className="text-sm font-semibold text-primary-600 hover:underline dark:text-primary-400"
              >
                Open opportunity planner →
              </Link>
            ) : null}
            <button
              type="button"
              onClick={handleReset}
              className="w-fit text-sm font-medium text-primary-600 transition hover:text-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded"
              aria-label="Update your profile"
            >
              Update Your Profile
            </button>
          </div>
        </div>

        {opportunityTimeline ? (
          <div className="mb-10">
            <OpportunityTimelineView timeline={opportunityTimeline} onShowAnalysis={setAnalysisMatch} compact />
          </div>
        ) : null}

        {hasExcluded ? (
          <ExcludedScholarshipsPanel diagnostics={diagnostics} profileId={profileId} className="mb-10" />
        ) : null}

        {matches.length === 0 && !opportunityTimeline ? (
          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-md">
            <div className="mx-auto mb-4 flex h-24 w-24 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-700">
              <svg
                className="h-12 w-12 text-slate-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <p className="text-lg font-medium text-slate-700 dark:text-slate-300">No matches yet</p>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
              No scholarships matched your profile yet—but you can unlock more. Complete missing profile fields, broaden
              your region or course interests, or browse the catalog while we add new programs.
            </p>
            {diagnostics?.total_checked != null ? (
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                Checked {diagnostics.total_checked} scholarship(s); {diagnostics.passed_hard_filters ?? 0} passed hard
                filters before scoring.
              </p>
            ) : null}
            <button
              type="button"
              onClick={handleReset}
              className="mt-6 rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              aria-label="Update your profile"
            >
              Update Your Profile
            </button>
          </div>
        ) : matches.length > 0 ? (
          <div className="space-y-10">
            {activeMatches.length > 0 ? (
              <div className="grid grid-cols-1 items-stretch gap-6 md:grid-cols-2 xl:grid-cols-3">
                {activeMatches.map((match) => (
                  <ErrorBoundary key={match.id}>
                    <ScholarshipCardV2 scholarship={match} onShowAnalysis={setAnalysisMatch} />
                  </ErrorBoundary>
                ))}
              </div>
            ) : null}

            {deadlinePassedMatches.length > 0 ? (
              <div>
                <h3 className="mb-2 text-lg font-semibold text-slate-900 dark:text-slate-100">
                  Eligible but deadline passed
                  <span className="ml-2 rounded-full bg-rose-100 px-2.5 py-0.5 text-sm font-medium text-rose-800 dark:bg-rose-900 dark:text-rose-200">
                    {deadlinePassedMatches.length}
                  </span>
                </h3>
                <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
                  These scholarships match your profile, but the application window has closed. Watch for the next cycle.
                </p>
                <div className="grid grid-cols-1 items-stretch gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {deadlinePassedMatches.map((match) => (
                    <ErrorBoundary key={`deadline-${match.id}`}>
                      <ScholarshipCardV2 scholarship={match} onShowAnalysis={setAnalysisMatch} />
                    </ErrorBoundary>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        ) : null}
      </div>

      <MatchAnalysisModal match={analysisMatch} open={analysisMatch != null} onOpenChange={handleAnalysisOpenChange} />
    </section>
  );
}
