"""Figures for pillar L3 (integration & series). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GOOD, apply_style, color, save

SUB = "L3"
C = color(SUB)  # pillar-L accent


def riemann_integral() -> None:
    """Left-endpoint Riemann rectangles for f(x) = x^2 on [0, 1] at n = 4, 16,
    64: the staircase fills in toward the area 1/3, and the printed sums creep
    up to it from below (f is increasing, so left sums underestimate)."""
    import matplotlib.pyplot as plt

    f = lambda t: t**2
    x = np.linspace(0, 1, 300)

    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.2), sharey=True)
    for ax, n in zip(axes, [4, 16, 64]):
        xi = np.linspace(0, 1, n + 1)[:-1]
        w = 1.0 / n
        s = np.sum(f(xi) * w)
        ax.bar(xi, f(xi), width=w, align="edge", color=C, alpha=0.45,
               edgecolor=C, linewidth=0.6)
        ax.plot(x, f(x), color=HOT, lw=2.0)
        ax.set_title(f"n = {n}:  sum = {s:.4f}")
        ax.set_xlabel("x")
    axes[0].set_ylabel("f(x) = x²")
    fig.suptitle("Riemann sums closing in on the area 1/3", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "riemann-integral")


def fundamental_theorem() -> None:
    """An integrand f(t) = sin(t) + 1.2 and its accumulation A(x): where f is
    large, A climbs steeply; where f dips, A flattens. The slope of A at the
    marked point equals the height of f there, which is FTC part 1."""
    import matplotlib.pyplot as plt

    t = np.linspace(0, 2 * np.pi, 600)
    f = np.sin(t) + 1.2
    A = -np.cos(t) + 1.2 * t + 1.0          # antiderivative, A(0) = 0

    x0 = 2.2
    f0 = np.sin(x0) + 1.2
    A0 = -np.cos(x0) + 1.2 * x0 + 1.0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)
    ax1.plot(t, f, color=C, lw=2.2, label="integrand f(t)")
    ax1.fill_between(t[t <= x0], f[t <= x0], color=C, alpha=0.22)
    ax1.axvline(x0, color=FG_MUTE, lw=1.0, ls=":")
    ax1.plot([x0], [f0], "o", ms=6, color=HOT, zorder=5)
    ax1.annotate(f"height f(x) = {f0:.2f}", (x0, f0), xytext=(x0 + 0.45, f0 + 0.32),
                 color="#e6e9f5", fontsize=9,
                 arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))
    ax1.set_ylabel("f(t)")
    ax1.legend(fontsize=9, loc="lower left")

    ax2.plot(t, A, color=ACCENT, lw=2.2, label="accumulation A(x) = shaded area")
    xx = np.linspace(x0 - 0.9, x0 + 0.9, 20)
    ax2.plot(xx, A0 + f0 * (xx - x0), color=HOT, lw=1.8, ls="--",
             label=f"tangent slope = {f0:.2f} = f(x)")
    ax2.plot([x0], [A0], "o", ms=6, color=HOT, zorder=5)
    ax2.axvline(x0, color=FG_MUTE, lw=1.0, ls=":")
    ax2.set_xlabel("x")
    ax2.set_ylabel("A(x)")
    ax2.legend(fontsize=9, loc="upper left")

    fig.suptitle("FTC: the accumulation's slope is the integrand's height", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "fundamental-theorem")


def integration_techniques() -> None:
    """Substitution u = x^2 reshapes the region without changing its area:
    the integral of 2x e^(x^2) on [0,1] becomes the integral of e^u on [0,1].
    Both shaded regions measure e - 1."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.8))

    x = np.linspace(0, 1, 300)
    y1 = 2 * x * np.exp(x**2)
    ax1.plot(x, y1, color=C, lw=2.2)
    ax1.fill_between(x, y1, color=C, alpha=0.3)
    ax1.set_title(r"$\int_0^1 2x\,e^{x^2}\,dx$")
    ax1.set_xlabel("x")

    u = np.linspace(0, 1, 300)
    y2 = np.exp(u)
    ax2.plot(u, y2, color=ACCENT, lw=2.2)
    ax2.fill_between(u, y2, color=ACCENT, alpha=0.3)
    ax2.set_title(r"after $u = x^2$:  $\int_0^1 e^{u}\,du$")
    ax2.set_xlabel("u")

    for ax in (ax1, ax2):
        ax.set_ylim(0, 6)
        ax.text(0.5, 4.6, f"area = e − 1 ≈ {np.e - 1:.4f}", ha="center",
                color="#e6e9f5", fontsize=10)
    fig.suptitle("Substitution reshapes the region; the area is invariant", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "integration-techniques")


