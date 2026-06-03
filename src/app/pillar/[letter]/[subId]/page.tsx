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
  const introParas = sub.intro?.split("\n\n").filter(Boolean) ?? [];
  const firstAvailable = lessons.find(
    (l) => lessonContentStatus(subId, l.id) === "available",
  );

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
        {lessons.length > 0
          ? `${lessons.length} lessons. Study in order; each one assumes the previous.`
          : "The curriculum for this discipline is still being defined."}
      </p>

      {introParas.length > 0 ? (
        <>
          <div className="max-w-2xl mb-8 flex flex-col gap-4">
            {introParas.map((para, i) => (
              <p key={i} className="text-[var(--fg)] leading-relaxed">
                {para}
              </p>
            ))}
          </div>

          {sub.prerequisites && sub.prerequisites.length > 0 && (
            <div
              className="card p-5 mb-8 max-w-2xl border-l-2"
              style={{ borderColor: pillar.color }}
            >
              <h2 className="text-sm font-semibold uppercase tracking-wider text-[var(--fg-dim)] mb-2">
                Before you start
              </h2>
              <ul className="list-disc pl-5 flex flex-col gap-1.5 text-sm text-[var(--fg-dim)]">
                {sub.prerequisites.map((req, i) => (
                  <li key={i}>{req}</li>
                ))}
              </ul>
            </div>
          )}

          {firstAvailable && (
            <Link
              href={`/pillar/${pillar.letter}/${subId}/${firstAvailable.id}`}
              className="inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-semibold no-underline text-[var(--bg)] transition-transform hover:-translate-y-0.5"
              style={{ backgroundColor: pillar.color }}
            >
              Start with lesson 1: {firstAvailable.title} →
            </Link>
          )}
        </>
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
