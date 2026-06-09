"""Figures for pillar D3 (sequence models & attention). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "D3"
C = color(SUB)  # pillar-D accent (blue)


def _softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def rnn() -> None:
    """The product of per-step Jacobians sets whether gradients survive through
    time: a recurrent matrix with spectral radius < 1 makes them vanish, > 1 makes
    them explode, ≈ 1 keeps them stable. Lesson's tanh RNN, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    T, d_h, d_in = 40, 16, 5
    X = rng.normal(size=(T, d_in))
    Wx = rng.normal(scale=0.05, size=(d_h, d_in))  # mild input → stays near-linear
    W0 = rng.normal(size=(d_h, d_h))
    sr0 = np.abs(np.linalg.eigvals(W0)).max()

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for rho, col, lab in [(0.5, ACCENT, "ρ = 0.5 (vanish)"),
                          (1.0, FG_MUTE, "ρ = 1.0 (marginal)"),
                          (1.5, HOT, "ρ = 1.5 (explode)")]:
        Wh = W0 * (rho / sr0)
        h = np.zeros(d_h)
        J = np.eye(d_h)
        norms = []
        for t in range(T):
            h = np.tanh(Wx @ X[t] + Wh @ h)
            J = (np.diag(1 - h**2) @ Wh) @ J
            norms.append(np.linalg.norm(J, 2))
        ax.semilogy(range(1, T + 1), norms, color=col, lw=2.2, label=lab)
    ax.set_title("Gradient norm through time")
    ax.set_xlabel("time steps backpropagated")
    ax.set_ylabel(r"$\|\prod_t J_t\|$")
    ax.legend(loc="center right")
    fig.tight_layout()
    save(fig, SUB, "rnn")


def lstm_gru() -> None:
    """LSTM gate activations over a sequence: with the forget-gate bias set to +1
    the forget gate sits high (it keeps memory by default), while input/output
    gates modulate around 0.5. Lesson's setup, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    T, d_x, d_h = 40, 5, 16
    X = rng.normal(size=(T, d_x))
    sig = lambda z: 1 / (1 + np.exp(-z))

    def init():
        return rng.normal(scale=0.1, size=(d_h, d_x + d_h))

    Wf, Wi, Wo, Wc = init(), init(), init(), init()
    bf = np.ones(d_h)  # forget bias = 1
    h, c = np.zeros(d_h), np.zeros(d_h)
    fh, ih, oh = [], [], []
    for t in range(T):
        z = np.concatenate([X[t], h])
        f = sig(Wf @ z + bf)
        i = sig(Wi @ z)
        o = sig(Wo @ z)
        c = f * c + i * np.tanh(Wc @ z)
        h = o * np.tanh(c)
        fh.append(f.mean()); ih.append(i.mean()); oh.append(o.mean())

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(fh, "-o", color=C, ms=3, label="forget gate (bias +1)")
    ax.plot(ih, "-o", color=HOT, ms=3, label="input gate")
    ax.plot(oh, "-o", color=GOOD, ms=3, label="output gate")
    ax.axhline(0.5, color=FG_MUTE, ls=":", lw=1.0)
    ax.set_ylim(0, 1)
    ax.set_title("LSTM gate activations over a sequence")
    ax.set_xlabel("time step")
    ax.set_ylabel("mean gate value")
    ax.legend(loc="center right")
    fig.tight_layout()
    save(fig, SUB, "lstm-gru")


def self_attention() -> None:
    """Self-attention as a soft, content-based lookup. Left: the full attention
    matrix (every token attends to every token). Right: a causal mask zeros out
    the future, leaving a lower-triangular pattern for autoregressive models.
    Lesson's N=6, d=8, rng(0)."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    rng = np.random.default_rng(0)
    toks = ["the", "cat", "that", "sat", "was", "happy"]
    N, d = len(toks), 8
    X = rng.normal(size=(N, d))
    Wq = rng.normal(scale=0.4, size=(d, d))
    Wk = rng.normal(scale=0.4, size=(d, d))
    S = (X @ Wq) @ (X @ Wk).T / np.sqrt(d)
    A_full = _softmax(S)
    mask = np.tril(np.ones((N, N), dtype=bool))
    A_causal = _softmax(np.where(mask, S, -np.inf))

    cmap = LinearSegmentedColormap.from_list("pd", ["#141a35", C])
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.0))
    for ax, A, ttl in [(axes[0], A_full, "Full attention"),
                       (axes[1], A_causal, "Causal-masked attention")]:
        im = ax.imshow(A, cmap=cmap, vmin=0, vmax=1)
        ax.set_xticks(range(N)); ax.set_yticks(range(N))
        ax.set_xticklabels(toks, rotation=45, ha="right", color=FG_DIM, fontsize=9)
        ax.set_yticklabels(toks, color=FG_DIM, fontsize=9)
        ax.set_title(ttl)
        ax.set_xlabel("key (attended to)")
        ax.grid(False)
    axes[0].set_ylabel("query (attending)")
    cb = fig.colorbar(im, ax=axes, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    save(fig, SUB, "self-attention")


def positional_encoding() -> None:
    """Sinusoidal positional encodings. Left: the position×dimension heatmap —
    each dimension is a sinusoid, with wavelength increasing across dimensions.
    Right: a few dimensions plotted as waves of geometrically growing period."""
    import matplotlib.pyplot as plt

    N, d = 80, 64
    pos = np.arange(N)[:, None]
    div = np.exp(np.arange(0, d, 2) * -(np.log(10000.0) / d))
    PE = np.zeros((N, d))
    PE[:, 0::2] = np.sin(pos * div)
    PE[:, 1::2] = np.cos(pos * div)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    im = ax1.imshow(PE.T, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1)
    ax1.set_title("Positional encoding (dim × position)")
    ax1.set_xlabel("position")
    ax1.set_ylabel("embedding dimension")
    ax1.grid(False)
    cb = fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)

    for dim, col in zip([0, 4, 12], [C, HOT, GOOD]):
        ax2.plot(PE[:, dim], color=col, lw=2.0, label=f"dim {dim}")
    ax2.set_title("Each dimension is a wave")
    ax2.set_xlabel("position")
    ax2.set_ylabel("value")
    ax2.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "positional-encoding")


