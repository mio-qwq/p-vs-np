# Six saved seeds: rank-at-most-12 completion obstruction

Source-only research archive, 19 October 2026.

## Accepted result and limits

For the six saved 24-term polynomial-zero permutation subsets, every cancelling
complete additive-cost fiber containing any one of them has augmented incidence
rank at least 13, equivalently affine dimension at least 12. The result covers
arbitrary real additive costs and sparse support because complete fibers are
incidence-closed. It is conditioned on these six seeds only.

Each seed has a 32-member rank-10 closure. Exhausting every rank-at-most-12 closed
extension gives 70,758 states per seed, 424,548 seed-relative states in total,
with no size cutoff and no zero full polynomial. All 16 scalar-evaluation-zero
survivors have nonzero full polynomials. The state count is not globally deduplicated.
The independent exact-rational/integer audit obtains the same mathematical results.

Unrestricted n=6 remains open. This does not enumerate all zero subsets, exclude
higher-rank repairs, provide a global six-row bound, or separate P from NP.
Structured-cost search negatives are bounded exploration, not an extra theorem.

## Reproduce

Check the three payload files with `sha256sum -c SHA256SUMS`, then extract the ZIP.
From the extracted package directory, with Python 3, SymPy and a C++17 `g++` with
signed 128-bit arithmetic and UBSan already installed:

    python -B reproduce.py --integrity-only
    python -B reproduce.py --output /tmp/pnp-sixseed-fresh-replay
    python -B test_package.py
    python -O -B test_package.py
    python -B test_audit_controls.py
    python -B build_archive.py /tmp/pnp-sixseed-rebuilt.zip

The replay output directory must not already exist. The full replay runs the primary
checker at -O0, -O3 and with UBSan, its verification and four mutation controls in
normal and optimized Python, and the independent audit in both Python modes.
The archive includes complete source checkers and compact exact certificates;
omitted binaries and structured ledgers are regenerated and checked. The package
has 43 integrity corruption controls per Python mode and six independent-audit
controls. Rebuild identity is toolchain-specific, with fixed timestamps and ordering.
No network is needed after the stated runtimes are installed.

Read the package README, PROOF.md, AUDIT.md and additive pin reconciliation for full
proofs, provenance, replay details and historical manifest limitations. Original
source files and historical manifests are preserved without changes.

## Verification and archival status

VERIFICATION.json includes the frozen clean-extraction replay receipt, with hashes
of the original test receipts. Its `checkpoint_verification.remote_changes: false`
describes the checkpoint before this additive source archival operation.
This directory adds exactly the original ZIP, this README, SHA256SUMS and
VERIFICATION.json to the specified preceding research commit. It creates no PR,
merge, tag or release. No existing archive is overwritten. These are AI-assisted
finite mathematics and executable regression checks, not external peer review or
proof-assistant formalization.
