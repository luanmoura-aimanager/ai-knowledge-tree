-- AI Knowledge Tree — database schema (Neon Postgres).
-- Run once against your Neon database:  psql "$DATABASE_URL" -f schema.sql
--
-- Auth.js (@auth/pg-adapter) tables + a per-user progress table.

-- ---- Auth.js core tables (schema required by @auth/pg-adapter) ------------
CREATE TABLE IF NOT EXISTS users (
  id            UUID NOT NULL DEFAULT gen_random_uuid(),
  name          VARCHAR(255),
  email         VARCHAR(255),
  "emailVerified" TIMESTAMPTZ,
  image         TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS accounts (
  id                  UUID NOT NULL DEFAULT gen_random_uuid(),
  "userId"            UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type                VARCHAR(255) NOT NULL,
  provider            VARCHAR(255) NOT NULL,
  "providerAccountId" VARCHAR(255) NOT NULL,
  refresh_token       TEXT,
  access_token        TEXT,
  expires_at          BIGINT,
  id_token            TEXT,
  scope               TEXT,
  session_state       TEXT,
  token_type          TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sessions (
  id             UUID NOT NULL DEFAULT gen_random_uuid(),
  "userId"       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  "sessionToken" VARCHAR(255) NOT NULL,
  expires        TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS verification_token (
  identifier TEXT NOT NULL,
  expires    TIMESTAMPTZ NOT NULL,
  token      TEXT NOT NULL,
  PRIMARY KEY (identifier, token)
);

-- ---- Per-user study progress ---------------------------------------------
-- status: 'in-progress' | 'studied'. Absence of a row = 'unstudied'.
CREATE TABLE IF NOT EXISTS progress (
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  sub_id     VARCHAR(8) NOT NULL,
  status     VARCHAR(16) NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, sub_id)
);

CREATE INDEX IF NOT EXISTS progress_user_idx ON progress(user_id);
