# Two uniform algorithms for binary edge-cost fibers

19 October 2026. Exact restricted-class results. They do not assume P=NP, do not solve general binary-fiber recognition, and do not establish a general matching-polynomial noncancellation theorem. All files and computations are local.

## 1. Problem and representation

Let G=(A,B,E) be a finite simple bipartite graph, |A|=|B|=n, with perfect-matching set X. A nonempty family F⊆X is a **binary cost fiber** when there are edge colors w:E→{0,1} and an integer t such that

    F = {M∈X : ∑_{e∈M} w(e)=t}.

The usual input here is the graph and an explicit list of F, with each matching represented by its n chosen columns. Input validation rejects a purported matching with repeated columns or missing graph edges. Duplicates can be removed. If L is the bit length of this family list, reading and validating it is charged. Neither theorem below relies on a lookup table of precomputed graphs or families.

The first theorem also allows F to be specified by any supplied membership procedure, provided its evaluation costs are charged. The second makes at most 2^k membership queries. A succinct description of F is therefore not silently expanded for free.

## 2. A polynomial-time class with unbounded cycle rank

Call a left vertex a **distinguishing vertex** if every edge incident to a belongs to at most one perfect matching. Assume X is nonempty. Equivalently, the map

    M ↦ the edge of M incident to a

is injective on X.

**Theorem 1.** On any bipartite graph with a distinguishing vertex, every nonempty F⊆X is a binary cost fiber. A suitable vertex can be found, or its nonexistence certified, in deterministic polynomial time. A coloring can then be constructed in polynomial time, including the cost of reading or evaluating the description of F. The number of perfect matchings is at most n.

**Construction and proof.** Let R be the edges at a used by matchings in F. Color precisely R red and all other edges blue. Every perfect matching contains exactly one edge at a. Its red count is one precisely when that edge lies in R. By injectivity, this occurs precisely for matchings in F. Thus t=1 works. This includes F=X. No other edge is colored red.

To recognize the class, for each edge e=ab examine H_e=G−{a,b}. A perfect matching in H_e extends by e to a perfect matching in G. Determine whether H_e has zero, one, or at least two perfect matchings:

1. Run an ordinary augmenting-path bipartite matching algorithm to find a perfect matching P, if one exists.
2. If P exists, contract its matched pairs to vertices. For every nonmatching edge a_i b_j create a directed arc i→j. H_e has a second perfect matching exactly when this directed graph has a directed cycle.

For the last claim, flipping the alternating cycle corresponding to a directed cycle gives a different perfect matching. Conversely, the symmetric difference of two perfect matchings is a nonempty disjoint union of alternating cycles. A topological-sort or depth-first-search cycle test is linear in the graph size.

An edge of G is therefore classified as belonging to zero, one, or multiple perfect matchings. A left vertex is distinguishing exactly when none of its incident edges has the last classification. Since X≠∅, each left vertex has at least one edge of the middle or last classification. For a distinguishing vertex, retain the unique extension for each edge in the middle class; these are all the perfect matchings, with no duplicates. Evaluate F on them, or match them against the explicit input list, and use the construction above.

A simple augmenting-path routine takes O(nm) graph operations per edge, where m=|E|. There are m residual graphs, giving O(nm²) graph operations plus polynomial-size input validation, storage, and cycle tests. Labels and counters have O(log(n+m)) bits. Thus even an elementary implementation has genuine polynomial bit complexity. This bound is intentionally conservative; a faster matching routine is unnecessary for the theorem. The output is m binary bits and the target 1.

### Connected examples with arbitrarily many cycles

Take two opposite-side terminals u∈A and v∈B, joined by r internally vertex-disjoint odd-length paths. There are no other edges. At most one path has length one in a simple graph. This connected bipartite multi-theta graph has cyclomatic number r−1, which is unbounded.

