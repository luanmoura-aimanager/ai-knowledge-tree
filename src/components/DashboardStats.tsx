import { globalStats } from "@/lib/dag";
import { lessonCount } from "@/lib/curriculum";
import type { ProgressMap } from "@/lib/progress";

/**
 * Big-number cards. Anonymous: the domain map (topics, coverage, connections).
 * Signed-in: the user's own study state: subsections studied / in-progress /
 * remaining: alongside the fixed domain totals.
 */
export function DashboardStats({
  signedIn,
  progress,
}: {
  signedIn?: boolean;
  progress?: ProgressMap;
}) {
  const s = globalStats();

  if (signedIn && progress) {
    const studied = [...progress.values()].filter(
      (v) => v === "studied",
    ).length;
    const inProgress = [...progress.values()].filter(
      (v) => v === "in-progress",
    ).length;
    const total = lessonCount();
    const remaining = Math.max(0, total - studied - inProgress);
    const pct = total > 0 ? Math.round((studied / total) * 100) : 0;
    return (
      <Wrap>
        <BigStat n={total} label="Lições" sub={`${s.nPillars} pilares`} />
        <BigStat
          n={studied}
          label="✓ Estudadas"
          sub={`${pct}% do currículo`}
          color="var(--good)"
        />
        <BigStat
          n={inProgress}
          label="◐ Em progresso"
          sub="retomar"
          color="var(--partial)"
        />
        <BigStat
          n={remaining}
          label="○ Restantes"
          sub="a estudar"
          color="var(--gap)"
        />
        <BigStat n={s.total} label="Tópicos" sub="no domínio" />
        <BigStat
          n={s.nConnections}
          label="🔗 Conexões"
          sub="cruzadas"
          color="var(--accent)"
        />
      </Wrap>
    );
  }

  const pctOverall = Math.round(((s.cov + s.par * 0.5) / s.total) * 100);
  return (
    <Wrap>
      <BigStat
        n={s.total}
        label="Tópicos"
        sub={`${s.nPillars} pilares · ${s.nSubsections} subseções`}
      />
      <BigStat
        n={s.cov}
        label="✓ Cobertos"
        sub={`${pctOverall}% do mapa`}
        color="var(--good)"
      />
      <BigStat
        n={s.par}
        label="◐ Parciais"
        sub="mencionados"
        color="var(--partial)"
      />
      <BigStat n={s.gap} label="○ Gaps" sub="a expandir" color="var(--gap)" />
      <BigStat
        n={s.hot}
        label="★ Hot"
        sub={`${s.hotGap} hot gaps`}
        color="var(--hot)"
      />
      <BigStat
        n={s.nConnections}
        label="🔗 Conexões"
        sub="cruzadas"
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
