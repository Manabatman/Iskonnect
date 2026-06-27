import { LazyMotion, domAnimation } from "framer-motion";
import type { ReactNode } from "react";

export function LandingMotionProvider({ children }: { children: ReactNode }) {
  return <LazyMotion features={domAnimation}>{children}</LazyMotion>;
}
