"""Figures for pillar L6 (multivariable optimization & the ML bridge)."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GOOD, apply_style, color, save

SUB = "L6"
C = color(SUB)  # pillar-L accent


def critical_points() -> None:
    """One landscape with all three critical-point types marked: a minimum,
    a maximum, and a saddle, classified by Hessian eigenvalue signs."""
    import matplotlib.pyplot as plt

    # f = sin(x) * sin(y) on a window catching a max, a min, and a saddle
    x = np.linspace(-0.6 * np.pi, 1.6 * np.pi, 300)
    y = np.linspace(-0.6 * np.pi, 1.6 * np.pi, 300)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.sin(Y)

    fig, ax = plt.subplots(figsize=(6.8, 5.4))
    cs = ax.contour(X, Y, Z, levels=13, cmap="viridis")
    ax.clabel(cs, inline=True, fontsize=6)

    ax.plot([np.pi / 2], [np.pi / 2], "o", ms=8, color=HOT, zorder=5)
    ax.annotate("max: both λ < 0", (np.pi / 2, np.pi / 2),
                xytext=(np.pi / 2 - 1.7, np.pi / 2 + 0.8), color="#e6e9f5",
                fontsize=9, arrowprops=dict(arrowstyle="-|>", color=FG_MUTE))
    ax.plot([3 * np.pi / 2], [np.pi / 2], "o", ms=8, color=GOOD, zorder=5)
    ax.annotate("min: both λ > 0", (3 * np.pi / 2, np.pi / 2),
                xytext=(3 * np.pi / 2 - 0.6, np.pi / 2 - 1.3), color="#e6e9f5",
                fontsize=9, arrowprops=dict(arrowstyle="-|>", color=FG_MUTE))
    ax.plot([np.pi], [np.pi], "o", ms=8, color=ACCENT, zorder=5)
    ax.annotate("saddle: mixed signs", (np.pi, np.pi),
                xytext=(np.pi - 0.5, np.pi + 1.0), color="#e6e9f5",
                fontsize=9, arrowprops=dict(arrowstyle="-|>", color=FG_MUTE))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.set_title("Critical points of sin(x)sin(y): gradient zero, Hessian decides")
    fig.tight_layout()
    save(fig, SUB, "critical-points")


def convexity() -> None:
    """Convex vs nonconvex in one dimension: the chord test. For a convex
    function every chord sits above the graph; the nonconvex one dips a chord
    below, creating a spurious local minimum."""
    import matplotlib.pyplot as plt

    x = np.linspace(-2.4, 2.4, 400)
    f1 = 0.5 * x**2 + 0.4 * np.abs(x)          # convex
    f2 = 0.25 * x**4 - x**2 + 0.3 * x + 1.2    # double well: nonconvex

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.8))

    a, b = -1.8, 1.4
    for ax, f, name in [(ax1, f1, "convex"), (ax2, f2, "nonconvex")]:
        ax.plot(x, f, color=C, lw=2.4)
        fa = np.interp(a, x, f)
        fb = np.interp(b, x, f)
        ax.plot([a, b], [fa, fb], color=HOT, lw=1.8, ls="--", label="chord")
        ax.plot([a, b], [fa, fb], "o", ms=6, color=HOT)
        ax.set_title(name)
        ax.set_xlabel("x")
        ax.legend(fontsize=8)
    ax1.set_ylabel("f(x)")

    fig.suptitle("Convexity is the chord test: graph below every chord", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "convexity")


def lagrange_multipliers() -> None:
    """Maximize f = xy on the circle g = x^2 + y^2 = 1: at the constrained
    optima the objective's contours are tangent to the constraint, i.e. the
    two gradients are parallel."""
    import matplotlib.pyplot as plt

    x = np.linspace(-1.6, 1.6, 300)
    X, Y = np.meshgrid(x, x)

    fig, ax = plt.subplots(figsize=(6.8, 5.4))
    cs = ax.contour(X, Y, X * Y, levels=11, cmap="viridis")
    ax.clabel(cs, inline=True, fontsize=6)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), color=HOT, lw=2.4, label="constraint g = 1")

    s = 1 / np.sqrt(2)
    for px, py in [(s, s), (-s, -s), (s, -s), (-s, s)]:
        ax.plot([px], [py], "o", ms=7, color="#e6e9f5", zorder=6)
        ax.annotate("", (px + 0.33 * py, py + 0.33 * px), (px, py),
                    arrowprops=dict(arrowstyle="-|>", color=GOOD, lw=1.8))
        ax.annotate("", (px + 0.4 * px, py + 0.4 * py), (px, py),
                    arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.8))

    ax.annotate("∇f ∥ ∇g at the optima", (s, s), xytext=(0.06, 1.32),
                color="#e6e9f5", fontsize=10,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Lagrange: tangency of objective contours and constraint")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "lagrange-multipliers")


def steepest_descent() -> None:
    """Gradient descent on a bowl for three step sizes: smooth convergence,
    efficient convergence, and overshoot oscillation near the stability edge."""
    import matplotlib.pyplot as plt

    # f = 0.5 (x^2 + 4 y^2); grad = (x, 4y); L = 4 so eta < 2/L = 0.5 stable
    x = np.linspace(-2.4, 2.4, 300)
    X, Y = np.meshgrid(x, x)
    Z = 0.5 * (X**2 + 4 * Y**2)

    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.contour(X, Y, Z, levels=12, cmap="viridis", alpha=0.75)

    for eta, col, lab in [(0.08, GOOD, "η = 0.08 (slow, steady)"),
                          (0.22, ACCENT, "η = 0.22 (fast)"),
                          (0.49, HOT, "η = 0.49 (edge: oscillates)")]:
        p = np.array([-2.0, 1.1])
        path = [p.copy()]
        for _ in range(30):
            p = p - eta * np.array([p[0], 4 * p[1]])
            path.append(p.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], marker="o", ms=3, lw=1.4,
                color=col, label=lab)

    ax.plot([0], [0], "*", ms=14, color="#e6e9f5", zorder=6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Step size against curvature: the stability budget η < 2/L")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "steepest-descent")


def curvature_conditioning() -> None:
    """Zigzag on an ill-conditioned valley (kappa = 50) vs direct descent on a
    round bowl: the eigenvalue spread, not the dimension, is what hurts."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.9))

    def run(ax, ky, eta, title):
        x = np.linspace(-2.3, 2.3, 300)
        y = np.linspace(-1.4, 1.4, 300)
        X, Y = np.meshgrid(x, y)
        ax.contour(X, Y, 0.5 * (X**2 + ky * Y**2), levels=14,
                   cmap="viridis", alpha=0.8)
        p = np.array([-2.0, 1.0])
        path = [p.copy()]
        for _ in range(40):
            p = p - eta * np.array([p[0], ky * p[1]])
            path.append(p.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], marker="o", ms=2.6, lw=1.2, color=HOT)
        ax.plot([0], [0], "*", ms=11, color="#e6e9f5")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x")

    run(ax1, 1.0, 0.8, "κ = 1: straight to the bottom")
    run(ax2, 50.0, 0.038, "κ = 50: zigzag across the valley")
    ax1.set_ylabel("y")
    fig.suptitle("Conditioning: the eigenvalue ratio sets the zigzag", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "curvature-conditioning")


