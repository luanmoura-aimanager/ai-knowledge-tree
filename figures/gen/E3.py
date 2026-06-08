"""Figures for pillar E3 (transformer architecture). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, apply_style, color, save

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


def main() -> None:
    apply_style()
    self_attention()


if __name__ == "__main__":
    main()
