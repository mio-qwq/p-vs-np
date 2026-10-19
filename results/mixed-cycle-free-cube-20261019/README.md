# Mixed-cycle real-offset counterexample

Source-only research archive, 19 October 2026.

## Established result

For some pairwise distinct real algebraic row offsets a_i, a 16-by-16 matrix with entries `(L+a_i)^j X^{c_ij}`, with column exponents exactly `j=0,...,15` and nonnegative integer costs `c_ij`, has a nonempty complete cost-2 permutation fiber whose signed polynomial is identically zero. There are exactly six permutations in that fiber.

The supported graph has four disjoint alternating cycles on 6, 3, 3 and 3 rows, plus one forced edge. Its local flip signs are (-1,+1,+1,+1), with positive cost differences (1,1,1,1). All unsupported edges cost 100. Nonnegative costs exclude every unsupported edge from the target-2 fiber.

This refutes the extension to four mixed-parity cycles in the model allowing arbitrary distinct real offsets. It does not address the original prescribed row offsets a_i=i, which remain open. It is not a P-versus-NP result, a general classification, or proof-assistant formalization.

## Start here

- `independent16row/AUDIT.md`: standalone proof and precise 16-row instance, including positive row offsets a_i=3-rho_i.
- `independent16row/cost_matrix.json`: actual 16-by-16 cost matrix; row order is the order in AUDIT.md, and column index is exponent j.
- `independent16row/complete_fiber.json`: all six permutations; entry p[i] is row i's column/exponent, with zero-based indexing.
- `independent16row/parameter_polynomial.txt`: the exact degree-51 integer polynomial specifying the parameter.
- `primary/COUNTEREXAMPLE.md`: original 15-active-row proof and its consecutive-column 16-row extension.
- `primary/CERTIFICATE.json`: exact rational interval endpoints, normalized polynomial coefficients, and modular/Sturm verification receipt.
- `VALIDATION.json`: clean normal and optimized replays, independent matching checks, common-parameter cross-check, and rejected fault injections.

The primary proof uses a different harmless ordering of plus/minus root pairs and first explains a 15-row version with nonconsecutive columns. Do not pair its 15-row permutations with the independent 16-row matrix. For the explicit complete 16-row example, use the independent proof, matrix and six permutations together.

Both proofs specify the same algebraic parameter: the primary isolating interval lies strictly inside the independent interval, each isolates one root, and the defining polynomials agree after monic normalization. The symbols r (primary) and s (independent) denote the same simple root of the cubic. The independent positive offsets amount to the variable translation t=L+3.

## Exactness and completeness

The proofs use rational Sturm root counting, exact rational polynomial identities and coefficient reduction modulo the degree-51 parameter polynomial. All denominators are checked invertible. Rational interval arithmetic establishes positivity and separates all row roots; display decimals are not assumptions.

The supplied cycle exponent orders realize the divisor multiplicities by actual single permutation cycles. The identity

    r2*r3 + r2*r4 + r3*r4 - r1*r2 - r1*r3 - r1*r4 = 0

then clears to the original signed matching polynomial. Direct backtracking on the supplied cost matrix finds 16 supported perfect matchings, with cost histogram 1,4,6,4,1 at costs 0,1,2,3,4. The independent bundle checker also verifies actual permutation signs relative to the baseline permutation.

## Reproduce

Requires Python 3.9 or newer and SymPy. Tested with Python 3.12.14 and SymPy 1.14.0; the pinned mathematical dependency is in `requirements.txt`.

From this extracted directory:

    python verify_bundle.py --negative-controls --output /tmp/pnp-validation.json
    python -O verify_bundle.py --negative-controls --output /tmp/pnp-validation-optimized.json

The bundle verifier works in disposable directories. It checks fresh certificate/matrix/fiber bytes against the supplied files, runs both underlying exact verifiers normally and under `-O`, checks the shared algebraic parameter, and independently checks the serialized cost fiber. Negative controls alter algebra, the isolating interval, a B-edge cost and a permutation, in both execution modes. It also corrupts the serialized cost matrix and serialized permutations directly. Each must fail at its intended mathematical validation.

For the authors' original independent mutation harness:

    cd independent16row
    python verify_negative_controls.py

That command rewrites the identical `NEGATIVE_CONTROLS.json` receipt. Both mathematical verifiers use explicit exceptions, so `python -O` does not disable their checks. Normal/optimized author receipts are retained as provenance, although their contents are identical.

## Integrity and deterministic rebuilding

`MANIFEST.json` lists every packaged file except itself with SHA-256 and byte size. The two source subdirectories retain their frozen source manifests/checksums. Exploratory probes, caches and redundant console logs are excluded.

After extraction, rebuild to a path outside this directory:

    python rebuild_archive.py /tmp/pnp-mixed-cycle-real-offset-counterexample-20261019.zip

The rebuild first verifies all manifest hashes, then uses sorted entries, fixed timestamps, fixed file permissions and uncompressed ZIP storage. Consequently the archive is byte-deterministic without depending on compression-library versions. The external `PNP_COMPLETE.json` receipt records the final archive hash and the verified identical rebuild.

The package was prepared locally before the additive source archival commit.

## Additive source archive verification

This directory contains exactly the original ZIP, README.md, SHA256SUMS and
VERIFICATION.json. Check the outer SHA256SUMS before extraction. All source file
paths discussed above refer to paths inside the ZIP. VERIFICATION.json records
the frozen checkpoint, fresh clean full replay in normal and optimized Python,
byte-identical deterministic rebuilding, and agreement with an additional root
replay of the primary certificate. No prior source or archive is replaced.
No PR, merge, tag or release is created by this source archival operation.
Local-only provenance in the frozen package describes preparation before this
commit. Hash pins detect changes and are not authenticity signatures.
