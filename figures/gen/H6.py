"""Figures for pillar H6 (RL with LLMs). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, apply_style, color, save

SUB = "H6"
C = color(SUB)  # pillar-H accent (pink)


def reward_hacking() -> None:
    """Reward hacking is Goodhart's law in action: optimizing a proxy reward improves
    the true objective at first, but past a point the policy exploits the gap between
    proxy and goal — the proxy keeps climbing while the true reward collapses. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    t = np.linspace(0, 10, 200)
    proxy = 1 - np.exp(-t / 1.5)
    true = 1.4 * (1 - np.exp(-t / 1.2)) - 0.16 * np.clip(t - 4, 0, None) ** 1.4
    proxy += 0.01 * rng.normal(size=t.size)
    true += 0.01 * rng.normal(size=t.size)
    peak = int(np.argmax(true))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(t, proxy, color=C, lw=2.4, label="proxy reward (optimized)")
    ax.plot(t, true, color=ACCENT, lw=2.4, label="true objective")
    ax.axvline(t[peak], color=FG_MUTE, ls=":", lw=1.4, label="divergence point")
    ax.set_title("Reward hacking: proxy and goal diverge")
    ax.set_xlabel("optimization pressure"); ax.set_ylabel("reward")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "reward-hacking")


def main() -> None:
    apply_style()
    reward_hacking()


if __name__ == "__main__":
    main()
