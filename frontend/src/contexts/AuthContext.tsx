import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { NetworkError, apiFetch } from "../api/client";

const AUTH_TOKEN_KEY = "auth_token";
const AUTH_REFRESH_KEY = "auth_refresh_token";

export interface AuthUser {
  id: number;
  email: string;
  role: string;
}

interface AuthContextType {
  token: string | null;
  user: AuthUser | null;
  loading: boolean;
  authError: string | null;
  clearAuthError: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  authHeaders: () => Record<string, string>;
}

const AuthContext = createContext<AuthContextType | null>(null);

async function tryRefreshAccessToken(): Promise<{ access_token: string; refresh_token: string } | null> {
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
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState<string | null>(null);

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

  const fetchUser = useCallback(
    async (t: string) => {
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
        setUser({ id: data.id, email: data.email, role: data.role ?? "student" });
        setAuthError(null);
        return true;
      };

      try {
        let ok = await loadMe(t);
        if (!ok) {
          const refreshed = await tryRefreshAccessToken();
          if (refreshed) {
            setToken(refreshed.access_token);
            setRefreshToken(refreshed.refresh_token);
            ok = await loadMe(refreshed.access_token);
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
        setAuthError("Something went wrong while loading your account.");
      }
    },
    [setToken, setRefreshToken]
  );

  useEffect(() => {
    if (!token) {
      setUser(null);
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
        throw new Error(data?.detail ?? "Login failed");
      }
      const data = await res.json();
      setToken(data.access_token);
      if (data.refresh_token) setRefreshToken(data.refresh_token);
      setUser({ id: data.user_id, email, role: data.role ?? "student" });
      setAuthError(null);
    },
    [setToken, setRefreshToken]
  );

  const register = useCallback(
    async (email: string, password: string) => {
      const res = await apiFetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Registration failed");
      }
      const data = await res.json();
      setToken(data.access_token);
      if (data.refresh_token) setRefreshToken(data.refresh_token);
      setUser({ id: data.user_id, email, role: data.role ?? "student" });
      setAuthError(null);
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
    setRefreshToken(null);
    setToken(null);
    setUser(null);
    setAuthError(null);
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
