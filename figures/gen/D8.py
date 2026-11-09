"""Figures for pillar D8 (tabular & event foundation models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_DIM, FG_MUTE, GOOD, GRID, HOT, LEGEND_BG, PARTIAL, apply_style, color, save

SUB = "D8"
C = color(SUB)  # pillar-D accent (blue)


def entropy_bits(counts: np.ndarray) -> float:
    p = counts / counts.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def amount_bins() -> None:
    """Uniform-width vs quantile buckets on log-normal transaction amounts: uniform
    bins put almost every amount in the first bucket (low token entropy); quantile
    bins spread mass evenly (log2 B bits). Same data as the lesson's code block."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    amounts = rng.lognormal(mean=np.log(20.0), sigma=1.2, size=100_000)
    B = 16
    uni_edges = np.linspace(0, amounts.max(), B + 1)
    q_edges = np.quantile(amounts, np.linspace(0, 1, B + 1))
    uni_counts = np.histogram(amounts, uni_edges)[0]
    q_counts = np.histogram(amounts, q_edges)[0]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.8))
    for ax, counts, name, col in (
        (axes[0], uni_counts, "uniform-width", HOT),
        (axes[1], q_counts, "quantile (equal mass)", C),
    ):
        ax.bar(np.arange(B), counts / counts.sum(), color=col, width=0.8)
        ax.set_title(f"{name}: H = {entropy_bits(counts):.2f} bits")
        ax.set_xlabel("bucket index (token id)")
        ax.set_ylim(0, 1.0)
    axes[0].set_ylabel("fraction of transactions")
    axes[1].axhline(1 / B, color=FG_MUTE, ls=":", lw=1)
    fig.suptitle("16 amount buckets on log-normal amounts (median 20)", color=FG_DIM, fontsize=10)
    fig.tight_layout()
    save(fig, SUB, "amount-bins")


def warp(t: np.ndarray) -> np.ndarray:
    return 8.0 * np.log1p(t / 8.0)


