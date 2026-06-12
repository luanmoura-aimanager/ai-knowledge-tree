# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-06-11 (intuition-examples campaign executed; remark-gfm scope corrected).

## Backlog

- [x] **Intuition-examples campaign — executed, in review.** Reader feedback on
  `A2/entropy` showed lessons jump from formula to formula without grounding; the
  fix (a magnitude scale, a contrasting pair, or a named confusion per STYLE.md
  §6.2 item 4, with `A2/entropy.mdx` as the canonical reference) is now a binding
  part of the lesson shape. The 2026-06-11 scan flagged 145 lessons (score ≥ 3);
  focused subagents read every one, verified each number against numpy or the
  lesson's own code block, and render-checked the MDX. **84 lessons got new
  verified examples (86 files changed, incl. 2 table-only conversions) across 9
  PRs; the remaining ~59 flagged lessons were already grounded and left
  untouched** (the heuristic intentionally over-flags). One open PR per pillar,
  pending review + merge:
  - A: #73 (15) · B: #74 (12) · C: #75 (12) · E: #76 (12) · F: #77 (14)
  - D: #78 (10) · G: #79 (6) · H: #80 (3) · I: #81 (1)

  Four pipe tables (`B2/bayesian-model-comparison`, `E1/crf`,
  `F2/conditional-random-fields`, `F8/mc-dropout-ensembles`) were converted to
  lists along the way. Once the 9 PRs merge, tick this item fully and drop the
  PR list.
- [ ] **Add `remark-gfm` (the pipe-table fix is now clearly plugin-not-convert).**
  The MDX pipeline (`MdxContent.tsx`) has only `remark-math`, so GFM tables render
  as raw `|` text. The 2026-06-11 sweep found this is **widespread: ~47 lesson
  files** carry raw pipe tables (`grep -rl '^|---' content --include='*.mdx'`),
  not the 4 originally listed. At that scale, hand-converting is the wrong call:
  add `remark-gfm` to `MdxContent.tsx`'s `remarkPlugins` and style `table`/`th`/
  `td` in `globals.css` (dark theme, matching `.mdx-body`). This is a
  site-wide rendering-pipeline change, so verify a sample of the 47 with
  `scripts/render-check.mjs` and visually before merging. (The campaign already
  cleared 4 of the 47 by converting them to lists.)
