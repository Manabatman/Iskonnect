/** Inter 700 — below-the-fold emphasis; not needed for landing LCP. */
export function loadDeferredFontWeights(): void {
  const run = () => {
    void import("@fontsource/inter/latin-700.css");
  };
  if (typeof window.requestIdleCallback === "function") {
    window.requestIdleCallback(run);
  } else {
    window.setTimeout(run, 1);
  }
}
