"use client";

import { useRef, useState } from "react";

const PYODIDE_VERSION = "0.27.2";
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

interface Pyodide {
  loadPackage: (names: string[]) => Promise<void>;
  setStdout: (opts: { batched: (s: string) => void }) => void;
  setStderr: (opts: { batched: (s: string) => void }) => void;
  runPythonAsync: (code: string) => Promise<unknown>;
}

declare global {
  interface Window {
    loadPyodide?: (opts: { indexURL: string }) => Promise<Pyodide>;
  }
}

// Shared across every PyRunner on the page: load the heavy WASM runtime once.
let pyodidePromise: Promise<Pyodide> | null = null;

function getPyodide(): Promise<Pyodide> {
  if (pyodidePromise) return pyodidePromise;
  pyodidePromise = (async () => {
    if (!window.loadPyodide) {
      await new Promise<void>((resolve, reject) => {
        const s = document.createElement("script");
        s.src = `${PYODIDE_URL}pyodide.js`;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error("Failed to load Pyodide"));
        document.head.appendChild(s);
      });
    }
    const pyodide = await window.loadPyodide!({ indexURL: PYODIDE_URL });
    await pyodide.loadPackage(["numpy"]);
    return pyodide;
  })();
  return pyodidePromise;
}

/**
 * Runnable Python block. Loads Pyodide (numpy preloaded) lazily on the first
 * "Run" so the dashboard and unopened pages pay no WASM cost.
 */
export function PyRunner({ code, html }: { code: string; html?: string }) {
  const [output, setOutput] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "running">("idle");
  const bufRef = useRef("");

  const run = async () => {
    setStatus(pyodidePromise ? "running" : "loading");
    setOutput(null);
    bufRef.current = "";
    try {
      const pyodide = await getPyodide();
      setStatus("running");
      const sink = { batched: (s: string) => (bufRef.current += s + "\n") };
      pyodide.setStdout(sink);
      pyodide.setStderr(sink);
      const result = await pyodide.runPythonAsync(code);
      if (result !== undefined && result !== null) {
        bufRef.current += String(result) + "\n";
      }
      setOutput(bufRef.current.trimEnd() || "(no output)");
    } catch (e) {
      setOutput(String(e));
    } finally {
      setStatus("idle");
    }
  };

  return (
    <div className="my-6 rounded-xl border border-[var(--border)] overflow-hidden">
      <div className="flex items-center justify-between px-3 py-2 bg-[var(--card-2)] border-b border-[var(--border)]">
        <span className="text-xs font-mono text-[var(--fg-mute)]">
          python · numpy
        </span>
        <button
          className="btn"
          onClick={run}
          disabled={status !== "idle"}
          style={{ padding: "4px 12px" }}
        >
          {status === "loading"
            ? "Loading runtime…"
            : status === "running"
              ? "Running…"
              : "▶ Run"}
        </button>
      </div>
      {html ? (
        <div
          className="text-sm [&_pre]:m-0 [&_pre]:p-4 [&_pre]:overflow-x-auto"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      ) : (
        <pre className="m-0 p-4 text-sm overflow-x-auto bg-[var(--card)] text-[var(--fg)]">
          <code>{code}</code>
        </pre>
      )}
      {output !== null && (
        <div className="border-t border-[var(--border)]">
          <div className="px-3 py-1 text-xs uppercase tracking-wider text-[var(--fg-mute)] bg-[var(--card-2)]">
            output
          </div>
          <pre className="m-0 p-4 text-sm overflow-x-auto bg-[#0a0e1f] text-[var(--good)] whitespace-pre-wrap">
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
