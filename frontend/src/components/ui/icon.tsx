import { type LucideIcon, type LucideProps } from "lucide-react";
import { cn } from "@/lib/utils";

/** DS-12 — normalized icon sizes (16 / 20 / 24). */
export const iconSizes = {
  sm: "size-4",
  md: "size-5",
  lg: "size-6",
} as const;

export type IconSize = keyof typeof iconSizes;

export interface IconProps extends LucideProps {
  icon: LucideIcon;
  size?: IconSize;
}

export function Icon({ icon: IconComponent, size = "md", className, ...props }: IconProps) {
  return <IconComponent className={cn(iconSizes[size], "shrink-0", className)} aria-hidden {...props} />;
}
