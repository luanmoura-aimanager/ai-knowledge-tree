"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

/** Rolled-up study state shared by pillars, subsections and lessons. */
type RollupState = "done" | "in-progress" | "untouched";

/** Visual mapping for a rolled-up study state (matches the .statbar palette). */
const STATE_COLOR: Record<RollupState, string> = {
  done: "var(--good)",
  "in-progress": "var(--partial)",
  untouched: "var(--fg-mute)",
};
const STATE_GLYPH: Record<RollupState, string> = {
  done: "✓",
  "in-progress": "◐",
  untouched: "○",
};

/** One lesson row inside a discipline (carries the FilterBar `data-*` keys). */
export interface PillarLessonView {
  id: string;
  title: string;
  available: boolean;
  state: RollupState;
  href: string;
  /** Pre-resolved FilterBar key: availability (anon) or study state (signed-in). */
  dataStatus: string;
}

/** One discipline (subsection) within a pillar. */
export interface PillarSubView {
  id: string;
  name: string;
  state: RollupState;
  studied: number;
  total: number;
  connCount: number;
  lessons: PillarLessonView[];
}

/** A fully-computed pillar view-model handed down from the server component. */
export interface PillarView {
  letter: string;
  name: string;
  tagline: string;
  color: string;
  pct: number;
  studied: number;
  total: number;
  inProgress: number;
  untouched: number;
  signedIn: boolean;
  subs: PillarSubView[];
}

/**
 * Client island for the pillars section. Pillars render as a grid of small cards
 * (letter + name + coverage %); clicking one opens a big detail panel below the
 * grid with the discipline → lesson tree, mirroring the suggested-paths explorer.
 *
 * The panel reproduces the `.subsection` / `.topic` markup with `data-status` /
 * `data-name` so FilterBar (lesson search/filter) and CollapseController
 * (per-discipline `h4` collapse) keep working against the open pillar.
 */
export function PillarExplorer({ pillars }: { pillars: PillarView[] }) {
  const [selected, setSelected] = useState(-1);
  const active = selected >= 0 ? pillars[selected] : null;

  // Opening/closing a panel swaps which lessons are in the DOM. Notify FilterBar
  // (a sibling island) so it re-applies any active filter to the new rows. Runs
  // after paint, so the panel's `.topic` nodes already exist when it fires.
  useEffect(() => {
    window.dispatchEvent(new Event("pillarpanelchange"));
  }, [selected]);

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {pillars.map((p, i) => {
          const isActive = i === selected;
          return (
            <button
              key={p.letter}
              id={p.letter}
              type="button"
              onClick={() => setSelected(isActive ? -1 : i)}
              aria-pressed={isActive}
              className={`card p-4 text-left flex items-center gap-3 min-h-[64px] scroll-mt-20 transition-all cursor-pointer ${
                isActive ? "" : "hover:-translate-y-0.5"
              }`}
              style={{
                borderTopColor: p.color,
                borderTopWidth: 3,
                ...(isActive
                  ? {
                      outline: `2px solid ${p.color}`,
                      outlineOffset: 2,
                      boxShadow: `0 0 18px color-mix(in srgb, ${p.color} 35%, transparent)`,
                    }
                  : {}),
              }}
            >
              <span
                className="w-8 h-8 rounded-lg flex items-center justify-center text-base font-extrabold text-[var(--bg)] shrink-0"
                style={{ background: p.color }}
              >
                {p.letter}
              </span>
              <h3 className="m-0 flex-1 text-sm font-bold leading-snug">
                {p.name}
              </h3>
              <span
                className="text-sm font-extrabold leading-none shrink-0"
                style={{ color: p.color }}
              >
                {p.pct}%
              </span>
            </button>
          );
        })}
      </div>

      {active && (
        <PillarDetail pillar={active} onClose={() => setSelected(-1)} />
      )}
    </div>
  );
}

