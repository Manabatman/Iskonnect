import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { NetworkError, apiFetch } from "../api/client";
import { useAuth } from "./AuthContext";
import type { SavedScholarship } from "../types";

export const SAVED_SCHOLARSHIP_CHANGED_EVENT = "iskonnect:saved-scholarship-changed";

export type SavedScholarshipChangedDetail = {
  scholarshipId: number;
  saved: boolean;
};

interface SavedScholarshipsContextType {
  savedIds: Set<number>;
  /** Full saved rows (same shape as GET /saved-scholarships) for dashboard and applications. */
  savedScholarships: SavedScholarship[];
  isSaved: (id: number) => boolean;
  toggleSave: (id: number) => Promise<boolean>;
  loading: boolean;
  /** True while loading the full saved list (GET /saved-scholarships). */
  savedListLoading: boolean;
  error: string | null;
  clearError: () => void;
  refresh: () => Promise<void>;
}

const SavedScholarshipsContext = createContext<SavedScholarshipsContextType | null>(null);

export function SavedScholarshipsProvider({ children }: { children: ReactNode }) {
  const { token: authToken, user } = useAuth();
  const [savedIds, setSavedIds] = useState<Set<number>>(new Set());
  const [savedScholarships, setSavedScholarships] = useState<SavedScholarship[]>([]);
  const [loading, setLoading] = useState(false);
  const [savedListLoading, setSavedListLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => setError(null), []);

  const fetchSaved = useCallback(async () => {
    if (!authToken) {
      setSavedIds(new Set());
      setSavedScholarships([]);
      setError(null);
      return;
    }
    setLoading(true);
    setSavedListLoading(true);
    try {
      const res = await apiFetch("/api/v1/saved-scholarships", {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (res.ok) {
        const data = (await res.json()) as { saved?: SavedScholarship[] };
        const list = Array.isArray(data.saved) ? data.saved : [];
        setSavedScholarships(list);
        setSavedIds(new Set(list.map((s) => s.scholarship_id)));
        setError(null);
      } else {
        setError(`Could not load saved scholarships (${res.status}).`);
      }
    } catch (e) {
      const msg =
        e instanceof NetworkError
          ? "Server unreachable — saved list may be out of date."
          : e instanceof Error
            ? e.message
            : "Failed to load saved scholarships.";
      setError(msg);
    } finally {
      setLoading(false);
      setSavedListLoading(false);
    }
  }, [authToken]);

  useEffect(() => {
    void fetchSaved();
  }, [fetchSaved, user?.id]);

  const isSaved = useCallback((id: number) => savedIds.has(id), [savedIds]);

  const toggleSave = useCallback(
    async (id: number): Promise<boolean> => {
      if (!authToken) return false;
      const currentlySaved = savedIds.has(id);
      setSavedIds((prev) => {
        const next = new Set(prev);
        if (currentlySaved) next.delete(id);
        else next.add(id);
        return next;
      });
      try {
        if (currentlySaved) {
          const res = await apiFetch(`/api/v1/saved-scholarships/${id}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${authToken}` },
          });
          if (!res.ok) throw new Error("Failed to unsave");
          setSavedScholarships((prev) => prev.filter((s) => s.scholarship_id !== id));
          window.dispatchEvent(
            new CustomEvent<SavedScholarshipChangedDetail>(SAVED_SCHOLARSHIP_CHANGED_EVENT, {
              detail: { scholarshipId: id, saved: false },
            })
          );
          return false;
        } else {
          const res = await apiFetch("/api/v1/saved-scholarships", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${authToken}`,
            },
            body: JSON.stringify({ scholarship_id: id }),
          });
          if (!res.ok) {
            const data = await res.json().catch(() => null);
            if (res.status === 409) {
              await fetchSaved();
              return true;
            }
            throw new Error(data?.detail ?? "Failed to save");
          }
          const row = (await res.json()) as SavedScholarship;
          setSavedScholarships((prev) => [row, ...prev.filter((s) => s.scholarship_id !== id)]);
          window.dispatchEvent(
            new CustomEvent<SavedScholarshipChangedDetail>(SAVED_SCHOLARSHIP_CHANGED_EVENT, {
              detail: { scholarshipId: id, saved: true },
            })
          );
          return true;
        }
      } catch {
        setSavedIds((prev) => {
          const next = new Set(prev);
          if (currentlySaved) next.add(id);
          else next.delete(id);
          return next;
        });
        void fetchSaved();
        return currentlySaved;
      }
    },
    [authToken, savedIds, fetchSaved]
  );

  return (
    <SavedScholarshipsContext.Provider
      value={{
        savedIds,
        savedScholarships,
        isSaved,
        toggleSave,
        loading,
        savedListLoading,
        error,
        clearError,
        refresh: fetchSaved,
      }}
    >
      {children}
    </SavedScholarshipsContext.Provider>
  );
}

export function useSavedScholarships() {
  const ctx = useContext(SavedScholarshipsContext);
  if (!ctx) throw new Error("useSavedScholarships must be used within SavedScholarshipsProvider");
  return ctx;
}
