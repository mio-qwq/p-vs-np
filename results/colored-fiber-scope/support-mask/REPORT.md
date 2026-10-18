# When a color-count fiber is a support mask

18 October 2026. Bounded route audit. No ASNC counterexample, general nonvanishing theorem, complexity separation, or historical novelty claim is made.

## Results

1. A nonempty fixed-color-count matching fiber is not generally the perfect-matching set of a binary support mask. The smallest balanced order at which this fails is **3**. The example is the intended brace K3,3 with its diagonal red and target t=1.
2. There is an exact criterion: let U be the union of the fiber's edges. The fiber is representable precisely when the color function on U is a sum of row and column potentials. Equivalently, every alternating cycle relative to one fiber matching has zero color displacement.
3. The smallest example also disproves the manuscript's sliced-polytope vertex identity **with a nonempty fiber**. It does not challenge the nonvanishing assertion: the exact-t polynomial is explicitly nonzero.
4. The previously audited order-at-most-four masked theorem transfers whenever this representability criterion holds and every matching-covered component of U has at most four rows. Extremal fibers satisfy the criterion by the standard assignment-dual argument in the [extremal-transfer note](../extremal-transfer/RESULT.md). Interior fibers need a separate certificate.

These are structural proofs and small certificate checks, not another exhaustive ASNC coloring test. The earlier complete-graph tests through n=4 are not rerun.

## 1. Definitions and the exact criterion

Let G be a finite simple bipartite graph with n vertices in each part, and let c:E(G)->R be an edge cost (the original coloring is the special case c in {0,1}). Suppose

    F = {M in PM(G): c(M)=t}

is nonempty. Let U be the graph whose edges are the union of all M in F. Every edge of U belongs to a perfect matching of U. A representation by a binary mask means equality of matching sets on the original labeled rows and columns. It is not merely a numerical equality between two specialized polynomials.

### Theorem

The following statements are equivalent.

1. There exists a binary mask H with PM(H)=F.
2. PM(U)=F.
3. Every perfect matching of U has cost t.
4. Fix any M0 in F. Every M0-alternating cycle C in U has displacement

       Delta(C)=sum_(e in C\M0) c(e) - sum_(e in C cap M0) c(e)=0.

5. There are real numbers alpha_i and beta_j with c_ij=alpha_i+beta_j for every edge ij in U.
6. conv{P_M:M in F} is a face of the matching polytope of G. Equivalently it is a face of the Birkhoff polytope.

If c is integer valued, integer alpha,beta can be chosen in item 5.

### Proof

**1 iff 2.** Every mask representing F must contain every edge of U. Hence PM(U) is contained in PM(H)=F, while F is contained in PM(U) by definition. Conversely, U itself is a mask if item 2 holds. Adding other edges to a mask cannot repair a failure of U by removing an unwanted matching.

**2 iff 3.** U is a subgraph of G, so the perfect matchings of U with cost t are exactly F.

**3 iff 4.** Flipping any M0-alternating cycle gives a perfect matching of U, proving necessity. Conversely, for any M in PM(U), the symmetric difference M0 triangle M splits into vertex-disjoint M0-alternating cycles. Summing their displacements gives c(M)-c(M0)=0.

**5 implies 3.** Every perfect matching has cost sum_i alpha_i+sum_j beta_j, independently of its chosen edges. Since M0 is in F, that constant is t.

**3 implies 5.** Let X be the average of the permutation matrices in F. Every U-entry of X is strictly positive. Let B be the vertex-edge incidence matrix of U, with a 1 at each endpoint of an edge. For any vector z in ker B, both X+epsilon z and X-epsilon z are nonnegative with all row and column sums equal to one for sufficiently small epsilon>0. The bipartite matching-polytope theorem expresses both as convex combinations of U-perfect matchings. By item 3 their costs are both t, so c dot z=0. Thus c is in (ker B)^perp=im B^T, exactly the row-plus-column potential condition.

Integer potentials, when c is integral, can be constructed component by component: set one potential to zero and propagate the equation alpha_i+beta_j=c_ij along a spanning tree. This gives integer values; consistency on the remaining edges follows from the real solution, since the tree determines all values up to the component's one-dimensional gauge freedom.

**2 iff 6.** The smallest Birkhoff face containing all P_M for M in F is precisely the support face B_U: the average X above is strictly positive on U and zero elsewhere, so it lies in the relative interior of B_U. Hence conv(F) is a Birkhoff face iff it equals B_U, which is equivalent to equality of their permutation vertices. Faces of the matching polytope B_G are exactly its further coordinate-zero support faces, so the relative formulation is equivalent as well.

### Practical scope

Once U is known, item 5 can be checked by spanning-forest propagation and a check of each remaining edge, using exact arithmetic for binary colors. However, producing U requires knowing which edges occur in exact-t matchings. This criterion is not itself a new polynomial-time algorithm for determining arbitrary exact-t fibers.

## 2. The smallest-order obstruction: an intended brace

