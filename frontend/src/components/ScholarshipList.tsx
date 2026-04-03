import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import type { ScholarshipInfo } from "../types";
import { apiFetch } from "../api/client";
import { ScholarshipCardV2 } from "./ScholarshipCardV2";

export function ScholarshipList() {
  const [scholarships, setScholarships] = useState<ScholarshipInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFetch("/api/v1/scholarships")
      .then((res) => {
        if (!res.ok) throw new Error("Unable to fetch scholarships");
        return res.json();
      })
      .then((data: ScholarshipInfo[]) => {
        if (!cancelled) setScholarships(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        if (!cancelled)
          setError(err instanceof Error ? err.message : "Something went wrong");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section id="scholarships" className="py-12">
      <div className="mx-auto max-w-6xl px-4">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
            All Scholarships
            <span className="ml-2 rounded-full bg-primary-100 dark:bg-primary-900 px-2.5 py-0.5 text-sm font-medium text-primary-800 dark:text-primary-300">
              {scholarships.length}
            </span>
          </h2>
          <div className="flex flex-wrap gap-3">
            <Link
              to="/scholarships/search"
              className="w-fit rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-6 py-3 font-semibold text-slate-700 dark:text-slate-300 shadow-md transition hover:bg-slate-50 dark:hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              aria-label="Search scholarships with filters"
            >
              Search Scholarships
            </Link>
            <Link
              to="/profile-builder"
              className="w-fit rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white shadow-md transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              aria-label="Build your profile to get personalized matches"
            >
              Complete Your Profile
            </Link>
          </div>
        </div>

        {loading && (
          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-md">
            <div
              className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-primary-200 border-t-primary-600"
              aria-hidden
            />
            <p className="mt-4 text-slate-600 dark:text-slate-400">Loading scholarships...</p>
          </div>
        )}

        {error && (
          <div
            className="rounded-lg border border-danger-200 bg-danger-50 px-3 py-2 text-sm text-danger-700"
            role="alert"
          >
            {error}
          </div>
        )}

        {!loading && !error && scholarships.length === 0 && (
          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-md">
            <p className="text-slate-600 dark:text-slate-400">No scholarships found.</p>
          </div>
        )}

        {!loading && !error && scholarships.length > 0 && (
          <div className="grid grid-cols-1 items-stretch gap-6 md:grid-cols-2 lg:grid-cols-3">
            {scholarships.map((s) => (
              <ScholarshipCardV2 key={s.id} scholarship={s} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
