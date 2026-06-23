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
import { PATHS } from "@/lib/dag";
import { allLessons } from "@/lib/curriculum";
import { expandPathSteps, validatePathClosure } from "@/lib/paths";

let failed = false;

// 1. Global: no lesson may reference a prerequisite that doesn't exist.
const exists = new Set(allLessons().map((l) => `${l.subId}/${l.id}`));
const dangling: string[] = [];
for (const l of allLessons()) {
  for (const t of l.prerequisites ?? []) {
    const key = t.includes("/") ? t : `${l.subId}/${t}`;
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
  if (issues.length === 0) {
    console.log(`✓ ${path.name} — ${steps.length} → ${expanded.length} steps`);
    continue;
  }
  failed = true;
  console.log(`✗ ${path.name} (${issues.length} issue(s) after expansion):`);
  for (const i of issues) console.log(`    [${i.kind}] ${i.detail}`);
}

console.log(`\n${failed ? "FAIL" : "PASS"}: path prerequisite closure check.`);
process.exit(failed ? 1 : 0);
