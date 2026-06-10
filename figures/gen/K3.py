"""Figures for pillar K3 (batch & distributed processing). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "K3"
C = color(SUB)  # pillar-K accent (mauve)


def mapreduce() -> None:
    """Cost of a distributed aggregation broken down by phase. Map and reduce are
    local, CPU-bound, and cheap; the shuffle moves every intermediate record across
    the network and dominates the wall-clock cost of a big job."""
    import matplotlib.pyplot as plt

    phases = ["map", "shuffle", "reduce"]
    # Relative cost units: shuffle (all-to-all network) dwarfs the local phases.
    cost = [12.0, 60.0, 10.0]
    colors = [FG_MUTE, C, FG_MUTE]

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    bars = ax.bar(phases, cost, color=colors, width=0.6)
    bars[1].set_label("network all-to-all")
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=3, color="#e6e9f5", fontsize=10)
    ax.annotate("shuffle dominates", (1, 60), color=HOT, fontsize=10,
                xytext=(1.15, 50), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Cost of a MapReduce job by phase")
    ax.set_ylabel("relative cost")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "mapreduce")


def distributed_joins() -> None:
    """Network bytes moved by a shuffle join vs a broadcast join as the small table
    grows, with W workers. Shuffle moves |A|+|B| (flat in the small side up to its own
    size); broadcast moves W*|small| (a line through the origin with slope W). They
    cross where W*small = |A|+small; below the crossover, broadcast wins."""
    import matplotlib.pyplot as plt

    A = 1000.0       # large table size (MB)
    W = 8            # workers
    small = np.linspace(0, 300, 300)   # small-table size (MB)

    shuffle = A + small               # both sides repartitioned by key
    broadcast = W * small             # ship the small side to every worker

    # Crossover: A + s = W*s  ->  s = A / (W - 1)
    s_star = A / (W - 1)
    cross_y = A + s_star

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(small, shuffle, color=C, lw=2.4, label="shuffle join  (|A|+|B|)")
    ax.plot(small, broadcast, color=ACCENT, lw=2.4, ls="--",
            label=f"broadcast join  (W·|small|, W={W})")
    ax.axvline(s_star, color=GRID, lw=1.0, ls=":")
    ax.plot(s_star, cross_y, "o", color=HOT, ms=8)
    ax.annotate(f"crossover\nsmall ≈ {s_star:.0f} MB", (s_star, cross_y),
                color=HOT, fontsize=9, xytext=(s_star + 30, cross_y + 250),
                textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Distributed join: bytes moved vs small-table size")
    ax.set_xlabel("small-table size (MB)")
    ax.set_ylabel("network bytes (MB)")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "distributed-joins")


def data_skew() -> None:
    """Per-reducer load before and after salting a skewed key distribution. A power-law
    key set piles onto one reducer, so wall-clock tracks the max bar (the straggler),
    not the mean. Salting splits the hottest key across reducers, dropping the max."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    R = 8
    # Power-law key counts hashed to R reducers: one reducer gets the hot key.
    n_keys = 200
    counts = (rng.pareto(1.2, n_keys) + 1) * 10
    assign = rng.integers(0, R, n_keys)
    load = np.zeros(R)
    for k in range(n_keys):
        load[assign[k]] += counts[k]

    # Force a clear hot reducer for the illustration.
    hot_r = int(np.argmax(load))
    before = load.copy()

    # Salting: split the hottest reducer's load across all R reducers.
    after = before.copy()
    spill = after[hot_r] * (1 - 1.0 / R)
    after[hot_r] -= spill
    after += spill / R

    x = np.arange(R)
    w = 0.38
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.bar(x - w / 2, before, w, color=FG_MUTE, label="before salting")
    ax.bar(x + w / 2, after, w, color=C, label="after salting")
    ax.axhline(before.max(), color=HOT, ls="--", lw=1.6,
               label=f"max load before ({before.max():.0f})")
    ax.axhline(before.mean(), color=ACCENT, ls=":", lw=1.6,
               label=f"mean load ({before.mean():.0f})")
    ax.set_title("Data skew: per-reducer load before vs after salting")
    ax.set_xlabel("reducer")
    ax.set_ylabel("records assigned")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "data-skew")


def query_execution_pushdown() -> None:
    """Bytes reaching the CPU at each plan stage. A naive plan reads the whole table;
    projection pushdown drops unread columns; predicate pushdown (partition pruning +
    Parquet stats) skips row groups that cannot match. Each step is strictly smaller."""
    import matplotlib.pyplot as plt

    N, Cn = 10_000_000, 20      # rows, columns
    bytes_per_cell = 8
    full = N * Cn * bytes_per_cell

    cols_kept = 3               # projection keeps 3 of 20 columns
    after_proj = N * cols_kept * bytes_per_cell

    selectivity = 0.05          # predicate keeps 5% of rows
    after_pred = int(N * selectivity) * cols_kept * bytes_per_cell

    stages = ["full scan", "+ projection", "+ predicate"]
    vals = np.array([full, after_proj, after_pred]) / 1e9   # GB
    colors = [FG_MUTE, ACCENT, C]

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    bars = ax.bar(stages, vals, color=colors, width=0.6)
    ax.bar_label(ax.containers[0], fmt="%.2f GB", padding=3,
                 color="#e6e9f5", fontsize=10)
    ax.annotate("bytes the CPU\nnever touches", (2, vals[2]), color=HOT, fontsize=9,
                xytext=(1.4, vals[0] * 0.55), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Query execution: bytes reaching the CPU shrink at each stage")
    ax.set_ylabel("bytes read (GB)")
    fig.tight_layout()
    save(fig, SUB, "query-execution-pushdown")


def main() -> None:
    apply_style()
    mapreduce()
    distributed_joins()
    data_skew()
    query_execution_pushdown()


if __name__ == "__main__":
    main()
