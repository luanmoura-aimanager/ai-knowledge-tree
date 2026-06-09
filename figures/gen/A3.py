"""Figures for pillar A3 (optimization). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, CYCLE, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

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


def convergence_rates() -> None:
    """Gap to optimum vs iteration on f = ½xᵀAx, A = diag(1, L). Strongly convex
    GD converges linearly at a rate set by κ = L; a convex-only 1/t reference
    shows the much slower sublinear regime."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for kappa, col in zip([2.0, 10.0, 100.0], CYCLE):
        A = np.diag([1.0, kappa])
        eta = 1.0 / kappa
        x = np.array([1.0, 1.0])
        f0 = 0.5 * x @ A @ x
        gaps = [1.0]
        for _ in range(60):
            x = x - eta * (A @ x)
            gaps.append((0.5 * x @ A @ x) / f0)
        ax.semilogy(gaps, color=col, lw=2.0, label=f"strongly convex, κ={kappa:.0f}")

    t = np.arange(1, 62)
    ax.semilogy(t, 1.0 / t, color=FG_MUTE, ls="--", lw=1.6, label="convex only, $O(1/t)$")
    ax.set_title("Linear vs sublinear convergence")
    ax.set_xlabel("iteration $t$")
    ax.set_ylabel("gap to optimum (relative)")
    ax.set_ylim(1e-12, 2)
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, SUB, "convergence-rates")


def momentum() -> None:
    """On an ill-conditioned quadratic (A = diag(1, 100)), heavy-ball/Nesterov
    momentum converges in ~√κ steps where plain GD needs ~κ — the gap-to-optimum
    curve drops far faster."""
    import matplotlib.pyplot as plt

    mu, L = 1.0, 100.0
    A = np.diag([mu, L])
    f = lambda x: 0.5 * x @ A @ x
    grad = lambda x: A @ x
    x0 = np.array([1.0, 1.0])
    f0 = f(x0)
    steps = 120

    # Plain gradient descent
    x = x0.copy()
    gd = [1.0]
    for _ in range(steps):
        x = x - (1.0 / L) * grad(x)
        gd.append(f(x) / f0)

    # Nesterov accelerated gradient
    kappa = L / mu
    beta = (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)
    x = x0.copy()
    y = x0.copy()
    nag = [1.0]
    for _ in range(steps):
        x_new = y - (1.0 / L) * grad(y)
        y = x_new + beta * (x_new - x)
        x = x_new
        nag.append(f(x) / f0)

    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.semilogy(gd, color=FG_MUTE, lw=2.0, label="gradient descent")
    ax.semilogy(nag, color=C, lw=2.4, label="Nesterov momentum")
    ax.set_title(f"Momentum on an ill-conditioned quadratic (κ={kappa:.0f})")
    ax.set_xlabel("iteration $t$")
    ax.set_ylabel("gap to optimum (relative)")
    ax.set_ylim(1e-8, 2)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "momentum")


def newton_method() -> None:
    """Newton vs gradient descent on f(x) = Σ(xᵢ - log xᵢ) (optimum at 1). Newton
    converges quadratically (error roughly squares each step); GD is only linear."""
    import matplotlib.pyplot as plt

    grad = lambda x: 1 - 1 / x
    opt = np.ones(3)
    x0 = np.array([1.5, 0.5, 1.8])

    # Newton: H = diag(1/x^2), so step = -H^{-1} grad = -(x^2)*(1 - 1/x)
    x = x0.copy()
    newton = [np.linalg.norm(x - opt)]
    for _ in range(8):
        x = x - (x**2) * grad(x)
        newton.append(np.linalg.norm(x - opt))

    # Gradient descent
    x = x0.copy()
    gd = [np.linalg.norm(x - opt)]
    for _ in range(8):
        x = x - 0.4 * grad(x)
        gd.append(np.linalg.norm(x - opt))

    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.semilogy(gd, "-o", color=FG_MUTE, ms=4, label="gradient descent (linear)")
    ax.semilogy(np.clip(newton, 1e-16, None), "-o", color=C, ms=4,
                label="Newton (quadratic)")
    ax.set_title("Newton's quadratic convergence")
    ax.set_xlabel("iteration $t$")
    ax.set_ylabel(r"$\|x_t - x^\star\|$")
    ax.set_ylim(1e-16, 2)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "newton-method")


