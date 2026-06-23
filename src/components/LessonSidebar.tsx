"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useSyncExternalStore } from "react";
import type { Lesson, Pillar, PathSidebar } from "@/lib/types";
import type { ProgressStatus } from "@/lib/progress";
import { groupLabelOf } from "@/lib/path-groups";

const STORAGE_KEY = "lessonSidebarCollapsed";

/**
 * Tiny external store for the collapse flag so every LessonSidebar instance
 * (and a fresh one after navigation) reflects the same persisted choice and
 * re-renders in sync, without setState-in-effect or hydration mismatch.
 */
const listeners = new Set<() => void>();

function subscribe(cb: () => void) {
  listeners.add(cb);
  window.addEventListener("storage", cb);
  return () => {
    listeners.delete(cb);
    window.removeEventListener("storage", cb);
  };
}

function isCollapsed() {
  return localStorage.getItem(STORAGE_KEY) === "1";
}

function setCollapsedFlag(next: boolean) {
  localStorage.setItem(STORAGE_KEY, next ? "1" : "0");
  listeners.forEach((cb) => cb());
}

function useCollapsed() {
  return useSyncExternalStore(subscribe, isCollapsed, () => false);
}

function glyph(st?: ProgressStatus) {
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
}

/** The thin rail shown when the sidebar is collapsed: links back to the discipline. */
function CollapsedRail({
  pillar,
  subId,
  subName,
  onExpand,
}: {
  pillar: Pillar;
  subId: string;
  subName: string;
  onExpand: () => void;
}) {
  return (
    <aside className="w-full lg:w-auto lg:flex-shrink-0">
      <div className="lg:sticky lg:top-20 flex lg:flex-col items-center gap-3">
        <button
          type="button"
          onClick={onExpand}
          title="Show lessons"
          aria-label="Show lessons"
          aria-expanded={false}
          className="w-9 h-9 rounded-md flex items-center justify-center text-[var(--fg-dim)] border border-[var(--border)] hover:text-[var(--fg)] hover:border-[var(--fg-mute)] transition-colors"
        >
          <ExpandIcon />
        </button>
        <Link
          href={`/pillar/${pillar.letter}/${subId}`}
          title={`${subId} ${subName}`}
          className="w-9 h-9 rounded-md flex items-center justify-center font-bold text-[var(--bg)] no-underline"
          style={{ background: pillar.color }}
        >
          {subId}
        </Link>
      </div>
    </aside>
  );
}

/**
 * Sidebar shown inside a discipline (subsection): the discipline header and its
 * ordered lessons. The lesson matching the current route is tinted with the
 * pillar color; the trailing glyph reflects per-lesson progress.
 *
 * This view reads no search params, so it doubles as the Suspense fallback for
 * the path-aware {@link LessonSidebar} (which does, and would otherwise force a
 * suspense boundary during static prerendering).
 */
export function DisciplineSidebarView({
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
  const collapsed = useCollapsed();
  const toggle = () => setCollapsedFlag(!collapsed);

  if (collapsed) {
    return (
      <CollapsedRail
        pillar={pillar}
        subId={subId}
        subName={subName}
        onExpand={toggle}
      />
    );
  }

  return (
    <aside className="w-full lg:w-[280px] lg:flex-shrink-0">
      <div className="lg:sticky lg:top-20 lg:max-h-[calc(100vh-6rem)] lg:flex lg:flex-col rounded-xl bg-[#161e47] border border-[#2b3566] p-4">
        <div className="flex items-start gap-2 mb-1 flex-shrink-0">
          <Link
            href={`/pillar/${pillar.letter}/${subId}`}
            className="no-underline flex-1 min-w-0"
          >
            <div className="flex items-center gap-3">
              <div
                className="w-9 h-9 rounded-md flex items-center justify-center font-bold text-[var(--bg)] flex-shrink-0"
                style={{ background: pillar.color }}
              >
                {subId}
              </div>
              <div className="font-semibold text-[var(--fg)] leading-tight">
                {subName}
              </div>
            </div>
          </Link>
          <button
            type="button"
            onClick={toggle}
            title="Hide lessons"
            aria-label="Hide lessons"
            aria-expanded={true}
            className="w-8 h-8 -mr-1 rounded-md flex items-center justify-center text-[var(--fg-mute)] hover:text-[var(--fg)] hover:bg-[var(--surface-2)] transition-colors flex-shrink-0"
          >
            <CollapseIcon />
          </button>
        </div>
        <div className="text-xs text-[var(--fg-mute)] mb-4 ml-12 flex-shrink-0">
          {pillar.name}
        </div>

        <nav className="lesson-scroll flex flex-col gap-0.5 lg:min-h-0 lg:flex-1 lg:overflow-y-auto -mr-1.5 pr-1.5">
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
                {glyph(progress[lesson.id])}
              </Link>
            );
          })}
          {lessons.length === 0 && (
            <p className="text-sm text-[var(--fg-mute)] px-2.5">
              Curriculum coming soon.
            </p>
          )}
        </nav>

        <div className="mt-5 pt-4 border-t border-[var(--border)] text-xs text-[var(--fg-dim)] flex flex-col gap-1 flex-shrink-0">
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

