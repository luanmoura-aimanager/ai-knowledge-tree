"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import type { PathSidebar } from "@/lib/types";
import { pathStepHref, resolveActiveStep } from "@/lib/path-url";

export type NavLink = { href: string; title: string } | null;

/**
 * Presentational prev/next nav. No hooks, so it doubles as the Suspense fallback
 * for {@link LessonPrevNext} (which reads `useSearchParams` and would otherwise
 * deopt the whole lesson page to client rendering during static prerender).
 */
export function PrevNextNav({ prev, next }: { prev: NavLink; next: NavLink }) {
  return (
    <nav className="flex justify-between gap-4 mt-12 pt-6 border-t border-[var(--border)]">
      {prev ? (
        <Link
          href={prev.href}
          className="card p-4 no-underline flex-1 max-w-[48%]"
        >
          <div className="text-xs text-[var(--fg-mute)]">← Previous</div>
          <div className="text-sm font-semibold text-[var(--fg)]">
            {prev.title}
          </div>
        </Link>
      ) : (
        <span className="flex-1 max-w-[48%]" />
      )}
      {next ? (
        <Link
          href={next.href}
          className="card p-4 no-underline flex-1 max-w-[48%] text-right"
        >
          <div className="text-xs text-[var(--fg-mute)]">Next →</div>
          <div className="text-sm font-semibold text-[var(--fg)]">
            {next.title}
          </div>
        </Link>
      ) : (
        <span className="flex-1 max-w-[48%]" />
      )}
    </nav>
  );
}

/**
 * The bottom prev/next nav. By default it moves within the discipline (the
 * `disciplinePrev`/`disciplineNext` computed on the server). When the lesson was
 * opened from a suggested path (`?path=<slug>&i=<step>`), it instead walks the
 * path's expanded sequence — and at the ends there is simply no neighbor (no
 * fall-back to discipline order, which would eject the reader from the path).
 *
 * Client-side (mirrors the sidebar) so it honors the query even on statically
 * prerendered lesson pages, where the server can't see `searchParams`. Wrap it in
 * a Suspense boundary whose fallback is a discipline-order {@link PrevNextNav}.
 */
export function LessonPrevNext({
  paths,
  disciplinePrev,
  disciplineNext,
}: {
  paths: PathSidebar[];
  disciplinePrev: NavLink;
  disciplineNext: NavLink;
}) {
  const sp = useSearchParams();
  const pathname = usePathname();
  const slug = sp.get("path");
  const active = slug ? paths.find((p) => p.slug === slug) : undefined;

  let prev = disciplinePrev;
  let next = disciplineNext;
  if (active) {
    const i = resolveActiveStep(active.steps, sp.get("i"), pathname);
    if (i >= 0) {
      const at = (j: number): NavLink => {
        const s = active.steps[j];
        return s
          ? { href: pathStepHref(active.slug, s, j), title: s.title }
          : null;
      };
      prev = at(i - 1);
      next = at(i + 1);
    }
  }

  return <PrevNextNav prev={prev} next={next} />;
}
