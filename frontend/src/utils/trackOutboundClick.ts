import { API_BASE_URL } from "../api/client";

export type ReferralSurface = "card" | "detail_page" | "detail_panel" | "trust_source";
export type ReferralLinkKind = "apply_official" | "check_official" | "view_source";

const ALLOWED_SURFACES = new Set<string>(["card", "detail_page", "detail_panel", "trust_source"]);
const ALLOWED_LINK_KINDS = new Set<string>(["apply_official", "check_official", "view_source"]);

/** Fire-and-forget aggregate referral click — no PII, never blocks navigation (C9). */
export function trackOutboundClick(payload: {
  scholarshipId: number;
  surface: ReferralSurface;
  linkKind: ReferralLinkKind;
}): void {
  if (!Number.isFinite(payload.scholarshipId) || payload.scholarshipId <= 0) return;
  if (!ALLOWED_SURFACES.has(payload.surface) || !ALLOWED_LINK_KINDS.has(payload.linkKind)) return;

  const body = JSON.stringify({
    scholarship_id: payload.scholarshipId,
    surface: payload.surface,
    link_kind: payload.linkKind,
  });

  const url = `${API_BASE_URL}/api/v1/analytics/referral-clicks`;
  if (typeof navigator !== "undefined" && typeof navigator.sendBeacon === "function") {
    const blob = new Blob([body], { type: "application/json" });
    if (navigator.sendBeacon(url, blob)) return;
  }

  void fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
    keepalive: true,
  }).catch(() => {
    /* tracking must not affect navigation */
  });
}
