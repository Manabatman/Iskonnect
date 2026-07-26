import { Link } from "react-router-dom";
import { apiFetch } from "../../api/client";

export type DuplicatePair = {
  id_a: number;
  id_b: number;
  title_a: string;
  title_b: string;
  provider_a?: string | null;
  provider_b?: string | null;
  link_a?: string | null;
  link_b?: string | null;
  confidence: number;
  match_reason: string;
  is_active_a?: boolean | null;
  is_active_b?: boolean | null;
};

type Props = {
  pairs: DuplicatePair[];
  dismissed: Set<string>;
  authHeaders: () => HeadersInit;
  onDismiss: (key: string) => void;
  onResolved: () => void;
  onError: (message: string) => void;
};

function pairKey(a: number, b: number) {
  return `${Math.min(a, b)}-${Math.max(a, b)}`;
}

export function DuplicateCandidatesPanel({
  pairs,
  dismissed,
  authHeaders,
  onDismiss,
  onResolved,
  onError,
}: Props) {
  const visible = pairs.filter((p) => !dismissed.has(pairKey(p.id_a, p.id_b)));

  const mergeAndDelete = async (canonicalId: number, duplicateId: number) => {
    const res = await apiFetch("/api/v1/admin/scholarships/merge-and-delete", {
      method: "POST",
      headers: { ...authHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({ canonical_id: canonicalId, duplicate_id: duplicateId }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => null);
      throw new Error(data?.detail ?? "Merge and delete failed");
    }
    onResolved();
  };

  if (visible.length === 0) {
    return <p className="text-slate-600 dark:text-slate-400">No potential duplicates in this view.</p>;
  }

  return (
    <div className="space-y-3">
      {visible.map((p) => {
        const key = pairKey(p.id_a, p.id_b);
        return (
          <div key={key} className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                {p.match_reason.replace(/_/g, " ")} · {(p.confidence * 100).toFixed(0)}% match
              </span>
              <button
                type="button"
                className="text-xs text-slate-500 hover:underline"
                onClick={() => onDismiss(key)}
              >
                Dismiss
              </button>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {[ 
                { id: p.id_a, title: p.title_a, provider: p.provider_a, active: p.is_active_a },
                { id: p.id_b, title: p.title_b, provider: p.provider_b, active: p.is_active_b },
              ].map((row) => (
                <div key={row.id} className="rounded border border-slate-100 p-2 dark:border-slate-700">
                  <p className="font-medium text-slate-900 dark:text-slate-100">{row.title}</p>
                  <p className="text-xs text-slate-500">
                    #{row.id} · {row.provider ?? "—"} · {row.active === false ? "inactive" : "active"}
                  </p>
                  <Link to={`/scholarship/${row.id}`} className="text-xs text-primary-600 hover:underline">
                    View
                  </Link>
                </div>
              ))}
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              <button
                type="button"
                className="rounded bg-primary-600 px-2 py-1 text-xs font-medium text-white hover:bg-primary-700"
                onClick={() =>
                  void mergeAndDelete(p.id_a, p.id_b)
                    .then(() => onDismiss(key))
                    .catch((e) => onError(e instanceof Error ? e.message : "Error"))
                }
              >
                Keep #{p.id_a}, delete #{p.id_b}
              </button>
              <button
                type="button"
                className="rounded border border-primary-300 px-2 py-1 text-xs font-medium text-primary-700 hover:bg-primary-50 dark:border-primary-800 dark:text-primary-300"
                onClick={() =>
                  void mergeAndDelete(p.id_b, p.id_a)
                    .then(() => onDismiss(key))
                    .catch((e) => onError(e instanceof Error ? e.message : "Error"))
                }
              >
                Keep #{p.id_b}, delete #{p.id_a}
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
