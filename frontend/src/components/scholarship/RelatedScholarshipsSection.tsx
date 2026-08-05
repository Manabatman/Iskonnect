import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiFetch } from "../../api/client";
import type { ScholarshipInfo } from "../../types";

interface RelatedScholarshipsSectionProps {
  scholarshipId: number;
  region?: string;
  field?: string;
  educationLevel?: string;
  provider?: string;
}

/** Similar programs via browse search — forward momentum (Wave 5 / L5). */
export function RelatedScholarshipsSection({
  scholarshipId,
  region,
  field,
  educationLevel,
  provider,
}: RelatedScholarshipsSectionProps) {
  const [related, setRelated] = useState<ScholarshipInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    const params = new URLSearchParams();
    if (region) params.set("region", region);
    if (field) params.set("field", field);
    if (educationLevel) params.set("education_level", educationLevel);
    if (provider) params.set("provider", provider);
    params.set("limit", "6");
    params.set("page", "1");
    params.set("sort", "relevance");

    apiFetch(`/api/v1/scholarships/search?${params.toString()}`)
      .then((res) => (res.ok ? res.json() : { results: [] }))
      .then((data: { results?: ScholarshipInfo[] }) => {
        if (cancelled) return;
        const list = (data.results ?? []).filter((s) => s.id !== scholarshipId).slice(0, 4);
        setRelated(list);
      })
      .catch(() => {
        if (!cancelled) setRelated([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [scholarshipId, region, field, educationLevel, provider]);

  if (loading) {
    return (
      <section className="mt-8" aria-labelledby="related-scholarships-heading" aria-busy="true">
        <h2 id="related-scholarships-heading" className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          Similar programs you may qualify for
        </h2>
        <div className="mt-3 h-20 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-700" />
      </section>
    );
  }

  if (related.length === 0) return null;

  return (
    <section className="mt-8" aria-labelledby="related-scholarships-heading">
      <h2
        id="related-scholarships-heading"
        className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400"
      >
        Similar programs you may qualify for
      </h2>
      <ul className="mt-3 space-y-2">
        {related.map((s) => (
          <li key={s.id}>
            <Link
              to={`/scholarship/${s.id}`}
              className="focus-visible-ring block rounded-xl border border-slate-200 bg-white px-4 py-3 transition hover:border-primary-300 hover:shadow-sm dark:border-slate-600 dark:bg-slate-800/60 dark:hover:border-primary-700"
            >
              <p className="font-semibold text-slate-900 dark:text-slate-100">{s.title}</p>
              <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{s.provider}</p>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
