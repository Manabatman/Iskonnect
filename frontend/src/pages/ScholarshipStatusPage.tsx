import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import {
  Archive,
  CalendarClock,
  CheckCircle2,
  ClipboardList,
  Clock,
  HelpCircle,
  History,
  Lock,
  TrendingUp,
} from "lucide-react";
import { BackNavLink } from "../components/BackNavLink";
import { LifecycleStatusExample } from "../components/LifecycleStatusBadge";
import {
  LIFECYCLE_STATUS_GUIDE,
  UI_ELIGIBILITY_GUIDE,
  type ScholarshipLifecycleStatus,
  type UiEligibilityState,
} from "../utils/scholarshipStatus";

const lifecycleIcons: Record<ScholarshipLifecycleStatus, ReactNode> = {
  open: <CheckCircle2 className="h-5 w-5" />,
  closed: <Lock className="h-5 w-5" />,
  previous_cycle: <History className="h-5 w-5" />,
  expected_reopen: <CalendarClock className="h-5 w-5" />,
  archived: <Archive className="h-5 w-5" />,
  needs_verification: <HelpCircle className="h-5 w-5" />,
};

const eligibilityIcons: Record<UiEligibilityState, ReactNode> = {
  eligible_now: <CheckCircle2 className="h-5 w-5" />,
  opening_soon: <Clock className="h-5 w-5" />,
  prepare_ahead: <ClipboardList className="h-5 w-5" />,
  future_eligibility: <TrendingUp className="h-5 w-5" />,
};

function StatusRow({
  label,
  shortDescription,
  whatToDo,
  icon,
  badge,
}: {
  label: string;
  shortDescription: string;
  whatToDo: string;
  icon: ReactNode;
  badge?: ReactNode;
}) {
  return (
    <details className="group rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900/60">
      <summary className="cursor-pointer list-none px-4 py-3 pr-12 outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-900 [&::-webkit-details-marker]:hidden">
        <span className="flex items-start gap-3">
          <span className="mt-0.5 shrink-0 text-primary-600 dark:text-primary-400" aria-hidden>
            {icon}
          </span>
          <span className="min-w-0 flex-1">
            <span className="flex flex-wrap items-center gap-2">
              <span className="font-semibold text-slate-900 dark:text-slate-100">{label}</span>
              {badge}
            </span>
            <span className="mt-1 block text-sm text-slate-600 dark:text-slate-400">{shortDescription}</span>
          </span>
          <span className="shrink-0 text-slate-400 transition motion-safe:group-open:rotate-180" aria-hidden>
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </span>
        </span>
      </summary>
      <div className="border-t border-slate-100 px-4 py-3 text-sm leading-relaxed text-slate-600 dark:border-slate-700 dark:text-slate-400">
        {whatToDo}
      </div>
    </details>
  );
}

export function ScholarshipStatusPage() {
  const lifecycleItems = Object.entries(LIFECYCLE_STATUS_GUIDE).map(([key, entry]) => ({
    id: key,
    label: entry.label,
    shortDescription: entry.shortDescription,
    whatToDo: entry.whatToDo,
    icon: lifecycleIcons[key as ScholarshipLifecycleStatus],
    badge: <LifecycleStatusExample statusKey={key} />,
  }));

  const eligibilityItems = Object.entries(UI_ELIGIBILITY_GUIDE).map(([key, entry]) => ({
    id: key,
    label: entry.label,
    shortDescription: entry.shortDescription,
    whatToDo: entry.whatToDo,
    icon: eligibilityIcons[key as UiEligibilityState],
  }));

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Scholarship status guide</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Quick labels tell you whether to apply now, prepare for later, or use a scholarship for reference. Expand any
          row for what to do next.
        </p>

        <div
          className="mt-6 rounded-xl border border-amber-200 bg-amber-50 p-5 dark:border-amber-800 dark:bg-amber-950/40"
          role="note"
          data-testid="status-guide-disclaimer"
        >
          <p className="text-sm font-semibold text-amber-950 dark:text-amber-100">Important</p>
          <p className="mt-2 text-sm leading-relaxed text-amber-900/90 dark:text-amber-100/90">
            Labels are guides based on the information we have. Scholarship providers make the final call on eligibility
            and deadlines. &quot;Needs verification&quot; means you should confirm details on the official provider site
            before applying. ISKONNECT does not guarantee funding or acceptance.
          </p>
        </div>

        <div className="mt-12">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Application cycle status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Whether a scholarship is accepting applications right now.
          </p>
          <div className="mt-4 space-y-2">
            {lifecycleItems.map(({ id, label, shortDescription, whatToDo, icon, badge }) => (
              <StatusRow
                key={id}
                label={label}
                shortDescription={shortDescription}
                whatToDo={whatToDo}
                icon={icon}
                badge={badge}
              />
            ))}
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Your eligibility status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            When you&apos;re signed in, cards may also show how you fit based on your profile.
          </p>
          <div className="mt-4 space-y-2">
            {eligibilityItems.map(({ id, label, shortDescription, whatToDo, icon }) => (
              <StatusRow
                key={id}
                label={label}
                shortDescription={shortDescription}
                whatToDo={whatToDo}
                icon={icon}
              />
            ))}
          </div>
        </div>

        <div className="mt-12 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80">
          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Closed scholarships stay visible so you can plan for the next cycle. Read{" "}
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
