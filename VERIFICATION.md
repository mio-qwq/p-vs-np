# Checkpoint verification

Date: 2026-10-17 UTC. Environment: Python 3.12.14, standard library.

Actually executed successfully from the packaged result directories:

- affine-residual/check_arb.py
- affine-residual/check_resource_edges.py
- affine-residual/check_marker_family.py
- affine-residual/run_growth.py
- affine-residual/run_controls.py
- pair-state-unrolling/check_pair_state_unrolling.py
- pair-state-unrolling/check_pointwise_unrolling.py

All exited zero. Adjacent logs and JSON record results. The solver SHA matches the independently reviewed frozen source. Negative controls cover damaged parity, clause-chain and Gaussian logic. These computations do not prove general asymptotic claims; the supplied mathematical proofs state exact hypotheses and limits. Separate reviews are AI-assisted, not human peer review.

## Additional repaired-candidate and witness checkpoint

Packaged commands actually rerun with exit zero: affine-residual-pc/checker/check_arb_pc.py, check_repairs.py, check_family_invariants.py, check_growth.py; affine-residual-pc/design/run_experiments.py; radial-witness-obstruction/verify_certificates.py, verify_parity3.py, verify_radial_attack.py. Solver SHA is unchanged from independent review. Five faulty implementation mutants are rejected; exact rational certificates and mixture checks pass. Timing fields are not reproducibility invariants. New algorithm results remain candidate-specific, and witness results refute the proposed restricted strategy only.
