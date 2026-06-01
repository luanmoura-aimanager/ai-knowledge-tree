import type { Lesson } from "@/lib/types";

/**
 * Pillar I: MLOps & Production Systems. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 *
 * MLOps is infrastructure-heavy, but most of it has a genuine quantitative
 * surface (drift statistics, queueing, quantization arithmetic, percentiles,
 * memory math, pass@k, cost models), so those lessons carry runnable numpy.
 * Only the purely architectural lessons (pipeline paradigms, edge deployment)
 * are marked codeExempt.
 */
export const I_CURRICULUM: Record<string, Lesson[]> = {
  I1: [
    {
      id: "pipeline-paradigms",
      title: "ETL vs ELT and batch vs streaming",
      goal: "Distinguish the four ways data reaches a model (extract-transform-load vs extract-load-transform, batch vs streaming) and pick the right shape from latency and reprocessing needs.",
      prerequisites: [],
      codeExempt: true,
    },
    {
      id: "orchestration-dags",
      title: "Orchestration: DAGs, idempotency, and backfills",
      goal: "Model a pipeline as a directed acyclic graph of tasks, schedule it in dependency order by topological sort, and make each task idempotent so retries and backfills are safe.",
      prerequisites: ["pipeline-paradigms", "A/graph-traversal"],
    },
    {
      id: "feature-stores",
      title: "Feature stores and point-in-time correctness",
      goal: "Serve the same feature values to training and inference from offline and online stores, and use point-in-time joins to compute training features without leaking the future.",
      prerequisites: ["orchestration-dags"],
    },
    {
      id: "data-versioning",
      title: "Data versioning and content-addressed storage",
      goal: "Make a dataset reproducible by addressing its contents with a hash, deduplicating shared chunks, and pinning a training run to an immutable data snapshot.",
      prerequisites: ["A/arrays-hashing"],
    },
    {
      id: "drift-detection",
      title: "Detecting data drift: KS statistic and PSI",
      goal: "Quantify how far an incoming data batch has moved from a reference distribution with the Kolmogorov-Smirnov statistic for continuous features and the population stability index for binned ones.",
      prerequisites: ["B/hypothesis-testing", "A/kl-cross-entropy"],
    },
  ],
  I2: [
    {
      id: "experiment-tracking",
      title: "Experiment tracking, lineage, and reproducibility",
      goal: "Log the inputs (code, data, config, seed) and outputs (metrics, artifacts) of every run so results are comparable and reproducible, and see why fixing the seed alone is not enough.",
      prerequisites: ["I1/data-versioning", "A/sgd"],
    },
    {
      id: "hyperparameter-search",
      title: "Hyperparameter search: grid vs random",
      goal: "Frame hyperparameter tuning as black-box optimization over a search space, and see why random search dominates grid search when only a few dimensions actually matter.",
      prerequisites: ["A/bayesian-optimization"],
    },
    {
      id: "multi-fidelity-hpo",
      title: "Multi-fidelity HPO: successive halving and Hyperband",
      goal: "Spend a fixed compute budget efficiently by training many configurations briefly, then promoting only the survivors, the successive-halving rule behind Hyperband and ASHA.",
      prerequisites: ["hyperparameter-search"],
    },
    {
      id: "data-parallel-training",
      title: "Data-parallel training and all-reduce",
      goal: "Scale training across workers by averaging per-worker gradients with all-reduce, prove the average equals the single-machine gradient on the union batch, and scale the learning rate accordingly.",
      prerequisites: ["A/sgd", "D/data-parallel"],
    },
    {
      id: "memory-and-sharding",
      title: "Memory math and ZeRO sharding",
      goal: "Account for the optimizer-state, gradient, and parameter memory that dominates large-model training, and compute how ZeRO's three sharding stages divide it across workers.",
      prerequisites: ["data-parallel-training", "D/model-parallel"],
    },
  ],
  I3: [
    {
      id: "latency-throughput",
      title: "Latency, throughput, and the batching tradeoff",
      goal: "Summarize a latency distribution with percentiles, relate concurrency, throughput, and latency through Little's law, and see why batching raises throughput at the cost of tail latency.",
      prerequisites: ["A/expectation"],
    },
    {
      id: "llm-serving",
      title: "Serving LLMs: KV cache and continuous batching",
      goal: "Size the KV-cache memory that bounds autoregressive serving and explain why continuous batching keeps the GPU saturated when requests finish at different lengths.",
      prerequisites: ["latency-throughput", "E/kv-cache", "E/paged-attention"],
    },
    {
      id: "quantization",
      title: "Quantization: affine integer arithmetic",
      goal: "Map floating-point weights to low-bit integers with an affine scale and zero-point, dequantize back, and bound the rounding error that buys memory and bandwidth.",
      prerequisites: ["A/floating-point", "E/quantization"],
    },
    {
      id: "distillation-pruning",
      title: "Distillation and pruning",
      goal: "Shrink a model by training a student on a teacher's temperature-softened outputs and by removing low-magnitude weights, then quantify the size-quality tradeoff each makes.",
      prerequisites: ["A/kl-cross-entropy", "D/regularization"],
    },
    {
      id: "edge-deployment",
      title: "Edge and on-device deployment",
      goal: "Reason about deploying to phones and embedded targets, where the binding constraints are memory, power, and offline operation rather than peak throughput, via exchange formats and graph optimization.",
      prerequisites: ["quantization"],
      codeExempt: true,
    },
  ],
  I4: [
    {
      id: "slos-and-error-budgets",
      title: "SLIs, SLOs, and error budgets",
      goal: "Turn user-facing reliability into a measurable service-level indicator and objective, derive the error budget it implies, and compute the burn rate that should trigger an alert.",
      prerequisites: ["I3/latency-throughput"],
    },
    {
      id: "production-drift",
      title: "Concept drift vs data drift under label delay",
      goal: "Separate a shift in the inputs P(x) from a shift in the labelling rule P(y|x), and monitor each in production when ground-truth labels arrive late or never.",
      prerequisites: ["I1/drift-detection"],
    },
    {
      id: "llm-evaluation",
      title: "LLM evaluation: pass@k and benchmark hygiene",
      goal: "Estimate functional accuracy from sampled generations with the unbiased pass@k estimator, put a confidence interval on a benchmark score, and guard against test-set contamination.",
      prerequisites: ["slos-and-error-budgets", "B/ab-testing"],
    },
    {
      id: "safety-evals-red-teaming",
      title: "Safety evals and red-teaming",
      goal: "Measure how often adversarial prompts break a model with an attack success rate, put a Wilson interval on it, and decide whether two models differ given finite, noisy trials.",
      prerequisites: ["llm-evaluation"],
    },
    {
      id: "cost-monitoring",
      title: "Cost monitoring and token economics",
      goal: "Build a per-request cost model for an LLM service from token counts and hardware utilization, and see how batching and caching change the unit economics.",
      prerequisites: ["I3/llm-serving", "slos-and-error-budgets"],
    },
  ],
};