function PillarDetail({
  pillar,
  onClose,
}: {
  pillar: PillarView;
  onClose: () => void;
}) {
  return (
    <div
      className="conn-panel card p-6"
      style={{ ["--panel-color" as never]: pillar.color }}
    >
      <div className="flex items-start justify-between gap-4 mb-5">
        <div className="flex items-center gap-4">
          <div
            className="w-[52px] h-[52px] rounded-[12px] flex items-center justify-center text-[1.7rem] font-extrabold text-[var(--bg)] shrink-0"
            style={{
              background: pillar.color,
              boxShadow: `0 6px 20px ${pillar.color}40`,
            }}
          >
            {pillar.letter}
          </div>
          <div>
            <h3 className="m-0 text-xl font-bold tracking-tight">
              {pillar.name}
            </h3>
            <p className="m-0 text-sm text-[var(--fg-dim)]">{pillar.tagline}</p>
          </div>
        </div>
        <div className="flex items-start gap-3 shrink-0">
          <div className="text-right min-w-[180px]">
            <span
              className="text-2xl font-extrabold leading-none"
              style={{ color: pillar.color }}
            >
              {pillar.pct}%
            </span>
            <div className="text-xs text-[var(--fg-mute)] mt-1 mb-2">
              {pillar.studied}/{pillar.total} studied · {pillar.inProgress} in
              progress · {pillar.untouched} to go
            </div>
            <div className="statbar">
              <div
                className="seg cov"
                style={{ width: pct(pillar.studied, pillar.total) }}
              />
              <div
                className="seg par"
                style={{ width: pct(pillar.inProgress, pillar.total) }}
              />
              <div
                className="seg gap"
                style={{ width: pct(pillar.untouched, pillar.total) }}
              />
            </div>
          </div>
          <button onClick={onClose} className="btn shrink-0" aria-label="close">
            ✕
          </button>
        </div>
      </div>

      <div className="subsections grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {pillar.subs.map((sub) => {
          const stateColor = STATE_COLOR[sub.state];
          return (
            <div key={sub.id} id={`sub-${sub.id}`} className="subsection">
              <h4 className="m-0 mb-2.5 pb-1.5 border-b border-[var(--border)] text-xs uppercase tracking-wider font-semibold text-[var(--fg-dim)]">
                <span className="chevron">▾</span>
                <span className="mr-1.5" style={{ color: stateColor }}>
                  {STATE_GLYPH[sub.state]}
                </span>
                <span
                  className="font-extrabold mr-1.5"
                  style={{ color: stateColor }}
                >
                  {sub.id}
                </span>
                <Link
                  href={`/pillar/${pillar.letter}/${sub.id}`}
                  className="no-underline text-inherit hover:text-[var(--fg)]"
                >
                  {sub.name}
                </Link>
                {sub.connCount > 0 && (
                  <span className="conn-count has ml-2">
                    🔗 {sub.connCount}
                  </span>
                )}
                {pillar.signedIn && sub.total > 0 && (
                  <span className="ml-2" style={{ color: stateColor }}>
                    {sub.studied}/{sub.total}
                  </span>
                )}
              </h4>
              <div className="topics flex flex-col gap-0.5">
                {sub.lessons.length === 0 ? (
                  <div className="topic text-[var(--fg-mute)] text-xs italic">
                    curriculum coming soon
                  </div>
                ) : (
                  sub.lessons.map((lesson) => {
                    const glyphColor = STATE_COLOR[lesson.state];
                    return (
                      <div
                        key={lesson.id}
                        className="topic"
                        data-status={lesson.dataStatus}
                        data-name={lesson.title.toLowerCase()}
                      >
                        <span className="ic" style={{ color: glyphColor }}>
                          {STATE_GLYPH[lesson.state]}
                        </span>
                        {lesson.available ? (
                          <Link
                            href={lesson.href}
                            className="name no-underline hover:text-[var(--fg)]"
                          >
                            {lesson.title}
                          </Link>
                        ) : (
                          <span className="name opacity-50">
                            {lesson.title}
                          </span>
                        )}
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/** A statbar segment width as a percentage string (0% when the pillar is empty). */
function pct(n: number, total: number): string {
  return total > 0 ? `${(n / total) * 100}%` : "0%";
}
