import { useCallback, useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch, NetworkError } from "../api/client";

type VerificationRow = {
  id: number;
  application_id: number;
  school_id: number;
  verification_type: string;
  status: string;
  requested_at: string;
  verified_at: string | null;
  notes: string | null;
};

const OUTCOMES = ["pending", "approved", "rejected"] as const;

export function SchoolPortalPage() {
  const { user, authHeaders } = useAuth();
  const [rows, setRows] = useState<VerificationRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/school/verifications", { headers: authHeaders() });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail ?? "Could not load verifications");
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

  const patch = async (id: number, status: (typeof OUTCOMES)[number]) => {
    setBusyId(id);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/school/verifications/${id}`, {
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
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">School verification</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Review enrollment or eligibility verification requests assigned to your school.
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
          {error}
        </div>
      )}

      {loading ? (
        <div className="mt-8 h-40 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
      ) : rows.length === 0 ? (
        <p className="mt-8 text-slate-600 dark:text-slate-400">No verification requests in your queue.</p>
      ) : (
        <ul className="mt-8 space-y-3">
          {rows.map((r) => (
            <li
              key={r.id}
              className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/40"
            >
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="font-semibold text-slate-900 dark:text-slate-100">
                    Application #{r.application_id} · {r.verification_type.replace(/_/g, " ")}
                  </p>
                  <p className="text-xs text-slate-500">
                    Requested {new Date(r.requested_at).toLocaleString()}
                    {r.verified_at ? ` · Resolved ${new Date(r.verified_at).toLocaleString()}` : ""}
                  </p>
                  {r.notes ? <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{r.notes}</p> : null}
                </div>
                <select
                  value={OUTCOMES.includes(r.status as (typeof OUTCOMES)[number]) ? r.status : "pending"}
                  disabled={busyId === r.id}
                  onChange={(e) => void patch(r.id, e.target.value as (typeof OUTCOMES)[number])}
                  className="rounded-lg border border-slate-300 bg-white px-2 py-1.5 text-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
                  aria-label="Verification decision"
                >
                  {OUTCOMES.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