Write a path's length as 2h+1. If neither terminal is matched along this path, its 2h internal vertices have the unique consecutive matching. If both terminals are matched along it, the entire path has the other unique consecutive matching. Exactly one terminal cannot be matched along it. For a length-one path, its sole edge matches both terminals together. For a longer path, consuming just one endpoint's adjacent internal vertex leaves an odd number of internal vertices to be matched within the path. Consequently, every global perfect matching chooses exactly one path to match both terminals and uses the internal matching on every other path. There are exactly r perfect matchings, each uniquely determined by its edge at u. Hence u is distinguishing, and every selected family is realized by the red edges at u, with target one.

This is a connected, unbounded-cycle-rank family rather than a bounded union of K2,2 blocks. The construction also applies to any other graph with a distinguishing vertex; the multi-theta decomposition is not required as input.

## 3. A uniform bounded-effective-cycle-rank algorithm

An edge is **allowed** if it occurs in at least one perfect matching. Delete all nonallowed edges, obtaining H. The edge tests above find H in polynomial time. The perfect matchings of G and H coincide. Colors on deleted edges can be zero.

Let m_H be the number of edges of H and c_H its number of connected components, including isolated vertices if any. For nonempty X and n>0 no vertex of H is isolated. Define

    k = m_H − 2n + c_H.

This is the ordinary cycle-space dimension of H. For n=0 the unique matching is empty; every nonempty family is that singleton, realized by target zero. Below assume n>0.

**Theorem 2.** There is one uniform, deterministic exact algorithm that recognizes binary-fiber realizability and constructs a coloring on every input (G,F). Its running time is polynomial preprocessing plus

    2^{O(k)} (2n+1)^k poly(n,m,L,k)

bit operations. In particular it is polynomial for every fixed k. This is an XP bound in k, not a fixed-parameter-tractable bound, and no polynomial claim is made when k grows with n.

The algorithm enumerates at most 2^k perfect matchings, then uses a k-dimensional bounded-integer dynamic program for the edge colors. It never enumerates all 2^{m_H} edge colorings.

### 3.1 Enumerating all perfect matchings with k chord bits

Choose a spanning forest T of H. There are exactly k non-tree edges, called chords f_1,…,f_k. For a fixed set of chosen chords, the required degrees remaining at every vertex are determined. A forest has at most one edge assignment with those degrees: repeatedly remove a leaf, whose incident tree edge must equal its residual degree, and subtract this value at its neighbor. A residual degree outside {0,1}, or a nonzero residual degree at an isolated vertex, makes the assignment infeasible.

Enumerate the 2^k binary chord assignments. The leaf procedure returns exactly the perfect matchings, without duplicates, in O(2^k(n+m_H)) graph operations. In particular

    |X| ≤ 2^k.

Validate the explicit F against this list, or evaluate the supplied membership procedure once per matching. Keep one M_0∈F.

### 3.2 Fundamental alternating cycles are integer coordinates

For each chord f_j, its fundamental cycle in T∪{f_j} is even. Define z_j∈{−1,0,1}^{E(H)} by giving f_j coefficient +1, alternating signs around its cycle, and zero elsewhere. Every vertex has total incident z_j coefficient zero. Moreover z_j(f_i)=1 if i=j and zero otherwise.

For every perfect matching M,

    p_M − p_M0 = ∑_{j=1}^k [p_M(f_j)−p_M0(f_j)] z_j.       (1)

Indeed, subtracting the right side from the left cancels every chord coordinate and retains zero incident sum at every vertex. A vector supported on a forest with zero incident sum is zero by leaf elimination. This proves (1) without rational coefficients or Gaussian elimination.

For any binary edge coloring w define its signature

    s(w) = (w·z_1,…,w·z_k).

Each fundamental cycle contains at most n positive and n negative coefficients, so every coordinate belongs to [−n,n]. The same bound holds for every partial sum of its edge contributions. By (1), the cost difference from M_0 is exactly

    d_M(s) = ∑_{j=1}^k [p_M(f_j)−p_M0(f_j)] s_j.          (2)

Thus a signature realizes F if and only if d_M(s)=0 for M∈F and d_M(s)≠0 for M∉F. These are integer equalities and inequalities.

