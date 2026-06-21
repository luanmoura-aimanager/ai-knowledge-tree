"""Figures for pillar L5 (vector calculus & multiple integrals). See _style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GOOD, apply_style, color, save

SUB = "L5"
C = color(SUB)  # pillar-L accent


def multiple_integrals() -> None:
    """Iterated integration: the same region sliced into vertical strips
    (dx outer) or horizontal strips (dy outer). Fubini says both stacks of
    1D integrals total the same volume."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.7))

    # Region: under y = 4 - x^2, above y = 0, for x in [-2, 2]
    x = np.linspace(-2, 2, 300)
    top = 4 - x**2

    for ax, mode in [(ax1, "v"), (ax2, "h")]:
        ax.plot(x, top, color=C, lw=2.2)
        ax.axhline(0, color=FG_MUTE, lw=1.0)
        if mode == "v":
            for xv in np.linspace(-1.8, 1.8, 13):
                ax.plot([xv, xv], [0, 4 - xv**2], color=ACCENT, lw=2.2, alpha=0.6)
            ax.set_title("vertical strips: dy inner, dx outer")
        else:
            for yv in np.linspace(0.15, 3.85, 13):
                xe = np.sqrt(max(4 - yv, 0))
                ax.plot([-xe, xe], [yv, yv], color=GOOD, lw=2.2, alpha=0.6)
            ax.set_title("horizontal strips: dx inner, dy outer")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    fig.suptitle("One region, two slicing orders, one volume (Fubini)", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "multiple-integrals")


def change_of_variables() -> None:
    """The polar map carries a (r, theta) rectangle to an annular wedge; the
    area element stretches by the Jacobian determinant r: outer cells of the
    wedge are visibly fatter than inner ones."""
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.8))

    r0, r1 = 0.6, 1.8
    t0, t1 = 0.3, 1.25

    for rv in np.linspace(r0, r1, 7):
        ax1.plot([t0, t1], [rv, rv], color=FG_MUTE, lw=0.8)
        th = np.linspace(t0, t1, 60)
        ax2.plot(rv * np.cos(th), rv * np.sin(th), color=C, lw=0.9)
    for tv in np.linspace(t0, t1, 8):
        ax1.plot([tv, tv], [r0, r1], color=FG_MUTE, lw=0.8)
        rr = np.linspace(r0, r1, 60)
        ax2.plot(rr * np.cos(tv), rr * np.sin(tv), color=C, lw=0.9)

    # Highlight one small inner cell and one outer cell in both views
    cells = [(0.45, 0.65, r0, r0 + 0.2, ACCENT), (0.45, 0.65, r1 - 0.2, r1, HOT)]
    for ta, tb, ra, rb, col in cells:
        ax1.fill([ta, tb, tb, ta], [ra, ra, rb, rb], color=col, alpha=0.5)
        th = np.linspace(ta, tb, 30)
        xs = np.concatenate([ra * np.cos(th), (rb * np.cos(th))[::-1]])
        ys = np.concatenate([ra * np.sin(th), (rb * np.sin(th))[::-1]])
        ax2.fill(xs, ys, color=col, alpha=0.5)

    ax1.set_xlabel(r"$\theta$")
    ax1.set_ylabel("r")
    ax1.set_title(r"$(r, \theta)$ space: equal rectangles")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_aspect("equal")
    ax2.set_title(r"$(x, y)$ space: area scales with $r$")
    fig.suptitle(r"Change of variables: $dA = r\,dr\,d\theta$, the Jacobian at work", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "change-of-variables")


def line_integrals() -> None:
    """Work along two paths through the non-conservative field F = (-y, x):
    counterclockwise quarter-circle vs straight chord between the same
    endpoints. Different work values: path dependence made visible."""
    import matplotlib.pyplot as plt

    g = np.linspace(-0.2, 1.4, 12)
    GX, GY = np.meshgrid(g, g)

    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    ax.quiver(GX, GY, -GY, GX, color=FG_MUTE, width=0.0035, alpha=0.8)

    t = np.linspace(0, np.pi / 2, 100)
    ax.plot(np.cos(t), np.sin(t), color=C, lw=2.6,
            label=r"arc: $W = \pi/2 \approx 1.571$")
    s = np.linspace(0, 1, 50)
    ax.plot(1 - s, s, color=HOT, lw=2.4, ls="--", label="chord: $W = 1$")
    ax.plot([1, 0], [0, 1], "o", ms=7, color="#e6e9f5", zorder=5)
    ax.annotate("start", (1, 0), xytext=(1.12, 0.04), color="#e6e9f5", fontsize=9)
    ax.annotate("end", (0, 1), xytext=(-0.18, 1.1), color="#e6e9f5", fontsize=9)

    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Same endpoints, different work: F = (−y, x) is not conservative")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "line-integrals")


def divergence_curl() -> None:
    """A source field (positive divergence, zero curl) next to a rotation
    field (zero divergence, positive curl): the two local behaviors the
    operators measure."""
    import matplotlib.pyplot as plt

    g = np.linspace(-1.5, 1.5, 13)
    X, Y = np.meshgrid(g, g)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.9))
    ax1.quiver(X, Y, X, Y, color=C, width=0.005)
    ax1.set_title("source F = (x, y):  div = 2,  curl = 0")
    ax2.quiver(X, Y, -Y, X, color=ACCENT, width=0.005)
    ax2.set_title("rotation F = (−y, x):  div = 0,  curl = 2")
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Divergence measures outflow; curl measures circulation", y=1.04)
    fig.tight_layout()
    save(fig, SUB, "divergence-curl")


def integral_theorems() -> None:
    """Green's theorem as cancellation: tile a region with small circulating
    cells; interior edges cancel pairwise, leaving only the boundary loop."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.8, 5.0))

    n = 4
    for i in range(n):
        for j in range(n):
            cx, cy = i + 0.5, j + 0.5
            th = np.linspace(0, 2 * np.pi, 60)
            rr = 0.32
            ax.plot(cx + rr * np.cos(th), cy + rr * np.sin(th),
                    color=FG_MUTE, lw=1.1)
            ax.annotate("", (cx + rr * np.cos(0.5), cy + rr * np.sin(0.5)),
                        (cx + rr * np.cos(0.3), cy + rr * np.sin(0.3)),
                        arrowprops=dict(arrowstyle="-|>", color=FG_MUTE, lw=1.1))

    box = np.array([[0, 0], [n, 0], [n, n], [0, n], [0, 0]], float).T
    ax.plot(box[0], box[1], color=HOT, lw=2.8)
    for (x0, y0, x1, y1) in [(2, 0, 2.6, 0), (4, 2, 4, 2.6), (2.6, 4, 2, 4), (0, 2.6, 0, 2)]:
        ax.annotate("", (x1, y1), (x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2))

    ax.text(n / 2, -0.75,
            "interior edges cancel in pairs;\nonly the boundary circulation survives",
            ha="center", color="#e6e9f5", fontsize=10)
    ax.set_xlim(-0.7, n + 0.7)
    ax.set_ylim(-1.3, n + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Green's theorem: sum of cell curls = boundary circulation")
    fig.tight_layout()
    save(fig, SUB, "integral-theorems")


def main() -> None:
    apply_style()
    multiple_integrals()
    change_of_variables()
    line_integrals()
    divergence_curl()
    integral_theorems()


if __name__ == "__main__":
    main()
