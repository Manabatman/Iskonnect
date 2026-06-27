import type { ReactNode } from "react";

interface SectionProps {
  children: ReactNode;
  variant?: "white" | "tint";
  className?: string;
  id?: string;
  border?: "top" | "bottom" | "both" | "none";
}

export function Section({
  children,
  variant = "white",
  className = "",
  id,
  border = "none",
}: SectionProps) {
  const borderClass =
    border === "top"
      ? "border-t border-slate-200 dark:border-slate-800"
      : border === "bottom"
        ? "border-b border-slate-200 dark:border-slate-800"
        : border === "both"
          ? "border-y border-slate-200 dark:border-slate-800"
          : "";

  const bgClass =
    variant === "tint"
      ? "bg-white dark:bg-slate-950"
      : "bg-white dark:bg-slate-900/40";

  return (
    <section
      id={id}
      className={`relative overflow-hidden py-20 sm:py-28 ${borderClass} ${bgClass} ${className}`}
    >
      {variant === "tint" ? (
        <div aria-hidden className="pointer-events-none absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-b from-primary-50/70 via-white to-white dark:from-primary-950/20 dark:via-slate-950 dark:to-slate-950" />
          <div className="absolute left-1/2 top-[-6rem] h-72 w-[48rem] -translate-x-1/2 rounded-full bg-primary-200/40 blur-3xl dark:bg-primary-900/20" />
          <div className="absolute inset-0 opacity-60 dark:opacity-30 [background-image:linear-gradient(to_right,rgba(2,6,23,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(2,6,23,0.05)_1px,transparent_1px)] [background-size:44px_44px] [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]" />
        </div>
      ) : null}
      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">{children}</div>
    </section>
  );
}

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: "center" | "left";
}

export function SectionHeader({
  eyebrow,
  title,
  description,
  align = "center",
}: SectionHeaderProps) {
  const alignClass = align === "center" ? "mx-auto max-w-3xl text-center" : "max-w-2xl";

  return (
    <div className={alignClass}>
      {eyebrow ? (
        <span className="inline-flex items-center gap-2 rounded-full border border-primary-200 bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-700 dark:border-primary-900/60 dark:bg-primary-950/40 dark:text-primary-300">
          {eyebrow}
        </span>
      ) : null}
      <h2
        className={`text-balance text-3xl font-bold leading-tight tracking-tight text-slate-900 dark:text-white sm:text-4xl ${eyebrow ? "mt-5" : ""}`}
      >
        {title}
      </h2>
      {description ? (
        <p className="mt-5 text-pretty text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
          {description}
        </p>
      ) : null}
    </div>
  );
}

interface IconTileProps {
  Icon: import("./landingData").LucideIcon;
  className?: string;
}

export function IconTile({ Icon, className = "" }: IconTileProps) {
  return (
    <span
      aria-hidden
      className={`flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 text-white shadow-lg shadow-primary-600/25 ring-1 ring-inset ring-white/20 transition duration-[250ms] ease-out group-hover:scale-105 motion-safe:group-hover:rotate-3 ${className}`}
    >
      <Icon className="h-6 w-6" strokeWidth={2} />
    </span>
  );
}

export const cardClass =
  "group relative flex flex-col rounded-2xl border border-slate-200 bg-white p-7 shadow-sm transition duration-[250ms] ease-out hover:border-primary-300 hover:shadow-xl hover:shadow-primary-900/5 motion-safe:hover:-translate-y-1 dark:border-slate-800 dark:bg-slate-900/60 dark:hover:border-primary-700";

export const primaryButtonClass =
  "inline-flex items-center justify-center gap-2 rounded-xl bg-primary-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-primary-600/25 transition hover:bg-primary-700 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-900";

export const secondaryButtonClass =
  "inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800 dark:focus-visible:ring-offset-slate-900";
