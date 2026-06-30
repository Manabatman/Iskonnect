import { Link } from "react-router-dom";
import {
  lifecycleStatusBadgeClasses,
  lifecycleStatusLabel,
  resolveApplicationStatus,
} from "../utils/scholarshipStatus";

interface LifecycleStatusBadgeProps {
  application_status?: string | null;
  data_status?: string | null;
  is_active?: boolean | null;
  className?: string;
}

export function LifecycleStatusBadge({
  application_status,
  data_status,
  is_active,
  className = "",
}: LifecycleStatusBadgeProps) {
  const status = resolveApplicationStatus({ application_status, data_status, is_active });
  const label = lifecycleStatusLabel(status);
  if (!label) return null;
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold shadow-sm ${lifecycleStatusBadgeClasses(status)} ${className}`}
    >
      {label}
    </span>
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
    <Link
      to="/scholarship-status"
      className={`text-sm font-medium text-primary-600 hover:underline dark:text-primary-400 ${className}`}
    >
      What do these labels mean?
    </Link>
  );
}
