const _env = (import.meta as unknown as { env?: { VITE_API_BASE_URL?: string; PROD?: boolean } }).env;
const _apiBase = _env?.VITE_API_BASE_URL?.trim();
const _isProd = Boolean(_env?.PROD);

if (_isProd && !_apiBase) {
  throw new Error(
    "VITE_API_BASE_URL must be set in production builds. Configure it in your hosting provider (e.g. Vercel) environment variables.",
  );
}

export const API_BASE_URL = _apiBase ?? "http://localhost:8000";
if (!_apiBase && typeof console !== "undefined") {
  console.warn(
    "[API] VITE_API_BASE_URL is not set; using http://localhost:8000. Set it in production builds.",
  );
}

const AUTH_TOKEN_KEY = "auth_token";
const AUTH_REFRESH_KEY = "auth_refresh_token";

/** Long enough for Render free-tier cold starts (often 50s+ after spin-down). */
const FETCH_TIMEOUT_MS = 70_000;
const NETWORK_RETRY_DELAY_MS = 1_000;

const API_BUSY = "iskonnect-api-busy";
const API_IDLE = "iskonnect-api-idle";

let apiInFlight = 0;

function bumpApiInFlight(delta: number) {
  const prev = apiInFlight;
  apiInFlight += delta;
  if (typeof window === "undefined") return;
  if (prev === 0 && apiInFlight > 0) {
    window.dispatchEvent(new CustomEvent(API_BUSY));
  }
  if (prev > 0 && apiInFlight === 0) {
    window.dispatchEvent(new CustomEvent(API_IDLE));
  }
}

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

function hasAuthHeader(options?: RequestInit): boolean {
  const headers = options?.headers;
  if (!headers) return false;
  if (headers instanceof Headers) {
    return headers.has("Authorization");
  }
  if (Array.isArray(headers)) {
    return headers.some(([k]) => k.toLowerCase() === "authorization");
  }
  return "Authorization" in headers || "authorization" in headers;
}

async function refreshAccessToken(): Promise<string | null> {
  const rt = localStorage.getItem(AUTH_REFRESH_KEY);
  if (!rt) return null;

  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: rt }),
      signal: controller.signal,
    });
    if (!res.ok) {
      localStorage.removeItem(AUTH_REFRESH_KEY);
      localStorage.removeItem(AUTH_TOKEN_KEY);
      return null;
    }
    const data = (await res.json()) as { access_token?: string; refresh_token?: string };
    if (!data.access_token) return null;
    localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
    if (data.refresh_token) {
      localStorage.setItem(AUTH_REFRESH_KEY, data.refresh_token);
    }
    return data.access_token;
  } catch {
    return null;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

function withBearerToken(options: RequestInit | undefined, accessToken: string): RequestInit {
  const headers = new Headers(options?.headers ?? undefined);
  headers.set("Authorization", `Bearer ${accessToken}`);
  return { ...options, headers };
}

async function fetchOnce(url: string, options?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    if (!res.ok && !_isProd) {
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

  const attempt = async (opts?: RequestInit): Promise<Response> => {
    try {
      return await fetchOnce(url, opts);
    } catch (err) {
      if (!isAbortOrNetworkFailure(err)) throw err;
      throw new NetworkError("Unable to reach the server", { cause: err });
    }
  };

  bumpApiInFlight(1);
  try {
    try {
      let res = await attempt(options);
      if (
        res.status === 401 &&
        hasAuthHeader(options) &&
        !path.includes("/auth/refresh") &&
        !path.includes("/auth/login")
      ) {
        const newToken = await refreshAccessToken();
        if (newToken) {
          res = await attempt(withBearerToken(options, newToken));
        }
      }
      return res;
    } catch (first) {
      if (!(first instanceof NetworkError)) throw first;
      if (!isIdempotentMethod(options)) throw first;
      await new Promise((r) => setTimeout(r, NETWORK_RETRY_DELAY_MS));
      return await attempt(options);
    }
  } finally {
    bumpApiInFlight(-1);
  }
}
