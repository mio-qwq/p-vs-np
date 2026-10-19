# All-degree symmetric proper-power obstruction

This local research package proves that every positive even polynomial whose factorial-weighted coefficients are log-concave has a simple imaginary root. It follows that every even symmetric log-concave moment polynomial has a simple imaginary pair and cannot be a proper polynomial power.

For nonconstant symmetric real offset multisets, translated complete homogeneous polynomials therefore have no proper-power representation in any positive degree. The exact one-outlier background h,h+1,...,h+n-3,h+n-2+d consequently has no constant full-column cofactor kernel for distinct symmetric real offsets and every allowed distinguished exponent.

- PROOF.md: full degree-uniform elementary proof, moment transfer, simplex consequence, precise ODE bridge, and scope warning.
- INDEPENDENT_AUDIT_AND_BRIDGE.md: separate audit and exact bridge review.
- check.py: exact universal pair identities and regression checks; uses no removable Python assertions.
- certificate.json: exact checker receipt.
- SHA256SUMS: integrity hashes.

Run python check.py and python -O check.py. The proof is analytic and algebraic, not a finite-degree computation. Arbitrary asymmetric even-degree offsets remain outside the new theorem. No novelty or complexity-class separation claim is made. No remote changes were made.
