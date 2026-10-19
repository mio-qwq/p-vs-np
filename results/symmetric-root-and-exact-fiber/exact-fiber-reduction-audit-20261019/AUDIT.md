# Independent audit: fixed-color binary-fiber completeness

19 October 2026. This audit checks the nonempty-explicit-list reduction independently of the construction worker's implementation. It concerns verification of a supplied binary coloring, not synthesis of a new coloring.

## 1. Exact statement

Let **BEM** be bipartite Exact Matching: the input is a simple bipartite graph G=(A,B,E), |A|=|B|=n, an edge coloring w:E->{0,1}, and integer k; ask whether a perfect matching of red count k exists.

Let **COMP** have input (H,c,t,F), where H is a separately supplied simple bipartite graph, c is a supplied binary edge coloring, t is supplied, and F is a nonempty explicit list of distinct perfect matchings. Ask whether

    F = {M in PM(H): c(M)=t}.

This is not a promise that H is the union graph of F. One can either reject malformed inputs or consider the well-formed restriction. The lower reduction below always outputs a well-formed instance with |F|=1 and with its listed matching already at target t.

The audited conclusions are:

1. BEM reduces by a deterministic polynomial-time many-one reduction to the complement of COMP, even when F has one member already at the prescribed target.
2. Equivalently, the complement of BEM reduces many-one to COMP on that restriction.
3. COMP reduces by a deterministic polynomial-time Turing reduction to BEM, using O(fn^2) exact-count queries for f=|F|.
4. Consequently BEM, COMP, and the complement of COMP are polynomial-time Turing equivalent. In particular BEM belongs to P if and only if COMP belongs to P.

The complement in item 1 is essential. This audit does not claim a many-one reduction from BEM to COMP, a many-one reverse reduction, NP-hardness, or a complexity-class separation.

## 2. A direct simple-graph dummy construction

First suppose n>=1 and 0<=k<=n. Set

    C=n+1,        T=nC+k.

Keep n left endpoints a_i and n right endpoints b_i. Add a blue direct edge a_i b_i for every i.

For each original edge e=a_i b_j, set q_e=C+w(e). Introduce a fresh path from a_i to b_j of length 2q_e-1, alternating between the bipartition classes. All internal vertices are new and belong only to this path. Color its first, third, fifth, ..., last edge red and all intervening edges blue. Do not retain the original direct edge. Since q_e>=2, every original edge uses a path of length at least three, so even an original diagonal edge never duplicates the direct blue edge.

Call this graph H_0. Independently add a cycle of length 2T, with one alternating perfect matching all red and the other all blue. T>=2, so this is a simple cycle. The full graph H is their disjoint union.

The distinguished matching D uses:

- every direct blue diagonal edge a_i b_i;
- all even-position, internal blue edges of every original-edge path;
- the all-red alternating matching of the new cycle.

D is immediately known without solving an ordinary or exact matching instance. Its red count is T. Output (H,c,T,F={D}).

### Local path lemma

Consider any perfect matching of H. A path's internal vertices have degree two and no outside neighbors. If its first edge is selected, alternation forces every odd-position edge, including the last one, to be selected. This consumes both original endpoints and contributes q_e red edges. If its first edge is not selected, the second edge is forced, then all even-position edges are forced. This consumes neither original endpoint and contributes zero red edges. These are the only two possibilities; in particular a path cannot consume just one endpoint.

Thus the activated original-edge paths form a partial matching P in G. If p=|P| and r=sum_{e in P} w(e), the H_0 cost is

    Cp+r,        0<=r<=p<=n.

The direct dummy diagonals must cover all original endpoints not consumed by these paths. This may exclude some partial matchings, but the proof does not need their full classification. For p=0 the H_0 perfect matching is unique. For p=n its activated paths are exactly a perfect matching of G, and its path completions are unique.

### Target equation

There are exactly two perfect matchings of the added cycle.

- If its all-red matching is used, its cost is T. The H_0 cost must be zero. Since C>0, this forces p=0 and gives precisely D.
- If its all-blue matching is used, the H_0 target equation is Cp+r=Cn+k. Because r,k lie in [0,n] and C=n+1, equality implies p=n and r=k. Equivalently, C(n-p)=r-k cannot be a positive multiple of C because r-k<C.

