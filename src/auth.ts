import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import PostgresAdapter from "@auth/pg-adapter";
import { getPool } from "@/lib/db";

/**
 * Auth.js (NextAuth v5) with Google. Wired to Neon via the Postgres adapter
 * with database sessions. When DATABASE_URL is unset (local dev without a DB)
 * the adapter and providers are empty, so `auth()` simply returns no session
 * and the site stays in anonymous-only mode.
 */
const pool = getPool();

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: pool ? PostgresAdapter(pool) : undefined,
  providers: pool ? [Google] : [],
  session: { strategy: "database" },
  callbacks: {
    session({ session, user }) {
      if (session.user && user) session.user.id = user.id;
      return session;
    },
  },
});
