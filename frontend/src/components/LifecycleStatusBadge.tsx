import { Link } from "react-router-dom";
import {
  lifecycleStatusBadgeClasses,
  lifecycleStatusLabel,
  lifecycleStatusTone,
  resolveApplicationStatus,
} from "../utils/scholarshipStatus";
import { Badge } from "@/components/ui/badge";

interface LifecycleStatusBadgeProps {
  application_status?: string | null;
  data_status?: string | null;
  is_active?: boolean | null;
  className?: string;
}

const toneToVariant = {
  success: "success",
  warning: "warning",
  neutral: "neutral",
  info: "info",
} as const;

export function LifecycleStatusBadge({
  application_status,
  data_status,
  is_active,
  className = "",
}: LifecycleStatusBadgeProps) {
  const status = resolveApplicationStatus({ application_status, data_status, is_active });
  const label = lifecycleStatusLabel(status);
  if (!label) return null;
  const tone = lifecycleStatusTone(status);
  return (
    <Badge variant={toneToVariant[tone]} className={className}>
      {label}
    </Badge>
  );
}

interface LifecycleStatusExampleProps {
  statusKey: string;
}

/** Renders a guide-accurate example badge for the status guide page. */
export function LifecycleStatusExample({ statusKey }: LifecycleStatusExampleProps) {
  return (
    <LifecycleStatusBadge application_status={statusKey} is_active={statusKey === "archived" ? false : true} />
  );
}

export function StatusGuideLink({ className = "" }: { className?: string }) {
  return (
    <Link to="/scholarship-status" className={`text-sm font-medium text-primary hover:underline ${className}`}>
      What do these labels mean?
    </Link>
  );
}

/** @deprecated Use Badge variant mapping — kept for any direct class consumers during migration */
export { lifecycleStatusBadgeClasses };
