import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";

interface CatalogQuality {
  active_scholarships: number;
  broken_links: number;
  broken_link_pct: number;
  with_field_evidence: number;
  evidence_pct: number;
  missing_deadline_precision: number;
}

interface Overview {
  total_scholarships: number;
  total_profiles: number;
  total_match_runs: number;
  avg_match_score: number | null;
  scholarships_by_status: Record<string, number>;
  profiles_by_region: Record<string, number>;
  scholarships_by_region: Record<string, number>;
  match_runs_last_30_days: number;
  catalog_quality?: CatalogQuality;
}

export function AdminAnalyticsPage() {
  const { authHeaders } = useAuth();
  const [data, setData] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    apiFetch("/api/v1/admin/analytics/overview", { headers: authHeaders() })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized or failed to load analytics");
        return res.json();
      })
      .then((d: Overview) => setData(d))
      .catch((err) => setError(err instanceof Error ? err.message : "Error"))
      .finally(() => setLoading(false));
  }, [authHeaders]);

  if (loading) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <p className="text-slate-600 dark:text-slate-400">Loading analytics…</p>
        </div>
      </section>
    );
  }

  if (error || !data) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-4">
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300">
            {error || "No data"}
          </div>
          <Button variant="ghost" size="sm" asChild className="mt-4">
            <Link to="/admin">
              <ChevronLeft className="size-4" aria-hidden />
              Back to admin
            </Link>
          </Button>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12">
      <div className="mx-auto max-w-6xl px-4">
        <div className="mb-8 flex items-center justify-between">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">Analytics overview</h2>
          <Link to="/admin" className="text-sm font-medium text-primary-600 hover:underline">
            Scholarship admin
          </Link>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: "Scholarships", value: data.total_scholarships },
            { label: "Profiles", value: data.total_profiles },
            { label: "Match runs (all time)", value: data.total_match_runs },
            { label: "Match runs (30 days)", value: data.match_runs_last_30_days },
          ].map((card) => (
            <div
              key={card.label}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800"
            >
              <p className="text-sm text-slate-500 dark:text-slate-400">{card.label}</p>
              <p className="mt-1 text-3xl font-semibold text-slate-900 dark:text-slate-100">{card.value}</p>
            </div>
          ))}
        </div>

        {data.catalog_quality ? (
          <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Catalog quality
            </h3>
            <ul className="mt-3 grid grid-cols-1 gap-2 text-sm text-slate-700 dark:text-slate-300 sm:grid-cols-2">
              <li>Active scholarships: <strong>{data.catalog_quality.active_scholarships}</strong></li>
              <li>With field evidence: <strong>{data.catalog_quality.with_field_evidence}</strong> ({data.catalog_quality.evidence_pct}%)</li>
              <li>Broken links: <strong>{data.catalog_quality.broken_links}</strong> ({data.catalog_quality.broken_link_pct}%)</li>
              <li>Missing deadline precision: <strong>{data.catalog_quality.missing_deadline_precision}</strong></li>
            </ul>
          </div>
        ) : null}

        {data.avg_match_score != null ? (
          <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <p className="text-sm text-slate-500 dark:text-slate-400">Average match score (stored results)</p>
            <p className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              {data.avg_match_score.toFixed(1)}
            </p>
          </div>
        ) : null}

        <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Scholarships by status
            </h3>
            <ul className="mt-2 space-y-1 text-sm text-slate-700 dark:text-slate-300">
              {Object.entries(data.scholarships_by_status).map(([k, v]) => (
                <li key={k}>
                  {k}: <strong>{v}</strong>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Profiles by region
            </h3>
            <ul className="mt-2 max-h-48 space-y-1 overflow-auto text-sm text-slate-700 dark:text-slate-300">
              {Object.entries(data.profiles_by_region)
                .slice(0, 20)
                .map(([k, v]) => (
                  <li key={k}>
                    {k}: <strong>{v}</strong>
                  </li>
                ))}
            </ul>
          </div>
          <div className="lg:col-span-2">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Scholarships by eligible regions
            </h3>
            <ul className="mt-2 max-h-48 space-y-1 overflow-auto text-sm text-slate-700 dark:text-slate-300">
              {Object.entries(data.scholarships_by_region)
                .slice(0, 20)
                .map(([k, v]) => (
                  <li key={k}>
                    {k}: <strong>{v}</strong>
                  </li>
                ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
