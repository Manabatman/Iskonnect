/**
 * First focusable element in each layout shell — lets keyboard users bypass nav (A11Y-01).
 */
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="focus-visible-ring sr-only left-4 top-4 z-[100] rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground focus:not-sr-only focus:absolute"
    >
      Skip to main content
    </a>
  );
}
