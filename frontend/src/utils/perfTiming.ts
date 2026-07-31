/** Client-side login/dashboard performance marks (P1-01). */

const PREFIX = "login:";

export function markLoginFlow(step: string): void {
  if (typeof performance === "undefined") return;
  performance.mark(`${PREFIX}${step}`);
}

export function measureLoginFlow(name: string, startStep: string, endStep: string): void {
  if (typeof performance === "undefined") return;
  const start = `${PREFIX}${startStep}`;
  const end = `${PREFIX}${endStep}`;
  try {
    performance.measure(`${PREFIX}${name}`, start, end);
  } catch {
    /* marks may be missing */
  }
}

export function clearLoginFlowMeasures(): void {
  if (typeof performance === "undefined") return;
  performance.getEntriesByType("mark").forEach((e) => {
    if (e.name.startsWith(PREFIX)) performance.clearMarks(e.name);
  });
  performance.getEntriesByType("measure").forEach((e) => {
    if (e.name.startsWith(PREFIX)) performance.clearMeasures(e.name);
  });
}

export function parseServerTiming(header: string | null): Record<string, number> {
  if (!header) return {};
  const out: Record<string, number> = {};
  for (const part of header.split(",")) {
    const trimmed = part.trim();
    const nameMatch = /^([a-zA-Z0-9_-]+)/.exec(trimmed);
    const durMatch = /dur=([\d.]+)/.exec(trimmed);
    if (nameMatch && durMatch) {
      out[nameMatch[1]] = parseFloat(durMatch[1]);
    }
  }
  return out;
}

export function logLoginWaterfall(): void {
  if (typeof performance === "undefined" || typeof console === "undefined") return;
  const measures = performance
    .getEntriesByType("measure")
    .filter((e) => e.name.startsWith(PREFIX))
    .map((e) => ({ step: e.name.replace(PREFIX, ""), ms: Number(e.duration.toFixed(1)) }));
  if (measures.length === 0) {
    console.info("[ISKONNECT perf] No login measures recorded yet.");
    return;
  }
  console.info("[ISKONNECT perf] Login waterfall:");
  console.table(measures);
}

declare global {
  interface Window {
    __iskonnectLogLoginWaterfall?: () => void;
  }
}

/** Dev-only helper: call from browser console after signing in. */
export function installLoginWaterfallDevHelper(): void {
  if (typeof window === "undefined") return;
  const env = (import.meta as unknown as { env?: { DEV?: boolean } }).env;
  if (!env?.DEV) return;
  window.__iskonnectLogLoginWaterfall = logLoginWaterfall;
}
