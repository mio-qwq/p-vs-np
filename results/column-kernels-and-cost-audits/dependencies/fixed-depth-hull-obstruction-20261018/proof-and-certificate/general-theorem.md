# Root derivation: bounded-depth hull obstruction without character-sum estimates

For integer t≥1 put L=ceil(log2(2t)) and choose m≥2L. Let F=GF(2^m), N=2^m. Rows of K_(N,N) are x∈F. First 2t columns have row label v(x)=(x,x³,...,x^(2t−1)) in F^t identified with F₂^(tm); remaining columns are zero. Target is zero.

## No accepted perfect matching

Such a matching chooses 2t distinct rows x_i. If their vector sum were zero, all odd power sums through 2t−1 vanish. Repeated squaring implies every power sum j=1,...,2t−1 vanishes. Power sum j=0 is also zero since 2t is even in F. The square Vandermonde matrix with columns (1,x_i,...,x_i^(2t−1)) then annihilates the nonzero all-ones vector. Its determinant is the nonzero product of pairwise differences, a contradiction.

## Nonzero trace functionals have large support

All ambient affine binary functionals are c+Tr(Σ_j a_j x^j) over odd j≤2t−1. The trace pairing is nondegenerate over every finite field: the trace polynomial is nonzero of degree 2^(m−1)<N, so trace is not identically zero; multiplication by any nonzero a is bijective.

The odd integers j<2^L have mutually disjoint full Frobenius orbits modulo N−1. Multiplication by 2 modulo N−1 rotates an m-bit string. If a nontrivial rotation r gives an odd integer j'<2^L, the bit at a=m−r of j must be 1. Hence 1≤a≤L−1. But the bit at zero of j is 1 and rotates to r=m−a≥L+1, contradicting j'<2^L. Thus no nontrivial rotation can map one of these odd exponents to another (including itself).

Consequently the expanded trace polynomial Σ_j Σ_(r=0)^(m−1) a_j^(2^r) X^((j2^r) mod(N−1)) has pairwise distinct exponents, all between 1 and N−2. It is a nonzero degree-<N polynomial whenever a coefficient a_j is nonzero, and adding a constant cannot cancel it. Thus the resulting nonzero ambient affine functional is a nonzero Boolean function on F.

In binary coordinates, x↦x^(2^i) is linear and x^j is a product of popcount(j) such linear maps. Therefore this Boolean function has algebraic degree at most L. Every nonzero Boolean polynomial on m variables of degree≤L has weight≥2^(m−L). Elementary induction: write P=P0+x_m P1. If P1=0, weight doubles the weight on m−1 variables. If P1≠0, at each point where P1=1 exactly one of P0 and P0+P1 equals1, so wt(P)≥wt(P1)≥2^((m−1)−(L−1)). Handle L≥m by the trivial bound1. Hence support≥2^(m−L)≥2^L≥2t.

Deleting at most2t−1 rows therefore leaves v(x) with full affine span F₂^(tm).

## All conditioning through depth 2t−1 fails

A partial matching P of h≤2t−1 edges fixes s≤h special columns. Among N−h surviving rows, exactly r=2t−s special columns remain, with 1≤r<N−h. The last inequality holds since N>2t+h−s; our m≥2L gives N≥(2t)²>4t−1 for t≥2, while t=1 gives N≥4>3.

For any affinely full set A and 1≤r<|A|, its r-subset sums affinely span the entire vector space: differences of two subsets sharing r−1 entries realize every pair difference a+b. Every r-subset of surviving rows occurs as the special-column rows of a perfect extension. Thus attainable total signatures conditioned on P have full affine hull, even though zero is unattainable.

For every fixed test depth d, choosing t=ceil((d+1)/2) yields 2t−1≥d and an infinite family in m, with k=tm=O_d(log N). This refutes completeness only of the specified fixed-depth conditioned affine-hull tests. It supplies no P-vs-NP separation, and no novelty claim about the standard finite-field/coding-theoretic ingredients. Independent verification requested.
