# Component lemma for orders at most three

This is the complete component argument used by Section 1 of PROOF.md. It is reproduced from the prior [v0.12.0 report](https://github.com/mio-qwq/p-vs-np/blob/8f3f26f624666663ff53a51cf90130ec9fdc3e9a/results/monic-four-gapped/REPORT.md#the-order-at-most-three-lemma-also-holds-over-complex-offsets). The script reference in the historical excerpt names the prior release checker; the current independent audit records its own component checks.

For distinct nonnegative integer exponents and distinct offsets in any characteristic-zero field, every binary masked determinant of order at most three with a perfect matching is nonzero. Here is the complete argument needed by both the structural proof and the finite reductions.

- Order one is immediate.
- A support with an odd number of perfect matchings has a nonzero top coefficient: every supported product is monic of the same total degree, and an odd sum of signs cannot be zero.
- With exactly two matchings, their signs either agree, giving a nonzero top coefficient, or disagree. In the latter case the two monic products cannot be identical, because the multiplicities at the distinct roots −aᵢ are the assigned exponents, which differ between distinct permutations. This covers order two and two-matching order-three cases over any characteristic-zero field.
- The 512 binary 3×3 masks have numbers of perfect matchings 0,1,2,3,4,6 with respective frequencies 265,150,69,18,9,1. Every four-matching mask is the full mask with exactly one entry removed. `check_negative_controls.py` independently enumerates all 512 masks and verifies these assertions.
- For a full k×k determinant, k=2 or 3, write S=Σeⱼ and expand at infinity. Its coefficient at degree S−k(k−1)/2 is

      det[aᵢ^ℓ]ᵢ,ℓ₌₀^(k−1) · det[binom(eⱼ,ℓ)]ℓ,ⱼ₌₀^(k−1)
      = ∏ᵢ<ⱼ(aⱼ−aᵢ) · ∏ᵢ<ⱼ(eⱼ−eᵢ) / ∏ℓ₌₀^(k−1)ℓ!.

  Every higher-degree coefficient vanishes: its expansion uses k nonnegative row powers with sum below 0+1+…+(k−1), so at least two are equal and the associated offset-power determinant is zero. The displayed coefficient is nonzero in characteristic zero. Thus the full order-three determinant has degree S−3, and a full order-two cofactor has degree equal to its exponent sum minus one.
- Deleting one entry from a full 3×3 matrix subtracts that entry times its signed full 2×2 cofactor. This subtracted polynomial has degree S−1 and nonzero leading coefficient, while the full determinant has degree S−3. Cancellation is impossible.

This proof contains no order, positivity, or conjugation argument. It therefore justifies the complex-field use, rather than inheriting a real-only statement without verification.
