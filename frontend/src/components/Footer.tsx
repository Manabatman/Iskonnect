import { Link } from "react-router-dom";

const productLinks = [
  { to: "/how-it-works", label: "How it works" },
  { to: "/scholarships/search", label: "Scholarships" },
  { to: "/how-we-verify", label: "How we verify" },
  { to: "/scholarship-status", label: "Scholarship status" },
  { to: "/transparency", label: "Transparency" },
  { to: "/faq", label: "FAQ" },
] as const;

const companyLinks = [
  { to: "/about", label: "About" },
  { to: "/why-iskonnect", label: "Why ISKONNECT" },
  { to: "/terms", label: "Terms" },
  { to: "/privacy", label: "Privacy" },
  { to: "/settings", label: "Settings" },
] as const;

const footerLinkClass =
  "text-sm text-slate-400 transition hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900";

export function Footer() {
  return (
    <footer id="about" className="bg-slate-900 py-12 dark:bg-slate-950 sm:py-16">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div className="sm:col-span-2 lg:col-span-1">
            <p className="font-semibold text-white">Iskonnect</p>
            <p className="mt-2 max-w-xs text-sm leading-relaxed text-slate-400">
              Connecting Filipino students to scholarship opportunities they actually qualify for.
            </p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Product</p>
            <ul className="mt-4 space-y-2">
              {productLinks.map(({ to, label }) => (
                <li key={to}>
                  <Link to={to} className={footerLinkClass}>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Company</p>
            <ul className="mt-4 space-y-2">
              {companyLinks.map(({ to, label }) => (
                <li key={to}>
                  <Link to={to} className={footerLinkClass}>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Sources</p>
            <p className="mt-4 text-sm leading-relaxed text-slate-400">
              Programs from CHED, DOST-SEI, TESDA, LGUs, universities, and private foundations. Always verify details on
              the official provider site.
            </p>
          </div>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-4 border-t border-slate-800 pt-8 sm:flex-row">
          <p className="text-sm text-slate-500">By Mark Justin S. Manabat.</p>
          <p className="text-xs text-slate-500">© {new Date().getFullYear()} Iskonnect. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
