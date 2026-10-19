# Independent proof and algorithmic-certificate audit

19 October 2026. Reviewer: the constructive algorithm/certificate auditor.

## Proof verdict

The final endpoint-pole proof is correct. I independently checked the Vandermonde deletion sign; the upper primitive-root pole and derivative; the partner residue ratio for every integer ell; the horizontal-line equal-modulus observation; the extreme-endpoint pole isolation argument; and the resulting three endpoint equations. The isolation step excludes all other pair/root collisions, not merely collisions involving the same primitive root. Negative ell creates only real own-node poles and therefore cannot interfere. The argument proves full complex independence, including the former half-phase case.

The remaining constant-weight possibility when zeta^ell=1 is excluded by the nonzero full generalized Vandermonde. The Rolle induction quoted in the proof justifies its positive-node nonsingularity. Column sorting is explicit, so the common sign convention is unambiguous.

## Independent exact checker

`check.py` is a self-contained standard-library program using integers and `fractions.Fraction`. It constructs all Laplace terms by raw signed permutation expansion, without using the root-of-unity theorem. It then independently checks their staircase Vandermonde factorization. For each case it selects a full-size coefficient minor and computes its exact nonzero determinant. These explicit minors certify the reported ranks over Q and hence over C.

Eight deliberately chosen cases cover m=3; m=4 and m=6 half phases; a negative exponent difference; the unit-phase branch; rational offsets; a common shift; and a three-row negative half phase. For each selected coefficient minor, the checker also solves the transposed rational system and verifies that the resulting coefficient functional has value exactly one on every T_s. These dual coefficients are included in `results.json`. Both `python check.py` and `python -O check.py` pass. Their outputs are `check-normal.log`, `check-optimized.log`, and `results.json`. The program does not rely on floating-point ranks or on `assert` statements removed by optimization.

Raw permutation expansion has factorial cost in n. It is used here only for small independent certificates, and is not the algorithm asserted in the next paragraph. The finite cases do not prove the universal theorem.

## A rational dual certificate follows without complex-number computation

For rational offsets, write the coefficient matrix of the T_s as C, with one column per row index s. The theorem gives rank(C)=n. Hence there is a rational coefficient functional y satisfying

    C^T y = (1,...,1)^T.

One explicit construction is to select n independent coefficient rows, solve the resulting transposed n-by-n system against the all-ones vector, and set every other functional coefficient to zero. This supplies a strictly positive functional on every T_s, with value exactly one. More generally the same left inverse recovers every constant column weight from the resulting polynomial. It is not necessary to represent the cyclotomic poles numerically or symbolically to obtain these certificates.

Put

    S=(n-1)h + m(n-1)(n-2)/2 + k.

All raw Laplace polynomials have degree at most S. If rational offset numerators and denominators have at most b bits, their coefficients have bit length polynomial in n, S, and b: clear offset denominators, expand translated monomials, and bound a determinant numerator by n! times products of coefficient bounds. The same coefficients can be formed in polynomial bit cost using exact determinant evaluations on S+1 integer shifts followed by interpolation; the defining raw permutation expansion is unnecessary. Interpolation denominator lengths are O(S log(S+2)), so this is an explicit degree-bounded procedure, not an assumed deterministic PIT oracle.

Exact Gaussian elimination then selects independent rows. If input coefficient entries have numerator/denominator bit length at most H, clearing denominators and applying the determinant/Cramer bound gives polynomial-size rational solution entries, conservatively O(n^3(H+log(n+2))) bits. Thus the dual certificate is constructible in deterministic bit cost polynomial in n, S, and b.

The degree dependence is essential: this is not polynomial in the bit length of arbitrarily large binary-encoded exponents. Nor does the certificate solve arbitrary independently masked columns. Its scope remains the exact arithmetic staircase with one weighted column; there is no P=NP or P!=NP consequence supplied here.

## Status

No open defect from this review. The distinct contributions in the proof's provenance describe one collaboratively consolidated theorem. No historical novelty or remote-publication claim is made.
