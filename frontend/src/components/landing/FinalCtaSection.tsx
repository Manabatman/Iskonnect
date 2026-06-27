import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { Reveal } from "./Reveal";
import { primaryButtonClass } from "./Section";

export function FinalCtaSection() {
  return (
    <section className="border-t border-slate-200 bg-gradient-to-b from-white to-primary-50/50 py-20 dark:border-slate-800 dark:from-slate-900 dark:to-slate-950 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
        <Reveal>
          <h2 className="text-balance text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
            Your next opportunity is one profile away.
          </h2>
          <p className="mx-auto mt-4 max-w-lg text-pretty text-base leading-relaxed text-slate-600 dark:text-slate-400 sm:text-lg">
            Create a free account in minutes. Your matches and saved programs stay in one place.
          </p>
          <Link to="/register" className={`${primaryButtonClass} mt-8`}>
            Create your free account
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
          <p className="mt-4 text-xs text-slate-500 dark:text-slate-400">No cost • Takes ~3 minutes</p>
        </Reveal>
      </div>
    </section>
  );
}
