import { BackNavLink } from "../components/BackNavLink";

const DPO_EMAIL = "privacy@iskonnect.ph";
const SUPPORT_EMAIL = "hello@iskonnect.ph";

export function ContactPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Contact</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          Questions about scholarships, data privacy, or partnership inquiries.
        </p>

        <div className="mt-8 space-y-8 text-slate-700 dark:text-slate-300">
          <section className="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Data Protection Officer</h2>
            <p className="mt-2 text-sm">
              For privacy requests, data access, correction, or erasure under RA 10173 (Data Privacy Act of 2012):
            </p>
            <a
              href={`mailto:${DPO_EMAIL}`}
              className="mt-3 inline-block text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
            >
              {DPO_EMAIL}
            </a>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">General inquiries</h2>
            <p className="mt-2 text-sm">Product feedback, bug reports, and scholarship listing corrections:</p>
            <a
              href={`mailto:${SUPPORT_EMAIL}`}
              className="mt-3 inline-block text-sm font-medium text-primary-600 hover:underline dark:text-primary-400"
            >
              {SUPPORT_EMAIL}
            </a>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Partnership &amp; verification</h2>
            <p className="mt-2 text-sm">
              Scholarship providers, LGUs, and institutions interested in listing verification or API integration should
              email{" "}
              <a href={`mailto:${SUPPORT_EMAIL}`} className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                {SUPPORT_EMAIL}
              </a>{" "}
              with your organization name and official domain.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Response time</h2>
            <p className="mt-2 text-sm">
              We aim to respond to privacy requests within 15 business days and general inquiries within 5 business
              days. Scholarship data corrections reported through opportunity detail pages are routed to our admin review
              queue.
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
