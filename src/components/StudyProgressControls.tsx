"use client";

import { useRef, useState, useTransition } from "react";
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
  // Last status the server actually accepted; the baseline to revert to on
  // failure (so overlapping toggles never revert to a stale optimistic value).
  const confirmed = useRef<ProgressStatus | null>(initial);

  const apply = (next: ProgressStatus | null) => {
    setLocal(next);
    setFailed(false);
    startTransition(async () => {
      const res =
        next === null
          ? await clearStatus(itemKey)
          : await setStatus(itemKey, next);
      if (res.ok) {
        confirmed.current = next;
      } else {
        setLocal(confirmed.current); // revert so the UI never lies
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
