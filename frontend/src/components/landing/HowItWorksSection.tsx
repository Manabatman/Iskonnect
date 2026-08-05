import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { howItWorksSteps } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function HowItWorksSection() {
  return (
    <Section variant="white" border="bottom" data-testid="landing-how-it-works">
      <SectionHeader
        eyebrow="How it works"
        title="From profile to ranked matches in three steps."
        description="We don't guess. Every match is based on actual program rules and your real profile."
      />
      <div className="mt-12 grid gap-6 sm:mt-16 md:grid-cols-3">
        {howItWorksSteps.map(({ n, title, body, Icon }, i) => (
          <Reveal key={title} delay={i * 0.08}>
            <article className={cardClass}>
              <div className="flex items-center gap-3">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-700 dark:bg-primary-900/60 dark:text-primary-300">
                  {n}
                </span>
                <IconTile Icon={Icon} />
              </div>
              <h3 className="mt-5 text-lg font-bold tracking-tight text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
            </article>
          </Reveal>
        ))}
      </div>
      <Reveal delay={0.24}>
        <p className="mt-10 text-center">
          <Link
            to="/how-it-works"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary-600 transition hover:text-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-primary-400 dark:hover:text-primary-300 dark:focus-visible:ring-offset-slate-900"
          >
            See the full process
            <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" aria-hidden />
          </Link>
        </p>
      </Reveal>
    </Section>
  );
}
