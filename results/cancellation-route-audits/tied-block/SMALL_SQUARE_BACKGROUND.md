# An all-red square-block extension

18 October 2026. This addendum proves a singular-block sufficient family left outside the nonsingular-incidence theorem. Complete underlying graph; no general ASNC or complexity claim; novelty unassessed.

Keep V_ij=(lambda+a_i)^e_j with distinct real offsets a and distinct nonnegative integer exponents e. Let exactly the edges I×J be red, with |I|=|J|=k and 1<=k<=floor(n/2). Set E=sum e and m=n-k. For every 0<=t<=k,

 deg P_t=E-binom(k,2)-binom(m,2).

Its leading coefficient is

 (-1)^(sumI+sumJ+k-t) binom(k,t)
 * [Delta(a_I)Delta(e_J)/product_{r=0}^{k-1}r!]
 * [Delta(a_Ic)Delta(e_Jc)/product_{r=0}^{m-1}r!].

All subsets retain original increasing index order. Every factor is nonzero. Thus each target 0,...,k is feasible and its exact-count polynomial nonzero. For k>=2 the binary red block is the singular all-ones matrix; this case is genuinely outside the previous nonsingular-block hypothesis.

## Proof

Let R coincide with V on I×J and vanish elsewhere. Generalized Laplace expansion of det(V+(z-1)R) has terms indexed by equally sized sets I' subset I and J' subset J, size s<=k:

 (z-1)^s (-1)^(sumI'+sumJ') det V[I',J'] det V[I'^c,J'^c].

Apply the proved generalized translated-minor degree lemma to both determinants. Every term of size s has degree

 d_s=E-binom(s,2)-binom(n-s,2).

For s<k<=floor(n/2), d_(s+1)-d_s=n-2s-1>=1. Thus all smaller s have strictly smaller degree. At s=k there is exactly one selected pair (I,J). Its leading coefficient is the signed product of the two minor leading coefficients. Taking `[z^t](z-1)^k` multiplies by (-1)^(k-t)binom(k,t). This proves the claim without cancellation assumptions.

The range k<=floor(n/2) is used essentially by this proof. For odd n and k=(n+1)/2 the last degree increment is zero, so several selected subsets can contribute at the maximal degree. No claim about those tied sums is made here.

## Boundary check

For n=4, k=2, I=J={0,1}, a_i=e_i=i, E=6 and both Vandermonde factors are 1. The degree is 4 and the leading coefficient at t=1 is -2. Indeed the previously checked polynomial is -2lambda^4-12lambda^3-38lambda^2-60lambda-24. That example falsifies application of the nonsingular-block degree-5 formula to a singular block; it is consistent with, and explained by, the present formula.

For n=6, k=3 with the first 3 rows/columns red and standard labels, E=15; degree 9; each three-by-three minor leading coefficient is 2. Hence target t=1 has leading coefficient 12. The parity-involution using two blue-only rows remains applicable, so nominal degree-15 parity balance does not decide this example.

The remaining research boundary is general singular incidence blocks and red supports with several tied maximal-degree selected pairs. The source's general claim has not been established by these sufficient families.
