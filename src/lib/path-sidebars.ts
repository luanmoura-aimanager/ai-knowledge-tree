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
import type { PathSidebar } from "./types";

/** Stable, url-safe slug for a path name (strips emoji/symbols, kebab-cases). */
export function pathSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
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
    steps: expandPathSteps(p.steps!).map((s) => {
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
    }),
  })),
);

/** A neighbor lesson in a path's expanded sequence (for path-order prev/next). */
export interface PathNeighbor {
  letter: string;
  subId: string;
  lessonId: string;
  title: string;
  index: number;
}

/**
 * The lessons immediately before/after step `index` in the path `slug`'s expanded
 * sequence, or null at the ends. Returns `{ prev: null, next: null }` when the
 * slug or index doesn't resolve, so the caller falls back to discipline order.
 */
export function getPathPrevNext(
  slug: string,
  index: number,
): { prev: PathNeighbor | null; next: PathNeighbor | null } {
  const path = getPathSidebars().find((p) => p.slug === slug);
  if (
    !path ||
    !Number.isInteger(index) ||
    index < 0 ||
    index >= path.steps.length
  ) {
    return { prev: null, next: null };
  }
  const at = (j: number): PathNeighbor | null => {
    const s = path.steps[j];
    return s
      ? {
          letter: s.letter,
          subId: s.subId,
          lessonId: s.lessonId,
          title: s.title,
          index: j,
        }
      : null;
  };
  return { prev: at(index - 1), next: at(index + 1) };
}
