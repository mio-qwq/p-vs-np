# Symmetric simple roots and explicit binary-fiber verification

Research-source follow-up, 19 October 2026. This package contains two separate mathematical results, their exact checkers, and independent mathematical audits. It makes no P-versus-NP, historical-novelty, formal-verification, external-human-peer-review, or hosted-CI claim.

## 1. All-degree symmetric proper-power obstruction

For every nondegenerate symmetric real random variable with a log-concave density and every even N >= 2, its translated Nth-moment polynomial has a simple pair of purely imaginary roots. More generally, the proved coefficient lemma assumes positive factorial-weighted coefficients forming a log-concave sequence. The proof is degree-uniform, using exact normalization and alternating-term bounds; finite checker examples are regression tests only.

Consequently, for every nonconstant symmetric real offset multiset, the translated complete homogeneous polynomial has a simple root and cannot be a proper polynomial power in any positive degree. Repeated offsets are allowed for this conclusion. The odd-degree argument also works without symmetry.

Together with the previously audited ODE reduction, this excludes constant full-column cofactor kernels for distinct symmetric offsets and exactly the one-outlier background

    h, h+1, ..., h+n-3, h+n-2+d.

It does not settle arbitrary asymmetric offsets in general even degree, arbitrary gapped backgrounds, or simplicity of every root.

Sources:

- `general-moment-barrier-20261019/PROOF.md`: full proof and exact one-outlier corollary.
- `general-moment-barrier-20261019/INDEPENDENT_AUDIT_AND_BRIDGE.md`: independently checked normalization, both truncation parities, root bounds, simplex transfer, and ODE bridge. This is byte-identical to the audit's original companion file.
- `general-moment-next-20261019/TAIL_AUDIT.md`: optional independent rational-tail proof.
- `general-moment-barrier-20261019/check.py`, `certificate.json`, and `check.log`: exact identities, 15 regression cases, scope counterexample, and original normal/optimized receipts.

The primary analytic input is Klartag and Lehec, [Poisson processes and a log-concave Bernstein theorem](https://www.math.tau.ac.il/~klartagb/papers/log_concave_bernstein.pdf), Lemma 2.1, equation (6), manuscript page 4. Simplex marginal log-concavity is also an analytic input.

The ODE implication uses earlier work already present at the baseline commit. Original source files retain their local provenance references; these immutable repository links resolve the referenced dependencies:

- [One-outlier cofactor proof](https://github.com/mio-qwq/p-vs-np/blob/906627d1d7fa1e40a66660787bfd57b70ba8e9fd/results/column-closure-mixed-background/mixed-column-positivity-20261019/PROOF.md)
- [Independent ODE audit](https://github.com/mio-qwq/p-vs-np/blob/906627d1d7fa1e40a66660787bfd57b70ba8e9fd/results/column-closure-mixed-background/mixed-background-ode-audit-20261019/AUDIT.md)

These prior proofs are mathematical dependencies of the corollary; no external source code is needed to run this package's checkers.

## 2. Exact Matching and supplied-color completeness

For a separately supplied arbitrary simple bipartite supergraph, a supplied binary coloring, a target count, and a nonempty explicit matching family F:

- Bipartite Exact Matching has a deterministic polynomial-time many-one reduction to finding an unlisted target matching, even when F has one explicitly known member.
- The constructed target fiber is in explicit bijection with one known dummy plus the original Exact Matching solutions. All graph edges are binary colored, and the exact graph-size formulas are polynomial.
- Explicit-list completeness and the existence of an extra target matching have deterministic polynomial-time Turing reductions to bipartite Exact Matching via first-departure prefix queries. The converse is not claimed as a many-one reduction.
- Global minimum/maximum targets and graphs of maximum degree two have direct deterministic verification algorithms.

This is fixed-color verification. It does not establish a synthesis lower bound: singleton synthesis is easy. It also does not apply to the additional promise that the supplied graph equals union(F); the singleton reduction deliberately uses edges outside the listed matching. No NP-hardness or complexity-class separation follows. The audit records dated primary-source claims about Exact Matching without declaring its October 2026 bipartite deterministic status settled or still open.

Sources:

- `exact-fiber-reductions-20261019/PROOF.md`, `check.py`, and `results.json`.
- `exact-fiber-reduction-audit-20261019/AUDIT.md`, `audit_check.py`, and `audit_results.json`.

The independent audit checker imports no partner implementation. Its graph enumerator checks the entire cost histogram, exact graph sizes, the known dummy, and all nonempty matching subfamilies for every binary coloring of K3,3.

## Reproduce

Tested with Python 3.12.14, SymPy 1.14.0, and mpmath 1.3.0. Python 3.10 or later is recommended. Only the symmetric-root checker needs SymPy; both graph checkers use the Python standard library. `requirements.txt` records the tested external dependency versions. No repository checkout, network access, external local paths, or downloaded data is required once those dependencies are installed.

From this directory:

    python -B verify_sources.py
    python -B verify_sources.py --run-checks
    python -B -O verify_sources.py --run-checks

The verification wrapper checks the complete file set, byte counts, SHA-256 hashes, and checksum-file coverage. With `--run-checks` it executes every canonical checker in both normal and optimized Python and verifies that every frozen byte remains unchanged. Checks use explicit exceptions rather than removable assertions. Checker-generated JSON receipts must reproduce the archived bytes exactly.

`LOCAL_VERIFICATION.json` records the package replay. `PACKAGE_MANIFEST.json` identifies all archived files except itself and `SHA256SUMS`; `SHA256SUMS` covers every other file including the manifest. An externally supplied archive digest is needed to authenticate the whole archive. Scratch searches, caches, bytecode, and environment files are excluded.

## Integration boundary

Prepared as an additive source-only directory `results/symmetric-root-and-exact-fiber` in `mio-qwq/p-vs-np`, based on research commit `906627d1d7fa1e40a66660787bfd57b70ba8e9fd`. The observed main commit was `b2c2926b69ee2ce9f2a357b4eb2911b434545dd2`. Package preparation itself performs no remote writes, merges, tags, or releases. Any later remote action requires its own authorized workflow and fresh baseline verification.
