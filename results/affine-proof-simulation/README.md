# Polynomial SF/EF upper simulation of the frozen certificate system

PROOF.md gives a mathematical proof-template construction translating accepted affine-residual UNSAT certificates into polynomial-size substitution-Frege proofs, followed by the established uniform extended-Frege simulation. The independent audit accepts the final proof hash. No executable SF/EF proof emitter is supplied.

The new construction closes the explicit normalization/interface obligation recorded in the historical MODEL_TRANSLATION.md snapshot. In particular, forward coordinate interfaces are projections; inverse assignment reconstruction may be affine. Safe pure-literal elimination is justified by clause deletion, never by claiming a pure assignment follows logically.

This is an upper simulation for a specific solver certificate system. It does not imply polynomial-size certificates, efficient proof search, an ordinary-resolution simulation, a lower bound, or P=NP. The SF/EF relationship and ordinary formula-caching comparisons are prior work, accurately cited in the proof and audit. No historical novelty or Lean certification is claimed.

Run:

    python audit_exact_tests.py

The packaged test was adapted only for relative paths and a mandatory frozen-source hash check, and rerun. It performs finite semantic regressions, not a proof-system verification. The separate executable residual-certificate verifier is in ../residual-certificates/.
