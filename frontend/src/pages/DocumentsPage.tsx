import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { apiFetch, NetworkError } from "../api/client";
import { formatDateTimeLong } from "../utils/formatDate";
import { maskDriveUrl, normalizeDriveUrl } from "../utils/driveUrl";
import type { StudentProfileResponse } from "../types";
import { DOCUMENT_LABELS } from "../components/dashboard/documentLabels";

type ApiApplication = {
  id: number;
  scholarship_id: number;
  status: string;
  drive_folder_url?: string | null;
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

function resolveOpenFolderUrl(appFolder: string | null | undefined, globalFolder: string | null | undefined): string {
  const raw = (appFolder && appFolder.trim()) || (globalFolder && globalFolder.trim()) || "";
  return normalizeDriveUrl(raw);
}

type DriveFolderPanelProps = {
  label: string;
  hint?: string;
  savedUrl: string;
  onSave: (url: string) => Promise<void>;
  saving: boolean;
  statusMsg: string | null;
};

function DriveFolderPanel({ label, hint, savedUrl, onSave, saving, statusMsg }: DriveFolderPanelProps) {
  const [editing, setEditing] = useState(!savedUrl.trim());
  const [revealFull, setRevealFull] = useState(false);
  const [draft, setDraft] = useState(savedUrl);
  useEffect(() => {
    setDraft(savedUrl);
    if (!savedUrl.trim()) setEditing(true);
  }, [savedUrl]);

  const normalized = normalizeDriveUrl(savedUrl);
  const hasLink = Boolean(normalized);

  const handleSave = async () => {
    await onSave(draft);
    setEditing(false);
    setRevealFull(false);
  };

  return (
    <div className="rounded-xl border border-teal-200/80 bg-white p-4 dark:border-teal-800 dark:bg-slate-900/50">
      <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">{label}</p>
      {hint ? <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">{hint}</p> : null}

      {!editing && hasLink ? (
        <div className="mt-3 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-lg bg-teal-50 px-2 py-1 font-mono text-xs text-teal-900 dark:bg-teal-950/50 dark:text-teal-100">
              {revealFull ? normalized : maskDriveUrl(normalized)}
            </span>
            <span className="text-xs font-medium text-emerald-700 dark:text-emerald-300">Link saved</span>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setRevealFull((v) => !v)}
              className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-800 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              {revealFull ? "Hide URL" : "Show full URL"}
            </button>
            <a
              href={normalized}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center rounded-lg bg-teal-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-teal-700"
            >
              Open folder
            </a>
            <button
              type="button"
              onClick={() => setEditing(true)}
              className="rounded-lg border border-teal-400 px-3 py-1.5 text-xs font-medium text-teal-800 hover:bg-teal-50 dark:border-teal-600 dark:text-teal-200 dark:hover:bg-teal-950/40"
            >
              Edit link
            </button>
          </div>
        </div>
      ) : (
        <div className="mt-3 space-y-2">
          <input
            type="url"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="https://drive.google.com/drive/folders/..."
            className="w-full rounded-xl border border-teal-300 bg-white px-3 py-2 text-sm dark:border-teal-700 dark:bg-slate-800 dark:text-slate-100"
            autoComplete="off"
          />
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              disabled={saving}
              onClick={() => void handleSave()}
              className="rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700 disabled:opacity-50"
            >
              {saving ? "Saving…" : "Save link"}
            </button>
            {hasLink ? (
              <button
                type="button"
                onClick={() => {
                  setEditing(false);
                  setDraft(savedUrl);
                }}
                className="rounded-lg border border-slate-300 px-4 py-2 text-sm text-slate-700 dark:border-slate-600 dark:text-slate-300"
              >
                Cancel
              </button>
            ) : null}
          </div>
        </div>
      )}

      {!editing && !hasLink ? (
        <button
          type="button"
          onClick={() => setEditing(true)}
          className="mt-3 w-full rounded-xl border-2 border-dashed border-teal-300 py-3 text-sm font-semibold text-teal-800 hover:bg-teal-50 dark:border-teal-700 dark:text-teal-200 dark:hover:bg-teal-950/30"
        >
          Add Drive folder
        </button>
      ) : null}

      {statusMsg ? (
        <p className="mt-2 text-xs text-teal-800 dark:text-teal-200" role="status">
          {statusMsg}
        </p>
      ) : null}
    </div>
  );
}

export function DocumentsPage() {
  const { user, authHeaders } = useAuth();
  const location = useLocation();
  const stateAppId = (location.state as { applicationId?: number } | null)?.applicationId;

  const [profile, setProfile] = useState<StudentProfileResponse | null>(null);
  const [applications, setApplications] = useState<ApiApplication[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<number | null>(stateAppId ?? null);
  const [checklist, setChecklist] = useState<ChecklistRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [docsLoading, setDocsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [patchingDocId, setPatchingDocId] = useState<number | null>(null);

  const [globalSaving, setGlobalSaving] = useState(false);
  const [globalMsg, setGlobalMsg] = useState<string | null>(null);
  const [appFolderSaving, setAppFolderSaving] = useState(false);
  const [appFolderMsg, setAppFolderMsg] = useState<string | null>(null);

  const loadProfile = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("/api/v1/profiles/me", { headers: authHeaders() });
      if (res.status === 404) {
        setProfile(null);
        return;
      }
      if (res.ok) {
        const data = await res.json();
        setProfile(data as StudentProfileResponse);
      }
    } catch {
      /* non-fatal */
    }
  }, [user, authHeaders]);

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
    void loadProfile();
    void loadApplications();
  }, [loadProfile, loadApplications]);

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

  const globalFolder = profile?.google_drive_folder_url ?? "";
  const appFolder = selectedApp?.drive_folder_url ?? "";
  const openTarget = resolveOpenFolderUrl(appFolder, globalFolder);

  const readyCount = useMemo(
    () => checklist.filter((r) => r.status === "ready" || r.status === "submitted").length,
    [checklist]
  );
  const totalReq = checklist.length;

  const saveGlobalVault = async (url: string) => {
    setGlobalSaving(true);
    setGlobalMsg(null);
    try {
      const body = { google_drive_folder_url: normalizeDriveUrl(url) || null };
      const res = await apiFetch("/api/v1/profiles/me/vault", {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const d = await res.json().catch(() => null);
        throw new Error((d as { detail?: string })?.detail ?? "Could not save.");
      }
      const next = (await res.json()) as StudentProfileResponse;
      setProfile(next);
      setGlobalMsg("Global folder link saved. Use it when a scholarship has no its own folder.");
    } catch (e) {
      setGlobalMsg(e instanceof Error ? e.message : "Save failed.");
    } finally {
      setGlobalSaving(false);
    }
  };

  const saveAppFolder = async (url: string) => {
    if (!selectedAppId) return;
    setAppFolderSaving(true);
    setAppFolderMsg(null);
    try {
      const body = { drive_folder_url: normalizeDriveUrl(url) || null };
      const res = await apiFetch(`/api/v1/applications/${selectedAppId}/drive-folder`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const d = await res.json().catch(() => null);
        throw new Error((d as { detail?: string })?.detail ?? "Could not save.");
      }
      const updated = (await res.json()) as ApiApplication;
      setApplications((prev) => prev.map((a) => (a.id === selectedAppId ? { ...a, ...updated } : a)));
      setAppFolderMsg("Folder for this application saved. Upload uses this folder first, then global.");
    } catch (e) {
      setAppFolderMsg(e instanceof Error ? e.message : "Save failed.");
    } finally {
      setAppFolderSaving(false);
    }
  };

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
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Documents</h1>
      <p className="mt-3 text-slate-600 dark:text-slate-400">
        Track document readiness per application. Files stay in <strong>your</strong> Google Drive — ISKONNECT does not
        store uploads. Use <strong>Upload to Drive</strong> to open the right folder and add files there.
      </p>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200">
          {error}
        </div>
      )}

      <div className="mt-8 space-y-4">
        <DriveFolderPanel
          label="Global Drive folder"
          hint="Used for every scholarship unless you set a folder below for a specific application."
          savedUrl={globalFolder}
          onSave={saveGlobalVault}
          saving={globalSaving}
          statusMsg={globalMsg}
        />
      </div>

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

          {selectedApp ? (
            <DriveFolderPanel
              label={`Folder for ${selectedApp.scholarship?.title ?? "this scholarship"}`}
              hint="If set, Upload to Drive opens this folder; otherwise your global folder opens."
              savedUrl={appFolder}
              onSave={saveAppFolder}
              saving={appFolderSaving}
              statusMsg={appFolderMsg}
            />
          ) : null}

          {!openTarget && selectedApp ? (
            <p className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-100">
              Add a global or per-application Drive folder link above to use &quot;Upload to Drive&quot;.
            </p>
          ) : null}

          {docsLoading ? (
            <div className="h-24 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
          ) : checklist.length === 0 ? (
            <p className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              No checklist rows yet. They appear when an application is created and the scholarship lists required
              documents.
            </p>
          ) : (
            <>
              <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 dark:border-slate-700 dark:bg-slate-800/60">
                <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                  {readyCount} of {totalReq} requirements ready
                </p>
                <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-600">
                  <div
                    className="h-full rounded-full bg-teal-500 transition-all"
                    style={{ width: `${totalReq ? Math.round((readyCount / totalReq) * 100) : 0}%` }}
                  />
                </div>
              </div>
              <ul className="space-y-3">
                {checklist.map((row) => (
                  <li
                    key={row.id}
                    className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/40 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-slate-900 dark:text-slate-100">
                        {DOCUMENT_LABELS[row.document_type] ?? row.document_type.replace(/_/g, " ")}
                      </p>
                      <p className="text-xs text-slate-500">Updated {formatDateTimeLong(row.updated_at)}</p>
                    </div>
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
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
                      {openTarget ? (
                        <a
                          href={openTarget}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center justify-center rounded-lg bg-teal-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-teal-700"
                        >
                          Upload to Drive
                        </a>
                      ) : (
                        <span className="text-xs text-slate-500">Set a folder link to open Drive</span>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
