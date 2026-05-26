import { PATHS, PILLARS } from "@/lib/dag";
import type { Path } from "@/lib/types";

/**
 * Curated reading sequences (PATHS) rendered as cards: name, description, the
 * ordered subsection chips, and a coverage mini-bar over the path's topics.
 */
export function LearningPaths() {
  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12">
      <h2 className="text-2xl font-bold mb-1.5">Trilhas sugeridas</h2>
      <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
        Caminhos curados que atravessam a DAG, conectando pilares em sequência
        didática para perfis distintos.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {PATHS.map((path) => (
          <PathCard key={path.name} path={path} />
        ))}
      </div>
    </div>
  );
}

function PathCard({ path }: { path: Path }) {
  const subs = PILLARS.flatMap((p) =>
    p.subs.filter((s) => path.pillars.includes(s.id)),
  );
  const all = subs.flatMap((s) => s.topics);
  const total = all.length || 1;
  const cov = all.filter((t) => t.status === "covered").length;
  const par = all.filter((t) => t.status === "partial").length;
  const pctCov = (cov / total) * 100;
  const pctPar = (par / total) * 100;
  const pctGap = 100 - pctCov - pctPar;

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
        {path.pillars.map((id) => (
          <span
            key={id}
            className="font-mono text-xs px-1.5 py-0.5 rounded bg-[var(--card-2)] text-[var(--fg-dim)]"
          >
            {id}
          </span>
        ))}
      </div>
      <div className="mt-auto">
        <div className="text-xs text-[var(--fg-mute)] mb-1">
          {cov}/{total} cobertos
        </div>
        <div className="statbar">
          <div className="seg cov" style={{ width: `${pctCov}%` }} />
          <div className="seg par" style={{ width: `${pctPar}%` }} />
          <div className="seg gap" style={{ width: `${pctGap}%` }} />
        </div>
      </div>
    </div>
  );
}
