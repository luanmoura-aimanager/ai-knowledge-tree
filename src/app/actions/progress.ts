"use server";

import { revalidatePath } from "next/cache";
import { getPool } from "@/lib/db";
import { auth } from "@/auth";
import type { ProgressStatus } from "@/lib/progress";

/** Upsert the study status for a subsection for the current user. */
export async function setStatus(subId: string, status: ProgressStatus) {
  const pool = getPool();
  if (!pool) return;
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return;

  await pool.query(
    `INSERT INTO progress (user_id, sub_id, status, updated_at)
     VALUES ($1, $2, $3, now())
     ON CONFLICT (user_id, sub_id)
     DO UPDATE SET status = EXCLUDED.status, updated_at = now()`,
    [userId, subId, status],
  );
  revalidatePath("/");
}

/** Mark a subsection unstudied (removes the row). */
export async function clearStatus(subId: string) {
  const pool = getPool();
  if (!pool) return;
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return;

  await pool.query("DELETE FROM progress WHERE user_id = $1 AND sub_id = $2", [
    userId,
    subId,
  ]);
  revalidatePath("/");
}
