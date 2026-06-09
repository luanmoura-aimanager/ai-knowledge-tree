"""Figures for pillar J4 (fine-tuning). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, GOOD, HOT, apply_style, color, save

SUB = "J4"
C = color(SUB)  # pillar-J accent


def lora_qlora() -> None:
    """Full fine-tuning must store gradients and Adam optimizer states for every
    weight, dwarfing the model itself; LoRA trains only small adapters (so gradients
    and optimizer states nearly vanish) and QLoRA additionally 4-bit-quantizes the
    frozen base — together turning a multi-GPU job into a single-GPU one. (7B model.)"""
    import matplotlib.pyplot as plt

    methods = ["full FT", "LoRA", "QLoRA"]
    base = np.array([14, 14, 3.5])      # frozen base weights (fp16 / 4-bit)
    grads = np.array([14, 0.2, 0.2])    # gradients
    optim = np.array([56, 0.6, 0.6])    # Adam states (fp32 m, v)
    act = np.array([8, 8, 6])           # activations

    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    bottom = np.zeros(3)
    for vals, col, lab in [(base, C, "base weights"), (grads, ACCENT, "gradients"),
                          (optim, HOT, "optimizer states"), (act, GOOD, "activations")]:
        ax.bar(x, vals, 0.55, bottom=bottom, color=col, label=lab)
        bottom += vals
    for i, tot in enumerate(bottom):
        ax.text(i, tot + 2, f"{tot:.0f} GB", ha="center", color="#e6e9f5", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(methods)
    ax.set_title("GPU memory: full FT vs LoRA vs QLoRA (7B)")
    ax.set_ylabel("memory (GB)")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "lora-qlora")


def main() -> None:
    apply_style()
    lora_qlora()


if __name__ == "__main__":
    main()
