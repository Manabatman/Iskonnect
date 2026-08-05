import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const chipVariants = cva(
  "inline-flex items-center rounded-full border border-border bg-background font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary/10 text-primary",
        secondary: "border-border bg-muted text-foreground",
        success: "border-tone-success bg-tone-success text-tone-success",
        warning: "border-tone-warning bg-tone-warning text-tone-warning",
        danger: "border-tone-danger bg-tone-danger text-tone-danger",
        info: "border-tone-info bg-tone-info text-tone-info",
        neutral: "border-tone-neutral bg-tone-neutral text-tone-neutral",
      },
      size: {
        sm: "px-2 py-0.5 text-[11px]",
        md: "px-3 py-0.5 text-xs font-semibold",
        lg: "px-4 py-1.5 text-sm font-medium",
      },
    },
    defaultVariants: {
      variant: "neutral",
      size: "md",
    },
  }
);

export interface ChipProps extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof chipVariants> {}

function Chip({ className, variant, size, ...props }: ChipProps) {
  return <span className={cn(chipVariants({ variant, size }), className)} {...props} />;
}

export { Chip, chipVariants };
