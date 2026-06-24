import type { Lesson } from "@/lib/types";

/**
 * Pillar N — Recommender Systems. The ML-engineer track for recommendation:
 * classical foundations → matrix factorization & embeddings → deep retrieval →
 * ranking / learning-to-rank → evaluation & experimentation → fairness & bias →
 * production serving → frontier & generative recsys.
 *
 * Six lessons (collaborative-filtering, matrix-factorization, implicit-feedback,
 * nmf, two-tower, sequential-rec) were relocated here from the former C8; the
 * rest are scaffolded and render "coming soon" until authored.
 */
export const N_CURRICULUM: Record<string, Lesson[]> = {
  N1: [
    {
      id: "content-based-filtering",
      title: "Content-based filtering",
      goal: "Recommend items from their own features and a learned user profile, the baseline that needs no other users.",
      prerequisites: ["A1/inner-products"],
    },
    {
      id: "collaborative-filtering",
      title: "Collaborative filtering",
      goal: "Recommend items by item-item or user-user neighborhoods over the rating matrix.",
    },
    {
      id: "similarity-and-neighborhoods",
      title: "Similarity metrics and neighborhoods",
      goal: "Compare cosine, Pearson, and Jaccard similarity and turn them into user- and item-neighborhoods.",
      prerequisites: ["collaborative-filtering"],
    },
    {
      id: "popularity-and-baselines",
      title: "Popularity and baselines",
      goal: "Build the popularity and most-recent baselines every recommender must beat, and see why they are strong.",
    },
    {
      id: "hybrid-recommenders",
      title: "Hybrid recommenders",
      goal: "Combine content and collaborative signals by weighting, switching, and feature augmentation.",
      prerequisites: ["content-based-filtering", "collaborative-filtering"],
    },
    {
      id: "cold-start",
      title: "The cold-start problem",
      goal: "Handle new users, items, and catalogs with content fallbacks, onboarding, and early exploration.",
      prerequisites: ["popularity-and-baselines", "content-based-filtering"],
    },
  ],
  N2: [
    {
      id: "matrix-factorization",
      title: "Matrix factorization (SVD, ALS)",
      goal: "Factor the rating matrix into low-rank user and item embeddings, fit with ALS or SGD.",
      prerequisites: ["A1/low-rank-pca"],
    },
    {
      id: "implicit-feedback",
      title: "Implicit feedback and weighted MF",
      goal: "Handle clicks and views (not ratings) with weighted alternating least squares.",
      prerequisites: ["matrix-factorization"],
    },
    {
      id: "nmf",
      title: "Non-negative matrix factorization",
      goal: "Restrict factors to be nonnegative and get parts-based representations of users and items.",
      prerequisites: ["matrix-factorization"],
    },
    {
      id: "bayesian-mf",
      title: "Bayesian matrix factorization",
      goal: "Place priors on user and item factors and recover regularization as MAP inference.",
      prerequisites: ["matrix-factorization"],
    },
    {
      id: "factorization-machines",
      title: "Factorization machines",
      goal: "Generalize MF to arbitrary sparse features with pairwise interactions in linear time.",
      prerequisites: ["matrix-factorization"],
    },
    {
      id: "embedding-regularization",
      title: "Embedding regularization and initialization",
      goal: "Regularize and initialize embedding tables so factors stay well-scaled and generalize.",
      prerequisites: ["matrix-factorization"],
    },
  ],
  N3: [
    {
      id: "two-tower",
      title: "Two-tower and neural collaborative filtering",
      goal: "Embed users and items with neural nets and score with a dot product, the basis of modern retrieval.",
      prerequisites: ["N2/matrix-factorization"],
    },
    {
      id: "tower-features",
      title: "Feature engineering for towers",
      goal: "Engineer user- and item-tower features: categoricals, hashing, and dense side-information.",
      prerequisites: ["two-tower", "I1/feature-engineering"],
    },
    {
      id: "embedding-tables",
      title: "Embedding tables and serving",
      goal: "Size, hash, and serve million-row embedding tables within a fixed memory budget.",
      prerequisites: ["two-tower"],
    },
    {
      id: "negative-sampling",
      title: "Hard and in-batch negatives",
      goal: "Train retrieval with in-batch and hard negatives, and correct for sampling bias.",
      prerequisites: ["two-tower"],
    },
    {
      id: "sequential-rec",
      title: "Sequential recommendation",
      goal: "Model user histories as sequences (SASRec, BERT4Rec) and predict the next item.",
      prerequisites: ["two-tower"],
    },
    {
      id: "gnn-recsys",
      title: "Graph neural networks for recsys",
      goal: "Encode the user-item graph with LightGCN and PinSage for collaborative filtering.",
      prerequisites: ["two-tower", "D6/graph-basics"],
    },
    {
      id: "multi-interest",
      title: "Multi-interest and cross-attention towers",
      goal: "Represent a user with several interest vectors and richer cross-attention towers.",
      prerequisites: ["two-tower", "E3/self-attention"],
    },
  ],
  N4: [
    {
      id: "retrieval-vs-ranking",
      title: "Retrieval vs ranking",
      goal: "Separate cheap candidate retrieval from expensive ranking, and see why two stages win.",
      prerequisites: ["N3/two-tower"],
    },
    {
      id: "pointwise-ranking",
      title: "Pointwise ranking",
      goal: "Score each candidate independently with logistic and MLP click-through models.",
      prerequisites: ["retrieval-vs-ranking", "C9/classification-metrics"],
    },
    {
      id: "pairwise-ranking",
      title: "Pairwise ranking (BPR, RankNet)",
      goal: "Learn from preference pairs with BPR, RankNet, and LambdaRank objectives.",
      prerequisites: ["pointwise-ranking"],
    },
    {
      id: "listwise-ranking",
      title: "Listwise ranking and ApproxNDCG",
      goal: "Optimize whole-list metrics directly with ListNet and differentiable ApproxNDCG.",
      prerequisites: ["pairwise-ranking"],
    },
    {
      id: "deep-ctr-models",
      title: "Wide&Deep, DeepFM, DCN, DLRM",
      goal: "Mix memorization and generalization with the standard deep click-through architectures.",
      prerequisites: ["pointwise-ranking"],
    },
    {
      id: "ranking-features",
      title: "Feature engineering for ranking",
      goal: "Build cross-, context-, and freshness features that the ranking stage depends on.",
      prerequisites: ["pointwise-ranking", "I1/feature-stores"],
    },
    {
      id: "multi-task-ranking",
      title: "Multi-task and multi-objective ranking",
      goal: "Predict clicks, conversions, and dwell jointly and trade the objectives off.",
      prerequisites: ["deep-ctr-models"],
    },
    {
      id: "distillation-serving",
      title: "Distillation for served ranking",
      goal: "Distill a heavy ranker into a fast served model that fits the latency budget.",
      prerequisites: ["deep-ctr-models"],
    },
  ],
  N5: [
    {
      id: "ranking-metrics",
      title: "Ranking metrics (nDCG, MAP, MRR)",
      goal: "Define nDCG, MAP, MRR, recall@k, and hit-rate and pick the one that matches the product.",
      prerequisites: ["C9/classification-metrics"],
    },
    {
      id: "beyond-accuracy",
      title: "Beyond accuracy: diversity & novelty",
      goal: "Measure diversity, coverage, novelty, and serendipity, not just relevance.",
      prerequisites: ["ranking-metrics"],
    },
    {
      id: "offline-eval",
      title: "Offline evaluation and splits",
      goal: "Design leakage-free, time-aware train/test splits for recommenders.",
      prerequisites: ["ranking-metrics", "C9/cv-strategies"],
    },
    {
      id: "online-ab-testing",
      title: "Online A/B testing and interleaving",
      goal: "Run trustworthy A/B tests and interleaving with recsys-specific interference in mind.",
      prerequisites: ["I2/experiment-tracking"],
    },
    {
      id: "counterfactual-eval",
      title: "Counterfactual and off-policy evaluation",
      goal: "Evaluate on logged implicit feedback with inverse-propensity weighting.",
      prerequisites: ["offline-eval", "B5/propensity-scores"],
    },
    {
      id: "offline-online-gap",
      title: "The offline-online gap",
      goal: "Diagnose why offline wins fail to reproduce online and close the loop.",
      prerequisites: ["offline-eval", "online-ab-testing"],
    },
  ],
  N6: [
    {
      id: "popularity-bias",
      title: "Popularity bias and amplification",
      goal: "See how popularity bias enters logged data and gets amplified, and how to temper it.",
      prerequisites: ["N1/popularity-and-baselines"],
    },
    {
      id: "exposure-selection-bias",
      title: "Exposure and selection bias",
      goal: "Model the exposure and selection bias baked into implicitly-logged feedback.",
      prerequisites: ["popularity-bias"],
    },
    {
      id: "position-bias-ipw",
      title: "Position bias and IPW correction",
      goal: "Correct position bias with click models and inverse-propensity weighting.",
      prerequisites: ["exposure-selection-bias"],
    },
    {
      id: "fairness-recsys",
      title: "Fairness in recommendation",
      goal: "Define provider and consumer fairness and enforce exposure constraints.",
      prerequisites: ["popularity-bias"],
    },
    {
      id: "filter-bubbles",
      title: "Filter bubbles and healthy diversity",
      goal: "Balance engagement against diversity to avoid filter bubbles and runaway feedback.",
      prerequisites: ["N5/beyond-accuracy"],
    },
    {
      id: "calibration-recsys",
      title: "Calibration for recommenders",
      goal: "Calibrate scores and category proportions so recommendations match user taste.",
      prerequisites: ["C9/calibration"],
    },
  ],
  N7: [
    {
      id: "multi-stage-funnel",
      title: "The multi-stage funnel",
      goal: "Assemble retrieval → ranking → re-ranking into one coherent serving funnel.",
      prerequisites: ["N4/retrieval-vs-ranking"],
    },
    {
      id: "feature-stores-recsys",
      title: "Feature stores for recsys",
      goal: "Serve point-in-time-correct user and item features to both training and inference.",
      prerequisites: ["I1/feature-stores"],
    },
    {
      id: "ann-serving",
      title: "ANN serving at latency",
      goal: "Serve approximate-nearest-neighbor retrieval at p99 latency with HNSW and IVF indexes.",
      prerequisites: ["C8/hnsw"],
    },
    {
      id: "realtime-features",
      title: "Real-time feature computation",
      goal: "Compute session and context features in real time with streaming pipelines.",
      prerequisites: ["feature-stores-recsys"],
    },
    {
      id: "retraining-online-learning",
      title: "Retraining cadence and online learning",
      goal: "Choose batch vs streaming retraining and update embeddings incrementally.",
      prerequisites: ["feature-stores-recsys", "I2/experiment-tracking"],
    },
    {
      id: "serving-latency",
      title: "Serving infrastructure and latency",
      goal: "Budget end-to-end latency and optimize with caching, batching, and quantization.",
      prerequisites: ["multi-stage-funnel", "I3/llm-serving"],
    },
    {
      id: "monitoring-recsys",
      title: "Monitoring and drift",
      goal: "Monitor coverage, click-through, and embedding drift, and alert on degradation.",
      prerequisites: ["I1/drift-detection"],
    },
    {
      id: "contextual-bandits-prod",
      title: "Contextual bandits in production",
      goal: "Explore in production with epsilon-greedy, UCB, and Thompson-sampling bandits.",
      prerequisites: ["H4/bandits-exploration", "realtime-features"],
    },
  ],
  N8: [
    {
      id: "contrastive-recsys",
      title: "Contrastive and self-supervised recsys",
      goal: "Pretrain recommenders with self-supervised contrastive objectives on sparse data.",
      prerequisites: ["D5/contrastive-ssl", "N2/matrix-factorization"],
    },
    {
      id: "causal-recsys",
      title: "Causal recommendation",
      goal: "Treat recommendation as intervention and estimate uplift rather than correlation.",
      prerequisites: ["B5/potential-outcomes"],
    },
    {
      id: "generative-retrieval",
      title: "Generative retrieval and semantic IDs",
      goal: "Generate item ids directly with semantic IDs and TIGER-style sequence models.",
      prerequisites: ["E3/transformer-block", "N3/sequential-rec"],
    },
    {
      id: "llm-recommenders",
      title: "LLM-based recommenders",
      goal: "Use LLMs for zero/few-shot and conversational recommendation.",
      prerequisites: ["E6/rag-fundamentals"],
    },
    {
      id: "kg-recsys",
      title: "Knowledge-graph recommendation",
      goal: "Use knowledge-graph structure to enrich sparse recommendations.",
      prerequisites: ["D6/graph-basics"],
    },
    {
      id: "cross-domain-transfer",
      title: "Cross-domain and transfer recsys",
      goal: "Transfer embeddings and models across domains and cold-start new platforms.",
      prerequisites: ["N2/matrix-factorization"],
    },
  ],
};
