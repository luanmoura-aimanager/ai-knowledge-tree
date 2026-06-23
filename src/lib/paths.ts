import type { PathStep } from "@/lib/types";
import { allLessons } from "@/lib/curriculum";

/**
 * Prerequisite closure for curated learning paths.
 *
 * A path's `steps[]` in `dag.ts` is hand-curated as a *highlight reel* — it lists
 * the lessons that tell the path's story, not every prerequisite they assume. But
 * a reader who opens a path expects to be able to follow it top to bottom without
 * landing on a lesson whose prerequisites live outside the path. `expandPathSteps`
 * closes that gap: it returns the curated steps with every transitive prerequisite
 * inserted **just before the first step that needs it**, so the expanded sequence
 * is prerequisite-closed and topologically ordered (its first lesson is always
 * prerequisite-free). The curated source stays small; closure is derived here, so
 * new paths get it for free.
 *
 * Inserted prerequisites inherit the grouping of the step that pulled them in
 * (the `section` header, or the ai-math-theory chapter parsed from `note`) so they
 * fold into the same collapsible group in the path detail.
 */

type Key = string; // "subId/lessonId"

interface Graph {
  exists: Set<Key>;
  prereqs: Map<Key, Key[]>;
  /** Pedagogically-sensible global order (curriculum insertion + lesson order). */
  rank: Map<Key, number>;
}

let GRAPH: Graph | null = null;

/** Normalize a prereq token for a lesson living in `ownSubId` (mirrors page.tsx). */
export function normalizePrereq(token: string, ownSubId: string): Key {
  return token.includes("/") ? token : `${ownSubId}/${token}`;
}

function buildGraph(): Graph {
  const exists = new Set<Key>();
  const prereqs = new Map<Key, Key[]>();
  const rank = new Map<Key, number>();
  allLessons().forEach((l, i) => {
    const key = `${l.subId}/${l.id}`;
    exists.add(key);
    prereqs.set(
      key,
      (l.prerequisites ?? []).map((t) => normalizePrereq(t, l.subId)),
    );
    rank.set(key, i);
  });
  return { exists, prereqs, rank };
}

function graph(): Graph {
  return (GRAPH ??= buildGraph());
}

const keyOf = (s: { subId: string; lessonId: string }): Key =>
  `${s.subId}/${s.lessonId}`;

/** Chapter number a `note` belongs to (the leading integer), or "". */
function chapterOf(note?: string): string {
  return note?.match(/\d+/)?.[0] ?? "";
}

/**
 * Topologically order a set of keys (prerequisites first), tie-broken by the
 * global `rank` so the order reads naturally. Any keys left over by a cycle are
 * appended in rank order (the caller's ordering check then surfaces the cycle).
 */
function topoOrder(keys: Set<Key>, g: Graph): Key[] {
  const nodes = [...keys];
  const indeg = new Map<Key, number>();
  const dependents = new Map<Key, Key[]>();
  for (const k of nodes) {
    indeg.set(k, 0);
    dependents.set(k, []);
  }
  for (const k of nodes) {
    for (const p of g.prereqs.get(k) ?? []) {
      if (!keys.has(p)) continue;
      dependents.get(p)!.push(k);
      indeg.set(k, indeg.get(k)! + 1);
    }
  }
  const rank = (k: Key) => g.rank.get(k) ?? Number.MAX_SAFE_INTEGER;
  const ready = nodes
    .filter((k) => indeg.get(k) === 0)
    .sort((a, b) => rank(a) - rank(b));
  const out: Key[] = [];
  const insertReady = (k: Key) => {
    const r = rank(k);
    let i = ready.findIndex((x) => rank(x) > r);
    if (i === -1) i = ready.length;
    ready.splice(i, 0, k);
  };
  while (ready.length) {
    const k = ready.shift()!;
    out.push(k);
    for (const d of dependents.get(k)!) {
      indeg.set(d, indeg.get(d)! - 1);
      if (indeg.get(d) === 0) insertReady(d);
    }
  }
  // Leftover = cycle members; keep the output total so nothing is silently lost.
  if (out.length < nodes.length) {
    for (const k of nodes.sort((a, b) => rank(a) - rank(b))) {
      if (!out.includes(k)) out.push(k);
    }
  }
  return out;
}

