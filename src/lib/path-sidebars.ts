/**
 * Server-side resolution of curated paths into the lesson-sidebar view-model.
 *
 * When a reader opens a lesson *from a suggested path* (the `?path=<slug>` query),
 * the lesson sidebar lists that path's lessons in order instead of the current
 * discipline's. This module builds that ordered, prerequisite-closed sequence
 * (reusing `expandPathSteps`) and resolves each step to a linkable view-model.
 * Lives apart from `paths.ts` (which is pure and imported by the prereq guard via
 * tsx) because it pulls in `content.ts` — a `server-only` module.
 */
import "server-only";
import { cache } from "react";
import { PATHS, getSubsectionById } from "./dag";
import { getLesson } from "./curriculum";
import { lessonContentStatus } from "./content";
import { expandPathSteps } from "./paths";
import { pathSlug } from "./path-url";
import type { PathSidebar, PathSidebarStep, PathStep } from "./types";

/**
 * Resolve one curated `PathStep` to its linkable view-model (pillar letter/color,
 * title, availability). The single source for step resolution: `getPathSidebars`
 * here and `LearningPaths` both build their per-step view-model from this.
 */
export function resolvePathStep(s: PathStep): PathSidebarStep {
  const sub = getSubsectionById(s.subId);
  const lesson = getLesson(s.subId, s.lessonId);
  return {
    letter: sub?.pillar.letter ?? "",
    subId: s.subId,
    lessonId: s.lessonId,
    title: lesson?.title ?? s.lessonId,
    color: sub?.pillar.color ?? "var(--fg-dim)",
    available: lessonContentStatus(s.subId, s.lessonId) === "available",
    section: s.section,
    note: s.note,
  };
}

/**
 * Every path that carries a lesson-level `steps` sequence, expanded to its
 * prerequisite closure and resolved to linkable steps. Memoized per request:
 * the result is static (no per-user progress) so it is computed once and shared.
 */
export const getPathSidebars = cache((): PathSidebar[] =>
  PATHS.filter((p) => p.steps && p.steps.length > 0).map((p) => ({
    slug: pathSlug(p.name),
    name: p.name,
    color: p.color,
    steps: expandPathSteps(p.steps!).map(resolvePathStep),
  })),
);

/** The expanded sidebar for one path, by slug (undefined if the slug is unknown). */
export function getPathSidebar(slug: string): PathSidebar | undefined {
  return getPathSidebars().find((p) => p.slug === slug);
}
