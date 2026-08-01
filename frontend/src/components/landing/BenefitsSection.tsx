import { benefitItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader, cardClass, IconTile } from "./Section";

export function BenefitsSection() {
  return (
    <Section variant="white" border="bottom" id="benefits">
      <SectionHeader
        eyebrow="Outcomes"
        title="Spend less time searching—and more time on applications that fit."
        description="You see programs ranked against your real profile, with clear labels for what is open now versus what to prepare for."
      />
      <div className="mt-10 grid gap-4 sm:mt-12 md:grid-cols-3 md:gap-6">
        {benefitItems.map(({ title, body, Icon }, i) => (
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
        You also get document checklists, saved programs, and reminders in one profile.
      </p>
      <Reveal delay={0.24}>
        <p className="mx-auto mt-10 max-w-2xl text-center text-xs text-slate-500 dark:text-slate-400">
          Always confirm deadlines and requirements on the official provider site before applying.
        </p>
      </Reveal>
    </Section>
  );
}
