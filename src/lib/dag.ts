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
    subs: [
      {
        id: "A1",
        name: "Linear algebra",
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
        topics: [
          { name: "Numerical stability (log-sum-exp)", status: "covered" },
          { name: "Iterative solvers (CG, GMRES)", status: "gap" },
          { name: "Mixed-precision arithmetic", status: "gap", hot: true },
        ],
      },
      {
        id: "A5",
        name: "Data structures & algorithms",
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
    subs: [
      {
        id: "B1",
        name: "Frequentist inference",
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
        topics: [
          { name: "Bootstrap, jackknife", status: "gap" },
          { name: "Permutation tests", status: "gap" },
          { name: "Cross-validation strategies", status: "gap" },
        ],
      },
      {
        id: "B4",
        name: "Experimental design",
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
    subs: [
      {
        id: "C1",
        name: "Linear & GLMs",
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
        topics: [
          { name: "Support Vector Machines", status: "gap" },
          { name: "Kernel trick & RKHS", status: "gap" },
          { name: "Gaussian processes", status: "gap" },
        ],
      },
      {
        id: "C3",
        name: "Tree-based methods",
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
        topics: [
          { name: "k-NN", status: "gap" },
          { name: "Naive Bayes", status: "gap" },
          { name: "LDA / QDA", status: "gap" },
        ],
      },
      {
        id: "C5",
        name: "Unsupervised learning",
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
        topics: [
          { name: "Isolation Forest", status: "gap" },
          { name: "One-class SVM", status: "gap" },
          { name: "Autoencoder-based AD", status: "gap" },
        ],
      },
      {
        id: "C7",
        name: "Ensembles",
        topics: [
          { name: "Bagging, boosting, stacking", status: "gap" },
          { name: "AutoML platforms", status: "gap", hot: true },
        ],
      },
      {
        id: "C8",
        name: "Recommendation systems",
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
    subs: [
      {
        id: "D1",
        name: "Core building blocks",
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
    tagline: "Tokenization, LLMs, alignment, agents: espinha do AI ML Theory",
    color: "#bb9af7",
    subs: [
      {
        id: "E1",
        name: "Classical NLP",
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
    subs: [
      {
        id: "F1",
        name: "Directed models",
        topics: [
          { name: "Bayesian networks", status: "gap" },
          { name: "Plate notation", status: "gap" },
          { name: "d-separation", status: "gap" },
        ],
      },
      {
        id: "F2",
        name: "Undirected models",
        topics: [
          { name: "Markov random fields", status: "gap" },
          { name: "Conditional random fields (CRF)", status: "gap" },
          { name: "Factor graphs", status: "gap" },
        ],
      },
      {
        id: "F3",
        name: "Temporal graphical models",
        topics: [
          { name: "Hidden Markov Models (HMM)", status: "gap" },
          { name: "Kalman & extended Kalman filters", status: "gap" },
          { name: "Particle filters / sequential MC", status: "gap" },
        ],
      },
      {
        id: "F4",
        name: "Exact inference",
        topics: [
          { name: "Variable elimination", status: "gap" },
          { name: "Belief propagation", status: "gap" },
          { name: "Junction tree", status: "gap" },
        ],
      },
      {
        id: "F5",
        name: "Approximate inference",
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
        topics: [
          { name: "EM algorithm", status: "gap" },
          { name: "LDA topic model", status: "gap" },
          { name: "Probabilistic PCA, factor analysis", status: "gap" },
        ],
      },
      {
        id: "F8",
        name: "Modern Bayesian DL",
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
    subs: [
      {
        id: "G1",
        name: "Classical statistical TS",
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
        topics: [
          { name: "Statistical (IQR, ESD, CUSUM)", status: "gap" },
          { name: "Deep AD (LSTM-AE, Transformer-AE)", status: "gap" },
        ],
      },
      {
        id: "G5",
        name: "Causal time series",
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
    subs: [
      {
        id: "H1",
        name: "RL foundations",
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
        topics: [
          { name: "Dyna-Q, planning", status: "gap" },
          { name: "MuZero, AlphaZero", status: "gap", hot: true },
          { name: "World models (Dreamer)", status: "gap", hot: true },
        ],
      },
      {
        id: "H4",
        name: "Exploration",
        topics: [
          { name: "ε-greedy, UCB, Thompson sampling", status: "gap" },
          { name: "Intrinsic motivation, RND", status: "gap" },
        ],
      },
      {
        id: "H5",
        name: "Beyond standard RL",
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
    subs: [
      {
        id: "I1",
        name: "Data engineering",
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
        topics: [
          { name: "Experiment tracking (W&B, MLflow)", status: "gap" },
          { name: "HPO orchestration (Optuna, Ray Tune)", status: "gap" },
          { name: "Distributed orchestrators (Ray, DeepSpeed)", status: "gap" },
        ],
      },
      {
        id: "I3",
        name: "Deployment & serving",
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
    subs: [
      {
        id: "J1",
        name: "Fundamentos (RAG, tool_use, agentes)",
        topics: [
          { name: "RAG do zero (pypdf, ChromaDB, embeddings)", status: "gap" },
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
        name: "Pensamento de sistemas",
        topics: [
          {
            name: "MCP: protocol, servers, integrations",
            status: "gap",
            hot: true,
          },
          {
            name: "Desenhar um servidor MCP (granularidade, versionamento)",
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
        name: "Data platform para IA",
        topics: [
          { name: "dbt em profundidade", status: "gap" },
          { name: "Orchestration (Dagster or Airflow)", status: "gap" },
          { name: "Data contracts", status: "gap" },
          {
            name: "Vector infra em escala (pgvector × managed)",
            status: "gap",
            hot: true,
          },
          {
            name: "Hybrid search, embedding lifecycle",
            status: "gap",
            hot: true,
          },
          {
            name: "Event-driven & streaming para IA (Kafka, CDC)",
            status: "gap",
          },
          { name: "Feature stores & embedding stores (Feast)", status: "gap" },
        ],
      },
      {
        id: "J6",
        name: "Cloud AI & enterprise integration",
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
            name: "Cost & FinOps para IA (caching tiers, reserved capacity)",
            status: "gap",
            hot: true,
          },
        ],
      },
      {
        id: "J7",
        name: "Skills de arquiteto",
        topics: [
          { name: "AI governance (LGPD/GDPR para sistemas IA)", status: "gap" },
          {
            name: "Red teaming, prompt injection em escala",
            status: "gap",
            hot: true,
          },
          { name: "Reference architectures, ADRs, C4 diagrams", status: "gap" },
          {
            name: "System design para IA (architect-interview style)",
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
  { from: "J1", to: "J2", label: "Fundamentos → sistemas", kind: "uses" },
  { from: "J2", to: "J3", label: "Systems → production", kind: "uses" },
  {
    from: "J3",
    to: "J4",
    label: "Production → advanced patterns",
    kind: "uses",
  },
  { from: "J3", to: "J5", label: "Production → data platform", kind: "uses" },
  { from: "J5", to: "J6", label: "Data platform → Cloud AI", kind: "uses" },
  { from: "J6", to: "J7", label: "Cloud → arquiteto", kind: "uses" },
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
    desc: "From CNNs to SAM/NeRF, with crossings to SSL and multimodal.",
    pillars: ["D2", "D5", "E7"],
    color: "var(--pd)",
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
