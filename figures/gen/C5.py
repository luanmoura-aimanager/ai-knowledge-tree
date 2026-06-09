"""Figures for pillar C5 (clustering). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, CYCLE, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "C5"
C = color(SUB)  # pillar-C accent

CLUSTER_COLS = [ACCENT, HOT, GOOD, "#bb9af7", "#e0af68"]


def _three_blobs(rng, n_per=100, scale=0.5):
    centers = np.array([[2.0, 0.0], [-2.0, 0.0], [0.0, 2.0]])
    X = np.vstack([rng.normal(c, scale, (n_per, 2)) for c in centers])
    return X


def kmeans() -> None:
    """k-means on three blobs: the assignment+update loop (Lloyd's algorithm)
    drives the inertia down to a fixed point. rng(0), k=3."""
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

    rng = np.random.default_rng(0)
    X = _three_blobs(rng)
    km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    for c in range(3):
        ax1.scatter(X[km.labels_ == c, 0], X[km.labels_ == c, 1], s=14,
                    color=CLUSTER_COLS[c], edgecolor="none")
    ax1.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=180,
                marker="*", color="#ffffff", edgecolor=GRID, linewidth=1.0, zorder=5)
    ax1.set_title("Final clusters and centroids")
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")

    # inertia vs iteration (run with max_iter=t, capturing the descent)
    inertias = []
    for t in range(1, 11):
        kt = KMeans(n_clusters=3, n_init=1, max_iter=t, init="random",
                    random_state=2).fit(X)
        inertias.append(kt.inertia_)
    ax2.plot(range(1, 11), inertias, "-o", color=C, ms=5)
    ax2.set_title("Inertia decreases each iteration")
    ax2.set_xlabel("Lloyd iteration")
    ax2.set_ylabel("inertia (within-cluster SS)")
    fig.tight_layout()
    save(fig, SUB, "kmeans")


def kmeans_init_and_k() -> None:
    """Choosing k: the inertia 'elbow' and the silhouette peak both point to the
    true k=3 on three blobs. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    rng = np.random.default_rng(0)
    X = _three_blobs(rng, n_per=120)

    ks = list(range(1, 8))
    inertia = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_ for k in ks]
    ksil = list(range(2, 8))
    sil = []
    for k in ksil:
        lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
        sil.append(silhouette_score(X, lab))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.plot(ks, inertia, "-o", color=C, ms=5)
    ax1.axvline(3, color=FG_MUTE, ls=":", lw=1.4)
    ax1.set_title("Elbow: inertia vs k")
    ax1.set_xlabel("number of clusters $k$")
    ax1.set_ylabel("inertia")

    ax2.plot(ksil, sil, "-o", color=HOT, ms=5)
    ax2.axvline(3, color=FG_MUTE, ls=":", lw=1.4, label="true k = 3")
    ax2.set_title("Silhouette vs k")
    ax2.set_xlabel("number of clusters $k$")
    ax2.set_ylabel("mean silhouette")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "kmeans-init-and-k")


def _cov_ellipse(ax, mean, cov, color, nstd=2.0):
    from matplotlib.patches import Ellipse

    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    angle = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    w, h = 2 * nstd * np.sqrt(vals)
    e = Ellipse(mean, w, h, angle=angle, facecolor="none", edgecolor=color, lw=2.2)
    ax.add_patch(e)


