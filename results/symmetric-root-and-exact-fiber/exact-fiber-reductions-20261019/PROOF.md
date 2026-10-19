# Exact Matching and completeness of a nonempty explicitly listed binary fiber

19 October 2026. Local mathematical result; no repository, PR, release, or remote state is changed.

## 1. Result and precise scope

Let **BEM** be bipartite Exact Matching: the input is a simple bipartite graph G=(A,B,E), |A|=|B|=n, a binary edge coloring c, and an integer k; decide whether G has a perfect matching with exactly k red edges.

Let **COMP** be fixed-color fiber completeness: the input is a simple bipartite graph H, a specified binary coloring w, an integer T, and an explicitly listed nonempty family F of distinct valid perfect matchings, all of cost T; decide whether F is exactly the set of cost-T perfect matchings of H. Its complement on these well-formed inputs is **EXTRA**: an unlisted cost-T perfect matching exists.

**Theorem.** There is a deterministic polynomial-time many-one reduction BEM <=_m EXTRA, even when F consists of one explicitly known matching. Equivalently, complement-BEM <=_m COMP for singleton F. The construction is count preserving up to one: the target fiber contains exactly one known dummy matching plus one distinct matching for each solution to the original BEM instance.

Conversely, EXTRA for arbitrary nonempty explicit F has a deterministic polynomial-time Turing reduction to BEM, using polynomially many nonadaptive exact-count queries after elementary validity checks. Thus these decision problems are polynomial-time Turing equivalent. The construction below does **not** establish two-way many-one equivalence.

In particular a deterministic polynomial-time general fixed-color completeness verifier would yield a deterministic polynomial-time algorithm for bipartite Exact Matching, and such an Exact Matching algorithm would yield a deterministic polynomial-time verifier. These are equivalences of algorithmic tasks, not a claim that either algorithm currently exists or that either problem is NP-hard.

The result is specifically about verifying a **supplied coloring**. For singleton F, finding some binary coloring that realizes F is already trivial: color exactly its edges red and use target equal to the number of vertices on one side. Consequently this reduction provides no hardness result for binary-fiber **synthesis**.

## 2. A two-state binary path

For an integer q>=2, replace an edge between an old left vertex a and an old right vertex b by a fresh path of odd length 2q-1. Write its successive edges as e_1,...,e_(2q-1). Color odd-indexed edges red and even-indexed edges blue. Every internal vertex is new and has degree two.

In any perfect matching of a larger graph containing this path, exactly two local states are possible:

* **Selected:** all odd-indexed edges are used, both old endpoints are covered by the path, and the red cost is q.
* **Unselected:** all even-indexed edges are used, neither old endpoint is covered by the path, and the red cost is zero.

To prove this, examine the first internal vertex. Its match to the first old endpoint forces the selected alternating pattern along the entire path; its match to the next internal vertex forces the unselected pattern. This accounts for every possibility. Equivalently, covering exactly one old endpoint would leave an odd number of remaining internal vertices.

The gadget has q-1 new left vertices, q-1 new right vertices, and 2q-1 edges. It is a unary implementation of a nonnegative weight q, so its size must be counted. All q used below are O(n), which makes this implementation polynomial.

## 3. Constructing the known dummy and the original solutions

First suppose n>=1 and 0<=k<=n. Index the old vertices as A={a_1,...,a_n} and B={b_1,...,b_n}, and put

    C=n+1,       q_e=C+c(e),       T=Cn+k.

Build H_0 as follows.

1. Replace each original edge e by the path from Section 2 with parameter q_e, using mutually disjoint internal vertices.
2. Add a direct blue edge a_i b_i for every i, whether or not that pair was an edge of G.

The result is simple: all original edges have become paths of length at least three, so none is a direct edge between two old vertices. In particular an original diagonal edge does not collide with its newly added dummy edge.

For any perfect matching of H_0, let J be the set of original edges whose paths are selected, p=|J|, and r=sum_(e in J)c(e). Then J is a partial matching of G, and

    cost(H_0 matching)=Cp+r,       0<=r<=p<=n.

The remaining old vertices must use their blue diagonal edges. Therefore the index set of old left vertices covered by J equals the index set of old right vertices covered by J. This extra restriction on partial matchings causes no problem: when p=n, J is precisely an arbitrary perfect matching of G, with no further restriction. All path states and direct dummy edges are forced by J.

There is exactly one matching D_0 with p=0: use every direct blue diagonal and every unselected path state. Its cost is zero. Every p>=1 has positive cost. Every p<n satisfies

    Cp+r <= C(n-1)+(n-1) = Cn-2 < T.

Every p=n has cost Cn+r, so it has cost T exactly when J is an original k-red perfect matching.

Now form H as the disjoint union of H_0 and a simple cycle on 2T vertices. This is possible because T>=2. Give the cycle its alternating perfect matchings R and Z, coloring every edge of R red and every edge of Z blue. These are exactly its two perfect matchings, of costs T and zero.

Supply the singleton family

    F={D},       D=D_0 union R,

and use target T. This known valid matching has exactly T red edges, regardless of whether the original graph has any perfect matching.

### Complete target-fiber classification

Every perfect matching of H is a matching of H_0 together with either R or Z.

* With R, total cost is T+Cp+r. Equality with T forces p=0 and hence gives exactly D.
* With Z, total cost is Cp+r. If p<n the strict inequality above rules out T. If p=n, equality with T is equivalent to r=k, so J is exactly an original BEM solution.

