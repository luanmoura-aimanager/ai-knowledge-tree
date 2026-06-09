"""Figures for pillar E4 (training & alignment). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "E4"
C = color(SUB)  # pillar-E accent (purple)


def lora() -> None:
    """LoRA freezes the weight matrix and learns a low-rank update ΔW = B A, so the
    trainable parameter count is 2·d·r instead of d² — a tiny fraction even at
    generous ranks. Shown for a 4096×4096 matrix."""
    import matplotlib.pyplot as plt

    d = 4096
    r = np.arange(1, 257)
    pct = 2 * d * r / d**2 * 100

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(r, pct, color=C, lw=2.6)
    ax.fill_between(r, pct, color=C, alpha=0.15)
    ax.axhline(100, color=FG_MUTE, ls="--", lw=1.4, label="full fine-tuning (100%)")
    ax.set_title("LoRA trainable parameters vs rank")
    ax.set_xlabel("LoRA rank $r$")
    ax.set_ylabel("trainable params (% of full, d=4096)")
    ax.set_ylim(0, 14)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "lora")


def reward_modeling() -> None:
    """A reward model is trained on preferences via the Bradley–Terry model: the
    probability that response A is preferred over B is a sigmoid of their reward
    difference, so the loss pushes the chosen response's reward above the rejected
    one's."""
    import matplotlib.pyplot as plt

    dr = np.linspace(-6, 6, 300)
    p = 1 / (1 + np.exp(-dr))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(dr, p, color=C, lw=2.6)
    ax.axhline(0.5, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.fill_between(dr, 0.5, p, where=dr > 0, color=GOOD, alpha=0.18)
    ax.fill_between(dr, p, 0.5, where=dr < 0, color=HOT, alpha=0.18)
    ax.set_title("Bradley–Terry preference model")
    ax.set_xlabel("reward difference  $r_A - r_B$")
    ax.set_ylabel("P(prefer A)")
    fig.tight_layout()
    save(fig, SUB, "reward-modeling")


def scaling_laws() -> None:
    """Scaling laws: test loss falls as a power law in compute — a straight line on
    log-log axes — bottoming out at an irreducible floor set by the data's entropy.
    Doubling compute gives a predictable, diminishing drop."""
    import matplotlib.pyplot as plt

    flops = np.logspace(18, 24, 100)
    floor = 1.7
    loss = floor + 12.0 * (flops / 1e18) ** -0.095

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(flops, loss, color=C, lw=2.6, label="test loss")
    ax.axhline(floor, color=FG_MUTE, ls="--", lw=1.4, label="irreducible floor")
    ax.set_title("Scaling law: loss vs training compute")
    ax.set_xlabel("training compute (FLOPs)")
    ax.set_ylabel("test loss")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "scaling-laws")


def main() -> None:
    apply_style()
    lora()
    reward_modeling()
    scaling_laws()


if __name__ == "__main__":
    main()
