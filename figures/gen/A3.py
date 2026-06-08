"""Figures for pillar A3 (optimization). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "A3"
C = color(SUB)  # pillar-A accent


def gradient_descent() -> None:
    """Trajectory on a 2D quadratic + the step-size tradeoff (gap vs iteration).

    Mirrors the lesson's worked example: f(x) = 0.5 xᵀAx - bᵀx with
    A = [[3,1],[1,2]], b = [1,-1], smoothness L = λ_max(A), threshold η = 2/L.
    """
    import matplotlib.pyplot as plt

    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([1.0, -1.0])
    x_star = np.linalg.solve(A, b)
    f = lambda x: 0.5 * x @ A @ x - b @ x
    grad = lambda x: A @ x - b
    L = np.linalg.eigvalsh(A).max()

    def run(eta, steps, x0=(5.0, 5.0)):
        x = np.array(x0)
        traj = [x.copy()]
        for _ in range(steps):
            x = x - eta * grad(x)
            traj.append(x.copy())
        return np.array(traj)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.7))

    # --- Left: contours of f + GD path at eta = 1/L -------------------------
    gx, gy = np.meshgrid(np.linspace(-1.5, 5.5, 200), np.linspace(-3, 5.5, 200))
    Z = np.array(
        [f(np.array([px, py])) for px, py in zip(gx.ravel(), gy.ravel())]
    ).reshape(gx.shape)
    ax1.contour(gx, gy, Z, levels=18, colors=GRID, linewidths=0.7)
    path = run(1.0 / L, 25)
    ax1.plot(path[:, 0], path[:, 1], "-o", color=C, ms=3.5, lw=1.6, label="η = 1/L")
    ax1.plot(*x_star, "*", color=HOT, ms=15, label="optimum x*")
    ax1.set_title("Descent path on a quadratic")
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")
    ax1.legend(loc="upper right")

    # --- Right: gap to optimum f(x_t) - f* vs iteration, several step sizes --
    f_star = f(x_star)
    regimes = [
        (0.15 / L, "η = 0.15/L (slow)", FG_MUTE, "-"),
        (1.0 / L, "η = 1/L (good)", C, "-"),
        (1.9 / L, "η = 1.9/L (oscillates)", "#7dcfff", "--"),
        (2.1 / L, "η = 2.1/L (diverges)", HOT, ":"),
    ]
    for eta, label, col, ls in regimes:
        traj = run(eta, 40)
        gap = np.array([f(x) - f_star for x in traj])
        gap = np.clip(gap, 1e-12, None)
        ax2.semilogy(gap, ls, color=col, label=label, lw=1.8)
    ax2.set_title("Step size sets the fate")
    ax2.set_xlabel("iteration $t$")
    ax2.set_ylabel("$f(x_t) - f^*$")
    ax2.set_ylim(1e-10, 1e4)
    ax2.legend(loc="lower left")

    fig.tight_layout()
    save(fig, SUB, "gradient-descent")


def main() -> None:
    apply_style()
    gradient_descent()


if __name__ == "__main__":
    main()
