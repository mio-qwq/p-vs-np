# Pair-state unrolling

The pinned complexitylib2 pair-state compiler stabilizes after k simultaneous pair rounds under pointwise set semantics. DAG unrolling uses at most k² charged AND gates and polynomial total size. Literal-source SAT slices have polynomial pair-cover size exactly when SAT belongs to P/poly. This supplies no lower bound or P-versus-NP separation.

See PROOF.md and REVIEW.md. The source-specific corollary has written proof and separate AI-assisted review, but no Lean formalization or historical-priority claim. The generic finite monotone-iteration principle is standard. Topology selection from arbitrary sets remains noncomputable.

Run with Python 3 standard library:

    python check_pair_state_unrolling.py
    python check_pointwise_unrolling.py

The first enumerates the special update maps and seeded cases; the second independently enumerates all small monotone Boolean networks. The proof handles arbitrary dimension and infinite carriers; finite checks do not replace it.
