/**
 * Normalize FastAPI error `detail` (string, array, or object) into student-safe text.
 */
export type FastApiValidationItem = {
  msg?: string;
  type?: string;
  loc?: (string | number)[];
};

const HTTP_STATUS_PATTERN = /^\(\d{3}\)$|^\d{3}$|\(\d{3}\)/;

export function parseApiDetail(detail: unknown, fallback = "Something went wrong. Please try again."): string {
  if (detail == null) return fallback;
  if (typeof detail === "string") {
    const trimmed = detail.trim();
    if (!trimmed) return fallback;
    if (HTTP_STATUS_PATTERN.test(trimmed)) return fallback;
    return trimmed;
  }
  if (Array.isArray(detail)) {
    for (const item of detail) {
      if (typeof item === "string" && item.trim()) return item.trim();
      if (item && typeof item === "object" && "msg" in item) {
        const msg = String((item as FastApiValidationItem).msg ?? "").trim();
        if (msg) return msg;
      }
    }
    return fallback;
  }
  if (typeof detail === "object" && detail !== null && "msg" in detail) {
    const msg = String((detail as FastApiValidationItem).msg ?? "").trim();
    if (msg) return msg;
  }
  return fallback;
}

/** True when the error looks like a lazy chunk / dynamic import failure (post-deploy stale cache). */
export function isChunkLoadError(error: unknown): boolean {
  if (!(error instanceof Error)) return false;
  const msg = error.message.toLowerCase();
  return (
    error.name === "ChunkLoadError" ||
    msg.includes("failed to fetch dynamically imported module") ||
    msg.includes("loading chunk") ||
    msg.includes("importing a module script failed")
  );
}
