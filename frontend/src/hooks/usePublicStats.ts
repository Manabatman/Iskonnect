import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export type PublicStats = {
  source: "live" | "fallback";
  verified_listing_count?: number | null;
  provider_count?: number | null;
  last_catalog_verification_at?: string | null;
  region_count?: number | null;
  education_level_count?: number | null;
};

export function usePublicStats() {
  const [stats, setStats] = useState<PublicStats | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await apiFetch("/api/v1/public/stats");
        if (!res.ok || cancelled) return;
        setStats((await res.json()) as PublicStats);
      } catch {
        /* public page renders without live stats */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return stats;
}
