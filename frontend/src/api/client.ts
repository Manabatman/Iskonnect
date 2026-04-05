const _env = (import.meta as unknown as { env?: { VITE_API_BASE_URL?: string } }).env;
export const API_BASE_URL = _env?.VITE_API_BASE_URL ?? "http://localhost:8000";
if (!_env?.VITE_API_BASE_URL && typeof console !== "undefined") {
  console.warn(
    "[API] VITE_API_BASE_URL is not set; using http://localhost:8000. Set it in production builds.",
  );
}

const FETCH_TIMEOUT_MS = 10_000;
const NETWORK_RETRY_DELAY_MS = 1_000;

/** Thrown when fetch fails (offline, DNS, CORS, timeout, etc.). */
export class NetworkError extends Error {
  override readonly cause?: unknown;

  constructor(message = "Unable to reach the server", options?: { cause?: unknown }) {
    super(message);
    this.name = "NetworkError";
    if (options?.cause !== undefined) this.cause = options.cause;
  }
}

function isAbortOrNetworkFailure(err: unknown): boolean {
  if (err instanceof TypeError) return true;
  if (err instanceof DOMException && err.name === "AbortError") return true;
  return false;
}

/** Only GET/HEAD are safe to auto-retry (writes may have succeeded on the server). */
function isIdempotentMethod(options?: RequestInit): boolean {
  const m = (options?.method ?? "GET").toUpperCase();
  return m === "GET" || m === "HEAD";
}

async function fetchOnce(url: string, options?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    if (!res.ok) {
      const pathOnly = url.replace(/^https?:\/\/[^/]+/, "");
      const body = await res.clone().text().catch(() => "");
      console.error(`[API] ${options?.method ?? "GET"} ${pathOnly} -> ${res.status}`, body);
    }
    return res;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function apiFetch(path: string, options?: RequestInit): Promise<Response> {
  const url = `${API_BASE_URL}${path}`;

  const attempt = async (): Promise<Response> => {
    try {
      return await fetchOnce(url, options);
    } catch (err) {
      if (!isAbortOrNetworkFailure(err)) throw err;
      throw new NetworkError("Unable to reach the server", { cause: err });
    }
  };

  try {
    return await attempt();
  } catch (first) {
    if (!(first instanceof NetworkError)) throw first;
    if (!isIdempotentMethod(options)) throw first;
    await new Promise((r) => setTimeout(r, NETWORK_RETRY_DELAY_MS));
    return await attempt();
  }
}
