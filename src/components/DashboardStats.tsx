import { globalStats } from "@/lib/dag";
import { allLessons, lessonCount, lessonKey } from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";

/**
 * Big-number cards. Anonymous: lesson-centric map of the curriculum (lessons,
 * authored, pillars, connections). Signed-in: the user's own study state
 * (studied / in progress / remaining) counted over real lessons.
 */
export function DashboardStats({
  signedIn,
  progress,
  availableLessons = 0,
}: {
  signedIn?: boolean;
  progress?: ProgressMap;
  availableLessons?: number;
}) {
  const s = globalStats();
  const total = lessonCount();

  if (signedIn && progress) {
    // Count over real lessons only, so this matches the per-pillar badges
    // (raw map values could include keys for removed/renamed lessons).
    let studied = 0;
    let inProgress = 0;
    for (const l of allLessons()) {
      const st = progress.get(lessonKey(l.subId, l.id));
      if (st === "studied") studied++;
      else if (st === "in-progress") inProgress++;
    }
    const remaining = Math.max(0, total - studied - inProgress);
    const pct = total > 0 ? Math.round((studied / total) * 100) : 0;
    return (
      <Wrap>
        <BigStat n={total} label="Lessons" sub={`${s.nPillars} pillars`} />
        <BigStat
          n={studied}
          label="✓ Studied"
          sub={`${pct}% of curriculum`}
          color="var(--good)"
        />
        <BigStat
          n={inProgress}
          label="◐ In progress"
          sub="resume"
          color="var(--partial)"
        />
        <BigStat
          n={remaining}
          label="○ Remaining"
          sub="to study"
          color="var(--gap)"
        />
        <BigStat n={s.total} label="Topics" sub="in the domain" />
        <BigStat
          n={s.nConnections}
          label="🔗 Connections"
          sub="cross-pillar"
          color="var(--accent)"
        />
      </Wrap>
    );
  }

  const pctAvail = total > 0 ? Math.round((availableLessons / total) * 100) : 0;
  return (
    <Wrap>
      <BigStat
        n={total}
        label="Lessons"
        sub={`${s.nPillars} pillars · ${s.nSubsections} subsections`}
      />
      <BigStat
        n={availableLessons}
        label="✓ Available"
        sub={`${pctAvail}% authored`}
        color="var(--good)"
      />
      <BigStat n={s.nPillars} label="Pillars" sub="subject areas" />
      <BigStat n={s.nSubsections} label="Disciplines" sub="subsections" />
      <BigStat n={s.total} label="Topics" sub="in the domain" />
      <BigStat
        n={s.nConnections}
        label="🔗 Connections"
        sub="cross-pillar"
        color="var(--accent)"
      />
    </Wrap>
  );
}

function Wrap({ children }: { children: React.ReactNode }) {
  return (
    <div className="max-w-[1280px] mx-auto px-6 pt-4 pb-2">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {children}
      </div>
    </div>
  );
}

function BigStat({
  n,
  label,
  sub,
  color,
}: {
  n: number;
  label: string;
  sub?: string;
  color?: string;
}) {
  return (
    <div className="card p-4 relative overflow-hidden">
      <div
        className="absolute top-0 left-0 right-0 h-0.5"
        style={{ background: color ?? "var(--accent)" }}
      />
      <div className="text-3xl font-extrabold leading-none">{n}</div>
      <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mt-1.5">
        {label}
      </div>
      {sub && <div className="text-xs text-[var(--fg-mute)] mt-1">{sub}</div>}
    </div>
  );
}
