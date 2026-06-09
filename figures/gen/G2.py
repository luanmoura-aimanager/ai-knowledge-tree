"""Figures for pillar G2 (feature-based forecasting). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "G2"
C = color(SUB)  # pillar-G accent (teal)


def prophet() -> None:
    """Prophet models a series as an additive sum of interpretable components — a
    piecewise-linear trend plus periodic seasonality (plus holidays) — that recombine
    into the fit. Decomposing this way makes the forecast easy to read. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 200
    t = np.arange(n)
    trend = np.where(t < 100, 0.05 * t, 0.05 * 100 - 0.03 * (t - 100))
    seasonal = 2.0 * np.sin(2 * np.pi * t / 30)
    y = 10 + trend + seasonal + rng.normal(0, 0.5, n)

    fig, axes = plt.subplots(3, 1, figsize=(7.4, 5.4), sharex=True)
    axes[0].plot(y, color=FG_MUTE, lw=0.9, label="data")
    axes[0].plot(10 + trend + seasonal, color=C, lw=2.0, label="trend + seasonal")
    axes[0].set_title("Prophet = trend + seasonality"); axes[0].legend(loc="upper left", fontsize=8)
    axes[1].plot(10 + trend, color=HOT, lw=2.0)
    axes[1].set_title("trend component")
    axes[2].plot(seasonal, color=GOOD, lw=2.0)
    axes[2].set_title("seasonal component"); axes[2].set_xlabel("time")
    fig.tight_layout()
    save(fig, SUB, "prophet")


def main() -> None:
    apply_style()
    prophet()


if __name__ == "__main__":
    main()
