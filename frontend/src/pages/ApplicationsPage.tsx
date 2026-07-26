import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useSavedScholarships } from "../contexts/SavedScholarshipsContext";
import { apiFetch, NetworkError } from "../api/client";
import { formatDateTimeLong } from "../utils/formatDate";
import { formatDeadlineDisplay } from "../utils/formatDeadline";

const APPLICATION_STATUSES = [
  "preparing",
  "submitted",
  "under_review",
  "shortlisted",
  "accepted",
  "rejected",
  "waitlisted",
] as const;

type ApplicationStatus = (typeof APPLICATION_STATUSES)[number];

type ApiApplication = {
  id: number;
  user_id: number;
  scholarship_id: number;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
  scholarship: {
    title?: string;
    provider?: string;
    application_deadline?: string | null;
    deadline_precision?: string | null;
    deadline_note?: string | null;
    last_verified_at?: string | null;
  } | null;
};

type StatusEvent = {
  id: number;
  from_status: string | null;
  to_status: string;
  created_at: string;
  note: string | null;
};

function statusLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function StatusChip({ status }: { status: string }) {
  const palette: Record<string, string> = {
    removed: "bg-zinc-200 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-100",
    preparing: "bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-100",
    submitted: "bg-blue-100 text-blue-900 dark:bg-blue-900/40 dark:text-blue-100",
    under_review: "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-100",
    shortlisted: "bg-violet-100 text-violet-900 dark:bg-violet-900/40 dark:text-violet-100",
    accepted: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-100",
    rejected: "bg-red-100 text-red-900 dark:bg-red-900/40 dark:text-red-100",
    waitlisted: "bg-orange-100 text-orange-900 dark:bg-orange-900/40 dark:text-orange-100",
  };
  const cls = palette[status] ?? "bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-200";
  return (
    <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${cls}`}>
      {statusLabel(status)}
    </span>
  );
}

export function ApplicationsPage() {
  const { user, authHeaders } = useAuth();
  const { savedScholarships: saved } = useSavedScholarships();
  const [applications, setApplications] = useState<ApiApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [eventsByApp, setEventsByApp] = useState<Record<number, StatusEvent[]>>({});
  const [eventsLoading, setEventsLoading] = useState<number | null>(null);
  const [creatingId, setCreatingId] = useState<number | null>(null);
  const [patchingId, setPatchingId] = useState<number | null>(null);
  const [removingId, setRemovingId] = useState<number | null>(null);

  const loadAll = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const appRes = await apiFetch("/api/v1/applications", { headers: authHeaders() });
      if (!appRes.ok) throw new Error("Failed to load applications");
      const appData = await appRes.json();
      setApplications(Array.isArray(appData) ? appData : []);
    } catch (e) {
      if (e instanceof NetworkError) setError("Could not reach the server.");
      else setError(e instanceof Error ? e.message : "Something went wrong.");
      setApplications([]);
    } finally {
      setLoading(false);
    }
  }, [user, authHeaders]);

  useEffect(() => {
    void loadAll();
  }, [loadAll]);

  const appScholarshipIds = useMemo(
    () => new Set(applications.map((a) => a.scholarship_id)),
    [applications]
  );

  const savedWithoutApplication = useMemo(
    () => saved.filter((s) => !appScholarshipIds.has(s.scholarship_id)),
    [saved, appScholarshipIds]
  );

  const patchStatus = async (applicationId: number, status: ApplicationStatus) => {
    setPatchingId(applicationId);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/applications/${applicationId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Update failed");
      }
      const updated = await res.json();
      setApplications((prev) => prev.map((a) => (a.id === applicationId ? { ...a, ...updated } : a)));
      setEventsByApp((prev) => {
        const next = { ...prev };
        delete next[applicationId];
        return next;
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Update failed");
    } finally {
      setPatchingId(null);
    }
  };

  const createFromSaved = async (scholarshipId: number) => {
    setCreatingId(scholarshipId);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/applications", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ scholarship_id: scholarshipId }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Could not create application");
      }
      const row = await res.json();
      setApplications((prev) => [row, ...prev]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not create application");
    } finally {
      setCreatingId(null);
    }
  };

  const removeEntry = async (applicationId: number) => {
    if (
      !window.confirm(
        "Delete this application permanently? Its status timeline and document checklist will be removed and cannot be recovered."
      )
    ) {
      return;
    }
    setRemovingId(applicationId);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/applications/${applicationId}`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Remove failed");
      }
      setApplications((prev) => prev.filter((a) => a.id !== applicationId));
      setEventsByApp((prev) => {
        const next = { ...prev };
        delete next[applicationId];
        return next;
      });
      if (expandedId === applicationId) setExpandedId(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Remove failed");
    } finally {
      setRemovingId(null);
    }
  };

  const toggleExpand = async (applicationId: number) => {
    if (expandedId === applicationId) {
      setExpandedId(null);
      return;
    }
    setExpandedId(applicationId);
    if (eventsByApp[applicationId]) return;
    setEventsLoading(applicationId);
    try {
      const res = await apiFetch(`/api/v1/applications/${applicationId}/events`, {
        headers: authHeaders(),
      });
      if (res.ok) {
        const data = await res.json();
        setEventsByApp((prev) => ({ ...prev, [applicationId]: Array.isArray(data) ? data : [] }));
      }
    } finally {
      setEventsLoading(null);
    }
  };

  if (!user) return null;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Applications</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Track each scholarship you&apos;re applying to. Status and history are saved to your account.
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
          {error}
        </div>
      )}

      {loading ? (
        <div className="mt-8 h-40 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
      ) : (
        <>
          {savedWithoutApplication.length > 0 ? (
            <div className="mt-8 rounded-xl border border-slate-200 bg-slate-50/80 p-4 dark:border-slate-700 dark:bg-slate-800/40">
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">Start from saved scholarships</h2>
              <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">
                Create a tracked application for programs you&apos;ve bookmarked.
              </p>
              <ul className="mt-3 space-y-2">
                {savedWithoutApplication.map((item) => (
                  <li
                    key={item.id}
                    className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 dark:border-slate-600 dark:bg-slate-900/60"
                  >
                    <div className="min-w-0">
                      <Link
                        to={`/scholarship/${item.scholarship_id}`}
                        className="font-medium text-primary-600 hover:underline dark:text-primary-400"
                      >
                        {item.scholarship?.title ?? `Scholarship #${item.scholarship_id}`}
                      </Link>
                      <p className="text-xs text-slate-500">{item.scholarship?.provider ?? "—"}</p>
                    </div>
                    <button
                      type="button"
                      disabled={creatingId === item.scholarship_id}
                      onClick={() => void createFromSaved(item.scholarship_id)}
                      className="rounded-lg bg-primary-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-primary-700 disabled:opacity-50"
                    >
                      {creatingId === item.scholarship_id ? "Creating…" : "Track application"}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {applications.length === 0 ? (
            <p className="mt-8 text-slate-600 dark:text-slate-400">
              No applications yet. Save scholarships from search, then use{" "}
              <strong className="text-slate-800 dark:text-slate-200">Track application</strong> above, or browse{" "}
              <Link to="/scholarships/search" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                scholarships
              </Link>
              .
            </p>
          ) : (
            <div className="mt-8 space-y-3">
              {applications.map((app) => {
                const sch = app.scholarship;
                const deadline = sch?.application_deadline;
                const expanded = expandedId === app.id;
                const evs = eventsByApp[app.id];
                return (
                  <div
                    key={app.id}
                    className="overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900/40"
                  >
                    <div className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between">
                      <div className="min-w-0 flex-1">
                        <Link
                          to={`/scholarship/${app.scholarship_id}`}
                          className="font-semibold text-primary-600 hover:underline dark:text-primary-400"
                        >
                          {sch?.title ?? `Scholarship #${app.scholarship_id}`}
                        </Link>
                        <p className="text-xs text-slate-500 dark:text-slate-400">{sch?.provider ?? "—"}</p>
                        <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">
                          {deadline || sch?.deadline_precision
                            ? formatDeadlineDisplay(
                                deadline,
                                sch?.deadline_precision,
                                sch?.deadline_note,
                                sch?.last_verified_at
                              )
                            : "Deadline not listed"}
                        </p>
                      </div>
                      <div className="flex flex-col gap-2 sm:items-end">
                        <StatusChip status={app.status} />
                        <div className="flex flex-wrap items-center gap-2">
                          <select
                            value={APPLICATION_STATUSES.includes(app.status as ApplicationStatus) ? app.status : "preparing"}
                            disabled={patchingId === app.id}
                            onChange={(e) => void patchStatus(app.id, e.target.value as ApplicationStatus)}
                            className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
                            aria-label="Update application status"
                          >
                            {APPLICATION_STATUSES.map((s) => (
                              <option key={s} value={s}>
                                {statusLabel(s)}
                              </option>
                            ))}
                          </select>
                          <button
                            type="button"
                            onClick={() => void toggleExpand(app.id)}
                            className="rounded-lg border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
                          >
                            {expanded ? "Hide timeline" : "Timeline"}
                          </button>
                          <Link
                            to="/documents"
                            state={{ applicationId: app.id }}
                            className="rounded-lg border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
                          >
                            Documents
                          </Link>
                          <button
                            type="button"
                            disabled={removingId === app.id}
                            onClick={() => void removeEntry(app.id)}
                            className="rounded-lg border border-red-200 px-2 py-1 text-xs font-medium text-red-700 hover:bg-red-50 disabled:opacity-50 dark:border-red-900 dark:text-red-300 dark:hover:bg-red-950/40"
                          >
                            {removingId === app.id ? "Deleting…" : "Delete"}
                          </button>
                        </div>
                      </div>
                    </div>
                    {expanded ? (
                      <div className="border-t border-slate-200 bg-slate-50 px-4 py-3 dark:border-slate-700 dark:bg-slate-800/50">
                        <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                          Status history
                        </h3>
                        {eventsLoading === app.id ? (
                          <p className="mt-2 text-sm text-slate-500">Loading…</p>
                        ) : evs && evs.length > 0 ? (
                          <ol className="mt-2 space-y-2">
                            {evs.map((ev) => (
                              <li key={ev.id} className="text-sm text-slate-700 dark:text-slate-300">
                                <span className="font-medium text-slate-900 dark:text-slate-100">
                                  {ev.from_status ? `${statusLabel(ev.from_status)} → ` : ""}
                                  {statusLabel(ev.to_status)}
                                </span>
                                <span className="ml-2 text-xs text-slate-500">
                                  {formatDateTimeLong(ev.created_at)}
                                </span>
                                {ev.note ? (
                                  <p className="mt-0.5 text-xs text-slate-600 dark:text-slate-400">{ev.note}</p>
                                ) : null}
                              </li>
                            ))}
                          </ol>
                        ) : (
                          <p className="mt-2 text-sm text-slate-500">No events yet.</p>
                        )}
                      </div>
                    ) : null}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
