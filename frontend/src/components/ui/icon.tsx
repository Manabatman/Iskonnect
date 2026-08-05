import { type LucideIcon, type LucideProps } from "lucide-react";
import { cn } from "@/lib/utils";

/** DS-12 — normalized icon sizes (16 / 20 / 24). */
export const iconSizes = {
  sm: "size-4",
  md: "size-5",
  lg: "size-6",
} as const;

/** Stroke width per size — 1.5 at 16px, 2 at 20px+. */
export const iconStrokeWidths = {
  sm: 1.5,
  md: 2,
  lg: 2,
} as const;

export type IconSize = keyof typeof iconSizes;

export interface IconProps extends Omit<LucideProps, "ref"> {
  icon: LucideIcon;
  size?: IconSize;
}

export function Icon({ icon: IconComponent, size = "md", className, strokeWidth, ...props }: IconProps) {
  return (
    <IconComponent
      className={cn(iconSizes[size], "shrink-0", className)}
      strokeWidth={strokeWidth ?? iconStrokeWidths[size]}
      aria-hidden
      {...props}
    />
  );
}
