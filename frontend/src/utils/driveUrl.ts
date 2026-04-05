/** Normalize pasted Drive / folder URLs for storage and opening. */
export function normalizeDriveUrl(input: string): string {
  const t = input.trim();
  if (!t) return "";
  if (t.startsWith("http://")) return `https://${t.slice(7)}`;
  return t;
}

/**
 * Short display like drive.google.com/.../abc123 — keeps host + last path segment hint.
 */
export function maskDriveUrl(url: string): string {
  const t = url.trim();
  if (!t) return "";
  try {
    const u = new URL(t.startsWith("http") ? t : `https://${t}`);
    const host = u.hostname.replace(/^www\./, "");
    const parts = u.pathname.split("/").filter(Boolean);
    const last = parts.length ? parts[parts.length - 1] : "";
    const tail = last.length > 12 ? `${last.slice(0, 6)}…${last.slice(-4)}` : last || "folder";
    return `${host}/…/${tail}`;
  } catch {
    return t.length > 48 ? `${t.slice(0, 24)}…${t.slice(-12)}` : t;
  }
}
