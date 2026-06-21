"""Figures for pillar L4 (multivariable differentiation). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "L4"
C = color(SUB)  # pillar-L accent


def _two_bumps(X, Y):
    return (np.exp(-((X - 1) ** 2 + (Y - 1) ** 2)) +
            0.7 * np.exp(-((X + 1.2) ** 2 + (Y + 0.8) ** 2) / 1.5))


def multivariable_functions() -> None:
    """One scalar field, two pictures: the 3D graph (a surface over the plane)
    and the contour map (level sets). Same information, different projections."""
    import matplotlib.pyplot as plt

    x = np.linspace(-3, 3, 160)
    X, Y = np.meshgrid(x, x)
    Z = _two_bumps(X, Y)

    fig = plt.figure(figsize=(7.4, 3.9))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True)
    ax1.set_title("graph z = f(x, y)", fontsize=11)
    ax1.set_xlabel("x", fontsize=8)
    ax1.set_ylabel("y", fontsize=8)
    ax1.tick_params(labelsize=6)
    ax1.set_facecolor("none")

    ax2 = fig.add_subplot(1, 2, 2)
    cs = ax2.contour(X, Y, Z, levels=10, cmap="viridis")
    ax2.clabel(cs, inline=True, fontsize=6)
    ax2.set_title("level sets f(x, y) = c", fontsize=11)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_aspect("equal")

    fig.suptitle("A scalar field as surface and as contour map", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "multivariable-functions")


def partial_derivatives() -> None:
    """Partial derivatives are slopes of axis-aligned slices: freeze y = y0 and
    the surface becomes a curve in x whose slope is df/dx; likewise for y."""
    import matplotlib.pyplot as plt

    f = lambda x, y: x**2 + 0.5 * y**2 + 0.5 * x * y
    x0, y0 = 1.0, -0.5
    t = np.linspace(-2.5, 2.5, 300)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.8))

    ax1.plot(t, f(t, y0), color=C, lw=2.2, label=f"slice y = {y0}")
    fx = 2 * x0 + 0.5 * y0
    xx = np.linspace(x0 - 1.0, x0 + 1.0, 20)
    ax1.plot(xx, f(x0, y0) + fx * (xx - x0), color=HOT, ls="--", lw=1.8,
             label=f"slope = ∂f/∂x = {fx:.2f}")
    ax1.plot([x0], [f(x0, y0)], "o", ms=6, color=HOT, zorder=5)
    ax1.set_xlabel("x")
    ax1.set_title("x-slice through (1, −0.5)")
    ax1.legend(fontsize=8)

    ax2.plot(t, f(x0, t), color=ACCENT, lw=2.2, label=f"slice x = {x0}")
    fy = 1.0 * y0 + 0.5 * x0
    yy = np.linspace(y0 - 1.0, y0 + 1.0, 20)
    ax2.plot(yy, f(x0, y0) + fy * (yy - y0), color=HOT, ls="--", lw=1.8,
             label=f"slope = ∂f/∂y = {fy:.2f}")
    ax2.plot([y0], [f(x0, y0)], "o", ms=6, color=HOT, zorder=5)
    ax2.set_xlabel("y")
    ax2.set_title("y-slice through (1, −0.5)")
    ax2.legend(fontsize=8)

    fig.suptitle("Each partial derivative is an ordinary slope along one axis", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "partial-derivatives")


def gradient_directional() -> None:
    """Contours of a quadratic bowl with the gradient field: every arrow is
    orthogonal to the level set it sits on and points uphill, longer where the
    contours are tighter."""
    import matplotlib.pyplot as plt

    f = lambda x, y: 0.5 * x**2 + y**2
    x = np.linspace(-2.2, 2.2, 200)
    X, Y = np.meshgrid(x, x)
    Z = f(X, Y)

    g = np.linspace(-2.0, 2.0, 11)
    GX, GY = np.meshgrid(g, g)
    UX, UY = GX, 2 * GY                      # gradient (x, 2y)

    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    cs = ax.contour(X, Y, Z, levels=9, cmap="viridis")
    ax.clabel(cs, inline=True, fontsize=6)
    ax.quiver(GX, GY, UX, UY, color=HOT, width=0.004, alpha=0.85)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("∇f is orthogonal to level sets and points uphill")
    fig.tight_layout()
    save(fig, SUB, "gradient-directional")


def total_derivative_chain_rule() -> None:
    """Differentiability in 2D: the tangent plane at a point is the best linear
    approximation; the surface peels away from it quadratically."""
    import matplotlib.pyplot as plt

    f = lambda x, y: x**2 + 0.5 * y**2
    x0, y0 = 0.8, -0.6
    z0 = f(x0, y0)
    fx, fy = 2 * x0, 1.0 * y0

    x = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, x)
    Z = f(X, Y)

    p = np.linspace(-1.0, 1.0, 12)
    PX, PY = np.meshgrid(x0 + p, y0 + p)
    PZ = z0 + fx * (PX - x0) + fy * (PY - y0)

    fig = plt.figure(figsize=(7.0, 5.0))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.75, linewidth=0)
    ax.plot_surface(PX, PY, PZ, color=HOT, alpha=0.5, linewidth=0)
    ax.scatter([x0], [y0], [z0], color="#e6e9f5", s=28, zorder=10)
    ax.set_xlabel("x", fontsize=8)
    ax.set_ylabel("y", fontsize=8)
    ax.set_zlabel("z", fontsize=8)
    ax.tick_params(labelsize=6)
    ax.set_facecolor("none")
    ax.set_title("The tangent plane: the best linear map at the marked point")
    fig.tight_layout()
    save(fig, SUB, "total-derivative-chain-rule")


def jacobian() -> None:
    """A nonlinear map warps a square grid; zooming to one point, the warp is
    a linear map: the Jacobian sends the little square to a parallelogram whose
    area scale is |det J|."""
    import matplotlib.pyplot as plt

    F = lambda x, y: (x + 0.35 * y**2, y + 0.35 * x**2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.9))

    g = np.linspace(-1.2, 1.2, 13)
    for v in g:
        t = np.linspace(-1.2, 1.2, 100)
        ax1.plot(t, np.full_like(t, v), color=FG_MUTE, lw=0.6)
        ax1.plot(np.full_like(t, v), t, color=FG_MUTE, lw=0.6)
        u1, w1 = F(t, np.full_like(t, v))
        u2, w2 = F(np.full_like(t, v), t)
        ax2.plot(u1, w1, color=C, lw=0.7)
        ax2.plot(u2, w2, color=C, lw=0.7)

    # The Jacobian parallelogram at p = (0.5, 0.4)
    px, py = 0.5, 0.4
    J = np.array([[1.0, 0.7 * py], [0.7 * px, 1.0]])
    e = 0.28
    sq = np.array([[0, 0], [e, 0], [e, e], [0, e], [0, 0]]).T
    ax1.plot(px + sq[0], py + sq[1], color=HOT, lw=2.0)
    Fp = np.array(F(px, py))
    par = Fp[:, None] + J @ sq
    ax2.plot(par[0], par[1], color=HOT, lw=2.0)
    ax2.annotate(f"area × |det J| = {abs(np.linalg.det(J)):.2f}",
                 (Fp[0], Fp[1]), xytext=(Fp[0] - 1.6, Fp[1] + 0.9),
                 color="#e6e9f5", fontsize=9,
                 arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))

    ax1.set_title("input grid + a small square")
    ax2.set_title("image grid + its parallelogram")
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.set_xlabel("x")
    fig.suptitle("Locally, a nonlinear map is its Jacobian", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "jacobian")


def hessian() -> None:
    """Three quadratic landscapes told apart by Hessian eigenvalue signs:
    bowl (both positive), saddle (mixed), ridge/valley (one zero direction)."""
    import matplotlib.pyplot as plt

    x = np.linspace(-2, 2, 200)
    X, Y = np.meshgrid(x, x)
    cases = [
        (X**2 + Y**2, "bowl: λ₁, λ₂ > 0"),
        (X**2 - Y**2, "saddle: λ₁ > 0 > λ₂"),
        (X**2 + 0 * Y, "valley: λ₂ = 0"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9))
    for ax, (Z, title) in zip(axes, cases):
        ax.contour(X, Y, Z, levels=11, cmap="viridis")
        ax.plot([0], [0], "o", ms=5, color=HOT)
        ax.set_title(title, fontsize=10)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Curvature signatures: the Hessian's eigenvalue signs", y=1.05)
    fig.tight_layout()
    save(fig, SUB, "hessian")


def main() -> None:
    apply_style()
    multivariable_functions()
    partial_derivatives()
    gradient_directional()
    total_derivative_chain_rule()
    jacobian()
    hessian()


if __name__ == "__main__":
    main()