def linear_attention() -> None:
    """Softmax attention builds an n×n score matrix, so its cost grows
    quadratically with sequence length; linear-attention variants factor the
    softmax to grow linearly, winning decisively for long sequences."""
    import matplotlib.pyplot as plt

    n = np.logspace(1, 4.5, 100)
    d = 64
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(n, n**2 * d, color=HOT, lw=2.4, label="softmax attention  $O(n^2 d)$")
    ax.loglog(n, n * d**2, color=C, lw=2.4, label="linear attention  $O(n d^2)$")
    ax.axvline(d, color=FG_MUTE, ls=":", lw=1.4, label=f"crossover n ≈ d = {d}")
    ax.set_title("Attention cost vs sequence length")
    ax.set_xlabel("sequence length $n$")
    ax.set_ylabel("operations")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "linear-attention")


def state_space_models() -> None:
    """A state-space model's output is a convolution with a kernel built from
    decaying modes Aᵏ: eigenvalues near 1 decay slowly and carry long-range memory,
    while small eigenvalues forget quickly."""
    import matplotlib.pyplot as plt

    k = np.arange(0, 100)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for lam, col, lab in [(0.99, C, "λ = 0.99 (long memory)"),
                          (0.95, GOOD, "λ = 0.95"),
                          (0.80, HOT, "λ = 0.80 (forgets fast)")]:
        ax.plot(k, lam**k, color=col, lw=2.4, label=lab)
    ax.set_title("SSM convolution kernel: decaying modes")
    ax.set_xlabel("time lag $k$")
    ax.set_ylabel("kernel weight $\\lambda^k$")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "state-space-models")


def word_embeddings() -> None:
    """Skip-gram with negative sampling learns vectors whose geometry reflects
    co-occurrence: words sharing contexts land near each other, so a 2D PCA of the
    learned embeddings reveals the corpus's topical clusters. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    rng = np.random.default_rng(0)
    groups = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
    sentences = []
    for _ in range(120):
        g = groups[rng.integers(3)]
        sentences.append(list(rng.choice(g, size=3, replace=False)))
    V, d, window, k_neg, lr = 12, 16, 2, 5, 0.05
    U = rng.normal(scale=0.1, size=(V, d))
    W = rng.normal(scale=0.1, size=(V, d))
    sig = lambda z: 1 / (1 + np.exp(-z))
    for _ in range(60):
        for s in sentences:
            for i, c in enumerate(s):
                for j in range(max(0, i - window), min(len(s), i + window + 1)):
                    if j == i:
                        continue
                    o = s[j]
                    g = (sig(U[c] @ W[o]) - 1) * W[o]
                    W[o] -= lr * (sig(U[c] @ W[o]) - 1) * U[c]
                    for ng in rng.integers(0, V, k_neg):
                        g = g + sig(U[c] @ W[ng]) * W[ng]
                        W[ng] -= lr * sig(U[c] @ W[ng]) * U[c]
                    U[c] -= lr * g

    emb = PCA(n_components=2).fit_transform(U)
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    cols = [C, GOOD, HOT]
    for gi, grp in enumerate(groups):
        ax.scatter(emb[grp, 0], emb[grp, 1], s=90, color=cols[gi], edgecolor="none",
                   label=f"topic {gi + 1}")
        for w in grp:
            ax.annotate(f"w{w}", (emb[w, 0], emb[w, 1]), fontsize=8, color=FG_DIM,
                        xytext=(4, 4), textcoords="offset points")
    ax.set_title("Word embeddings cluster by co-occurrence (PCA)")
    ax.set_xlabel("PC 1"); ax.set_ylabel("PC 2")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "word-embeddings")


def main() -> None:
    apply_style()
    rnn()
    lstm_gru()
    self_attention()
    positional_encoding()
    linear_attention()
    state_space_models()
    word_embeddings()


if __name__ == "__main__":
    main()
