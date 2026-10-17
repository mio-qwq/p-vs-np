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
