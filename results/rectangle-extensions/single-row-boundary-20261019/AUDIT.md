# Audit status

The scoped theorem in PROOF.md was checked independently. No mathematical error was found. The independent audit verifies the full-polynomial mask reduction, deletion signs, exact first and second correction formulas, normalization of the exponent-variance coefficient, its strict positivity at resonance, and the strict degree comparisons.

The author checker uses exact integer polynomial arithmetic and signed permutations. All 40 cases pass both normally and with Python optimization; its checks raise exceptions explicitly and are not disabled by optimization.

The independent audit uses a separately written exact SymPy polynomial implementation. Its mathematical review and commands are documented in `independent/AUDIT.md`.

The parent review independently checked equations (8)–(14), including the calibration m=3, b=(0,2,4), k=1, giving α=1/4, β=3/4, v=1/4. The required noncentered exponent-resonance case is included in both checkers.

Two important limitations remain explicit:
- The simultaneous-resonance regime for general n≥5 is not proved nonvanishing.
- Exact examples with three and four cancelled top coefficients remain nonzero and are not strict counterexamples.

No remote writes, publication, or claims concerning arbitrary colorings or complexity lower bounds were made.
