import { Suspense } from "react";
import { notFound } from "next/navigation";
import {
  LessonSidebar,
  DisciplineSidebarView,
} from "@/components/LessonSidebar";
import { getPillarByLetter, lessonContentStatus } from "@/lib/content";
import { getCurriculum, lessonKey } from "@/lib/curriculum";
import { getProgressMap } from "@/lib/progress";
import { getSubsectionById } from "@/lib/dag";
import { getPathSidebars } from "@/lib/path-sidebars";
import type { ProgressStatus } from "@/lib/progress";

export default async function DisciplineLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ letter: string; subId: string }>;
}) {
  const { letter, subId } = await params;
  const pillar = getPillarByLetter(letter);
  const sub = getSubsectionById(subId);
  if (!pillar || !sub || sub.pillar.letter !== pillar.letter) notFound();

  const lessons = getCurriculum(subId);
  const availableIds = lessons
    .filter((l) => lessonContentStatus(subId, l.id) === "available")
    .map((l) => l.id);

  // Per-lesson progress for this subsection (keyed by lessonId) drives the
  // discipline view; the full map (keyed "subId/lessonId") drives path mode,
  // whose steps cross subsections.
  const fullMap = await getProgressMap();
  const progress: Record<string, ProgressStatus> = {};
  for (const l of lessons) {
    const st = fullMap.get(lessonKey(subId, l.id));
    if (st) progress[l.id] = st;
  }
  const fullProgress = Object.fromEntries(fullMap);

  const paths = getPathSidebars();

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-10 flex flex-col lg:flex-row gap-10">
      <Suspense
        fallback={
          <DisciplineSidebarView
            pillar={pillar}
            subId={subId}
            subName={sub.name}
            lessons={lessons}
            availableIds={availableIds}
            progress={progress}
          />
        }
      >
        <LessonSidebar
          pillar={pillar}
          subId={subId}
          subName={sub.name}
          lessons={lessons}
          availableIds={availableIds}
          progress={progress}
          paths={paths}
          fullProgress={fullProgress}
        />
      </Suspense>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  );
}
