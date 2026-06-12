// Quick render check for lesson .mdx files (per mdx-rendering-pitfalls memory):
// compile AND render, since `npm run build` does not prerender dynamic lesson routes.
//
// Usage:
//   node scripts/render-check.mjs [--exercises] <file.mdx|dir> [...more]
//
// Directories are recursed for *.mdx. With --exercises, each file must also
// contain a rendered "Exercises" <h2> followed by at least 3 exercise prompts
// and 3 <details> blocks whose first child is <summary> (a body that starts
// with anything else means the missing-blank-line failure: MDX folded the
// summary into a paragraph). See content/STYLE.md §6.7.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { evaluate } from "@mdx-js/mdx";
import * as runtime from "react/jsx-runtime";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import rehypeUnwrapImages from "rehype-unwrap-images";

const argv = process.argv.slice(2);
const checkExercises = argv.includes("--exercises");
const inputs = argv.filter((a) => a !== "--exercises");
if (inputs.length === 0) {
  console.error(
    "usage: node scripts/render-check.mjs [--exercises] <file.mdx|dir> [...]",
  );
  process.exit(2);
}

const files = [];
let badInputs = 0;
function collect(path) {
  let stat;
  try {
    stat = statSync(path);
  } catch {
    console.error(`FAIL ${path}: no such file or directory`);
    badInputs++;
    return;
  }
  if (stat.isDirectory()) {
    for (const entry of readdirSync(path).sort()) collect(join(path, entry));
  } else if (path.endsWith(".mdx")) {
    files.push(path);
  }
}
inputs.forEach(collect);
if (files.length === 0) {
  console.error("FAIL: no .mdx files matched the given inputs");
  process.exit(2);
}

const components = {
  FN: () => React.createElement("sup", null, "fn"),
  FNItem: (p) => React.createElement("li", null, p.children),
  Footnotes: (p) => React.createElement("section", null, p.children),
  pre: (p) => React.createElement("pre", null, p.children),
  img: (p) => React.createElement("img", { src: p.src, alt: p.alt }),
};

async function check(file) {
  let src = readFileSync(file, "utf8");
  src = src.replace(/^---\n[\s\S]*?\n---\n/, ""); // strip frontmatter
  try {
    const { default: MDXContent } = await evaluate(src, {
      ...runtime,
      // Keep in sync with src/components/mdx/MdxContent.tsx.
      remarkPlugins: [[remarkGfm, { singleTilde: false }], remarkMath],
      rehypePlugins: [rehypeKatex, rehypeUnwrapImages],
    });
    const html = renderToStaticMarkup(
      React.createElement(MDXContent, { components }),
    );
    if (html.includes("katex-error") || html.includes("\\color{")) {
      console.error(`FAIL ${file}: RENDER ERROR (katex-error)`);
      return false;
    }
    // A literal "|---" surviving into rendered HTML means a GFM table was NOT
    // parsed (raw pipe text leaked through). Flag it.
    if (/\|\s*-{3,}/.test(html)) {
      console.error(`FAIL ${file}: RAW PIPE TABLE (not parsed as <table>)`);
      return false;
    }
    if (checkExercises && !checkExercisesSection(file, html)) return false;
    const tbl = html.includes("<table") ? " [has <table>]" : "";
    const ex = checkExercises ? " [exercises ok]" : "";
    console.log(`OK ${file} (${html.length} chars rendered)${tbl}${ex}`);
    return true;
  } catch (e) {
    console.error(`FAIL ${file}: ${e.message}`);
    return false;
  }
}

function checkExercisesSection(file, html) {
  const parts = html.split(/<h2[^>]*>Exercises<\/h2>/);
  if (parts.length < 2) {
    console.error(`FAIL ${file}: no "Exercises" <h2> in rendered HTML`);
    return false;
  }
  const section = parts[parts.length - 1];
  const prompts = section.match(/<strong>Exercise \d/g) ?? [];
  if (prompts.length < 3) {
    console.error(
      `FAIL ${file}: only ${prompts.length} "**Exercise N.**" prompts after the Exercises h2 (need >= 3)`,
    );
    return false;
  }
  const details = section.match(/<details[^>]*>[\s\S]*?<\/details>/g) ?? [];
  if (details.length < 3) {
    console.error(
      `FAIL ${file}: only ${details.length} <details> blocks after the Exercises h2 (need >= 3)`,
    );
    return false;
  }
  for (const d of details) {
    const body = d.replace(/^<details[^>]*>/, "").replace(/<\/details>$/, "");
    // The first child must be <summary>; anything else (typically <p><summary>)
    // means a missing blank line folded the summary into the solution body.
    if (!body.startsWith("<summary>")) {
      console.error(
        `FAIL ${file}: <details> does not start with <summary> (missing blank line after </summary>?)`,
      );
      return false;
    }
    const inner = body.replace(/^<summary>[\s\S]*?<\/summary>/, "");
    // A parsed solution body contains element markup; raw unparsed text has none.
    if (!/</.test(inner)) {
      console.error(
        `FAIL ${file}: <details> body did not parse as markup (missing blank lines?)`,
      );
      return false;
    }
  }
  return true;
}

let failed = 0;
for (const f of files) {
  if (!(await check(f))) failed++;
}
if (files.length > 1) {
  console.log(`${files.length - failed}/${files.length} OK`);
}
process.exit(failed === 0 && badInputs === 0 ? 0 : 1);
