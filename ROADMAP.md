# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-06-12 (Calculus pillar L shipped; Causal Inference ML
remains queued).

## Backlog

### New pillars to author

- **Causal Inference / Machine Learning pillar.** A new top-level pillar covering
  causal inference and causal ML (e.g. potential outcomes, DAGs & do-calculus,
  confounding & adjustment, instrumental variables, propensity scores & matching,
  difference-in-differences, regression discontinuity, structural causal models,
  causal discovery, heterogeneous treatment effects / uplift modeling,
  double/debiased ML, causal forests). Follow the standard pillar workflow in
  CLAUDE.md ("Author a complete pillar"): add subsections + topics to
  `src/lib/dag.ts`, author `src/lib/curriculum/<Letter>.ts`, write all lesson MDX
  (each with figures + exercises per STYLE.md), wire cross-pillar `CONNECTIONS`,
  then `npm run build`/`npm run lint`, open a PR, run `/code-review`, and print the
  PR link.
---

Four efforts shipped:

- **Calculus pillar L** (2026-06-12). New top-level pillar with 6 subsections
  (L1 limits & continuity, L2 differentiation, L3 integration & series, L4
  multivariable differentiation, L5 vector calculus & multiple integrals, L6
  multivariable optimization & the ML bridge), 35 lessons, all per STYLE.md:
  derivations, an SVG figure per lesson (figures/gen/L1-L6.py), >=3 exercises
  with hidden solutions, and 2-3 verified references each. 12 cross-pillar
  CONNECTIONS express that L underpins A/B/D/F/H; pillar A's "single-variable
  calculus" prerequisites now point at L; new "Calculus for ML" learning path.
  All 70 runnable python blocks executed under python3; render-check
  --exercises 35/35; figures byte-deterministic.

- **Exercises campaign** (PRs #85–#95, merged, 2026-06-11/12). Every lesson now
  ends with an `## Exercises` section: at least 3 difficulty-laddered exercises
  (theory and runnable numpy code, or theory-only for `codeExempt` lessons) with
  hidden `<details>` solutions, per the new binding **STYLE.md §6.7**.
  Infrastructure shipped first (PR #85: §6.7, `.mdx-body details` CSS,
  `render-check.mjs --exercises` gate, exemplar `A2/entropy.mdx`); then one PR
  per pillar A→K retrofitted all 458 lessons. Pillar status: all complete
  (A☑ B☑ C☑ D☑ E☑ F☑ G☑ H☑ I☑ J☑ K☑). Every code solution was executed under
  python3; every pillar passed `render-check.mjs --exercises` and a subagent
  review before merge.

Two earlier efforts shipped on 2026-06-11:

- **Intuition-examples campaign** (PRs #73–82, merged). The scan flagged 145
  lessons; 84 gained verified concrete examples (magnitude scale / contrasting
  pair / named confusion per STYLE.md §6.2 item 4), the rest were already
  grounded. `scripts/find-intuition-candidates.mjs` is the triage tool;
  `A2/entropy.mdx` is the canonical reference.
- **remark-gfm** (PR #83, merged). GFM pipe tables in lesson prose now render as
  real tables (42 files had raw `|---|` text). `remark-gfm` is in
  `MdxContent.tsx` (and the render-check harness), with `singleTilde: false` so
  it does not clash with KaTeX math. Full 458-lesson render sweep is clean.

Add new agreed next steps here.
