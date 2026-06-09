"""Figures for pillar D5 (self-supervised learning). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, GRID, apply_style, color, save

SUB = "D5"
C = color(SUB)  # pillar-D accent (blue)


def contrastive_ssl() -> None:
    """Contrastive learning aligns two augmented views of the same item and repels
    views of different items: the similarity matrix between the two view-batches
    therefore has a bright diagonal (positive pairs) and dim off-diagonal (negatives)
    — exactly what the InfoNCE loss sharpens. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, d = 16, 32
    z1 = rng.normal(size=(n, d))
    z2 = z1 + 0.35 * rng.normal(size=(n, d))     # second view = same item + augmentation
    z1 /= np.linalg.norm(z1, axis=1, keepdims=True)
    z2 /= np.linalg.norm(z2, axis=1, keepdims=True)
    sim = z1 @ z2.T

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    im = ax.imshow(sim, cmap="magma", vmin=-0.3, vmax=1.0)
    ax.set_title("Similarity matrix: positives on the diagonal")
    ax.set_xlabel("view 2 (item index)")
    ax.set_ylabel("view 1 (item index)")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("cosine similarity", color=FG_DIM)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    fig.tight_layout()
    save(fig, SUB, "contrastive-ssl")


def main() -> None:
    apply_style()
    contrastive_ssl()


if __name__ == "__main__":
    main()
