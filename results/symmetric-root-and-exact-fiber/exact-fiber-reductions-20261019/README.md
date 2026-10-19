# Exact-fiber completeness reduction

Local result dated 19 October 2026.

## Files

- `PROOF.md`: self-contained dummy-selector reduction, reverse oracle reduction, size bounds, deterministic subcases, and scope boundaries.
- `check.py`: independent finite checks of actual expanded graphs, the explicit solution bijection, exhaustive compressed 3-by-3 instances, prefix queries, and maximum-degree-two counting.
- `results.json`: deterministic checker result.

The independent audit is maintained separately in `../exact-fiber-reduction-audit-20261019/`. An unchanged checker copy under `partner-check/` is used only for cross-replay and is not a dependency of the primary checker.

## Reproduce

Requirements: Python 3 standard library only. No third-party packages, network, credentials, repositories, or remote services are used.

    python check.py
    python -O check.py

Both commands were run and passed with identical results:

- 1,272 actual expanded-graph instances, including degenerate and out-of-range inputs
- 45,332 actual expanded perfect matchings enumerated
- 78,732 exhaustive compressed 3-by-3 target checks
- 28,357 maximum-degree-two capped coefficient distributions
- 81 explicit-family prefix checks

The independent proof review also checked the minimum/maximum target argument and degree-two dynamic program without finding a material defect. Finite tests support implementation correctness; the universal reduction and algorithmic claims rely on the mathematical proofs.

## Scope

The graph is supplied independently of the listed family. This is fixed-color verification, not binary-color synthesis, and not a promise that the graph equals the union of the listed matchings. The proved lower reduction is BEM to incompleteness; the reverse is a polynomial-time Turing reduction. No NP-hardness, P-versus-NP separation, ASNC theorem, or unconditional general deterministic Exact Matching algorithm is claimed.
