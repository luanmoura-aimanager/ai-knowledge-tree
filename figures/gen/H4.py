"""Figures for pillar H4 (exploration). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, apply_style, color, save

SUB = "H4"
C = color(SUB)  # pillar-H accent (pink)


def bandits_exploration() -> None:
    """UCB explores optimistically: it adds an uncertainty bonus to each arm's mean,
    so rarely-pulled arms get a wide bonus and stay candidates until enough data
    shrinks it. The bonus narrows as √(ln t / n), focusing pulls on the best arm.
    rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    mus = [0.3, 0.55, 0.7, 0.45]
    K, T = len(mus), 2000
    n = np.ones(K); val = np.array(mus) + rng.normal(0, 0.1, K)
    bonus_hist = [[] for _ in range(K)]
    for t in range(1, T):
        ucb = val + np.sqrt(2 * np.log(t + 1) / n)
        a = int(np.argmax(ucb))
        r = rng.random() < mus[a]
        val[a] += (r - val[a]) / n[a]; n[a] += 1
        for k in range(K):
            bonus_hist[k].append(np.sqrt(2 * np.log(t + 1) / n[k]))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    cols = [FG_MUTE, ACCENT, C, GOOD]
    for k in range(K):
        ax.plot(bonus_hist[k], color=cols[k], lw=1.8,
                label=f"arm {k} (μ={mus[k]})")
    ax.set_title("UCB exploration bonus shrinks with pulls")
    ax.set_xlabel("time step"); ax.set_ylabel("exploration bonus")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "bandits-exploration")


def intrinsic_motivation() -> None:
    """Intrinsic motivation rewards novelty: a curiosity bonus is large for rarely-
    visited states and decays as a state is seen more often (here ∝ 1/√count), so the
    agent is drawn to unexplored regions even without external reward. rng(0)."""
    import matplotlib.pyplot as plt

    counts = np.arange(1, 60)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(counts, 1 / np.sqrt(counts), color=C, lw=2.6, label="count-based  $1/\\sqrt{n}$")
    ax.plot(counts, np.exp(-counts / 12), color=ACCENT, lw=2.2, label="prediction-error (decaying)")
    ax.fill_between(counts, 1 / np.sqrt(counts), color=C, alpha=0.12)
    ax.set_title("Intrinsic reward decays as states become familiar")
    ax.set_xlabel("times state visited"); ax.set_ylabel("intrinsic reward")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "intrinsic-motivation")


def main() -> None:
    apply_style()
    bandits_exploration()
    intrinsic_motivation()


if __name__ == "__main__":
    main()
