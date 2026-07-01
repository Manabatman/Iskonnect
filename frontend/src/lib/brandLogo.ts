/** Brand logos: light UI / system default vs dark UI. */
export const LOGO_LIGHT_SRC = "/images/logo-light.png";
export const LOGO_DARK_SRC = "/images/logo-dark.png";

/** Navbar mark — prominent beside wordmark (56→64px was h-14/h-16; now larger). */
export const BRAND_LOGO_NAV_CLASS = "h-10 w-10 object-contain sm:h-12 sm:w-12 md:h-14 md:w-14";
export const BRAND_LOGO_NAV_WIDTH = 56;
export const BRAND_LOGO_NAV_HEIGHT = 56;

/** Auth panel corner mark (login / register hero). */
export const BRAND_LOGO_AUTH_CLASS =
  "absolute left-8 top-8 object-contain lg:left-12 lg:top-12 h-16 w-16 lg:h-20 lg:w-20";
export const BRAND_LOGO_AUTH_WIDTH = 80;
export const BRAND_LOGO_AUTH_HEIGHT = 80;

export function brandLogoSrc(resolvedTheme: "light" | "dark"): string {
  return resolvedTheme === "dark" ? LOGO_DARK_SRC : LOGO_LIGHT_SRC;
}
