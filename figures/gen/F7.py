"""Figures for pillar F7 (latent-variable models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "F7"
C = color(SUB)  # pillar-F accent (cyan)


def em_algorithm() -> None:
    """EM fits a latent-variable model by alternating soft assignments (E-step) with
    parameter updates (M-step); each round can only raise the data log-likelihood, so
    it climbs monotonically to a local optimum. Left: the fitted Gaussian mixture;
    right: the log-likelihood per iteration. rng(0)."""
    import warnings

    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    from sklearn.exceptions import ConvergenceWarning
    from sklearn.mixture import GaussianMixture

    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal([0, 0], 0.6, (120, 2)),
                   rng.normal([3, 1], 0.5, (120, 2)),
                   rng.normal([1.5, 3], 0.7, (120, 2))])
    ll = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        for n in range(1, 26):
            gm = GaussianMixture(3, max_iter=n, n_init=1, init_params="random",
                                 random_state=0, tol=1e-9).fit(X)
            ll.append(gm.score(X) * len(X))
    gm = GaussianMixture(3, random_state=0).fit(X)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.0))
    ax1.scatter(X[:, 0], X[:, 1], s=8, color=FG_MUTE, alpha=0.5)
    for k, col in enumerate([C, HOT, GOOD]):
        m = gm.means_[k]; cov = gm.covariances_[k]
        vals, vecs = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
        for s in (1, 2):
            ax1.add_patch(Ellipse(m, 2 * s * np.sqrt(vals[0]), 2 * s * np.sqrt(vals[1]),
                                  angle=ang, fill=False, color=col, lw=1.8, alpha=0.9))
    ax1.set_title("Fitted Gaussian mixture"); ax1.set_aspect("equal")
    ax1.set_xticks([]); ax1.set_yticks([])
    ax2.plot(range(1, 26), ll, "-o", color=C, ms=3.5)
    ax2.set_title("Log-likelihood increases each step")
    ax2.set_xlabel("EM iteration"); ax2.set_ylabel("data log-likelihood")
    fig.tight_layout()
    save(fig, SUB, "em-algorithm")


def probabilistic_pca() -> None:
    """Probabilistic PCA models data as a low-dimensional latent coordinate mapped
    through a linear subspace plus isotropic Gaussian noise. The fitted principal
    axis recovers the signal direction; the noise sets the spread around it. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 300
    z = rng.normal(0, 1.6, n)
    w = np.array([2.0, 1.0])
    X = z[:, None] * w + rng.normal(0, 0.4, (n, 2))
    Xc = X - X.mean(0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    d = Vt[0]

    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    ax.scatter(X[:, 0], X[:, 1], s=12, color=C, alpha=0.5, edgecolor="none")
    t = np.linspace(-6, 6, 2)
    ax.plot(t * d[0], t * d[1], color=HOT, lw=2.6, label="principal axis $W$")
    ax.set_aspect("equal")
    ax.set_title("Probabilistic PCA: latent line + isotropic noise")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "probabilistic-pca")


def main() -> None:
    apply_style()
    em_algorithm()
    probabilistic_pca()


if __name__ == "__main__":
    main()
