# Result: one disjoint red entry beyond a red rectangle

The separated-offset nonvanishing result extends to a genuinely nonrectangular family: an all-red `r×(r+q)` rectangle together with one red entry in a different row and column.

For distinct real row offsets, distinct nonnegative integer exponents, `q≥1`, and strict separation of the rectangle's row offsets from all remaining rows:

- If `n≥2r+q+1`, every feasible target `0,…,r+1` has a nonzero coefficient polynomial. Its highest coefficient is one common nonzero constant times the corresponding coefficient of `(z−1)^(r+1)`.
- If `n=2r+q` and `r≥2`, the conclusion still holds. Targets `1,…,r+1` have highest polynomial proportional to `z(z−1)^r`; target zero is exactly the nonzero original rectangle fiber.
- The remaining `r=1,n=q+2` boundary has an explicit leading-order cancellation test. The two leading constants agree precisely when `∏_{s≠i,p}(a_s−a_i)/(a_s−a_p)=1`. Away from that equality, all three targets are proved nonzero. On the equality locus this argument does not settle later coefficients.

The key identity is exact cofactor linearity:

    F_new = F_rectangle
            +(z−1)(Λ+a_p)^(e_c)(−1)^(p+c)F_deleted_minor.

The new ingredient is the elementary loss comparison `κ_deleted≤κ_original+q`. It follows because deleting complementary exponent `e_c` divides each moment weight by `x−e_c`; multiplying the tested symmetric polynomial by `∏(x−e_c)` recovers the original nonzero evaluation at a degree cost of exactly `q`.

A positive-loss certificate checks the theorem beyond generic zero-loss examples: a six-row rectangle with original loss two changes its leading coefficient from `21600(z−1)^2` at degree nine to `20(z−1)^3` at degree fourteen after the added edge.

The smallest presented boundary obstruction is fully evaluated: its one-red polynomial is `−18Λ²−54Λ−42`, so its cubic leading term cancels while the polynomial itself remains nonzero. This is an obstruction to naive leading-term gluing, not a counterexample to nonvanishing.

See `PROOF.md` for complete statements and proofs. Run `python checker/check.py` or `python -O checker/check.py` for the exact standard-library certificates. The prior audited rectangle theorem is included in `../general-omission-20261018/PROOF.md`.

No conclusion about arbitrary colorings or P versus NP is asserted.
