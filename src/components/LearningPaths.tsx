import Link from "next/link";
import { PATHS, getSubsectionById } from "@/lib/dag";
import type { Path } from "@/lib/types";
import { pillarProgress } from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";

/**
 * Curated reading sequences (PATHS) rendered as cards: name, description, the
 * ordered subsection chips, and a mini-bar showing how many lessons across the
 * path the signed-in user has studied (anonymous visitors see 0 / total).
 */
export function LearningPaths({ progress }: { progress?: ProgressMap }) {
  const prog = progress ?? new Map();
  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12">
      <h2 className="text-2xl font-bold mb-1.5">Suggested paths</h2>
      <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
        Curated reading sequences that cross the DAG, connecting pillars in a
        didactic order for different reader profiles.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {PATHS.map((path) => (
          <PathCard key={path.name} path={path} progress={prog} />
        ))}
      </div>
    </div>
  );
}

function PathCard({ path, progress }: { path: Path; progress: ProgressMap }) {
  const pp = pillarProgress(path.pillars, progress);
  const total = pp.total || 1;
  const pctStudied = (pp.studied / total) * 100;
  const pctProgress = (pp.inProgress / total) * 100;
  const pctGap = 100 - pctStudied - pctProgress;

  return (
    <div
      className="card p-5 flex flex-col gap-3"
      style={{ borderTopColor: path.color, borderTopWidth: 3 }}
    >
      <h3 className="m-0 text-lg font-bold">{path.name}</h3>
      <p className="m-0 text-sm text-[var(--fg-dim)] leading-relaxed">
        {path.desc}
      </p>
      <div className="flex gap-1 flex-wrap">
        {path.pillars.map((id) => {
          const sub = getSubsectionById(id);
          if (!sub) return null;
          const state = pp.subs[id]?.state;
          const color = sub.pillar.color;
          const base =
            "font-mono text-xs px-1.5 py-0.5 rounded no-underline transition-colors";
          return (
            <Link
              key={id}
              href={`/pillar/${sub.pillar.letter}/${id}`}
              title={`${id} · ${sub.name}`}
              className={
                state === "done"
                  ? `${base} font-semibold hover:opacity-85`
                  : state === "in-progress"
                    ? `${base} text-[var(--fg)] hover:opacity-85`
                    : `${base} bg-[var(--card-2)] text-[var(--fg-dim)] hover:text-[var(--fg)]`
              }
              style={
                state === "done"
                  ? { background: color, color: "var(--bg)" }
                  : state === "in-progress"
                    ? {
                        background: `color-mix(in srgb, ${color} 22%, transparent)`,
                      }
                    : undefined
              }
            >
              {id}
            </Link>
          );
        })}
      </div>
      <div className="mt-auto">
        <div className="text-xs text-[var(--fg-mute)] mb-1">
          {pp.studied}/{pp.total} studied
        </div>
        <div className="statbar">
          <div className="seg cov" style={{ width: `${pctStudied}%` }} />
          <div className="seg par" style={{ width: `${pctProgress}%` }} />
          <div className="seg gap" style={{ width: `${pctGap}%` }} />
        </div>
      </div>
    </div>
  );
}
