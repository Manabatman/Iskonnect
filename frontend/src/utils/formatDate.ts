/** Asia/Manila for all user-visible dates/times (Philippines). */
const PH_TIMEZONE = "Asia/Manila";

const dateMediumOpts: Intl.DateTimeFormatOptions = {
  timeZone: PH_TIMEZONE,
  dateStyle: "medium",
};

const dateTimeOpts: Intl.DateTimeFormatOptions = {
  timeZone: PH_TIMEZONE,
  dateStyle: "short",
  timeStyle: "short",
};

const dateTimeLongOpts: Intl.DateTimeFormatOptions = {
  timeZone: PH_TIMEZONE,
  dateStyle: "medium",
  timeStyle: "short",
};


/** Medium date in Manila (e.g. Apr 4, 2026). */
export function formatDateMedium(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString("en-PH", dateMediumOpts);
  } catch {
    return String(iso);
  }
}

/** Date + time in Manila. */
export function formatDateTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString("en-PH", dateTimeOpts);
  } catch {
    return String(iso);
  }
}

/** Date + time with medium date style. */
export function formatDateTimeLong(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString("en-PH", dateTimeLongOpts);
  } catch {
    return String(iso);
  }
}

/** Start of "today" in Manila (for comparing calendar dates from API date strings). */
export function startOfTodayManila(): Date {
  const now = new Date();
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: PH_TIMEZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const y = parts.find((p) => p.type === "year")?.value;
  const m = parts.find((p) => p.type === "month")?.value;
  const d = parts.find((p) => p.type === "day")?.value;
  if (!y || !m || !d) return new Date(now.getFullYear(), now.getMonth(), now.getDate());
  return new Date(Number(y), Number(m) - 1, Number(d));
}


/** Short month + day + year in Manila (e.g. Apr 4, 2026). */
export function formatDateShort(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString("en-PH", {
      timeZone: PH_TIMEZONE,
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return String(iso);
  }
}

/** Month and year only in Manila. */
export function formatMonthYear(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString("en-PH", {
      timeZone: PH_TIMEZONE,
      month: "long",
      year: "numeric",
    });
  } catch {
    return String(iso);
  }
}

/** Relative time for recent activity (Manila wall-clock friendly). */
export function formatRelativeManila(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    const then = new Date(iso).getTime();
    const now = Date.now();
    const sec = Math.max(0, Math.round((now - then) / 1000));
    if (sec < 45) return "Just now";
    const min = Math.floor(sec / 60);
    if (min < 60) return `${min} min ago`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr} hr ago`;
    const day = Math.floor(hr / 24);
    if (day === 1) return "Yesterday";
    if (day < 7) return `${day} days ago`;
    return formatDateTime(iso);
  } catch {
    return String(iso);
  }
}
