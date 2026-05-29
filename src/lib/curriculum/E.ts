import type { Lesson } from "@/lib/types";

/**
 * Pillar E: NLP & Language Models. Ordered lesson curriculum per subsection.
 * Lesson order is the array order; prerequisites are bare ids within the same
 * subsection or "subId/lessonId" across subsections.
 */
export const E_CURRICULUM: Record<string, Lesson[]> = {
  E1: [
    {
      id: "ngram-lm",
      title: "N-gram language models",
      goal: "Derive the Markov n-gram approximation, build an MLE bigram table by counting, and compute sentence probabilities.",
      prerequisites: [],
    },
    {
      id: "smoothing",
      title: "Smoothing and back-off",
      goal: "Fix zero-probability n-grams with Laplace add-one and Kneser-Ney interpolation, and measure the improvement with perplexity.",
      prerequisites: ["ngram-lm"],
    },
    {
      id: "tokenization",
      title: "Subword tokenization: BPE, WordPiece, SentencePiece",
      goal: "Implement BPE merge training on a toy corpus and encode a new word at inference; contrast WordPiece likelihood and SentencePiece unigram variants.",
      prerequisites: ["ngram-lm"],
    },
    {
      id: "hmm-pos-ner",
      title: "HMM for POS tagging and NER",
      goal: "Define a first-order HMM with emission and transition matrices, run Viterbi decoding on a short sentence, and connect it to POS/NER sequence labeling.",
      prerequisites: ["ngram-lm"],
    },
    {
      id: "crf",
      title: "Conditional random fields",
      goal: "Replace the HMM generative assumptions with a discriminative linear-chain CRF; derive the forward algorithm for the partition function and the Viterbi path for decoding.",
      prerequisites: ["hmm-pos-ner"],
    },
    {
      id: "topic-models",
      title: "Topic models: LDA and NMF",
      goal: "Build LDA's plate model, understand Gibbs sampling as the inference engine, and use NMF as a deterministic matrix-factorization alternative.",
      prerequisites: [],
    },
    {
      id: "ir-tfidf-bm25",
      title: "Information retrieval: TF-IDF and BM25",
      goal: "Derive TF-IDF from information-theoretic first principles, then improve it with BM25's saturation and length normalization; implement a tiny inverted index.",
      prerequisites: [],
    },
  ],

  E2: [
    {
      id: "word2vec",
      title: "Word2vec: CBOW and skip-gram",
      goal: "Train word vectors with the skip-gram negative-sampling objective; see why nearby tokens share embedding space and how analogies emerge.",
      prerequisites: ["E1/ngram-lm"],
    },
    {
      id: "glove-fasttext",
      title: "GloVe and fastText",
      goal: "Derive GloVe's log-bilinear objective from the co-occurrence ratio, and add fastText's subword composition to handle morphology and OOV.",
      prerequisites: ["word2vec"],
    },
    {
      id: "rnn-lm",
      title: "RNN language models and BPTT",
      goal: "Unroll an RNN as a computational graph, derive backpropagation through time (BPTT), and quantify the vanishing-gradient problem.",
      prerequisites: ["word2vec", "D1/backprop"],
    },
    {
      id: "lstm-gru",
      title: "LSTM and GRU",
      goal: "Build an LSTM cell gate-by-gate; show how the constant error carousel defeats vanishing gradients; then simplify to the GRU.",
      prerequisites: ["rnn-lm"],
    },
    {
      id: "elmo",
      title: "ELMo and contextual embeddings",
      goal: "Train a bidirectional language model and extract ELMo representations as a weighted sum of layer activations; contrast with static word2vec.",
      prerequisites: ["lstm-gru"],
    },
    {
      id: "seq2seq",
      title: "Seq2seq with Bahdanau attention",
      goal: "Build an encoder-decoder seq2seq model and add the Bahdanau additive attention mechanism; visualize the attention matrix on a toy translation.",
      prerequisites: ["lstm-gru"],
    },
  ],

  E3: [
    {
      id: "self-attention",
      title: "Scaled dot-product attention",
      goal: "Derive the query-key-value soft lookup, show why 1/sqrt(d_k) scaling is necessary, and implement a single attention head in numpy.",
      prerequisites: ["E2/seq2seq"],
    },
    {
      id: "multi-head-attention",
      title: "Multi-head attention",
      goal: "Project queries, keys, and values into h parallel subspaces, run h attention heads, and concatenate; show that heads learn complementary patterns.",
      prerequisites: ["self-attention"],
    },
    {
      id: "transformer-block",
      title: "The transformer block",
      goal: "Assemble multi-head attention, position-wise FFN, residual connections, and layer norm into one transformer block, and trace the tensor shapes through a full forward pass.",
      prerequisites: ["multi-head-attention"],
    },
    {
      id: "positional-encodings",
      title: "Positional encodings: sinusoidal, RoPE, ALiBi",
      goal: "Show why attention is position-agnostic, add sinusoidal absolute encodings, and upgrade to rotary (RoPE) and length-extrapolating (ALiBi) schemes.",
      prerequisites: ["transformer-block"],
    },
    {
      id: "decoder-only",
      title: "Decoder-only transformers: the GPT family",
      goal: "Trace a decoder-only language model from token ids to next-token logits through causal masking, and walk through GPT-2's parameter counts.",
      prerequisites: ["positional-encodings"],
    },
    {
      id: "encoder-only",
      title: "Encoder-only transformers: BERT and RoBERTa",
      goal: "Replace causal masking with bidirectional attention, train with masked language modeling and next-sentence prediction, and fine-tune a BERT head.",
      prerequisites: ["decoder-only"],
    },
    {
      id: "encoder-decoder",
      title: "Encoder-decoder transformers: T5 and BART",
      goal: "Add cross-attention between encoder and decoder stacks; frame every NLP task as text-to-text (T5) and see how BART adds denoising pretraining.",
      prerequisites: ["decoder-only", "encoder-only"],
    },
    {
      id: "gqa-moe",
      title: "GQA, MQA, and Mixture of Experts",
      goal: "Reduce KV-cache memory with grouped-query and multi-query attention; then sparsify depth with mixture-of-experts routing (top-k gating).",
      prerequisites: ["decoder-only"],
    },
  ],

  E4: [
    {
      id: "pretraining-data",
      title: "Pretraining data curation",
      goal: "Survey the pipeline that turns raw web crawls into a clean pretraining corpus: quality filtering, deduplication, domain mixing, and data curricula.",
      prerequisites: ["E3/decoder-only"],
      codeExempt: true,
    },
    {
      id: "scaling-laws",
      title: "Scaling laws: Kaplan and Chinchilla",
      goal: "Read Kaplan et al.'s power-law fits (loss vs parameters and tokens), then Chinchilla's correction: for a fixed compute budget, model size and token count should scale equally.",
      prerequisites: ["pretraining-data"],
      codeExempt: true,
    },
    {
      id: "sft",
      title: "Supervised fine-tuning",
      goal: "Convert a pretrained LLM into an instruction follower by fine-tuning on human-written (prompt, completion) pairs using a cross-entropy objective.",
      prerequisites: ["pretraining-data"],
    },
    {
      id: "reward-modeling",
      title: "Reward modeling and preference data",
      goal: "Collect human preference pairs, train a Bradley-Terry reward model, and understand how the reward score will guide policy optimization.",
      prerequisites: ["sft"],
    },
    {
      id: "ppo-rlhf",
      title: "RLHF with PPO",
      goal: "Run the four-model RLHF training loop (policy, reference, reward, value), derive the PPO clipped surrogate objective, and see how the KL penalty prevents reward hacking.",
      prerequisites: ["reward-modeling", "D1/dl-optimizers"],
    },
    {
      id: "dpo",
      title: "DPO, IPO, and offline preference optimization",
      goal: "Derive DPO's closed-form policy reparameterization that eliminates the reward model; then survey IPO, KTO, and ORPO as robust alternatives.",
      prerequisites: ["ppo-rlhf"],
    },
    {
      id: "grpo",
      title: "Group relative policy optimization (GRPO)",
      goal: "Replace the value baseline in PPO with a group-relative reward; show how this simplifies the training loop and scales to DeepSeek-R1-style reasoning.",
      prerequisites: ["ppo-rlhf"],
    },
    {
      id: "rlaif",
      title: "Constitutional AI and RLAIF",
      goal: "Replace human feedback with AI feedback: have a supervisor model critique and revise responses using a written constitution, then train the policy with RL.",
      prerequisites: ["dpo"],
      codeExempt: true,
    },
    {
      id: "lora",
      title: "LoRA, QLoRA, and DoRA",
      goal: "Freeze the pretrained weights, inject low-rank adapter matrices A and B, and train only their product delta W = BA; extend to 4-bit QLoRA and magnitude-direction DoRA.",
      prerequisites: ["sft"],
    },
  ],

  E5: [
    {
      id: "decoding",
      title: "Decoding strategies",
      goal: "Implement greedy, beam search, top-k sampling, nucleus (top-p) sampling, and temperature scaling; understand the quality-diversity tradeoff each controls.",
      prerequisites: ["E3/decoder-only"],
    },
    {
      id: "kv-cache",
      title: "KV cache",
      goal: "Cache key and value tensors for all previous tokens so each new token incurs only one new attention row, reducing per-token cost from O(T^2) to O(T).",
      prerequisites: ["decoding"],
    },
    {
      id: "speculative-decoding",
      title: "Speculative decoding",
      goal: "Draft k tokens with a small model, verify them in a single parallel forward pass of the target model, and prove the acceptance-rejection scheme preserves the target distribution.",
      prerequisites: ["kv-cache"],
    },
    {
      id: "quantization",
      title: "Quantization: GPTQ, AWQ, and GGUF",
      goal: "Reduce weight precision from fp16 to int8 or int4 using post-training quantization; compare the one-shot Hessian-based GPTQ, the activation-aware AWQ, and the portable GGUF format.",
      prerequisites: ["kv-cache"],
      codeExempt: true,
    },
    {
      id: "paged-attention",
      title: "PagedAttention and continuous batching",
      goal: "Manage KV cache as fixed-size pages mapped to logical blocks (PagedAttention), and use continuous batching to saturate GPU throughput across requests of different lengths.",
      prerequisites: ["kv-cache"],
      codeExempt: true,
    },
    {
      id: "inference-engines",
      title: "Inference engines: vLLM, TGI, SGLang",
      goal: "Survey the architecture of production inference servers: how vLLM, TGI, and SGLang implement PagedAttention, speculative decoding, and structured output scheduling.",
      prerequisites: ["paged-attention", "speculative-decoding"],
      codeExempt: true,
    },
  ],

  E6: [
    {
      id: "rag-fundamentals",
      title: "RAG fundamentals",
      goal: "Build a retrieval-augmented generation pipeline: chunk documents, embed with a bi-encoder, store in a vector index, retrieve top-k, and pass to an LLM.",
      prerequisites: ["E3/decoder-only"],
    },
    {
      id: "dense-retrieval",
      title: "Dense retrieval and bi-encoders",
      goal: "Train a bi-encoder with contrastive loss on positive/negative passage pairs (DPR) and build a FAISS index for approximate nearest neighbor search.",
      prerequisites: ["rag-fundamentals"],
    },
    {
      id: "advanced-rag",
      title: "Advanced RAG: HyDE, rerankers, and GraphRAG",
      goal: "Generate a hypothetical document to improve sparse retrieval (HyDE), add a cross-encoder reranker to re-score retrieved passages, and connect entities in a knowledge graph (GraphRAG).",
      prerequisites: ["dense-retrieval"],
      codeExempt: true,
    },
    {
      id: "function-calling",
      title: "Tool use and function calling",
      goal: "Teach an LLM to emit structured JSON tool calls, parse tool outputs, and continue the conversation; implement a minimal tool-use loop with a calculator and search tool.",
      prerequisites: ["E3/decoder-only"],
    },
    {
      id: "chain-of-thought",
      title: "Chain-of-thought and self-consistency",
      goal: "Elicit multi-step reasoning with few-shot CoT prompting; then sample multiple reasoning paths and majority-vote the final answer (self-consistency).",
      prerequisites: ["function-calling"],
    },
    {
      id: "react-agents",
      title: "ReAct and Reflexion agents",
      goal: "Interleave reasoning traces with tool actions in a Thought-Action-Observation loop (ReAct); add memory-based self-reflection to diagnose and correct past failures (Reflexion).",
      prerequisites: ["chain-of-thought", "function-calling"],
    },
    {
      id: "test-time-compute",
      title: "Test-time compute scaling",
      goal: "Scale inference compute by searching over reasoning paths with process reward models (PRMs); understand how o1 and DeepSeek-R1 use this to outperform training-only scaling.",
      prerequisites: ["react-agents", "E4/grpo"],
      codeExempt: true,
    },
    {
      id: "multi-agent",
      title: "Multi-agent systems",
      goal: "Decompose complex tasks across specialized agents with defined roles and communication protocols; contrast AutoGen's two-agent chat with CrewAI's role-based orchestration.",
      prerequisites: ["react-agents"],
      codeExempt: true,
    },
  ],

  E7: [
    {
      id: "clip",
      title: "CLIP: contrastive vision-language pretraining",
      goal: "Train an image encoder and text encoder jointly with an InfoNCE contrastive loss on image-caption pairs; show how zero-shot classification emerges from cosine similarity.",
      prerequisites: ["E3/encoder-only", "D5/contrastive-ssl"],
    },
    {
      id: "vlm-architecture",
      title: "Vision-language model architecture",
      goal: "Bridge a frozen image encoder to an LLM with a learnable projection layer (LLaVA) or a Q-Former bottleneck (BLIP-2); trace a visual question-answering forward pass.",
      prerequisites: ["clip"],
    },
    {
      id: "lmm-finetuning",
      title: "Fine-tuning large multimodal models",
      goal: "Survey instruction fine-tuning for LMMs: visual instruction tuning datasets, the two-stage freeze-then-unfreeze schedule, and GPT-4V's proprietary pipeline.",
      prerequisites: ["vlm-architecture", "E4/sft"],
      codeExempt: true,
    },
    {
      id: "audio-llms",
      title: "Audio language models: Whisper and Wav2Vec",
      goal: "Encode audio as log-mel spectrograms, pretrain with masked prediction (Wav2Vec 2.0) or multitask supervised fine-tuning (Whisper), and decode to text.",
      prerequisites: ["E3/encoder-only"],
    },
    {
      id: "text-to-image",
      title: "Text-to-image: DALL-E, Stable Diffusion, Midjourney",
      goal: "Condition a diffusion model on a CLIP text embedding; contrast DALL-E 2 (CLIP prior + decoder), Stable Diffusion (latent diffusion + cross-attention), and classifier-free guidance.",
      prerequisites: ["clip", "D4/diffusion"],
      codeExempt: true,
    },
    {
      id: "video-generation",
      title: "Video generation: Sora and Veo",
      goal: "Extend spatial diffusion to spacetime patches, understand the role of DiT (diffusion transformers) for video, and survey the training and evaluation challenges at video scale.",
      prerequisites: ["text-to-image"],
      codeExempt: true,
    },
  ],

  E8: [
    {
      id: "probing",
      title: "Probing classifiers",
      goal: "Train linear probes on frozen LLM activations to test which layer encodes part-of-speech, syntax, or factual knowledge; interpret probe accuracy as evidence (not proof) of representation.",
      prerequisites: ["E3/encoder-only"],
    },
    {
      id: "circuits",
      title: "Mechanistic interpretability and circuits",
      goal: "Decompose a transformer into a graph of attention heads and MLP neurons that implement algorithmic sub-tasks; reproduce the indirect object identification circuit on a small model.",
      prerequisites: ["probing"],
    },
    {
      id: "induction-heads",
      title: "Induction heads",
      goal: "Identify the two-head induction circuit (previous-token head + induction head) that implements in-context learning; show how ablating it destroys few-shot performance.",
      prerequisites: ["circuits"],
    },
    {
      id: "superposition",
      title: "Superposition and polysemanticity",
      goal: "Model why a network with fewer neurons than features stores multiple features per neuron in nearly-orthogonal directions (superposition); show toy models that exhibit the phase transition.",
      prerequisites: ["circuits"],
    },
    {
      id: "sparse-autoencoders",
      title: "Sparse autoencoders",
      goal: "Decompose residual stream activations into a sparse linear combination of monosemantic dictionary features using an L1-penalized autoencoder; evaluate with feature ablation.",
      prerequisites: ["superposition"],
    },
    {
      id: "activation-steering",
      title: "Activation patching and representation engineering",
      goal: "Intervene on model behavior by patching activations from a clean run into a corrupted run (causal tracing); then steer generation by adding a direction vector to residual stream activations.",
      prerequisites: ["circuits"],
    },
    {
      id: "scalable-oversight",
      title: "Scalable oversight and weak-to-strong generalization",
      goal: "Survey scalable oversight: debate, amplification, and recursive reward modeling; then study the weak-to-strong experiment as an empirical proxy for aligning a model smarter than its supervisor.",
      prerequisites: ["E4/rlaif"],
      codeExempt: true,
    },
  ],
};
