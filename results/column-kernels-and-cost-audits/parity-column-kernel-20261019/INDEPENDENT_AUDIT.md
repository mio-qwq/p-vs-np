# Independent audit of the parity-background column theorem

19 October 2026. Reviewer: the constructive algorithm/certificate auditor, independently of the theorem author. This audit concerns the local `PROOF.md` and reviewed `check.py`; it is not a claim about arbitrary support noncancellation or a complexity-class separation.

## Verdict

The proof establishes the stated three-case theorem. A harmless ordering convention identified during review is now explicitly resolved in Section 1: sort the columns before defining c and the background list. Reordering columns first multiplies all signed Laplace terms by the same permutation sign and therefore preserves their constant kernel. I checked the amended wording; equation (1)'s fixed sign is correct under that convention.

## Independently checked mathematical points

1. Write the increasing background powers as `h+2g_j`. Their normalized exponents include zero. The alternant partition therefore has final part zero and length at most `n-2`. Factoring the row powers and the squared-node Vandermonde gives the displayed rational representation, with the preceding ordering convention.

2. At a pair midpoint, the two distinguished squared nodes are the same strictly positive number. The remaining squared nodes are nonnegative and at most one is zero. Thus each retained Schur specialization has at least `n-2` positive variables. Since the partition length is at most `n-2`, at least one semistandard-tableau monomial is strictly positive; all are nonnegative. This proves the needed strict positivity even when other squared nodes repeat. Distinctness of the original offsets excludes any additional denominator zero in an individual pair residue.

3. With `d=(a_s-a_t)/2`, differentiation gives `d/dL (y_s-y_t)=4d`. Direct substitution gives the residue `d^(ell-1) S_st/(4D_st)` and the partner ratio `(-1)^(ell+1)`, including negative integer ell. These residues are nonzero. Different colliding pairs are disjoint, but their individual contributions need not be discarded; the proof accounts for them.

4. At the midpoint of `a_0` and `a_r`, any other equal-sum pair uses only indices below r. If ell is negative, an own-node pole at that same location also has an index strictly between 0 and r. Therefore the minimal-active-index argument eliminates both ordinary pair-pole collisions and possible higher-order own-node poles. It does not rely on generic or distinct pair sums.

5. For `k<h`, the cofactor of `T_0` at `L=-a_0` is a nonzero generalized Vandermonde on strictly positive distinct nodes. Its exact lowest order is k. All other terms have order at least h. This forces the first weight to vanish. The unique first pair pole then forces the second to vanish, and the minimum-index lemma finishes independence.

6. For nonnegative odd ell, the unique smallest pair sum forces `u_0=-u_1`. The minimum-index lemma makes projection of the kernel to its first coordinate injective. This proves dimension at most one and opposite first two signs for every nonzero relation.

7. For nonnegative even ell, the all-ones rational sum is pole-free: partner residues cancel separately in every colliding pair, and there are no own-node poles. An individual rational summand has only simple pair poles, so cancellation of all residues removes them. Subtracting the first weight times the all-ones vector gives the hypothesis of the minimum-index lemma. Any kernel vector is constant. The full generalized Vandermonde is nonzero at sufficiently large positive L, which excludes every nonzero constant kernel vector.

8. Nonnegative-kernel exclusion follows immediately in all three cases. The proof applies to a single weighted column with every other column full. It does not establish stability under further masking, arbitrary sparse-graph noncancellation, or either answer to P versus NP.

## Executed corroboration

After reading the entire checker source, I independently reran:

    python check.py
    python -O check.py

Both completed successfully. The logs are `independent-check.log` and `independent-check-optimized.log`. The six deliberately selected cases include a genuine signed one-dimensional kernel, arbitrary background gaps, all-even independence, a distinguished exponent below the background minimum, a common shift, and a five-row case. They verify 40 individual pair-residue identities in total and exact coefficient-matrix ranks using raw symbolic cofactors. No floating-point numerical rank or optimized-away `assert` is used. These finite checks corroborate the proof; they do not replace any universal step.

The checker constructs rational quotients from the raw cofactors. Accordingly, its residue checks independently corroborate the parity identity but do not independently implement the Schur factorization. The latter was audited algebraically above.

## Certificate and cost boundary

For rational offsets, the factorization and residues are rational. The exact linear-alternative framework in the separate frozen nonnegative-column-kernel certificate package therefore supplies rational positive functionals for this theorem's families. The triangular-residue construction also extends directly to the nonnegative odd-ell branch, if an explicit formula is wanted. Coefficient expansion and the resulting certificates are polynomial in the numerical total degree and offset bit lengths; this is not a polynomial bound in the binary encoding length of arbitrarily large exponents.

## Review status

Mathematical result approved. The common column-order sign convention has been recorded and rechecked; no open correction remains from this review. No historical novelty assertion is assessed. This audit does not authorize a remote write, merge, release, or publication.
