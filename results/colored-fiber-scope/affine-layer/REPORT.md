# Affine closure does not characterize binary exact-count fibers

18 October 2026. Bounded audit of Remark 2.9 in Yuefeng Du, arXiv:2604.01571v3.

## Result

The correct finite-configuration theorem is:

> A nonempty subset of the permutation matrices is closed under affine span within that configuration if and only if it is a single equality layer for some **integer-valued cost matrix**.

The corresponding statement with **binary costs** is false. An explicit seven-permutation family in S4 below is affine-closed and is a layer of a matrix with entries only 0, 1, 2. It cannot be an exact-count fiber for **any binary-colored graph on the same labeled vertices**. Its union of edges is all of K4,4, so deleting edges cannot repair the failure. A three-value pigeonhole argument proves the obstruction without exhaustive search.

This refutes the identification of the affine-closed domain with the binary exact-count domain. It does **not** refute binary ASNC: the family's polynomial is nonzero, with leading coefficient 1. It also does not establish or refute the stronger nonvanishing assertion over all affine-closed families.

## 1. What the source says, and the missing restriction

The source's Theorem 2.7(ii) defines W as a matrix in {0,1}^(n x n). Remark 2.9 then claims that every proper affinely closed permutation subset is a full equality layer, and uses that claim to identify ASNC with nonvanishing over all nonempty proper affinely closed subsets.

There are two different readings:

1. If the equality-layer matrix W may be arbitrary real, rational, or integer valued, the representability claim is correct. The proof below even gives integer costs.
2. If W must remain binary, as in the preceding definition and actual red/blue ASNC, the claim is false. Section 3 gives a counterexample that also rules out choosing a different underlying support graph.

Consequently, the asserted equivalence with binary ASNC does not follow from the stated affine-closure observation. An additional reduction preserving the relevant polynomial would be required. This audit does not claim that two conjectures with different domains cannot happen to have the same truth value; it refutes the proposed identification of their input families.

The already-audited sliced-polytope error in Theorem 2.7(iii) is separate. None of the arguments here identifies the permutation points of a hyperplane slice with all its vertices or assumes that slicing cannot create fractional vertices.

