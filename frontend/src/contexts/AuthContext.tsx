import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { NetworkError, apiFetch } from "../api/client";
import { ERROR_COPY } from "../constants/errorCopy";
import { parseApiDetail } from "../utils/apiErrors";
import { clearProfileDraft } from "../components/profile-builder/profileBuilderState";
import {
  installLoginWaterfallDevHelper,
  markLoginFlow,
  measureLoginFlow,
} from "../utils/perfTiming";

const AUTH_TOKEN_KEY = "auth_token";
const AUTH_REFRESH_KEY = "auth_refresh_token";

/** Fired when login/register/logout changes the authenticated user so dashboards reset cached state. */
export const AUTH_USER_CHANGED_EVENT = "scholarship-match-auth-user-changed";

export type AuthUserChangedDetail = {
  previousUserId: number | null;
  userId: number | null;
};

function dispatchAuthUserChanged(previousUserId: number | null, userId: number | null) {
  window.dispatchEvent(
    new CustomEvent(AUTH_USER_CHANGED_EVENT, {
      detail: { previousUserId, userId } satisfies AuthUserChangedDetail,
    })
  );
}

export interface AuthUser {
  id: number;
  email: string;
  role: string;
  emailVerified: boolean;
  requireEmailVerification: boolean;
  hasProfile: boolean;
}

export type RegisterResult =
  | { status: "authenticated"; user: AuthUser; betaNotice?: string }
  | { status: "verify_required"; message: string; email: string };

/** Thrown when login is blocked until the user verifies their email (HTTP 403). */
export class EmailVerificationRequiredError extends Error {
  readonly name = "EmailVerificationRequiredError";

  constructor(message: string) {
    super(message);
    Object.setPrototypeOf(this, EmailVerificationRequiredError.prototype);
  }
}

type TokenPayload = {
  user_id: number;
  email?: string;
  role?: string;
  email_verified?: boolean;
  require_email_verification?: boolean;
  has_profile?: boolean;
};

export function userFromTokenPayload(data: TokenPayload): AuthUser {
  return {
    id: data.user_id,
    email: data.email ?? "",
    role: data.role ?? "student",
    emailVerified: Boolean(data.email_verified),
    requireEmailVerification: data.require_email_verification !== false,
    hasProfile: Boolean(data.has_profile),
  };
}

/** Presentational only — decode JWT payload without verification for optimistic shell (PERF-03). */
export function decodeJwtPayload(token: string): TokenPayload | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
    const json = atob(padded);
    const data = JSON.parse(json) as TokenPayload;
    if (typeof data.user_id !== "number") return null;
    return data;
  } catch {
    return null;
  }
}

function cachedUserFromStorage(): AuthUser | null {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (!token) return null;
  const payload = decodeJwtPayload(token);
  if (!payload) return null;
  return userFromTokenPayload(payload);
}

/** Post-login/register destination based on profile completeness (P1-05). */
export function getPostAuthPath(user: AuthUser, returnTo?: string | null): string {
  if (returnTo) return returnTo;
  return user.hasProfile ? "/dashboard" : "/profile-builder";
}

interface AuthContextType {
  token: string | null;
  user: AuthUser | null;
  loading: boolean;
  authError: string | null;
  clearAuthError: () => void;
  login: (email: string, password: string) => Promise<AuthUser>;
  register: (email: string, password: string, turnstileToken?: string | null) => Promise<RegisterResult>;
  logout: () => Promise<void>;
  authHeaders: () => Record<string, string>;
}

const AuthContext = createContext<AuthContextType | null>(null);

