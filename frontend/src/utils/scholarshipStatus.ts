/** Shared scholarship status and eligibility labels for consistent student-facing copy. */

export type ScholarshipLifecycleStatus =
  | "open"
  | "closed"
  | "previous_cycle"
  | "expected_reopen"
  | "archived"
  | "needs_review";

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
    shortDescription: "Applications are currently accepted or the window is active.",
    whatToDo: "Review requirements, gather documents, and apply through the official provider link.",
    tone: "success",
  },
  closed: {
    label: "Closed",
    shortDescription: "The application window for this cycle has ended.",
    whatToDo: "Save it for reference or watch for the next cycle if the program runs again.",
    tone: "neutral",
  },
  previous_cycle: {
    label: "Previous cycle",
    shortDescription: "This listing reflects a past application period we keep for planning.",
    whatToDo: "Use it to learn typical requirements and deadlines—not to apply right now.",
    tone: "neutral",
  },
  expected_reopen: {
    label: "Expected to reopen",
    shortDescription: "Based on past cycles, this scholarship may open again around a similar time.",
    whatToDo: "Save it, start preparing documents early, and confirm dates on the official site when it reopens.",
    tone: "info",
  },
  archived: {
    label: "Archived",
    shortDescription: "This program is no longer actively offered or has been retired from the catalog.",
    whatToDo: "Browse similar scholarships or search for updated programs from the same provider.",
    tone: "neutral",
  },
  needs_review: {
    label: "Needs verification",
    shortDescription: "We're double-checking some details before treating this listing as fully current.",
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

export function formatUiStateLabel(state: string | null | undefined): string {
  if (!state) return "";
  const key = state as UiEligibilityState;
  return UI_ELIGIBILITY_GUIDE[key]?.label ?? state.replaceAll("_", " ");
}

export function dataStatusToLifecycle(status: string | null | undefined): ScholarshipLifecycleStatus | null {
  const s = (status || "").toLowerCase();
  if (s === "expired" || s === "past_deadline") return "closed";
  if (s === "needs_review") return "needs_review";
  if (s === "broken_link") return "needs_review";
  return null;
}
