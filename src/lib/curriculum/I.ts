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
      prerequisites: ["pipeline-paradigms", "A5/graph-traversal"],
    },
    {
      id: "feature-stores",
      title: "Feature stores and point-in-time correctness",
      goal: "Serve the same feature values to training and inference from offline and online stores, and use point-in-time joins to compute training features without leaking the future.",
      prerequisites: ["orchestration-dags"],
    },
    {
      id: "feature-engineering",
      title: "Feature engineering: encoding, scaling, and leakage",
      goal: "Turn raw columns into model-ready features by encoding categoricals and standardizing numerics, fit every transform on the training split only, and see how a leaked statistic silently inflates offline accuracy.",
      prerequisites: ["feature-stores", "A2/expectation"],
    },
    {
      id: "missing-values",
      title: "Missing values: imputation and missingness indicators",
      goal: "Classify why a value is missing, derive how mean imputation shrinks a feature's variance and its correlation with the target, and use a missingness indicator fitted alongside a train-only imputer to keep the signal that the gap itself carries.",
      prerequisites: ["feature-engineering", "A2/variance-moments"],
    },
    {
      id: "categorical-encoding-production",
      title: "Categorical encoding in production: unseen levels, hashing, and target encoding",
      goal: "Encode categoricals so that a level never seen in training maps to a defined vector instead of an error, size a hashing space from the collision probability, and fit target encodings out of fold so a high-cardinality column does not leak its own labels.",
      prerequisites: ["feature-engineering", "missing-values", "A2/expectation"],
    },
    {
      id: "data-versioning",
      title: "Data versioning and content-addressed storage",
      goal: "Make a dataset reproducible by addressing its contents with a hash, deduplicating shared chunks, and pinning a training run to an immutable data snapshot.",
      prerequisites: ["A5/arrays-hashing"],
    },
    {
      id: "drift-detection",
      title: "Detecting data drift: KS statistic and PSI",
      goal: "Quantify how far an incoming data batch has moved from a reference distribution with the Kolmogorov-Smirnov statistic for continuous features and the population stability index for binned ones.",
      prerequisites: ["B1/hypothesis-testing", "A2/kl-cross-entropy"],
    },
  ],
  I2: [
    {
      id: "experiment-tracking",
      title: "Experiment tracking, lineage, and reproducibility",
      goal: "Log the inputs (code, data, config, seed) and outputs (metrics, artifacts) of every run so results are comparable and reproducible, and see why fixing the seed alone is not enough.",
      prerequisites: ["I1/data-versioning", "A3/sgd"],
    },
    {
      id: "model-registry",
      title: "Model registry: versions, aliases, and promotion",
      goal: "Track every trained model as an immutable, versioned artifact and promote it by moving a named alias such as champion, so a deploy is a pointer swap you can audit and roll back rather than a rebuild.",
      prerequisites: ["experiment-tracking"],
      codeExempt: true,
    },
    {
      id: "ml-cicd",
      title: "CI/CD for ML: data, model, and pipeline tests",
      goal: "Gate a model release behind automated checks the way code is gated, schema and distribution tests on the data, behavioral and threshold tests on the model, so a regression fails the pipeline instead of reaching users.",
      prerequisites: ["model-registry", "I1/drift-detection"],
    },
    {
      id: "deploy-code-vs-model",
      title: "Promoting across environments: deploy models vs deploy code",
      goal: "Lay out development, staging, and production environments, choose between promoting a trained model artifact and promoting the code that trains it, and justify the choice from training cost, data access, and retraining cadence.",
      prerequisites: ["model-registry", "ml-cicd"],
      codeExempt: true,
    },
    {
      id: "declarative-deployment",
      title: "Declarative deployment: desired state and reconciliation",
      goal: "Describe jobs, pipelines, and serving endpoints as a desired-state configuration with per-environment overrides, compute a deployment plan as the difference between desired and actual state, and show that applying the plan is idempotent and never touches resources the tool does not own.",
      prerequisites: ["deploy-code-vs-model", "I1/orchestration-dags"],
    },
    {
      id: "hyperparameter-search",
      title: "Hyperparameter search: grid vs random",
      goal: "Frame hyperparameter tuning as black-box optimization over a search space, and see why random search dominates grid search when only a few dimensions actually matter.",
      prerequisites: ["A3/bayesian-optimization"],
    },
    {
      id: "multi-fidelity-hpo",
      title: "Multi-fidelity HPO: successive halving and Hyperband",
      goal: "Spend a fixed compute budget efficiently by training many configurations briefly, then promoting only the survivors, the successive-halving rule behind Hyperband and ASHA.",
      prerequisites: ["hyperparameter-search"],
    },
    {
      id: "tpe",
      title: "Tree-structured Parzen estimator",
      goal: "Derive why the tree-structured Parzen estimator picks the next hyperparameter by maximizing the density ratio l(x)/g(x), implement it in one dimension, and keep the study direction and the objective's sign consistent so the search optimizes the metric you meant.",
      prerequisites: ["hyperparameter-search", "multi-fidelity-hpo", "A3/bayesian-optimization"],
    },
    {
      id: "data-parallel-training",
      title: "Data-parallel training and all-reduce",
      goal: "Scale training across workers by averaging per-worker gradients with all-reduce, prove the average equals the single-machine gradient on the union batch, and scale the learning rate accordingly.",
      prerequisites: ["A3/sgd", "D7/data-parallel"],
    },
    {
      id: "memory-and-sharding",
      title: "Memory math and ZeRO sharding",
      goal: "Account for the optimizer-state, gradient, and parameter memory that dominates large-model training, and compute how ZeRO's three sharding stages divide it across workers.",
      prerequisites: ["data-parallel-training", "D7/model-parallel"],
    },
  ],
  I3: [
    {
      id: "latency-throughput",
      title: "Latency, throughput, and the batching tradeoff",
      goal: "Summarize a latency distribution with percentiles, relate concurrency, throughput, and latency through Little's law, and see why batching raises throughput at the cost of tail latency.",
      prerequisites: ["A2/expectation"],
    },
    {
      id: "inference-modes",
      title: "Batch, streaming, and real-time inference",
      goal: "Place batch, streaming, real-time, and edge inference on one latency and throughput spectrum, derive the average staleness of a batch prediction and the cost of an always-on endpoint, and choose a mode from how fresh the inputs must be and how many entities are actually scored.",
      prerequisites: ["latency-throughput", "I1/pipeline-paradigms"],
    },
    {
      id: "model-packaging",
      title: "Packaging a model: one predict interface, signatures, and environments",
      goal: "Package a trained model behind a uniform predict interface, enforce an input signature by column name so a reordered or mistyped request fails loudly instead of scoring silently, bundle pre- and post-processing into the artifact, and pin the environment it needs.",
      prerequisites: ["inference-modes", "I2/model-registry", "I1/feature-engineering"],
    },
    {
      id: "deployment-strategies",
      title: "Deployment strategies: shadow, canary, and blue-green",
      goal: "Release a new model behind shadow, canary, and blue-green patterns, and size a canary as a two-proportion test so you ship on evidence and roll back on a metric, not a hunch.",
      prerequisites: ["latency-throughput", "B4/ab-testing"],
    },
    {
      id: "llm-serving",
      title: "Serving LLMs: KV cache and continuous batching",
      goal: "Size the KV-cache memory that bounds autoregressive serving and explain why continuous batching keeps the GPU saturated when requests finish at different lengths.",
      prerequisites: [
        "latency-throughput",
        "E5/kv-cache",
        "E5/paged-attention",
      ],
    },
    {
      id: "quantization",
      title: "Quantization: affine integer arithmetic",
      goal: "Map floating-point weights to low-bit integers with an affine scale and zero-point, dequantize back, and bound the rounding error that buys memory and bandwidth.",
      prerequisites: ["A4/floating-point", "E5/quantization"],
    },
    {
      id: "distillation-pruning",
      title: "Distillation and pruning",
      goal: "Shrink a model by training a student on a teacher's temperature-softened outputs and by removing low-magnitude weights, then quantify the size-quality tradeoff each makes.",
      prerequisites: ["A2/kl-cross-entropy", "D1/regularization"],
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
      id: "drift-distances",
      title: "Drift distances: Wasserstein, Jensen-Shannon, and chi-square",
      goal: "Measure drift with the Wasserstein distance in the feature's own units and the bounded Jensen-Shannon divergence, show that a chi-square or KS test statistic grows with sample size so its p-value flags any shift on enough traffic, and alert on a distance instead.",
      prerequisites: ["production-drift", "I1/drift-detection", "A2/kl-cross-entropy"],
    },
    {
      id: "sliced-monitoring",
      title: "Inference logs and sliced monitoring",
      goal: "Log every prediction in a schema that can be joined to late labels, show why an aggregate metric hides a failing slice and how a shift in traffic mix moves it with no slice changing, test many slices without drowning in false alarms, and track per-slice fairness gaps.",
      prerequisites: ["drift-distances", "B1/multiple-testing", "C9/classification-metrics"],
    },
    {
      id: "automated-retraining",
      title: "Automated retraining and continual learning",
      goal: "Decide when a decaying model is worth retraining by weighing accuracy loss against retrain cost, choose a trigger (scheduled vs drift-based), and guard the new model behind a champion-challenger gate.",
      prerequisites: ["production-drift", "I1/drift-detection"],
    },
    {
      id: "llm-evaluation",
      title: "LLM evaluation: pass@k and benchmark hygiene",
      goal: "Estimate functional accuracy from sampled generations with the unbiased pass@k estimator, put a confidence interval on a benchmark score, and guard against test-set contamination.",
      prerequisites: ["slos-and-error-budgets", "B4/ab-testing"],
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
