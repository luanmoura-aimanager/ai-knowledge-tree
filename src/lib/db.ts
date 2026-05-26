import "server-only";
import { Pool } from "@neondatabase/serverless";

/**
 * Lazily-created Neon connection pool. Returns null when no connection string
 * is set, so the site runs in anonymous-only mode (public pages, no auth/
 * progress) without a database.
 *
 * Different Neon/Vercel setups name the pooled connection string differently,
 * so we accept the common variants.
 */
function getDatabaseUrl(): string | undefined {
  return (
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.DATABASE_URL_UNPOOLED ||
    process.env.POSTGRES_PRISMA_URL
  );
}

let pool: Pool | null = null;

export function getPool(): Pool | null {
  const url = getDatabaseUrl();
  if (!url) return null;
  if (!pool) pool = new Pool({ connectionString: url });
  return pool;
}

/** True when a database is configured (auth + progress features are active). */
export function dbEnabled(): boolean {
  return Boolean(getDatabaseUrl());
}
