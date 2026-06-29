import { Link } from "react-router-dom";
import { BackNavLink } from "../components/BackNavLink";
import { LIFECYCLE_STATUS_GUIDE, UI_ELIGIBILITY_GUIDE } from "../utils/scholarshipStatus";

const toneClasses = {
  success: "border-emerald-200 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950/30",
  warning: "border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-950/30",
  neutral: "border-slate-200 bg-slate-50 dark:border-slate-700 dark:bg-slate-800/50",
  info: "border-primary-200 bg-primary-50 dark:border-primary-800 dark:bg-primary-950/30",
} as const;

function StatusCard({
  label,
  shortDescription,
  whatToDo,
  tone,
}: {
  label: string;
  shortDescription: string;
  whatToDo: string;
  tone: keyof typeof toneClasses;
}) {
  return (
    <article className={`rounded-xl border p-5 ${toneClasses[tone]}`}>
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{label}</h3>
      <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{shortDescription}</p>
      <p className="mt-3 text-sm font-medium text-slate-800 dark:text-slate-200">
        What to do: <span className="font-normal text-slate-700 dark:text-slate-300">{whatToDo}</span>
      </p>
    </article>
  );
}

export function ScholarshipStatusPage() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Scholarship status guide</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          ISKONNECT uses clear labels so you know whether to apply now, prepare for later, or use a listing for
          reference. Here&apos;s what each label means and what we suggest you do next.
        </p>

        <div className="mt-10">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Application cycle status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            These describe whether a scholarship is currently accepting applications.
          </p>
          <div className="mt-6 space-y-4">
            {Object.values(LIFECYCLE_STATUS_GUIDE).map((entry) => (
              <StatusCard key={entry.label} {...entry} />
            ))}
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Your eligibility status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            When you&apos;re signed in, cards may also show how you fit based on your profile.
          </p>
          <div className="mt-6 space-y-4">
            {Object.values(UI_ELIGIBILITY_GUIDE).map((entry) => (
              <StatusCard key={entry.label} {...entry} />
            ))}
          </div>
        </div>

        <div className="mt-12 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80">
          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Labels are guides based on the information we have. Scholarship providers make the final call on eligibility
            and deadlines. Read{" "}
            <Link to="/how-we-verify" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              how we verify scholarships
            </Link>{" "}
            and always confirm on the official site before applying.
          </p>
        </div>

        <div className="mt-12">
          <BackNavLink />
        </div>
      </div>
    </section>
  );
}
