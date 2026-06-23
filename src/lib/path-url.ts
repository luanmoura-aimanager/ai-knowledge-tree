/**
 * Pure helpers for the `?path=<slug>&i=<step>` contract that carries a suggested
 * path's identity onto a lesson page. Kept dependency-free (no curriculum/dag
 * imports) so client components — PathExplorer, LessonSidebar — can import it
 * without pulling the whole lesson graph into the client bundle. The single
 * owner of the path-mode URL format, so the path detail, the sidebar links, and
 * the lesson prev/next can never drift apart.
 */

/** A step addressable by route — the minimum the URL/active-step helpers need. */
export interface RoutableStep {
  letter: string;
  subId: string;
  lessonId: string;
}

/** Stable, url-safe slug for a path name (strips emoji/symbols, kebab-cases). */
export function pathSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/** The lesson href for step `i` of path `slug` (keeps the reader in path mode). */
export function pathStepHref(
  slug: string,
  step: RoutableStep,
  i: number,
): string {
  return `/pillar/${step.letter}/${step.subId}/${step.lessonId}?path=${slug}&i=${i}`;
}

/**
 * The index of the active step in a path. Trusts the explicit `?i=` index when
 * it is an integer in range (a path may revisit a lesson, so the index — not the
 * route — is authoritative); otherwise falls back to the first step whose route
 * matches `currentRoute`. Returns -1 when no step matches. Shared by the lesson
 * page (server) and the sidebar (client) so both agree on "you are here".
 */
export function resolveActiveStep(
  steps: RoutableStep[],
  rawIndex: string | null | undefined,
  currentRoute: string,
): number {
  const i = rawIndex != null && rawIndex !== "" ? Number(rawIndex) : Number.NaN;
  if (Number.isInteger(i) && i >= 0 && i < steps.length) return i;
  return steps.findIndex(
    (s) => `/pillar/${s.letter}/${s.subId}/${s.lessonId}` === currentRoute,
  );
}
