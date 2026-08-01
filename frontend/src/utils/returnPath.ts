/** Safe in-app return path for post-login navigation (UX-15). */
export function safeReturnPath(from: unknown): string | null {
  if (typeof from !== "string" || !from.startsWith("/")) return null;
  if (from.startsWith("//")) return null;
  return from;
}
