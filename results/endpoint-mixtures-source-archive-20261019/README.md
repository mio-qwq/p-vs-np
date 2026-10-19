# Exact canonical binary endpoint cuts

Source-only recovery archive, 19 October 2026. This directory adds one frozen, deterministic ZIP and its verification metadata. All pre-existing repository paths remain outside this addition.

## Accepted scope

For nonempty cancelling complete canonical n=5 binary-cost fibers at targets 1, 2, 3, and 4, both endpoint rows must use at least three columns, include column 1, and include at least one of columns 0 and 2. Exactly 10 endpoint support patterns remain. This is a necessary-condition result; existence among the remaining sparse fibers is unresolved.

Remaining canonical sparse binary-fiber cases remain unresolved. No P-versus-NP or Yang-Mills solution, historical originality, human peer review, or formal verification is claimed. Yang-Mills-side conclusions are restricted scalar Gaussian covariance obstructions, not an interacting Yang-Mills construction or mass-gap result.

## Recovery

1. Run `sha256sum -c SHA256SUMS` in this directory.
2. Extract `pnp-binary-endpoint-cuts-20261019.zip` into a fresh directory and enter `pnp-binary-endpoint-cuts-20261019`.
3. Read its README, proof and audit files; run `python reproduce.py` or `python -O reproduce.py`. For a quick source-integrity check, use `python -O reproduce.py --integrity-only`.

Requires Python 3.10+ standard library and g++ with C++17 and UBSan support. Reproduction writes generated data and temporary executables only into disposable temporary directories. No dependency installation was performed by this archival operation.

Archive: 129,683 bytes; SHA-256 `a7bedd2d4a260045d1a7fba0b5b3ce03f0079d55c4052a6385735817c86d5c9b`.

## Verified checkpoint and limits

The accepted replay checks 3,455,136 primary assignments, 207,360 independent gap assignments, and the independent C++ minimum-two enumeration of 3,247,776 assignments. The 4,657 exceptional assignments are checked, including 4,645 minimum-two survivor coefficient replays; the L2 survivor count is zero. Normal/optimized Python and normal/UBSan C++ outputs agree. The exact prior endpoint theorem archive is included and 263 used root-slice memberships are pinned; full prior enumeration was not rerun by default. Use --replay-prior to rerun that dependency.

Both clean outer-mode replays passed, exact deterministic ZIP rebuilds matched, and manifest tampering was rejected in normal and optimized modes. VERIFICATION.json records the completed local checkpoint and supporting receipt hashes. This receipt does not claim a remote read-back that has not yet happened at commit creation time.

The embedded package retains its original local-only provenance statements: those describe its construction before this source-branch archival commit. Source files and ZIP bytes are unchanged. No expanded duplicate source tree, cache, executable checker, large regenerable rejection ledger, or release attachment is added here. Exact necessary certificates and pinned prior source dependencies are retained.

This archival operation creates no PR, merge, tag or research release. Any later research PR merge or external research release requires separate consolidated approval.
