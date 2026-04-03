export function providerInitials(provider: string | null | undefined): string {
  const clean = (provider ?? "").replace(/[^a-zA-Z0-9]/g, "").slice(0, 2);
  return clean.length ? clean.toUpperCase() : "?";
}

export function statusToFactorPercent(status: string | undefined): number {
  const s = (status ?? "").toLowerCase();
  if (s === "met" || s === "exceeded" || s === "ready") return 100;
  if (s === "partial") return 50;
  return 0;
}

export function getUrgencyLevel(
  deadline: string | null | undefined,
  openDate?: string | null
): { level: string; label: string } {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (openDate) {
    try {
      const open = new Date(openDate);
      open.setHours(0, 0, 0, 0);
      const daysUntilOpen = Math.ceil((open.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
      if (daysUntilOpen > 0) {
        if (daysUntilOpen <= 7) return { level: "upcoming", label: `Opens in ${daysUntilOpen}d` };
        return { level: "upcoming", label: "Opens soon" };
      }
    } catch {
      /* ignore */
    }
  }

  if (!deadline) return { level: "unknown", label: "No deadline" };
  try {
    const d = new Date(deadline);
    d.setHours(0, 0, 0, 0);
    const diffMs = d.getTime() - today.getTime();
    const daysLeft = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    if (daysLeft < 0) return { level: "closed", label: "Closed" };
    if (daysLeft <= 3) return { level: "critical", label: `Closes in ${daysLeft}d` };
    if (daysLeft <= 7) return { level: "urgent", label: `Closes in ${daysLeft}d` };
    if (daysLeft <= 30) return { level: "soon", label: "Closing Soon" };
    return { level: "open", label: "Open" };
  } catch {
    return { level: "unknown", label: "No deadline" };
  }
}

export function getUrgencyBadgeClasses(level: string): string {
  switch (level) {
    case "critical":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
    case "urgent":
      return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300";
    case "soon":
      return "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300";
    case "open":
      return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
    case "closed":
      return "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-400";
    case "upcoming":
      return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300";
    default:
      return "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400";
  }
}

export function MatchStatusIcon({ status }: { status: string }) {
  switch (status) {
    case "met":
    case "exceeded":
    case "ready":
      return (
        <span className="text-green-600" aria-label="Met">
          ✓
        </span>
      );
    case "partial":
      return (
        <span className="text-amber-600" aria-label="Partial">
          ◐
        </span>
      );
    case "missing":
    case "disqualified":
      return (
        <span className="text-red-600" aria-label="Missing">
          ✗
        </span>
      );
    default:
      return <span className="text-slate-400">—</span>;
  }
}

