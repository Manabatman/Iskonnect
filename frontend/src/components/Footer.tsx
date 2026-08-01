import { Link } from "react-router-dom";
import { APP_RELEASE_DATE, APP_RELEASE_LABEL } from "../data/changelog";
import { usePublicStats } from "../hooks/usePublicStats";

export const footerProductLinks = [
  { to: "/scholarships/search", label: "Search" },
  { to: "/how-it-works", label: "How it works" },
  { to: "/roadmap", label: "Roadmap" },
  { to: "/changelog", label: "Changelog" },
] as const;

export const footerTransparencyLinks = [
  { to: "/how-we-verify", label: "How we verify" },
  { to: "/how-matching-works", label: "How matching works" },
  { to: "/scholarship-status", label: "Scholarship status guide" },
] as const;

export const footerCompanyLinks = [
  { to: "/about", label: "About" },
  { to: "/contact", label: "Contact" },
  { to: "/success-stories", label: "Success stories" },
] as const;

export const footerLegalLinks = [
  { to: "/terms", label: "Terms" },
  { to: "/privacy", label: "Privacy" },
] as const;

const footerLinkClass =
  "inline-flex min-h-11 items-center text-sm text-slate-400 transition hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900";

function FooterColumn({ title, links }: { title: string; links: readonly { to: string; label: string }[] }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</p>
      <ul className="mt-4 space-y-2">
        {links.map(({ to, label }) => (
          <li key={to}>
            <Link to={to} className={footerLinkClass}>
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function Footer() {
  const stats = usePublicStats();
  const lastVerified = stats?.last_catalog_verification_at
    ? new Date(stats.last_catalog_verification_at).toLocaleDateString(undefined, {
        month: "long",
        day: "numeric",
        year: "numeric",
      })
    : null;

  return (
    <footer id="about" className="bg-slate-900 py-12 dark:bg-slate-950 sm:py-16">
      <div className="mx-auto max-w-[1200px] px-4 sm:px-6">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-5">
          <div className="sm:col-span-2 lg:col-span-1">
            <p className="font-semibold text-white">Iskonnect</p>
            <p className="mt-2 max-w-xs text-sm leading-relaxed text-slate-400">
              Connecting Filipino students to scholarship opportunities they actually qualify for.
            </p>
            <p className="mt-2 text-xs font-medium text-primary-300">
              {APP_RELEASE_LABEL} · {APP_RELEASE_DATE}
            </p>
            {lastVerified ? (
              <p className="mt-3 text-xs text-slate-500">Catalog last verified {lastVerified}</p>
            ) : null}
          </div>

          <FooterColumn title="Product" links={footerProductLinks} />
          <FooterColumn title="Transparency" links={footerTransparencyLinks} />
          <FooterColumn title="Company" links={footerCompanyLinks} />
          <FooterColumn title="Legal" links={footerLegalLinks} />
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-4 border-t border-slate-800 pt-8 sm:flex-row">
          <Link to="/contact" className="text-sm text-slate-400 transition hover:text-white">
            By Mark Justin S. Manabat.
          </Link>
          <p className="text-xs text-slate-400">© {new Date().getFullYear()} Iskonnect. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
