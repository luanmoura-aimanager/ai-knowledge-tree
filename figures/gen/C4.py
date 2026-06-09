"""Figures for pillar C4 (distance-based methods). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "C4"
C = color(SUB)  # pillar-C accent


def curse_of_dimensionality() -> None:
    """Distance concentration: as the dimension grows, pairwise distances between
    uniform points bunch together — (max−min)/min collapses toward 0, so 'nearest'
    and 'farthest' become almost indistinguishable. rng(0), n=200 in [0,1]^d."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    dims = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    ratio, relspread = [], []
    for d in dims:
        Xp = rng.random((200, d))
        # pairwise distances from point 0 to the rest
        dist = np.linalg.norm(Xp[1:] - Xp[0], axis=1)
        ratio.append((dist.max() - dist.min()) / dist.min())
        relspread.append(dist.std() / dist.mean())

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(dims, ratio, "-o", color=C, ms=4, label="(max − min) / min distance")
    ax.plot(dims, relspread, "-o", color=HOT, ms=4, label="std / mean distance")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Distances concentrate in high dimensions")
    ax.set_xlabel("dimension $d$")
    ax.set_ylabel("relative spread of distances")
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, SUB, "curse-of-dimensionality")


def knn() -> None:
    """k-NN test error is U-shaped in k: k=1 overfits (high variance), large k
    oversmooths across the classes (high bias); the best k is in between. Two
    overlapping Gaussian blobs, rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.neighbors import KNeighborsClassifier

    rng = np.random.default_rng(0)
    npc = 250
    X = np.vstack([rng.normal([1.1, 0.4], 1.0, (npc, 2)),
                   rng.normal([-1.1, -0.4], 1.0, (npc, 2))])
    y = np.array([1] * npc + [0] * npc)
    perm = rng.permutation(len(y))
    Xtr, ytr = X[perm[:300]], y[perm[:300]]
    Xte, yte = X[perm[300:]], y[perm[300:]]

    ks = [1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 160]
    tr_err, te_err = [], []
    for k in ks:
        knn = KNeighborsClassifier(n_neighbors=k).fit(Xtr, ytr)
        tr_err.append(1 - knn.score(Xtr, ytr))
        te_err.append(1 - knn.score(Xte, yte))
    best = ks[int(np.argmin(te_err))]

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(ks, tr_err, "-o", color=FG_MUTE, ms=4, label="training error")
    ax.plot(ks, te_err, "-o", color=C, ms=4, lw=2.2, label="test error")
    ax.axvline(best, color=ACCENT, ls=":", lw=1.4, label=f"best k = {best}")
    ax.set_xscale("log")
    ax.set_title("k-NN: the U-shaped test error")
    ax.set_xlabel("number of neighbors $k$  (← more flexible | smoother →)")
    ax.set_ylabel("error rate")
    ax.legend(loc="upper center")
    fig.tight_layout()
    save(fig, SUB, "knn")


def main() -> None:
    apply_style()
    curse_of_dimensionality()
    knn()


if __name__ == "__main__":
    main()
