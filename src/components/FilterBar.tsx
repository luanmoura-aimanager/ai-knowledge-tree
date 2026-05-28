"use client";

import { useEffect, useState } from "react";

type Filter = "all" | "covered" | "partial" | "gap" | "hot" | "hot-gap";

/**
 * Sticky filter bar. Mutates the DOM directly (toggles a `hidden` class on
 * `.topic` elements based on their data-* attributes) instead of re-rendering
 * React. This keeps the heavy server-rendered topic grid intact and the
 * interaction snappy.
 */
export function FilterBar() {
  const [filter, setFilter] = useState<Filter>("all");
  const [query, setQuery] = useState("");

  useEffect(() => {
    const q = query.toLowerCase().trim();
    const topics = document.querySelectorAll<HTMLElement>(".topic");
    topics.forEach((el) => {
      const status = el.dataset.status as "covered" | "partial" | "gap";
      const hot = el.dataset.hot === "true";
      const name = el.dataset.name ?? "";
      let show = true;
      switch (filter) {
        case "covered":
          show = status === "covered";
          break;
        case "partial":
          show = status === "partial";
          break;
        case "gap":
          show = status === "gap";
          break;
        case "hot":
          show = hot;
          break;
        case "hot-gap":
          show = hot && status === "gap";
          break;
      }
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
    });
  }, [filter, query]);

  const filters: { id: Filter; label: string }[] = [
    { id: "all", label: "All" },
    { id: "covered", label: "✓ Covered" },
    { id: "partial", label: "◐ Partial" },
    { id: "gap", label: "○ Gaps" },
    { id: "hot", label: "★ Hot" },
    { id: "hot-gap", label: "🎯 Hot gaps" },
  ];

  const setAllCollapsed = (collapsed: boolean) => {
    document
      .querySelectorAll<HTMLElement>(".subsection")
      .forEach((s) => s.classList.toggle("collapsed", collapsed));
  };

  return (
    <div className="sticky top-14 z-10 bg-[var(--bg)]/90 backdrop-blur-md border-b border-[var(--border)] py-3 my-2">
      <div className="max-w-[1280px] mx-auto px-6 flex gap-3 items-center flex-wrap">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="🔍 Search topic (e.g. diffusion, kalman, RAG)..."
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
