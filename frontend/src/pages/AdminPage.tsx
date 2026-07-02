import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE_URL, apiFetch, NetworkError } from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import type { ScholarshipInfo } from "../types";
import { formatDateTime } from "../utils/formatDate";
import { lifecycleStatusLabel, resolveApplicationStatus } from "../utils/scholarshipStatus";

type Tab = "scholarships" | "staging" | "reviews" | "users" | "matches" | "feedback" | "reports" | "system";

type AdminUser = { id: number; email: string; role: string; email_verified: boolean };
type AdminMatchRun = {
  id: number;
  user_id: number;
  profile_id: number;
  created_at: string | null;
  ph_created_at?: string | null;
  result_count: number;
};
type AdminFeedback = {
  id: number;
  user_id: number | null;
  category: string;
  message: string;
  contact_email: string | null;
  created_at: string | null;
  ph_created_at?: string | null;
};
type AdminReport = {
  id: number;
  scholarship_id: number;
  issue_type: string;
  description: string | null;
  status: string;
  created_at: string;
};
type MaintenanceRunRow = {
  id: number;
  source: string;
  started_at: string | null;
  completed_at: string | null;
  status: string;
  records_found: number | null;
  records_ingested: number | null;
  output_path?: string | null;
  error_detail: string | null;
};

type DataQualitySummary = {
  as_of?: string;
  publishability_threshold?: number;
  total_active?: number;
  average_completeness?: number;
  tier_distribution?: Record<string, number>;
  below_publishable_threshold?: number;
  needs_review?: number;
  missing_residency_rules?: number;
  missing_income_rules?: number;
  missing_course_restrictions?: number;
  expired_verification?: number;
  high_priority_records?: {
    id: number;
    title: string;
    completeness_score: number;
    gaps: string[];
  }[];
};
type StagingRow = {
  id: number;
  title: string;
  provider: string | null;
  source: string | null;
  status: string;
  dedupe_key: string | null;
  created_at: string;
  duplicate_candidates?: { scholarship_id: number; title: string; confidence: number }[];
};

const SCH_PAGE_SIZE = 50;
const REVIEW_QUEUES = [
  { id: "needs_review", label: "Needs verification" },
  { id: "missing_image", label: "Missing image" },
  { id: "low_quality", label: "Low quality" },
  { id: "stale", label: "Stale verification" },
  { id: "duplicates", label: "Duplicates" },
] as const;

