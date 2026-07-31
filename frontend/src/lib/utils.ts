import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** MOB-02 — minimum interactive target (44×44 CSS px). */
export const MIN_TOUCH_TARGET_CLASS = "min-h-11 min-w-11";
