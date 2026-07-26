import { type ReactNode } from "react";
import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";

const steps = [
  {
    n: 1,
    title: "Build your profile once",
    body: "Tell us your GWA, region, course interests, income range, and household background. You only do this once — every match uses the same profile.",
  },
  {
    n: 2,
    title: "We check actual eligibility rules",
    body: "Each scholarship has real rules — minimum GWA, income ceiling, region, course, age. We check your profile against every one of them before anything is ranked.",
  },
  {
    n: 3,
    title: "Programs you don't qualify for are removed",
    body: "If you can't apply, we don't show it. There's no clutter — only scholarships you're actually eligible for reach your list.",
  },
  {
    n: 4,
    title: "Qualifying scholarships are scored and ranked",
    body: "The ones that remain are scored across five factors: grades, financial need, field of study, location, and priority group (when the program names one). Higher fit = higher position.",
  },
  {
    n: 5,
    title: "You see, save, and apply",
    body: "Your ranked list updates whenever you update your profile. Save scholarships you're interested in and track your applications in one place.",
  },
] as const;

/** Neutral card + left accent stripe — readable in light and dark (no pastel text on dark). */
const flowNodes = [
  { label: "Profile data", accent: "border-l-4 border-l-primary-600 dark:border-l-primary-400" },
  { label: "Eligibility gate", accent: "border-l-4 border-l-slate-500 dark:border-l-slate-400" },
  { label: "Scoring", accent: "border-l-4 border-l-primary-600 dark:border-l-primary-400" },
  { label: "Ranked list", accent: "border-l-4 border-l-emerald-600 dark:border-l-emerald-400" },
  { label: "You apply", accent: "border-l-4 border-l-sky-600 dark:border-l-sky-400" },
] as const;

const faqItems: { q: string; a: ReactNode }[] = [
  {
    q: "Why might my matches change over time?",
    a: "Your matches update when you update your profile, when program rules change, or when administrators adjust scoring weights for a new funding cycle.",
  },
  {
    q: "Could I be missing scholarships I qualify for?",
    a: "Hard eligibility filters only remove programs where your profile clearly fails a required rule (like a region restriction). If data is missing from your profile, you may see fewer results — which is why completing your profile matters.",
  },
  {
    q: "How is my personal data used?",
    a: (
      <>
        Your profile data is used only to match you with scholarships. We don&apos;t sell it or share it with scholarship
        providers. See our{" "}
        <Link to="/privacy" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
          Privacy Policy
        </Link>{" "}
        for full details.
      </>
    ),
  },
];

export function HowItWorksPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600 dark:text-primary-400">How it works</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">
          How Iskonnect finds your scholarships
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          We don&apos;t guess. Every match is based on actual program rules and your real profile.
        </p>

        <div className="mt-10 space-y-4">
          {steps.map((s) => (
            <div
              key={s.n}
              className="flex gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900 sm:flex-row"
            >
              <span
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-600 text-sm font-bold text-white"
                aria-hidden
              >
                {s.n}
              </span>
              <div className="min-w-0">
                <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{s.title}</h2>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400 sm:text-base">{s.body}</p>
              </div>
            </div>
          ))}
        </div>

        <div
          className="mt-10 overflow-x-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900"
          aria-hidden
        >
          <p className="text-center text-sm font-medium text-slate-600 dark:text-slate-300">At a glance</p>
          <div className="mt-4 flex min-w-min flex-nowrap items-center justify-center gap-1 px-1 text-xs font-medium sm:flex-wrap sm:gap-2 sm:text-sm">
            {flowNodes.map((node, i) => (
              <span key={node.label} className="flex shrink-0 items-center gap-1 sm:gap-2">
                <span
                  className={`whitespace-nowrap rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-slate-900 shadow-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100 ${node.accent}`}
                >
                  {node.label}
                </span>
                {i < flowNodes.length - 1 ? (
                  <span className="text-slate-400" aria-hidden>
                    →
                  </span>
                ) : null}
              </span>
            ))}
          </div>
        </div>

        <div className="mt-12" id="matching">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How matching works</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            ISKONNECT uses a two-stage engine: hard eligibility filters remove programs you cannot apply for, then a
            transparent scoring model ranks what remains. Every result includes a qualification status and a list of
            requirements you meet or still need.
          </p>
        </div>

        <div className="mt-10" id="scoring">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How scores are built</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Scores reflect fit across academics, financial need, field of study, location, and priority groups—not a
            black-box AI guess. Higher scores mean stronger alignment with the program&apos;s stated criteria.
          </p>
        </div>

        <div className="mt-10" id="verification">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How we verify scholarships</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Our catalog is built from official provider sources—CHED, DOST, TESDA, LGUs, universities, and foundations.
            Each listing is reviewed by the ISKONNECT team before publication. We re-check listings on a regular
            maintenance schedule and flag stale records for review. Verification means the data matched the official
            source when we last checked—not a guarantee of funding or acceptance.
          </p>
          <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">
            Always confirm deadlines and requirements on the provider&apos;s website before applying.{" "}
            <Link to="/scholarship-status" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Scholarship status guide
            </Link>
          </p>
        </div>

        <div className="mt-12">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Common questions</h2>
          <div className="mt-4 space-y-2">
            {faqItems.map((item) => (
              <details
                key={item.q}
                className="group rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800/40"
              >
                <summary className="cursor-pointer list-none px-4 py-3 pr-10 text-sm font-semibold text-slate-900 outline-none ring-primary-500 focus-visible:ring-2 dark:text-slate-100 [&::-webkit-details-marker]:hidden">
                  <span className="flex items-center justify-between gap-2">
                    {item.q}
                    <span
                      className="text-slate-400 transition group-open:rotate-180"
                      aria-hidden
                    >
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </span>
                  </span>
                </summary>
                <div className="border-t border-slate-100 px-4 py-3 text-sm leading-relaxed text-slate-600 dark:border-slate-700 dark:text-slate-400">
                  {item.a}
                </div>
              </details>
            ))}
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            to="/dashboard"
            className="inline-flex rounded-xl bg-primary-600 px-8 py-3 text-base font-semibold text-white shadow-lg shadow-primary-600/20 hover:bg-primary-700"
          >
            View My Matches
          </Link>
          <Link
            to="/how-we-verify"
            className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            How we verify listings →
          </Link>
        </div>

        <p className="mt-8 text-center text-sm text-slate-500 dark:text-slate-400">
          New here?{" "}
          <Link to="/register" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            Create an account
          </Link>{" "}
          or{" "}
          <Link to="/login" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            sign in
          </Link>
          .
        </p>

        <div className="mt-10 flex justify-center">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
