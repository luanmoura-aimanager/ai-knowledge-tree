import type { Lesson } from "@/lib/types";

/**
 * Pillar M: Advanced Causal Machine Learning. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 *
 * This pillar is the advanced course that sits on top of pillar B's causal
 * foundations (B5). B5 establishes the language (potential outcomes, SCMs,
 * d-separation, do-calculus, propensity scores, IV, diff-in-diff) and the first
 * estimators; pillar M is the machine-learning frontier built on that base:
 * discovering the graph from data, estimating heterogeneous effects, the
 * semiparametric/orthogonal estimation theory behind debiased ML, neural
 * counterfactual models, turning effects into decisions (policy learning and
 * off-policy evaluation), and the robustness layer that stress-tests the
 * untestable assumptions. Prerequisites point back into B5 rather than
 * re-teaching it.
 */
export const M_CURRICULUM: Record<string, Lesson[]> = {
  M1: [
    {
      id: "discovery-problem",
      title: "The causal discovery problem and Markov equivalence",
      goal: "State what observational data can and cannot reveal about a DAG, and characterize the Markov equivalence class a CPDAG summarizes.",
      prerequisites: ["B5/scm-dags", "B5/d-separation"],
    },
    {
      id: "pc-algorithm",
      title: "Constraint-based discovery: the PC algorithm",
      goal: "Recover the skeleton by conditional-independence testing, then orient colliders and propagate Meek's rules to a CPDAG.",
      prerequisites: ["discovery-problem"],
    },
    {
      id: "ges-score",
      title: "Score-based discovery: greedy equivalence search",
      goal: "Score a DAG with a decomposable, consistent criterion (BIC) and search equivalence-class space with GES forward and backward phases.",
      prerequisites: ["discovery-problem"],
    },
    {
      id: "lingam",
      title: "Functional models: LiNGAM and additive noise",
      goal: "Use non-Gaussianity and nonlinear additive noise to orient edges a CPDAG leaves undirected, recovering a fully directed graph.",
      prerequisites: ["discovery-problem"],
    },
    {
      id: "notears",
      title: "Continuous structure learning: NOTEARS",
      goal: "Replace the combinatorial acyclicity constraint with a smooth trace-exponential penalty and learn a weighted DAG by gradient descent.",
      prerequisites: ["ges-score", "L6/steepest-descent"],
    },
    {
      id: "fci-latent",
      title: "Latent confounders and selection: FCI and PAGs",
      goal: "Extend constraint-based discovery to unobserved confounding, reading bidirected edges and partial ancestral graphs.",
      prerequisites: ["pc-algorithm"],
    },
  ],
  M2: [
    {
      id: "cate-estimand",
      title: "The CATE estimand and conditional ignorability",
      goal: "Define the conditional average treatment effect, state the identification assumptions it needs, and see why an average effect hides decision-relevant heterogeneity.",
      prerequisites: ["B5/potential-outcomes", "B5/propensity-scores"],
    },
    {
      id: "meta-learners",
      title: "Meta-learners: S, T, and X",
      goal: "Build CATE estimators by wrapping any regression learner (S-, T-, and X-learner) and reason about which wins under imbalance.",
      prerequisites: ["cate-estimand"],
    },
    {
      id: "r-learner",
      title: "The R-learner and Robinson's transformation",
      goal: "Derive the Robinson residual-on-residual loss and turn it into an orthogonal objective whose minimizer is the CATE.",
      prerequisites: ["meta-learners", "B5/double-ml"],
    },
    {
      id: "dr-learner",
      title: "The DR-learner and the doubly-robust pseudo-outcome",
      goal: "Construct the AIPW pseudo-outcome whose conditional mean is the CATE, then regress it on covariates for a doubly-robust estimator.",
      prerequisites: ["r-learner"],
    },
    {
      id: "generalized-random-forests",
      title: "Generalized random forests and causal forests",
      goal: "Estimate the CATE by solving a local moment condition with forest-derived weights, using honest splitting to get valid confidence intervals.",
      prerequisites: ["dr-learner", "B5/causal-forests"],
    },
    {
      id: "uplift-modeling",
      title: "Uplift modeling and its evaluation",
      goal: "Frame targeting as uplift, score models with the Qini and uplift curves, and estimate the value of a treatment policy from logged data.",
      prerequisites: ["meta-learners"],
    },
  ],
  M3: [
    {
      id: "influence-functions",
      title: "Influence functions and the efficiency bound",
      goal: "Read an estimator's first-order behavior off its influence function and identify the efficient influence function that sets the semiparametric variance bound.",
      prerequisites: ["M2/cate-estimand", "B1/estimator-properties"],
    },
    {
      id: "neyman-orthogonality",
      title: "Neyman orthogonality",
      goal: "Define a Neyman-orthogonal moment, show its insensitivity to first-order nuisance error via the Gateaux derivative, and see why it is what makes debiased ML work.",
      prerequisites: ["influence-functions", "B5/double-ml"],
    },
    {
      id: "aipw",
      title: "Augmented IPW and double robustness",
      goal: "Derive the AIPW estimator of the ATE from the efficient influence function and prove it is consistent if either the outcome or the propensity model is correct.",
      prerequisites: ["neyman-orthogonality", "B5/propensity-scores"],
    },
    {
      id: "tmle",
      title: "Targeted maximum likelihood estimation",
      goal: "Update an initial outcome model with a propensity-driven fluctuation step so the plug-in estimate solves the efficient influence-function equation.",
      prerequisites: ["aipw"],
    },
    {
      id: "auto-dml-riesz",
      title: "Automatic debiased ML and Riesz representers",
      goal: "Express the bias correction as a Riesz representer and learn it directly by minimizing the Riesz loss, avoiding hand-derived nuisance scores.",
      prerequisites: ["aipw"],
    },
    {
      id: "dml-inference",
      title: "Inference after debiased ML",
      goal: "Build cross-fitted confidence intervals from the orthogonal score's variance and understand when the normal approximation is trustworthy.",
      prerequisites: ["neyman-orthogonality", "B3/cross-validation"],
    },
  ],
  M4: [
    {
      id: "representation-balancing",
      title: "Balancing representations for counterfactuals",
      goal: "Frame ITE estimation as a covariate-shift problem and bound the counterfactual error with an integral-probability-metric penalty on the representation.",
      prerequisites: ["M2/cate-estimand", "B5/causal-representation-learning"],
    },
    {
      id: "tarnet-dragonnet",
      title: "TARNet and Dragonnet",
      goal: "Build a shared-trunk network with per-treatment heads, add a propensity head and targeted regularization, and read off the ITE.",
      prerequisites: ["representation-balancing", "M3/aipw"],
    },
    {
      id: "ganite",
      title: "Generative counterfactuals with GANITE",
      goal: "Impute counterfactual outcomes with a counterfactual GAN, then train an ITE network on the completed potential-outcome table.",
      prerequisites: ["tarnet-dragonnet", "D4/gan"],
    },
    {
      id: "cevae",
      title: "Latent-confounder models: CEVAE",
      goal: "Treat the confounder as a latent variable and recover effects with a variational autoencoder over the proxy-treatment-outcome structure.",
      prerequisites: ["representation-balancing", "D4/vae"],
    },
    {
      id: "deep-iv",
      title: "Deep instrumental variables",
      goal: "Replace two-stage least squares with two neural stages: a treatment density given the instrument, then an outcome network trained against it.",
      prerequisites: ["B5/iv-estimation", "tarnet-dragonnet"],
    },
  ],
  M5: [
    {
      id: "optimal-policies",
      title: "From effects to decisions: the optimal policy",
      goal: "Define a treatment policy and its value, and show the value-maximizing policy treats exactly the units with positive CATE.",
      prerequisites: ["M2/dr-learner"],
    },
    {
      id: "off-policy-evaluation",
      title: "Off-policy evaluation",
      goal: "Estimate a new policy's value from logged data with inverse-propensity scoring, the direct method, and the doubly-robust estimator, and compare their variance.",
      prerequisites: ["optimal-policies", "M3/aipw"],
    },
    {
      id: "policy-learning",
      title: "Policy learning from observational data",
      goal: "Turn off-policy value into an optimization objective (outcome-weighted learning and policy trees) and bound the regret of the learned policy.",
      prerequisites: ["off-policy-evaluation"],
    },
    {
      id: "counterfactual-risk-minimization",
      title: "Counterfactual risk minimization",
      goal: "Control the variance of an off-policy objective with clipping and self-normalized importance weights, and add the sample-variance penalty CRM prescribes.",
      prerequisites: ["off-policy-evaluation"],
    },
    {
      id: "offline-contextual-bandits",
      title: "Offline contextual bandits and the RL bridge",
      goal: "Cast policy learning as an offline contextual bandit, connect it to the exploration of B4 and the off-policy value of reinforcement learning.",
      prerequisites: ["policy-learning", "B4/contextual-bandits"],
    },
  ],
  M6: [
    {
      id: "unconfoundedness-failure",
      title: "When ignorability fails",
      goal: "Quantify the bias a hidden confounder injects into an adjusted estimate, and frame sensitivity analysis as asking how strong that confounder would have to be.",
      prerequisites: ["M3/aipw", "B5/counterfactuals"],
    },
    {
      id: "sensitivity-rosenbaum-evalue",
      title: "Sensitivity analysis: Rosenbaum bounds and the E-value",
      goal: "Bound how much unmeasured confounding it takes to overturn a finding, computing Rosenbaum's gamma and the E-value from an observed effect.",
      prerequisites: ["unconfoundedness-failure"],
    },
    {
      id: "partial-identification-bounds",
      title: "Partial identification and Manski bounds",
      goal: "Drop point identification and report the interval of effects consistent with the data and weak assumptions, deriving the no-assumption and monotonicity bounds.",
      prerequisites: ["unconfoundedness-failure"],
    },
    {
      id: "negative-controls-proximal",
      title: "Negative controls and proximal causal inference",
      goal: "Use outcome and exposure proxies of an unmeasured confounder to identify effects through the proximal bridge function.",
      prerequisites: ["unconfoundedness-failure", "B5/iv-estimation"],
    },
    {
      id: "refutation-tests",
      title: "Refutation and falsification tests",
      goal: "Stress-test an estimate with placebo treatments, random common causes, and data-subset refuters, and read what each failure implies.",
      prerequisites: ["sensitivity-rosenbaum-evalue"],
    },
  ],
};
