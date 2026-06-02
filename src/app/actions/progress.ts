"use server";

import { revalidatePath } from "next/cache";
import { getPool } from "@/lib/db";
import { auth } from "@/auth";
import type { ProgressStatus } from "@/lib/progress";

/** Result of a progress mutation. `ok: false` lets the client revert its optimistic state. */
export type ProgressResult = { ok: boolean };

/** Upsert the study status for a lesson for the current user. Never throws. */
export async function setStatus(
  key: string,
  status: ProgressStatus,
): Promise<ProgressResult> {
  const pool = getPool();
  if (!pool) return { ok: false };
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return { ok: false };

  try {
    await pool.query(
      `INSERT INTO progress (user_id, sub_id, status, updated_at)
       VALUES ($1, $2, $3, now())
       ON CONFLICT (user_id, sub_id)
       DO UPDATE SET status = EXCLUDED.status, updated_at = now()`,
      [userId, key, status],
    );
  } catch (err) {
    console.error("setStatus failed", err);
    return { ok: false };
  }
  revalidatePath("/");
  return { ok: true };
}

/** Mark a lesson unstudied (removes the row). Never throws. */
export async function clearStatus(key: string): Promise<ProgressResult> {
  const pool = getPool();
  if (!pool) return { ok: false };
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return { ok: false };

  try {
    await pool.query(
      "DELETE FROM progress WHERE user_id = $1 AND sub_id = $2",
      [userId, key],
    );
  } catch (err) {
    console.error("clearStatus failed", err);
    return { ok: false };
  }
  revalidatePath("/");
  return { ok: true };
}
