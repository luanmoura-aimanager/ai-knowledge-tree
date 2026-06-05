import { PATHS, getSubsectionById } from "@/lib/dag";
import { getLesson, lessonKey, pillarProgress } from "@/lib/curriculum";
import { lessonContentStatus } from "@/lib/content";
import type { ProgressMap } from "@/lib/progress";
import {
  PathExplorer,
  type PathView,
  type PathStepView,
} from "@/components/PathExplorer";

/**
 * Curated reading sequences (PATHS). The heavy per-path roll-up (chips + study
 * percentages) is computed here on the server and handed to the PathExplorer
 * client island, which renders the title-only cards and the click-to-open
 * detail card.
 *
 * Paths may also carry a lesson-level `steps` sequence (e.g. the ai-math-theory
 * mirror). For those, the progress bar is rolled up over the steps themselves
 * (distinct lesson stops) rather than over whole subsections, and each step is
 * resolved to a linkable lesson view-model.
 */
export function LearningPaths({ progress }: { progress?: ProgressMap }) {
  const prog = progress ?? new Map();

  const views: PathView[] = PATHS.map((path) => {
    const pp = pillarProgress(path.pillars, prog);

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

    const steps: PathStepView[] | undefined = path.steps?.map((s) => {
      const sub = getSubsectionById(s.subId);
      const lesson = getLesson(s.subId, s.lessonId);
      const raw = prog.get(lessonKey(s.subId, s.lessonId));
      const state =
        raw === "studied"
          ? "done"
          : raw === "in-progress"
            ? "in-progress"
            : "untouched";
      return {
        subId: s.subId,
        lessonId: s.lessonId,
        letter: sub?.pillar.letter ?? "",
        color: sub?.pillar.color ?? "var(--fg-dim)",
        title: lesson?.title ?? s.lessonId,
        note: s.note,
        available: lessonContentStatus(s.subId, s.lessonId) === "available",
        state,
      };
    });

    // Lesson-stepped paths roll progress over their steps; others over pillars.
    const total = steps ? steps.length : pp.total;
    const studied = steps
      ? steps.filter((s) => s.state === "done").length
      : pp.studied;
    const inProgress = steps
      ? steps.filter((s) => s.state === "in-progress").length
      : pp.inProgress;
    const denom = total || 1;
    const pctStudied = (studied / denom) * 100;
    const pctProgress = (inProgress / denom) * 100;

    return {
      name: path.name,
      desc: path.desc,
      color: path.color,
      studied,
      total,
      pctStudied,
      pctProgress,
      pctGap: 100 - pctStudied - pctProgress,
      chips,
      steps,
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
