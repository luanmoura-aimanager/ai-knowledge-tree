"""Shared dark-native matplotlib theme + save helper for lesson figures (Path A).

Every ``figures/gen/<sub>.py`` script imports this, calls :func:`apply_style`
once, builds figures, and writes them with :func:`save`. Output lands in
``public/figures/<sub>/<name>.svg`` and is embedded in a lesson with
``![caption](/figures/<sub>/<name>.svg)``.

Design goals:
  * Dark-native — transparent background + light text so the SVG sits as a card
    on the dark site (#0a0e1f). See globals.css `.mdx-body img`.
  * Palette-matched — data uses the pillar accent colors (mirror of the
    `--pa..--pj` tokens in globals.css / dag.ts; kept here as a copy, same as
    the offline HTML export).
  * Deterministic — scripts seed `np.random.default_rng(0)` so re-running yields
    byte-identical SVGs and clean git diffs.
"""

from __future__ import annotations

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless; no display needed
import matplotlib.pyplot as plt  # noqa: E402

# --- Palette (mirror of --pa..--pj in src/app/globals.css / dag.ts) -----------
PILLAR = {
    "A": "#e0af68",
    "B": "#f7768e",
    "C": "#ff9e64",
    "D": "#7aa2f7",
    "E": "#bb9af7",
    "F": "#7dcfff",
    "G": "#73daca",
    "H": "#ff7eb6",
    "I": "#9ece6a",
    "J": "#c0caf5",
}

# Surface chrome (mirror of globals.css :root).
FG = "#e6e9f5"        # primary text
FG_DIM = "#9aa3c7"    # axis labels / ticks
FG_MUTE = "#6c7596"   # de-emphasized
GRID = "#242b52"      # grid + spines
GOOD = "#9ece6a"
HOT = "#f7768e"
ACCENT = PILLAR["D"]   # generic accent (= pillar D blue)
PARTIAL = PILLAR["A"]  # = pillar A gold

# A small ordered cycle for multi-series plots (distinct, palette-consistent).
CYCLE = ["#7aa2f7", "#f7768e", "#9ece6a", "#e0af68", "#bb9af7", "#7dcfff", "#ff9e64"]

# Background for framed legends placed over data (a touch lighter than --card).
LEGEND_BG = "#161c3a"

# Repo root = two levels up from this file (figures/gen/_style.py).
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_OUT = os.path.join(_ROOT, "public", "figures")


def apply_style() -> None:
    """Set dark-native rcParams sized for the 760px lesson column."""
    # NumPy 2.0's SIMD matmul can raise spurious FP-flag RuntimeWarnings on
    # benign products (platform-dependent, also from inside sklearn); they do
    # not indicate bad output. Suppress just those.
    warnings.filterwarnings(
        "ignore", message=".*encountered in matmul", category=RuntimeWarning
    )
    plt.rcParams.update(
        {
            "figure.figsize": (7.0, 4.0),
            "figure.dpi": 110,
            # Fixed salt → deterministic <defs> element ids across runs, so
            # re-running gives byte-identical SVGs (clean git diffs).
            "svg.hashsalt": "ai-knowledge-tree",
            "savefig.transparent": True,
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "savefig.facecolor": "none",
            "text.color": FG,
            "axes.labelcolor": FG_DIM,
            "axes.titlecolor": FG,
            "xtick.color": FG_DIM,
            "ytick.color": FG_DIM,
            "axes.edgecolor": GRID,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "grid.alpha": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.prop_cycle": plt.cycler(color=CYCLE),
            "font.size": 12,
            "axes.titlesize": 13,
            "legend.fontsize": 10,
            "legend.frameon": False,
            "lines.linewidth": 2.0,
            "font.family": "sans-serif",
        }
    )


def color(sub: str) -> str:
    """Pillar accent color for a subsection id, e.g. ``"C1" -> #ff9e64``."""
    return PILLAR[sub[0].upper()]


def save(fig, sub: str, name: str) -> None:
    """Write ``fig`` to public/figures/<sub>/<name>.svg and close it."""
    out_dir = os.path.join(_OUT, sub)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.svg")
    # metadata={"Date": None} drops the per-run <dc:date> timestamp so output is
    # byte-stable (paired with the fixed svg.hashsalt in apply_style).
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    rel = os.path.relpath(path, _ROOT)
    print(f"  wrote {rel}")
