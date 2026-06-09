"""Figures for pillar E2 (word & contextual embeddings). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, GOOD, HOT, apply_style, color, save

SUB = "E2"
C = color(SUB)  # pillar-E accent (purple)


def word2vec() -> None:
    """word2vec embeddings encode relations as directions: the vector from "man" to
    "woman" is nearly parallel to "king"→"queen", so analogies become vector
    arithmetic — king − man + woman lands next to queen. (A hand-built 2D sketch of
    that learned structure.)"""
    import matplotlib.pyplot as plt

    pts = {
        "man": (0.0, 0.0), "woman": (0.0, 1.2),
        "king": (2.2, 0.2), "queen": (2.2, 1.4),
    }
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    for w, (x, y) in pts.items():
        ax.scatter(x, y, s=70, color=C, zorder=3)
        ax.annotate(w, (x, y), color=FG_DIM, fontsize=11,
                    xytext=(6, 4), textcoords="offset points")
    # gender direction (two parallel arrows)
    for (a, b), col in [(("man", "woman"), GOOD), (("king", "queen"), GOOD)]:
        ax.annotate("", xy=pts[b], xytext=pts[a],
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
    # analogy: king - man + woman ≈ queen
    pred = (pts["king"][0] - pts["man"][0] + pts["woman"][0],
            pts["king"][1] - pts["man"][1] + pts["woman"][1])
    ax.scatter(*pred, s=120, facecolor="none", edgecolor=HOT, lw=2.0, zorder=4)
    ax.annotate("king − man + woman", pred, color=HOT, fontsize=9,
                xytext=(6, -14), textcoords="offset points")
    ax.set_title("Analogies as vector arithmetic")
    ax.set_xlabel("embedding dim 1"); ax.set_ylabel("embedding dim 2")
    ax.set_xlim(-0.6, 3.2); ax.set_ylim(-0.5, 2.0)
    fig.tight_layout()
    save(fig, SUB, "word2vec")


def main() -> None:
    apply_style()
    word2vec()


if __name__ == "__main__":
    main()
