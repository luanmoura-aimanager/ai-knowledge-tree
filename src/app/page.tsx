import Link from "next/link";
import { getSubsectionById } from "@/lib/dag";
import { allLessons, getLesson } from "@/lib/curriculum";
import { lessonContentStatus } from "@/lib/content";
import { Hero } from "@/components/Hero";
import { DashboardStats } from "@/components/DashboardStats";
import { FilterBar } from "@/components/FilterBar";
import { CollapseController } from "@/components/CollapseController";
import { PillarsSection } from "@/components/PillarsSection";
import { ConnectionsGraph } from "@/components/ConnectionsGraph";
import { LearningPaths } from "@/components/LearningPaths";
import { PathHighlightProvider } from "@/components/PathHighlightProvider";
import { getProgressMap, getResume, isSignedIn } from "@/lib/progress";

/**
 * Homepage = the dashboard. Server-rendered pillar grid with client islands for
 * interactivity. When signed in, the per-subsection progress overlay and the
 * big stats reflect the user's own study state (see DashboardStats / PillarsSection).
 */
export default async function HomePage() {
  const signedIn = await isSignedIn();
  const progress = signedIn ? await getProgressMap() : new Map();
  const resume = signedIn ? await getResume() : null;

  // Authored-lesson count for the anonymous big-stats (only shown when signed out).
  const availableLessons = signedIn
    ? 0
    : allLessons().filter(
        (l) => lessonContentStatus(l.subId, l.id) === "available",
      ).length;

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

      <FilterBar signedIn={signedIn} />
      <CollapseController />

      <DashboardStats
        signedIn={signedIn}
        progress={progress}
        availableLessons={availableLessons}
      />

      <PillarsSection progress={progress} signedIn={signedIn} />

      <PathHighlightProvider>
        <LearningPaths progress={progress} />

        <section className="max-w-[1280px] mx-auto px-6 py-8">
          <h2 className="text-2xl font-bold mb-1.5">
            Cross-pillar connections
          </h2>
          <p className="text-[var(--fg-dim)] text-sm max-w-2xl mb-6">
            Force-directed graph of subsections. Drag nodes, scroll to zoom, and
            click to pin a subsection and see its connections. Selecting a
            suggested path above lights up its subsections here.
          </p>
          <ConnectionsGraph />
        </section>
      </PathHighlightProvider>

      <footer className="max-w-[1280px] mx-auto px-6 py-10 border-t border-[var(--border)] text-sm text-[var(--fg-dim)]">
        <div className="flex gap-5 flex-wrap text-xs text-[var(--fg-mute)]">
          <span>Your progress:</span>
          <span className="text-[var(--good)]">✓ studied</span>
          <span className="text-[var(--partial)]">◐ in progress</span>
          <span>○ not started</span>
        </div>
        <div className="mt-4 text-sm">
          Any feedback, suggestions, or want to contribute? Get in touch:{" "}
          <a
            href="mailto:luanmisaelmoura@gmail.com"
            className="text-[var(--accent)] hover:underline"
          >
            luanmisaelmoura@gmail.com
          </a>
        </div>
      </footer>
    </>
  );
}
