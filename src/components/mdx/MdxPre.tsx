import type { ReactElement } from "react";
import { codeToHtml } from "shiki";
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
export async function MdxPre({
  children,
}: {
  children?: ReactElement<CodeProps>;
}) {
  const codeProps = children?.props;
  const className = codeProps?.className ?? "";
  const lang = className.replace(/^language-/, "");
  const code = String(codeProps?.children ?? "").replace(/\n$/, "");

  if (lang === "mermaid") return <Mermaid code={code} />;
  if (lang === "python") {
    // Highlight on the server (Shiki, same theme as static blocks) and hand the
    // markup to the client runner; the raw `code` still drives execution.
    const html = await codeToHtml(code, {
      lang: "python",
      theme: "tokyo-night",
    });
    return <PyRunner code={code} html={html} />;
  }
  if (lang === "python-static") return <CodeBlock lang="python" code={code} />;
  return <CodeBlock lang={lang} code={code} />;
}
