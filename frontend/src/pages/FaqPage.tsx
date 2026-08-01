import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import { faqItems } from "../components/landing/landingData";

export function FaqPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Frequently asked questions</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Straight answers about matching, trust, and how ISKONNECT helps you plan—not just search—for scholarships.
        </p>

        <div className="mt-10 space-y-3">
          {faqItems.map((item) => (
            <details
              key={item.q}
              className="group rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800/80"
            >
              <summary className="cursor-pointer list-none px-5 py-4 pr-12 text-sm font-semibold text-slate-900 outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:text-slate-100 [&::-webkit-details-marker]:hidden">
                <span className="flex items-center justify-between gap-2">
                  {item.q}
                  <span className="text-slate-400 transition motion-safe:group-open:rotate-180" aria-hidden>
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </span>
              </summary>
              <div className="border-t border-slate-100 px-5 py-4 text-sm leading-relaxed text-slate-600 dark:border-slate-700 dark:text-slate-400">
                {item.q === "How is my personal data used?" ? (
                  <>
                    Your profile data is used only to match you with scholarships. We don&apos;t sell it or share it with
                    scholarship providers. See our{" "}
                    <Link to="/privacy" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                      Privacy Policy
                    </Link>{" "}
                    for full details.
                  </>
                ) : item.q === "Where does scholarship information come from?" ? (
                  <>
                    From official public sources—CHED, DOST-SEI, TESDA, LGUs, universities, and foundations. Read{" "}
                    <Link
                      to="/how-we-verify"
                      className="font-medium text-primary-600 hover:underline dark:text-primary-400"
                    >
                      how we verify scholarships
                    </Link>{" "}
                    for the full process.
                  </>
                ) : (
                  item.a
                )}
              </div>
            </details>
          ))}
        </div>

        <div className="mt-10 rounded-xl border border-slate-200 bg-slate-50 p-5 dark:border-slate-700 dark:bg-slate-800/50">
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Still have questions? Learn{" "}
            <Link to="/how-matching-works#why" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              why ISKONNECT exists
            </Link>{" "}
            or explore{" "}
            <Link to="/how-matching-works" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              how matching works
            </Link>
            .
          </p>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
