"""Figures for pillar A3 (optimization). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import (ACCENT, CYCLE, FG_MUTE, GOOD, GRID, HOT, LEGEND_BG,
                    apply_style, color, save)

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


def bayesian_optimization() -> None:
    """Bayesian optimization fits a surrogate (a GP) to the evaluated points, then
    maximizes an acquisition function (expected improvement) to choose where to
    sample next — balancing exploitation and exploration."""
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    def f(x):
        return np.sin(x) + 0.3 * (x - 4) ** 2 / 4

    xt = np.array([1.0, 3.5, 6.0, 9.0])[:, None]
    yt = f(xt).ravel()
    xs = np.linspace(0, 10, 300)[:, None]
    ell, sf, sn = 1.2, 1.0, 1e-3

    def k(a, b):
        return sf**2 * np.exp(-0.5 * (a - b.T) ** 2 / ell**2)

    K = k(xt, xt) + sn * np.eye(len(xt))
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, yt))
    mu = (k(xs, xt) @ alpha)
    v = np.linalg.solve(L, k(xs, xt).T)
    sd = np.sqrt(np.clip(np.diag(k(xs, xs)) - np.sum(v**2, axis=0), 1e-9, None))
    best = yt.min()
    imp = best - mu
    z = imp / sd
    ei = imp * norm.cdf(z) + sd * norm.pdf(z)
    nxt = xs[np.argmax(ei), 0]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 5.0), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.fill_between(xs.ravel(), mu - 1.96 * sd, mu + 1.96 * sd, color=C, alpha=0.2)
    ax1.plot(xs, f(xs.ravel()), color=FG_MUTE, ls="--", lw=1.4, label="true f")
    ax1.plot(xs, mu, color=C, lw=2.0, label="GP mean")
    ax1.scatter(xt.ravel(), yt, color=HOT, s=40, zorder=5, label="evaluations")
    ax1.set_title("Bayesian optimization")
    ax1.set_ylabel("f(x)")
    ax1.legend(loc="upper center", fontsize=8, ncol=2)
    ax2.fill_between(xs.ravel(), ei, color=ACCENT, alpha=0.4)
    ax2.axvline(nxt, color=HOT, lw=1.8, label=f"next sample x={nxt:.1f}")
    ax2.set_ylabel("EI")
    ax2.set_xlabel("x")
    ax2.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "bayesian-optimization")


def constrained_optimization() -> None:
    """Minimizing x²+y² subject to x+y=1: the solution is where an objective
    contour just touches the constraint line — the gradients are parallel there."""
    import matplotlib.pyplot as plt

    g = np.linspace(-1, 2, 300)
    gx, gy = np.meshgrid(g, g)
    Z = gx**2 + gy**2
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.contour(gx, gy, Z, levels=12, colors=GRID, linewidths=0.8)
    ax.plot(g, 1 - g, color=ACCENT, lw=2.2, label="constraint x+y=1")
    ax.plot(0.5, 0.5, "*", color=HOT, ms=16, label="optimum (0.5, 0.5)")
    ax.set_aspect("equal"); ax.set_xlim(-1, 2); ax.set_ylim(-1, 2)
    ax.set_title("Constrained optimum")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "constrained-optimization")


def convex_sets() -> None:
    """A set is convex if the segment between any two of its points stays inside.
    The disk passes; the crescent fails — a chord leaves the set."""
    import matplotlib.pyplot as plt

    t = np.linspace(0, 2 * np.pi, 200)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 4.2))
    ax1.fill(np.cos(t), np.sin(t), color=C, alpha=0.3)
    ax1.plot([-0.7, 0.6], [0.3, -0.5], "-o", color=ACCENT, lw=2)
    ax1.set_title("Convex: chord stays inside")

    big = np.column_stack([1.3 * np.cos(t), 1.3 * np.sin(t)])
    small = np.column_stack([1.3 * np.cos(t) + 0.7, 1.3 * np.sin(t)])
    ax2.fill(big[:, 0], big[:, 1], color=C, alpha=0.3)
    ax2.fill(small[:, 0], small[:, 1], color="#0a0e1f")
    ax2.plot([-1.0, 1.7], [0.4, 0.4], "-o", color=HOT, lw=2)
    ax2.set_title("Non-convex: chord exits")
    for ax in (ax1, ax2):
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    fig.tight_layout()
    save(fig, SUB, "convex-sets")


def kkt() -> None:
    """At a constrained optimum the objective gradient is a non-negative combination
    of the active constraint gradients (stationarity), so −∇f points out of the
    feasible region along ∇g."""
    import matplotlib.pyplot as plt

    g = np.linspace(-0.5, 2.5, 300)
    gx, gy = np.meshgrid(g, g)
    Z = gx**2 + gy**2
    a = np.array([1.0, 2.0]) / np.sqrt(5)
    xopt = a / (a @ a)  # min ||x||^2 s.t. a^T x = 1
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.contour(gx, gy, Z, levels=12, colors=GRID, linewidths=0.8)
    ax.fill_between(g, (1 / a[1]) - (a[0] / a[1]) * g, 3, color=ACCENT, alpha=0.12)
    ax.plot(g, (1 - a[0] * g) / a[1], color=ACCENT, lw=2.0, label="a·x = 1 (boundary)")
    ax.plot(*xopt, "*", color=HOT, ms=16, label="optimum")
    ax.annotate("", xy=xopt + 0.5 * a, xytext=xopt,
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2))
    ax.text(*(xopt + 0.55 * a), "∇f ∥ ∇g", color=HOT, fontsize=10)
    ax.set_aspect("equal"); ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 2.5)
    ax.set_title("KKT stationarity at the optimum")
    ax.legend(loc="lower left", fontsize=8, frameon=True, facecolor=LEGEND_BG,
              edgecolor=GRID, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "kkt")


def optimization_landscape() -> None:
    """The Hessian's eigenvalues classify a critical point: all positive gives a
    bowl (minimum), mixed signs give a saddle. Left: x²+3y² (bowl); right: x²−y²
    (saddle)."""
    import matplotlib.pyplot as plt

    g = np.linspace(-2, 2, 200)
    gx, gy = np.meshgrid(g, g)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9))
    for ax, Z, ttl in [(ax1, gx**2 + 3 * gy**2, "minimum (bowl)"),
                       (ax2, gx**2 - gy**2, "saddle")]:
        cf = ax.contourf(gx, gy, Z, levels=20, cmap="viridis")
        ax.contour(gx, gy, Z, levels=10, colors=GRID, linewidths=0.4)
        ax.plot(0, 0, "o", color=HOT, ms=8)
        ax.set_title(ttl); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    save(fig, SUB, "optimization-landscape")


def proximal_methods() -> None:
    """The proximal operator of the L1 norm is soft-thresholding: it shrinks every
    coordinate toward zero by λ and clamps the small ones exactly to zero — the
    source of sparsity."""
    import matplotlib.pyplot as plt

    v = np.linspace(-3, 3, 400)
    lam = 1.0
    prox = np.sign(v) * np.maximum(np.abs(v) - lam, 0)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(v, v, color=FG_MUTE, ls="--", lw=1.4, label="identity")
    ax.plot(v, prox, color=C, lw=2.6, label="soft-threshold (λ=1)")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title("Proximal operator of the L1 norm")
    ax.set_xlabel("input v")
    ax.set_ylabel("prox(v)")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "proximal-methods")


def quasi_newton() -> None:
    """BFGS builds a curvature estimate from successive gradients, achieving
    near-Newton (superlinear) convergence using only gradients — far faster than
    gradient descent on an ill-conditioned quadratic (κ=50)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 20
    d = np.linspace(1, 50, n)
    Q = np.linalg.qr(rng.normal(size=(n, n)))[0]
    A = Q @ np.diag(d) @ Q.T
    grad = lambda x: A @ x
    f = lambda x: 0.5 * x @ A @ x
    x0 = np.ones(n)
    f0 = f(x0)

    x = x0.copy(); gd = [1.0]
    eta = 1.0 / 50
    for _ in range(60):
        x = x - eta * grad(x); gd.append(f(x) / f0)

    x = x0.copy(); H = np.eye(n); g = grad(x); bf = [1.0]
    for _ in range(60):
        gap = f(x) / f0
        if gap < 1e-15:                      # converged; stop before s,y → 0
            bf.append(gap)
            continue
        p = -H @ g
        al = -(g @ p) / (p @ A @ p)          # exact line search for a quadratic
        xn = x + al * p; gn = grad(xn)
        s = xn - x; yv = gn - g
        rho = 1.0 / (yv @ s)
        I = np.eye(n)
        H = (I - rho * np.outer(s, yv)) @ H @ (I - rho * np.outer(yv, s)) + rho * np.outer(s, s)
        x, g = xn, gn
        bf.append(f(x) / f0)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(np.clip(gd, 1e-16, None), color=FG_MUTE, lw=2.0, label="gradient descent")
    ax.semilogy(np.clip(bf, 1e-16, None), color=C, lw=2.4, label="BFGS (quasi-Newton)")
    ax.set_title("Quasi-Newton converges superlinearly")
    ax.set_xlabel("iteration")
    ax.set_ylabel("gap to optimum (relative)")
    ax.set_ylim(1e-16, 2)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "quasi-newton")


