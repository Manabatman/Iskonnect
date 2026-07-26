import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";

const COLLECTION_TABLE = [
  { field: "Name, email", purpose: "Account and profile identity", required: "Yes" },
  { field: "Age, gender, region, school", purpose: "Eligibility matching", required: "For accurate matches" },
  { field: "Education level, GWA, field of study", purpose: "Academic eligibility filters", required: "For accurate matches" },
  { field: "Income bracket / household income", purpose: "Need-based scholarship filters", required: "Optional but unlocks more checks" },
  { field: "Priority group flags (4Ps, PWD, IP, etc.)", purpose: "Targeted program matching", required: "Optional" },
  { field: "Saved scholarships & applications", purpose: "Your planning data", required: "Only if you use these features" },
  { field: "Match history", purpose: "Show past match runs", required: "Automatic when you run matching" },
] as const;

const SUBPROCESSORS = [
  { name: "Supabase", role: "Database, authentication, file storage", location: "Cloud (region configured per project)" },
  { name: "Sentry", role: "Error monitoring (no intentional PII in events)", location: "United States / EU" },
  { name: "Render", role: "API hosting", location: "United States" },
  { name: "Vercel", role: "Frontend hosting & CDN", location: "Global edge" },
] as const;

const VERSION_HISTORY = [
  { version: "2026-07-public-beta", summary: "Honest solo-developer contact; removed formal DPO claim; student project disclosure" },
  { version: "2026-07", summary: "Field collection table, subprocessors, retention periods, export right" },
  { version: "2026-01", summary: "Initial privacy policy — profile data for matching only" },
] as const;

export function PrivacyPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Privacy Policy</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Effective: July 2026 · Version 2026-07-public-beta</p>

        <div className="mt-8 space-y-8 text-slate-700 dark:text-slate-300">
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Who operates ISKONNECT</h2>
            <p className="mt-2">
              ISKONNECT is a student project built and maintained by Mark Justin S. Manabat (University of the
              Philippines Diliman). It is not a registered company and does not have a formal Data Protection Officer.
            </p>
            <p className="mt-2">
              For privacy requests, data access, correction, or erasure under the Data Privacy Act of 2012 (RA 10173),
              contact:
            </p>
            <p className="mt-2">
              <a
                href="mailto:manabat.markjustin@gmail.com"
                className="font-medium text-primary-600 hover:underline dark:text-primary-400"
              >
                manabat.markjustin@gmail.com
              </a>
            </p>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              You can also export or delete your account data directly from{" "}
              <Link to="/settings" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Account Settings
              </Link>
              .
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">What we collect</h2>
            <p className="mt-2">
              We collect only what you provide for scholarship matching and account features. We do not sell your data or
              share it with scholarship providers for marketing.
            </p>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[480px] border-collapse text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-600">
                    <th className="py-2 pr-4 font-semibold text-slate-900 dark:text-slate-100">Field</th>
                    <th className="py-2 pr-4 font-semibold text-slate-900 dark:text-slate-100">Purpose</th>
                    <th className="py-2 font-semibold text-slate-900 dark:text-slate-100">Required?</th>
                  </tr>
                </thead>
                <tbody>
                  {COLLECTION_TABLE.map((row) => (
                    <tr key={row.field} className="border-b border-slate-100 dark:border-slate-700">
                      <td className="py-2 pr-4 align-top">{row.field}</td>
                      <td className="py-2 pr-4 align-top text-slate-600 dark:text-slate-400">{row.purpose}</td>
                      <td className="py-2 align-top text-slate-600 dark:text-slate-400">{row.required}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How we use your data</h2>
            <p className="mt-2">
              Your profile is used to evaluate eligibility against our scholarship catalog, save your preferences, and
              show match history. We may use aggregated, non-identifying analytics to improve the service.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Retention</h2>
            <ul className="mt-2 list-inside list-disc space-y-1">
              <li>
                <strong>Account &amp; profile data:</strong> kept until you delete your account from Settings.
              </li>
              <li>
                <strong>Server &amp; access logs:</strong> retained up to 90 days for security and debugging, then
                deleted or aggregated.
              </li>
              <li>
                <strong>Anonymous feedback:</strong> may be kept after account deletion if submitted without identifying
                details.
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Subprocessors</h2>
            <p className="mt-2">We rely on the following service providers to operate ISKONNECT:</p>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[480px] border-collapse text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-600">
                    <th className="py-2 pr-4 font-semibold">Provider</th>
                    <th className="py-2 pr-4 font-semibold">Role</th>
                    <th className="py-2 font-semibold">Location</th>
                  </tr>
                </thead>
                <tbody>
                  {SUBPROCESSORS.map((row) => (
                    <tr key={row.name} className="border-b border-slate-100 dark:border-slate-700">
                      <td className="py-2 pr-4">{row.name}</td>
                      <td className="py-2 pr-4 text-slate-600 dark:text-slate-400">{row.role}</td>
                      <td className="py-2 text-slate-600 dark:text-slate-400">{row.location}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Your rights</h2>
            <p className="mt-2">
              You may export your data or delete your account from{" "}
              <Link to="/settings" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Account Settings
              </Link>
              . Deletion is permanent and removes your profile, match history, saved scholarships, and applications.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Cookies</h2>
            <p className="mt-2">
              We use cookies and similar storage for session authentication only. We do not use advertising or cross-site
              tracking cookies.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Children</h2>
            <p className="mt-2">
              ISKONNECT is intended for students. Users under 18 should use the service with parental or guardian
              guidance.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Policy version history</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full border-collapse text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-600">
                    <th className="py-2 pr-4 font-semibold">Version</th>
                    <th className="py-2 font-semibold">Summary</th>
                  </tr>
                </thead>
                <tbody>
                  {VERSION_HISTORY.map((row) => (
                    <tr key={row.version} className="border-b border-slate-100 dark:border-slate-700">
                      <td className="py-2 pr-4 font-medium">{row.version}</td>
                      <td className="py-2 text-slate-600 dark:text-slate-400">{row.summary}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
