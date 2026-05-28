# ai-knowledge-tree

A deployed Next.js study site mapping the full DAG of topics in Data Science,
Machine Learning, Deep Learning, and AI Engineering. Each pillar (A → J) has
subsections, each subsection is a discipline taught as an ordered sequence of
atomic lessons, and subsections in different pillars are linked by explicit
cross-pillar connections (e.g. `D4 ↔ F8` because VAEs sit in both Generative
DL and Bayesian DL).

Anonymous visitors see the whole map and read every page. Signed-in students
get per-user progress: mark a lesson studied, resume where they left off, and
the dashboard recolors to their own study state.

Inspired by [AI ML Theory](https://github.com/luanmoura/ai-math-theory) (the
long-form LLM curriculum that seeds pillars A, C, D, E) and
[AI Eng Journey](../AI%20Eng%20Journey/) (the applied roadmap behind pillar J).

## Pillars

| ID | Name | Coverage |
|----|------|----------|
| A | Foundations | Math, prob, opt, numerical, DSA |
| B | Statistics & Causal Inference | Frequentist, Bayesian, causal, experimental design |
| C | Classical Machine Learning | Linear, kernel, tree, clustering, rec sys, ANN |
| D | Deep Learning: Core & Tracks | MLPs, CV, sequence, generative, SSL, GNN |
| E | NLP & Language Models | The backbone of AI ML Theory |
| F | Probabilistic Graphical Models | Bayes nets, HMM, VI, MCMC |
| G | Time Series & Forecasting | Classical, DL, foundation models |
| H | Reinforcement Learning | MDPs, deep RL, RLHF |
| I | MLOps & Production Systems | Data, training infra, serving, monitoring |
| J | **AI Engineering** | The AI Eng Journey roadmap (RAG, agents, MCP, Cloud AI) |

## How it's built

The Next.js app is the **primary** front end. The homepage `/` is the dashboard:
hero, big stats, sticky filter bar, all 10 pillars with three-level collapse,
the D3 force-directed connections graph with click-to-pin panel, and the
learning paths. Deep routes serve every discipline and lesson:

- `/`: dashboard (the homepage *is* the dashboard)
- `/connections`: standalone D3 graph page
- `/pillar/[letter]`: pillar overview, lists subsections
- `/pillar/[letter]/[subId]`: discipline overview, lists lessons
- `/pillar/[letter]/[subId]/[lessonId]`: the lesson study page (MDX)

A single self-contained `content-dag-dashboard.html` is kept as an **offline
export** (D3 via CDN, opens directly in a browser, no build). It is **not**
wired into the Next.js build; regenerate its embedded `PILLARS` / `CONNECTIONS`
/ `PATHS` literals only when you specifically want the offline file to stay in
sync with `src/lib/dag.ts`.

## Stack

- **Next.js 16** (App Router, Turbopack) + **React 19** + **TypeScript strict**
- **Tailwind CSS v4** (`@import "tailwindcss"` + `@theme inline`, with
  `@tailwindcss/postcss`); design tokens and pillar colors in
  `src/app/globals.css` as CSS variables
- **D3 v7** for the connections graph
- **MDX** rendered with `next-mdx-remote/rsc`; math via `remark-math` +
  `rehype-katex`; structural diagrams via **Mermaid**; static code via
  **Shiki**; runnable code via **Pyodide** (numpy preloaded)
- **Auth.js v5** (NextAuth) + Google provider, **Neon Postgres** (Vercel
  Marketplace) via `@auth/pg-adapter` for users and progress

## Run locally

```bash
npm install
npm run dev        # http://localhost:3000  (anonymous-only without env)
npm run build
npm run lint
```

With no environment variables, the dashboard and every study page work; sign-in
and progress tracking are simply hidden. To enable auth and progress, copy
`.env.example` to `.env.local` and set `DATABASE_URL` + the `AUTH_*` keys.

## Architecture

```
ai-knowledge-tree/
├── content-dag-dashboard.html      # offline export only (not built)
├── schema.sql                      # Neon: Auth.js tables + progress
├── .env.example                    # env template
├── DEPLOY.md                       # Vercel + Neon + Google OAuth steps
├── content/<pillar-slug>/<subId>/<lessonId>.mdx
│   └── STYLE.md                    # BINDING voice/tone + lesson pedagogy
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Header + globals.css + katex CSS
│   │   ├── page.tsx                # home = the dashboard
│   │   ├── connections/page.tsx    # standalone graph page
│   │   ├── pillar/[letter]/        # pillar overview
│   │   │   └── [subId]/            # discipline overview, lesson list
│   │   │       └── [lessonId]/page.tsx   # the lesson study page
│   │   ├── api/auth/[...nextauth]/route.ts
│   │   └── actions/progress.ts     # setStatus / clearStatus
│   ├── components/
│   │   ├── Hero / DashboardStats / LearningPaths
│   │   ├── PillarCard / TopicChip
│   │   ├── FilterBar / CollapseController
│   │   ├── ConnectionsGraph (D3)
│   │   ├── LessonSidebar / PillarSidebar
│   │   ├── StudyProgressControls
│   │   └── mdx/ { MdxContent, MdxPre, CodeBlock, PyRunner, Mermaid }
│   ├── lib/
│   │   ├── types.ts
│   │   ├── dag.ts                  # PILLARS + CONNECTIONS + PATHS (source of truth)
│   │   ├── curriculum/{index,A,...}.ts  # per-subsection ordered Lesson[]
│   │   ├── content.ts              # lesson resolve/load, prev/next
│   │   ├── db.ts                   # guarded Neon pool
│   │   └── progress.ts             # getProgressMap / getResume / isSignedIn
│   ├── auth.ts                     # Auth.js config (guarded)
│   └── types/next-auth.d.ts
└── public/figures/<sub>/<name>.svg # generated plot assets
```

`src/lib/dag.ts` is the structural source of truth for pillars, subsections,
topics, connections, and curated learning paths. Per-discipline ordered lesson
lists live under `src/lib/curriculum/`; lesson prose lives under
`content/<pillar-slug>/<subId>/<lessonId>.mdx`, and the file's presence flips
the lesson from "coming soon" to "available".

## Authoring

See `content/STYLE.md` for the binding voice/tone and lesson pedagogy. Each
lesson is one atomic concept and follows the same arc: motivate, define on
first use, derive step by step (no hand-waving), runnable numpy block at the
end, one-sentence handoff to the next lesson.

The curriculum-first authoring order is A → C → D → E → B → F → G → H → I → J.
Pillar A is fully authored (71 lessons across A1–A5); pillar C is next.

## Deploy

See `DEPLOY.md` for the end-to-end Vercel + Neon + Google OAuth steps.

## Conventions

- **English** end-to-end (UI chrome, content, code identifiers, topic names)
- **No em-dash** ("—") anywhere; replace with a colon, comma, semicolon, or
  parentheses (see `content/STYLE.md` §2.1)
- TypeScript strict; server components by default, `"use client"` only where
  hooks or events are needed
- Pillar IDs are single letters `A–J`; subsection IDs are `<letter><n>`,
  uppercased
- Status glyphs: `✓` covered/studied, `◐` partial/in-progress, `○` gap,
  `★` hot
