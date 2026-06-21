"""Figures for pillar M1 (causal discovery). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, GOOD, HOT, FG_MUTE, apply_style, color, save

SUB = "M1"
C = color(SUB)  # pillar-M accent


def mec_size() -> None:
    """How underdetermined orientation is: the fraction of edges a CPDAG leaves
    undirected grows with graph density. Random Erdos-Renyi DAGs over a fixed
    topological order; for each, count edges that are reversible (their reversal
    gives the same skeleton and v-structures, so they stay undirected in the
    essential graph). Lesson: d=8 nodes, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    d = 8
    densities = np.linspace(0.1, 0.9, 9)
    undirected_frac = []
    for p in densities:
        fracs = []
        for _ in range(200):
            # upper-triangular adjacency over a fixed order = a random DAG
            A = (rng.random((d, d)) < p).astype(int)
            A = np.triu(A, 1)
            edges = list(zip(*np.nonzero(A)))
            if not edges:
                continue
            # an edge i->j is "covered" (reversible without changing the MEC)
            # iff parents(i) == parents(j) \ {i}; covered edges are exactly the
            # ones whose reversal keeps skeleton and v-structures.
            n_rev = 0
            for (i, j) in edges:
                pa_i = set(np.nonzero(A[:, i])[0])
                pa_j = set(np.nonzero(A[:, j])[0]) - {i}
                if pa_i == pa_j:
                    n_rev += 1
            fracs.append(n_rev / len(edges))
        undirected_frac.append(np.mean(fracs))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(densities, undirected_frac, "o-", color=C, lw=2.2)
    ax.set_title("Orientation left undetermined by the data\n(reversible edges in random DAGs)")
    ax.set_xlabel("edge probability $p$")
    ax.set_ylabel("fraction of reversible edges")
    ax.set_ylim(0, max(undirected_frac) * 1.2 + 0.02)
    fig.tight_layout()
    save(fig, SUB, "mec-size")


def ci_test() -> None:
    """The PC skeleton step rests on a conditional-independence test. For a
    Gaussian chain X1 -> X2 -> X3, the partial correlation rho(X1, X3 | X2) is
    ~0 (Fisher-z statistic centered at 0), while the marginal correlation
    rho(X1, X3) is large. The test must condition on X2 to delete the X1-X3 edge.
    Lesson: n=400 per draw, 2000 draws, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, reps = 400, 2000

    def partial_corr(a, b, c):
        # residualize a and b on [1, c], correlate the residuals
        Z = np.column_stack([np.ones(n), c])
        ra = a - Z @ np.linalg.lstsq(Z, a, rcond=None)[0]
        rb = b - Z @ np.linalg.lstsq(Z, b, rcond=None)[0]
        return np.corrcoef(ra, rb)[0, 1]

    marg, part = [], []
    for _ in range(reps):
        x1 = rng.normal(0, 1, n)
        x2 = x1 + rng.normal(0, 1, n)
        x3 = x2 + rng.normal(0, 1, n)
        marg.append(np.corrcoef(x1, x3)[0, 1])
        part.append(partial_corr(x1, x3, x2))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.hist(marg, bins=40, density=True, color=HOT, alpha=0.6,
            label=r"$\rho(X_1, X_3)$ (marginal)")
    ax.hist(part, bins=40, density=True, color=GOOD, alpha=0.6,
            label=r"$\rho(X_1, X_3 \mid X_2)$ (partial)")
    ax.axvline(0, color=FG_MUTE, lw=1.0, ls="--")
    ax.set_title("Conditioning on $X_2$ breaks the $X_1$-$X_3$ dependence")
    ax.set_xlabel("correlation")
    ax.set_ylabel("density")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "ci-test")


def bic_tradeoff() -> None:
    """GES scores a graph by BIC = fit - complexity penalty. On a chain
    X1->X2->X3->X4 (n=500), adding the true edges raises the log-likelihood a
    lot; adding spurious edges raises it negligibly while paying a fixed
    (log n / 2) * params penalty, so total BIC peaks at the true edge count.
    Lesson: rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 500
    x1 = rng.normal(0, 1, n)
    x2 = x1 + rng.normal(0, 1, n)
    x3 = x2 + rng.normal(0, 1, n)
    x4 = x3 + rng.normal(0, 1, n)
    X = np.column_stack([x1, x2, x3, x4])

    # local Gaussian log-likelihood of regressing target on a set of parents
    def loglik(target, parents):
        y = X[:, target]
        if parents:
            Z = np.column_stack([np.ones(n)] + [X[:, p] for p in parents])
        else:
            Z = np.ones((n, 1))
        resid = y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]
        sigma2 = max((resid @ resid) / n, 1e-8)
        return -0.5 * n * (np.log(2 * np.pi * sigma2) + 1)

    pen = 0.5 * np.log(n)
    # incrementally build the true chain, then add one spurious edge
    edge_sets = [
        ([], "empty"),
        ([(0, 1)], "+1 true"),
        ([(0, 1), (1, 2)], "+2 true"),
        ([(0, 1), (1, 2), (2, 3)], "+3 true (chain)"),
        ([(0, 1), (1, 2), (2, 3), (0, 3)], "+spurious"),
    ]
    fit, complexity, bic = [], [], []
    for edges, _ in edge_sets:
        # build parent sets per node
        parents = {t: [s for (s, tt) in edges if tt == t] for t in range(4)}
        ll = sum(loglik(t, parents.get(t, [])) for t in range(4))
        k = len(edges)  # one extra parameter per edge
        fit.append(ll)
        complexity.append(pen * k)
        bic.append(ll - pen * k)

    labels = [s for _, s in edge_sets]
    xs = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.plot(xs, fit, "o-", color=ACCENT, label="log-likelihood (fit)")
    ax.plot(xs, [-c for c in complexity], "s--", color=HOT, label="$-$penalty")
    ax.plot(xs, bic, "D-", color=C, lw=2.4, label="BIC = fit $-$ penalty")
    best = int(np.argmax(bic))
    ax.scatter([best], [bic[best]], s=120, facecolor="none", edgecolor=GOOD,
               lw=2.0, zorder=5, label="BIC maximum")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("score")
    ax.set_title("BIC peaks at the true edge set")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "bic-tradeoff")


