"use client";

import { useState, useTransition } from "react";
import { setStatus, clearStatus } from "@/app/actions/progress";
import type { ProgressStatus } from "@/lib/progress";

/**
 * "Mark as studied" controls on a lesson page. `itemKey` is the global
 * progress key ("subId/lessonId"). Calls the progress server actions and
 * reflects the new state optimistically. Only rendered for signed-in users.
 */
export function StudyProgressControls({
  itemKey,
  initial,
}: {
  itemKey: string;
  initial: ProgressStatus | null;
}) {
  const [status, setLocal] = useState<ProgressStatus | null>(initial);
  const [pending, startTransition] = useTransition();

  const apply = (next: ProgressStatus | null) => {
    setLocal(next);
    startTransition(async () => {
      if (next === null) await clearStatus(itemKey);
      else await setStatus(itemKey, next);
    });
  };

  return (
    <div className="flex items-center gap-2 my-6 flex-wrap">
      <button
        className={`btn ${status === "studied" ? "active" : ""}`}
        disabled={pending}
        onClick={() => apply(status === "studied" ? null : "studied")}
      >
        {status === "studied" ? "✓ Studied" : "Mark as studied"}
      </button>
      <button
        className={`btn ${status === "in-progress" ? "active" : ""}`}
        disabled={pending}
        onClick={() => apply(status === "in-progress" ? null : "in-progress")}
      >
        ◐ In progress
      </button>
    </div>
  );
}
