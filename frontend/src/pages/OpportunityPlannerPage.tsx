import { useCallback, useEffect, useState, lazy, Suspense } from "react";
import { Link, useParams } from "react-router-dom";
import type { MatchResult, OpportunityTimeline, PlanResponse, ProfileCompleteness } from "../types";
import { getNetworkErrorMessage, resolveUserErrorMessage } from "../constants/errorCopy";
import { NetworkError, apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import { OpportunityTimelineView } from "../components/OpportunityTimeline";
import { OpportunityCalendarView } from "../components/OpportunityCalendarView";
import { ProfileQualityCard } from "../components/ProfileQualityCard";
import { ExcludedScholarshipsPanel } from "../components/ExcludedScholarshipsPanel";
import type { MatchDiagnostics } from "../types";

const MatchAnalysisModal = lazy(() =>
  import("../components/MatchAnalysisModal").then((m) => ({ default: m.MatchAnalysisModal }))
);

function fetchErrorMessage(err: unknown): string {
  if (err instanceof NetworkError) return getNetworkErrorMessage();
  return resolveUserErrorMessage(err, "load_failed");
}

export function OpportunityPlannerPage() {
  const { profileId } = useParams<{ profileId: string }>();
  const { authHeaders } = useAuth();
  const [timeline, setTimeline] = useState<OpportunityTimeline | null>(null);
  const [profileCompleteness, setProfileCompleteness] = useState<ProfileCompleteness | null>(null);
  const [diagnostics, setDiagnostics] = useState<MatchDiagnostics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysisMatch, setAnalysisMatch] = useState<MatchResult | null>(null);

  useEffect(() => {
    if (!profileId) {
      setLoading(false);
      setError("Invalid profile");
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFetch(`/api/v1/plan/${profileId}`, { headers: authHeaders() })
      .then((res) => {
        if (res.status === 401 || res.status === 403) {
          throw new Error("Session expired or not authorized. Please sign in again.");
        }
        if (!res.ok) throw new Error("Unable to load your opportunity plan");
        return res.json() as Promise<PlanResponse>;
      })
      .then((data) => {
        if (cancelled) return;
        setTimeline(data.timeline ?? null);
        setProfileCompleteness(data.profile_completeness ?? null);
        setDiagnostics(data.diagnostics ?? null);
      })
      .catch((err) => {
        if (!cancelled) setError(fetchErrorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [profileId, authHeaders]);

  const handleAnalysisOpenChange = useCallback((open: boolean) => {
    if (!open) setAnalysisMatch(null);
  }, []);

  if (loading) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <p className="text-sm text-slate-600 dark:text-slate-400">Loading your opportunity planner…</p>
        </div>
      </section>
    );
  }

  if (error || !timeline) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <div className="rounded-xl border border-red-200 bg-red-50 p-8 text-center dark:border-red-800 dark:bg-red-950/40">
            <p className="font-medium text-red-800 dark:text-red-200">{error ?? "Plan unavailable"}</p>
            <Link
              to="/profile-builder"
              className="mt-4 inline-block rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
            >
              Update profile
            </Link>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12">
      <div className="mx-auto max-w-6xl space-y-8 px-4">
        <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Opportunity planner</h1>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              Timeline and calendar for scholarships tied to your profile — open windows, prep time, and future cycles.
            </p>
          </div>
          <Link
            to={`/match/${profileId}`}
            className="text-sm font-semibold text-primary-600 hover:underline dark:text-primary-400"
          >
            View match results →
          </Link>
        </header>

        <ProfileQualityCard completeness={profileCompleteness} />

        <OpportunityTimelineView timeline={timeline} onShowAnalysis={setAnalysisMatch} />

        <OpportunityCalendarView timeline={timeline} />

        <ExcludedScholarshipsPanel diagnostics={diagnostics} profileId={profileId} />
      </div>

      <Suspense fallback={null}>
        <MatchAnalysisModal match={analysisMatch} open={analysisMatch != null} onOpenChange={handleAnalysisOpenChange} />
      </Suspense>
    </section>
  );
}
