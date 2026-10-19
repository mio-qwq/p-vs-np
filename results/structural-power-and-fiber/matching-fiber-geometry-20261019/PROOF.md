# An exact affine criterion for edge-cost matching fibers

19 October 2026. A reusable finite-dimensional lemma, not a new noncancellation theorem. All statements below concern exact level sets of edge-additive costs. They do not turn an arbitrary subset of determinant terms into a binary-color fiber.

## 1. Setup and theorem

Let G=(A,B,E) be a finite bipartite graph with |A|=|B|=n, and write X for the set of its perfect matchings. For M in X, let p_M in {0,1}^E be its edge-incidence vector. Fix a nonempty F subset of X. For an edge cost vector w, define c_w(M)=w dot p_M.

A **complete cost fiber** means that for some t,

    F = {M in X : c_w(M)=t}.

Merely giving the matchings in F equal cost does not establish this equality: every matching outside F must have a different cost.

**Theorem.** The following conditions are equivalent:

1. F is a complete cost fiber for some real edge costs.
2. The only matching incidence vectors in aff{p_M:M in F} are those of F.
3. F is a complete cost fiber for some rational edge costs.
4. F is a complete cost fiber for some integer edge costs.
5. F is a complete cost fiber for some nonnegative integer edge costs.

Here aff is the affine hull over the real numbers. No complexity bound polynomial in the graph encoding is asserted; the statement may quantify over all perfect matchings.

### Proof

Choose M0 in F and set

    D = span{p_M-p_M0 : M in F},
    V = D-perp.

An edge cost is constant on F exactly when w belongs to V. If p_N lies in aff(F), then p_N-p_M0 lies in D. Every w in V therefore has c_w(N)=c_w(M0). This proves necessity of condition 2.

Conversely, assume condition 2. For each N in X\F, the vector v_N=p_N-p_M0 does not belong to D. The functional w -> w dot v_N is consequently nonzero on V: otherwise v_N would lie in (D-perp)-perp=D. Thus

    H_N = {w in V : w dot v_N=0}

is a proper hyperplane of V. A finite union of proper real hyperplanes cannot cover V. A point outside their union gives equal cost precisely on F.

For an exact construction, take an integer basis b_1,...,b_d of V as a real vector space. Such a basis exists because the equations defining V have integer coefficients: perform rational Gaussian elimination and clear each basis vector's denominators. Let q=|X\F|. If q=0, w=0 already works. If q>0, then d>=1. Put

    w(s) = b_1 + s b_2 + ... + s^(d-1) b_d.

For each outside N, the integer polynomial w(s) dot v_N is nonzero and has degree at most d-1. At most q(d-1) real values of s are roots of at least one such polynomial. Therefore some integer s in {0,...,q(d-1)} avoids them all. This gives integer w. The usual convention makes w(0)=b_1, including when d=1.

Finally, choose a nonnegative integer C so that w_e+C>=0 for every edge e. Every perfect matching contains n edges, so replacing all edge costs by w_e+C adds the same nC to every matching cost. It preserves the complete fiber and makes all edge costs nonnegative. This also handles the empty graph case: then the nonempty F is the unique empty matching and w is empty. The remaining implications are immediate. QED.

## 2. Exact obstruction certificates

To disprove real-cost realizability, it is enough to exhibit one N in X\F and rational coefficients alpha_M such that

    p_N = sum_(M in F) alpha_M p_M,
    sum_(M in F) alpha_M = 1.                         (1)

Coefficients may be negative. This is an affine-hull obstruction, not a convex-hull claim. If a 0/1 vector were a convex combination of distinct 0/1 vectors, each coordinate at zero or one would force every participating vector to agree with it; thus a new matching cannot be in their convex hull.

Clearing denominators in (1) gives an entirely integral certificate:

    k p_N = sum_(M in F) b_M p_M,
    k = sum_(M in F) b_M > 0.                         (2)

If all matching costs in F equal t, taking the dot product with w in (2) forces c_w(N)=t.

Equivalently, form the matrix whose rows are p_M-p_M0 for M in F. An outside N is an obstruction exactly when adjoining the row p_N-p_M0 leaves its rational rank unchanged. Integer inputs make rational and real ranks identical. This provides an exact test without a floating-point tolerance.

### A small illustration

On K3,3, permutations list the column chosen in each row. Set

    F = {012, 021, 102, 120, 201},    N=210.

The union of the edges used by F is the entire K3,3. Its six matching incidence vectors satisfy

    p_012 + p_120 + p_201 = p_021 + p_102 + p_210,

since each side is the all-ones 3-by-3 edge matrix. Hence

    p_210 = p_012 + p_120 + p_201 - p_021 - p_102.

The coefficients sum to one, so these five matchings cannot be a complete equal-cost fiber for any real edge costs. This example is only a geometric illustration. It is not a cancellation example: it does not assert that the signed polynomial sum indexed by F vanishes.

## 3. Why the allowed support matters

If the problem supplies a graph G, the test is against X=PM(G), not against permutations that use absent edges.

When a proposed subset F is given without a graph, use its union graph

    E_F = union_(M in F) M,    G_F=(A,B,E_F).

Every graph containing all matchings of F must contain G_F. Consequently an outside matching N in PM(G_F) satisfying (1) excludes realization in **every** graph that contains F. A matching that uses an edge outside E_F cannot establish that conclusion: the edge can simply be omitted.

