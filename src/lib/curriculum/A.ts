import type { Lesson } from "@/lib/types";

/**
 * Pillar A: Foundations. Ordered lesson curriculum per subsection (discipline).
 * Lesson order is the array order; prerequisites are bare ids within the same
 * subsection or "subId/lessonId" across subsections.
 */
export const A_CURRICULUM: Record<string, Lesson[]> = {
  A1: [
    {
      id: "vector-spaces",
      title: "Vector spaces & subspaces",
      goal: "Define a vector space and a subspace from the axioms, and see why closure under linear combination is the only property we ever use.",
    },
    {
      id: "basis-dimension",
      title: "Span, independence, basis, dimension",
      goal: "Build span and linear independence into the notion of a basis, prove that dimension is well defined, and read off coordinates.",
      prerequisites: ["vector-spaces"],
    },
    {
      id: "linear-maps-matrices",
      title: "Linear maps and matrices",
      goal: "Show every linear map between finite-dimensional spaces is a matrix once bases are fixed, and that composition is matrix multiplication.",
      prerequisites: ["basis-dimension"],
    },
    {
      id: "rank-nullity",
      title: "Rank, nullity, and the four fundamental subspaces",
      goal: "Prove the rank–nullity theorem and use the column/null/row/left-null spaces to decide when Ax=b is solvable.",
      prerequisites: ["linear-maps-matrices"],
    },
    {
      id: "norms",
      title: "Norms and the geometry of distance",
      goal: "Define norms via their three axioms, meet the p-norms, and connect L1/L2 to sparsity and Euclidean length.",
      prerequisites: ["vector-spaces"],
    },
    {
      id: "inner-products",
      title: "Inner products, orthogonality, Cauchy–Schwarz",
      goal: "Define the inner product, prove the Cauchy–Schwarz inequality, and derive angle and orthogonality from it.",
      prerequisites: ["norms"],
    },
    {
      id: "gram-schmidt",
      title: "Orthonormal bases & Gram–Schmidt",
      goal: "Construct an orthonormal basis by Gram–Schmidt, prove orthogonal matrices are isometries, and connect to the QR factorization.",
      prerequisites: ["inner-products", "basis-dimension"],
    },
    {
      id: "determinants",
      title: "Determinants and volume",
      goal: "Define the determinant as a signed volume scaling, derive its key properties, and tie det=0 to singularity.",
      prerequisites: ["linear-maps-matrices"],
    },
    {
      id: "eigenvalues",
      title: "Eigenvalues & eigenvectors",
      goal: "Define eigenpairs, find them through the characteristic polynomial, and interpret them as invariant scaling directions.",
      prerequisites: ["determinants"],
    },
    {
      id: "spectral-theorem",
      title: "Diagonalization & the spectral theorem",
      goal: "Prove that real symmetric matrices have real eigenvalues and an orthonormal eigenbasis, giving A = QΛQᵀ.",
      prerequisites: ["eigenvalues", "gram-schmidt"],
    },
    {
      id: "quadratic-forms",
      title: "Quadratic forms & positive definiteness",
      goal: "Read a quadratic form through the spectrum of its matrix, and use eigenvalue signs to test positive (semi)definiteness.",
      prerequisites: ["spectral-theorem"],
    },
    {
      id: "svd",
      title: "Singular value decomposition",
      goal: "Construct the SVD of any matrix from the spectral theorem applied to AᵀA, and read it as rotate–scale–rotate.",
      prerequisites: ["spectral-theorem"],
    },
    {
      id: "low-rank-pca",
      title: "Low-rank approximation (Eckart–Young) & PCA",
      goal: "Prove the truncated SVD is the best low-rank approximation, and identify PCA as the SVD of the centered data matrix.",
      prerequisites: ["svd"],
    },
    {
      id: "factorizations",
      title: "LU, QR, and Cholesky factorizations",
      goal: "See how LU, QR, and Cholesky each solve linear systems by structure, and why we factor instead of inverting.",
      prerequisites: ["gram-schmidt", "quadratic-forms"],
    },
    {
      id: "least-squares",
      title: "Least squares & the Moore–Penrose pseudo-inverse",
      goal: "Derive the normal equations from the residual, interpret the solution as a projection, and build the pseudo-inverse from the SVD.",
      prerequisites: ["svd", "factorizations"],
    },
    {
      id: "matrix-calculus",
      title: "Matrix calculus & the chain rule",
      goal: "Fix a layout convention, derive the gradients of the linear, quadratic, and affine forms, and compose them into backprop.",
      prerequisites: ["linear-maps-matrices"],
    },
    {
      id: "tensors-einsum",
      title: "Tensors & einsum",
      goal: "Generalize to higher-order tensors with index notation and the Einstein summation convention behind einsum.",
      prerequisites: ["matrix-calculus"],
    },
  ],
  A2: [],
  A3: [],
  A4: [],
  A5: [],
};
