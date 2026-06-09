"""Figures for pillar J6 (FinOps). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "J6"
C = color(SUB)  # pillar-J accent


def finops_for_ai() -> None:
    """FinOps drives down the unit cost of AI: successive levers — prompt caching,
    request batching, a smaller distilled model, and quantized serving — each step
    the cost-per-request down, so total spend can fall even as traffic grows."""
    import matplotlib.pyplot as plt

    days = np.arange(120)
    cpr = np.full(120, 2.0)                       # cents per request
    levers = [(20, 0.7, "prompt caching"), (50, 0.65, "batching"),
              (80, 0.55, "distilled model"), (100, 0.7, "quantization")]
    for d, factor, _ in levers:
        cpr[d:] *= factor

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(days, cpr, color=C, lw=2.4)
    ax.fill_between(days, cpr, color=C, alpha=0.12)
    for d, _, name in levers:
        ax.axvline(d, color=FG_MUTE, ls=":", lw=1.0)
        ax.annotate(name, (d, cpr[d - 1]), fontsize=8, color=ACCENT,
                    xytext=(2, 8), textcoords="offset points", rotation=0)
    ax.set_title("FinOps: cost per request falls with each lever")
    ax.set_xlabel("day"); ax.set_ylabel("cost per request (cents)")
    ax.set_ylim(0, 2.2)
    fig.tight_layout()
    save(fig, SUB, "finops-for-ai")


def main() -> None:
    apply_style()
    finops_for_ai()


if __name__ == "__main__":
    main()
