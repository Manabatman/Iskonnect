import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { HeroCarousel } from "../components/HeroCarousel";
import { HeroDirectionalOverlay } from "../components/visual/DirectionalImageOverlays";
import { SocialProofTicker } from "../components/SocialProofTicker";
import { HERO_CAROUSEL_IMAGES } from "../constants/heroImages";

function IconSparkles({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconClipboard({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        stroke="currentColor"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconRocket({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M15.59 14.37a6 6 0 01-5.84 5.84 2.18 2.18 0 01-2.12-2.12 6 6 0 015.84-5.84m4.24-4.24a2 2 0 010 2.83l-1.41 1.41a2 2 0 01-2.83 0l-4.24-4.24a6 6 0 117.48 7.48z"
        stroke="currentColor"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

const steps = [
  {
    n: 1,
    title: "Build profile",
    body: "Tell us about yourself in a few minutes — one profile powers every match.",
    Icon: IconClipboard,
    accent: "bg-primary-100 text-primary-700 dark:bg-primary-900/50 dark:text-primary-300",
  },
  {
    n: 2,
    title: "Get matched",
    body: "We rank programs using real eligibility rules — not guesswork.",
    Icon: IconSparkles,
    accent: "bg-accent-100 text-accent-700 dark:bg-accent-900/40 dark:text-accent-300",
  },
  {
    n: 3,
    title: "Apply with confidence",
    body: "See deadlines, documents, and next steps in one student-friendly flow.",
    Icon: IconRocket,
    accent: "bg-success-100 text-success-800 dark:bg-success-900/40 dark:text-success-300",
  },
] as const;

/** Feature highlights — honest product explanation, not testimonials. */
const featureHighlights = [
  {
    title: "Eligibility-first matching",
    body: "Scholarships are ranked using program rules you can see — region, level, income, field, and more.",
    Icon: IconSparkles,
  },
  {
    title: "One profile, many programs",
    body: "Build your profile once, then browse, match, and save opportunities without re-entering the same details.",
    Icon: IconClipboard,
  },
  {
    title: "Deadlines and next steps",
    body: "Keep saved programs, reminders, and application tracking in one place alongside official links.",
    Icon: IconRocket,
  },
] as const;

const providerPills = ["CHED / TESDA", "DOST-SEI", "LGUs", "Private institutions"] as const;

export function LandingPage() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && user) {
      navigate("/dashboard", { replace: true });
    }
  }, [loading, user, navigate]);

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
          <p className="text-sm text-slate-500 dark:text-slate-400">Loading…</p>
        </div>
      </div>
    );
  }

  if (user) {
    return null;
  }

  const heroAlts = [
    "Filipino graduates celebrating together",
    "Graduation ceremony in the Philippines",
    "University campus at sunset — inspiration for students",
  ] as const;

  return (
    <div className="overflow-hidden">
      {/* Hero — full-bleed background + overlay copy */}
      <section className="relative min-h-[calc(100vh-4rem)] overflow-hidden border-b border-slate-800">
        <HeroCarousel images={HERO_CAROUSEL_IMAGES} alts={heroAlts} />
        <HeroDirectionalOverlay />
        <div className="relative z-10 mx-auto flex min-h-[calc(100vh-4rem)] max-w-7xl flex-col justify-center px-4 py-16 sm:py-20 lg:py-24">
          <div className="max-w-2xl">
            <h1 className="flex flex-col gap-0 text-4xl font-extrabold tracking-tight leading-none sm:text-5xl lg:text-[3.25rem]">
              <span className="leading-none text-white">Find Scholarships</span>
              <span className="leading-none bg-gradient-to-r from-primary-300 to-accent-300 bg-clip-text text-transparent">
                Matched to your profile
              </span>
            </h1>
            <p className="mt-5 max-w-xl text-lg leading-relaxed text-slate-200">
              Built for Filipino students: build one profile, see ranked matches based on real program rules, and track
              what matters in one place.
            </p>
            <div className="mt-8 flex flex-col gap-4">
              <Link
                to="/register"
                className="inline-flex w-full max-w-xs items-center justify-center gap-2 rounded-2xl bg-primary-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-primary-900/40 transition hover:bg-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2 focus:ring-offset-slate-900 sm:w-auto"
              >
                Get started free
                <span aria-hidden>→</span>
              </Link>
              <p className="text-sm text-slate-400">
                Already have an account?{" "}
                <Link to="/login" className="font-medium text-white underline decoration-primary-400/80 underline-offset-2 hover:text-primary-200">
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </section>

      <SocialProofTicker />

      {/* Your path to success */}
      <section className="border-b border-slate-200 bg-white py-16 dark:border-slate-800 dark:bg-slate-900/40 sm:py-20">
        <div className="mx-auto max-w-7xl px-4">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Your path to success</h2>
            <p className="mt-3 text-slate-600 dark:text-slate-400">Three steps from uncertainty to a clearer plan.</p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {steps.map(({ n, title, body, Icon, accent }) => (
              <div
                key={title}
                className="glass flex flex-col rounded-2xl p-8 transition hover:-translate-y-0.5 hover:shadow-xl"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-700 dark:bg-primary-900/60 dark:text-primary-300">
                    {n}
                  </span>
                  <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${accent}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                </div>
                <h3 className="mt-5 text-lg font-bold text-slate-900 dark:text-white">{title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust */}
      <section className="bg-slate-950 py-16 text-white sm:py-20">
        <div className="mx-auto max-w-7xl px-4">
          <div className="flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-2xl font-bold sm:text-3xl">Built for the Philippines</h2>
              <p className="mt-2 max-w-xl text-sm text-slate-400">
                Programs from government, LGUs, and schools — always verify details on the official site before you
                apply.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {providerPills.map((p) => (
                <span
                  key={p}
                  className="rounded-full border border-white/15 bg-white/5 px-3 py-1 text-xs font-medium text-slate-200">
                  {p}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {featureHighlights.map(({ title, body, Icon }) => (
              <div
                key={title}
                className="glass-dark flex flex-col rounded-2xl border border-white/10 p-6">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-500/20 text-primary-200">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">{title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-300">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-slate-200 bg-gradient-to-b from-white to-slate-50 py-14 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950">
        <div className="mx-auto max-w-7xl px-4 text-center">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white sm:text-3xl">Ready to build your profile?</h2>
          <p className="mx-auto mt-3 max-w-lg text-slate-600 dark:text-slate-400">
            Create a free account in minutes. Your matches and saved programs stay in one place.
          </p>
          <Link
            to="/register"
            className="mt-8 inline-flex rounded-2xl bg-primary-600 px-8 py-3.5 font-semibold text-white shadow-lg shadow-primary-600/25 transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900">
            Create your free account
          </Link>
        </div>
      </section>
    </div>
  );
}
