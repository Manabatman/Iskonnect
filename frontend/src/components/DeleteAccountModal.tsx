import * as Dialog from "@radix-ui/react-dialog";
import { useState } from "react";
import { apiFetch } from "../api/client";
import { useAuth } from "../contexts/AuthContext";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  userEmail: string;
};

export function DeleteAccountModal({ open, onOpenChange, userEmail }: Props) {
  const { authHeaders, logout } = useAuth();
  const [confirmText, setConfirmText] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canDelete = confirmText.trim().toLowerCase() === "delete";

  const handleDelete = async () => {
    if (!canDelete || deleting) return;
    setDeleting(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/profiles/me", {
        method: "DELETE",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Account deletion failed");
      }
      onOpenChange(false);
      await logout();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Account deletion failed");
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
            Delete your account permanently?
          </Dialog.Title>
          <Dialog.Description className="mt-2 space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <p>
              This permanently removes your profile, match history, saved scholarships, and applications for{" "}
              <strong className="text-slate-900 dark:text-slate-100">{userEmail}</strong>.
            </p>
            <p>
              This cannot be undone and is not reversible. You can create a new account later, but your previous data
              will not be restored.
            </p>
            <p>Type <strong>delete</strong> to confirm.</p>
          </Dialog.Description>
          <input
            type="text"
            value={confirmText}
            onChange={(e) => setConfirmText(e.target.value)}
            placeholder="delete"
            className="mt-4 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
            autoComplete="off"
          />
          {error ? <p className="mt-2 text-sm text-danger-600 dark:text-danger-400">{error}</p> : null}
          <div className="mt-6 flex flex-col gap-2 sm:flex-row sm:justify-end">
            <Dialog.Close
              type="button"
              disabled={deleting}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Cancel
            </Dialog.Close>
            <button
              type="button"
              onClick={() => void handleDelete()}
              disabled={!canDelete || deleting}
              className="rounded-lg bg-danger-600 px-4 py-2 text-sm font-semibold text-white hover:bg-danger-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {deleting ? "Deleting…" : "Delete my account"}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
