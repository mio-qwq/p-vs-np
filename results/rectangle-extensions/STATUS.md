# Status and boundaries

The three included proofs have independent AI-assisted mathematical audits.
No human peer-review, proof-assistant or historical-novelty claim is made.

- General rectangle: all q>=1, r>=1, n>=2r+q; unconditional fiber nonvanishing
  requires separated row-offset blocks. The arbitrary-offset coefficient
  identity does not settle later coefficients when its row factor vanishes.
- Rectangle plus one disjoint red entry: proved in the slack range and at the
  tight boundary for r>=2, with the same separated-row hypothesis.
- One-row tight boundary: the exact D/D-1/D-2 tests and stated all-size
  corollaries are proved. Simultaneous resonance for n>=5 remains unresolved.
  Nonzero examples losing several leading terms do not settle that regime.

The earlier equal-halves moment package is a separate immutable checkpoint.
This bundle does not rewrite it or include later exploratory extensions.

All six source checker scripts are unchanged. Default verification reruns the
four standard-library scripts. Full mode additionally runs the two SymPy
scripts and compares the complete stress certificate. The general proof audit
explicitly did not execute the q=3 checker; the packaging verification runs
that checker separately and does not attribute that execution to the audit.

No arbitrary-coloring, general ASNC, P-versus-NP or complexity result is claimed.