def lingam_residuals() -> None:
    """LiNGAM orients X -> Y by non-Gaussianity. With Y = X + e and e uniform
    (non-Gaussian), regressing Y on X leaves a residual independent of X (correct
    direction), but regressing X on Y leaves a residual dependent on Y (wrong
    direction). The scatter of residual vs regressor shows the asymmetry.
    Lesson: n=600, uniform noise, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 600
    x = rng.uniform(-1, 1, n)            # non-Gaussian cause
    e = rng.uniform(-0.5, 0.5, n)        # non-Gaussian noise
    y = x + e                            # true model X -> Y

    def resid(a, b):  # residual of a regressed on [1, b]
        Z = np.column_stack([np.ones(n), b])
        return a - Z @ np.linalg.lstsq(Z, a, rcond=None)[0]

    r_fwd = resid(y, x)   # correct: residual of Y|X vs X
    r_bwd = resid(x, y)   # wrong:   residual of X|Y vs Y

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9))
    ax1.scatter(x, r_fwd, s=10, color=GOOD, alpha=0.6, edgecolor="none")
    ax1.set_title("Correct: $X \\to Y$\nresidual $\\perp X$")
    ax1.set_xlabel("$X$")
    ax1.set_ylabel("residual of $Y \\mid X$")

    ax2.scatter(y, r_bwd, s=10, color=HOT, alpha=0.6, edgecolor="none")
    ax2.set_title("Wrong: $Y \\to X$\nresidual depends on $Y$")
    ax2.set_xlabel("$Y$")
    ax2.set_ylabel("residual of $X \\mid Y$")
    fig.tight_layout()
    save(fig, SUB, "lingam-residuals")


def notears_acyclicity() -> None:
    """NOTEARS replaces the combinatorial acyclicity constraint with the smooth
    measure h(W) = tr(exp(W o W)) - d, which is 0 iff W o W has no directed
    cycle. Left: h grows as a single cycle's weight increases (a 3-cycle
    W[0,1]=W[1,2]=W[2,0]=w). Right: an augmented-Lagrangian run drives h(W)
    toward 0 over iterations. Lesson: d=3 and a small least-squares run, rng(0)."""
    import matplotlib.pyplot as plt
    from scipy.linalg import expm

    d = 3
    ws = np.linspace(0, 1.5, 60)
    hs = []
    for w in ws:
        W = np.zeros((d, d))
        W[0, 1] = W[1, 2] = W[2, 0] = w   # a directed 3-cycle
        M = W * W
        hs.append(np.trace(expm(M)) - d)

    # a tiny gradient run minimizing h via penalty, starting from a cyclic W
    rng = np.random.default_rng(0)
    W = 0.6 * np.ones((d, d)) - 0.6 * np.eye(d)
    np.fill_diagonal(W, 0.0)
    hist = []
    lr = 0.05
    for _ in range(60):
        M = W * W
        E = expm(M)
        h = np.trace(E) - d
        hist.append(max(h, 1e-6))
        grad_h = E.T * 2 * W            # dh/dW = (expm(W o W))^T o 2W
        W = W - lr * grad_h

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9))
    ax1.plot(ws, hs, color=C, lw=2.4)
    ax1.axhline(0, color=FG_MUTE, lw=1.0, ls="--")
    ax1.set_title("$h(W)$ vs cycle weight\n($h=0$ iff acyclic)")
    ax1.set_xlabel("cycle weight $w$")
    ax1.set_ylabel("$h(W) = \\mathrm{tr}\\,e^{W \\circ W} - d$")

    ax2.semilogy(hist, color=GOOD, lw=2.2)
    ax2.set_title("Penalized descent drives $h(W) \\to 0$")
    ax2.set_xlabel("iteration")
    ax2.set_ylabel("$h(W)$ (log scale)")
    fig.tight_layout()
    save(fig, SUB, "notears-acyclicity")


def main() -> None:
    apply_style()
    mec_size()
    ci_test()
    bic_tradeoff()
    lingam_residuals()
    notears_acyclicity()


if __name__ == "__main__":
    main()
