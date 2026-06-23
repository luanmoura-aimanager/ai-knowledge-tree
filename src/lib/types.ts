/**
 * types.ts: domain types for the knowledge tree.
 *
 * A pillar is a top-level subject area (A → J). Each pillar has subsections
 * (A1, A2, ...), and each subsection has a flat list of topics. Topics carry
 * a coverage status indicating whether the AI ML Theory site already covers
 * them, plus a `hot` flag for frontier (2023-2025) material.
 *
 * Connections live separately and link two subsection IDs across pillars :
 * for example "D4 ↔ F8" because VAEs sit in both Generative DL and Bayesian DL.
 */

export type Status = "covered" | "partial" | "gap";

export interface Topic {
  name: string;
  status: Status;
  /** Hot / frontier topic (2023-2025): surfaced in filters and visualizations. */
  hot?: boolean;
}

export interface Subsection {
  /** Stable ID like "A1", "J3". Used in routes and connection edges. */
  id: string;
  name: string;
  /**
   * Short prose overview shown on the discipline overview page: what this
   * discipline teaches, what the reader will be able to do afterward, and why
   * it matters. Plain paragraphs separated by blank lines.
   */
  intro?: string;
  /** What a reader should already know before starting this discipline. */
  prerequisites?: string[];
  topics: Topic[];
}

export interface Pillar {
  letter: string;
  slug: string;
  name: string;
  /** Compact label for the connections-graph pill (e.g. "Stats & Causal"). */
  shortName: string;
  tagline: string;
  /** CSS color (hex) used to tint cards and graph nodes. */
  color: string;
  /**
   * Short prose overview shown on the pillar overview page: what this pillar
   * teaches and why it matters. Plain paragraphs separated by blank lines.
   */
  intro?: string;
  /** What a reader should already know before starting this pillar. */
  prerequisites?: string[];
  subs: Subsection[];
}

export type ConnectionKind =
  | "shared-concept" // same idea appears in both places (e.g. VAE in D4 and F8)
  | "uses" // one subsection depends on the other (e.g. RAG uses ANN search)
  | "alternative" // alternative approaches to the same problem (RNN vs Transformer)
  | "generalizes"; // one is a generalization of the other

export interface Connection {
  /** Subsection ID, e.g. "D4". */
  from: string;
  to: string;
  /** Short human label rendered as edge tooltip / legend. */
  label: string;
  kind: ConnectionKind;
}

/**
 * One lesson-level stop in a path's ordered sequence. Used by paths that thread
 * individual lessons (across many subsections, possibly revisiting one) rather
 * than whole disciplines. `note` carries the external origin label, e.g. the
 * ai-math-theory lesson id "6.2" the step mirrors.
 */
export interface PathStep {
  subId: string;
  lessonId: string;
  note?: string;
  /**
   * Optional phase label used to group consecutive steps under a heading in the
   * path detail (e.g. "Retrieval & agents"). When absent, the renderer falls
   * back to the ai-math-theory chapter parsed from `note` (the LLM Theory path).
   */
  section?: string;
}

/** A curated reading sequence across the DAG, rendered in the learning-paths grid. */
export interface Path {
  name: string;
  desc: string;
  /** Ordered subsection IDs the path traverses (drives the graph highlight). */
  pillars: string[];
  /**
   * Optional lesson-level sequence. When present, the path detail renders these
   * ordered lesson links instead of (or alongside) the subsection chips. Paths
   * without `steps` render unchanged from `pillars`.
   */
  steps?: PathStep[];
  /** CSS color (a `var(--p?)` token or hex) used to tint the path card. */
  color: string;
}

/**
 * A single lesson within a subsection (discipline). Lessons are the atomic
 * study unit: one concept per page. The curriculum (ordered Lesson[] per
 * subsection) lives in src/lib/curriculum; the prose lives in
 * content/<slug>/<subId>/<lessonId>.mdx.
 */
export interface Lesson {
  /** URL slug, unique within its subsection, e.g. "vector-spaces". */
  id: string;
  title: string;
  goal: string;
  /**
   * Prerequisite lessons. Each entry is either a bare lesson id in the same
   * subsection ("norms") or a cross-subsection "subId/lessonId" key.
   */
  prerequisites?: string[];
  /** Conceptual lessons with no natural code surface (infra/org material). */
  codeExempt?: boolean;
}

/** A lesson plus the subsection it belongs to (returned by curriculum helpers). */
export type LessonWithSub = Lesson & { subId: string };

/** One resolved lesson stop in a path's expanded sequence, for the lesson sidebar. */
export interface PathSidebarStep {
  letter: string;
  subId: string;
  lessonId: string;
  title: string;
  /** The pillar color of this step's subsection (steps cross pillars). */
  color: string;
  available: boolean;
  section?: string;
  note?: string;
}

/**
 * A path's prerequisite-closed lesson sequence, handed to the lesson sidebar so a
 * reader following a path sees the path's lessons (not the current discipline's).
 */
export interface PathSidebar {
  /** Stable slug derived from the path name; carried in the `?path=` query. */
  slug: string;
  name: string;
  color: string;
  steps: PathSidebarStep[];
}

/** Frontmatter schema for a lesson MDX file (`content/<slug>/<subId>/<lessonId>.mdx`). */
export interface LessonFrontmatter {
  title: string;
  /** Pillar letter, e.g. "A". */
  pillar: string;
  /** Subsection ID, e.g. "A1". */
  subId: string;
  /** Lesson slug, e.g. "vector-spaces". */
  lessonId: string;
  order: number;
  estimatedMinutes: number;
  goal: string;
  /** Lesson keys this assumes (bare id same-subsection, or "subId/lessonId"). */
  prerequisites: string[];
  codeExempt?: boolean;
}
