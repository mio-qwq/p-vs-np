# XOR matching, exact reductions, and the missing separation quantifier

19 October 2026. Independent mathematical audit and explicit finite certificates. No remote repository writes, merge, or release. No proof of P=NP, P!=NP, universal noncancellation, or a logarithmic-dimension NP-hardness reduction is claimed. The constructions below use standard ingredients; no literature-novelty claim is made.

## Results

1. The prior constructive-cost audit is correct at its stated scope: canonical universal binary-color ASNC implies a polynomial deterministic Exact Matching algorithm; the colored C6 defeats unconditioned tight-cut count convolution; the binary-weight SUBSET-SUM barrier is valid.
2. Perfect 3-dimensional matching reduces uniformly to prescribed-XOR perfect matching on simple bipartite graphs. With parts of size n and m triples, the output has n+m vertices on each side and 3m edges. The label dimension can be n-1. This proves NP-completeness when dimension grows with the input, not hardness at logarithmic dimension.
3. For every k>=1 there is a simple bipartite graph with 6k-1 vertices per side and 14k-5 edges whose perfect-matching signatures are exactly F_2^k minus {0}, each once. Every rank-deficient linear projection of its labels creates a false YES at target zero, even if the projection is chosen specifically for that graph. Indeed, all exact proper linear-projection supports are indistinguishable from those of a graph realizing every signature.
4. These are restricted-method obstructions. The missing P!=NP quantifier ranges over all polynomial-time deterministic algorithms, not all fixed conditioning depths, linear projections, or tested specializations.

## 1. Independent verdict on the prior constructive-cost proof

The audited document is `constructive-cost-audit-20261019/PROOF.md`. Its three principal conclusions pass. The audit checked the argument, not merely its test output.

### 1.1 What U-ASNC supplies

For an explicit simple bipartite graph with n vertices per side and binary color rho, the matrix is

    M(x,L)[i,j] = x^rho(i,j) (L+i)^j on allowed edges, and 0 elsewhere,
    P_t(L) = [x^t] det M(x,L),   0<=i,j<n.

The required hypothesis is nonvanishing of P_t for every nonempty target fiber, on every such graph and coloring, for these fixed offsets and exponents. It is not a theorem for arbitrary offsets, a complete-graph mask, or braces alone.

The L-degree is at most D=n(n-1)/2 and the x-degree at most n. Thus an explicit (D+1)-by-(n+1) integer grid suffices. Each determinant entry has O(n log n) bits; minors and Bareiss intermediates have O(n^2 log n) bits. There are O(n^3) determinants, each using O(n^3) arithmetic operations. Charging schoolbook bit arithmetic gives O(n^10 log^2(n+2)). Integer Lagrange coefficient numerators use only an additional O(n log n) bits, so interpolation does not hide exponential denominators.

The extraction argument is also correct: after finding one nonzero P_t(ell), keep ell and the original row offsets/column exponents. Laplace expansion ensures that some edge leads to a nonzero residual coefficient. Iterating gives a witness without invoking ASNC for residual graphs. The number of arithmetic operations remains O(n^6), before charging the same bit bound. Renumbering residual exponents would invalidate this particular invariant, and the source correctly forbids it.

Therefore the advertised runtime is a conservative upper bound under precisely U-ASNC. Without that hypothesis, the procedure has sound YES answers and an unproved NO implication.

### 1.2 The C6 criterion is genuine

The edges are a0b0, a1b0, a1b1, a2b1, a2b2, a0b2. Only a0b0 and a2b2 are red. Its perfect matchings have red counts 2 and 0. The shore S={a0,b0,a1} has exactly two crossing edges, e_A=a1b1 and e_B=a0b2, both blue. Each matching uses exactly one, so the cut is tight.

Each shore contraction is C4, and each has count set {0,1}. Selecting e_A contributes one red edge in each block; selecting e_B contributes zero in each. The valid glued totals are therefore {0,2}. The naive Minkowski sum {0,1,2} wrongly admits 1. Because both crossing edges are blue, subtracting a double-counted red-edge contribution cannot repair the example.

The correct local rule is

    F_G(t) = OR over e,u,v with u+v-rho(e)=t
             of F_(1,e)(u) AND F_(2,e)(v),

where the two block matchings must choose copies of the same original crossing edge e. This follows from a bijection, and O(|cut| n^2) work suffices once the forced-edge tables exist. The proof does not establish that all such tables throughout a decomposition can be represented and obtained in polynomial time. Nor does this obstacle prove that every repaired algorithm is exponential.

The graph has strict proper Hall expansion but is not a brace. Equality-Hall splitting therefore cannot be asserted to produce brace leaves. This does not refute the separate determinant identity for genuinely balanced Hall blocks.

### 1.3 Weighted encoding is a different problem

