"use client";

import { useEffect, useState } from "react";

type Filter =
  | "all"
  | "studied"
  | "in-progress"
  | "unstudied"
  | "available"
  | "coming-soon";

/**
 * Sticky filter bar over the lesson grid. Mutates the DOM directly (toggles a
 * `hidden` class on `.topic` lesson rows based on their `data-status` /
 * `data-name`) instead of re-rendering React, keeping the server-rendered grid
 * intact and interactions snappy. Signed-in users filter by study state;
 * anonymous visitors by lesson availability.
 */
export function FilterBar({ signedIn = false }: { signedIn?: boolean }) {
  const [filter, setFilter] = useState<Filter>("all");
  const [query, setQuery] = useState("");

  useEffect(() => {
    const q = query.toLowerCase().trim();
    const filtering = filter !== "all" || q !== "";
    const topics = document.querySelectorAll<HTMLElement>(".topic");
    topics.forEach((el) => {
      const status = el.dataset.status ?? "";
      const name = el.dataset.name ?? "";
      let show = filter === "all" || status === filter;
      if (show && q && !name.includes(q)) show = false;
      el.classList.toggle("hidden", !show);
    });
    document.querySelectorAll<HTMLElement>(".subsection").forEach((s) => {
      const v = s.querySelectorAll(".topic:not(.hidden)").length;
      s.classList.toggle("hidden", v === 0);
    });
    document.querySelectorAll<HTMLElement>(".pillar").forEach((p) => {
      const v = p.querySelectorAll(".subsection:not(.hidden)").length;
      p.classList.toggle("opacity-25", v === 0);
      // Pillars are collapsed by default. While filtering, open the ones with
      // matches (and collapse the rest) so results stay visible; when the
      // filter clears, snap every pillar back to the collapsed default.
      p.classList.toggle("body-collapsed", filtering ? v === 0 : true);
    });
  }, [filter, query]);

  const filters: { id: Filter; label: string }[] = signedIn
    ? [
        { id: "all", label: "All" },
        { id: "studied", label: "✓ Studied" },
        { id: "in-progress", label: "◐ In progress" },
        { id: "unstudied", label: "○ Not started" },
      ]
    : [
        { id: "all", label: "All" },
        { id: "available", label: "Available" },
        { id: "coming-soon", label: "Coming soon" },
      ];

  const setAllCollapsed = (collapsed: boolean) => {
    document
      .querySelectorAll<HTMLElement>(".pillar")
      .forEach((p) => p.classList.toggle("body-collapsed", collapsed));
    // Expanding a pillar should reveal everything inside it, so also clear any
    // per-subsection collapse left over from manual h4 toggles.
    if (!collapsed) {
      document
        .querySelectorAll<HTMLElement>(".subsection")
        .forEach((s) => s.classList.remove("collapsed"));
    }
  };

  return (
    <div className="bg-[var(--bg)] border-b border-[var(--border)] py-3">
      <div className="max-w-[1280px] mx-auto px-6 flex gap-3 items-center flex-wrap">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="🔍 Search lessons (e.g. diffusion, kalman, RAG)..."
          className="flex-1 min-w-[200px] bg-[var(--card)] border border-[var(--border)] rounded-lg px-3.5 py-2 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
        />
        <div className="flex gap-1.5 flex-wrap">
          {filters.map((f) => (
            <button
              key={f.id}
              className={`btn ${filter === f.id ? "active" : ""}`}
              onClick={() => setFilter(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>
        <div className="flex gap-1.5 ml-auto">
          <button className="btn" onClick={() => setAllCollapsed(false)}>
            ▾ Expand all
          </button>
          <button className="btn" onClick={() => setAllCollapsed(true)}>
            ▸ Collapse all
          </button>
        </div>
      </div>
    </div>
  );
}
