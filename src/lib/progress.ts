import "server-only";
import { getPool } from "./db";
import { auth } from "@/auth";

export type ProgressStatus = "in-progress" | "studied";
export type ProgressMap = Map<string, ProgressStatus>;

/** True when a user is authenticated (and a DB is configured). */
export async function isSignedIn(): Promise<boolean> {
  if (!getPool()) return false;
  const session = await auth();
  return Boolean(session?.user?.id);
}

/** Progress for the signed-in user as a "subId/lessonId" → status map (empty if anon/no DB). */
export async function getProgressMap(): Promise<ProgressMap> {
  const pool = getPool();
  if (!pool) return new Map();
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return new Map();

  const { rows } = await pool.query<{ sub_id: string; status: ProgressStatus }>(
    "SELECT sub_id, status FROM progress WHERE user_id = $1",
    [userId],
  );
  return new Map(rows.map((r) => [r.sub_id, r.status]));
}

/** The most recently touched lesson, for the "resume" link. `key` is "subId/lessonId". */
export async function getResume(): Promise<{
  key: string;
  status: ProgressStatus;
} | null> {
  const pool = getPool();
  if (!pool) return null;
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) return null;

  const { rows } = await pool.query<{ sub_id: string; status: ProgressStatus }>(
    "SELECT sub_id, status FROM progress WHERE user_id = $1 ORDER BY updated_at DESC LIMIT 1",
    [userId],
  );
  return rows[0] ? { key: rows[0].sub_id, status: rows[0].status } : null;
}
