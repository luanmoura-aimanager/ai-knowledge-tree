"""Figures for pillar K2 (storage & file formats). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GRID, apply_style, color, save

SUB = "K2"
C = color(SUB)  # pillar-K accent


def row_vs_columnar() -> None:
    """An analytical query reads few columns over many rows. A row layout must scan
    every byte of every row to reach the wanted columns; a columnar layout reads only
    the selected columns. The bars contrast the bytes scanned for a 2-of-8-column query."""
    import matplotlib.pyplot as plt

    n_rows = 1_000_000
    # Byte width of each of the 8 columns (mixed types).
    widths = np.array([8, 8, 4, 4, 2, 1, 16, 8])      # total 51 bytes/row
    selected = np.array([0, 6])                        # query reads cols 0 and 6
    row_bytes = n_rows * widths.sum()
    col_bytes = n_rows * widths[selected].sum()

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    labels = ["row layout\n(reads all 8 cols)", "columnar\n(reads 2 cols)"]
    vals = np.array([row_bytes, col_bytes]) / 1e6      # MB
    bars = ax.bar(labels, vals, color=[FG_MUTE, C], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,.0f} MB",
                ha="center", va="bottom", color="#e6e9f5", fontsize=10)
    ax.set_ylabel("bytes scanned (MB)")
    ax.set_title("Bytes scanned by a 2-of-8-column query")
    ax.set_ylim(0, vals[0] * 1.18)
    fig.tight_layout()
    save(fig, SUB, "row-vs-columnar")


def compression_encoding() -> None:
    """Each lightweight encoding wins on the column shape it was built for:
    dictionary on low cardinality, run-length on runs, delta on monotonic values.
    The bars show the compression ratio (raw/encoded) of each on a fitting column."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 100_000

    # Dictionary: low-cardinality strings -> small integer codes.
    cats = np.array(["US", "BR", "DE", "JP"])
    dict_col = cats[rng.integers(0, 4, n)]
    raw_dict = n * 2                                   # 2 bytes/char, 2-char codes
    enc_dict = n * 1 + cats.size * 2                   # 1-byte code/row + table
    r_dict = raw_dict / enc_dict

    # Run-length: a sorted/repetitive column collapses to (value, count) runs.
    rle_col = np.repeat(np.arange(200), n // 200)
    runs = 1 + np.count_nonzero(np.diff(rle_col))
    raw_rle = rle_col.size * 4
    enc_rle = runs * 8                                 # 4-byte value + 4-byte count
    r_rle = raw_rle / enc_rle

    # Delta: monotonic timestamps -> small gaps stored in 1 byte each.
    delta_col = np.cumsum(rng.integers(1, 60, n)).astype(np.int64)
    raw_delta = delta_col.size * 8
    enc_delta = 8 + (delta_col.size - 1) * 1           # one base + 1-byte deltas
    r_delta = raw_delta / enc_delta

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    labels = ["dictionary\n(low card.)", "run-length\n(runs)", "delta\n(monotonic)"]
    vals = [r_dict, r_rle, r_delta]
    bars = ax.bar(labels, vals, color=[C, ACCENT, FG_MUTE], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.0f}x",
                ha="center", va="bottom", color="#e6e9f5", fontsize=10)
    ax.axhline(1.0, color=HOT, ls="--", lw=1.4, label="no compression (1x)")
    ax.set_ylabel("compression ratio (raw / encoded)")
    ax.set_title("Compression ratio by encoding, on a fitting column")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "compression-encoding")


def partitioning_pruning() -> None:
    """Total query cost as a function of partition count. More partitions means a
    selective predicate scans fewer of them (data cost falls), but each file carries
    a fixed open/metadata overhead (overhead cost rises). The sum is U-shaped with a
    sweet spot; pushed too far, tiny-file overhead dominates."""
    import matplotlib.pyplot as plt

    total_rows = 6_000_000
    bytes_per_row = 64
    selectivity = 0.05                                 # query touches 5% of the key range
    overhead_per_file = 3_000_000.0                    # fixed bytes-equiv per file opened

    P = np.arange(1, 4001)
    # A selective query reads ceil(selectivity * P) partitions (at least one).
    touched = np.maximum(1, np.ceil(selectivity * P))
    data_cost = (total_rows / P) * touched * bytes_per_row
    overhead_cost = touched * overhead_per_file
    total = data_cost + overhead_cost
    p_opt = P[np.argmin(total)]

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(P, data_cost / 1e6, color=FG_MUTE, ls="--", lw=1.6, label="data scanned (pruned)")
    ax.plot(P, overhead_cost / 1e6, color=ACCENT, ls=":", lw=1.8, label="per-file overhead")
    ax.plot(P, total / 1e6, color=C, lw=2.4, label="total cost")
    ax.axvline(p_opt, color=HOT, lw=1.6)
    ax.annotate(f"sweet spot\n≈ {p_opt} partitions", (p_opt, total.min() / 1e6),
                color=HOT, fontsize=9, xytext=(p_opt + 500, total.min() / 1e6 + 40),
                textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_xlabel("number of partitions")
    ax.set_ylabel("query cost (MB-equiv)")
    ax.set_title("Partition pruning: a sweet spot, not 'more is better'")
    ax.set_ylim(0, 6 * total.min() / 1e6)
    ax.legend(loc="upper center", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "partitioning-pruning")


def main() -> None:
    apply_style()
    row_vs_columnar()
    compression_encoding()
    partitioning_pruning()


if __name__ == "__main__":
    main()
