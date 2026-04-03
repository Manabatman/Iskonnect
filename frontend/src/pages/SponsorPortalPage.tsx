import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch, NetworkError } from "../api/client";

type SponsorApp = {
  application_id: number;
  user_id: number;
  scholarship_id: number;
  status: string;
  scholarship_title: string;
  updated_at: string;
};

const STATUSES = [
  "preparing",
  "submitted",
  "under_review",
  "shortlisted",
  "accepted",
  "rejected",
  "waitlisted",
] as const;

export function SponsorPortalPage() {
  const { user, authHeaders } = useAuth();
  const [rows, setRows] = useState<SponsorApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/sponsor/applications", { headers: authHeaders() });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Could not load applications");
      }
      const data = await res.json();
      setRows(Array.isArray(data) ? data : []);
    } catch (e) {
      if (e instanceof NetworkError) setError("Could not reach the server.");
      else setError(e instanceof Error ? e.message : "Failed to load");
      setRows([]);
    } finally {
      setLoading(false);
    }
  }, [user, authHeaders]);

  useEffect(() => {
    void load();
  }, [load]);

  const updateStatus = async (applicationId: number, status: (typeof STATUSES)[number]) => {
    setBusyId(applicationId);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/sponsor/applications/${applicationId}/review`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Update failed");
      }
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Update failed");
    } finally {
      setBusyId(null);
    }
  };

  if (!user) return null;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Sponsor portal</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Applications for scholarships linked to your organization. Students are identified by user ID until a messaging
        layer ships.
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
          {error}
        </div>
      )}

      {loading ? (
        <div className="mt-8 h-40 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
      ) : rows.length === 0 ? (
        <p className="mt-8 text-slate-600 dark:text-slate-400">
          No applications yet. When scholarships are assigned to your sponsor account, incoming applications appear
          here.
        </p>
      ) : (
        <div className="mt-8 overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
          <table className="min-w-full divide-y divide-slate-200 text-sm dark:divide-slate-700">
            <thead className="bg-slate-50 dark:bg-slate-800/80">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Scholarship</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Student user</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Status</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Review</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white dark:divide-slate-700 dark:bg-slate-900/40">
              {rows.map((r) => (
                <tr key={r.application_id}>
                  <td className="px-4 py-3">
                    <p className="font-medium text-slate-900 dark:text-slate-100">{r.scholarship_title}</p>
                    <Link
                      to={`/scholarship/${r.scholarship_id}`}
                      className="text-xs text-primary-600 hover:underline dark:text-primary-400"
                    >
                      View listing
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-slate-700 dark:text-slate-300">#{r.user_id}</td>
                  <td className="px-4 py-3 text-slate-700 dark:text-slate-300">{r.status.replace(/_/g, " ")}</td>
                  <td className="px-4 py-3">
                    <select
                      value={STATUSES.includes(r.status as (typeof STATUSES)[number]) ? r.status : "under_review"}
                      disabled={busyId === r.application_id}
                      onChange={(e) => void updateStatus(r.application_id, e.target.value as (typeof STATUSES)[number])}
                      className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
                      aria-label="Set application status"
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s.replace(/_/g, " ")}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
