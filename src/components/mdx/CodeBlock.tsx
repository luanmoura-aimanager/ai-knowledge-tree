import { codeToHtml } from "shiki";

/**
 * Static, syntax-highlighted code block (Shiki, Tokyo Night). Async server
 * component: highlighting happens at render time, no client JS.
 */
export async function CodeBlock({
  lang,
  code,
}: {
  lang: string;
  code: string;
}) {
  const html = await codeToHtml(code, {
    lang: lang || "text",
    theme: "tokyo-night",
  });
  return (
    <div
      className="my-6 rounded-xl border border-[var(--border)] overflow-hidden text-sm [&_pre]:m-0 [&_pre]:p-4 [&_pre]:overflow-x-auto"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
