import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import type { OrganizationProfile } from "../types";
import { apiFetch } from "../api/client";
import { BackNavLink } from "../components/BackNavLink";
import { resolveUserErrorMessage } from "../constants/errorCopy";

export function OrganizationPage() {
  const { slug } = useParams<{ slug: string }>();
  const [org, setOrg] = useState<OrganizationProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) {
      setLoading(false);
      setError("Organization not found");
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFetch(`/api/v1/organizations/${encodeURIComponent(slug)}`)
      .then((res) => {
        if (!res.ok) throw new Error("Organization not found");
        return res.json() as Promise<OrganizationProfile>;
      })
      .then((data) => {
        if (!cancelled) setOrg(data);
      })
      .catch((err) => {
        if (!cancelled) setError(resolveUserErrorMessage(err, "load_failed"));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [slug]);

  if (loading) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-3xl px-4">
          <div className="animate-pulse rounded-xl border border-slate-200 bg-white p-12 dark:border-slate-700 dark:bg-slate-800">
            <div className="h-8 w-2/3 rounded bg-slate-200 dark:bg-slate-700" />
            <div className="mt-4 h-4 w-full rounded bg-slate-100 dark:bg-slate-700" />
          </div>
        </div>
      </section>
    );
  }

  if (error || !org) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-3xl px-4 text-center">
          <p className="text-red-700 dark:text-red-300">{error ?? "Organization not found"}</p>
          <div className="mt-6">
            <BackNavLink />
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <article className="rounded-xl border border-slate-200 bg-white p-8 shadow-md dark:border-slate-700 dark:bg-slate-800">
          <div className="flex flex-wrap items-start gap-4">
            {org.logo_url ? (
              <img
                src={org.logo_url}
                alt=""
                width={64}
                height={64}
                className="h-16 w-16 rounded-lg border border-slate-200 object-contain dark:border-slate-600"
              />
            ) : (
              <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-primary-100 text-xl font-bold text-primary-800 dark:bg-primary-900/40 dark:text-primary-200">
                {org.canonical_name.charAt(0)}
              </div>
            )}
            <div className="min-w-0 flex-1">
              <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">{org.canonical_name}</h1>
              {org.org_type ? (
                <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{org.org_type}</p>
              ) : null}
              {org.verification_status ? (
                <p className="mt-2 text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Provider status: {org.verification_status.replace(/_/g, " ")}
                </p>
              ) : null}
            </div>
          </div>

          <dl className="mt-8 grid gap-4 sm:grid-cols-3">
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-900/40">
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Active programs
              </dt>
              <dd className="mt-1 text-2xl font-bold text-slate-900 dark:text-slate-100">{org.opportunity_count}</dd>
            </div>
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-900/40">
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Avg. data freshness
              </dt>
              <dd className="mt-1 text-2xl font-bold text-slate-900 dark:text-slate-100">
                {org.avg_freshness_days != null ? `${org.avg_freshness_days}d` : "—"}
              </dd>
            </div>
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-600 dark:bg-slate-900/40">
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Community reports
              </dt>
              <dd className="mt-1 text-2xl font-bold text-slate-900 dark:text-slate-100">{org.report_count}</dd>
            </div>
          </dl>

          {org.website ? (
            <p className="mt-6">
              <a
                href={org.website}
                target="_blank"
                rel="noreferrer"
                className="text-sm font-semibold text-primary-600 hover:underline dark:text-primary-400"
              >
                Official website →
              </a>
            </p>
          ) : null}

          <p className="mt-6 text-sm text-slate-600 dark:text-slate-400">
            Browse scholarships from this provider in{" "}
            <Link to="/scholarships/search" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              scholarship search
            </Link>
            . Counts reflect active scholarships on ISKONNECT, not guaranteed availability on the provider&apos;s site.
          </p>
        </article>

        <div className="mt-8">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
