import type { Lesson } from "@/lib/types";

/**
 * Pillar L: Calculus. Ordered lesson curriculum per subsection. Lesson order is
 * the array order; prerequisites are bare ids within the same subsection or
 * "subId/lessonId" across subsections.
 *
 * This pillar is the mathematical root of the tree: limits and continuity,
 * single-variable differentiation and integration, Taylor approximation,
 * multivariable and vector calculus, and multivariable optimization, taught
 * from scratch with no prior calculus assumed. It is deliberately upstream of
 * pillar A (whose matrix calculus, optimization theory, and probability
 * densities all assume it). Every lesson has a genuine quantitative surface,
 * so none are codeExempt; runnable numpy checks every result.
 */
export const L_CURRICULUM: Record<string, Lesson[]> = {
  L1: [
    {
      id: "functions-and-graphs",
      title: "Functions, graphs, and the elementary functions",
      goal: "Work fluently with functions, composition, and inverses, and know the graphs and qualitative behavior of polynomials, exponentials, logarithms, and the trig functions.",
      prerequisites: [],
    },
    {
      id: "limits",
      title: "Limits: the idea and the epsilon-delta definition",
      goal: "Compute limits numerically and graphically, then pin the idea down with the epsilon-delta definition and verify one from scratch.",
      prerequisites: ["functions-and-graphs"],
    },
    {
      id: "limit-laws",
      title: "Limit laws and the squeeze theorem",
      goal: "Evaluate limits algebraically with the sum, product, quotient, and composition laws, and trap hard cases like sin(x)/x with the squeeze theorem.",
      prerequisites: ["limits"],
    },
    {
      id: "continuity",
      title: "Continuity and the intermediate value theorem",
      goal: "Define continuity at a point, classify removable, jump, and infinite discontinuities, and use the IVT and extreme value theorem to guarantee roots and extrema exist.",
      prerequisites: ["limit-laws"],
    },
    {
      id: "sequences",
      title: "Sequences and convergence",
      goal: "Define convergence of a sequence, prove limits with the monotone convergence theorem, and recognize geometric decay against harmonic divergence.",
      prerequisites: ["limit-laws"],
    },
    {
      id: "growth-rates",
      title: "Limits at infinity and growth rates",
      goal: "Compare polynomial, exponential, and logarithmic growth with limits at infinity, and read little-o and big-O as statements about limits of ratios.",
      prerequisites: ["sequences"],
    },
  ],
  L2: [
    {
      id: "derivative-definition",
      title: "The derivative as a limit",
      goal: "Define the derivative as the limit of difference quotients, compute one from the definition, and read it as tangent slope and instantaneous rate of change.",
      prerequisites: ["L1/limit-laws"],
    },
    {
      id: "differentiation-rules",
      title: "Power, product, and quotient rules",
      goal: "Derive the power, product, and quotient rules from the limit definition and differentiate any rational combination of the elementary functions.",
      prerequisites: ["derivative-definition"],
    },
    {
      id: "chain-rule",
      title: "The chain rule",
      goal: "Derive the chain rule by composing linear approximations and apply it to nested functions; this is the one rule backpropagation runs on.",
      prerequisites: ["differentiation-rules"],
    },
    {
      id: "implicit-log-differentiation",
      title: "Implicit and logarithmic differentiation",
      goal: "Differentiate relations not given as y = f(x) by implicit differentiation, and tame products and variable powers with the logarithmic trick.",
      prerequisites: ["chain-rule"],
    },
    {
      id: "mvt-lhopital",
      title: "The mean value theorem and L'Hopital's rule",
      goal: "Prove the mean value theorem, read monotonicity off the derivative's sign, and resolve 0/0 and infinity-over-infinity limits with L'Hopital's rule.",
      prerequisites: ["differentiation-rules", "L1/continuity"],
    },
    {
      id: "linearization",
      title: "Linearization and differentials",
      goal: "Replace a function near a point by its tangent line, bound the error of the approximation with the mean value theorem, and see why locally linear is the idea the rest of calculus scales up.",
      prerequisites: ["chain-rule", "mvt-lhopital"],
    },
  ],
  L3: [
    {
      id: "riemann-integral",
      title: "The Riemann integral",
      goal: "Define the definite integral as a limit of Riemann sums, compute one from the definition, and read integrals as signed area and accumulated change.",
      prerequisites: ["L1/continuity", "L1/sequences"],
    },
    {
      id: "fundamental-theorem",
      title: "The fundamental theorem of calculus",
      goal: "Prove both parts of the fundamental theorem, linking accumulation to differentiation, and evaluate definite integrals through antiderivatives.",
      prerequisites: ["riemann-integral", "L2/mvt-lhopital"],
    },
    {
      id: "integration-techniques",
      title: "Substitution and integration by parts",
      goal: "Run the chain rule and product rule in reverse: evaluate integrals by substitution and by parts, and recognize which to reach for.",
      prerequisites: ["fundamental-theorem", "L2/chain-rule"],
    },
    {
      id: "improper-integrals",
      title: "Improper integrals",
      goal: "Extend integration to infinite intervals and unbounded integrands, test convergence by comparison, and meet the Gaussian integral that normalizes the normal density.",
      prerequisites: ["integration-techniques", "L1/growth-rates"],
    },
    {
      id: "taylor-polynomials",
      title: "Taylor polynomials and the remainder",
      goal: "Build the degree-n polynomial matching a function's derivatives at a point, and bound the approximation error with the Lagrange remainder.",
      prerequisites: ["L2/linearization", "fundamental-theorem"],
    },
    {
      id: "power-series",
      title: "Power series and Taylor series",
      goal: "Sum geometric series, find a power series' radius of convergence, and expand exp, log, and sine as the Taylor series numerical libraries evaluate.",
      prerequisites: ["taylor-polynomials", "L1/sequences"],
    },
  ],
  L4: [
    {
      id: "multivariable-functions",
      title: "Functions of several variables",
      goal: "Visualize scalar fields through graphs, level sets, and contour maps, and extend limits and continuity to n dimensions, where approach along every path replaces two-sided approach.",
      prerequisites: ["L1/continuity"],
    },
    {
      id: "partial-derivatives",
      title: "Partial derivatives",
      goal: "Differentiate in one coordinate at a time, compute and interpret partial derivatives, and verify the symmetry of mixed partials (Clairaut's theorem).",
      prerequisites: ["multivariable-functions", "L2/differentiation-rules"],
    },
    {
      id: "gradient-directional",
      title: "The gradient and directional derivatives",
      goal: "Assemble the partials into the gradient, compute directional derivatives as dot products, and prove the gradient points in the direction of steepest ascent, orthogonal to level sets.",
      prerequisites: ["partial-derivatives"],
    },
    {
      id: "total-derivative-chain-rule",
      title: "The total derivative and the multivariable chain rule",
      goal: "Define differentiability as the existence of a best linear map, and compose linear approximations into the multivariable chain rule that backpropagation executes.",
      prerequisites: ["gradient-directional"],
    },
    {
      id: "jacobian",
      title: "The Jacobian matrix",
      goal: "Linearize a vector-valued map with its Jacobian, compose Jacobians by matrix multiplication, and read the determinant as local volume scaling.",
      prerequisites: ["total-derivative-chain-rule", "A1/linear-maps-matrices"],
    },
    {
      id: "hessian",
      title: "The Hessian and second-order approximation",
      goal: "Collect the second partials into the Hessian, write the second-order Taylor expansion in n dimensions, and read curvature from the Hessian's eigenvalues.",
      prerequisites: ["jacobian", "L3/taylor-polynomials"],
    },
  ],
  L5: [
    {
      id: "multiple-integrals",
      title: "Double and triple integrals",
      goal: "Integrate over regions of the plane and space with iterated integrals, justify swapping order with Fubini's theorem, and compute volumes and averages.",
      prerequisites: ["L3/fundamental-theorem", "L4/multivariable-functions"],
    },
    {
      id: "change-of-variables",
      title: "Change of variables and the Jacobian determinant",
      goal: "Transform integrals to polar, cylindrical, and spherical coordinates with the Jacobian determinant, and evaluate the Gaussian integral with the polar trick.",
      prerequisites: ["multiple-integrals", "L4/jacobian"],
    },
    {
      id: "line-integrals",
      title: "Vector fields, line integrals, and potentials",
      goal: "Integrate a vector field along a curve to compute work, characterize conservative fields by path independence, and recover potentials via the gradient theorem.",
      prerequisites: ["L4/gradient-directional", "L3/integration-techniques"],
    },
    {
      id: "divergence-curl",
      title: "Divergence and curl",
      goal: "Define divergence as local flux density and curl as local circulation density, compute both, and identify irrotational and incompressible fields.",
      prerequisites: ["line-integrals"],
    },
    {
      id: "integral-theorems",
      title: "Green, Stokes, and the divergence theorem",
      goal: "Use the three big integral theorems and read them as one statement: the integral of a derivative over a region equals the integral over its boundary.",
      prerequisites: ["divergence-curl", "multiple-integrals"],
    },
  ],
  L6: [
    {
      id: "critical-points",
      title: "Critical points and the second-derivative test",
      goal: "Find interior extrema by setting the gradient to zero, and classify minima, maxima, and saddles from the signs of the Hessian's eigenvalues.",
      prerequisites: ["L4/hessian"],
    },
    {
      id: "convexity",
      title: "Convexity through the Hessian",
      goal: "Define convex functions, test convexity by positive semidefiniteness of the Hessian, and see why convexity turns local minima into global ones.",
      prerequisites: ["critical-points"],
    },
    {
      id: "lagrange-multipliers",
      title: "Constrained optimization and Lagrange multipliers",
      goal: "Derive the condition that the objective's gradient is a multiple of the constraint's gradient from the geometry of tangent level sets, and solve equality-constrained problems by hand.",
      prerequisites: ["critical-points", "L4/gradient-directional"],
    },
    {
      id: "steepest-descent",
      title: "Gradient descent as steepest descent",
      goal: "Derive gradient descent from the first-order Taylor model, choose a step size that provably decreases a smooth function, and watch the iterates run downhill on a real surface.",
      prerequisites: ["convexity"],
    },
    {
      id: "curvature-conditioning",
      title: "Curvature, conditioning, and why optimizers zigzag",
      goal: "Connect the Hessian's eigenvalue spread to the condition number, show why gradient descent zigzags across ill-conditioned ravines, and preview the momentum and second-order fixes.",
      prerequisites: ["steepest-descent"],
    },
    {
      id: "backprop-chain-rule",
      title: "Backpropagation is the chain rule",
      goal: "Express a small network as a composition of maps, multiply Jacobians in reverse order to get every parameter's gradient, and verify the result against finite differences in numpy.",
      prerequisites: ["L4/jacobian", "steepest-descent"],
    },
  ],
};
