import Link from "next/link";
import { notFound } from "next/navigation";
import { PILLARS, getSubsectionById } from "@/lib/dag";
import { getPillarByLetter, lessonContentStatus } from "@/lib/content";
import { getCurriculum } from "@/lib/curriculum";

export function generateStaticParams() {
  return PILLARS.flatMap((p) =>
    p.subs.map((s) => ({ letter: p.letter, subId: s.id })),
  );
}

export default async function DisciplineOverviewPage({
  params,
}: {
  params: Promise<{ letter: string; subId: string }>;
}) {
  const { letter, subId } = await params;
  const pillar = getPillarByLetter(letter);
  const sub = getSubsectionById(subId);
  if (!pillar || !sub || sub.pillar.letter !== pillar.letter) notFound();

  const lessons = getCurriculum(subId);

  return (
    <article>
      <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-1">
        <Link
          href={`/pillar/${pillar.letter}`}
          className="no-underline hover:text-[var(--fg)]"
        >
          {pillar.letter}. {pillar.name}
        </Link>
      </div>
      <h1 className="text-3xl font-bold tracking-tight mb-2">
        <span className="font-mono mr-2" style={{ color: pillar.color }}>
          {sub.id}
        </span>
        {sub.name}
      </h1>
      <p className="text-[var(--fg-dim)] mb-6">
        {lessons.length} lessons. Study in order; each one assumes the previous.
      </p>

      {lessons.length === 0 ? (
        <div className="card p-6 text-[var(--fg-dim)]">
          The curriculum for this discipline is still being defined.
        </div>
      ) : (
        <ol className="flex flex-col gap-2 list-none p-0 m-0">
          {lessons.map((lesson, i) => {
            const available =
              lessonContentStatus(subId, lesson.id) === "available";
            const inner = (
              <>
                <span className="font-mono text-sm text-[var(--fg-mute)] w-6 text-right shrink-0">
                  {i + 1}
                </span>
                <span className="flex-1">
                  <span className="font-semibold text-[var(--fg)]">
                    {lesson.title}
                  </span>
                  <span className="block text-xs text-[var(--fg-mute)] mt-0.5">
                    {lesson.goal}
                  </span>
                </span>
                {!available && (
                  <span className="text-xs shrink-0 text-[var(--fg-mute)]">
                    coming soon
                  </span>
                )}
              </>
            );
            const cls = "card p-4 flex items-start gap-3 no-underline";
            return (
              <li key={lesson.id}>
                {available ? (
                  <Link
                    href={`/pillar/${pillar.letter}/${subId}/${lesson.id}`}
                    className={`${cls} transition-transform hover:-translate-y-0.5`}
                  >
                    {inner}
                  </Link>
                ) : (
                  <div className={`${cls} opacity-70`}>{inner}</div>
                )}
              </li>
            );
          })}
        </ol>
      )}
    </article>
  );
}
