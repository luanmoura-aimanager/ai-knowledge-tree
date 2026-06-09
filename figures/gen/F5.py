"""Figures for pillar F5 (variational inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, HOT, apply_style, color, save

SUB = "F5"
C = color(SUB)  # pillar-F accent (cyan)


def mean_field_vi() -> None:
    """Mean-field VI approximates the posterior with a factorized (axis-aligned)
    distribution. It centres correctly but, by ignoring correlations, it shrinks
    onto one direction and underestimates the variance — the classic mean-field
    pathology."""
    import matplotlib.pyplot as plt

    rho = 0.85
    g = np.linspace(-3.5, 3.5, 200)
    gx, gy = np.meshgrid(g, g)
    true = np.exp(-(gx**2 - 2 * rho * gx * gy + gy**2) / (2 * (1 - rho**2)))
    # mean-field optimum: independent Gaussians with the conditional variance
    v = 1 - rho**2
    mf = np.exp(-(gx**2 + gy**2) / (2 * v))

    fig, ax = plt.subplots(figsize=(6.0, 5.4))
    ax.contour(gx, gy, true, levels=6, colors=[FG_MUTE], linewidths=1.4)
    ax.contour(gx, gy, mf, levels=6, colors=[C], linewidths=1.8)
    ax.plot([], [], color=FG_MUTE, lw=1.4, label="true posterior")
    ax.plot([], [], color=C, lw=1.8, label="mean-field approx")
    ax.set_aspect("equal")
    ax.set_title("Mean-field VI underestimates variance")
    ax.set_xlabel("$\\theta_1$"); ax.set_ylabel("$\\theta_2$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "mean-field-vi")


def stochastic_vi() -> None:
    """Stochastic VI optimizes the ELBO with noisy mini-batch gradients: the bound
    climbs quickly toward the optimum but rattles around it because each step uses a
    noisy estimate, unlike the smooth full-batch ascent. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    opt = 0.0
    it = np.arange(300)
    full = opt - 6.0 * np.exp(-it / 40)
    svi = full + rng.normal(0, 0.25, it.size) * (1 - np.exp(-it / 60))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(it, svi, color=C, lw=1.0, alpha=0.8, label="stochastic VI (noisy)")
    ax.plot(it, full, color=HOT, lw=2.2, label="full-batch (smooth)")
    ax.axhline(opt, color=FG_MUTE, ls="--", lw=1.2, label="optimum")
    ax.set_title("Stochastic VI: noisy but fast ELBO ascent")
    ax.set_xlabel("iteration"); ax.set_ylabel("ELBO")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "stochastic-vi")


def main() -> None:
    apply_style()
    mean_field_vi()
    stochastic_vi()


if __name__ == "__main__":
    main()
