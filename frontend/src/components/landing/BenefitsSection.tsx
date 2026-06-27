import { benefitItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function BenefitsSection() {
  return (
    <Section variant="white" border="bottom">
      <SectionHeader
        eyebrow="Why ISKONNECT"
        title="Every Filipino student deserves to discover opportunities they qualify for."
        description="ISKONNECT matches scholarships from government agencies, universities, LGUs, and private organizations based on your profile—so you spend less time searching and more time applying."
      />
      <div className="mt-12 grid gap-6 sm:mt-16 md:grid-cols-3">
        {benefitItems.map(({ title, body, Icon }, i) => (
          <Reveal key={title} delay={i * 0.08}>
            <article className={cardClass}>
              <IconTile Icon={Icon} />
              <h3 className="mt-5 text-lg font-bold tracking-tight text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{body}</p>
            </article>
          </Reveal>
        ))}
      </div>
      <Reveal delay={0.24}>
        <p className="mx-auto mt-10 max-w-2xl text-center text-xs text-slate-500 dark:text-slate-400">
          Always confirm deadlines and requirements on the official provider site before applying.
        </p>
      </Reveal>
    </Section>
  );
}
