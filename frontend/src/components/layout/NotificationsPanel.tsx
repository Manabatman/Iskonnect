import { useCallback, useEffect, useRef, type MouseEvent as ReactMouseEvent } from "react";
import { useNavigate } from "react-router-dom";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

export type NotificationItem = {
  id: number;
  type: string;
  title: string;
  body?: string | null;
  scholarship_id?: number | null;
  is_read: boolean;
  created_at: string;
};

interface NotificationsPanelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  items: NotificationItem[];
  loading: boolean;
  onMarkRead: (id: number) => void;
  onMarkAllRead: () => void;
  onClearAll: () => void;
  onDelete: (id: number, e: ReactMouseEvent) => void;
  formatTime: (iso: string) => string;
  /** Desktop dropdown anchor; omit on mobile sheet-only usage. */
  dropdownClassName?: string;
  useSheet: boolean;
}

function NotificationRows({
  items,
  loading,
  onMarkRead,
  onDelete,
  formatTime,
  onNavigate,
}: {
  items: NotificationItem[];
  loading: boolean;
  onMarkRead: (id: number) => void;
  onDelete: (id: number, e: ReactMouseEvent) => void;
  formatTime: (iso: string) => string;
  onNavigate: () => void;
}) {
  const navigate = useNavigate();

  if (loading) {
    return <p className="px-3 py-4 text-sm text-slate-500">Loading…</p>;
  }
  if (items.length === 0) {
    return <p className="px-3 py-4 text-sm text-slate-500 dark:text-slate-400">No notifications yet.</p>;
  }

  return (
    <ul className="list-none p-0 m-0">
      {items.map((n) => (
        <li
          key={n.id}
          className={`flex items-start gap-2 border-b border-slate-50 dark:border-slate-700 ${
            !n.is_read ? "bg-primary-50/50 dark:bg-primary-950/20" : ""
          }`}
        >
          <button
            type="button"
            className="min-h-11 min-w-0 flex-1 px-3 py-3 text-left text-sm text-slate-800 transition hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-700/80"
            onClick={() => {
              if (!n.is_read) onMarkRead(n.id);
              if (n.scholarship_id) {
                navigate(`/scholarship/${n.scholarship_id}`);
                onNavigate();
              }
            }}
          >
            <p className="font-medium">{n.title}</p>
            {n.body ? <p className="mt-0.5 text-xs text-slate-600 dark:text-slate-400">{n.body}</p> : null}
            <p className="mt-1 text-caption text-slate-400">{formatTime(n.created_at)}</p>
          </button>
          <button
            type="button"
            onClick={(e) => onDelete(n.id, e)}
            className="focus-visible-ring flex min-h-11 min-w-11 shrink-0 items-center justify-center text-lg text-slate-400 hover:text-red-600 dark:hover:text-red-400"
            aria-label="Delete notification"
          >
            ×
          </button>
        </li>
      ))}
    </ul>
  );
}

function PanelHeader({
  items,
  onMarkAllRead,
  onClearAll,
}: {
  items: NotificationItem[];
  onMarkAllRead: () => void;
  onClearAll: () => void;
}) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 px-3 py-2 dark:border-slate-700">
      <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">Notifications</p>
      {items.length > 0 ? (
        <div className="flex gap-2">
          <button
            type="button"
            onClick={onMarkAllRead}
            className="text-xs font-medium text-primary-600 hover:underline dark:text-primary-400"
          >
            Mark all read
          </button>
          <button
            type="button"
            onClick={onClearAll}
            className="text-xs font-medium text-red-600 hover:underline dark:text-red-400"
          >
            Clear all
          </button>
        </div>
      ) : null}
    </div>
  );
}

/** D-07 — scrollable notifications with mobile bottom sheet. */
export function NotificationsPanel({
  open,
  onOpenChange,
  items,
  loading,
  onMarkRead,
  onMarkAllRead,
  onClearAll,
  onDelete,
  formatTime,
  dropdownClassName = "",
  useSheet,
}: NotificationsPanelProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const close = useCallback(() => onOpenChange(false), [onOpenChange]);

  useEffect(() => {
    if (!open || useSheet) return;
    const panel = panelRef.current;
    if (!panel) return;
    const focusable = panel.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusable[0]?.focus();

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      if (e.key !== "Tab" || focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open, useSheet, close]);

  const list = (
    <div className="max-h-[min(24rem,calc(100dvh-5rem))] overflow-y-auto overscroll-contain">
      <NotificationRows
        items={items}
        loading={loading}
        onMarkRead={onMarkRead}
        onDelete={onDelete}
        formatTime={formatTime}
        onNavigate={close}
      />
    </div>
  );

  if (useSheet) {
    return (
      <Sheet open={open} onOpenChange={onOpenChange}>
        <SheetContent side="bottom" className="max-h-[85dvh] rounded-t-2xl p-0">
          <SheetHeader className="sr-only">
            <SheetTitle>Notifications</SheetTitle>
            <SheetDescription>Your deadline reminders and updates</SheetDescription>
          </SheetHeader>
          <PanelHeader items={items} onMarkAllRead={onMarkAllRead} onClearAll={onClearAll} />
          {list}
        </SheetContent>
      </Sheet>
    );
  }

  if (!open) return null;

  return (
    <div
      ref={panelRef}
      role="dialog"
      aria-label="Notifications"
      className={`absolute right-0 z-40 mt-1 w-80 max-w-[calc(100vw-2rem)] overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg dark:border-slate-600 dark:bg-slate-800 ${dropdownClassName}`}
    >
      <PanelHeader items={items} onMarkAllRead={onMarkAllRead} onClearAll={onClearAll} />
      {list}
    </div>
  );
}
