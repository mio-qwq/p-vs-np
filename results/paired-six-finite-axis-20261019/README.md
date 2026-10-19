# Restricted paired-six-row noncancellation checkpoint

This additive source-branch checkpoint preserves the accepted proof, independently written proof and checker, and reproducible source package.

## Result and strict scope

For canonical n=6 with row pairs (0,5), (1,4), and (2,3), BOTH pair-equal costs and pair-invariant support are required. Costs may be arbitrary real numbers. Every nonempty complete supported cost fiber has a nonzero canonical signed permutation polynomial, with offsets and exponents 0,1,2,3,4,5. Unrestricted n=6 remains open. No P-versus-NP separation is claimed.

The primary exhaustive traversal visits 818 states; a differently implemented independent traversal visits 2,049. Both find zero polynomial-zero states. The package preserves the original pending-status receipts byte for byte and resolves them in FINAL_ACCEPTANCE.json. Original independent n=8 center-mask material is retained only as secondary historical content, outside this package's accepted claims.

## Verify and reproduce

- Archive: pnp-restricted-paired-six-row-noncancellation-20261019.zip
- Bytes: 100610
- SHA-256: 67b76a5153910684b840034e9efc0548efb9b4db92ea4e713a987cbece6de0a8
- Requirements: Python 3.10+ standard library and g++ with C++17, __uint128_t, and UBSan support. Tested with Python 3.12.14 and GCC 14.2.0. No network or external solver is needed.

Run `sha256sum -c SHA256SUMS`, extract the ZIP, and read its README.md. From the extracted package directory:

    python reproduce.py --integrity-only
    python reproduce.py
    python -O reproduce.py
    python reproduce.py --sanitize
    python test_package.py
    python -O test_package.py

The accepted clean normal/optimized/UBSan replays regenerate all mathematical tables and match the pinned deterministic outputs. Five primary mathematical negative controls, six independent zero-triple controls, and twelve package-corruption controls pass. Repeated builds and clean-extraction rebuilds are byte-identical. UBSan covers the primary C++ traversal; the independent audit uses Python arbitrary-precision integers.

## Provenance and archive boundary

VERIFICATION.json is the unchanged pre-archive checkpoint acceptance summary. Its remote_changes=false field describes the earlier local packaging stage. This directory adds exactly four files: the unchanged ZIP, this README, that summary, and SHA256SUMS covering the other three files. The work is AI-assisted research; passing checks is not external human peer review or proof-assistant formalization.

Existing archives, files, branches, main, tags, release assets, and PR state are preserved. This operation creates no PR, merge, tag, or release. A research merge or release requires separate batch approval.
