import { Link } from "react-router-dom";

const steps = [
  {
    n: 1,
    title: "Create your profile",
    body: "Tell us about your education, region, course interests, and household context. One profile powers every match.",
  },
  {
    n: 2,
    title: "We analyze eligibility",
    body: "We apply each scholarship’s real rules—age, region, income ceiling, course, GPA, and more—before anything is scored.",
  },
  {
    n: 3,
    title: "Get matched and ranked",
    body: "Programs you don’t qualify for are filtered out. The rest are scored and ranked so you see the best fits first.",
  },
] as const;

export function HowItWorksPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">How it works</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">From profile to ranked matches</h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          We don&apos;t guess — we match based on real eligibility criteria from program rules.
        </p>

        <ol className="mt-10 space-y-8">
          {steps.map((s) => (
            <li key={s.n} className="flex gap-4">
              <span
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-600 text-sm font-bold text-white"
                aria-hidden
              >
                {s.n}
              </span>
              <div>
                <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">{s.title}</h2>
                <p className="mt-2 text-slate-600 dark:text-slate-400">{s.body}</p>
              </div>
            </li>
          ))}
        </ol>

        <div
          className="mt-12 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/50"
          aria-hidden
        >
          <p className="text-center text-sm font-medium text-slate-500 dark:text-slate-400">Flow overview</p>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-sm">
            <span className="rounded-lg bg-primary-50 px-3 py-1.5 font-medium text-primary-800 dark:bg-primary-950/50 dark:text-primary-200">
              Profile
            </span>
            <span className="text-slate-400">→</span>
            <span className="rounded-lg bg-slate-100 px-3 py-1.5 font-medium text-slate-800 dark:bg-slate-700 dark:text-slate-200">
              Eligibility checks
            </span>
            <span className="text-slate-400">→</span>
            <span className="rounded-lg bg-primary-50 px-3 py-1.5 font-medium text-primary-800 dark:bg-primary-950/50 dark:text-primary-200">
              Scoring & rank
            </span>
            <span className="text-slate-400">→</span>
            <span className="rounded-lg bg-slate-100 px-3 py-1.5 font-medium text-slate-800 dark:bg-slate-700 dark:text-slate-200">
              Your list
            </span>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            to="/register"
            className="inline-flex rounded-xl bg-primary-600 px-8 py-3 text-base font-semibold text-white shadow-lg shadow-primary-600/20 hover:bg-primary-700"
          >
            Get Started
          </Link>
          <Link to="/login" className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400">
            Already have an account? Sign in
          </Link>
        </div>

        <p className="mt-8 text-center text-sm text-slate-500 dark:text-slate-400">
          Want the details? See{" "}
          <Link to="/transparency" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Matching transparency
          </Link>
          .
        </p>
      </div>
    </section>
  );
}
