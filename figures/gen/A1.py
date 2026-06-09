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
    # NumPy 2.0's SIMD matmul can raise spurious FP-flag warnings on these
    # benign products; the values are finite and the figure is correct.
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
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


def _arrow(ax, vec, color, label=None, origin=(0, 0), ls="-"):
    ax.annotate("", xy=vec, xytext=origin,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2, ls=ls))
    if label:
        ax.text(vec[0] * 1.06, vec[1] * 1.06, label, color=color, fontsize=11)


def basis_dimension() -> None:
    """A basis is a minimal spanning set: two independent vectors tile the plane
    with a lattice of integer combinations (left), but a dependent pair spans only
    a line (right)."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 4.0))
    b1, b2 = np.array([1.0, 0.3]), np.array([0.4, 1.0])
    for i in range(-3, 4):
        for j in range(-3, 4):
            p = i * b1 + j * b2
            ax1.plot(*p, "o", color=FG_MUTE, ms=2.5)
    _arrow(ax1, b1, C, "$b_1$"); _arrow(ax1, b2, ACCENT, "$b_2$")
    ax1.set_title("Independent basis spans the plane")

    d1, d2 = np.array([1.0, 0.5]), np.array([2.0, 1.0])  # d2 = 2 d1
    ts = np.linspace(-3, 3, 50)
    ax2.plot([t * d1[0] for t in ts], [t * d1[1] for t in ts], color=FG_MUTE, lw=1.0)
    _arrow(ax2, d1, C, "$d_1$"); _arrow(ax2, d2, HOT, "$d_2=2d_1$")
    ax2.set_title("Dependent pair spans only a line")
    for ax in (ax1, ax2):
        ax.set_aspect("equal"); ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
        ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    fig.tight_layout()
    save(fig, SUB, "basis-dimension")


def determinants() -> None:
    """The determinant is the signed area-scaling factor: the unit square maps to a
    parallelogram whose area equals |det A|."""
    import matplotlib.pyplot as plt

    A = np.array([[2.0, 1.0], [0.5, 1.5]])
    det = np.linalg.det(A)
    sq = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]])
    img = A @ sq

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.fill(sq[0], sq[1], color=FG_MUTE, alpha=0.3, label="unit square (area 1)")
    ax.fill(img[0], img[1], color=C, alpha=0.4, label=f"A·square (area {det:.1f})")
    _arrow(ax, A[:, 0], ACCENT, "$Ae_1$"); _arrow(ax, A[:, 1], HOT, "$Ae_2$")
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title(f"det A = {det:.1f} = area scaling")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "determinants")


def gram_schmidt() -> None:
    """Gram–Schmidt orthogonalizes a basis: subtract from a₂ its projection onto
    a₁, leaving the perpendicular component that becomes q₂."""
    import matplotlib.pyplot as plt

    a1 = np.array([2.0, 0.5])
    a2 = np.array([1.0, 2.0])
    proj = (a2 @ a1) / (a1 @ a1) * a1
    q2 = a2 - proj

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    _arrow(ax, a1, C, "$a_1$")
    _arrow(ax, a2, ACCENT, "$a_2$")
    _arrow(ax, proj, FG_MUTE, "proj")
    _arrow(ax, q2, HOT, "$q_2 \\perp a_1$")
    ax.plot([proj[0], a2[0]], [proj[1], a2[1]], color=HOT, ls=":", lw=1.4)
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 2.5)
    ax.set_title("Gram–Schmidt: subtract the projection")
    fig.tight_layout()
    save(fig, SUB, "gram-schmidt")


def inner_products() -> None:
    """The inner product measures alignment: u·v = |u||v|cos θ, recovered as the
    length of v's projection onto u times |u|."""
    import matplotlib.pyplot as plt

    u = np.array([3.0, 0.5])
    v = np.array([1.5, 2.0])
    proj = (u @ v) / (u @ u) * u
    cos = (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    _arrow(ax, u, C, "$u$")
    _arrow(ax, v, ACCENT, "$v$")
    _arrow(ax, proj, HOT, "proj of v on u")
    ax.plot([v[0], proj[0]], [v[1], proj[1]], color=FG_MUTE, ls=":", lw=1.4)
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_xlim(-0.5, 3.5); ax.set_ylim(-0.5, 2.5)
    ax.set_title(f"Inner product: cos θ = {cos:.2f}")
    fig.tight_layout()
    save(fig, SUB, "inner-products")


def least_squares() -> None:
    """Least squares projects the target b onto the column space; the residual is
    orthogonal to that space, which is exactly the normal equations."""
    import matplotlib.pyplot as plt

    a = np.array([3.0, 1.0])          # column space = span(a), a line
    b = np.array([2.0, 3.0])
    p = (a @ b) / (a @ a) * a          # projection of b onto span(a)
    ts = np.linspace(-0.3, 1.2, 50)

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.plot([t * a[0] for t in ts], [t * a[1] for t in ts], color=FG_MUTE, lw=1.4,
            label="column space")
    _arrow(ax, b, ACCENT, "$b$")
    _arrow(ax, p, C, "$\\hat b = Ax$")
    ax.plot([p[0], b[0]], [p[1], b[1]], color=HOT, lw=2.0, label="residual $\\perp$ space")
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title("Least squares = orthogonal projection")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "least-squares")


