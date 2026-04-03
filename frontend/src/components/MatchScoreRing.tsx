interface MatchScoreRingProps {
  score: number;
  size?: number;
  className?: string;
  /** When true, uses high-contrast styling for dark/gradient backgrounds + “Match Score” label. */
  variant?: "default" | "onDark";
  /** When variant is onDark, shows “Match Score” under the percentage. */
  showMatchLabel?: boolean;
}

function clamp(n: number, min: number, max: number) {
  return Math.min(max, Math.max(min, n));
}

/**
 * Circular match score indicator. Purely visual — does not change API data.
 * Green 80–100, orange 50–79, gray below 50.
 */
export function MatchScoreRing({
  score,
  size = 56,
  className = "",
  variant = "default",
  showMatchLabel = false,
}: MatchScoreRingProps) {
  const pct = clamp(Math.round(score), 0, 100);
  const stroke = size >= 80 ? 6 : 5;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const dash = (pct / 100) * c;

  const strokeColor =
    pct >= 80 ? "stroke-success-500" : pct >= 50 ? "stroke-accent-500" : "stroke-slate-400";

  const onDark = variant === "onDark";
  const trackClass = onDark ? "stroke-white/30" : "stroke-slate-200 dark:stroke-slate-600";
  const labelClass = onDark
    ? "text-white drop-shadow-sm"
    : "text-slate-900 dark:text-slate-100";
  const subLabelClass = onDark ? "text-white/90" : "text-slate-500 dark:text-slate-400";

  const textSize = size >= 100 ? "text-base" : size >= 72 ? "text-sm" : "text-[11px]";
  const pctSize = size >= 100 ? "text-2xl" : size >= 72 ? "text-lg" : "";

  const ringBlock = (
    <div className="relative inline-flex shrink-0 items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" className={trackClass} strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          className={strokeColor}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${dash} ${c}`}
        />
      </svg>
      <span
        className={`absolute inset-0 flex flex-col items-center justify-center text-center font-bold leading-none ${labelClass} ${textSize}`}
      >
        <span className={pctSize}>{pct}</span>
        <span className={`mt-0.5 text-[9px] font-semibold ${subLabelClass}`}>%</span>
      </span>
    </div>
  );

  if (onDark && showMatchLabel) {
    return (
      <div
        className={`relative inline-flex shrink-0 flex-col items-center justify-center ${className}`}
        style={{ width: size, height: size + 18 }}
        title={`${pct}% match`}
      >
        {ringBlock}
        <span className="mt-1 text-center text-[9px] font-bold uppercase tracking-wide text-white drop-shadow">
          Match Score
        </span>
      </div>
    );
  }

  return (
    <div
      className={`relative inline-flex shrink-0 items-center justify-center ${className}`}
      style={{ width: size, height: size }}
      title={`${pct}% match`}
    >
      {ringBlock}
    </div>
  );
}