export function AdminPage() {
  const { authHeaders } = useAuth();
  const [tab, setTab] = useState<Tab>("scholarships");
  const [scholarships, setScholarships] = useState<ScholarshipInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [users, setUsers] = useState<AdminUser[]>([]);
  const [matchRuns, setMatchRuns] = useState<AdminMatchRun[]>([]);
  const [feedback, setFeedback] = useState<AdminFeedback[]>([]);
  const [reports, setReports] = useState<AdminReport[]>([]);
  const [maintenanceRuns, setMaintenanceRuns] = useState<MaintenanceRunRow[]>([]);
  const [healthJson, setHealthJson] = useState<string | null>(null);
  const [dataQuality, setDataQuality] = useState<DataQualitySummary | null>(null);
  const [catalogHealth, setCatalogHealth] = useState<Record<string, number> | null>(null);
  const [importDashboard, setImportDashboard] = useState<{
    staging_pending?: number;
    staging_total?: number;
    recent_maintenance_runs?: MaintenanceRunRow[];
  } | null>(null);
  const [uploadingImageId, setUploadingImageId] = useState<number | null>(null);
  const [stagingRows, setStagingRows] = useState<StagingRow[]>([]);
  const [stagingActionId, setStagingActionId] = useState<number | null>(null);
  const [schPage, setSchPage] = useState(1);
  const [reviewQueue, setReviewQueue] = useState<(typeof REVIEW_QUEUES)[number]["id"]>("needs_review");
  const [reviewItems, setReviewItems] = useState<Record<string, unknown>[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editProvider, setEditProvider] = useState("");
  const [editLink, setEditLink] = useState("");
  const [showCreate, setShowCreate] = useState(false);

  const headers = useCallback(() => authHeaders(), [authHeaders]);

  const fetchScholarships = useCallback(() => {
    setLoading(true);
    apiFetch("/api/v1/scholarships?include_inactive=true", { headers: headers() })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized or failed to fetch");
        return res.json();
      })
      .then((data: ScholarshipInfo[]) => setScholarships(Array.isArray(data) ? data : []))
      .catch((err) => setError(err instanceof Error ? err.message : "Error"))
      .finally(() => setLoading(false));
  }, [headers]);

  useEffect(() => {
    fetchScholarships();
  }, [fetchScholarships]);

  useEffect(() => {
    if (tab !== "users") return;
    setError(null);
    apiFetch("/api/v1/admin/users", { headers: headers() })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load users");
        return r.json();
      })
      .then((d: AdminUser[]) => setUsers(Array.isArray(d) ? d : []))
      .catch((e) => setError(e instanceof Error ? e.message : "Error"));
  }, [tab, headers]);

  useEffect(() => {
    if (tab !== "matches") return;
    setError(null);
    apiFetch("/api/v1/admin/match-runs/recent?limit=50", { headers: headers() })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load match runs");
        return r.json();
      })
      .then((d: AdminMatchRun[]) => setMatchRuns(Array.isArray(d) ? d : []))
      .catch((e) => setError(e instanceof Error ? e.message : "Error"));
  }, [tab, headers]);

  useEffect(() => {
    if (tab !== "feedback") return;
    setError(null);
    apiFetch("/api/v1/admin/feedback/list?limit=100", { headers: headers() })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load feedback");
        return r.json();
      })
      .then((d: AdminFeedback[]) => setFeedback(Array.isArray(d) ? d : []))
      .catch((e) => setError(e instanceof Error ? e.message : "Error"));
  }, [tab, headers]);

  useEffect(() => {
    if (tab !== "staging") return;
    setError(null);
    apiFetch("/api/v1/scholarships/staging/pending", { headers: headers() })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load pending staging rows");
        return r.json();
      })
      .then((d: StagingRow[]) => setStagingRows(Array.isArray(d) ? d : []))
      .catch((e) => setError(e instanceof Error ? e.message : "Error"));
  }, [tab, headers]);

  useEffect(() => {
    if (tab !== "reports") return;
    setError(null);
    apiFetch("/api/v1/reports/pending", { headers: headers() })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load reports");
        return r.json();
      })
      .then((d: AdminReport[]) => setReports(Array.isArray(d) ? d : []))
      .catch((e) => setError(e instanceof Error ? e.message : "Error"));
  }, [tab, headers]);

  useEffect(() => {
    if (tab !== "system") return;
    setError(null);
    Promise.all([
      apiFetch("/health").then(async (r) => {
        if (!r.ok) throw new Error(`health HTTP ${r.status}`);
        return r.json();
      }),
      apiFetch("/api/v1/admin/data-quality", { headers: headers() }).then((r) => {
        if (!r.ok) throw new Error("data quality");
        return r.json();
      }),
      apiFetch("/api/v1/admin/dashboard/health", { headers: headers() }).then((r) => {
        if (!r.ok) throw new Error("catalog health");
        return r.json();
      }),
      apiFetch("/api/v1/admin/dashboard/import", { headers: headers() }).then((r) => {
        if (!r.ok) throw new Error("import dashboard");
        return r.json();
      }),
    ])
      .then(([h, dq, ch, imp]) => {
        setHealthJson(JSON.stringify(h, null, 2));
        setDataQuality(dq && typeof dq === "object" ? (dq as DataQualitySummary) : null);
        setCatalogHealth(ch && typeof ch === "object" ? ch : null);
        setImportDashboard(imp && typeof imp === "object" ? imp : null);
        const runs = (imp as { recent_maintenance_runs?: MaintenanceRunRow[] })?.recent_maintenance_runs;
        setMaintenanceRuns(Array.isArray(runs) ? runs : []);
      })
      .catch((e) => {
        setHealthJson(null);
        setMaintenanceRuns([]);
        setDataQuality(null);
        setCatalogHealth(null);
        setImportDashboard(null);
        if (e instanceof NetworkError) {
          setError(
            `Unable to reach the API at ${API_BASE_URL}. Confirm the backend is running, VITE_API_BASE_URL is set, and CORS allows this site.`
          );
          return;
        }
        setError("Could not load system health (check admin role and API URL).");
      });
  }, [tab, headers]);

  const handleDelete = (id: number) => {
    if (!confirm("Deactivate this scholarship?")) return;
    apiFetch(`/api/v1/scholarships/${id}`, {
      method: "DELETE",
      headers: headers(),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to delete");
        fetchScholarships();
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Error"));
  };

  const handleImageUpload = async (scholarshipId: number, file: File) => {
    setUploadingImageId(scholarshipId);
    setError(null);
    try {
      const title = scholarships.find((s) => s.id === scholarshipId)?.title ?? "";
      const fd = new FormData();
      fd.append("file", file);
      if (title) fd.append("image_alt", title);
      const res = await apiFetch(`/api/v1/scholarships/${scholarshipId}/image`, {
        method: "POST",
        headers: headers(),
        body: fd,
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Image upload failed");
      }
      const updated = (await res.json()) as ScholarshipInfo;
      setScholarships((prev) => prev.map((s) => (s.id === scholarshipId ? { ...s, ...updated } : s)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Image upload failed");
    } finally {
      setUploadingImageId(null);
    }
  };

  const handleImageDelete = async (scholarshipId: number) => {
    if (!confirm("Remove this scholarship image?")) return;
    setUploadingImageId(scholarshipId);
    try {
      const res = await apiFetch(`/api/v1/scholarships/${scholarshipId}/image`, {
        method: "DELETE",
        headers: headers(),
      });
      if (!res.ok) throw new Error("Failed to remove image");
      const updated = (await res.json()) as ScholarshipInfo;
      setScholarships((prev) => prev.map((s) => (s.id === scholarshipId ? { ...s, ...updated } : s)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to remove image");
    } finally {
      setUploadingImageId(null);
    }
  };

  useEffect(() => {
    if (tab !== "reviews") return;
    setError(null);
    apiFetch(`/api/v1/admin/queues/${reviewQueue}?limit=50`, { headers: headers() })
      .then(async (r) => {
        if (!r.ok) {
          const body = await r.text().catch(() => "");
          throw new Error(
            `Failed to load review queue (HTTP ${r.status})${body ? `: ${body.slice(0, 160)}` : ""}`
          );
        }
        return r.json();
      })
      .then((d: { items?: Record<string, unknown>[] }) =>
        setReviewItems(Array.isArray(d.items) ? d.items : [])
      )
      .catch((e) => {
        if (e instanceof NetworkError) {
          setError(
            `Unable to reach the API at ${API_BASE_URL}. Confirm the backend is running, VITE_API_BASE_URL is set, and CORS allows this site.`
          );
          return;
        }
        setError(e instanceof Error ? e.message : "Error");
      });
  }, [tab, reviewQueue, headers]);

  const handleStagingApprove = async (stagingId: number, action: "create" | "update" = "create") => {
    setStagingActionId(stagingId);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/scholarships/staging/${stagingId}/approve`, {
        method: "POST",
        headers: { ...headers(), "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Approve failed");
      }
      setStagingRows((prev) => prev.filter((r) => r.id !== stagingId));
      fetchScholarships();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Approve failed");
    } finally {
      setStagingActionId(null);
    }
  };

  const handleStagingReject = async (stagingId: number) => {
    if (!confirm("Reject this staging row? It will not be added to the live catalog.")) return;
    setStagingActionId(stagingId);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/scholarships/staging/${stagingId}/reject`, {
        method: "POST",
        headers: headers(),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Reject failed");
      }
      setStagingRows((prev) => prev.filter((r) => r.id !== stagingId));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reject failed");
    } finally {
      setStagingActionId(null);
    }
  };

  const handleReportAction = async (reportId: number, action: "resolve" | "dismiss") => {
    const res = await apiFetch(`/api/v1/reports/${reportId}/${action}`, {
      method: "POST",
      headers: headers(),
    });
    if (!res.ok) throw new Error(`Failed to ${action} report`);
    setReports((prev) => prev.filter((r) => r.id !== reportId));
  };

  const handleSaveScholarship = async (scholarshipId?: number) => {
    const payload = {
      title: editTitle.trim(),
      provider: editProvider.trim() || null,
      link: editLink.trim() || null,
      source: "manual",
    };
    if (!payload.title) {
      setError("Title is required");
      return;
    }
    const res = await apiFetch(
      scholarshipId ? `/api/v1/scholarships/${scholarshipId}` : "/api/v1/scholarships",
      {
        method: scholarshipId ? "PUT" : "POST",
        headers: { ...headers(), "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }
    );
    if (!res.ok) {
      const data = await res.json().catch(() => null);
      throw new Error(data?.detail ?? "Save failed");
    }
    setEditingId(null);
    setShowCreate(false);
    fetchScholarships();
  };

  const pagedScholarships = scholarships.slice(
    (schPage - 1) * SCH_PAGE_SIZE,
    schPage * SCH_PAGE_SIZE
  );
  const schTotalPages = Math.max(1, Math.ceil(scholarships.length / SCH_PAGE_SIZE));

  const tabs: { id: Tab; label: string }[] = [
    { id: "scholarships", label: "Scholarships" },
    { id: "staging", label: "Pending" },
    { id: "reviews", label: "Review queues" },
    { id: "users", label: "Users" },
    { id: "matches", label: "Matches" },
    { id: "feedback", label: "Feedback" },
    { id: "reports", label: "Reports" },
    { id: "system", label: "System" },
  ];

  if (loading && tab === "scholarships") {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <p className="text-slate-600 dark:text-slate-400">Loading...</p>
        </div>
      </section>
    );
  }

  if (error && tab === "scholarships" && scholarships.length === 0) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300">
            {error}
            <p className="mt-2 text-sm">
              <Link to="/dashboard" className="text-primary-600 hover:underline">
                Return to dashboard
              </Link>
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12">
      <div className="mx-auto max-w-6xl px-4">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Admin</h2>
          <div className="flex flex-wrap gap-2">
            <Link
              to="/admin/analytics"
              className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm dark:border-slate-600"
            >
              Analytics
            </Link>
            <Link to="/dashboard" className="text-sm font-medium text-primary-600 hover:underline">
              Back to app
            </Link>
          </div>
        </div>

        <div className="mb-6 flex flex-wrap gap-2 border-b border-slate-200 pb-2 dark:border-slate-700">
          {tabs.map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => setTab(t.id)}
              className={[
                "rounded-lg px-3 py-1.5 text-sm font-medium",
                tab === t.id
                  ? "bg-primary-600 text-white"
                  : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800",
              ].join(" ")}
            >
              {t.label}
            </button>
          ))}
        </div>

        {error ? (
          <div className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40">
            {error}
          </div>
        ) : null}

        {tab === "scholarships" && (
          <>
            <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
              <p className="text-sm text-slate-600 dark:text-slate-400">
                {scholarships.length} scholarships (page {schPage} of {schTotalPages})
              </p>
              <button
                type="button"
                onClick={() => {
                  setShowCreate(true);
                  setEditTitle("");
                  setEditProvider("");
                  setEditLink("");
                }}
                className="rounded-lg bg-primary-600 px-3 py-1.5 text-sm font-medium text-white"
              >
                Create scholarship
              </button>
            </div>
            {(showCreate || editingId !== null) && (
              <div className="mb-4 rounded-lg border border-slate-200 p-4 dark:border-slate-700">
                <h3 className="mb-2 font-medium">{editingId ? "Edit scholarship" : "New scholarship"}</h3>
                <div className="grid gap-2 sm:grid-cols-3">
                  <input
                    className="rounded border px-2 py-1 text-sm dark:border-slate-600 dark:bg-slate-900"
                    placeholder="Title"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                  />
                  <input
                    className="rounded border px-2 py-1 text-sm dark:border-slate-600 dark:bg-slate-900"
                    placeholder="Provider"
                    value={editProvider}
                    onChange={(e) => setEditProvider(e.target.value)}
                  />
                  <input
                    className="rounded border px-2 py-1 text-sm dark:border-slate-600 dark:bg-slate-900"
                    placeholder="Application link"
                    value={editLink}
                    onChange={(e) => setEditLink(e.target.value)}
                  />
                </div>
                <div className="mt-2 flex gap-2">
                  <button
                    type="button"
                    className="rounded bg-primary-600 px-3 py-1 text-sm text-white"
                    onClick={() => void handleSaveScholarship(editingId ?? undefined).catch((e) => setError(String(e)))}
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    className="rounded border px-3 py-1 text-sm"
                    onClick={() => {
                      setEditingId(null);
                      setShowCreate(false);
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
            <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
              <table className="min-w-full text-sm">
                <thead className="bg-slate-50 dark:bg-slate-800">
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold">ID</th>
                    <th className="px-4 py-2 text-left font-semibold">Title</th>
                    <th className="px-4 py-2 text-left font-semibold">Provider</th>
                    <th className="px-4 py-2 text-left font-semibold">Level</th>
                    <th className="px-4 py-2 text-left font-semibold">Image</th>
                    <th className="px-4 py-2 text-left font-semibold">Status</th>
                    <th className="px-4 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {pagedScholarships.map((s) => (
                    <tr key={s.id} className="border-t border-slate-100 dark:border-slate-700">
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.id}</td>
                      <td className="px-4 py-2 font-medium text-slate-900 dark:text-slate-100">{s.title}</td>
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.provider ?? "—"}</td>
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.level ?? "—"}</td>
                      <td className="px-4 py-2">
                        <div className="flex flex-col gap-1">
                          {s.image_url ? (
                            <a
                              href={s.image_url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-xs text-primary-600 hover:underline dark:text-primary-400"
                            >
                              View
                            </a>
                          ) : (
                            <span className="text-xs text-slate-400">None</span>
                          )}
                          <label className="cursor-pointer text-xs font-medium text-primary-600 hover:underline dark:text-primary-400">
                            {uploadingImageId === s.id ? "Uploading…" : "Upload"}
                            <input
                              type="file"
                              accept="image/jpeg,image/png,image/webp"
                              className="sr-only"
                              disabled={uploadingImageId === s.id}
                              onChange={(e) => {
                                const f = e.target.files?.[0];
                                if (f) void handleImageUpload(s.id, f);
                                e.target.value = "";
                              }}
                            />
                          </label>
                          {s.image_url ? (
                            <button
                              type="button"
                              className="text-left text-xs text-red-600 hover:underline"
                              disabled={uploadingImageId === s.id}
                              onClick={() => void handleImageDelete(s.id)}
                            >
                              Remove
                            </button>
                          ) : null}
                        </div>
                      </td>
                      <td className="px-4 py-2">
                        <span
                          className={`rounded px-2 py-0.5 text-xs font-medium ${
                            resolveApplicationStatus(s) === "archived"
                              ? "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400"
                              : "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                          }`}
                        >
                          {lifecycleStatusLabel(resolveApplicationStatus(s))}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <div className="flex flex-wrap gap-2">
                          <button
                            type="button"
                            onClick={() => {
                              setEditingId(s.id);
                              setEditTitle(s.title);
                              setEditProvider(s.provider ?? "");
                              setEditLink(s.link ?? "");
                              setShowCreate(false);
                            }}
                            className="text-primary-600 hover:underline"
                          >
                            Edit
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(s.id)}
                            className="text-red-600 hover:text-red-700 disabled:opacity-50"
                            disabled={s.is_active === false}
                          >
                            Deactivate
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 flex gap-2">
              <button
                type="button"
                disabled={schPage <= 1}
                onClick={() => setSchPage((p) => Math.max(1, p - 1))}
                className="rounded border px-3 py-1 text-sm disabled:opacity-50"
              >
                Previous
              </button>
              <button
                type="button"
                disabled={schPage >= schTotalPages}
                onClick={() => setSchPage((p) => p + 1)}
                className="rounded border px-3 py-1 text-sm disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </>
        )}

        {tab === "reviews" && (
          <>
            <div className="mb-4 flex flex-wrap gap-2">
              {REVIEW_QUEUES.map((q) => (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => setReviewQueue(q.id)}
                  className={[
                    "rounded-lg px-3 py-1 text-sm",
                    reviewQueue === q.id ? "bg-primary-600 text-white" : "border",
                  ].join(" ")}
                >
                  {q.label}
                </button>
              ))}
            </div>
            <ul className="space-y-2">
              {reviewItems.length === 0 ? (
                <p className="text-slate-600 dark:text-slate-400">Queue empty.</p>
              ) : (
                reviewItems.map((item) => (
                  <li
                    key={String(item.id)}
                    className="rounded-lg border border-slate-200 p-3 text-sm dark:border-slate-700"
                  >
                    <p className="font-medium">{String(item.title ?? "—")}</p>
                    <p className="text-slate-500">
                      #{String(item.id)} · score {String(item.confidence_score ?? "—")}
                    </p>
                    <Link to={`/scholarship/${item.id}`} className="text-primary-600 hover:underline">
                      View
                    </Link>
                  </li>
                ))
              )}
            </ul>
          </>
        )}

        {tab === "staging" && (
          <>
            <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
              {stagingRows.length} pending row(s) awaiting approval. Approved rows are published to the live
              catalog; rejected rows are discarded.
            </p>
            {stagingRows.length === 0 ? (
              <p className="text-slate-600 dark:text-slate-400">No pending staging scholarships.</p>
            ) : (
              <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
                <table className="min-w-full text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-800">
                    <tr>
                      <th className="px-4 py-2 text-left font-semibold">ID</th>
                      <th className="px-4 py-2 text-left font-semibold">Title</th>
                      <th className="px-4 py-2 text-left font-semibold">Provider</th>
                      <th className="px-4 py-2 text-left font-semibold">Source</th>
                      <th className="px-4 py-2 text-left font-semibold">Queued</th>
                      <th className="px-4 py-2 text-left font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stagingRows.map((r) => (
                      <tr key={r.id} className="border-t border-slate-100 dark:border-slate-700">
                        <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{r.id}</td>
                        <td className="px-4 py-2 font-medium text-slate-900 dark:text-slate-100">{r.title}</td>
                        <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{r.provider ?? "—"}</td>
                        <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{r.source ?? "—"}</td>
                        <td className="px-4 py-2 text-xs text-slate-500">{formatDateTime(r.created_at)}</td>
                        <td className="px-4 py-2">
                          <div className="flex flex-wrap gap-2">
                            <button
                              type="button"
                              disabled={stagingActionId === r.id}
                              onClick={() =>
                                void handleStagingApprove(
                                  r.id,
                                  (r.duplicate_candidates?.length ?? 0) > 0 ? "update" : "create"
                                )
                              }
                              className="rounded bg-green-600 px-2 py-1 text-xs font-medium text-white hover:bg-green-700 disabled:opacity-50"
                            >
                              {stagingActionId === r.id
                                ? "…"
                                : (r.duplicate_candidates?.length ?? 0) > 0
                                  ? "Update live"
                                  : "Approve"}
                            </button>
                            <button
                              type="button"
                              disabled={stagingActionId === r.id}
                              onClick={() => void handleStagingReject(r.id)}
                              className="rounded border border-red-300 px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 disabled:opacity-50 dark:border-red-800 dark:hover:bg-red-950/40"
                            >
                              Reject
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        {tab === "users" && (
          <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
            <table className="min-w-full text-sm">
              <thead className="bg-slate-50 dark:bg-slate-800">
                <tr>
                  <th className="px-4 py-2 text-left">ID</th>
                  <th className="px-4 py-2 text-left">Email</th>
                  <th className="px-4 py-2 text-left">Role</th>
                  <th className="px-4 py-2 text-left">Verified</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id} className="border-t border-slate-100 dark:border-slate-700">
                    <td className="px-4 py-2">{u.id}</td>
                    <td className="px-4 py-2">{u.email}</td>
                    <td className="px-4 py-2">{u.role}</td>
                    <td className="px-4 py-2">{u.email_verified ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {tab === "matches" && (
          <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
            <table className="min-w-full text-sm">
              <thead className="bg-slate-50 dark:bg-slate-800">
                <tr>
                  <th className="px-4 py-2 text-left">Run ID</th>
                  <th className="px-4 py-2 text-left">User</th>
                  <th className="px-4 py-2 text-left">Profile</th>
                  <th className="px-4 py-2 text-left">When (PH)</th>
                  <th className="px-4 py-2 text-left">Results</th>
                </tr>
              </thead>
              <tbody>
                {matchRuns.map((m) => (
                  <tr key={m.id} className="border-t border-slate-100 dark:border-slate-700">
                    <td className="px-4 py-2">{m.id}</td>
                    <td className="px-4 py-2">{m.user_id}</td>
                    <td className="px-4 py-2">{m.profile_id}</td>
                    <td className="px-4 py-2">{formatDateTime(m.ph_created_at ?? m.created_at ?? "")}</td>
                    <td className="px-4 py-2">{m.result_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {tab === "feedback" && (
          <ul className="space-y-3">
            {feedback.map((f) => (
              <li key={f.id} className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
                <p className="text-xs text-slate-500">
                  #{f.id} · {f.category} · {formatDateTime(f.ph_created_at ?? f.created_at ?? "")}
                </p>
                <p className="mt-2 whitespace-pre-wrap text-sm text-slate-800 dark:text-slate-200">{f.message}</p>
                {f.contact_email ? (
                  <p className="mt-1 text-xs text-slate-500">Contact: {f.contact_email}</p>
                ) : null}
              </li>
            ))}
          </ul>
        )}

        {tab === "reports" && (
          <ul className="space-y-3">
            {reports.length === 0 ? (
              <p className="text-slate-600 dark:text-slate-400">No pending reports.</p>
            ) : (
              reports.map((r) => (
                <li key={r.id} className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
                  <p className="font-medium">
                    Scholarship #{r.scholarship_id} — {r.issue_type}
                  </p>
                  <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{r.description}</p>
                  <p className="mt-1 text-xs text-slate-500">{r.created_at}</p>
                  <div className="mt-2 flex gap-2">
                    <button
                      type="button"
                      className="rounded bg-green-600 px-2 py-1 text-xs text-white"
                      onClick={() =>
                        void handleReportAction(r.id, "resolve").catch((e) =>
                          setError(e instanceof Error ? e.message : "Error")
                        )
                      }
                    >
                      Resolve
                    </button>
                    <button
                      type="button"
                      className="rounded border border-slate-300 px-2 py-1 text-xs"
                      onClick={() =>
                        void handleReportAction(r.id, "dismiss").catch((e) =>
                          setError(e instanceof Error ? e.message : "Error")
                        )
                      }
                    >
                      Dismiss
                    </button>
                  </div>
                </li>
              ))
            )}
          </ul>
        )}

        {tab === "system" && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Scholarship health</h3>
              {catalogHealth ? (
                <ul className="mt-2 grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-3">
                  {Object.entries(catalogHealth).map(([k, v]) => (
                    <li
                      key={k}
                      className="flex justify-between rounded-lg border border-slate-200 px-3 py-2 dark:border-slate-700"
                    >
                      <span className="text-slate-600 dark:text-slate-400">{k.replace(/_/g, " ")}</span>
                      <span className="font-semibold text-slate-900 dark:text-slate-100">{String(v)}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-2 text-sm text-slate-500">—</p>
              )}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Import pipeline</h3>
              {importDashboard ? (
                <div className="mt-2 space-y-2 text-sm">
                  <p>
                    Staging pending: <strong>{importDashboard.staging_pending ?? 0}</strong> /{" "}
                    {importDashboard.staging_total ?? 0}
                  </p>
                </div>
              ) : (
                <p className="mt-2 text-sm text-slate-500">—</p>
              )}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">GET /health</h3>
              <pre className="mt-2 max-h-64 overflow-auto rounded-lg bg-slate-900 p-4 text-xs text-green-200">
                {healthJson ?? "—"}
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Data quality dashboard</h3>
              {dataQuality ? (
                <div className="mt-3 space-y-4">
                  <ul className="grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-3">
                    {[
                      ["Active scholarships", dataQuality.total_active],
                      ["Average completeness", `${dataQuality.average_completeness ?? 0}%`],
                      ["Below publishable threshold", dataQuality.below_publishable_threshold],
                      ["Needs review", dataQuality.needs_review],
                      ["Missing residency rules", dataQuality.missing_residency_rules],
                      ["Missing income rules", dataQuality.missing_income_rules],
                      ["Missing course restrictions", dataQuality.missing_course_restrictions],
                      ["Expired verification", dataQuality.expired_verification],
                    ].map(([label, value]) => (
                      <li
                        key={String(label)}
                        className="flex justify-between rounded-lg border border-slate-200 px-3 py-2 dark:border-slate-700"
                      >
                        <span className="text-slate-600 dark:text-slate-400">{label}</span>
                        <span className="font-semibold text-slate-900 dark:text-slate-100">{String(value ?? "—")}</span>
                      </li>
                    ))}
                  </ul>
                  {dataQuality.tier_distribution ? (
                    <div>
                      <p className="text-sm font-medium text-slate-700 dark:text-slate-300">Completeness tiers</p>
                      <ul className="mt-2 grid gap-2 text-sm sm:grid-cols-3">
                        {Object.entries(dataQuality.tier_distribution).map(([tier, count]) => (
                          <li
                            key={tier}
                            className="rounded-lg border border-slate-200 px-3 py-2 dark:border-slate-700"
                          >
                            <span className="text-slate-600 dark:text-slate-400">{tier.replace(/_/g, " ")}</span>
                            <span className="ml-2 font-semibold">{count}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                  {dataQuality.high_priority_records && dataQuality.high_priority_records.length > 0 ? (
                    <div>
                      <p className="text-sm font-medium text-slate-700 dark:text-slate-300">High-priority records</p>
                      <ul className="mt-2 max-h-48 space-y-1 overflow-y-auto text-sm">
                        {dataQuality.high_priority_records.map((row) => (
                          <li key={row.id} className="rounded border border-slate-200 px-2 py-1 dark:border-slate-700">
                            <Link to={`/scholarship/${row.id}`} className="font-medium text-primary-600 hover:underline">
                              {row.title}
                            </Link>
                            <span className="ml-2 text-xs text-slate-500">
                              {row.completeness_score}% · {row.gaps?.slice(0, 2).join(", ")}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                </div>
              ) : (
                <p className="mt-2 text-sm text-slate-500">—</p>
              )}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Recent maintenance runs</h3>
              <div className="mt-2 overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
                <table className="min-w-full text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-800">
                    <tr>
                      <th className="px-3 py-2 text-left">ID</th>
                      <th className="px-3 py-2 text-left">Job</th>
                      <th className="px-3 py-2 text-left">Status</th>
                      <th className="px-3 py-2 text-left">Records</th>
                      <th className="px-3 py-2 text-left">Error</th>
                      <th className="px-3 py-2 text-left">Started</th>
                    </tr>
                  </thead>
                  <tbody>
                    {maintenanceRuns.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="px-3 py-4 text-center text-slate-500">
                          No maintenance runs logged yet.
                        </td>
                      </tr>
                    ) : (
                      maintenanceRuns.map((r) => (
                        <tr key={r.id} className="border-t border-slate-100 dark:border-slate-700">
                          <td className="px-3 py-2">{r.id}</td>
                          <td className="px-3 py-2">{r.source}</td>
                          <td className="px-3 py-2">{r.status}</td>
                          <td className="px-3 py-2">{r.records_ingested ?? r.records_found ?? "—"}</td>
                          <td className="max-w-xs truncate px-3 py-2 text-xs text-slate-600 dark:text-slate-400">
                            {r.error_detail ?? "—"}
                          </td>
                          <td className="px-3 py-2 text-xs">{r.started_at}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
