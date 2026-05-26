import type { Topic } from "@/lib/types";

const STATUS_GLYPH: Record<Topic["status"], string> = {
  covered: "✓",
  partial: "◐",
  gap: "○",
};

export function TopicChip({ topic }: { topic: Topic }) {
  return (
    <div
      className="topic"
      data-status={topic.status}
      data-hot={topic.hot ? "true" : "false"}
      data-name={topic.name.toLowerCase()}
    >
      <span className="ic">{STATUS_GLYPH[topic.status]}</span>
      <span className="name">{topic.name}</span>
      {topic.hot && <span className="flame">★</span>}
    </div>
  );
}
