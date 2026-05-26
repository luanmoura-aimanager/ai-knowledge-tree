import { MDXRemote } from "next-mdx-remote/rsc";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import type { MDXComponents } from "mdx/types";
import { MdxPre } from "./MdxPre";

const components: MDXComponents = {
  pre: MdxPre as MDXComponents["pre"],
};

/** Compiles and renders a subsection's MDX body (math via KaTeX, code via MdxPre). */
export function MdxContent({ source }: { source: string }) {
  return (
    <div className="mdx-body">
      <MDXRemote
        source={source}
        components={components}
        options={{
          mdxOptions: {
            remarkPlugins: [remarkMath],
            rehypePlugins: [rehypeKatex],
          },
        }}
      />
    </div>
  );
}
