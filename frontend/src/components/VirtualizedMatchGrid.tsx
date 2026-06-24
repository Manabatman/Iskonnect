import { useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import type { MatchResult } from "../types";
import { ScholarshipCardV2 } from "./ScholarshipCardV2";
import { ErrorBoundary } from "./ErrorBoundary";

export interface VirtualizedMatchGridProps {
  matches: MatchResult[];
  onShowAnalysis?: (match: MatchResult) => void;
  /** Estimated card height in px for the virtualizer (responsive grids). */
  estimateSize?: number;
}

/**
 * Windowed scholarship match grid to limit DOM nodes on low-memory mobile devices.
 */
export function VirtualizedMatchGrid({
  matches,
  onShowAnalysis,
  estimateSize = 320,
}: VirtualizedMatchGridProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: matches.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimateSize,
    overscan: 4,
  });

  if (matches.length === 0) {
    return null;
  }

  return (
    <div ref={parentRef} className="max-h-[70vh] overflow-y-auto pr-1">
      <div
        style={{
          height: `${rowVirtualizer.getTotalSize()}px`,
          width: "100%",
          position: "relative",
        }}
      >
        {rowVirtualizer.getVirtualItems().map((virtualRow) => {
          const match = matches[virtualRow.index];
          return (
            <div
              key={match.id}
              data-index={virtualRow.index}
              ref={rowVirtualizer.measureElement}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                transform: `translateY(${virtualRow.start}px)`,
              }}
              className="pb-6"
            >
              <ErrorBoundary>
                <ScholarshipCardV2 scholarship={match} onShowAnalysis={onShowAnalysis} />
              </ErrorBoundary>
            </div>
          );
        })}
      </div>
    </div>
  );
}
