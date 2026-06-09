"""Figures for pillar C4 (distance-based methods). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, HOT, apply_style, color, save

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


def fisher_lda() -> None:
    """Fisher's LDA finds the direction that maximizes between-class separation
    relative to within-class spread: two overlapping 2D clouds collapse to cleanly
    separated 1D histograms along that axis. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    rng = np.random.default_rng(0)
    n = 200
    cov = np.array([[1.0, 0.8], [0.8, 1.0]])
    X0 = rng.multivariate_normal([0, 0], cov, n)
    X1 = rng.multivariate_normal([2, 2], cov, n)
    X = np.vstack([X0, X1]); y = np.array([0] * n + [1] * n)
    w = LinearDiscriminantAnalysis().fit(X, y).coef_[0]
    w = w / np.linalg.norm(w)
    proj = X @ w

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.scatter(X0[:, 0], X0[:, 1], s=12, color=ACCENT, alpha=0.5, edgecolor="none")
    ax1.scatter(X1[:, 0], X1[:, 1], s=12, color=HOT, alpha=0.5, edgecolor="none")
    c = X.mean(0)
    ax1.annotate("", xy=c + 2.5 * w, xytext=c - 2.5 * w,
                 arrowprops=dict(arrowstyle="<->", color=C, lw=2.4))
    ax1.set_title("2D data + Fisher axis"); ax1.set_aspect("equal")
    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax2.hist(proj[y == 0], bins=25, color=ACCENT, alpha=0.6, label="class 0")
    ax2.hist(proj[y == 1], bins=25, color=HOT, alpha=0.6, label="class 1")
    ax2.set_title("Projected onto the Fisher axis")
    ax2.set_xlabel("projection"); ax2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "fisher-lda")


def lda_qda() -> None:
    """LDA assumes one shared covariance, so its boundaries are linear; QDA gives
    each class its own covariance, so its boundaries curve to fit elliptical
    classes. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.discriminant_analysis import (
        LinearDiscriminantAnalysis as LDA,
        QuadraticDiscriminantAnalysis as QDA)

    rng = np.random.default_rng(0)
    n = 200
    blobs = [([2, 0], [[0.6, 0.4], [0.4, 0.6]]),
             ([-2, 0], [[0.6, -0.4], [-0.4, 0.6]]),
             ([0, 2.5], [[1.4, 0], [0, 0.3]])]
    X = np.vstack([rng.multivariate_normal(m, c, n) for m, c in blobs])
    y = np.array([0] * n + [1] * n + [2] * n)
    gx, gy = np.meshgrid(np.linspace(-5, 5, 300), np.linspace(-3, 5, 300))
    grid = np.c_[gx.ravel(), gy.ravel()]
    cols = [ACCENT, HOT, GOOD]

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))
    for ax, model, ttl in [(axes[0], LDA(), "LDA: linear boundaries"),
                           (axes[1], QDA(), "QDA: quadratic boundaries")]:
        Z = model.fit(X, y).predict(grid).reshape(gx.shape)
        ax.contourf(gx, gy, Z, levels=[-0.5, 0.5, 1.5, 2.5], colors=cols, alpha=0.2)
        for ci in range(3):
            ax.scatter(X[y == ci, 0], X[y == ci, 1], s=8, color=cols[ci], edgecolor="none")
        ax.set_title(ttl); ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    save(fig, SUB, "lda-qda")


def naive_bayes() -> None:
    """Gaussian naive Bayes assumes the features are independent within each class,
    so its per-class densities are axis-aligned and the decision boundary stays
    simple — often good enough even when independence does not hold. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.naive_bayes import GaussianNB

    rng = np.random.default_rng(0)
    n = 200
    X0 = rng.normal([1.0, -0.5], [1.0, 0.7], (n, 2))
    X1 = rng.normal([-1.0, 0.7], [0.7, 1.0], (n, 2))
    X = np.vstack([X0, X1]); y = np.array([0] * n + [1] * n)
    nb = GaussianNB().fit(X, y)
    gx, gy = np.meshgrid(np.linspace(-4, 4, 300), np.linspace(-4, 4, 300))
    Z = nb.predict_proba(np.c_[gx.ravel(), gy.ravel()])[:, 1].reshape(gx.shape)

    fig, ax = plt.subplots(figsize=(6.0, 4.8))
    ax.contourf(gx, gy, Z, levels=12, cmap="RdBu_r", alpha=0.5, vmin=0, vmax=1)
    ax.contour(gx, gy, Z, levels=[0.5], colors=[FG_MUTE], linewidths=2.0)
    ax.scatter(X0[:, 0], X0[:, 1], s=10, color=ACCENT, edgecolor="none")
    ax.scatter(X1[:, 0], X1[:, 1], s=10, color=HOT, edgecolor="none")
    ax.set_title("Gaussian naive Bayes boundary")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "naive-bayes")


def main() -> None:
    apply_style()
    fisher_lda()
    lda_qda()
    naive_bayes()
    curse_of_dimensionality()
    knn()


if __name__ == "__main__":
    main()
