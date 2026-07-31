import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Menu } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";
import { brandLogoSrc, BRAND_LOGO_NAV_CLASS, BRAND_LOGO_NAV_HEIGHT, BRAND_LOGO_NAV_WIDTH, LOGO_LIGHT_SRC } from "../lib/brandLogo";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn, MIN_TOUCH_TARGET_CLASS } from "@/lib/utils";

const navLinkClass = (active: boolean) =>
  cn(
    "inline-flex min-h-11 items-center rounded-md px-3 text-sm transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
    active ? "font-medium text-primary" : "text-muted-foreground hover:text-primary"
  );

export function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { resolvedTheme } = useTheme();
  const path = location.pathname;
  const logoSrc = brandLogoSrc(resolvedTheme);

  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [path]);

  const isActive = (to: string) => (to === "/" ? path === "/" : path === to || path.startsWith(`${to}/`));

  const navItems: { to: string; label: string; match?: () => boolean }[] = [
    { to: "/", label: "Home" },
    { to: "/scholarships/search", label: "Explore", match: () => path.startsWith("/scholarships") },
    {
      to: "/how-it-works",
      label: "Trust & matching",
      match: () => isActive("/how-it-works") || isActive("/transparency") || isActive("/match-methodology"),
    },
  ] as const;

  const navLinks = (mobile = false) =>
    navItems.map(({ to, label, match }) => {
      const active = match ? match() : isActive(to);
      return (
        <Link
          key={to}
          to={to}
          className={cn(navLinkClass(active), mobile && "w-full")}
          aria-current={active ? "page" : undefined}
          onClick={() => mobile && setMobileOpen(false)}
        >
          {label}
        </Link>
      );
    });

  const authLinks = (mobile = false) =>
    user ? (
      <>
        <Link
          to="/dashboard"
          className={cn(navLinkClass(path.startsWith("/dashboard")), mobile && "w-full")}
          aria-current={path.startsWith("/dashboard") ? "page" : undefined}
          onClick={() => mobile && setMobileOpen(false)}
        >
          Dashboard
        </Link>
        <span
          className="hidden max-w-[10rem] truncate text-sm text-muted-foreground sm:inline"
          title={user.email}
        >
          {user.email}
        </span>
        <Button
          type="button"
          variant="ghost"
          className={cn("text-sm", mobile && "w-full justify-start")}
          onClick={() => {
            logout();
            navigate("/");
            setMobileOpen(false);
          }}
        >
          Log out
        </Button>
      </>
    ) : (
      <>
        <Link
          to="/login"
          className={cn(navLinkClass(isActive("/login")), mobile && "w-full")}
          aria-current={isActive("/login") ? "page" : undefined}
          onClick={() => mobile && setMobileOpen(false)}
        >
          Login
        </Link>
        <Button asChild className={mobile ? "w-full" : undefined}>
          <Link to="/register" onClick={() => mobile && setMobileOpen(false)}>
            Get Started
          </Link>
        </Button>
      </>
    );

  return (
    <header
      className={cn(
        "sticky top-0 z-40 border-b pt-[env(safe-area-inset-top)] transition-colors duration-base",
        scrolled ? "border-border bg-background shadow-1" : "border-border/80 bg-background"
      )}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-2 sm:px-6 sm:py-2.5">
        <Link to="/" className="flex shrink-0 items-center gap-3">
          <img
            src={logoSrc}
            alt=""
            className={BRAND_LOGO_NAV_CLASS}
            width={BRAND_LOGO_NAV_WIDTH}
            height={BRAND_LOGO_NAV_HEIGHT}
            onError={(e) => {
              (e.target as HTMLImageElement).src = LOGO_LIGHT_SRC;
            }}
          />
          <span>
            <span className="block font-display text-xl tracking-tight text-primary sm:text-2xl">Iskonnect</span>
            <span className="hidden text-xs font-medium text-muted-foreground sm:block">
              Connecting Filipino Students to Opportunity
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-x-2 md:flex" aria-label="Primary">
          {navLinks()}
        </nav>

        <div className="hidden items-center gap-2 md:flex">{authLinks()}</div>

        <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
          <SheetTrigger asChild>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className={cn("md:hidden", MIN_TOUCH_TARGET_CLASS)}
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
            >
              <Menu className="h-6 w-6" aria-hidden />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-[min(100vw-2rem,20rem)]">
            <SheetHeader>
              <SheetTitle>Menu</SheetTitle>
            </SheetHeader>
            <nav className="mt-6 flex flex-col gap-2" aria-label="Mobile primary">
              {navLinks(true)}
              <div className="mt-4 flex flex-col gap-2 border-t border-border pt-4">{authLinks(true)}</div>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
