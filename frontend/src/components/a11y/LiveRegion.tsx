interface LiveRegionProps {
  /** Text announced to screen readers when it changes. */
  message: string;
  politeness?: "polite" | "assertive";
}

/**
 * Visually hidden live region for dynamic status updates (A11Y-10).
 */
export function LiveRegion({ message, politeness = "polite" }: LiveRegionProps) {
  return (
    <div aria-live={politeness} aria-atomic="true" className="sr-only">
      {message}
    </div>
  );
}
