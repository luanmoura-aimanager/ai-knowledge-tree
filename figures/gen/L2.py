"""Figures for pillar L2 (differentiation). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GOOD, apply_style, color, save

SUB = "L2"
C = color(SUB)  # pillar-L accent


def derivative_definition() -> None:
    """Secant lines through (a, f(a)) for shrinking h collapse onto the tangent.
    f(x) = x^2 at a = 1: secant slopes 2 + h march toward the tangent slope 2."""
    import matplotlib.pyplot as plt

    f = lambda t: t**2
    a = 1.0
    x = np.linspace(-0.4, 3.2, 400)

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(x, f(x), color=C, lw=2.4, label=r"$f(x) = x^2$")

    hs = [2.0, 1.0, 0.5, 0.1]
    greys = ["#3a4374", "#4a5598", "#5d6bbf", "#7d8be0"]
    for h, g in zip(hs, greys):
        slope = (f(a + h) - f(a)) / h        # = 2 + h
        xx = np.linspace(a - 0.7, a + max(h, 0.8) + 0.55, 50)
        ax.plot(xx, f(a) + slope * (xx - a), color=g, lw=1.5,
                label=f"secant, h={h} (slope {slope:.1f})")
        ax.plot([a + h], [f(a + h)], marker="o", ms=5, color=g)

    ax.plot(x, f(a) + 2 * (x - a), color=HOT, lw=2.0, ls="--",
            label="tangent (slope 2)")
    ax.plot([a], [f(a)], marker="o", ms=7, color="#e6e9f5", zorder=5)
    ax.set_xlim(-0.4, 3.2)
    ax.set_ylim(-1.2, 7.5)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Secants through (1, 1) collapse onto the tangent as h shrinks")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "derivative-definition")


def differentiation_rules() -> None:
    """f and f' stacked: where f' is positive f rises, where f' is negative f
    falls, and f' crosses zero exactly at f's flat points. f(x) = x^3 - 3x."""
    import matplotlib.pyplot as plt

    x = np.linspace(-2.4, 2.4, 500)
    f = x**3 - 3 * x
    df = 3 * x**2 - 3

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)
    ax1.plot(x, f, color=C, lw=2.2, label=r"$f(x) = x^3 - 3x$")
    ax1.plot([-1, 1], [2, -2], "o", ms=7, color=HOT, zorder=5)
    ax1.legend(fontsize=9, loc="upper left")
    ax1.set_ylabel("f(x)")

    ax2.plot(x, df, color=ACCENT, lw=2.2, label=r"$f'(x) = 3x^2 - 3$")
    ax2.axhline(0, color=FG_MUTE, lw=1.0)
    ax2.plot([-1, 1], [0, 0], "o", ms=7, color=HOT, zorder=5)
    ax2.fill_between(x, df, 0, where=df > 0, color=GOOD, alpha=0.15)
    ax2.fill_between(x, df, 0, where=df < 0, color=HOT, alpha=0.15)
    ax2.legend(fontsize=9, loc="upper center")
    ax2.set_xlabel("x")
    ax2.set_ylabel("f'(x)")

    fig.suptitle("The derivative's sign is the function's direction", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "differentiation-rules")


def chain_rule() -> None:
    """f(g(x)) = sin(x^2): the inner rate g'(x) = 2x stretches the outer
    oscillation, so the derivative's envelope grows linearly. Top: the
    composite; bottom: its derivative 2x cos(x^2) inside the envelope +/-2x."""
    import matplotlib.pyplot as plt

    x = np.linspace(0, 4 * np.pi**0.5, 800)
    y = np.sin(x**2)
    dy = 2 * x * np.cos(x**2)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)
    ax1.plot(x, y, color=C, lw=1.8, label=r"$\sin(x^2)$")
    ax1.set_ylabel("value")
    ax1.legend(fontsize=9, loc="lower left")

    ax2.plot(x, dy, color=ACCENT, lw=1.5, label=r"$(\sin(x^2))' = 2x\cos(x^2)$")
    ax2.plot(x, 2 * x, color=HOT, lw=1.6, ls="--", label=r"envelope $\pm 2x$ (inner rate)")
    ax2.plot(x, -2 * x, color=HOT, lw=1.6, ls="--")
    ax2.set_xlabel("x")
    ax2.set_ylabel("rate")
    ax2.legend(fontsize=9, loc="lower left")

    fig.suptitle("Chain rule: the inner rate 2x scales the outer derivative", y=1.0)
    fig.tight_layout()
    save(fig, SUB, "chain-rule")


def implicit_log_differentiation() -> None:
    """The unit circle is no function y = f(x), yet implicit differentiation
    hands every point a tangent: slope -x/y. Tangents drawn at six points."""
    import matplotlib.pyplot as plt

    t = np.linspace(0, 2 * np.pi, 400)
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    ax.plot(np.cos(t), np.sin(t), color=C, lw=2.2, label=r"$x^2 + y^2 = 1$")

    for ang in [0.5, 1.4, 2.4, 3.5, 4.4, 5.6]:
        px, py = np.cos(ang), np.sin(ang)
        ax.plot([px], [py], "o", ms=6, color=HOT, zorder=5)
        if abs(py) > 1e-9:
            m = -px / py                       # dy/dx = -x/y from 2x + 2y y' = 0
            xx = np.linspace(px - 0.55, px + 0.55, 20)
            ax.plot(xx, py + m * (xx - px), color=ACCENT, lw=1.4)
        else:
            ax.axvline(px, ymin=0.3, ymax=0.7, color=ACCENT, lw=1.4)

    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(r"Implicit differentiation: tangent slope $-x/y$ on the circle")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "implicit-log-differentiation")


def mvt_lhopital() -> None:
    """The mean value theorem on f(x) = x^3 - x over [a, b]: somewhere between
    the endpoints the tangent is parallel to the secant. Both lines drawn."""
    import matplotlib.pyplot as plt

    f = lambda t: t**3 - t
    df = lambda t: 3 * t**2 - 1
    a, b = -0.2, 1.5
    sec = (f(b) - f(a)) / (b - a)
    # Solve f'(c) = sec on (a, b): c = sqrt((sec + 1)/3), positive root in range
    c = np.sqrt((sec + 1) / 3)

    x = np.linspace(-0.6, 1.8, 400)
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(x, f(x), color=C, lw=2.4, label=r"$f(x) = x^3 - x$")
    ax.plot([a, b], [f(a), f(b)], color=ACCENT, lw=1.8, marker="o", ms=6,
            label=f"secant on [{a}, {b}] (slope {sec:.2f})")
    xx = np.linspace(c - 0.55, c + 0.55, 20)
    ax.plot(xx, f(c) + sec * (xx - c), color=HOT, lw=2.0, ls="--",
            label=f"parallel tangent at c = {c:.2f}")
    ax.plot([c], [f(c)], "o", ms=7, color=HOT, zorder=5)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("MVT: some interior tangent matches the secant's slope")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "mvt-lhopital")


def linearization() -> None:
    """sqrt(x) against its tangent line at a = 4, with the error shaded. Inset
    bars: the error at distances 0.5, 1, 2 from a roughly quadruples per
    doubling, the quadratic signature |error| ~ |x-a|^2."""
    import matplotlib.pyplot as plt

    f = np.sqrt
    a = 4.0
    L = lambda t: 2.0 + (t - a) / 4.0          # f(a) + f'(a)(x-a), f'(4) = 1/4

    x = np.linspace(0.5, 8.5, 400)
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(x, f(x), color=C, lw=2.4, label=r"$\sqrt{x}$")
    ax.plot(x, L(x), color=HOT, lw=1.8, ls="--",
            label=r"tangent $L(x) = 2 + (x-4)/4$")
    ax.fill_between(x, f(x), L(x), color=ACCENT, alpha=0.25,
                    label=r"error $|\sqrt{x} - L(x)|$")
    ax.plot([a], [2], "o", ms=7, color="#e6e9f5", zorder=5)

    for d in [0.5, 1.0, 2.0]:
        e = abs(f(a + d) - L(a + d))
        ax.annotate(f"err({a + d:.1f}) = {e:.4f}", (a + d, L(a + d)),
                    xytext=(a + d - 0.4, L(a + d) + 0.42), fontsize=8,
                    color="#e6e9f5",
                    arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.0))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Linearization: tiny error nearby, quadratic growth away")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "linearization")


def main() -> None:
    apply_style()
    derivative_definition()
    differentiation_rules()
    chain_rule()
    implicit_log_differentiation()
    mvt_lhopital()
    linearization()


if __name__ == "__main__":
    main()
