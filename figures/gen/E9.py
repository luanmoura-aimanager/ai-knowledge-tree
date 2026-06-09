"""Figures for pillar E9 (build a transformer from scratch). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import GOOD, HOT, apply_style, color, save

SUB = "E9"
C = color(SUB)  # pillar-E accent (purple)


def rope_rmsnorm() -> None:
    """Rotary position embeddings rotate each embedding pair by an angle proportional
    to position, with a spectrum of frequencies: low dimensions rotate fast (encoding
    local order) and high dimensions rotate slowly (encoding long-range position)."""
    import matplotlib.pyplot as plt

    pos = np.arange(0, 128)
    d = 64
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for i, col, lab in [(0, C, "dim pair 0 (high freq)"),
                        (8, GOOD, "dim pair 8"),
                        (24, HOT, "dim pair 24 (low freq)")]:
        theta = pos / 10000 ** (2 * i / d)
        ax.plot(pos, np.cos(theta), color=col, lw=2.2, label=lab)
    ax.set_title("RoPE: rotation frequency across dimensions")
    ax.set_xlabel("token position")
    ax.set_ylabel("cosine of rotation angle")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "rope-rmsnorm")


def train_tinyshakespeare() -> None:
    """A representative nanoGPT run on tiny-shakespeare: training and validation loss
    fall together as the model learns, then the validation loss flattens while
    training loss keeps inching down — the onset of mild overfitting. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    steps = np.arange(0, 5000, 25)
    base = 1.5 + 3.0 * np.exp(-steps / 700)
    train = base + 0.03 * rng.normal(size=steps.size)
    val = 1.62 + 3.0 * np.exp(-steps / 700) + 0.05 * (steps / 5000) + \
        0.03 * rng.normal(size=steps.size)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(steps, train, color=C, lw=2.0, label="training loss")
    ax.plot(steps, val, color=HOT, lw=2.0, label="validation loss")
    ax.set_title("nanoGPT on tiny-shakespeare (a typical run)")
    ax.set_xlabel("training step")
    ax.set_ylabel("cross-entropy loss")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "train-tinyshakespeare")


def main() -> None:
    apply_style()
    rope_rmsnorm()
    train_tinyshakespeare()


if __name__ == "__main__":
    main()
