# Result and limits

The remaining tight one-row boundary is now reduced to a smaller explicit simultaneous-resonance regime. This is rigorous scoped progress, not a complete solution.

For the red 1×(n−1) rectangle plus one disjoint red entry, let k=e_c and D=Σe−binom(n−1,2). The middle fiber is exactly the generalized Vandermonde determinant with just entries (i,c),(p,c) set to zero. Its outer two fibers are always nonzero.

The middle fiber has:
- Degree D when the earlier offset product R differs from 1.
- Degree D−1 when R=1 but n e_c≠D.
- Degree D−2 when R=1, n e_c=D, and the mean offset differs from (a_i+a_p)/2.

In particular, the boundary is completely settled for every size when e_c is the smallest or largest exponent, and for every size with consecutive exponents.

The coefficient in the third case contains an explicitly positive centered-exponent-variance gap. The proof is self-contained, including the confluent-alternant calculation and strict positivity.

Still unresolved by this method: n≥5 with R=1, n e_c=D, and mean offset exactly (a_i+a_p)/2. This regime genuinely exists. Exact n5 examples lose the first three, or even first four, highest coefficients but remain nonzero. No strict zero-polynomial counterexample was found or claimed.

Files:
- PROOF.md: complete scoped theorem and remaining gap
- checker/check.py and checker/results.json: 40 exact signed-permutation checks, passed normally and with Python optimization
- independent/: independently derived audit and symbolic determinant checks

No remote writes or publication were performed.
