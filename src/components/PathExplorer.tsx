"use client";

import { useState } from "react";
import Link from "next/link";

/** Per-pillar chip in a path: an ordered subsection with its rolled-up state. */
export interface PathChip {
  id: string;
  name: string;
  letter: string;
  color: string;
  state: "done" | "in-progress" | "untouched";
}

/** A fully-computed path view-model handed down from the server component. */
export interface PathView {
  name: string;
  desc: string;
  color: string;
  studied: number;
  total: number;
  pctStudied: number;
  pctProgress: number;
  pctGap: number;
  chips: PathChip[];
}

/**
 * Client island for the suggested-paths section. The paths render as a grid of
 * small title-only cards; clicking one highlights it and opens a big horizontal
 * detail card (description, pillar squares, progress bar) below the grid.
 */
export function PathExplorer({ paths }: { paths: PathView[] }) {
  const [selected, setSelected] = useState(0);
  const active = selected >= 0 ? paths[selected] : null;

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {paths.map((path, i) => {
          const isActive = i === selected;
          return (
            <button
              key={path.name}
              type="button"
              onClick={() => setSelected(isActive ? -1 : i)}
              aria-pressed={isActive}
              className={`card p-4 text-left flex items-center min-h-[64px] transition-all cursor-pointer ${
                isActive ? "" : "hover:-translate-y-0.5"
              }`}
              style={{
                borderTopColor: path.color,
                borderTopWidth: 3,
                ...(isActive
                  ? {
                      outline: `2px solid ${path.color}`,
                      outlineOffset: 2,
                      boxShadow: `0 0 18px color-mix(in srgb, ${path.color} 35%, transparent)`,
                    }
                  : {}),
              }}
            >
              <h3 className="m-0 text-sm font-bold leading-snug">
                {path.name}
              </h3>
            </button>
          );
        })}
      </div>

      {active && <PathDetail path={active} onClose={() => setSelected(-1)} />}
    </div>
  );
}

function PathDetail({
  path,
  onClose,
}: {
  path: PathView;
  onClose: () => void;
}) {
  return (
    <div
      className="conn-panel card p-6"
      style={{ ["--panel-color" as never]: path.color }}
    >
      <div className="flex items-start justify-between gap-4 mb-4">
        <h3 className="m-0 text-xl font-bold leading-snug">{path.name}</h3>
        <button onClick={onClose} className="btn shrink-0" aria-label="close">
          ✕
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
            About this path
          </h4>
          <p className="m-0 text-sm text-[var(--fg)] leading-relaxed">
            {path.desc}
          </p>
        </div>

        <div>
          <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
            Subsections ({path.chips.length})
          </h4>
          <div className="flex gap-1.5 flex-wrap">
            {path.chips.map((chip) => {
              const base =
                "font-mono text-xs px-1.5 py-0.5 rounded no-underline transition-colors";
              return (
                <Link
                  key={chip.id}
                  href={`/pillar/${chip.letter}/${chip.id}`}
                  title={`${chip.id} · ${chip.name}`}
                  className={
                    chip.state === "done"
                      ? `${base} font-semibold hover:opacity-85`
                      : chip.state === "in-progress"
                        ? `${base} text-[var(--fg)] hover:opacity-85`
                        : `${base} bg-[var(--card-2)] text-[var(--fg-dim)] hover:text-[var(--fg)]`
                  }
                  style={
                    chip.state === "done"
                      ? { background: chip.color, color: "var(--bg)" }
                      : chip.state === "in-progress"
                        ? {
                            background: `color-mix(in srgb, ${chip.color} 22%, transparent)`,
                          }
                        : undefined
                  }
                >
                  {chip.id}
                </Link>
              );
            })}
          </div>
        </div>
      </div>

      <div className="mt-6">
        <div className="text-xs text-[var(--fg-mute)] mb-1">
          {path.studied}/{path.total} studied
        </div>
        <div className="statbar">
          <div className="seg cov" style={{ width: `${path.pctStudied}%` }} />
          <div className="seg par" style={{ width: `${path.pctProgress}%` }} />
          <div className="seg gap" style={{ width: `${path.pctGap}%` }} />
        </div>
      </div>
    </div>
  );
}
