# Exact parity cost for every number of variables

For every m>=2 the minimum binary AND count is exactly 2m-3 in finite monotone cyclic circuits with both supplied input polarities, free ORs/constants and least-fixed-point semantics. Equivalently, unrestricted semifilter pair-cover cost is 2m-3. The one-bit cost is zero.

EXACT_PROOF.md gives a complete gate-elimination proof. The critical strengthening is an OR-minor obstruction at a unique two-literal AND bottleneck; it removes the even-arity gap of the earlier recurrence. The general lower proof does not require exhaustive four-bit enumeration.

The precise cover correspondence is in ../parity-recurrence/model-linkage.md; the explicit upper construction and its tests are in ../parity-recurrence/. The independently verified four-bit certificate remains in ../parity4-cover/ as a separate consistency check.

stronger-or-minor-audit.md accepts the exact proof hash. This is independent AI-assisted mathematical review, not human peer review or a Lean certificate. Finite tests are regression checks, not a substitute for the proof.

Historical novelty remains unverified. PRIOR_ART_EXACT.md records close classical gate-elimination precedents, including Wegener (1991), as well as unresolved literature checks. The cover/cyclic characterization is prior work of Cavalar–Oliveira, adapting Nakayama–Maruoka. No new general characterization or first-discovery claim is made.

This theorem concerns parity, which has linear-size circuits. It does not prove P!=NP or a superpolynomial circuit lower bound.

Reproduce the new checks with Python3 standard library:

    python check_opposite_bottleneck.py
    python check_bottleneck_minor.py
    python negative_control.py

Also rerun the preceding normalization and upper-bound checks in ../parity-recurrence/.
