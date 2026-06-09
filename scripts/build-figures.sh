#!/bin/sh
# Regenerate all lesson figures (Path A). Runs every figures/gen/<sub>.py (skipping
# helpers prefixed with "_") and writes SVGs under public/figures/<sub>/.
#
# Generated SVGs are committed; this is a local authoring step, NOT part of the
# Vercel build (no Python in CI). Use a venv:
#   python3 -m venv figures/.venv
#   figures/.venv/bin/pip install -r figures/requirements.txt
#   npm run figures
set -e

cd "$(dirname "$0")/.."

# Prefer the project venv if present, else fall back to python3 on PATH.
if [ -x "figures/.venv/bin/python" ]; then
  PY="figures/.venv/bin/python"
else
  PY="python3"
fi

ran=0
for f in figures/gen/*.py; do
  [ -e "$f" ] || continue   # no-match glob stays literal under set -e; skip it
  case "$(basename "$f")" in
    _*) continue ;;  # skip _style.py and other helpers
  esac
  echo "→ $f"
  "$PY" "$f"
  ran=$((ran + 1))
done

echo "done: ran $ran figure script(s)."
