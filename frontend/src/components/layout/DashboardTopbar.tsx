import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { apiFetch } from "../../api/client";

export interface DashboardTopbarProps {
  onOpenMobileSidebar: () => void;
}

type ScholarshipSearchHit = {
  id: number;
  title: string;
  provider?: string | null;
};

type ScholarshipSearchApiResponse = {
  results: ScholarshipSearchHit[];
  total: number;
};

type NotificationItem = {
  id: number;
  type: string;
  title: string;
  body?: string | null;
  scholarship_id?: number | null;
  is_read: boolean;
  created_at: string;
};

function titleForPath(pathname: string): string {
  if (pathname === "/dashboard") return "Dashboard";
  if (pathname.startsWith("/opportunities")) return "Opportunities";
  if (pathname.startsWith("/scholarships/search")) return "Scholarship search";
  if (pathname.startsWith("/scholarships")) return "Scholarships";
  if (pathname.startsWith("/scholarship/")) return "Scholarship";
  if (pathname.startsWith("/applications")) return "Applications";
  if (pathname.startsWith("/documents")) return "Documents";
  if (pathname.startsWith("/profile-builder")) return "Complete Your Profile";
  if (pathname.startsWith("/settings")) return "Account settings";
  if (pathname.startsWith("/match-compare")) return "Compare matches";
  if (pathname.startsWith("/match/")) return "Match results";
  if (pathname.startsWith("/admin/analytics")) return "Admin analytics";
  if (pathname.startsWith("/admin")) return "Admin";
  if (pathname.startsWith("/sponsor")) return "Sponsor portal";
  if (pathname.startsWith("/school")) return "School verification";
  return "Dashboard";
}

function IconMenu({ className }: { className?: string }) {
  return (
    <svg className={className} width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" fill="currentColor" />
    </svg>
  );
}

function IconBell({ className }: { className?: string }) {
  return (
    <svg className={className} width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"
        fill="currentColor"
      />
    </svg>
  );
}

function IconChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path d="M7 10l5 5 5-5z" fill="currentColor" />
    </svg>
  );
}

const SEARCH_DEBOUNCE_MS = 300;

