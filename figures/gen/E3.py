"""Figures for pillar E3 (transformer architecture). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "E3"
C = color(SUB)  # pillar-E accent


def _softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def self_attention() -> None:
    """Scaled dot-product attention: the attention matrix + why 1/√d_k matters.

    Left: a token×token softmax(QKᵀ/√d_k) heatmap for a short sequence.
    Right: one query's attention distribution, scaled vs unscaled — without the
    1/√d_k factor the logits grow with d_k and the softmax collapses to a spike.
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    rng = np.random.default_rng(0)
    tokens = ["The", "cat", "sat", "on", "the", "mat"]
    n, d_k = len(tokens), 64
    Q = rng.standard_normal((n, d_k))
    K = rng.standard_normal((n, d_k))
    # Nudge a couple of tokens to attend to "cat"/"mat" so the pattern reads.
    K[1] += 0.6 * Q[2]   # "sat" -> "cat"
    K[5] += 0.6 * Q[3]   # "mat" -> "on"

    logits = Q @ K.T
    attn = _softmax(logits / np.sqrt(d_k))

    # Dark-native sequential colormap from background -> pillar accent.
    cmap = LinearSegmentedColormap.from_list("pe", ["#141a35", C])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.8))

    # --- Left: attention heatmap -------------------------------------------
    im = ax1.imshow(attn, cmap=cmap, vmin=0, vmax=attn.max())
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    ax1.set_xticklabels(tokens, rotation=45, ha="right", color=FG_DIM)
    ax1.set_yticklabels(tokens, color=FG_DIM)
    ax1.set_xlabel("key (attended to)")
    ax1.set_ylabel("query (attending)")
    ax1.set_title("softmax($QK^\\top/\\sqrt{d_k}$)")
    ax1.grid(False)
    cb = fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor("#242b52")

    # --- Right: why scaling matters. One query vs many random keys at large
    # d_k. Unscaled logits have std ~ √d_k, so softmax saturates onto a single
    # key; the 1/√d_k factor restores unit-scale logits and a soft spread.
    m = 12
    q = rng.standard_normal(d_k)
    Kr = rng.standard_normal((m, d_k))
    lr = Kr @ q
    scaled = _softmax(lr / np.sqrt(d_k))
    unscaled = _softmax(lr)
    xs = np.arange(m)
    w = 0.4
    ax2.bar(xs - w / 2, unscaled, w, color="#f7768e",
            label=f"unscaled (peaks, std≈{lr.std():.0f})")
    ax2.bar(xs + w / 2, scaled, w, color=C, label="scaled by 1/√d_k (soft)")
    ax2.set_xlabel(f"key index (one query, {m} random keys, $d_k$={d_k})")
    ax2.set_ylabel("attention weight")
    ax2.set_title("Scaling prevents softmax saturation")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    save(fig, SUB, "self-attention")


def multi_head_attention() -> None:
    """Multiple heads let one layer attend several ways at once: here three heads on
    the same sequence specialize — a previous-token head, a first-token head, and a
    local-window head — and their outputs are concatenated."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    n = 8
    prev = np.eye(n, k=-1) + 0.15
    first = np.zeros((n, n)); first[:, 0] = 1.0; first += 0.05
    local = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            local[i, j] = np.exp(-((i - j) ** 2) / 2.0)
    cmap = LinearSegmentedColormap.from_list("pe", ["#141a35", C])

    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.4))
    for ax, M, ttl in [(axes[0], prev, "head 1: previous token"),
                       (axes[1], first, "head 2: first token"),
                       (axes[2], local, "head 3: local window")]:
        M = M / M.sum(axis=1, keepdims=True)
        ax.imshow(M, cmap=cmap, vmin=0, vmax=1)
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel("key"); ax.grid(False)
        ax.set_xticks([]); ax.set_yticks([])
    axes[0].set_ylabel("query")
    fig.suptitle("Different heads learn different attention patterns", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "multi-head-attention")


def positional_encodings() -> None:
    """Sinusoidal positional encodings give each position a unique fingerprint:
    every dimension is a sine/cosine of a different frequency, so position is encoded
    smoothly and relative offsets become linear shifts. Rows = positions, columns =
    dimensions."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    pos, d = 60, 64
    p = np.arange(pos)[:, None]
    i = np.arange(d)[None, :]
    angle = p / np.power(10000, (2 * (i // 2)) / d)
    pe = np.where(i % 2 == 0, np.sin(angle), np.cos(angle))
    cmap = LinearSegmentedColormap.from_list("pe2", [HOT, "#141a35", C])

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    im = ax.imshow(pe, cmap=cmap, aspect="auto", vmin=-1, vmax=1)
    ax.set_title("Sinusoidal positional encoding")
    ax.set_xlabel("embedding dimension")
    ax.set_ylabel("position in sequence")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    fig.tight_layout()
    save(fig, SUB, "positional-encodings")


def swiglu_geglu() -> None:
    """Modern transformers swap ReLU for smooth gated activations. The building
    blocks — GELU and Swish (SiLU) — are smooth, non-monotonic curves that pass a
    little negative signal, which SwiGLU and GeGLU use as multiplicative gates."""
    import matplotlib.pyplot as plt
    from scipy.special import erf

    x = np.linspace(-5, 5, 400)
    relu = np.maximum(0, x)
    gelu = 0.5 * x * (1 + erf(x / np.sqrt(2)))
    swish = x / (1 + np.exp(-x))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(x, relu, color=FG_MUTE, ls="--", lw=1.8, label="ReLU")
    ax.plot(x, gelu, color=C, lw=2.4, label="GELU (used by GeGLU)")
    ax.plot(x, swish, color=HOT, lw=2.4, label="Swish/SiLU (used by SwiGLU)")
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title("Smooth gated activations")
    ax.set_xlabel("input")
    ax.set_ylabel("output")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "swiglu-geglu")


def main() -> None:
    apply_style()
    self_attention()
    multi_head_attention()
    positional_encodings()
    swiglu_geglu()


if __name__ == "__main__":
    main()
