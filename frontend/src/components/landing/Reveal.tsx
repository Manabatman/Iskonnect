import { m, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";
import { MOTION_DURATION_S } from "@/lib/motion";

interface RevealProps {
  children: ReactNode;
  className?: string;
  delay?: number;
}

export function Reveal({ children, className = "", delay = 0 }: RevealProps) {
  const prefersReduced = useReducedMotion();

  return (
    <m.div
      className={className}
      initial={prefersReduced ? false : { opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: MOTION_DURATION_S.reveal, ease: "easeOut", delay }}
    >
      {children}
    </m.div>
  );
}
