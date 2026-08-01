import { problemItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function ProblemSection() {
  return (
    <Section variant="tint" border="bottom" id="problem">
      <SectionHeader
        eyebrow="The problem"
        title="You shouldn't need ten tabs open just to find one scholarship you qualify for."
        description="Filipino students jump between government portals, university sites, and social posts—often without knowing if they meet the rules."
      />
      <div className="mt-10 grid gap-4 sm:mt-12 md:grid-cols-3 md:gap-6">
        {problemItems.map(({ title, body, Icon }, i) => (
          <Reveal key={title} delay={i * 0.06}>
            <article className={`${cardClass} ${i > 0 ? "hidden md:flex" : ""}`}>
              <IconTile Icon={Icon} />
              <h3 className="mt-5 text-lg font-bold tracking-tight text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
            </article>
          </Reveal>
        ))}
      </div>
      <p className="mt-4 text-sm text-slate-600 dark:text-slate-400 md:hidden">
        Plus unclear eligibility rules and deadlines that close while you&apos;re still searching.
      </p>
    </Section>
  );
}
