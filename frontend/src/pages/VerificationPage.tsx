import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import { LIFECYCLE_STATUS_GUIDE } from "../utils/scholarshipStatus";

const sources = [
  "CHED (Commission on Higher Education)",
  "DOST-SEI (Department of Science and Technology — Science Education Institute)",
  "TESDA (Technical Education and Skills Development Authority)",
  "Local government units (LGUs)",
  "Universities and state colleges",
  "Private foundations and corporate sponsors",
];

const verificationChecks = [
  "We confirm the scholarship exists through an official source.",
  "We verify application dates, eligibility requirements, and benefits.",
  "We check for duplicate listings.",
  "We ensure every listing links back to the official provider.",
  "We flag uncertain information for additional review before publication.",
];

export function VerificationPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">How we verify scholarships</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Can you trust the information on ISKONNECT? This page explains how we review listings, what
          &quot;verified&quot; means, and what we still ask you to confirm on your own.
        </p>

        <div className="mt-10 space-y-10 text-slate-700 dark:text-slate-300">
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What ISKONNECT verifies</h2>
            <p className="mt-2 leading-relaxed">
              ISKONNECT helps you discover scholarships, but we are not the scholarship provider.
            </p>
            <p className="mt-3 leading-relaxed">
              Before a scholarship appears in our catalog, we review its source, eligibility requirements,
              application period, and official links. We also continue monitoring listings for updates whenever
              possible.
            </p>
            <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
              We still recommend confirming important details on the provider&apos;s official website before
              submitting an application.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Where our information comes from</h2>
            <p className="mt-2 leading-relaxed">
              We gather scholarship details from publicly available official sources, including:
            </p>
            <ul className="mt-3 list-inside list-disc space-y-1 text-sm">
              {sources.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
            <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
              Each listing links back to the provider&apos;s site so you can verify eligibility, deadlines, and
              requirements yourself.
            </p>
          </section>

          <section className="rounded-xl border border-primary-200 bg-primary-50/60 p-5 dark:border-primary-800 dark:bg-primary-950/30">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What &quot;Verified&quot; means</h2>
            <p className="mt-2 leading-relaxed">
              A verified scholarship has been checked against an official source by our team or automated
              verification process. Verification means the information matched the official source at the time it
              was reviewed.
            </p>
            <p className="mt-3 leading-relaxed">
              Because scholarship providers can update their requirements at any time, we still recommend checking
              the official announcement before applying. &quot;Verified&quot; is not a guarantee of funding or
              acceptance—it means we believe the listing was accurate when we last checked it.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How we verify scholarships</h2>
            <p className="mt-2 leading-relaxed">
              Every scholarship goes through multiple checks before being published:
            </p>
            <ul className="mt-4 list-inside list-disc space-y-2 text-sm leading-relaxed">
              {verificationChecks.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Verification status</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              Status labels help you decide whether to apply now, prepare for later, or use a listing for reference.
              See also our{" "}
              <Link to="/scholarship-status" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Scholarship Status Guide
              </Link>{" "}
              for what to do in each situation.
            </p>
            <ul className="mt-4 space-y-4">
              {Object.values(LIFECYCLE_STATUS_GUIDE).map((entry) => (
                <li key={entry.label} className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
                  <p className="font-medium text-slate-900 dark:text-slate-100">{entry.label}</p>
                  <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{entry.shortDescription}</p>
                </li>
              ))}
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why past cycles stay visible</h2>
            <p className="mt-2 leading-relaxed">
              Closed or previous-cycle scholarships remain in ISKONNECT so you can learn typical requirements, plan for
              the next opening, and compare benefits—even when you can&apos;t apply right now.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Last verified</h2>
            <p className="mt-2 leading-relaxed">
              When our team or automated checks confirm a listing against an official source, we record the date.
              You&apos;ll see labels like &quot;Verified Mar 15, 2026&quot; on scholarship cards and detail pages.
            </p>
            <p className="mt-3 leading-relaxed">
              If a listing hasn&apos;t been checked recently, we show &quot;Not yet verified&quot; so you know to
              double-check on the provider&apos;s site before relying on the details.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How freshness works</h2>
            <p className="mt-2 leading-relaxed">
              Freshness chips summarize what we know—verification date, source, and whether a cycle has closed. They
              guide your judgment; they do not replace reading the official announcement.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How matching works</h2>
            <p className="mt-2 leading-relaxed">
              ISKONNECT compares the information you provide—such as your school level, location, income, and academic
              profile—with the eligibility requirements published by scholarship providers.
            </p>
            <p className="mt-3 leading-relaxed">
              Matches indicate scholarships you may qualify for based on available information. They are not guarantees
              of eligibility or acceptance. Providers make the final decision.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Report an issue</h2>
            <p className="mt-2 leading-relaxed">
              Found a broken link, wrong deadline, or outdated requirement? Use &quot;Report an issue&quot; on any
              scholarship page. Reports are reviewed by our team. You can also reach us through the feedback option in
              the app.
            </p>
          </section>

          <section className="rounded-xl border border-amber-200 bg-amber-50 p-5 dark:border-amber-800 dark:bg-amber-950/40">
            <h2 className="text-lg font-semibold text-amber-900 dark:text-amber-100">What we do not guarantee</h2>
            <p className="mt-2 text-sm leading-relaxed text-amber-900/90 dark:text-amber-100/90">
              ISKONNECT does not guarantee admission, funding, or that every detail is current. Scholarship providers
              may change income ceilings, document requirements, or deadlines without telling us. Matching shows
              programs you may qualify for based on the information we have—it is not a promise of acceptance. Always
              confirm on the official provider&apos;s website before applying.
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
