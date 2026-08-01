import { proofStripItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader } from "./Section";

function ProofFrame({ variant }: { variant: (typeof proofStripItems)[number]["variant"] }) {
  const palettes: Record<string, { bar: string; chip: string; line: string }> = {
    matches: { bar: "bg-primary-500", chip: "bg-emerald-100 text-emerald-800", line: "w-3/4" },
    breakdown: { bar: "bg-violet-500", chip: "bg-primary-100 text-primary-800", line: "w-2/3" },
    search: { bar: "bg-sky-500", chip: "bg-amber-100 text-amber-900", line: "w-5/6" },
    mobile: { bar: "bg-primary-600", chip: "bg-slate-100 text-slate-700", line: "w-4/5" },
  };
  const p = palettes[variant] ?? palettes.matches;

  return (
    <div
      className="aspect-[16/10] w-full overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900"
      aria-hidden
    >
      <div className={`h-2 ${p.bar}`} />
      <div className="space-y-2 p-3">
        <div className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-semibold ${p.chip}`}>Eligible</div>
        <div className={`h-2 rounded bg-slate-200 dark:bg-slate-700 ${p.line}`} />
        <div className="h-2 w-1/2 rounded bg-slate-100 dark:bg-slate-800" />
        <div className="mt-3 h-8 rounded-lg bg-slate-50 dark:bg-slate-800/80" />
      </div>
    </div>
  );
}

export function ProofStripSection() {
  return (
    <Section variant="white" border="bottom" id="proof">
      <SectionHeader
        align="left"
        eyebrow="See the product"
        title="You get clarity before you commit time to an application."
        description="Every screen is built around eligibility fit—not catalog volume."
      />
      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {proofStripItems.map(({ caption, variant }, i) => (
          <Reveal key={caption} delay={i * 0.05}>
            <figure>
              <ProofFrame variant={variant} />
              <figcaption className="mt-3 text-sm leading-snug text-slate-600 dark:text-slate-400">{caption}</figcaption>
            </figure>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
