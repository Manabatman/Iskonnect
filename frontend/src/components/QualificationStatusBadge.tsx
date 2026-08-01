import type { QualificationStatus } from "../types";
import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";
import { MATCH_CONFIDENCE_COMPACT } from "./MatchConfidenceNote";

const REQUIREMENT_PROFILE_LINKS: Record<string, string> = {
  age: "/profile-builder?step=personal",
  education_level: "/profile-builder?step=education",
  region: "/profile-builder?step=location",
  school_type: "/profile-builder?step=education",
  school: "/profile-builder?step=education",
  school_category: "/profile-builder?step=education",
  year_level: "/profile-builder?step=education",
  enrollment_status: "/profile-builder?step=education",
  citizenship: "/profile-builder?step=personal",
  income: "/profile-builder?step=location",
  gwa: "/profile-builder?step=education",
  field: "/profile-builder?step=field",
  members_only: "/profile-builder?step=equity",
};

const STATUS_VARIANT: Record<
  QualificationStatus,
  { label: string; variant: "success" | "warning" | "info" | "neutral" }
> = {
  qualified: { label: "Qualified", variant: "success" },
  provisionally_qualified: { label: "Provisionally qualified", variant: "warning" },
  almost_qualified: { label: "Almost qualified", variant: "info" },
  not_eligible: { label: "Not eligible", variant: "neutral" },
};

export function QualificationStatusBadge({
  status,
  className = "",
}: {
  status?: QualificationStatus | string | null;
  className?: string;
}) {
  if (!status) return null;
  const key = status as QualificationStatus;
  const cfg = STATUS_VARIANT[key];
  if (!cfg) return null;
  return (
    <Badge variant={cfg.variant} className={className} title={MATCH_CONFIDENCE_COMPACT}>
      {cfg.label}
    </Badge>
  );
}

export function VerificationBadge({
  badge,
  label,
}: {
  badge?: string | null;
  label?: string | null;
}) {
  if (!badge && !label) return null;
  const variant =
    badge === "verified"
      ? "success"
      : badge === "partially_verified"
        ? "warning"
        : "neutral";
  return <Badge variant={variant}>{label ?? badge}</Badge>;
}

export function EligibilityRequirementsList({
  qualifying,
  missing,
  compact = false,
}: {
  qualifying?: string[];
  missing?: string[];
  compact?: boolean;
}) {
  const q = qualifying ?? [];
  const m = missing ?? [];
  if (!q.length && !m.length) return null;
  const limit = compact ? 3 : 6;
  return (
    <div className="mt-2 space-y-1 text-xs text-muted-foreground">
      {q.slice(0, limit).map((item) => (
        <div key={`q-${item}`} className="text-tone-success">
          ✓ {item}
        </div>
      ))}
      {m.slice(0, limit).map((item) => (
        <div key={`m-${item}`} className="text-tone-warning">
          ✗ {item}
        </div>
      ))}
    </div>
  );
}

export function UnverifiedRequirementsList({
  unverified,
  requirements,
  provisionalReason,
  compact = false,
}: {
  unverified?: string[];
  requirements?: Array<{ key?: string; result?: string; label?: string }>;
  provisionalReason?: string | null;
  compact?: boolean;
}) {
  const labels = unverified ?? [];
  if (!labels.length && !provisionalReason) return null;

  const unknownReqs = (requirements ?? []).filter((r) => r.result === "unknown");

  return (
    <div
      className={`rounded-lg border border-tone-warning bg-tone-warning px-3 py-2 ${
        compact ? "mt-2 text-xs" : "mt-3 text-sm"
      }`}
      role="note"
    >
      <p className="font-semibold text-tone-warning">
        {provisionalReason ?? "We could not verify some requirements"}
      </p>
      {labels.length > 0 ? (
        <ul className="mt-1.5 space-y-1 text-tone-warning">
          {labels.map((label) => {
            const req = unknownReqs.find(
              (r) => r.label?.toLowerCase().includes(label.replace(/^your /, "")) || r.key
            );
            const link = req?.key ? REQUIREMENT_PROFILE_LINKS[req.key] : undefined;
            return (
              <li key={label}>
                {link ? (
                  <Link to={link} className="font-medium underline underline-offset-2 hover:opacity-90">
                    Add {label}
                  </Link>
                ) : (
                  <span>Add {label} in your profile</span>
                )}
              </li>
            );
          })}
        </ul>
      ) : null}
    </div>
  );
}
