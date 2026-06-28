/** Brand logos: light UI / system default vs dark UI. */
export const LOGO_LIGHT_SRC = "/images/logo-light.png";
export const LOGO_DARK_SRC = "/images/logo-dark.png";

export function brandLogoSrc(resolvedTheme: "light" | "dark"): string {
  return resolvedTheme === "dark" ? LOGO_DARK_SRC : LOGO_LIGHT_SRC;
}
