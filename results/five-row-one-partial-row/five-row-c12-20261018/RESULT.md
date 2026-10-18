# Five-row one-partial-row milestone

18 October 2026.

The one-partial-row subclass is proved: a binary 5-by-5 mask with four full rows and one nonempty row, distinct real offsets, and distinct nonnegative integer exponents has a nonzero translated-power determinant.

The proof extends the previously audited coefficient-6 through coefficient-10 reduction with exact coefficient-12 identities. Eliminating the offset-shape parameter gives two quadratic equations in the integer exponent product `T`. The retained-pair branch forces `d<23` and `d=1 mod 4`; the complementary-triple branch forces `d<25` and `d` odd. Every remaining quadratic has negative or nonsquare discriminant, excluding all integer `T`.

Files:

- `PROOF.md`: complete theorem and mathematical proof, including signed-exponent normalization, all row support sizes, real-offset constraints, every division, exact coefficient identities, uniform gap bounds and finite exhaustive discriminant tables.
- `verify.py`: standalone exact symbolic reconstruction and certificate checker; 69 checks pass in ordinary and optimized Python.
- `verification.json`, `verification_optimized.json`: exact receipts and discriminant tables.
- `verify.log`, `verify_optimized.log`: successful run logs.
- `negative_control.log`: deliberate coefficient corruption fails as required.
- `coefficients.json`, `elimination.json`: early exact coefficient and resultant records.
- `explore.py`, `eliminate.py`: exploratory derivations retained for provenance; the final checker does not import them.

The independent audit is complete and passes: `../five-row-c12-audit-20261018/AUDIT.md`. It uses a different coefficient algorithm (double Cauchy–Binet expansion and Schur polynomials) and independently checks the earlier reduction, the elimination, bounds, finite tables and final theorem text. Its checkers are `audit_c12.py`, `audit_complement.py` and `audit_reduction.py`, with normal and optimized receipts and deliberate-failure tests.

This theorem does not settle arbitrary five-row masks or the general colored problem. It is a mathematical proof with computer-algebra certificates, not a formal proof-assistant verification. No remote writes were made.
