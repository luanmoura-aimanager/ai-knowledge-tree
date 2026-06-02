import Link from "next/link";
import { PILLARS, getSubsectionById } from "@/lib/dag";
import { getLesson } from "@/lib/curriculum";
import { Hero } from "@/components/Hero";
import { DashboardStats } from "@/components/DashboardStats";
import { FilterBar } from "@/components/FilterBar";
import { CollapseController } from "@/components/CollapseController";
import { PillarCard } from "@/components/PillarCard";
import { ConnectionsGraph } from "@/components/ConnectionsGraph";
import { LearningPaths } from "@/components/LearningPaths";
import { getProgressMap, getResume, isSignedIn } from "@/lib/progress";

/**
 * Homepage = the dashboard. Server-rendered pillar grid with client islands for
 * interactivity. When signed in, the per-subsection progress overlay and the
 * big stats reflect the user's own study state (see DashboardStats / PillarCard).
 */
export default async function HomePage() {
  const signedIn = await isSignedIn();
  const progress = signedIn ? await getProgressMap() : new Map();
  const resume = signedIn ? await getResume() : null;

  // resume.key is "subId/lessonId"; resolve to a deep link + label.
  let resumeHref: string | null = null;
  let resumeLabel = "";
  if (resume) {
    const [rSubId, rLessonId] = resume.key.split("/");
    const rSub = getSubsectionById(rSubId);
    const rLesson =
      rSubId && rLessonId ? getLesson(rSubId, rLessonId) : undefined;
    if (rSub && rLesson) {
      resumeHref = `/pillar/${rSub.pillar.letter}/${rSubId}/${rLessonId}`;
      resumeLabel = `${rSub.id} · ${rLesson.title}`;
    }
  }

  return (
    <>
      <Hero />

      {resumeHref && (
        <div className="max-w-[1280px] mx-auto px-6 pt-2">
          <Link
            href={resumeHref}
            className="inline-flex items-center gap-2 btn active no-underline"
          >
            ▶ Continue: {resumeLabel}
          </Link>
        </div>
      )}

      <DashboardStats signedIn={signedIn} progress={progress} />

      <FilterBar />
      <CollapseController />

      <div className="max-w-[1280px] mx-auto px-6 pt-4 pb-4">
        {PILLARS.map((p) => (
          <PillarCard
            key={p.letter}
            pillar={p}
            progress={progress}
            signedIn={signedIn}
          />
        ))}
      </div>

      <section className="max-w-[1280px] mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold mb-1.5">Cross-pillar connections</h2>
        <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
          Force-directed graph of subsections. Drag nodes, scroll to zoom, and
          click to pin a subsection and see its connections.
        </p>
        <ConnectionsGraph />
      </section>

      <LearningPaths />

      <footer className="max-w-[1280px] mx-auto px-6 py-10 border-t border-[var(--border)] text-sm text-[var(--fg-dim)]">
        <div className="flex gap-5 flex-wrap">
          <span>✓ covered</span>
          <span>◐ partial</span>
          <span>○ gap</span>
          <span className="text-[var(--hot)]">★ hot (2023–2025)</span>
        </div>
        <div className="flex gap-5 flex-wrap mt-2 text-xs text-[var(--fg-mute)]">
          <span>Your progress:</span>
          <span className="text-[var(--good)]">✓ studied</span>
          <span className="text-[var(--partial)]">◐ in progress</span>
          <span>○ not started</span>
        </div>
      </footer>
    </>
  );
}
