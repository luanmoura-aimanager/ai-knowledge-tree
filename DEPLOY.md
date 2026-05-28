# Deploy: AI Knowledge Tree

The app runs in two modes:

- **Anonymous-only** (no env vars): the dashboard, connections graph, and every
  study page work. Sign-in and progress tracking are hidden.
- **Full** (DB + Google OAuth configured): visitors can sign in with Google and
  the dashboard reflects their own study progress.

The steps below are **yours to run**: they need interactive auth and a Vercel
account. The Vercel CLI is not installed yet.

## 1. Install the Vercel CLI and link the project

```bash
npm i -g vercel
vercel login          # interactive
vercel link           # creates the Vercel project
```

## 2. Provision the database (Neon, via Vercel Marketplace)

In the Vercel dashboard → your project → **Storage** → add **Neon Postgres**
(or `vercel install neon`). This auto-injects a `DATABASE_URL`-style variable
into the project's environments. Then create the tables:

```bash
vercel env pull .env.local          # pulls DATABASE_URL locally
psql "$(grep DATABASE_URL .env.local | cut -d= -f2- | tr -d '\"')" -f schema.sql
```

(`schema.sql` is in the repo root: Auth.js tables + the `progress` table.)

## 3. Google OAuth credentials

Google Cloud Console → **APIs & Services → Credentials → Create OAuth client ID**
(type: Web application). Add **Authorized redirect URIs** for every origin:

```
http://localhost:3000/api/auth/callback/google      # local dev
https://<your-preview-domain>/api/auth/callback/google
https://<your-prod-domain>/api/auth/callback/google
```

Copy the client ID and secret.

## 4. Set environment variables

```bash
# one-time secret for Auth.js
npx auth secret                       # prints AUTH_SECRET (or: openssl rand -base64 33)

vercel env add AUTH_SECRET            # paste value, select Production + Preview
vercel env add AUTH_GOOGLE_ID
vercel env add AUTH_GOOGLE_SECRET
# DATABASE_URL was added automatically by the Neon integration
```

For local dev, mirror these into `.env.local` (see `.env.example`).

## 5. Deploy

```bash
vercel                  # preview deploy (per-branch URL)
vercel --prod           # promote to production
```

Verify on the deployed URL: sign in with Google, mark a subsection studied,
reload: the dashboard stats and per-subsection badges should reflect your
progress; sign out and they revert to the domain view.
