import { problemItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function ProblemSection() {
  return (
    <Section variant="tint" border="bottom" data-testid="landing-problem">
      <SectionHeader
        eyebrow="The problem"
        title="Searching for scholarships shouldn't be this hard."
        description="Filipino students spend hours jumping between government sites, university pages, and social media, often without knowing if they even qualify."
      />
      <div className="mt-12 grid gap-6 sm:mt-16 md:grid-cols-3">
        {problemItems.map(({ title, body, Icon }, i) => (
          <Reveal key={title} delay={i * 0.08}>
            <article className={cardClass}>
              <IconTile Icon={Icon} />
              <h3 className="mt-5 text-lg font-bold tracking-tight text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
