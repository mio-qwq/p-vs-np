# Exact unrestricted pair-cover cost of parity on four bits

**The cost is exactly 5** for the stated semifilter model with both literal polarities. This is a finite computer-assisted result, not a P-versus-NP separation or historical-priority claim.

The upper bound is an explicit five-AND construction. The lower certificate gives 120 explicit valid semifilters, recomputes every possible pair, and excludes every four-cover by exhaustive exact search. Three different algorithms agree: ordered search, full compatible-four-clique enumeration, and rarest-uncovered-witness branching. No floating-point optimizer or discovery history is trusted.

Read PROOF.md and the separate AI-assisted REVIEW.md. Run Python3 standard-library checks:

    python verify_dual.py
    python check_frozen_four.py
    python check_four_cliques.py
    python independent_verify.py
    python verify_upper5.py
    python negative_tests.py

The frozen witness JSON is unchanged from review. Packaged imports and file paths were made relative; the ordered checker now exits unsuccessfully if its explicit resource deadline is hit or a four-cover is found. All packaged versions were actually rerun. Timing fields may vary. No Lean/kernel verification or human peer review is claimed. The general fusion framework and quadratic bound are prior work cited in PROOF.md.
