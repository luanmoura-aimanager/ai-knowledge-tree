"""Figures for pillar H5 (advanced RL). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, apply_style, color, save

SUB = "H5"
C = color(SUB)  # pillar-H accent (pink)


def offline_rl() -> None:
    """Offline RL learns from a fixed dataset, so it must avoid querying actions the
    data never covered: a naive policy exploits the value function's overestimates in
    those gaps (spurious peaks), while a conservative method stays near the supported
    actions. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    a = np.linspace(-3, 3, 300)
    trueQ = -(a - 0.5) ** 2 + 4
    # data only covers a band around the behavior policy
    data_a = np.concatenate([rng.normal(-0.5, 0.5, 150), rng.normal(1.0, 0.5, 150)])
    naive = trueQ + 3.5 * np.exp(-((a + 2.4) ** 2) / 0.2) + 2.8 * np.exp(-((a - 2.5) ** 2) / 0.2)
    conservative = trueQ - 2.0 * (np.abs(a - 0.25) > 1.8) * (np.abs(a - 0.25) - 1.8)

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.hist(data_a, bins=40, density=True, color=FG_MUTE, alpha=0.3, label="data coverage")
    ax.plot(a, trueQ, color=GOOD, lw=2.0, label="true Q(a)")
    ax.plot(a, naive, color=ACCENT, lw=2.0, label="naive: overestimates off-data")
    ax.plot(a, conservative, color=C, lw=2.2, label="conservative (CQL-style)")
    ax.set_ylim(-1, 8)
    ax.set_title("Offline RL: overestimation off the data")
    ax.set_xlabel("action"); ax.set_ylabel("estimated Q-value")
    ax.legend(loc="upper center", fontsize=8, ncol=2)
    fig.tight_layout()
    save(fig, SUB, "offline-rl")


def main() -> None:
    apply_style()
    offline_rl()


if __name__ == "__main__":
    main()
