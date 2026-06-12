# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-06-11 (intuition-examples campaign + remark-gfm both shipped).

## Backlog

_Empty._ Two efforts shipped on 2026-06-11:

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
