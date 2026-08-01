import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { Reveal } from "./Reveal";
import { primaryButtonClass } from "./Section";

export function FinalCtaSection() {
  return (
    <section
      data-testid="landing-final-cta"
      className="border-t border-slate-200 bg-gradient-to-b from-white to-primary-50/50 py-12 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950 sm:py-16 lg:py-24"
    >
      <div className="mx-auto max-w-[1200px] px-4 text-center sm:px-6">
        <Reveal>
          <h2 className="text-balance text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
            Your next opportunity is one profile away.
          </h2>
          <p className="mx-auto mt-4 max-w-lg text-pretty text-base leading-relaxed text-slate-600 dark:text-slate-400 sm:text-lg">
            Create a free account in minutes. Your scholarship plan, saved programs, and preparation tools stay in one
            place.
          </p>
          <Link to="/register" className={`${primaryButtonClass} mt-8`} data-testid="final-primary-cta">
            Get started free
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
          <p className="mt-4 text-xs text-slate-500 dark:text-slate-400">
            No cost • Takes ~3 minutes •{" "}
            <Link to="/how-matching-works#why" className="underline hover:text-slate-700 dark:hover:text-slate-300">
              Why ISKONNECT exists
            </Link>
          </p>
        </Reveal>
      </div>
    </section>
  );
}