def time_warp() -> None:
    """Left: the soft-log warp phi(a) = 8 ln(1 + a/8) of an event's age in seconds,
    with calendar landmarks. Right: the mean RoPE score cos(theta_i * dphi) averaged
    over frequency pairs, for base 10,000 vs the range-matched base, over the warped
    range of a 25-month history."""
    import matplotlib.pyplot as plt

    a = np.logspace(0, np.log10(66e6), 400)
    marks = {"1 s": 1, "1 min": 60, "1 h": 3600, "1 day": 86400, "1 week": 604800,
             "30 days": 2.592e6, "25 months": 65.7e6}

    d = 64
    R = float(warp(np.array(65.7e6)))
    b_star = (2 * R / np.pi) ** (d / (d - 2))
    dphi = np.linspace(0, R, 400)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax = axes[0]
    ax.plot(a, warp(a), color=C, lw=2)
    for k, v in marks.items():
        y = float(warp(np.array(v)))
        ax.plot([v], [y], "o", color=PARTIAL, ms=4)
        ax.annotate(k, (v, y), textcoords="offset points", xytext=(4, -11), fontsize=7.5,
                    color=FG_DIM)
    ax.set_xscale("log")
    ax.set_xlabel("event age a (seconds, log scale)")
    ax.set_ylabel(r"warped coordinate $\varphi(a)$")
    ax.set_title(r"$\varphi(a) = 8\ln(1 + a/8)$")

    ax = axes[1]
    for base, col, lab in ((1e4, HOT, "base 10,000"), (b_star, GOOD, f"base {b_star:.0f}")):
        theta = base ** (-2 * np.arange(d // 2) / d)
        score = np.cos(np.outer(dphi, theta)).mean(axis=1)
        ax.plot(dphi, score, color=col, lw=1.8, label=lab)
    ax.axhline(0, color=GRID, lw=1)
    ax.set_xlabel(r"warped time gap $\Delta\varphi$")
    ax.set_ylabel("mean cos over 32 pairs")
    ax.set_title("How fast scores decorrelate")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "time-warp")


def masking_patterns() -> None:
    """Three masking granularities on an events x fields grid: token-level (scattered
    cells), event-level (whole rows), key-level (whole columns)."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    rng = np.random.default_rng(0)
    E, F = 10, 6
    tok = (rng.random((E, F)) < 0.15).astype(float)
    evt = np.zeros((E, F)); evt[[2, 7], :] = 1
    key = np.zeros((E, F)); key[:, 1] = 1
    fields = ["amount", "MCC", "merchant", "currency", "channel", "text"]
    cmap = ListedColormap([LEGEND_BG, HOT])

    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.9), sharey=True)
    for ax, m, title in ((axes[0], tok, "token-level (15%)"),
                         (axes[1], evt, "event-level (whole event)"),
                         (axes[2], key, "key-level (whole field)")):
        ax.imshow(m, cmap=cmap, vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(F)); ax.set_xticklabels(fields, rotation=55, fontsize=7.5)
        ax.set_xticks(np.arange(-.5, F, 1), minor=True)
        ax.set_yticks(np.arange(-.5, E, 1), minor=True)
        ax.grid(which="minor", color=GRID, lw=0.8)
        ax.grid(which="major", visible=False)
        ax.tick_params(which="minor", length=0)
        ax.set_title(title, fontsize=9)
    axes[0].set_ylabel("event index in history")
    fig.tight_layout()
    save(fig, SUB, "masking-patterns")


def context_budget() -> None:
    """Context tokens consumed vs history length: textualized events (~25 tokens each)
    against one learned embedding per event, with the 40,960-position limit of the
    Qwen3-0.6B config."""
    import matplotlib.pyplot as plt

    n = np.arange(0, 8001, 50)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.plot(n, 25 * n, color=HOT, lw=2, label="textualized (25 tokens/event)")
    ax.plot(n, n, color=GOOD, lw=2, label="event embeddings (1 token/event)")
    ax.axhline(40960, color=PARTIAL, ls="--", lw=1.2)
    ax.text(150, 43000, "Qwen3-0.6B max_position_embeddings = 40,960", color=PARTIAL, fontsize=8)
    ax.axvline(40960 / 25, color=FG_MUTE, ls=":", lw=1)
    ax.text(40960 / 25 + 80, 120000, "1,638 events", color=FG_DIM, fontsize=8)
    ax.set_xlabel("events in the user's history")
    ax.set_ylabel("tokens in the context")
    ax.set_ylim(0, 200000)
    ax.set_title("Two ways to feed events to an LLM backbone")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(0, 0.9))
    fig.tight_layout()
    save(fig, SUB, "context-budget")


def pragma_scaling() -> None:
    """PRAGMA Table 2 (LoRA vs task-specific baseline, credit scoring), relative lifts
    for S / M / L: PR-AUC lifts dwarf ROC-AUC lifts on the same models."""
    import matplotlib.pyplot as plt

    sizes = ["S (10M)", "M (100M)", "L (1B)"]
    pr = [70.3, 98.0, 130.2]
    roc = [6.2, 10.1, 12.4]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.bar(x - 0.18, pr, width=0.36, color=C, label="PR-AUC lift")
    ax.bar(x + 0.18, roc, width=0.36, color=PARTIAL, label="ROC-AUC lift")
    for xi, v in zip(x, pr):
        ax.text(xi - 0.18, v + 2, f"+{v:.1f}%", ha="center", fontsize=8, color=FG_DIM)
    for xi, v in zip(x, roc):
        ax.text(xi + 0.18, v + 2, f"+{v:.1f}%", ha="center", fontsize=8, color=FG_DIM)
    ax.set_xticks(x); ax.set_xticklabels(sizes)
    ax.set_ylabel("relative lift over baseline (%)")
    ax.set_title("Credit scoring, same models, two metrics (PRAGMA, Table 2)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "pragma-scaling")


def pfn_nll() -> None:
    """Prior-data NLL of the estimator family q_a = (h + a)/(n + 2a) on coin datasets
    drawn from a uniform prior: the minimizer is a = 1, the Bayesian posterior
    predictive (Laplace's rule). Same Monte Carlo as the lesson's code."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    S = 200_000
    theta = rng.random(S)
    n = rng.integers(0, 11, S)
    h = rng.binomial(n, theta)
    y = rng.random(S) < theta
    grid = np.linspace(0.05, 4, 160)
    nll = []
    for a in grid:
        q = (h + a) / (n + 2 * a)
        nll.append(-np.mean(np.where(y, np.log(q), np.log(1 - q))))
    nll = np.array(nll)
    a_star = grid[nll.argmin()]

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.plot(grid, nll, color=C, lw=2)
    ax.axvline(1.0, color=GOOD, ls="--", lw=1.2, label="a = 1 (posterior predictive)")
    ax.plot([a_star], [nll.min()], "o", color=HOT, label=f"empirical minimum a = {a_star:.2f}")
    ax.set_xlabel(r"pseudo-count $a$ in $q_a = (h+a)/(n+2a)$")
    ax.set_ylabel("prior-data NLL (nats)")
    ax.set_title("Training on the prior recovers Bayes")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "pfn-nll")


def main() -> None:
    apply_style()
    amount_bins()
    time_warp()
    masking_patterns()
    context_budget()
    pragma_scaling()
    pfn_nll()


if __name__ == "__main__":
    main()
