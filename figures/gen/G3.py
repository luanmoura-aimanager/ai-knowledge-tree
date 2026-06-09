"""Figures for pillar G3 (deep forecasting). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "G3"
C = color(SUB)  # pillar-G accent (teal)


def deepar() -> None:
    """DeepAR outputs a probabilistic forecast: instead of a single line it predicts a
    distribution per step, so the forecast is a median path inside widening quantile
    bands that honestly express growing uncertainty over the horizon. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, h = 100, 40
    t = np.arange(n)
    hist = 10 + 0.05 * t + 2 * np.sin(2 * np.pi * t / 24) + rng.normal(0, 0.5, n)
    ft = np.arange(n, n + h)
    median = 10 + 0.05 * ft + 2 * np.sin(2 * np.pi * ft / 24)
    width = 0.6 + 0.06 * np.arange(h)

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.plot(t, hist, color=C, lw=1.4, label="history")
    ax.plot(ft, median, color=HOT, lw=2.0, label="forecast median")
    ax.fill_between(ft, median - 2.6 * width, median + 2.6 * width, color=HOT, alpha=0.12,
                    label="P1–P99")
    ax.fill_between(ft, median - 1.3 * width, median + 1.3 * width, color=HOT, alpha=0.18,
                    label="P10–P90")
    ax.axvline(n - 1, color=FG_MUTE, ls=":", lw=1.2)
    ax.set_title("DeepAR: probabilistic forecast")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "deepar")


def main() -> None:
    apply_style()
    deepar()


if __name__ == "__main__":
    main()
