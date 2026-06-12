"""Figures for pillar L1 (limits & continuity). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GOOD, apply_style, color, save

SUB = "L1"
C = color(SUB)  # pillar-L accent


def functions_and_graphs() -> None:
    """Small-multiples grid of the four elementary function families a calculus
    course leans on: power, exponential, logarithm, sine. One panel each, with
    the qualitative behavior (growth, domain edge, periodicity) visible."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.2))

    x = np.linspace(-2.2, 2.2, 400)
    ax = axes[0, 0]
    ax.plot(x, x**2, color=C, label="$x^2$")
    ax.plot(x, x**3, color=FG_MUTE, ls="--", label="$x^3$")
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.set_title("powers")
    ax.legend(fontsize=8)

    x = np.linspace(-2.5, 2.5, 400)
    ax = axes[0, 1]
    ax.plot(x, np.exp(x), color=C, label="$e^x$")
    ax.plot(x, np.exp(-x), color=FG_MUTE, ls="--", label="$e^{-x}$")
    ax.set_title("exponentials")
    ax.legend(fontsize=8)

    x = np.linspace(0.02, 6, 400)
    ax = axes[1, 0]
    ax.plot(x, np.log(x), color=C, label=r"$\ln x$")
    ax.axvline(0, color=HOT, lw=1.2, ls=":")
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.set_title("logarithm (domain edge at 0)")
    ax.legend(fontsize=8)

    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    ax = axes[1, 1]
    ax.plot(x, np.sin(x), color=C, label=r"$\sin x$")
    ax.plot(x, np.cos(x), color=FG_MUTE, ls="--", label=r"$\cos x$")
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.set_title("trig (period $2\\pi$)")
    ax.legend(fontsize=8)

    fig.suptitle("The elementary functions at a glance", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "functions-and-graphs")


