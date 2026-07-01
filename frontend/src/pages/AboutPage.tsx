import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";

export function AboutPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">About ISKONNECT</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          We help Filipino students discover scholarships they qualify for—today, soon, or in the future—and give them
          time to prepare before deadlines close.
        </p>

        <div className="mt-8 space-y-8 text-slate-700 dark:text-slate-300">
          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Our story</h2>
            <p className="mt-2 leading-relaxed">
              ISKONNECT began as a personal effort to learn backend development while addressing how hard it is for
              Filipino students to discover scholarships—including ones I could have benefited from when I was eligible.
              What started as a learning project in late 2025 grew into a full platform through months of continuous
              iteration, guided by user feedback and a focus on trustworthy scholarship information.
            </p>
            <p className="mt-3 leading-relaxed">
              ISKONNECT is currently in <strong>Public Beta</strong>. The core flows work today, and we are improving
              the catalog, matching, and experience every week.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Our mission</h2>
            <p className="mt-2 leading-relaxed">
              Too many qualified students miss scholarships because programs are scattered, deadlines pass quickly, and
              requirements are hard to understand. ISKONNECT brings government, university, LGU, and private programs
              into one place—and matches them to your real profile so you can plan ahead, not just search.
            </p>
            <p className="mt-3">
              <Link to="/why-iskonnect" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                Why ISKONNECT exists →
              </Link>
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">How matching works</h2>
            <p className="mt-2 leading-relaxed">
              We check your education level, region, field of study, income, and priority group status against each
              scholarship&apos;s actual rules. Programs you clearly don&apos;t qualify for are filtered out. What remains is
              ranked so your strongest fits rise to the top—and you can see why each one matched.
            </p>
            <p className="mt-3">
              <Link to="/transparency" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                How match scores work →
              </Link>
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Trust and verification</h2>
            <p className="mt-2 leading-relaxed">
              Our recommendations are based on publicly available eligibility criteria from official sources. ISKONNECT
              is not affiliated with any scholarship provider. We verify listings before publishing and show when
              information was last checked—but providers can change rules without notice.
            </p>
            <p className="mt-3 leading-relaxed font-medium text-slate-800 dark:text-slate-200">
              Always confirm eligibility, deadlines, and requirements on the official provider&apos;s website before applying.
            </p>
            <p className="mt-3">
              <Link to="/how-we-verify" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
                How we verify scholarships →
              </Link>
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Your data</h2>
            <p className="mt-2 leading-relaxed">
              We do not sell or share your profile with scholarship providers. Your data is used only to compute your
              matches and power your plan. For more details, see our{" "}
              <Link to="/privacy" className="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400">
                Privacy Policy
              </Link>
              .
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
