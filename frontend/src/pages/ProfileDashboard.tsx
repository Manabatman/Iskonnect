import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AUTH_USER_CHANGED_EVENT, useAuth } from "../contexts/AuthContext";
import { useSavedScholarships } from "../contexts/SavedScholarshipsContext";
import type { MatchResult, MatchRunSummary, ProfileCompleteness, StudentProfileResponse } from "../types";
import { NetworkError, apiFetch } from "../api/client";
import { ProfileQualityCard } from "../components/ProfileQualityCard";
import { formatDateMedium, formatDateTime, formatRelativeManila, startOfTodayManila } from "../utils/formatDate";
import { formatDeadlineDisplay } from "../utils/formatDeadline";
import { markLoginFlow, measureLoginFlow } from "../utils/perfTiming";
import { MatchScoreRing } from "../components/MatchScoreRing";
import { QualificationStatusBadge } from "../components/QualificationStatusBadge";
import { LifecycleStatusBadge } from "../components/LifecycleStatusBadge";

function IconGraduationCap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 3L2 8l10 5 10-5-10-5zM2 13l10 5 10-5M2 18l10 5 10-5"
        stroke="currentColor"
        strokeWidth={1.75}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconTrash({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
      />
    </svg>
  );
}

function insertRunSorted(prev: MatchRunSummary[], run: MatchRunSummary): MatchRunSummary[] {
  const merged = [...prev, run];
  merged.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  return merged;
}

function deadlineUrgency(deadlineIso: string | null | undefined): "soon" | "upcoming" | "later" | null {
  if (!deadlineIso) return null;
  try {
    const d = new Date(deadlineIso);
    const today = startOfTodayManila();
    const diffDays = Math.ceil((d.getTime() - today.getTime()) / 86400000);
    if (diffDays < 0) return null;
    if (diffDays <= 7) return "soon";
    if (diffDays <= 30) return "upcoming";
    return "later";
  } catch {
    return null;
  }
}


