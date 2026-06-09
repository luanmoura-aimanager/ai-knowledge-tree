"""Figures for pillar D2 (convolutional networks). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "D2"
C = color(SUB)  # pillar-D accent (blue)


def convolution() -> None:
    """Left: a 3×3 vertical-edge filter convolved with a white square fires only
    at the vertical edges. Right: stacking convolutions grows the receptive field
    linearly, 1 + L(k−1), so deep stacks see wide context. Lesson's setup."""
    import matplotlib.pyplot as plt

    X = np.zeros((10, 10))
    X[3:7, 3:7] = 1.0
    K = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    H, W = X.shape
    Y = np.zeros((H - 2, W - 2))
    for i in range(H - 2):
        for j in range(W - 2):
            Y[i, j] = np.sum(X[i:i + 3, j:j + 3] * K)

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(9.2, 3.4))
    ax0.imshow(X, cmap="Blues", vmin=0, vmax=1)
    ax0.set_title("input")
    ax1.imshow(Y, cmap="RdBu_r", vmin=-np.abs(Y).max(), vmax=np.abs(Y).max())
    ax1.set_title("after vertical-edge filter")
    for ax in (ax0, ax1):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)

    layers = np.arange(0, 9)
    for k, col in [(3, C), (5, HOT), (7, GOOD)]:
        ax2.plot(layers, 1 + layers * (k - 1), "-o", color=col, ms=3.5,
                 label=f"{k}×{k} kernels")
    ax2.set_title("Receptive field grows with depth")
    ax2.set_xlabel("stacked conv layers $L$")
    ax2.set_ylabel("receptive field (px)")
    ax2.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "convolution")


def cnn_architectures() -> None:
    """Forward signal norm through depth: a plain deep stack attenuates the signal
    toward zero, while a residual stack's skip connections preserve it — why
    ResNets train at depths plain nets cannot. Lesson's setup, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    width = 64
    depth = 40
    h0 = rng.normal(size=(64, width))

    def run(residual):
        h = h0.copy()
        norms = [np.linalg.norm(h) / h.size**0.5]
        for _ in range(depth):
            W1 = rng.normal(scale=0.1, size=(width, width))
            W2 = rng.normal(scale=0.1, size=(width, width))
            f = np.maximum(0, h @ W1) @ W2
            h = np.maximum(0, f + h) if residual else np.maximum(0, f)
            norms.append(np.linalg.norm(h) / h.size**0.5)
        return norms

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(run(False), "-o", color=FG_MUTE, ms=3.5, label="plain deep stack")
    ax.semilogy(run(True), "-o", color=C, ms=3.5, label="residual (skip connections)")
    ax.set_title("Residual connections preserve the signal")
    ax.set_xlabel("layer depth")
    ax.set_ylabel("activation RMS")
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, SUB, "cnn-architectures")


def main() -> None:
    apply_style()
    convolution()
    cnn_architectures()


if __name__ == "__main__":
    main()
