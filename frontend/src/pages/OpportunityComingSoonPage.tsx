import { Link, useParams } from "react-router-dom";
import { getOpportunityType, OPPORTUNITY_TYPES } from "../constants/opportunityTypes";

export function OpportunityComingSoonPage() {
  const { typeSlug } = useParams<{ typeSlug: string }>();
  const oppType = typeSlug ? getOpportunityType(typeSlug) : undefined;

  if (!oppType || oppType.available) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-2xl px-4 text-center">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Opportunity type not found</h1>
          <p className="mt-4 text-slate-600 dark:text-slate-400">
            <Link to="/scholarships/search" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Back to Search Opportunities
            </Link>
          </p>
        </div>
      </section>
    );
  }

  const availableTypes = OPPORTUNITY_TYPES.filter((t) => t.available);

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">Coming soon</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">{oppType.label}</h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">{oppType.description}</p>

        <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why it&apos;s not live yet</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{oppType.roadmapNote}</p>
          <p className="mt-4 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            ISKONNECT is becoming a unified student opportunity platform — not just a scholarship directory. During public
            beta, scholarships are the only fully supported opportunity type. Every listing type we add must meet the
            same standard: verified sources, honest eligibility rules, and explainable matching.
          </p>
        </div>

        <div className="mt-8">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Available now</h2>
          <ul className="mt-3 space-y-2">
            {availableTypes.map((t) => (
              <li key={t.slug}>
                <Link
                  to="/scholarships/search"
                  className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
                >
                  {t.label} →
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-12">
          <Link
            to="/scholarships/search"
            className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            ← Back to Search Opportunities
          </Link>
        </div>
      </div>
    </section>
  );
}
