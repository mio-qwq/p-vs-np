# Rational-family obstruction and canonical embedding

Local source-only research checkpoint, 19 October 2026.

## Results and limits

1. primary/PROOF.md excludes rational a,k,d in the specified reflected quadratic
   three-source family when its fourth quotient must be one genuine matching cycle
   with distinct real row roots and distinct integer column exponents. Both cubic
   branches and all possible common-factor cancellations are covered. This rules
   out all-rational rows and their affine rationalizations within that family.
2. primary/CANONICAL_EMBEDDING.md gives an existence-preserving affine scaling and
   forced-edge padding from any rational-offset nonempty zero COMPLETE cost fiber
   to consecutive offsets and exponents in some larger dimension. It preserves the
   whole fiber; padding can be enormous. It supplies no counterexample and no
   polynomial-size reduction.

General rational/canonical full-fiber cancellation remains open. No P-versus-NP
separation, complexity lower bound, or solution is claimed.

## Evidence included

- primary/: full proofs, recovery conditions, author checkers and one frozen
  certificate per checker. The obstruction checker executes 48 explicit checks,
  including five internal rejection controls. Embedding examples have dimensions
  4 and 10 and include negative source costs and both indexing conventions.
- audit/: independent proofs, reconstructed polynomial coefficients and padding
  checker. The elimination uses an independently coded integer Bareiss Sylvester
  determinant at 121 distinct integers against degree bound 120. It does not read
  the author certificate as an input. The bundle additionally compares both full
  reconstructed coefficient lists with the author certificate.
- review/ROOT_REVIEW.md: dated root review of both research directions.

The obstruction and padding arguments are self-contained. Earlier real-example
archives are historical context, not prerequisites for either proof, so their
large redundant contents are not included. The independent padding examples verify
nonzero identities and full-fiber preservation; they are not zero counterexamples.

Recovery in the family requires identifying an exact failure in the cycle bound,
parametrization, discriminant/resultant, or finite-field certificate. A new search
may instead change the reflected-source hypothesis, divisor patterns, or cycle
structure. Merely larger first-cycle exponents, factor cancellation, or an affine
shift cannot evade this theorem. See primary/DEAD_ENDS_AND_RECOVERY.md.

## Offline verification and deterministic rebuilding

The archive contains UTF-8 source, proofs, exact JSON certificates and verification
scripts only. It contains no nested archives, cached environments, binaries or bytecode.
Use Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0 for the frozen byte-exact replay.
Dependencies are pinned in requirements.txt; they are not vendored or automatically installed.
The runtime used is recorded in RUNTIME.json. Only Python's standard library and
SymPy/mpmath are needed; no network access is used by the scripts.

From the extracted package directory:

    python -I -B verify_bundle.py
    python -I -B -O verify_bundle.py
    python -I -B rebuild_archive.py ../rebuilt.zip

The verifier checks every file hash and the exact inventory, copies each checker to
a clean temporary directory, and runs every positive replay in BOTH normal and -O
mode. Each generated certificate must equal its frozen JSON byte for byte. It also
checks scientific negative controls and deliberate inventory corruptions. Python
assert statements are not used for verification. No frozen source is modified.
The expected aggregate output is EXPECTED_REPLAY.json. Different software versions
can legitimately change textual symbolic output, so a mismatch requires review.

The rebuild uses lexicographically sorted paths, a fixed 2026-10-19 00:00:00 ZIP
timestamp, fixed Unix regular-file mode 0644 and DEFLATE level 9. Byte-identical
rebuilds were verified after fresh extraction with the recorded Python/zlib runtime.
Output must be outside the extracted package. MANIFEST.json inventories all files
except itself and SHA256SUMS; SHA256SUMS additionally pins MANIFEST.json. The outer
completion manifest pins the ZIP and the internal manifest. Hashes detect altered
bytes; they are not authenticity signatures or mathematical proofs.

## Provenance and recovery

SOURCE_PINS.json maps exact copied files to their frozen local research sources.
The root-review note is an earlier dated snapshot; its then-pending freeze language
is historical. This completed package supplies the later verification evidence.
References in preserved reports to their original sibling folders are provenance;
the bundled mapping below identifies the included dependencies. Optimized duplicate
certificates, caches and exploratory scratch probes are intentionally omitted.

If a hash, exact replay, negative-control rejection or deterministic rebuild fails,
retain the failing evidence and suspend the affected claim/package. Restore the
pinned source snapshot or investigate the discrepancy before issuing a replacement.
Do not treat near-zero numerical output as an exact certificate. These checks are
computer-assisted exact algebra/enumeration, not proof-assistant certification or
external peer review. This local checkpoint performs no external publication.

## Outer payload

This directory contains exactly the original source ZIP, this README.md,
VERIFICATION.json and SHA256SUMS. Check the outer hashes before extracting.
VERIFICATION.json records clean exact normal/optimized replays, rejection tests,
root-certificate agreement and byte-identical deterministic rebuilds.
This is the frozen local payload; preparation alone does not publish or merge it.
