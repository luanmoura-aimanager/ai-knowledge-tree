import type { Lesson, LessonWithSub } from "@/lib/types";
import type { ProgressMap } from "@/lib/progress";
import { A_CURRICULUM } from "./A";
import { B_CURRICULUM } from "./B";
import { C_CURRICULUM } from "./C";
import { D_CURRICULUM } from "./D";
import { E_CURRICULUM } from "./E";
import { F_CURRICULUM } from "./F";
import { G_CURRICULUM } from "./G";
import { H_CURRICULUM } from "./H";
import { I_CURRICULUM } from "./I";
import { J_CURRICULUM } from "./J";
import { K_CURRICULUM } from "./K";

/**
 * Lesson curriculum registry: subsection id → ordered Lesson[]. Each pillar's
 * lessons live in their own module to keep these maps readable; new pillars are
 * added by importing their curriculum and spreading it here.
 */
const CURRICULA: Record<string, Lesson[]> = {
  ...A_CURRICULUM,
  ...B_CURRICULUM,
  ...C_CURRICULUM,
  ...D_CURRICULUM,
  ...E_CURRICULUM,
  ...F_CURRICULUM,
  ...G_CURRICULUM,
  ...H_CURRICULUM,
  ...I_CURRICULUM,
  ...J_CURRICULUM,
  ...K_CURRICULUM,
};

/** Ordered lessons for a subsection (empty if none authored/planned yet). */
export function getCurriculum(subId: string): Lesson[] {
  return CURRICULA[subId] ?? [];
}

/** A lesson by subsection + slug, with its 1-based order, or undefined. */
export function getLesson(
  subId: string,
  lessonId: string,
): (Lesson & { order: number }) | undefined {
  const lessons = getCurriculum(subId);
  const i = lessons.findIndex((l) => l.id === lessonId);
  return i === -1 ? undefined : { ...lessons[i], order: i + 1 };
}

/** Every lesson across all subsections, tagged with its subId. */
export function allLessons(): LessonWithSub[] {
  return Object.entries(CURRICULA).flatMap(([subId, lessons]) =>
    lessons.map((l) => ({ ...l, subId })),
  );
}

/** Total number of planned lessons across the whole curriculum. */
export function lessonCount(): number {
  return Object.values(CURRICULA).reduce((n, ls) => n + ls.length, 0);
}

/** The global progress key for a lesson. */
export function lessonKey(subId: string, lessonId: string): string {
  return `${subId}/${lessonId}`;
}

/** A subsection's rolled-up study state: untouched → in-progress → done. */
export type ProgressState = "untouched" | "in-progress" | "done";

/**
 * Roll a user's per-lesson progress up to one subsection. A subsection is
 * "done" once every lesson is studied, "in-progress" if any lesson is studied
 * or in progress, else "untouched". Empty curricula stay "untouched" (the
 * `total > 0` guard prevents a vacuous "done").
 */
export interface SubProgress {
  total: number;
  studied: number;
  inProgress: number;
  state: ProgressState;
}

export function subProgress(subId: string, progress: ProgressMap): SubProgress {
  const lessons = getCurriculum(subId);
  const total = lessons.length;
  const studied = lessons.filter(
    (l) => progress.get(lessonKey(subId, l.id)) === "studied",
  ).length;
  const inProgress = lessons.filter(
    (l) => progress.get(lessonKey(subId, l.id)) === "in-progress",
  ).length;
  const state: ProgressState =
    total > 0 && studied === total
      ? "done"
      : studied + inProgress > 0
        ? "in-progress"
        : "untouched";
  return { total, studied, inProgress, state };
}

/**
 * Aggregate per-lesson progress across a set of subsections (a pillar). Returns
 * the rolled-up totals plus the per-subsection breakdown (`subs`, keyed by id)
 * so callers can reuse each `subProgress` result instead of recomputing it.
 */
export function pillarProgress(subIds: string[], progress: ProgressMap) {
  const subs: Record<string, SubProgress> = {};
  let total = 0;
  let studied = 0;
  let inProgress = 0;
  for (const id of subIds) {
    const p = subProgress(id, progress);
    subs[id] = p;
    total += p.total;
    studied += p.studied;
    inProgress += p.inProgress;
  }
  const untouched = total - studied - inProgress;
  const pct = total > 0 ? Math.round((studied / total) * 100) : 0;
  return { total, studied, inProgress, untouched, pct, subs };
}
