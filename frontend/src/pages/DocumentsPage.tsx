import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch, NetworkError } from "../api/client";

type ApiApplication = {
  id: number;
  scholarship_id: number;
  status: string;
  scholarship: { title?: string; provider?: string } | null;
};

type ChecklistRow = {
  id: number;
  application_id: number;
  document_type: string;
  status: string;
  notes: string | null;
  updated_at: string;
};

const DOC_STATUSES = ["not_started", "in_progress", "ready", "submitted"] as const;

function docStatusLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function DocumentsPage() {
  const { user, authHeaders } = useAuth();
  const location = useLocation();
  const stateAppId = (location.state as { applicationId?: number } | null)?.applicationId;

  const [applications, setApplications] = useState<ApiApplication[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<number | null>(stateAppId ?? null);
  const [checklist, setChecklist] = useState<ChecklistRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [docsLoading, setDocsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [patchingDocId, setPatchingDocId] = useState<number | null>(null);

  const loadApplications = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/applications", { headers: authHeaders() });
      if (!res.ok) throw new Error("Failed to load applications");
      const data = await res.json();
      const list = Array.isArray(data) ? data : [];
      setApplications(list);
      setSelectedAppId((prev) => {
        if (prev && list.some((a: ApiApplication) => a.id === prev)) return prev;
        if (stateAppId && list.some((a: ApiApplication) => a.id === stateAppId)) return stateAppId;
        return list[0]?.id ?? null;
      });
    } catch (e) {
      if (e instanceof NetworkError) setError("Could not reach the server.");
      else setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, [user, authHeaders, stateAppId]);

  useEffect(() => {
    void loadApplications();
  }, [loadApplications]);

  const loadChecklist = useCallback(
    async (applicationId: number) => {
      setDocsLoading(true);
      setError(null);
      try {
        const res = await apiFetch(`/api/v1/applications/${applicationId}/documents`, {
          headers: authHeaders(),
        });
        if (!res.ok) throw new Error("Could not load checklist");
        const data = await res.json();
        setChecklist(Array.isArray(data) ? data : []);
      } catch (e) {
        setChecklist([]);
        setError(e instanceof Error ? e.message : "Could not load checklist");
      } finally {
        setDocsLoading(false);
      }
    },
    [authHeaders]
  );

  useEffect(() => {
    if (selectedAppId) void loadChecklist(selectedAppId);
    else setChecklist([]);
  }, [selectedAppId, loadChecklist]);

  const selectedApp = useMemo(
    () => applications.find((a) => a.id === selectedAppId) ?? null,
    [applications, selectedAppId]
  );

  const patchDoc = async (docId: number, status: (typeof DOC_STATUSES)[number]) => {
    if (!selectedAppId) return;
    setPatchingDocId(docId);
    try {
      const res = await apiFetch(`/api/v1/applications/${selectedAppId}/documents/${docId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) throw new Error("Update failed");
      const row = await res.json();
      setChecklist((prev) => prev.map((r) => (r.id === docId ? { ...r, ...row } : r)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Update failed");
    } finally {
      setPatchingDocId(null);
    }
  };

  if (!user) return null;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Document checklist</h1>
      <p className="mt-3 text-slate-600 dark:text-slate-400">
        Track readiness for each required document per application. File uploads are not enabled yet — this is a
        checklist to support your workflow.
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
          {error}
        </div>
      )}

      {loading ? (
        <div className="mt-8 h-32 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
      ) : applications.length === 0 ? (
        <p className="mt-8 text-slate-600 dark:text-slate-400">
          Create an application first from the{" "}
          <Link to="/applications" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Applications
          </Link>{" "}
          page.
        </p>
      ) : (
        <div className="mt-8 space-y-6">
          <div>
            <label htmlFor="app-select" className="text-sm font-medium text-slate-900 dark:text-slate-100">
              Application
            </label>
            <select
              id="app-select"
              value={selectedAppId ?? ""}
              onChange={(e) => setSelectedAppId(Number(e.target.value) || null)}
              className="mt-2 block w-full max-w-lg rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
            >
              {applications.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.scholarship?.title ?? `Scholarship #${a.scholarship_id}`}
                </option>
              ))}
            </select>
            {selectedApp ? (
              <p className="mt-1 text-xs text-slate-500">
                Status: <strong>{selectedApp.status.replace(/_/g, " ")}</strong> ·{" "}
                <Link
                  to={`/scholarship/${selectedApp.scholarship_id}#requirements`}
                  className="text-primary-600 hover:underline dark:text-primary-400"
                >
                  View official requirements
                </Link>
              </p>
            ) : null}
          </div>

          {docsLoading ? (
            <div className="h-24 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
          ) : checklist.length === 0 ? (
            <p className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              No checklist rows yet. They appear when an application is created and the scholarship lists required
              documents.
            </p>
          ) : (
            <ul className="space-y-3">
              {checklist.map((row) => (
                <li
                  key={row.id}
                  className="flex flex-col gap-2 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/40 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <p className="font-medium text-slate-900 dark:text-slate-100">{row.document_type}</p>
                    <p className="text-xs text-slate-500">
                      Updated {new Date(row.updated_at).toLocaleString()}
                    </p>
                  </div>
                  <select
                    value={DOC_STATUSES.includes(row.status as (typeof DOC_STATUSES)[number]) ? row.status : "not_started"}
                    disabled={patchingDocId === row.id}
                    onChange={(e) => void patchDoc(row.id, e.target.value as (typeof DOC_STATUSES)[number])}
                    className="rounded-lg border border-slate-300 bg-white px-2 py-1.5 text-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200"
                    aria-label={`Status for ${row.document_type}`}
                  >
                    {DOC_STATUSES.map((s) => (
                      <option key={s} value={s}>
                        {docStatusLabel(s)}
                      </option>
                    ))}
                  </select>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