It follows that the target fiber has exactly one known member D, plus one uniquely lifted member for each k-red perfect matching of G:

    |{M in PM(H): c(M)=T}| = 1 + |{M in PM(G): w(M)=k}|.

This is also an explicit bijection, not only an existence equivalence. Hence F is complete exactly when the BEM instance is a NO instance.

### Boundary inputs

If k<0 or k>n, BEM is false. Output one blue edge with its unique matching listed and target zero, a COMP YES instance. This comparison needs only the input integer's bit length; no construction depends on an out-of-range numerical value of k.

For n=0, the empty graph has exactly the empty perfect matching. If k=0, output an all-blue K2,2 with one of its two matchings listed at target zero, a COMP NO instance. Otherwise use the one-edge COMP YES instance above. These constant outputs retain nonempty F.

## 3. Exact size and bit cost

Let m=|E| and R=sum_e w(e), with 0<=R<=m. Let N be the number of vertices in each bipartition class of H and M its edge count. The construction gives

    N = n + sum_e(q_e-1) + T
      = n + mn + R + T,

    M = n + sum_e(2q_e-1) + 2T
      = n + m(2n+1) + 2R + 2T.

Both are O(nm+n^2). Number the vertices consecutively. The edge list, binary colors, singleton matching D, and binary target T can be emitted in

    O((nm+n^2) log(nm+n+2))

bit output size and elementary bit-operation time, apart from reading the original input. The counters and labels have O(log(nm+n+2)) bits. All actual edge colors are binary; q_e and T are only polynomial-size gadget parameters. There is no exponential unary expansion hidden in this bound.

For dense simple G, m<=n^2, giving O(n^3) vertices/edges and O(n^3 log(n+2)) output bits. This is a polynomial reduction even if the source has no perfect matching.

## 4. Reverse prefix-oracle reduction

Validate every listed matching and check its supplied-color cost equals t. If this fails, COMP is false immediately. Normalize duplicate entries if the list representation permits them. Handle n=0 directly.

Fix the left-vertex order. Represent each matching by its list of matched right vertices and make the trie of all prefixes of the f listed matchings. There are at most 1+fn trie nodes. At each proper trie prefix P ending before row i, inspect each edge (i,j) such that j is not already used. If appending j leaves the trie, freeze that extended prefix, delete its matched vertices, and query BEM on the residual graph with target t minus the frozen prefix's red count. Out-of-range residual targets are immediately false.

Any unlisted matching has a unique first edge that exits the trie. Conversely every completion of an exiting prefix is unlisted. Therefore an outside target-count matching exists exactly when one of these residual queries is YES. COMP is true exactly when all queries are NO.

At most (1+fn)n=O(fn^2) queries are made for n>=1 and f>=1. Each query has at most n vertices in each class, m edges, and O(log(n+1)) target bits. A direct implementation that scans the graph when preparing each query has polynomial overhead, bounded for example by

    O(fn^2 (n+m) log(n+2) + validation/input costs)

bit operations and oracle-query output bits. The algorithm is uniform and deterministic with a BEM oracle. Replacing that oracle by a deterministic polynomial-time BEM algorithm would produce a deterministic polynomial-time COMP algorithm; the reduction alone does not supply that oracle.

## 5. Important scope boundaries

### Fixed coloring is essential

Every singleton family {D} can be synthesized as a complete binary fiber by coloring edges in D blue, all other edges red, and choosing target zero. A perfect matching with no red edge must use only D's edges and hence equal D. Thus every output of the lower reduction is a YES instance of the *synthesis* problem if the supplied coloring may be discarded. The reduction gives no synthesis lower bound.

### The separately supplied support graph is essential

The graph H is not the union graph of the singleton F: it contains many edges not used by D. If one imposed H=union(F), then a singleton F would make the support graph a disjoint union of matching edges, rendering completeness trivial. No hardness or equivalence for that additional promise is established here. A previous explicit-list complexity statement must not be transferred to that promise without a separate reduction.

### No complexity separation follows

The construction transfers deterministic algorithms and relative difficulty. It does not show that BEM or COMP is outside P. It does not prove NP-hardness of BEM. It does not validate or refute ASNC, specialized determinant noncancellation, or a proposed deterministic algorithm.

