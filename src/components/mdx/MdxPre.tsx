import type { ReactElement } from "react";
import { CodeBlock } from "./CodeBlock";
import { PyRunner } from "./PyRunner";
import { Mermaid } from "./Mermaid";

interface CodeProps {
  className?: string;
  children?: string;
}

/**
 * Routes fenced code blocks by language:
 *   ```mermaid        → rendered diagram
 *   ```python         → runnable (Pyodide, numpy-first)
 *   ```python-static  → static highlight (e.g. torch examples Pyodide can't run)
 *   anything else     → static Shiki highlight
 */
export function MdxPre({ children }: { children?: ReactElement<CodeProps> }) {
  const codeProps = children?.props;
  const className = codeProps?.className ?? "";
  const lang = className.replace(/^language-/, "");
  const code = String(codeProps?.children ?? "").replace(/\n$/, "");

  if (lang === "mermaid") return <Mermaid code={code} />;
  if (lang === "python") return <PyRunner code={code} />;
  if (lang === "python-static") return <CodeBlock lang="python" code={code} />;
  return <CodeBlock lang={lang} code={code} />;
}