For each original solution J, choose selected paths for its edges, unselected paths for all other original edges, no direct dummy diagonals, and Z on the cycle. This is a uniquely specified cost-T matching, different from D. Conversely every target matching different from D has exactly this form. The maps are mutually inverse.

Thus

    |{M in PM(H): w(M)=T}| = 1 + |{J in PM(G): c(J)=k}|.

In particular G has a k-red perfect matching if and only if the supplied nonempty family F is incomplete. This is the asserted many-one reduction.

## 4. Size and exceptional inputs

Let m=|E| and R_G be the number of red original edges. The number N of vertices on either side of H is exactly

    N = n + sum_e(q_e-1) + T
      = n + mn + R_G + n(n+1) + k.

The total number of edges is exactly

    |E(H)| = sum_e(2q_e-1) + n + 2T
           = m(2n+1) + 2R_G + n + 2[n(n+1)+k].

Both are O(nm+n^2); target T is O(n^2); every edge is binary colored. The singleton dummy matching is listed explicitly using N edges. The construction and both solution maps take time polynomial in these sizes. No exponentially large weights are hidden in a path expansion.

For n>=1 but k outside [0,n], BEM is immediately false, so output a fixed complete instance: one blue edge, target zero, and its sole perfect matching as F. For n=0, the unique original matching is empty and has red count zero. If k=0, output a fixed incomplete instance: K_2,2 with all edges blue, target zero, and just one of its two perfect matchings listed as F. Otherwise output the fixed complete instance. This extends the reduction to every well-formed BEM input, including graphs with no original perfect matching.

## 5. The converse oracle reduction, without an empty-list loophole

Suppose the input to EXTRA has n vertices on each side, f>=1 explicitly listed matchings, coloring w, and target T. First check list validity, distinctness, and the claimed common count. Under the definition above these are promised; if one chooses a total-language definition, failed validity is decided separately in polynomial time.

Write each matching as its row-ordered column sequence. Build the prefix trie of the f listed sequences. Every unlisted matching has a unique first row at which its prefix leaves that trie. A departure is specified by a trie node P of depth j<n and an available graph edge (a_(j+1),b) whose child is absent from the trie. There are at most 1+fn trie nodes and at most n candidate departures per node.

For each departure that is itself a valid partial matching, fix its prefix edges, delete their endpoints, and ask BEM whether the remaining graph has a perfect matching of red count

    T minus the number of red edges in that fixed prefix.

Out-of-range residual targets can be discarded. An affirmative answer completes that departure to an outside matching of target cost. Conversely every outside target matching appears in one of these queries, at its first departure. Therefore EXTRA is true if and only if at least one query is true. There are O(fn^2+n) queries, each of polynomial size; no response is needed to construct subsequent queries. The same oracle procedure decides COMP by negating the final OR.

This proves the stated polynomial-time Turing equivalence, including for singleton F. It is not an asserted many-one OR-composition theorem.

## 6. Deterministic subcases without polynomial identity testing

### 6.1 A target that is globally minimum or maximum

If the target T equals the minimum attainable red count, fixed-color completeness can be verified deterministically in time polynomial in the explicit input. Run the same prefix-departure construction. For each residual graph compute its minimum red-cost perfect matching by an ordinary deterministic minimum-cost bipartite matching algorithm. A departure extends to a target matching exactly when prefix cost plus that minimum equals T: every complete matching has cost at least T by assumption. The maximum case is analogous. Compute the global minimum/maximum first if the extremality is not promised.

In particular targets zero and n are handled by ordinary matching in the all-blue or all-red support. This uses no randomized identity test and need not enumerate all graph matchings.

### 6.2 Maximum degree at most two, with arbitrary target

For a graph of maximum degree at most two, each connected component is a path, an even cycle, or an isolated vertex. An isolated vertex or a path with no perfect matching immediately rules out nonempty valid F. Every other path has a unique perfect matching. Every even cycle has exactly two alternating perfect matchings. Hence its perfect matching red-count generating polynomial has the form

    z^a product_(i=1)^h (z^(b_i)+z^(d_i)),

where a is the total forced path cost and b_i,d_i are the red counts of the two choices on cycle i. The two terms must both be kept even if b_i=d_i, since they represent distinct matchings.

Multiply these factors by an elementary dynamic program on degrees 0,...,n, capping every coefficient at f+1. Nonnegative coefficients ensure that capping preserves the test whether the final target coefficient equals f or exceeds f. After checking that the f listed distinct matchings really have cost T, completeness is equivalent to the capped target coefficient being f. Time is O(nh) arithmetic operations on O(log(f+2))-bit nonnegative integers, plus input validation. Thus this is deterministic and polynomial in the explicit input even when there are 2^h total perfect matchings and unbounded affine dimension.

## 7. What this does not establish

* It does not transfer succinct-circuit-input coNP-hardness to explicitly listed F.
* It does not show Exact Matching is NP-hard, or resolve P versus NP.
* It does not show two-way polynomial many-one equivalence.
* It does not prove binary-fiber synthesis hard. Singleton synthesis is easy even though verification of an arbitrary proposed coloring already captures the Exact Matching obstacle.
* It does not cover a different problem that additionally requires H to equal the union of the listed matchings. For singleton F, that promise forces H to be its single matching, whereas this construction deliberately includes edges outside D. The unrestricted-graph explicit-list verification problem is the scope of the theorem.

All universal claims above are proved directly. The accompanying finite checker independently enumerates actual constructed graphs; its test results are corroboration, not a substitute for these proofs. Current-literature status is recorded separately in the audit if used; the equivalence theorem itself does not require a claim about the current best algorithm.