def convex_functions() -> None:
    """The chord test: for a convex function every chord lies above the graph;
    a nonconvex function (cos) has chords that dip below it."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.6))

    x = np.linspace(-2, 2, 400)
    ax1.plot(x, x**2, color=C, lw=2.2)
    a, b = -1.5, 1.0
    ax1.plot([a, b], [a**2, b**2], "-o", color=HOT, ms=5)
    ax1.set_title("Convex: chord stays above")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$f(x)=x^2$")

    xc = np.linspace(-3.5, 3.5, 400)
    ax2.plot(xc, np.cos(xc), color=C, lw=2.2)
    a2, b2 = -3.0, 3.0
    ax2.plot([a2, b2], [np.cos(a2), np.cos(b2)], "-o", color=HOT, ms=5)
    ax2.set_title("Nonconvex: graph rises above chord")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$f(x)=\\cos x$")

    fig.tight_layout()
    save(fig, SUB, "convex-functions")


def adaptive_methods() -> None:
    """On a badly-scaled quadratic (curvatures 1…1000), per-coordinate adaptive
    methods (AdaGrad/RMSProp/Adam) crush the loss while plain GD — capped by the
    largest curvature — barely moves on the flat directions. Lesson's setup."""
    import matplotlib.pyplot as plt

    scales = np.array([1.0, 10.0, 100.0, 1000.0])
    f = lambda x: 0.5 * np.sum(scales * x**2)
    grad = lambda x: scales * x
    x0 = np.ones(4)
    steps = 500
    eps = 1e-8

    def run_gd():
        x = x0.copy()
        hist = [f(x)]
        for _ in range(steps):
            x = x - (1.0 / 1000.0) * grad(x)
            hist.append(f(x))
        return hist

    def run_adagrad(eta=0.5):
        x = x0.copy(); G = np.zeros(4); hist = [f(x)]
        for _ in range(steps):
            g = grad(x); G += g**2
            x = x - eta * g / (np.sqrt(G) + eps)
            hist.append(f(x))
        return hist

    def run_rmsprop(eta=0.05, rho=0.9):
        x = x0.copy(); v = np.zeros(4); hist = [f(x)]
        for _ in range(steps):
            g = grad(x); v = rho * v + (1 - rho) * g**2
            x = x - eta * g / (np.sqrt(v) + eps)
            hist.append(f(x))
        return hist

    def run_adam(eta=0.1, b1=0.9, b2=0.999):
        x = x0.copy(); m = np.zeros(4); v = np.zeros(4); hist = [f(x)]
        for t in range(1, steps + 1):
            g = grad(x)
            m = b1 * m + (1 - b1) * g
            v = b2 * v + (1 - b2) * g**2
            mh = m / (1 - b1**t); vh = v / (1 - b2**t)
            x = x - eta * mh / (np.sqrt(vh) + eps)
            hist.append(f(x))
        return hist

    series = [
        ("GD (η=1/1000)", run_gd(), FG_MUTE),
        ("AdaGrad", run_adagrad(), ACCENT),
        ("RMSProp", run_rmsprop(), GOOD),
        ("Adam", run_adam(), C),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for label, hist, col in series:
        ax.semilogy(np.clip(hist, 1e-16, None), color=col, lw=2.0, label=label)
    ax.set_title("Adaptive methods on a badly-scaled quadratic")
    ax.set_xlabel("iteration $t$")
    ax.set_ylabel("loss $f(x)$")
    ax.set_ylim(1e-16, 2e3)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "adaptive-methods")


def main() -> None:
    apply_style()
    gradient_descent()
    convergence_rates()
    momentum()
    newton_method()
    convex_functions()
    adaptive_methods()


if __name__ == "__main__":
    main()
