# Independent mathematical audit

19 October 2026. Reviewed PROOF.md Sections 1–7 independently of its checker. No mathematical defect was found in the stated scoped theorems.

The audit checked:

1. Sorting and reflection preserve identically-zero status; extracting the common minimum exponent is legitimate even at a zeroed entry. The root reduction yields a positive-node generalized Vandermonde with exactly one remaining hole.
2. R=1 forces p odd and p>=3. The even-column-rank removed term has negative cofactor sign, so subtracting it strictly increases the determinant. Exact root multiplicity h follows from the nonzero reduced evaluation and the other nonzero row factors.
3. In the c=1 proof, the full Schur polynomial has m variables and length at most m-1. Deleting its constant column changes the smaller partition to (mu_1+1,...,mu_(m-1)+1), yielding exactly the stated product factor and R ratio, with correct cofactor signs. Removing a corner supplies a strictly positive branching term. A consecutive tail is incompatible with exponent resonance.
4. The principal-minor Desnanot–Jacobi identity has the stated positive mixed-minor product, including nonconsecutive sorted index sets. Iterating the ratio inequality proves the strict diagonal-hole result for every strictly totally positive square matrix of size at least two.
5. In n=5, R=1 forces p=3; the only exponent-resonant non-extreme column ranks are 1,2,3, and the three tests cover them. This closes the previous five-row tight boundary only.
6. The explicit n4 signed Laplace dependence is correct and does not give a nonnegative or binary mask dependence.
7. In the remaining n6 case, p=5,c=3. Normalize the two extreme offsets to -1 and 1. The centroid condition makes the interior quartic's cubic coefficient zero; R=1 equates its values at 1 and -1, making its linear coefficient zero. Hence the quartic is even and the four interior offsets occur in opposite pairs. Exponent resonance makes S=6e_3+10 even. Reflection reverses six rows (sign (-1)^15=-1), preserves the two-hole support, and contributes (-1)^S=1 from columns, so the centered masked polynomial is odd. This is a valid reduction, not a nonvanishing proof.

The proof does not establish arbitrary five-row masks, arbitrary colored sparse graphs, the wider nonnegative-kernel conjecture, or any complexity-class conclusion. Finite checker output is corroboration only. A separate infinite-family kernel result is kept outside this frozen package.
