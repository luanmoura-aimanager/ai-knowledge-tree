import Link from "next/link";
import { notFound } from "next/navigation";
import { PILLARS } from "@/lib/dag";
import {
  getPillarByLetter,
  subsectionStatus,
  availableLessonCount,
} from "@/lib/content";
import { getCurriculum } from "@/lib/curriculum";

export function generateStaticParams() {
  return PILLARS.map((p) => ({ letter: p.letter }));
}

export default async function PillarOverviewPage({
  params,
}: {
  params: Promise<{ letter: string }>;
}) {
  const { letter } = await params;
  const pillar = getPillarByLetter(letter);
  if (!pillar) notFound();

  return (
    <div className="max-w-[1100px] mx-auto px-6 py-10">
      <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-1">
        <Link href="/" className="no-underline hover:text-[var(--fg)]">
          Mapa
        </Link>{" "}
        / Pilar {pillar.letter}
      </div>
      <h1
        className="text-3xl font-bold tracking-tight mb-2"
        style={{ color: pillar.color }}
      >
        {pillar.name}
      </h1>
      <p className="text-[var(--fg-dim)] max-w-2xl mb-6">{pillar.tagline}</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {pillar.subs.map((sub) => {
          const total = getCurriculum(sub.id).length;
          const done = availableLessonCount(sub.id);
          const available = subsectionStatus(sub.id) === "available";
          return (
            <Link
              key={sub.id}
              href={`/pillar/${pillar.letter}/${sub.id}`}
              className="card p-4 no-underline block transition-transform hover:-translate-y-0.5"
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="font-mono font-bold"
                  style={{ color: pillar.color }}
                >
                  {sub.id}
                </span>
                <span className="font-semibold text-[var(--fg)]">
                  {sub.name}
                </span>
              </div>
              <div className="text-xs text-[var(--fg-mute)]">
                {total > 0 ? (
                  <>
                    {total} lições ·{" "}
                    {available ? (
                      <span className="text-[var(--good)]">
                        {done} disponíveis
                      </span>
                    ) : (
                      <span>em breve</span>
                    )}
                  </>
                ) : (
                  <span>currículo em breve</span>
                )}
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
