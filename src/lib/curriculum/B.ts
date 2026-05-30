import type { Lesson } from "@/lib/types";

/**
 * Pillar B: Statistics & Causal Inference. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 */
export const B_CURRICULUM: Record<string, Lesson[]> = {
  B1: [
    {
      id: "sampling-distributions",
      title: "Sampling distributions, standard error, and confidence intervals",
      goal: "Treat a statistic as a random variable over repeated samples, derive its standard error via the CLT, and construct a frequentist confidence interval.",
      prerequisites: ["A2/lln-clt", "A2/mle"],
    },
    {
      id: "method-of-moments",
      title: "Method of moments",
      goal: "Equate population moments to sample moments to derive closed-form parameter estimates, and compare MoM and MLE efficiency on the Gamma distribution.",
      prerequisites: ["sampling-distributions"],
    },
    {
      id: "estimator-properties",
      title: "Bias, consistency, and efficiency",
      goal: "Define unbiasedness, consistency (MSE and probability convergence), and efficiency; decompose MSE into squared bias plus variance.",
      prerequisites: ["sampling-distributions"],
    },
    {
      id: "cramer-rao-bound",
      title: "The Cramér-Rao lower bound",
      goal: "Prove the CRLB from the Cauchy-Schwarz inequality and use it to verify that the sample mean achieves the bound for Gaussian location families.",
      prerequisites: ["estimator-properties", "A2/information-geometry"],
    },
    {
      id: "hypothesis-testing",
      title: "Hypothesis testing: z, t, and χ² tests",
      goal: "State null and alternative hypotheses, derive the z-test and t-test for means and the χ² test for variance, and compute p-values from sampling distributions.",
      prerequisites: ["sampling-distributions"],
    },
    {
      id: "anova",
      title: "One-way ANOVA",
      goal: "Partition total sum of squares into between-group and within-group components, derive the F-statistic, and connect ANOVA to the simultaneous comparison of group means.",
      prerequisites: ["hypothesis-testing"],
    },
    {
      id: "multiple-testing",
      title: "Multiple testing: Bonferroni and Benjamini-Hochberg",
      goal: "Quantify how FWER inflates with the number of tests, apply Bonferroni correction, and derive the Benjamini-Hochberg step-up procedure for FDR control.",
      prerequisites: ["hypothesis-testing"],
    },
  ],
  B2: [
    {
      id: "prior-likelihood-posterior",
      title: "Prior, likelihood, and posterior",
      goal: "Derive the posterior from Bayes' rule, compute the normalizing constant for a Beta-Binomial model, and interpret posterior concentration as data accumulates.",
      prerequisites: ["A2/bayes-rule", "A2/mle"],
    },
    {
      id: "conjugate-priors",
      title: "Conjugate prior families",
      goal: "Prove that Beta-Binomial, Dirichlet-Categorical, and Gaussian-Gaussian are conjugate pairs and derive the closed-form posterior update in each case.",
      prerequisites: ["prior-likelihood-posterior", "A2/exponential-family"],
    },
    {
      id: "hierarchical-models",
      title: "Hierarchical Bayesian models",
      goal: "Build a two-level model with hyperpriors over group parameters and explain how partial pooling balances no-pooling and complete pooling.",
      prerequisites: ["conjugate-priors"],
    },
    {
      id: "posterior-predictive",
      title: "Posterior predictive distribution",
      goal: "Marginalize the likelihood over the posterior to form the posterior predictive; compute it in closed form for the Beta-Binomial and Gaussian models.",
      prerequisites: ["hierarchical-models"],
    },
    {
      id: "bayesian-model-comparison",
      title: "Bayesian model comparison",
      goal: "Compute the marginal likelihood as the evidence for model selection, define the Bayes factor, and compare it to frequentist p-values.",
      prerequisites: ["posterior-predictive", "B1/hypothesis-testing"],
    },
  ],
  B3: [
    {
      id: "bootstrap",
      title: "The bootstrap",
      goal: "Estimate the sampling distribution of any statistic by resampling with replacement; construct percentile and BCa confidence intervals.",
      prerequisites: ["B1/sampling-distributions", "B1/estimator-properties"],
    },
    {
      id: "jackknife",
      title: "The jackknife",
      goal: "Use leave-one-out resampling to estimate bias and standard error of an estimator; prove that the jackknife is the first-order Taylor approximation of the bootstrap.",
      prerequisites: ["bootstrap"],
    },
    {
      id: "permutation-tests",
      title: "Permutation tests",
      goal: "Compute an exact permutation p-value by permuting labels under the null; connect permutation tests to the two-sample t-test and rank tests.",
      prerequisites: ["B1/hypothesis-testing"],
    },
    {
      id: "cross-validation",
      title: "Cross-validation strategies",
      goal: "Build k-fold, leave-one-out, stratified, and time-series CV; characterize their bias-variance tradeoff and the conditions under which each is appropriate.",
      prerequisites: ["B1/estimator-properties", "bootstrap"],
    },
  ],
  B4: [
    {
      id: "ab-testing",
      title: "A/B testing and two-sample tests",
      goal: "Design a two-sample proportion test, translate a minimum detectable effect into a sample size, and control Type I and II errors.",
      prerequisites: ["B1/hypothesis-testing", "B1/multiple-testing"],
    },
    {
      id: "power-analysis",
      title: "Power analysis and sample size",
      goal: "Define statistical power as 1-β, derive the required sample size for a two-sample z-test, and plot power as a function of n, δ, and α.",
      prerequisites: ["ab-testing"],
    },
    {
      id: "cuped",
      title: "CUPED and variance reduction",
      goal: "Apply CUPED (Controlled-experiment Using Pre-Experiment Data) to remove pre-experiment covariate variance, and derive the effective variance reduction factor as 1 - ρ².",
      prerequisites: ["power-analysis"],
    },
    {
      id: "multi-armed-bandits",
      title: "Multi-armed bandits",
      goal: "Formalize the explore-exploit tradeoff, prove the UCB1 regret bound, and implement Thompson sampling for Bernoulli arms.",
      prerequisites: ["power-analysis"],
    },
    {
      id: "contextual-bandits",
      title: "Contextual bandits",
      goal: "Extend bandits to contexts; implement LinUCB (linear upper confidence bound) with a ridge-regression reward model and prove its regret bound.",
      prerequisites: ["multi-armed-bandits"],
    },
  ],
  B5: [
    {
      id: "potential-outcomes",
      title: "Potential outcomes and the causal estimand",
      goal: "Define potential outcomes Y(1) and Y(0), the ATE, ATT, and ATU, and state the fundamental problem of causal inference.",
      prerequisites: ["B1/hypothesis-testing"],
    },
    {
      id: "scm-dags",
      title: "Structural causal models and DAGs",
      goal: "Write a structural causal model as a DAG with structural equations; distinguish causes from associations and read intervention effects from the graph.",
      prerequisites: ["potential-outcomes"],
    },
    {
      id: "d-separation",
      title: "d-separation and conditional independence",
      goal: "Apply d-separation through chains, forks, and colliders to read all conditional independencies from a DAG without algebra.",
      prerequisites: ["scm-dags"],
    },
    {
      id: "do-calculus",
      title: "The do-operator and do-calculus",
      goal: "Define do(X=x) as a graph surgery, state the three rules of do-calculus, and derive the backdoor and frontdoor adjustment formulas.",
      prerequisites: ["d-separation"],
    },
    {
      id: "counterfactuals",
      title: "Counterfactuals in structural equation models",
      goal: "Compute counterfactuals by the three-step procedure (abduction, action, prediction) in a structural equation model and connect them to potential outcomes.",
      prerequisites: ["do-calculus"],
    },
    {
      id: "propensity-scores",
      title: "Propensity scores, matching, and IPW",
      goal: "Estimate propensity scores with logistic regression, balance covariates via nearest-neighbor matching, and estimate the ATE with inverse-probability weighting.",
      prerequisites: ["potential-outcomes"],
    },
    {
      id: "iv-estimation",
      title: "Instrumental variables and 2SLS",
      goal: "State the three IV conditions, derive the Wald estimator and two-stage least squares, and identify the local average treatment effect (LATE).",
      prerequisites: ["propensity-scores"],
    },
    {
      id: "diff-in-diff",
      title: "Difference-in-differences and synthetic controls",
      goal: "Apply the parallel-trends assumption to estimate ATT from panel data via DiD, then relax it with a synthetic control built as a convex combination of donor units.",
      prerequisites: ["iv-estimation"],
    },
    {
      id: "double-ml",
      title: "Double / debiased machine learning",
      goal: "Apply the Frisch-Waugh-Lovell theorem with arbitrary ML nuisance estimators and cross-fitting to debias the treatment effect estimate and achieve semiparametric efficiency.",
      prerequisites: ["diff-in-diff"],
    },
    {
      id: "causal-forests",
      title: "Causal forests and meta-learners",
      goal: "Estimate conditional average treatment effects with the T-learner, S-learner, and X-learner, then understand how causal forests enforce honest splitting to avoid overfitting.",
      prerequisites: ["double-ml"],
    },
    {
      id: "causal-representation-learning",
      title: "Causal representation learning",
      goal: "Connect causal structure to identifiable representation learning via independent causal mechanisms, invariant risk minimization, and sparse mechanism shift.",
      prerequisites: ["causal-forests"],
    },
  ],
};
