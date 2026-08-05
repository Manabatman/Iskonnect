import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** When set, wires aria-invalid and aria-describedby to `{id}-error`. */
  error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, id, "aria-describedby": ariaDescribedBy, ...props }, ref) => {
    const errorId = error && id ? `${id}-error` : undefined;
    const describedBy =
      [ariaDescribedBy, errorId].filter(Boolean).join(" ") || undefined;

    return (
      <input
        type={type}
        id={id}
        className={cn(
          "focus-visible-ring flex h-11 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          error && "border-tone-danger",
          className
        )}
        ref={ref}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input };
