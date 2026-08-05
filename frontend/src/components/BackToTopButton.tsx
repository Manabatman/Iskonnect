import { useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const SCROLL_THRESHOLD = 600;

export function BackToTopButton() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > SCROLL_THRESHOLD);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <Button
      type="button"
      variant="default"
      size="icon"
      aria-label="Back to top"
      onClick={scrollToTop}
      className={cn(
        "fixed right-4 z-40 rounded-full shadow-lg transition-all duration-base",
        "bottom-[calc(var(--bottom-nav-offset)+var(--safe-area-bottom)+4.75rem)] lg:bottom-[calc(1.5rem+3.5rem)]",
        visible ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0"
      )}
    >
      <ArrowUp className="size-5" aria-hidden />
    </Button>
  );
}
