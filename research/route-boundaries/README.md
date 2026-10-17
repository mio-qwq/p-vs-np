# Boundaries of the next P-versus-NP routes

The exact parity benchmark is closed in results/parity-exact. These notes prevent two invalid extensions of that result.

- CANONICAL_GAP.md: the explicitly defined minimal generator-upset witnesses have cost1 for even parity, while the unrestricted cost is2m-3. Thus no universal constant-factor comparison holds for this witness class. This is not asserted to refute an identified published conjecture.
- ROUTE_AUDIT.md: a uniform polynomial-time constructor of complete polynomial-size wiring for SAT on standard formula-encoding bits would suffice for P=NP, but is not constructed here. Nonuniform small covers imply only a nonuniform circuit conclusion. A small cover for evaluating one formula on assignments does not perform existential search.

Both documents have independent AI-assisted audits, not peer review. The route audit required and now includes polynomial-overhead SAT encoding. No new SAT algorithm or P-versus-NP separation is claimed.

Actual Python3 checks:

    python check_canonical_gap.py
    python check_projection.py

The minimal counterexample to premature existential projection is (x) AND (NOT x). The general claims are proved in the notes; finite enumeration is corroboration. Historical novelty of the canonical-gap corollary is unverified.
