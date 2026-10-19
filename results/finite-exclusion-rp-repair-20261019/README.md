# Complete canonical five-row binary-fiber exclusion

Source-only recovery archive, 19 October 2026. This additive directory contains one original deterministic ZIP and three metadata files.

## Accepted scope and status

For the fixed canonical signed polynomial family at n=5, every nonempty complete fiber of every supported binary edge-cost matrix is noncancelling, at all targets 0 through 5. This is a restricted finite-model result; general n, arbitrary costs and P versus NP remain unresolved.

The accepted clean-extracted replay regenerates all 29,238,600 reduced extensions. All 20,575 Q(1)=0 survivors have nonzero Q(2); all 52,094 single-edge pruning witnesses are reconstructed. Primary and independent exact enumeration, full survivor multisets, coefficient reconstruction, symmetry transfers, normal/optimized Python and UBSan checks pass. Deliberately corrupted Q(2), complete-fiber membership, edge domains and payload bytes are rejected.

Independent audits are AI-assisted. No human peer review, proof-assistant verification, historical-originality claim, P-versus-NP solution or interacting Yang-Mills mass-gap proof is asserted.

## Recovery

1. Run `sha256sum -c SHA256SUMS` in this directory.
2. Extract `pnp-complete-binary-fiber-exclusion-20261019.zip` into a fresh directory and enter `pnp-complete-binary-fiber-exclusion-20261019`.
3. Read the included README, proof and audit documents. Run `python reproduce.py` or `python -O reproduce.py --ubsan`. The pinned prior endpoint-cut source ZIP and its original endpoint theorem are included and integrity-checked. Their full earlier enumeration was not newly rerun at this checkpoint; add `--replay-prior` to request it.

For a quick integrity-only check, run `python reproduce.py --integrity-only` or `python -O reproduce.py --integrity-only`.

Requires Python 3.10+ standard library and g++ with C++17; the --ubsan option requires undefined-behavior sanitizer support. The reproduction entry point places generated files and temporary executables in disposable directories. No dependency installation or numerical-solver run was performed by this archive operation.

Archive: 191,655 bytes. SHA-256: `4d3fe03930f644da9344a377af879188c89ec637aa6d4cd3fb4a43b759d8420d`.

## Verification and preservation

The frozen local checkpoint completed clean-extracted normal/optimized replays, negative controls and deterministic byte-identical archive rebuilds. This archive operation freshly verified every checkpoint-manifest file, ZIP SHA-256 and size, CRC, forbidden-path/cache/executable exclusion, and both normal/optimized integrity-only wrappers. VERIFICATION.json records these checks and supporting receipt hashes; it does not preclaim post-commit remote verification.

Original ZIP bytes and retained research sources are unchanged. Embedded local-only provenance statements refer to package construction before this source-branch commit. The exact pinned prior proof dependencies remain inside the ZIP for offline recovery. No expanded duplicate source tree, executable binary, large regenerable ledger or cache is added.

This operation adds a new source branch only. It creates no PR, merge, tag, release or release attachment. Any later research PR merge or external research release requires separate consolidated approval.
