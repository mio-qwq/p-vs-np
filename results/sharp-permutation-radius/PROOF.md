# Sharp fixed-point testing radius for permutation polynomials

Research draft, 17 October 2026. Historical novelty has not been established.

## Statement

Let K be any field. Evaluate polynomials in the n^2 matrix entries on permutation matrices P_sigma, where sigma belongs to S_n. For n>=2 and integer d>=1, the least integer R such that every polynomial of total degree at most d which is not identically zero on these matrices has a nonzero evaluation at a permutation moving at most R points is

    R = min(n, 2d+1).

For d=0, or n<=1, radius zero suffices and is optimal. This is a statement about polynomial evaluations on the full symmetric group, not arbitrary sets of allowed matchings.

Derksen, The Graph Isomorphism Problem and approximate categories, Journal of Symbolic Computation 59 (2013), Lemmas 2.7--2.9, proves the established sufficient radius 3d by disjoint-transposition arguments. The argument below refines the minimization criterion and supplies matching lower examples. No claim that the refinement is previously unpublished is made.
Source: https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.38.pdf

## Upper bound

Suppose f has a nonzero evaluation. Choose such a permutation sigma minimizing, in lexicographic order, first its number k of moved points and then its number c of nontrivial cycles. If k<=2d+1 we are done.

Assume k>=2d+2. In each even nontrivial cycle, pair its vertices consecutively along the cycle, covering all vertices. In each odd nontrivial cycle, do the same except leave one vertex unpaired. Pair these leftover vertices across distinct odd cycles, leaving at most one vertex unpaired overall. There are exactly floor(k/2)>=d+1 disjoint vertex pairs. Call a pair internal if its vertices were adjacent in one original cycle, and cross if its vertices were leftovers in two different odd cycles. Each original odd cycle participates in at most one cross pair.

Select any d+1 of the pairs and swap the corresponding pairs of matrix rows independently. Every resulting Boolean-cube vertex is a permutation matrix. The row pairs are disjoint, so the resulting matrix is an affine-linear function of the d+1 toggle bits: start with P_sigma and add, for each activated pair, its fixed row-swap difference. Consequently the restriction of f to this cube has total degree at most d. Its (d+1)-fold alternating finite difference is zero over K, including characteristic two.

Every nonempty toggle subset has zero f-value by the minimal choice of sigma:

* If it contains an internal pair, that row swap fixes at least one formerly moved point. Indeed if sigma(a)=b, swapping rows a,b makes row b map to b. Other toggles touch disjoint rows, so cannot undo that fixed point. No originally fixed row is touched. Thus the moved-point count strictly decreases.
* If it consists only of cross pairs, each swap joins two distinct original odd cycles into one nontrivial even cycle. The paired original cycles are disjoint across the selected swaps. No fixed point is created or lost, while the number of nontrivial cycles strictly decreases.

The alternating cube identity would therefore have its sole nonzero term at the untoggled vertex, with coefficient +1 or -1. This contradicts f(P_sigma)!=0. Hence k<=2d+1. The bound n is automatic.

## Sharp lower examples

First suppose n>=2d+1. Fix a subset S of 2d indices and define

    q(X) = Pf((X-X^T)[S,S]).

This is a polynomial of degree d with integer coefficients, so it is defined over every field, including characteristic two (the skew matrix is alternating there as well).

It vanishes on every permutation moving at most 2d points. If such a permutation fixes an index in S, the corresponding row and column of the skew principal submatrix are zero. Otherwise every index in S moves; the support bound forces exactly S to move and all outside indices to be fixed. Then S is invariant, its permutation submatrix has every row and column sum one, and the skew difference has the nonzero all-ones vector in its kernel. Its determinant is zero. The polynomial identity det(A)=Pf(A)^2 for an even alternating matrix implies Pf(A)=0 over the field.

On a single (2d+1)-cycle containing S and one outside index, with every other point fixed, removing that outside index leaves a skew adjacency matrix of a path on 2d vertices. The path has a unique perfect matching and all its edge entries are +1 or -1, so q evaluates to +1 or -1, which is nonzero in every field. Thus radius 2d fails.

For smaller n, sharpness at radius n is as follows. If n=2r is even and r<=d, the degree-r monomial

    product over i=1,...,r of x_(2i-1,2i)

can be nonzero only if every odd row moves. Every even column is then occupied by its paired odd row, so every even row moves too. The permutation of disjoint paired transpositions gives value one. If n=2r+1 is odd with r<=d, use the preceding Pfaffian construction on n-1 indices; it vanishes whenever fewer than n points move and is nonzero on an n-cycle. These cover n<=2d+1. Constant polynomials and the trivial groups supply the stated edge cases.

## Algorithmic consequence and limits

A k-bit parity target t on complete bipartite perfect matchings is detected over GF(2) by

    product over j=1,...,k of (1 + L_j(X) + t_j),

where L_j is the linear parity label sum. Thus it suffices to enumerate permutations moving at most min(n,2k+1) points. There are at most n^(2k+1) such permutations for fixed k, by choosing a support superset and its permutation. Labels can be evaluated from the identity label using only changed rows. This is deterministic polynomial time for each fixed k (XP, not an FPT or uniform general polynomial bound). The sharp radius does not assert optimal algorithmic running time.

For arbitrary missing-edge graphs, the row-swap cube need not remain inside the allowed matching domain. No such transfer is claimed. No conclusion about P versus NP follows. This draft is mathematical proof, not Lean/formal verification or human peer review; independent audit and historical comparison remain required.
