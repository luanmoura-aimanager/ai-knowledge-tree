"use client";

import { useEffect } from "react";

/**
 * Wires the per-discipline collapse by event delegation (renders nothing).
 *
 * Clicking a subsection `h4` (in the open pillar detail panel) toggles
 * `.collapsed` on its `.subsection`, hiding that discipline's lesson list.
 *
 * Links inside the header (the subsection name) call stopPropagation, so
 * navigating to the study page does not also collapse.
 */
export function CollapseController() {
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;

      // Let links (e.g. the subsection name → study page) navigate normally.
      if (target.closest("a")) return;

      const h4 = target.closest(".subsection h4");
      if (h4) {
        h4.closest(".subsection")?.classList.toggle("collapsed");
      }
    };

    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  return null;
}
