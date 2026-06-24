import { PILLARS, CONNECTIONS } from "@/lib/dag";
import { getCurriculum, lessonKey, pillarProgress } from "@/lib/curriculum";
import { lessonContentStatus } from "@/lib/content";
import type { ProgressMap } from "@/lib/progress";
import {
  PillarExplorer,
  type PillarView,
  type PillarSubView,
  type PillarLessonView,
} from "@/components/PillarExplorer";

/**
 * Server side of the pillars section. Rolls up each pillar's per-lesson progress
 * (the same overlay PillarCard used to compute) into a serializable
 * `PillarView[]` and hands it to the PillarExplorer client island, which renders
 * the compact card grid and the click-to-open detail panel.
 */
export function PillarsSection({
  progress,
  signedIn = false,
}: {
  progress?: ProgressMap;
  signedIn?: boolean;
}) {
  const prog = progress ?? new Map();

  const connCount = (subId: string) =>
    CONNECTIONS.filter((c) => c.from === subId || c.to === subId).length;

  const views: PillarView[] = PILLARS.map((pillar) => {
    const pp = pillarProgress(
      pillar.subs.map((sub) => sub.id),
      prog,
    );

    const subs: PillarSubView[] = pillar.subs.map((sub) => {
      const sp = pp.subs[sub.id];
      const lessons: PillarLessonView[] = getCurriculum(sub.id).map(
        (lesson) => {
          const available =
            lessonContentStatus(sub.id, lesson.id) === "available";
          // Signed-in rows carry the user's study state; anonymous rows untouched.
          const raw = signedIn
            ? prog.get(lessonKey(sub.id, lesson.id))
            : undefined;
          const state =
            raw === "studied"
              ? "done"
              : raw === "in-progress"
                ? "in-progress"
                : "untouched";
          // FilterBar filters signed-in rows by study state, anonymous by availability.
          const dataStatus = signedIn
            ? (raw ?? "unstudied")
            : available
              ? "available"
              : "coming-soon";
          return {
            id: lesson.id,
            title: lesson.title,
            available,
            state,
            href: `/pillar/${pillar.letter}/${sub.id}/${lesson.id}`,
            dataStatus,
          };
        },
      );

      return {
        id: sub.id,
        name: sub.name,
        state: sp.state,
        studied: sp.studied,
        total: sp.total,
        connCount: connCount(sub.id),
        lessons,
      };
    });

    return {
      letter: pillar.letter,
      name: pillar.name,
      tagline: pillar.tagline,
      color: pillar.color,
      pct: pp.pct,
      studied: pp.studied,
      total: pp.total,
      inProgress: pp.inProgress,
      untouched: pp.untouched,
      signedIn,
      subs,
    };
  });

  return (
    <section className="max-w-[1280px] mx-auto px-6 py-12">
      <h2 className="text-2xl font-bold mb-1.5">Pillars</h2>
      <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
        The top-level domains of the map (A → N), spanning Data Science, Machine
        Learning, Deep Learning, and AI Engineering. Each pillar is a set of
        disciplines taught as ordered, one-concept-per-page lessons. Pick a
        pillar to see its subsections and lessons.
      </p>
      <PillarExplorer pillars={views} />
    </section>
  );
}
