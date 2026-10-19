# What noncancellation would actually buy

19 October 2026. A conditional algorithmic theorem, an exact tight-cut counterexample, and a representation-cost barrier. No proof of P=NP, P!=NP, or universal ASNC is claimed. No remote files were changed.

## Results first

1. For explicitly given bipartite graphs, universal binary-color ASNC at the specific offsets `a_i=i` and exponents `e_j=j` would give deterministic Exact Matching, including witnesses, in `O(n^10 log^2(n+2))` schoolbook bit operations. The identity test uses explicit polynomial-size grids and needs no separate PIT assumption.
2. Brace-only ASNC does not justify independent feasible-count convolution across tight cuts. An explicit colored six-cycle has feasible counts `{0,2}`, while its two four-cycle contraction blocks each have counts `{0,1}`. The missing condition is agreement on the exact crossing edge, even when every crossing edge is blue.
3. Binary-encoded weighted Exact Matching already contains SUBSET-SUM on disjoint four-cycles. Replacing weights by red-edge path gadgets is only pseudopolynomial. Thus the NP-hard weighted variant cannot be silently substituted for binary-color Exact Matching.

These are independent mathematical derivations. The source manuscript is [Du, v3](https://arxiv.org/html/2604.01571v3), especially Proposition 2.3 and the reduction discussion in Section 3.6. The prior local audit expressly excluded the tight-cut algorithm and cost analysis, so item 2 is additional to that audit, without a literature-novelty claim.

## 1. Explicit input and the exact hypothesis

The input is an explicit simple bipartite graph with `n` named vertices on each side, its allowed-edge list or adjacency matrix, one bit `rho(e)` per allowed edge, and an integer target `t`. The graph representation must explicitly account for its vertices; a huge binary vertex count together with a succinct edge-generation circuit is a different input model. Targets outside `[0,n]` can be rejected immediately.

Use rows and columns numbered `0,...,n-1`, and define

    M(x,L)[i,j] = x^rho(i,j) (L+i)^j   if (i,j) is an edge,
                 0                   otherwise;
    P_t(L) = [x^t] det M(x,L).

Call the following hypothesis U-ASNC:

    For EVERY explicit bipartite graph, EVERY binary edge coloring,
    and EVERY target, a nonempty target matching fiber implies P_t != 0.

The reverse implication is automatic from the determinant expansion. The universal graph quantifier is essential. A result only for complete graphs, one red rectangle, a rectangle plus one entry, or braces is not this hypothesis. Nor is a result for different, graph-dependent offsets/exponents sufficient without a uniform constructor and bounds on those parameters.

The hypothesis uses exactly `a_i=i`, `e_j=j`; it does not quantify over binary-encoded arbitrary exponents. A failure of a stronger arbitrary-exponent conjecture need not refute this one.

## 2. Conditional bit-complexity theorem

**Theorem.** Under U-ASNC, binary-color Exact Matching on explicit bipartite graphs is decidable deterministically in `O(n^10 log^2(n+2))` bit operations with elementary integer arithmetic. The same asymptotic bound suffices to output a matching whenever one exists.

The exponent is deliberately conservative, not an optimal implementation claim. Without U-ASNC, the algorithm remains an exact algebraic nonzero-fiber detector: every YES is valid, but a zero polynomial is not an established NO certificate.

### 2.1 Degree and deterministic test points

Set `D=n(n-1)/2`. Every determinant monomial uses each column exponent exactly once. Therefore

    deg_x det M <= n,    deg_L P_t <= D.

For each integer `ell=0,...,D`, compute `det M(j,ell)` for every `j=0,...,n`, then recover the coefficient of `x^t`. Accept iff that coefficient is nonzero at at least one `ell`.

An ordinary nonzero univariate polynomial of degree at most D cannot vanish at D+1 distinct rational points. Interpolation in x is likewise exact at n+1 points. Thus this is a fully specified deterministic identity test after the specialization. There is no invocation of general circuit PIT or an unconstructed hitting set. The *unproved combinatorial part* is precisely that the specialization preserves every nonempty target fiber.

There are `(D+1)(n+1)=O(n^3)` determinant evaluations. All n+1 target coefficients can be recovered together; the determinant grid need not be rerun for each target.

### 2.2 Integer determinant sizes

Assume n>=2; n=0,1 are direct cases. Let

    A = n (D+n)^(n-1).

Every entry of every evaluated matrix has absolute value at most A. The convention `0^0=1` is the polynomial convention. Every k-by-k minor is bounded by `k! A^k`, hence every minor has at most

    B = 2 + ceil(log2(n! A^n)) = O(n^2 log(n+2))

bits. A pivoted fraction-free Bareiss determinant algorithm performs O(n^3) additions, multiplications and exact divisions; stored quantities are minors (up to signs), and the multiplication/subtraction temporaries have O(B) bits. Row pivoting handles zero pivots; if no pivot exists the determinant is zero.

With schoolbook multiplication and long division, each operation costs O(B^2) bit operations. Hence the entire determinant grid costs

    O(n^3) * O(n^3) * O(B^2)
       = O(n^10 log^2(n+2)).

This also charges exact arithmetic rather than treating arbitrarily large integers as unit-cost objects. Matrix entries can be generated by successive powers, and their construction is dominated by the same bound.

### 2.3 Interpolation without hidden rational blowup

For the nodes `0,...,n`, put

    c_(j,t) = [x^t] product_(0<=h<=n, h!=j) (x-h).

Lagrange interpolation gives the integer formula

    n! P_t(ell)
      = sum_(j=0)^n (-1)^(n-j) binom(n,j) c_(j,t) det M(j,ell).    (1)

Thus the zero test can use the numerator in (1) and never divide by interpolation denominators. Each `|c_(j,t)|` is at most `(n+1)!`, by the product of the coefficient absolute sums. The sum in (1) has O(B+n log(n+2))=O(B) bits, including intermediate partial sums. Precomputing all c values and applying (1) to every target at every ell takes fewer integer operations than the determinant grid. The possible denominators `j!(n-j)!` have only O(n log(n+2)) bits and are cleared by n!.

### 2.4 Witness extraction requires no residual ASNC

Suppose `P_t(ell)!=0` at a grid point ell. Keep ell fixed, and retain the ORIGINAL row offsets and column exponents throughout deletion. For a current row set R, column set C and residual target s, maintain

    [x^s] det M(x,ell)[R,C] != 0.

Expand along any remaining row i. The nonzero coefficient is a sum over allowed incident edges `(i,j)` of

    sign(i,j) (ell+i)^j
       [x^(s-rho(i,j))] det M(x,ell)[R\{i}, C\{j}].

At least one summand is nonzero. Compute the smaller coefficients exactly, choose such an edge, remove its endpoints, and decrease the target by its color. At the empty matrix the target must be zero. The selected edges form the required perfect matching.

This works even if a residual graph is outside the graph class on which ASNC was proved: the invariant is nonzero algebra, which alone implies a witness. It must NOT renumber exponents or change ell during this argument.

At residual size m, at most m candidate edges require at most m evaluations of an (m-1)-square determinant each. The total arithmetic work is `sum_(m<=n) O(m^5)=O(n^6)`. Original-index entries and all their minors obey the same O(B) bit bound, so the bit cost remains as claimed. In particular, brace-only ASNC does yield a decision-and-search algorithm for an input already known to be a brace; deletion-closure is unnecessary for this positive extraction.

## 3. A precise tight-cut obstruction and its repair obligation

### 3.1 The six-cycle certificate

Let rows be a0,a1,a2, columns b0,b1,b2, and let

    E = {a0b0, a1b0, a1b1, a2b1, a2b2, a0b2}.
    Red = {a0b0, a2b2}.

This is a six-cycle. Its only perfect matchings are

    M_A = {a0b0, a1b1, a2b2},  with 2 red edges;
    M_B = {a1b0, a2b1, a0b2},  with 0 red edges.

Take the shore `S={a0,b0,a1}`. The cut consists of the two BLUE edges

    e_A=a1b1,    e_B=a0b2.

Each perfect matching uses exactly one cut edge, so this is a nontrivial tight cut. Contracting either shore gives a four-cycle, hence a brace. Every edge of the original graph belongs to a perfect matching.

In the S-side block, the matching selecting e_A has one red edge and the matching selecting e_B has zero. Exactly the same is true in the complementary block. Both independent block-count sets are therefore `{0,1}`, whose Minkowski sum is `{0,1,2}`. The count-only knapsack rule accepts t=1, but the original graph has no such matching.

All cut edges are blue, so correcting double-counted red cut edges does not fix this counterexample. The error is incompatible edge identities. The two blocks also have two vertices per side each, so their side sizes sum to 4, not the original 3; the literal additive-size assertion for contraction blocks fails too. This size error alone is not an asymptotic impossibility result.

### 3.2 Correct local recurrence

Preserve the identities of cut edges, including parallel copies after contraction. Let `F_(1,e)(u)` mean that contraction block 1 has a perfect matching with red count u containing the copy of e; define `F_(2,e)(v)` similarly. There is a bijection

    PM(G) <-> {(M1,M2): M1,M2 choose the SAME edge e of the cut}.

The original edge e is duplicated in the pair, so the correct recurrence is

    F_G(t) = OR_(e in cut) OR_(u+v-rho(e)=t)
                 (F_(1,e)(u) AND F_(2,e)(v)).          (2)

Once these forced-edge tables are available, one gluing takes at most O(|cut| n^2) elementary Boolean operations. Equation (2) proves a local repair, not that all required tables on an arbitrary decomposition can be obtained from unconditioned brace ASNC in polynomial time.

Forcing an edge usually deletes its two endpoints or suppresses its competing incident edges. The resulting graph need not be a brace. A block with many child interfaces may require simultaneous compatibility states. Explicitly listing all interface choices can have product-size state space. This is an algorithmic obligation, not a proof that every possible repaired DP is exponential. A valid general reduction needs a uniform polynomial bound on all tables and on how its oracle queries are represented and solved.

### 3.3 Hall-balanced blocks are different

For a partition with `|A1|=|B1|` and no edges from A1 to B2, every perfect matching matches A1 entirely to B1; therefore unconditioned count convolution is valid for those balanced blocks. In a connected matching-covered graph, there cannot also be edges from A2 to B1: those edges would belong to no perfect matching. Consequently such a proper balanced partition does not model the nontrivial tight cut of the connected six-cycle.

The C6 example has strict Hall expansion `|N(U)|>|U|` for every proper nonempty row subset U, but is not a brace. Thus recursively splitting only equality Hall blocks cannot be asserted to terminate in braces. The finite checker verifies both strict Hall expansion and the tight-cut/contraction certificate.

The source manuscript's general Hall-block determinant identity is not refuted by this example. The false bridge is the identification of arbitrary tight-cut decomposition with independent balanced blocks and the resulting unconditioned count DP. No ASNC counterexample follows.

## 4. Binary encoding is the NP-hardness boundary

### 4.1 Elementary SUBSET-SUM reduction

Given positive binary integers `w_1,...,w_r` and target T, create r disjoint K2,2 components. In component h, give one diagonal edge weight w_h and all other edges weight zero. Its diagonal matching has weight w_h, and its off-diagonal matching has weight zero. Independent component choices give

    total matching weight = sum_(h in selected subset) w_h.

The graph has 2r vertices per side and 4r edges; its total binary encoding is polynomial in the SUBSET-SUM input. Thus binary-encoded nonnegative weighted Exact Matching is NP-hard even on disjoint four-cycles, and is in NP. This is the ordinary exact-sum problem, not the red/blue special case. The classical NP-completeness anchor is Karp's [1972 paper](https://doi.org/10.1007/978-1-4684-2001-2_9), whose knapsack decision formulation is the exact subset-sum formulation.

### 4.2 Why the tempting red/blue conversion is pseudopolynomial

An edge of integer weight w can be replaced by a private path of length `2w+1`. Color w of the odd-position edges red and every other edge blue. Internal degree-two vertices permit exactly two matching states: the odd edges cover both original endpoints and contribute w reds, or the even edges cover neither endpoint and contribute zero. This is a correct weight-preserving bijection and preserves bipartiteness.

But this gadget creates `2w` internal vertices. A single weight `w=2^L` uses only L+1 input bits and requires exponentially many explicit vertices. Even the simpler observation that a red/blue matching has at most one red edge per selected edge forces any exact target-preserving gadget for weight w to contain at least w selected edges in that state. A different, non-weight-preserving reduction is not ruled out; it simply has not been supplied by this gadget.

Likewise, changing the matrix entries to `x^w(e)(L+i)^j` makes the x-degree at most `n max_e w(e)`, a numerical rather than binary-input polynomial bound. Uniformly interpolating at degree+1 points is pseudopolynomial. Binary-color U-ASNC neither proves the required weighted noncancellation nor removes this degree cost.

The same warning applies to arbitrary binary-encoded exponent lists in structural theorems: the L-degree is bounded by `sum_j e_j`, which may be exponential in the input bit length. Fast exponentiation alone does not supply a polynomial-size identity-test grid, and evaluating enormous integers exactly is not a unit-cost step. This is a limitation of this explicit algorithm, not a general lower bound against other representations or modular methods.

### 4.3 Fixed label dimension versus growing dimension

For k binary edge labels, positional encoding with base n+1 assigns

    w(e) = sum_(h=0)^(k-1) (n+1)^h b_h(e).

Matching totals uniquely encode the k coordinate counts, each in `[0,n]`. Enumerating all count tuples with the required parities and applying the path construction is polynomial for every fixed k. It gives the previously checked k=2 reduction. Its numerical weights and number of targets grow as `(n+1)^{Theta(k)}`. For `k=Theta(log L)` and polynomial n(L), this particular reduction can be quasipolynomial rather than polynomial. It does not supply the single-exponential-in-k parameter dependence required by a logarithmic-parameter SAT route.

## 5. Honest P-versus-NP consequence and next proof contract

U-ASNC would settle this binary-color bipartite Exact Matching derandomization route. It would not by itself establish P=NP. One additionally needs a deterministic uniform polynomial-size reduction from an NP-complete problem to the exact explicit graph class and encoding solved above. Both directions of correctness, constructor time, graph size, labels/weights, and any promised graph property must be charged.

For perspective, a direct randomized polynomial-time test for binary-color bipartite Exact Matching already follows by retaining an independent variable y_e for each allowed edge:

    Q_t(y) = [x^t] det[x^rho(e) y_e].

Different matchings give different edge monomials with coefficients +/-1. Thus a target fiber is nonempty iff Q_t is nonzero. Over a prime field with more than 2n elements, random edge evaluations miss a nonzero polynomial with probability less than 1/2; the same field has n+1 distinct interpolation points for x, so coefficient recovery is polynomial. A prime of size O(n) can be found by elementary deterministic search and primality checks, using the existence of a prime between successive doubled positive integers. This is a standard algebraic derivation consistent with the classical [MVV matching paper](https://people.eecs.berkeley.edu/~vazirani/pubs/matching.pdf). Therefore a deterministic polynomial reduction from an NP-complete problem to the binary-color problem would imply NP is contained in RP. Since RP is contained in NP, this gives NP=RP. It does not prove such a reduction impossible, and it does not identify RP with P.

The local all-red-rectangle and single-row-boundary results are useful scoped noncancellation theorems. Closing their remaining resonant cases alone does not supply arbitrary masks, arbitrary binary colorings, the brace compatibility reduction, or a SAT compiler. Each is a separate named obligation.

## 6. Reproduction and limits

`check.py` is a newly written standard-library checker. It verifies the C6 matchings, genuine tight cut, contractions, both incompatible and compatible recurrences, strict Hall expansion, exact interpolation formula, determinant-grid fiber detection on bounded small examples, and the SUBSET-SUM gadget bijection. It imports no research code. Finite tests corroborate the explicit certificates, not U-ASNC or any asymptotic theorem.

Run `python check.py` and `python -O check.py`. The proofs of the cost lemma, self-reduction, and encoding barrier above do not depend on experimental success. No public release, repository modification, or merge was performed.
