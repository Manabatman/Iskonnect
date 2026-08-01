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
import { StatusGuideAccordion } from "../components/StatusGuideAccordion";
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

const toneSummaryClasses = {
  success: "border-emerald-200 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950/30",
  warning: "border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-950/30",
  neutral: "border-slate-200 bg-slate-50 dark:border-slate-700 dark:bg-slate-800/50",
  info: "border-primary-200 bg-primary-50 dark:border-primary-800 dark:bg-primary-950/30",
} as const;

function SummaryCard({
  label,
  shortDescription,
  tone,
  icon,
  badge,
}: {
  label: string;
  shortDescription: string;
  tone: keyof typeof toneSummaryClasses;
  icon: ReactNode;
  badge?: ReactNode;
}) {
  return (
    <article className={`rounded-xl border p-4 ${toneSummaryClasses[tone]}`}>
      <div className="flex items-start gap-3">
        <span className="shrink-0 text-primary-600 dark:text-primary-400" aria-hidden>
          {icon}
        </span>
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="font-semibold text-slate-900 dark:text-slate-100">{label}</h3>
            {badge}
          </div>
          <p className="mt-1 text-sm leading-snug text-slate-600 dark:text-slate-400">{shortDescription}</p>
        </div>
      </div>
    </article>
  );
}

export function ScholarshipStatusPage() {
  const lifecycleItems = Object.entries(LIFECYCLE_STATUS_GUIDE).map(([key, entry]) => ({
    id: key,
    label: entry.label,
    shortDescription: entry.shortDescription,
    entry,
    icon: lifecycleIcons[key as ScholarshipLifecycleStatus],
    badge: <LifecycleStatusExample statusKey={key} />,
  }));

  const eligibilityItems = Object.entries(UI_ELIGIBILITY_GUIDE).map(([key, entry]) => ({
    id: key,
    label: entry.label,
    shortDescription: entry.shortDescription,
    entry,
    icon: eligibilityIcons[key as UiEligibilityState],
  }));

  return (
    <section className="py-12">
      <div className="mx-auto max-w-3xl px-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Scholarship status guide</h1>
        <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
          Quick labels tell you whether to apply now, prepare for later, or use a listing for reference. Expand any row
          for what to do next.
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

        <div className="mt-10">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Application cycle status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            At a glance — whether a scholarship is accepting applications right now.
          </p>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {lifecycleItems.map(({ id, label, shortDescription, entry, icon, badge }) => (
              <SummaryCard
                key={id}
                label={label}
                shortDescription={shortDescription}
                tone={entry.tone}
                icon={icon}
                badge={badge}
              />
            ))}
          </div>
          <div className="mt-6">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Full details
            </h3>
            <div className="mt-3">
              <StatusGuideAccordion items={lifecycleItems} />
            </div>
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Your eligibility status</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            When you&apos;re signed in, cards may also show how you fit based on your profile.
          </p>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {eligibilityItems.map(({ id, label, shortDescription, entry, icon }) => (
              <SummaryCard
                key={id}
                label={label}
                shortDescription={shortDescription}
                tone={entry.tone}
                icon={icon}
              />
            ))}
          </div>
          <div className="mt-6">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Full details
            </h3>
            <div className="mt-3">
              <StatusGuideAccordion items={eligibilityItems} />
            </div>
          </div>
        </div>

        <div className="mt-10 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/80">
          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            Closed scholarships stay visible so you can plan for the next cycle — they are not silently removed. Read{" "}
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
