/** Product facts — no fabricated user activity. */
const ITEMS = [
  "Eligibility rules drive your match ranking — not guesswork",
  "One student profile powers search, matching, and saved programs",
  "Always confirm deadlines and requirements on the official provider site",
  "Track saved scholarships and application status in one dashboard",
] as const;

export function SocialProofTicker() {
  const doubled = [...ITEMS, ...ITEMS];
  return (
    <div className="relative overflow-hidden border-y border-white/10 bg-slate-900 py-3 text-sm text-white">
      <div className="flex w-max animate-marquee gap-12 pr-12">
        {doubled.map((text, i) => (
          <span key={`${i}-${text}`} className="shrink-0 font-medium text-slate-200">
            <span className="text-success-400">●</span> {text}
          </span>
        ))}
      </div>
    </div>
  );
}
