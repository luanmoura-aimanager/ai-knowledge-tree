import type { ReactNode } from "react";

/**
 * Paper-style references for a lesson (adapted from the sibling ai-math-theory
 * project). Inline marker is a bracketed number rendered at body size, e.g.
 * "scaled dot-product attention [3]", and the bottom block is a 'References'
 * section with a thin rule above it and bracketed entries like "[3] Vaswani…".
 *
 * IMPORTANT — props are STRINGS, not `{number}` expressions. This content is
 * rendered with `next-mdx-remote/rsc`, which does not evaluate numeric JSX
 * expression attributes in MDX (`n={1}` arrives as `undefined`); string
 * attributes (`n="1"`) are passed through literally and parsed here. Use:
 *
 *   ... scaled dot-product attention<FN n="1" />.       // single
 *   ... both losses<FN ns="2, 3" />.                     // grouped: [2, 3]
 *
 *   <Footnotes>
 *     <FNItem n="1">**Vaswani, A., et al.** (2017). "Attention is all you
 *       need". *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)</FNItem>
 *   </Footnotes>
 *
 * Numbering is local to a lesson (each lesson starts at 1). The three
 * components are registered in the MDX component map (MdxContent.tsx). See
 * content/STYLE.md §9 for the authoring convention.
 */

/** Normalize the string/number props into a list of citation numbers. */
function toList(n?: string | number, ns?: string | number[]): number[] {
  if (ns !== undefined) {
    // filter(Boolean) drops empty tokens from leading/trailing/double separators
    // BEFORE Number(), since Number("") is 0 (finite) and would leak a stray [0].
    const arr = Array.isArray(ns)
      ? ns
      : String(ns)
          .split(/[,\s]+/)
          .filter(Boolean);
    return arr.map(Number).filter((k) => Number.isFinite(k));
  }
  if (n !== undefined && n !== "") {
    const k = Number(n);
    return Number.isFinite(k) ? [k] : [];
  }
  return [];
}

export function FN({ n, ns }: { n?: string | number; ns?: string | number[] }) {
  // Single ref: <FN n="3" />. Grouped refs: <FN ns="1, 2, 4" /> → "[1, 2, 4]"
  // with each number linked individually (the CS-paper grouping convention).
  const list = toList(n, ns);
  if (list.length === 0) return null;
  if (list.length === 1) {
    const k = list[0];
    return (
      <span className="mdx-fn-ref">
        <a href={`#fn-${k}`} id={`fn-ref-${k}`} aria-label={`Reference ${k}`}>
          [{k}]
        </a>
      </span>
    );
  }
  return (
    <span className="mdx-fn-ref mdx-fn-ref--multi">
      [
      {list.map((k, i) => (
        <span key={k}>
          {i > 0 && ", "}
          <a href={`#fn-${k}`} id={`fn-ref-${k}`} aria-label={`Reference ${k}`}>
            {k}
          </a>
        </span>
      ))}
      ]
    </span>
  );
}

export function FNItem({
  n,
  children,
}: {
  n: string | number;
  children: ReactNode;
}) {
  const k = Number(n);
  return (
    <li id={`fn-${k}`} className="mdx-fn-item">
      <span className="mdx-fn-item__num">[{k}]</span>
      <span className="mdx-fn-item__body">{children}</span>
      <a
        href={`#fn-ref-${k}`}
        className="mdx-fn-backref"
        aria-label={`Back to citation ${k}`}
      >
        ↩
      </a>
    </li>
  );
}

export function Footnotes({ children }: { children: ReactNode }) {
  return (
    <section className="mdx-footnotes" aria-label="References">
      <hr className="mdx-footnotes__rule" />
      <h2 className="mdx-footnotes__heading">References</h2>
      <ol className="mdx-footnotes__list">{children}</ol>
    </section>
  );
}
