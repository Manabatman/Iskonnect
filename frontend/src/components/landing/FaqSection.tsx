import { Link } from "react-router-dom";
import { faqItems } from "./landingData";
import { Reveal } from "./Reveal";
import { Section, SectionHeader } from "./Section";

export function FaqSection() {
  return (
    <Section variant="tint" border="bottom" id="faq" data-testid="landing-faq">
      <SectionHeader
        eyebrow="FAQ"
        title="Common questions"
        description="Straight answers about matching, trust, and how we handle your data."
      />
      <div className="mx-auto mt-12 max-w-2xl space-y-2 sm:mt-16">
        {faqItems.slice(0, 5).map((item, i) => (
          <Reveal key={item.q} delay={i * 0.06}>
            <details className="group rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900/60">
              <summary className="cursor-pointer list-none px-4 py-3 pr-10 text-sm font-semibold text-slate-900 outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:text-slate-100 dark:focus-visible:ring-offset-slate-900 [&::-webkit-details-marker]:hidden">
                <span className="flex items-center justify-between gap-2">
                  {item.q}
                  <span className="text-slate-400 transition motion-safe:group-open:rotate-180" aria-hidden>
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </span>
              </summary>
              <div className="border-t border-slate-100 px-4 py-3 text-sm leading-relaxed text-slate-600 dark:border-slate-700 dark:text-slate-400">
                {item.q === "How is my personal data used?" ? (
                  <>
                    Your profile data is used only to match you with scholarships. We don&apos;t sell it or share it
                    with scholarship providers. See our{" "}
                    <Link
                      to="/privacy"
                      className="font-medium text-primary-600 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:text-primary-400"
                    >
                      Privacy Policy
                    </Link>{" "}
                    for full details.
                  </>
                ) : item.q === "Where does scholarship information come from?" ? (
                  <>
                    From official public sources (CHED, DOST-SEI, TESDA, LGUs, universities, and foundations). Read{" "}
                    <Link
                      to="/how-we-verify"
                      className="font-medium text-primary-600 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:text-primary-400"
                    >
                      how we verify scholarships
                    </Link>
                    .
                  </>
                ) : (
                  item.a
                )}
              </div>
            </details>
          </Reveal>
        ))}
        <p className="pt-4 text-center text-sm">
          <Link to="/faq" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
            View all FAQs
          </Link>
        </p>
      </div>
    </Section>
  );
}
