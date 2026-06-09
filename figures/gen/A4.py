"""Figures for pillar A4 (numerical linear algebra). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, HOT, apply_style, color, save

SUB = "A4"
C = color(SUB)  # pillar-A accent (gold)


def conditioning_stability() -> None:
    """Solving Ax = b in float64: the relative error grows like the condition
    number κ — it tracks the κ·ε bound, so κ = 10¹² loses ~12 of 16 digits.

    Reuses the lesson's matrix builder: random orthogonal U, V and geometrically
    spaced singular values from 1 down to 1/κ (rng(0), n = 50)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    eps = np.finfo(float).eps
    n = 50

    def make_A(kappa):
        U = np.linalg.qr(rng.normal(size=(n, n)))[0]
        V = np.linalg.qr(rng.normal(size=(n, n)))[0]
        s = np.geomspace(1.0, 1.0 / kappa, n)
        return U @ np.diag(s) @ V.T

    kappas = np.geomspace(1e0, 1e15, 31)
    errors = []
    x_true = np.ones(n)
    # κ up to 1e15 deliberately drives nearly-singular solves; the FP flags that
    # raises are the phenomenon under study, not a code bug — silence them.
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        for kappa in kappas:
            A = make_A(kappa)
            b = A @ x_true
            x_hat = np.linalg.solve(A, b)
            errors.append(np.linalg.norm(x_hat - x_true) / np.linalg.norm(x_true))
    errors = np.array(errors)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(kappas, np.clip(errors, eps, None), "-o", color=C, ms=4,
              label="measured relative error")
    ax.loglog(kappas, kappas * eps, color=HOT, ls="--", lw=1.8,
              label=r"bound  $\kappa \cdot \varepsilon_{\mathrm{mach}}$")
    ax.axhline(1.0, color=FG_MUTE, ls=":", lw=1.2, label="no correct digits")
    ax.set_title("Error amplification by the condition number")
    ax.set_xlabel(r"condition number $\kappa(A)$")
    ax.set_ylabel("relative error of the solution")
    ax.set_ylim(1e-17, 10)
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, SUB, "conditioning-stability")


def main() -> None:
    apply_style()
    conditioning_stability()


if __name__ == "__main__":
    main()
