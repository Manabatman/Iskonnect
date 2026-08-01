import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { usePublicStats } from "../../hooks/usePublicStats";
import { heroTrustChips } from "./landingData";
import { primaryButtonClass } from "./Section";
import { TrustCounter } from "./TrustCounter";

function HeroProductVisual() {
  return (
    <div
      className="relative mx-auto w-full max-w-md lg:max-w-none"
      aria-hidden
    >
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl shadow-primary-900/10 dark:border-slate-700 dark:bg-slate-900">
        <div className="flex items-center gap-2 border-b border-slate-100 px-4 py-2 dark:border-slate-800">
          <span className="h-2 w-2 rounded-full bg-red-400" />
          <span className="h-2 w-2 rounded-full bg-amber-400" />
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          <span className="ml-2 text-[10px] font-medium text-slate-500">Your scholarship plan</span>
        </div>
        <div className="space-y-3 p-4">
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 dark:border-emerald-900 dark:bg-emerald-950/40">
            <p className="text-xs font-semibold text-emerald-800 dark:text-emerald-200">Strong fit · 87</p>
            <p className="mt-1 text-sm font-medium text-slate-900 dark:text-slate-100">DOST-SEI Undergraduate Scholarship</p>
            <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">Eligible now · Verified recently</p>
          </div>
          <div className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-400">Moderate fit · 72</p>
            <p className="mt-1 text-sm font-medium text-slate-900 dark:text-slate-100">CHED Merit Scholarship Program</p>
          </div>
          <p className="text-[10px] text-slate-500 dark:text-slate-400">
            Scores measure fit—not your odds of winning.
          </p>
        </div>
      </div>
    </div>
  );
}

export function HeroSection() {
  const stats = usePublicStats();

  return (
    <section
      data-testid="landing-hero"
      className="border-b border-slate-200 bg-gradient-to-b from-primary-50/80 via-white to-white dark:border-slate-800 dark:from-slate-950 dark:via-slate-900 dark:to-slate-900"
    >
      <div className="mx-auto grid max-w-[1200px] gap-8 px-4 py-12 sm:px-6 sm:py-16 lg:grid-cols-2 lg:items-center lg:gap-12 lg:py-24">
        <div className="max-w-xl">
          <h1 className="text-balance text-[clamp(2rem,5vw,3.5rem)] font-extrabold leading-[1.1] tracking-tight text-slate-900 dark:text-white">
            Find scholarships you&apos;re actually eligible for.
          </h1>
          <p className="mt-4 max-w-prose text-pretty text-[clamp(0.9375rem,1.2vw,1.125rem)] leading-relaxed text-slate-600 dark:text-slate-300">
            ISKONNECT checks your profile against real program rules—then shows what you can apply for now, prepare for,
            or watch for next cycle. Providers make the final decision; we help you focus on fit.
          </p>

          <div className="mt-6">
            <Link to="/register" className={primaryButtonClass} data-testid="hero-primary-cta">
              Get started free
              <ArrowRight className="h-4 w-4" aria-hidden />
            </Link>
          </div>

          <p className="mt-4 text-sm text-slate-600 dark:text-slate-400">
            <Link to="/how-it-works" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              See how it works
            </Link>
            {" · "}
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Sign in
            </Link>
          </p>

          <ul className="mt-5 flex flex-wrap gap-2" aria-label="Platform highlights">
            {heroTrustChips.map((chip) => (
              <li
                key={chip}
                className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
              >
                <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                {chip}
              </li>
            ))}
          </ul>

          <div className="mt-8 min-h-[5.5rem] max-w-sm border-t border-slate-200 pt-6 dark:border-slate-800">
            {stats?.verified_listing_count != null && stats.verified_listing_count > 0 ? (
              <div className="grid grid-cols-2 gap-4">
                <TrustCounter value={stats.verified_listing_count} label="Verified listings" />
                <TrustCounter value={stats.provider_count} label="Providers" />
              </div>
            ) : null}
          </div>
        </div>

        <div className="hidden sm:block lg:pl-4">
          <HeroProductVisual />
        </div>
      </div>
    </section>
  );
}
