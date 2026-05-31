import type { Lesson } from "@/lib/types";

/**
 * Pillar F: Probabilistic Graphical Models. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 */
export const F_CURRICULUM: Record<string, Lesson[]> = {
  F1: [
    {
      id: "bayesian-networks",
      title: "Bayesian networks and the joint factorization",
      goal: "Factor a joint distribution over a DAG, read local Markov independence from parent sets, and compute exact probabilities from conditional probability tables.",
      prerequisites: ["A2/bayes-rule", "A2/mle"],
    },
    {
      id: "plate-notation",
      title: "Plate notation for repeated variables",
      goal: "Use plate diagrams to compactly represent models with i.i.d. replication, and translate a plate diagram into its full joint factorization.",
      prerequisites: ["bayesian-networks"],
    },
    {
      id: "d-separation",
      title: "d-separation and conditional independence",
      goal: "Identify the three canonical motifs (chain, fork, collider) and apply the Bayes-ball algorithm to determine which pairs of variables are d-separated given an observation set.",
      prerequisites: ["bayesian-networks"],
    },
  ],
  F2: [
    {
      id: "markov-random-fields",
      title: "Markov random fields and the Gibbs distribution",
      goal: "Represent a joint distribution as a Gibbs distribution over clique potentials, identify Markov blankets from graph structure, and state the Hammersley-Clifford theorem.",
      prerequisites: ["F1/bayesian-networks", "A2/bayes-rule"],
    },
    {
      id: "conditional-random-fields",
      title: "Conditional random fields for structured prediction",
      goal: "Formulate a linear-chain CRF as a discriminative log-linear model over sequences, derive the partition function, and contrast CRFs with generative HMMs.",
      prerequisites: ["markov-random-fields"],
    },
    {
      id: "factor-graphs",
      title: "Factor graphs: a unified representation",
      goal: "Convert any directed or undirected graphical model to a factor graph, and express the sum-product algorithm as message passing on the bipartite factor-variable graph.",
      prerequisites: ["markov-random-fields", "F1/d-separation"],
    },
  ],
  F3: [
    {
      id: "hidden-markov-models",
      title: "Hidden Markov models: forward-backward and Viterbi",
      goal: "Derive the forward-backward algorithm for marginal state posteriors and the Viterbi algorithm for the MAP sequence in an HMM.",
      prerequisites: ["F1/bayesian-networks", "A2/bayes-rule"],
    },
    {
      id: "kalman-filter",
      title: "The Kalman filter for linear-Gaussian state space",
      goal: "Derive the Kalman predict-update recursion by applying Bayes' rule to a linear-Gaussian state-space model, and compute the Kalman gain in closed form.",
      prerequisites: ["hidden-markov-models"],
    },
    {
      id: "particle-filters",
      title: "Particle filters and sequential Monte Carlo",
      goal: "Implement sequential importance resampling (SIR) to approximate a non-Gaussian filtering distribution, and explain why systematic resampling controls weight degeneracy.",
      prerequisites: ["kalman-filter", "F6/rejection-importance-sampling"],
    },
  ],
  F4: [
    {
      id: "variable-elimination",
      title: "Variable elimination for exact marginals",
      goal: "Execute variable elimination on a small graphical model, derive the complexity in terms of elimination order, and identify the treewidth as the bottleneck.",
      prerequisites: ["F2/factor-graphs"],
    },
    {
      id: "belief-propagation",
      title: "Belief propagation and the sum-product algorithm",
      goal: "Derive the BP message-update equations from first principles on a tree, show they return exact marginals in one pass, and explain why loopy BP is only approximate.",
      prerequisites: ["variable-elimination"],
    },
    {
      id: "junction-tree",
      title: "The junction tree algorithm",
      goal: "Triangulate a graph, build its clique tree, verify the running intersection property, and perform exact inference via the calibration (collect-distribute) schedule.",
      prerequisites: ["belief-propagation"],
    },
  ],
  F5: [
    {
      id: "mean-field-vi",
      title: "Mean-field variational inference and the ELBO",
      goal: "Derive the evidence lower bound (ELBO) via Jensen's inequality, write the mean-field factorization, and derive the coordinate ascent VI (CAVI) update for each factor.",
      prerequisites: [
        "F1/bayesian-networks",
        "B2/prior-likelihood-posterior",
        "A2/kl-cross-entropy",
      ],
    },
    {
      id: "stochastic-vi",
      title: "Stochastic variational inference",
      goal: "Derive the mini-batch ELBO estimator, apply the reparameterization trick to obtain low-variance gradient estimates, and contrast it with the score-function estimator.",
      prerequisites: ["mean-field-vi"],
    },
    {
      id: "amortized-vi",
      title: "Amortized variational inference and encoder networks",
      goal: "Replace per-datapoint variational parameters with a shared encoder network, derive the amortized ELBO objective, and identify the trade-off between flexibility and amortization gap.",
      prerequisites: ["stochastic-vi"],
    },
    {
      id: "normalizing-flow-posteriors",
      title: "Normalizing flows as variational posteriors",
      goal: "Apply the change-of-variables formula for flows to express the log-density of a transformed variable, incorporate a flow posterior into the ELBO, and implement a simple planar flow.",
      prerequisites: ["amortized-vi", "A2/change-of-variables"],
    },
  ],
  F6: [
    {
      id: "rejection-importance-sampling",
      title: "Rejection and importance sampling",
      goal: "Derive the acceptance probability for rejection sampling from an envelope distribution, derive the importance weights for importance sampling, and compute the effective sample size.",
      prerequisites: ["A2/bayes-rule", "A2/mle"],
    },
    {
      id: "metropolis-hastings",
      title: "The Metropolis-Hastings algorithm",
      goal: "Derive the detailed balance condition, construct the MH acceptance ratio, prove that the chain's stationary distribution is the target, and diagnose mixing with trace plots.",
      prerequisites: ["rejection-importance-sampling"],
    },
    {
      id: "gibbs-sampling",
      title: "Gibbs sampling",
      goal: "Derive Gibbs updates as a special case of Metropolis-Hastings using full conditional distributions, implement a Gibbs sampler for a bivariate Gaussian, and identify when full conditionals are tractable.",
      prerequisites: ["metropolis-hastings"],
    },
    {
      id: "hamiltonian-mc",
      title: "Hamiltonian Monte Carlo and NUTS",
      goal: "Frame MCMC proposals as Hamiltonian dynamics, derive the leapfrog integrator, show that the volume-preserving property keeps acceptance high, and explain what NUTS adds.",
      prerequisites: ["gibbs-sampling"],
    },
    {
      id: "langevin-sgld",
      title: "Langevin dynamics and SGLD",
      goal: "Derive the unadjusted Langevin algorithm from overdamped Langevin diffusion, apply stochastic gradient noise to obtain SGLD, and interpret SGLD as approximate Bayesian posterior sampling.",
      prerequisites: ["hamiltonian-mc"],
    },
  ],
  F7: [
    {
      id: "em-algorithm",
      title: "The EM algorithm for maximum marginal likelihood",
      goal: "Derive the E-step and M-step from the ELBO lower bound on the marginal log-likelihood, prove the monotone increase property, and apply EM to a Gaussian mixture model.",
      prerequisites: ["F5/mean-field-vi", "A2/mle"],
    },
    {
      id: "lda-topic-model",
      title: "Latent Dirichlet Allocation",
      goal: "Describe the LDA generative process, derive the collapsed Gibbs sampling update for topic assignments, and interpret the Dirichlet hyperparameters as document and topic concentration.",
      prerequisites: ["em-algorithm", "A2/exponential-family"],
    },
    {
      id: "probabilistic-pca",
      title: "Probabilistic PCA and factor analysis",
      goal: "Derive the maximum-likelihood solution for the PPCA loading matrix showing it recovers the top principal components, formulate the EM update, and explain how factor analysis generalizes PPCA with heteroscedastic noise.",
      prerequisites: ["em-algorithm", "A1/low-rank-pca"],
    },
  ],
  F8: [
    {
      id: "vae-reparameterization",
      title: "Variational autoencoders and the reparameterization trick",
      goal: "Derive the VAE objective as an amortized ELBO, apply the reparameterization trick to pass gradients through a stochastic latent variable, and identify the KL term as a regularizer on the latent code.",
      prerequisites: ["F5/amortized-vi", "A2/kl-cross-entropy"],
    },
    {
      id: "mc-dropout-ensembles",
      title: "MC dropout and deep ensembles",
      goal: "Interpret MC dropout as approximate Bayesian inference, decompose predictive uncertainty into epistemic and aleatoric components, and contrast the diversity mechanisms in dropout vs. deep ensembles.",
      prerequisites: ["vae-reparameterization"],
    },
    {
      id: "bayesian-neural-networks",
      title: "Bayesian neural networks",
      goal: "Place a prior over network weights, derive the Laplace approximation to the posterior, and formulate the mean-field variational objective for BNNs.",
      prerequisites: ["mc-dropout-ensembles", "F5/mean-field-vi"],
    },
    {
      id: "conformal-prediction",
      title: "Conformal prediction and coverage guarantees",
      goal: "Derive the split-conformal prediction interval, prove the finite-sample marginal coverage guarantee under exchangeability, and implement it for regression and classification.",
      prerequisites: ["bayesian-neural-networks"],
    },
  ],
};
