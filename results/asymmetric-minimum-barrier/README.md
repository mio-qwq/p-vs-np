# Minimum-centering barrier and a restricted recovery condition

Research-source supplement, 19 October 2026. This small package contains only the asymmetric minimum-centering counterexample and its exact rational certificate. The previously archived all-degree symmetric result is not duplicated or modified.

## Result and limits

The uniform-simplex projection on 100 distinct rational knots supplies a degree-six moment polynomial whose unique real minimizer fails normalized even-moment log-concavity. The proof isolates that minimizer in a rational interval and proves strict negativity of the relevant polynomial throughout the interval. This refutes one attempted extension of the symmetric coefficient argument.

The final section gives a sufficient coefficient-tail condition for a simple conjugate pair via Rouché's theorem. Its geometric-tail constants are checked exactly. These coefficient assumptions are not asserted for every asymmetric real-knot projection. This is not a proper-power counterexample; degree six already satisfies the previously proved no-proper-power result. No unrestricted asymmetric theorem, kernel counterexample, novelty, or P-versus-NP claim is made.

## Contents

- `general-moment-next-20261019/ASYMMETRIC_MINIMUM_BARRIER.md`: exact counterexample and optional quantitative recovery condition.
- `general-moment-next-20261019/check_asymmetric_barrier.py`: independent exact moment constructions, derivative identities, root isolation, rational interval signs, independent root counts, and recovery-bound arithmetic.
- `general-moment-next-20261019/asymmetric_barrier_certificate.json`: complete rational certificate, reproduced byte-for-byte by the checker.

## Reproduce

Tested with Python 3.12.14, SymPy 1.14.0, and mpmath 1.3.0. Python 3.10 or later is recommended. `requirements.txt` records the tested dependency versions. With dependencies installed, no network, repository checkout, or external file is needed.

    python -B verify_sources.py
    python -B verify_sources.py --run-checks
    python -B -O verify_sources.py --run-checks

The wrapper validates the complete file set and hashes. Each checker is replayed in normal and optimized Python; all checks use explicit exceptions and remain active under `-O`. Frozen output bytes and expected standard output are compared after each run. `LOCAL_VERIFICATION.json` records the initial local replay. These checks verify finite identities and certificate arithmetic, not every analytic theorem or a formal proof.

`PACKAGE_MANIFEST.json` lists every file except itself and `SHA256SUMS`; `SHA256SUMS` covers every file except itself. An external archive digest authenticates the entire package. Caches, searches, unrelated audits, and scratch files are excluded.

## Integration boundary

Prepared locally for the new additive directory `results/asymmetric-minimum-barrier` in `mio-qwq/p-vs-np`. The baseline is recorded separately in the prepared commit inputs after the earlier symmetric-source archival commit is verified. This package performs no remote writes, main changes, PR operations, tags, or releases. A later integration requires its own authorization and fresh baseline checks.
