"""Figures for pillar E3 (transformer architecture). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

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


def rope_scaling() -> None:
    """Per-pair frequency multiplier theta'_i / theta_i for extending a d=128, base-10,000
    RoPE model from 4,096 to 32,768 tokens (s = 8): position interpolation scales every
    pair by 1/s, the NTK-aware base change keeps the fastest pair and interpolates the
    slowest, and YaRN's ramp (alpha=1, beta=32) keeps fast pairs exactly."""
    import matplotlib.pyplot as plt
    from _style import PARTIAL

    d, b, L, s = 128, 1e4, 4096, 8.0
    i = np.arange(d // 2)
    theta = b ** (-2 * i / d)
    ntk = (b * s ** (d / (d - 2))) ** (-2 * i / d) / theta
    r = L / (2 * np.pi / theta)
    g = np.clip((r - 1) / (32 - 1), 0, 1)
    yarn = (1 - g) / s + g
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.plot(i, np.full_like(theta, 1 / s), color=HOT, lw=2, label="PI: every pair x 1/s")
    ax.plot(i, ntk, color=PARTIAL, lw=2, label="NTK-aware base change")
    ax.plot(i, yarn, color=GOOD, lw=2, label="YaRN (NTK-by-parts ramp)")
    ax.set_yscale("log")
    ax.set_xlabel("frequency pair i (0 = fastest)")
    ax.set_ylabel(r"$\theta'_i / \theta_i$")
    ax.set_title("How each method rescales RoPE frequencies (s = 8)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "rope-scaling")

def attention_stability() -> None:
    """Entropy of softmax attention over 512 keys as the logit scale grows: unbounded
    query/key norms drive attention toward one-hot (entropy -> 0), the collapse QK-norm
    prevents by fixing the norms."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    z = rng.normal(size=(200, 512))
    scales = np.logspace(-1, 2, 60)
    H = []
    for c in scales:
        p = _softmax(c * z, axis=1)
        H.append(-(p * np.log(p + 1e-300)).sum(1).mean())
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(scales, H, color=C, lw=2)
    ax.axhline(np.log(512), color=FG_MUTE, ls=":", lw=1)
    ax.text(0.12, np.log(512) - 0.45, "uniform: ln 512 = 6.24 nats", color=FG_DIM, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("logit scale (grows with |q| |k|)")
    ax.set_ylabel("attention entropy (nats)")
    ax.set_title("Unbounded logits collapse attention to one key")
    fig.tight_layout()
    save(fig, SUB, "attention-entropy")

def modern_moe() -> None:
    """Expert load (share of top-2 assignments) for 16 experts with skewed affinities,
    before and after 1,000 steps of loss-free bias balancing (u = 0.001). Same
    simulation as the lesson's code."""
    import matplotlib.pyplot as plt

    loads0, loads1 = _moe_balance()
    E = len(loads0)
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    x = np.arange(E)
    ax.bar(x - 0.2, loads0, width=0.4, color=HOT, label="no balancing")
    ax.bar(x + 0.2, loads1, width=0.4, color=GOOD, label="with routing bias")
    ax.axhline(1 / E, color=FG_MUTE, ls=":", lw=1)
    ax.set_xlabel("expert")
    ax.set_ylabel("share of routed slots")
    ax.set_title("Loss-free balancing evens out expert load")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "moe-balance")


def _moe_balance():
    rng = np.random.default_rng(0)
    E, K, T, dim = 16, 2, 1024, 8
    W = rng.normal(scale=0.5, size=(dim, E))
    skew = np.linspace(-1.5, 1.5, E)
    def batch_scores():
        x = rng.normal(size=(T, dim))
        return 1 / (1 + np.exp(-(x @ W + skew)))
    def loads(s, bias):
        top = np.argsort(-(s + bias), axis=1)[:, :K]
        return np.bincount(top.ravel(), minlength=E) / (T * K)
    s = batch_scores()
    loads0 = loads(s, np.zeros(E))
    bias = np.zeros(E)
    for _ in range(1000):
        c = loads(batch_scores(), bias)
        bias += 0.001 * np.sign(c.mean() - c)
    loads1 = loads(batch_scores(), bias)
    return loads0, loads1

def sparse_attention() -> None:
    """Share of softmax attention mass captured by the top-k of 8,192 keys, for a peaked
    score distribution (std 3) and a flat one (std 0.5): sparse attention is nearly
    lossless only when attention is concentrated."""
    import matplotlib.pyplot as plt
    from _style import PARTIAL

    rng = np.random.default_rng(0)
    L = 8192
    ks = np.unique(np.logspace(0, np.log10(L), 50).astype(int))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for sd, col, lab in ((3.0, GOOD, "peaked scores (std 3)"), (0.5, PARTIAL, "flat scores (std 0.5)")):
        p = np.sort(_softmax(rng.normal(scale=sd, size=L)))[::-1]
        ax.plot(ks, np.cumsum(p)[ks - 1], color=col, lw=2, label=lab)
    ax.axvline(2048, color=FG_MUTE, ls=":", lw=1)
    ax.text(2150, 0.08, "k = 2048 (DSA)", color=FG_DIM, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("keys kept per query (k)")
    ax.set_ylabel("attention mass captured")
    ax.set_title("Top-k sparse attention over 8,192 keys")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, SUB, "sparse-topk-mass")


def main() -> None:
    apply_style()
    self_attention()
    multi_head_attention()
    positional_encodings()
    swiglu_geglu()

    rope_scaling()
    attention_stability()
    modern_moe()
    sparse_attention()

if __name__ == "__main__":
    main()
