# Extremal color fibers and the audited masked determinant theorem

18 October 2026. Extremal-fiber transfer. Standard assignment-polytope reasoning applied to the audited order-four theorem; no historical novelty claim, no general ASNC or P versus NP conclusion.

Let G be a finite bipartite graph with n vertices in each part, admitting a perfect matching. Assign real edge costs c_ij, distinct real row offsets a_i, and distinct nonnegative integer column exponents e_j. For a matching permutation pi write w_pi(x)=sign(pi) product_i (x+a_i)^(e_pi(i)). Let m be the minimum total matching cost and E_min the union of edges appearing in minimum-cost perfect matchings.

## Exact transfer

The perfect matchings of (V,E_min) are exactly the minimum-cost perfect matchings of G. Consequently their signed polynomial sum is exactly det[1_(ij in E_min)(x+a_i)^e_j]. The same statement holds for maximum-cost matchings, by replacing c with -c.

Proof: the assignment linear program has constraints X>=0, row sums and column sums equal to one, with forbidden entries omitted. Its feasible polytope is the bipartite perfect-matching polytope and is integral. A dual optimum supplies row and column potentials u_i,v_j with u_i+v_j<=c_ij and sum u_i+sum v_j=m. Every minimum matching has total slack zero. All edge slacks are nonnegative, hence every edge of E_min is tight. Every perfect matching using E_min therefore has cost sum u_i+sum v_j=m. The reverse inclusion is by definition. This proves equality of permutation sets, with no alteration of signs or row/column labels.

For binary red/blue costs, define P_t(x)=[z^t] det[eta_ij z^c_ij (x+a_i)^e_j]. The result applies to the smallest and largest feasible red counts t. For every n<=4, the audited masked determinant theorem (and its lower-order dependencies) proves these two polynomials nonzero, for arbitrary distinct real offsets and arbitrary distinct nonnegative integer exponents.

More generally, for any n, suppose each connected component of E_min has at most four vertices in each part. Each component is balanced because every edge belongs to an optimal perfect matching and a perfect matching covers each component separately. Permuting rows and columns puts the support in diagonal blocks. The determinant is the product of their determinants, up to a fixed sign. Each factor is nonzero by the order-at-most-four theorem, hence their product is nonzero in R[x]. The identical statement applies to E_max.

## Boundary

This does not cover a prescribed interior red count. A fiber need not be a face of the matching polytope, and taking its union of edges can introduce matchings of other costs. Nonvanishing of the determinant of that union cannot then establish nonvanishing of the individual coefficient P_t. A cycle-balance/face certificate would be required for that transfer. No polynomial-time test of all interior targets, and no arbitrary-order masked determinant theorem, has been established here.

The support-union and extremal-face step is standard linear programming. The determinant input is the [audited arbitrary-gap order-four theorem](https://github.com/mio-qwq/p-vs-np/blob/94d094d82d14e15729cac0b478d0d6f1bec33de9/results/monic-four-general/PROOF.md) at commit 94d094d82d14e15729cac0b478d0d6f1bec33de9. This note is a route clarification, not a new breakthrough.
