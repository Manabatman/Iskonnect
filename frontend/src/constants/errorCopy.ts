/** Student-safe error messages — no env vars, URLs, or developer jargon (CLARITY-01). */

export type ErrorKind =
  | "offline"
  | "server_unreachable"
  | "cold_start"
  | "validation"
  | "generic"
  | "load_failed"
  | "not_found"
  | "search_no_results"
  | "session_expired";

export type ErrorCopyEntry = {
  title: string;
  message: string;
  recoveryAction: string;
};

export const ERROR_COPY: Record<ErrorKind, ErrorCopyEntry> = {
  offline: {
    title: "You're offline",
    message: "Check your internet connection, then try again.",
    recoveryAction: "Retry when you're back online",
  },
  server_unreachable: {
    title: "We couldn't reach our servers",
    message: "This is usually temporary. Wait a moment and try again.",
    recoveryAction: "Try again",
  },
  cold_start: {
    title: "Connecting to the server",
    message:
      "If this is your first visit in a while, waking the server can take up to a minute. Please wait.",
    recoveryAction: "Wait and try again",
  },
  validation: {
    title: "Something needs fixing",
    message: "Please check the highlighted fields and try again.",
    recoveryAction: "Fix and try again",
  },
  generic: {
    title: "This page hit an unexpected error",
    message: "Something interrupted loading. Go back to your dashboard or refresh the page to try again.",
    recoveryAction: "Try again",
  },
  load_failed: {
    title: "We couldn't load your data",
    message: "The server may be waking up or your connection dropped. Wait a moment, then refresh.",
    recoveryAction: "Refresh the page",
  },
  not_found: {
    title: "Page not found",
    message: "That link may be outdated or the page moved. Head home or search scholarships to keep going.",
    recoveryAction: "Back to home",
  },
  search_no_results: {
    title: "No scholarships match your filters",
    message: "Try removing the most restrictive filter first—often region, education level, or income ceiling.",
    recoveryAction: "Clear filters",
  },
  session_expired: {
    title: "Your session expired",
    message: "Sign in again to continue. We'll bring you back to the page you were on.",
    recoveryAction: "Sign in",
  },
};

export function isOffline(): boolean {
  return typeof navigator !== "undefined" && navigator.onLine === false;
}

/** Message for network / fetch failures shown to students. */
export function getNetworkErrorMessage(): string {
  if (isOffline()) return ERROR_COPY.offline.message;
  return ERROR_COPY.server_unreachable.message;
}

/** Map unknown errors to a student-safe string; logs technical detail only in dev. */
export function resolveUserErrorMessage(err: unknown, fallbackKind: ErrorKind = "generic"): string {
  if (err instanceof Error) {
    if (err.name === "NetworkError" || err.message === "Failed to fetch") {
      return getNetworkErrorMessage();
    }
    if (err.name === "TypeError" && /fetch|network/i.test(err.message)) {
      return getNetworkErrorMessage();
    }
    const msg = err.message.trim();
    if (msg && !containsDevString(msg)) return msg;
  }
  return ERROR_COPY[fallbackKind].message;
}

const DEV_STRING_PATTERN = /VITE_|API_BASE_URL|localhost:\d+|127\.0\.0\.1/i;

export function containsDevString(text: string): boolean {
  return DEV_STRING_PATTERN.test(text);
}
