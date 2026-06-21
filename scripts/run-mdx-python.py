#!/usr/bin/env python3
"""Extract and execute every runnable ```python block in the given .mdx files.

Each block runs in its own fresh namespace (like a PyRunner cell). A failing
block (exception or failed assert) reports the file, block index, and error,
and the script exits nonzero. Usage:

    figures/.venv/bin/python scripts/run-mdx-python.py content/L-calculus/L1
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCK_RE = re.compile(r"^```python\n(.*?)^```", re.M | re.S)


def main() -> int:
    targets: list[Path] = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        targets.extend(sorted(p.rglob("*.mdx")) if p.is_dir() else [p])
    if not targets:
        print("no .mdx files found", file=sys.stderr)
        return 2

    failures = 0
    for f in targets:
        blocks = BLOCK_RE.findall(f.read_text())
        for i, code in enumerate(blocks, 1):
            try:
                exec(compile(code, f"{f}#block{i}", "exec"), {"__name__": "__main__"})
                print(f"PASS {f.name} block {i}")
            except Exception as e:  # noqa: BLE001
                failures += 1
                print(f"FAIL {f.name} block {i}: {type(e).__name__}: {e}")
    print(f"\n{failures} failing block(s)" if failures else "\nall blocks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
