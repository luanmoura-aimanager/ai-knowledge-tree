# STATUS: where we left off

Handoff note. Durable project guidance is in `CLAUDE.md`; content voice rules in
`content/STYLE.md`; the full implementation plan is at
`~/.claude/plans/silly-imagining-bee.md` (auto-loads is not guaranteed, read it
explicitly). This file is the "what just happened / what is next" sticky note.

Last updated: 2026-05-25.

## The project in one paragraph

A deployed study site (Next.js 16 + React 19 + Tailwind v4) mapping the DAG of
DS/ML/DL/AI Engineering. Dashboard homepage, D3 connections graph, MDX study
content with KaTeX math + Mermaid diagrams + runnable in-browser Python
(Pyodide), Google sign-in (Auth.js v5) with per-user progress in Neon Postgres.
Live at https://ai-knowledge-tree.vercel.app.

## What is DONE and working

- **Shell shipped + deployed** (was milestones M0 to M4): dashboard, content
  routes, MDX pipeline, auth, per-user progress, Vercel deploy. Verified end to
  end in production (Google sign-in + progress persistence work).
- **Content model v2 (the current structure):** three levels,
  **Pillar -> Subsection (discipline) -> Lesson**. A lesson is one atomic concept
  = one MDX page with step-by-step proofs.
  - Curriculum (ordered lesson list per subsection) lives in
    `src/lib/curriculum/<letter>.ts`. Prose lives in
    `content/<pillar-slug>/<subId>/<lessonId>.mdx`. Progress is per lesson,
    keyed `"subId/lessonId"`.
  - Routes: `/pillar/[letter]` (overview) -> `/pillar/[letter]/[subId]`
    (discipline, lists lessons) -> `/pillar/[letter]/[subId]/[lessonId]` (lesson).
  - Sidebar inside a discipline lists its lessons; prev/next chains across
    lessons; dashboard counts lessons studied / total.
- **A1 (Linear algebra) curriculum defined**: 17 lessons in
  `src/lib/curriculum/A.ts`. Two authored and reviewed/approved by the user:
  `A1/vector-spaces` and `A1/inner-products`.
- **Tone rule locked:** the em-dash character is banned outright everywhere
  (`content/STYLE.md` 2.1, plus a saved memory). Use `:` `,` `(` or a full stop.
  Proper-name en-dashes (Cauchy–Schwarz) are allowed.
- `npm run build` and `npm run lint` are green.

## What is NEXT (resume here)

Authoring, curriculum-first, gentle step-by-step (see `content/STYLE.md` 6).
The user approved the depth of the two A1 sample lessons. Continue:

1. **Author the remaining 15 A1 lessons** in curriculum order:
   basis-dimension, linear-maps-matrices, rank-nullity, norms, gram-schmidt,
   determinants, eigenvalues, spectral-theorem, quadratic-forms, svd,
   low-rank-pca, factorizations, least-squares, matrix-calculus, tensors-einsum.
   The retired single-file `content/A-foundations/A1.mdx` (and A2 to A5, E3, I3)
   hold reusable draft material to mine, then delete.
2. Then **A2 to A5**: for each, first draft its lesson curriculum into
   `src/lib/curriculum/A.ts` (currently empty arrays) for user approval, then
   author the lessons.
3. Then pillars **C -> D -> E** (richest reuse from `../ai-math-theory/content`,
   which is 135 atomic sessions that map roughly 1:1 onto lessons), then
   B, F, G, H, I, J.

After a batch, redeploy with `vercel --prod` (production currently predates the
lesson refactor; it still shows the old single-page version until redeployed).

## Per-lesson definition of done

- One concept; motivate -> define on first use -> derive every nontrivial
  equation step by step -> worked numpy block at the end -> one-sentence handoff.
- `content/STYLE.md`-compliant; no em-dash; no unsupported MDX components
  (only KaTeX, ```mermaid, ```python / ```python-static).
- Frontmatter complete (LessonFrontmatter); prereqs + prev/next resolve.
- Verify: `npm run build`, then load the lesson page, run the PyRunner block.

## Files of note

- `src/lib/curriculum/{index,A}.ts` : the lesson curriculum (A1 = 17 lessons).
- `content/A-foundations/A1/{vector-spaces,inner-products}.mdx` : the 2 approved
  sample lessons (the quality/style bar).
- `src/lib/content.ts` : lesson resolve/load, contentStatus, prev/next.
- `src/app/pillar/[letter]/[subId]/[lessonId]/page.tsx` : the lesson page.
- `CLAUDE.md` : durable conventions (updated for the lesson model).
- `content/STYLE.md` : voice + 6 lesson pedagogy.
- `~/.claude/plans/silly-imagining-bee.md` : the full plan (workstreams W5/W6/W7).

## Environment / deploy reminders

- Local: `npm run dev` (anonymous-only without env; full with `.env.local`).
- Env lives in Vercel + local `.env.local` (DATABASE_URL, AUTH_SECRET,
  AUTH_GOOGLE_ID, AUTH_GOOGLE_SECRET). DB tables already created in Neon
  (`scripts/init-db.mjs` re-runs `schema.sql`). Deploy steps in `DEPLOY.md`.
- Vercel CLI is installed and the project is linked.
