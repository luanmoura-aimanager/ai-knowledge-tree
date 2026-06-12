# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-06-11 (exercises campaign started; intuition-examples
campaign + remark-gfm both shipped).

## Backlog

_Empty._ Three efforts shipped:

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
