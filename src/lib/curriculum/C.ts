import type { Lesson } from "@/lib/types";

/**
 * Pillar C: Classical Machine Learning. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 */
export const C_CURRICULUM: Record<string, Lesson[]> = {
  C1: [
    {
      id: "linear-regression-ols",
      title: "Linear regression and OLS",
      goal: "Set up linear regression, derive the OLS estimator from the normal equations, and read it as projection onto the column space.",
      prerequisites: ["A1/least-squares"],
    },
    {
      id: "linear-regression-mle",
      title: "Linear regression as maximum likelihood",
      goal: "Show that OLS is the MLE under Gaussian noise, and recover the noise variance from the residuals.",
      prerequisites: ["linear-regression-ols", "A2/mle"],
    },
    {
      id: "bias-variance",
      title: "Bias-variance decomposition",
      goal: "Decompose expected squared error into bias, variance, and noise, and read it as the central tradeoff of every estimator.",
      prerequisites: ["linear-regression-mle"],
    },
    {
      id: "ridge-regression",
      title: "Ridge regression",
      goal: "Add an L2 penalty, derive the closed-form solution, and see why ridge shrinks small singular directions the most.",
      prerequisites: ["linear-regression-ols", "bias-variance"],
    },
    {
      id: "lasso",
      title: "LASSO and L1 regularization",
      goal: "Solve the LASSO with proximal gradient (soft-thresholding) and explain why L1 produces sparse coefficients.",
      prerequisites: ["ridge-regression", "A3/proximal-methods"],
    },
    {
      id: "elastic-net",
      title: "Elastic net",
      goal: "Combine L1 and L2 to get sparsity with correlated-feature stability.",
      prerequisites: ["lasso"],
    },
    {
      id: "logistic-regression",
      title: "Logistic regression",
      goal: "Build logistic regression from log-odds, write its log-likelihood, and fit it with IRLS or gradient descent.",
      prerequisites: ["A2/mle", "A2/exponential-family"],
    },
    {
      id: "softmax-regression",
      title: "Softmax regression",
      goal: "Generalize logistic regression to multiple classes via the softmax and the cross-entropy loss.",
      prerequisites: ["logistic-regression", "A2/kl-cross-entropy"],
    },
    {
      id: "glm-framework",
      title: "Generalized linear models",
      goal: "Wrap linear regression, logistic regression, and Poisson regression into one exponential-family framework with link functions.",
      prerequisites: ["softmax-regression", "A2/exponential-family"],
    },
    {
      id: "poisson-gamma-glm",
      title: "Poisson and Gamma GLMs",
      goal: "Use Poisson regression for counts and Gamma regression for positive continuous durations.",
      prerequisites: ["glm-framework"],
    },
  ],
  C2: [
    {
      id: "perceptron",
      title: "The perceptron",
      goal: "Run the perceptron update rule and prove convergence on linearly separable data with Novikoff's theorem.",
    },
    {
      id: "hard-margin-svm",
      title: "Hard-margin SVM",
      goal: "Define the geometric margin and derive the hard-margin SVM as a quadratic program.",
      prerequisites: ["perceptron", "A3/kkt"],
    },
    {
      id: "soft-margin-svm",
      title: "Soft-margin SVM and hinge loss",
      goal: "Relax separability with slack variables, get the hinge-loss primal, and tune the regularization C.",
      prerequisites: ["hard-margin-svm"],
    },
    {
      id: "svm-dual",
      title: "The SVM dual and support vectors",
      goal: "Form the SVM dual, identify support vectors via complementary slackness, and read sparsity off KKT.",
      prerequisites: ["soft-margin-svm", "A3/duality"],
    },
    {
      id: "kernel-trick",
      title: "The kernel trick",
      goal: "Replace inner products with a Mercer kernel and lift learning into an implicit feature space.",
      prerequisites: ["svm-dual"],
    },
    {
      id: "common-kernels",
      title: "RBF, polynomial, and string kernels",
      goal: "Build the workhorse kernels, understand their hyperparameters, and combine them with sum/product rules.",
      prerequisites: ["kernel-trick"],
    },
    {
      id: "gaussian-processes",
      title: "Gaussian process regression",
      goal: "Treat the function as a draw from a GP prior, condition on data, and get closed-form posterior mean and variance.",
      prerequisites: ["common-kernels", "A2/map-conjugate"],
    },
  ],
  C3: [
    {
      id: "decision-trees",
      title: "Decision trees",
      goal: "Build a decision tree by recursive partitioning and read predictions off its leaves.",
    },
    {
      id: "impurity-criteria",
      title: "Impurity criteria and splits",
      goal: "Choose splits with Gini, entropy, or MSE; understand information gain and overfitting on noisy data.",
      prerequisites: ["decision-trees", "A2/entropy"],
    },
    {
      id: "tree-pruning",
      title: "Pruning and regularizing trees",
      goal: "Control depth, leaf size, and cost-complexity pruning to keep trees from memorizing the training set.",
      prerequisites: ["impurity-criteria"],
    },
    {
      id: "bagging-rf",
      title: "Bagging and random forests",
      goal: "Average bootstrap replicas to reduce variance, and decorrelate trees with random feature subsets.",
      prerequisites: ["tree-pruning", "C1/bias-variance"],
    },
    {
      id: "feature-importance",
      title: "Tree feature importance",
      goal: "Compare Gini-impurity importance against permutation importance and know when each lies.",
      prerequisites: ["bagging-rf"],
    },
    {
      id: "adaboost",
      title: "AdaBoost",
      goal: "Reweight examples each round to focus on mistakes, and derive the exponential-loss view of AdaBoost.",
      prerequisites: ["impurity-criteria"],
    },
    {
      id: "gradient-boosting",
      title: "Gradient boosting",
      goal: "Frame boosting as functional gradient descent in loss space and fit trees to negative gradients.",
      prerequisites: ["adaboost", "A3/gradient-descent"],
    },
    {
      id: "xgboost-lightgbm",
      title: "XGBoost and LightGBM",
      goal: "Add second-order information, regularized objectives, and histogram splits to make boosting fast and accurate.",
      prerequisites: ["gradient-boosting"],
    },
  ],
  C4: [
    {
      id: "knn",
      title: "k-nearest neighbors",
      goal: "Predict by majority vote (classification) or average (regression) over the k closest points, and choose k by cross-validation.",
    },
    {
      id: "curse-of-dimensionality",
      title: "Distance metrics and the curse of dimensionality",
      goal: "See how nearest-neighbor methods degrade as dimension grows and pick metrics that respect the data.",
      prerequisites: ["knn", "A1/norms"],
    },
    {
      id: "naive-bayes",
      title: "Naive Bayes",
      goal: "Assume conditional independence of features given the class, fit class-conditional models, and classify via Bayes' rule.",
      prerequisites: ["A2/bayes-rule"],
    },
    {
      id: "lda-qda",
      title: "Linear and quadratic discriminant analysis",
      goal: "Model classes as Gaussians (shared or per-class covariance) and derive linear vs quadratic decision boundaries.",
      prerequisites: ["naive-bayes", "A2/common-distributions"],
    },
    {
      id: "fisher-lda",
      title: "Fisher's LDA as projection",
      goal: "Project data to maximize between-class variance over within-class variance, the supervised twin of PCA.",
      prerequisites: ["lda-qda", "A1/eigenvalues"],
    },
  ],
  C5: [
    {
      id: "kmeans",
      title: "k-means clustering",
      goal: "Run Lloyd's algorithm and see it as alternating minimization of the within-cluster sum of squares.",
    },
    {
      id: "kmeans-init-and-k",
      title: "k-means++ and choosing k",
      goal: "Use k-means++ for a smarter initialization and pick k with the elbow method or silhouette score.",
      prerequisites: ["kmeans"],
    },
    {
      id: "kmedoids",
      title: "k-medoids and robust centers",
      goal: "Swap means for actual data points to handle non-Euclidean distances and outliers.",
      prerequisites: ["kmeans"],
    },
    {
      id: "dbscan",
      title: "DBSCAN",
      goal: "Define clusters as dense, connected regions, separate noise points, and pick eps from a k-distance plot.",
      prerequisites: ["kmeans"],
    },
    {
      id: "hdbscan",
      title: "HDBSCAN",
      goal: "Build a hierarchy of DBSCAN clusterings and extract a flat clustering that adapts to varying density.",
      prerequisites: ["dbscan"],
    },
    {
      id: "hierarchical-clustering",
      title: "Hierarchical clustering",
      goal: "Build dendrograms with single, complete, average, and Ward linkage; read them at a chosen cut.",
    },
    {
      id: "gmm-em",
      title: "Gaussian mixture models and EM",
      goal: "Fit a mixture of Gaussians with the EM algorithm and interpret it as soft k-means with covariances.",
      prerequisites: ["kmeans", "A2/mle"],
    },
    {
      id: "tsne-umap",
      title: "t-SNE and UMAP",
      goal: "Use neighborhood-preserving methods to visualize high-dimensional structure, and know their failure modes.",
      prerequisites: ["A1/low-rank-pca"],
    },
  ],
  C6: [
    {
      id: "statistical-ad",
      title: "Statistical anomaly detection",
      goal: "Flag points beyond IQR, ESD, or CUSUM thresholds, the simplest and most defensible AD baselines.",
      prerequisites: ["A2/inequalities"],
    },
    {
      id: "isolation-forest",
      title: "Isolation Forest",
      goal: "Build randomized trees whose path length isolates anomalies in few splits, with no distance metric needed.",
      prerequisites: ["C3/bagging-rf"],
    },
    {
      id: "one-class-svm",
      title: "One-class SVM",
      goal: "Carve out a small region containing most of the data with a kernel SVM, and use the boundary as a novelty detector.",
      prerequisites: ["C2/kernel-trick"],
    },
    {
      id: "autoencoder-ad",
      title: "Autoencoder-based anomaly detection",
      goal: "Train a reconstruction model on normal data and flag points whose reconstruction error exceeds a threshold.",
      prerequisites: ["A1/low-rank-pca"],
    },
  ],
  C7: [
    {
      id: "ensemble-theory",
      title: "Why ensembles work",
      goal: "Show how bagging reduces variance and boosting reduces bias, and see correlated errors as the failure mode.",
      prerequisites: ["C1/bias-variance", "C3/bagging-rf"],
    },
    {
      id: "stacking",
      title: "Stacking and blending",
      goal: "Train a meta-learner on out-of-fold predictions to combine heterogeneous base models.",
      prerequisites: ["ensemble-theory"],
    },
    {
      id: "snapshot-and-voting",
      title: "Snapshot ensembles and voting",
      goal: "Average models cheaply via snapshots, hard/soft voting, and rank averaging.",
      prerequisites: ["ensemble-theory"],
    },
    {
      id: "automl",
      title: "AutoML platforms",
      goal: "Survey AutoML systems and the search problem they solve over pipelines and hyperparameters.",
      prerequisites: ["A3/bayesian-optimization"],
    },
  ],
  C8: [
    {
      id: "collaborative-filtering",
      title: "Collaborative filtering",
      goal: "Recommend items by item-item or user-user neighborhoods over the rating matrix.",
    },
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
      id: "two-tower",
      title: "Two-tower and neural collaborative filtering",
      goal: "Embed users and items with neural nets and score with a dot product, the basis of modern retrieval.",
      prerequisites: ["matrix-factorization"],
    },
    {
      id: "sequential-rec",
      title: "Sequential recommendation",
      goal: "Model user histories as sequences (SASRec, BERT4Rec) and predict the next item.",
      prerequisites: ["two-tower"],
    },
  ],
  C9: [
    {
      id: "ann-problem",
      title: "The approximate nearest neighbor problem",
      goal: "State the ANN problem, see why exact NN is infeasible at scale, and define recall@k.",
      prerequisites: ["C4/curse-of-dimensionality"],
    },
    {
      id: "lsh",
      title: "Locality-sensitive hashing",
      goal: "Hash similar points to the same bucket with high probability, with MinHash for Jaccard and SimHash for cosine.",
      prerequisites: ["ann-problem"],
    },
    {
      id: "ivf-pq",
      title: "IVF and product quantization",
      goal: "Partition the space with coarse clusters and compress residuals with product quantization for billion-scale search.",
      prerequisites: ["ann-problem", "C5/kmeans"],
    },
    {
      id: "hnsw",
      title: "HNSW graph index",
      goal: "Build a hierarchical small-world graph that supports logarithmic-time greedy search.",
      prerequisites: ["ann-problem"],
    },
    {
      id: "vector-databases",
      title: "Vector databases",
      goal: "Compare FAISS, pgvector, and managed vector DBs along recall, throughput, and operational cost.",
      prerequisites: ["hnsw", "ivf-pq"],
    },
  ],
  C10: [
    {
      id: "classification-metrics",
      title: "Classification metrics",
      goal: "Define precision, recall, F1, ROC curves, and AUC; choose the metric that matches the cost structure.",
    },
    {
      id: "regression-metrics",
      title: "Regression metrics",
      goal: "Compare MSE, MAE, R^2, MAPE, and quantile losses, and know when each one misleads.",
    },
    {
      id: "calibration",
      title: "Probability calibration",
      goal: "Use reliability diagrams and Brier scores, and recalibrate with Platt scaling and isotonic regression.",
      prerequisites: ["classification-metrics", "C1/logistic-regression"],
    },
    {
      id: "cv-strategies",
      title: "Cross-validation strategies",
      goal: "Pick k-fold, stratified, group, or time-series CV based on what the test distribution actually looks like.",
    },
    {
      id: "hpo",
      title: "Hyperparameter optimization",
      goal: "Search hyperparameter space with grid, random, and Bayesian methods; understand the bias/variance of the search itself.",
      prerequisites: ["cv-strategies", "A3/bayesian-optimization"],
    },
    {
      id: "learning-curves",
      title: "Learning and validation curves",
      goal: "Diagnose bias vs variance from training/validation curves over sample size and model complexity.",
      prerequisites: ["C1/bias-variance"],
    },
  ],
};
