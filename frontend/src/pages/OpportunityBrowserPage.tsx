import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { SplitLayout } from "../components/layout/SplitLayout";
import { OpportunityDetail } from "../components/OpportunityDetail";
import { OpportunityList } from "../components/OpportunityList";
import { scholarshipToOpportunity } from "../data/scholarshipToOpportunity";
import { MOCK_OPPORTUNITIES, type Opportunity } from "../data/mockOpportunities";
import { useScholarshipSearch } from "../hooks/useScholarshipSearch";

function ListSkeleton() {
  return (
    <div className="space-y-3" aria-hidden>
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className="animate-pulse rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800"
        >
          <div className="h-4 w-3/4 rounded bg-slate-200 dark:bg-slate-700" />
          <div className="mt-2 h-3 w-1/2 rounded bg-slate-200 dark:bg-slate-700" />
          <div className="mt-2 h-3 w-2/5 rounded bg-slate-200 dark:bg-slate-700" />
          <div className="mt-3 flex gap-1">
            <div className="h-5 w-14 rounded-full bg-slate-200 dark:bg-slate-700" />
            <div className="h-5 w-20 rounded-full bg-slate-200 dark:bg-slate-700" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function OpportunityBrowserPage() {
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const { results, loading, error } = useScholarshipSearch({
    limit: 50,
    enableSuggestions: false,
    syncUrlQuery: false,
  });

  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [usingMock, setUsingMock] = useState(false);

  useEffect(() => {
    if (loading) return;
    if (error) {
      if (import.meta.env.DEV) {
        setOpportunities(MOCK_OPPORTUNITIES);
        setUsingMock(true);
      } else {
        setOpportunities([]);
        setUsingMock(false);
      }
      return;
    }
    setUsingMock(false);
    setOpportunities(results.map(scholarshipToOpportunity));
  }, [loading, error, results]);

  const selectedOpportunity = useMemo(
    () => (selectedId != null ? opportunities.find((o) => o.id === selectedId) ?? null : null),
    [opportunities, selectedId]
  );

  return (
    <section className="px-4 py-6 sm:px-6 lg:py-8" aria-labelledby="opportunity-browser-heading">
      <div className="mx-auto max-w-7xl">
        {usingMock ? (
          <div
            role="status"
            className="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950/80 dark:text-amber-100"
          >
            Showing sample data — server unavailable.
          </div>
        ) : null}

        <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1
              id="opportunity-browser-heading"
              className="text-2xl font-semibold text-slate-900 dark:text-slate-100"
            >
              Opportunity browser
            </h1>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
              {loading ? "Loading listings…" : `${opportunities.length} opportunities`}
            </p>
          </div>
          <Link
            to="/scholarships/search"
            className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
          >
            Advanced scholarship search
          </Link>
        </div>

        {loading ? (
          <div className="flex min-h-[min(70vh,640px)] flex-col gap-4 lg:flex-row lg:items-start lg:gap-6">
            <div className="max-h-[min(50vh,480px)] w-full shrink-0 overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-800 lg:max-h-[calc(100vh-8rem)] lg:w-[min(420px,40%)] lg:min-h-0">
              <ListSkeleton />
            </div>
            <div className="min-h-[min(40vh,320px)] min-w-0 flex-1 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
              <div className="animate-pulse space-y-4">
                <div className="h-8 w-2/3 rounded bg-slate-200 dark:bg-slate-700" />
                <div className="h-4 w-full rounded bg-slate-200 dark:bg-slate-700" />
                <div className="h-4 w-full rounded bg-slate-200 dark:bg-slate-700" />
                <div className="h-4 w-4/5 rounded bg-slate-200 dark:bg-slate-700" />
              </div>
            </div>
          </div>
        ) : !loading && error && !import.meta.env.DEV ? (
          <p className="rounded-xl border border-red-200 bg-red-50 p-8 text-center text-sm text-red-800 dark:border-red-900/50 dark:bg-red-950/40 dark:text-red-200">
            Could not load opportunities. {error} Try again later or use{" "}
            <Link to="/scholarships/search" className="font-medium text-primary-600 dark:text-primary-400">
              advanced search
            </Link>
            .
          </p>
        ) : opportunities.length === 0 ? (
          <p className="rounded-xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
            No opportunities matched. Try{" "}
            <Link to="/scholarships/search" className="font-medium text-primary-600 dark:text-primary-400">
              advanced search
            </Link>
            .
          </p>
        ) : (
          <SplitLayout
            listPane={
              <OpportunityList
                opportunities={opportunities}
                selectedId={selectedId}
                onSelect={setSelectedId}
              />
            }
            detailPane={<OpportunityDetail opportunity={selectedOpportunity} />}
          />
        )}
      </div>
    </section>
  );
}
