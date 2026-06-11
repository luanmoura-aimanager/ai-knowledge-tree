// Heuristic triage for the intuition-examples pass (STYLE.md §6.2 item 4).
// Ranks lessons by how equation-heavy their prose is relative to how many
// concrete-example signals it carries. High score = lots of derivation, little
// grounding = candidate for an examples pass. A triage, not a verdict: top
// candidates still need a human/LLM read before editing.
//
// Usage: node scripts/find-intuition-candidates.mjs [topN]
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const ROOT = "content";
const topN = Number(process.argv[2] ?? 50);

// Markers that concrete grounding tends to leave in prose.
const SIGNAL =
  /\b(for example|for instance|e\.g\.|concretely|make this concrete|imagine|picture|suppose|say you|consider (a|the|two)|real[- ]world|in practice|mental hook|intuition|intuitively|as an example|worked example|numerically|plug(ging)? in|toy (example|problem|model)|sanity[- ]check)\b/gi;

function* mdxFiles(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* mdxFiles(p);
    else if (e.name.endsWith(".mdx") && /\/[A-K]\d+\//.test(p)) yield p;
  }
}

const rows = [];
for (const file of mdxFiles(ROOT)) {
  let src = readFileSync(file, "utf8");
  src = src.replace(/^---\n[\s\S]*?\n---\n/, ""); // frontmatter
  src = src.replace(/<Footnotes>[\s\S]*?<\/Footnotes>/g, ""); // references
  src = src.replace(/```[\s\S]*?```/g, ""); // code + mermaid blocks

  const displayEq = (src.match(/^\s*\$\$/gm) ?? []).length / 2;
  const prose = src
    .replace(/\$\$[\s\S]*?\$\$/g, " ")
    .replace(/\$[^$\n]*\$/g, " ");
  const words = (prose.match(/\b[a-zA-Z]{2,}\b/g) ?? []).length;
  const signals = (prose.match(SIGNAL) ?? []).length;

  // Equations per signal, dampened by prose length so short heavy pages rank up.
  const score =
    displayEq < 2
      ? 0
      : displayEq / (signals + 1) + displayEq / Math.max(words / 200, 1) / 10;
  rows.push({
    file: file.replace(`${ROOT}/`, ""),
    displayEq,
    signals,
    words,
    score,
  });
}

rows.sort((a, b) => b.score - a.score);

console.log(`scanned ${rows.length} lessons; top ${topN} candidates:\n`);
console.log("score\teqs\tsignals\twords\tlesson");
for (const r of rows.slice(0, topN))
  console.log(
    `${r.score.toFixed(2)}\t${r.displayEq}\t${r.signals}\t${r.words}\t${r.file}`,
  );

const byPillar = {};
for (const r of rows.filter((r) => r.score >= 3)) {
  const p = r.file[0];
  byPillar[p] = (byPillar[p] ?? 0) + 1;
}
console.log(`\nlessons with score >= 3 (suggested triage cutoff), by pillar:`);
console.log(
  Object.entries(byPillar)
    .sort()
    .map(([p, n]) => `${p}:${n}`)
    .join("  "),
  ` total:${rows.filter((r) => r.score >= 3).length}`,
);
