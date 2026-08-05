import { useEffect, useState, type ReactNode } from "react";
import { MOTION_DURATION_MS } from "@/lib/motion";

const STAGGER_MS = MOTION_DURATION_MS.fast;

interface StaggeredRevealGridProps {
  count: number;
  active: boolean;
  children: (index: number, visible: boolean) => ReactNode;
  className?: string;
}

/** Progressive card reveal after match load (Wave 5 / M6). */
export function StaggeredRevealGrid({ count, active, children, className = "" }: StaggeredRevealGridProps) {
  const [revealed, setRevealed] = useState(0);
  const prefersReduced =
    typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  useEffect(() => {
    if (!active || count === 0) {
      setRevealed(0);
      return;
    }
    if (prefersReduced) {
      setRevealed(count);
      return;
    }
    setRevealed(0);
    let i = 0;
    const id = window.setInterval(() => {
      i += 1;
      setRevealed(i);
      if (i >= count) window.clearInterval(id);
    }, STAGGER_MS);
    return () => window.clearInterval(id);
  }, [active, count, prefersReduced]);

  return (
    <div className={className}>
      {Array.from({ length: count }, (_, index) => children(index, index < revealed))}
    </div>
  );
}

export function MatchResultsSkeleton() {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-6xl px-4">
        <p className="mb-4 text-sm text-slate-600 dark:text-slate-400" role="status">
          Finding scholarships that match your profile…
        </p>
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-64 rounded-lg bg-slate-200 dark:bg-slate-700" />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-52 rounded-xl border border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-800">
                <div className="h-28 rounded-t-xl bg-slate-100 dark:bg-slate-700" />
                <div className="space-y-2 p-4">
                  <div className="h-4 w-3/4 rounded bg-slate-100 dark:bg-slate-700" />
                  <div className="h-3 w-1/2 rounded bg-slate-100 dark:bg-slate-700" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
