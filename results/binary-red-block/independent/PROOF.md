# Exact-count nonvanishing when red edges form a proper matching

18 October 2026. Auxiliary sufficient family, not a resolution of ASNC or P versus NP. Historical novelty unassessed.

Let the underlying graph be complete bipartite on n+n labeled vertices. Let a_i be distinct real numbers and e_j distinct nonnegative integers, in their original orders. Put V_ij(lambda)=(lambda+a_i)^e_j. Color exactly k<n edges red, with no shared row or column. Let P_t be the coefficient of y^t in det(y^rho(i,j) V_ij).

Write D=sum_j e_j and m=n-k. For every 0<=t<=k,

 deg P_t = D - m(m-1)/2.

Its leading coefficient is (-1)^(k-t) binom(k,t) epsilon times

 Delta(a_Ic) Delta(e_Jc) / product_{r=0}^{m-1} r!,

where I,J are the red matching's row/column sets, complements use original increasing index order, and epsilon is the signed partial matching cofactor (the sign contributed by selecting all its entries in the determinant). In particular every P_t is nonzero. Offsets need not be positive, and labels need not be reordered. Empty Vandermonde products equal one.

## Generalized translated minor lemma

For q rows with distinct offsets b_i and q columns with distinct nonnegative exponents f_j, the determinant has degree sum f_j - q(q-1)/2 and leading coefficient Delta(b) Delta(f)/product_{r=0}^{q-1} r!.

Proof: introduce z=1/lambda and factor lambda^f_j from column j. Expand (1+b_i z)^f_j = sum_r binom(f_j,r)b_i^r z^r. Cauchy–Binet expresses the determinant as a sum over strictly increasing q-tuples r_0<...<r_(q-1), with coefficient det(b_i^r_l) det(binom(f_j,r_l)) and z-degree sum r_l. The unique minimum sum is q(q-1)/2, at r_l=l. The first determinant is Delta(b); the second is Delta(f)/product l!, because binom(x,l) has degree l and leading coefficient 1/l!. Both are nonzero. All expansions are finite; minimum degree exists even if some binomial entries vanish. This proves the lemma exactly.

## Matching expansion

Let R have V_ij on red edges and zero elsewhere. The colored matrix is V+(y-1)R. Expand the determinant by which red entries use the second summand. Because red edges form a matching, any subset S can be selected. Its contribution is (y-1)^|S| times the signed product of selected entries times the complementary minor of V. The lemma shows its lambda degree is D-binom(n-|S|,2).

Since k<n, the degree for |S|=k strictly exceeds the degree for every |S|<k. There is exactly one subset of size k: all red edges. Its leading coefficient is epsilon times the complementary-minor leading coefficient; selected factors are monic. Extracting any y^t, 0<=t<=k, multiplies this unique top term by (-1)^(k-t) binom(k,t), which is nonzero over the reals. No cancellation with lower subsets is possible.

The assumption k<n matters for this argument: for k=n, subset sizes n and n-1 have the same lambda degree. The argument makes no conclusion in that case.

## Why this is beyond leading parity imbalance

If n-k>=2, swapping the assigned columns of two rows incident to no red edge is a fixed-point-free, sign-reversing involution on each exact-count fiber. Thus its numbers of even and odd permutations are equal. The coefficient of lambda^D vanishes in every fiber. The theorem locates a lower nonzero coefficient instead.

For the first k red diagonal edges and standard a_i=e_i=i, the complement exponents are consecutive. The leading coefficient simplifies to (-1)^(k-t) binom(k,t) product_{r=0}^{n-k-1} r!.

Caution: not all interior fibers have full support. At t=k-1, an edge between distinct marked row and marked column excludes two red diagonals and is impossible. Full support needs a separate proof for 1<=t<=k-2; do not infer it merely from nonvanishing.

## Nonsingular square red-block extension

More generally, suppose every red edge lies in I×J, where |I|=|J|=k<n, and the binary k×k incidence block B is nonsingular. The theorem still holds with epsilon replaced by (-1)^(sum I+sum J) det B.

Indeed expand by red matchings S. No S has size greater than k. All size-k S use precisely I and J, so their complementary minor is identical. Their selected-entry products are monic of identical degree sum_{j in J}e_j. Their signed leading coefficients sum to (-1)^(sum I+sum J) det B, which is nonzero. All smaller red matchings have strictly smaller degree by the same lemma. Hence the top coefficient cannot cancel, and extraction of each y^t again supplies (-1)^(k-t)binom(k,t).

This permits intersecting red edges and multiple red perfect matchings. It applies to arbitrary nonsingular binary blocks, not only unique-match or triangular blocks. Every exact count 0 through k is nonempty, as follows also from its nonzero polynomial. The complement must contain at least one row and column. If n-k>=2, the two unmarked-row involution still makes the leading parity coefficient zero.
