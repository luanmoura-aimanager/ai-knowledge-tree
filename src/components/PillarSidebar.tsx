"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Pillar } from "@/lib/types";
import type { ProgressStatus } from "@/lib/progress";
import { pillarStats } from "@/lib/dag";

/**
 * Left navigation for a pillar's study pages. Lists every subsection; the one
 * matching the current route is tinted with the pillar color. The trailing
 * glyph reflects the user's progress (✓ studied / ◐ in-progress / ○ otherwise).
 */
export function PillarSidebar({
  pillar,
  availableIds,
  progress = {},
}: {
  pillar: Pillar;
  availableIds: string[];
  progress?: Record<string, ProgressStatus>;
}) {
  const pathname = usePathname();
  const s = pillarStats(pillar);
  const available = new Set(availableIds);

  const glyph = (subId: string) => {
    const st = progress[subId];
    if (st === "studied")
      return (
        <span className="text-[var(--good)]" title="estudado">
          ✓
        </span>
      );
    if (st === "in-progress")
      return (
        <span className="text-[var(--partial)]" title="em progresso">
          ◐
        </span>
      );
    return (
      <span className="text-[var(--fg-mute)] text-xs" title="não estudado">
        ○
      </span>
    );
  };

  return (
    <aside className="w-full lg:w-[260px] lg:flex-shrink-0">
      <div className="lg:sticky lg:top-20">
        <Link href={`/pillar/${pillar.letter}`} className="no-underline">
          <div className="flex items-center gap-3 mb-3">
            <div
              className="w-9 h-9 rounded-md flex items-center justify-center font-bold text-[var(--bg)]"
              style={{ background: pillar.color }}
            >
              {pillar.letter}
            </div>
            <div className="font-semibold text-[var(--fg)]">{pillar.name}</div>
          </div>
        </Link>
        <div className="statbar mb-4">
          <div className="seg cov" style={{ width: `${s.pctCov}%` }} />
          <div className="seg par" style={{ width: `${s.pctPar}%` }} />
          <div className="seg gap" style={{ width: `${s.pctGap}%` }} />
        </div>

        <nav className="flex flex-col gap-0.5">
          {pillar.subs.map((sub) => {
            const href = `/pillar/${pillar.letter}/${sub.id}`;
            const active = pathname === href;
            return (
              <Link
                key={sub.id}
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
                <span
                  className="font-mono font-bold"
                  style={{ color: pillar.color }}
                >
                  {sub.id}
                </span>
                <span
                  className={`flex-1 ${available.has(sub.id) ? "" : "opacity-60"}`}
                >
                  {sub.name}
                </span>
                {glyph(sub.id)}
              </Link>
            );
          })}
        </nav>

        <div className="mt-5 pt-4 border-t border-[var(--border)] text-xs text-[var(--fg-dim)]">
          <Link href="/" className="hover:text-[var(--fg)] no-underline">
            ← Voltar ao mapa
          </Link>
        </div>
      </div>
    </aside>
  );
}
