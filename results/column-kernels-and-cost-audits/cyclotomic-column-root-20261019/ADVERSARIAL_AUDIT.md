# Independent adversarial audit of the final endpoint-pole proof

19 October 2026. Reviewed the complete final PROOF.md, including its strengthened full-complex-independence statement. No defect found.

## Mathematical checks

- The background cofactor is exactly a Vandermonde in y_s=(L+a_s)^m after extracting common row powers. The deletion signs give the same fixed prefactor (-1)^(n-1+c) for every R_s. The rational reduction is valid for negative ell as well as nonnegative ell.
- For an ordered pair i<j, the displayed upper-half-plane location satisfies x_i=zeta*x_j with zeta=exp(2 pi i/m). The derivative of y_i-y_j is nonzero there, and the partner residue is exactly -zeta^(-ell) times the first residue. Integer negative powers cause no problem because neither endpoint node is zero.
- Equality of mth powers at a nonreal point cannot involve three distinct real offsets: equal moduli allow only two points on the real-shift line. Thus the relevant endpoint poles are simple with nonzero residues.
- The endpoint isolation argument is stronger than a maximal-active-gap argument and handles all inactive or disjoint-pair collisions automatically. Equal real parts fix the midpoint; the cotangent bound forces a competing pair to have at least the target gap. At a global extreme this is impossible unless the pairs coincide.
- The minimum-endpoint star gives u_j=zeta^ell*u_0 for every j>0. The pair (1,n-1), available because n>=3, gives the additional phase equation. This excludes every phase except 1 over the complex numbers, including the previously retained half-phase exception.
- At phase 1 the weights are constant, and the sum of Laplace terms is the full generalized Vandermonde, nonzero for distinct positive nodes and distinct exponents. This excludes the remaining candidate. No real-weight restriction is required.
- Own-node poles when k<h are real, so they do not affect any of these nonreal equations. The proof therefore correctly avoids a separate negative-ell argument.

## Targeted exact checks

A separately executed raw signed-permutation expansion produced full coefficient rank in six controls: m=3 ordinary phase; m=4 and m=6 half phases; m=6,h=5,k=2 negative half phase; m=3,h=5,k=2 negative phase 1; and a five-row m=3,h=1,k=0 negative phase. These tests found no counterexample and corroborate the algebra, but are not used as proof of the universal theorem.

The final statement must retain m>=3, exact arithmetic-staircase background, distinct real offsets, and only one weighted column. The known m=2 signed dependencies show why an unqualified full-independence claim would be false. Arbitrary residue-class gaps can introduce complex Schur zeros, so this proof does not establish that extension. No arbitrary sparse-graph or complexity-class conclusion follows.
