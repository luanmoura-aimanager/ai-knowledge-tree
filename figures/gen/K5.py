"""Figures for pillar K5 (orchestration & ELT). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GRID, apply_style, color, save

SUB = "K5"
C = color(SUB)  # pillar-K accent (mauve)


def incremental_processing() -> None:
    """Rows processed per run: a full-refresh model reprocesses the entire accumulated
    table every run (its per-run cost climbs with history), while an incremental model
    touches only each run's new/changed rows (flat). The right panel shows cumulative
    work: full-refresh grows quadratically, incremental linearly."""
    import matplotlib.pyplot as plt

    runs = np.arange(1, 21)
    delta = 50                                   # new/changed rows arriving each run
    incremental = np.full_like(runs, delta, dtype=float)
    full_refresh = delta * runs                  # whole table = delta * (runs so far)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 4.2))

    ax1.bar(runs - 0.2, full_refresh, width=0.4, color=FG_MUTE, label="full-refresh")
    ax1.bar(runs + 0.2, incremental, width=0.4, color=C, label="incremental")
    ax1.set_title("Rows processed per run")
    ax1.set_xlabel("run"); ax1.set_ylabel("rows processed")
    ax1.legend(loc="upper left", fontsize=8)

    ax2.plot(runs, np.cumsum(full_refresh), color=FG_MUTE, lw=2.2, label="full-refresh")
    ax2.plot(runs, np.cumsum(incremental), color=C, lw=2.4, label="incremental")
    ax2.set_title("Cumulative work")
    ax2.set_xlabel("run"); ax2.set_ylabel("rows processed (cumulative)")
    ax2.legend(loc="upper left", fontsize=8)

    fig.tight_layout()
    save(fig, SUB, "incremental-processing")


def scheduling_backfills() -> None:
    """Per-partition row counts after a backfill that re-touches every date (a double
    run). A buggy append doubles every partition (HOT); an idempotent overwrite holds
    the correct per-day counts (C). The dashed line marks each partition's true size."""
    import matplotlib.pyplot as plt

    dates = ["01-01", "01-02", "01-03", "01-04", "01-05"]
    true_counts = np.array([3, 2, 4, 5, 3], dtype=float)
    append = 2 * true_counts                      # appended twice -> doubled
    overwrite = true_counts.copy()                # overwrite -> correct
    x = np.arange(len(dates))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(x - 0.2, append, width=0.4, color=HOT, label="append (double-counts)")
    ax.bar(x + 0.2, overwrite, width=0.4, color=C, label="idempotent overwrite")
    for xi, t in zip(x, true_counts):
        ax.hlines(t, xi - 0.42, xi + 0.42, color=FG_MUTE, ls="--", lw=1.4,
                  zorder=3)
    ax.plot([], [], color=FG_MUTE, ls="--", lw=1.4, label="true partition size")
    ax.set_title("Partition row counts after a double backfill")
    ax.set_xlabel("partition (date)"); ax.set_ylabel("rows in partition")
    ax.set_xticks(x); ax.set_xticklabels(dates)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "scheduling-backfills")


def main() -> None:
    apply_style()
    incremental_processing()
    scheduling_backfills()


if __name__ == "__main__":
    main()
