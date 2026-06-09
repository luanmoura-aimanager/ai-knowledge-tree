"""Figures for pillar A1 (linear algebra). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "A1"
C = color(SUB)  # pillar-A accent (gold)


def low_rank_pca() -> None:
    """Scree (variance explained) + reconstruction-error decay vs rank.

    Reuses the lesson's data: rng(42), 200×10 with a rank-3 signal (component
    std [5,3,1]) plus 0.2 noise; the knee at k=3 is the whole point.
    """
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(42)
    d, n, k_true = 10, 200, 3
    V_true = np.linalg.qr(rng.normal(size=(d, k_true)))[0]
    scores = rng.normal(scale=[5, 3, 1], size=(n, k_true))
    X = scores @ V_true.T + 0.2 * rng.normal(size=(n, d))
    X_c = X - X.mean(axis=0)
    s = np.linalg.svd(X_c, full_matrices=False)[1]

    energy = s**2
    frac = energy / energy.sum()
    cum = np.cumsum(frac)
    ranks = np.arange(1, d + 1)
    # ||X - X_k||_F / ||X||_F = sqrt(tail energy / total)
    recon = np.sqrt(1 - cum)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.6))

    ax1.bar(ranks, frac, color=C, alpha=0.85, label="per-component")
    ax1.plot(ranks, cum, "-o", color=ACCENT, ms=4, label="cumulative")
    ax1.axvline(k_true, color=FG_MUTE, ls=":", lw=1.2)
    ax1.set_title("Scree plot")
    ax1.set_xlabel("component / rank $k$")
    ax1.set_ylabel("variance explained")
    ax1.set_xticks(ranks)
    ax1.legend(loc="center right")

    ax2.plot(np.arange(0, d + 1), np.concatenate([[1.0], recon]), "-o", color=C, ms=4)
    ax2.axvline(k_true, color=FG_MUTE, ls=":", lw=1.2, label=f"true rank = {k_true}")
    ax2.set_title("Reconstruction error vs rank")
    ax2.set_xlabel("rank $k$ kept")
    ax2.set_ylabel(r"$\|X-X_k\|_F / \|X\|_F$")
    ax2.set_xticks(np.arange(0, d + 1, 2))
    ax2.legend(loc="upper right")

    fig.tight_layout()
    save(fig, SUB, "low-rank-pca")


def _unit_circle(npts=200):
    t = np.linspace(0, 2 * np.pi, npts)
    return np.stack([np.cos(t), np.sin(t)])


def eigenvalues() -> None:
    """Eigenvectors are the invariant directions of A = [[4,1],[2,3]] (λ = 5, 2).

    The unit circle maps to an ellipse; a generic vector rotates, but the two
    eigen-directions only stretch (by their eigenvalue), staying on their line.
    """
    import matplotlib.pyplot as plt

    A = np.array([[4.0, 1.0], [2.0, 3.0]])
    w, V = np.linalg.eig(A)
    order = np.argsort(-w)
    w, V = w[order], V[:, order]

    circle = _unit_circle()
    ellipse = A @ circle

    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot(circle[0], circle[1], color=GRID, lw=1.4, label="unit circle")
    ax.plot(ellipse[0], ellipse[1], color=C, lw=2.0, label="$A\\,\\cdot$ circle")

    cols = [ACCENT, HOT]
    for i in range(2):
        v = V[:, i]
        if v[0] < 0 or (v[0] == 0 and v[1] < 0):
            v = -v
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=cols[i], lw=2.2))
        Av = A @ v
        ax.annotate("", xy=Av, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=cols[i], lw=2.2, ls=(0, (4, 2))))
        ax.text(Av[0] * 1.05, Av[1] * 1.05, f"$\\lambda={w[i]:.0f}$", color=cols[i], fontsize=11)

    ax.set_aspect("equal")
    ax.set_title("Eigenvectors: directions A only stretches")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right")
    fig.tight_layout()
    save(fig, SUB, "eigenvalues")


def spectral_theorem() -> None:
    """A symmetric matrix has ORTHOGONAL eigenvectors: A = QΛQᵀ rotates a circle
    to an ellipse whose axes lie exactly along the (perpendicular) eigenvectors.

    Uses A = [[2,1],[1,2]] (λ = 3, 1; eigenvectors [1,1]/√2 ⟂ [-1,1]/√2) — a 2D
    stand-in for the lesson's symmetric example, chosen so orthogonality is visible.
    """
    import matplotlib.pyplot as plt

    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    w, Q = np.linalg.eigh(A)  # ascending
    w, Q = w[::-1], Q[:, ::-1]

    circle = _unit_circle()
    ellipse = A @ circle

    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot(circle[0], circle[1], color=GRID, lw=1.4, label="unit circle")
    ax.plot(ellipse[0], ellipse[1], color=C, lw=2.0, label="$A\\,\\cdot$ circle")

    cols = [ACCENT, GOOD]
    for i in range(2):
        v = Q[:, i]
        axis = w[i] * v
        ax.annotate("", xy=axis, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=cols[i], lw=2.4))
        ax.text(axis[0] * 1.08, axis[1] * 1.08, f"$\\lambda={w[i]:.0f}$",
                color=cols[i], fontsize=11)

    ax.set_aspect("equal")
    ax.set_title("Symmetric ⇒ orthogonal eigenvectors")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right")
    fig.tight_layout()
    save(fig, SUB, "spectral-theorem")


def quadratic_forms() -> None:
    """Contours of xᵀAx for positive-definite, indefinite, and negative-definite
    A — eigenvalue signs decide the shape (bowl / saddle / dome).

    Reuses the lesson's rotation θ = π/6 with eigenvalues [3,1], [3,-1], [-3,-1].
    """
    import matplotlib.pyplot as plt

    theta = np.pi / 6
    Qr = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta), np.cos(theta)]])
    cases = [
        ("Positive definite", [3.0, 1.0]),
        ("Indefinite", [3.0, -1.0]),
        ("Negative definite", [-3.0, -1.0]),
    ]
    g = np.linspace(-1.5, 1.5, 240)
    gx, gy = np.meshgrid(g, g)
    pts = np.stack([gx.ravel(), gy.ravel()])

    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.3))
    for ax, (title, eig) in zip(axes, cases):
        A = Qr @ np.diag(eig) @ Qr.T
        q = np.einsum("ji,jk,ki->i", pts, A, pts).reshape(gx.shape)
        vmax = np.abs(q).max()
        ax.contourf(gx, gy, q, levels=18, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.contour(gx, gy, q, levels=10, colors=GRID, linewidths=0.5)
        ax.set_title(f"{title}\n$\\lambda={eig[0]:.0f},\\,{eig[1]:.0f}$", fontsize=11)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.tight_layout()
    save(fig, SUB, "quadratic-forms")


def main() -> None:
    apply_style()
    low_rank_pca()
    eigenvalues()
    spectral_theorem()
    quadratic_forms()


if __name__ == "__main__":
    main()
