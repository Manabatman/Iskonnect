import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch, NetworkError } from "../api/client";
import type { SavedScholarship } from "../types";

const STATUS_STORAGE_KEY = "iskonnect_application_status_v1";

export type ApplicationStatus = "not_started" | "pending" | "applied" | "rejected";

function loadStatusMap(): Record<number, ApplicationStatus> {
  try {
    const raw = localStorage.getItem(STATUS_STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as Record<string, string>;
    const out: Record<number, ApplicationStatus> = {};
    for (const [k, v] of Object.entries(parsed)) {
      const id = Number(k);
      if (!Number.isFinite(id)) continue;
      if (v === "not_started" || v === "pending" || v === "applied" || v === "rejected") {
        out[id] = v;
      }
    }
    return out;
  } catch {
    return {};
  }
}

function saveStatusMap(map: Record<number, ApplicationStatus>) {
  try {
    const serial: Record<string, string> = {};
    for (const [k, v] of Object.entries(map)) {
      serial[String(k)] = v;
    }
    localStorage.setItem(STATUS_STORAGE_KEY, JSON.stringify(serial));
  } catch {
    /* ignore */
  }
}

const statusLabel: Record<ApplicationStatus, string> = {
  not_started: "Not started",
  pending: "Pending",
  applied: "Applied",
  rejected: "Rejected",
};

function StatusChip({ status }: { status: ApplicationStatus }) {
  const styles: Record<ApplicationStatus, string> = {
    not_started: "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200",
    pending: "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-100",
    applied: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-100",
    rejected: "bg-red-100 text-red-900 dark:bg-red-900/40 dark:text-red-100",
  };
  return (
    <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${styles[status]}`}>
      {statusLabel[status]}
    </span>
  );
}

export function ApplicationsPage() {
  const { user, authHeaders } = useAuth();
  const [saved, setSaved] = useState<SavedScholarship[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusByScholarshipId, setStatusByScholarshipId] = useState<Record<number, ApplicationStatus>>(() =>
    loadStatusMap()
  );

  useEffect(() => {
    if (!user) return;
    setLoading(true);
    setError(null);
    apiFetch("/api/v1/saved-scholarships", { headers: authHeaders() })
      .then((r) => (r.ok ? r.json() : { saved: [] }))
      .then((data: { saved?: SavedScholarship[] }) => {
        const list = Array.isArray(data.saved) ? data.saved : [];
        setSaved(list);
      })
      .catch((e) => {
        if (e instanceof NetworkError) setError("Could not reach the server.");
        else setError("Failed to load saved scholarships.");
      })
      .finally(() => setLoading(false));
  }, [user, authHeaders]);

  const setStatus = useCallback((scholarshipId: number, status: ApplicationStatus) => {
    setStatusByScholarshipId((prev) => {
      const next = { ...prev, [scholarshipId]: status };
      saveStatusMap(next);
      return next;
    });
  }, []);

  const rows = useMemo(() => {
    return saved.map((item) => {
      const sid = item.scholarship_id;
      const status = statusByScholarshipId[sid] ?? "not_started";
      const docs = item.scholarship?.required_documents?.length ?? 0;
      return {
        item,
        status,
        docs,
        deadline: item.scholarship?.application_deadline,
      };
    });
  }, [saved, statusByScholarshipId]);

  if (!user) return null;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Applications</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Track application status for scholarships you&apos;ve saved. Status is stored on this device until we add a
        server-backed workflow.
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
          No saved scholarships yet.{" "}
          <Link to="/scholarships/search" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Browse scholarships
          </Link>{" "}
          and save programs you plan to apply to.
        </p>
      ) : (
        <div className="mt-8 overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
          <table className="min-w-full divide-y divide-slate-200 text-sm dark:divide-slate-700">
            <thead className="bg-slate-50 dark:bg-slate-800/80">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Scholarship</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Deadline</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Documents</th>
                <th className="px-4 py-3 text-left font-semibold text-slate-900 dark:text-slate-100">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white dark:divide-slate-700 dark:bg-slate-900/40">
              {rows.map(({ item, status, docs, deadline }) => (
                <tr key={item.id}>
                  <td className="px-4 py-3">
                    <Link
                      to={`/scholarship/${item.scholarship_id}`}
                      className="font-medium text-primary-600 hover:underline dark:text-primary-400"
                    >
                      {item.scholarship?.title ?? `Scholarship #${item.scholarship_id}`}
                    </Link>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{item.scholarship?.provider ?? "—"}</p>
                  </td>
                  <td className="px-4 py-3 text-slate-700 dark:text-slate-300">
                    {deadline ? new Date(deadline).toLocaleDateString(undefined, { dateStyle: "medium" }) : "—"}
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      to={`/scholarship/${item.scholarship_id}#requirements`}
                      className="text-primary-600 hover:underline dark:text-primary-400"
                    >
                      {docs} required
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
                      <StatusChip status={status} />
                      <select
                        value={status}
                        onChange={(e) => setStatus(item.scholarship_id, e.target.value as ApplicationStatus)}
                        className="rounded-lg border border-slate-300 bg-white px-2 py-1 text-xs dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
                        aria-label="Update application status"
                      >
                        <option value="not_started">Not started</option>
                        <option value="pending">Pending</option>
                        <option value="applied">Applied</option>
                        <option value="rejected">Rejected</option>
                      </select>
                    </div>
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
