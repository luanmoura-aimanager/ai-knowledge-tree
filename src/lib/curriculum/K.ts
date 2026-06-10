import type { Lesson } from "@/lib/types";

/**
 * Pillar K: Data Engineering. Ordered lesson curriculum per subsection. Lesson
 * order is the array order; prerequisites are bare ids within the same
 * subsection or "subId/lessonId" across subsections.
 *
 * This pillar is the general data-systems foundation: modeling, physical
 * storage, batch and stream processing, orchestration, and data quality. It is
 * deliberately upstream of pillar I (which applies these ideas to ML feature
 * pipelines) and pillar J5 (which applies them to an AI/vector data platform).
 * Most of it is infrastructure-flavored, so the conceptual lessons are marked
 * codeExempt and carry a diagram; the lessons with a genuine quantitative
 * surface (scan/shuffle cost, compression ratios, windowing, anomaly z-scores)
 * keep runnable numpy.
 */
export const K_CURRICULUM: Record<string, Lesson[]> = {
  K1: [
    {
      id: "relational-model",
      title: "The relational model and normal forms",
      goal: "Model data as relations with keys and functional dependencies, and normalize to 3NF/BCNF to remove the update, insertion, and deletion anomalies that redundancy causes.",
      prerequisites: [],
      codeExempt: true,
    },
    {
      id: "oltp-vs-olap",
      title: "OLTP vs OLAP and the two shapes of a workload",
      goal: "Separate transactional (many small writes, point lookups) from analytical (few large scans, aggregations) workloads, and see why one storage layout cannot serve both well.",
      prerequisites: ["relational-model"],
      codeExempt: true,
    },
    {
      id: "dimensional-modeling",
      title: "Dimensional modeling: facts, dimensions, and star schemas",
      goal: "Design an analytics schema the Kimball way, a central fact table of measurements surrounded by dimension tables of context, and see why the star shape makes aggregation queries fast and legible.",
      prerequisites: ["oltp-vs-olap"],
      codeExempt: true,
    },
    {
      id: "slowly-changing-dimensions",
      title: "Slowly changing dimensions",
      goal: "Track how a dimension's attributes change over time with Type 1 (overwrite), Type 2 (new versioned row), and Type 3 (prior-value column), and reconstruct the state as of any past date.",
      prerequisites: ["dimensional-modeling"],
    },
    {
      id: "normalization-tradeoffs",
      title: "Normalization vs denormalization for analytics",
      goal: "Weigh the storage and update cost of denormalization against the join cost it removes, and decide when a wide pre-joined table beats a normalized star for read-heavy analytics.",
      prerequisites: ["dimensional-modeling"],
    },
  ],
  K2: [
    {
      id: "row-vs-columnar",
      title: "Row vs columnar storage",
      goal: "Lay the same table out by row or by column and compute the bytes an analytical query must scan in each, the I/O argument that makes columnar the default for analytics.",
      prerequisites: ["K1/oltp-vs-olap"],
    },
    {
      id: "compression-encoding",
      title: "Lightweight encodings: dictionary, run-length, and delta",
      goal: "Shrink a column with dictionary, run-length, and delta encoding, compute the compression ratio each gives on real data, and see why columnar layout makes these encodings so effective.",
      prerequisites: ["row-vs-columnar"],
    },
    {
      id: "parquet-internals",
      title: "Inside Parquet: row groups, column chunks, and statistics",
      goal: "Read the Parquet file layout, row groups split into per-column chunks with min/max statistics, and see how those statistics let an engine skip whole row groups without decoding them.",
      prerequisites: ["compression-encoding"],
      codeExempt: true,
    },
    {
      id: "partitioning-pruning",
      title: "Partitioning and partition pruning",
      goal: "Lay data out in directories keyed by a column and compute how a predicate prunes the files an engine must open, plus why over-partitioning into tiny files destroys the gain.",
      prerequisites: ["parquet-internals"],
    },
    {
      id: "table-formats-lakehouse",
      title: "Table formats and the lakehouse",
      goal: "Turn a pile of Parquet files into a transactional table with a metadata layer (Iceberg, Delta, Hudi): atomic snapshots, schema evolution, and time travel over object storage.",
      prerequisites: ["partitioning-pruning"],
      codeExempt: true,
    },
  ],
  K3: [
    {
      id: "mapreduce",
      title: "MapReduce and the shuffle",
      goal: "Express a distributed aggregation as map, shuffle, and reduce, and see why the all-to-all shuffle in the middle is the step that dominates the cost of a big job.",
      prerequisites: ["K1/oltp-vs-olap"],
    },
    {
      id: "spark-dataframes",
      title: "Spark: lazy DataFrames and the execution DAG",
      goal: "Build a transformation as a lazy DataFrame lineage that Spark compiles into a DAG of stages, and distinguish the narrow transformations that pipeline from the wide ones that force a shuffle.",
      prerequisites: ["mapreduce"],
      codeExempt: true,
    },
    {
      id: "distributed-joins",
      title: "Distributed joins: shuffle vs broadcast",
      goal: "Choose between a shuffle join and a broadcast join by comparing the bytes each moves across the network, and see why broadcasting a small table avoids the shuffle entirely.",
      prerequisites: ["spark-dataframes"],
    },
    {
      id: "data-skew",
      title: "Data skew and the straggler problem",
      goal: "Quantify how a skewed key distribution overloads one reducer, making job time track the largest partition rather than the average, and fix it with salting.",
      prerequisites: ["distributed-joins"],
    },
    {
      id: "query-execution-pushdown",
      title: "Query execution: predicate pushdown and vectorization",
      goal: "Trace how a query planner pushes filters and column projections down to the scan and processes data in vectorized batches, cutting the rows and bytes that reach the CPU.",
      prerequisites: ["K2/partitioning-pruning", "distributed-joins"],
    },
  ],
  K4: [
    {
      id: "log-and-kafka",
      title: "The log abstraction and Kafka",
      goal: "Model a stream as an append-only partitioned log with per-consumer offsets, and see how partitioning by key gives ordered, replayable, horizontally scalable ingestion.",
      prerequisites: ["K1/oltp-vs-olap"],
      codeExempt: true,
    },
    {
      id: "windowing",
      title: "Windowing: tumbling, sliding, and session windows",
      goal: "Aggregate an unbounded stream by cutting it into tumbling, sliding, and session windows, and compute the same metric under each to see how the window choice changes the answer.",
      prerequisites: ["log-and-kafka"],
    },
    {
      id: "watermarks-late-data",
      title: "Event time, watermarks, and late data",
      goal: "Separate event time from processing time, track progress with a watermark that bounds how late data can be, and reason about the completeness-versus-latency tradeoff it sets.",
      prerequisites: ["windowing"],
    },
    {
      id: "delivery-semantics",
      title: "Delivery semantics and idempotency",
      goal: "Distinguish at-most-once, at-least-once, and exactly-once delivery, and see why an idempotent consumer turns cheap at-least-once delivery into effectively-once processing.",
      prerequisites: ["watermarks-late-data"],
    },
    {
      id: "change-data-capture",
      title: "Change data capture and the outbox pattern",
      goal: "Stream a database's row-level changes off its write-ahead log instead of polling, and use the transactional outbox to publish events without dual-write inconsistency.",
      prerequisites: ["delivery-semantics"],
      codeExempt: true,
    },
  ],
  K5: [
    {
      id: "etl-vs-elt",
      title: "ETL vs ELT and pushdown transformation",
      goal: "Contrast transform-before-load with load-then-transform, and see why cheap cloud storage and scalable warehouses made ELT (pushing transformation into the warehouse) the modern default.",
      prerequisites: ["K1/dimensional-modeling"],
      codeExempt: true,
    },
    {
      id: "transformation-as-code",
      title: "Transformations as tested code",
      goal: "Define warehouse transformations as version-controlled, dependency-linked models (the dbt mental model) so a transformation layer becomes a testable DAG with lineage instead of ad hoc SQL.",
      prerequisites: ["etl-vs-elt"],
      codeExempt: true,
    },
    {
      id: "incremental-processing",
      title: "Incremental models: merge and upsert",
      goal: "Process only new or changed rows instead of rebuilding a table, and use a merge/upsert keyed on a stable id so a reprocessed batch updates rather than duplicates.",
      prerequisites: ["transformation-as-code"],
    },
    {
      id: "scheduling-backfills",
      title: "Scheduling, backfills, and idempotent reruns",
      goal: "Schedule a pipeline as dependency-driven runs partitioned by time, and design each task to be idempotent so a backfill or retry recomputes a partition cleanly without double-counting.",
      prerequisites: ["incremental-processing", "A5/graph-traversal"],
    },
    {
      id: "orchestrators-compared",
      title: "Orchestrators: task-based vs asset-based",
      goal: "Compare task-centric orchestration (Airflow: run these steps in order) with asset-centric orchestration (Dagster: produce these tables), and see what each makes easy or hard.",
      prerequisites: ["scheduling-backfills"],
      codeExempt: true,
    },
  ],
  K6: [
    {
      id: "data-quality-dimensions",
      title: "Data quality dimensions and validation checks",
      goal: "Make data quality measurable along completeness, validity, uniqueness, and consistency, and turn each into an automated check with a pass rate you can alert on.",
      prerequisites: ["K5/transformation-as-code"],
    },
    {
      id: "schema-evolution-contracts",
      title: "Schema evolution and data contracts",
      goal: "Classify a schema change as backward-, forward-, or full-compatible, and enforce a data contract so a producer's breaking change fails fast at the boundary instead of corrupting consumers.",
      prerequisites: ["data-quality-dimensions"],
    },
    {
      id: "data-lineage",
      title: "Data lineage and provenance",
      goal: "Trace a column end to end as a dependency graph from source to dashboard, and use lineage to scope the blast radius of a change and to debug where a bad value entered.",
      prerequisites: ["schema-evolution-contracts", "A5/graph-traversal"],
      codeExempt: true,
    },
    {
      id: "data-observability",
      title: "Data observability: freshness, volume, and anomalies",
      goal: "Monitor the operational health of a pipeline, freshness, row volume, and null rates, and flag a broken upstream feed with a robust z-score before it reaches a dashboard.",
      prerequisites: ["data-quality-dimensions"],
    },
    {
      id: "governance-pii",
      title: "Governance: PII, access control, and compliance",
      goal: "Classify and protect sensitive data with masking, tokenization, and role-based access, and meet regimes like GDPR (purpose limitation, the right to deletion) with an auditable trail.",
      prerequisites: ["data-lineage"],
      codeExempt: true,
    },
  ],
};
