import { Suspense } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSubsectionById } from "@/lib/dag";
import {
  getPillarByLetter,
  loadLesson,
  getLessonPrevNext,
} from "@/lib/content";
import {
  getCurriculum,
  getLesson,
  allLessons,
  lessonKey,
} from "@/lib/curriculum";
import { getProgressMap, isSignedIn } from "@/lib/progress";
import { getPathSidebars } from "@/lib/path-sidebars";
import { MdxContent } from "@/components/mdx/MdxContent";
import { StudyProgressControls } from "@/components/StudyProgressControls";
import { LessonPrevNext, PrevNextNav } from "@/components/LessonPrevNext";

export function generateStaticParams() {
  return allLessons().flatMap((l) => {
    const sub = getSubsectionById(l.subId);
    return sub
      ? [{ letter: sub.pillar.letter, subId: l.subId, lessonId: l.id }]
      : [];
  });
}

function PrereqLink({ token }: { token: string }) {
  // token is "lessonId" (same subsection) or "subId/lessonId"
  const [a, b] = token.includes("/") ? token.split("/") : [null, token];
  const subId = a ?? "";
  const lessonId = b;
  const sub = subId ? getSubsectionById(subId) : null;
  const lesson = subId ? getLesson(subId, lessonId) : null;
  if (!sub || !lesson) return <span className="font-mono">{token}</span>;
  return (
    <Link
      href={`/pillar/${sub.pillar.letter}/${subId}/${lessonId}`}
      className="no-underline hover:text-[var(--fg)]"
      style={{ color: sub.pillar.color }}
    >
      {lesson.title}
    </Link>
  );
}

export default async function LessonPage({
  params,
}: {
  params: Promise<{ letter: string; subId: string; lessonId: string }>;
}) {
  const { letter, subId, lessonId } = await params;
  const pillar = getPillarByLetter(letter);
  const sub = getSubsectionById(subId);
  const lesson = getLesson(subId, lessonId);
  if (!pillar || !sub || sub.pillar.letter !== pillar.letter || !lesson)
    notFound();

  // Resolve cross-subsection prerequisites: bare id ⇒ this subId.
  const prereqs = (lesson.prerequisites ?? []).map((t) =>
    t.includes("/") ? t : `${subId}/${t}`,
  );

  const loaded = loadLesson(subId, lessonId);
  const fm = loaded?.frontmatter;

  // Discipline-order prev/next, computed here; the client LessonPrevNext swaps to
  // path order when the lesson was opened from a path (`?path=`). Path mode is
  // resolved client-side (like the sidebar) so it works even when this page is
  // statically prerendered and the server can't see the query.
  const fallback = getLessonPrevNext(subId, lessonId);
  const discLink = (l: { subId: string; id: string; title: string } | null) =>
    l
      ? { href: `/pillar/${pillar.letter}/${l.subId}/${l.id}`, title: l.title }
      : null;

  const key = lessonKey(subId, lessonId);
  const showControls = await isSignedIn();
  const myStatus = showControls
    ? ((await getProgressMap()).get(key) ?? null)
    : null;

  return (
    <article className="min-w-0">
      <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-1">
        <Link
          href={`/pillar/${pillar.letter}/${subId}`}
          className="no-underline hover:text-[var(--fg)]"
        >
          {sub.id} · {sub.name}
        </Link>{" "}
        · lesson {lesson.order}
      </div>
      <h1 className="text-3xl font-bold tracking-tight mb-3">
        {fm?.title ?? lesson.title}
      </h1>

      <p
        className="text-[var(--fg-dim)] max-w-2xl leading-relaxed border-l-2 pl-4 my-4"
        style={{ borderColor: pillar.color }}
      >
        {fm?.goal ?? lesson.goal}
      </p>

      <div className="flex items-center gap-4 text-xs text-[var(--fg-mute)] mb-6 flex-wrap">
        {fm?.estimatedMinutes ? <span>⏱ {fm.estimatedMinutes} min</span> : null}
        {prereqs.length > 0 && (
          <span className="flex items-center gap-1.5 flex-wrap">
            Prerequisites:
            {prereqs.map((t) => (
              <PrereqLink key={t} token={t} />
            ))}
          </span>
        )}
      </div>

      {showControls && (
        <StudyProgressControls itemKey={key} initial={myStatus} />
      )}

      {loaded ? (
        <MdxContent source={loaded.body} />
      ) : (
        <div className="card p-6 text-[var(--fg-dim)]">
          This lesson has not been written yet. Planned goal: {lesson.goal}
        </div>
      )}

      <Suspense
        fallback={
          <PrevNextNav
            prev={discLink(fallback.prev)}
            next={discLink(fallback.next)}
          />
        }
      >
        <LessonPrevNext
          paths={getPathSidebars()}
          disciplinePrev={discLink(fallback.prev)}
          disciplineNext={discLink(fallback.next)}
        />
      </Suspense>
    </article>
  );
}
