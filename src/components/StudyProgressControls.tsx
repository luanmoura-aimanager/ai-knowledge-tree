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
  const [failed, setFailed] = useState(false);
  const [pending, startTransition] = useTransition();

  const apply = (next: ProgressStatus | null) => {
    const prev = status;
    setLocal(next);
    setFailed(false);
    startTransition(async () => {
      const res =
        next === null
          ? await clearStatus(itemKey)
          : await setStatus(itemKey, next);
      if (!res.ok) {
        setLocal(prev); // revert optimistic update so the UI never lies
        setFailed(true);
      }
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
      {failed && (
        <span className="text-xs text-[var(--hot)]">
          Couldn&apos;t save: please try again.
        </span>
      )}
    </div>
  );
}
