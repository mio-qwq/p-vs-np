# Canonical n=5 real-cost complete-fiber checkpoint

This additive source archive contains the accepted finite real-cost result and its independently implemented audit. It is a source-branch checkpoint, not a release.

## Result and strict scope

For every bipartite support on five labelled rows and columns, every nonempty complete fiber of an arbitrary real additive edge cost has a nonzero canonical polynomial sum sum_p sign(p) product_i (L+i)^p(i), with offsets and exponents exactly 0,1,2,3,4. Completeness is essential. No arbitrary-dimension or unrestricted P-versus-NP conclusion is claimed.

The package includes the accepted proof, independent audit, two source-only C++17 checker implementations, exact manifests, compact certificates, negative controls, and a deterministic archive builder. AI-assisted independent checks are not external peer review or proof-assistant formalization.

## Verify and reproduce

- Archive: pnp-real-cost-n5-20261019.zip
- Bytes: 122387
- SHA-256: dbfe978d15f1721e8b239000bc7ff3f7424787e1b596a825e2a879841896cfbb
- Requirements: Python 3.10+, C++17 g++ with 128-bit integers. No network, downloaded packages, or external solver is needed.

First run `sha256sum -c SHA256SUMS`, then extract the ZIP and read its README.md. From the extracted package directory, use a new output directory outside the package:

    python -B reproduce.py --output ../pnp-clean-replay
    python -B -O reproduce.py --optimized --output ../pnp-optimized-replay
    python -B reproduce.py --sanitize --output ../pnp-sanitized-replay

The acceptance record reports ordinary, optimized, and undefined-behavior-sanitizer replay for both implementations. All 571 root memberships and 1949 core memberships/ranks agree; each uncapped traversal visits 177379 states and finds zero cancelling complete fibers. All 13 deterministic evidence outputs agree across modes; packaging and mathematical negative controls pass. Read the packaged proof and audit for the logical argument and boundary of these finite checks.

## Provenance and archival boundary

VERIFICATION.json is an unchanged copy of the pre-archive package-acceptance receipt. Its remote_changes=false and merge_or_release_performed=false fields describe packaging, before this separate additive source commit. This directory adds only this README, that receipt, the unchanged ZIP, and SHA256SUMS. The manifest covers the other three files.

Existing source paths, branches, main, tags, release assets, and historical receipts are preserved. This archival operation does not create a PR, merge, tag, or release. A research merge or release requires separate batch approval.
