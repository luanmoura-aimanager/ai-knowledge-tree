# Roadmap — next steps

Canonical backlog of upcoming work for `ai-knowledge-tree`. When asked "what are
the next steps?", read this file. As items ship, check them off or remove them so
the list never claims work that's already done.

Last reviewed: 2026-11-09 (2025-26 modern-algorithms gap pass shipped: D8 tabular &
event foundation models plus 9 new architecture/training lessons).

## Backlog

- [ ] **Further 2025-26 lesson candidates** (from the 2026-11 gap pass, not yet authored):
  multi-token prediction (DeepSeek-V3 MTP), FP8/MXFP4 training, manifold-constrained
  hyper-connections (DeepSeek-V4), and KV sharing / per-layer embeddings (Gemma 4).

_No new pillars queued._ The causal-inference work is shipped: foundations live
in pillar B (B5), and the advanced machine-learning frontier is pillar M below.
Add new agreed next steps here.

---

Latest shipped (2026-11-09): **modern-algorithms gap pass** (2025-26 techniques).

- **D8 Tabular & event foundation models** (PR #109): new subsection, 6 lessons on
  transaction/event-sequence foundation models (PRAGMA, nuFormer, TREASURE): tokenization,
  continuous-time RoPE, masked vs next-event pretraining, LLM backbones (Qwen + LoRA),
  downstream evaluation and leakage, and TabPFN.
- **9 lessons appended to existing subsections**: E3 long-context RoPE scaling (PI, NTK-aware,
  YaRN), attention sinks / QK-norm / gated attention, fine-grained + shared experts with
  loss-free balancing, NSA and DeepSeek sparse attention; D3 delta rule and Gated DeltaNet
  (Qwen3-Next, Kimi Linear); D1 Muon and QK-Clip; E4 GRPO variants (Dr. GRPO, DAPO, GSPO);
  D4 diffusion language models (LLaDA, MDLM); N8 generative recommenders (HSTU, OneRec).
- Refreshes: G3 time-series foundation models (Chronos-2, TimesFM 2.5/3.0, Moirai 2.0, Toto),
  forward links from E3 positional encodings / GQA-MoE (DeepSeek-V3 expert counts corrected),
  D3 hybrids, E8 frontier, and the handoffs of each subsection's former last lesson.

Five efforts shipped:

- **Advanced Causal Machine Learning pillar M** (2026-06-20). New top-level pillar,
  the ML frontier sitting on top of B5's causal foundations (cross-linked, not
  duplicative). 6 subsections (M1 causal discovery, M2 heterogeneous treatment
  effects, M3 orthogonal & semiparametric estimation, M4 deep causal inference, M5
  policy learning & off-policy evaluation, M6 robustness/sensitivity/assumptions),
  33 lessons, all per STYLE.md: derivations, ≥1 image per lesson (Mermaid and/or
  the per-subsection figure scripts figures/gen/M1-M6.py, 23 SVGs), ≥3 exercises
  with hidden solutions, and verified references each. 10 cross-pillar CONNECTIONS
  tie M to B5/B4/D4/H; new "Advanced Causal ML" learning path threads B5 → M1-M6.
  Every runnable numpy block executes under python3 (asserts pass); render-check
  --exercises 33/33; build + lint clean. (B5 was found already complete during
  scoping, so M was authored as the differentiated advanced course rather than a
  duplicate foundations pillar.)

Four earlier efforts shipped:

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
