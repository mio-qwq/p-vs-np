# Independent audit of the one-row-boundary proposition

19 October 2026. Audited the current `../PROOF.md` independently of the parent checker. No mathematical error was found in the stated sufficient conditions, coefficient formulas, positivity argument, or two printed exact examples. The stated limitation is essential: the simultaneous-resonance regime is not settled by this proposition.

## Symbolic checks

1. **Mask reduction and signs.** In a permutation, the row receiving column c uniquely determines the red count: i gives 0, p gives 2, and any other row gives 1. Hence P₁ = det V − Tᵢ − Tₚ exactly. The signed deleted Vandermonde identity gives Lₚ/Lᵢ = −R when all retained lists keep their original order. This verifies the sign in formula (2).

2. **Formula (3).** Symmetry and homogeneity of the normalized Schur polynomial give βₛ = (d/m)(A−aₛ)+kaₛ. Therefore βᵢ−βₚ = (k−d/m)(aᵢ−aₚ). With R=1 the deleted contribution is Lᵢ times this difference; subtracting it gives exactly the minus sign in (3). Since the full determinant has degree D−m and m≥2, it cannot affect that coefficient.

3. **Formula (4).** Write B=Σaₛ². Expanding Qₛ independently gives

   Qₛ = constant + (k²−β) A aₛ + [k(k−1)/2−k²−α+β] aₛ².

   The displayed derivative identities (10) reduce this to

   Qₛ = constant + v A aₛ − nv aₛ²/2.

   Thus Qᵢ−Qₚ = v(aᵢ−aₚ)[A−n(aᵢ+aₚ)/2], exactly (11), and subtracting the deleted contribution gives (4). For n≥4, D−m < D−2, so the full determinant cannot alter this coefficient.

4. **Variance normalization.** The confluent formula (12) is correctly normalized: the coefficient of (x−1)^(m−1) in Σx^b/f′(b) equals 1/(m−1)!, so its right-hand side tends to 1. Expanding the falling factorial of order m+1 gives the stated E₂ and α. Independent symbolic simplification in `audit_checker.py` verifies identity (13) identically in m,B₁,B₂. The denominator m(m²−1) in v is correct; replacing it by m²−1 would introduce a factor-m error.

5. **Strict positivity.** The variance identity in (14), the integer-spacing lower bound, and its equality case are correct. Equality in the sum forces every pairwise gap to be minimal, equivalently bₕ=b₀+h. At resonance d=mk, this forces b₀=k, impossible because k is excluded from the cofactor exponent list. Therefore v>0 at resonance, as required. Outside resonance, v=0 is possible and is not incorrectly excluded.

6. **Degree and ordering details.** Distinct nonnegative integer exponents imply S≥n(n−1)/2, hence D≥n−1; the degree indices used in the proposition are nonnegative. Sorting the cofactor exponents changes numerator and leading constant by the same sign, so the Schur normalization remains valid for unsorted original exponent lists. The proof itself does not require extremality of aᵢ, consistently with its stated extension.

## Exact independent checker

`audit_checker.py` computes determinants and every column-c Laplace term by signed permutation expansion in the exact ring Q[Λ]. It does not import the parent checker. It checks (2), (3), (4), all first normalized cofactor corrections, all second normalized cofactor corrections at resonance, v, and the full determinant degree and leading coefficient. A reversed row/column case checks ordering signs.

Run:

    python independent/audit_checker.py
    python -O independent/audit_checker.py

Both commands were run successfully. All checks use explicit `require` calls that raise on failure, so optimization cannot disable them. All seven cases passed in both modes, including:

- Formula (3): n=4, a=(0,1,2,3), e=(0,1,2,3), i=0,p=3,c=0; D=3, deg P₁=2, v=0.
- Formula (4): n=5, a=(0,1,2,4,6), e=(0,1,2,3,5), i=0,p=3,c=1; D=5, deg P₁=3, v=2/15.
- Printed n=4 residual example: P₁=12(2Λ+3).
- Printed n=5 residual example: P₁=−480480(49Λ²+446Λ−1680).

A harmless scope observation: for n=4, R=1 already forces A=2(aᵢ+aₚ), so the strict noncentering hypothesis in item 3 cannot occur in that size. This does not invalidate the statement; n=4 is included to make the degree comparison uniform.

## Additional stress test, kept separate from the proof

The exact offset/exponent choice

    a=(0,2,4,14,15), i=0,p=3,
    e=(0,7,10,17,22), c=2, k=10

satisfies all three residual equalities. Here the main proof's D is **50**. Direct signed expansion gives:

- The coefficients of degrees 50,49,48,47 in Tᵢ+Tₚ all vanish.
- deg(det V)=46, with leading coefficient 990593604000000.
- deg(Tᵢ+Tₚ)=46, with leading coefficient 447990903360000.
- deg(P₁)=46, with leading coefficient 542602700640000.

Thus merely extending the displayed tests by one more leading-coefficient check would still leave genuine cases. This is an exact nonzero polynomial example, not a zero-polynomial counterexample, and no unproved cumulant formula is used to certify it.

The full middle-fiber coefficient list is in `residual_stress_test.json`. Its SHA-256, under the encoding specified in that file, is:

    be7a3c0c265e30ad70ca0bcaf93ce39a84704f08ea28ff710e92cb9906fd1b74

Rebuild it with `python independent/save_stress_certificate.py`.
