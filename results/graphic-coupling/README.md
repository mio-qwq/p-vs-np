# Graphic coupling with local quota constraints

A bounded constructive research checkpoint for binary linear systems with local restrictions. **No general SAT algorithm, P versus NP resolution, or historical novelty is claimed.**

## Results and implementation boundary

- [Graphic parity and incident pairs](base/RESULT.md): an explicit perfect-matching reduction with witness extraction. Arbitrary remote disjoint pairs remain NP-complete. The [distance-two construction](base/DISTANCE_TWO.md) proves that weakening incidence to line-graph distance at most two is already NP-complete; it does not preserve a two-vertex target or series-parallel geometry.
- [Local partition upper quotas](quota/RESULT.md): a polynomial-size matching gadget, implemented with the bundled [standard Edmonds backend](blossom/README.md). Groups must be disjoint at each host vertex; an edge can have separate endpoint constraints. This is an implementation of known matching machinery, not a new general matching algorithm.
- [Pair-sum representation criterion and target transport](pair/RESULT.md): appended pair-sum columns force simultaneous incidence in a graphic representation. Original targets are transported by solving Az=b and using Bz, justified by equal labeled binary kernels.
- [Common-star group criterion](star/RESULT.md): distinct directions in each group must be independent, and the full pair-sum extension must be graphic. Parallel variables remain separate for quota counting. The triangle negative control demonstrates why independence is essential.

**The executed certificate and star solvers verify a supplied graph representation. They do not implement automatic general graphic recognition.** Classical constructive graphic recognition gives the theorem-level discovery step; the exhaustive GL(3,2) routines are only finite validation oracles. Invalid structural certificates are rejected as outside the class, not as certificates that the original instance is unsatisfiable. Recognition-only appended columns are never selectable variables.

The current star integration requires globally disjoint quota groups and preprocessed zero columns. It handles upper quotas only. The separate laminar extension and unrelated extra-parity work are excluded from this checkpoint. The prototypes are intended for the stated mathematical input domain, not as hardened adversarial-input services.

## Direct prior art

The local incident-pair polynomial case is already a direct corollary of Cannon, Ishaque and Tóth, [Conflict-free graph orientations with parity constraints (2012)](https://arxiv.org/abs/1203.3256): subdivide each edge, impose even indegree at its midpoint, and interpret midpoint indegree zero as selection. The exact mapping is explained in quota/RESULT.md and audit-local/RESULT.md. The independently written gadget and tests are an adaptation, not a new tractability discovery.

General matching uses Edmonds' established method. Constructive binary graphic recognition uses established graph-realization results such as Bixby–Wagner (1988), after polynomial Gaussian normalization; Seymour's recognition theorem is discussed in audit-pair/RESULT.md. No automatic recognizer is included here, and no almost-linear bound is asserted for the full explicit-matrix pipeline.

## Reproduce

Python 3, standard library only, from this directory:

    python run_checks.py

This runs all 13 packaged test commands, including the independent auditors' programs. Each program can also be run separately. JSON outputs are written beside their tests; CHECK_OUTPUT.txt is the actual full preparation run. Exponential matching/search and small-rank enumeration occur only in bounded validation programs, not in the quota/certificate solver pipeline.

## Evidence and provenance

See VERIFICATION.md, SOURCE_PROVENANCE.json, audit-local/RESULT.md, audit-pair/RESULT.md and audit-star/RESULT.md. The last audit is explicitly excerpted to omit its separate laminar discussion. The base report is labeled as a historical first-stage snapshot because it predates the implemented backend and direct prior-art clarification. AI-assisted review and finite tests are not human peer review or formal proof verification.