def improper_integrals() -> None:
    """Tails of 1/x and 1/x^2 on [1, inf): visually similar, opposite fates.
    The shaded 1/x^2 tail encloses finite area 1; the 1/x tail diverges. The
    Gaussian, decaying faster than any power, encloses sqrt(pi)."""
    import matplotlib.pyplot as plt

    x = np.linspace(1, 8, 400)
    xg = np.linspace(-3, 3, 400)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.8))
    ax1.plot(x, 1 / x, color=HOT, lw=2.2, label=r"$1/x$: area $\to \infty$")
    ax1.plot(x, 1 / x**2, color=C, lw=2.2, label=r"$1/x^2$: area $= 1$")
    ax1.fill_between(x, 1 / x**2, color=C, alpha=0.3)
    ax1.fill_between(x, 1 / x**2, 1 / x, color=HOT, alpha=0.12)
    ax1.set_xlabel("x")
    ax1.set_title("two tails, opposite fates")
    ax1.legend(fontsize=8)

    ax2.plot(xg, np.exp(-xg**2), color=ACCENT, lw=2.2,
             label=r"$e^{-x^2}$: area $=\sqrt{\pi}$")
    ax2.fill_between(xg, np.exp(-xg**2), color=ACCENT, alpha=0.3)
    ax2.set_xlabel("x")
    ax2.set_title("the Gaussian integral")
    ax2.legend(fontsize=8)

    fig.suptitle("Improper integrals: convergence is a race against the tail", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "improper-integrals")


def taylor_polynomials() -> None:
    """sin(x) and its Taylor polynomials T1, T3, T5, T7 at 0: each added
    degree hugs the curve farther out before peeling away."""
    import matplotlib.pyplot as plt

    x = np.linspace(-np.pi - 0.6, np.pi + 0.6, 500)

    T = {
        1: x,
        3: x - x**3 / 6,
        5: x - x**3 / 6 + x**5 / 120,
        7: x - x**3 / 6 + x**5 / 120 - x**7 / 5040,
    }

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(x, np.sin(x), color="#e6e9f5", lw=2.6, label=r"$\sin x$")
    for (deg, y), col in zip(T.items(), [HOT, ACCENT, GOOD, C]):
        ax.plot(x, y, color=col, lw=1.7, ls="--", label=f"$T_{deg}$")
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Taylor polynomials of sin at 0: each degree hugs farther")
    ax.legend(loc="lower right", fontsize=9, ncol=2)
    fig.tight_layout()
    save(fig, SUB, "taylor-polynomials")


def power_series() -> None:
    """Partial sums of the geometric series against 1/(1-x): inside the
    radius |x| < 1 they converge (fast in the middle, slowly near the edge);
    past x = 1 they explode. The vertical line marks the radius."""
    import matplotlib.pyplot as plt

    x = np.linspace(-1.4, 0.96, 500)
    target = 1 / (1 - x)

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(x, target, color="#e6e9f5", lw=2.6, label=r"$\frac{1}{1-x}$")
    for N, col in zip([2, 5, 10, 30], [HOT, ACCENT, GOOD, C]):
        S = np.sum([x**k for k in range(N + 1)], axis=0)
        ax.plot(x, S, color=col, lw=1.6, ls="--", label=f"$S_{{{N}}}$")
    ax.axvline(-1, color=FG_MUTE, lw=1.4, ls=":")
    ax.axvline(1, color=FG_MUTE, lw=1.4, ls=":")
    ax.annotate("radius of convergence |x| = 1", (-1, 8.5), xytext=(-0.86, 8.5),
                color="#9aa3c7", fontsize=9)
    ax.set_ylim(-3, 12)
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.set_title("Geometric partial sums: convergence strictly inside the radius")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "power-series")


def main() -> None:
    apply_style()
    riemann_integral()
    fundamental_theorem()
    integration_techniques()
    improper_integrals()
    taylor_polynomials()
    power_series()


if __name__ == "__main__":
    main()
