# Fiber/angular source archive checkpoint

Source-only additive research snapshot, 19 October 2026. Existing repository
files and earlier archive bytes are preserved. No release, merge, tag or PR is
part of this checkpoint. Historical statements inside unchanged source ZIPs
about their local-only status describe the time they were prepared, not the
current location of this copy. Original local paths in provenance manifests
are historical identifiers; the portable commands below use only included files.

## Scoped results

- Canonical binary cancellation: minimum eight-term relation at n=5, affine
  obstruction to being a complete edge-cost fiber, exact sweeps of all 2^25
  canonical 5x5 support determinants and full K5,5 binary colorings, checks of
  every subset/coloring of its 15-edge union, and a self-contained n<=4 check.
  Arbitrary intermediate sparse colored supports are not exhausted.
- Union-support normalization: explicit fixed-color-fiber verification reduction,
  with full encoding and actual path-expanded graph checks. Converse reduction
  is Turing, not a claimed two-way many-one equivalence or NP-hardness result.
- Canonical continuation: unique eight-term relation, affine non-fiber obstruction
  and cardinality lower bound ten for a nonempty cancelling complete real-cost
  fiber with n=5 offsets and exponents 0,1,2,3,4. Historical k=1/k=2 timeouts prove no infeasibility.
- Endpoint continuation: any such complete fiber needs at least three columns
  in each endpoint row, with the stated endpoint-gap restrictions. This is a
  necessary condition, not a full sparse-fiber classification.

The fixed-size exact model exports in the earlier continuation ZIP are retained
because independent audits consume them without importing solver code. No new
solver run, strengthened-model snapshot, numerical search cache, compiled binary,
or large regenerable polynomial table is included. The known-singleton prior
proof is retained once inside the union-support archive as its necessary prior
dependency. New archive bytes are not also duplicated as expanded source files.

Requires Python 3.10+, standard library, and GNU-compatible g++ with C++17 and
UBSan support. The largest regenerable scratch array uses about 288 MiB.
Neither P=NP nor P!=NP is proved, and no general sparse-fiber noncancellation
claim is made.

## Extracted proof map

Each ZIP extracts to the directory of the same name without .zip:

- pnp-canonical-binary-cancellation-20261019/binary-cancellation-search-20261019/PROOF.md
  and binary-cancellation-audit-20261019/PROOF.md; minimum-dimension check in
  canonical-dimension-check/PROOF.md within that archive.
- pnp-union-support-normalization-20261019/union-support-verifier-20261019/PROOF.md
  and union-support-verifier-audit-20261019/AUDIT.md; cited prior proof in
  exact-fiber-reductions-20261019/PROOF.md within that archive.
- pnp-continuation-20261019/sparse-fiber-one-audit-20261019/PROOF_AND_AUDIT.md.
  The neighboring sparse-fiber-one/two modules record stopped MILP attempts;
  their terminal receipts are checked as history, never treated as infeasibility
  certificates, and the reproduction wrapper launches no solver.
- endpoint-continuation-20261019/PROOF.md and audit/AUDIT.md, with its retained
  ENDPOINT_CERTIFICATE.json and independent exact endpoint certificates.

## Reproduce and verify integrity

From this directory, run:

    python verify_archives.py
    python -O verify_archives.py

The wrapper verifies this directory's manifest, all ZIP hashes, safe member paths,
CRC, sorted paths and fixed metadata, clean-extracts each source archive, checks
its internal SHA256SUMS, and runs every entrypoint under both ordinary Python and
-O. Source trees are checked again afterward and temporary copies are discarded.
Inner wrappers replay exact certificates, the indicated C++ exhaustive checks,
and negative controls. The stored REPRODUCTION.json is the fresh clean-extraction
receipt from preparing this snapshot. No network or solver is used.

SHA256SUMS covers every other file in this directory. ARCHIVES.json records exact
sizes, hashes, entrypoints and the pinned single parent. Finite computation and
AI-assisted reviews complement written arguments; neither human peer review,
historical originality nor proof-assistant formal verification is claimed.
