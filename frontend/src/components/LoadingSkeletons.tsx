/** Lightweight loading skeletons (P1-07). */

export function RouteFallbackSkeleton() {
  return (
    <div className="mx-auto max-w-6xl animate-pulse px-4 py-8" aria-busy="true" aria-label="Loading page">
      <div className="h-8 w-2/3 max-w-md rounded-lg bg-slate-200 dark:bg-slate-700" />
      <div className="mt-4 h-4 w-full max-w-xl rounded bg-slate-200 dark:bg-slate-700" />
      <div className="mt-2 h-4 w-5/6 max-w-lg rounded bg-slate-200 dark:bg-slate-700" />
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-40 rounded-2xl bg-slate-200 dark:bg-slate-800" />
        ))}
      </div>
    </div>
  );
}

export function DashboardShellSkeleton() {
  return (
    <div className="min-h-screen bg-slate-50 px-4 py-6 dark:bg-slate-900" aria-busy="true" aria-label="Loading dashboard">
      <div className="mx-auto max-w-6xl animate-pulse space-y-6">
        <div className="h-24 rounded-2xl bg-slate-200 dark:bg-slate-800" />
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="h-48 rounded-2xl bg-slate-200 dark:bg-slate-800 lg:col-span-2" />
          <div className="h-48 rounded-2xl bg-slate-200 dark:bg-slate-800" />
        </div>
        <div className="space-y-3">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-28 rounded-xl bg-slate-200 dark:bg-slate-800" />
          ))}
        </div>
      </div>
    </div>
  );
}

export function AuthShellSkeleton() {
  return (
    <div
      className="flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-900"
      aria-busy="true"
      aria-label="Loading"
    >
      <div className="w-full max-w-md animate-pulse space-y-4 px-4">
        <div className="mx-auto h-10 w-10 rounded-full bg-slate-200 dark:bg-slate-700" />
        <div className="h-8 rounded-lg bg-slate-200 dark:bg-slate-700" />
        <div className="h-12 rounded-xl bg-slate-200 dark:bg-slate-700" />
        <div className="h-12 rounded-xl bg-slate-200 dark:bg-slate-700" />
        <div className="h-12 rounded-2xl bg-slate-200 dark:bg-slate-700" />
      </div>
    </div>
  );
}