def gmm_em() -> None:
    """A Gaussian mixture fit by EM: soft responsibilities (right) assign each
    point partially to every component, and the fitted covariance ellipses (left)
    capture the elliptical, overlapping clusters a hard k-means would miss. K=3,
    rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.mixture import GaussianMixture

    rng = np.random.default_rng(0)
    mus = [np.array([2.0, 0.0]), np.array([-2.0, 0.0]), np.array([0.0, 2.0])]
    covs = [np.array([[0.6, 0.5], [0.5, 0.6]]),
            np.array([[0.6, -0.45], [-0.45, 0.6]]),
            np.array([[1.0, 0.0], [0.0, 0.25]])]
    pis = [0.4, 0.4, 0.2]
    n = 500
    counts = rng.multinomial(n, pis)
    X = np.vstack([rng.multivariate_normal(m, c, k)
                   for m, c, k in zip(mus, covs, counts)])
    gm = GaussianMixture(n_components=3, covariance_type="full", random_state=0).fit(X)
    resp = gm.predict_proba(X)
    lab = resp.argmax(1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9),
                                   gridspec_kw={"width_ratios": [1.1, 1]})
    for c in range(3):
        ax1.scatter(X[lab == c, 0], X[lab == c, 1], s=10, color=CLUSTER_COLS[c],
                    edgecolor="none", alpha=0.6)
        _cov_ellipse(ax1, gm.means_[c], gm.covariances_[c], CLUSTER_COLS[c])
    ax1.set_title("Fitted Gaussian components")
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")

    order = np.argsort(lab)
    im = ax2.imshow(resp[order], aspect="auto", cmap="magma", vmin=0, vmax=1)
    ax2.set_title("Responsibilities (soft assignment)")
    ax2.set_xlabel("component")
    ax2.set_ylabel("points (sorted by cluster)")
    ax2.set_xticks([0, 1, 2])
    cb = fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_MUTE)
    cb.outline.set_edgecolor(GRID)
    fig.tight_layout()
    save(fig, SUB, "gmm-em")


def hierarchical_clustering() -> None:
    """Agglomerative (Ward) clustering builds a dendrogram; cutting it at a chosen
    height yields the clusters — here a cut gives the three blobs. rng(0), 60 points."""
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram, linkage

    rng = np.random.default_rng(0)
    X = _three_blobs(rng, n_per=20, scale=0.4)
    Z = linkage(X, method="ward")
    cut = 0.5 * (Z[-3, 2] + Z[-2, 2])  # between the 3→2 and 2→1 merges

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    dendrogram(Z, ax=ax, color_threshold=cut, no_labels=True,
               above_threshold_color=FG_MUTE)
    ax.axhline(cut, color=HOT, ls="--", lw=1.6, label="cut → 3 clusters")
    ax.set_title("Hierarchical clustering dendrogram (Ward)")
    ax.set_xlabel("points")
    ax.set_ylabel("merge distance")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "hierarchical-clustering")


def dbscan() -> None:
    """DBSCAN finds density-connected clusters of any shape and labels sparse
    points as noise. The k-distance plot (left) has an elbow that sets eps; the
    result (right) recovers the two moons with a handful of noise points. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.cluster import DBSCAN
    from sklearn.datasets import make_moons
    from sklearn.neighbors import NearestNeighbors

    X, _ = make_moons(n_samples=300, noise=0.08, random_state=0)
    rng = np.random.default_rng(0)
    X = np.vstack([X, rng.uniform([-1.5, -1], [2.5, 1.5], (20, 2))])  # noise

    min_pts = 5
    nn = NearestNeighbors(n_neighbors=min_pts).fit(X)
    kd = np.sort(nn.kneighbors(X)[0][:, -1])
    eps = 0.18
    db = DBSCAN(eps=eps, min_samples=min_pts).fit(X)
    lab = db.labels_

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.plot(kd, color=C, lw=2.2)
    ax1.axhline(eps, color=HOT, ls="--", lw=1.4, label=f"eps = {eps}")
    ax1.set_title(f"{min_pts}-distance plot (elbow → eps)")
    ax1.set_xlabel("points sorted by distance")
    ax1.set_ylabel(f"distance to {min_pts}th neighbor")
    ax1.legend(loc="upper left")

    for c in sorted(set(lab)):
        m = lab == c
        if c == -1:
            ax2.scatter(X[m, 0], X[m, 1], s=14, color=FG_MUTE, marker="x",
                        label="noise")
        else:
            ax2.scatter(X[m, 0], X[m, 1], s=14, color=CLUSTER_COLS[c], edgecolor="none")
    ax2.set_title("DBSCAN clusters + noise")
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "dbscan")


def tsne_umap() -> None:
    """t-SNE lays out high-dimensional clusters in 2D by preserving local
    neighborhoods; here three 5-D Gaussian blobs separate cleanly, much as a
    linear PCA projection does on this easy case. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE

    rng = np.random.default_rng(0)
    centers = [np.array([5, 0, 0, 0, 0]), np.array([-5, 0, 0, 0, 0]),
               np.array([0, 5, 0, 0, 0])]
    npc = 60
    X = np.vstack([rng.normal(c, 1.0, (npc, 5)) for c in centers])
    y = np.array([0] * npc + [1] * npc + [2] * npc)

    emb = TSNE(n_components=2, perplexity=20, random_state=0, init="pca").fit_transform(X)
    pca = PCA(n_components=2).fit_transform(X)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    for ax, Z, ttl in [(ax1, emb, "t-SNE embedding"), (ax2, pca, "PCA projection")]:
        for c in range(3):
            ax.scatter(Z[y == c, 0], Z[y == c, 1], s=14, color=CLUSTER_COLS[c],
                       edgecolor="none")
        ax.set_title(ttl)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, SUB, "tsne-umap")


def main() -> None:
    apply_style()
    kmeans()
    kmeans_init_and_k()
    gmm_em()
    hierarchical_clustering()
    dbscan()
    tsne_umap()


if __name__ == "__main__":
    main()