Take G=K3,3 with rho(i,j)=1 exactly when i=j. Its permutation costs are their numbers of fixed points:

- The identity has cost 3.
- The three transpositions have cost 1.
- The two 3-cycles have cost 0.

At t=1 the nonempty fiber consists of exactly the three transpositions. Every one of the nine edges belongs to exactly one of these three matchings. Therefore U=K3,3. Any mask containing the fiber contains all nine edges, and necessarily admits the identity and the two 3-cycles as well. It cannot represent the fiber.

The potential criterion fails on the 2x2 rectangle using rows/columns 0,1:

    rho00+rho11=2, whereas rho01+rho10=0.

For M0=(01), switching that alternating 4-cycle changes its count from 1 to 3. Some edges of that cycle come from other fiber matchings; the cycle need not belong to the union of M0 and one other fiber matching.

### Why the intended ASNC assumptions do not avoid this example

K3,3 is connected and matching-covered, and every matching of size at most two extends to a perfect matching. For the standard applicable Hall+2 range 1<=|S|<=n-2, its only case here is |S|=1, where |N(S)|=3=|S|+2. Thus this is a brace under the intended 2-extendability interpretation used in the source.

The previously documented source typo remains relevant: its literal Hall+2 quantifier includes |S|=n-1, which no balanced graph of order n>=2 can satisfy. We do not use that impossible literal definition to assert either an in-scope counterexample or a way around the obstruction.

### It is not an ASNC counterexample

For the original labels a_i=i and exponents e_j=j, writing lambda for the polynomial variable,

    P1(lambda)
      = -[(lambda+1)^2(lambda+2)
          +lambda(lambda+2)^2+lambda^2(lambda+1)]
      = -3 lambda^3-9 lambda^2-9 lambda-2,

which is nonzero. All three permutations have the same negative sign, so their monic degree-three products cannot cancel.

By contrast, the determinant of the forced union mask is the full uncolored Vandermonde determinant, equal to 2. This illustrates exactly why nonvanishing of the union-mask determinant does not by itself prove nonvanishing of the selected coefficient.

There is also no accidental polynomial representation by some other 3x3 binary mask with the same offsets and exponents. The fiber's leading coefficient is -3. Every such masked determinant has leading coefficient det(eta), which for a binary 3x3 matrix has absolute value at most 2. For a short proof of this bound, a Leibniz sum can have magnitude at most 3. Equality would require all three terms of one parity to be present and all three of the other parity absent. But the three same-parity permutation supports together cover all nine entries, forcing the entire mask and all six terms to be present, a contradiction. This argument also works with arbitrary row offsets and nonnegative column exponents: all permutation products remain monic of the same degree. It excludes exact equality, without allowing auxiliary variables, extra vertices, arbitrary scalar weights, or additional polynomial operations.

### Pairwise closure does not repair the reduction

Each pair of the three transpositions differs on a single alternating 6-cycle. Their union has exactly those two perfect matchings, so the fiber is closed under every matching recombination supported on a pair of its members. Nevertheless its three-member union leaks other matchings. Thus pairwise recombination closure is strictly weaker than the theorem's full support-union closure. The manuscript's valid affine/parallelogram completion implication is not contradicted or strengthened into support closure by this example.

## 3. Exact minimality, with two size conventions

### Minimum balanced order: n=3, with nine support edges

For n=1 there is at most one matching. For n=2 every nonempty matching family is either a singleton (represented by that matching) or both permutations (represented by their union). Hence no failure occurs below n=3.

At n=3, even arbitrary matching families supported by a proper subgraph of K3,3 are representable. To see this, choose a missing edge and permute its endpoints to (0,0). The four permutations avoiding (0,0), written as their column tuples, are

    A=(1,0,2), B=(1,2,0), C=(2,0,1), D=(2,1,0).

They respectively have the private edges

    (2,2), (1,2), (2,1), (1,1).

Each private edge occurs in only its indicated matching among A,B,C,D. If a chosen family omits a matching, its private edge is absent from the union, preventing that matching from leaking back in. This proves representability for every proper support. Therefore the nine-edge example is also support-minimal at the smallest order.

No family of at most two matchings at n=3 can fail: two distinct permutations differ on exactly one alternating cycle, so their union has just those two matchings. The three-transposition example has the minimum possible fiber size at this order.

### Minimum number of support edges over all orders: eight

If size is measured solely by total support edges while the order can vary, there is a different minimum. Take the disjoint union of two K2,2 blocks, color each block's diagonal red and its off-diagonal blue, and set t=2. The fiber consists of the two matchings that choose the red diagonal in one block and the blue off-diagonal in the other. Their union has all eight block edges, and also supports the counts 0 and 4. This is a two-matching nonrepresentable fiber at n=4. This graph is disconnected, so it is not being used as a brace example.