Source: [v3, Section 2.4, Theorem 2.7 and Remark 2.9](https://arxiv.org/html/2604.01571v3#S2.SS4). The complete preserved primary-source text and HTML were inspected locally.

## 2. The correct integer-cost theorem

Let A be a finite rational point configuration. For nonempty S contained in A, define its configuration-relative affine closure by

    cl_A(S) = A intersect aff(S).

Then the following are equivalent:

1. S = cl_A(S).
2. There is a rational affine functional ell with S = {p in A: ell(p)=0}.
3. After clearing denominators, there is an integer affine functional with the same zero set in A.

For permutation matrices, an integer affine functional has the form

    ell(P) = <W,P> - t,

with integer W and t. No binary restriction follows.

### Proof

An equality layer is affine-closed because its affine hull remains in the defining hyperplane.

Conversely, suppose S is affine-closed and put L=aff(S). Since S is rational, the vector space V of rational affine functionals vanishing on L has a rational basis ell_1,...,ell_k. For every q in A outside S, q is outside L, so at least one ell_j(q) is nonzero. Thus

    f_q(z) = sum_(j=1)^k z^(j-1) ell_j(q)

is a nonzero polynomial. There are finitely many such q and finitely many roots to avoid. Choose an integer z avoiding all these roots. The rational affine functional sum_j z^(j-1) ell_j vanishes at every point of S and at no other point of A. Clear its denominators.

If S=A, the zero functional works directly. If S is proper, the construction gives a nontrivial equality condition on A. Adding a sufficiently large constant to every entry of an integer cost matrix, while adding n times that constant to the target, also makes all its entries nonnegative without changing its permutation layer.

### Relation to graph fibers

Every binary graph fiber is affine-closed in the **full** permutation configuration: an affine combination preserves both the color-count equation and all zero coordinates outside the graph. Thus a resulting permutation matrix cannot acquire a forbidden edge.

A binary graph fiber can also be represented by an integer full layer directly: keep its 0/1 costs on graph edges and put n+1 on every nonedge. For a nonempty target in {0,...,n}, every permutation using a nonedge then has cost larger than the target. This does not give a binary full layer, and the next example shows why the integer qualification matters.

## 3. An explicit full-support counterexample at n=4

Rows and columns are labeled 0,1,2,3. Let

    W = [[1,2,2,2],
         [2,1,0,0],
         [2,1,0,2],
         [1,1,2,0]],
    t = 4.

The complete cost-4 layer in S4 is exactly

    S = {(0,2,3,1),
         (0,3,1,2),
         (1,0,2,3),
         (1,2,0,3),
         (2,3,1,0),
         (3,1,2,0),
         (3,2,1,0)}.

Tuples give the selected column in each row. The checker verifies all 24 costs exactly, and every one of the 16 row-column pairs occurs in at least one listed permutation.

Being a full integer equality layer makes S affine-closed immediately. Its full support also means that any graph whose exact-count fiber were S would have to contain every edge of K4,4. Therefore it suffices to rule out a binary cost matrix on K4,4.

### A structural impossibility proof for binary costs

Suppose a real matrix B has the same cost on all seven members of S. Normalize away row and column potentials by setting

    Q_ij = B_ij - B_i3 - B_3j + B_33.

The last row and column of Q are zero. This operation shifts every permutation cost by the same constant, so it preserves equality layers.

Write the upper-left 3 by 3 entries as q_ij. The seven common-score equations are

    q00+q12 = q00+q21 = q01+q10+q22
            = q01+q12+q20 = q02+q21
            = q11+q22 = q12+q21 = T.

Setting a=q20, b=q21, and c=q22, these equations give

    Q = [[b,     b-a,  b, 0],
         [a+b-c, 2b-c, b, 0],
         [a,     b,    c, 0],
         [0,     0,    0, 0]],
    T = 2b.

The following six permutations are outside S. Their normalized costs minus T are:

- (1,2,3,0): -a
- (0,1,2,3): b
- (1,0,3,2): -c
- (2,3,0,1): a-b
- (2,0,3,1): a-c
- (0,1,3,2): b-c

For S to be the **entire** equality layer, each of these differences must be nonzero. Hence the four numbers 0,a,b,c must be pairwise distinct.

Now assume B is binary. Let d_j=B_2j-B_3j. Every d_j belongs to {-1,0,1}, while

    (a,b,c,0) = (d_0-d_3, d_1-d_3, d_2-d_3, 0).

There are four d_j but only three possible values. Two must agree. Therefore two of 0,a,b,c agree, and one of the six excluded permutations has cost T. This contradiction proves that no binary matrix has exact layer S.

This proof establishes the requested separation without relying on the computer enumeration. In fact, it applies whenever the four differences between rows 2 and 3 take at most three values.

### Brace and polynomial boundaries

The forced support K4,4 is a brace under the intended 2-extendability interpretation. This does not turn S into a binary ASNC input: no binary coloring produces it. The earlier source typo in its unrestricted Hall+2 quantifier is not used here.

Four members of S are even and three are odd, so the leading coefficient of P_S is 1. Exact expansion gives

    P_S(lambda) = lambda^6 + 14 lambda^5 + 64 lambda^4
                  + 129 lambda^3 + 130 lambda^2 + 86 lambda + 42.

Thus S is not a zero-sum family and is not an ASNC counterexample. This note makes no claim that seven is the minimum cardinality needed for a full-support separation, and it does not enlarge or rerun an ASNC nonvanishing search.

## 4. What can be said about the source's n=5 zero-sum subset

Remark 2.9 mentions unions H disjoint-union H-up at n=5. The discussion following Theorem 2.10 asserts that a 24-element zero-sum subset is not affine-closed and that its 96-element affine closure has a nonzero polynomial.

However, the preserved complete v3 text and HTML do not define that H/H-up construction or list the 24 permutations. The occurrence of H-up is only the mention in Remark 2.9. Therefore the specific family is not identified well enough in these materials to independently verify the claimed 24/96 calculation. The earlier source audit also records that the linked formalization repository returned HTTP 403; this audit did not bypass that restriction or run any repository code.

Accordingly:

- The 24-element and 96-element statements are reported as **source assertions**, not independently certified facts.
- If the source's claimed lack of affine closure is correct, it alone excludes that subset from every exact-cost fiber on these same vertices, whether costs are binary, integer, or real and whatever support graph is chosen.
- Nonvanishing of that particular affine closure would not prove nonvanishing for every affine-closed family.
- Neither the source's unspecified zero-sum subset nor this note's explicit nonzero seven-permutation example is an actual binary ASNC counterexample.

The bounded audit stops here rather than inventing an identification of the source family or escalating to an exhaustive n=5 ASNC search.

## 5. Exact checks and controls

Run `python check.py` and `python -O check.py` in this directory. The checker uses only the Python standard library and explicit integer/rational arithmetic. It contains no `assert` statements, so optimization does not disable checks.

It verifies:

1. The integer matrix has precisely the seven stated cost-4 permutations and their union contains all 16 edges.
2. The six constancy equations have exact rank six, and the displayed three-parameter normal form spans their nullspace.
3. All six excluded-permutation cost identities.
4. All 65,536 binary matrices independently. Exactly **174** give the seven selected permutations a common cost; every one admits at least one additional matching at that cost. There are 14 distinct resulting layers.
5. The exact polynomial coefficient vector.
6. Positive controls: the integer matrix realizes S, and the all-zero binary matrix realizes the full permutation family.
7. A deliberately altered integer certificate is rejected with a nonzero exit code; its failure is recorded in `negative-control.txt` and is reproduced by `../verify.py`.

The binary-layer-size histogram is:

    size 8: 4 matrices
    size 10: 12
    size 11: 6
    size 12: 12
    size 13: 10
    size 14: 60
    size 16: 40
    size 24: 30

The normal and optimized outputs agree on every mathematical field. The structural pigeonhole proof is primary; this tiny exhaustive domain check corroborates its concrete certificate and is not a polynomial-nonvanishing search.

## Sources and artifact boundaries

- Primary source: Yuefeng Du, [arXiv:2604.01571v3, Section 2.4](https://arxiv.org/html/2604.01571v3#S2.SS4), particularly Theorem 2.7, Remark 2.9, and Theorem 2.10.
- Related support-mask audit: [REPORT.md](../support-mask/REPORT.md). Support-mask representability and binary-cost representability are different questions.
- The explicit seven-permutation candidate was independently checked by the accompanying exact checker and the normal-form/pigeonhole proof above.
- `certificate.json` is the self-contained exact input. It contains only the matrix, target, and permutations required by `check.py`.
- `check-normal.json`, `check-optimized.json`, and `negative-control.txt` record the finite checks. The package verifier reproduces them in temporary storage.

The mathematical argument is a structural proof supported by exact integer/rational arithmetic. This is an AI-assisted research audit, not human peer review, Lean verification, or another proof-assistant certification. No historical novelty claim is made.
