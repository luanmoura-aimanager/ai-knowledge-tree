"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathHighlight } from "@/components/PathHighlightProvider";

/** Per-pillar chip in a path: an ordered subsection with its rolled-up state. */
export interface PathChip {
  id: string;
  name: string;
  letter: string;
  color: string;
  state: "done" | "in-progress" | "untouched";
}

/** One resolved lesson stop in a lesson-stepped path (e.g. the amt mirror). */
export interface PathStepView {
  subId: string;
  lessonId: string;
  letter: string;
  color: string;
  title: string;
  note?: string;
  section?: string;
  available: boolean;
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
  steps?: PathStepView[];
}

/** amt chapter labels, keyed by the chapter number parsed from a step's note. */
const AMT_CHAPTERS: Record<string, string> = {
  "0": "Ch0 · Math foundations",
  "1": "Ch1 · Linear models & the perceptron",
  "2": "Ch2 · MLPs & backprop",
  "3": "Ch3 · Optimization & regularization",
  "4": "Ch4 · CNN bridge",
  "5": "Ch5 · Sequence modeling & embeddings",
  "6": "Ch6 · Attention & the Transformer",
  "7": "Ch7 · Training language models",
  "8": "Ch8 · Modern LLM architectures",
  "9": "Ch9 · Alignment",
  "10": "Ch10 · Inference & decoding",
  "11": "Ch11 · Interpretability & the frontier",
  "12": "Ch12 · Capstone: build a tiny GPT",
};

function chapterOf(note?: string): string {
  const m = note?.match(/\d+/);
  return m ? m[0] : "";
}

/**
 * The heading a step is grouped under. An explicit `section` wins (curated
 * role-paths); otherwise fall back to the ai-math-theory chapter parsed from the
 * note (the LLM Theory mirror). Empty string means "no header".
 */
function groupLabelOf(step: PathStepView): string {
  if (step.section) return step.section;
  const ch = chapterOf(step.note);
  return AMT_CHAPTERS[ch] ?? ch;
}

/**
 * Client island for the suggested-paths section. The paths render as a grid of
 * small title-only cards; clicking one highlights it and opens a big horizontal
 * detail card (description, pillar squares, progress bar) below the grid.
 */
export function PathExplorer({ paths }: { paths: PathView[] }) {
  const [selected, setSelected] = useState(-1);
  const highlight = usePathHighlight();
  const active = selected >= 0 ? paths[selected] : null;

  // Select a path (or -1 to clear) and mirror its subsection ids + color into the
  // shared highlight context so the connections graph can light up the same nodes
  // and draw the route between them.
  const select = (i: number) => {
    setSelected(i);
    highlight?.setActive(
      i >= 0
        ? { ids: paths[i].chips.map((c) => c.id), color: paths[i].color }
        : null,
    );
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {paths.map((path, i) => {
          const isActive = i === selected;
          return (
            <button
              key={path.name}
              type="button"
              onClick={() => select(isActive ? -1 : i)}
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

      {active && <PathDetail path={active} onClose={() => select(-1)} />}
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
            Disciplines ({path.chips.length})
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

      {path.steps && path.steps.length > 0 && <PathSteps steps={path.steps} />}

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

/** The ordered lesson sequence, grouped by amt chapter, with per-step links. */
function PathSteps({ steps }: { steps: PathStepView[] }) {
  return (
    <div className="mt-6">
      <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
        Course sequence ({steps.length} steps)
      </h4>
      <ol className="m-0 p-0 list-none max-h-[440px] overflow-y-auto pr-1 flex flex-col gap-0.5">
        {steps.map((step, i) => {
          const group = groupLabelOf(step);
          const showHeader =
            group !== "" && (i === 0 || groupLabelOf(steps[i - 1]) !== group);
          return (
            <li key={`${step.subId}/${step.lessonId}/${i}`}>
              {showHeader && (
                <div className="text-[11px] font-semibold text-[var(--fg-dim)] mt-3 mb-1 sticky top-0 bg-[var(--card)] py-0.5">
                  {group}
                </div>
              )}
              <Link
                href={`/pillar/${step.letter}/${step.subId}/${step.lessonId}`}
                className="flex items-center gap-2 px-2 py-1 rounded no-underline hover:bg-[var(--card-2)] transition-colors group"
                title={`${step.subId}/${step.lessonId}`}
              >
                <span
                  className="font-mono text-[10px] w-4 text-right shrink-0"
                  style={{ color: step.color }}
                >
                  {i + 1}
                </span>
                <span
                  className="font-mono text-[10px] px-1 py-0.5 rounded shrink-0"
                  style={{
                    background: `color-mix(in srgb, ${step.color} 18%, transparent)`,
                    color: step.color,
                  }}
                >
                  {step.subId}
                </span>
                <span
                  className={`text-sm truncate ${
                    step.state === "done"
                      ? "text-[var(--fg)] font-medium"
                      : step.available
                        ? "text-[var(--fg)]"
                        : "text-[var(--fg-dim)] italic"
                  } group-hover:text-[var(--fg)]`}
                >
                  {step.state === "done" && "✓ "}
                  {step.title}
                </span>
                {step.note && (
                  <span className="ml-auto font-mono text-[10px] text-[var(--fg-mute)] shrink-0">
                    {step.note}
                  </span>
                )}
                {!step.available && (
                  <span className="font-mono text-[9px] text-[var(--fg-mute)] border border-[var(--border)] rounded px-1 shrink-0">
                    soon
                  </span>
                )}
              </Link>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
