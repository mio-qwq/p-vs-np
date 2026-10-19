# Status and scope

18 October 2026.

## Established

The accompanying proof establishes the first-differing-moment leading-coefficient formula for the structured red rectangle `n=2r+2`, `|I|=r`, `|J|=r+1`, with arbitrary distinct real row offsets and distinct nonnegative integer exponents. All coefficients above its candidate degree vanish. The candidate is the actual leading coefficient whenever its offset factor is nonzero.

Strict separation of the two row-offset blocks guarantees nonvanishing. Standard consecutive rows with the first `r` selected satisfy this condition and admit the exact closed form `q_l=(r+1)^l/l!`. Each feasible red-count fiber has the same proved degree and a nonzero signed binomial leading coefficient.

The [independent audit](audit/AUDIT.md) accepts the final frozen proof. It checked the signs, factorial normalization, boundary cases, lower-layer rank bound, positivity argument, and formal-series closed form. It identified and repaired an initially insufficient justification of the additional `k=3` lower-layer statement; the final proof includes the refined rank count. The audit also rederived complete polynomials without importing the producer's expansion routines.

## What changed from the earlier rectangular obstruction

The earlier calculation showed that the leading maximal-Laplace coefficient can cancel. For standard `n=8` rows with `J={0,1,6,7}`, the next coefficient survives at degree 14. The present theorem determines the first possible survivor from the first differing exponent moment throughout the equal-halves rectangular family, and proves nonvanishing for separated row blocks.

For `n=8`, `J={0,3,5,6}`, two moments agree and the exact degree is 13, with coefficient `−37324800(z−1)^3`. Included examples reach `k=4` and `k=5`; the latter has `n=10`, degree 65, and coefficient `20071103433434726400000(z−1)^4` for the stated standard-row exponent partition.

## Limitations

Distinctness alone does not ensure a nonzero offset factor. The included `n=6` irrational and integer `q_2=0` examples have actual degree 7 rather than the candidate degree 9. Every target fiber in these examples is nevertheless nonzero. They are not ASNC counterexamples.

The all-offset nonvanishing problem outside the sufficient conditions is not settled by this theorem. Arbitrary binary colorings, general ASNC, and P versus NP remain unresolved. These materials make no novelty, human-peer-review, or proof-assistant-verification claim. Finite computations support the proof only within their explicitly recorded cases.

Historical source paths in the preserved audit source manifest identify original records. The package's canonical inventory and executable verification are self-contained.
