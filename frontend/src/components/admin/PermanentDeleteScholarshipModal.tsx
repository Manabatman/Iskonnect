import * as Dialog from "@radix-ui/react-dialog";
import { useState } from "react";
import { apiFetch } from "../../api/client";

export type PermanentDeleteScholarshipModalProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  scholarship: { id: number; title: string; is_active?: boolean | null } | null;
  authHeaders: () => HeadersInit;
  onDeleted: () => void;
};

export function PermanentDeleteScholarshipModal({
  open,
  onOpenChange,
  scholarship,
  authHeaders,
  onDeleted,
}: PermanentDeleteScholarshipModalProps) {
  const [confirmText, setConfirmText] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inactive = scholarship?.is_active === false;
  const canDelete = confirmText.trim().toUpperCase() === "DELETE" && inactive;

  const handleDelete = async () => {
    if (!scholarship || !canDelete || deleting) return;
    setDeleting(true);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/admin/scholarships/${scholarship.id}/permanent`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Permanent delete failed");
      }
      onOpenChange(false);
      onDeleted();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Permanent delete failed");
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Dialog.Root
      open={open}
      onOpenChange={(next) => {
        if (!deleting) {
          onOpenChange(next);
          if (!next) {
            setConfirmText("");
            setError(null);
          }
        }
      }}
    >
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm" />
        <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-[min(100%-2rem,28rem)] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-danger-200 bg-white p-6 shadow-xl dark:border-danger-900/50 dark:bg-slate-900">
          <Dialog.Title className="text-lg font-semibold text-danger-700 dark:text-danger-400">
            Delete scholarship permanently?
          </Dialog.Title>
          <Dialog.Description asChild>
            <div className="mt-2 space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <p>
                <strong className="text-slate-900 dark:text-slate-100">{scholarship?.title ?? "—"}</strong>
              </p>
              <p>
                This scholarship will be permanently removed from the catalog, including match history references and
                saved bookmarks for all users.
              </p>
              <p className="font-medium text-danger-700 dark:text-danger-400">This action cannot be undone.</p>
              {!inactive ? (
                <p className="text-amber-700 dark:text-amber-300">
                  Deactivate this scholarship before permanent deletion.
                </p>
              ) : (
                <p>
                  Type <strong>DELETE</strong> to confirm.
                </p>
              )}
            </div>
          </Dialog.Description>
          {inactive ? (
            <input
              type="text"
              value={confirmText}
              onChange={(e) => setConfirmText(e.target.value)}
              placeholder="DELETE"
              className="mt-4 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
              autoComplete="off"
            />
          ) : null}
          {error ? <p className="mt-2 text-sm text-danger-600 dark:text-danger-400">{error}</p> : null}
          <div className="mt-6 flex flex-col gap-2 sm:flex-row sm:justify-end">
            <Dialog.Close
              type="button"
              disabled={deleting}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium dark:border-slate-600"
            >
              Cancel
            </Dialog.Close>
            <button
              type="button"
              disabled={!canDelete || deleting}
              onClick={() => void handleDelete()}
              className="rounded-lg bg-danger-600 px-4 py-2 text-sm font-semibold text-white hover:bg-danger-700 disabled:opacity-50"
            >
              {deleting ? "Deleting…" : "Delete permanently"}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
