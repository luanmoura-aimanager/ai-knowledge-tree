"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Lesson, Pillar } from "@/lib/types";
import type { ProgressStatus } from "@/lib/progress";

/**
 * Sidebar shown inside a discipline (subsection): the discipline header and its
 * ordered lessons. The lesson matching the current route is tinted with the
 * pillar color; the trailing glyph reflects per-lesson progress.
 */
export function LessonSidebar({
  pillar,
  subId,
  subName,
  lessons,
  availableIds,
  progress = {},
}: {
  pillar: Pillar;
  subId: string;
  subName: string;
  lessons: Lesson[];
  availableIds: string[];
  progress?: Record<string, ProgressStatus>;
}) {
  const pathname = usePathname();
  const available = new Set(availableIds);

  const glyph = (lessonId: string) => {
    const st = progress[lessonId];
    if (st === "studied")
      return (
        <span className="text-[var(--good)]" title="studied">
          ✓
        </span>
      );
    if (st === "in-progress")
      return (
        <span className="text-[var(--partial)]" title="in progress">
          ◐
        </span>
      );
    return (
      <span className="text-[var(--fg-mute)] text-xs" title="not studied">
        ○
      </span>
    );
  };

  return (
    <aside className="w-full lg:w-[280px] lg:flex-shrink-0">
      <div className="lg:sticky lg:top-20">
        <Link
          href={`/pillar/${pillar.letter}/${subId}`}
          className="no-underline"
        >
          <div className="flex items-center gap-3 mb-1">
            <div
              className="w-9 h-9 rounded-md flex items-center justify-center font-bold text-[var(--bg)]"
              style={{ background: pillar.color }}
            >
              {subId}
            </div>
            <div className="font-semibold text-[var(--fg)] leading-tight">
              {subName}
            </div>
          </div>
        </Link>
        <div className="text-xs text-[var(--fg-mute)] mb-4 ml-12">
          {pillar.name}
        </div>

        <nav className="flex flex-col gap-0.5">
          {lessons.map((lesson, i) => {
            const href = `/pillar/${pillar.letter}/${subId}/${lesson.id}`;
            const active = pathname === href;
            return (
              <Link
                key={lesson.id}
                href={href}
                className="no-underline text-sm px-2.5 py-1.5 rounded-md flex items-center gap-2 transition-colors"
                style={
                  active
                    ? {
                        background: `color-mix(in srgb, ${pillar.color} 22%, transparent)`,
                        color: "var(--fg)",
                      }
                    : { color: "var(--fg-dim)" }
                }
              >
                <span className="font-mono text-xs text-[var(--fg-mute)] w-5 text-right">
                  {i + 1}
                </span>
                <span
                  className={`flex-1 ${available.has(lesson.id) ? "" : "opacity-60"}`}
                >
                  {lesson.title}
                </span>
                {glyph(lesson.id)}
              </Link>
            );
          })}
          {lessons.length === 0 && (
            <p className="text-sm text-[var(--fg-mute)] px-2.5">
              Curriculum coming soon.
            </p>
          )}
        </nav>

        <div className="mt-5 pt-4 border-t border-[var(--border)] text-xs text-[var(--fg-dim)] flex flex-col gap-1">
          <Link
            href={`/pillar/${pillar.letter}`}
            className="hover:text-[var(--fg)] no-underline"
          >
            ← {pillar.name}
          </Link>
          <Link href="/" className="hover:text-[var(--fg)] no-underline">
            ← Map
          </Link>
        </div>
      </div>
    </aside>
  );
}
