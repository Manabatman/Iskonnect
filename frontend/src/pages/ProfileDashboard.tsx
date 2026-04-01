import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useSavedScholarships } from "../contexts/SavedScholarshipsContext";
import type { MatchResult, MatchRunSummary, SavedScholarship, StudentProfileResponse } from "../types";
import { NetworkError, apiFetch } from "../api/client";
import { MatchScoreRing } from "../components/MatchScoreRing";

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

function formatDeadlineShort(iso: string | null | undefined): string | null {
  if (!iso) return null;
  try {
    return new Date(iso).toLocaleDateString(undefined, { dateStyle: "medium" });
  } catch {
    return null;
  }
}

function profileCompleteness(p: StudentProfileResponse | undefined): number {
  if (!p) return 0;
  const fields = [
    p.full_name,
    p.region,
    p.education_level || p.current_academic_stage,
    p.field_of_study_broad,
    p.gwa_normalized != null ? "1" : "",
    p.household_income_annual != null || p.income_bracket ? "1" : "",
  ];
  const filled = fields.filter(Boolean).length;
  return Math.round((filled / fields.length) * 100);
}

export function ProfileDashboard() {
  const { user, authHeaders } = useAuth();
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState<StudentProfileResponse[]>([]);
  const [runs, setRuns] = useState<MatchRunSummary[]>([]);
  const [latestMatches, setLatestMatches] = useState<MatchResult[]>([]);
  const [latestMatchesLoading, setLatestMatchesLoading] = useState(false);
  const [saved, setSaved] = useState<SavedScholarship[]>([]);
  const [savedLoading, setSavedLoading] = useState(true);
  const [selectedRuns, setSelectedRuns] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [runLoading, setRunLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toggleSave } = useSavedScholarships();

  const profile = profiles[0];
  const completeness = useMemo(() => profileCompleteness(profile), [profile]);

  useEffect(() => {
    if (!user) return;
    const headers = authHeaders();
    setSavedLoading(true);
    Promise.all([
      apiFetch("/api/v1/profiles", { headers }).then((r) => (r.ok ? r.json() : [])),
      apiFetch("/api/v1/match-runs", { headers }).then((r) => (r.ok ? r.json() : [])),
      apiFetch("/api/v1/saved-scholarships", { headers }).then((r) =>
        r.ok ? r.json() : { saved: [] }
      ),
    ])
      .then(([profData, runsData, savedData]) => {
        setProfiles(Array.isArray(profData) ? profData : []);
        setRuns(Array.isArray(runsData) ? runsData : []);
        const savedList = (savedData as { saved?: SavedScholarship[] }).saved;
        setSaved(Array.isArray(savedList) ? savedList : []);
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
        setSavedLoading(false);
      });
  }, [user, authHeaders]);

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
      });
    return () => {
      cancelled = true;
    };
  }, [user, authHeaders, runs]);

  const handleRunMatches = async () => {
    const p = profiles[0];
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

  const formatDate = (s: string) => {
    try {
      return new Date(s).toLocaleString();
    } catch {
      return s;
    }
  };

  const upcomingDeadlines = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return saved
      .map((item) => ({
        ...item,
        deadline: item.scholarship?.application_deadline
          ? new Date(item.scholarship.application_deadline)
          : null,
      }))
      .filter((x) => x.deadline && x.deadline >= today)
      .sort((a, b) => (a.deadline!.getTime() - b.deadline!.getTime()))
      .slice(0, 5);
  }, [saved]);

  const reminders = useMemo(() => {
    const today = new Date();
    const in14 = new Date(today);
    in14.setDate(in14.getDate() + 14);
    return upcomingDeadlines.filter((x) => x.deadline && x.deadline <= in14);
  }, [upcomingDeadlines]);

  if (!user) return null;

  const displayName = profile?.full_name?.trim() || "there";
  const strengthBarColor =
    completeness < 34 ? "bg-red-500" : completeness < 67 ? "bg-amber-500" : "bg-success-500";
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

        <div className="lg:grid lg:grid-cols-3 lg:gap-8 lg:items-start">
          <div className="min-w-0 space-y-8 lg:col-span-2">
            {/* Welcome */}
            <div className="glass overflow-hidden rounded-2xl p-6 shadow-sm">
              <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0 flex-1">
                  <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    Welcome back, {displayName}
                  </h2>
                  <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                    Profile strength:{" "}
                    <span className="font-semibold text-primary-700 dark:text-primary-300">{completeness}%</span>
                  </p>
                  <div className="mt-3 h-3 w-full max-w-md overflow-hidden rounded-full bg-slate-200 dark:bg-slate-600">
                    <div
                      className={`h-full rounded-full transition-all ${strengthBarColor}`}
                      style={{ width: `${completeness}%` }}
                    />
                  </div>
                  <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                    {completeness < 100
                      ? "Add a few details to unlock more accurate matches."
                      : "Great — your profile is in good shape for matching."}
                  </p>
                </div>
                <div className="flex shrink-0 flex-col gap-2 sm:items-stretch sm:text-right">
                  {profiles.length === 0 ? (
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
                    Browse scholarships
                  </Link>
                </div>
              </div>
            </div>

            {/* Next steps */}
            <div className="grid gap-4 sm:grid-cols-2">
              {completeness < 100 ? (
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
                <span className="mt-1 font-semibold text-slate-900 dark:text-slate-100">Track saved programs</span>
                <span className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  Status and deadlines for scholarships you bookmark.
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
                    const deadlineLabel = formatDeadlineShort(m.application_deadline);
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
                              <p className="font-semibold text-slate-900 line-clamp-2 dark:text-slate-100">{m.title}</p>
                              <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400 line-clamp-1">{m.provider}</p>
                            </div>
                          </div>
                          <MatchScoreRing score={score} size={isTop ? 58 : 52} />
                        </div>
                        {deadlineLabel ? (
                          <p className="mt-2 text-xs font-medium text-amber-800 dark:text-amber-200/90">
                            Deadline: {deadlineLabel}
                          </p>
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

            {/* Profile summary */}
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">Your profile</h3>
              {loading ? (
                <div className="mt-4 h-20 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : profiles.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No profile yet.{" "}
                  <Link to="/profile-builder" className="font-medium text-primary-600 hover:text-primary-700">
                    Complete your profile
                  </Link>
                </p>
              ) : (
                <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <p className="font-medium text-slate-900 dark:text-slate-100">{profiles[0].full_name}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {profiles[0].email} • {profiles[0].region ?? "—"} • {profiles[0].education_level ?? "—"}
                    </p>
                  </div>
                  <Link
                    to="/profile-builder"
                    className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-300 dark:hover:bg-slate-600"
                  >
                    Edit Profile
                  </Link>
                </div>
              )}
            </div>

            {/* Match history */}
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">Your Match History</h3>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleRunMatches}
                    disabled={loading || runLoading || profiles.length === 0}
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
                </div>
              </div>

              {loading ? (
                <div className="mt-4 h-32 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : runs.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No match runs yet. Complete your profile and run matches to see your history.
                </p>
              ) : (
                <div className="mt-4 space-y-2">
                  {runs.map((run) => (
                    <div
                      key={run.id}
                      className="flex items-center gap-4 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                    >
                      <input
                        type="checkbox"
                        checked={selectedRuns.has(run.id)}
                        onChange={() => toggleRunSelection(run.id)}
                        className="rounded border-slate-300 text-primary-600"
                      />
                      <div className="flex-1">
                        <span className="font-medium text-slate-900 dark:text-slate-100">
                          {formatDate(run.created_at)}
                        </span>
                        <span className="ml-2 text-sm text-slate-500 dark:text-slate-400">
                          {run.result_count} matches
                        </span>
                      </div>
                      <Link
                        to={`/match/${run.profile_id}?run=${run.id}`}
                        className="text-sm font-medium text-primary-600 hover:text-primary-700"
                      >
                        View Results
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Saved */}
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">Saved Scholarships</h3>
              {savedLoading ? (
                <div className="mt-4 h-24 animate-pulse rounded bg-slate-100 dark:bg-slate-700" />
              ) : saved.length === 0 ? (
                <p className="mt-4 text-slate-600 dark:text-slate-400">
                  No saved scholarships yet.{" "}
                  <Link to="/scholarships/search" className="font-medium text-primary-600 hover:text-primary-700">
                    Browse scholarships
                  </Link>{" "}
                  to save some.
                </p>
              ) : (
                <div className="mt-4 space-y-3">
                  {saved.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                    >
                      <div className="min-w-0 flex-1">
                        <Link
                          to={`/scholarship/${item.scholarship_id}`}
                          className="font-medium text-slate-900 hover:text-primary-600 dark:text-slate-100 dark:hover:text-primary-400"
                        >
                          {item.scholarship?.title ?? `Scholarship #${item.scholarship_id}`}
                        </Link>
                        <p className="text-sm text-slate-500 dark:text-slate-400">
                          {item.scholarship?.provider ?? "—"}
                          {item.scholarship?.application_deadline && (
                            <>
                              {" "}
                              • Deadline: {new Date(item.scholarship.application_deadline).toLocaleDateString()}
                            </>
                          )}
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={async () => {
                          await toggleSave(item.scholarship_id);
                          setSaved((prev) => prev.filter((x) => x.scholarship_id !== item.scholarship_id));
                        }}
                        className="shrink-0 rounded p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-700 dark:hover:text-slate-300"
                        title="Remove from saved"
                        aria-label="Remove from saved"
                      >
                        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right column */}
          <aside className="mt-8 space-y-6 lg:mt-0">
            <div className="glass rounded-2xl p-5 shadow-md">
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                At a glance
              </h3>
              <dl className="mt-3 space-y-3 text-sm">
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-3 dark:border-slate-700">
                  <dt className="text-slate-600 dark:text-slate-400">Profile strength</dt>
                  <dd className="font-semibold text-slate-900 dark:text-slate-100">{completeness}%</dd>
                </div>
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-3 dark:border-slate-700">
                  <dt className="text-slate-600 dark:text-slate-400">Saved programs</dt>
                  <dd className="font-semibold text-slate-900 dark:text-slate-100">{saved.length}</dd>
                </div>
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-3 dark:border-slate-700">
                  <dt className="text-slate-600 dark:text-slate-400">Match runs</dt>
                  <dd className="font-semibold text-slate-900 dark:text-slate-100">{runs.length}</dd>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <dt className="text-slate-600 dark:text-slate-400">Latest run results</dt>
                  <dd className="font-semibold text-slate-900 dark:text-slate-100">
                    {runs[0]?.result_count ?? "—"}
                  </dd>
                </div>
              </dl>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-md dark:border-slate-700 dark:bg-slate-800">
              <div className="flex items-center gap-3">
                <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 text-xl font-bold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                  {(profile?.full_name?.[0] || user.email?.[0] || "?").toUpperCase()}
                </div>
                <div className="min-w-0">
                  <p className="truncate font-semibold text-slate-900 dark:text-slate-100">
                    {profile?.full_name || "Your profile"}
                  </p>
                  <p className="truncate text-xs text-slate-500 dark:text-slate-400">{user.email}</p>
                </div>
              </div>
              <Link
                to="/profile-builder"
                className="mt-4 block w-full rounded-lg border border-slate-300 py-2 text-center text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-700"
              >
                Edit Profile
              </Link>
            </div>

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
                        {item.deadline?.toLocaleDateString(undefined, { dateStyle: "medium" })}
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
                      — {item.deadline?.toLocaleDateString()}
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
