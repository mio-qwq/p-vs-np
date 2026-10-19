# Column noncancellation and constructive-cost audits

19 October 2026. Research source bundle. Proofs, independent
AI-assisted audits and exact reproducible certificates are included. No P-versus-NP
solution, universal noncancellation theorem, historical novelty, human peer review,
or proof-assistant verification is claimed.

## Proven, within the stated hypotheses

- [Extreme-root theorem](resonant-column-structure-20261019/PROOF.md): closes the
  five-row two-hole simultaneous-resonance boundary and several rank patterns at
  every size. It concerns one distinguished column and an extreme masked row.
- [One missing degree](noncancellation-adversarial-20261019/KERNEL-THEOREM.md): a
  complete constant-kernel classification for the specified exponent family.
  Exceptional kernels are one-dimensional and mixed-sign, so nonempty
  nonnegative one-column masks cannot annihilate the determinant.
- [Same-parity background](parity-column-kernel-20261019/PROOF.md): arbitrary gaps
  are allowed among the other exponents. The constant kernel is either trivial
  or at most one-dimensional with both signs. Nonnegative one-column weights
  remain nonvanishing. The theorem assumes n>=3.
- [Explicit positive functional](even-background-column-kernel-20261019/PROOF.md):
  the narrower consecutive-even background supplies a constructive positive
  functional, repeated-pole coefficient certificates, and explicit degree/bit
  costs, together with sharpness examples. This special case is not counted as an
  additional general noncancellation theorem beyond the same-parity result.
- [Arithmetic-step background](cyclotomic-column-root-20261019/PROOF.md):
  for step m>=3, the finalized maximal-pole argument proves full complex
  linear independence under its exact staircase hypotheses. Arbitrary
  gaps within a residue class are outside this result.
- [Conditional exact algorithm](constructive-cost-audit-20261019/PROOF.md):
  universal binary-color ASNC at the fixed canonical parameters would yield an
  explicit deterministic decision/search procedure with a conservative
  O(n^10 log^2(n+2)) schoolbook bit bound. This universal hypothesis is unproved.
- [Representation and reduction limits](separation-reduction-audit-20261019/PROOF.md):
  an exact C6 witness invalidates independent count-only tight-cut convolution;
  weighted SUBSET-SUM and group-label bounds isolate encoding costs. The
  obstruction targets a specific graph-preserving linear compression template,
  not all reductions.
- [Per-instance certificates](nonnegative-column-kernel-cost-20261019/PROOF.md):
  rational coefficient-matrix alternatives give either a nonnegative kernel or
  a strictly positive functional. Formation is polynomial in explicit total
  degree, and may be pseudopolynomial in binary-encoded exponents.

## Exact limits and finite evidence

The [six-row boundary note](n6-boundary-root-limit-20261019/PROOF.md) shows an
extreme-root evaluation can vanish while its full polynomial has degree 15.
The [third-correction note](n6-third-correction-obstruction-20261019/PROOF.md)
gives an exact vanishing third correction; it is not a zero-polynomial example.
These are method limits, not counterexamples to general noncancellation.

The C++ supplement checks all 2^25 canonical complete K5 binary colorings via
2^24 complement representatives. The saved result reports no zero nonempty
fiber among 50,208 evaluation-zero candidates. This finite search is not a
proof at arbitrary size, and is not an independent second implementation.
No compiled executable or cache is distributed.

## Open scope

Arbitrary exponent families, several independently masked columns, arbitrary
sparse supports/colorings, general U-ASNC, a uniform NP-complete-to-solved-class
reduction, and the remaining six-row resonance cases are not settled here.
One-column results cannot simply be iterated after other columns are masked.
Prior-art comparisons are qualified in the included review; no novelty claim
is made. Original source documents retain their historical scope statements;
this README gives the consolidated scope of the assembled bundle.

## Reproduce

From this directory, Python 3.10 or later:

    python -B verify.py
    python -B -O verify.py

Default mode uses the standard library and reports symbolic scripts as NOT_RUN.
For every included symbolic checker, use SymPy 1.14.0:

    python -m pip install -r requirements.txt
    python -B verify.py --full
    python -B -O verify.py --full

To freshly rerun the finite K5 supplement with an available g++ compiler:

    python -B verify.py --full --exhaustive

The aggregate checks the complete inventory and provenance, recomputes saved
certificates in temporary copies, and rejects package and selected mathematical
corruptions. It never changes this frozen directory or contacts the network.
Normal and optimized modes retain all validations for these Python checkers.
A passing finite checker corroborates its accompanying proof; it does not
machine-verify the all-size proof or asymptotic complexity argument.

## Provenance and dependencies

PROVENANCE.json maps every selected original to its SHA-256-preserved packaged
copy and records omissions. DEPENDENCIES.json locates earlier proofs stored
once under dependencies/. Historical inventories are renamed SOURCE_* and are
not the aggregate inventory. manifest.json and SHA256SUMS describe the actual
bundle. Source receipts distinguish directly checked sources from limited
source access. No raw upstream paper, nested archive, executable or cache is
included. This bundle is additive under results/column-kernels-and-cost-audits/;
no previously frozen material is replaced.
