import type { Lesson } from "@/lib/types";

/**
 * Pillar J: AI Engineering. Ordered lesson curriculum per subsection. Lesson
 * order is the array order; prerequisites are bare ids within the same
 * subsection or "subId/lessonId" across subsections.
 *
 * J is the applied capstone (sourced from the AI Eng Journey roadmap). It is
 * framework- and architecture-heavy, so most lessons are codeExempt conceptual
 * (mermaid + static framework code that cannot run in Pyodide). Lessons with a
 * genuine self-contained quantitative surface (RAG retrieval, ANN recall, RRF,
 * rate limiting, LoRA parameter math, routing/cost, capacity modeling) carry
 * runnable numpy or pure-python blocks.
 */
export const J_CURRICULUM: Record<string, Lesson[]> = {
  J1: [
    {
      id: "rag-from-scratch",
      title: "RAG from scratch: chunk, embed, retrieve",
      goal: "Build the retrieval-augmented generation loop end to end: split documents into chunks, embed them, and retrieve the top-k most similar chunks by cosine similarity to ground a model's answer.",
      prerequisites: [
        "E/rag-fundamentals",
        "E/dense-retrieval",
        "A/inner-products",
      ],
    },
    {
      id: "tool-use",
      title: "Native tool use and schema injection",
      goal: "Give a model the ability to call functions by injecting tool schemas, parsing the structured call it emits, dispatching to real code, and feeding the result back.",
      prerequisites: ["E/function-calling"],
    },
    {
      id: "react-loop",
      title: "The ReAct loop by hand",
      goal: "Implement the reason-act-observe loop that turns a single tool call into multi-step agency, alternating model thoughts with tool actions until it reaches an answer.",
      prerequisites: ["tool-use", "E/react-agents"],
    },
    {
      id: "agent-frameworks",
      title: "Agent frameworks: what LangChain abstracts",
      goal: "Map the manual ReAct loop onto the abstractions a framework provides (tools, agent executors, memory) and judge what the framework buys you and what it hides.",
      prerequisites: ["react-loop"],
      codeExempt: true,
    },
    {
      id: "langgraph-state-machines",
      title: "LangGraph: agents as state machines",
      goal: "Model an agent as an explicit graph of nodes, edges, and routers over a shared state, and see why a graph beats a linear chain when control flow branches, loops, or needs checkpoints.",
      prerequisites: ["agent-frameworks"],
      codeExempt: true,
    },
  ],
  J2: [
    {
      id: "mcp-protocol",
      title: "The Model Context Protocol",
      goal: "Explain why a standard protocol for exposing tools, resources, and prompts turns an N-by-M integration mess into N-plus-M, and trace the MCP client-server message flow.",
      prerequisites: ["J1/tool-use"],
      codeExempt: true,
    },
    {
      id: "designing-mcp-servers",
      title: "Designing an MCP server",
      goal: "Choose the right tool granularity, name and document tools for a model rather than a human, and version a server so existing clients keep working as it evolves.",
      prerequisites: ["mcp-protocol"],
      codeExempt: true,
    },
    {
      id: "llm-as-judge",
      title: "Evaluation with LLM-as-judge",
      goal: "Score open-ended outputs with a model judge, measure whether the judge agrees with humans using Cohen's kappa, and build a regression suite that catches quality drops before release.",
      prerequisites: ["I4/llm-evaluation", "B/ab-testing"],
    },
    {
      id: "production-rag",
      title: "Production RAG: chunking and reranking",
      goal: "Move past naive RAG with deliberate chunking and a two-stage retrieve-then-rerank pipeline, and quantify the ranking-quality gain a reranker buys with nDCG.",
      prerequisites: ["J1/rag-from-scratch", "E/advanced-rag"],
    },
    {
      id: "lakehouse-architecture",
      title: "Data lake, warehouse, and lakehouse",
      goal: "Distinguish the three storage architectures behind AI data platforms by how they trade schema-on-write structure against schema-on-read flexibility, and place each workload.",
      prerequisites: ["I1/pipeline-paradigms"],
      codeExempt: true,
    },
  ],
  J3: [
    {
      id: "serving-api-design",
      title: "Serving APIs: streaming, async, versioning",
      goal: "Design the HTTP surface of an AI service: stream tokens as they generate, serve concurrent requests with async I/O, and version the API so contracts do not break.",
      prerequisites: ["I3/llm-serving"],
      codeExempt: true,
    },
    {
      id: "governance-rate-limiting",
      title: "Governance: auth, rate limiting, cost attribution",
      goal: "Put a governance layer in front of a model: authenticate callers, throttle them with a token-bucket rate limiter, and attribute token cost back to each tenant.",
      prerequisites: ["I4/cost-monitoring"],
    },
    {
      id: "deployment-cicd",
      title: "Deployment: containers, CI/CD, secrets",
      goal: "Package an AI service into a reproducible container, ship it through a CI/CD pipeline, and manage configuration and secrets across environments without baking them into the image.",
      prerequisites: ["serving-api-design"],
      codeExempt: true,
    },
    {
      id: "observability-tracing",
      title: "Observability: tracing an AI request",
      goal: "Instrument a multi-step AI request as a tree of spans so you can see where latency and tokens go, the trace-based observability that tools like LangSmith provide.",
      prerequisites: ["I4/slos-and-error-budgets"],
      codeExempt: true,
    },
    {
      id: "prompt-injection-security",
      title: "Prompt injection and data exfiltration",
      goal: "Understand why mixing trusted instructions with untrusted content is the core LLM vulnerability, and defend with trust boundaries, least privilege, and output filtering.",
      prerequisites: ["I4/safety-evals-red-teaming"],
      codeExempt: true,
    },
    {
      id: "multi-source-ingestion",
      title: "Multi-source ingestion and the dbt mental model",
      goal: "Pull data from REST APIs, object storage, and databases into one place, and adopt the ELT-plus-transformation mental model that dbt formalizes for the warehouse.",
      prerequisites: ["I1/orchestration-dags"],
      codeExempt: true,
    },
  ],
  J4: [
    {
      id: "when-not-to-finetune",
      title: "When not to fine-tune",
      goal: "Reach for prompting, RAG, and long context before fine-tuning, and recognize the narrow conditions (stable task, latency or format constraints, enough data) where fine-tuning actually pays.",
      prerequisites: ["J2/production-rag", "E/sft"],
      codeExempt: true,
    },
    {
      id: "lora-qlora",
      title: "LoRA and QLoRA: the parameter budget",
      goal: "Count exactly how few parameters a low-rank adapter trains, and see how QLoRA's quantized base weights make fine-tuning a large model fit on one GPU.",
      prerequisites: ["E/lora", "I3/quantization"],
    },
    {
      id: "dspy-context-engineering",
      title: "DSPy and programmatic prompt optimization",
      goal: "Treat prompts as parameters to be optimized rather than strings to be hand-tuned, the shift from prompt engineering to context engineering that DSPy automates.",
      prerequisites: ["J1/react-loop"],
      codeExempt: true,
    },
    {
      id: "multi-agent-orchestration",
      title: "Multi-agent orchestration",
      goal: "Decompose a hard task across a supervisor and specialized workers with explicit handoffs and shared memory, and weigh that against the simpler single-agent baseline.",
      prerequisites: ["J1/langgraph-state-machines", "E/multi-agent"],
      codeExempt: true,
    },
    {
      id: "cost-latency-routing",
      title: "Cost and latency: routing and caching",
      goal: "Cut serving cost with a model cascade that routes easy queries to a cheap model and escalates only hard ones, and quantify the blended cost-quality tradeoff.",
      prerequisites: ["I4/cost-monitoring"],
    },
  ],
  J5: [
    {
      id: "dbt-transformations",
      title: "dbt: transformations as a tested DAG",
      goal: "Build warehouse transformations as version-controlled SQL models wired into a dependency DAG with built-in tests and lineage, the backbone of an analytics-engineering workflow.",
      prerequisites: ["J3/multi-source-ingestion"],
      codeExempt: true,
    },
    {
      id: "data-contracts",
      title: "Data contracts and schema enforcement",
      goal: "Make a schema an enforced contract between data producers and consumers, validating type, presence, and range at the boundary so a bad upstream change fails fast instead of silently.",
      prerequisites: ["I1/feature-stores"],
    },
    {
      id: "vector-infra-ann",
      title: "Vector infrastructure: approximate nearest neighbors",
      goal: "Scale retrieval past brute-force search with an approximate nearest-neighbor index, and measure the recall-versus-speed tradeoff that every vector database is built around.",
      prerequisites: ["E/dense-retrieval", "A/probabilistic-structures"],
    },
    {
      id: "hybrid-search-rrf",
      title: "Hybrid search and reciprocal rank fusion",
      goal: "Combine dense (semantic) and sparse (keyword) retrieval with reciprocal rank fusion, and show why fusing two rankings beats either one on queries where they disagree.",
      prerequisites: ["J2/production-rag", "vector-infra-ann"],
    },
    {
      id: "streaming-embeddings",
      title: "Streaming and the embedding lifecycle",
      goal: "Keep an index fresh with event-driven updates and change data capture, and manage the embedding lifecycle (reindexing on model upgrades) that keeps retrieval honest over time.",
      prerequisites: ["vector-infra-ann", "I1/pipeline-paradigms"],
      codeExempt: true,
    },
  ],
  J6: [
    {
      id: "managed-ai-platforms",
      title: "Managed AI platforms and build-vs-buy",
      goal: "Read a managed stack like AWS Bedrock (knowledge bases, agents, guardrails) as pre-assembled building blocks, and decide build-versus-buy against control, lock-in, and time-to-ship.",
      prerequisites: ["J2/production-rag"],
      codeExempt: true,
    },
    {
      id: "cloud-identity-security",
      title: "Cloud identity and security for AI",
      goal: "Secure an enterprise AI system with the cloud identity primitives (IAM roles, VPCs, SSO, OAuth) and the principle of least privilege that contains the blast radius of a compromise.",
      prerequisites: ["J3/prompt-injection-security"],
      codeExempt: true,
    },
    {
      id: "multi-tenancy-gateway",
      title: "Multi-tenancy and the API gateway",
      goal: "Serve many tenants from one system with isolation, per-tenant quotas, and a gateway that centralizes auth, routing, and rate limiting in front of the model services.",
      prerequisites: ["J3/governance-rate-limiting"],
      codeExempt: true,
    },
    {
      id: "finops-for-ai",
      title: "FinOps for AI: capacity and commitment",
      goal: "Plan AI spend past per-request cost: model the break-even between on-demand and reserved capacity, and layer caching tiers to cut the bill at scale.",
      prerequisites: ["J4/cost-latency-routing"],
    },
  ],
  J7: [
    {
      id: "ai-governance-compliance",
      title: "AI governance and compliance",
      goal: "Build the controls that data-protection regimes (GDPR, LGPD) demand of AI systems: data residency, purpose limitation, the right to deletion, and an audit trail for automated decisions.",
      prerequisites: ["J6/cloud-identity-security"],
      codeExempt: true,
    },
    {
      id: "red-teaming-at-scale",
      title: "Red teaming and defense in depth",
      goal: "Turn one-off safety testing into a continuous, automated red-teaming pipeline, and layer defenses so no single bypass compromises the system.",
      prerequisites: [
        "I4/safety-evals-red-teaming",
        "J3/prompt-injection-security",
      ],
      codeExempt: true,
    },
    {
      id: "reference-architectures-adrs",
      title: "Reference architectures, ADRs, and C4",
      goal: "Communicate a system design with the architect's tools: reference architectures as reusable templates, architecture decision records to capture the why, and C4 diagrams for layered views.",
      prerequisites: ["J3/serving-api-design"],
      codeExempt: true,
    },
    {
      id: "system-design-for-ai",
      title: "System design for an AI product",
      goal: "Drive a system design from requirements to components to tradeoffs the way an architect interview expects, assembling the RAG, agent, serving, and data pieces into one coherent whole.",
      prerequisites: ["reference-architectures-adrs", "J2/production-rag"],
      codeExempt: true,
    },
    {
      id: "capacity-cost-modeling",
      title: "Capacity and cost modeling",
      goal: "Size an AI system from first principles: turn a traffic estimate into a token rate, a GPU count, and a monthly bill, the back-of-the-envelope model an architect defends a design with.",
      prerequisites: ["I3/llm-serving", "I4/cost-monitoring"],
    },
  ],
};