export function ProfileDashboard() {
  const { user, authHeaders } = useAuth();
  const navigate = useNavigate();
  const [profile, setProfile] = useState<StudentProfileResponse | null>(null);
  const [runs, setRuns] = useState<MatchRunSummary[]>([]);
  const [latestMatches, setLatestMatches] = useState<MatchResult[]>([]);
  const [latestMatchesLoading, setLatestMatchesLoading] = useState(false);
  const [matchProfileCompleteness, setMatchProfileCompleteness] = useState<ProfileCompleteness | null>(null);
  const [selectedRuns, setSelectedRuns] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [runLoading, setRunLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toggleSave, savedScholarships, savedListLoading: savedLoading } = useSavedScholarships();

  useEffect(() => {
    if (!user) return;
    setProfile(null);
    setRuns([]);
    setLatestMatches([]);
    setSelectedRuns(new Set());
    setError(null);
    setLoading(true);
    const headers = authHeaders();
    Promise.all([
      apiFetch("/api/v1/profiles/me", { headers }).then((r) => {
        if (r.status === 404) return null;
        return r.ok ? r.json() : null;
      }),
      apiFetch("/api/v1/match-runs", { headers }).then((r) => (r.ok ? r.json() : [])),
    ])
      .then(([profData, runsData]) => {
        setProfile(
          profData && typeof profData === "object" && "id" in profData
            ? (profData as StudentProfileResponse)
            : null
        );
        setRuns(Array.isArray(runsData) ? runsData : []);
      })
      .catch((err) => {
        if (err instanceof NetworkError) {
          setError(
            "Unable to reach the server. Check that the API is running and VITE_API_BASE_URL matches your backend."
          );
        } else {
          setError("Failed to load data");
        }
      })
      .finally(() => {
        setLoading(false);
        markLoginFlow("dashboard-data");
        measureLoginFlow("submit-to-dashboard-data", "submit", "dashboard-data");
      });
  }, [user?.id, authHeaders]);

  useEffect(() => {
    if (!profile?.id) {
      setMatchProfileCompleteness(null);
      return;
    }
    let cancelled = false;
    apiFetch(`/api/v1/plan/${profile.id}`, { headers: authHeaders() })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!cancelled && data?.profile_completeness) {
          setMatchProfileCompleteness(data.profile_completeness);
        }
      })
      .catch(() => {
        if (!cancelled) setMatchProfileCompleteness(null);
      });
    return () => {
      cancelled = true;
    };
  }, [profile?.id, authHeaders]);

  useEffect(() => {
    const onAuthChange = () => {
      setProfile(null);
      setRuns([]);
      setLatestMatches([]);
      setSelectedRuns(new Set());
      setError(null);
    };
    window.addEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
    return () => window.removeEventListener(AUTH_USER_CHANGED_EVENT, onAuthChange);
  }, []);

  useEffect(() => {
    if (!user || runs.length === 0) {
      setLatestMatches([]);
      return;
    }
    const runId = runs[0].id;
    let cancelled = false;
    setLatestMatchesLoading(true);
    apiFetch(`/api/v1/match-runs/${runId}`, { headers: authHeaders() })
      .then((r) => (r.ok ? r.json() : null))
      .then((data: { results?: MatchResult[] } | null) => {
        if (cancelled || !data?.results) return;
        setLatestMatches(data.results.slice(0, 5));
      })
      .catch(() => {
        if (!cancelled) setLatestMatches([]);
      })
      .finally(() => {
        if (!cancelled) setLatestMatchesLoading(false);
        if (!cancelled) {
          markLoginFlow("dashboard-matches");
          measureLoginFlow("submit-to-dashboard-matches", "submit", "dashboard-matches");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [user, authHeaders, runs]);

  const handleRunMatches = async () => {
    const p = profile;
    if (!p) {
      setError("Complete your profile first");
      return;
    }
    setError(null);
    setRunLoading(true);
    try {
      const res = await apiFetch("/api/v1/match-runs", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ profile_id: p.id }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to run matches");
      }
      const data = await res.json();
      setRuns((prev) => [
        {
          id: data.run_id,
          profile_id: data.profile_id,
          created_at: data.created_at,
          ph_created_at: data.ph_created_at ?? null,
          result_count: data.matches?.length ?? 0,
        },
        ...prev,
      ]);
      if (Array.isArray(data.matches)) {
        setLatestMatches(data.matches.slice(0, 5));
      }
      navigate(`/match/${p.id}?run=${data.run_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to run matches");
    } finally {
      setRunLoading(false);
    }
  };

  const toggleRunSelection = (id: number) => {
    setSelectedRuns((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleCompare = () => {
    const arr = Array.from(selectedRuns);
    if (arr.length !== 2) {
      setError("Select exactly 2 runs to compare");
      return;
    }
    navigate(`/match-compare?run_a=${arr[0]}&run_b=${arr[1]}`);
  };

  const handleDeleteMatchRun = async (run: MatchRunSummary) => {
    setRuns((prev) => prev.filter((r) => r.id !== run.id));
    setSelectedRuns((prev) => {
      const next = new Set(prev);
      next.delete(run.id);
      return next;
    });
    try {
      const res = await apiFetch(`/api/v1/match-runs/${run.id}`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      if (!res.ok) throw new Error("Delete failed");
    } catch {
      setRuns((prev) => (prev.some((r) => r.id === run.id) ? prev : insertRunSorted(prev, run)));
    }
  };

  const handleClearAllMatchRuns = async () => {
    if (!window.confirm("Remove all runs from your match history?")) return;
    const snapshot = [...runs];
    setRuns([]);
    setSelectedRuns(new Set());
    await Promise.all(
      snapshot.map((run) =>
        apiFetch(`/api/v1/match-runs/${run.id}`, { method: "DELETE", headers: authHeaders() }).catch(() => null)
      )
    );
    const res = await apiFetch("/api/v1/match-runs", { headers: authHeaders() });
    if (res.ok) {
      const data = await res.json();
      setRuns(Array.isArray(data) ? data : []);
    } else {
      setRuns(snapshot);
    }
  };

  const formatRunDate = (run: MatchRunSummary) => {
    const s = run.ph_created_at ?? run.created_at;
    return formatDateTime(s);
  };

  const upcomingDeadlines = useMemo(() => {
    const today = startOfTodayManila();
    today.setHours(0, 0, 0, 0);
    return savedScholarships
      .map((item) => ({
        ...item,
        deadline: item.scholarship?.application_deadline
          ? new Date(item.scholarship.application_deadline)
          : null,
      }))
      .filter((x) => x.deadline && x.deadline >= today)
      .sort((a, b) => (a.deadline!.getTime() - b.deadline!.getTime()))
      .slice(0, 5);
  }, [savedScholarships]);

  const reminders = useMemo(() => {
    const today = startOfTodayManila();
    const in14 = new Date(today);
    in14.setDate(in14.getDate() + 14);
    return upcomingDeadlines.filter((x) => x.deadline && x.deadline <= in14);
  }, [upcomingDeadlines]);

  if (!user) return null;

  const displayName = profile?.full_name?.trim() || "there";
  const qualityPercent =
    matchProfileCompleteness?.quality_percent ??
    (matchProfileCompleteness && matchProfileCompleteness.total_fields > 0
      ? Math.round(
          (matchProfileCompleteness.filled_fields / matchProfileCompleteness.total_fields) * 100
        )
      : 0);
  const profileNeedsWork = qualityPercent < 100;
  const topThree = latestMatches.slice(0, 3);

  return (
    <section className="py-8 sm:py-12">
      <div className="mx-auto max-w-7xl px-4">
        {error && (
          <div
            className="mb-6 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-800 dark:bg-red-900/30 dark:text-red-300"
            role="alert"
          >
            {error}
          </div>
        )}
        {user && user.requireEmailVerification && !user.emailVerified && (
          <div
            className="mb-6 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-900/30 dark:text-amber-200"
            role="status"
          >
            Please verify your email — check your inbox for the verification link from Iskonnect.
            {" "}
            <button
              type="button"
              className="font-semibold underline"
              onClick={async () => {
                try {
                  await apiFetch("/api/v1/auth/resend-verification", {
                    method: "POST",
                    headers: authHeaders(),
                  });
                } catch {
                  /* generic UX — server always returns 200 when authenticated */
                }
              }}
            >
              Resend verification email
            </button>
          </div>
        )}

        <div className="lg:grid lg:grid-cols-3 lg:gap-8 lg:items-start">
          <div className="min-w-0 space-y-8 lg:col-span-2">
            {/* Welcome */}
            <div className="glass overflow-hidden rounded-2xl p-6 shadow-sm">
              <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0 flex-1">
                  <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    Welcome back, {displayName}
                  </h2>
                  <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                    {profile
                      ? "Run a match to see scholarships you qualify for, or browse the catalog."
                      : "Complete your profile to unlock personalized matching."}
                  </p>
                </div>
                <div className="flex shrink-0 flex-col gap-2 sm:items-stretch sm:text-right">
                  {!profile ? (
                    <Link
                      to="/profile-builder"
                      className="inline-flex items-center justify-center rounded-2xl bg-primary-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-primary-600/25 transition hover:bg-primary-700"
                    >
                      Complete your profile
                    </Link>
                  ) : (
                    <button
                      type="button"
                      onClick={handleRunMatches}
                      disabled={loading || runLoading}
                      className="inline-flex items-center justify-center rounded-2xl bg-primary-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-primary-600/25 transition hover:bg-primary-700 disabled:opacity-50"
                    >
                      {runLoading ? "Running…" : runs.length === 0 ? "Run your first match" : "Find my matches"}
                    </button>
                  )}
                  <Link
                    to="/scholarships/search"
                    className="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-5 py-2.5 text-sm font-semibold text-slate-800 transition hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
                  >
                    Browse opportunities
                  </Link>
                  {profile?.id ? (
                    <Link
                      to={`/planner/${profile.id}`}
                      className="inline-flex items-center justify-center rounded-2xl border border-primary-200 bg-primary-50 px-5 py-2.5 text-sm font-semibold text-primary-800 transition hover:bg-primary-100 dark:border-primary-800 dark:bg-primary-950/40 dark:text-primary-200 dark:hover:bg-primary-900/50"
                    >
                      Opportunity planner
                    </Link>
                  ) : null}
                </div>
              </div>
            </div>

            <ProfileQualityCard completeness={matchProfileCompleteness} />

            {/* Next steps: applications + documents — 2-col when Profile card hidden to avoid empty third column */}
            <div
              className={
                profileNeedsWork
                  ? "grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
                  : "grid gap-4 sm:grid-cols-2"
              }
            >
              {profileNeedsWork ? (
                <Link
                  to="/profile-builder"
                  className="glass flex flex-col rounded-2xl p-4 transition hover:-translate-y-0.5 hover:shadow-lg"
                >
                  <span className="text-xs font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">
                    Profile
                  </span>
                  <span className="mt-1 font-semibold text-slate-900 dark:text-slate-100">Complete your profile</span>
                  <span className="mt-1 text-sm text-slate-600 dark:text-slate-400">Strengthen your match scores.</span>
                </Link>
              ) : null}
              <Link
                to="/applications"
                className="glass flex flex-col rounded-2xl p-4 transition hover:-translate-y-0.5 hover:shadow-lg"
              >
                <span className="text-xs font-semibold uppercase tracking-wide text-accent-600 dark:text-accent-400">
                  Applications
                </span>
                <span className="mt-1 font-semibold text-slate-900 dark:text-slate-100">Track applications</span>
                <span className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  Status, timelines, and per-scholarship document checklists.
                </span>
              </Link>
              <Link
                to="/documents"
                className="glass flex flex-col rounded-2xl p-4 transition hover:-translate-y-0.5 hover:shadow-lg"
              >
                <span className="text-xs font-semibold uppercase tracking-wide text-teal-600 dark:text-teal-400">
                  Documents
                </span>
                <span className="mt-1 font-semibold text-slate-900 dark:text-slate-100">Document checklist</span>
                <span className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  Per-application checklist, Drive folder links, and upload shortcuts (files stay in your Drive).
                </span>
              </Link>
            </div>

            {/* Recommended matches */}
            <div className="glass rounded-2xl p-6 shadow-md">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">Top matches</h3>
                {runs.length > 0 ? (
                  <Link
                    to={`/match/${runs[0].profile_id}?run=${runs[0].id}`}
                    className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
                  >
                    View full results
                  </Link>
                ) : null}
              </div>
              {latestMatchesLoading ? (
                <div className="mt-4 h-24 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : latestMatches.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No matches yet. Run a match to see your top scholarships here.
                </p>
              ) : (
                <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {topThree.map((m, idx) => {
                    const score = Number(m.final_score ?? m.score ?? 0);
                    const why = (m.explanation && m.explanation.length > 0 ? m.explanation.join(" ") : "") || "";
                    const deadlineLine =
                      m.application_deadline || m.deadline_precision
                        ? formatDeadlineDisplay(
                            m.application_deadline,
                            m.deadline_precision,
                            m.deadline_note,
                            m.last_verified_at
                          )
                        : null;
                    const isTop = idx === 0;
                    return (
                      <div
                        key={m.id}
                        className={[
                          "flex flex-col rounded-2xl border bg-white/70 p-4 dark:bg-slate-900/50",
                          isTop
                            ? "border-primary-400/60 shadow-lg shadow-primary-500/10 ring-2 ring-primary-500/25 dark:border-primary-500/40"
                            : "border-white/30 dark:border-slate-600",
                        ].join(" ")}
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="flex min-w-0 flex-1 gap-3">
                            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-100 text-primary-700 dark:bg-primary-900/50 dark:text-primary-300">
                              <IconGraduationCap className="h-6 w-6" />
                            </div>
                            <div className="min-w-0 flex-1">
                              {isTop ? (
                                <span className="inline-block rounded-full bg-primary-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-primary-800 dark:bg-primary-900/60 dark:text-primary-200">
                                  Top match
                                </span>
                              ) : null}
                              {m.qualification_status ? (
                                <div className="mt-1">
                                  <QualificationStatusBadge status={m.qualification_status} />
                                </div>
                              ) : null}
                              <p className="font-semibold text-slate-900 line-clamp-2 dark:text-slate-100">{m.title}</p>
                              <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400 line-clamp-1">{m.provider}</p>
                            </div>
                          </div>
                          <MatchScoreRing score={score} size={isTop ? 58 : 52} />
                        </div>
                        {deadlineLine ? (
                          <p className="mt-2 text-xs font-medium text-amber-800 dark:text-amber-200/90">{deadlineLine}</p>
                        ) : null}
                        {why ? (
                          <div className="mt-2 rounded-lg bg-slate-100/80 px-2 py-1.5 dark:bg-slate-800/80">
                            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
                              Why you matched
                            </p>
                            <p className="mt-0.5 text-xs text-slate-600 line-clamp-3 dark:text-slate-300" title={why}>
                              {why}
                            </p>
                          </div>
                        ) : null}
                        <Link
                          to={`/scholarship/${m.id}`}
                          className="mt-3 inline-flex text-sm font-semibold text-primary-600 hover:underline dark:text-primary-400"
                        >
                          View details →
                        </Link>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Saved scholarships (above match history, most recent saved first) */}
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Saved Scholarships</h3>
              {savedLoading ? (
                <div className="mt-4 h-24 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : savedScholarships.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No saved scholarships yet.{" "}
                  <Link to="/scholarships/search" className="font-medium text-primary-600 hover:text-primary-700">
                    Browse scholarships
                  </Link>{" "}
                  to save some.
                </p>
              ) : (
                <div className="mt-5 space-y-4">
                  {[...savedScholarships]
                    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                    .map((item) => {
                      const sch = item.scholarship;
                      const urgency = deadlineUrgency(sch?.application_deadline ?? null);
                      const typeLabel = sch?.scholarship_type?.trim() || "Scholarship";
                      return (
                        <div
                          key={item.id}
                          className="group relative rounded-xl border border-slate-200 bg-slate-50/50 p-4 transition hover:border-primary-300 hover:bg-white hover:shadow-md dark:border-slate-600 dark:bg-slate-900/30 dark:hover:border-primary-600/50 dark:hover:bg-slate-900/60"
                        >
                          <div className="flex flex-wrap items-start justify-between gap-3">
                            <div className="min-w-0 flex-1 space-y-2">
                              <div className="flex flex-wrap items-center gap-2">
                                <span className="inline-flex rounded-full bg-primary-100 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                                  {typeLabel}
                                </span>
                                {sch ? (
                                  <LifecycleStatusBadge
                                    application_status={sch.application_status}
                                    data_status={sch.data_status}
                                    is_active={sch.is_active}
                                    className="!text-[10px]"
                                  />
                                ) : null}
                                {urgency === "soon" ? (
                                  <span className="inline-flex rounded-full bg-red-100 px-2 py-0.5 text-[10px] font-semibold text-red-800 dark:bg-red-900/40 dark:text-red-200">
                                    Deadline soon
                                  </span>
                                ) : urgency === "upcoming" ? (
                                  <span className="inline-flex rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold text-amber-900 dark:bg-amber-900/40 dark:text-amber-100">
                                    Deadline within 30 days
                                  </span>
                                ) : urgency === "later" ? (
                                  <span className="inline-flex rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-semibold text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200">
                                    Deadline clear
                                  </span>
                                ) : null}
                              </div>
                              <Link
                                to={`/scholarship/${item.scholarship_id}`}
                                className="block font-semibold text-slate-900 hover:text-primary-600 dark:text-slate-100 dark:hover:text-primary-400"
                              >
                                {sch?.title ?? `Scholarship #${item.scholarship_id}`}
                              </Link>
                              <p className="text-sm text-slate-600 dark:text-slate-400">{sch?.provider ?? "—"}</p>
                              {sch?.application_deadline || sch?.deadline_precision ? (
                                <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
                                  {formatDeadlineDisplay(
                                    sch.application_deadline,
                                    sch.deadline_precision,
                                    sch.deadline_note,
                                    sch.last_verified_at
                                  )}
                                </p>
                              ) : null}
                            </div>
                            <div className="flex shrink-0 gap-2 opacity-100 sm:opacity-0 sm:transition sm:group-hover:opacity-100">
                              <Link
                                to={`/scholarship/${item.scholarship_id}`}
                                className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
                              >
                                View
                              </Link>
                              <button
                                type="button"
                                onClick={async () => {
                                  await toggleSave(item.scholarship_id);
                                }}
                                className="rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-semibold text-red-700 hover:bg-red-50 dark:border-red-900 dark:bg-slate-800 dark:text-red-300 dark:hover:bg-red-950/30"
                              >
                                Remove
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                </div>
              )}
            </div>

            {/* Match history */}
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Your Match History</h3>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={handleRunMatches}
                    disabled={loading || runLoading || !profile}
                    className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
                  >
                    {runLoading ? "Running..." : "Find My Matches"}
                  </button>
                  <button
                    type="button"
                    onClick={handleCompare}
                    disabled={selectedRuns.size !== 2}
                    className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-300 dark:hover:bg-slate-600"
                  >
                    Compare Selected
                  </button>
                  <button
                    type="button"
                    onClick={handleClearAllMatchRuns}
                    disabled={loading || runs.length === 0}
                    className="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 hover:text-red-600 disabled:opacity-50 dark:text-slate-400 dark:hover:text-red-400"
                  >
                    Clear All
                  </button>
                </div>
              </div>

              {loading ? (
                <div className="mt-4 h-32 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : runs.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No match runs yet. Complete your profile and run matches to see your history.
                </p>
              ) : (
                <div className="relative mt-4">
                  {runs.length > 5 ? (
                    <>
                      <div
                        className="pointer-events-none absolute inset-x-0 top-0 z-10 h-8 rounded-t-lg bg-gradient-to-b from-white to-transparent dark:from-slate-800"
                        aria-hidden
                      />
                      <div
                        className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-8 rounded-b-lg bg-gradient-to-t from-white to-transparent dark:from-slate-800"
                        aria-hidden
                      />
                    </>
                  ) : null}
                  <div
                    className="max-h-[360px] space-y-3 overflow-y-auto scroll-smooth pr-1 [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-slate-300 dark:[&::-webkit-scrollbar-thumb]:bg-slate-600"
                  >
                    {runs.map((run) => {
                      const runTs = run.ph_created_at ?? run.created_at;
                      return (
                        <div
                          key={run.id}
                          className="rounded-xl border border-slate-200 bg-slate-50/80 p-4 shadow-sm transition hover:border-primary-200 hover:bg-white dark:border-slate-600 dark:bg-slate-900/40 dark:hover:border-primary-800"
                        >
                          <div className="flex flex-wrap items-start gap-3">
                            <input
                              type="checkbox"
                              checked={selectedRuns.has(run.id)}
                              onChange={() => toggleRunSelection(run.id)}
                              className="mt-1 rounded border-slate-300 text-primary-600"
                              aria-label="Select for compare"
                            />
                            <div className="min-w-0 flex-1">
                              <p className="text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
                                {formatRelativeManila(runTs)}
                              </p>
                              <p className="mt-0.5 text-base font-semibold text-slate-900 dark:text-slate-100">
                                {formatRunDate(run)}
                              </p>
                              <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                                <span className="inline-flex items-center rounded-full bg-primary-100 px-2 py-0.5 text-xs font-bold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                                  {run.result_count} matches
                                </span>
                              </p>
                            </div>
                            <div className="flex w-full shrink-0 flex-col gap-2 sm:w-auto sm:items-end">
                              <Link
                                to={`/match/${run.profile_id}?run=${run.id}`}
                                className="inline-flex items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-center text-sm font-bold text-white shadow hover:bg-primary-700"
                              >
                                View results
                              </Link>
                              <button
                                type="button"
                                onClick={() => void handleDeleteMatchRun(run)}
                                className="text-xs font-medium text-slate-500 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400"
                                aria-label={`Delete match run from ${formatRunDate(run)}`}
                              >
                                <span className="inline-flex items-center gap-1">
                                  <IconTrash className="h-3.5 w-3.5" /> Remove run
                                </span>
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right column */}
          <aside className="mt-8 space-y-6 lg:mt-0">
            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Upcoming deadlines
              </h3>
              {savedLoading ? (
                <div className="mt-3 h-16 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : upcomingDeadlines.length === 0 ? (
                <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">No upcoming deadlines from saved items.</p>
              ) : (
                <ul className="mt-3 space-y-2 text-sm">
                  {upcomingDeadlines.map((item) => (
                    <li key={item.id}>
                      <Link
                        to={`/scholarship/${item.scholarship_id}`}
                        className="font-medium text-primary-600 hover:underline dark:text-primary-400"
                      >
                        {item.scholarship?.title ?? `#${item.scholarship_id}`}
                      </Link>
                      <p className="text-xs text-slate-500">
                        {item.scholarship?.application_deadline
                          ? formatDateMedium(item.scholarship.application_deadline)
                          : ""}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="rounded-xl border border-amber-200 bg-amber-50/80 p-5 dark:border-amber-900 dark:bg-amber-950/30">
              <h3 className="text-sm font-semibold text-amber-900 dark:text-amber-100">Reminders</h3>
              {reminders.length === 0 ? (
                <p className="mt-2 text-sm text-amber-900/80 dark:text-amber-200/90">No deadlines in the next 14 days.</p>
              ) : (
                <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-amber-950 dark:text-amber-100">
                  {reminders.map((item) => (
                    <li key={item.id}>
                      <Link to={`/scholarship/${item.scholarship_id}`} className="underline">
                        {item.scholarship?.title}
                      </Link>{" "}
                      —{" "}
                      {item.scholarship?.application_deadline || item.scholarship?.deadline_precision
                        ? formatDeadlineDisplay(
                            item.scholarship.application_deadline,
                            item.scholarship.deadline_precision,
                            item.scholarship.deadline_note,
                            item.scholarship.last_verified_at
                          )
                        : "No deadline listed"}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}