async function tryRefreshAccessToken(): Promise<(TokenPayload & {
  access_token: string;
  refresh_token: string;
}) | null> {
  const rt = localStorage.getItem(AUTH_REFRESH_KEY);
  if (!rt) return null;
  const res = await apiFetch("/api/v1/auth/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: rt }),
  });
  if (!res.ok) {
    localStorage.removeItem(AUTH_REFRESH_KEY);
    return null;
  }
  return res.json();
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() =>
    localStorage.getItem(AUTH_TOKEN_KEY)
  );
  const [user, setUser] = useState<AuthUser | null>(() => cachedUserFromStorage());
  const [loading, setLoading] = useState(() => Boolean(localStorage.getItem(AUTH_TOKEN_KEY)));
  const [authError, setAuthError] = useState<string | null>(null);
  const skipFetchUserRef = useRef(false);
  /** Last signed-in user id — used to detect account switches vs anonymous → authenticated. */
  const lastAuthenticatedUserIdRef = useRef<number | null>(null);

  const setToken = useCallback((t: string | null) => {
    if (t) {
      localStorage.setItem(AUTH_TOKEN_KEY, t);
    } else {
      localStorage.removeItem(AUTH_TOKEN_KEY);
    }
    setTokenState(t);
  }, []);

  const setRefreshToken = useCallback((t: string | null) => {
    if (t) {
      localStorage.setItem(AUTH_REFRESH_KEY, t);
    } else {
      localStorage.removeItem(AUTH_REFRESH_KEY);
    }
  }, []);

  const clearAuthError = useCallback(() => setAuthError(null), []);

  const applyUserFromMe = useCallback((data: Record<string, unknown>) => {
    setUser({
      id: data.id as number,
      email: data.email as string,
      role: (data.role as string) ?? "student",
      emailVerified: Boolean(data.email_verified),
      requireEmailVerification: data.require_email_verification !== false,
      hasProfile: Boolean(data.has_profile),
    });
    setAuthError(null);
  }, []);

  const fetchUser = useCallback(
    async (t: string) => {
      markLoginFlow("auth-me-start");
      const loadMe = async (access: string) => {
        const res = await apiFetch("/api/v1/auth/me", {
          headers: { Authorization: `Bearer ${access}` },
        });
        if (!res.ok) {
          if (res.status === 401 || res.status === 403) {
            return false;
          }
          setAuthError(`Could not verify session (${res.status}). Will retry when the server is available.`);
          return true;
        }
        const data = await res.json();
        applyUserFromMe(data);
        markLoginFlow("auth-me-done");
        measureLoginFlow("auth-me", "auth-me-start", "auth-me-done");
        return true;
      };

      try {
        let ok = await loadMe(t);
        if (!ok) {
          const refreshed = await tryRefreshAccessToken();
          if (refreshed) {
            setToken(refreshed.access_token);
            setRefreshToken(refreshed.refresh_token);
            skipFetchUserRef.current = true;
            setUser(userFromTokenPayload(refreshed));
            ok = true;
          }
          if (!ok) {
            setToken(null);
            setRefreshToken(null);
            setUser(null);
            setAuthError(null);
          }
        }
      } catch (err) {
        if (err instanceof NetworkError) {
          setAuthError("Server unreachable — your session is preserved. Try again when you are online.");
          return;
        }
        setAuthError(ERROR_COPY.load_failed.message);
      }
    },
    [applyUserFromMe, setToken, setRefreshToken]
  );

  useEffect(() => {
    installLoginWaterfallDevHelper();
  }, []);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    if (skipFetchUserRef.current) {
      skipFetchUserRef.current = false;
      setLoading(false);
      return;
    }
    fetchUser(token).finally(() => setLoading(false));
  }, [token, fetchUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      const res = await apiFetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        const detail = data?.detail ?? "Login failed";
        if (res.status === 403) {
          throw new EmailVerificationRequiredError(parseApiDetail(detail, "Please verify your email before signing in."));
        }
        if (res.status === 429) {
          throw new Error(parseApiDetail(detail, "Too many failed sign-in attempts. Please wait and try again."));
        }
        throw new Error(parseApiDetail(detail, "Login failed"));
      }
      markLoginFlow("login-response");
      measureLoginFlow("login-request", "submit", "login-response");
      const data = await res.json();
      const authUser = userFromTokenPayload(data);
      setToken(data.access_token);
      if (data.refresh_token) setRefreshToken(data.refresh_token);
      skipFetchUserRef.current = true;
      setUser(authUser);
      setLoading(false);
      setAuthError(null);
      const prevId = lastAuthenticatedUserIdRef.current;
      if (prevId !== null && prevId !== data.user_id) {
        clearProfileDraft();
      }
      lastAuthenticatedUserIdRef.current = data.user_id;
      dispatchAuthUserChanged(prevId, data.user_id);
      return authUser;
    },
    [setToken, setRefreshToken]
  );

  const register = useCallback(
    async (email: string, password: string, turnstileToken?: string | null) => {
      const body: Record<string, string> = { email, password };
      if (turnstileToken) body.turnstile_token = turnstileToken;
      const res = await apiFetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(parseApiDetail(data?.detail, "Registration failed"));
      }
      const data = await res.json();
      if (!data.access_token || data.user_id == null) {
        const message = parseApiDetail(
          data.detail,
          "Check your email to verify your address before signing in.",
        );
        return { status: "verify_required" as const, message, email };
      }
      const authUser = userFromTokenPayload(data);
      setToken(data.access_token);
      if (data.refresh_token) setRefreshToken(data.refresh_token);
      skipFetchUserRef.current = true;
      setUser(authUser);
      setLoading(false);
      setAuthError(null);
      const prevId = lastAuthenticatedUserIdRef.current;
      if (prevId !== null && prevId !== data.user_id) {
        clearProfileDraft();
      }
      lastAuthenticatedUserIdRef.current = data.user_id;
      dispatchAuthUserChanged(prevId, data.user_id);
      const betaNotice =
        typeof data.detail === "string" && data.detail.includes("Public Beta") ? data.detail : undefined;
      return { status: "authenticated" as const, user: authUser, betaNotice };
    },
    [setToken, setRefreshToken]
  );

  const logout = useCallback(async () => {
    const rt = localStorage.getItem(AUTH_REFRESH_KEY);
    if (rt) {
      try {
        await apiFetch("/api/v1/auth/logout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: rt }),
        });
      } catch {
        /* ignore */
      }
    }
    const prevId = lastAuthenticatedUserIdRef.current;
    setRefreshToken(null);
    setToken(null);
    setUser(null);
    setAuthError(null);
    clearProfileDraft();
    lastAuthenticatedUserIdRef.current = null;
    dispatchAuthUserChanged(prevId, null);
  }, [setToken, setRefreshToken]);

  const authHeaders = useCallback(
    (): Record<string, string> => {
      if (!token) return {};
      return { Authorization: `Bearer ${token}` };
    },
    [token]
  );

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        loading,
        authError,
        clearAuthError,
        login,
        register,
        logout,
        authHeaders,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
