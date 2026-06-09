"""Figures for pillar E1 (classical NLP). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "E1"
C = color(SUB)  # pillar-E accent (purple)


def ir_tfidf_bm25() -> None:
    """BM25 saturates term frequency: the first occurrence of a query term matters a
    lot, but each extra occurrence adds diminishing weight — unlike raw term
    frequency, which grows without bound. The k1 knob sets how fast it saturates."""
    import matplotlib.pyplot as plt

    tf = np.linspace(0, 20, 200)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(tf, tf / tf.max() * 4, color=FG_MUTE, ls="--", lw=1.6, label="raw tf (linear)")
    for k1, col in zip([0.5, 1.2, 3.0], [C, GOOD, HOT]):
        ax.plot(tf, tf * (k1 + 1) / (tf + k1), color=col, lw=2.4, label=f"BM25, $k_1$ = {k1}")
    ax.set_title("BM25 term-frequency saturation")
    ax.set_xlabel("term frequency in document")
    ax.set_ylabel("term weight contribution")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "ir-tfidf-bm25")


def ngram_lm() -> None:
    """Word frequencies follow Zipf's law — frequency is roughly inversely
    proportional to rank, a near-straight line on log-log axes. The long tail of
    rare words is why higher-order n-grams hit unseen contexts and need smoothing."""
    import matplotlib.pyplot as plt

    rank = np.arange(1, 10001)
    freq = 1.0 / rank**1.07          # Zipf with exponent ~1
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(rank, freq / freq[0], color=C, lw=2.4)
    ax.axvspan(1000, 10000, color=FG_MUTE, alpha=0.12)
    ax.text(1800, 0.3, "long tail of\nrare words", color=FG_MUTE, fontsize=9)
    ax.set_title("Zipf's law: word frequency vs rank")
    ax.set_xlabel("word rank")
    ax.set_ylabel("relative frequency")
    fig.tight_layout()
    save(fig, SUB, "ngram-lm")


def smoothing() -> None:
    """Maximum-likelihood n-gram estimates assign probability 0 to every unseen
    event — fatal for a language model. Smoothing shaves mass off the seen events
    and redistributes it to the unseen ones, so nothing has zero probability."""
    import matplotlib.pyplot as plt

    counts = np.array([8, 5, 3, 2, 0, 0, 0, 0], dtype=float)
    labels = [f"w{i}" for i in range(len(counts))]
    mle = counts / counts.sum()
    k = 1.0
    smoothed = (counts + k) / (counts.sum() + k * len(counts))

    x = np.arange(len(counts))
    w = 0.4
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.bar(x - w / 2, mle, w, color=FG_MUTE, label="MLE (zeros for unseen)")
    ax.bar(x + w / 2, smoothed, w, color=C, label="add-1 smoothed")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_title("Add-k smoothing redistributes probability mass")
    ax.set_xlabel("n-gram (last 4 are unseen)")
    ax.set_ylabel("probability")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "smoothing")


def main() -> None:
    apply_style()
    ir_tfidf_bm25()
    ngram_lm()
    smoothing()


if __name__ == "__main__":
    main()
