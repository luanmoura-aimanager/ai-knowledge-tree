import type { Lesson, LessonWithSub } from "@/lib/types";
import { A_CURRICULUM } from "./A";
import { B_CURRICULUM } from "./B";
import { C_CURRICULUM } from "./C";
import { D_CURRICULUM } from "./D";
import { E_CURRICULUM } from "./E";
import { F_CURRICULUM } from "./F";
import { G_CURRICULUM } from "./G";
import { H_CURRICULUM } from "./H";

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