def backprop_chain_rule() -> None:
    """Analytic backprop gradients vs finite differences for every parameter
    of a tiny two-layer network: agreement bar by bar."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    W1 = rng.normal(0, 1.0, (3, 2))
    W2 = rng.normal(0, 1.0, (1, 3))
    xin = np.array([0.6, -0.4])
    target = 0.7

    def forward(W1, W2):
        h = np.tanh(W1 @ xin)
        yhat = (W2 @ h)[0]
        return 0.5 * (yhat - target) ** 2

    # Backprop by hand
    h = np.tanh(W1 @ xin)
    yhat = (W2 @ h)[0]
    dy = yhat - target
    gW2 = dy * h[None, :]
    gh = dy * W2[0]
    gW1 = ((1 - h**2) * gh)[:, None] @ xin[None, :]

    grads = np.concatenate([gW1.ravel(), gW2.ravel()])

    eps = 1e-6
    fd = []
    for M, idx in [(W1, range(W1.size)), (W2, range(W2.size))]:
        for i in idx:
            P = M.ravel().copy()
            Mp, Mm = M.copy().ravel(), M.copy().ravel()
            Mp[i] += eps
            Mm[i] -= eps
            if M is W1:
                fd.append((forward(Mp.reshape(W1.shape), W2)
                           - forward(Mm.reshape(W1.shape), W2)) / (2 * eps))
            else:
                fd.append((forward(W1, Mp.reshape(W2.shape))
                           - forward(W1, Mm.reshape(W2.shape))) / (2 * eps))
    fd = np.array(fd)

    k = np.arange(grads.size)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.bar(k - 0.18, grads, width=0.36, color=C, label="backprop (chain rule)")
    ax.bar(k + 0.18, fd, width=0.36, color=HOT, alpha=0.8,
           label="finite differences")
    ax.axhline(0, color=FG_MUTE, lw=1.0)
    ax.set_xticks(k)
    ax.set_xticklabels([f"W1[{i}]" for i in range(6)] + [f"W2[{i}]" for i in range(3)],
                       fontsize=8)
    ax.set_ylabel("∂loss/∂parameter")
    ax.set_title("Every parameter's gradient, two ways: they coincide")
    ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "backprop-chain-rule")


def main() -> None:
    apply_style()
    critical_points()
    convexity()
    lagrange_multipliers()
    steepest_descent()
    curvature_conditioning()
    backprop_chain_rule()


if __name__ == "__main__":
    main()
