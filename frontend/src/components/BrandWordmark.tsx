import { Link } from "react-router-dom";
import { cn, MIN_TOUCH_TARGET_CLASS } from "@/lib/utils";
import { brandLogoSrc, BRAND_LOGO_NAV_CLASS, LOGO_DARK_SRC, LOGO_LIGHT_SRC } from "@/lib/brandLogo";
import { useTheme } from "@/contexts/ThemeContext";

type BrandWordmarkSize = "sm" | "md" | "lg";

const sizeClasses: Record<BrandWordmarkSize, { logo: string; text: string; tagline?: string }> = {
  sm: {
    logo: "h-8 w-8 sm:h-9 sm:w-9",
    text: "font-brand text-lg font-black tracking-tight",
  },
  md: {
    logo: BRAND_LOGO_NAV_CLASS,
    text: "font-brand text-xl font-black tracking-tight sm:text-2xl",
    tagline: "text-xs",
  },
  lg: {
    logo: "h-14 w-14 sm:h-16 sm:w-16",
    text: "font-brand text-2xl font-black tracking-tight sm:text-3xl",
  },
};

interface BrandWordmarkProps {
  size?: BrandWordmarkSize;
  to?: string;
  showLogo?: boolean;
  showTagline?: boolean;
  tagline?: string;
  className?: string;
  textClassName?: string;
  inverted?: boolean;
}

export function BrandWordmark({
  size = "md",
  to = "/",
  showLogo = true,
  showTagline = false,
  tagline = "Scholarship matching for Filipino students",
  className,
  textClassName,
  inverted = false,
}: BrandWordmarkProps) {
  const { resolvedTheme } = useTheme();
  const styles = sizeClasses[size];
  const logoSrc = showLogo ? brandLogoSrc(resolvedTheme) : null;

  const content = (
    <>
      {showLogo && logoSrc ? (
        <img
          src={logoSrc}
          alt=""
          className={cn("object-contain", styles.logo)}
          onError={(e) => {
            const img = e.currentTarget;
            img.src = resolvedTheme === "dark" ? LOGO_LIGHT_SRC : LOGO_DARK_SRC;
          }}
        />
      ) : null}
      <span className="flex flex-col">
        <span
          className={cn(
            styles.text,
            inverted ? "text-white" : "text-primary-700 dark:text-primary-400",
            textClassName
          )}
        >
          Iskonnect
        </span>
        {showTagline && styles.tagline ? (
          <span
            className={cn(
              styles.tagline,
              inverted ? "text-slate-400" : "text-muted-foreground"
            )}
          >
            {tagline}
          </span>
        ) : null}
      </span>
    </>
  );

  if (to) {
    return (
      <Link
        to={to}
        className={cn("inline-flex items-center gap-2.5 focus-visible-ring rounded-md", MIN_TOUCH_TARGET_CLASS, className)}
      >
        {content}
      </Link>
    );
  }

  return <div className={cn("inline-flex items-center gap-2.5", className)}>{content}</div>;
}
