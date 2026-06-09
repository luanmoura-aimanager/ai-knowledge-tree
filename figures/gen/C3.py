"""Figures for pillar C3 (tree ensembles). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "C3"
C = color(SUB)  # pillar-C accent


def decision_trees() -> None:
    """A decision tree carves the plane into axis-aligned rectangles, each with a
    constant prediction. Lesson's data: rng(0), y = (x₀²+x₁²<2) | (x₀>1.5),
    max_depth=5."""
    import matplotlib.pyplot as plt
    from sklearn.tree import DecisionTreeClassifier

    rng = np.random.default_rng(0)
    X = rng.uniform(-3, 3, size=(200, 2))
    y = ((X[:, 0] ** 2 + X[:, 1] ** 2 < 2) | (X[:, 0] > 1.5)).astype(int)
    clf = DecisionTreeClassifier(max_depth=5, random_state=0).fit(X, y)

    gx, gy = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-3, 3, 300))
    Z = clf.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)

    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    ax.contourf(gx, gy, Z, levels=[-0.5, 0.5, 1.5], colors=[ACCENT, HOT], alpha=0.22)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=16, color=HOT, edgecolor="none")
    ax.scatter(X[y == 0, 0], X[y == 0, 1], s=16, color=ACCENT, edgecolor="none")
    ax.set_title("Decision tree: axis-aligned regions (depth 5)")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "decision-trees")


def impurity_criteria() -> None:
    """Node impurity vs class balance for a two-class node: Gini and entropy both
    peak at p = 1/2 (maximally mixed) and vanish at the pure ends. Misclassification
    error is the lower, kinked curve splits favour."""
    import matplotlib.pyplot as plt

    p = np.linspace(1e-6, 1 - 1e-6, 400)
    gini = 2 * p * (1 - p)
    entropy = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    misclass = np.minimum(p, 1 - p)

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(p, entropy, color=C, lw=2.2, label="entropy (bits)")
    ax.plot(p, entropy / 2, color=C, lw=1.2, ls="--", label="entropy / 2")
    ax.plot(p, gini, color=HOT, lw=2.2, label="Gini")
    ax.plot(p, misclass, color=ACCENT, lw=2.0, label="misclassification")
    ax.set_title("Impurity measures vs class proportion")
    ax.set_xlabel("$p$ = fraction in class 1")
    ax.set_ylabel("impurity")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "impurity-criteria")


def bagging_rf() -> None:
    """Averaging many decorrelated trees drives test error down and flattens it:
    bagging/RF cut variance without adding bias. Lesson: rng(0), n=400, d=6,
    y = (x₀+x₁>0) XOR (x₂>0), 10% label noise."""
    import matplotlib.pyplot as plt
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier

    rng = np.random.default_rng(0)
    n, d = 400, 6
    X = rng.normal(size=(n, d))
    y = ((X[:, 0] + X[:, 1] > 0) ^ (X[:, 2] > 0)).astype(int)
    flip = rng.random(n) < 0.10
    y = np.where(flip, 1 - y, y)
    Xtr, ytr, Xte, yte = X[:300], y[:300], X[300:], y[300:]

    Bs = [1, 2, 5, 10, 20, 50, 100, 200]
    rf_err, tree_err = [], []
    single = DecisionTreeClassifier(max_depth=8, random_state=0).fit(Xtr, ytr)
    base_err = 1 - single.score(Xte, yte)
    for B in Bs:
        rf = RandomForestClassifier(n_estimators=B, max_features=2, max_depth=8,
                                    random_state=0).fit(Xtr, ytr)
        rf_err.append(1 - rf.score(Xte, yte))
        tree_err.append(base_err)

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(Bs, tree_err, color=FG_MUTE, ls="--", lw=1.8, label="single deep tree")
    ax.plot(Bs, rf_err, "-o", color=C, ms=4, lw=2.2, label="random forest")
    ax.set_xscale("log")
    ax.set_title("Variance reduction with ensemble size")
    ax.set_xlabel("number of trees $B$")
    ax.set_ylabel("test error")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "bagging-rf")


def adaboost() -> None:
    """AdaBoost builds a nonlinear boundary by reweighting hard examples: with more
    rounds the boundary tracks the XOR-like structure ever more tightly. Lesson:
    rng(0), n=400, y = sign(x₀x₁ - 0.3 + noise)."""
    import matplotlib.pyplot as plt
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier

    rng = np.random.default_rng(0)
    n = 400
    X = rng.normal(size=(n, 2))
    y = np.sign(X[:, 0] * X[:, 1] - 0.3 + 0.4 * rng.normal(size=n))

    gx, gy = np.meshgrid(np.linspace(-3, 3, 250), np.linspace(-3, 3, 250))
    grid = np.c_[gx.ravel(), gy.ravel()]
    fig, axes = plt.subplots(1, 4, figsize=(10.5, 3.0))
    for ax, T in zip(axes, [1, 5, 20, 50]):
        clf = AdaBoostClassifier(
            DecisionTreeClassifier(max_depth=1), n_estimators=T, random_state=0
        ).fit(X, y)
        Z = clf.predict(grid).reshape(gx.shape)
        ax.contourf(gx, gy, Z, levels=[-1.5, 0, 1.5], colors=[ACCENT, HOT], alpha=0.22)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=6, color=HOT, edgecolor="none")
        ax.scatter(X[y == -1, 0], X[y == -1, 1], s=6, color=ACCENT, edgecolor="none")
        ax.set_title(f"T = {T}")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("AdaBoost decision boundary across rounds", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "adaboost")


def gradient_boosting() -> None:
    """Gradient boosting drives training loss down monotonically; validation loss
    bottoms out and then creeps up as added trees overfit — the basis for early
    stopping. Lesson: rng(0), n=600, η=0.1, depth=3, T=... rounds."""
    import matplotlib.pyplot as plt
    from sklearn.ensemble import GradientBoostingRegressor

    rng = np.random.default_rng(0)
    n = 600
    X = rng.uniform(-3, 3, size=(n, 2))
    y = np.sin(X[:, 0]) + 0.3 * X[:, 1] ** 2 + 0.3 * rng.normal(size=n)
    Xtr, ytr, Xte, yte = X[:400], y[:400], X[400:], y[400:]

    T = 300
    gb = GradientBoostingRegressor(n_estimators=T, learning_rate=0.1, max_depth=3,
                                   random_state=0).fit(Xtr, ytr)

    def mse_path(Xd, yd):
        return np.array([((yd - p) ** 2).mean() for p in gb.staged_predict(Xd)])

    tr_mse, te_mse = mse_path(Xtr, ytr), mse_path(Xte, yte)
    best = int(np.argmin(te_mse))

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(tr_mse, color=C, lw=2.0, label="training loss")
    ax.plot(te_mse, color=HOT, lw=2.0, label="validation loss")
    ax.axvline(best, color=FG_MUTE, ls=":", lw=1.4, label=f"early-stop ≈ {best}")
    ax.set_title("Gradient boosting: train vs validation loss")
    ax.set_xlabel("boosting rounds")
    ax.set_ylabel("mean squared error")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "gradient-boosting")


def feature_importance() -> None:
    """MDI (impurity) importance is biased toward the high-cardinality / correlated
    features, while permutation importance splits credit between correlated copies.
    Lesson: rng(0), feats 0,1 informative, 2,3 noise, 4 ≈ copy of 0."""
    import matplotlib.pyplot as plt
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.inspection import permutation_importance

    rng = np.random.default_rng(0)
    n, d = 500, 5
    X = rng.normal(size=(n, d))
    X[:, 4] = X[:, 0] + 0.1 * rng.normal(size=n)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    Xtr, ytr, Xte, yte = X[:300], y[:300], X[300:], y[300:]
    rf = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=0).fit(Xtr, ytr)

    mdi = rf.feature_importances_
    perm = permutation_importance(rf, Xte, yte, n_repeats=20, random_state=0).importances_mean

    labels = ["0\n(signal)", "1\n(signal)", "2\n(noise)", "3\n(noise)", "4\n(≈copy of 0)"]
    xs = np.arange(d)
    w = 0.4
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.bar(xs - w / 2, mdi, w, color=C, label="MDI (impurity)")
    ax.bar(xs + w / 2, perm, w, color=HOT, label="permutation")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_title("Feature importance: MDI vs permutation")
    ax.set_xlabel("feature")
    ax.set_ylabel("importance")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "feature-importance")


def main() -> None:
    apply_style()
    decision_trees()
    impurity_criteria()
    bagging_rf()
    adaboost()
    gradient_boosting()
    feature_importance()


if __name__ == "__main__":
    main()
