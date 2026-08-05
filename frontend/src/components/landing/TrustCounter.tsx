import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "framer-motion";
import { MOTION_DURATION_MS } from "@/lib/motion";

interface TrustCounterProps {
  value: number | null | undefined;
  label: string;
  suffix?: string;
  tone?: "default" | "onDark";
}

function formatValue(n: number, suffix?: string) {
  return `${n.toLocaleString()}${suffix ?? ""}`;
}

export function TrustCounter({ value, label, suffix, tone = "default" }: TrustCounterProps) {
  const prefersReduced = useReducedMotion();
  const [display, setDisplay] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (value == null || value <= 0) {
      setDisplay(null);
      return;
    }
    if (prefersReduced) {
      setDisplay(value);
      return;
    }
    const el = ref.current;
    if (!el) {
      setDisplay(value);
      return;
    }
    let frame = 0;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return;
        obs.disconnect();
        const start = performance.now();
        const duration = MOTION_DURATION_MS.reveal;
        const tick = (now: number) => {
          const t = Math.min(1, (now - start) / duration);
          setDisplay(Math.round(value * t));
          if (t < 1) frame = requestAnimationFrame(tick);
        };
        frame = requestAnimationFrame(tick);
      },
      { threshold: 0.2 }
    );
    obs.observe(el);
    return () => {
      obs.disconnect();
      cancelAnimationFrame(frame);
    };
  }, [value, prefersReduced]);

  if (display == null) return null;

  const valueClass =
    tone === "onDark" ? "text-white" : "text-slate-900 dark:text-white";
  const labelClass =
    tone === "onDark" ? "text-slate-300" : "text-slate-600 dark:text-slate-400";

  return (
    <div ref={ref} className="text-center">
      <p className={`text-2xl font-bold tabular-nums sm:text-3xl ${valueClass}`}>
        {formatValue(display, suffix)}
      </p>
      <p className={`mt-1 text-xs font-medium sm:text-sm ${labelClass}`}>{label}</p>
    </div>
  );
}
