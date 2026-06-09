"""Figures for pillar J5 (retrieval & data). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, apply_style, color, save

SUB = "J5"
C = color(SUB)  # pillar-J accent


def hybrid_search_rrf() -> None:
    """Reciprocal rank fusion blends two rankings without tuning weights: each list
    contributes 1/(k+rank) to a document's score, so an item ranked decently by BOTH
    keyword and vector search outscores one ranked first by only a single retriever.
    Here doc B (ranked #2 by each) wins, beating doc A (#1 keyword) and doc D
    (#1 vector)."""
    import matplotlib.pyplot as plt

    k = 60
    docs = ["A", "B", "C", "D", "E"]
    bm25_rank = {"A": 1, "B": 2, "C": 3, "D": 10, "E": 5}
    vec_rank = {"A": 10, "B": 2, "C": 3, "D": 1, "E": 5}
    bm = np.array([1 / (k + bm25_rank[d]) for d in docs])
    ve = np.array([1 / (k + vec_rank[d]) for d in docs])
    total = bm + ve
    order = np.argsort(-total)

    y = np.arange(len(docs))[::-1]
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.barh(y, bm[order], color=C, label="from keyword (BM25)")
    ax.barh(y, ve[order], left=bm[order], color=ACCENT, label="from vector")
    for i, o in enumerate(order):
        ax.text(total[o] + 0.0002, y[i],
                f"BM25 #{bm25_rank[docs[o]]}, vec #{vec_rank[docs[o]]}",
                va="center", fontsize=8, color=FG_DIM)
    ax.set_yticks(y); ax.set_yticklabels([f"doc {docs[o]}" for o in order])
    ax.set_xlabel("RRF score  =  Σ 1/(k + rank)")
    ax.set_title("Reciprocal rank fusion ranks the consensus pick first")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(0, total.max() * 1.5)
    fig.tight_layout()
    save(fig, SUB, "hybrid-search-rrf")


def main() -> None:
    apply_style()
    hybrid_search_rrf()


if __name__ == "__main__":
    main()
