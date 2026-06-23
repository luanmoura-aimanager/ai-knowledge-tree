import type { PathStep } from "@/lib/types";

/** ai-math-theory chapter labels, keyed by the chapter number parsed from a step's note. */
export const AMT_CHAPTERS: Record<string, string> = {
  "0": "Ch0 · Math foundations",
  "1": "Ch1 · Linear models & the perceptron",
  "2": "Ch2 · MLPs & backprop",
  "3": "Ch3 · Optimization & regularization",
  "4": "Ch4 · CNN bridge",
  "5": "Ch5 · Sequence modeling & embeddings",
  "6": "Ch6 · Attention & the Transformer",
  "7": "Ch7 · Training language models",
  "8": "Ch8 · Modern LLM architectures",
  "9": "Ch9 · Alignment",
  "10": "Ch10 · Inference & decoding",
  "11": "Ch11 · Interpretability & the frontier",
  "12": "Ch12 · Capstone: build a tiny GPT",
};

/** The chapter number a `note` belongs to (its leading integer), or "". */
export function chapterOf(note?: string): string {
  return note?.match(/\d+/)?.[0] ?? "";
}

/**
 * The heading a step is grouped under. An explicit `section` wins (curated
 * role-paths); otherwise fall back to the ai-math-theory chapter parsed from the
 * note (the LLM Theory mirror). Empty string means "no header".
 */
export function groupLabelOf(step: Pick<PathStep, "section" | "note">): string {
  if (step.section) return step.section;
  const ch = chapterOf(step.note);
  return AMT_CHAPTERS[ch] ?? ch;
}
