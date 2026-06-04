"use client";

import { createContext, useContext, useState, type ReactNode } from "react";

/**
 * Shares the "currently highlighted path" between the suggested-paths section
 * (PathExplorer, the publisher) and the connections graph (ConnectionsGraph,
 * the subscriber), which are otherwise independent client islands. `active`
 * holds the ordered subsection ids of the selected path plus its color (used to
 * tint the route overlay drawn between consecutive nodes), or null when no path
 * is selected.
 *
 * The context is optional: components call `usePathHighlight()` and tolerate a
 * null result, so ConnectionsGraph still works standalone (e.g. /connections)
 * outside any provider.
 */
export interface ActivePath {
  /** Ordered subsection ids the path traverses. */
  ids: string[];
  /** CSS color used to tint the highlighted nodes' route. */
  color: string;
}

interface PathHighlightValue {
  active: ActivePath | null;
  setActive: (active: ActivePath | null) => void;
}

const PathHighlightContext = createContext<PathHighlightValue | null>(null);

export function PathHighlightProvider({ children }: { children: ReactNode }) {
  const [active, setActive] = useState<ActivePath | null>(null);
  return (
    <PathHighlightContext.Provider value={{ active, setActive }}>
      {children}
    </PathHighlightContext.Provider>
  );
}

export function usePathHighlight(): PathHighlightValue | null {
  return useContext(PathHighlightContext);
}
