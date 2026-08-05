import { Link, Navigate, useParams } from "react-router-dom";
import { OpportunityJourneyTimeline } from "../components/OpportunityJourneyTimeline";
import { OpportunityNotifyForm } from "../components/OpportunityNotifyForm";
import { getOpportunityType } from "../constants/opportunityTypes";

export function OpportunityComingSoonPage() {
  const { typeSlug } = useParams<{ typeSlug: string }>();
  const oppType = typeSlug ? getOpportunityType(typeSlug) : undefined;

  if (!oppType) {
    return (
      <section className="py-12">
        <div className="mx-auto max-w-2xl px-4 text-center">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Opportunity type not found</h1>
          <p className="mt-4 text-slate-600 dark:text-slate-400">
            <Link to="/scholarships/search" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Back to search
            </Link>
          </p>
        </div>
      </section>
    );
  }

  if (oppType.available && oppType.searchPath) {
    return <Navigate to={oppType.searchPath} replace />;
  }

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
          {oppType.label} on your opportunity journey
        </h1>
        <p className="mt-3 text-lg text-slate-600 dark:text-slate-400">{oppType.description}</p>
        {oppType.plannedFor ? (
          <p className="mt-2 text-sm font-medium text-primary-700 dark:text-primary-300">
            Planned for {oppType.plannedFor}
          </p>
        ) : null}

        <div className="mt-12">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Your opportunity journey</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            ISKONNECT is building one place for every student opportunity, starting with scholarships.
          </p>
          <div className="mt-6">
            <OpportunityJourneyTimeline selectedSlug={oppType.slug} linkItems />
          </div>
        </div>

        <div className="mt-12 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why we build in this order</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Every new opportunity type must meet the same bar as scholarships: verified sources, honest eligibility rules,
            and explainable matching. {oppType.roadmapNote}
          </p>
          <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            We ship verticals when the data and workflows are trustworthy, not before.
          </p>
        </div>

        <div className="mt-12 rounded-2xl border border-primary-200 bg-primary-50/50 p-6 dark:border-primary-800 dark:bg-primary-950/30">
          <OpportunityNotifyForm opportunitySlug={oppType.slug} opportunityLabel={oppType.label} />
        </div>

        <div className="mt-12 flex flex-wrap gap-4">
          <Link
            to="/scholarships/search"
            className="focus-visible-ring inline-flex min-h-[44px] items-center rounded-xl bg-primary-600 px-6 py-3 text-sm font-semibold text-white shadow-md hover:bg-primary-700"
          >
            Explore scholarships now
          </Link>
          <Link
            to="/scholarships/search"
            className="inline-flex min-h-[44px] items-center text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
          >
            Back to search
          </Link>
        </div>
      </div>
    </section>
  );
}
