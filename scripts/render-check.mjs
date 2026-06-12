// Quick render check for a lesson .mdx (per mdx-rendering-pitfalls memory):
// compile AND render, since `npm run build` does not prerender dynamic lesson routes.
import { readFileSync } from "node:fs";
import { evaluate } from "@mdx-js/mdx";
import * as runtime from "react/jsx-runtime";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";

const file = process.argv[2];
let src = readFileSync(file, "utf8");
src = src.replace(/^---\n[\s\S]*?\n---\n/, ""); // strip frontmatter

const components = {
  FN: () => React.createElement("sup", null, "fn"),
  FNItem: (p) => React.createElement("li", null, p.children),
  Footnotes: (p) => React.createElement("section", null, p.children),
  pre: (p) => React.createElement("pre", null, p.children),
  img: (p) => React.createElement("img", { src: p.src, alt: p.alt }),
};

try {
  const { default: MDXContent } = await evaluate(src, {
    ...runtime,
    // Keep in sync with src/components/mdx/MdxContent.tsx.
    remarkPlugins: [[remarkGfm, { singleTilde: false }], remarkMath],
    rehypePlugins: [rehypeKatex],
  });
  const html = renderToStaticMarkup(
    React.createElement(MDXContent, { components }),
  );
  if (html.includes("katex-error") || html.includes("\\color{")) {
    console.error(`RENDER ERROR (katex-error) in ${file}`);
    process.exit(1);
  }
  // A literal "|---" surviving into rendered HTML means a GFM table was NOT
  // parsed (raw pipe text leaked through). Flag it.
  if (/\|\s*-{3,}/.test(html)) {
    console.error(`RAW PIPE TABLE (not parsed as <table>) in ${file}`);
    process.exit(1);
  }
  const tbl = html.includes("<table") ? " [has <table>]" : "";
  console.log(`OK ${file} (${html.length} chars rendered)${tbl}`);
} catch (e) {
  console.error(`FAILED ${file}: ${e.message}`);
  process.exit(1);
}
