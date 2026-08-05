import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onGoToConsent: () => void;
};

export function ConsentRequiredModal({ open, onOpenChange, onGoToConsent }: Props) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Privacy consent required</DialogTitle>
          <DialogDescription>
            Please confirm the Data Privacy Act (RA 10173) consent checkbox on the Eligibility step before saving your
            profile to your account.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="gap-2 sm:gap-0">
          <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            type="button"
            onClick={() => {
              onOpenChange(false);
              onGoToConsent();
            }}
          >
            Go to consent checkbox
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
