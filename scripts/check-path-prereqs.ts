/**
 * Guard: every curated learning path must be prerequisite-closed once expanded.
 *
 * Paths in `src/lib/dag.ts` are curated highlight reels; `expandPathSteps`
 * (src/lib/paths.ts) inserts each lesson's transitive prerequisites just before
 * the first step that needs it, so the rendered path can be followed top to
 * bottom. This guard asserts the EXPANSION is in fact prerequisite-closed and
 * ordered (every step's prerequisites resolve and appear earlier), and that no
 * curated lesson references a prerequisite id that doesn't exist.
 *
 * It catches authoring mistakes — a dangling prereq id, a prerequisite cycle, or
 * a regression in the expansion logic — before they ship. Run via
 * `npm run check:paths` (tsx; reuses the real curriculum/dag data).
 */
import { PATHS, getSubsectionById } from "@/lib/dag";
import { allLessons } from "@/lib/curriculum";
import {
  expandPathSteps,
  validatePathClosure,
  normalizePrereq,
} from "@/lib/paths";

let failed = false;

// 1. Global: no lesson may reference a prerequisite that doesn't exist.
const exists = new Set(allLessons().map((l) => `${l.subId}/${l.id}`));
const dangling: string[] = [];
for (const l of allLessons()) {
  for (const t of l.prerequisites ?? []) {
    const key = normalizePrereq(t, l.subId);
    if (!exists.has(key)) dangling.push(`${l.subId}/${l.id} → ${key}`);
  }
}
if (dangling.length) {
  failed = true;
  console.log(`✗ dangling prerequisite ids (curriculum bug):`);
  for (const d of dangling) console.log(`    ${d}`);
}

// 2. Per path: the expansion must be prerequisite-closed and ordered.
for (const path of PATHS) {
  const steps = path.steps ?? [];
  if (steps.length === 0) {
    console.log(`· ${path.name} (no lesson steps)`);
    continue;
  }
  const expanded = expandPathSteps(steps);
  const issues = validatePathClosure(expanded);
  // Every traversed subsection must be a real dag.ts subsection: the chips and
  // each step's lesson link are now derived from the expanded steps, so an
  // unknown subId renders a broken /pillar// link and a dropped discipline chip.
  const unknownSubs = [
    ...new Set(
      expanded.map((s) => s.subId).filter((id) => !getSubsectionById(id)),
    ),
  ];
  if (issues.length === 0 && unknownSubs.length === 0) {
    console.log(`✓ ${path.name} — ${steps.length} → ${expanded.length} steps`);
    continue;
  }
  failed = true;
  console.log(
    `✗ ${path.name} (${issues.length + unknownSubs.length} issue(s) after expansion):`,
  );
  for (const i of issues) console.log(`    [${i.kind}] ${i.detail}`);
  for (const id of unknownSubs)
    console.log(`    [unknown-subsection] ${id} is not a subsection in dag.ts`);
}

console.log(`\n${failed ? "FAIL" : "PASS"}: path prerequisite closure check.`);
process.exit(failed ? 1 : 0);
