interface MatchScoreRingProps {
  score: number;
  size?: number;
  className?: string;
}

function clamp(n: number, min: number, max: number) {
  return Math.min(max, Math.max(min, n));
}

/**
 * Circular match score indicator. Purely visual — does not change API data.
 */
export function MatchScoreRing({ score, size = 56, className = "" }: MatchScoreRingProps) {
  const pct = clamp(Math.round(score), 0, 100);
  const stroke = 5;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const dash = (pct / 100) * c;

  const strokeColor =
    pct >= 70 ? "stroke-success-500" : pct >= 50 ? "stroke-highlight-500" : "stroke-slate-400";

  return (
    <div
      className={`relative inline-flex shrink-0 items-center justify-center ${className}`}
      style={{ width: size, height: size }}
      title={`${pct}% match`}
    >
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          className="stroke-slate-200 dark:stroke-slate-600"
          strokeWidth={stroke}
        />
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
      <span className="absolute inset-0 flex flex-col items-center justify-center text-center text-[11px] font-bold leading-none text-slate-900 dark:text-slate-100">
        <span>{pct}</span>
        <span className="mt-0.5 text-[9px] font-semibold text-slate-500 dark:text-slate-400">%</span>
      </span>
    </div>
  );
}