def sgd() -> None:
    """Stochastic gradient descent follows noisy mini-batch gradients: with a
    constant step it descends fast but rattles around a noise floor, where
    full-batch GD converges smoothly. Decaying the step removes the floor."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, dim = 400, 2
    A = rng.normal(size=(n, dim))
    xstar = np.array([1.0, -1.0])
    b = A @ xstar + 0.1 * rng.normal(size=n)
    full_grad = lambda x: A.T @ (A @ x - b) / n

    def run(stochastic, steps=200, lr=0.02):
        x = np.array([-1.5, 1.5]); path = [x.copy()]
        for t in range(steps):
            if stochastic:
                i = rng.integers(n, size=16)
                grd = A[i].T @ (A[i] @ x - b[i]) / 16
            else:
                grd = full_grad(x)
            x = x - lr * grd; path.append(x.copy())
        return np.array(path)

    gd, sg = run(False), run(True)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    gx, gy = np.meshgrid(np.linspace(-2, 2, 120), np.linspace(-2, 2, 120))
    Z = np.array([[((A @ [a, c] - b) ** 2).mean() for a in gx[0]] for c in gy[:, 0]])
    ax.contour(gx, gy, Z, levels=15, colors=GRID, linewidths=0.5)
    ax.plot(sg[:, 0], sg[:, 1], color=HOT, lw=1.0, alpha=0.8, label="SGD (noisy)")
    ax.plot(gd[:, 0], gd[:, 1], color=C, lw=2.0, label="full-batch GD")
    ax.plot(*xstar, "*", color=ACCENT, ms=14)
    ax.set_title("SGD jitters; GD is smooth")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "sgd")


def main() -> None:
    apply_style()
    gradient_descent()
    convergence_rates()
    momentum()
    newton_method()
    convex_functions()
    adaptive_methods()
    bayesian_optimization()
    constrained_optimization()
    convex_sets()
    kkt()
    optimization_landscape()
    proximal_methods()
    quasi_newton()
    sgd()


if __name__ == "__main__":
    main()
