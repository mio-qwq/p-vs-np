# Exact cover certificates and a failed radial witness strategy

Parity on three bits has unrestricted pair-cover number exactly 3. For parity on m=2^r bits, one fixed list of r pairs defeats every above-target radial weighted-threshold semifilter. This refutes the proposed radial witness strategy, not unrestricted cover complexity or a public P-versus-NP conjecture.

See PROOF.md and separate AI-assisted REVIEW.md. No priority or human-review claim. Python3 standard-library reproduction:

    python verify_certificates.py
    python verify_parity3.py
    python verify_radial_attack.py

The exploratory floating-point LP is not required or included; exact rational certificates are reconstructed by the checkers. The all-dimension assertion uses the supplied syndrome proof, not numerical extrapolation.
