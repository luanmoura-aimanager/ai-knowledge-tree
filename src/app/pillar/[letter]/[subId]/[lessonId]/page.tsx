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
import { getPathPrevNext } from "@/lib/path-sidebars";
import { MdxContent } from "@/components/mdx/MdxContent";
import { StudyProgressControls } from "@/components/StudyProgressControls";

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
  searchParams,
}: {
  params: Promise<{ letter: string; subId: string; lessonId: string }>;
  searchParams: Promise<{ path?: string; i?: string }>;
}) {
  const { letter, subId, lessonId } = await params;
  const { path: pathSlug, i: pathIndex } = await searchParams;
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

  // When following a path (`?path=<slug>&i=<step>`), prev/next walk the path's
  // expanded sequence (carrying the query so the next page stays in path mode);
  // otherwise they move within the current discipline.
  const pathNav = pathSlug
    ? getPathPrevNext(pathSlug, Number(pathIndex))
    : { prev: null, next: null };
  const query = (i: number) => `?path=${pathSlug}&i=${i}`;
  const fallback = getLessonPrevNext(subId, lessonId);
  const prev = pathNav.prev
    ? {
        href: `/pillar/${pathNav.prev.letter}/${pathNav.prev.subId}/${pathNav.prev.lessonId}${query(pathNav.prev.index)}`,
        title: pathNav.prev.title,
      }
    : fallback.prev
      ? {
          href: `/pillar/${pillar.letter}/${fallback.prev.subId}/${fallback.prev.id}`,
          title: fallback.prev.title,
        }
      : null;
  const next = pathNav.next
    ? {
        href: `/pillar/${pathNav.next.letter}/${pathNav.next.subId}/${pathNav.next.lessonId}${query(pathNav.next.index)}`,
        title: pathNav.next.title,
      }
    : fallback.next
      ? {
          href: `/pillar/${pillar.letter}/${fallback.next.subId}/${fallback.next.id}`,
          title: fallback.next.title,
        }
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
    </article>
  );
}
