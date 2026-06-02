import Link from "next/link";
import type { Pillar } from "@/lib/types";
import { CONNECTIONS } from "@/lib/dag";
import {
  pillarProgress,
  subProgress,
  type ProgressState,
} from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";
import { TopicChip } from "./TopicChip";

/** Visual mapping for a rolled-up study state (matches the .statbar palette). */
const STATE_COLOR: Record<ProgressState, string> = {
  done: "var(--good)",
  "in-progress": "var(--partial)",
  untouched: "var(--fg-mute)",
};
const STATE_GLYPH: Record<ProgressState, string> = {
  done: "✓",
  "in-progress": "◐",
  untouched: "○",
};

/**
 * One pillar rendered as a full-width card: header with letter + coverage stat
 * bar, then subsections in a responsive grid.
 *
 * Stays a pure server component. Interactivity (filter/search) is handled by
 * FilterBar mutating `data-*` attributes; collapse is handled by
 * CollapseController via event delegation on `.pillar-header` / `.subsection h4`.
 */
export function PillarCard({
  pillar,
  progress,
  signedIn,
}: {
  pillar: Pillar;
  progress?: ProgressMap;
  signedIn?: boolean;
}) {
  // Personal study overlay: statbar + header + subsection coloring track the
  // user's per-lesson progress. Anonymous (no map) → everything untouched/gray.
  const prog = progress ?? new Map();
  const pp = pillarProgress(
    pillar.subs.map((sub) => sub.id),
    prog,
  );

  const connCount = (subId: string) =>
    CONNECTIONS.filter((c) => c.from === subId || c.to === subId).length;

  return (
    <section
      id={pillar.letter}
      className="pillar card mb-7 overflow-hidden scroll-mt-20"
      data-pillar={pillar.letter}
      style={{ ["--pillar" as never]: pillar.color }}
    >
      <header
        className="pillar-header grid grid-cols-[auto_1fr_auto] gap-5 px-7 py-5 border-b border-[var(--border)]"
        style={{
          background: `linear-gradient(90deg, color-mix(in srgb, ${pillar.color} 18%, transparent), transparent 70%)`,
        }}
      >
        <div
          className="w-[52px] h-[52px] rounded-[12px] flex items-center justify-center text-[1.7rem] font-extrabold text-[var(--bg)]"
          style={{
            background: pillar.color,
            boxShadow: `0 6px 20px ${pillar.color}40`,
          }}
        >
          {pillar.letter}
        </div>
        <div>
          <h2 className="m-0 text-xl font-bold tracking-tight">
            {pillar.name}
          </h2>
          <p className="m-0 text-sm text-[var(--fg-dim)]">{pillar.tagline}</p>
        </div>
        <div className="text-right min-w-[200px]">
          <div className="flex items-center justify-end">
            <span
              className="text-2xl font-extrabold leading-none"
              style={{ color: pillar.color }}
            >
              {pp.pct}%
            </span>
            <span className="pillar-chev" aria-hidden>
              ▾
            </span>
          </div>
          <div className="text-xs text-[var(--fg-mute)] mt-1 mb-2">
            {pp.studied}/{pp.total} studied · {pp.inProgress} in progress ·{" "}
            {pp.untouched} to go
          </div>
          <div className="statbar">
            <div
              className="seg cov"
              style={{ width: pct(pp.studied, pp.total) }}
            />
            <div
              className="seg par"
              style={{ width: pct(pp.inProgress, pp.total) }}
            />
            <div
              className="seg gap"
              style={{ width: pct(pp.untouched, pp.total) }}
            />
          </div>
        </div>
      </header>

      <div className="subsections grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-7">
        {pillar.subs.map((sub) => {
          const n = connCount(sub.id);
          const sp = subProgress(sub.id, prog);
          const stateColor = STATE_COLOR[sp.state];
          return (
            <div key={sub.id} id={`sub-${sub.id}`} className="subsection">
              <h4 className="m-0 mb-2.5 pb-1.5 border-b border-[var(--border)] text-xs uppercase tracking-wider font-semibold text-[var(--fg-dim)]">
                <span className="chevron">▾</span>
                <span className="mr-1.5" style={{ color: stateColor }}>
                  {STATE_GLYPH[sp.state]}
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
                {n > 0 && <span className="conn-count has ml-2">🔗 {n}</span>}
                {signedIn && sp.total > 0 && (
                  <span className="ml-2" style={{ color: stateColor }}>
                    {sp.studied}/{sp.total}
                  </span>
                )}
              </h4>
              <div className="topics flex flex-col gap-0.5">
                {sub.topics.map((t) => (
                  <TopicChip key={t.name} topic={t} />
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

/** A statbar segment width as a percentage string (0% when the pillar is empty). */
function pct(n: number, total: number): string {
  return total > 0 ? `${(n / total) * 100}%` : "0%";
}
