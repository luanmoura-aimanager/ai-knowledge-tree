import Link from "next/link";
import { notFound } from "next/navigation";
import { PILLARS } from "@/lib/dag";
import { getPillarByLetter } from "@/lib/content";
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

  const introParas = pillar.intro?.split("\n\n").filter(Boolean) ?? [];

  return (
    <div className="max-w-[1100px] mx-auto px-6 py-10">
      <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-1">
        <Link href="/" className="no-underline hover:text-[var(--fg)]">
          Map
        </Link>{" "}
        / Pillar {pillar.letter}
      </div>
      <h1
        className="text-3xl font-bold tracking-tight mb-2"
        style={{ color: pillar.color }}
      >
        {pillar.name}
      </h1>
      <p className="text-[var(--fg-dim)] max-w-2xl mb-6">{pillar.tagline}</p>

      {introParas.length > 0 && (
        <div className="max-w-2xl mb-8 flex flex-col gap-4">
          {introParas.map((para, i) => (
            <p key={i} className="text-[var(--fg)] leading-relaxed">
              {para}
            </p>
          ))}
        </div>
      )}

      {pillar.prerequisites && pillar.prerequisites.length > 0 && (
        <div
          className="card p-5 mb-8 max-w-2xl border-l-2"
          style={{ borderColor: pillar.color }}
        >
          <h2 className="text-sm font-semibold uppercase tracking-wider text-[var(--fg-dim)] mb-2">
            Before you start
          </h2>
          <ul className="list-disc pl-5 flex flex-col gap-1.5 text-sm text-[var(--fg-dim)]">
            {pillar.prerequisites.map((req, i) => (
              <li key={i}>{req}</li>
            ))}
          </ul>
        </div>
      )}

      <h2 className="text-sm font-semibold uppercase tracking-wider text-[var(--fg-dim)] mb-3">
        Disciplines in this pillar
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {pillar.subs.map((sub) => {
          const total = getCurriculum(sub.id).length;
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
                {total > 0 ? `${total} lessons` : "curriculum coming soon"}
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
