import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn, MIN_TOUCH_TARGET_CLASS } from "@/lib/utils";

const buttonVariants = cva(
  "focus-visible-ring inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold ring-offset-background transition-colors active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary-600 text-white shadow-lg shadow-primary-600/25 hover:bg-primary-700",
        destructive: "bg-danger-600 text-white hover:bg-danger-700",
        outline:
          "border border-border bg-background text-foreground shadow-sm hover:bg-muted",
        secondary: "bg-muted text-foreground hover:bg-muted/80",
        ghost: "hover:bg-muted hover:text-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: `h-11 px-4 py-2 ${MIN_TOUCH_TARGET_CLASS}`,
        sm: "h-9 rounded-md px-3",
        lg: `h-12 rounded-md px-8 ${MIN_TOUCH_TARGET_CLASS}`,
        xl: `h-12 rounded-xl px-8 text-base ${MIN_TOUCH_TARGET_CLASS}`,
        icon: `size-11 ${MIN_TOUCH_TARGET_CLASS}`,
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
