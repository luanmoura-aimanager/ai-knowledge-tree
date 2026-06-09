"""Figures for pillar E6 (RAG, agents, reasoning). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, apply_style, color, save

SUB = "E6"
C = color(SUB)  # pillar-E accent (purple)


def test_time_compute() -> None:
    """Spending more compute at inference — sampling many candidate answers and
    selecting among them — raises accuracy. A verifier (best-of-N) beats plain
    majority vote, and both improve roughly with the log of the sample budget."""
    import matplotlib.pyplot as plt

    n = np.logspace(0, 3, 60)
    majority = 0.42 + 0.30 * (1 - np.exp(-n / 60))
    best_of_n = 0.42 + 0.46 * (1 - np.exp(-n / 35))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogx(n, best_of_n, color=C, lw=2.6, label="best-of-N (verifier)")
    ax.semilogx(n, majority, color=GOOD, lw=2.6, label="majority vote")
    ax.axhline(0.42, color=FG_MUTE, ls="--", lw=1.4, label="single sample")
    ax.set_title("Test-time compute trades samples for accuracy")
    ax.set_xlabel("number of sampled solutions")
    ax.set_ylabel("accuracy")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "test-time-compute")


def main() -> None:
    apply_style()
    test_time_compute()


if __name__ == "__main__":
    main()