/**
 * Sidebar shown when a lesson was opened from a suggested path (`?path=<slug>`):
 * the path's prerequisite-closed lesson sequence in order, grouped by section,
 * with the active step tinted by its pillar color. A "View discipline instead"
 * link drops the path context back to the normal discipline sidebar.
 */
function PathSidebarView({
  path,
  index,
  pillar,
  subId,
  subName,
  fullProgress,
}: {
  path: PathSidebar;
  index: string | null;
  pillar: Pillar;
  subId: string;
  subName: string;
  fullProgress: Record<string, ProgressStatus>;
}) {
  const pathname = usePathname();
  const collapsed = useCollapsed();
  const toggle = () => setCollapsedFlag(!collapsed);

  if (collapsed) {
    return (
      <CollapsedRail
        pillar={pillar}
        subId={subId}
        subName={subName}
        onExpand={toggle}
      />
    );
  }

  // The active step: the explicit `?i=` index when present, else the first step
  // whose route matches (a path may revisit a lesson, so `?i=` disambiguates).
  const idxNum = index != null && index !== "" ? Number(index) : NaN;
  const activeIdx = Number.isInteger(idxNum)
    ? idxNum
    : path.steps.findIndex(
        (s) => `/pillar/${s.letter}/${s.subId}/${s.lessonId}` === pathname,
      );

  return (
    <aside className="w-full lg:w-[280px] lg:flex-shrink-0">
      <div className="lg:sticky lg:top-20 lg:max-h-[calc(100vh-6rem)] lg:flex lg:flex-col rounded-xl bg-[#161e47] border border-[#2b3566] p-4">
        <div className="flex items-start gap-2 mb-1 flex-shrink-0">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <div
              className="w-9 h-9 rounded-md flex items-center justify-center font-bold text-[var(--bg)] flex-shrink-0"
              style={{ background: path.color }}
              aria-hidden="true"
            >
              ↳
            </div>
            <div className="font-semibold text-[var(--fg)] leading-tight min-w-0">
              {path.name}
            </div>
          </div>
          <button
            type="button"
            onClick={toggle}
            title="Hide lessons"
            aria-label="Hide lessons"
            aria-expanded={true}
            className="w-8 h-8 -mr-1 rounded-md flex items-center justify-center text-[var(--fg-mute)] hover:text-[var(--fg)] hover:bg-[var(--surface-2)] transition-colors flex-shrink-0"
          >
            <CollapseIcon />
          </button>
        </div>
        <div className="text-xs mb-4 ml-12 flex-shrink-0 text-[var(--fg-mute)]">
          Following this path ·{" "}
          <Link
            href={pathname}
            className="text-[var(--fg-dim)] hover:text-[var(--fg)] underline-offset-2 hover:underline"
          >
            View discipline instead
          </Link>
        </div>

        <nav className="lesson-scroll flex flex-col gap-0.5 lg:min-h-0 lg:flex-1 lg:overflow-y-auto -mr-1.5 pr-1.5">
          {path.steps.map((step, i) => {
            const group = groupLabelOf(step);
            const showHeader =
              group !== "" &&
              (i === 0 || groupLabelOf(path.steps[i - 1]) !== group);
            const base = `/pillar/${step.letter}/${step.subId}/${step.lessonId}`;
            const href = `${base}?path=${path.slug}&i=${i}`;
            const active = i === activeIdx;
            return (
              <div key={`${step.subId}/${step.lessonId}/${i}`}>
                {showHeader && (
                  <div className="text-[11px] font-semibold text-[var(--fg-dim)] mt-3 mb-1 px-2.5">
                    {group}
                  </div>
                )}
                <Link
                  href={href}
                  className="no-underline text-sm px-2.5 py-1.5 rounded-md flex items-center gap-2 transition-colors"
                  style={
                    active
                      ? {
                          background: `color-mix(in srgb, ${step.color} 22%, transparent)`,
                          color: "var(--fg)",
                        }
                      : { color: "var(--fg-dim)" }
                  }
                >
                  <span className="font-mono text-xs text-[var(--fg-mute)] w-5 text-right">
                    {i + 1}
                  </span>
                  <span
                    className="font-mono text-[10px] px-1 py-0.5 rounded shrink-0"
                    style={{
                      background: `color-mix(in srgb, ${step.color} 18%, transparent)`,
                      color: step.color,
                    }}
                  >
                    {step.subId}
                  </span>
                  <span
                    className={`flex-1 min-w-0 ${step.available ? "" : "opacity-60"}`}
                  >
                    {step.title}
                  </span>
                  {glyph(fullProgress[`${step.subId}/${step.lessonId}`])}
                </Link>
              </div>
            );
          })}
        </nav>

        <div className="mt-5 pt-4 border-t border-[var(--border)] text-xs text-[var(--fg-dim)] flex flex-col gap-1 flex-shrink-0">
          <Link href="/" className="hover:text-[var(--fg)] no-underline">
            ← Map
          </Link>
        </div>
      </div>
    </aside>
  );
}

