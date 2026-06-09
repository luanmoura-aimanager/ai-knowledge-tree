"""Figures for pillar C6 (anomaly detection). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, LEGEND_BG, apply_style, color, save

SUB = "C6"
C = color(SUB)  # pillar-C accent


def statistical_ad() -> None:
    """Threshold-based outlier detection: the IQR fences (1.5·IQR) and the ±3σ
    z-score band flag the three planted outliers. The robust IQR fences sit
    tighter than the σ band, which the outliers themselves inflate. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    normal = rng.normal(0, 1, 200)
    outliers = np.array([6.0, -7.0, 8.0])
    data = np.concatenate([normal, outliers])
    idx = np.arange(len(data))

    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mu, sd = data.mean(), data.std()
    zlo, zhi = mu - 3 * sd, mu + 3 * sd

    is_out = (data < lo) | (data > hi)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.scatter(idx[~is_out], data[~is_out], s=14, color=ACCENT, edgecolor="none",
               label="inliers")
    ax.scatter(idx[is_out], data[is_out], s=70, color=HOT, marker="X",
               edgecolor="none", zorder=4, label="flagged (IQR)")
    ax.axhline(hi, color=C, ls="-", lw=1.4, label="IQR fence (1.5·IQR)")
    ax.axhline(lo, color=C, ls="-", lw=1.4)
    ax.axhline(zhi, color=FG_MUTE, ls="--", lw=1.4, label="z-score ±3σ")
    ax.axhline(zlo, color=FG_MUTE, ls="--", lw=1.4)
    ax.set_title("Statistical outlier thresholds")
    ax.set_xlabel("sample index")
    ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=9, frameon=True, facecolor=LEGEND_BG,
              edgecolor=FG_MUTE, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "statistical-ad")


def isolation_forest() -> None:
    """Isolation Forest scores points by how few random splits isolate them:
    outliers sit in sparse regions and are isolated quickly, so the score surface
    flags them. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.ensemble import IsolationForest

    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(0, 1, (400, 2)), rng.uniform(-5, 5, (20, 2))])
    clf = IsolationForest(random_state=0, contamination=0.05).fit(X)
    gx, gy = np.meshgrid(np.linspace(-6, 6, 300), np.linspace(-6, 6, 300))
    Z = clf.decision_function(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
    pred = clf.predict(X)

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.contourf(gx, gy, Z, levels=15, cmap="RdBu", alpha=0.7)
    ax.scatter(X[pred == 1, 0], X[pred == 1, 1], s=10, color=ACCENT, edgecolor="none",
               label="normal")
    ax.scatter(X[pred == -1, 0], X[pred == -1, 1], s=34, color=HOT, marker="X",
               label="flagged")
    ax.set_title("Isolation Forest anomaly score")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="upper left", fontsize=8, frameon=True, facecolor=LEGEND_BG,
              edgecolor=GRID)
    fig.tight_layout()
    save(fig, SUB, "isolation-forest")


def one_class_svm() -> None:
    """A one-class SVM learns a boundary that tightly encloses the normal data;
    points outside it — here a ring of anomalies around a dense cluster — are
    flagged as novelties. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.svm import OneClassSVM

    rng = np.random.default_rng(0)
    Xn = rng.normal(0, 0.6, (200, 2))
    th = rng.uniform(0, 2 * np.pi, 40)
    r = 3 + 0.2 * rng.normal(size=40)
    Xa = np.column_stack([r * np.cos(th), r * np.sin(th)])
    clf = OneClassSVM(nu=0.05, gamma=0.3).fit(Xn)
    gx, gy = np.meshgrid(np.linspace(-4, 4, 300), np.linspace(-4, 4, 300))
    Z = clf.decision_function(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)

    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    ax.contourf(gx, gy, Z, levels=[-100, 0, 100], colors=[HOT, ACCENT], alpha=0.15)
    ax.contour(gx, gy, Z, levels=[0], colors=[C], linewidths=2.4)
    ax.scatter(Xn[:, 0], Xn[:, 1], s=10, color=ACCENT, edgecolor="none", label="normal")
    ax.scatter(Xa[:, 0], Xa[:, 1], s=14, color=HOT, edgecolor="none", label="anomalies")
    ax.set_aspect("equal")
    ax.set_title("One-class SVM boundary")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", fontsize=8, frameon=True, facecolor=LEGEND_BG,
              edgecolor=GRID)
    fig.tight_layout()
    save(fig, SUB, "one-class-svm")


def main() -> None:
    apply_style()
    isolation_forest()
    one_class_svm()
    statistical_ad()


if __name__ == "__main__":
    main()
