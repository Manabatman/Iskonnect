import { BackNavLink } from "../components/BackNavLink";

const CONTACT_EMAIL = "manabat.markjustin@gmail.com";

export function ContactPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Contact</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          Questions about scholarships, data privacy, bug reports, or partnership inquiries.
        </p>

        <div className="mt-8 space-y-8 text-slate-700 dark:text-slate-300">
          <section className="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Mark Justin S. Manabat</h2>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">Student Developer</p>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">University of the Philippines Diliman</p>
            <a
              href={`mailto:${CONTACT_EMAIL}`}
              className="mt-4 inline-block text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
            >
              {CONTACT_EMAIL}
            </a>
            <p className="mt-4 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
              ISKONNECT is currently built and maintained by a solo student developer. There is no company office or
              support team — you will reach me directly.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What you can reach out about</h2>
            <ul className="mt-2 list-inside list-disc space-y-1 text-sm">
              <li>Scholarship corrections (also available on each scholarship detail page)</li>
              <li>Privacy requests — account export and deletion are in Account Settings</li>
              <li>Bug reports and product feedback</li>
              <li>Partnership or verification inquiries from scholarship providers, LGUs, or institutions</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Response time</h2>
            <p className="mt-2 text-sm">
              I aim to respond within a few business days. Scholarship data corrections reported through opportunity
              detail pages are routed to the admin review queue.
            </p>
          </section>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
