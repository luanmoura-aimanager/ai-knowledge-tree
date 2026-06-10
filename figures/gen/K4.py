"""Figures for pillar K4 (streaming & ingestion). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "K4"
C = color(SUB)  # pillar-K accent (mauve)


def windowing() -> None:
    """A timeline of events cut by tumbling vs sliding windows. Tumbling windows tile
    the axis with no overlap, so each event lands in exactly one; sliding windows step
    by a smaller slide and overlap, so most events land in several. The per-window
    counts differ accordingly. Events seeded with rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    t_end = 20.0
    times = np.sort(rng.uniform(0, t_end, 16))

    width, slide = 5.0, 2.5
    tumbling = [(s, s + width) for s in np.arange(0, t_end, width)]
    sliding = [(s, s + width) for s in np.arange(0, t_end - width + 1e-9, slide)]

    fig, (ax_t, ax_s) = plt.subplots(2, 1, figsize=(7.2, 4.4), sharex=True)

    for ax, wins, title in (
        (ax_t, tumbling, "Tumbling (width 5, no overlap)"),
        (ax_s, sliding, "Sliding (width 5, slide 2.5, overlap)"),
    ):
        for i, (a, b) in enumerate(wins):
            y = 0.35 + 0.18 * (i % 3)
            ax.axvspan(a, b, ymin=0.55, ymax=0.55 + 0.12, color=C, alpha=0.22)
            ax.hlines(y, a, b, color=C, lw=2.4, alpha=0.9)
            cnt = int(np.sum((times >= a) & (times < b)))
            ax.text((a + b) / 2, y + 0.05, str(cnt), color=FG_MUTE,
                    ha="center", va="bottom", fontsize=9)
        ax.vlines(times, 0.05, 0.30, color=HOT, lw=1.6)
        ax.set_ylim(0, 1.05)
        ax.set_yticks([])
        ax.set_title(title, fontsize=11, loc="left")

    ax_s.set_xlabel("event time")
    fig.suptitle("Windowing the same event stream", fontsize=13)
    fig.tight_layout()
    save(fig, SUB, "windowing")


def watermarks_late_data() -> None:
    """Event time vs processing time for an out-of-order stream. Each point is an event:
    x is when it happened, y is when it arrived. The watermark (max event time seen so
    far, minus the allowed lateness) rises as a step line; events that arrive after the
    watermark has already passed their event time are late and flagged in HOT. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 40
    event_time = np.sort(rng.uniform(0, 20, n))
    delay = rng.exponential(1.2, n)
    delay[[7, 19, 31]] += 6.0                      # three badly delayed events
    proc_time = event_time + delay
    order = np.argsort(proc_time)                  # arrival order
    et, pt = event_time[order], proc_time[order]

    allowed_lateness = 2.0
    running_max = np.maximum.accumulate(et)
    watermark = running_max - allowed_lateness     # watermark at each arrival
    late = et < watermark                          # event older than current watermark

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.scatter(et[~late], pt[~late], color=C, s=34, label="on-time event", zorder=3)
    ax.scatter(et[late], pt[late], color=HOT, s=60, marker="X",
               label="late (dropped)", zorder=4)
    ax.plot(et, watermark + pt - et, color=FG_MUTE, lw=0)  # keep axes framed
    ax.step(running_max, watermark, where="post", color=ACCENT, lw=1.8,
            label="watermark = max(event time) − 2")
    ax.plot([0, 28], [0, 28], color=GRID, ls="--", lw=1.2, label="proc = event time")
    ax.set_title("Event time vs processing time, with watermark")
    ax.set_xlabel("event time"); ax.set_ylabel("processing time")
    ax.set_xlim(0, 21); ax.set_ylim(0, 28)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "watermarks-late-data")


def delivery_semantics() -> None:
    """At-least-once delivery duplicates some events, so a naive counter over-counts the
    true number of distinct events. An idempotent consumer keyed on the event id dedups
    and recovers the true count. The bars compare true, naive, and idempotent. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    true_n = 1000
    ids = np.arange(true_n)
    dup_mask = rng.random(true_n) < 0.18           # ~18% of events redelivered once
    stream = np.concatenate([ids, ids[dup_mask]])  # at-least-once: originals + dups
    naive = stream.size
    idempotent = np.unique(stream).size

    labels = ["true", "naive\n(at-least-once)", "idempotent\n(dedup by id)"]
    vals = [true_n, naive, idempotent]
    cols = [FG_MUTE, HOT, C]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bars = ax.bar(labels, vals, color=cols, width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 6, str(v),
                ha="center", va="bottom", color=FG_MUTE, fontsize=10)
    ax.axhline(true_n, color=FG_MUTE, ls="--", lw=1.2)
    ax.set_ylim(0, naive * 1.12)
    ax.set_ylabel("events counted")
    ax.set_title("Delivery semantics: idempotency recovers the true count")
    fig.tight_layout()
    save(fig, SUB, "delivery-semantics")


def main() -> None:
    apply_style()
    windowing()
    watermarks_late_data()
    delivery_semantics()


if __name__ == "__main__":
    main()