def limits() -> None:
    """The epsilon-delta picture on f(x) = sin(x)/x at x -> 0: an epsilon band
    around the limit L = 1 and the delta window around 0 that keeps the graph
    inside the band. The point at x = 0 is missing; the limit does not care."""
    import matplotlib.pyplot as plt

    eps = 0.05
    # sin(x)/x stays within eps of 1 when x^2/6 < eps, i.e. |x| < sqrt(6 eps).
    delta = np.sqrt(6 * eps) * 0.92  # a hair inside, so the band visibly holds

    x = np.linspace(-3.0, 3.0, 1201)
    x = x[np.abs(x) > 1e-9]
    y = np.sin(x) / x

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.plot(x, y, color=C, lw=2.2, label=r"$f(x) = \sin(x)/x$")
    ax.axhspan(1 - eps, 1 + eps, color=ACCENT, alpha=0.18,
               label=r"$\varepsilon$-band around $L=1$")
    ax.axvspan(-delta, delta, color=HOT, alpha=0.12,
               label=r"$\delta$-window around $a=0$")
    ax.axhline(1, color=ACCENT, lw=1.0, ls="--")
    for s in (-1, 1):
        ax.axvline(s * delta, color=HOT, lw=1.2, ls=":")
    # The hole: f is undefined at 0 even though the limit is 1.
    ax.plot([0], [1], marker="o", ms=8, mfc="none", mec=C, mew=1.8)
    ax.annotate("f(0) undefined,\nlimit still 1", (0, 1), xytext=(0.9, 1.10),
                color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_ylim(-0.35, 1.25)
    ax.set_title(r"Inside the $\delta$-window, the graph stays in the $\varepsilon$-band")
    ax.legend(loc="lower center", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "limits")


def limit_laws() -> None:
    """The squeeze theorem on x^2 sin(1/x): the oscillation never escapes the
    envelope +/- x^2, and both envelope curves go to 0, so the trapped function
    must too. The plot shows the wild oscillation dying inside the parabolas."""
    import matplotlib.pyplot as plt

    x = np.linspace(-0.5, 0.5, 4001)
    x = x[np.abs(x) > 1e-6]
    y = x**2 * np.sin(1.0 / x)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(x, y, color=C, lw=1.0, label=r"$x^2 \sin(1/x)$")
    ax.plot(x, x**2, color=HOT, lw=1.8, ls="--", label=r"upper bound $x^2$")
    ax.plot(x, -(x**2), color=ACCENT, lw=1.8, ls="--", label=r"lower bound $-x^2$")
    ax.plot([0], [0], marker="o", ms=6, color=GOOD, zorder=5)
    ax.annotate("both bounds meet at 0:\nthe limit is forced", (0, 0),
                xytext=(0.13, -0.16), color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("The squeeze theorem: trapped between two curves that agree at 0")
    ax.legend(loc="upper center", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "limit-laws")


def continuity() -> None:
    """One function exhibiting the three discontinuity types: a removable hole
    at x = -2, a jump at x = 1, and an infinite (vertical asymptote) blowup at
    x = 3. Open/closed dots mark which value the function takes."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.0, 4.4))

    # Piece 1: smooth up to the removable hole at x = -2 (value relocated).
    x1 = np.linspace(-4, 1, 400)
    f1 = 0.25 * (x1 + 3) ** 2 - 1
    hole_y = 0.25 * (-2 + 3) ** 2 - 1
    ax.plot(x1, f1, color=C, lw=2.2)
    ax.plot([-2], [hole_y], marker="o", ms=8, mfc="none", mec=C, mew=1.8)
    ax.plot([-2], [hole_y + 1.6], marker="o", ms=7, color=C)
    ax.annotate("removable:\nlimit exists, value moved", (-2, hole_y + 1.6),
                xytext=(-3.9, 2.6), color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))

    # Piece 2: jump at x = 1.
    left_end = 0.25 * (1 + 3) ** 2 - 1          # = 3, open at x=1 from the left
    x2 = np.linspace(1, 2.95, 300)
    f2 = 0.8 * (x2 - 1) + 0.5                    # restarts lower, closed at x=1
    ax.plot(x2, f2, color=C, lw=2.2)
    ax.plot([1], [left_end], marker="o", ms=8, mfc="none", mec=C, mew=1.8)
    ax.plot([1], [f2[0]], marker="o", ms=7, color=C)
    ax.annotate("jump:\nleft and right limits differ", (1, f2[0]),
                xytext=(-0.6, -2.4), color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))

    # Piece 3: infinite discontinuity at x = 3.
    x3 = np.linspace(3.05, 4.5, 300)
    f3 = 1.0 / (x3 - 3) - 0.5
    ax.plot(x3, f3, color=C, lw=2.2)
    x2b = np.linspace(2.0, 2.95, 200)            # left branch blowing down
    ax.plot(x2b, -1.0 / (3 - x2b) + 2.4, color=C, lw=2.2)
    ax.axvline(3, color=HOT, lw=1.4, ls=":")
    ax.annotate("infinite:\nvertical asymptote", (3, 4.0), xytext=(3.45, 4.0),
                color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))

    ax.set_xlim(-4.3, 4.8)
    ax.set_ylim(-3.2, 5.2)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("The three ways continuity fails")
    fig.tight_layout()
    save(fig, SUB, "continuity")


def sequences() -> None:
    """Left: two convergent sequences, the monotone (1 + 1/n)^n climbing to e
    and the alternating (-0.8)^n collapsing to 0. Right: partial sums, the
    geometric series leveling off at 2 while the harmonic series keeps growing."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 4.0))

    n = np.arange(1, 31)
    a = (1 + 1 / n) ** n
    b = (-0.8) ** n
    ax1.plot(n, a, marker="o", ms=3.5, lw=1.0, color=C,
             label=r"$(1+1/n)^n \to e$")
    ax1.plot(n, b, marker="o", ms=3.5, lw=1.0, color=ACCENT,
             label=r"$(-0.8)^n \to 0$")
    ax1.axhline(np.e, color=C, lw=1.0, ls="--")
    ax1.axhline(0, color=ACCENT, lw=1.0, ls="--")
    ax1.set_xlabel("n")
    ax1.set_title("convergent sequences")
    ax1.legend(fontsize=8, loc="center right")

    m = np.arange(1, 61)
    geo = np.cumsum((0.5) ** (m - 1))            # -> 2
    harm = np.cumsum(1.0 / m)                    # diverges like ln n
    ax2.plot(m, geo, lw=2.0, color=C, label=r"$\sum (1/2)^k \to 2$")
    ax2.plot(m, harm, lw=2.0, color=HOT, label=r"$\sum 1/k$ diverges")
    ax2.axhline(2, color=C, lw=1.0, ls="--")
    ax2.set_xlabel("n")
    ax2.set_title("partial sums")
    ax2.legend(fontsize=8, loc="center right")

    fig.suptitle("Convergence is about the tail settling down", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "sequences")


def growth_rates() -> None:
    """The growth-rate race on a log scale: log x, x, x^2, and 2^x over the
    same range. On a log axis the exponential is the only straight line, and
    every curve below it eventually falls behind, which is what little-o says."""
    import matplotlib.pyplot as plt

    x = np.linspace(1, 30, 400)

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.semilogy(x, np.log(x), color=FG_MUTE, lw=2.0, label=r"$\ln x$")
    ax.semilogy(x, x, color=ACCENT, lw=2.0, label=r"$x$")
    ax.semilogy(x, x**2, color=GOOD, lw=2.0, label=r"$x^2$")
    ax.semilogy(x, 2**x, color=HOT, lw=2.2, label=r"$2^x$")
    ax.annotate("straight line on a log axis\n= exponential growth",
                (22, 2.0**22), xytext=(8, 1e7), color="#e6e9f5", fontsize=9,
                arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.2))
    ax.set_xlabel("x")
    ax.set_ylabel("value (log scale)")
    ax.set_title("The growth hierarchy: log < polynomial < exponential")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "growth-rates")


def main() -> None:
    apply_style()
    functions_and_graphs()
    limits()
    limit_laws()
    continuity()
    sequences()
    growth_rates()


if __name__ == "__main__":
    main()
