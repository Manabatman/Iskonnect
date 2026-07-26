import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { MatchResult, OpportunityTimeline } from "../types";
import { formatDateShort, formatMonthYear } from "../utils/formatDate";
import { formatDeadlineDisplay, formatOpenDateDisplay } from "../utils/formatDeadline";

type CalendarEventKind = "open" | "deadline" | "predicted";

interface CalendarEvent {
  id: number;
  title: string;
  date: string;
  kind: CalendarEventKind;
  match: MatchResult;
}

function eventDateForMatch(match: MatchResult): { date: string; kind: CalendarEventKind } | null {
  if (match.application_open_date?.trim()) {
    return { date: match.application_open_date.slice(0, 10), kind: "open" };
  }
  if (match.predicted_open?.trim()) {
    return { date: match.predicted_open.slice(0, 10), kind: "predicted" };
  }
  if (match.application_deadline?.trim()) {
    return { date: match.application_deadline.slice(0, 10), kind: "deadline" };
  }
  return null;
}

function collectEvents(timeline: OpportunityTimeline): CalendarEvent[] {
  const events: CalendarEvent[] = [];
  const seen = new Set<string>();

  for (const lane of Object.values(timeline.lanes)) {
    for (const match of lane) {
      const parsed = eventDateForMatch(match);
      if (!parsed) continue;
      const key = `${match.id}-${parsed.date}-${parsed.kind}`;
      if (seen.has(key)) continue;
      seen.add(key);
      events.push({
        id: match.id,
        title: match.title,
        date: parsed.date,
        kind: parsed.kind,
        match,
      });
    }
  }

  events.sort((a, b) => a.date.localeCompare(b.date));
  return events;
}

const KIND_LABELS: Record<CalendarEventKind, string> = {
  open: "Opens",
  deadline: "Deadline",
  predicted: "Predicted open",
};

const KIND_STYLES: Record<CalendarEventKind, string> = {
  open: "border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-100",
  deadline: "border-rose-200 bg-rose-50 text-rose-900 dark:border-rose-800 dark:bg-rose-950/40 dark:text-rose-100",
  predicted: "border-amber-200 bg-amber-50 text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100",
};

export interface OpportunityCalendarViewProps {
  timeline: OpportunityTimeline;
  className?: string;
}

export function OpportunityCalendarView({ timeline, className = "" }: OpportunityCalendarViewProps) {
  const events = useMemo(() => collectEvents(timeline), [timeline]);
  const months = useMemo(() => {
    const map = new Map<string, CalendarEvent[]>();
    for (const ev of events) {
      const monthKey = ev.date.slice(0, 7);
      const list = map.get(monthKey) ?? [];
      list.push(ev);
      map.set(monthKey, list);
    }
    return Array.from(map.entries()).sort(([a], [b]) => a.localeCompare(b));
  }, [events]);

  const [expandedMonth, setExpandedMonth] = useState<string | null>(months[0]?.[0] ?? null);

  if (events.length === 0) {
    return (
      <div
        className={`rounded-xl border border-dashed border-slate-300 bg-slate-50/50 p-8 text-center text-sm text-slate-500 dark:border-slate-600 dark:bg-slate-900/30 dark:text-slate-400 ${className}`}
      >
        No dated opportunities to plot yet. Add profile details or check back when programs publish schedules.
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      <div>
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Calendar view</h3>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Month-by-month view of open dates, deadlines, and predicted reopenings from your plan.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {months.map(([monthKey]) => (
          <button
            key={monthKey}
            type="button"
            onClick={() => setExpandedMonth(monthKey)}
            className={[
              "rounded-full px-3 py-1.5 text-sm font-medium transition",
              expandedMonth === monthKey
                ? "bg-primary-600 text-white"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600",
            ].join(" ")}
          >
            {formatMonthYear(`${monthKey}-01`)}
          </button>
        ))}
      </div>

      {months.map(([monthKey, monthEvents]) => {
        if (expandedMonth && expandedMonth !== monthKey) return null;
        return (
          <section
            key={monthKey}
            className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800"
            aria-label={formatMonthYear(`${monthKey}-01`)}
          >
            <h4 className="text-base font-semibold text-slate-900 dark:text-slate-100">
              {formatMonthYear(`${monthKey}-01`)}
              <span className="ml-2 text-sm font-normal text-slate-500 dark:text-slate-400">
                {monthEvents.length} event{monthEvents.length === 1 ? "" : "s"}
              </span>
            </h4>
            <ul className="mt-3 space-y-2">
              {monthEvents.map((ev) => (
                <li
                  key={`${ev.id}-${ev.date}-${ev.kind}`}
                  className={`flex flex-col gap-1 rounded-lg border px-3 py-2 sm:flex-row sm:items-center sm:justify-between ${KIND_STYLES[ev.kind]}`}
                >
                  <div className="min-w-0">
                    <p className="font-medium">{ev.title}</p>
                    <p className="text-xs opacity-90">
                      {ev.kind === "deadline"
                        ? formatDeadlineDisplay(
                            ev.match.application_deadline,
                            ev.match.deadline_precision,
                            ev.match.deadline_note,
                            ev.match.last_verified_at
                          )
                        : ev.kind === "open"
                          ? formatOpenDateDisplay(
                              ev.match.application_open_date,
                              ev.match.deadline_precision,
                              ev.match.deadline_note
                            )
                          : `${KIND_LABELS[ev.kind]} · ${formatDateShort(ev.date)} (estimate)`}
                    </p>
                  </div>
                  <Link
                    to={`/scholarship/${ev.id}`}
                    className="shrink-0 text-xs font-semibold underline-offset-2 hover:underline"
                  >
                    Details
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}
