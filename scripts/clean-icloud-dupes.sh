#!/usr/bin/env sh
# Remove iCloud Drive conflict-copy duplicates that sync creates inside the
# repo: files named like "name 2.ext" / "thing.d 3.ts". They are never
# intentional, they break `tsc` (duplicate identifiers) and clutter the tree,
# and they are the reason `git add -A` is banned here (see CLAUDE.md / memory).
#
# Run automatically before `dev` and `build` (npm pre-hooks), or on demand:
#   npm run clean:dupes
#
# Scoped to the repo, skipping .git and node_modules. The glob "* [0-9].*"
# matches a space + single digit immediately before the extension, which is
# exactly the iCloud pattern; real files here use kebab-case (no spaces).
set -eu

root="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

# -print before -delete so the run is auditable in CI / logs.
find "$root" \
  \( -name node_modules -o -name .git \) -prune -o \
  -type f -name '* [0-9].*' -print -delete