/**
 * The in-discipline lesson navigator. By default it shows the current
 * discipline's lessons ({@link DisciplineSidebarView}); when the lesson was
 * opened from a suggested path (`?path=<slug>`), it instead lists that path's
 * lessons in order ({@link PathSidebarView}). A collapse toggle (persisted in
 * localStorage) carries across every discipline/lesson/path page.
 */
export function LessonSidebar({
  pillar,
  subId,
  subName,
  lessons,
  availableIds,
  progress = {},
  paths = [],
  fullProgress = {},
}: {
  pillar: Pillar;
  subId: string;
  subName: string;
  lessons: Lesson[];
  availableIds: string[];
  progress?: Record<string, ProgressStatus>;
  paths?: PathSidebar[];
  fullProgress?: Record<string, ProgressStatus>;
}) {
  const sp = useSearchParams();
  const slug = sp.get("path");
  const activePath = slug ? paths.find((p) => p.slug === slug) : null;

  if (activePath) {
    return (
      <PathSidebarView
        path={activePath}
        index={sp.get("i")}
        pillar={pillar}
        subId={subId}
        subName={subName}
        fullProgress={fullProgress}
      />
    );
  }

  return (
    <DisciplineSidebarView
      pillar={pillar}
      subId={subId}
      subName={subName}
      lessons={lessons}
      availableIds={availableIds}
      progress={progress}
    />
  );
}

function CollapseIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="1.5" y="2.5" width="13" height="11" rx="1.5" />
      <line x1="6" y1="2.5" x2="6" y2="13.5" />
      <polyline points="11.5 6 9.5 8 11.5 10" />
    </svg>
  );
}

function ExpandIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="1.5" y="2.5" width="13" height="11" rx="1.5" />
      <line x1="6" y1="2.5" x2="6" y2="13.5" />
      <polyline points="9.5 6 11.5 8 9.5 10" />
    </svg>
  );
}
