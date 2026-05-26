/**
 * content.ts: resolves the long-form MDX lesson layer on top of the DAG.
 *
 * Study prose lives at `content/<pillar-slug>/<subId>/<lessonId>.mdx`. The
 * presence of a file is the source of truth for a lesson's `contentStatus`
 * (available vs coming-soon); dag.ts is the source of truth for pillars/
 * subsections, and src/lib/curriculum for the ordered lesson list.
 */
import "server-only";
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { PILLARS, getSubsectionById } from "./dag";
import { getCurriculum } from "./curriculum";
import type { LessonFrontmatter, Pillar } from "./types";

const CONTENT_DIR = path.join(process.cwd(), "content");

export type ContentStatus = "available" | "coming-soon";

function lessonPath(pillar: Pillar, subId: string, lessonId: string): string {
  return path.join(CONTENT_DIR, pillar.slug, subId, `${lessonId}.mdx`);
}

/** True when an authored MDX file exists for this lesson. */
export function lessonContentStatus(
  subId: string,
  lessonId: string,
): ContentStatus {
  const sub = getSubsectionById(subId);
  if (!sub) return "coming-soon";
  return fs.existsSync(lessonPath(sub.pillar, subId, lessonId))
    ? "available"
    : "coming-soon";
}

/** Number of authored (available) lessons in a subsection. */
export function availableLessonCount(subId: string): number {
  return getCurriculum(subId).filter(
    (l) => lessonContentStatus(subId, l.id) === "available",
  ).length;
}

/** A subsection is "available" once at least one of its lessons is authored. */
export function subsectionStatus(subId: string): ContentStatus {
  return availableLessonCount(subId) > 0 ? "available" : "coming-soon";
}

export interface LoadedLesson {
  frontmatter: LessonFrontmatter;
  body: string;
}

/** Read + parse a lesson MDX file. Returns null when not yet authored. */
export function loadLesson(
  subId: string,
  lessonId: string,
): LoadedLesson | null {
  const sub = getSubsectionById(subId);
  if (!sub) return null;
  const fp = lessonPath(sub.pillar, subId, lessonId);
  if (!fs.existsSync(fp)) return null;
  const raw = fs.readFileSync(fp, "utf8");
  const { data, content } = matter(raw);
  return { frontmatter: data as LessonFrontmatter, body: content };
}

export interface LessonNav {
  prev: { subId: string; id: string; title: string } | null;
  next: { subId: string; id: string; title: string } | null;
}

/** Previous/next lesson within the same subsection, by curriculum order. */
export function getLessonPrevNext(subId: string, lessonId: string): LessonNav {
  const lessons = getCurriculum(subId);
  const i = lessons.findIndex((l) => l.id === lessonId);
  const at = (j: number) =>
    lessons[j] ? { subId, id: lessons[j].id, title: lessons[j].title } : null;
  return { prev: i > 0 ? at(i - 1) : null, next: i >= 0 ? at(i + 1) : null };
}

export function getPillarByLetter(letter: string): Pillar | undefined {
  return PILLARS.find((p) => p.letter === letter.toUpperCase());
}
