# CLAUDE.md

Guidance for Claude Code when working in `ai-knowledge-tree/`.

## What this project is

A deployed study site mapping the full DAG of Data Science, Machine Learning,
Deep Learning and AI Engineering. Each top-level **pillar** (A → J) has
**subsections** (e.g. `A1`, `J3`); each subsection is a *discipline* taught as an
ordered sequence of atomic **lessons** (one concept per page, with step-by-step
derivations). Subsections in different pillars are linked by explicit
**connections** (e.g. `D4 ↔ F8` because VAEs sit in both Generative DL and
Bayesian DL).

Anonymous visitors see the whole map and read every page. Signed-in students get
**per-user progress**: mark a subsection studied, resume where they left off, and
the dashboard recolors to their own study state.

Inspired by `../ai-math-theory/` (the long-form LLM curriculum that seeds
pillars A/C/D/E) and `../AI Eng Journey/` (the applied roadmap behind pillar J).

## The Next.js app is primary

The homepage `/` **is** the dashboard, served by Next.js. It renders the hero,
big stats, sticky filter bar, all 10 pillars with three-level collapse, the D3
force-directed connections graph with click-to-pin panel, and the learning
paths, the same experience the old standalone HTML had, now in React.

`content-dag-dashboard.html` is **retired as the front page**; it is kept only
as an **offline export** (a single shareable file). It is not wired into the
build. If you change `dag.ts`, the live site updates automatically; only
regenerate the HTML's embedded `PILLARS`/`CONNECTIONS`/`PATHS` literals if you
specifically want the offline file to stay in sync.

## Stack

- **Next.js 16** (App Router, Turbopack) + **React 19** + **TypeScript strict**
- **Tailwind CSS v4** (`@import "tailwindcss"` + `@theme inline`; needs
  `@tailwindcss/postcss`). Design tokens + pillar colors live in
  `src/app/globals.css` as CSS variables.
- **D3 v7** for the connections graph (`ConnectionsGraph.tsx`).
- **MDX** content rendered with `next-mdx-remote/rsc`; math via
  `remark-math` + `rehype-katex`; structural diagrams via **Mermaid**; static
  code via **Shiki**; runnable code via **Pyodide**.
- **Auth.js v5** (NextAuth) + Google provider, **Neon Postgres** (Vercel
  Marketplace) via `@auth/pg-adapter` for users + progress.

## Architecture

```
ai-knowledge-tree/
├── content-dag-dashboard.html      # offline export only (not built)
├── schema.sql                      # Neon: Auth.js tables + progress
├── .env.example / DEPLOY.md        # env + deploy steps (user-run)
├── content/<pillar-slug>/<subId>/<lessonId>.mdx  # lesson pages (A-foundations/A1/svd.mdx)
│   └── STYLE.md                    # BINDING voice/tone + lesson pedagogy (§6)
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Header + globals.css + katex CSS
│   │   ├── page.tsx                # home = the dashboard (async; reads progress)
│   │   ├── connections/page.tsx    # standalone graph page
│   │   ├── tree/page.tsx           # redirect → /
│   │   ├── pillar/[letter]/        # passthrough layout + pillar overview
│   │   │   └── [subId]/           # discipline: lesson-sidebar layout + lesson list
│   │   │       └── [lessonId]/page.tsx   # the lesson study page (MDX or coming-soon)
│   │   ├── api/auth/[...nextauth]/route.ts
│   │   └── actions/progress.ts     # "use server": setStatus / clearStatus (key = subId/lessonId)
│   ├── components/
│   │   ├── Hero / DashboardStats / LearningPaths   # dashboard sections
│   │   ├── PillarCard / TopicChip                  # pillar + topic render
│   │   ├── FilterBar (client) / CollapseController (client)
│   │   ├── ConnectionsGraph (client, D3)
│   │   ├── LessonSidebar (client)                  # in-discipline lesson nav
│   │   ├── StudyProgressControls (client)          # mark studied (per lesson)
│   │   └── mdx/ { MdxContent, MdxPre, CodeBlock, PyRunner, Mermaid }
│   ├── lib/
│   │   ├── types.ts                # Pillar, Subsection, Topic, Connection, Path, Lesson, LessonFrontmatter
│   │   ├── dag.ts                  # PILLARS + CONNECTIONS + PATHS (structure source of truth)
│   │   ├── curriculum/{index,A,…}.ts  # per-subsection ordered Lesson[] (the lesson list)
│   │   ├── content.ts              # lesson resolve/load, lessonContentStatus, prev/next
│   │   ├── db.ts                   # guarded Neon pool (null when no DATABASE_URL)
│   │   └── progress.ts             # getProgressMap / getResume / isSignedIn (keyed subId/lessonId)
│   ├── auth.ts                     # Auth.js config (guarded)
│   └── types/next-auth.d.ts        # Session.user.id augmentation
└── public/figures/<sub>/<name>.svg # generated plot assets (see Figures)
```

