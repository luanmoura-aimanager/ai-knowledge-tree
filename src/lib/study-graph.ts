import type { SubProgress } from "@/lib/curriculum";

/**
 * Pure logic behind ConnectionsGraph's zoom buttons and Studied view, kept out of
 * the component so it can be tested without a DOM.
 */

export type StudyMap = Record<string, SubProgress>;
export type ZoomLimit = "min" | "max" | null;

export const MAX_ZOOM = 5;

// Button steps multiply the scale, so zooming back out can land on
// 1.0000000000000002 rather than exactly 1.
const ZOOM_EPSILON = 1e-6;

/** Which end of the zoom range `k` sits at, if any. */
export function zoomLimitAt(k: number): ZoomLimit {
  if (k <= 1 + ZOOM_EPSILON) return "min";
  return k >= MAX_ZOOM - ZOOM_EPSILON ? "max" : null;
}

/** Share of a subsection done; an in-progress lesson counts for half. */
export function studyFraction(p: SubProgress | undefined): number {
  if (!p || p.total === 0) return 0;
  return (p.studied + 0.5 * p.inProgress) / p.total;
}

/** 0% keeps the dimmed look; the floor keeps a first lesson visibly distinct. */
export function studyOpacity(fraction: number): string {
  return fraction === 0 ? "var(--dim-opacity)" : String(0.38 + 0.62 * fraction);
}