export function DashboardTopbar({ onOpenMobileSidebar }: DashboardTopbarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, authHeaders } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifUnread, setNotifUnread] = useState<number | null>(null);
  const [notifOpen, setNotifOpen] = useState(false);
  const [notifItems, setNotifItems] = useState<NotificationItem[]>([]);
  const [notifLoading, setNotifLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchResults, setSearchResults] = useState<ScholarshipSearchHit[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLDivElement>(null);
  const searchDebounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const pageTitle = titleForPath(location.pathname);

  const refreshUnreadCount = useCallback(() => {
    apiFetch("/api/v1/notifications/unread-count", { headers: authHeaders() })
      .then((res) => {
        if (res.status === 404 || res.status === 401) return null;
        if (!res.ok) return null;
        return res.json() as Promise<{ unread?: number }>;
      })
      .then((data) => {
        if (data && typeof data.unread === "number") {
          setNotifUnread(data.unread);
        }
      })
      .catch(() => setNotifUnread(null));
  }, [authHeaders]);

  useEffect(() => {
    let cancelled = false;
    apiFetch("/api/v1/notifications/unread-count", { headers: authHeaders() })
      .then((res) => {
        if (res.status === 404 || res.status === 401) return null;
        if (!res.ok) return null;
        return res.json() as Promise<{ unread?: number }>;
      })
      .then((data) => {
        if (!cancelled && data && typeof data.unread === "number") {
          setNotifUnread(data.unread);
        }
      })
      .catch(() => {
        if (!cancelled) setNotifUnread(null);
      });
    return () => {
      cancelled = true;
    };
  }, [authHeaders, location.pathname]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      const t = e.target as Node;
      if (menuRef.current && !menuRef.current.contains(t)) {
        setMenuOpen(false);
      }
      if (notifRef.current && !notifRef.current.contains(t)) {
        setNotifOpen(false);
      }
      if (searchRef.current && !searchRef.current.contains(t)) {
        setSearchOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const runSearch = useCallback(
    async (q: string) => {
      const trimmed = q.trim();
      if (!trimmed) {
        setSearchResults([]);
        setSearchLoading(false);
        return;
      }
      setSearchLoading(true);
      try {
        const params = new URLSearchParams();
        params.set("query", trimmed);
        params.set("limit", "8");
        params.set("page", "1");
        const res = await apiFetch(`/api/v1/scholarships/search?${params.toString()}`);
        if (!res.ok) {
          setSearchResults([]);
          return;
        }
        const data = (await res.json()) as ScholarshipSearchApiResponse;
        setSearchResults(Array.isArray(data.results) ? data.results : []);
      } catch {
        setSearchResults([]);
      } finally {
        setSearchLoading(false);
      }
    },
    []
  );

  const onSearchInputChange = (value: string) => {
    setSearchQuery(value);
    setSearchOpen(true);
    if (searchDebounceRef.current) {
      clearTimeout(searchDebounceRef.current);
    }
    if (!value.trim()) {
      setSearchResults([]);
      setSearchLoading(false);
      return;
    }
    setSearchLoading(true);
    searchDebounceRef.current = setTimeout(() => {
      void runSearch(value);
    }, SEARCH_DEBOUNCE_MS);
  };

  useEffect(() => {
    return () => {
      if (searchDebounceRef.current) clearTimeout(searchDebounceRef.current);
    };
  }, []);

  const loadNotifications = useCallback(() => {
    setNotifLoading(true);
    apiFetch("/api/v1/notifications?limit=15", { headers: authHeaders() })
      .then((res) => {
        if (res.status === 404 || res.status === 401) return null;
        if (!res.ok) return null;
        return res.json() as Promise<NotificationItem[]>;
      })
      .then((data) => {
        if (Array.isArray(data)) setNotifItems(data);
        else setNotifItems([]);
      })
      .catch(() => setNotifItems([]))
      .finally(() => setNotifLoading(false));
  }, [authHeaders]);

  const toggleNotif = () => {
    const next = !notifOpen;
    setNotifOpen(next);
    if (next) loadNotifications();
  };

  const markNotificationRead = async (id: number) => {
    try {
      const res = await apiFetch(`/api/v1/notifications/${id}/read`, {
        method: "POST",
        headers: authHeaders(),
      });
      if (res.ok) {
        setNotifItems((prev) => prev.map((n) => (n.id === id ? { ...n, is_read: true } : n)));
        refreshUnreadCount();
      }
    } catch {
      /* ignore */
    }
  };

  const formatNotifTime = (iso: string) => {
    try {
      return new Date(iso).toLocaleString(undefined, { dateStyle: "short", timeStyle: "short" });
    } catch {
      return iso;
    }
  };

  return (
    <header className="sticky top-0 z-20 flex h-16 shrink-0 items-center gap-3 border-b border-slate-200 bg-white/95 px-3 shadow-sm backdrop-blur dark:border-slate-700 dark:bg-slate-800/95 sm:px-4">
      <button
        type="button"
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700 lg:hidden"
        onClick={onOpenMobileSidebar}
        aria-label="Open navigation menu"
      >
        <IconMenu />
      </button>

      <div className="min-w-0 flex-1">
        <p className="truncate text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
          ISKONNECT
        </p>
        <h1 className="truncate text-lg font-semibold text-slate-900 dark:text-slate-100">{pageTitle}</h1>
      </div>

      <div className="relative hidden max-w-md flex-1 sm:block md:max-w-lg lg:max-w-xl" ref={searchRef}>
        <label htmlFor="dashboard-global-search" className="sr-only">
          Search scholarships
        </label>
        <input
          id="dashboard-global-search"
          type="search"
          placeholder="Search scholarships by title…"
          value={searchQuery}
          onChange={(e) => onSearchInputChange(e.target.value)}
          onFocus={() => setSearchOpen(true)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && searchQuery.trim()) {
              e.preventDefault();
              navigate(`/scholarships/search?query=${encodeURIComponent(searchQuery.trim())}`);
              setSearchOpen(false);
              setSearchQuery("");
              setSearchResults([]);
            }
          }}
          className="w-full rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/30 dark:border-slate-600 dark:bg-slate-900/50 dark:text-slate-200 dark:placeholder:text-slate-500"
          autoComplete="off"
        />
        {searchOpen && (searchQuery.trim() || searchLoading || searchResults.length > 0) ? (
          <div
            className="absolute left-0 right-0 top-full z-30 mt-1 max-h-80 overflow-auto rounded-xl border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-600 dark:bg-slate-800"
            role="listbox"
          >
            {searchLoading ? (
              <p className="px-3 py-2 text-sm text-slate-500 dark:text-slate-400">Searching…</p>
            ) : searchQuery.trim() && searchResults.length === 0 ? (
              <p className="px-3 py-2 text-sm text-slate-500 dark:text-slate-400">No results</p>
            ) : (
              searchResults.map((s) => (
                <Link
                  key={s.id}
                  to={`/scholarship/${s.id}`}
                  role="option"
                  className="block px-3 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-700"
                  onClick={() => {
                    setSearchOpen(false);
                    setSearchQuery("");
                    setSearchResults([]);
                  }}
                >
                  <span className="font-medium text-slate-900 dark:text-slate-100">{s.title}</span>
                  {s.provider ? (
                    <span className="mt-0.5 block text-xs text-slate-500 dark:text-slate-400">{s.provider}</span>
                  ) : null}
                </Link>
              ))
            )}
            {searchQuery.trim() ? (
              <div className="border-t border-slate-100 px-3 py-2 dark:border-slate-600">
                <Link
                  to={`/scholarships/search?query=${encodeURIComponent(searchQuery.trim())}`}
                  className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
                  onClick={() => {
                    setSearchOpen(false);
                  }}
                >
                  See all results
                </Link>
              </div>
            ) : null}
          </div>
        ) : null}
      </div>

      <div className="flex shrink-0 items-center gap-1 sm:gap-2">
        <div className="relative" ref={notifRef}>
          <button
            type="button"
            onClick={toggleNotif}
            className="relative flex h-10 w-10 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-slate-100"
            aria-label="Notifications"
            aria-expanded={notifOpen}
          >
            <IconBell />
            {notifUnread != null && notifUnread > 0 ? (
              <span className="absolute right-1 top-1 flex h-4 min-w-[1rem] items-center justify-center rounded-full bg-red-600 px-1 text-[10px] font-bold text-white">
                {notifUnread > 9 ? "9+" : notifUnread}
              </span>
            ) : null}
          </button>
          {notifOpen ? (
            <div className="absolute right-0 z-40 mt-1 w-80 max-w-[calc(100vw-2rem)] rounded-xl border border-slate-200 bg-white shadow-lg dark:border-slate-600 dark:bg-slate-800">
              <div className="border-b border-slate-100 px-3 py-2 dark:border-slate-700">
                <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">Notifications</p>
              </div>
              <div className="max-h-80 overflow-y-auto">
                {notifLoading ? (
                  <p className="px-3 py-4 text-sm text-slate-500">Loading…</p>
                ) : notifItems.length === 0 ? (
                  <p className="px-3 py-4 text-sm text-slate-500 dark:text-slate-400">No notifications yet.</p>
                ) : (
                  notifItems.map((n) => (
                    <button
                      key={n.id}
                      type="button"
                      className={`w-full border-b border-slate-50 px-3 py-2.5 text-left text-sm text-slate-800 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-700/80 ${
                        !n.is_read ? "bg-primary-50/50 dark:bg-primary-950/20" : ""
                      }`}
                      onClick={() => {
                        if (!n.is_read) void markNotificationRead(n.id);
                        if (n.scholarship_id) {
                          navigate(`/scholarship/${n.scholarship_id}`);
                          setNotifOpen(false);
                        }
                      }}
                    >
                      <p className="font-medium">{n.title}</p>
                      {n.body ? <p className="mt-0.5 text-xs text-slate-600 dark:text-slate-400">{n.body}</p> : null}
                      <p className="mt-1 text-[10px] text-slate-400">{formatNotifTime(n.created_at)}</p>
                    </button>
                  ))
                )}
              </div>
            </div>
          ) : null}
        </div>

        <div className="relative" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((o) => !o)}
            className="flex max-w-[12rem] items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 py-1.5 pl-2 pr-2 text-left transition hover:bg-slate-100 dark:border-slate-600 dark:bg-slate-900/40 dark:hover:bg-slate-700"
            aria-expanded={menuOpen}
            aria-haspopup="true"
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-800 dark:bg-primary-900/50 dark:text-primary-200">
              {user?.email?.[0]?.toUpperCase() ?? "?"}
            </span>
            <span className="hidden min-w-0 flex-1 sm:block">
              <span className="block truncate text-xs font-medium text-slate-900 dark:text-slate-100">
                {user?.email ?? "Account"}
              </span>
            </span>
            <IconChevronDown className="shrink-0 text-slate-500" />
          </button>

          {menuOpen ? (
            <div
              className="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-600 dark:bg-slate-800"
              role="menu"
            >
              <div className="border-b border-slate-100 px-3 py-2 dark:border-slate-700">
                <p className="truncate text-xs text-slate-500 dark:text-slate-400">Signed in as</p>
                <p className="truncate text-sm font-medium text-slate-900 dark:text-slate-100">{user?.email}</p>
              </div>
              <Link
                to="/settings"
                className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-700"
                role="menuitem"
                onClick={() => setMenuOpen(false)}
              >
                Account Settings
              </Link>
              <button
                type="button"
                className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-700"
                role="menuitem"
                onClick={() => {
                  setMenuOpen(false);
                  logout();
                  navigate("/");
                }}
              >
                Log out
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </header>
  );
}
