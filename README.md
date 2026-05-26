# ai-knowledge-tree

Site interativo mapeando a DAG completa de tópicos em Data Science, Machine Learning,
Deep Learning e AI Engineering. Cada pilar (A → J) tem subseções, e subseções
relacionadas entre pilares são conectadas explicitamente.

Inspirado em [AI ML Theory](https://github.com/luanmoura/ai-math-theory) (que cobre
a espinha de LLMs em profundidade) e [AI Eng Journey](../AI%20Eng%20Journey/)
(que define o roadmap de engenharia de IA aplicada).

## Pilares

| ID | Nome | Origem |
|----|------|--------|
| A  | Foundations | math, prob, opt, numerical, DSA |
| B  | Statistics & Causal Inference | frequentist, Bayesian, causal, design |
| C  | Classical Machine Learning | linear, kernel, tree, clustering, rec sys, ANN |
| D  | Deep Learning — Core & Tracks | MLPs, CV, sequence, generative, SSL, GNN |
| E  | NLP & Language Models | espinha do AI ML Theory |
| F  | Probabilistic Graphical Models | Bayes nets, HMM, VI, MCMC |
| G  | Time Series & Forecasting | clássico → DL → foundation models |
| H  | Reinforcement Learning | MDPs, deep RL, RLHF |
| I  | MLOps & Production Systems | data, training infra, serving, monitoring |
| J  | **AI Engineering** | roadmap do AI Eng Journey (RAG, agents, MCP, Cloud AI) |

## Front page

**`content-dag-dashboard.html`** é a página principal — um único arquivo
HTML auto-contido (D3 via CDN) que abre direto no navegador. Tem dashboard
de stats, filtros, busca, todos os 10 pilares com collapse/expand, o grafo
D3 force-directed das conexões e trilhas sugeridas.

```bash
open content-dag-dashboard.html
```

## Páginas Next (em construção)

A scaffold Next.js está em paralelo, para hospedar a camada de conteúdo
longo (MDX por subseção) em rotas profundas:

- `/` — vai espelhar o dashboard do HTML (ainda landing menor)
- `/tree` — dashboard
- `/connections` — grafo D3
- `/pillar/[letter]/[sub-id]` — página por subseção *(planejada)*

## Stack

- **HTML standalone** + JS + D3 v7 — a front page
- Next.js 16, React 19, TypeScript — scaffold paralelo
- Tailwind CSS v4
- D3.js v7
- MDX via `@next/mdx` (para futuras sessões de conteúdo, ainda não populadas)

## Setup

```bash
# Front page — sem build:
open content-dag-dashboard.html

# Scaffold Next (quando trabalhar nas rotas profundas):
npm install
npm run dev   # http://localhost:3000
```

## Estrutura

```
ai-knowledge-tree/
├── content/                # pasta para futuros .mdx (uma por pilar; vazias por ora)
│   └── pillars.json        # manifest com metadados de cada pilar
├── src/
│   ├── app/
│   │   ├── page.tsx        # home
│   │   ├── tree/           # dashboard view
│   │   └── connections/    # grafo D3
│   ├── components/         # PillarCard, TopicChip, FilterBar, ConnectionsGraph
│   └── lib/
│       └── dag.ts          # PILLARS + CONNECTIONS (fonte de verdade)
└── public/
```

## Próximos passos

1. `npm install` e validar que o dev server sobe sem erros
2. Popular `content/<pillar>/<subsection>/` com MDX (mover material do AI ML Theory)
3. Expandir `CONNECTIONS` em `src/lib/dag.ts` com mais conexões cruzadas
4. Sidebar de navegação por pilar (estilo AI ML Theory)
5. Persistir progresso do usuário em localStorage
6. Deploy (Vercel)
