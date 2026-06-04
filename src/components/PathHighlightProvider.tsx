"use client";

import { createContext, useContext, useState, type ReactNode } from "react";

/**
 * Shares the "currently highlighted path" between the suggested-paths section
 * (PathExplorer, the publisher) and the connections graph (ConnectionsGraph,
 * the subscriber), which are otherwise independent client islands. `activeIds`
 * is the ordered list of subsection ids belonging to the selected path, or an
 * empty array when no path is selected.
 *
 * The context is optional: components call `usePathHighlight()` and tolerate a
 * null result, so ConnectionsGraph still works standalone (e.g. /connections)
 * outside any provider.
 */
interface PathHighlightValue {
  activeIds: string[];
  setActiveIds: (ids: string[]) => void;
}

const PathHighlightContext = createContext<PathHighlightValue | null>(null);

export function PathHighlightProvider({ children }: { children: ReactNode }) {
  const [activeIds, setActiveIds] = useState<string[]>([]);
  return (
    <PathHighlightContext.Provider value={{ activeIds, setActiveIds }}>
      {children}
    </PathHighlightContext.Provider>
  );
}

export function usePathHighlight(): PathHighlightValue | null {
  return useContext(PathHighlightContext);
}
