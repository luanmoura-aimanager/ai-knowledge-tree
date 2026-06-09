"""Figures for pillar C8 (recommenders). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, GRID, apply_style, color, save

SUB = "C8"
C = color(SUB)  # pillar-C accent


def matrix_factorization() -> None:
    """Matrix factorization explains a sparse rating matrix as a low-rank product
    U Vᵀ: a few latent factors per user and item reconstruct the full matrix and
    fill in the missing entries. rng(0), rank-4 signal."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    nu, ni, k = 40, 30, 4
    U = rng.normal(size=(nu, k))
    V = rng.normal(size=(ni, k))
    R = U @ V.T + 0.3 * rng.normal(size=(nu, ni))
    # rank-k reconstruction via truncated SVD of the (fully observed) matrix
    Us, s, Vt = np.linalg.svd(R, full_matrices=False)
    Rhat = (Us[:, :k] * s[:k]) @ Vt[:k]

    vmax = np.abs(R).max()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.0))
    for ax, M, ttl in [(ax1, R, "observed ratings R"),
                       (ax2, Rhat, "rank-4 reconstruction $UV^\\top$")]:
        im = ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
        ax.set_title(ttl)
        ax.set_xlabel("items"); ax.grid(False)
    ax1.set_ylabel("users")
    cb = fig.colorbar(im, ax=(ax1, ax2), fraction=0.04, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    save(fig, SUB, "matrix-factorization")


def main() -> None:
    apply_style()
    matrix_factorization()


if __name__ == "__main__":
    main()
