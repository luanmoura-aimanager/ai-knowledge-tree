import { PATHS, getSubsectionById } from "@/lib/dag";
import { pillarProgress } from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";
import { PathExplorer, type PathView } from "@/components/PathExplorer";

/**
 * Curated reading sequences (PATHS). The heavy per-path roll-up (chips + study
 * percentages) is computed here on the server and handed to the PathExplorer
 * client island, which renders the title-only cards and the click-to-open
 * detail card.
 */
export function LearningPaths({ progress }: { progress?: ProgressMap }) {
  const prog = progress ?? new Map();

  const views: PathView[] = PATHS.map((path) => {
    const pp = pillarProgress(path.pillars, prog);
    const total = pp.total || 1;
    const pctStudied = (pp.studied / total) * 100;
    const pctProgress = (pp.inProgress / total) * 100;

    const chips = path.pillars
      .map((id) => {
        const sub = getSubsectionById(id);
        if (!sub) return null;
        return {
          id,
          name: sub.name,
          letter: sub.pillar.letter,
          color: sub.pillar.color,
          state: pp.subs[id]?.state ?? "untouched",
        };
      })
      .filter((c): c is NonNullable<typeof c> => c !== null);

    return {
      name: path.name,
      desc: path.desc,
      color: path.color,
      studied: pp.studied,
      total: pp.total,
      pctStudied,
      pctProgress,
      pctGap: 100 - pctStudied - pctProgress,
      chips,
    };
  });

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12">
      <h2 className="text-2xl font-bold mb-1.5">Suggested paths</h2>
      <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
        Curated reading sequences that cross the DAG, connecting pillars in a
        didactic order for different reader profiles. Pick a path to see its
        details.
      </p>
      <PathExplorer paths={views} />
    </div>
  );
}
