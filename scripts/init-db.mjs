import { readFileSync } from "node:fs";
import { Pool, neonConfig } from "@neondatabase/serverless";

// Use the runtime's global WebSocket (Node 22+) for the Neon driver.
neonConfig.webSocketConstructor = globalThis.WebSocket;

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL not set");
  process.exit(1);
}

const sql = readFileSync(new URL("../schema.sql", import.meta.url), "utf8");
const pool = new Pool({ connectionString: url });

await pool.query(sql);

const { rows } = await pool.query(
  "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name",
);
console.log("Tables:", rows.map((r) => r.table_name).join(", "));

await pool.end();