### Three structural levels

**Pillar → Subsection (discipline) → Lesson.** `dag.ts` defines pillars,
subsections, topics, and connections (the map). `src/lib/curriculum/<letter>.ts`
defines, per subsection, the **ordered `Lesson[]`**, the atomic study units
(one concept each). A lesson's prose is `content/<slug>/<subId>/<lessonId>.mdx`;
its presence is its `contentStatus`. Routes: `/pillar/[letter]` (pillar overview)
→ `/pillar/[letter]/[subId]` (discipline overview, lists lessons) →
`/pillar/[letter]/[subId]/[lessonId]` (the lesson). Progress is **per lesson**,
keyed `"subId/lessonId"` (see `lessonKey`).

### Single source of truth: `src/lib/dag.ts`

Everything structural reads from three exports:

- `PILLARS: Pillar[]`. 10 pillars A → J. Each has `letter`, `slug`, `name`,
  `shortName` (compact label for graph pills), `tagline`, `color` (hex), `subs[]`.
  Each subsection has a stable `id` (`"D4"`), `name`, and flat `topics`.
- `CONNECTIONS: Connection[]`. Cross-pillar edges `{ from, to, label, kind }`,
  `kind ∈ "shared-concept" | "uses" | "alternative" | "generalizes"`.
- `PATHS: Path[]`. Curated reading sequences for the learning-paths grid.

Helpers: `getAllSubsections()`, `getSubsectionById(id)`, `pillarStats(p)`,
`globalStats()`.

### Two status layers (the conceptual core)

`dag.ts` still carries a per-topic `status`/`hot` (the *domain* map). On top of
it the site computes display state from two layers:

- **`contentStatus`** (`src/lib/content.ts`): does an authored `.mdx` exist for
  this **lesson**? `available` vs `coming-soon`. Derived from the filesystem,
  never hand-kept. A subsection is "available" once any of its lessons is.
- **`userProgress`** (`src/lib/progress.ts`, in Neon): `studied | in-progress`
  per **lesson**, keyed `"subId/lessonId"` (absence = unstudied).

Dashboard coloring: **anonymous** visitors see the domain map / availability;
**signed-in** users see big stats counted over **lessons** (studied / total from
`lessonCount()`), per-subsection `x/N` badges, and a "Continuar" link that deep-
links to the last-touched lesson. When adding dashboard surfaces, keep the
anonymous path working without a DB (guards in `db.ts`/`progress.ts`).

### Filtering + collapse pattern (DOM mutation, not React state)

`FilterBar` and `CollapseController` deliberately do **not** lift topic-tree
state into React. Each topic carries `data-status` / `data-hot` / `data-name`;
filters toggle a `hidden` class and cascade (hide topics → hide empty
subsections → dim empty pillars). Collapse toggles `.collapsed` /
`.body-collapsed` via event delegation. This keeps the server-rendered grid
intact and interactions instant. Match this pattern for new filters/toggles.

### Connections graph

`ConnectionsGraph.tsx` builds a D3 force simulation: pillars anchored to a 5×2
grid (top row `y=240`, bottom `y=height-180`), `forceY` strength `0.32`, pillar
**pill labels** (rect sized to text bbox, using `shortName`), within-pillar
sequence links + cross-pillar `CONNECTIONS`. Hover/click highlights a node + its
neighbors via CSS classes; the click-to-pin side panel is tinted with the active
pillar color and links to `/pillar/<letter>/<sub-id>`.

## Authoring conventions

