# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-06-11 (intuition-examples campaign planned).

## Backlog

- [ ] **Intuition-examples campaign.** Reader feedback on `A2/entropy` showed the
  lessons jump from axioms to formulas without grounding; the fix (a magnitude
  scale, a contrasting pair, a named confusion, per STYLE.md §6.2 item 4, with
  `A2/entropy.mdx` as the canonical reference) shipped in `2b7911f` and is now a
  binding part of the lesson shape. Backfill the existing lessons:
  1. **Triage** with `node scripts/find-intuition-candidates.mjs` (heuristic:
     display-equation density vs concrete-example signals in prose). At the
     score ≥ 3 cutoff the 2026-06-11 scan flags **145 of 458** lessons:
     A:35 B:22 C:17 D:12 E:21 F:17 G:15 H:5 I:1 (J/K are conceptual and
     largely exempt). Re-run the scan per batch; the list shrinks as edits land.
  2. **Work pillar by pillar** in priority order **A → B → C → E → F → D → G →
     H → I** (foundations first; their intuitions are reused downstream). One
     branch + PR per pillar, like the figures and citation campaigns.
  3. **Per lesson:** read it, decide which of the three §6.2-4 patterns actually
     teaches (the heuristic only triages; some flagged lessons are fine), add
     the examples with every number verified (compute it, or tie it to the
     closing `python` block), keep §2 voice rules, no pipe tables (no
     `remark-gfm`). Verify each edited file with
     `node scripts/render-check.mjs <file>`; `npm run build` + `npm run lint`
     clean before each PR.
- [ ] **Add `remark-gfm` or remove prose pipe tables.** The MDX pipeline
  (`MdxContent.tsx`) has only `remark-math`, so GFM tables render as raw `|` text.
  Known affected: `E9/aiayn-revisited`, `F2/conditional-random-fields`,
  `F8/mc-dropout-ensembles`, `B2/bayesian-model-comparison` (grep `^\|` for the
  full list). Either add the plugin (then restyle `table` in `globals.css`) or
  convert those tables to lists.
