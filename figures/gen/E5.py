"""Figures for pillar E5 (LLM inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "E5"
C = color(SUB)  # pillar-E accent (purple)


def _softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def decoding() -> None:
    """Temperature reshapes the next-token distribution before sampling: T < 1
    sharpens it toward the top tokens (more deterministic), T > 1 flattens it (more
    diverse and more random). The same logits, three temperatures."""
    import matplotlib.pyplot as plt

    logits = np.array([3.0, 2.4, 2.0, 1.2, 0.8, 0.3, -0.2, -0.6])
    x = np.arange(len(logits))
    w = 0.27
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for off, T, col, lab in [(-w, 0.5, C, "T = 0.5 (sharp)"),
                            (0.0, 1.0, GOOD, "T = 1.0"),
                            (w, 2.0, HOT, "T = 2.0 (flat)")]:
        ax.bar(x + off, _softmax(logits / T), w, color=col, label=lab)
    ax.set_title("Temperature reshapes the sampling distribution")
    ax.set_xlabel("candidate token (ranked by logit)")
    ax.set_ylabel("probability")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "decoding")


def kv_cache() -> None:
    """The KV cache stores one key and value vector per layer for every token
    generated so far, so its memory grows linearly with sequence length — at long
    context it dominates and caps the batch size. Shown for a 32-layer, 4096-dim
    model with full multi-head attention (grouped-query attention shrinks it)."""
    import matplotlib.pyplot as plt

    seq = np.linspace(0, 128_000, 200)
    layers, d, bytes_ = 32, 4096, 2          # fp16
    mem = 2 * layers * d * bytes_ * seq / 1e9   # GB per sequence

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(seq / 1000, mem, color=C, lw=2.6)
    ax.fill_between(seq / 1000, mem, color=C, alpha=0.15)
    ax.set_title("KV-cache memory grows linearly with context")
    ax.set_xlabel("sequence length (thousands of tokens)")
    ax.set_ylabel("KV-cache memory (GB)")
    fig.tight_layout()
    save(fig, SUB, "kv-cache")


def quantization() -> None:
    """Quantization stores weights in fewer bits, shrinking model memory in direct
    proportion: fp16→int4 is a 4× reduction, turning a 14 GB model into 3.5 GB with
    only a modest quality cost. Shown for 7B parameters."""
    import matplotlib.pyplot as plt

    params = 7e9
    precisions = ["fp32", "fp16", "int8", "int4"]
    bits = np.array([32, 16, 8, 4])
    mem = params * bits / 8 / 1e9

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    bars = ax.bar(precisions, mem, color=[FG_MUTE, C, GOOD, HOT], width=0.6)
    for b, m in zip(bars, mem):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.4, f"{m:.0f} GB",
                ha="center", color="#e6e9f5", fontsize=9)
    ax.set_title("Quantization shrinks model memory (7B params)")
    ax.set_ylabel("weight memory (GB)")
    ax.set_ylim(0, 32)
    fig.tight_layout()
    save(fig, SUB, "quantization")


def main() -> None:
    apply_style()
    decoding()
    kv_cache()
    quantization()


if __name__ == "__main__":
    main()
