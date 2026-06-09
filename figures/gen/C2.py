"""Figures for pillar C2 (SVMs & kernels). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "C2"
C = color(SUB)  # pillar-C accent


def _scatter_two(ax, X, y):
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=20, color=HOT, edgecolor="none", zorder=3)
    ax.scatter(X[y == -1, 0], X[y == -1, 1], s=20, color=ACCENT, edgecolor="none", zorder=3)


def hard_margin_svm() -> None:
    """The maximum-margin separator: the widest band that fits between two
    linearly separable classes; the points touching it are the support vectors.
    Lesson's setup: rng(0), 30/class."""
    import matplotlib.pyplot as plt
    from sklearn.svm import SVC

    rng = np.random.default_rng(0)
    n = 30
    X = np.vstack([rng.normal([2.5, 1.0], 0.6, (n, 2)),
                   rng.normal([-1.0, -1.0], 0.6, (n, 2))])
    y = np.array([1] * n + [-1] * n)
    clf = SVC(kernel="linear", C=1e6).fit(X, y)  # large C ≈ hard margin

    gx, gy = np.meshgrid(np.linspace(-3, 4.5, 300), np.linspace(-3.5, 3.5, 300))
    Z = clf.decision_function(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)

    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    _scatter_two(ax, X, y)
    ax.contour(gx, gy, Z, levels=[-1, 0, 1], colors=[FG_MUTE, C, FG_MUTE],
               linestyles=["--", "-", "--"], linewidths=[1.2, 2.2, 1.2])
    sv = clf.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=130, facecolors="none", edgecolors=GOOD,
               linewidths=2.0, label="support vectors", zorder=4)
    ax.set_title("Hard-margin SVM: the widest separating band")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right", frameon=True, facecolor="#161c3a",
              edgecolor=GRID, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "hard-margin-svm")


def soft_margin_svm() -> None:
    """With overlapping classes the soft margin trades a wider band for some
    margin violations; C controls the trade — small C = wide, forgiving margin,
    large C = narrow margin that fits the data harder. rng(0), n=200."""
    import matplotlib.pyplot as plt
    from sklearn.svm import SVC

    rng = np.random.default_rng(0)
    n = 100
    X = np.vstack([rng.normal([0.9, 0], 1.0, (n, 2)),
                   rng.normal([-0.9, 0], 1.0, (n, 2))])
    y = np.array([1] * n + [-1] * n)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))
    for ax, Cval in zip(axes, [0.05, 100.0]):
        clf = SVC(kernel="linear", C=Cval).fit(X, y)
        gx, gy = np.meshgrid(np.linspace(-4, 4, 250), np.linspace(-4, 4, 250))
        Z = clf.decision_function(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
        _scatter_two(ax, X, y)
        ax.contour(gx, gy, Z, levels=[-1, 0, 1], colors=[FG_MUTE, C, FG_MUTE],
                   linestyles=["--", "-", "--"], linewidths=[1.0, 2.0, 1.0])
        ax.set_title(f"C = {Cval:g}  ({'wide' if Cval < 1 else 'narrow'} margin)")
        ax.set_xlabel("$x_1$")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
    axes[0].set_ylabel("$x_2$")
    fig.suptitle("Soft-margin SVM: the regularization knob C", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "soft-margin-svm")


def kernel_trick() -> None:
    """Two concentric rings are not linearly separable, but an RBF-kernel SVM
    draws a closed nonlinear boundary that wraps the inner ring. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.svm import SVC

    rng = np.random.default_rng(0)
    npc = 100
    r1 = 1 + 0.15 * rng.normal(size=npc)
    r2 = 3 + 0.15 * rng.normal(size=npc)
    th1 = 2 * np.pi * rng.random(npc)
    th2 = 2 * np.pi * rng.random(npc)
    X = np.vstack([np.column_stack([r1 * np.cos(th1), r1 * np.sin(th1)]),
                   np.column_stack([r2 * np.cos(th2), r2 * np.sin(th2)])])
    y = np.array([1] * npc + [-1] * npc)
    clf = SVC(kernel="rbf", gamma=0.5, C=10).fit(X, y)

    gx, gy = np.meshgrid(np.linspace(-4, 4, 300), np.linspace(-4, 4, 300))
    Z = clf.decision_function(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    ax.contourf(gx, gy, Z, levels=[-100, 0, 100], colors=[ACCENT, HOT], alpha=0.18)
    ax.contour(gx, gy, Z, levels=[0], colors=[C], linewidths=2.4)
    _scatter_two(ax, X, y)
    ax.set_aspect("equal")
    ax.set_title("Kernel trick: RBF separates concentric rings")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "kernel-trick")


def gaussian_processes() -> None:
    """A GP posterior: the mean interpolates the data and the credible band widens
    away from observations. Lesson's f(x)=sin(2x)+0.3cos(7x), n=12, ℓ=0.5,
    σ_f=1, σ_n=0.1, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)

    def f_true(x):
        return np.sin(2 * x) + 0.3 * np.cos(7 * x)

    n = 12
    xt = np.sort(rng.uniform(-3, 3, n))[:, None]
    yt = f_true(xt).ravel() + 0.1 * rng.normal(size=n)
    xs = np.linspace(-4, 4, 300)[:, None]

    ell, sf, sn = 0.5, 1.0, 0.1

    def k(a, b):
        d2 = (a - b.T) ** 2
        return sf**2 * np.exp(-0.5 * d2 / ell**2)

    K = k(xt, xt) + sn**2 * np.eye(n)
    Ks = k(xs, xt)
    Kss = k(xs, xs)
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, yt))
    mu = Ks @ alpha
    v = np.linalg.solve(L, Ks.T)
    var = np.diag(Kss) - np.sum(v**2, axis=0)
    sd = np.sqrt(np.clip(var, 0, None))

    xs1 = xs.ravel()
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.fill_between(xs1, mu - 1.96 * sd, mu + 1.96 * sd, color=C, alpha=0.22,
                    label="95% credible band")
    ax.plot(xs1, f_true(xs1), color=FG_MUTE, ls="--", lw=1.6, label="true $f$")
    ax.plot(xs1, mu, color=C, lw=2.2, label="GP mean")
    ax.scatter(xt.ravel(), yt, s=30, color=HOT, edgecolor="none", zorder=4,
               label="observations")
    ax.set_title("Gaussian-process posterior")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.legend(loc="upper right", fontsize=9, frameon=True, facecolor="#161c3a",
              edgecolor=GRID, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "gaussian-processes")


def common_kernels() -> None:
    """The RBF kernel k(0, x) = exp(-γx²) as a similarity-vs-distance curve: γ
    sets the bandwidth — small γ = broad, far-reaching similarity, large γ =
    narrow, local similarity."""
    import matplotlib.pyplot as plt

    r = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for gamma, col in zip([0.1, 0.5, 2.0], [ACCENT, C, HOT]):
        ax.plot(r, np.exp(-gamma * r**2), color=col, lw=2.2, label=f"γ = {gamma}")
    ax.set_title("RBF kernel: bandwidth γ sets the reach")
    ax.set_xlabel("distance $x - x'$")
    ax.set_ylabel("similarity $k(x, x')$")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "common-kernels")


def main() -> None:
    apply_style()
    hard_margin_svm()
    soft_margin_svm()
    kernel_trick()
    gaussian_processes()
    common_kernels()


if __name__ == "__main__":
    main()
