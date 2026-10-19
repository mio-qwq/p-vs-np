# Structural power obstructions and matching-fiber boundaries

Source-only research snapshot, 19 October 2026. This package records restricted mathematical results and their limits. It makes no novelty, human peer-review, proof-assistant verification, general noncancellation, or P-versus-NP claim.

## Precisely scoped results

- `general-power-obstruction-20261019/PROOF.md`: for at least two nonconstant real offsets and every integer s >= 2, the translated complete homogeneous polynomial h_(2s) is not a scalar multiple of an s-th power of a quadratic. This excludes every proper power when the half-degree is prime. Bases of degree at least four remain untreated in the residual cases.
- `power-kernel-bridge-audit-20261019/RESULT.md`: for n >= 3 distinct real offsets, every root of H_d has multiplicity less than n-1; nonreal root multiplicity is at most floor(n/2). The prime-(n-1) independence corollary concerns the existing one-gap cofactor/ODE family. The stronger nonreal bound does not supply an additional independence family. The shifted-power span criterion is necessary and sufficient, not a universal exclusion claim.
- `translated-power-root-analysis-20261019/ROOT_GEOMETRY.md`: a unit-circle hypothesis on an integer-knot barycentric shift symbol gives all-degree squarefreeness on a vertical line. Arithmetic grids and grids with their center deleted satisfy it. Arbitrary real or lattice offsets do not automatically satisfy the hypothesis.
- `translated-power-root-analysis-20261019/EVENTUAL_SIMPLE_ROOT.md`: for each fixed distinct real offset tuple, every sufficiently high degree has a simple root. The explicit Rouché threshold depends on the geometry of that tuple. This leaves finitely many even degrees for each fixed tuple; it is neither a uniform-in-offsets threshold nor a proof of all remaining finite cases.
- `power-obstruction-limits-20261019/`: exact algebraic repeated-root and rational off-axis examples refute stronger root-location routes. They retain simple roots and are not proper-power or kernel counterexamples. The positive compact atomic-measure example is not a simplex-projection example.
- `binary-matching-relations-20261019/`: the 24 canonical four-row signed matching polynomials have no nonempty binary zero subset. An algebraic substitution extends this to equally spaced offsets and consecutive nonnegative exponents. Arbitrary unequal gaps, arbitrary exponent lists, and larger n remain outside the result. The independent audit covers canonical n <= 4. These bounded results are explicitly not general progress.
- `matching-fiber-geometry-20261019/`: affine closure characterizes complete real/rational/integer/nonnegative-integer edge-cost fibers. Binary edge costs require a separate condition. The two endpoint matchings in r disjoint K2,2 blocks form a binary-cost fiber exactly when r <= 3. This is a geometric separation, not a polynomial-cancellation example or a polynomial-time algorithm.

## Dependency and provenance map

The one-gap ODE reduction is already archived in the same repository at
[`results/column-closure-mixed-background/mixed-column-positivity-20261019/PROOF.md`](https://github.com/mio-qwq/p-vs-np/blob/c1f59339bc3fb6b1f9a5f81ad659a2c50d5d93d9/results/column-closure-mixed-background/mixed-column-positivity-20261019/PROOF.md).
All other columns remain full in that reduction; no arbitrary-background conclusion follows.

Frozen research files retain their original creation-time status and local provenance paths verbatim. A reference ending in one of the seven bundled directory names resolves to that sibling directory here. Optional preliminary root derivations, exploratory scripts, duplicate run outputs, and caches are omitted; the polished proofs and independent audits are included. Historical statements that work was local refer to when those notes were written.

Primary attribution remains in `ROOT_GEOMETRY.md`, including the author manuscripts https://arxiv.org/abs/1901.06398 and https://arxiv.org/abs/2001.01658 and their publication DOIs. No upstream papers or copied binary files are bundled. This archival pass checks preservation of those citations; it does not assert a new literature-priority review.

## Reproduction and integrity

Run `python verify_sources.py` to verify package byte counts and SHA-256 hashes. Run `python verify_sources.py --run-checks` to additionally run all eight checkers under normal and optimized Python. SymPy is needed by four algebraic checkers; the other four use the standard library. The observed environment was Python 3.12.14 and SymPy 1.14.0; `LOCAL_VERIFICATION.json` records the actual versions and sixteen local runs.

The checkers were inspected before execution, use explicit exceptions rather than removable assertions, and leave frozen certificate bytes unchanged. Finite checks support identities and bounded certificates; universal claims rely on the accompanying mathematical arguments. The Rouché argument is an analytic proof, not a numerically verified all-degree assertion. No hosted CI result is claimed.

`PACKAGE_MANIFEST.json` records every payload file except itself. `SHA256SUMS` records the payload and the manifest, excluding itself. The manifest distinguishes frozen research from package metadata. No existing repository source or released archive needs to be overwritten to add this package.