/** Topo-ordered transitive prerequisite closure of `key` (excluding `key`). */
function prereqClosure(key: Key, g: Graph): Key[] {
  const required = new Set<Key>();
  (function dfs(x: Key) {
    for (const p of g.prereqs.get(x) ?? []) {
      if (!g.exists.has(p)) continue; // dangling id: skip (the guard reports it)
      if (!required.has(p)) {
        required.add(p);
        dfs(p);
      }
    }
  })(key);
  return topoOrder(required, g);
}

/**
 * Expand a curated path into a prerequisite-closed, just-in-time-ordered sequence.
 * For each curated step, any not-yet-included transitive prerequisite is emitted
 * immediately before it (an out-of-order curated step that another lesson depends
 * on is likewise pulled forward, keeping its own metadata). Repeated curated
 * lessons (intentional revisits) are preserved.
 */
export function expandPathSteps(steps: PathStep[]): PathStep[] {
  if (!steps || steps.length === 0) return steps ?? [];
  const g = graph();

  const firstIdx = new Map<Key, number>();
  const origByKey = new Map<Key, PathStep>();
  steps.forEach((s, i) => {
    const k = keyOf(s);
    if (!firstIdx.has(k)) firstIdx.set(k, i);
    if (!origByKey.has(k)) origByKey.set(k, s);
  });

  const inherit = (k: Key, trigger: PathStep): PathStep => {
    const [subId, lessonId] = k.split("/");
    if (trigger.section) return { subId, lessonId, section: trigger.section };
    if (trigger.note) {
      const ch = chapterOf(trigger.note);
      return { subId, lessonId, note: ch ? `${ch} · prereq` : undefined };
    }
    return { subId, lessonId };
  };

  const emitted = new Set<Key>();
  const out: PathStep[] = [];

  const placePrereqs = (k: Key, trigger: PathStep) => {
    for (const p of prereqClosure(k, g)) {
      if (emitted.has(p)) continue;
      // A curated-but-later step that's needed here is pulled forward with its
      // own metadata; a brand-new prerequisite inherits the trigger's grouping.
      out.push(firstIdx.has(p) ? origByKey.get(p)! : inherit(p, trigger));
      emitted.add(p);
    }
  };

  steps.forEach((s, i) => {
    const k = keyOf(s);
    placePrereqs(k, s);
    // Skip a step that was already pulled forward as a prerequisite (its slot
    // moved earlier); a genuine later repeat still re-emits.
    if (emitted.has(k) && i === firstIdx.get(k)) return;
    out.push(s);
    emitted.add(k);
  });

  return out;
}

/** Distinct subsection ids in first-occurrence order (for chips / graph highlight). */
export function distinctSubIds(steps: PathStep[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const s of steps)
    if (!seen.has(s.subId)) {
      seen.add(s.subId);
      out.push(s.subId);
    }
  return out;
}

export interface PathPrereqIssue {
  kind: "dangling" | "unordered";
  detail: string;
}

/**
 * Validate that `steps` (typically the expansion) is prerequisite-closed and
 * ordered: every step's prerequisites resolve and appear earlier. Used by the
 * guard script; exported here so the check reuses the exact same graph/normalize
 * logic as the expansion.
 */
export function validatePathClosure(steps: PathStep[]): PathPrereqIssue[] {
  const g = graph();
  const issues: PathPrereqIssue[] = [];
  const seen = new Set<Key>();
  steps.forEach((s, i) => {
    const k = keyOf(s);
    for (const p of g.prereqs.get(k) ?? []) {
      if (!g.exists.has(p)) {
        issues.push({
          kind: "dangling",
          detail: `${k} → ${p} (no such lesson)`,
        });
      } else if (!seen.has(p)) {
        issues.push({
          kind: "unordered",
          detail: `step #${i + 1} ${k} needs ${p} earlier`,
        });
      }
    }
    seen.add(k);
  });
  return issues;
}