### Lesson template (one concept → `content/<pillar-slug>/<subId>/<lessonId>.mdx`)

A lesson is one atomic concept. The full pedagogy is in **`content/STYLE.md` §6**
(binding): motivate → define on first use → derive every nontrivial equation
step by step → worked numpy at the end → one-sentence handoff. Gentle pacing,
undergraduate physics/eng/math level, but no hand-waving.

Frontmatter (`LessonFrontmatter` in `types.ts`):

```yaml
---
title: "Singular value decomposition"
pillar: A
subId: A1
lessonId: svd
order: 12
estimatedMinutes: 24
goal: "One sentence: what the reader can do after this lesson."
prerequisites: ["spectral-theorem"]   # bare id (same subsection) or "subId/lessonId"
codeExempt: false                       # optional; omit unless true
---
```

The ordered lesson list per subsection lives in `src/lib/curriculum/<letter>.ts`
(titles + goals + prereqs). Add/curate lessons there; the file presence flips a
lesson to `available`.

### Code blocks (the `MdxPre` router)

Fenced blocks are dispatched by language:

- ` ```python ` → **runnable** in `<PyRunner>` (Pyodide, numpy preloaded, lazy
  on first "Run"). Keep runnable code **numpy-first**.
- ` ```python-static ` → static Shiki highlight. Use when the code needs PyTorch
  or GPU (Pyodide can't load torch).
- ` ```mermaid ` → rendered diagram.
- any other language → static Shiki highlight.

### Figures (hybrid mechanism)

- **Structural diagrams** (flow, architecture, pipelines): ```mermaid blocks.
- **Equations**: KaTeX (always).
- **Quantitative plots** (loss curves, heatmaps, distributions): a committed
  matplotlib script `figures/gen/<sub>.py` writes `public/figures/<sub>/<name>.svg`,
  embedded with `![caption](/figures/<sub>/<name>.svg)`. Plots are reproducible
  from the script; the SVGs are committed (do not hand-commit opaque binaries).

  **Pipeline (live).** One script per subsection. Each imports
  `figures/gen/_style.py` and calls `apply_style()` (dark-native theme matching
  `globals.css`: transparent bg, light text, pillar accents via `color(sub)`),
  builds figures, and writes them with `save(fig, sub, name)`. Keep generation
  deterministic (`np.random.default_rng(0)`) so re-runs give byte-identical SVGs.
  Seed plot data from the lesson's existing `python` block where one exists.

  ```bash
  python3 -m venv figures/.venv                                  # once
  figures/.venv/bin/pip install -r figures/requirements.txt      # once
  npm run figures      # runs scripts/build-figures.sh → all figures/gen/<sub>.py
  ```

  Figures are **not** built in CI/Vercel (no Python there) — the committed SVGs
  are served as-is. `MdxContent.tsx` renders `![alt](src)` as a captioned
  `<figure>` (alt = caption); `.mdx-body img` styles it as a card.

### Code-exempt topics

Pillars **I** (MLOps) and **J** (AI Engineering) deployment/infra/governance
material, plus infra-flavored D7 topics, have no natural code surface. Mark them
`codeExempt: true` and keep them conceptual; do not force code onto them.

## Conventions

- **TypeScript strict**: no `any`. Use the types in `src/lib/types.ts`.
- **Server components by default**; mark `"use client"` only where you need
  hooks/events (FilterBar, CollapseController, ConnectionsGraph, PyRunner,
  Mermaid, LessonSidebar, StudyProgressControls).
- **Tailwind classes inline**; tokens (surfaces + `--pa`…`--pj` pillar colors)
  in `globals.css` via `@theme inline` and `:root`.
- **Status glyphs**: `✓` covered/studied, `◐` partial/in-progress, `○` gap, `★` hot.
- **Pillar IDs** are single letters `A–J`; subsection IDs are `<letter><n>`, uppercased.
- **English** for all strings (UI chrome, content, code identifiers, topic
  names). The site is written in English end-to-end.

## Common tasks

### Define a discipline's curriculum (do this first, per the curriculum-first flow)
Add/edit the ordered `Lesson[]` for the subsection in `src/lib/curriculum/<letter>.ts`
(id slug + title + goal + prerequisites). New pillars get a new module imported in
`src/lib/curriculum/index.ts`. The lesson list drives the sidebar and overview
even before any prose exists (unwritten lessons show "coming soon").

### Author a lesson
1. Create `content/<pillar-slug>/<subId>/<lessonId>.mdx` with `LessonFrontmatter`.
2. Follow `content/STYLE.md` §6: one concept, motivate → define → step-by-step
   derivations → worked `python` (numpy) block (or `python-static` / `codeExempt`).
3. `contentStatus` flips to `available` on file presence. Verify the lesson page,
   sidebar highlight, prev/next, and prereq links; spot-run the `<PyRunner>` block.

### Author a complete pillar (the standard workflow)

This is the workflow for every new pillar. Follow it in order.

1. **Sync with main.**
   ```bash
   git checkout main && git pull origin main
   ```
   Check the diff since the last pillar was merged:
   ```bash
   git log --oneline -5
   git diff HEAD~1..HEAD --stat
   ```

2. **Create a feature branch.**
   ```bash
   git checkout -b feature/<letter>-<slug>-curriculum
   # e.g. feature/f-probabilistic-graphical-models-curriculum
   ```

3. **Write the pillar in one session.**
   - Read `src/lib/dag.ts` to enumerate all subsections and topics for the pillar.
   - Create `src/lib/curriculum/<Letter>.ts` with ordered `Lesson[]` for every subsection.
   - Import and spread it in `src/lib/curriculum/index.ts`.
   - Create `content/<pillar-slug>/<SubId>/<lessonId>.mdx` for every lesson.
   - Run `npm run build` and `npm run lint` before committing; both must be clean.

4. **Commit and push, then open a PR.**
   ```bash
   git add src/lib/curriculum/<Letter>.ts src/lib/curriculum/index.ts content/<pillar-slug>/
   git commit -m "Author <Letter>1-<Letter>N curricula and all N lessons (complete pillar <Letter>)"
   git push -u origin feature/<letter>-<slug>-curriculum
   gh pr create ...
   ```

5. **Run `/code-review` on the PR, then fix findings before merging.**
   Use `/code-review` (the bundled skill) to review the branch. Apply all confirmed
   and plausible findings, push a fix commit, then merge.

6. **Always end by printing the PR link.**
   After opening the PR (step 4) and after pushing any fix commits (step 5), print
   the full GitHub PR URL so the user can navigate directly to it.

### Add a topic / subsection / connection / path
Edit the relevant array in `src/lib/dag.ts`. Add `shortName` for new pillars and
bump the graph grid (`cols`/`rows`) if you exceed 10 pillars.

### Run / build / deploy
```bash
npm install
npm run dev        # http://localhost:3000  (anonymous-only without env)
npm run build
npm run lint
```
Auth + progress activate when `DATABASE_URL` + `AUTH_*` are set. See
`.env.example` and `DEPLOY.md` (deploy steps are user-run; Vercel CLI required).

## Roadmap (next steps)

`ROADMAP.md` (repo root) is the canonical backlog of upcoming work. When the user
asks "what are the next steps?" (or similar), read `ROADMAP.md` and answer from
it. When you finish one of its items, check it off or remove it in the same change
so the list never claims work that's already shipped. Add new agreed next steps
there too — it is the single source of truth for planned work.

## What is intentionally NOT here

- **Most lessons are unwritten.** Pillars A, C, D, E, B are complete; F through J
  are not yet authored. Authoring order: A → C → D → E → B → **F → G → H → I → J**.
  Unwritten lessons render a "coming soon" fallback.
- **Stale single-file content.** Earlier seed files `content/<slug>/<subId>.mdx`
  (A1–A5, E3, I3) predate the lesson model and are no longer read by any route;
  mine them when splitting their discipline into lessons, then remove.
- **No tests yet**: add them when behavior (not just rendering) is introduced.

## Pointers to related work

- `../ai-math-theory/content/`: 135 MDX files seeding pillars A/C/D/E (heavy
  math, ~⅓ have code; needs STYLE.md pass + interactive code on migration).
- `../AI Eng Journey/`: the roadmap behind pillar J (J1–J7).
- `content-dag-dashboard.html`: the retired single-file dashboard (offline export).
