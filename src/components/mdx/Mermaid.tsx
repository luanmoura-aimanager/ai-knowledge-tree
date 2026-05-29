"use client";

import { useEffect, useRef, useState } from "react";

let mermaidReady: Promise<typeof import("mermaid").default> | null = null;

function loadMermaid() {
  if (!mermaidReady) {
    mermaidReady = import("mermaid").then((m) => {
      m.default.initialize({
        startOnLoad: false,
        theme: "dark",
        themeVariables: {
          background: "#141a35",
          primaryColor: "#1a2148",
          primaryBorderColor: "#353e75",
          primaryTextColor: "#e6e9f5",
          lineColor: "#9aa3c7",
          fontFamily: "ui-monospace, monospace",
          fontSize: "15px",
        },
      });
      return m.default;
    });
  }
  return mermaidReady;
}

let counter = 0;

/** Renders a Mermaid diagram from a fenced ```mermaid block. */
export function Mermaid({ code }: { code: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const id = `mermaid-${counter++}`;
    loadMermaid()
      .then((mermaid) => mermaid.render(id, code))
      .then(({ svg }) => {
        if (!cancelled && ref.current) ref.current.innerHTML = svg;
      })
      .catch((e) => {
        if (!cancelled) setError(String(e));
      });
    return () => {
      cancelled = true;
    };
  }, [code]);

  if (error) {
    return (
      <pre className="text-[var(--hot)] text-sm whitespace-pre-wrap">
        Mermaid error: {error}
      </pre>
    );
  }
  return (
    <div ref={ref} className="my-6 flex justify-center [&_svg]:max-w-full" />
  );
}