Conversely, if F passes the affine-closure criterion on G_F, the theorem realizes it by integer nonnegative costs on G_F. This does not assert a binary-color realization.

## 4. Binary costs have a separate condition

A red/blue edge coloring is w in {0,1}^E, and its red-count target is an integer t in [0,n]. In the notation of the proof, the exact binary condition is

    ({0,1}^E intersect V) \ union_(N in X\F) H_N != empty.       (3)

The affine-closure condition remains necessary. The finite-hyperplane avoidance proof establishes sufficiency in the full real vector space V; it does not establish (3) on its finite set of binary points. Rational scaling or adding a common edge cost likewise does not turn general integer costs into 0/1 costs.

Condition (3) is equivalently the feasibility of the exact finite system

    w_e in {0,1} for every e,
    w dot (p_M-p_M0)=0 for every M in F,
    w dot (p_N-p_M0)!=0 for every N in X\F.

### A sharp real-versus-binary boundary in a disjoint-cycle family

Let G_r be the disjoint union of r copies of K2,2, with r>=1. In block j, denote its diagonal matching by A_j and its off-diagonal matching by B_j. Its 2^r perfect matchings independently choose A_j or B_j in each block. Define

    M_A = union_(j=1)^r A_j,
    M_B = union_(j=1)^r B_j,
    F_r = {M_A, M_B}.

**Proposition.** F_r is a complete nonnegative-integer-cost fiber for every r. It is a complete binary-cost fiber if and only if r<=3.

The union of F_r is exactly G_r. The affine line through two distinct 0/1 vectors contains no other 0/1 vector: at a coordinate where they differ, the affine parameter must be zero or one. Thus F_r passes the real-cost criterion for every r.

For r>=2, an explicit nonnegative integer realization assigns cost one to one off-diagonal edge in each of blocks 1,...,r-1, cost r-1 to one diagonal edge in block r, and zero to every other edge. The local cost differences c(B_j)-c(A_j) are

    delta = (1,...,1,-(r-1)).

M_A has cost r-1. Choosing B_j instead on a subset S of the blocks changes its cost by sum_(j in S) delta_j. This sum is zero only for S empty or all r blocks. Thus F_r is exactly the cost-(r-1) fiber. For r=1, all-zero costs suffice, since F_1 contains both matchings of G_1.

No binary edge coloring realizes F_r as a complete fiber when r>=4. For any such coloring, each local difference delta_j belongs to {-2,-1,0,1,2}. Equal cost for M_A and M_B requires sum_j delta_j=0. Exactness requires that no proper nonempty subset of the deltas sum to zero.

If a delta is zero, its singleton subset contradicts exactness. If two deltas are opposites, their two-element subset contradicts exactness. Otherwise positive and negative deltas must both occur. Without opposite pairs, the signs must be exclusively +1 and -2, or exclusively +2 and -1. In the first case, zero total ensures at least two +1 entries and one -2 entry; those three entries sum to zero. In the second case, at least one +2 and two -1 entries likewise give a three-entry zero subsum. Each subset found is proper when r>=4. Hence an extra equal-cost matching is unavoidable under binary costs.

For r=2 and r=3, respectively, the local difference vectors (1,-1) and (1,1,-2) have zero total and no proper nonempty zero subsum. Each is realizable by binary edge weights: realize +1 with one off-diagonal red edge, -1 with one diagonal red edge, and -2 with both diagonal edges red, keeping other edges blue. For r=1 use the zero vector. This proves sharpness within this particular disjoint-cycle family.

The first failure is r=4, with eight vertices on each side and local integer differences (1,1,1,-3). This proves that affine closure is strictly weaker than binary-fiber realizability even on a graph that is precisely the union of F. No globally minimal-size claim is made. It is not a polynomial-cancellation example or an ASNC counterexample.

## 5. Consequence for noncancellation searches

For canonical translated powers, a matching indexed by a permutation sigma contributes

    T_sigma(L) = sgn(sigma) product_i (L+i)^(sigma(i)).

The geometric theorem is independent of these particular polynomials. If a search finds a nonempty subset F with sum_(sigma in F) T_sigma(L)=0, that proves arbitrary-subset cancellation. It refutes binary-color sparse noncancellation only after a graph G, a binary edge coloring w, and a target t have been supplied and checked such that F is the complete target fiber in PM(G). An affine obstruction on G_F rules out that direct realization even for arbitrary real costs. Passing the affine test does not complete the binary obligation.

The separate exact search reports no nonempty cancellation subset among the 24 canonical four-row terms; this note neither depends on that computation nor claims a new candidate from it.

## 6. Local verification

`check.py` is a standard-library exact checker. It checks the six-permutation affine relation, the union-edge condition, rational rank obstruction, and a constructive integer fiber for a small affine-closed example. It also exhaustively verifies the equivalence between affine closure and binary realizability on every subset of the six K3,3 matchings, using all 512 binary edge colorings. That bounded coincidence is only a finite regression test. The r=1,2,3 binary witnesses are checked explicitly. The four-cycle example is checked against its 16 matchings, and all 625 possible local binary cost-difference vectors are checked for the claimed unavoidable proper zero subsum.

Run `python check.py` and `python -O check.py`. Universal statements follow from the proof above, not from the bounded tests. No remote files, PRs, merges, tags, or releases were changed.
