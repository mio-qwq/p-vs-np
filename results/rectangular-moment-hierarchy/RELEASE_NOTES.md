# Rectangular moment hierarchy research checkpoint

- Proves the first-differing-moment coefficient and candidate degree for red rectangles with `n=2r+2`, `|I|=r`, `|J|=r+1`.
- Proves that all smaller Laplace layers vanish above the stated bound, so they cannot invalidate the candidate coefficient.
- Establishes exact fiber degree and nonvanishing whenever the offset factor is nonzero, including all strictly separated row-offset blocks.
- Gives `q_l=(r+1)^l/l!` for standard consecutive rows, and the corresponding power-sum leading coefficient.
- Records additional cancellation for arbitrary distinct offsets, with complete irrational and integer degree-7 examples whose fibers remain nonzero.
- Includes an independent mathematical audit, 15 complete determinant reconstructions, seven producer examples, 90 affine closed-form checks, and source-level negative controls.
- Preserves the audited proof and all five checker files byte-for-byte. The aggregate verifier reruns everything under ordinary and optimized Python without third-party dependencies.

Scope: one structured rectangular family. No arbitrary-coloring theorem, ASNC resolution or counterexample, P-versus-NP result, novelty claim, human peer review, or formal proof-assistant verification.

This checkpoint is additive under `results/rectangular-moment-hierarchy/`; it does not replace earlier research artifacts.