### 3.3 Exact binary-signature dynamic programming

Order the edges e_1,…,e_mH. Let a_i=(z_1(e_i),…,z_k(e_i)). The attainable signatures after the first i edges satisfy

    R_0 = {(0,…,0)},
    R_i = R_{i−1} ∪ {s+a_i : s∈R_{i−1}}.               (3)

This recurrence chooses each edge color once, as either zero or one. Therefore R_mH is exactly the set of signatures of binary colorings, with no relaxation. Every R_i lies in [−n,n]^k, so it has at most S=(2n+1)^k states.

A deterministic implementation keeps each R_i lexicographically sorted. Adding the fixed vector a_i preserves order, so R_i is obtained by a linear merge of R_{i−1} and its translate, with duplicate removal. Comparing or adding two k-vectors uses O(k log(n+2)) bit operations, apart from standard polynomial indexing overhead. The total number of vector operations is O(m_H S). Keep all layers for reconstruction.

Test each final signature with (2) on all at most 2^k matchings. The intermediate dot-product magnitudes are at most kn, so their bit length is O(log(kn+2)); the number of terms tested is O(S 2^k k). If a signature passes, trace it backward: if it was already reachable in the preceding layer choose color zero; otherwise choose color one and subtract a_i. The resulting w is binary and has the desired signature. Set

    t = ∑_{e∈M0} w(e),

which lies in [0,n]. If no signature passes, (3) has exhausted every possible binary coloring and proves nonrealizability.

For k=0, there is one perfect matching, the empty-dimensional signature is unique, and the algorithm correctly returns the all-blue coloring with target zero.

### Why the parameter is genuinely effective

Removing edges that never occur in perfect matchings can make k much smaller than the original graph's cycle rank. Forced matching edges need not be contracted: they form tree components or cancel from all cycle coordinates. In fact k equals the affine dimension of the perfect-matching incidence vectors of H. One way to see this is that the convex hull of bipartite perfect matchings is the polytope defined by nonnegative edge entries and incident sums one. The average of all its matchings is strictly positive on every allowed edge, so its affine hull has only those degree equations; their rank is 2n−c_H. This observation is not needed by the algorithm or its proof.

## 4. Boundaries

- Theorem 1 covers a recognizable class with unbounded k; it is not a theorem for every graph having only polynomially many perfect matchings. Its injectivity hypothesis is essential to its one-star coloring construction.
- Theorem 2 covers overlapping cycles and arbitrary bipartite graphs after effective-cycle-rank restriction. Its exponent depends on k. It does not make a uniform polynomial-time claim for arbitrary graphs.
- Merely passing the affine-hull test is insufficient. Four disjoint K2,2 blocks with F consisting of the two opposite global matchings remain a negative binary instance; the dynamic program rejects it.
- These algorithms concern exact complete fibers. A successful coloring proves that no outside matching has the target cost, because every matching is represented in the test or because the distinguishing-vertex proof excludes it.
- They do not prove that a given nonempty fiber's signed polynomial sum is nonzero. The separate four-row noncancellation result and the fiber-realizability problem remain distinct obligations.
- A description of F by a large or expensive program contributes its evaluation cost. There is no nonuniform advice, free truth table, or unit-cost arithmetic on unbounded integers.

## 5. Reproducible exact checks

`check.py` uses Python's standard library, integer arithmetic, and explicit exceptions rather than assertions. It implements ordinary matching and alternating-cycle uniqueness tests, the distinguishing-vertex construction, fundamental-cycle signature DP with sorted merges, and chord-based matching enumeration. Independent exhaustive checks enumerate edge colorings on small graphs.

Checks compare all realizable nonempty family masks from the DP against all binary edge colorings on K3,3 and a five-rung ladder. Additional checks cover the four-K2,2 negative example, a connected multi-theta graph with every family tested, and a larger multi-theta graph with many cycles. The output `results.json` gives instance sizes and exact counts.

Run `python check.py` and `python -O check.py`. Theorems follow from the proofs above; the finite checks are regression tests.
