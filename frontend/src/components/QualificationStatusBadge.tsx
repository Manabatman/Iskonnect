import type { QualificationStatus } from "../types";
import { Badge } from "@/components/ui/badge";

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
    <Badge variant={cfg.variant} className={className}>
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
