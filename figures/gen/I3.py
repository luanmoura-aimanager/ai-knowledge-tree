"""Figures for pillar I3 (model optimization & serving). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "I3"
C = color(SUB)  # pillar-I accent (green)


def distillation_pruning() -> None:
    """Pruning removes weights to shrink and speed up a model: accuracy holds nearly
    flat while the easy weights go, then falls off a cliff once too much capacity is
    removed. The sweet spot is the knee just before the drop. rng(0)."""
    import matplotlib.pyplot as plt

    sparsity = np.linspace(0, 0.95, 100)
    # nearly flat until the knee, then a sharp drop in accuracy
    acc = 0.918 - 0.004 * sparsity - 1.3 * np.clip(sparsity - 0.8, 0, None) ** 1.6

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(sparsity * 100, acc * 100, color=C, lw=2.6)
    knee = 80
    ax.axvline(knee, color=HOT, ls="--", lw=1.6, label="knee: best size/accuracy")
    ax.fill_between(sparsity * 100, acc * 100, 84, where=sparsity < 0.8, color=C, alpha=0.1)
    ax.set_title("Pruning: accuracy vs sparsity")
    ax.set_xlabel("weights pruned (%)"); ax.set_ylabel("accuracy (%)")
    ax.set_ylim(84, 93)
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "distillation-pruning")


def latency_throughput() -> None:
    """Batching trades latency for throughput: larger batches keep the accelerator
    busier, so throughput (tokens/s) climbs toward saturation, but each request waits
    longer. Serving systems pick a batch size that meets the latency budget while
    maximizing throughput."""
    import matplotlib.pyplot as plt

    batch = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    throughput = 2000 * batch / (batch + 6)
    latency = 12 + 0.9 * batch

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(latency, throughput, "-o", color=C, ms=5)
    for b, x, y in zip(batch, latency, throughput):
        ax.annotate(f"b={b}", (x, y), fontsize=7, color=FG_MUTE,
                    xytext=(4, -8), textcoords="offset points")
    ax.axvline(60, color=HOT, ls="--", lw=1.6, label="latency budget (60 ms)")
    ax.set_title("Latency–throughput trade-off (batching)")
    ax.set_xlabel("per-request latency (ms)"); ax.set_ylabel("throughput (req/s)")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "latency-throughput")


def quantization() -> None:
    """Quantizing weights to fewer bits shrinks the model and speeds inference with
    little accuracy loss down to int8; below that, accuracy starts to degrade unless
    more careful schemes are used. Memory falls in direct proportion to the bit
    width."""
    import matplotlib.pyplot as plt

    bits = np.array([32, 16, 8, 4, 2])
    acc = np.array([92.0, 91.9, 91.5, 89.0, 78.0])
    size = bits / 32

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(bits, acc, "-o", color=C, ms=6, label="accuracy (%)")
    ax.set_xlabel("weight precision (bits)"); ax.set_ylabel("accuracy (%)", color=C)
    ax.invert_xaxis()
    ax2 = ax.twinx()
    ax2.plot(bits, size * 100, "-s", color=ACCENT, ms=5, label="relative size (%)")
    ax2.set_ylabel("model size (% of fp32)", color=ACCENT)
    ax.axvspan(7, 9, color=HOT, alpha=0.12)
    ax.set_title("Quantization: accuracy vs precision")
    fig.tight_layout()
    save(fig, SUB, "quantization")


def deployment_strategies() -> None:
    """Three rollout patterns as fraction of USER traffic served by the new model over
    time. Shadow keeps users at 0% (it only mirrors traffic, zero user risk); canary
    ramps a small live fraction up in steps while watching a metric; blue-green flips
    all traffic at once for an atomic cutover."""
    import matplotlib.pyplot as plt

    t = np.arange(0, 60)
    shadow = np.zeros_like(t, dtype=float)                 # users never see the new model
    canary = np.piecewise(
        t.astype(float),
        [t < 10, (t >= 10) & (t < 25), (t >= 25) & (t < 40), t >= 40],
        [0.0, 5.0, 25.0, 100.0],
    )
    blue_green = np.where(t < 35, 0.0, 100.0)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t, canary, color=C, lw=2.4, label="canary (stepped ramp)")
    ax.plot(t, blue_green, color=ACCENT, lw=2.0, ls="-.", label="blue-green (atomic flip)")
    ax.plot(t, shadow, color=FG_MUTE, lw=2.0, ls="--", label="shadow (0% user traffic)")
    ax.fill_between(t, shadow, 4, color=FG_MUTE, alpha=0.12)
    ax.text(2, 8, "shadow mirrors\ntraffic, users at 0%", color=FG_MUTE, fontsize=8)
    ax.set_title("Deployment strategies: traffic to the new model")
    ax.set_xlabel("time"); ax.set_ylabel("% of user traffic on new model")
    ax.set_ylim(-5, 110)
    ax.legend(loc="center left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "deployment-strategies")


def main() -> None:
    apply_style()
    deployment_strategies()
    distillation_pruning()
    latency_throughput()
    quantization()


if __name__ == "__main__":
    main()
