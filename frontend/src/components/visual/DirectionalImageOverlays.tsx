/**
 * Layered semi-transparent dark gradients over photography — improves legibility
 * and adds depth without a flat wash.
 */

export function HeroDirectionalOverlay() {
  return (
    <>
      {/* Left → right: copy sits on the left */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1] bg-gradient-to-r from-slate-950/90 via-slate-950/55 to-slate-950/20 sm:from-slate-950/85 sm:via-slate-950/50 sm:to-slate-950/15 lg:from-slate-950/80"
      />
      {/* Top depth + bottom weight */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1] bg-gradient-to-b from-slate-900/45 via-transparent to-slate-950/60"
      />
    </>
  );
}

export function AuthDirectionalOverlay() {
  return (
    <>
      {/* Bottom → top: trust copy at bottom; logo top-left */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1] bg-gradient-to-t from-slate-950/92 via-slate-950/45 to-slate-900/20"
      />
      {/* Corner depth toward top-left (logo + edge) */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-[1] bg-gradient-to-br from-slate-950/70 via-transparent to-transparent"
      />
    </>
  );
}