def linear_maps_matrices() -> None:
    """A matrix is a linear map: it sends the square grid to a sheared/rotated grid,
    moving every point by the same linear rule."""
    import matplotlib.pyplot as plt

    A = np.array([[1.0, 0.6], [-0.4, 1.1]])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 4.2))
    lines = np.arange(-3, 4)
    t = np.linspace(-3, 3, 30)
    for ax, M, ttl in [(ax1, np.eye(2), "before"), (ax2, A, "after A")]:
        for k in lines:
            v1 = M @ np.vstack([np.full_like(t, k), t])
            v2 = M @ np.vstack([t, np.full_like(t, k)])
            ax.plot(v1[0], v1[1], color=GRID, lw=0.8)
            ax.plot(v2[0], v2[1], color=GRID, lw=0.8)
        sq = M @ np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]])
        ax.fill(sq[0], sq[1], color=C, alpha=0.4)
        ax.set_aspect("equal"); ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
        ax.set_title(ttl)
    fig.suptitle("A linear map deforms the grid uniformly", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "linear-maps-matrices")


def norms() -> None:
    """Different norms have different unit balls: the L1 ball is a diamond, L2 a
    circle, L∞ a square — the same vector has a different 'length' under each."""
    import matplotlib.pyplot as plt

    t = np.linspace(0, 2 * np.pi, 400)
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=HOT, lw=2.2, label="$L_1$ (diamond)")
    ax.plot(np.cos(t), np.sin(t), color=C, lw=2.2, label="$L_2$ (circle)")
    ax.plot([1, 1, -1, -1, 1], [1, -1, -1, 1, 1], color=ACCENT, lw=2.2, label="$L_\\infty$ (square)")
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title("Unit balls of the L1, L2, L∞ norms")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "norms")


def svd() -> None:
    """SVD factors any matrix as rotate–scale–rotate: it maps the unit circle to an
    ellipse whose semi-axis lengths are the singular values σ₁ ≥ σ₂. The spectrum
    (right) ranks each direction's importance."""
    import matplotlib.pyplot as plt

    A = np.array([[3.0, 1.2], [0.5, 2.0]])
    U, s, Vt = np.linalg.svd(A)
    circle = _unit_circle()
    ell = A @ circle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9))
    ax1.plot(circle[0], circle[1], color=GRID, lw=1.4, label="unit circle")
    ax1.plot(ell[0], ell[1], color=C, lw=2.2, label="A·circle")
    for i in range(2):
        _arrow(ax1, s[i] * U[:, i], [ACCENT, HOT][i], f"$\\sigma_{i+1}$")
    ax1.set_aspect("equal")
    ax1.set_title("Rotate–scale–rotate")
    ax1.legend(loc="lower right", fontsize=8)

    ax2.bar([1, 2], s, color=C, width=0.5)
    ax2.set_xticks([1, 2]); ax2.set_xticklabels(["$\\sigma_1$", "$\\sigma_2$"])
    ax2.set_title("Singular-value spectrum")
    ax2.set_ylabel("singular value")
    fig.tight_layout()
    save(fig, SUB, "svd")


def main() -> None:
    apply_style()
    low_rank_pca()
    eigenvalues()
    spectral_theorem()
    quadratic_forms()
    basis_dimension()
    determinants()
    gram_schmidt()
    inner_products()
    least_squares()
    linear_maps_matrices()
    norms()
    svd()


if __name__ == "__main__":
    main()
