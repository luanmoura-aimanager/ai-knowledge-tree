import { PILLARS } from "@/lib/dag";

/**
 * Dashboard hero: gradient title, one-paragraph framing, and a quick-nav row of
 * pillar letter chips that jump to each pillar card (`#<letter>`).
 */
export function Hero() {
  return (
    <div className="max-w-[1280px] mx-auto px-6 pt-12 pb-2">
      <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3 bg-gradient-to-r from-[#7aa2f7] via-[#bb9af7] to-[#f7768e] bg-clip-text text-transparent">
        🌳 AI Knowledge Tree
      </h1>
      <p className="text-[var(--fg-dim)] max-w-3xl leading-relaxed">
        Interactive map of the full DAG of Data Science, Machine Learning, Deep
        Learning, and <strong>AI Engineering</strong>. 10 pillars (A → J), with
        the cross-links that tie VAEs in Generative DL and Bayesian DL, Kalman
        in PGMs and Time Series, RAG in LLMs and AI Engineering.
      </p>

      <div className="flex gap-1.5 flex-wrap mt-5">
        {PILLARS.map((p) => (
          <a
            key={p.letter}
            href={`#${p.letter}`}
            className="w-8 h-8 rounded-md flex items-center justify-center font-bold text-sm text-[var(--bg)] no-underline transition-transform hover:-translate-y-0.5"
            style={{ background: p.color }}
            title={p.name}
          >
            {p.letter}
          </a>
        ))}
      </div>
    </div>
  );
}
