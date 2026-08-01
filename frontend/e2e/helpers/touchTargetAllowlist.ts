import type { TouchTargetViolation } from "./touchTargets";

export type TouchTargetAllowlistEntry = {
  route: string;
  text?: string;
  selector?: string;
  comment: string;
};

export type TouchTargetAllowlist = {
  description: string;
  entries: TouchTargetAllowlistEntry[];
};

export function isAllowlisted(
  violation: TouchTargetViolation,
  entry: TouchTargetAllowlistEntry,
): boolean {
  if (violation.route !== entry.route) return false;
  if (entry.selector && violation.selector !== entry.selector) return false;
  if (entry.text && !violation.text.includes(entry.text)) return false;
  return true;
}

export function filterBlockingViolations(
  violations: TouchTargetViolation[],
  allowlist: TouchTargetAllowlist,
): TouchTargetViolation[] {
  return violations.filter(
    (violation) => !allowlist.entries.some((entry) => isAllowlisted(violation, entry)),
  );
}
