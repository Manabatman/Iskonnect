import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE_URL, apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import type { ScholarshipInfo } from "../types";
import { formatDateTime } from "../utils/formatDate";

type Tab = "scholarships" | "users" | "matches" | "feedback" | "reports" | "system";

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
type ScraperRunRow = {
  id: number;
  source: string;
  started_at: string | null;
  completed_at: string | null;
  status: string;
  records_found: number | null;
  records_ingested: number | null;
  output_path: string | null;
  error_detail: string | null;
};

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
  const [scraperRuns, setScraperRuns] = useState<ScraperRunRow[]>([]);
  const [healthJson, setHealthJson] = useState<string | null>(null);

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
      fetch(`${API_BASE_URL}/health`).then((r) => r.json()),
      apiFetch("/api/v1/admin/scraper-runs/latest?limit=15", { headers: headers() }).then((r) => {
        if (!r.ok) throw new Error("scraper runs");
        return r.json();
      }),
    ])
      .then(([h, s]) => {
        setHealthJson(JSON.stringify(h, null, 2));
        setScraperRuns(Array.isArray(s) ? s : []);
      })
      .catch(() => {
        setHealthJson(null);
        setScraperRuns([]);
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

  const tabs: { id: Tab; label: string }[] = [
    { id: "scholarships", label: "Scholarships" },
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

        {error && tab !== "scholarships" ? (
          <div className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/40">
            {error}
          </div>
        ) : null}

        {tab === "scholarships" && (
          <>
            <p className="mb-4 text-sm text-slate-600 dark:text-slate-400">
              {scholarships.length} scholarships. Use API POST/PUT to add or edit.
            </p>
            <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
              <table className="min-w-full text-sm">
                <thead className="bg-slate-50 dark:bg-slate-800">
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold">ID</th>
                    <th className="px-4 py-2 text-left font-semibold">Title</th>
                    <th className="px-4 py-2 text-left font-semibold">Provider</th>
                    <th className="px-4 py-2 text-left font-semibold">Level</th>
                    <th className="px-4 py-2 text-left font-semibold">Active</th>
                    <th className="px-4 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {scholarships.map((s) => (
                    <tr key={s.id} className="border-t border-slate-100 dark:border-slate-700">
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.id}</td>
                      <td className="px-4 py-2 font-medium text-slate-900 dark:text-slate-100">{s.title}</td>
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.provider ?? "—"}</td>
                      <td className="px-4 py-2 text-slate-600 dark:text-slate-400">{s.level ?? "—"}</td>
                      <td className="px-4 py-2">
                        <span
                          className={`rounded px-2 py-0.5 text-xs font-medium ${
                            s.is_active !== false
                              ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                              : "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400"
                          }`}
                        >
                          {s.is_active !== false ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <button
                          type="button"
                          onClick={() => handleDelete(s.id)}
                          className="text-red-600 hover:text-red-700 disabled:opacity-50"
                          disabled={s.is_active === false}
                        >
                          Deactivate
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
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
                </li>
              ))
            )}
          </ul>
        )}

        {tab === "system" && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">GET /health</h3>
              <pre className="mt-2 max-h-64 overflow-auto rounded-lg bg-slate-900 p-4 text-xs text-green-200">
                {healthJson ?? "—"}
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Recent scraper runs</h3>
              <div className="mt-2 overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
                <table className="min-w-full text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-800">
                    <tr>
                      <th className="px-3 py-2 text-left">ID</th>
                      <th className="px-3 py-2 text-left">Source</th>
                      <th className="px-3 py-2 text-left">Status</th>
                      <th className="px-3 py-2 text-left">Found</th>
                      <th className="px-3 py-2 text-left">Ingested</th>
                      <th className="px-3 py-2 text-left">Started</th>
                    </tr>
                  </thead>
                  <tbody>
                    {scraperRuns.map((r) => (
                      <tr key={r.id} className="border-t border-slate-100 dark:border-slate-700">
                        <td className="px-3 py-2">{r.id}</td>
                        <td className="px-3 py-2">{r.source}</td>
                        <td className="px-3 py-2">{r.status}</td>
                        <td className="px-3 py-2">{r.records_found ?? "—"}</td>
                        <td className="px-3 py-2">{r.records_ingested ?? "—"}</td>
                        <td className="px-3 py-2 text-xs">{r.started_at}</td>
                      </tr>
                    ))}
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