For a proof that seven edges cannot suffice, work in the allowed graph U. A degree-one vertex forces its matched edge into every perfect matching. Its partner then has no other allowed incident edge, so this component is an isolated matched edge. Remove all such components. Every vertex in the remaining graph has degree at least two. If q rows remain, there are at least 2q edges, so a graph with at most seven total edges has q<=3. The remaining graph has either a single 2-row component, or a proper 3-row support, or is empty; two nontrivial components would require at least four rows. The preceding small-order argument makes every subfamily representable in these cases. Reattaching the forced isolated edges cannot create leakage. Thus eight is the exact global support-edge minimum.

## 4. A nonempty-fiber failure of the sliced-polytope identity

Keep the K3,3 diagonal-red example. Let Q be the permutation matrix of the 3-cycle (0->1,1->2,2->0), and set

    X=(I+2Q)/3
     = [[1/3,2/3,0], [0,1/3,2/3], [2/3,0,1/3]].

X is doubly stochastic and has diagonal sum one. Its support, I union Q, is a single alternating 6-cycle and has exactly the two perfect matchings I and Q. Thus its Birkhoff support face is the edge [I,Q]. The red-count hyperplane intersects that edge only at X, because the endpoint counts are 3 and 0. This singleton is a face of the sliced polytope: intersect the slice with the same coordinate-zero supporting hyperplanes defining [I,Q]. Therefore X is a vertex of B3 intersect H1, and it is fractional.

Yet F1 is nonempty, consisting of the three transpositions. None of these is supported on I union Q, so X is not even in conv(F1). This refutes the source's Theorem 2.7(iii) also when its fiber is nonempty. It does not refute its valid equality identifying the integral permutation points of the slice, the parallelogram corollary, or ASNC.

## 5. What the masked theorem can legitimately transfer

If the equivalent criteria in Section 1 hold, there is an exact identity, preserving all labels and signs,

    sum_(M in F) sign(M) product_i (x+a_i)^(e_M(i))
      = det[1_(ij in U) (x+a_i)^e_j].

For distinct real a_i and distinct nonnegative integer e_j, the audited order-at-most-four theorem proves the right-hand side nonzero whenever every connected component of U has at most four rows. Each component is balanced, and row/column permutation gives a product of nonzero block determinants up to a fixed sign.

As derived in the [extremal-transfer note](../extremal-transfer/RESULT.md), minimum-cost and maximum-cost fibers always satisfy the criterion: optimal assignment dual potentials are tight on every edge used by an optimal matching. This exact transfer and its component-size corollary are sound. Extremality is sufficient, not necessary. For example, in K3,3 color just (0,0),(1,1) red. The target t=1 is interior between attainable counts 0 and 2, yet its two matchings differ on one 6-cycle, so their union represents that fiber.

For the interior diagonal-red target above, the required support representation fails even at n=3 on a brace. Therefore repairing or extending an uncolored masked determinant lemma cannot, on its own, settle all colored coefficients. This note does not claim that the original manuscript explicitly relies on this particular direct reduction; it audits a proposed route from the auxiliary theorem to ASNC.

The source's Theorem 2.10 already claims nonvanishing for every nonempty subset of S_n at n<=4 with the original consecutive integer offsets and exponents. Accordingly, the original-label small-order extremal corollary is not presented here as a new result. The audited auxiliary theorem has the different, more general parameter scope of arbitrary distinct real offsets and arbitrary distinct nonnegative integer exponent gaps. This route audit makes no historical novelty claim for either the standard polytope facts or their applications.

## Sources, checks, and boundaries

- Primary source: Yuefeng Du, arXiv:2604.01571v3, Sections 1.2, 2.1-2.4 and 3.1. The audit used a locally preserved source text. [Section 2.4](https://arxiv.org/html/2604.01571v3#S2.SS4) and [Section 3.1](https://arxiv.org/html/2604.01571v3#S3.SS1).
- Auxiliary theorem: [frozen arbitrary-gap order-four proof at the dependency commit](https://github.com/mio-qwq/p-vs-np/blob/94d094d82d14e15729cac0b478d0d6f1bec33de9/results/monic-four-general/PROOF.md). Its [audit status](https://github.com/mio-qwq/p-vs-np/blob/94d094d82d14e15729cac0b478d0d6f1bec33de9/results/monic-four-general/STATUS.json) is separate from the proof's original candidate label. The dependency is not re-proved by this package.
- [Extremal transfer](../extremal-transfer/RESULT.md): assignment-dual proof and component factorization.
- Exact certificate: `check.py` uses only Python's standard library and integer/rational arithmetic. It verifies the examples, private-edge minimality certificate, positive and negative potential certificates, intended brace extension condition, fractional slice vertex certificate, and displayed polynomial. Its complete output certificates are in `results.json`. It does not numerically test arbitrary offsets or exponent sets.

The support and geometric arguments are structural proofs with small exact certificates. They do not rerun the prior complete-graph ASNC enumeration. This is an AI-assisted research audit, not human peer review, Lean verification, or another proof-assistant certification. No ASNC, P-versus-NP, or historical novelty claim is made.
