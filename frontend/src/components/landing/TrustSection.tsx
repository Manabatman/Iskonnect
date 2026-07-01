import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { scoringFactors, trustPoints } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function TrustSection() {
  return (
    <Section variant="tint" border="bottom">
      <SectionHeader
        eyebrow="Why trust us"
        title="Built on transparency, not guesswork."
        description="Your match score measures eligibility fit—not your chances of winning. Here's exactly what goes into it."
      />

      <Reveal delay={0.08}>
        <div className="mt-12 rounded-2xl border border-primary-200 bg-primary-50/80 p-6 shadow-sm dark:border-primary-800 dark:bg-slate-900/80 sm:mt-16 sm:p-8">
          <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">
            How your match score is built
          </p>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            After you pass eligibility checks, five weighted factors combine into a score from 0 to 100. A score of 85
            means your profile strongly matches the program&apos;s criteria—it does <strong>not</strong> mean you have an
            85% chance of receiving the scholarship.
          </p>
          <div className="mt-6 space-y-4">
            {scoringFactors.map((factor) => (
              <div key={factor.name}>
                <div className="flex items-center justify-between gap-2 text-sm">
                  <span className="font-medium text-slate-900 dark:text-slate-100">{factor.name}</span>
                  <span className="rounded-full bg-primary-100 px-2 py-0.5 text-xs font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
                    {factor.weight}%
                  </span>
                </div>
                <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                  <div
                    className="h-full rounded-full bg-primary-500 dark:bg-primary-400"
                    style={{ width: `${factor.weight}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </Reveal>

      <div className="mt-8 grid gap-6 md:grid-cols-3">
        {trustPoints.map(({ title, body, Icon }, i) => (
          <Reveal key={title} delay={0.12 + i * 0.08}>
            <article className={cardClass}>
              <IconTile Icon={Icon} />
              <h3 className="mt-5 text-lg font-bold tracking-tight text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
            </article>
          </Reveal>
        ))}
      </div>

      <Reveal delay={0.32}>
        <p className="mt-10 text-center">
          <Link
            to="/match-methodology"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary-600 transition hover:text-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-primary-400 dark:hover:text-primary-300 dark:focus-visible:ring-offset-slate-900"
          >
            Why these weights exist
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
          <span className="mx-2 text-slate-400" aria-hidden>
            ·
          </span>
          <Link
            to="/transparency"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary-600 transition hover:text-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-primary-400 dark:hover:text-primary-300 dark:focus-visible:ring-offset-slate-900"
          >
            See how scores are built
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
        </p>
      </Reveal>
    </Section>
  );
}
