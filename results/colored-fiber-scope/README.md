# Colored-fiber scope: affine layers and support masks

Research checkpoint, 18 October 2026.

## Principal result

A seven-permutation family on K4,4 is a complete integer-cost equality layer and hence is affine-closed within the permutation configuration. It is not an exact-count fiber of any binary-colored graph on the same labeled vertices. Its union uses all 16 edges, so a graph restriction cannot change this conclusion. The proof reduces binary representability to four pairwise-distinct row differences, which is impossible because binary row differences have only three values.

The family's polynomial is nonzero:

    P(lambda) = lambda^6 + 14 lambda^5 + 64 lambda^4
                + 129 lambda^3 + 130 lambda^2 + 86 lambda + 42.

For a finite rational point configuration, affine-closed nonempty families are exactly integer affine equality layers. This characterization does not impose binary coefficients. The example therefore invalidates the identification of affine-closed families with binary exact-count fibers used in the domain discussion of Remark 2.9 of [arXiv:2604.01571v3](https://arxiv.org/html/2604.01571v3#S2.SS4). It does not disprove a possible equivalence established by some additional, presently absent reduction.

## Contents

- [Affine-layer theorem, seven-permutation obstruction, and source limitations](affine-layer/REPORT.md)
- [Independent affine proof review](affine-layer/REVIEW.md)
- [Support-mask criterion, minimal examples, and nonempty fractional slice](support-mask/REPORT.md)
- [Extremal-fiber transfer by assignment duality](extremal-transfer/RESULT.md)
- [Cross-review and transfer boundary](extremal-transfer/REVIEW.md)
- [Input provenance](PROVENANCE.json), [source manifest](manifest.json), and [fresh verification](verification.json)

The support-mask result and the binary-cost obstruction address different questions. A fixed-color-count fiber need not be the full perfect-matching family of any support mask; the diagonal-red K3,3 target-one fiber is the smallest-order obstruction. Extremal fibers do admit the support-mask transfer. The component-size-at-most-four nonvanishing corollary depends on the previously [audited determinant theorem](https://github.com/mio-qwq/p-vs-np/blob/94d094d82d14e15729cac0b478d0d6f1bec33de9/results/monic-four-general/PROOF.md).

## Reproduction

Python 3.9 or later; standard library only. No solver, network, or additional package is required. From the repository root or extracted archive:

    python3 results/colored-fiber-scope/verify.py
    python3 -O results/colored-fiber-scope/verify.py

Each invocation checks the exact file inventory, sizes, manifest and SHA256SUMS, then runs the three supplied mathematical checkers in clean temporary storage under the current interpreter mode. It reproduces the frozen affine outputs, support certificates, and extremal counts; rejects a deliberately altered integer certificate; and exercises modified-file, missing-file, unexpected-file, and altered-manifest controls. Optimized execution does not disable checks. The distributed files remain unchanged.

The affine checker examines all 65,536 binary matrices on K4,4: exactly 174 are constant on the seven selected permutations, and every one admits an additional matching at that cost. The short structural proof is primary; this bounded representability check is not an ASNC polynomial-nonvanishing search.

`manifest.json` hashes every payload file except itself and `SHA256SUMS`; `SHA256SUMS` hashes the payload and manifest. Their finite self-exclusion is deliberate. These hashes detect inconsistent or damaged contents; they are not a signature or independent authenticity guarantee.

## Scope and status

The arguments have undergone AI-assisted mathematical checking and exact integer/rational verification. There is no claim of human peer review, Lean or other proof-assistant verification, historical novelty, an ASNC counterexample, a general ASNC theorem, or a P-versus-NP conclusion. The seven-permutation example is explicitly nonzero. The source's unspecified n=5 zero-sum family is not independently certified here.

This package is an additive research checkpoint under `results/colored-fiber-scope/`, based on the dependency commit 94d094d82d14e15729cac0b478d0d6f1bec33de9. It contains no replacement for any earlier result or shared repository index. Publication and remote-branch status are separate from this local verification.
