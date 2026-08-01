/** Shared scholarship status and eligibility labels — single source of truth for student-facing copy. */

export type ScholarshipLifecycleStatus =
  | "open"
  | "closed"
  | "previous_cycle"
  | "expected_reopen"
  | "archived"
  | "needs_verification";

export type UiEligibilityState = "eligible_now" | "opening_soon" | "prepare_ahead" | "future_eligibility";

export interface StatusGuideEntry {
  label: string;
  shortDescription: string;
  whatToDo: string;
  tone: "success" | "warning" | "neutral" | "info";
}

export const LIFECYCLE_STATUS_GUIDE: Record<ScholarshipLifecycleStatus, StatusGuideEntry> = {
  open: {
    label: "Open now",
    shortDescription:
      "Applications are currently being accepted according to the latest official information available.",
    whatToDo: "Review requirements, gather documents, and apply through the official provider link.",
    tone: "success",
  },
  closed: {
    label: "Closed",
    shortDescription:
      "The application window for this cycle has ended. The program may still run again in a future cycle.",
    whatToDo: "Save it for reference or watch for the next cycle if the program runs again.",
    tone: "neutral",
  },
  previous_cycle: {
    label: "Past cycle",
    shortDescription:
      "This listing reflects a past application period we keep so you can plan for the next opening.",
    whatToDo: "Use it to learn typical requirements and deadlines—not to apply right now.",
    tone: "neutral",
  },
  expected_reopen: {
    label: "Expected to reopen",
    shortDescription:
      "Based on past cycles, this scholarship is likely to open again around a similar time of year.",
    whatToDo: "Save it, start preparing documents early, and confirm dates on the official site when it reopens.",
    tone: "info",
  },
  archived: {
    label: "No longer offered",
    shortDescription:
      "This program is no longer actively offered or has been retired from our active catalog.",
    whatToDo: "Browse similar scholarships or search for updated programs from the same provider.",
    tone: "neutral",
  },
  needs_verification: {
    label: "Needs verification",
    shortDescription:
      "We are still confirming some details against official sources before treating this listing as fully current.",
    whatToDo: "Use it as a lead, but confirm all requirements and deadlines on the official provider website.",
    tone: "warning",
  },
};

export const UI_ELIGIBILITY_GUIDE: Record<UiEligibilityState, StatusGuideEntry> = {
  eligible_now: {
    label: "Eligible now",
    shortDescription: "You appear to meet the main requirements and applications may be open.",
    whatToDo: "Review the official link and apply if the deadline hasn't passed.",
    tone: "success",
  },
  opening_soon: {
    label: "Opening soon",
    shortDescription: "You may qualify, and the application window is expected to open shortly.",
    whatToDo: "Save this scholarship and prepare your documents before applications open.",
    tone: "info",
  },
  prepare_ahead: {
    label: "Prepare ahead",
    shortDescription: "You're on track to apply, but you may need more documents or profile details.",
    whatToDo: "Work through the document checklist and complete missing profile fields.",
    tone: "warning",
  },
  future_eligibility: {
    label: "Future eligibility",
    shortDescription: "You might qualify later—for example when you reach the required grade or GWA.",
    whatToDo: "Keep it on your radar and revisit when your situation changes.",
    tone: "info",
  },
};

const LIFECYCLE_TONE_CLASSES: Record<StatusGuideEntry["tone"], string> = {
  success: "border-tone-success bg-tone-success text-tone-success",
  warning: "border-tone-warning bg-tone-warning text-tone-warning",
  neutral: "border-tone-neutral bg-tone-neutral text-tone-neutral",
  info: "border-tone-info bg-tone-info text-tone-info",
};

/** Map legacy data_status values to canonical application_status keys. */
export function legacyDataStatusToApplicationStatus(status: string | null | undefined): ScholarshipLifecycleStatus | null {
  const s = (status || "").toLowerCase();
  if (s === "needs_review") return "needs_verification";
  if (s === "broken_link") return null;
  if (s === "expired" || s === "past_deadline") return "closed";
  if (s === "active") return "open";
  return null;
}

export function resolveApplicationStatus(sch: {
  application_status?: string | null;
  data_status?: string | null;
  is_active?: boolean | null;
}): ScholarshipLifecycleStatus {
  if (sch.is_active === false) return "archived";
  const app = (sch.application_status || "").toLowerCase();
  if (app && app in LIFECYCLE_STATUS_GUIDE) return app as ScholarshipLifecycleStatus;
  const legacy = legacyDataStatusToApplicationStatus(sch.data_status);
  if (legacy) return legacy;
  return "needs_verification";
}

export function lifecycleStatusLabel(status: string | null | undefined): string {
  if (!status) return "";
  const key = status as ScholarshipLifecycleStatus;
  return LIFECYCLE_STATUS_GUIDE[key]?.label ?? status.replaceAll("_", " ");
}

export function lifecycleStatusTone(status: string | null | undefined): StatusGuideEntry["tone"] {
  const key = (status || "") as ScholarshipLifecycleStatus;
  return LIFECYCLE_STATUS_GUIDE[key]?.tone ?? "neutral";
}

export function lifecycleStatusBadgeClasses(status: string | null | undefined): string {
  const tone = lifecycleStatusTone(status);
  return LIFECYCLE_TONE_CLASSES[tone];
}

const ELIGIBILITY_STATE_TO_UI: Record<string, UiEligibilityState> = {
  eligible_now: "eligible_now",
  eligible_soon: "opening_soon",
  prepare_now: "prepare_ahead",
  missing_one_requirement: "prepare_ahead",
  expected_next_cycle: "opening_soon",
  past_opportunity: "opening_soon",
  potential_match: "prepare_ahead",
  requires_future_grade_level: "future_eligibility",
  requires_future_enrollment: "future_eligibility",
  requires_better_academic_standing: "future_eligibility",
  not_eligible: "future_eligibility",
};

export function formatUiStateLabel(state: string | null | undefined): string {
  if (!state) return "";
  const key = state as UiEligibilityState;
  if (UI_ELIGIBILITY_GUIDE[key]) return UI_ELIGIBILITY_GUIDE[key].label;
  const mapped = ELIGIBILITY_STATE_TO_UI[state];
  if (mapped) return UI_ELIGIBILITY_GUIDE[mapped].label;
  return state.replaceAll("_", " ");
}

export function humanizeVerificationSource(source: string | null | undefined): string | null {
  if (!source?.trim()) return null;
  const mapping: Record<string, string> = {
    manual: "Verified by ISKONNECT team",
    scraper: "Verified by ISKONNECT team",
    team_verified: "Verified by ISKONNECT team",
    partner: "Partner organization",
    csv_import: "Imported record",
  };
  const key = source.trim().toLowerCase();
  return mapping[key] ?? source.replaceAll("_", " ");
}

/** Deep-link anchor for the scholarship status guide (CONT-01). */
export function statusGuideHref(statusKey: string): string {
  return `/scholarship-status#${encodeURIComponent(statusKey)}`;
}
