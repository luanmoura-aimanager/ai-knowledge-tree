"""Figures for pillar G4 (time-series anomalies & change). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "G4"
C = color(SUB)  # pillar-G accent (teal)


def cusum_changepoint() -> None:
    """CUSUM accumulates how far each point sits above (or below) the expected mean;
    while the process is in control the sum hovers near zero, but after a mean shift
    it drifts steadily until it crosses a threshold — flagging the change. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, cp = 200, 120
    x = rng.normal(0, 1, n)
    x[cp:] += 1.2                                  # mean shift
    k, thr = 0.5, 8.0
    s = np.zeros(n)
    for t in range(1, n):
        s[t] = max(0, s[t - 1] + (x[t] - 0) - k)
    detect = np.argmax(s > thr) if (s > thr).any() else None

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True)
    ax1.plot(x, color=FG_MUTE, lw=0.8)
    ax1.axvline(cp, color=GOOD, ls="--", lw=1.4, label="true change")
    ax1.set_title("Series with a mean shift"); ax1.legend(loc="upper left", fontsize=8)
    ax2.plot(s, color=C, lw=1.8, label="CUSUM statistic")
    ax2.axhline(thr, color=HOT, ls="--", lw=1.4, label=f"threshold = {thr:.0f}")
    if detect:
        ax2.axvline(detect, color=HOT, lw=1.2)
    ax2.set_title("CUSUM crosses the threshold after the shift")
    ax2.set_xlabel("time"); ax2.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "cusum-changepoint")


def statistical_anomaly_detection() -> None:
    """Statistical detection flags points that fall outside a rolling band: a moving
    mean ± k·(rolling σ) adapts to the local level, so genuine spikes stand out while
    normal fluctuation stays inside. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 240
    x = 5 + np.sin(np.arange(n) / 12) + rng.normal(0, 0.4, n)
    anom = [60, 130, 195]
    x[anom] += np.array([3.5, -3.0, 3.2])
    w = 20
    mean = np.array([x[max(0, t - w):t + 1].mean() for t in range(n)])
    sd = np.array([x[max(0, t - w):t + 1].std() for t in range(n)])
    sd = np.maximum(sd, 0.6)                         # floor: don't flag normal jitter
    flag = np.abs(x - mean) > 3 * sd

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.fill_between(range(n), mean - 3 * sd, mean + 3 * sd, color=C, alpha=0.15,
                    label="rolling mean ± 3σ")
    ax.plot(x, color=FG_MUTE, lw=0.9)
    ax.scatter(np.where(flag)[0], x[flag], s=40, color=HOT, zorder=5, label="flagged")
    ax.set_title("Statistical anomaly detection")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "statistical-anomaly-detection")


def deep_anomaly_detection() -> None:
    """A deep detector learns to reconstruct normal patterns, so its reconstruction
    error stays low on routine data and spikes wherever the signal departs from what
    it has seen — thresholding the error surfaces the anomalies. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 300
    t = np.arange(n)
    x = np.sin(t / 10) + 0.5 * np.sin(t / 3)
    err = np.abs(rng.normal(0, 0.05, n))
    for c, mag in [(80, 0.9), (170, 0.7), (245, 1.0)]:
        err[c:c + 6] += mag * np.exp(-np.arange(6) / 2)
    thr = 0.4

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 4.8), sharex=True)
    ax1.plot(x, color=FG_MUTE, lw=0.9); ax1.set_title("signal")
    ax2.plot(err, color=C, lw=1.2, label="reconstruction error")
    ax2.axhline(thr, color=HOT, ls="--", lw=1.4, label=f"threshold = {thr}")
    ax2.scatter(np.where(err > thr)[0], err[err > thr], s=20, color=HOT, zorder=5)
    ax2.set_title("Reconstruction error spikes at anomalies")
    ax2.set_xlabel("time"); ax2.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "deep-anomaly-detection")


def main() -> None:
    apply_style()
    cusum_changepoint()
    statistical_anomaly_detection()
    deep_anomaly_detection()


if __name__ == "__main__":
    main()
