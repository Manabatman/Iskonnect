import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { CheckCircle2 } from "lucide-react";

interface SuccessModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description: string;
  actionLabel?: string;
  onAction: () => void;
}

export function SuccessModal({
  open,
  onOpenChange,
  title,
  description,
  actionLabel = "Continue",
  onAction,
}: SuccessModalProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass max-w-md border-border">
        <DialogHeader className="items-center text-center sm:items-center sm:text-center">
          <div className="mb-2 flex h-14 w-14 items-center justify-center rounded-full bg-tone-success">
            <CheckCircle2 className="h-8 w-8 text-tone-success" aria-hidden />
          </div>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter className="sm:justify-center">
          <Button type="button" onClick={onAction} className="w-full sm:w-auto">
            {actionLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