## 6. Primary-literature check, 19 October 2026

These sources are recorded to avoid treating an old status statement as a current theorem:

- [Sato and Yamaguchi, Exact Matching in Matrix Multiplication Time, arXiv:2508.04081v2](https://arxiv.org/html/2508.04081v2), revised 10 August 2026. The introduction describes deterministic polynomial-time Exact Matching as an open problem and presents a randomized algorithm. Its general-graph scope means this statement alone does not settle the bipartite case.
- [Du, Bipartite Exact Matching in P, arXiv:2604.01571v3](https://arxiv.org/abs/2604.01571v3), revised 9 April 2026. The current abstract claims a deterministic bipartite algorithm through ASNC. It says the accompanying Lean formalization reduces the main theorem to eight explicit hypotheses. This is narrower than v1's unqualified full-verification wording. This audit has not independently validated the algorithm or those hypotheses and does not use them as a premise.
- [Jia, Svensson and Yuan, The Exact Bipartite Matching Polytope Has Exponential Extension Complexity](https://arxiv.org/abs/2211.09106), 2022 preprint / SODA 2023. Its abstract says no deterministic polynomial-time algorithm was known even for bipartite graphs at that time. This dated statement does not establish the status in October 2026.

The rigorous safe conclusion here is the unconditional reduction theorem, which remains valid regardless of the eventual deterministic status. No claim of a newly settled or definitively still-open bipartite problem is needed.

## 7. Independent computational checks

`audit_check.py` imports no partner implementation. It constructs the actual expanded simple graph and enumerates its perfect matchings. It compares the entire red-count histogram against an independent partial-permutation model, checks the explicit dummy, checks exact size formulas, and checks the target count `1 + original exact count`.

The tested family comprises all 1x1 and 2x2 graphs with each potential edge absent, blue, or red, every valid target, and seeded additional 3x3, 4x4, and 5x5 instances. The independent reverse-reduction checker tests every binary coloring of K3,3, every nonempty subset of its six matchings, and every target 0..3, including listed families with inconsistent costs.

Normal Python run passed:

- 737 expanded-graph instances
- 19,636 actual expanded perfect matchings enumerated
- 129,024 prefix-oracle completeness cases
- 12,400 residual exact-count queries

The script uses explicit exceptions, so checks remain active under optimized Python. Both `python audit_check.py` and `python -O audit_check.py` completed with exit code zero and the identical counts above, reproduced in `audit_results.json`.

## 8. Review of the paired construction and additional tractable cases

The full paired `PROOF.md` in the `exact-fiber-reductions-20261019` deliverable was reviewed, including its exceptional inputs, exact vertex/edge formulas, and nonadaptive prefix queries. It agrees with this independently derived construction. No material proof defect was found.

The paired proof also gives two deterministic restricted verification algorithms, which are valid:

1. **Extremal red count.** When t is the global minimum matching red count, an exiting prefix has a target-cost completion precisely if its cost plus the minimum residual completion cost equals t. Every full completion already has cost at least t, so an exact-count gap cannot produce a false positive. The maximum case reverses the inequality. Ordinary min-cost bipartite matching with binary weights is deterministic polynomial time with polynomial-bit arithmetic. Compute the global extremum first if it is not promised.
2. **Maximum degree two.** Every viable path component contributes one forced matching and every even cycle contributes its two alternating matchings. The cost distribution is a product of binomials with nonnegative integer coefficients, even when the two exponents agree. A dynamic program capped at f+1 correctly distinguishes exactly f target matchings from more than f, since capping commutes with nonnegative addition and multiplication for this threshold. Given f distinct listed matchings already at target, equality of the total target count to f is equivalent to completeness. The DP uses O(nh) additions/comparisons of O(log(f+2))-bit integers, hence O(nh log(f+2)) elementary bit operations, plus graph processing and explicit-list validation; h is the number of cycle components. It handles exponentially many total matchings without listing them.

These restricted algorithms do not yield a general deterministic verifier or a synthesis result. The degree-two result is stronger than an enumeration bound based only on fixed affine dimension: it permits arbitrarily many independent cycles.

No remote files, pull requests, merges, tags, or releases were changed.
