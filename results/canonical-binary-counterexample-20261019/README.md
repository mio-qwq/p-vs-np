# Canonical binary-cost cancellation: reproducible source checkpoint

This archive contains an exact counterexample to unrestricted canonical full-fiber nonvanishing on sparse bipartite graphs: 73 canonical row offsets and column exponents `0,...,72`, 83 allowed edges of costs 0 or 1, and eight target-cost-3 perfect matchings whose complete signed translated-power polynomial is identically zero. All 32 supported matchings are enumerated, with cost histogram `(1,4,7,8,7,4,1)`.

For the matrix with allowed entries `x^cost(i,j) (L+i)^j` and zero entries off support, `[x^3] det M(x,L)` vanishes identically. The exact check expands all 47 active coefficients, constructs the monic degree-2582 forced-edge factor, and verifies all 2629 full coefficients. The eight unsigned active terms are distinct and their actual global permutation signs split four positive/four negative.

## Scope and primary-source boundary

The support is disconnected: five K2,2 components and 63 isolated matching edges. It is not a brace. [Du v3, Theorem 1.2](https://arxiv.org/html/2604.01571v3#S1.SS2) restricts ASNC to bipartite braces. Remark 1.4 explicitly allows cancellation on non-brace graphs; Proposition 2.3 describes testing brace blocks separately and combining feasibility. This example therefore does not refute that brace-only theorem or establish failure of that blockwise algorithm. It refutes the stronger all-graphs nonvanishing assertion and a direct whole-graph zero test relying on that assertion.

The dense completion assigns cost 4 to absent edges and has alphabet `{0,1,4}`. It is not a complete-graph 0/1-cost counterexample. No P-versus-NP conclusion, minimum-dimension result, or formal proof-assistant verification is claimed. Historical novelty is unconfirmed; this checkpoint does not claim a literature-first result.

The public-source scope was checked against the versioned arXiv page on 2026-10-19. No theorem-history or comprehensive prior-art review is bundled.

## Files and replay

- `canonical-binary-cost-counterexample-20261019.zip`: 27 compact source, proof, certificate, receipt, and inventory files; no large dense matrix is needed.
- `VERIFICATION.json`: reproducibility and test receipt for this exact archive.
- `SHA256SUMS`: SHA-256 hashes for this README, verification receipt, and archive.

Extract the ZIP. Inside `canonical-binary-cost/`, run:

    python replay_all.py

This requires Python 3.10 or later and the standard library only. It verifies the inventory, reconstructs the instance independently, replays normal and optimized Python checks in temporary directories, compares certificates, and exercises mutation controls. For the optional supplementary symbolic review, with SymPy already installed, run:

    python replay_all.py --with-sympy

The archive records a successful integrated run including that supplementary review. Independent checks cover the rational identity, actual support/fiber enumeration, true global signs, exact integer coefficients, full-degree forced-factor expansion, supplied sparse-certificate validation, and public theorem scope. Mutations in rows, exponents, edge costs, permutation signs, support edges, and forbidden-edge completion are rejected.

`rebuild_zip.py` reproduces the archive with sorted members, stored bytes, fixed timestamps, and fixed permissions. Two builds were compared byte-for-byte, and the extracted archive was replayed independently. See the verification receipt for the exact result and hashes.

Prepared 2026-10-19 as research material. The contents do not execute uploads, repository writes, PR actions, merges, tags, or releases. Any external archiving or publication is a separate authorized operation.
