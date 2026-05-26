"use client";

import { useEffect } from "react";

/**
 * Wires the two click-to-collapse levels by event delegation (renders nothing).
 *
 * - Clicking a subsection `h4` toggles `.collapsed` on its `.subsection`.
 * - Clicking a `.pillar-header` toggles `.body-collapsed` on its `.pillar`.
 *
 * Links inside the header (the subsection name) call stopPropagation, so
 * navigating to the study page does not also collapse. Global expand/collapse
 * lives in FilterBar and mutates `.subsection` classes directly.
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
        return;
      }

      const header = target.closest(".pillar-header");
      if (header) {
        header.closest(".pillar")?.classList.toggle("body-collapsed");
      }
    };

    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  return null;
}
