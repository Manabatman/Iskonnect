import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiFetch } from "../api/client";
import { BackNavLink } from "../components/BackNavLink";
type CatalogTrust = {
  published_count: number;
  last_catalog_verification_at: string | null;
  verified_within_90d_count: number;
  verification_fresh_days: number;
};

function formatCatalogVerifiedDate(iso: string | null | undefined): string | null {
  if (!iso?.trim()) return null;
  try {
    const d = new Date(iso.slice(0, 10));
    return d.toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" });
  } catch {
    return null;
  }
}

const sources = [
  "CHED (Commission on Higher Education)",
  "DOST-SEI (Department of Science and Technology, Science Education Institute)",
  "TESDA (Technical Education and Skills Development Authority)",
  "Local government units (LGUs)",
  "Universities and state colleges",
  "Private foundations and corporate sponsors",
];

const verificationChecks = [
  "We confirm the scholarship exists through an official source.",
  "We verify application dates, eligibility requirements, and benefits.",
  "We check for duplicate scholarships.",
  "We ensure every scholarship links back to the official provider.",
  "We flag uncertain information for additional review before publication.",
];

export function VerificationPage() {
  const [catalogTrust, setCatalogTrust] = useState<CatalogTrust | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await apiFetch("/api/v1/public/catalog-trust");
        if (!res.ok || cancelled) return;
        setCatalogTrust((await res.json()) as CatalogTrust);
      } catch {
        /* Public page still renders without aggregate stats */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const catalogLastVerified = formatCatalogVerifiedDate(catalogTrust?.last_catalog_verification_at);

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">How we verify scholarships</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Can you trust the information on ISKONNECT? This page explains how we review scholarships, what
          &quot;verified&quot; means, and what we still ask you to confirm on your own.
        </p>

        <div className="mt-12 space-y-12 text-slate-700 dark:text-slate-300">
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What ISKONNECT verifies</h2>
            <p className="mt-2 leading-relaxed">
              ISKONNECT helps you discover scholarships, but we are not the scholarship provider.
            </p>
            <p className="mt-3 leading-relaxed">
              Before a scholarship appears in our catalog, we review its source, eligibility requirements,
              application period, and official links. We re-check scholarships on a rolling basis and show the
              date each scholarship was last verified. We do not promise a fixed re-verification window for every
              program at once.
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
              Each scholarship links back to the provider&apos;s site so you can verify eligibility, deadlines, and
              requirements yourself.
            </p>
          </section>

          <section className="rounded-xl border border-primary-200 bg-primary-50/60 p-5 dark:border-primary-800 dark:bg-primary-950/30">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What &quot;Verified&quot; means</h2>
            <p className="mt-2 leading-relaxed">
              A verified scholarship has been checked against an official source by the ISKONNECT team.
              Verification means the information matched the official source at the time it was reviewed.
            </p>
            <p className="mt-3 leading-relaxed">
              Because scholarship providers can update their requirements at any time, we still recommend checking
              the official announcement before applying. &quot;Verified&quot; is not a guarantee of funding or
              acceptance. It means we believe the scholarship was accurate when we last checked it.
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
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Verification status labels</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              Status labels help you decide whether to apply now, prepare for later, or use a scholarship for reference.
              See our{" "}
              <Link to="/scholarship-status" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Scholarship Status Guide
              </Link>{" "}
              for a scannable summary and full details on each label, including Open now, Needs verification, and Past
              cycle.
            </p>
          </section>
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Why past cycles stay visible</h2>
            <p className="mt-2 leading-relaxed">
              Closed or previous-cycle scholarships remain in ISKONNECT so you can learn typical requirements, plan for
              the next opening, and compare benefits, even when you can&apos;t apply right now.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Last verified</h2>
            <p className="mt-2 leading-relaxed">
              When our team or automated checks confirm a scholarship against an official source, we record the date.
              You&apos;ll see labels like &quot;Verified Mar 15, 2026&quot; on scholarship cards and detail pages.
            </p>
            <p className="mt-3 leading-relaxed">
              If a scholarship hasn&apos;t been checked recently, we show &quot;Not yet verified&quot; so you know to
              double-check on the provider&apos;s site before relying on the details.
            </p>
            {catalogTrust && catalogTrust.published_count > 0 ? (
              <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                {catalogLastVerified ? (
                  <>
                    Across our {catalogTrust.published_count} active scholarships, the most recent verification was on{" "}
                    <span className="font-medium text-slate-800 dark:text-slate-200">{catalogLastVerified}</span>.
                    {catalogTrust.verified_within_90d_count > 0 ? (
                      <>
                        {" "}
                        {catalogTrust.verified_within_90d_count} scholarship
                        {catalogTrust.verified_within_90d_count === 1 ? "" : "s"} were checked within the last{" "}
                        {catalogTrust.verification_fresh_days} days.
                      </>
                    ) : null}
                  </>
                ) : (
                  <>None of our {catalogTrust.published_count} active scholarships have a verification date recorded yet.</>
                )}
              </p>
            ) : null}
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How freshness works</h2>
            <p className="mt-2 leading-relaxed">
              Freshness chips summarize what we know: verification date, source, and whether a cycle has closed. They
              guide your judgment; they do not replace reading the official announcement.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How matching works</h2>
            <p className="mt-2 leading-relaxed">
              ISKONNECT compares the information you provide, such as your school level, location, income, and academic
              profile, with the eligibility requirements published by scholarship providers.
            </p>
            <p className="mt-3 leading-relaxed">
              Matches indicate scholarships you may qualify for based on available information. They are not guarantees
              of eligibility or acceptance. Providers make the final decision. Read{" "}
              <Link
                to="/how-matching-works"
                className="font-medium text-primary-600 hover:underline dark:text-primary-400"
              >
                how matching works
              </Link>{" "}
              for scoring weights, limits, and what your match percentage means.
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
              programs you may qualify for based on the information we have. It is not a promise of acceptance. Always
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