For each binary SUBSET-SUM weight w_i, a disjoint K2,2 component with one diagonal edge of weight w_i and all other weights zero has matching totals 0 and w_i. Component choices give the exact subset sums. This polynomial binary encoding establishes NP-hardness of binary-weight exact matching.

The private path of length 2w+1 correctly simulates weight w by w red edges, but uses 2w internal vertices. It is pseudopolynomial in binary weights. Likewise, interpolation degree based on numerical weights may be exponential in their bit lengths. Neither fact transfers NP-hardness to the binary-color problem.

Both runs of the prior checker, ordinary and Python -O, passed with 689 graphs, 11,126 determinant evaluations, and 1,643 extracted witnesses each. These checks corroborate finite certificates, not U-ASNC.

## 2. A complete 3DM-to-XOR reduction

### 2.1 Definitions and multigraph construction

Let X,Y,Z be explicitly given sets of equal size n, and let T subset X cross Y cross Z be a list of m distinct triples. A perfect 3-dimensional matching consists of n triples covering each element of all three parts exactly once. This is the classical NP-complete decision problem in [Karp (1972)](https://doi.org/10.1007/978-1-4684-2001-2_9).

For every triple (x,y,z), create a separate bipartite edge from x to y with label e_z in F_2^n. Distinct triples can give parallel edges, and their identities must be preserved. Set target tau=(1,...,1).

A perfect matching selects exactly n triples covering X and Y. Let c_z be its count for coordinate z. Then

    sum_z c_z=n,   lambda(M)=tau iff every c_z is odd.

If every c_z is odd, all n counts are at least 1, and their sum is n. Therefore every c_z=1. The converse is immediate. This is a witness-preserving bijection between perfect 3DM solutions and target-XOR perfect matchings.

### 2.2 Removing parallel edges without changing dimension

Replace each individual edge e=(x,y) by a private path

    x -- b_e -- a_e -- y,

where a_e is on the left, b_e on the right. Put the original label on x--b_e and zero on the other two edges. Distinct original edges get distinct internal vertices.

In any perfect matching exactly one of two local states occurs:

- Unselected: a_e--b_e is chosen. The original endpoints are covered elsewhere and the gadget contributes zero.
- Selected: x--b_e and a_e--y are both chosen. The gadget covers both original endpoints and contributes exactly lambda(e).

There is no half-selected state: omitting a_e--b_e forces both degree-two internal vertices outward. Thus perfect matchings of the simple graph correspond bijectively to those of the multigraph, with identical signatures. The output has n+m vertices per side and 3m edges. This establishes a simple-graph reduction, rather than silently collapsing parallel triples.

### 2.3 One coordinate is redundant

In the original multigraph every matching chooses n one-hot labels. Its signature p always satisfies

    sum_z p_z = n mod 2.

Consequently its last coordinate is determined by the first n-1. Delete coordinate n from all edge labels and from the all-ones target. Matching the resulting target in F_2^(n-1) is equivalent to matching the original target. The private-path transformation preserves this property by its bijection, even though its perfect matchings have n+m edges.

Thus n-1 bits suffice; for n=1 the dimension-zero case is just existence of the lone possible triple. The empty n=0 instance can be handled directly. Dense vectors cost O(mn) bits plus graph encoding, which is polynomial in the explicit 3DM input. The constructor and inverse witness map are uniform polynomial-time procedures. A matching and its XOR can be checked in polynomial time, so the unbounded-dimension simple bipartite XOR problem is NP-complete.

This reduction does not promise a brace, a complete graph, or a special rectangular mask. Its internal vertices have degree two. Additional promised graph classes require their own reduction.

### 2.4 A sharp limit for a universal one-hot linear encoding

Suppose a fixed linear map A:F_2^n -> F_2^r is intended to replace the one-hot labels above while preserving correctness for every 3DM instance of size n. Put

    H={d in F_2^n : sum_z d_z=0},   dim H=n-1.

Every parity vector p with sum p_z=n mod 2 can occur as the XOR of n one-hot labels: use each coordinate in its support once and allocate the remaining even number of labels in equal pairs. Such a multiset can be realized by a unique perfect matching using only triples (x_i,y_i,z_i).

If r<n-1, the restriction of A to H has a nonzero kernel vector d. Let p=tau+d. It is parity-compatible and distinct from tau, so the unique-matching realization is a 3DM NO instance. Yet A(p)=A(tau), making the projected instance YES. Therefore a fixed label dictionary correct for all instances needs r>=n-1. Deleting one coordinate attains this bound.

The quantifiers here are important: for every fixed A there is a counterexample instance. This alone does not rule out an A chosen after inspecting the particular instance. The next construction supplies that stronger obstruction for general XOR matching inputs.

## 3. An instance that defeats every proper linear label projection

### 3.1 A small labeled DAG

Fix k>=1. A length-k binary string is processed by a two-state automaton whose state records whether a 1 has appeared. Begin at state (0,0). For each position i, the transition for bit b updates (i,q) to (i+1,q OR b) and emits b e_i. Accept only the final seen-1 state.

Make the layered transition graph explicit. Some transitions, once a 1 has occurred, have identical endpoints but different labels. Subdivide every transition with its own private vertex; put the emission label on its first arc and zero on its second. This makes the directed graph simple. Add a new sink t and the zero-labeled arc from (k,1) to t. The source is s=(0,0).

Each nonzero binary string gives exactly one s-to-t path, and every such path is obtained this way. Its signature is that string. There are 1+2k automaton-state vertices, 4k-2 transition vertices, and one sink: exactly 6k vertices. There are 8k-3 directed arcs. Unreachable or nonaccepting states cause no problem.

### 3.2 Acyclic paths to bipartite perfect matchings

For any simple acyclic digraph D with distinguished source s and sink t, construct a bipartite graph as follows:

- Left vertices are V(D) minus {t}; right vertices are V(D) minus {s}.
- Each directed arc u->v gives an edge u_left--v_right with its arc label.
- Each internal vertex v other than s,t gets the zero-labeled diagonal v_left--v_right.

An s-to-t path gives a perfect matching by taking all its directed-arc edges and the diagonals of vertices outside the path. Conversely, a perfect matching gives outdegree one at every vertex except t and indegree one at every vertex except s. Starting at s must reach t: it cannot close a nontrivial directed cycle in an acyclic graph, and cannot enter a chosen self-diagonal because that diagonal would already occupy the incoming slot. Any non-diagonal edges outside the s-to-t path would form a directed cycle, also impossible. Hence all remaining choices are diagonals. This proves a label-preserving bijection.

Applied to the automaton DAG, the result G_k is simple, has 6k-1 vertices per side, and has

    (8k-3) + (6k-2) = 14k-5 edges.

Its signature support is exactly

    S(G_k)=F_2^k minus {0},

with one perfect matching per signature. In particular, the target-zero instance is NO.

### 3.3 Projection impossibility, including instance-dependent choice

Let A:F_2^k -> F_2^r be any rank-deficient linear map, and apply it to every edge label and to the target. Choose nonzero sigma in ker A. Since sigma is in S(G_k), one perfect matching becomes zero-labeled after projection. The projected instance is YES.

Thus for this single G_k, every rank-deficient A fails. The map may be selected with full knowledge of G_k and unlimited computation; the problem is not merely finding the right map. In particular, no universally correct graph-preserving linear dimension compressor exists.

Moreover, for every rank-deficient A,

    A(F_2^k minus {0}) = A(F_2^k).

Each fiber has at least two elements, so deleting zero leaves every image value attained. Adding one extra zero-labeled accepting arc from the final seen-0 state to t gives a graph G_k^+ with one matching per signature in the whole space. All exact proper linear-projection support sets of G_k and G_k^+ coincide. Therefore even asking every proper linear projection, not just a few random hashes or scalar parity tests, cannot distinguish these two signature supports. Combining independently feasible projections by AND is unsound because their witnesses need not agree.

This is stronger than an affine-hull false positive at the level of unconditioned signature abstractions: for k>=2, both supports have full affine hull, but here even exact supports of every proper quotient coincide. It is not a claim about algorithms that inspect other graph structure or condition on edges.

The family itself is easy to understand and its target-zero answer is immediate from the automaton. No computational hardness follows. The theorem leaves open arbitrary topology-changing reductions, nonlinear encodings, keeping additional compatibility information, special input families, and exact algorithms operating on the original labels.

## 4. The precise logarithmic-parameter obligation

Let L be the bit length of a SAT or 3DM instance. The reduction in Section 2 produces polynomial-size graphs with k=n-1. In ordinary explicit 3DM encodings, L is polynomial in n, so n need not be O(log L). Exponentiating k therefore remains exponential rather than polynomial. Exponential padding to make log(output size) large violates the polynomial output-size requirement.

A successful logarithmic-dimension compiler requires a single deterministic algorithm R and fixed constants c,C such that, for every input phi of length L:

1. R runs in time at most L^c (with harmless small-input adjustments).
2. Its explicit graph and all labels have at most L^c bits.
3. Its output has k<=C log(L+2).
4. phi is satisfiable if and only if its target signature is attainable.
5. Every graph-class promise required by the solver is actually satisfied.

An existential statement that each instance has some small encoding is insufficient: a constructor could conceal the original decision problem. Specifying F_2^k by a full operation table is also not free; that table has 2^(2k) entries. Bit-vector labels and explicitly tabulated groups are different input encodings.

The associated deterministic solver must have a uniform bound such as 2^(a k) N^b for fixed constants a,b, where N measures the explicit graph input. A statement 'polynomial for every fixed k' with degree depending on k only gives an XP-type guarantee; N^O(k) becomes quasipolynomial at k=Theta(log L). The positional-count reduction in the prior audit has precisely this cost issue. U-ASNC for one binary coloring does not, by itself, establish the required deterministic multi-XOR bound.

### 4.1 Why even the compiler alone is consequential

For a bipartite graph with q vertices per side, give each edge e its own variable y_e. Over an odd prime field of size p>2q, for every a in F_2^k form

    B_a[i,j] = y_e (-1)^(a dot lambda(e)) on edge e, else 0.

Define

    Q_tau(y) = 2^(-k) sum_a (-1)^(a dot tau) det B_a(y).

Character orthogonality gives

    Q_tau(y) = sum over target matchings M of sign(M) product_(e in M) y_e.

Distinct matchings give distinct monomials with coefficients +/-1, so this polynomial is nonzero exactly on YES instances. Its degree is q. Independent uniform edge evaluations yield false negatives with probability at most q/p<1/2 and never false positives. Evaluation uses 2^k determinants and polynomial bit arithmetic, hence randomized 2^k poly(N,k) time. The formula is a direct derivation, consistent with the represented-common-basis algorithm in [Hörsch et al., ICALP 2024, Theorem 4.2](https://drops.dagstuhl.de/storage/00lipics/lipics-vol297-icalp2024/LIPIcs.ICALP.2024.86/LIPIcs.ICALP.2024.86.pdf). Their group-table input must be charged as stated above.

Consequently, a deterministic uniform polynomial reduction from SAT to k=O(log L) bipartite XOR matching would already imply NP=RP, by this randomized baseline. Supplying a deterministic single-exponential-in-k solver as well would imply P=NP. Neither implication proves that the compiler is impossible, and NP=RP is not the same assertion as P=NP.

## 5. Fixed-depth hull obstructions and the all-algorithms quantifier

The prior fixed-depth construction, audited in the accompanying local project, gives for every fixed depth d infinitely many explicit XOR-matching NO instances with k=O_d(log N) on which every permitted conditioned affine-hull test through depth d still contains the target. Its finite-field proof uses 2t special columns and k=tm with t=ceil((d+1)/2), N=2^m. This is a useful infinite-family obstruction to that specified relaxation.

Its logical form is

    for every fixed d, there are instances defeating the depth-d hull criterion.

The linear-projection result here has the different form

    for every k>=1, there is one explicit instance defeating every
    rank-deficient graph-preserving linear label projection.

Neither statement quantifies over all deterministic polynomial-time algorithms. They exclude concrete lossy abstractions. They do not exclude nonlinear algebraic invariants, algorithms retaining correlations, adaptive methods outside the specified abstraction, or growing-depth procedures with an independently proved runtime. Conversely, simply choosing d to grow with N is not a proved efficient repair: the old family's constant in k=O_d(log N) also depends on d, and the number of conditioned states must be charged.

For a fixed NP-complete language such as SAT, an actual separation requires

    for every deterministic machine A and every polynomial time bound p,
    there is an input x on which A does not give the correct SAT answer
    within p(|x|) steps.

Equivalently, no single deterministic machine decides SAT correctly on every input within one polynomial time bound. Failure of one specialization, one DP, all constant depths of one test, or every map in one compression template does not establish this statement. To turn restricted-method lower bounds into a separation, one would need an additional universality theorem showing that every polynomial-time SAT algorithm is captured by the restricted method with appropriate overhead. No such theorem is supplied or claimed here.

The concrete advance is therefore a complete unbounded-dimension reduction, a sharp universal one-hot encoding limit, and an instance-wise obstruction to graph-preserving linear compression. The outstanding bridges are now explicit rather than hidden in parameter notation.

## 6. Reproduction and limits

Run `python check.py` and `python -O check.py`; both produce identical output. The checker uses Python's standard library and explicit exceptions, so optimization does not disable its validations.

It independently rechecks the C6 count sets and the distinction between naive and crossing-compatible convolution. It checks 359 3DM instances, including all 256 subsets of the n=2 triple universe, 100 reproducibly sampled n=3 cases, and boundary/complete cases. A generic sparse perfect-matching enumerator independently verifies the private-path bijection, signature multiplicities, target equivalence, and removal of one coordinate. It also enumerates G_k and G_k^+ for k=1,...,7, confirming every signature exactly once and the exact graph counts. Exhaustive checks cover 4,448 proper-output linear maps through k=4 and 283 one-hot compression maps.

The proofs establish the asymptotic statements; finite checks are corroboration. Neither formal proof-assistant verification nor a comprehensive novelty review was performed. All work remained local.
