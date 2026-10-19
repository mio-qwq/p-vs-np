# Degree-eight powers and restricted binary matching fibers

19 October 2026. A compact source-only research follow-up. The source manuscripts and independent review receipts are preserved byte for byte in their original named directories.

## Results and boundaries

1. For every n >= 2 and every nonconstant real offset multiset, the translated complete homogeneous polynomial h_8(L+a_1,...,L+a_n) is not a proper polynomial power over C, even up to a nonzero scalar. The primary proof reconstructs knot moments and uses eleven universal exact rational positivity certificates after n=v+2. It does not claim squarefreeness or exclude all proper powers at arbitrary degrees.
2. A separate symmetric log-concave moment argument excludes proper-power bases of degrees two, four, and six. Its hypotheses and degree corollaries are stated in SYMMETRIC_LOW_BASE.md. It invokes an established normalized-moment theorem and is not covered by the H_8 computer certificate.
3. Complete binary matching fibers have a deterministic polynomial algorithm on the distinguishing-vertex class, even with unbounded cycle rank. After pruning unusable edges, an effective-cycle-rank algorithm is polynomial for each fixed rank k; its dependence is XP, not an FPT bound.
4. The complexity audit distinguishes explicit and succinct family representations. It gives coNP/coRP verification and MA synthesis upper bounds for explicit families, a coNP-hardness result only for succinct families, and a polynomial-bit large-radix construction of the affine-closure fiber with integer weights. That construction does not decide equality with the requested family and does not yield binary weights.

None of these results establishes a complexity-class separation, a general deterministic binary-fiber synthesis algorithm, or a general noncancellation theorem. No publication novelty or external human peer review is claimed.

## Reading order

- quartic-power-20261019/PROOF.md: primary universal H_8 proof
- quartic-power-20261019/SYMMETRIC_LOW_BASE.md: separate symmetric supplement
- quartic-power-20261019/AUDIT.md: copy of the final universal audit receipt, retained because the primary proof refers to it
- quartic-power-audit-20261019/AUDIT_UNIVERSAL.md: independent reconstruction review
- quartic-power-audit-20261019/PROOF.md: independently derived finite/large-n backup proof
- binary-fiber-algorithm-20261019/PROOF.md: restricted-class algorithms and full bit-cost account
- binary-fiber-complexity-audit-20261019/AUDIT.md and REVIEW.md: representation-sensitive bounds and reciprocal review

The universal audit imports its own sibling check.py, so both that checker and its generated backup certificate are intentionally included. Scratch searches, duplicate replay directories, bytecode, and unrelated prior packages are excluded.

## Reproduction

Use Python 3.9 or later; the checked environment used Python 3.12.14 and SymPy 1.14.0. The matching checkers need only the standard library. The symbolic H_8 checkers need SymPy. Dependencies are not bundled or installed automatically.

From this package directory run:

    python verify_sources.py
    python verify_sources.py --run-checks

The second command runs all five listed checkers under both ordinary and optimized Python, then rechecks every package byte. Generated certificates and results must reproduce exactly. Every substantive check uses explicit failure logic that remains active with -O. LOCAL_VERIFICATION.json records local results; these are not hosted CI or formal proof verification. The universal mathematical claims rely on the accompanying proofs, not on finite regression tests.

## Provenance

This is an additive follow-up to the source-only structural-power-and-fiber archive at commit 1a05e45cbacec7f67fc7e72fcf1d61a33e991151 of mio-qwq/p-vs-np. Prior papers named in the audit remain in that earlier archive. Absolute source paths in immutable manuscripts are historical provenance; the same final component directory and filenames are retained here where included. Package creation itself changes no repository, PR, merge, tag, or release.
