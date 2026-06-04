/**
 * dag.ts: single source of truth for the knowledge tree.
 *
 * Two exports:
 *
 *   PILLARS     : array of 10 top-level pillars (A → J), each with subsections
 *                  and topics. Coverage status reflects what AI ML Theory
 *                  already covers; `hot` flags frontier material.
 *
 *   CONNECTIONS : cross-pillar edges that link related subsections (e.g.
 *                  D4 Generative DL ↔ F8 Bayesian DL because VAEs are in both).
 *                  Used by /connections to draw the live DAG.
 *
 * Topic data is the structural skeleton, NOT the chapter prose. Actual MDX
 * sessions live under /content and are wired in later.
 */

import type { Pillar, Connection, Path } from "./types";

// -------------------------------------------------------------------------
// PILLARS
// -------------------------------------------------------------------------

export const PILLARS: Pillar[] = [
  {
    letter: "A",
    slug: "A-foundations",
    name: "Foundations",
    shortName: "Foundations",
    tagline: "Math, prob, opt, numerical, DSA",
    color: "#e0af68",
    intro:
      "Foundations is the mathematical and computational bedrock the rest of the tree stands on. Every model you will meet later is, underneath, linear algebra applied to data, a probability model fit by optimization, and an algorithm that has to run in finite time and memory. This pillar builds those four pieces from first principles so that nothing downstream has to be taken on faith.\n\nYou will start with linear algebra (vector spaces, eigenstructure, the SVD, and the matrix factorizations that power least squares and PCA), then probability and information theory (distributions, Bayes' rule, entropy and KL divergence, the language of all modeling under uncertainty). From there you turn to optimization theory (gradient methods, convexity, the KKT conditions, and the Adam family that trains real networks), then to numerical methods (floating point, conditioning, and stability, the difference between math that works on paper and code that works at scale). The pillar closes with the data structures and algorithms you need to make any of it tractable.\n\nTreat this as the reference you will return to. You do not need to master every lesson before moving on, but the more fluent you are here, the less the later pillars will feel like magic.",
    prerequisites: [
      "Single-variable calculus: derivatives, the chain rule, and integrals.",
      "Comfort reading and writing basic Python (loops, functions, arrays).",
      "High-school algebra and trigonometry; familiarity with vectors and matrices helps but is rebuilt from scratch in A1.",
    ],
    subs: [
      {
        id: "A1",
        name: "Linear algebra",
        intro:
          "Linear algebra is the language of data once you stack it into vectors and matrices. Almost everything downstream, from a least-squares fit to a transformer's attention block, is some arrangement of linear maps acting on high-dimensional points, so this discipline is where you learn to see those operations clearly instead of as opaque tensor shapes.\n\nYou will build from vector spaces, bases, and the four fundamental subspaces up through eigenvalues, the spectral theorem, and the singular value decomposition, then put them to work: low-rank approximation and PCA, the LU/QR/Cholesky factorizations that solve linear systems without inverting anything, least squares and the pseudo-inverse, and the matrix calculus and einsum notation that make backpropagation just the chain rule on arrays. By the end you can decompose a matrix, reason about why a system is solvable, and differentiate vector-valued expressions by hand.\n\nThis is the most reused pillar in the tree. PCA, recommender factorizations, the geometry of embeddings, and the entire training loop of deep networks all rest on what you build here, so fluency now pays off in every later subject.",
        prerequisites: [
          "High-school algebra and trigonometry; comfort manipulating symbolic expressions.",
          "Single-variable calculus: derivatives and the chain rule.",
          "Basic Python with numpy (arrays, indexing); vectors and matrices are rebuilt from scratch here.",
        ],
        topics: [
          { name: "Vector spaces, norms, basis", status: "covered" },
          { name: "Matrix calculus, chain rule", status: "covered" },
          { name: "Eigendecomposition, SVD", status: "gap" },
          { name: "Matrix factorizations (LU, QR, Cholesky)", status: "gap" },
          { name: "Pseudo-inverse, least squares", status: "gap" },
          { name: "Tensor algebra, einsum", status: "gap" },
        ],
      },
      {
        id: "A2",
        name: "Probability & info theory",
        intro:
          "Probability is how you reason quantitatively about uncertainty, and information theory measures how much a distribution actually tells you. Together they are the modeling language of machine learning: every loss function, every generative model, and every notion of how confident a prediction should be is, underneath, a statement about probability.\n\nYou will start from the Kolmogorov axioms and random variables, work through expectation, variance, and the moment generating function, then the joint, marginal, and conditional view that leads to Bayes' rule. From there you meet the workhorse distributions and the exponential family, the Markov, Chebyshev, and Jensen inequalities, and the law of large numbers and central limit theorem that explain why averages behave. The discipline then turns to estimation (maximum likelihood, MAP, conjugate priors) and to information theory: entropy, KL divergence, cross-entropy, and mutual information, closing with Markov chains and a first look at Fisher information and information geometry.\n\nYou will leave able to write a likelihood, derive an estimator, and recognize cross-entropy loss as maximum likelihood in disguise. That vocabulary underpins pillar B statistics, the VAEs and diffusion models of pillar D, the RLHF penalty in pillar E, and the graphical models of pillar F.",
        prerequisites: [
          "Single-variable calculus and basic integration (for continuous densities and expectations).",
          "A1 Linear algebra: vectors, matrices, and eigenvalues (used in the Markov-chain lesson).",
          "Comfort running small numerical experiments in Python with numpy.",
        ],
        topics: [
          {
            name: "Distributions (Bernoulli, Gaussian, exp. family)",
            status: "covered",
          },
          { name: "Bayes rule, conditional probability", status: "covered" },
          {
            name: "Entropy, KL divergence, mutual information",
            status: "covered",
          },
          { name: "Cross-entropy, MLE", status: "covered" },
          { name: "MAP, conjugate priors", status: "gap" },
          { name: "Concentration inequalities", status: "gap" },
          { name: "Markov chains, stochastic processes", status: "gap" },
          { name: "Information geometry", status: "gap", hot: true },
        ],
      },
      {
        id: "A3",
        name: "Optimization theory",
        intro:
          "Optimization is how a model learns: you write down a loss surface and then search it for the parameters that make the loss small. Training a neural network, fitting a logistic regression, and tuning a support vector machine are all the same problem in different clothing, which is minimizing a function you can differentiate.\n\nYou will formalize what a minimum is through the gradient and Hessian, study convex sets and convex functions (the cases where local means global), and then build the descent methods in order: gradient descent and its convergence guarantees, stochastic gradient descent, momentum and Nesterov acceleration, and the adaptive AdaGrad/RMSProp/Adam family that trains real networks. The discipline also covers constrained optimization through Lagrange multipliers, duality, and the KKT conditions, then second-order and specialized methods (Newton, BFGS and L-BFGS, proximal gradient for nonsmooth penalties, and Bayesian optimization for expensive black boxes).\n\nAfter this you can read an optimizer's update rule and know why it behaves as it does, diagnose slow or unstable training, and choose a method to match a problem's structure. Every training loop in pillars C through H is an instance of what you study here.",
        prerequisites: [
          "A1 Linear algebra: matrix calculus, quadratic forms, and the spectral theorem.",
          "Single-variable and basic multivariable calculus (gradients, partial derivatives).",
          "A2 Probability helps for the stochastic methods and Bayesian optimization.",
        ],
        topics: [
          { name: "Gradient descent, SGD, momentum", status: "covered" },
          { name: "Adam family (Adam, AdamW, RMSProp)", status: "covered" },
          { name: "Convex optimization (Boyd)", status: "gap" },
          { name: "KKT, Lagrangian duality", status: "gap" },
          { name: "Newton, BFGS, L-BFGS", status: "gap" },
          { name: "Proximal methods", status: "gap" },
          { name: "Bayesian optimization", status: "gap", hot: true },
        ],
      },
      {
        id: "A4",
        name: "Numerical methods",
        intro:
          "Numerical methods are the gap between mathematics on paper and code that runs correctly at scale. Computers store real numbers in finite precision, so an algorithm that is exact in theory can quietly lose all its accuracy, and this discipline teaches you to predict, detect, and prevent that failure.\n\nYou will start with IEEE-754 floating point and machine epsilon, then separate the conditioning of a problem from the stability of an algorithm and bound error with the condition number. You will see catastrophic cancellation and learn to reformulate around it, derive the log-sum-exp trick behind a stable softmax, and study iterative solvers: fixed-point iteration, conjugate gradient for symmetric positive-definite systems, and GMRES for the nonsymmetric case. The discipline closes with mixed-precision arithmetic (fp32 versus fp16 and bf16, plus loss scaling), the foundation of modern large-scale training.\n\nThis is short but high-leverage. The skills here explain why a naive softmax overflows, why an ill-conditioned matrix wrecks a least-squares fit, and how billion-parameter models train in low precision without diverging, which connects directly to the training systems of pillar D.",
        prerequisites: [
          "A1 Linear algebra: the SVD, condition number, and positive-definite systems.",
          "Single-variable calculus and basic familiarity with exponentials and logarithms.",
          "Python with numpy to reproduce overflow, cancellation, and precision experiments.",
        ],
        topics: [
          { name: "Numerical stability (log-sum-exp)", status: "covered" },
          { name: "Iterative solvers (CG, GMRES)", status: "gap" },
          { name: "Mixed-precision arithmetic", status: "gap", hot: true },
        ],
      },
      {
        id: "A5",
        name: "Data structures & algorithms",
        intro:
          "Data structures and algorithms are what make any of the math actually run within finite time and memory. A correct model that is too slow to train or serve is useless, so this discipline gives you the toolkit for choosing representations and procedures that scale, and the analysis to know in advance which ones will.\n\nYou will begin with asymptotic complexity and amortized analysis, then build the core structures (dynamic arrays and hash maps, linked lists, stacks and queues, balanced search trees, and heaps) and the sorting algorithms that hit the n log n bound. From there come the algorithm-design paradigms: divide and conquer with the master theorem, dynamic programming, and greedy methods with the exchange argument. The discipline then covers graphs (representations, BFS and DFS, Dijkstra's shortest paths, and minimum spanning trees) and finishes with probabilistic structures, Bloom filters and HyperLogLog, that trade exactness for huge space savings.\n\nThese skills are the difference between a pipeline that finishes and one that stalls. Graph algorithms feed directly into the graph neural networks of pillar D, and the probabilistic sketches and nearest-neighbor thinking here reappear across retrieval, feature stores, and large-scale systems.",
        prerequisites: [
          "Comfortable Python: writing functions, loops, and using lists and dictionaries.",
          "Basic discrete math and logarithms for the complexity analysis.",
          "A2 Probability (common distributions) for the Bloom filter and HyperLogLog lesson.",
        ],
        topics: [
          { name: "Complexity analysis (Big-O, amortized)", status: "gap" },
          { name: "Core DSA (arrays, hashmaps, trees, heaps)", status: "gap" },
          { name: "Algorithm paradigms (DP, greedy, D&C)", status: "gap" },
          { name: "Graph algorithms (BFS/DFS, Dijkstra, MST)", status: "gap" },
          { name: "Probabilistic structures (Bloom, HLL)", status: "gap" },
        ],
      },
    ],
  },
  {
    letter: "B",
    slug: "B-statistics-causal",
    name: "Statistics & Causal Inference",
    shortName: "Stats & Causal",
    tagline: "Frequentist, Bayesian, causal, experimental design",
    color: "#f7768e",
    intro:
      "Statistics is how you reason from a finite sample back to the world that produced it, and causal inference is how you go from 'these two things move together' to 'this one causes that one.' This pillar is the inferential backbone behind every honest model evaluation and every experiment you will run.\n\nYou will study frequentist inference (estimators, sampling distributions, confidence intervals, and hypothesis tests), then Bayesian inference (priors, likelihoods, posteriors, and credible intervals), then the resampling and validation machinery (bootstrap, permutation tests, cross-validation) that your metrics actually rest on. From there you turn to experimental design (randomization, A/B tests, statistical power) and finally causal inference (potential outcomes, confounding, backdoor adjustment, and instrumental variables), where the central lesson is that prediction and intervention are not the same question.\n\nThis is the pillar that keeps the rest of the tree honest: it tells you when a number means something and when it is noise.",
    prerequisites: [
      "A2 Probability and information theory: distributions, expectation, and Bayes' rule.",
      "Single-variable calculus and basic linear algebra (A1).",
      "Comfort running numerical experiments in Python and numpy.",
    ],
    subs: [
      {
        id: "B1",
        name: "Frequentist inference",
        intro:
          "Frequentist inference is the art of reasoning from a finite sample back to the parameters of the population that produced it, without ever assuming a prior over those parameters. The estimate you compute is itself a random variable, so the whole game is understanding how it would vary if you drew the data again, and turning that variability into honest statements like confidence intervals and p-values.\n\nYou will learn to treat a statistic as a sampling distribution, derive its standard error from the central limit theorem, and build confidence intervals around it. You will derive estimators by maximum likelihood and the method of moments, judge them by bias, consistency, and efficiency, and prove the Cramér-Rao bound that limits how good any unbiased estimator can be. Then you will run real tests: z, t, and chi-square tests, one-way ANOVA, and the Bonferroni and Benjamini-Hochberg corrections that keep many simultaneous tests honest.\n\nThis is the machinery behind every reported metric, A/B test, and significance claim downstream, so it is what separates a result that means something from a number that is noise.",
        prerequisites: [
          "A2 Probability and information theory: distributions, expectation, the law of large numbers, and the CLT",
          "Maximum likelihood estimation (A2)",
          "Comfort running numerical experiments in Python and numpy",
        ],
        topics: [
          { name: "MLE", status: "covered" },
          { name: "Method of moments, MAP", status: "gap" },
          { name: "Estimator properties", status: "gap" },
          { name: "Fisher information, Cramér-Rao", status: "gap" },
          { name: "Hypothesis testing (z, t, χ², ANOVA)", status: "gap" },
          { name: "Multiple testing (Bonferroni, BH-FDR)", status: "gap" },
        ],
      },
      {
        id: "B2",
        name: "Bayesian inference",
        intro:
          "Bayesian inference treats unknown parameters as quantities you hold beliefs about, encoded as a prior, and then updates those beliefs against data to form a posterior. Instead of a single point estimate plus a confidence interval, you get a full distribution over the parameter, which makes uncertainty a first-class citizen and lets you pool information across related problems.\n\nYou will derive the posterior from Bayes' rule and work the normalizing constant explicitly for a Beta-Binomial model, then prove conjugacy for the Beta-Binomial, Dirichlet-Categorical, and Gaussian-Gaussian pairs so the posterior update becomes a closed form. From there you will build hierarchical models with hyperpriors and see how partial pooling sits between no-pooling and complete pooling, form the posterior predictive distribution by marginalizing the likelihood over the posterior, and compare models through the marginal likelihood and Bayes factors.\n\nThis pillar is the conceptual seed of much that follows: the same posterior reasoning powers the variational inference and MCMC of probabilistic graphical models (F), Bayesian deep learning, and principled uncertainty estimation throughout ML.",
        prerequisites: [
          "A2 Probability and information theory: Bayes' rule, the exponential family, and marginalization",
          "B1 Frequentist inference (MLE, hypothesis testing) for the contrasts and model comparison",
          "Comfort with Python and numpy for the closed-form posterior computations",
        ],
        topics: [
          { name: "Prior / likelihood / posterior", status: "gap" },
          { name: "Conjugate families", status: "gap" },
          { name: "Hierarchical Bayesian models", status: "gap" },
          { name: "Posterior predictive checks", status: "gap" },
        ],
      },
      {
        id: "B3",
        name: "Resampling & validation",
        intro:
          "Resampling and validation give you the sampling distribution of a statistic when no clean formula exists, by reusing the data you already have. Rather than deriving a standard error analytically, you simulate variability: resample, recompute, and let the spread of the results stand in for the distribution you cannot write down.\n\nYou will build the bootstrap to estimate the sampling distribution of any statistic by resampling with replacement, construct percentile and BCa intervals, and use the jackknife's leave-one-out scheme to estimate bias and standard error (and see why it is a first-order approximation of the bootstrap). You will run permutation tests that compute exact p-values by shuffling labels under the null, and you will design cross-validation strategies (k-fold, leave-one-out, stratified, and time-series) while reasoning carefully about their bias-variance tradeoffs.\n\nThese tools are the honest backbone of model evaluation: cross-validation is how you estimate generalization without fooling yourself, and the bootstrap is how you put error bars on metrics that have no textbook formula. Every claim that a model is better rests on getting this right.",
        prerequisites: [
          "B1 Frequentist inference: sampling distributions, estimator properties, hypothesis testing",
          "A2 Probability and information theory",
          "Comfort writing resampling loops in Python and numpy",
        ],
        topics: [
          { name: "Bootstrap, jackknife", status: "gap" },
          { name: "Permutation tests", status: "gap" },
          { name: "Cross-validation strategies", status: "gap" },
        ],
      },
      {
        id: "B4",
        name: "Experimental design",
        intro:
          "Experimental design is how you collect data so that a comparison actually answers the question you care about. Randomization is the lever: assign treatment by chance and the groups become comparable on everything you did not measure, which is what turns a difference in outcomes into evidence about the treatment itself.\n\nYou will design two-sample tests for A/B experiments, translate a minimum detectable effect into a required sample size, and reason about Type I and Type II errors. You will define statistical power as 1 minus beta and trace how it depends on sample size, effect size, and alpha; apply CUPED to strip out pre-experiment variance and run experiments faster; and move from fixed experiments to adaptive ones with multi-armed bandits (UCB1 and Thompson sampling) and their contextual extension, LinUCB, complete with regret bounds.\n\nThis is the practical engine of data-driven product decisions, and the bandit material connects directly to the explore-exploit problem at the heart of reinforcement learning (H).",
        prerequisites: [
          "B1 Frequentist inference: hypothesis testing and multiple-testing corrections",
          "A2 Probability and information theory (distributions, expectation, variance)",
          "Comfort simulating experiments and regret curves in Python and numpy",
        ],
        topics: [
          { name: "A/B testing (CUPED, sequential)", status: "gap" },
          { name: "Power analysis, sample-size", status: "gap" },
          { name: "Multi-armed bandits", status: "gap", hot: true },
          { name: "Contextual bandits", status: "gap", hot: true },
        ],
      },
      {
        id: "B5",
        name: "Causal inference",
        intro:
          "Causal inference is how you move from 'these two things move together' to 'this one causes that one,' the question correlation alone can never settle. It gives you a precise language for interventions and counterfactuals, so you can ask what would happen if you changed something, not just what tends to co-occur in data you happened to observe.\n\nYou will define potential outcomes and the ATE, ATT, and ATU, then encode assumptions as structural causal models and DAGs, read off independencies with d-separation, and use the do-operator and do-calculus to derive backdoor and frontdoor adjustment. You will estimate effects in practice through propensity scores and inverse-probability weighting, instrumental variables and two-stage least squares, and difference-in-differences with synthetic controls, before reaching modern methods: double/debiased ML with cross-fitting, causal forests and meta-learners for heterogeneous effects, and causal representation learning.\n\nThis is the pillar that keeps decisions honest. It underpins rigorous experimentation, policy evaluation, and uplift modeling, and it connects forward to causal time series (G5) where intervention questions meet forecasting.",
        prerequisites: [
          "B1 Frequentist inference: hypothesis testing, estimators, and standard errors",
          "C1 Linear and logistic regression (used inside propensity, IV, and DML estimators)",
          "A2 Probability and information theory; comfort with Python and numpy",
        ],
        topics: [
          { name: "Structural causal models (Pearl)", status: "gap" },
          { name: "DAGs, d-separation", status: "gap" },
          { name: "do-calculus, identifiability", status: "gap" },
          { name: "Counterfactuals & potential outcomes", status: "gap" },
          { name: "Propensity scores, IPW", status: "gap" },
          { name: "Instrumental variables", status: "gap" },
          { name: "Diff-in-differences, synthetic controls", status: "gap" },
          { name: "Double / debiased ML", status: "gap", hot: true },
          { name: "Causal forests, meta-learners", status: "gap", hot: true },
          { name: "Causal representation learning", status: "gap", hot: true },
        ],
      },
    ],
  },
  {
    letter: "C",
    slug: "C-classical-ml",
    name: "Classical Machine Learning",
    shortName: "Classical ML",
    tagline: "Linear, kernel, tree, clustering, rec sys, ANN",
    color: "#ff9e64",
    intro:
      "Classical machine learning is everything that turns features into predictions without a deep network, and for most tabular problems it is still the right tool: strong theory, modest data requirements, and models you can actually explain. Long before transformers, these algorithms were the field, and gradient-boosted trees remain the quiet winner of a large share of real-world prediction tasks.\n\nYou will cover linear models and GLMs, margin and kernel methods (support vector machines), tree-based methods and gradient boosting, instance-based and probabilistic classifiers, and unsupervised learning (clustering and dimensionality reduction). On top of that sit anomaly detection, ensembles, recommendation systems, and approximate nearest neighbor search with vector databases, the retrieval substrate that modern LLM applications also lean on. The pillar closes with how to evaluate and select among all of these without fooling yourself.\n\nMaster this pillar and you will reach for a 200-line scikit-learn pipeline before a GPU, and be right to.",
    prerequisites: [
      "A1 Linear algebra and A3 optimization (gradient descent, convexity).",
      "A2 Probability; B3 resampling and validation makes the evaluation lessons land harder.",
      "Working Python with numpy; scikit-learn familiarity helps.",
    ],
    subs: [
      {
        id: "C1",
        name: "Linear & GLMs",
        intro:
          "Linear models and generalized linear models are the workhorses of classical machine learning: a weighted sum of features, optionally squeezed through a link function, that turns inputs into a prediction. They are fast to fit, easy to interpret, and backed by clean theory, which is why they remain the default first model on most tabular problems and the baseline everything fancier has to beat.\n\nYou will derive ordinary least squares from the normal equations and read it as a projection onto the column space, then see the same fit fall out of maximum likelihood under Gaussian noise. From there you will work through the bias-variance tradeoff, the ridge, LASSO, and elastic-net penalties (and why L1 yields sparse coefficients), logistic and softmax regression for classification, and the exponential-family framework that unifies them with Poisson and Gamma GLMs for counts and durations.\n\nThese ideas recur everywhere downstream: a neural network is a stack of linear models with nonlinearities between them, regularization shows up in every training loop, and the cross-entropy loss you meet here is the loss that trains modern language models.",
        prerequisites: [
          "A1 Linear algebra: least squares, projections, eigenvalues and the SVD.",
          "A2 Probability and information theory: MLE, the exponential family, cross-entropy.",
          "A3 Optimization: gradient descent and proximal methods (for the LASSO).",
        ],
        topics: [
          { name: "Linear regression (OLS, MLE)", status: "covered" },
          { name: "Logistic regression", status: "covered" },
          { name: "Softmax / multinomial", status: "covered" },
          { name: "Regularization (L1/L2/ElasticNet)", status: "partial" },
          { name: "GLMs (Poisson, Gamma)", status: "gap" },
        ],
      },
      {
        id: "C2",
        name: "Margin & kernel methods",
        intro:
          "Margin and kernel methods ask a sharper question than ordinary classifiers: not just where to draw the boundary, but how to draw it with the widest possible buffer between classes. Support vector machines formalize that intuition, and the kernel trick then lets you carry it into rich, even infinite-dimensional feature spaces without ever computing the features explicitly. The payoff is strong, principled models that work well even when data is scarce.\n\nYou will start with the perceptron and its convergence proof, build the hard-margin SVM as a quadratic program, relax it with slack variables and the hinge loss, and pass to the dual to see support vectors emerge from the KKT conditions. Then you will replace inner products with Mercer kernels, construct the RBF and polynomial workhorses, and finish with Gaussian process regression, which treats the unknown function itself as a distribution and returns calibrated uncertainty for free.\n\nThe margin idea reaches far beyond SVMs (it underlies one-class novelty detection and much of statistical learning theory), and Gaussian processes are the backbone of Bayesian optimization and principled uncertainty estimates throughout ML.",
        prerequisites: [
          "A1 Linear algebra: inner products, norms, positive-definite matrices.",
          "A3 Optimization: convexity, KKT conditions, and Lagrangian duality.",
          "A2 Probability: Gaussians and conjugate priors (for Gaussian processes).",
        ],
        topics: [
          { name: "Support Vector Machines", status: "gap" },
          { name: "Kernel trick & RKHS", status: "gap" },
          { name: "Gaussian processes", status: "gap" },
        ],
      },
      {
        id: "C3",
        name: "Tree-based methods",
        intro:
          "Tree-based methods split the feature space into axis-aligned regions and predict a constant in each one. A single tree is interpretable but brittle; the breakthrough is combining many of them, and gradient-boosted trees are still the quiet winner of a large share of real-world tabular competitions and production systems. If you only learn one family of models well, this is a strong candidate.\n\nYou will grow a decision tree by recursive partitioning, choose splits with Gini, entropy, or MSE, and tame overfitting with pruning and cost-complexity control. Then you will move to ensembles: bagging and random forests to cut variance, feature importance done honestly with permutation, AdaBoost and its exponential-loss view, and gradient boosting framed as functional gradient descent. The track ends with XGBoost and LightGBM, where second-order objectives and histogram splits make boosting both fast and accurate.\n\nThese models handle mixed feature types, missing values, and nonlinear interactions with almost no preprocessing, which is why they remain the default for structured data and a recurring baseline for forecasting and ranking tasks downstream.",
        prerequisites: [
          "C1 Linear and GLMs: the bias-variance tradeoff and a working modeling mindset.",
          "A2 Probability and information theory: entropy and information gain.",
          "A3 Optimization: gradient descent (boosting is gradient descent in function space).",
        ],
        topics: [
          { name: "Decision trees", status: "gap" },
          { name: "Random forests", status: "gap" },
          {
            name: "Gradient boosting (XGBoost, LightGBM, CatBoost)",
            status: "gap",
          },
        ],
      },
      {
        id: "C4",
        name: "Instance & probabilistic",
        intro:
          "Instance-based and probabilistic classifiers are two of the oldest and most transparent ways to label data. Instance-based methods, like k-nearest neighbors, make no model at all: they just remember the training set and let nearby points vote. Probabilistic classifiers, like naive Bayes and discriminant analysis, instead model how each class generates its features and then invert that with Bayes' rule. Both are excellent baselines and surprisingly hard to beat on the right problem.\n\nYou will implement k-NN for classification and regression, choose k by cross-validation, and confront the curse of dimensionality that erodes distance-based methods as features pile up. Then you will build naive Bayes from the conditional-independence assumption, derive linear and quadratic discriminant analysis by modeling classes as Gaussians, and meet Fisher's LDA as a supervised projection that maximizes class separation, the discriminative twin of PCA.\n\nThe Bayes-rule reasoning here is foundational for probabilistic graphical models later, the distance intuitions feed directly into nearest-neighbor search and vector databases, and LDA-style projections recur throughout dimensionality reduction.",
        prerequisites: [
          "A2 Probability: Bayes' rule, Gaussian and common distributions.",
          "A1 Linear algebra: norms, distances, and eigenvalues (for Fisher's LDA).",
          "C1 Linear and GLMs for the classification framing helps but is not strictly required.",
        ],
        topics: [
          { name: "k-NN", status: "gap" },
          { name: "Naive Bayes", status: "gap" },
          { name: "LDA / QDA", status: "gap" },
        ],
      },
      {
        id: "C5",
        name: "Unsupervised learning",
        intro:
          "Unsupervised learning looks for structure when there are no labels to lean on: groups of similar points, or a low-dimensional summary of high-dimensional data. It is how you explore a fresh dataset, compress it, and build intuition before any predictive model exists, and it is often the first thing you reach for when you do not yet know what question to ask.\n\nYou will cluster with k-means (seen as alternating minimization), improve it with k-means++ and principled choices of k, and handle non-Euclidean or noisy data with k-medoids, DBSCAN, and HDBSCAN. You will read dendrograms from hierarchical clustering, fit Gaussian mixture models with the EM algorithm (soft k-means with covariances), and visualize high-dimensional structure with t-SNE and UMAP while learning where they mislead.\n\nThese tools power exploratory analysis, customer and image segmentation, and feature compression across the field. The EM algorithm reappears throughout latent-variable modeling, and the clustering and quantization ideas here are exactly what large-scale vector search builds on later.",
        prerequisites: [
          "A1 Linear algebra: PCA, low-rank structure, eigenvalues.",
          "A2 Probability: Gaussians and maximum likelihood (for GMMs and EM).",
          "Working Python with numpy; scikit-learn familiarity helps.",
        ],
        topics: [
          { name: "k-means, k-medoids", status: "gap" },
          { name: "DBSCAN, HDBSCAN", status: "gap" },
          { name: "Hierarchical clustering", status: "gap" },
          { name: "GMM + EM", status: "gap" },
          { name: "PCA (linear)", status: "gap" },
          { name: "t-SNE, UMAP", status: "gap" },
        ],
      },
      {
        id: "C6",
        name: "Anomaly detection",
        intro:
          "Anomaly detection is the search for the rare and the wrong: fraud, defects, intrusions, sensor faults, the handful of points that do not look like the rest. The defining difficulty is that anomalies are scarce and often unlabeled, so you usually model what normal looks like and flag whatever falls outside it, rather than training a standard classifier.\n\nYou will begin with statistical baselines (IQR, ESD, and CUSUM thresholds) that are simple and easy to defend, then build Isolation Forest, which isolates outliers in few random splits with no distance metric required. From there you will carve out a region of normal data with a one-class SVM and use its boundary as a novelty detector, and finally train an autoencoder on normal examples and flag points whose reconstruction error runs high.\n\nThese techniques run in fraud and security pipelines, manufacturing quality control, and monitoring systems, and the reconstruction-error idea connects directly to deep autoencoders and to drift detection in production ML.",
        prerequisites: [
          "A2 Probability: distributions and concentration inequalities.",
          "C3 Tree-based methods (Isolation Forest builds on bagging) and C2 kernel methods (one-class SVM).",
          "A1 Linear algebra: PCA and low-rank reconstruction (for autoencoder-based detection).",
        ],
        topics: [
          { name: "Isolation Forest", status: "gap" },
          { name: "One-class SVM", status: "gap" },
          { name: "Autoencoder-based AD", status: "gap" },
        ],
      },
      {
        id: "C7",
        name: "Ensembles",
        intro:
          "Ensembles combine many models into one that is more accurate and more stable than any single member. The insight is statistical: averaging diverse models cancels their independent errors, so a committee of mediocre learners can outperform a finely tuned single model. This is why nearly every winning solution on tabular data is an ensemble of some kind.\n\nYou will work out why ensembles help (bagging shrinks variance, boosting shrinks bias) and see correlated errors as the failure mode that caps the gains. Then you will train a meta-learner on out-of-fold predictions with stacking and blending, combine models cheaply with snapshot ensembles, voting, and rank averaging, and survey AutoML platforms that automate the search over pipelines and hyperparameters.\n\nThese patterns are the standard last mile of competitive and production modeling, and the diversity-and-aggregation principle here reappears in deep ensembles for uncertainty and in multi-model routing strategies for LLM systems.",
        prerequisites: [
          "C1 Linear and GLMs: the bias-variance decomposition.",
          "C3 Tree-based methods: bagging, random forests, and boosting.",
          "A3 Optimization: Bayesian optimization (for the AutoML lesson).",
        ],
        topics: [
          { name: "Bagging, boosting, stacking", status: "gap" },
          { name: "AutoML platforms", status: "gap", hot: true },
        ],
      },
      {
        id: "C8",
        name: "Recommendation systems",
        intro:
          "Recommendation systems decide what to show next: products, movies, songs, posts. The core problem is filling in a vast, mostly empty matrix of user-item interactions and ranking what a person is most likely to want. It is one of the highest-leverage applications of machine learning in industry, quietly driving a large fraction of engagement and revenue on the platforms you use daily.\n\nYou will start with neighborhood-based collaborative filtering, then factor the rating matrix into low-rank user and item embeddings with SVD and ALS, extend it to implicit feedback (clicks and views) with weighted least squares, and get parts-based representations from non-negative matrix factorization. From there you will move to neural recommenders: two-tower and neural collaborative filtering models that embed users and items and score them with a dot product, and sequential models like SASRec and BERT4Rec that read user history as a sequence.\n\nThe matrix-factorization and embedding ideas here are the same retrieval substrate behind modern dense retrieval and RAG, and the two-tower architecture is now standard far beyond recommendations.",
        prerequisites: [
          "A1 Linear algebra: the SVD, low-rank factorization, PCA.",
          "A3 Optimization: gradient descent and alternating minimization (ALS).",
          "Working Python with numpy; D Deep learning basics help for the neural lessons.",
        ],
        topics: [
          { name: "Collaborative filtering", status: "gap" },
          { name: "Matrix factorization (SVD, ALS, NMF)", status: "gap" },
          { name: "Two-tower / neural CF", status: "gap", hot: true },
          {
            name: "Sequential rec (SASRec, BERT4Rec)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "C9",
        name: "Approximate nearest neighbor",
        intro:
          "Approximate nearest neighbor search is how you find the closest vectors to a query when there are millions or billions of them and exact comparison is hopeless. By trading a sliver of accuracy for orders-of-magnitude speed, ANN methods make similarity search practical at scale, and they have quietly become critical infrastructure behind retrieval, recommendation, and every RAG pipeline.\n\nYou will state the ANN problem and the recall@k metric, then build the major index families: locality-sensitive hashing (with MinHash for Jaccard and SimHash for cosine), inverted-file partitioning with product quantization for billion-scale compressed search, and HNSW small-world graphs that support near-logarithmic greedy traversal. You will close by comparing FAISS, pgvector, and managed vector databases along recall, throughput, and operational cost.\n\nThis is the engine room of modern semantic search: embeddings from any model become useful only once you can query them fast, which is why these structures sit underneath LLM retrieval, deduplication, and large-scale recommendation alike.",
        prerequisites: [
          "C4 Instance and probabilistic methods: nearest neighbors and the curse of dimensionality.",
          "C5 Unsupervised learning: k-means (used by IVF partitioning).",
          "A1 Linear algebra: norms, inner products, and cosine similarity.",
        ],
        topics: [
          { name: "LSH, MinHash", status: "gap" },
          { name: "HNSW, IVF, Product Quantization", status: "gap" },
          {
            name: "Vector DBs (FAISS, Pinecone, pgvector)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "C10",
        name: "Evaluation & selection",
        intro:
          "Evaluation and model selection are how you find out whether a model is actually good or just lucky, and how you choose among competing models without fooling yourself. This is the most underrated discipline in machine learning: a wrong metric or a leaky validation split can make a useless model look brilliant right up until it meets real data.\n\nYou will define classification metrics (precision, recall, F1, ROC and AUC) and regression metrics (MSE, MAE, R-squared, MAPE, quantile losses), learning when each one misleads. You will diagnose whether predicted probabilities are trustworthy with reliability diagrams and Brier scores, recalibrate with Platt scaling and isotonic regression, choose the right cross-validation scheme (stratified, group, or time-series) for the test distribution you actually face, and tune hyperparameters with grid, random, and Bayesian search while watching the bias and variance of the search itself.\n\nEvery other subsection in this pillar, and every pillar after it, ultimately reports a number from here. Getting evaluation right is what separates a credible result from a misleading one.",
        prerequisites: [
          "C1 Linear and GLMs: logistic regression and the bias-variance tradeoff.",
          "A2 Probability and B3 resampling and validation (cross-validation, the bootstrap).",
          "A3 Optimization: Bayesian optimization (for hyperparameter search).",
        ],
        topics: [
          {
            name: "Metrics (precision/recall, ROC/AUC, calibration)",
            status: "gap",
          },
          { name: "Probability calibration (Platt, isotonic)", status: "gap" },
          { name: "HPO search (grid, random, BO)", status: "gap" },
        ],
      },
    ],
  },
  {
    letter: "D",
    slug: "D-deep-learning",
    name: "Deep Learning: Core & Tracks",
    shortName: "Deep Learning",
    tagline: "MLPs, CV, sequence, generative, SSL, GNN, training systems",
    color: "#7aa2f7",
    intro:
      "Deep learning is what happens when you stack differentiable building blocks and let optimization do the feature engineering for you. Instead of hand-crafting what matters in the data, you define an architecture, a loss, and a gradient, and the representations emerge from training. This pillar builds the core mechanics first, then branches into the major application tracks.\n\nYou will start with the core building blocks (layers, activations, backpropagation, normalization, and regularization), then work through computer vision (CNNs from LeNet to ConvNeXt, detection, and neural rendering), sequence modeling (recurrent networks, attention, and state space models like Mamba), and generative modeling (autoencoders, GANs, and the diffusion models behind modern image generation). The track widens further into self-supervised learning and graph neural networks, and closes with the training systems (mixed precision, distributed training, and compilation) that make billion-parameter models trainable at all.\n\nThis is the hinge of the whole tree: NLP, modern RL, and most of AI engineering downstream assume you are fluent here.",
    prerequisites: [
      "A1 Linear algebra, A2 probability, and A3 optimization (backprop is just the chain rule plus gradient descent).",
      "C Classical ML for the modeling mindset (loss functions, over/underfitting, evaluation).",
      "Python with numpy; PyTorch familiarity helps for the systems lessons.",
    ],
    subs: [
      {
        id: "D1",
        name: "Core building blocks",
        intro:
          "This is where deep learning starts: the small set of differentiable parts that every architecture in the rest of the pillar reuses. A network is just affine maps interleaved with nonlinearities, trained by pushing gradients backward through the computation that produced the loss. Get these mechanics right and everything downstream is variations on a theme; get them wrong and training quietly stalls.\n\nBy the end you can trace a forward pass through an MLP, derive backpropagation as reverse-mode differentiation, and even hand-roll a tiny autodiff engine that records its own graph. You will know why Cybenko's theorem promises expressiveness, how to pick activations and avoid dead ReLUs, how Xavier and He initialization keep variance from collapsing, where BatchNorm, LayerNorm, and RMSNorm belong, and how dropout, weight decay, and the Adam family of optimizers actually shape training.\n\nThese building blocks recur in every CNN, Transformer, and diffusion model later in the pillar, so the time spent here pays off in every track that follows.",
        prerequisites: [
          "A1 Linear algebra and matrix calculus",
          "A2 Probability",
          "A3 Optimization (SGD, gradient descent)",
          "Python with numpy",
        ],
        topics: [
          { name: "Perceptron → MLPs", status: "covered" },
          { name: "Backpropagation, autodiff", status: "covered" },
          { name: "Universal approximation", status: "covered" },
          { name: "Activations (ReLU, GELU, Swish)", status: "covered" },
          { name: "Initialization (Xavier, He)", status: "covered" },
          { name: "Normalization (BN, LN, RMSNorm)", status: "covered" },
          { name: "Regularization (dropout, weight decay)", status: "covered" },
          { name: "Optimizers (SGD, Adam, AdamW)", status: "covered" },
        ],
      },
      {
        id: "D2",
        name: "Computer Vision",
        intro:
          "Computer vision is the track that taught deep learning to see, and it remains the field where architectural ideas tend to appear first. The core problem is turning raw pixels into structured understanding: a label, a set of boxes, a per-pixel mask, or a full 3D scene. Convolution provides the inductive bias that makes this tractable, sharing weights across space so a network learns local patterns it can reuse everywhere.\n\nYou will build convolution and pooling from sliding inner products, then trace the architectural lineage from LeNet through ResNet's skip connections to ConvNeXt, and see how Vision Transformers reframe an image as a sequence of patches. From there you move into detection (R-CNN, YOLO, DETR), segmentation (U-Net, Mask R-CNN, Segment Anything), label-free pretraining with DINO and MAE, and neural rendering with NeRF and Gaussian Splatting.\n\nThese methods power everything from medical imaging to autonomous driving to the image encoders inside multimodal models, so the track connects directly to self-supervised learning and generative modeling later on.",
        prerequisites: [
          "D1 Core building blocks (MLPs, backprop)",
          "A1 Linear algebra",
          "Python with numpy",
          "D3 Transformer architecture (for Vision Transformers)",
        ],
        topics: [
          { name: "Convolution & pooling intuition", status: "partial" },
          {
            name: "CNN architectures (LeNet → ResNet → ConvNeXt)",
            status: "gap",
          },
          { name: "Object detection (R-CNN, YOLO, DETR)", status: "gap" },
          { name: "Segmentation (U-Net, Mask R-CNN)", status: "gap" },
          { name: "Segment Anything (SAM, SAM 2)", status: "gap", hot: true },
          { name: "Vision Transformers (ViT, Swin, DeiT)", status: "gap" },
          {
            name: "Self-supervised vision (DINO, MAE)",
            status: "gap",
            hot: true,
          },
          {
            name: "3D / neural rendering (NeRF, Gaussian Splatting)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "D3",
        name: "Sequence modeling",
        intro:
          "Sequence modeling is about data where order carries meaning: language, time series, audio, code. The central difficulty is reach, letting a model relate a token to context that may sit hundreds of steps away without losing or exploding the signal in between. This track traces how the field solved that problem and arrived at the architecture behind every modern language model.\n\nYou will start with word embeddings, then build recurrent networks and watch their gradients vanish over long ranges, fix that with LSTM and GRU gates, and add attention to encoder-decoder translation. From there self-attention and the full Transformer come into focus, along with positional encodings (sinusoidal, ALiBi, RoPE) and the newer linear-time alternatives: state space models like Mamba, sub-quadratic attention including FlashAttention, and hybrid designs such as Jamba and Griffin.\n\nThe Transformer you assemble here is the same backbone used across NLP, modern reinforcement learning, and nearly all of AI engineering, which makes this one of the most load-bearing disciplines in the tree.",
        prerequisites: [
          "D1 Core building blocks (MLPs, backprop, normalization)",
          "A1 Linear algebra",
          "A2 Probability",
          "Python with numpy",
        ],
        topics: [
          { name: "Word embeddings (word2vec, GloVe)", status: "partial" },
          { name: "RNN, LSTM, GRU", status: "gap" },
          { name: "Seq2seq + attention (Bahdanau, Luong)", status: "gap" },
          { name: "Transformer (encoder/decoder)", status: "covered" },
          {
            name: "State Space Models: S4, Mamba, Mamba-2",
            status: "gap",
            hot: true,
          },
          {
            name: "Linear / sub-quadratic attention",
            status: "gap",
            hot: true,
          },
          { name: "RWKV, Hyena, RetNet", status: "gap", hot: true },
          { name: "Hybrid arch (Jamba, Griffin)", status: "gap", hot: true },
        ],
      },
      {
        id: "D4",
        name: "Generative modeling",
        intro:
          "Generative modeling asks a model not to classify data but to produce it: to learn the underlying distribution well enough to sample new images, audio, or molecules that look like they belong. This is the machinery behind text-to-image systems and a deep probabilistic subject in its own right, where the central tension is always between sample quality, likelihood, and how stably the thing trains.\n\nYou will build autoencoders and their denoising variant, derive the VAE's evidence lower bound and reparameterization trick, work through GANs and their mode-collapse pitfalls, and use normalizing flows for exact likelihoods. The track then reaches diffusion: the forward noising process, the reverse denoising objective behind DDPM, latent diffusion as used in Stable Diffusion, and the newer flow-matching and consistency models that distill sampling down to a few steps.\n\nThese ideas drive image and video generation, drug discovery, and data augmentation, and they connect back to the Bayesian deep learning that shares the VAE's variational core.",
        prerequisites: [
          "D1 Core building blocks",
          "A2 Probability (KL divergence, change of variables)",
          "C Classical ML (loss functions, evaluation)",
          "Python with numpy",
        ],
        topics: [
          { name: "Autoencoders", status: "gap" },
          {
            name: "Variational Autoencoders (VAE, β-VAE, VQ-VAE)",
            status: "gap",
          },
          { name: "GANs (DCGAN, StyleGAN, BigGAN)", status: "gap" },
          { name: "Normalizing flows", status: "gap" },
          {
            name: "Diffusion models (DDPM, DDIM, EDM)",
            status: "gap",
            hot: true,
          },
          {
            name: "Latent diffusion (Stable Diffusion)",
            status: "gap",
            hot: true,
          },
          { name: "Flow matching, rectified flow", status: "gap", hot: true },
          { name: "Consistency models", status: "gap", hot: true },
        ],
      },
      {
        id: "D5",
        name: "Self-supervised learning",
        intro:
          "Self-supervised learning is the answer to a practical bottleneck: labels are expensive, but raw data is nearly free. The idea is to invent a pretext task the data labels itself, so a network can learn rich, general-purpose representations from unlabeled images or text and then transfer them to downstream tasks with very little supervision.\n\nYou will pretrain representations contrastively by pulling augmented views together with the InfoNCE loss (SimCLR, MoCo), extend that across modalities to align images and captions in CLIP, and see how non-contrastive methods like BYOL and DINO drop negatives entirely through predictors and student-teacher distillation. On the masked-prediction side you will work through BERT-style masked language modeling and its image analogue, MAE-style masked image modeling.\n\nThis paradigm is why foundation models exist at all: nearly every large pretrained encoder, and the embeddings that power retrieval and multimodal systems, comes out of a self-supervised objective like the ones here.",
        prerequisites: [
          "D1 Core building blocks",
          "D3 Transformer architecture",
          "D2 Vision Transformers (for masked image modeling)",
          "C Classical ML mindset",
        ],
        topics: [
          { name: "Contrastive (SimCLR, MoCo, CLIP)", status: "gap" },
          { name: "Non-contrastive (BYOL, DINO)", status: "gap" },
          { name: "Masked Language Modeling", status: "partial" },
          { name: "Masked image modeling (MAE, BEiT)", status: "gap" },
        ],
      },
      {
        id: "D6",
        name: "Graph Neural Networks",
        intro:
          "Graph neural networks handle data that is naturally relational: molecules, social networks, knowledge graphs, recommendation systems, anything best described by nodes and the edges between them. Standard CNNs and Transformers assume a grid or a sequence, but a graph has no fixed ordering or neighborhood size, so this track builds architectures that respect that irregular structure directly.\n\nYou will represent graphs through adjacency and feature matrices, frame learning as the message, aggregate, and update steps of message passing, and then instantiate that framework as concrete models: GCN's Laplacian smoothing, GraphSAGE's neighborhood sampling, and GAT's attention weights. The track extends to graph Transformers that swap local passing for global attention, and to equivariant and geometric networks whose outputs transform predictably under symmetries, the kind used for 3D molecules.\n\nThese methods underpin drug discovery, materials science, traffic and logistics modeling, and large-scale recommendation, and they share the attention machinery you met in sequence modeling.",
        prerequisites: [
          "D1 Core building blocks",
          "A5 Graph algorithms (adjacency, traversal)",
          "D3 Transformer architecture (for graph Transformers)",
          "A1 Linear algebra",
        ],
        topics: [
          { name: "Message passing framework", status: "gap" },
          { name: "GCN, GraphSAGE, GAT", status: "gap" },
          { name: "Graph Transformers", status: "gap", hot: true },
          { name: "Equivariant / geometric DL", status: "gap", hot: true },
        ],
      },
      {
        id: "D7",
        name: "Training systems",
        intro:
          "Training systems is the engineering that turns a working architecture into a model you can train at billion-parameter scale without running out of memory or waiting weeks. Once models outgrow a single GPU, the bottleneck shifts from math to systems: numeric precision, memory budgets, and how computation is split across many devices and kept in sync.\n\nYou will learn mixed-precision training with fp16 or bf16 and loss scaling, trade compute for memory with gradient checkpointing, and shard work across devices through data parallelism (DDP, FSDP, ZeRO) and model parallelism (pipeline and tensor splits like GPipe and Megatron). The track also covers compilation through torch.compile, XLA, and Triton, the IO-aware tiling behind FlashAttention, and the cluster infrastructure (storage, schedulers, NCCL collectives, observability) that holds a large training run together.\n\nThis is mostly conceptual and infrastructure-flavored, but it is what separates research code from systems that actually train modern models, and it leads naturally into the MLOps and serving concerns of later pillars.",
        prerequisites: [
          "D1 Core building blocks (backprop)",
          "D3 Self-attention (for FlashAttention)",
          "A4 Numerical methods (floating-point, mixed precision)",
          "PyTorch familiarity",
        ],
        topics: [
          {
            name: "Mixed precision (FP16, BF16, FP8)",
            status: "gap",
            hot: true,
          },
          {
            name: "Distributed training (DDP, FSDP, ZeRO)",
            status: "gap",
            hot: true,
          },
          { name: "Pipeline & tensor parallelism", status: "gap", hot: true },
          { name: "Gradient checkpointing", status: "gap" },
          {
            name: "Compilation (torch.compile, XLA, Triton)",
            status: "gap",
            hot: true,
          },
          { name: "FlashAttention v1/v2/v3", status: "gap", hot: true },
        ],
      },
    ],
  },
  {
    letter: "E",
    slug: "E-nlp-llms",
    name: "NLP & Language Models",
    shortName: "NLP & LLMs",
    tagline:
      "Tokenization, LLMs, alignment, agents: the backbone of AI ML Theory",
    color: "#bb9af7",
    intro:
      "This pillar traces the path from counting words to models that write code, hold conversations, and reason through multi-step problems. It is the densest frontier track in the tree, and the one moving fastest, so the emphasis is on the durable ideas underneath the headline models.\n\nYou will begin with classical NLP (tokenization, n-gram language models, and parsing), then pre-Transformer neural NLP (word embeddings and recurrent encoders), before reaching the Transformer and modern language models (attention, positional encoding, and mixture-of-experts). From there the pillar covers training LLMs (scaling laws, pretraining, alignment, and parameter-efficient fine-tuning), inference and serving (KV caching, batching, and engines like vLLM), and LLM agents and retrieval (RAG, tool use, and test-time compute). It closes with multimodal models and with interpretability and alignment science, the study of what these systems are actually doing and how to keep them steerable.\n\nIf pillar D taught you how to train a network, this pillar is where that skill meets the models reshaping the field.",
    prerequisites: [
      "D Deep learning, especially D3 sequence modeling and D7 training systems.",
      "A2 Probability and information theory (cross-entropy, KL divergence).",
      "Comfortable Python; access to an LLM API or a small local model for the applied lessons.",
    ],
    subs: [
      {
        id: "E1",
        name: "Classical NLP",
        intro:
          "Classical NLP is where language modeling began: treat text as a sequence of tokens and count. Before any neural network, the discipline solved real problems (predicting the next word, tagging parts of speech, finding named entities, retrieving relevant documents) with probability tables, dynamic programming, and clever weighting schemes. The ideas here are not museum pieces; they are the foundations every modern system quietly reuses.\n\nYou will build n-gram language models from the Markov approximation and counting, fix their zero-probability holes with Laplace and Kneser-Ney smoothing, and measure quality with perplexity. You will train byte-pair encoding tokenizers and contrast WordPiece and SentencePiece, decode part-of-speech and entity tags with HMMs and Viterbi, sharpen them into discriminative CRFs, and rank documents with TF-IDF and BM25.\n\nThis matters because tokenization still feeds every LLM, BM25 still anchors hybrid retrieval in production RAG, and perplexity is the yardstick you carry through the rest of the pillar.",
        prerequisites: [
          "A2 Probability: distributions, conditional probability, and Bayes' rule.",
          "A2 Information theory: entropy and cross-entropy (perplexity builds on these).",
          "Comfortable Python with numpy for counting and small matrix operations.",
        ],
        topics: [
          {
            name: "Tokenization (BPE, WordPiece, SentencePiece)",
            status: "covered",
          },
          { name: "n-gram LM, smoothing", status: "gap" },
          { name: "POS tagging, NER (HMM/CRF era)", status: "gap" },
          { name: "Parsing (dependency, constituency)", status: "gap" },
          { name: "Topic models (LDA, NMF)", status: "gap" },
          { name: "Information retrieval (TF-IDF, BM25)", status: "gap" },
        ],
      },
      {
        id: "E2",
        name: "Pre-Transformer neural NLP",
        intro:
          "This discipline covers the neural NLP that came after counting but before the Transformer: the era when models learned to represent words as dense vectors and to read sequences with recurrence. It solves the core weakness of n-grams, the inability to generalize across similar words, by placing meaning in a continuous space where 'king' and 'queen' sit close together.\n\nYou will train word2vec with skip-gram negative sampling, derive GloVe from co-occurrence ratios, and add fastText's subword composition for rare and out-of-vocabulary words. From static embeddings you move to recurrent language models, deriving backpropagation through time and the vanishing-gradient problem, then defeat it with LSTM and GRU gates. You finish with ELMo's contextual embeddings and a seq2seq encoder-decoder equipped with Bahdanau attention.\n\nThis is the bridge to everything that follows: attention is introduced here in its original additive form, and the encoder-decoder shape you build is the direct ancestor of the Transformer in E3.",
        prerequisites: [
          "E1 Classical NLP: tokenization and n-gram language models.",
          "D1 Deep learning core: backpropagation and autodiff (BPTT is the chain rule unrolled in time).",
          "A1 Linear algebra: vectors, dot products, and matrix multiplication.",
        ],
        topics: [
          {
            name: "Word embeddings (word2vec, GloVe, fastText)",
            status: "partial",
          },
          { name: "ELMo, contextual embeddings", status: "gap" },
          { name: "Seq2seq + attention", status: "gap" },
        ],
      },
      {
        id: "E3",
        name: "Transformer LMs",
        intro:
          "Transformer language models are the architecture behind essentially every modern LLM, and this discipline builds one from the attention operation up. It replaces recurrence with a mechanism that lets every token attend to every other token in parallel, which is what made training at today's scale possible.\n\nYou will derive scaled dot-product attention (including why the 1/sqrt(d_k) factor is there), stack heads into multi-head attention, and assemble a full transformer block with residual connections and layer norm, tracing tensor shapes through a forward pass. You will add positional information from sinusoidal encodings up to RoPE and ALiBi, then specialize the block into the three families: decoder-only GPT models with causal masking, encoder-only BERT with bidirectional masked pretraining, and encoder-decoder T5 and BART with cross-attention. The discipline closes with the efficiency tricks production models rely on: grouped-query and multi-query attention, and mixture-of-experts routing.\n\nThis is the load-bearing center of the pillar: training, inference, agents, and multimodal models all assume you understand the block built here.",
        prerequisites: [
          "E2 Pre-Transformer NLP: word embeddings and seq2seq with attention.",
          "A1 Linear algebra: matrix multiplication, projections, and softmax.",
          "D1 Deep learning core: normalization, residual connections, and optimizers.",
        ],
        topics: [
          { name: "Encoder-only (BERT, RoBERTa)", status: "gap" },
          { name: "Encoder-decoder (T5, BART)", status: "gap" },
          { name: "Decoder-only / GPT family", status: "covered" },
          { name: "Positional encodings (RoPE, ALiBi)", status: "covered" },
          {
            name: "Mixture of Experts (Mixtral, DeepSeek-V3)",
            status: "gap",
            hot: true,
          },
          { name: "Grouped Query Attention, MQA", status: "gap", hot: true },
        ],
      },
      {
        id: "E4",
        name: "Training LLMs",
        intro:
          "Training LLMs is the pipeline that turns raw web text into a model that follows instructions and respects human preferences. It answers the questions that decide whether a base model becomes something useful: what data to train on, how big to make it for a given compute budget, and how to align its behavior after pretraining.\n\nYou will study data curation (quality filtering, deduplication, domain mixing), then the Kaplan and Chinchilla scaling laws that govern how to spend compute between parameters and tokens. From there you move through alignment: supervised fine-tuning, Bradley-Terry reward modeling, the four-model RLHF loop with PPO's clipped objective and KL penalty, and the offline preference methods (DPO, IPO, KTO, ORPO) that drop the reward model. You will also cover GRPO behind reasoning models, Constitutional AI and RLAIF, and parameter-efficient fine-tuning with LoRA, QLoRA, and DoRA.\n\nThis is where the abstract Transformer becomes a deployable assistant, and the alignment ideas here reappear directly in pillar H's RL and pillar J's applied fine-tuning.",
        prerequisites: [
          "E3 Transformer LMs: decoder-only models and causal language modeling.",
          "A2 Probability and information theory: cross-entropy and KL divergence.",
          "A3 Optimization and D1 deep learning optimizers (PPO and DPO are gradient methods); H1 RL foundations help for RLHF.",
        ],
        topics: [
          { name: "Pretraining, data curation", status: "covered" },
          {
            name: "Scaling laws (Kaplan, Chinchilla)",
            status: "gap",
            hot: true,
          },
          { name: "Supervised fine-tuning (SFT)", status: "covered" },
          { name: "RLHF (PPO end-to-end)", status: "covered" },
          { name: "DPO, IPO, KTO, ORPO", status: "covered" },
          { name: "GRPO", status: "covered" },
          { name: "Constitutional AI / RLAIF", status: "covered" },
          {
            name: "Parameter-efficient FT (LoRA, QLoRA, DoRA)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "E5",
        name: "Inference & serving",
        intro:
          "Inference and serving is the engineering of getting tokens out of a trained model quickly and cheaply, which is where most of an LLM's real-world cost actually lives. A model that is accurate but too slow or too expensive to run never reaches users, so this discipline treats latency, throughput, and memory as first-class concerns.\n\nYou will implement the decoding strategies that shape every output (greedy, beam, top-k, nucleus, temperature), then the KV cache that cuts per-token cost from quadratic to linear. From there you cover speculative decoding with a draft model (and the proof that it preserves the target distribution), post-training quantization with GPTQ, AWQ, and GGUF, and the memory management behind PagedAttention and continuous batching. The discipline closes with how production engines like vLLM, TGI, and SGLang combine these techniques.\n\nThis matters the moment you move from a notebook to a service: the same techniques underlie LLM serving in pillar I and the cost-and-latency engineering of pillar J.",
        prerequisites: [
          "E3 Transformer LMs: decoder-only models and the attention KV computation.",
          "A4 Numerical methods: floating point and precision (quantization rests on this).",
          "Comfortable Python; familiarity with GPU memory and batching helps for the systems lessons.",
        ],
        topics: [
          { name: "Decoding (greedy, beam, top-k, top-p)", status: "covered" },
          { name: "KV cache", status: "covered" },
          { name: "Speculative decoding", status: "covered", hot: true },
          { name: "Quantization (GPTQ, AWQ, GGUF)", status: "gap", hot: true },
          {
            name: "Inference engines (vLLM, TGI, SGLang)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "E6",
        name: "LLM agents & retrieval",
        intro:
          "LLM agents and retrieval is where a language model stops being a closed box and starts using external knowledge and tools. It solves the model's two biggest limitations, a fixed knowledge cutoff and an inability to act, by grounding generation in retrieved documents and letting the model call functions to do things in the world.\n\nYou will build a retrieval-augmented generation pipeline (chunk, embed, index, retrieve, generate), train dense bi-encoders with contrastive loss and search them with FAISS, and add advanced techniques like HyDE, cross-encoder rerankers, and GraphRAG. On the agent side you will implement structured tool calling, few-shot chain-of-thought with self-consistency voting, and the ReAct and Reflexion loops that interleave reasoning with actions. The discipline finishes with test-time compute scaling behind o1 and DeepSeek-R1, and multi-agent orchestration patterns.\n\nThis is the conceptual backbone of applied AI engineering: the RAG, tool use, and agent patterns here are exactly what pillar J builds into production systems.",
        prerequisites: [
          "E3 Transformer LMs: decoder-only generation and prompting.",
          "E1 Information retrieval (TF-IDF, BM25) and C9 approximate nearest neighbor search.",
          "Comfortable Python and access to an LLM API for the applied agent lessons.",
        ],
        topics: [
          { name: "RAG fundamentals", status: "gap" },
          { name: "Advanced RAG (HyDE, rerankers, graph RAG)", status: "gap" },
          { name: "Tool use, function calling", status: "gap" },
          { name: "ReAct, Reflexion agents", status: "gap" },
          { name: "Chain-of-Thought, self-consistency", status: "gap" },
          {
            name: "Test-time compute (o1, DeepSeek-R1)",
            status: "gap",
            hot: true,
          },
          { name: "Multi-agent systems (AutoGen, CrewAI)", status: "gap" },
        ],
      },
      {
        id: "E7",
        name: "Multimodal",
        intro:
          "Multimodal models break language out of text alone, joining it with images, audio, and video so a single system can see, hear, and generate across modalities. The central trick is alignment: mapping different kinds of data into a shared representation where a caption and its picture, or a question and the image it asks about, can be compared and reasoned over together.\n\nYou will train CLIP's joint image-text encoders with a contrastive InfoNCE loss and watch zero-shot classification fall out of cosine similarity. From there you bridge a frozen vision encoder to an LLM with a projection layer (LLaVA) or a Q-Former (BLIP-2), fine-tune large multimodal models, and handle audio with Whisper and Wav2Vec. The discipline closes on generation: text-to-image diffusion with classifier-free guidance (DALL-E, Stable Diffusion) and text-to-video with spacetime diffusion transformers (Sora, Veo).\n\nThis connects the pillar back to vision and generative modeling in pillar D, and it is the direction frontier assistants are moving as they become natively multimodal.",
        prerequisites: [
          "E3 Transformer LMs: encoder-only and decoder-only models.",
          "D5 Self-supervised learning (contrastive methods) and D4 generative modeling (diffusion).",
          "E4 Supervised fine-tuning for the multimodal fine-tuning lessons.",
        ],
        topics: [
          { name: "Vision-Language (CLIP, BLIP-2)", status: "gap" },
          { name: "LMMs (LLaVA, GPT-4V)", status: "gap" },
          { name: "Audio LLMs (Whisper, Wav2Vec)", status: "gap" },
          { name: "Text-to-image (DALL-E, SD, Midjourney)", status: "gap" },
          { name: "Text-to-video (Sora, Veo)", status: "gap", hot: true },
        ],
      },
      {
        id: "E8",
        name: "Interpretability & alignment science",
        intro:
          "Interpretability and alignment science asks what these models are actually computing inside, and how to keep systems steerable as they grow more capable. Where the rest of the pillar trains and serves LLMs, this discipline opens them up: it treats a trained network as an object of study, looking for the structures and circuits that produce its behavior.\n\nYou will train probing classifiers on frozen activations, then move to mechanistic interpretability, reproducing the indirect-object-identification circuit and the induction heads that implement in-context learning. You will model superposition and polysemanticity, decompose the residual stream into monosemantic features with sparse autoencoders, and intervene on behavior through activation patching and representation steering. The discipline closes with scalable oversight (debate, amplification) and weak-to-strong generalization, the empirical proxy for aligning a model smarter than its supervisor.\n\nThis matters because capability without understanding is fragile: the techniques here feed directly into safety evaluations in pillar I and AI governance in pillar J.",
        prerequisites: [
          "E3 Transformer LMs: the residual stream, attention heads, and MLP blocks.",
          "E4 Alignment basics (RLHF, RLAIF) for the oversight lessons.",
          "A1 Linear algebra (directions and projections) and comfortable Python with numpy.",
        ],
        topics: [
          { name: "Probing & linear classifiers", status: "partial" },
          {
            name: "Mechanistic interpretability (circuits)",
            status: "covered",
            hot: true,
          },
          { name: "Sparse Autoencoders (SAEs)", status: "gap", hot: true },
          { name: "Activation patching", status: "partial" },
          { name: "Representation engineering", status: "gap", hot: true },
          {
            name: "Scalable oversight, weak-to-strong",
            status: "gap",
            hot: true,
          },
        ],
      },
    ],
  },
  {
    letter: "F",
    slug: "F-graphical-models",
    name: "Probabilistic Graphical Models",
    shortName: "PGMs",
    tagline: "Bayes nets, MRFs, HMM, VI, MCMC, latent variable models",
    color: "#7dcfff",
    intro:
      "Probabilistic graphical models are the grammar of probability over many variables. They let you draw a joint distribution as a picture of conditional independencies, read off what depends on what, and then compute with it efficiently. Where pillar B reasons about a few quantities, this pillar gives you the language for hundreds of interacting random variables.\n\nYou will study directed models (Bayesian networks), undirected models (Markov random fields and CRFs), and temporal graphical models (hidden Markov models and Kalman filters). Then come the inference engines: exact inference (variable elimination and belief propagation), approximate inference (the variational methods that scale), and sampling (MCMC, Gibbs, and Hamiltonian Monte Carlo). The pillar finishes with latent variable models (EM and mixtures) and modern Bayesian deep learning, which is where this classical machinery reconnects with the VAEs and uncertainty estimates of pillar D.\n\nThis is the most mathematically demanding pillar, and the one that most changes how you think about every other model as a distribution you could have written down.",
    prerequisites: [
      "A2 Probability and information theory: this pillar leans on it heavily.",
      "B2 Bayesian inference (priors, posteriors, marginalization).",
      "A1 Linear algebra and A3 optimization; D Deep learning for the F8 lessons.",
    ],
    subs: [
      {
        id: "F1",
        name: "Directed models",
        intro:
          "Directed graphical models, or Bayesian networks, let you write a joint distribution over many variables as a product of simple local pieces, one conditional probability per node given its parents. The picture (a directed acyclic graph) is not decoration: its arrows encode exactly which variables are conditionally independent, so you can reason about cause-like structure and dependence by inspecting the graph instead of grinding through algebra.\n\nAfter these lessons you can factor a joint distribution over a DAG, read local Markov independencies straight from parent sets, and compute probabilities from conditional probability tables. You will also use plate notation to compactly draw models with i.i.d. replication, and apply d-separation (via the chain, fork, and collider motifs and the Bayes-ball procedure) to decide which variables become independent once you observe others.\n\nThis is the foundation for everything else in the pillar. Inference algorithms, latent variable models, and Bayesian deep learning all start from a graph you drew here, so getting fluent in reading independence pays off across F.",
        prerequisites: [
          "Bayes' rule and conditional probability (pillar A2)",
          "Maximum likelihood estimation (pillar A2)",
          "Comfort manipulating joint and conditional distributions",
        ],
        topics: [
          { name: "Bayesian networks", status: "gap" },
          { name: "Plate notation", status: "gap" },
          { name: "d-separation", status: "gap" },
        ],
      },
      {
        id: "F2",
        name: "Undirected models",
        intro:
          "Some dependencies have no natural direction: pixels in an image or labels in a sentence influence each other symmetrically. Undirected graphical models (Markov random fields) capture this by scoring configurations with clique potentials instead of directed conditionals, giving a Gibbs distribution whose structure encodes independence through graph separation rather than parent sets.\n\nHere you will represent a joint distribution as a Gibbs distribution over clique potentials, read Markov blankets off the graph, and state the Hammersley-Clifford theorem that ties potentials to independence. You will formulate a linear-chain conditional random field as a discriminative log-linear model for sequence labeling, derive its partition function, and see why a CRF can beat a generative HMM when you only need the labels. Factor graphs then unify directed and undirected models into one bipartite representation where message passing becomes natural.\n\nThese models power structured prediction in NLP, vision, and any setting with symmetric or sequential dependencies, and the factor-graph view sets up the inference algorithms in F4.",
        prerequisites: [
          "Bayesian networks and joint factorization (F1)",
          "d-separation and conditional independence (F1)",
          "Bayes' rule and basic probability (pillar A2)",
        ],
        topics: [
          { name: "Markov random fields", status: "gap" },
          { name: "Conditional random fields (CRF)", status: "gap" },
          { name: "Factor graphs", status: "gap" },
        ],
      },
      {
        id: "F3",
        name: "Temporal graphical models",
        intro:
          "When data arrives as a stream and a hidden state evolves over time, you need graphical models built for sequences. Temporal models track a latent state that you never observe directly, updating your belief about it as each new measurement arrives. This is the machinery behind tracking, filtering, and decoding noisy time-ordered signals.\n\nYou will derive the forward-backward algorithm for marginal state posteriors in a hidden Markov model and the Viterbi algorithm for the single most likely state sequence. For continuous linear-Gaussian states you will derive the Kalman filter's predict-update recursion directly from Bayes' rule and compute the Kalman gain in closed form. When the dynamics turn nonlinear or non-Gaussian, you will implement particle filters using sequential importance resampling and understand why resampling controls weight degeneracy.\n\nThese tools underpin speech recognition, robot localization, target tracking, and financial state estimation, and they connect to the broader time-series work in pillar G.",
        prerequisites: [
          "Bayesian networks and joint factorization (F1)",
          "Bayes' rule and Gaussian distributions (pillar A2)",
          "Importance sampling for particle filters (F6)",
        ],
        topics: [
          { name: "Hidden Markov Models (HMM)", status: "gap" },
          { name: "Kalman & extended Kalman filters", status: "gap" },
          { name: "Particle filters / sequential MC", status: "gap" },
        ],
      },
      {
        id: "F4",
        name: "Exact inference",
        intro:
          "Once you have a graphical model, the central question is how to answer queries from it: what is the marginal probability of one variable, or the posterior given some observations? Exact inference computes these answers without approximation by exploiting the graph's factorization to avoid summing over an exponential number of configurations.\n\nYou will run variable elimination on a small model, derive its complexity in terms of elimination order, and identify treewidth as the quantity that decides whether exact inference is feasible. You will derive the belief propagation (sum-product) message updates from first principles on a tree, see that they return exact marginals in a single pass, and understand why loopy belief propagation is only approximate. Finally you will triangulate a graph, build its junction tree, check the running intersection property, and run exact inference through the collect-distribute calibration schedule.\n\nThese algorithms are the exact backbone of probabilistic reasoning, and knowing when treewidth makes them intractable is exactly what motivates the approximate inference and sampling methods that follow.",
        prerequisites: [
          "Factor graphs and message passing (F2)",
          "Bayesian networks and conditional independence (F1)",
          "Comfort with marginalizing and conditioning distributions",
        ],
        topics: [
          { name: "Variable elimination", status: "gap" },
          { name: "Belief propagation", status: "gap" },
          { name: "Junction tree", status: "gap" },
        ],
      },
      {
        id: "F5",
        name: "Approximate inference",
        intro:
          "When exact inference is intractable, variational inference turns the problem into optimization: instead of computing the true posterior, you find the closest tractable distribution to it by maximizing a lower bound on the evidence. This trades a hard summation for a gradient-based search, which is what lets Bayesian methods scale to large models and datasets.\n\nYou will derive the evidence lower bound (ELBO) via Jensen's inequality, write the mean-field factorization, and derive the coordinate-ascent updates for each factor. From there you will build stochastic variational inference with mini-batch ELBO estimates and the reparameterization trick for low-variance gradients, then amortize the per-datapoint variational parameters into a shared encoder network and reason about the resulting amortization gap. The final lesson uses normalizing flows as flexible variational posteriors via the change-of-variables formula.\n\nVariational inference is the engine behind variational autoencoders, modern probabilistic programming, and scalable Bayesian deep learning, so this discipline connects classical PGMs directly to pillars D and F8.",
        prerequisites: [
          "Bayesian networks and joint factorization (F1)",
          "Priors, likelihoods, and posteriors (pillar B2)",
          "KL divergence and cross-entropy (pillar A2)",
        ],
        topics: [
          { name: "Mean-field variational inference", status: "gap" },
          { name: "Stochastic VI (SVI)", status: "gap", hot: true },
          { name: "Amortized VI (encoder networks)", status: "gap", hot: true },
          { name: "Normalizing flow posteriors", status: "gap", hot: true },
        ],
      },
      {
        id: "F6",
        name: "Sampling",
        intro:
          "Sampling is the other answer to intractable inference: rather than approximate the posterior with a simpler distribution, you draw representative samples from it and estimate any quantity you need from those draws. Markov chain Monte Carlo builds a chain whose long-run behavior matches the target distribution, giving asymptotically exact estimates with only mild assumptions.\n\nYou will start with rejection and importance sampling, deriving acceptance probabilities, importance weights, and the effective sample size. You will then derive the Metropolis-Hastings acceptance ratio from detailed balance and prove the target is the chain's stationary distribution, specialize it to Gibbs sampling using full conditionals, and move to Hamiltonian Monte Carlo and NUTS, where physics-inspired dynamics and the leapfrog integrator keep acceptance high in high dimensions. The final lesson connects Langevin dynamics and SGLD to approximate Bayesian posterior sampling with stochastic gradients.\n\nThese samplers power Bayesian data analysis, probabilistic programming languages, and uncertainty quantification across the sciences and machine learning.",
        prerequisites: [
          "Bayes' rule and maximum likelihood estimation (pillar A2)",
          "Probability density manipulation and expectations",
          "Gradients and basic optimization (pillar A3) for HMC and SGLD",
        ],
        topics: [
          { name: "Rejection & importance sampling", status: "gap" },
          { name: "MCMC (Metropolis-Hastings)", status: "gap" },
          { name: "Gibbs sampling", status: "gap" },
          { name: "Hamiltonian MC, NUTS", status: "gap" },
          { name: "Langevin dynamics, SGLD", status: "gap", hot: true },
        ],
      },
      {
        id: "F7",
        name: "Latent variable models",
        intro:
          "Latent variable models assume that observed data is generated by hidden factors you never see directly: a cluster assignment, a topic, or a low-dimensional code. Fitting them means maximizing a marginal likelihood that integrates over those hidden variables, which the Expectation-Maximization algorithm handles by alternating between inferring the latents and updating the parameters.\n\nYou will derive the E-step and M-step from the same ELBO bound used in variational inference, prove EM increases the marginal log-likelihood at every iteration, and apply it to a Gaussian mixture model. You will then study Latent Dirichlet Allocation, deriving the collapsed Gibbs update for topic assignments and interpreting the Dirichlet concentration hyperparameters, and finally probabilistic PCA and factor analysis, showing how the maximum-likelihood solution recovers principal components and how factor analysis generalizes it with per-dimension noise.\n\nThese models are workhorses for clustering, dimensionality reduction, and topic discovery, and EM is the conceptual ancestor of the variational and Bayesian deep learning methods elsewhere in the pillar.",
        prerequisites: [
          "Mean-field variational inference and the ELBO (F5)",
          "Maximum likelihood estimation (pillar A2)",
          "PCA and low-rank structure (pillar A1)",
        ],
        topics: [
          { name: "EM algorithm", status: "gap" },
          { name: "LDA topic model", status: "gap" },
          { name: "Probabilistic PCA, factor analysis", status: "gap" },
        ],
      },
      {
        id: "F8",
        name: "Modern Bayesian DL",
        intro:
          "Modern Bayesian deep learning brings the uncertainty machinery of this pillar to neural networks, so a model can say not just what it predicts but how confident it is and why. This matters wherever a wrong, overconfident prediction is costly: medicine, autonomous systems, and any deployment where you need calibrated risk rather than a bare point estimate.\n\nYou will derive the variational autoencoder objective as an amortized ELBO and use the reparameterization trick to backpropagate through a stochastic latent variable, the same trick from F5 now wired into a deep model. You will interpret MC dropout as approximate Bayesian inference, separate epistemic from aleatoric uncertainty, and contrast it with deep ensembles. From there you will place priors over network weights and derive the Laplace and mean-field variational approximations for Bayesian neural networks, and finally build split-conformal prediction intervals with a finite-sample coverage guarantee that holds under exchangeability with no distributional assumptions.\n\nThese methods are how probabilistic reasoning reaches production deep learning, and they cross-link directly to the VAEs and generative models of pillar D.",
        prerequisites: [
          "Amortized variational inference and the ELBO (F5)",
          "KL divergence and cross-entropy (pillar A2)",
          "Neural network training and backpropagation (pillar D)",
        ],
        topics: [
          { name: "VAE (cross-ref D4)", status: "gap" },
          { name: "MC dropout, deep ensembles", status: "gap" },
          { name: "Bayesian neural networks", status: "gap" },
          { name: "Uncertainty, conformal prediction", status: "gap" },
        ],
      },
    ],
  },
  {
    letter: "G",
    slug: "G-time-series",
    name: "Time Series & Forecasting",
    shortName: "Time Series",
    tagline: "ARIMA, state-space, DL forecasting, TS foundation models",
    color: "#73daca",
    intro:
      "Time series is data with memory. Order matters, each observation correlates with its own past, and the thing you actually want, the future, is the one value you never get to see during training. That single twist breaks the usual i.i.d. assumptions and demands its own toolkit, which this pillar builds from classical statistics up to foundation models.\n\nYou will start with classical statistical time series (ARIMA, exponential smoothing, and state-space models), then ML for time series (turning lags, rolling windows, and Fourier features into a supervised problem for gradient boosting). From there the pillar covers deep learning for time series (sequence models and the new time-series foundation models like Chronos), then anomaly and change-point detection, and finally causal time series, where forecasting meets the intervention questions of pillar B.\n\nThe recurring discipline here is honest backtesting: respecting time when you split, validate, and report, so that a model that looks brilliant in a notebook does not collapse the moment it meets tomorrow.",
    prerequisites: [
      "A2 Probability and B1 frequentist inference (autocorrelation, stationarity, intervals).",
      "C3 Tree-based methods and gradient boosting for the ML track.",
      "D3 Sequence modeling helps for the deep-learning lessons; Python with numpy and pandas.",
    ],
    subs: [
      {
        id: "G1",
        name: "Classical statistical TS",
        intro:
          "Classical statistical time series is the foundation of forecasting: a small, rigorous toolkit for series whose observations are correlated with their own past. The core problem is to model that memory honestly, separate genuine signal from drift and noise, and produce forecasts you can attach intervals to rather than point guesses.\n\nAfter this discipline you will test a series for stationarity with ADF and KPSS, read AR and MA orders off the ACF and partial ACF, and fit the full ARIMA and seasonal SARIMA family. You will derive Holt-Winters and the ETS taxonomy as recursive weighted averages, cast models in state-space form and run the Kalman filter for exact likelihoods, extend AR to vector autoregressions with cointegration and the VECM, model time-varying volatility with GARCH, and read a series in the frequency domain with the periodogram and wavelets.\n\nThese methods remain strong baselines in economics, finance, demand planning, and sensor monitoring, and every later forecasting pillar (the ML and deep-learning tracks especially) is measured against them.",
        prerequisites: [
          "A2 probability: expectation, variance, and moments.",
          "B1 frequentist inference: hypothesis testing for the unit-root tests.",
          "A1 linear algebra: eigenvalues and inner products for VAR and spectral lessons.",
          "Python with numpy and pandas.",
        ],
        topics: [
          { name: "Stationarity, ACF/PACF, ADF/KPSS", status: "gap" },
          { name: "ARIMA family (AR, MA, SARIMA)", status: "gap" },
          { name: "Exponential smoothing (Holt-Winters, ETS)", status: "gap" },
          { name: "State-space + Kalman filtering", status: "gap" },
          { name: "VAR, VECM, cointegration", status: "gap" },
          { name: "GARCH (volatility)", status: "gap" },
          { name: "Spectral analysis (Fourier, wavelets)", status: "gap" },
        ],
      },
      {
        id: "G2",
        name: "ML for time series",
        intro:
          "ML for time series reframes forecasting as a supervised learning problem. Instead of a bespoke statistical model, you engineer features from the past (lags, rolling statistics, and Fourier seasonality terms) and hand them to a general-purpose learner like gradient-boosted trees. The catch, and the whole discipline, is doing this without leaking future information into the training table.\n\nAfter this section you will build leakage-safe feature tables, forecast with XGBoost and LightGBM, and weigh the recursive against the direct multi-step strategy. You will reconcile forecasts across a hierarchy of series with bottom-up and the optimal MinT projection so totals and parts agree, and fit Prophet as a decomposable additive model of piecewise-linear trend, Fourier seasonality, and holiday effects with changepoint regularization.\n\nThis track is what wins many real forecasting competitions and powers retail demand, capacity, and revenue planning, where dozens of engineered features and a strong tabular learner often beat a hand-tuned ARIMA.",
        prerequisites: [
          "G1 classical time series, especially stationarity and the ACF.",
          "C3 tree-based methods: gradient boosting with XGBoost and LightGBM.",
          "C1 linear regression for the Prophet lesson.",
          "Python with numpy and pandas.",
        ],
        topics: [
          {
            name: "Feature engineering (lags, rolling, Fourier)",
            status: "gap",
          },
          { name: "XGBoost/LightGBM forecasting", status: "gap" },
          { name: "Hierarchical / grouped forecasting", status: "gap" },
          { name: "Prophet, Greykite", status: "gap" },
        ],
      },
      {
        id: "G3",
        name: "Deep learning for TS",
        intro:
          "Deep learning for time series scales forecasting up to many related series and long horizons, learning patterns directly from raw history rather than from hand-built features. The problem it solves is shared structure: when you have thousands of series, a single neural model can borrow strength across them and emit full probabilistic forecasts, not just point estimates.\n\nAfter this discipline you will build DeepAR as an autoregressive RNN that emits likelihood parameters, construct the basis-expansion blocks of N-BEATS and N-HiTS, and assemble the Temporal Fusion Transformer with variable selection, gated residual networks, and quantile loss. You will trace the long-horizon transformer line through Informer, Autoformer, and FEDformer, understand the patching and channel tricks of PatchTST and iTransformer, and finish with zero-shot foundation models like Chronos, TimeGPT, and Lag-Llama.\n\nThese models drive large-scale forecasting at retailers, cloud providers, and energy operators, and the foundation-model lessons connect directly to the transformer and LLM machinery of pillars D and E.",
        prerequisites: [
          "G2 ML for time series: feature engineering as a supervised problem.",
          "D1 and D3 deep learning core: MLPs and sequence models (LSTM, GRU).",
          "E3 transformer block and decoder-only architectures for the transformer lessons.",
          "A2 maximum likelihood; Python with numpy and a deep-learning framework.",
        ],
        topics: [
          { name: "DeepAR (probabilistic, RNN-based)", status: "gap" },
          { name: "N-BEATS, N-HiTS", status: "gap" },
          { name: "Temporal Fusion Transformer (TFT)", status: "gap" },
          { name: "Informer, Autoformer, FEDformer", status: "gap" },
          { name: "PatchTST, iTransformer", status: "gap", hot: true },
          {
            name: "TS foundation models (TimeGPT, Chronos, Lag-Llama)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "G4",
        name: "Anomaly & change-point",
        intro:
          "Anomaly and change-point detection asks a different question from forecasting: not what comes next, but when something has gone wrong. The problem is to flag unusual points and detect structural shifts in a stream, ideally online and with a controlled false-alarm rate, so alerts are trustworthy rather than noisy.\n\nAfter this section you will flag point anomalies with the IQR rule and a robust z-score, apply the generalized ESD test for multiple outliers, and derive the CUSUM statistic as a sequential likelihood-ratio accumulator that catches a shift in mean as it happens. You will then score anomalies by reconstruction error from sequence autoencoders, set thresholds from the residual distribution, and understand the LSTM-AE and transformer-AE variants for richer temporal structure.\n\nThis discipline underpins fraud detection, infrastructure and sensor monitoring, predictive maintenance, and the drift alarms that keep production models healthy, linking it directly to the monitoring concerns of pillar I.",
        prerequisites: [
          "G1 classical time series: stationarity and the ACF.",
          "B1 frequentist inference: hypothesis testing for the statistical tests.",
          "D4 autoencoders for the deep detection lesson.",
          "Python with numpy and pandas.",
        ],
        topics: [
          { name: "Statistical (IQR, ESD, CUSUM)", status: "gap" },
          { name: "Deep AD (LSTM-AE, Transformer-AE)", status: "gap" },
        ],
      },
      {
        id: "G5",
        name: "Causal time series",
        intro:
          "Causal time series is where forecasting meets the intervention questions of causal inference: not just predicting a series, but estimating what an action did to it. The problem is that you only ever observe one timeline, so the effect of a launch, a policy, or a campaign has to be read against a counterfactual you have to construct.\n\nAfter this discipline you will define and test Granger causality as predictive improvement with a restricted-versus-full VAR F-test, and state precisely what it does and does not claim. You will estimate intervention effects with CausalImpact by forecasting the counterfactual from a Bayesian structural time-series model fit on control series, and build a synthetic control as a convex combination of donor units matched on pre-treatment outcomes, reading the effect as the post-period gap.\n\nThese methods are the workhorses of marketing and product experimentation, economics, and policy evaluation when a clean randomized trial is impossible, and they tie pillar G back to the causal-inference machinery of pillar B.",
        prerequisites: [
          "G1 classical time series: VAR, cointegration, and the Kalman filter.",
          "B5 causal inference: potential outcomes and difference-in-differences.",
          "A1 least squares for the synthetic-control construction.",
          "Python with numpy and pandas.",
        ],
        topics: [
          { name: "Granger causality", status: "gap" },
          { name: "CausalImpact (Bayesian structural TS)", status: "gap" },
          { name: "Synthetic control for TS", status: "gap", hot: true },
        ],
      },
    ],
  },
  {
    letter: "H",
    slug: "H-reinforcement-learning",
    name: "Reinforcement Learning",
    shortName: "RL",
    tagline: "MDPs, deep RL, model-based, RLHF",
    color: "#ff7eb6",
    intro:
      "Reinforcement learning is decision-making under uncertainty. An agent acts, the world responds with a new state and a reward, and over many such steps it learns a policy that maximizes long-run return. Unlike supervised learning, there are no labels, only consequences, often delayed, which makes credit assignment the central difficulty.\n\nYou will build from RL foundations (Markov decision processes, value functions, dynamic programming, and temporal-difference learning), then deep RL (DQN, policy gradients, actor-critic, and PPO), then model-based RL (learning a world model and planning inside it). From there the pillar covers exploration (how an agent decides what to try), topics beyond standard RL (offline, multi-agent, and inverse RL), and the RL-LLM connection (RLHF and verifier-guided RLVR), which is how the reasoning models of pillar E are actually trained.\n\nExpect this pillar to feel different from the others: the data is something your own policy generates, so training is a moving target, and stability is as much of an achievement as accuracy.",
    prerequisites: [
      "A2 Probability and A3 optimization (expectations, gradients, stochastic approximation).",
      "D1 Deep learning core building blocks for the function approximators in deep RL.",
      "Python with numpy; E NLP/LLMs helps for the H6 RL-and-LLMs lessons.",
    ],
    subs: [
      {
        id: "H1",
        name: "RL foundations",
        intro:
          "RL foundations is where decision-making under uncertainty gets its vocabulary. You frame a problem as a Markov decision process: states, actions, transitions, and rewards, with a discount that ties future payoff to the present. From that single object come the value functions that say how good a state or action is, and the Bellman equations that relate each value to the values that follow it.\n\nBy the end you can solve a known MDP exactly with policy iteration and value iteration, and prove both converge because the Bellman operator is a contraction. When the dynamics are unknown, you can estimate values from sampled experience instead: Monte Carlo from full episodes, temporal-difference learning by bootstrapping one step at a time, and control with Q-learning and SARSA.\n\nThese ideas are the bedrock of everything else in the pillar. Deep RL, exploration, and even RLHF are all built on the MDP frame and the value estimates you learn to reason about here.",
        prerequisites: [
          "A2 Probability: expectations, Markov chains, the law of large numbers",
          "Basic familiarity with sequences and limits (for convergence arguments)",
          "Python with numpy for small tabular experiments",
        ],
        topics: [
          { name: "MDPs, Bellman equations", status: "gap" },
          { name: "Value iteration, policy iteration", status: "gap" },
          { name: "Monte Carlo & TD methods", status: "gap" },
          { name: "Q-learning, SARSA", status: "gap" },
        ],
      },
      {
        id: "H2",
        name: "Deep RL",
        intro:
          "Deep RL scales the tabular methods of H1 to problems where states are too numerous or too high-dimensional to enumerate, like pixels or continuous control. The move is to replace value tables and explicit policies with neural networks, then ask what breaks: function approximation, bootstrapping, and off-policy data together form the deadly triad that can make training diverge.\n\nYou will learn the two main families and the tricks that make them stable. On the value side: DQN with experience replay and target networks, plus the Double, dueling, and prioritized refinements that compose Rainbow. On the policy side: the policy gradient theorem and REINFORCE, variance reduction with a baseline, actor-critic with GAE, the clipped PPO objective, and continuous-control methods DDPG, TD3, and SAC.\n\nThis is the toolkit behind most modern applied RL, from game-playing agents to robotics, and PPO and GRPO reappear directly in the RLHF pipeline of H6.",
        prerequisites: [
          "H1 RL foundations: Q-learning, SARSA, value functions",
          "D1 Deep learning core: backpropagation and network training",
          "A3 Optimization: stochastic gradient descent",
        ],
        topics: [
          { name: "DQN family (Double, Dueling, Rainbow)", status: "gap" },
          { name: "Policy gradient (REINFORCE)", status: "covered" },
          { name: "Actor-critic (A2C, A3C)", status: "partial" },
          { name: "PPO", status: "covered" },
          { name: "DDPG, TD3, SAC", status: "gap" },
          { name: "GRPO", status: "covered" },
        ],
      },
      {
        id: "H3",
        name: "Model-based RL",
        intro:
          "Model-based RL asks the agent to learn how the world works, not just which actions paid off. Once you have a model of transitions and rewards, you can plan: simulate possible futures and update your policy from imagined experience, which is far more sample-efficient than learning from real interaction alone.\n\nYou will start with Dyna-Q, which interleaves real updates with model-generated ones, then build the search-based line: Monte Carlo tree search with UCT, AlphaZero replacing rollouts with a self-play-trained network, and MuZero learning a latent dynamics model so it can plan without the true simulator. The pillar closes with world models and Dreamer, which learn latent dynamics from pixels and train a policy entirely inside imagined rollouts by backpropagating returns through the model.\n\nThese methods sit behind some of the field's most striking results in games and control, and the latent-dynamics idea connects directly to the generative models of pillar D.",
        prerequisites: [
          "H1 RL foundations: dynamic programming and value functions",
          "H2 Deep RL: training value and policy networks",
          "D4 VAEs / latent variable models (helpful for world models)",
        ],
        topics: [
          { name: "Dyna-Q, planning", status: "gap" },
          { name: "MuZero, AlphaZero", status: "gap", hot: true },
          { name: "World models (Dreamer)", status: "gap", hot: true },
        ],
      },
      {
        id: "H4",
        name: "Exploration",
        intro:
          "Exploration is the question of what an agent should try when it does not yet know what is good. Exploit too early and you lock onto a mediocre choice; explore forever and you waste reward. This discipline gives you principled ways to balance the two, starting in the clean setting of the multi-armed bandit where the tradeoff is laid bare.\n\nYou will derive and compare the classic strategies: epsilon-greedy, the UCB confidence bonus, and Thompson sampling, including how their regret grows over time. Then you move to hard exploration in sparse-reward MDPs, where reward almost never arrives, using intrinsic motivation: bonuses from prediction error and novelty, implemented concretely with random network distillation.\n\nExploration is the hidden ingredient in many RL success stories, and the bandit framing here also underpins recommendation, A/B testing, and the action-selection step inside the search methods of H3.",
        prerequisites: [
          "H1 RL foundations: MDPs and value functions",
          "A2 Probability: Bayes' rule and confidence intervals",
          "H2 Deep RL: DQN (for the intrinsic-motivation lessons)",
        ],
        topics: [
          { name: "ε-greedy, UCB, Thompson sampling", status: "gap" },
          { name: "Intrinsic motivation, RND", status: "gap" },
        ],
      },
      {
        id: "H5",
        name: "Beyond standard RL",
        intro:
          "Beyond standard RL collects the settings that break the usual online, single-agent, reward-given assumptions. Sometimes you have expert demonstrations but no reward; sometimes a fixed dataset and no environment to query; sometimes several learning agents at once. Each twist needs its own machinery, and this discipline supplies it.\n\nYou will learn imitation learning by behavioral cloning and DAgger (and why naive cloning compounds errors under distribution shift), inverse RL that recovers the reward behind expert behavior with the GAIL connection, offline RL methods CQL and IQL that learn safely from a fixed dataset, multi-agent RL with self-play and centralized-training-decentralized-execution, and hierarchical RL via the options framework over a semi-MDP.\n\nThese are the techniques that make RL practical when interaction is expensive or dangerous, and the imitation and offline ideas here are close cousins of how preference data is used to align language models in H6.",
        prerequisites: [
          "H1 RL foundations: MDPs and value functions",
          "H2 Deep RL: policy gradients and actor-critic, plus DDPG/TD3/SAC for offline RL",
          "A2 Probability: entropy (for inverse RL)",
        ],
        topics: [
          { name: "Imitation learning, behavioral cloning", status: "gap" },
          { name: "Inverse RL", status: "gap" },
          { name: "Offline RL (CQL, IQL)", status: "gap", hot: true },
          { name: "Multi-agent RL", status: "gap" },
          { name: "Hierarchical RL", status: "gap" },
        ],
      },
      {
        id: "H6",
        name: "RL ↔ LLMs",
        intro:
          "RL meets LLMs is where this pillar connects to the language models of pillar E. The key reframe is that autoregressive text generation is itself a Markov decision process: each token is an action, the prompt and partial text are the state, and a reward scores the finished response. Seen this way, RLHF and its successors are RL algorithms, and the PPO and GRPO machinery of H2 applies directly.\n\nYou will cast generation as a token-level MDP with a KL-to-reference penalty, then study RLVR, which swaps a learned reward model for a programmatic verifier and optimizes with a group-relative baseline, the recipe behind R1-style emergence of long reasoning chains. You will also analyze reward hacking: why optimizing a proxy reward eventually degrades the true objective (Goodhart), and how KL control and reward ensembles push back.\n\nThis is among the most active areas in AI right now, and it is how the reasoning and aligned models you use every day are actually trained.",
        prerequisites: [
          "H2 Deep RL: PPO and policy gradients",
          "E4 LLM post-training: RLHF, reward modeling, GRPO",
          "Familiarity with transformer language models (pillar E)",
        ],
        topics: [
          { name: "RLHF end-to-end", status: "covered" },
          { name: "DPO, IPO, KTO, RLAIF", status: "covered" },
          { name: "Process reward models", status: "covered" },
          { name: "Reward hacking", status: "covered" },
          {
            name: "Verifier-guided / RLVR (R1 style)",
            status: "gap",
            hot: true,
          },
        ],
      },
    ],
  },
  {
    letter: "I",
    slug: "I-mlops",
    name: "MLOps & Production Systems",
    shortName: "MLOps",
    tagline: "Data, training infra, deployment, monitoring",
    color: "#9ece6a",
    intro:
      "A model that works in a notebook is not a product. MLOps is the engineering discipline that gets models into production and keeps them healthy once real traffic and real data start hitting them. This pillar is deliberately conceptual and infrastructure-focused rather than mathematical: the hard parts here are systems, reliability, and process, not derivations.\n\nYou will cover data engineering (ingestion, ETL and ELT pipelines, and feature stores), training infrastructure (experiment tracking, orchestration, and scaling jobs across hardware), deployment and serving (containers, model servers, autoscaling, and latency budgets), and monitoring and governance (data and concept drift, observability, lineage, and the compliance trail). The throughline is the lifecycle: a deployed model is never finished, only maintained.\n\nThis is where the rest of the tree meets reality, the difference between a clever result and a system other people can depend on.",
    prerequisites: [
      "A trained model from any modeling pillar (C through H) that you want to ship.",
      "Comfort with Python, the command line, and basic version control.",
      "Familiarity with containers (Docker) and a cloud provider helps; no heavy math required.",
    ],
    subs: [
      {
        id: "I1",
        name: "Data engineering",
        intro:
          "Data engineering is the plumbing that gets clean, trustworthy data to your models on a schedule you can rely on. Before any training run matters, something has to ingest raw data, transform it, store it, and feed the same values to both training and inference without leaking the future. This discipline is about building those pipelines so they stay correct under retries, backfills, and shifting upstream sources.\n\nAfter studying it you will be able to choose between ETL and ELT and between batch and streaming based on latency and reprocessing needs, model a pipeline as a directed acyclic graph and make each task idempotent so retries are safe, serve features through point-in-time joins that avoid label leakage, version a dataset by content hash for reproducibility, and quantify distribution shift with the Kolmogorov-Smirnov statistic and the population stability index.\n\nEvery production ML system lives or dies on its data layer: a feature computed differently in training and serving, or a silently drifting input, breaks models long after the code looks fine. These are the skills that keep that from happening.",
        prerequisites: [
          "Graph traversal and topological sort, plus hashing (pillar A5)",
          "Probability basics: distributions, KL and cross-entropy (pillar A2)",
          "Hypothesis testing for drift statistics (pillar B1)",
          "Comfort with Python and the command line",
        ],
        topics: [
          {
            name: "ETL/ELT pipelines (Airflow, Dagster, Prefect)",
            status: "gap",
          },
          { name: "Feature stores (Feast, Tecton)", status: "gap" },
          { name: "Data versioning (DVC, lakeFS)", status: "gap" },
          { name: "Data quality & drift detection", status: "gap" },
        ],
      },
      {
        id: "I2",
        name: "Training infrastructure",
        intro:
          "Training infrastructure is everything around the optimizer that lets experiments be reproducible and large jobs run across many machines. A single training script is easy; what is hard is tracking which code, data, config, and seed produced which result, searching a hyperparameter space without wasting compute, and scaling a run past the memory of one GPU. This discipline covers that scaffolding.\n\nAfter studying it you will be able to log the full lineage of a run so results are comparable and reproducible, frame tuning as black-box optimization and see why random search beats grid search when only a few dimensions matter, spend a fixed budget efficiently with successive halving and Hyperband, scale training by averaging gradients with all-reduce (and adjust the learning rate accordingly), and do the memory math that shows how ZeRO's three sharding stages divide optimizer state, gradients, and parameters across workers.\n\nThis is the difference between a result you got once and a result your team can rerun, and between a model that fits on one card and one that needs a cluster. It is the daily reality of any group training models at scale.",
        prerequisites: [
          "Stochastic gradient descent and learning-rate intuition (pillar A3)",
          "Bayesian optimization basics (pillar A3)",
          "Data and model parallelism fundamentals (pillar D7)",
          "Data versioning from I1",
        ],
        topics: [
          { name: "Experiment tracking (W&B, MLflow)", status: "gap" },
          { name: "HPO orchestration (Optuna, Ray Tune)", status: "gap" },
          { name: "Distributed orchestrators (Ray, DeepSpeed)", status: "gap" },
        ],
      },
      {
        id: "I3",
        name: "Deployment & serving",
        intro:
          "Deployment and serving is where a trained model becomes a service that answers requests under a latency budget. The questions change completely: now you care about percentiles, GPU memory, batching, and how to make a big model small enough to run fast or fit on a phone. This discipline gives you the quantitative tools to serve models, especially large language models, without guessing.\n\nAfter studying it you will be able to summarize latency with percentiles and relate concurrency, throughput, and latency through Little's law, size the KV cache that bounds LLM serving and explain why continuous batching keeps the GPU saturated, map weights to low-bit integers with affine quantization and bound the rounding error, shrink models through distillation and magnitude pruning while quantifying the size-quality tradeoff, and reason about edge deployment where memory, power, and offline operation are the binding constraints.\n\nServing is where cost and user experience are decided. The same model can be cheap and snappy or slow and expensive depending entirely on how it is batched, quantized, and scheduled, which is what these lessons teach you to control.",
        prerequisites: [
          "Expectation and percentiles (pillar A2)",
          "Floating-point representation (pillar A4)",
          "KV cache, paged attention, and quantization in LLMs (pillar E5)",
          "Regularization, and KL/cross-entropy for distillation (pillars D1, A2)",
        ],
        topics: [
          { name: "Classical serving (TF Serving, TorchServe)", status: "gap" },
          { name: "LLM serving (vLLM, TGI, Ollama)", status: "gap", hot: true },
          { name: "Quantization, distillation, pruning", status: "gap" },
          { name: "Edge / on-device (ONNX, CoreML)", status: "gap" },
        ],
      },
      {
        id: "I4",
        name: "Monitoring & governance",
        intro:
          "Monitoring and governance is what keeps a deployed model honest after launch, when traffic and data quietly change and labels arrive late or never. A model is never finished, only maintained, so this discipline is about measuring reliability, detecting decay, evaluating models defensibly, and tracking what they cost. It turns vague worries about production health into numbers you can alert on.\n\nAfter studying it you will be able to turn user-facing reliability into service-level indicators and objectives, derive the error budget and the burn rate that should trigger an alert, separate a shift in inputs from a shift in the labelling rule under label delay, estimate LLM accuracy with the unbiased pass@k estimator while guarding against test-set contamination, put Wilson intervals on attack success rates when red-teaming, and build a per-request cost model that shows how batching and caching change unit economics.\n\nThis is the discipline that catches silent failure: a model that still returns answers but has stopped being right, or a service whose costs creep until it is no longer viable. In production, monitoring is the difference between a controlled system and a surprise.",
        prerequisites: [
          "Latency, throughput, and percentiles from I3",
          "Drift detection from I1",
          "A/B testing and confidence intervals (pillar B4)",
          "LLM serving and its cost structure from I3",
        ],
        topics: [
          {
            name: "Performance monitoring (latency, throughput, p99)",
            status: "gap",
          },
          { name: "Concept drift, data drift", status: "gap" },
          { name: "LLM evals (lm-eval, MMLU, HELM)", status: "gap" },
          { name: "Safety evals, red-teaming", status: "gap", hot: true },
          { name: "Cost monitoring (token economics)", status: "gap" },
        ],
      },
    ],
  },

  // ----------------------------------------------------------------
  // J: AI Engineering (sourced from AI Eng Journey roadmap, Cap 1–7)
  // ----------------------------------------------------------------
  {
    letter: "J",
    slug: "J-ai-engineering",
    name: "AI Engineering",
    shortName: "AI Engineering",
    tagline:
      "RAG, agents, MCP, production, Cloud AI: the AI Eng Journey roadmap",
    color: "#c0caf5",
    intro:
      "AI engineering is building real applications on top of foundation models. You are not training the model here; you are composing it, grounding it in your own data, wrapping it in tools, and shipping it as something users and businesses can rely on. This pillar is the applied capstone of the tree, and the one closest to the work most practitioners actually do day to day.\n\nYou will begin with the fundamentals (retrieval-augmented generation, tool use, agents, and the LangChain and LangGraph frameworks), then systems thinking (the Model Context Protocol, evaluation harnesses, and production-grade RAG). From there the pillar covers production and enterprise integration (API design, governance, deployment, observability, and security against prompt injection), advanced patterns (when not to fine-tune, LoRA, DSPy, multi-agent systems, and cost and latency engineering), the data platform for AI (vector infrastructure at scale, hybrid search, and event-driven pipelines), and cloud AI (Bedrock end to end, identity and security, and FinOps). It closes with architect-level skills: red teaming and system design for AI.\n\nThe mindset shift here is from accuracy to systems: latency, cost, reliability, and security matter as much as whether the model is right.",
    prerequisites: [
      "E NLP and LLMs (especially RAG, agents, and inference) is the conceptual backbone.",
      "Solid Python plus web and API basics (HTTP, JSON, async); FastAPI familiarity helps.",
      "I MLOps is complementary; basic cloud and Docker for the deployment lessons.",
    ],
    subs: [
      {
        id: "J1",
        name: "Fundamentals (RAG, tool_use, agents)",
        intro:
          "This discipline is where you stop thinking of a language model as a finished product and start treating it as a component you compose. The problem it solves is concrete: a raw model knows nothing about your documents and cannot take action in the world. Retrieval-augmented generation grounds it in your data, tool use lets it call real functions, and the ReAct loop chains those calls into multi-step agency.\n\nAfter studying it you can build a RAG pipeline end to end (chunk documents, embed them, retrieve the top-k most similar chunks by cosine similarity), inject tool schemas and dispatch the structured calls a model emits, hand-write the reason-act-observe loop, and then read frameworks like LangChain and LangGraph as abstractions over machinery you already understand.\n\nThis matters because almost every AI product is some arrangement of these four pieces. Knowing what a framework hides keeps you in control when an agent loops forever, retrieves the wrong chunk, or calls a tool it should not.",
        prerequisites: [
          "Pillar E NLP and LLMs: RAG fundamentals, dense retrieval, and function calling",
          "Inner products and cosine similarity from A1",
          "Comfortable Python: parsing JSON, calling APIs, writing functions",
        ],
        topics: [
          {
            name: "RAG from scratch (pypdf, ChromaDB, embeddings)",
            status: "gap",
          },
          {
            name: "Native tool_use (Claude API, schema injection)",
            status: "gap",
          },
          { name: "ReAct loop manual", status: "gap" },
          {
            name: "LangChain (@tool, create_react_agent, memory)",
            status: "gap",
          },
          {
            name: "LangGraph (StateGraph, nodes, edges, routers)",
            status: "gap",
          },
        ],
      },
      {
        id: "J2",
        name: "Systems thinking",
        intro:
          "Once a single agent works, the next problem is making it a system you can integrate, trust, and improve. This discipline covers the connective tissue: the Model Context Protocol that standardizes how tools and resources are exposed, evaluation harnesses that tell you whether a change helped or hurt, production-grade retrieval, and the storage architectures your data sits on.\n\nYou will learn why a shared protocol turns an N-by-M integration mess into N-plus-M, how to design and version an MCP server for a model audience rather than a human one, how to score open-ended outputs with an LLM judge and check that judge against humans with Cohen's kappa, and how a retrieve-then-rerank pipeline lifts ranking quality (measured with nDCG). You will also place workloads across data lake, warehouse, and lakehouse architectures.\n\nThis is the layer that separates a demo from something a team can extend. Without evaluation you are guessing; without a protocol every new tool is bespoke plumbing.",
        prerequisites: [
          "J1: tool use, the ReAct loop, and RAG from scratch",
          "Pillar I4 LLM evaluation and B4 A/B testing for the judging lessons",
          "Pillar E6 advanced RAG and I1 pipeline paradigms",
        ],
        topics: [
          {
            name: "MCP: protocol, servers, integrations",
            status: "gap",
            hot: true,
          },
          {
            name: "Design an MCP server (granularity, versioning)",
            status: "gap",
            hot: true,
          },
          {
            name: "Evaluation: LLM-as-judge, datasets, regression",
            status: "gap",
          },
          {
            name: "Production RAG (chunking, hybrid search, rerank)",
            status: "gap",
          },
          { name: "Data Lake × Warehouse × Lakehouse", status: "gap" },
        ],
      },
      {
        id: "J3",
        name: "Production grade & enterprise integration",
        intro:
          "This discipline takes a working AI service and makes it something you can run in front of real users and a real business. The problem it solves is everything that is not the model: serving the API, controlling who calls it and at what cost, shipping it reliably, seeing inside it when it breaks, and defending it against attack.\n\nYou will be able to design an HTTP surface that streams tokens, handles concurrent requests with async I/O, and versions cleanly; put a governance layer in front of the model with authentication, a token-bucket rate limiter, and per-tenant cost attribution; package the service into a reproducible container and ship it through CI/CD with secrets kept out of the image; instrument a request as a tree of spans to find where latency and tokens go; and reason about prompt injection by treating untrusted content as a trust boundary with least privilege and output filtering.\n\nThese are the skills that decide whether an AI feature survives contact with production traffic, a budget, and an adversary.",
        prerequisites: [
          "J1 and J2: a working agent plus production RAG and evaluation",
          "Pillar I MLOps: LLM serving, cost monitoring, SLOs, and safety evals",
          "Web and API basics (HTTP, JSON, async); Docker and CI/CD familiarity helps",
        ],
        topics: [
          {
            name: "API design (FastAPI, streaming, async, versioning)",
            status: "gap",
          },
          {
            name: "Governance layer (auth, rate limiting, cost attribution)",
            status: "gap",
          },
          {
            name: "Deployment (Docker, CI/CD, env config, secrets)",
            status: "gap",
          },
          {
            name: "Observability (tracing, latency, LangSmith)",
            status: "gap",
          },
          { name: "Surfaces (Slack/Teams/Outlook integration)", status: "gap" },
          {
            name: "Security thread (prompt injection, data exfiltration)",
            status: "gap",
            hot: true,
          },
          { name: "Multi-source ingestion (REST + S3 + DB)", status: "gap" },
          { name: "ELT × ETL + dbt mental model", status: "gap" },
        ],
      },
      {
        id: "J4",
        name: "Advanced patterns",
        intro:
          "This discipline is about the judgment calls that separate an engineer who reaches for the heaviest tool from one who reaches for the right one. The central problem: teams over-fine-tune, over-engineer single agents into committees, and ignore cost until the bill arrives. The lessons give you cheaper, sharper alternatives and the reasoning to choose between them.\n\nYou will learn when prompting, RAG, and long context beat fine-tuning and the narrow conditions where fine-tuning actually pays; count exactly how few parameters a LoRA adapter trains and how QLoRA's quantized base weights fit a large model on one GPU; treat prompts as parameters to be optimized rather than strings to hand-tune (the DSPy shift to context engineering); decompose a hard task across a supervisor and specialized workers with explicit handoffs; and cut serving cost with a model cascade that escalates only the hard queries.\n\nThese patterns are where senior engineering shows: every one trades capability against cost, latency, or complexity, and you will be able to argue the tradeoff with numbers.",
        prerequisites: [
          "J1 and J2: agents, LangGraph, and production RAG",
          "Pillar E4 SFT and LoRA, E6 multi-agent for the fine-tuning and orchestration lessons",
          "Pillar I3 quantization and I4 cost monitoring",
        ],
        topics: [
          {
            name: "When NOT to fine-tune (prompting + RAG + long context)",
            status: "gap",
          },
          {
            name: "LoRA / QLoRA (single session, not a black box)",
            status: "gap",
            hot: true,
          },
          {
            name: "DSPy, prompt optimization, context engineering",
            status: "gap",
            hot: true,
          },
          {
            name: "Multi-agent (supervisor, worker, handoffs, shared memory)",
            status: "gap",
            hot: true,
          },
          {
            name: "Cost & latency (caching, model routing, prompt compression)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "J5",
        name: "Data platform for AI",
        intro:
          "An AI product is only as good as the data flowing into it, and this discipline builds the platform underneath. The problem it solves is keeping retrieval fast, fresh, and trustworthy at scale, and keeping the transformations that feed it tested rather than ad hoc.\n\nYou will be able to build warehouse transformations as a version-controlled, tested dbt DAG with lineage; enforce a schema as a contract so a bad upstream change fails fast instead of silently corrupting downstream tables; scale retrieval past brute force with an approximate nearest-neighbor index and measure the recall-versus-speed tradeoff every vector database is built on; fuse dense and sparse retrieval with reciprocal rank fusion so two rankings beat either alone; and keep an index current with change-data-capture updates and a disciplined embedding lifecycle for model upgrades.\n\nThis matters because retrieval quality, freshness, and data trust are where most production RAG systems quietly degrade. The vector index and the pipeline feeding it are as load-bearing as the model itself.",
        prerequisites: [
          "J2 production RAG and J3 multi-source ingestion",
          "Pillar E6 dense retrieval; A5 probabilistic structures for ANN intuition",
          "Pillar I1 pipeline paradigms and feature stores",
        ],
        topics: [
          { name: "dbt in depth", status: "gap" },
          { name: "Orchestration (Dagster or Airflow)", status: "gap" },
          { name: "Data contracts", status: "gap" },
          {
            name: "Vector infra at scale (pgvector × managed)",
            status: "gap",
            hot: true,
          },
          {
            name: "Hybrid search, embedding lifecycle",
            status: "gap",
            hot: true,
          },
          {
            name: "Event-driven & streaming for AI (Kafka, CDC)",
            status: "gap",
          },
          { name: "Feature stores & embedding stores (Feast)", status: "gap" },
        ],
      },
      {
        id: "J6",
        name: "Cloud AI & enterprise integration",
        intro:
          "This discipline scales an AI system from one team's project to an enterprise platform running on cloud infrastructure. The problem it solves: at organizational scale you face build-versus-buy decisions, hostile threat models, many tenants sharing one system, and a spend that compounds with every request.\n\nYou will be able to read a managed stack like AWS Bedrock (knowledge bases, agents, guardrails) as pre-assembled building blocks and decide build-versus-buy against control, lock-in, and time-to-ship; secure the system with cloud identity primitives (IAM roles, VPCs, SSO, OAuth) and least privilege that contains a compromise's blast radius; serve many tenants with isolation, per-tenant quotas, and a gateway that centralizes auth and routing; and plan spend by modeling the break-even between on-demand and reserved capacity and layering caching tiers.\n\nThese are the integration and economics concerns that decide whether an AI system is viable inside a real company, not just a notebook.",
        prerequisites: [
          "J2 production RAG, J3 governance and security, J4 cost and routing",
          "Basic cloud concepts: IAM, VPCs, and managed services",
          "Comfort with auth flows (OAuth, SSO) and the build-vs-buy framing",
        ],
        topics: [
          {
            name: "AWS Bedrock end-to-end (KB, Agents, Guardrails)",
            status: "gap",
            hot: true,
          },
          {
            name: "Managed × self-hosted LangGraph (tradeoffs)",
            status: "gap",
          },
          {
            name: "Identity & security (IAM, VPC, SSO, OAuth)",
            status: "gap",
          },
          { name: "API gateway, service mesh, multi-tenancy", status: "gap" },
          {
            name: "Cost & FinOps for AI (caching tiers, reserved capacity)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "J7",
        name: "Architect skills",
        intro:
          "This is the capstone of the capstone: the architect-level skills that turn a pile of components into a defensible system design. The problem it solves is communicating, governing, securing, and sizing an AI product at the level a staff engineer or architect is held to.\n\nYou will be able to build the controls data-protection regimes like GDPR and LGPD demand (data residency, purpose limitation, the right to deletion, an audit trail for automated decisions); turn one-off safety testing into a continuous, automated red-teaming pipeline with layered defenses so no single bypass wins; communicate a design with reference architectures, architecture decision records, and C4 diagrams; drive a system design from requirements to components to tradeoffs the way an architect interview expects; and size a system from first principles, turning a traffic estimate into a token rate, a GPU count, and a monthly bill.\n\nThis matters because at the senior level the deliverable is not code but a design others can trust, audit, and fund.",
        prerequisites: [
          "The full pillar J path: J1 through J6",
          "Pillar I4 safety evals and red teaming, I3 LLM serving for capacity modeling",
          "Some exposure to compliance, system design, and back-of-the-envelope estimation",
        ],
        topics: [
          { name: "AI governance (LGPD/GDPR for AI systems)", status: "gap" },
          {
            name: "Red teaming, prompt injection at scale",
            status: "gap",
            hot: true,
          },
          { name: "Reference architectures, ADRs, C4 diagrams", status: "gap" },
          {
            name: "System design for AI (architect-interview style)",
            status: "gap",
          },
          { name: "Capacity / cost modeling", status: "gap" },
        ],
      },
    ],
  },
];

// -------------------------------------------------------------------------
// CONNECTIONS: cross-pillar links between subsections
// -------------------------------------------------------------------------
// Each edge means "to understand X you should also know Y" or "the same idea
// shows up in both places". Used by /connections to render the live DAG.

export const CONNECTIONS: Connection[] = [
  // ---- A. Foundations radiating outward ----
  { from: "A1", to: "C5", label: "SVD ⇒ PCA", kind: "uses" },
  {
    from: "A1",
    to: "C8",
    label: "Matrix factorization for rec sys",
    kind: "uses",
  },
  {
    from: "A2",
    to: "E4",
    label: "KL divergence (RLHF penalty)",
    kind: "shared-concept",
  },
  {
    from: "A2",
    to: "F1",
    label: "Bayes rule ⇒ Bayes nets",
    kind: "generalizes",
  },
  {
    from: "A2",
    to: "B2",
    label: "Probability ⇒ Bayesian inference",
    kind: "uses",
  },
  { from: "A3", to: "D1", label: "Optimization powers training", kind: "uses" },
  {
    from: "A3",
    to: "H2",
    label: "Policy gradient is gradient descent",
    kind: "uses",
  },
  { from: "A5", to: "D6", label: "Graph algorithms ⇒ GNNs", kind: "uses" },
  {
    from: "A4",
    to: "D7",
    label: "Numerical stability ⇒ mixed precision",
    kind: "uses",
  },

  // ---- B. Statistics & Causal ----
  { from: "B2", to: "F5", label: "Bayesian inference ⇒ VI", kind: "uses" },
  { from: "B2", to: "F6", label: "Bayesian inference ⇒ MCMC", kind: "uses" },
  {
    from: "B4",
    to: "H4",
    label: "Bandits ↔ RL exploration",
    kind: "shared-concept",
  },
  {
    from: "B5",
    to: "G5",
    label: "Causal inference for TS",
    kind: "shared-concept",
  },

  // ---- C. Classical ML bridges to DL ----
  { from: "C1", to: "D1", label: "Linear → MLPs", kind: "generalizes" },
  {
    from: "C5",
    to: "D5",
    label: "PCA → representation learning",
    kind: "generalizes",
  },
  { from: "C7", to: "G2", label: "XGBoost on time series", kind: "uses" },
  { from: "C8", to: "C9", label: "Rec sys uses ANN search", kind: "uses" },
  { from: "C9", to: "E6", label: "Vector DBs power RAG", kind: "uses" },
  {
    from: "C9",
    to: "J5",
    label: "Vector infra in data platform",
    kind: "uses",
  },

  // ---- D. Deep Learning cross-links ----
  { from: "D1", to: "D2", label: "Core ⇒ CNNs", kind: "uses" },
  { from: "D1", to: "D3", label: "Core ⇒ sequence models", kind: "uses" },
  {
    from: "D2",
    to: "D3",
    label: "ViT applies Transformer to images",
    kind: "uses",
  },
  { from: "D3", to: "E3", label: "Transformer ⇒ LLMs", kind: "generalizes" },
  {
    from: "D4",
    to: "F5",
    label: "VAEs use variational inference",
    kind: "uses",
  },
  {
    from: "D4",
    to: "F8",
    label: "VAE / Bayesian DL overlap",
    kind: "shared-concept",
  },
  {
    from: "D5",
    to: "E7",
    label: "CLIP bridges vision + language",
    kind: "shared-concept",
  },
  { from: "D6", to: "E6", label: "Graph RAG", kind: "uses" },
  {
    from: "D7",
    to: "E5",
    label: "FlashAttention ⇒ fast inference",
    kind: "uses",
  },
  {
    from: "D7",
    to: "I3",
    label: "Training systems ⇒ deployment",
    kind: "uses",
  },

  // ---- E. NLP / LLMs ----
  { from: "E1", to: "F3", label: "HMM/CRF era of NLP", kind: "shared-concept" },
  {
    from: "E1",
    to: "F7",
    label: "LDA is a latent variable model",
    kind: "shared-concept",
  },
  { from: "E1", to: "E6", label: "BM25 / TF-IDF in RAG", kind: "uses" },
  {
    from: "E3",
    to: "G3",
    label: "Transformers for time series",
    kind: "shared-concept",
  },
  {
    from: "E4",
    to: "H6",
    label: "RLHF / DPO are RL on LMs",
    kind: "shared-concept",
  },
  {
    from: "E5",
    to: "I3",
    label: "LLM serving (vLLM, TGI)",
    kind: "shared-concept",
  },
  {
    from: "E6",
    to: "J1",
    label: "RAG fundamentals overlap",
    kind: "shared-concept",
  },
  { from: "E6", to: "J2", label: "Tool use ↔ MCP", kind: "shared-concept" },
  { from: "E7", to: "D2", label: "Multimodal needs vision", kind: "uses" },
  { from: "E8", to: "I4", label: "Mech interp ⇒ safety evals", kind: "uses" },
  { from: "E8", to: "J7", label: "Interp ⇒ governance", kind: "uses" },

  // ---- F. PGMs ↔ Time Series ----
  {
    from: "F3",
    to: "G1",
    label: "Kalman = state-space TS",
    kind: "shared-concept",
  },
  { from: "F5", to: "F8", label: "VI powers Bayesian DL", kind: "uses" },

  // ---- G. Time Series ↔ DL ----
  {
    from: "G3",
    to: "D3",
    label: "DL forecasting uses sequence models",
    kind: "uses",
  },

  // ---- H. RL ↔ LLMs ----
  { from: "H1", to: "H6", label: "RL foundations ⇒ RLHF", kind: "generalizes" },
  {
    from: "H5",
    to: "J4",
    label: "Multi-agent RL ↔ multi-agent LLM",
    kind: "shared-concept",
  },

  // ---- I. MLOps ↔ AI Engineering ----
  {
    from: "I1",
    to: "J5",
    label: "Data eng ↔ AI data platform",
    kind: "shared-concept",
  },
  {
    from: "I3",
    to: "J3",
    label: "Deployment in production",
    kind: "shared-concept",
  },
  { from: "I3", to: "J6", label: "Cloud AI extends serving", kind: "uses" },
  { from: "I4", to: "J7", label: "Monitoring ⇒ governance", kind: "uses" },

  // ---- J. AI Engineering internal flow ----
  { from: "J1", to: "J2", label: "Fundamentals → systems", kind: "uses" },
  { from: "J2", to: "J3", label: "Systems → production", kind: "uses" },
  {
    from: "J3",
    to: "J4",
    label: "Production → advanced patterns",
    kind: "uses",
  },
  { from: "J3", to: "J5", label: "Production → data platform", kind: "uses" },
  { from: "J5", to: "J6", label: "Data platform → Cloud AI", kind: "uses" },
  { from: "J6", to: "J7", label: "Cloud → architect", kind: "uses" },
];

// -------------------------------------------------------------------------
// PATHS: curated reading sequences across the DAG
// -------------------------------------------------------------------------
// Each path is an ordered list of subsection IDs that threads the DAG for a
// particular learner profile. Rendered in the learning-paths grid.

export const PATHS: Path[] = [
  {
    name: "🎓 LLM Researcher",
    desc: "Classic LLM spine: math → DL → Transformers → alignment.",
    pillars: ["A2", "A3", "D1", "D3", "E3", "E4", "E8", "H6"],
    color: "var(--pe)",
  },
  {
    name: "🛠️ AI Engineer (applied)",
    desc: "The AI Eng Journey roadmap: RAG → MCP → production → cloud.",
    pillars: ["E6", "J1", "J2", "J3", "J4", "J5", "J6", "J7"],
    color: "var(--pj)",
  },
  {
    name: "🤖 AI Agent Engineer",
    desc: "Agentic AI: RAG, tool use, MCP, multi-agent orchestration, and eval design. The fastest-growing 2026 role family.",
    pillars: ["E6", "J1", "J2", "J4", "C10", "E8"],
    color: "var(--ph)",
  },
  {
    name: "🛡️ Responsible AI & Governance",
    desc: "Alignment, evaluation, validation, monitoring, and governance for safe, compliant AI (EU AI Act, NIST AI RMF).",
    pillars: ["E8", "C10", "B3", "I4", "J7"],
    color: "var(--pa)",
  },
  {
    name: "📈 Causal & Experimental DS",
    desc: "Rigorous statistics + causal inference for product decisions.",
    pillars: ["A2", "B1", "B2", "B4", "B5", "G5"],
    color: "var(--pb)",
  },
  {
    name: "🏭 ML Platform / MLOps",
    desc: "Data, distributed training, serving, and monitoring at scale.",
    pillars: ["A5", "D7", "E5", "I1", "I2", "I3", "I4"],
    color: "var(--pi)",
  },
  {
    name: "🔬 Frontier Researcher",
    desc: "★ topics 2023–2025: SSMs, diffusion, SAEs, R1-style RL, MCP.",
    pillars: ["D3", "D4", "D7", "E4", "E6", "E8", "H6", "J2"],
    color: "var(--pf)",
  },
  {
    name: "👁️ Computer Vision",
    desc: "From DL core to CNNs and SAM/NeRF, with crossings to SSL and multimodal.",
    pillars: ["D1", "D2", "D5", "E7"],
    color: "var(--pd)",
  },
  {
    name: "📊 Classical ML / Data Scientist",
    desc: "The canonical starting roadmap: stats foundations → supervised learners (linear, trees, kernels) → unsupervised → ensembles → rigorous evaluation.",
    pillars: ["A2", "B1", "C1", "C3", "C2", "C4", "C5", "C7", "C10"],
    color: "var(--pc)",
  },
];

// -------------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------------

export function getAllSubsections() {
  return PILLARS.flatMap((p) => p.subs.map((s) => ({ ...s, pillar: p })));
}

export function getSubsectionById(id: string) {
  for (const p of PILLARS) {
    const s = p.subs.find((s) => s.id === id);
    if (s) return { ...s, pillar: p };
  }
  return undefined;
}

export function pillarStats(p: Pillar) {
  const all = p.subs.flatMap((s) => s.topics);
  const cov = all.filter((t) => t.status === "covered").length;
  const par = all.filter((t) => t.status === "partial").length;
  const gap = all.filter((t) => t.status === "gap").length;
  const hot = all.filter((t) => t.hot).length;
  const total = all.length || 1;
  return {
    total,
    cov,
    par,
    gap,
    hot,
    pctCov: (cov / total) * 100,
    pctPar: (par / total) * 100,
    pctGap: (gap / total) * 100,
    pctOverall: Math.round(((cov + par * 0.5) / total) * 100),
  };
}

export function globalStats() {
  const all = PILLARS.flatMap((p) => p.subs.flatMap((s) => s.topics));
  return {
    total: all.length,
    cov: all.filter((t) => t.status === "covered").length,
    par: all.filter((t) => t.status === "partial").length,
    gap: all.filter((t) => t.status === "gap").length,
    hot: all.filter((t) => t.hot).length,
    hotGap: all.filter((t) => t.hot && t.status === "gap").length,
    nPillars: PILLARS.length,
    nSubsections: PILLARS.reduce((n, p) => n + p.subs.length, 0),
    nConnections: CONNECTIONS.length,
  };
}
